"""Fuzzy retrieval orchestration for Session 04.

Entry point: retrieve(raw_query, partition_result) -> RetrievalResult

Execution path:
1. Validate partition is OK and not from the exact path.
2. Optionally classify the fuzzy query (advisory only).
3. Run scoped lexical retrieval (BM25).
4. Run scoped embedding retrieval (if precomputed embeddings exist).
5. Fuse lexical + embedding candidates deterministically (RRF).
6. Apply stop behavior if the candidate pool is unsafe.
7. Return typed RetrievalResult — no final answer generation.

Architecture invariants enforced here:
- Exact-path queries must not enter fuzzy retrieval (checked via from_exact_path).
- Partition must be OK before any retrieval runs.
- Model output (classifier) is advisory only and schema-validated.
- No answer generation — RetrievalResult contains candidates only.
- Empty/unsafe pools fail closed with explicit stop reason.

Session 04 implementation.
"""
from __future__ import annotations

import logging

from atlas_qa.qa.classifier import classify_fuzzy_query
from atlas_qa.qa.loaders import (
    get_course_cards,
    get_guide_section_cards,
    get_program_version_cards,
    get_version_diff_cards,
)
from atlas_qa.qa.retrieval_embedding import embedding_retrieve
from atlas_qa.qa.retrieval_fusion import rrf_fuse
from atlas_qa.qa.retrieval_lexical import lexical_retrieve
from atlas_qa.qa.types import (
    FuzzyRetrievalRequest,
    PartitionResult,
    PartitionStatus,
    RetrievalResult,
    RetrievalStopReason,
)

logger = logging.getLogger(__name__)

# Controls whether the classifier is invoked during orchestration.
# Set to False to run lexical-only retrieval (useful for testing without Ollama).
USE_CLASSIFIER = True

# Default number of candidates in the final selected set
DEFAULT_TOP_K = 5


