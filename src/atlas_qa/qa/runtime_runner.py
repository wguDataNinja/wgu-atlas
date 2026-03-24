"""Runtime validation runner for Atlas QA Session 07.

Runs the full end-to-end Atlas QA pipeline against a bounded query sample using
the real local Ollama backend. Captures a structured verbose/debug trace per query
and writes runtime artifacts to data/atlas_qa/runtime_checks/session07/.

This module does not redesign the pipeline. It instruments the existing call
chain (coordinator → retrieval → evidence → gate → generation → post-check)
and maps internal typed outputs to an inspectable RuntimeQueryTrace.

Usage (live run):
    from atlas_qa.qa.runtime_runner import run_session, save_artifacts, SESSION07_QUERIES
    summary = run_session(SESSION07_QUERIES)
    artifacts = save_artifacts(summary)

Usage (CLI):
    python -m atlas_qa.qa.runtime_runner
"""
from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Outcome classification
# ---------------------------------------------------------------------------


class RuntimeOutcome:
    ANSWER = "answer"
    ABSTAIN = "abstain"
    CLARIFY = "clarify"
    FAILURE = "failure"


# ---------------------------------------------------------------------------
# Typed trace model
# ---------------------------------------------------------------------------


class RuntimeQueryTrace(BaseModel):
    """Verbose/debug trace for one query through the Atlas QA runtime pipeline.

    All fields correspond directly to control-layer decisions, not just final text.
    """
    # Identity
    trace_id: str
    timestamp: str
    raw_query: str

    # Routing
    routed_path: str  # "compare" | "exact" | "fuzzy" | "out_of_scope"
    route_candidate_codes: list[str] = []
    route_explicit_version: str | None = None
    compare_intent_detected: bool = False

    # Classifier (if invoked on fuzzy path)
    classifier_invoked: bool = False
    classifier_output: dict[str, Any] | None = None
    classifier_parse_ok: bool | None = None
    classifier_schema_ok: bool | None = None
    classifier_used_fallback: bool = False

    # Entity resolution
    entity_code: str | None = None
    entity_type: str | None = None
    entity_resolution_result: str = "n/a"  # "resolved" | "ambiguous" | "not_found" | "n/a"

    # Version resolution
    resolved_version: str | None = None
    version_resolution_result: str = "n/a"  # "resolved" | "ambiguous" | "n/a"

    # Scope
    source_scope: list[str] = []
    section_scope: str | None = None

    # Compare mode state
    compare_mode: bool = False
    compare_from_version: str | None = None
    compare_to_version: str | None = None

    # Anomaly / conflict flags present before generation
    anomaly_flags: list[dict[str, str]] = []

    # Evidence
    top_evidence_ids: list[str] = []
    evidence_bundle_artifact_count: int = 0
    evidence_bundle_sources: list[str] = []
    evidence_bundle_notes: list[str] = []

    # Answerability gate
    gate_result: str = "n/a"  # "answerable" | "not_answerable" | "n/a"
    gate_notes: list[str] = []

    # Generation
    generation_invoked: bool = False
    prompt_type: str | None = None  # "answer" | "compare"

    # Post-check
    postcheck_passed: bool | None = None
    postcheck_failures: list[str] = []

    # Final outcome
    final_outcome: str  # RuntimeOutcome.{ANSWER,ABSTAIN,CLARIFY,FAILURE}
    outcome_reason: str
    answer_text: str | None = None

    # Runtime error (exception text if the pipeline raised)
    error: str | None = None


class RuntimeSessionSummary(BaseModel):
    """Session-level summary of a Session 07 runtime validation run."""
    session_id: str
    timestamp: str
    model_name: str
    queries_run: list[str]
    total_queries: int
    outcome_counts: dict[str, int]
    traces: list[RuntimeQueryTrace]
    major_failures: list[str] = []
    immediate_blockers: list[str] = []
    notes: list[str] = []


# ---------------------------------------------------------------------------
# Session 07 required query sample (per SESSION_SPEC.md)
# ---------------------------------------------------------------------------

