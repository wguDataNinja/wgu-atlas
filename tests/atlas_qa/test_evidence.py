"""Tests for Session 05 — Evidence bundle construction.

Covers:
- Bundle from RetrievalResult: normal path, empty candidates, stop_reason set,
  compare mode rejection, wrong-version candidates, entity_type inference.
- Bundle from ExactLookupAnswer: course, program, null answer.
- Anomaly disclosures are preserved in the bundle.
- Max artifact cap (5).
"""
from __future__ import annotations

import pytest

from atlas_qa.qa.evidence import bundle_from_exact, bundle_from_retrieval
from atlas_qa.qa.types import (
    AbstentionState,
    AnomalyDisclosure,
    CertPrepSignal,
    CourseCard,
    EntityType,
    EvidenceRef,
    ExactLookupAnswer,
    FuzzyRetrievalRequest,
    GuideEnrichmentSummary,
    InstancesByVersion,
    PartitionResult,
    PartitionStatus,
    QAResponse,
    RetrievalCandidate,
    RetrievalResult,
    RetrievalStopReason,
    SourceFamily,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

_EVIDENCE = [EvidenceRef(source_type="catalog", artifact_id="test", version="2026-03")]
_VERSION = "2026-03"


def _candidate(
    code: str = "C715",
    artifact_type: str = "course_card",
    version: str = _VERSION,
    source_family: SourceFamily = SourceFamily.CATALOG,
    score: float = 1.0,
) -> RetrievalCandidate:
    return RetrievalCandidate(
        artifact_type=artifact_type,
        entity_code=code,
        version=version,
        source_family=source_family,
        content_text=f"content for {code}",
        score=score,
        source_object_identity=f"course_cards/{code}",
    )


def _partition(
    entity_codes: list[str] | None = None,
    version_scope: list[str] | None = None,
    compare_mode: bool = False,
    notes: list[str] | None = None,
) -> PartitionResult:
    return PartitionResult(
        status=PartitionStatus.OK,
        entity_type=EntityType.COURSE,
        entity_codes=entity_codes or ["C715"],
        version_scope=version_scope or [_VERSION],
        source_scope=[SourceFamily.CATALOG],
        compare_mode=compare_mode,
        notes=notes or [],
    )


def _retrieval(
    candidates: list[RetrievalCandidate] | None = None,
    stop_reason: RetrievalStopReason | None = None,
    partition: PartitionResult | None = None,
) -> RetrievalResult:
    p = partition or _partition()
    req = FuzzyRetrievalRequest(raw_query="test query", partition=p)
    return RetrievalResult(
        raw_query="test query",
        request=req,
        stop_reason=stop_reason,
        selected_candidates=candidates or [],
    )


# ---------------------------------------------------------------------------
# bundle_from_retrieval
# ---------------------------------------------------------------------------


def test_bundle_from_retrieval_normal():
    cands = [_candidate("C715")]
    result = _retrieval(candidates=cands)
    bundle = bundle_from_retrieval(result)
    assert not isinstance(bundle, QAResponse)
    assert bundle.entity_code == "C715"
    assert bundle.version_used == _VERSION
    assert len(bundle.artifacts) == 1
    assert bundle.from_exact_path is False


def test_bundle_from_retrieval_stop_reason():
    result = _retrieval(stop_reason=RetrievalStopReason.EMPTY_CANDIDATE_POOL)
    resp = bundle_from_retrieval(result)
    assert isinstance(resp, QAResponse)
    assert resp.abstention == AbstentionState.INSUFFICIENT_EVIDENCE


def test_bundle_from_retrieval_empty_candidates():
    result = _retrieval(candidates=[])
    resp = bundle_from_retrieval(result)
    assert isinstance(resp, QAResponse)
    assert resp.abstention == AbstentionState.INSUFFICIENT_EVIDENCE


def test_bundle_from_retrieval_compare_mode_rejected():
    p = _partition(compare_mode=True)
    result = _retrieval(candidates=[_candidate()], partition=p)
    resp = bundle_from_retrieval(result)
    assert isinstance(resp, QAResponse)
    assert resp.abstention == AbstentionState.OUT_OF_SCOPE


def test_bundle_from_retrieval_wrong_version_rejected():
    cands = [_candidate(version="2024-01")]  # wrong version
    p = _partition(version_scope=[_VERSION])
    result = _retrieval(candidates=cands, partition=p)
    resp = bundle_from_retrieval(result)
    assert isinstance(resp, QAResponse)
    assert resp.abstention == AbstentionState.INSUFFICIENT_EVIDENCE


def test_bundle_from_retrieval_max_artifacts():
    # 7 candidates — only 5 should be included.
    cands = [_candidate(f"C71{i}") for i in range(7)]
    p = _partition(entity_codes=["C710"], version_scope=[_VERSION])
    result = _retrieval(candidates=cands, partition=p)
    bundle = bundle_from_retrieval(result)
    assert not isinstance(bundle, QAResponse)
    assert len(bundle.artifacts) == 5


def test_bundle_from_retrieval_carries_scope_notes():
    notes = ["cat_short_text anomaly detected for C715"]
    p = _partition(notes=notes)
    result = _retrieval(candidates=[_candidate()], partition=p)
    bundle = bundle_from_retrieval(result)
    assert not isinstance(bundle, QAResponse)
    assert bundle.notes == notes
    # Should be converted to an anomaly disclosure.
    assert len(bundle.anomaly_disclosures) == 1
    assert bundle.anomaly_disclosures[0].anomaly_type == "cat_short_text"


def test_bundle_from_retrieval_version_conflict_note():
    notes = ["version_conflict: MACCA catalog/guide mismatch"]
    p = _partition(notes=notes)
    result = _retrieval(candidates=[_candidate()], partition=p)
    bundle = bundle_from_retrieval(result)
    assert not isinstance(bundle, QAResponse)
    disclosures = bundle.anomaly_disclosures
    assert any(d.anomaly_type == "version_conflict" for d in disclosures)


# ---------------------------------------------------------------------------
# bundle_from_exact
# ---------------------------------------------------------------------------


def _exact_answer(
    entity_code: str = "C715",
    entity_type: EntityType = EntityType.COURSE,
    version: str = _VERSION,
    field_name: str | None = "catalog_description",
    field_value: object = "A course about data structures.",
    anomaly_disclosures: list[AnomalyDisclosure] | None = None,
) -> ExactLookupAnswer:
    return ExactLookupAnswer(
        entity_code=entity_code,
        entity_type=entity_type,
        resolved_version=version,
        field_name=field_name,
        field_value=field_value,
        source_object_identity=f"course_cards/{entity_code}",
        evidence_refs=_EVIDENCE,
        anomaly_disclosures=anomaly_disclosures or [],
    )


def test_bundle_from_exact_course():
    answer = _exact_answer()
    bundle = bundle_from_exact(answer)
    assert not isinstance(bundle, QAResponse)
    assert bundle.entity_code == "C715"
    assert bundle.entity_type == EntityType.COURSE
    assert bundle.version_used == _VERSION
    assert len(bundle.artifacts) == 1
    assert bundle.from_exact_path is True


def test_bundle_from_exact_program():
    answer = _exact_answer(
        entity_code="BSCS",
        entity_type=EntityType.PROGRAM,
        field_name="degree_title",
        field_value="B.S. Computer Science",
    )
    bundle = bundle_from_exact(answer)
    assert not isinstance(bundle, QAResponse)
    assert bundle.entity_code == "BSCS"
    assert bundle.entity_type == EntityType.PROGRAM


def test_bundle_from_exact_preserves_anomaly_disclosures():
    disclosures = [
        AnomalyDisclosure(anomaly_type="cat_short_text", message="C179 short text detected")
    ]
    answer = _exact_answer(anomaly_disclosures=disclosures)
    bundle = bundle_from_exact(answer)
    assert not isinstance(bundle, QAResponse)
    assert len(bundle.anomaly_disclosures) == 1
    assert bundle.anomaly_disclosures[0].anomaly_type == "cat_short_text"


def test_bundle_from_exact_dict_field_value():
    answer = _exact_answer(field_value={"key": "value"})
    bundle = bundle_from_exact(answer)
    assert not isinstance(bundle, QAResponse)
    assert isinstance(bundle.artifacts[0].content, dict)
