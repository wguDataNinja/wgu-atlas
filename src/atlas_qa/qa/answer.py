"""End-to-end answer orchestrator for Atlas QA Session 05.

Wires together evidence bundle construction, answerability gate, constrained
generation, and post-check into a single typed QAResponse.

Fail-closed at every step — explicit abstention states are returned for all
failure modes. No unchecked answer text is ever emitted.

Accepts either:
- (raw_query, RetrievalResult)  — fuzzy path
- (raw_query, ExactLookupAnswer) — exact path

Compare-mode inputs are rejected. Session 06 handles Class D queries.
"""
from __future__ import annotations

import re

from atlas_qa.qa.evidence import bundle_from_exact, bundle_from_retrieval
from atlas_qa.qa.gate import check_answerability
from atlas_qa.qa.generation import DEFAULT_MODEL, generate_answer
from atlas_qa.qa.postcheck import post_check
from atlas_qa.qa.types import (
    AbstentionState,
    EvidenceBundle,
    ExactLookupAnswer,
    QAResponse,
    RetrievalResult,
    SectionScope,
)

# Keyword pattern that indicates the user is explicitly asking about guide content.
# Used to distinguish guide-seeking queries from generic entity queries when
# the guide_misrouted_text anomaly is present.
_GUIDE_SEEKING_RE = re.compile(
    r"\bprogram\s+guide\b|\bguide\s+description\b|\bguide\s+say[s]?\b",
    re.IGNORECASE,
)


def answer_from_retrieval(
    retrieval_result: RetrievalResult,
    section_scope: SectionScope | None = None,
    model_name: str = DEFAULT_MODEL,
) -> QAResponse:
    """Produce a QAResponse from a fuzzy RetrievalResult.

    Full pipeline: bundle → gate → generate → post-check.
    Returns abstention at any failure point.
    """
    raw_query = retrieval_result.raw_query

    # Step 1 — Evidence bundle construction.
    bundle_or_abstain = bundle_from_retrieval(retrieval_result)
    if isinstance(bundle_or_abstain, QAResponse):
        return bundle_or_abstain   # abstention already formed
    bundle: EvidenceBundle = bundle_or_abstain

    return _run_pipeline(raw_query, bundle, section_scope, model_name)


def answer_from_exact(
    raw_query: str,
    exact_answer: ExactLookupAnswer,
    section_scope: SectionScope | None = None,
    model_name: str = DEFAULT_MODEL,
) -> QAResponse:
    """Produce a QAResponse from an ExactLookupAnswer.

    Full pipeline: bundle → gate → generate → post-check.
    Returns abstention at any failure point.
    """
    # Step 1 — Evidence bundle construction from exact answer.
    bundle_or_abstain = bundle_from_exact(exact_answer)
    if isinstance(bundle_or_abstain, QAResponse):
        return bundle_or_abstain
    bundle: EvidenceBundle = bundle_or_abstain

    return _run_pipeline(raw_query, bundle, section_scope, model_name)


# ---------------------------------------------------------------------------
# Shared pipeline
# ---------------------------------------------------------------------------


def _run_pipeline(
    raw_query: str,
    bundle: EvidenceBundle,
    section_scope: SectionScope | None,
    model_name: str,
) -> QAResponse:
    """Run the gate → generate → post-check pipeline over a pre-built bundle."""

    # Step 2 — Answerability gate.
    guide_seeking_intent = bool(_GUIDE_SEEKING_RE.search(raw_query))
    gate_result = check_answerability(
        bundle,
        section_scope=section_scope,
        guide_seeking_intent=guide_seeking_intent,
    )
    if not gate_result.answerable:
        return QAResponse(
            raw_query=raw_query,
            entity_code=bundle.entity_code,
            entity_type=bundle.entity_type,
            version_used=bundle.version_used,
            abstention=gate_result.abstention_reason or AbstentionState.INSUFFICIENT_EVIDENCE,
            answer_text=None,
            evidence_bundle=bundle,
            generation_output=None,
            postcheck=None,
            diagnostics={"gate_notes": gate_result.gate_notes},
        )

    # Step 3 — Constrained generation.
    try:
        gen_output = generate_answer(bundle, raw_query, model_name=model_name)
    except Exception as exc:
        return QAResponse(
            raw_query=raw_query,
            entity_code=bundle.entity_code,
            entity_type=bundle.entity_type,
            version_used=bundle.version_used,
            abstention=AbstentionState.INSUFFICIENT_EVIDENCE,
            answer_text=None,
            evidence_bundle=bundle,
            generation_output=None,
            postcheck=None,
            diagnostics={"generation_error": str(exc)},
        )

    if gen_output.llm_failure or gen_output.answer_text is None:
        return QAResponse(
            raw_query=raw_query,
            entity_code=bundle.entity_code,
            entity_type=bundle.entity_type,
            version_used=bundle.version_used,
            abstention=AbstentionState.INSUFFICIENT_EVIDENCE,
            answer_text=None,
            evidence_bundle=bundle,
            generation_output=gen_output,
            postcheck=None,
            diagnostics={"reason": "generation abstained or failed"},
        )

    # Step 4 — Post-check.
    postcheck_result = post_check(gen_output, bundle)
    if not postcheck_result.passed:
        return QAResponse(
            raw_query=raw_query,
            entity_code=bundle.entity_code,
            entity_type=bundle.entity_type,
            version_used=bundle.version_used,
            abstention=AbstentionState.INSUFFICIENT_EVIDENCE,
            answer_text=None,
            evidence_bundle=bundle,
            generation_output=gen_output,
            postcheck=postcheck_result,
            diagnostics={"postcheck_failures": postcheck_result.failure_reasons},
        )

    # All checks passed — emit the grounded answer.
    return QAResponse(
        raw_query=raw_query,
        entity_code=bundle.entity_code,
        entity_type=bundle.entity_type,
        version_used=bundle.version_used,
        abstention=None,
        answer_text=gen_output.answer_text,
        evidence_bundle=bundle,
        generation_output=gen_output,
        postcheck=postcheck_result,
        diagnostics={},
    )
