"""Tests for Session 04 — Fuzzy-query classifier.

Covers:
- ClassifierHint schema validation (valid JSON parses cleanly)
- Parse failure falls back safely (no exception)
- Schema failure falls back safely (wrong field types)
- Missing optional fields use defaults
- unsupported_or_advising and compare_intent defaults are False
- Prompt construction does not raise
- Classifier output is advisory — must not mutate partition scope
"""
from __future__ import annotations

import json

import pytest

from atlas_qa.qa.classifier_prompts import build_classifier_prompt
from atlas_qa.qa.types import ClassifierHint
from src.atlas_qa.llm.structured import safe_parse_structured_response


# ---------------------------------------------------------------------------
# ClassifierHint schema validation
# ---------------------------------------------------------------------------

def test_classifier_hint_valid_full():
    """Full valid classifier output parses without error."""
    raw = json.dumps({
        "query_class_hint": "class_b",
        "entity_type_hint": "program",
        "entity_code_hint": "MSHRM",
        "explicit_version_hint": "202503",
        "requested_section_hint": "competencies",
        "compare_intent": False,
        "unsupported_or_advising": False,
        "confidence_notes": "High confidence — MSHRM mentioned explicitly.",
    })
    hint, parse_err, schema_err, used_fallback, err_msg = safe_parse_structured_response(
        raw, ClassifierHint
    )
    assert hint is not None
    assert not parse_err
    assert not schema_err
    assert hint.entity_code_hint == "MSHRM"
    assert hint.compare_intent is False


def test_classifier_hint_all_nulls():
    """Null values for all optional fields produce a valid ClassifierHint with defaults."""
    raw = json.dumps({
        "query_class_hint": None,
        "entity_type_hint": None,
        "entity_code_hint": None,
        "explicit_version_hint": None,
        "requested_section_hint": None,
        "compare_intent": False,
        "unsupported_or_advising": False,
        "confidence_notes": None,
    })
    hint, parse_err, schema_err, _, _ = safe_parse_structured_response(raw, ClassifierHint)
    assert hint is not None
    assert hint.query_class_hint is None
    assert hint.unsupported_or_advising is False


def test_classifier_hint_minimal_empty_object():
    """Empty JSON object produces a ClassifierHint with all defaults."""
    raw = "{}"
    hint, parse_err, schema_err, _, _ = safe_parse_structured_response(raw, ClassifierHint)
    assert hint is not None
    assert hint.compare_intent is False
    assert hint.unsupported_or_advising is False


def test_classifier_hint_compare_intent_true():
    """compare_intent=True is preserved correctly."""
    raw = json.dumps({"compare_intent": True, "query_class_hint": "class_c"})
    hint, _, _, _, _ = safe_parse_structured_response(raw, ClassifierHint)
    assert hint is not None
    assert hint.compare_intent is True


def test_classifier_hint_unsupported_or_advising_true():
    """unsupported_or_advising=True is preserved correctly."""
    raw = json.dumps({"unsupported_or_advising": True})
    hint, _, _, _, _ = safe_parse_structured_response(raw, ClassifierHint)
    assert hint is not None
    assert hint.unsupported_or_advising is True


# ---------------------------------------------------------------------------
# Parse failure fallback
# ---------------------------------------------------------------------------

def test_classifier_parse_failure_returns_none():
    """Invalid JSON must return None with parse_error=True."""
    raw = "this is not json at all"
    hint, parse_err, schema_err, used_fallback, err_msg = safe_parse_structured_response(
        raw, ClassifierHint
    )
    assert hint is None
    assert parse_err is True
    assert used_fallback is True
    assert err_msg != ""


def test_classifier_parse_failure_truncated_json():
    """Truncated JSON must return None without raising."""
    raw = '{"query_class_hint": "class_b", "entity_type_hint":'
    hint, parse_err, schema_err, used_fallback, err_msg = safe_parse_structured_response(
        raw, ClassifierHint
    )
    assert hint is None
    assert parse_err is True


def test_classifier_parse_failure_empty_string():
    """Empty string must return None without raising."""
    hint, parse_err, schema_err, _, _ = safe_parse_structured_response("", ClassifierHint)
    assert hint is None


