"""Constrained LLM generation for Atlas QA Session 05.

Calls the LLM with a strict prompt contract (from generation_prompts.py),
schema-validates the output, and returns a typed GenerationOutput.

On any failure (LLM failure, parse error, schema error, empty text, or model
returning abstain=true), returns a GenerationOutput with the appropriate error
flags set and answer_text=None.

No retry in the answer path — the spec requires abstention on first failure.
"""
from __future__ import annotations

import json

from pydantic import BaseModel, ValidationError

from atlas_qa.qa.generation_prompts import render_generation_prompt
from atlas_qa.qa.types import EvidenceBundle, GenerationOutput
from atlas_qa.llm.client import generate

# Default local model per session spec.
DEFAULT_MODEL = "llama3"

# ---------------------------------------------------------------------------
# Internal schema for model output validation
# ---------------------------------------------------------------------------


class _ModelOutput(BaseModel):
    answer_text: str | None = None
    cited_evidence_ids: list[str] = []
    version_disclosed: str | None = None
    abstain: bool = False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_answer(
    bundle: EvidenceBundle,
    question: str,
    model_name: str = DEFAULT_MODEL,
    _retried: bool = False,
) -> GenerationOutput:
    """Call the LLM with a strict prompt contract and return a typed GenerationOutput.

    Steps:
    1. Render the prompt from the evidence bundle.
    2. Call the LLM (via atlas_qa.llm.client.generate).
    3. Extract and validate the JSON output against _ModelOutput schema.
    4. Return GenerationOutput with populated fields or error flags.

    Post-check is NOT performed here — that belongs in postcheck.py.
    """
    prompt = render_generation_prompt(bundle, question)

    # Step 1 — LLM call.
    llm_result = generate(model_name, prompt)

    raw_text = llm_result.raw_text or ""

    if llm_result.llm_failure or not raw_text.strip():
        return GenerationOutput(
            raw_text=raw_text,
            answer_text=None,
            cited_evidence_ids=[],
            version_disclosed=None,
            parse_error=False,
            schema_error=False,
            llm_failure=True,
        )

    # Step 2 — Extract JSON block.
    json_text = _extract_json(raw_text)

    # Step 3 — Parse JSON.
    try:
        data = json.loads(json_text)
    except (json.JSONDecodeError, ValueError) as exc:
        return GenerationOutput(
            raw_text=raw_text,
            answer_text=None,
            cited_evidence_ids=[],
            version_disclosed=None,
            parse_error=True,
            schema_error=True,
            llm_failure=False,
        )

    # Step 4 — Schema validate.
    try:
        parsed = _ModelOutput(**data)
    except (ValidationError, TypeError):
        return GenerationOutput(
            raw_text=raw_text,
            answer_text=None,
            cited_evidence_ids=[],
            version_disclosed=None,
            parse_error=False,
            schema_error=True,
            llm_failure=False,
        )

    # Step 5 — Check model-level abstention.
    if parsed.abstain or not parsed.answer_text:
        # Retry once on clean model-level abstention for non-empty bundles.
        # Only retries when no parse/schema/LLM error occurred — the model cleanly
        # chose to abstain. Handles non-deterministic over-caution (e.g., B-018).
        if not _retried and bundle.artifacts:
            retry_result = generate_answer(bundle, question, model_name, _retried=True)
            return GenerationOutput(
                raw_text=retry_result.raw_text,
                answer_text=retry_result.answer_text,
                cited_evidence_ids=retry_result.cited_evidence_ids,
                version_disclosed=retry_result.version_disclosed,
                parse_error=retry_result.parse_error,
                schema_error=retry_result.schema_error,
                llm_failure=retry_result.llm_failure,
                retried=True,
            )
        return GenerationOutput(
            raw_text=raw_text,
            answer_text=None,
            cited_evidence_ids=parsed.cited_evidence_ids,
            version_disclosed=parsed.version_disclosed,
            parse_error=False,
            schema_error=False,
            llm_failure=False,
            retried=_retried,
        )

    return GenerationOutput(
        raw_text=raw_text,
        answer_text=parsed.answer_text,
        cited_evidence_ids=parsed.cited_evidence_ids,
        version_disclosed=parsed.version_disclosed,
        parse_error=False,
        schema_error=False,
        llm_failure=False,
        retried=_retried,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _extract_json(text: str) -> str:
    """Strip code fences and trim to outermost JSON object."""
    s = text.strip()
    if s.startswith("```"):
        lines = s.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    start = s.find("{")
    end = s.rfind("}")
    if start != -1 and end != -1 and end > start:
        return s[start:end + 1]
    return s
