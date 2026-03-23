"""Tests for Session 06 evaluation harness (eval_runner.py).

Covers:
- gold question set parsing from markdown text
- launch subset flagging
- eval_question with injected mock answer_fn
- run_eval producing EvalRunSummary
- compute_launch_gate producing per-class metrics
- class thresholds applied correctly
- gate pass/fail logic
- save_results / serialization
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from atlas_qa.qa.eval_runner import (
    _LAUNCH_SUBSET_IDS,
    _parse_gold_questions,
    compute_launch_gate,
    eval_question,
    load_gold_questions,
    run_eval,
    run_launch_subset,
    save_results,
)
from atlas_qa.qa.types import (
    EvalCaseResult,
    EvalExpectedBehavior,
    EvalRunSummary,
    GoldQuestion,
    LaunchGateSummary,
    QueryClass,
)

# ---------------------------------------------------------------------------
# Minimal mock markdown with all 7 query classes
# ---------------------------------------------------------------------------

_MOCK_GOLD_MD = """\
# Atlas QA — Gold Question Set

## 3. Gold Question Table

### Class A — Exact Identifier Lookup

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| A-001 | What is D426? | A | answer | course | catalog | N | Deterministic path |
| A-002 | How many CUs is C715? | A | answer | course | canon | N | CU lookup |
| A-003 | What is BSACC? | A | answer | program | catalog | N | Not in launch subset |

### Class B — Single-Entity Factual Lookup

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| B-016 | What is the catalog description for D426? | B | answer | course | catalog | Y | Version citation required |

### Class C — Section-Grounded NL Lookup

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| C-038 | What courses are in the standard path for BSCS? | C | answer | section | guide | Y | Standard path qualification |

### Class D — Explicit Version Comparison

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| D-054 | What changed in BSCS between the 2025-06 and 2026-03 catalog editions? | D | answer | compare | both | Y | version_diff_card preferred |

### Class E — Ambiguity / Disambiguation

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| E-066 | What courses are in the MBA program? | E | clarify | program | none | N | Disambiguation required |

### Class F — Abstain / Out-of-Scope

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| F-076 | Which WGU class is the easiest? | F | abstain | none | none | N | Opinion |