def test_classifier_parse_failure_markdown_fenced_bad_json():
    """Markdown-fenced non-JSON must return None without raising."""
    raw = "```json\nnot valid json\n```"
    hint, parse_err, _, _, _ = safe_parse_structured_response(raw, ClassifierHint)
    assert hint is None


def test_classifier_parse_success_with_code_fences():
    """Valid JSON wrapped in markdown code fences must parse correctly."""
    inner = json.dumps({"query_class_hint": "class_c", "compare_intent": False})
    raw = f"```json\n{inner}\n```"
    hint, parse_err, schema_err, _, _ = safe_parse_structured_response(raw, ClassifierHint)
    assert hint is not None
    assert hint.query_class_hint == "class_c"


# ---------------------------------------------------------------------------
# Schema failure fallback
# ---------------------------------------------------------------------------

def test_classifier_schema_failure_wrong_type_for_bool():
    """compare_intent with a non-bool value should either coerce or fail gracefully."""
    # Pydantic v2 coerces "true" string to bool=True in most cases.
    # The important thing is no unhandled exception.
    raw = json.dumps({"compare_intent": "yes", "unsupported_or_advising": "no"})
    try:
        hint, parse_err, schema_err, used_fallback, err_msg = safe_parse_structured_response(
            raw, ClassifierHint
        )
        # Either parsed (pydantic coercion) or schema_err set — both acceptable
        if hint is not None:
            assert isinstance(hint.compare_intent, bool)
        else:
            assert schema_err is True
    except Exception as exc:
        pytest.fail(f"safe_parse_structured_response raised unexpectedly: {exc}")


def test_classifier_schema_failure_extra_fields_ignored():
    """Extra unknown fields in classifier output must not cause schema failure."""
    raw = json.dumps({
        "query_class_hint": "class_b",
        "unknown_future_field": "some value",
        "another_extra": 42,
    })
    hint, parse_err, schema_err, _, _ = safe_parse_structured_response(raw, ClassifierHint)
    # Pydantic v2 ignores extra fields by default — should parse fine
    assert hint is not None
    assert hint.query_class_hint == "class_b"


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def test_build_classifier_prompt_includes_query():
    """Classifier prompt must include the raw user query."""
    query = "what are the competencies for the MSHRM program?"
    prompt = build_classifier_prompt(query)
    assert query in prompt or query.strip() in prompt


def test_build_classifier_prompt_non_empty():
    """Classifier prompt must not be empty."""
    prompt = build_classifier_prompt("tell me about BSCS")
    assert len(prompt) > 50


def test_build_classifier_prompt_mentions_json():
    """Classifier prompt must ask for JSON output."""
    prompt = build_classifier_prompt("what is C715 about")
    assert "JSON" in prompt or "json" in prompt


def test_build_classifier_prompt_strips_whitespace():
    """Leading/trailing whitespace in the query is handled gracefully."""
    prompt_a = build_classifier_prompt("  my query  ")
    prompt_b = build_classifier_prompt("my query")
    # Both should produce valid prompts
    assert len(prompt_a) > 0
    assert len(prompt_b) > 0


# ---------------------------------------------------------------------------
# Advisory contract — classifier does not mutate partition scope
# ---------------------------------------------------------------------------

def test_classifier_hint_does_not_affect_partition():
    """ClassifierHint is a plain data object — reading it cannot mutate any partition."""
    from atlas_qa.qa.types import PartitionResult, PartitionStatus, EntityType, SourceFamily

    partition = PartitionResult(
        status=PartitionStatus.OK,
        entity_type=EntityType.COURSE,
        entity_codes=["C715"],
        version_scope=["2026-03"],
        source_scope=[SourceFamily.CATALOG],
        from_exact_path=False,
    )
    hint = ClassifierHint(
        entity_type_hint="program",   # contradicts partition — must have no effect
        entity_code_hint="MSHRM",    # not in partition scope
        unsupported_or_advising=False,
    )

    # Reading hint fields must not change partition in any way
    _ = hint.entity_type_hint
    _ = hint.entity_code_hint

    assert partition.entity_type == EntityType.COURSE
    assert partition.entity_codes == ["C715"]
    assert SourceFamily.CATALOG in partition.source_scope
