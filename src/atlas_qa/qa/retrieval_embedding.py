"""Embedding-based retrieval within partition-scoped candidate pool.

Document embeddings are precomputed and stored under data/atlas_qa/embeddings/.
Query embeddings are computed on demand.

Fails gracefully (returns empty candidates) if:
- sentence-transformers is not installed
- embeddings file does not exist
- any runtime error occurs during embedding computation

Precomputation is emitted as a manual operator command (see DEV_LOG.md).

Session 04 implementation.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

from atlas_qa.qa.retrieval_lexical import (
    _build_doc_pool,
    _course_card_text,
    _guide_section_card_text,
    _program_card_text,
    _version_diff_card_text,
)
from atlas_qa.qa.types import (
    CourseCard,
    FuzzyRetrievalRequest,
    GuideSectionCard,
    PartitionStatus,
    ProgramVersionCard,
    RetrievalCandidate,
    VersionDiffCard,
)

logger = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).parents[3] / "data" / "atlas_qa"
_EMBEDDINGS_DIR = _DATA_DIR / "embeddings"

DEFAULT_EMBED_MODEL = "all-MiniLM-L6-v2"
MAX_EMBEDDING_CANDIDATES = 10


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Pure-Python cosine similarity (used when numpy unavailable)."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _cosine_similarity_numpy(a: "np.ndarray", b: "np.ndarray") -> float:
    norm_a = float((a * a).sum() ** 0.5)
    norm_b = float((b * b).sum() ** 0.5)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float((a * b).sum()) / (norm_a * norm_b)


def _load_precomputed_embeddings(
    model_name: str = DEFAULT_EMBED_MODEL,
) -> dict[str, list[float]] | None:
    """Load precomputed embeddings from disk.

    Returns None if the file does not exist or cannot be parsed.
    Keys are source_object_identity strings; values are embedding vectors.
    """
    embed_file = _EMBEDDINGS_DIR / f"{model_name.replace('/', '_')}_embeddings.json"
    if not embed_file.exists():
        logger.debug(
            "Embedding file not found: %s — embedding retrieval disabled. "
            "Run precomputation command from DEV_LOG.md to enable.",
            embed_file,
        )
        return None
    try:
        return json.loads(embed_file.read_text())
    except Exception as exc:
        logger.warning("Failed to load embeddings from %s: %s", embed_file, exc)
        return None


def _embed_query(query: str, model_name: str) -> list[float] | None:
    """Compute a query embedding using sentence-transformers.

    Returns None if sentence-transformers is not installed or fails.
    """
    try:
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415
    except ImportError:
        logger.debug(
            "sentence-transformers not installed — embedding retrieval disabled. "
            "Install with: pip install sentence-transformers numpy"
        )
        return None

    try:
        model = SentenceTransformer(model_name)
        vec = model.encode(query, convert_to_numpy=True)
        return list(float(x) for x in vec)
    except Exception as exc:
        logger.warning("Query embedding failed: query=%r error=%s", query, exc)
        return None


def embedding_retrieve(
    request: FuzzyRetrievalRequest,
    course_cards: dict[str, CourseCard],
    program_cards: dict[str, ProgramVersionCard],
    guide_section_cards: list[GuideSectionCard],
    version_diff_cards: list[VersionDiffCard],
    model_name: str = DEFAULT_EMBED_MODEL,
    top_k: int = MAX_EMBEDDING_CANDIDATES,
) -> list[RetrievalCandidate]:
    """Run embedding retrieval over the scoped document pool.

    Returns a ranked list of RetrievalCandidate objects. Returns empty list
    on any failure (missing embeddings, missing package, runtime error).

    Scope enforcement: the document pool is derived from the same partition
    as lexical retrieval — no broadening occurs.
    """
    if request.partition.status != PartitionStatus.OK:
        return []

    precomputed = _load_precomputed_embeddings(model_name)
    if precomputed is None:
        return []

    query_vec = _embed_query(request.raw_query, model_name)
    if query_vec is None:
        return []

    pool = _build_doc_pool(
        request, course_cards, program_cards, guide_section_cards, version_diff_cards
    )

    if not pool:
        return []

    # Try numpy for faster cosine similarity
    try:
        import numpy as np  # noqa: PLC0415
        q = np.array(query_vec, dtype=float)
        use_numpy = True
    except ImportError:
        use_numpy = False

    scored: list[tuple[float, RetrievalCandidate]] = []
    for candidate in pool:
        doc_vec = precomputed.get(candidate.source_object_identity)
        if doc_vec is None:
            continue
        if use_numpy:
            d = np.array(doc_vec, dtype=float)
            sim = _cosine_similarity_numpy(q, d)
        else:
            sim = _cosine_similarity(query_vec, doc_vec)
        scored.append((sim, candidate))

    scored.sort(key=lambda x: x[0], reverse=True)

    results: list[RetrievalCandidate] = []
    for rank, (score, candidate) in enumerate(scored[:top_k], start=1):
        candidate = candidate.model_copy(update={"score": float(score), "rank_embedding": rank})
        results.append(candidate)

    return results


# ---------------------------------------------------------------------------
# Precomputation entry point (operator-run only)
# ---------------------------------------------------------------------------


def precompute_embeddings(
    model_name: str = DEFAULT_EMBED_MODEL,
    output_dir: Path | None = None,
) -> None:
    """Precompute and persist document embeddings for all canonical artifacts.

    This function is intended for manual operator execution only.
    It is NOT called automatically by the retrieval layer.

    Usage (from repo root):
        python -m atlas_qa.qa.retrieval_embedding --precompute \\
            --model all-MiniLM-L6-v2 \\
            --output data/atlas_qa/embeddings/

    See DEV_LOG.md for the full manual operator command.
    """
    try:
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415
    except ImportError:
        raise RuntimeError(
            "sentence-transformers not installed. "
            "Run: pip install sentence-transformers numpy"
        ) from None

    from atlas_qa.qa.loaders import (
        get_course_cards,
        get_guide_section_cards,
        get_program_version_cards,
        get_version_diff_cards,
    )

    if output_dir is None:
        output_dir = _EMBEDDINGS_DIR
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    course_cards = get_course_cards()
    program_cards = get_program_version_cards()
    guide_sections = get_guide_section_cards()
    diff_cards = get_version_diff_cards()

    docs: list[tuple[str, str]] = []  # (source_object_identity, text)

    for code, card in course_cards.items():
        docs.append((f"course_cards/{code}", _course_card_text(card)))

    for code, card in program_cards.items():
        docs.append((f"program_version_cards/{code}", _program_card_text(card)))

    for card in guide_sections:
        identity = f"guide_section_cards/{card.program_code}/{card.guide_version}/{card.section_type}"
        docs.append((identity, _guide_section_card_text(card)))

    for card in diff_cards:
        identity = f"version_diff_cards/{card.entity_id}/{card.from_version}_{card.to_version}"
        docs.append((identity, _version_diff_card_text(card)))

    model = SentenceTransformer(model_name)
    texts = [text for _, text in docs]
    identities = [ident for ident, _ in docs]

    print(f"Encoding {len(texts)} documents with {model_name}…")
    vectors = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    result = {ident: list(float(x) for x in vec) for ident, vec in zip(identities, vectors)}

    out_file = output_dir / f"{model_name.replace('/', '_')}_embeddings.json"
    out_file.write_text(json.dumps(result))
    print(f"Embeddings written to {out_file} ({len(result)} entries)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Atlas QA embedding precomputation")
    parser.add_argument("--precompute", action="store_true")
    parser.add_argument("--model", default=DEFAULT_EMBED_MODEL)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.precompute:
        out = Path(args.output) if args.output else None
        precompute_embeddings(model_name=args.model, output_dir=out)
    else:
        parser.print_help()