def retrieve(
    raw_query: str,
    partition_result: PartitionResult,
    use_classifier: bool = USE_CLASSIFIER,
    top_k: int = DEFAULT_TOP_K,
    classifier_model: str = "llama3",
) -> RetrievalResult:
    """Run fuzzy retrieval for a non-exact NL query.

    Parameters
    ----------
    raw_query : str
        The original user query (not resolved on the exact path).
    partition_result : PartitionResult
        Upstream scope from Session 03 — binding. Must be status=OK.
    use_classifier : bool
        Whether to invoke the LLM classifier for advisory hints.
        Set False for deterministic-only mode (no LLM).
    top_k : int
        Number of candidates to include in selected_candidates.
    classifier_model : str
        Model name for the classifier (must be in MODEL_REGISTRY).

    Returns
    -------
    RetrievalResult
        Typed retrieval output suitable for Session 05 evidence-bundle construction.
        Never contains final answers.
    """
    # --- Invariant: partition must be OK ---
    if partition_result.status != PartitionStatus.OK:
        logger.warning(
            "retrieve() called with failed partition: reason=%s query=%r",
            partition_result.failure_reason,
            raw_query,
        )
        return RetrievalResult(
            raw_query=raw_query,
            stop_reason=RetrievalStopReason.PARTITION_FAILED,
            diagnostics={"failure_reason": str(partition_result.failure_reason)},
        )

    # --- Invariant: exact-path queries must not enter fuzzy retrieval ---
    if partition_result.from_exact_path:
        logger.warning(
            "retrieve() called with from_exact_path=True — exact queries must bypass fuzzy retrieval. query=%r",
            raw_query,
        )
        return RetrievalResult(
            raw_query=raw_query,
            stop_reason=RetrievalStopReason.PARTITION_FAILED,
            diagnostics={"note": "Exact-path queries must use Session 02 exact lookup."},
        )

    # --- Build fuzzy retrieval request ---
    request = FuzzyRetrievalRequest(raw_query=raw_query, partition=partition_result)

    # --- Optional classifier ---
    classifier_output = None
    parse_error = False
    schema_error = False
    used_fallback = False
    classifier_error_msg = ""

    if use_classifier:
        hint, parse_error, schema_error, used_fallback, classifier_error_msg = (
            classify_fuzzy_query(raw_query, model_name=classifier_model)
        )
        classifier_output = hint

        # Safety: if classifier says unsupported/advising, stop
        if classifier_output is not None and classifier_output.unsupported_or_advising:
            logger.info(
                "Classifier flagged query as unsupported/advising: query=%r",
                raw_query,
            )
            return RetrievalResult(
                raw_query=raw_query,
                request=request,
                stop_reason=RetrievalStopReason.CLASSIFIER_UNUSABLE_NO_FALLBACK,
                classifier_output=classifier_output,
                classifier_parse_error=parse_error,
                classifier_schema_error=schema_error,
                classifier_used_fallback=used_fallback,
                diagnostics={"classifier_note": "unsupported_or_advising flag set"},
            )

        # Update request with classifier hint
        request = request.model_copy(update={"classifier_hint": classifier_output})

    # --- Load scoped artifacts ---
    from atlas_qa.qa.scope_partitioning import (
        enforce_course_partition,
        enforce_guide_section_partition,
        enforce_program_partition,
    )

    all_course_cards = get_course_cards()
    all_program_cards = get_program_version_cards()
    all_guide_sections = get_guide_section_cards()
    all_diff_cards = get_version_diff_cards()

    scoped_courses = enforce_course_partition(partition_result, all_course_cards)
    scoped_programs = enforce_program_partition(partition_result, all_program_cards)
    scoped_guide_sections = enforce_guide_section_partition(partition_result, all_guide_sections)
    # Version diff cards scoped inside retrieval_lexical._build_doc_pool by entity_codes

    # --- Lexical retrieval ---
    lexical_candidates = lexical_retrieve(
        request,
        scoped_courses,
        scoped_programs,
        scoped_guide_sections,
        all_diff_cards,
    )

    # --- Embedding retrieval ---
    embedding_candidates = embedding_retrieve(
        request,
        scoped_courses,
        scoped_programs,
        scoped_guide_sections,
        all_diff_cards,
    )

    # --- Fusion ---
    fused_candidates = rrf_fuse(lexical_candidates, embedding_candidates, top_k=top_k * 2)

    # --- Select top-k ---
    selected = fused_candidates[:top_k] if fused_candidates else lexical_candidates[:top_k]

    # --- Stop behavior: empty pool ---
    if not selected:
        logger.info("Retrieval produced empty candidate pool: query=%r", raw_query)
        return RetrievalResult(
            raw_query=raw_query,
            request=request,
            stop_reason=RetrievalStopReason.EMPTY_CANDIDATE_POOL,
            classifier_output=classifier_output,
            classifier_parse_error=parse_error,
            classifier_schema_error=schema_error,
            classifier_used_fallback=used_fallback,
            lexical_candidates=lexical_candidates,
            embedding_candidates=embedding_candidates,
            fused_candidates=fused_candidates,
            selected_candidates=[],
            diagnostics={
                "classifier_error": classifier_error_msg,
                "scoped_course_count": len(scoped_courses),
                "scoped_program_count": len(scoped_programs),
                "scoped_guide_section_count": len(scoped_guide_sections),
            },
        )

    return RetrievalResult(
        raw_query=raw_query,
        request=request,
        stop_reason=None,
        classifier_output=classifier_output,
        classifier_parse_error=parse_error,
        classifier_schema_error=schema_error,
        classifier_used_fallback=used_fallback,
        lexical_candidates=lexical_candidates,
        embedding_candidates=embedding_candidates,
        fused_candidates=fused_candidates,
        selected_candidates=selected,
        diagnostics={
            "classifier_error": classifier_error_msg,
            "scoped_course_count": len(scoped_courses),
            "scoped_program_count": len(scoped_programs),
            "scoped_guide_section_count": len(scoped_guide_sections),
            "lexical_count": len(lexical_candidates),
            "embedding_count": len(embedding_candidates),
            "fused_count": len(fused_candidates),
        },
    )