### Class G — Known Anomaly / Conflict

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| G-091 | What is the catalog description for C179? | G | answer | course | catalog | Y | Anomaly disclosure required |
"""


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


class TestParseGoldQuestions:
    def test_parses_all_classes(self):
        questions = _parse_gold_questions(_MOCK_GOLD_MD)
        classes = {q.query_class for q in questions}
        assert classes == {
            QueryClass.A, QueryClass.B, QueryClass.C, QueryClass.D,
            QueryClass.E, QueryClass.F, QueryClass.G,
        }

    def test_correct_question_count(self):
        questions = _parse_gold_questions(_MOCK_GOLD_MD)
        assert len(questions) == 9

    def test_question_fields_populated(self):
        questions = _parse_gold_questions(_MOCK_GOLD_MD)
        a001 = next(q for q in questions if q.question_id == "A-001")
        assert a001.query == "What is D426?"
        assert a001.query_class == QueryClass.A
        assert a001.expected_behavior == EvalExpectedBehavior.ANSWER
        assert a001.entity_type_label == "course"
        assert a001.source_scope_label == "catalog"
        assert a001.version_sensitive is False

    def test_abstain_behavior_parsed(self):
        questions = _parse_gold_questions(_MOCK_GOLD_MD)
        f076 = next(q for q in questions if q.question_id == "F-076")
        assert f076.expected_behavior == EvalExpectedBehavior.ABSTAIN

    def test_clarify_behavior_parsed(self):
        questions = _parse_gold_questions(_MOCK_GOLD_MD)
        e066 = next(q for q in questions if q.question_id == "E-066")
        assert e066.expected_behavior == EvalExpectedBehavior.CLARIFY

    def test_version_sensitive_flag(self):
        questions = _parse_gold_questions(_MOCK_GOLD_MD)
        b016 = next(q for q in questions if q.question_id == "B-016")
        assert b016.version_sensitive is True

    def test_launch_subset_flagged(self):
        questions = _parse_gold_questions(_MOCK_GOLD_MD)
        # A-001 and A-002 are in the launch subset; A-001 should be flagged.
        a001 = next(q for q in questions if q.question_id == "A-001")
        assert a001.is_launch_subset is True
        # B-016 is in the subset too.
        b016 = next(q for q in questions if q.question_id == "B-016")
        assert b016.is_launch_subset is True

    def test_non_launch_subset_not_flagged(self):
        questions = _parse_gold_questions(_MOCK_GOLD_MD)
        # A-003 is NOT in the launch subset per _LAUNCH_SUBSET_IDS.
        a003 = next(q for q in questions if q.question_id == "A-003")
        assert a003.is_launch_subset is False

    def test_empty_text_returns_empty_list(self):
        assert _parse_gold_questions("") == []


# ---------------------------------------------------------------------------
# eval_question with mock answer_fn
# ---------------------------------------------------------------------------


def _mock_answer_fn(behavior: str):
    """Return a mock answer_fn that always returns the given behavior."""
    def fn(question: GoldQuestion) -> EvalCaseResult:
        passed = behavior == question.expected_behavior.value
        return EvalCaseResult(
            question_id=question.question_id,
            query=question.query,
            query_class=question.query_class,
            expected_behavior=question.expected_behavior,
            actual_behavior=behavior,
            passed=passed,
        )
    return fn


class TestEvalQuestion:
    def _make_question(
        self,
        qid: str = "A-001",
        behavior: EvalExpectedBehavior = EvalExpectedBehavior.ANSWER,
        qclass: QueryClass = QueryClass.A,
    ) -> GoldQuestion:
        return GoldQuestion(
            question_id=qid,
            query="What is D426?",
            query_class=qclass,
            expected_behavior=behavior,
            entity_type_label="course",
            source_scope_label="catalog",
            version_sensitive=False,
        )

    def test_pass_when_behavior_matches(self):
        q = self._make_question(behavior=EvalExpectedBehavior.ANSWER)
        result = eval_question(q, answer_fn=_mock_answer_fn("answer"))
        assert result.passed is True
        assert result.actual_behavior == "answer"

    def test_fail_when_behavior_mismatches(self):
        q = self._make_question(behavior=EvalExpectedBehavior.ABSTAIN)
        result = eval_question(q, answer_fn=_mock_answer_fn("answer"))
        assert result.passed is False
        assert result.actual_behavior == "answer"

    def test_clarify_pass(self):
        q = self._make_question(
            qid="E-066",
            behavior=EvalExpectedBehavior.CLARIFY,
            qclass=QueryClass.E,
        )
        result = eval_question(q, answer_fn=_mock_answer_fn("clarify"))
        assert result.passed is True

    def test_abstain_pass(self):
        q = self._make_question(
            qid="F-076",
            behavior=EvalExpectedBehavior.ABSTAIN,
            qclass=QueryClass.F,
        )
        result = eval_question(q, answer_fn=_mock_answer_fn("abstain"))
        assert result.passed is True


# ---------------------------------------------------------------------------
# run_eval
# ---------------------------------------------------------------------------


class TestRunEval:
    def _questions_from_mock(self) -> list[GoldQuestion]:
        return _parse_gold_questions(_MOCK_GOLD_MD)

    def test_returns_eval_run_summary(self):
        questions = self._questions_from_mock()
        summary = run_eval(questions, answer_fn=_mock_answer_fn("answer"))
        assert isinstance(summary, EvalRunSummary)
        assert summary.total_questions == len(questions)  # 9 questions from mock

    def test_cases_count_matches_questions(self):
        questions = self._questions_from_mock()
        summary = run_eval(questions, answer_fn=_mock_answer_fn("answer"))
        assert len(summary.cases) == len(questions)

    def test_all_pass_when_mock_returns_correct_behavior(self):
        # Build answer_fn that returns expected behavior per class.
        def perfect_fn(question: GoldQuestion) -> EvalCaseResult:
            return EvalCaseResult(
                question_id=question.question_id,
                query=question.query,
                query_class=question.query_class,
                expected_behavior=question.expected_behavior,
                actual_behavior=question.expected_behavior.value,
                passed=True,
            )

        questions = self._questions_from_mock()
        summary = run_eval(questions, answer_fn=perfect_fn)
        assert all(c.passed for c in summary.cases)

    def test_launch_gate_computed_when_requested(self):
        questions = self._questions_from_mock()
        summary = run_eval(questions, answer_fn=_mock_answer_fn("answer"), include_launch_gate=True)
        assert summary.launch_gate is not None

    def test_launch_gate_absent_when_not_requested(self):
        questions = self._questions_from_mock()
        summary = run_eval(questions, answer_fn=_mock_answer_fn("answer"), include_launch_gate=False)
        assert summary.launch_gate is None

    def test_question_set_label_stored(self):
        questions = self._questions_from_mock()
        summary = run_eval(
            questions,
            answer_fn=_mock_answer_fn("answer"),
            question_set_label="test_run",
        )
        assert summary.question_set == "test_run"


# ---------------------------------------------------------------------------
# compute_launch_gate
# ---------------------------------------------------------------------------


def _make_cases(
    class_counts: dict[QueryClass, tuple[int, int]],
) -> list[EvalCaseResult]:
    """Build EvalCaseResult list. class_counts: {class: (total, passing)}."""
    cases: list[EvalCaseResult] = []
    for qc, (total, passing) in class_counts.items():
        for i in range(total):
            passed = i < passing
            cases.append(EvalCaseResult(
                question_id=f"{qc.value}-{i:03d}",
                query="test query",
                query_class=qc,
                expected_behavior=EvalExpectedBehavior.ANSWER,
                actual_behavior="answer" if passed else "abstain",
                passed=passed,
            ))
    return cases


class TestComputeLaunchGate:
    def test_all_class_gates_pass(self):
        # All classes at or above their thresholds.
        cases = _make_cases({
            QueryClass.A: (20, 20),   # 100% >= 95%
            QueryClass.B: (20, 18),   # 90% >= 85%
            QueryClass.C: (18, 16),   # ~89% >= 85%
            QueryClass.D: (12, 10),   # ~83% >= 80%
            QueryClass.E: (10, 10),   # 100% >= 90%
            QueryClass.F: (15, 15),   # 100% >= 98%
            QueryClass.G: (10, 10),   # 100% >= 100%
        })
        gate = compute_launch_gate(cases)
        assert gate.gate_passed is True
        assert all(r.gate_passed for r in gate.per_class)

    def test_gate_fails_if_one_class_below_threshold(self):
        # Class F at 80% — below 98% threshold.
        cases = _make_cases({
            QueryClass.A: (15, 15),
            QueryClass.B: (20, 18),
            QueryClass.F: (10, 8),   # 80% < 98%
        })
        gate = compute_launch_gate(cases)
        assert gate.gate_passed is False
        f_result = next(r for r in gate.per_class if r.query_class == QueryClass.F)
        assert f_result.gate_passed is False

    def test_pass_rates_computed_correctly(self):
        cases = _make_cases({QueryClass.A: (10, 9)})
        gate = compute_launch_gate(cases)
        a_result = next(r for r in gate.per_class if r.query_class == QueryClass.A)
        assert a_result.pass_rate == pytest.approx(0.9, abs=0.001)

    def test_overall_pass_rate(self):
        cases = _make_cases({
            QueryClass.A: (10, 8),
            QueryClass.B: (10, 6),
        })
        gate = compute_launch_gate(cases)
        assert gate.total_questions == 20
        assert gate.total_passed == 14
        assert gate.overall_pass_rate == pytest.approx(0.7, abs=0.001)

    def test_failure_details_populated_on_failure(self):
        cases = _make_cases({QueryClass.F: (5, 4)})  # 80% < 98%
        gate = compute_launch_gate(cases)
        f_result = next(r for r in gate.per_class if r.query_class == QueryClass.F)
        assert len(f_result.failure_details) == 1

    def test_class_g_requires_100_percent(self):
        # Class G at 90% — below 100% threshold.
        cases = _make_cases({QueryClass.G: (10, 9)})
        gate = compute_launch_gate(cases)
        g_result = next(r for r in gate.per_class if r.query_class == QueryClass.G)
        assert g_result.gate_passed is False

    def test_empty_class_not_included(self):
        cases = _make_cases({QueryClass.A: (5, 5)})
        gate = compute_launch_gate(cases)
        present = {r.query_class for r in gate.per_class}
        assert QueryClass.B not in present

    def test_threshold_values_encoded(self):
        cases = _make_cases({
            QueryClass.A: (1, 1),
            QueryClass.B: (1, 1),
            QueryClass.C: (1, 1),
            QueryClass.D: (1, 1),
            QueryClass.E: (1, 1),
            QueryClass.F: (1, 1),
            QueryClass.G: (1, 1),
        })
        gate = compute_launch_gate(cases)
        threshold_by_class = {r.query_class: r.threshold for r in gate.per_class}
        assert threshold_by_class[QueryClass.A] == 0.95
        assert threshold_by_class[QueryClass.B] == 0.85
        assert threshold_by_class[QueryClass.C] == 0.85
        assert threshold_by_class[QueryClass.D] == 0.80
        assert threshold_by_class[QueryClass.E] == 0.90
        assert threshold_by_class[QueryClass.F] == 0.98
        assert threshold_by_class[QueryClass.G] == 1.00


# ---------------------------------------------------------------------------
# save_results / serialization
# ---------------------------------------------------------------------------


class TestSaveResults:
    def test_writes_json_to_disk(self, tmp_path, monkeypatch):
        monkeypatch.setattr("atlas_qa.qa.eval_runner._EVAL_OUTPUT_DIR", tmp_path)

        summary = run_eval(
            _parse_gold_questions(_MOCK_GOLD_MD),
            answer_fn=_mock_answer_fn("answer"),
            question_set_label="test_save",
        )
        out_path = save_results(summary)

        assert out_path.exists()
        data = json.loads(out_path.read_text())
        assert data["question_set"] == "test_save"
        assert data["total_questions"] == len(summary.cases)

    def test_saved_json_is_valid_model(self, tmp_path, monkeypatch):
        monkeypatch.setattr("atlas_eva.qa.eval_runner._EVAL_OUTPUT_DIR", tmp_path) if False else None
        monkeypatch.setattr("atlas_qa.qa.eval_runner._EVAL_OUTPUT_DIR", tmp_path)

        summary = run_eval(
            _parse_gold_questions(_MOCK_GOLD_MD),
            answer_fn=_mock_answer_fn("answer"),
        )
        out_path = save_results(summary)
        data = json.loads(out_path.read_text())

        # Must round-trip via pydantic.
        reloaded = EvalRunSummary.model_validate(data)
        assert reloaded.run_id == summary.run_id


# ---------------------------------------------------------------------------
# load_gold_questions integration (reads real file)
# ---------------------------------------------------------------------------


class TestLoadGoldQuestionsIntegration:
    def test_loads_100_questions(self):
        questions = load_gold_questions()
        assert len(questions) == 100

    def test_all_classes_present(self):
        questions = load_gold_questions()
        classes = {q.query_class for q in questions}
        assert classes == set(QueryClass)

    def test_launch_subset_has_20_questions(self):
        questions = load_gold_questions()
        subset = [q for q in questions if q.is_launch_subset]
        assert len(subset) == 20

    def test_launch_subset_ids_match_spec(self):
        questions = load_gold_questions()
        subset_ids = {q.question_id for q in questions if q.is_launch_subset}
        assert subset_ids == _LAUNCH_SUBSET_IDS
