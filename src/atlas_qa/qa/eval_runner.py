"""Atlas-local evaluation harness for Session 06.

Reads the gold question set and evaluates the answer pipeline against each
question. Records per-question results and computes launch-gate metrics.

Design:
- All evaluation state is deterministic and serializable.
- The answer function is injectable — pass a custom answer_fn to run_eval()
  to use a mock pipeline (e.g. for testing). The default answer_fn calls the
  real Atlas QA pipeline.
- Launch-gate thresholds are encoded here per the gold question set §5.
- Outputs are written to data/atlas_qa/eval/ as timestamped JSON artifacts.

Usage:
    from atlas_qa.qa.eval_runner import load_gold_questions, run_eval, run_launch_subset

    # Full gold question set eval (requires real corpus + LLM):
    questions = load_gold_questions()
    summary = run_eval(questions)

    # Launch subset only (20 questions):
    summary = run_launch_subset()
"""
from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from atlas_qa.qa.types import (
    AbstentionState,
    ClassGateResult,
    EvalCaseResult,
    EvalExpectedBehavior,
    EvalRunSummary,
    GoldQuestion,
    LaunchGateSummary,
    QueryClass,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).parents[3]
_GOLD_QUESTION_SET_PATH = (
    _REPO_ROOT / "_internal" / "atlas_qa" / "QA_GOLD_QUESTION_SET.md"
)
_EVAL_OUTPUT_DIR = _REPO_ROOT / "data" / "atlas_qa" / "eval"

# ---------------------------------------------------------------------------
# Launch-gate thresholds (from gold question set §5)
# ---------------------------------------------------------------------------

_CLASS_THRESHOLDS: dict[QueryClass, float] = {
    QueryClass.A: 0.95,
    QueryClass.B: 0.85,
    QueryClass.C: 0.85,
    QueryClass.D: 0.80,
    QueryClass.E: 0.90,
    QueryClass.F: 0.98,
    QueryClass.G: 1.00,
}

# The 20 question IDs that form the recommended launch-gate subset (gold §5).
_LAUNCH_SUBSET_IDS: frozenset[str] = frozenset({
    "A-001", "A-002", "A-005",
    "B-016", "B-019", "B-020",
    "C-038", "C-041", "C-044",
    "D-054", "D-060",
    "E-066", "E-067",
    "F-076", "F-079", "F-087",
    "G-091", "G-092", "G-094", "G-095",
})


# ---------------------------------------------------------------------------
# Gold question set parsing
# ---------------------------------------------------------------------------


def load_gold_questions(path: Path | None = None) -> list[GoldQuestion]:
    """Parse the gold question set markdown and return all GoldQuestion objects.

    Reads all class sections (A–G) from the markdown table. Questions in
    the launch subset are flagged with is_launch_subset=True.
    """
    source = path or _GOLD_QUESTION_SET_PATH
    text = source.read_text(encoding="utf-8")
    return _parse_gold_questions(text)


def _parse_gold_questions(text: str) -> list[GoldQuestion]:
    """Parse markdown table rows from the gold question set text."""
    questions: list[GoldQuestion] = []

    # Match table rows: | id | query | class | behavior | entity_type | scope | vsens | notes |
    # We look for rows where the first cell matches a question ID pattern like A-001, D-054, etc.
    row_re = re.compile(
        r"^\|\s*([A-G]-\d{3})\s*\|\s*(.*?)\s*\|\s*([A-G])\s*\|\s*(answer|abstain|clarify)\s*"
        r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*([YN])\s*\|\s*(.*?)\s*\|",
        re.MULTILINE,
    )

    for m in row_re.finditer(text):
        question_id = m.group(1).strip()
        query = m.group(2).strip()
        query_class_str = m.group(3).strip()
        behavior_str = m.group(4).strip()
        entity_type_label = m.group(5).strip()
        source_scope_label = m.group(6).strip()
        v_sens = m.group(7).strip() == "Y"
        notes = m.group(8).strip()

        try:
            qc = QueryClass(query_class_str)
            behavior = EvalExpectedBehavior(behavior_str)
        except ValueError:
            continue  # skip malformed rows

        questions.append(GoldQuestion(
            question_id=question_id,
            query=query,
            query_class=qc,
            expected_behavior=behavior,
            entity_type_label=entity_type_label,
            source_scope_label=source_scope_label,
            version_sensitive=v_sens,
            notes=notes,
            is_launch_subset=(question_id in _LAUNCH_SUBSET_IDS),
        ))

    return questions


# ---------------------------------------------------------------------------
# Default answer function (real pipeline)
# ---------------------------------------------------------------------------


