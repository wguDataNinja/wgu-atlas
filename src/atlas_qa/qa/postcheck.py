"""Deterministic post-check for Atlas QA Session 05.

Verifies a GenerationOutput against the EvidenceBundle before any answer is
emitted. All checks are structural — no model calls.

If any check fails, PostCheckResult.passed is False and the answer path must
return an abstention rather than emitting the unchecked answer text.
"""
from __future__ import annotations

from atlas_qa.qa.types import EvidenceBundle, GenerationOutput, PostCheckResult


def post_check(
    gen_output: GenerationOutput,
    bundle: EvidenceBundle,
) -> PostCheckResult:
    """Run deterministic checks on a GenerationOutput.

    Checks:
    1. Schema valid: GenerationOutput has no parse_error or schema_error.
    2. Citation IDs present: at least one source_object_identity from the bundle
       appears in gen_output.cited_evidence_ids or in the answer_text.
    3. Version token present: bundle.version_used appears in the answer_text.

    Returns PostCheckResult with passed=True only if all three pass.
    """
    failure_reasons: list[str] = []

    # 1. Schema validity — parse/schema errors already detected in generation.py.
    schema_valid = not gen_output.parse_error and not gen_output.schema_error and not gen_output.llm_failure
    if not schema_valid:
        failure_reasons.append("generation output failed schema validation or LLM call failed")

    # 2. Citation IDs present.
    bundle_ids = {a.source_object_identity for a in bundle.artifacts}
    cited = set(gen_output.cited_evidence_ids)
    answer_text = gen_output.answer_text or ""

    citation_ids_present = bool(
        # At least one bundle ID in the cited list, OR at least one appears in answer text.
        (cited & bundle_ids)
        or any(bid in answer_text for bid in bundle_ids)
    )
    if not citation_ids_present:
        failure_reasons.append(
            f"no bundle source_object_identity found in cited_evidence_ids or answer_text "
            f"(bundle IDs: {sorted(bundle_ids)})"
        )

    # 3. Version token present in answer text.
    version_token = bundle.version_used
    version_token_present = bool(version_token and version_token in answer_text)
    if not version_token_present:
        failure_reasons.append(
            f"version token '{version_token}' not found in answer_text"
        )

    passed = schema_valid and citation_ids_present and version_token_present

    return PostCheckResult(
        passed=passed,
        citation_ids_present=citation_ids_present,
        version_token_present=version_token_present,
        schema_valid=schema_valid,
        failure_reasons=failure_reasons,
    )
