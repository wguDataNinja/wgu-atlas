"""Tests for Session 05 — Deterministic answerability gate.

Covers all failure modes:
- Empty bundle.
- No artifact matching entity code.
- Wrong-version artifacts.
- Section scope required but no guide section card.
- D554 guide block.
- Compare mode (multiple versions).
- Passing case.
"""
from __future__ import annotations

import pytest

from atlas_qa.qa.gate import check_answerability
from atlas_qa.qa.types import (
    AbstentionState,
    AnomalyDisclosure,
    EntityType,
    EvidenceArtifact,
    EvidenceBundle,
    EvidenceRef,
    SectionScope,
    SourceFamily,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

_VERSION = "2026-03"
_EVIDENCE_REF = EvidenceRef(source_type="catalog", artifact_id="test", version=_VERSION)


def _artifact(
    entity_code: str = "C715",
    artifact_type: str = "course_card",
    version: str = _VERSION,
    source_family: SourceFamily = SourceFamily.CATALOG,
    identity: str | None = None,
) -> EvidenceArtifact:
    return EvidenceArtifact(
        artifact_type=artifact_type,
        entity_code=entity_code,
        version=version,
        source_family=source_family,
        content="test content",
        source_object_identity=identity or f"course_cards/{entity_code}",
        evidence_ref=_EVIDENCE_REF,
    )


def _bundle(
    entity_code: str = "C715",
    entity_type: EntityType = EntityType.COURSE,
    version_used: str = _VERSION,
    artifacts: list[EvidenceArtifact] | None = None,
    anomaly_disclosures: list[AnomalyDisclosure] | None = None,
    notes: list[str] | None = None,
) -> EvidenceBundle:
    return EvidenceBundle(
        entity_code=entity_code,
        entity_type=entity_type,
        version_used=version_used,
        source_scope=[SourceFamily.CATALOG],
        artifacts=artifacts if artifacts is not None else [_artifact(entity_code)],
        anomaly_disclosures=anomaly_disclosures or [],
        notes=notes or [],
        from_exact_path=False,
    )


# ---------------------------------------------------------------------------
# Passing case
# ---------------------------------------------------------------------------


def test_gate_passes_normal_bundle():
    result = check_answerability(_bundle())
    assert result.answerable is True
    assert result.abstention_reason is None


# ---------------------------------------------------------------------------
# Failure: empty bundle
# ---------------------------------------------------------------------------


def test_gate_fails_empty_bundle():
    result = check_answerability(_bundle(artifacts=[]))
    assert result.answerable is False
    assert result.abstention_reason == AbstentionState.INSUFFICIENT_EVIDENCE
    assert any("empty" in n for n in result.gate_notes)


# ---------------------------------------------------------------------------
# Failure: no artifact matches entity code
# ---------------------------------------------------------------------------


def test_gate_fails_no_matching_entity():
    artifact = _artifact(entity_code="D426")  # different code
    result = check_answerability(_bundle(entity_code="C715", artifacts=[artifact]))
    assert result.answerable is False
    assert result.abstention_reason == AbstentionState.INSUFFICIENT_EVIDENCE


# ---------------------------------------------------------------------------
# Failure: wrong version
# ---------------------------------------------------------------------------


def test_gate_fails_wrong_version():
    artifact = _artifact(entity_code="C715", version="2024-01")
    result = check_answerability(_bundle(version_used=_VERSION, artifacts=[artifact]))
    assert result.answerable is False
    assert result.abstention_reason == AbstentionState.INSUFFICIENT_EVIDENCE


# ---------------------------------------------------------------------------
# Failure: section scope requires guide_section_card
# ---------------------------------------------------------------------------


def test_gate_fails_competencies_no_guide_section():
    # Only a course_card — no guide_section_card.
    result = check_answerability(
        _bundle(),
        section_scope=SectionScope.COMPETENCIES,
    )
    assert result.answerable is False
    assert result.abstention_reason == AbstentionState.INSUFFICIENT_EVIDENCE
    assert any("guide_section_card" in n for n in result.gate_notes)


def test_gate_passes_competencies_with_guide_section():
    artifacts = [
        _artifact(entity_code="C715", artifact_type="guide_section_card"),
    ]
    result = check_answerability(
        _bundle(artifacts=artifacts),
        section_scope=SectionScope.COMPETENCIES,
    )
    assert result.answerable is True


def test_gate_no_section_scope_no_guide_required():
    # Without a section scope, guide_section_card is not required.
    result = check_answerability(_bundle(), section_scope=None)
    assert result.answerable is True


# ---------------------------------------------------------------------------
# Failure: D554 guide block
# ---------------------------------------------------------------------------


def test_gate_fails_d554_guide_block_with_section_scope():
    disclosures = [
        AnomalyDisclosure(
            anomaly_type="guide_misrouted_text",
            message="D554 guide block: guide text misrouted",
        )
    ]
    artifacts = [
        _artifact(entity_code="C715", artifact_type="guide_section_card"),
    ]
    result = check_answerability(
        _bundle(artifacts=artifacts, anomaly_disclosures=disclosures),
        section_scope=SectionScope.COMPETENCIES,
    )
    assert result.answerable is False
    assert any("D554" in n for n in result.gate_notes)


# ---------------------------------------------------------------------------
# Failure: compare mode (multiple versions in bundle)
# ---------------------------------------------------------------------------


def test_gate_fails_compare_mode():
    artifacts = [
        _artifact(entity_code="C715", version="2026-03"),
        _artifact(entity_code="C715", version="2024-01"),  # second version
    ]
    result = check_answerability(
        _bundle(version_used="2026-03", artifacts=artifacts)
    )
    assert result.answerable is False
    assert result.abstention_reason == AbstentionState.OUT_OF_SCOPE


# ---------------------------------------------------------------------------
# course_overview scope: no guide section required
# ---------------------------------------------------------------------------


def test_gate_passes_course_overview_no_guide_needed():
    result = check_answerability(
        _bundle(),
        section_scope=SectionScope.COURSE_OVERVIEW,
    )
    assert result.answerable is True


# ---------------------------------------------------------------------------
# Fix 2 — guide-seeking intent gate (check 6b)
# ---------------------------------------------------------------------------


def _guide_misrouted_disclosure() -> AnomalyDisclosure:
    return AnomalyDisclosure(
        anomaly_type="guide_misrouted_text",
        message="D554: guide description text matches catalog; guide alternates suppressed.",
    )


def test_gate_blocks_guide_seeking_with_disclosure_no_guide_cards():
    """guide_misrouted_text disclosure + no guide_section_card artifacts + guide_seeking → block."""
    bundle = _bundle(
        entity_code="D554",
        anomaly_disclosures=[_guide_misrouted_disclosure()],
        artifacts=[_artifact(entity_code="D554", artifact_type="course_card")],
    )
    result = check_answerability(bundle, guide_seeking_intent=True)
    assert result.answerable is False
    assert result.abstention_reason == AbstentionState.INSUFFICIENT_EVIDENCE
    assert any("guide-seeking" in n for n in result.gate_notes)


def test_gate_allows_guide_seeking_with_disclosure_when_guide_cards_present():
    """guide_misrouted_text disclosure + guide_section_card present → allow (cards exist)."""
    bundle = _bundle(
        entity_code="D554",
        anomaly_disclosures=[_guide_misrouted_disclosure()],
        artifacts=[
            _artifact(entity_code="D554", artifact_type="course_card"),
            _artifact(entity_code="D554", artifact_type="guide_section_card"),
        ],
    )
    result = check_answerability(bundle, guide_seeking_intent=True)
    assert result.answerable is True


def test_gate_allows_non_guide_query_with_disclosure():
    """generic query (guide_seeking_intent=False) + disclosure → allow (check 6b does not fire)."""
    bundle = _bundle(
        entity_code="D554",
        anomaly_disclosures=[_guide_misrouted_disclosure()],
        artifacts=[_artifact(entity_code="D554", artifact_type="course_card")],
    )
    result = check_answerability(bundle, guide_seeking_intent=False)
    assert result.answerable is True