SESSION07_QUERIES: list[tuple[str, str]] = [
    # (raw_query, behavior_class_label)
    # Exact lookup
    ("What is D426?", "exact_lookup"),
    ("How many CUs is BSACC?", "exact_lookup"),
    # Single-entity factual
    ("What is the capstone for BSDA?", "single_entity_factual"),
    # Section-grounded
    ("What competencies are listed for C949?", "section_grounded"),
    # Compare (two course codes — note: requires explicit version strings for
    # compare-mode activation; this exercises the route that handles two entities)
    ("How does D335 compare with D522?", "compare"),
    # Ambiguity / clarify
    ("What courses are in the MBA program?", "ambiguity_clarify"),
    # Abstain / out-of-scope
    ("Which WGU class is easiest?", "abstain_out_of_scope"),
    # Known anomaly / conflict
    ("Tell me about C179", "anomaly_conflict"),
    ("Tell me about D554", "anomaly_conflict"),
    ("What is the current version of MSHRM?", "anomaly_conflict"),
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _map_abstention_to_outcome(state) -> str:
    """Map an AbstentionState to a RuntimeOutcome string."""
    from atlas_qa.qa.types import AbstentionState
    if state is None:
        return RuntimeOutcome.FAILURE
    if state == AbstentionState.AMBIGUOUS_ENTITY:
        return RuntimeOutcome.CLARIFY
    return RuntimeOutcome.ABSTAIN


# ---------------------------------------------------------------------------
# Single-query runner
# ---------------------------------------------------------------------------


def run_query(raw_query: str, model_name: str = "llama3") -> RuntimeQueryTrace:
    """Run one query through the full Atlas QA pipeline and return a verbose trace.

    All failure modes are captured — exceptions are recorded in the trace, not
    re-raised.  The final_outcome is always populated.
    """
    from atlas_qa.qa.compare import (
        answer_compare,
        detect_compare_intent,
        extract_compare_versions,
    )
    from atlas_qa.qa.coordinator import coordinate
    from atlas_qa.qa.answer import answer_from_exact, answer_from_retrieval
    from atlas_qa.qa.retrieval import retrieve
    from atlas_qa.qa.router import route as _route, RouteClass
    from atlas_qa.qa.types import AbstentionState, EntityType, PartitionStatus

    trace_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now(tz=timezone.utc).isoformat()

    # Defaults — overwritten as we progress through the pipeline.
    trace_kwargs: dict[str, Any] = {
        "trace_id": trace_id,
        "timestamp": timestamp,
        "raw_query": raw_query,
        "routed_path": "unknown",
        "final_outcome": RuntimeOutcome.FAILURE,
        "outcome_reason": "not_reached",
    }

    try:
        # ------------------------------------------------------------------
        # Step 1 — Pre-route: extract candidate codes and version hints.
        # ------------------------------------------------------------------
        route_decision = _route(raw_query.strip().upper())
        candidate_codes = (
            route_decision.candidate_codes
            if route_decision.route_class == RouteClass.EXACT_LOOKUP
            else []
        )
        explicit_version = route_decision.explicit_version

        trace_kwargs["route_candidate_codes"] = candidate_codes
        trace_kwargs["route_explicit_version"] = explicit_version

        # ------------------------------------------------------------------
        # Step 2 — Compare intent detection.
        # ------------------------------------------------------------------
        is_compare = detect_compare_intent(raw_query)
        trace_kwargs["compare_intent_detected"] = is_compare

        if is_compare:
            # --- Compare path (Class D) ---
            trace_kwargs["routed_path"] = "compare"
            trace_kwargs["compare_mode"] = True

            from_v, to_v = extract_compare_versions(raw_query)
            trace_kwargs["compare_from_version"] = from_v
            trace_kwargs["compare_to_version"] = to_v

            entity_code = candidate_codes[0] if candidate_codes else None
            if entity_code is None:
                trace_kwargs["final_outcome"] = RuntimeOutcome.ABSTAIN
                trace_kwargs["outcome_reason"] = "no_entity_code_detected_for_compare"
                trace_kwargs["entity_resolution_result"] = "not_found"
                return RuntimeQueryTrace(**trace_kwargs)

            trace_kwargs["entity_code"] = entity_code

            # Determine entity type from quick coordinate pass.
            try:
                _, exact_resp = coordinate(raw_query)
                if exact_resp and exact_resp.answer:
                    entity_type = exact_resp.answer.entity_type.value
                    trace_kwargs["entity_type"] = entity_type
                    trace_kwargs["resolved_version"] = exact_resp.answer.resolved_version
                    trace_kwargs["version_resolution_result"] = "resolved"
                    trace_kwargs["entity_resolution_result"] = "resolved"
                else:
                    entity_type = EntityType.PROGRAM
                    trace_kwargs["entity_type"] = "program"
                    trace_kwargs["entity_resolution_result"] = "not_found"
            except Exception:
                entity_type = EntityType.PROGRAM
                trace_kwargs["entity_type"] = "program"
                trace_kwargs["entity_resolution_result"] = "n/a"

            result = answer_compare(raw_query, entity_code, EntityType(entity_type) if isinstance(entity_type, str) else entity_type, model_name=model_name)

            # Extract trace data from compare result.
            if result.compare_bundle:
                bundle = result.compare_bundle
                trace_kwargs["source_scope"] = [s.value for s in bundle.source_scope]
                trace_kwargs["anomaly_flags"] = [
                    {"anomaly_type": d.anomaly_type, "message": d.message}
                    for d in bundle.anomaly_disclosures
                ]
                all_artifacts = bundle.from_side.artifacts + bundle.to_side.artifacts if (bundle.from_side and bundle.to_side) else []
                trace_kwargs["top_evidence_ids"] = [a.source_object_identity for a in all_artifacts[:5]]
                trace_kwargs["evidence_bundle_artifact_count"] = len(all_artifacts)
                trace_kwargs["evidence_bundle_sources"] = list({a.source_family.value for a in all_artifacts})
                trace_kwargs["evidence_bundle_notes"] = bundle.notes
                trace_kwargs["gate_result"] = "answerable" if result.generation_output else "not_answerable"
                trace_kwargs["compare_from_version"] = bundle.from_version
                trace_kwargs["compare_to_version"] = bundle.to_version

            if result.generation_output:
                trace_kwargs["generation_invoked"] = True
                trace_kwargs["prompt_type"] = "compare"

            if result.postcheck:
                trace_kwargs["postcheck_passed"] = result.postcheck.passed
                trace_kwargs["postcheck_failures"] = result.postcheck.failure_reasons

            if result.abstention is not None:
                outcome = _map_abstention_to_outcome(result.abstention)
                trace_kwargs["final_outcome"] = outcome
                trace_kwargs["outcome_reason"] = result.abstention.value
            else:
                trace_kwargs["final_outcome"] = RuntimeOutcome.ANSWER
                trace_kwargs["outcome_reason"] = "generation_passed_postcheck"
                trace_kwargs["answer_text"] = result.answer_text

            return RuntimeQueryTrace(**trace_kwargs)

        # ------------------------------------------------------------------
        # Step 3 — Single-entity path.
        # ------------------------------------------------------------------
        if route_decision.route_class == RouteClass.OUT_OF_SCOPE or not candidate_codes:
            trace_kwargs["routed_path"] = "out_of_scope"
        else:
            trace_kwargs["routed_path"] = "exact"

        # Coordinate: route + exact lookup + partition.
        partition, exact_resp = coordinate(raw_query)

        # Extract entity/version info from partition or exact resp.
        if exact_resp and exact_resp.answer:
            ans = exact_resp.answer
            trace_kwargs["entity_code"] = ans.entity_code
            trace_kwargs["entity_type"] = ans.entity_type.value
            trace_kwargs["resolved_version"] = ans.resolved_version
            trace_kwargs["entity_resolution_result"] = "resolved"
            trace_kwargs["version_resolution_result"] = "resolved"
            trace_kwargs["anomaly_flags"] = [
                {"anomaly_type": d.anomaly_type, "message": d.message}
                for d in ans.anomaly_disclosures
            ]
        elif candidate_codes:
            trace_kwargs["entity_code"] = candidate_codes[0]
            trace_kwargs["entity_resolution_result"] = (
                "ambiguous"
                if partition.failure_reason == AbstentionState.AMBIGUOUS_ENTITY
                else "not_found"
            )

        if partition.entity_type:
            trace_kwargs["entity_type"] = partition.entity_type.value
        if partition.version_scope:
            trace_kwargs["resolved_version"] = partition.version_scope[0]
            trace_kwargs["version_resolution_result"] = "resolved"
        if partition.source_scope:
            trace_kwargs["source_scope"] = [s.value for s in partition.source_scope]
        if partition.section_scope:
            trace_kwargs["section_scope"] = partition.section_scope.value

        # Handle partition failure.
        if partition.status == PartitionStatus.FAILED:
            reason = partition.failure_reason
            outcome = _map_abstention_to_outcome(reason) if reason else RuntimeOutcome.ABSTAIN
            trace_kwargs["routed_path"] = "out_of_scope"
            trace_kwargs["final_outcome"] = outcome
            trace_kwargs["outcome_reason"] = reason.value if reason else "partition_failed"
            if reason == AbstentionState.AMBIGUOUS_ENTITY:
                trace_kwargs["entity_resolution_result"] = "ambiguous"
            return RuntimeQueryTrace(**trace_kwargs)

        # ------------------------------------------------------------------
        # Step 4 — Retrieval (fuzzy path when no exact answer).
        # ------------------------------------------------------------------
        if exact_resp is None:
            trace_kwargs["routed_path"] = "fuzzy"

        retrieval_result = retrieve(raw_query, partition)

        # Extract classifier trace.
        if retrieval_result.classifier_output is not None:
            trace_kwargs["classifier_invoked"] = True
            trace_kwargs["classifier_output"] = retrieval_result.classifier_output.model_dump()
            trace_kwargs["classifier_parse_ok"] = not retrieval_result.classifier_parse_error
            trace_kwargs["classifier_schema_ok"] = not retrieval_result.classifier_schema_error
            trace_kwargs["classifier_used_fallback"] = retrieval_result.classifier_used_fallback

        # ------------------------------------------------------------------
        # Step 5 — Answer orchestration (bundle → gate → generate → postcheck).
        # ------------------------------------------------------------------
        if exact_resp is not None:
            response = answer_from_exact(raw_query, exact_resp.answer, model_name=model_name)
        else:
            response = answer_from_retrieval(retrieval_result, model_name=model_name)

        # Extract evidence bundle info from response.
        if response.evidence_bundle:
            bundle = response.evidence_bundle
            trace_kwargs["top_evidence_ids"] = [a.source_object_identity for a in bundle.artifacts[:5]]
            trace_kwargs["evidence_bundle_artifact_count"] = len(bundle.artifacts)
            trace_kwargs["evidence_bundle_sources"] = [s.value for s in bundle.source_scope]
            trace_kwargs["evidence_bundle_notes"] = bundle.notes
            if not trace_kwargs.get("anomaly_flags"):
                trace_kwargs["anomaly_flags"] = [
                    {"anomaly_type": d.anomaly_type, "message": d.message}
                    for d in bundle.anomaly_disclosures
                ]
            # Infer gate result: gate is the only pre-generation check
            if response.generation_output is not None or response.answer_text is not None:
                trace_kwargs["gate_result"] = "answerable"
            elif response.abstention == AbstentionState.INSUFFICIENT_EVIDENCE:
                # Could be gate rejection OR generation failure — check diagnostics
                if "gate_notes" in response.diagnostics:
                    trace_kwargs["gate_result"] = "not_answerable"
                    trace_kwargs["gate_notes"] = response.diagnostics.get("gate_notes", [])
                else:
                    trace_kwargs["gate_result"] = "answerable"  # gate passed, generation failed
            else:
                trace_kwargs["gate_result"] = "n/a"

        # Extract generation info.
        if response.generation_output is not None:
            trace_kwargs["generation_invoked"] = True
            trace_kwargs["prompt_type"] = "answer"
        elif (
            trace_kwargs.get("gate_result") == "answerable"
            and "generation_error" in response.diagnostics
        ):
            # Gate passed but generate_answer() raised before producing a GenerationOutput.
            trace_kwargs["generation_invoked"] = True
            trace_kwargs["prompt_type"] = "answer"

        # Extract post-check info.
        if response.postcheck is not None:
            trace_kwargs["postcheck_passed"] = response.postcheck.passed
            trace_kwargs["postcheck_failures"] = response.postcheck.failure_reasons

        # Final outcome.
        if response.abstention is not None:
            outcome = _map_abstention_to_outcome(response.abstention)
            trace_kwargs["final_outcome"] = outcome
            trace_kwargs["outcome_reason"] = response.abstention.value
        else:
            trace_kwargs["final_outcome"] = RuntimeOutcome.ANSWER
            trace_kwargs["outcome_reason"] = "generation_passed_postcheck"
            trace_kwargs["answer_text"] = response.answer_text

    except Exception as exc:
        trace_kwargs["final_outcome"] = RuntimeOutcome.FAILURE
        trace_kwargs["outcome_reason"] = "exception"
        trace_kwargs["error"] = str(exc)
        if trace_kwargs.get("routed_path") == "unknown":
            trace_kwargs["routed_path"] = "unknown"

    return RuntimeQueryTrace(**trace_kwargs)


# ---------------------------------------------------------------------------
# Session runner
# ---------------------------------------------------------------------------


def run_session(
    query_sample: list[tuple[str, str]] | None = None,
    model_name: str = "llama3",
) -> RuntimeSessionSummary:
    """Run the full Session 07 query sample and return a typed summary.

    Args:
        query_sample: List of (raw_query, behavior_class_label) pairs.
                      Defaults to SESSION07_QUERIES.
        model_name:   Ollama model to use for live generation.
    """
    queries = query_sample or SESSION07_QUERIES
    session_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now(tz=timezone.utc).isoformat()

    traces: list[RuntimeQueryTrace] = []
    outcome_counts: dict[str, int] = {
        RuntimeOutcome.ANSWER: 0,
        RuntimeOutcome.ABSTAIN: 0,
        RuntimeOutcome.CLARIFY: 0,
        RuntimeOutcome.FAILURE: 0,
    }

    print(f"[session07] Starting runtime validation — {len(queries)} queries, model={model_name}")

    for i, (raw_query, label) in enumerate(queries, start=1):
        print(f"[session07] [{i}/{len(queries)}] {label}: {raw_query!r}", flush=True)
        trace = run_query(raw_query, model_name=model_name)
        traces.append(trace)
        outcome_counts[trace.final_outcome] = outcome_counts.get(trace.final_outcome, 0) + 1
        print(f"[session07]   → outcome={trace.final_outcome}  reason={trace.outcome_reason}")
        if trace.error:
            print(f"[session07]   → ERROR: {trace.error}")

    major_failures = [
        f"{t.raw_query!r}: {t.outcome_reason}" + (f" ({t.error})" if t.error else "")
        for t in traces
        if t.final_outcome == RuntimeOutcome.FAILURE
    ]

    immediate_blockers: list[str] = []
    if outcome_counts.get(RuntimeOutcome.FAILURE, 0) > 0:
        immediate_blockers.append(
            f"{outcome_counts[RuntimeOutcome.FAILURE]} queries ended in FAILURE — check major_failures"
        )

    notes = [
        f"Model: {model_name}",
        f"Total: {len(traces)} queries",
        f"Outcomes: answer={outcome_counts.get(RuntimeOutcome.ANSWER,0)}, "
        f"abstain={outcome_counts.get(RuntimeOutcome.ABSTAIN,0)}, "
        f"clarify={outcome_counts.get(RuntimeOutcome.CLARIFY,0)}, "
        f"failure={outcome_counts.get(RuntimeOutcome.FAILURE,0)}",
    ]

    return RuntimeSessionSummary(
        session_id=session_id,
        timestamp=timestamp,
        model_name=model_name,
        queries_run=[q for q, _ in queries],
        total_queries=len(queries),
        outcome_counts=outcome_counts,
        traces=traces,
        major_failures=major_failures,
        immediate_blockers=immediate_blockers,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Artifact serialization
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).parents[3]
_DEFAULT_ARTIFACT_DIR = _REPO_ROOT / "data" / "atlas_qa" / "runtime_checks" / "session07"


def save_artifacts(
    summary: RuntimeSessionSummary,
    output_dir: Path | None = None,
) -> dict[str, Path]:
    """Write per-query trace files and a session summary artifact.

    Returns a dict mapping artifact names to written paths.
    """
    out = output_dir or _DEFAULT_ARTIFACT_DIR
    out.mkdir(parents=True, exist_ok=True)

    written: dict[str, Path] = {}

    # Per-query trace files.
    for trace in summary.traces:
        slug = trace.raw_query[:40].replace(" ", "_").replace("?", "").replace("'", "")
        filename = f"trace_{trace.trace_id}_{slug}.json"
        path = out / filename
        path.write_text(
            json.dumps(trace.model_dump(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        written[f"trace/{trace.trace_id}"] = path

    # Session summary (without individual traces to keep it readable).
    summary_data = summary.model_dump()
    # Exclude per-trace detail from top-level summary for readability.
    summary_no_traces = {k: v for k, v in summary_data.items() if k != "traces"}
    summary_no_traces["trace_files"] = [str(p.name) for p in written.values()]

    ts_slug = summary.timestamp.replace(":", "-").replace(".", "-")[:19]
    summary_filename = f"session_summary_{ts_slug}_{summary.session_id}.json"
    summary_path = out / summary_filename
    summary_path.write_text(
        json.dumps(summary_no_traces, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    written["session_summary"] = summary_path

    print(f"[session07] Artifacts written to: {out}")
    for name, path in written.items():
        print(f"[session07]   {path.name}")

    return written


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Run Session 07 runtime validation and save artifacts."""
    model_name = "llama3:latest"
    if len(sys.argv) > 1:
        model_name = sys.argv[1]

    summary = run_session(SESSION07_QUERIES, model_name=model_name)
    save_artifacts(summary)

    # Print a brief session report.
    print("\n=== Session 07 Runtime Validation Report ===")
    for note in summary.notes:
        print(f"  {note}")
    if summary.major_failures:
        print("\nMajor failures:")
        for f in summary.major_failures:
            print(f"  - {f}")
    if summary.immediate_blockers:
        print("\nImmediate blockers:")
        for b in summary.immediate_blockers:
            print(f"  - {b}")
    print()

    return 0 if not summary.immediate_blockers else 1


if __name__ == "__main__":
    sys.exit(main())
