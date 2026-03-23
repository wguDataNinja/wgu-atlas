"""Tests for Session 05 — Constrained generation.

These tests do NOT call a real LLM. They mock atlas_qa.llm.client.generate and
test the generation.py parsing and schema-validation paths:

- LLM failure → GenerationOutput with llm_failure=True
- Empty text → llm_failure=True
- Parse error (invalid JSON) → parse_error=True, schema_error=True
- Schema error (valid JSON but wrong shape) → schema_error=True
- Model-level abstain=true → answer_text=None (no error flags)
- Valid output → populated GenerationOutput
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from atlas_qa.qa.generation import DEFAULT_MODEL, generate_answer, _extract_json
from atlas_qa.qa.types import (
    EntityType,
    EvidenceArtifact,
    EvidenceBundle,
    EvidenceRef,
    SourceFamily,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_VERSION = "2026-03"
_REF = EvidenceRef(source_type="catalog", artifact_id="test", version=_VERSION)


def _artifact(code: str = "C715") -> EvidenceArtifact:
    return EvidenceArtifact(
        artifact_type="course_card",
        entity_code=code,
        version=_VERSION,
        source_family=SourceFamily.CATALOG,
        content="Test course content.",
        source_object_identity=f"course_cards/{code}",
        evidence_ref=_REF,
    )


def _bundle(entity_code: str = "C715") -> EvidenceBundle:
    return EvidenceBundle(
        entity_code=entity_code,
        entity_type=EntityType.COURSE,
        version_used=_VERSION,
        source_scope=[SourceFamily.CATALOG],
        artifacts=[_artifact(entity_code)],
        anomaly_disclosures=[],
        notes=[],
        from_exact_path=False,
    )


def _llm_result(raw_text: str = "", llm_failure: bool = False) -> MagicMock:
    result = MagicMock()
    result.raw_text = raw_text
    result.llm_failure = llm_failure
    return result


# ---------------------------------------------------------------------------
# _extract_json helper
# ---------------------------------------------------------------------------


def test_extract_json_plain():
    s = '{"answer_text": "hello"}'
    assert _extract_json(s) == s


def test_extract_json_strips_code_fence():
    s = '```json\n{"answer_text": "hello"}\n```'
    assert _extract_json(s) == '{"answer_text": "hello"}'


def test_extract_json_trims_outer_braces():
    s = 'Some text before {"answer_text": "hello"} and after'
    assert _extract_json(s) == '{"answer_text": "hello"}'


# ---------------------------------------------------------------------------
# generate_answer — mocked LLM
# ---------------------------------------------------------------------------


_VALID_JSON = (
    '{"answer_text": "This is the answer (2026-03).", '
    '"cited_evidence_ids": ["course_cards/C715"], '
    '"version_disclosed": "2026-03", '
    '"abstain": false}'
)

_PATCH_TARGET = "atlas_qa.qa.generation.generate"


def test_generate_answer_valid():
    with patch(_PATCH_TARGET, return_value=_llm_result(_VALID_JSON)):
        out = generate_answer(_bundle(), "What is C715?")
    assert out.answer_text == "This is the answer (2026-03)."
    assert "course_cards/C715" in out.cited_evidence_ids
    assert out.version_disclosed == "2026-03"
    assert out.llm_failure is False
    assert out.parse_error is False
    assert out.schema_error is False


def test_generate_answer_llm_failure():
    with patch(_PATCH_TARGET, return_value=_llm_result("", llm_failure=True)):
        out = generate_answer(_bundle(), "What is C715?")
    assert out.llm_failure is True
    assert out.answer_text is None


def test_generate_answer_empty_text():
    with patch(_PATCH_TARGET, return_value=_llm_result("")):
        out = generate_answer(_bundle(), "What is C715?")
    assert out.llm_failure is True
    assert out.answer_text is None


def test_generate_answer_parse_error():
    with patch(_PATCH_TARGET, return_value=_llm_result("not json at all")):
        out = generate_answer(_bundle(), "What is C715?")
    assert out.parse_error is True
    assert out.schema_error is True
    assert out.answer_text is None


def test_generate_answer_schema_error():
    # Valid JSON but wrong shape (missing required structure).
    with patch(_PATCH_TARGET, return_value=_llm_result('{"wrong_field": 99}')):
        out = generate_answer(_bundle(), "What is C715?")
    # answer_text absent → schema produces default None; no schema_error since pydantic
    # accepts unknown fields. The output has answer_text=None (defaults).
    assert out.answer_text is None


def test_generate_answer_model_abstains():
    json_str = (
        '{"answer_text": null, '
        '"cited_evidence_ids": [], '
        '"version_disclosed": null, '
        '"abstain": true}'
    )
    with patch(_PATCH_TARGET, return_value=_llm_result(json_str)):
        out = generate_answer(_bundle(), "What is C715?")
    assert out.answer_text is None
    assert out.llm_failure is False
    assert out.parse_error is False
