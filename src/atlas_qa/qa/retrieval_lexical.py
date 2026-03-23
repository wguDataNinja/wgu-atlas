"""BM25 lexical retrieval within partition-scoped candidate pool.

Operates strictly inside the scopes provided by Session 03 partition outputs.
Never broadens entity, version, source, or section scope.

Session 04 implementation.
"""
from __future__ import annotations

import re
from typing import Sequence

from atlas_qa.qa.types import (
    CourseCard,
    FuzzyRetrievalRequest,
    GuideSectionCard,
    PartitionResult,
    PartitionStatus,
    ProgramVersionCard,
    RetrievalCandidate,
    SourceFamily,
    VersionDiffCard,
)

_TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")

# Maximum candidates returned from lexical retrieval
MAX_LEXICAL_CANDIDATES = 10


def _tokenize(text: str) -> list[str]:
    """Simple whitespace/punctuation tokenizer for BM25."""
    return _TOKEN_RE.findall(text.lower())


def _course_card_text(card: CourseCard) -> str:
    parts = [
        card.course_code,
        card.canonical_title,
        card.catalog_description or "",
    ]
    for variant in card.title_variants:
        parts.append(variant)
    for cv in card.competency_variants:
        parts.extend(cv.bullets)
    for gda in card.guide_description_alternates:
        parts.append(gda.description_text)
    return " ".join(p for p in parts if p)


def _program_card_text(card: ProgramVersionCard) -> str:
    parts = [
        card.program_code,
        card.degree_title,
        card.college,
        card.version,
    ]
    return " ".join(p for p in parts if p)


def _guide_section_card_text(card: GuideSectionCard) -> str:
    parts = [
        card.program_code,
        card.guide_version,
        card.section_type,
    ]
    # Include linked course codes
    parts.extend(card.linked_course_codes)
    # Include section_data values (flatten shallow dict)
    for v in card.section_data.values():
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, str):
                    parts.append(item)
    return " ".join(p for p in parts if p)


def _version_diff_card_text(card: VersionDiffCard) -> str:
    parts = [
        card.entity_type,
        card.entity_id,
        card.from_version,
        card.to_version,
    ]
    parts.extend(card.added)
    parts.extend(card.removed)
    for ch in card.changed:
        if isinstance(ch, dict):
            for v in ch.values():
                if isinstance(v, str):
                    parts.append(v)
    return " ".join(p for p in parts if p)


def _build_doc_pool(
    request: FuzzyRetrievalRequest,
    course_cards: dict[str, CourseCard],
    program_cards: dict[str, ProgramVersionCard],
    guide_section_cards: list[GuideSectionCard],
    version_diff_cards: list[VersionDiffCard],
) -> list[RetrievalCandidate]:
    """Build the scoped document pool for lexical indexing.

    Only includes artifacts within the hard scopes from the PartitionResult.
    """
    partition = request.partition
    pool: list[RetrievalCandidate] = []

    # --- Course cards ---
    if SourceFamily.CATALOG in partition.source_scope:
        for code, card in course_cards.items():
            pool.append(RetrievalCandidate(
                artifact_type="course_card",
                entity_code=code,
                version=card.catalog_description_version,
                source_family=SourceFamily.CATALOG,
                content_text=_course_card_text(card),
                source_object_identity=f"course_cards/{code}",
            ))

    # --- Program version cards ---
    if SourceFamily.CATALOG in partition.source_scope:
        for code, card in program_cards.items():
            pool.append(RetrievalCandidate(
                artifact_type="program_version_card",
                entity_code=code,
                version=card.version,
                source_family=SourceFamily.CATALOG,
                content_text=_program_card_text(card),
                source_object_identity=f"program_version_cards/{code}",
            ))

    # --- Guide section cards ---
    if SourceFamily.GUIDE in partition.source_scope:
        for card in guide_section_cards:
            pool.append(RetrievalCandidate(
                artifact_type="guide_section_card",
                entity_code=card.program_code,
                version=card.guide_version,
                source_family=SourceFamily.GUIDE,
                content_text=_guide_section_card_text(card),
                source_object_identity=(
                    f"guide_section_cards/{card.program_code}/{card.guide_version}/{card.section_type}"
                ),
            ))

    # --- Version diff cards (compare mode only) ---
    if partition.compare_mode:
        for card in version_diff_cards:
            if card.entity_id in partition.entity_codes:
                pool.append(RetrievalCandidate(
                    artifact_type="version_diff_card",
                    entity_code=card.entity_id,
                    version=card.to_version,
                    source_family=SourceFamily.CATALOG,
                    content_text=_version_diff_card_text(card),
                    source_object_identity=(
                        f"version_diff_cards/{card.entity_id}/{card.from_version}_{card.to_version}"
                    ),
                ))

    return pool


def lexical_retrieve(
    request: FuzzyRetrievalRequest,
    course_cards: dict[str, CourseCard],
    program_cards: dict[str, ProgramVersionCard],
    guide_section_cards: list[GuideSectionCard],
    version_diff_cards: list[VersionDiffCard],
    top_k: int = MAX_LEXICAL_CANDIDATES,
) -> list[RetrievalCandidate]:
    """Run BM25 retrieval over the scoped document pool.

    Returns a ranked list of RetrievalCandidate objects. Returns empty list
    if the pool is empty or the query tokenizes to nothing.

    Scope enforcement: all documents in the pool are already within the
    hard scopes from the partition. No broadening occurs here.
    """
    from rank_bm25 import BM25Okapi

    if request.partition.status != PartitionStatus.OK:
        return []

    pool = _build_doc_pool(
        request, course_cards, program_cards, guide_section_cards, version_diff_cards
    )

    if not pool:
        return []

    query_tokens = _tokenize(request.raw_query)
    if not query_tokens:
        return []

    corpus_tokens = [_tokenize(doc.content_text) for doc in pool]
    bm25 = BM25Okapi(corpus_tokens)
    scores = bm25.get_scores(query_tokens)

    # Pair with candidates and rank
    scored = sorted(
        zip(scores, pool),
        key=lambda x: x[0],
        reverse=True,
    )

    results: list[RetrievalCandidate] = []
    for rank, (score, candidate) in enumerate(scored[:top_k], start=1):
        candidate = candidate.model_copy(update={"score": float(score), "rank_lexical": rank})
        results.append(candidate)

    return results