def _default_answer_fn(question: GoldQuestion) -> EvalCaseResult:
    """Call the real Atlas QA pipeline and map the response to an EvalCaseResult.

    This function wires compare routing, exact lookup, fuzzy retrieval, and
    the answer orchestrator. It maps all abstention states to their eval
    behavior category.
    """
    from atlas_qa.qa.compare import detect_compare_intent, answer_compare
    from atlas_qa.qa.coordinator import coordinate
    from atlas_qa.qa.answer import answer_from_retrieval, answer_from_exact
    from atlas_qa.qa.retrieval import retrieve
    from atlas_qa.qa.types import (
        EntityType as ET,
        SectionScope,
    )

    raw_query = question.query
    actual_behavior = "error"
    citation_present: bool | None = None
    version_disclosed: bool | None = None
    anomaly_disclosure_present: bool | None = None
    failure_reason: str | None = None
    diagnostics: dict = {}

    try:
        # --- Compare path (Class D) ---
        if detect_compare_intent(raw_query):
            from atlas_qa.qa.router import route as _route, RouteClass
            decision = _route(raw_query.strip().upper())
            entity_code = decision.candidate_codes[0] if decision.candidate_codes else None

            if entity_code is None:
                actual_behavior = "abstain"
                failure_reason = "no entity code detected for compare query"
            else:
                # Determine entity type from partition
                _, exact_resp = coordinate(raw_query)
                entity_type = ET.PROGRAM
                if exact_resp and exact_resp.answer:
                    entity_type = exact_resp.answer.entity_type

                result = answer_compare(raw_query, entity_code, entity_type)
                if result.abstention is not None:
                    actual_behavior = _map_abstention(result.abstention)
                    failure_reason = result.abstention.value
                    diagnostics = result.diagnostics
                else:
                    actual_behavior = "answer"
                    citation_present = (
                        result.postcheck.citation_ids_present if result.postcheck else None
                    )
                    version_disclosed = (
                        result.postcheck.from_version_named and result.postcheck.to_version_named
                        if result.postcheck else None
                    )
                    anomaly_disclosure_present = bool(
                        result.compare_bundle and result.compare_bundle.anomaly_disclosures
                    )
            return _build_result(
                question, actual_behavior, citation_present, version_disclosed,
                anomaly_disclosure_present, failure_reason, diagnostics,
            )

        # --- Single-entity path ---
        partition, exact_resp = coordinate(raw_query)

        if partition.status.value == "failed":
            reason = partition.failure_reason
            actual_behavior = _map_abstention(reason) if reason else "abstain"
            failure_reason = reason.value if reason else "partition failed"
            return _build_result(
                question, actual_behavior, None, None, None, failure_reason, {},
            )

        # Run retrieval + answer.
        retrieval_result = retrieve(raw_query, partition)

        if exact_resp is not None:
            response = answer_from_exact(raw_query, exact_resp.answer)
        else:
            response = answer_from_retrieval(retrieval_result)

        if response.abstention is not None:
            actual_behavior = _map_abstention(response.abstention)
            failure_reason = response.abstention.value
            diagnostics = response.diagnostics
        else:
            actual_behavior = "answer"
            citation_present = (
                response.postcheck.citation_ids_present if response.postcheck else None
            )
            version_disclosed = (
                response.postcheck.version_token_present if response.postcheck else None
            )
            anomaly_disclosure_present = bool(
                response.evidence_bundle and response.evidence_bundle.anomaly_disclosures
            )

    except Exception as exc:
        actual_behavior = "error"
        failure_reason = str(exc)
        diagnostics = {"exception": str(exc)}

    return _build_result(
        question, actual_behavior, citation_present, version_disclosed,
        anomaly_disclosure_present, failure_reason, diagnostics,
    )


def _map_abstention(state: AbstentionState | None) -> str:
    if state is None:
        return "error"
    if state == AbstentionState.AMBIGUOUS_ENTITY:
        return "clarify"
    return "abstain"


def _build_result(
    question: GoldQuestion,
    actual_behavior: str,
    citation_present: bool | None,
    version_disclosed: bool | None,
    anomaly_disclosure_present: bool | None,
    failure_reason: str | None,
    diagnostics: dict,
) -> EvalCaseResult:
    passed = actual_behavior == question.expected_behavior.value
    return EvalCaseResult(
        question_id=question.question_id,
        query=question.query,
        query_class=question.query_class,
        expected_behavior=question.expected_behavior,
        actual_behavior=actual_behavior,
        passed=passed,
        citation_present=citation_present,
        version_disclosed=version_disclosed,
        anomaly_disclosure_present=anomaly_disclosure_present,
        failure_reason=failure_reason if not passed else None,
        diagnostics=diagnostics,
    )


# ---------------------------------------------------------------------------
# Eval runner
# ---------------------------------------------------------------------------


def eval_question(
    question: GoldQuestion,
    answer_fn: Callable[[GoldQuestion], EvalCaseResult] | None = None,
) -> EvalCaseResult:
    """Evaluate a single question and return an EvalCaseResult.

    Pass answer_fn to inject a mock pipeline (e.g. in tests).
    """
    fn = answer_fn or _default_answer_fn
    return fn(question)


