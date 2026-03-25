"""Tests for Session 05 — Deterministic post-check.

Covers:
- All three checks pass → passed=True.
- parse_error → schema_valid=False → passed=False.
- schema_error → schema_valid=False → passed=False.
- llm_failure → schema_valid=False → passed=False.
- Citation IDs absent from cited_evidence_ids and answer_text → passed=False.
- Citation IDs present only in answer_text (not cited list) → passed=True.
- Version token absent → passed=False.
- Multiple failure reasons accumulated.
"""
from __future__ import annotations

import pytest

from atlas_qa.qa.postcheck import post_check
from atlas_qa.qa.types import (
    EntityType,
    EvidenceArtifact,
    EvidenceBundle,
    EvidenceRef,
    GenerationOutput,
    PostCheckResult,
    SourceFamily,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_VERSION = "2026-03"
_IDENTITY = "course_cards/C715"
_REF = EvidenceRef(source_type="catalog", artifact_id="test", version=_VERSION)


def _artifact(identity: str = _IDENTITY) -> EvidenceArtifact:
    return EvidenceArtifact(
        artifact_type="course_card",
        entity_code="C715",
        version=_VERSION,
        source_family=SourceFamily.CATALOG,
        content="test",
        source_object_identity=identity,
        evidence_ref=_REF,
    )


def _bundle(artifacts: list[EvidenceArtifact] | None = None) -> EvidenceBundle:
    return EvidenceBundle(
        entity_code="C715",
        entity_type=EntityType.COURSE,
        version_used=_VERSION,
        source_scope=[SourceFamily.CATALOG],
        artifacts=artifacts or [_artifact()],
        anomaly_disclosures=[],
        notes=[],
        from_exact_path=False,
    )


def _gen(
    answer_text: str | None = None,
    cited: list[str] | None = None,
    version_disclosed: str | None = None,
    parse_error: bool = False,
    schema_error: bool = False,
    llm_failure: bool = False,
) -> GenerationOutput:
    return GenerationOutput(
        raw_text="raw",
        answer_text=answer_text,
        cited_evidence_ids=cited or [],
        version_disclosed=version_disclosed,
        parse_error=parse_error,
        schema_error=schema_error,
        llm_failure=llm_failure,
    )


# ---------------------------------------------------------------------------
# Passing case
# ---------------------------------------------------------------------------


def test_postcheck_passes():
    gen = _gen(
        answer_text=f"Answer citing {_IDENTITY}. Version {_VERSION}.",
        cited=[_IDENTITY],
        version_disclosed=_VERSION,
    )
    result = post_check(gen, _bundle())
    assert result.passed is True
    assert result.citation_ids_present is True
    assert result.version_token_present is True
    assert result.schema_valid is True
    assert result.failure_reasons == []


# ---------------------------------------------------------------------------
# Schema failures
# ---------------------------------------------------------------------------


def test_postcheck_fails_parse_error():
    gen = _gen(parse_error=True, schema_error=True)
    result = post_check(gen, _bundle())
    assert result.passed is False
    assert result.schema_valid is False


def test_postcheck_fails_schema_error():
    gen = _gen(schema_error=True)
    result = post_check(gen, _bundle())
    assert result.passed is False
    assert result.schema_valid is False


def test_postcheck_fails_llm_failure():
    gen = _gen(llm_failure=True)
    result = post_check(gen, _bundle())
    assert result.passed is False
    assert result.schema_valid is False


# ---------------------------------------------------------------------------
# Citation ID failures
# ---------------------------------------------------------------------------


def test_postcheck_fails_no_citation_ids():
    gen = _gen(
        answer_text=f"Answer without a citation. Version {_VERSION}.",
        cited=[],  # no IDs cited
        version_disclosed=_VERSION,
    )
    result = post_check(gen, _bundle())
    assert result.passed is False
    assert result.citation_ids_present is False


def test_postcheck_passes_citation_in_answer_text_only():
    # citation in the text, not in cited_evidence_ids list
    gen = _gen(
        answer_text=f"See {_IDENTITY} for details. Version {_VERSION}.",
        cited=[],
        version_disclosed=_VERSION,
    )
    result = post_check(gen, _bundle())
    assert result.citation_ids_present is True
    assert result.version_token_present is True
    assert result.passed is True


def test_postcheck_passes_citation_in_cited_list_only():
    gen = _gen(
        answer_text=f"Some answer. Version {_VERSION}.",
        cited=[_IDENTITY],
        version_disclosed=_VERSION,
    )
    result = post_check(gen, _bundle())
    assert result.citation_ids_present is True
    assert result.passed is True


# ---------------------------------------------------------------------------
# Version token failures
# ---------------------------------------------------------------------------


def test_postcheck_fails_version_absent():
    gen = _gen(
        answer_text="An answer without a version token.",
        cited=[_IDENTITY],
        version_disclosed=None,
    )
    result = post_check(gen, _bundle())
    assert result.passed is False
    assert result.version_token_present is False


def test_postcheck_passes_version_in_answer():
    gen = _gen(
        answer_text=f"Answer with version {_VERSION}.",
        cited=[_IDENTITY],
        version_disclosed=_VERSION,
    )
    result = post_check(gen, _bundle())
    assert result.version_token_present is True
    assert result.passed is True


# ---------------------------------------------------------------------------
# Multiple failures
# ---------------------------------------------------------------------------


def test_postcheck_multiple_failures():
    gen = _gen(
        answer_text="No citation, no version.",
        cited=[],
    )
    result = post_check(gen, _bundle())
    assert result.passed is False
    assert len(result.failure_reasons) >= 2


# ---------------------------------------------------------------------------
# Session 12 — entity-code fallback for empty cited_evidence_ids
# ---------------------------------------------------------------------------


def _artifact_prog(code: str = "MACCA") -> EvidenceArtifact:
    return EvidenceArtifact(
        artifact_type="program_version_card",
        entity_code=code,
        version=_VERSION,
        source_family=SourceFamily.CATALOG,
        content="test",
        source_object_identity=f"program_version_cards/{code}",
        evidence_ref=_REF,
    )


def _bundle_prog(code: str = "MACCA") -> EvidenceBundle:
    return EvidenceBundle(
        entity_code=code,
        entity_type=EntityType.PROGRAM,
        version_used=_VERSION,
        source_scope=[SourceFamily.CATALOG],
        artifacts=[_artifact_prog(code)],
        anomaly_disclosures=[],
        notes=[],
        from_exact_path=True,
    )


def test_postcheck_fallback_entity_code_in_answer():
    # cited_evidence_ids empty, but entity code "MACCA" appears in answer_text.
    # Single-artifact bundle → fallback fires → citation_ids_present=True.
    gen = _gen(
        answer_text=f"MACCA is the Master of Accounting program. As of version {_VERSION}.",
        cited=[],
        version_disclosed=_VERSION,
    )
    result = post_check(gen, _bundle_prog("MACCA"))
    assert result.citation_ids_present is True
    assert result.passed is True


def test_postcheck_fallback_entity_code_absent_from_answer():
    # cited_evidence_ids empty, entity code not mentioned → fallback does not fire.
    gen = _gen(
        answer_text=f"The program is an accounting master's degree. As of version {_VERSION}.",
        cited=[],
        version_disclosed=_VERSION,
    )
    result = post_check(gen, _bundle_prog("MACCA"))
    assert result.citation_ids_present is False
    assert result.passed is False


def test_postcheck_fallback_does_not_fire_for_two_artifact_bundle():
    # Two artifacts → fallback guard: len(non_none) == 1 fails → fallback does not fire.
    second = _artifact_prog("MACCF")
    bundle = EvidenceBundle(
        entity_code="MACCA",
        entity_type=EntityType.PROGRAM,
        version_used=_VERSION,
        source_scope=[SourceFamily.CATALOG],
        artifacts=[_artifact_prog("MACCA"), second],
        anomaly_disclosures=[],
        notes=[],
        from_exact_path=True,
    )
    gen = _gen(
        answer_text=f"MACCA and MACCF are both accounting programs. As of version {_VERSION}.",
        cited=[],
        version_disclosed=_VERSION,
    )
    result = post_check(gen, bundle)
    # Fallback must not fire; multi-artifact bundle falls through to original check.
    assert result.citation_ids_present is False
    assert result.passed is False


def test_postcheck_fallback_normal_citation_path_unchanged():
    # cited_evidence_ids contains the correct ID → original path wins, no fallback needed.
    gen = _gen(
        answer_text=f"MACCA is the program. As of version {_VERSION}.",
        cited=["program_version_cards/MACCA"],
        version_disclosed=_VERSION,
    )
    result = post_check(gen, _bundle_prog("MACCA"))
    assert result.citation_ids_present is True
    assert result.passed is True
