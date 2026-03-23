"""Deterministic Reciprocal Rank Fusion (RRF) for Session 04.

Merges lexical and embedding candidate lists without using model judgment.
Pure function — no LLM calls, no scope decisions.

Session 04 implementation.
"""
from __future__ import annotations

from atlas_qa.qa.types import RetrievalCandidate

# RRF constant — standard choice from literature; higher k reduces the weight
# of top-ranked candidates and smooths the fusion.
RRF_K = 60

MAX_FUSED_CANDIDATES = 10


def rrf_fuse(
    lexical: list[RetrievalCandidate],
    embedding: list[RetrievalCandidate],
    top_k: int = MAX_FUSED_CANDIDATES,
) -> list[RetrievalCandidate]:
    """Fuse lexical and embedding candidate lists using Reciprocal Rank Fusion.

    Each candidate's RRF score is the sum of 1/(k + rank) across all lists
    it appears in, where rank is 1-indexed.

    Candidates are identified by source_object_identity. When a candidate
    appears in both lists, both ranks contribute to its RRF score.

    Returns a new list of RetrievalCandidate objects with rank_fused set.
    score is set to the RRF score (for diagnostics; not a probability).
    """
    if not lexical and not embedding:
        return []

    # If only one list, just re-rank it
    if not embedding:
        return [
            c.model_copy(update={"rank_fused": c.rank_lexical or i + 1})
            for i, c in enumerate(lexical[:top_k])
        ]
    if not lexical:
        return [
            c.model_copy(update={"rank_fused": c.rank_embedding or i + 1})
            for i, c in enumerate(embedding[:top_k])
        ]

    # Build identity → candidate map (prefer lexical for shared candidates)
    candidates_by_id: dict[str, RetrievalCandidate] = {}
    for c in embedding:
        candidates_by_id[c.source_object_identity] = c
    for c in lexical:
        candidates_by_id[c.source_object_identity] = c  # lexical wins on merge

    # Build rank maps
    lexical_rank: dict[str, int] = {
        c.source_object_identity: (c.rank_lexical or i + 1)
        for i, c in enumerate(lexical)
    }
    embedding_rank: dict[str, int] = {
        c.source_object_identity: (c.rank_embedding or i + 1)
        for i, c in enumerate(embedding)
    }

    all_ids = set(lexical_rank) | set(embedding_rank)

    rrf_scores: dict[str, float] = {}
    for identity in all_ids:
        score = 0.0
        if identity in lexical_rank:
            score += 1.0 / (RRF_K + lexical_rank[identity])
        if identity in embedding_rank:
            score += 1.0 / (RRF_K + embedding_rank[identity])
        rrf_scores[identity] = score

    sorted_ids = sorted(all_ids, key=lambda i: rrf_scores[i], reverse=True)

    results: list[RetrievalCandidate] = []
    for fused_rank, identity in enumerate(sorted_ids[:top_k], start=1):
        base = candidates_by_id[identity]
        results.append(base.model_copy(update={
            "score": rrf_scores[identity],
            "rank_fused": fused_rank,
        }))

    return results