def run_eval(
    questions: list[GoldQuestion],
    answer_fn: Callable[[GoldQuestion], EvalCaseResult] | None = None,
    question_set_label: str = "gold_v1",
    include_launch_gate: bool = True,
    save_results: bool = False,
) -> EvalRunSummary:
    """Evaluate a list of questions and produce a typed EvalRunSummary.

    Args:
        questions: Questions to evaluate (from load_gold_questions()).
        answer_fn: Optional injectable answer function. Default uses real pipeline.
        question_set_label: Label for the run (e.g. "gold_v1" or "launch_subset").
        include_launch_gate: Whether to compute launch-gate metrics.
        save_results: Whether to write results to data/atlas_qa/eval/.

    Returns:
        EvalRunSummary with all case results and optional launch gate.
    """
    run_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now(tz=timezone.utc).isoformat()

    cases: list[EvalCaseResult] = []
    for q in questions:
        result = eval_question(q, answer_fn=answer_fn)
        cases.append(result)

    launch_gate: LaunchGateSummary | None = None
    if include_launch_gate:
        launch_gate = compute_launch_gate(cases, run_id=run_id, timestamp=timestamp)

    summary = EvalRunSummary(
        run_id=run_id,
        timestamp=timestamp,
        question_set=question_set_label,
        total_questions=len(cases),
        cases=cases,
        launch_gate=launch_gate,
    )

    if save_results:
        _save_results(summary)

    return summary


def run_launch_subset(
    answer_fn: Callable[[GoldQuestion], EvalCaseResult] | None = None,
    save_results: bool = False,
) -> EvalRunSummary:
    """Load and evaluate only the 20-question launch-gate subset."""
    all_questions = load_gold_questions()
    subset = [q for q in all_questions if q.is_launch_subset]
    return run_eval(
        subset,
        answer_fn=answer_fn,
        question_set_label="launch_subset",
        include_launch_gate=True,
        save_results=save_results,
    )


# ---------------------------------------------------------------------------
# Launch-gate computation
# ---------------------------------------------------------------------------


def compute_launch_gate(
    cases: list[EvalCaseResult],
    run_id: str = "",
    timestamp: str = "",
) -> LaunchGateSummary:
    """Compute per-class launch-gate metrics from a list of EvalCaseResult objects."""
    from collections import defaultdict

    by_class: dict[QueryClass, list[EvalCaseResult]] = defaultdict(list)
    for case in cases:
        by_class[case.query_class].append(case)

    per_class_results: list[ClassGateResult] = []
    all_gate_passed = True
    notes: list[str] = []

    for qc in QueryClass:
        class_cases = by_class.get(qc, [])
        if not class_cases:
            continue

        total = len(class_cases)
        passed = sum(1 for c in class_cases if c.passed)
        pass_rate = passed / total if total > 0 else 0.0
        threshold = _CLASS_THRESHOLDS.get(qc, 0.85)
        gate_passed = pass_rate >= threshold

        failure_details: list[str] = []
        if not gate_passed:
            all_gate_passed = False
            failure_details = [
                f"{c.question_id}: expected={c.expected_behavior.value} "
                f"actual={c.actual_behavior} "
                f"reason={c.failure_reason or 'n/a'}"
                for c in class_cases if not c.passed
            ]
            notes.append(
                f"Class {qc.value}: {passed}/{total} ({pass_rate:.1%}) "
                f"— below threshold {threshold:.0%}"
            )

        per_class_results.append(ClassGateResult(
            query_class=qc,
            total=total,
            passed=passed,
            pass_rate=round(pass_rate, 4),
            threshold=threshold,
            gate_passed=gate_passed,
            failure_details=failure_details,
        ))

    total_q = len(cases)
    total_p = sum(1 for c in cases if c.passed)
    overall = total_p / total_q if total_q > 0 else 0.0

    return LaunchGateSummary(
        run_id=run_id,
        timestamp=timestamp,
        total_questions=total_q,
        total_passed=total_p,
        overall_pass_rate=round(overall, 4),
        per_class=per_class_results,
        gate_passed=all_gate_passed,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Result serialization
# ---------------------------------------------------------------------------


def _save_results(summary: EvalRunSummary) -> Path:
    """Write EvalRunSummary to data/atlas_qa/eval/ as a JSON artifact."""
    _EVAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts_slug = summary.timestamp.replace(":", "-").replace(".", "-")[:19]
    filename = f"eval_{summary.question_set}_{ts_slug}_{summary.run_id}.json"
    out_path = _EVAL_OUTPUT_DIR / filename
    out_path.write_text(
        json.dumps(summary.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return out_path


def save_results(summary: EvalRunSummary) -> Path:
    """Public wrapper — write an EvalRunSummary to disk and return the path."""
    return _save_results(summary)
