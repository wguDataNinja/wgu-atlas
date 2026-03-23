"""Tests for Session 04 — Fuzzy Retrieval.

Covers:
- Wrong-version blocking under fuzzy retrieval
- Section-scope enforcement
- Source-scope enforcement (D554 guide block, C179 anomaly metadata)
- Empty-pool stop behavior
- Partition-failed propagation
- Exact-path rejection at fuzzy retrieval entry
- Mixed-version blocking without compare intent
- Lexical retrieval correctness within scope
- Fusion produces candidates with rank_fused set
- RetrievalResult typing completeness
"""
from __future__ import annotations

import pytest

from atlas_qa.qa.retrieval import retrieve
from atlas_qa.qa.retrieval_fusion import rrf_fuse
from atlas_qa.qa.retrieval_lexical import lexical_retrieve
from atlas_qa.qa.scope_partitioning import (
    derive_partition,
    enforce_course_partition,
    enforce_guide_section_partition,
    enforce_program_partition,
    from_partial_context,
)
from atlas_qa.qa.types import (
    AbstentionState,
    CertPrepSignal,
    CourseCard,
    EntityType,
    EvidenceRef,
    FuzzyRetrievalRequest,
    GuideSectionCard,
    GuideEnrichmentSummary,
    InstancesByVersion,
    PartitionResult,
    PartitionStatus,
    ProgramVersionCard,
    RetrievalCandidate,
    RetrievalStopReason,
    SectionScope,
    SourceFamily,
)

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

_EVIDENCE = [EvidenceRef(source_type="catalog", artifact_id="test", version="2026-03")]
_LONG_DESC = "This is a sufficiently long catalog description for testing purposes. " * 5


def _course(
    code: str,
    versions: list[str] | None = None,
    guide_available: bool = False,
    guide_misrouted: bool = False,
    cat_short_text: bool = False,
    description: str = _LONG_DESC,
) -> CourseCard:
    ivs = [InstancesByVersion(catalog_version=v, program_codes=[]) for v in (versions or ["2026-03"])]
    return CourseCard(
        course_code=code,
        canonical_title=f"Test Course {code}",
        canonical_cus="3",
        title_variants=[],
        catalog_description=description,
        catalog_description_version="2026-03",
        cat_short_text_flag=cat_short_text,
        guide_description_alternates=[],
        guide_misrouted_text_flag=guide_misrouted,
        competency_variants=[],
        competency_variant_count=0,
        cert_prep_signal=CertPrepSignal(
            status="not_found_in_observed_guides", label=None, guide_versions_observed=[]
        ),
        prerequisite_course_codes=[],
        is_prereq_for=[],
        program_codes=["BSCS"],
        instances_by_version=ivs,
        guide_enrichment_available=guide_available,
        guide_enrichment_summary=GuideEnrichmentSummary(
            has_guide_description_alternates=False,
            has_competencies=False,
            competency_variant_count=0,
            has_cert_prep_signal=False,
            program_count_with_guide_enrichment=0,
        ),
        version_conflict_programs=[],
        evidence_refs=_EVIDENCE,
    )


def _program(
    code: str,
    version: str = "202503",
    catalog_version: str = "2026-03",
    guide_version: str | None = "202503",
) -> ProgramVersionCard:
    return ProgramVersionCard(
        program_code=code,
        degree_title=f"Test Degree {code}",
        college="College of Test",
        version=version,
        is_latest=True,
        total_cus=120,
        catalog_version=catalog_version,
        course_codes=["C715", "D426"],
        section_presence={"has_standard_path": True},
        guide_version=guide_version,
        guide_pub_date="2025-03-01",
        evidence_refs=_EVIDENCE,
    )


def _guide_section(
    program_code: str,
    guide_version: str = "202503",
    section_type: str = "standard_path",
) -> GuideSectionCard:
    return GuideSectionCard(
        program_code=program_code,
        guide_version=guide_version,
        section_type=section_type,
        linked_course_codes=["C715", "D426"],
        section_data={"description": "Standard path for test program."},
        evidence_refs=_EVIDENCE,
    )


def _ok_partition(
    entity_codes: list[str],
    entity_type: EntityType,
    version_scope: list[str],
    source_scope: list[SourceFamily],
    section_scope: SectionScope | None = None,
    compare_mode: bool = False,
) -> PartitionResult:
    return PartitionResult(
        status=PartitionStatus.OK,
        entity_type=entity_type,
        entity_codes=entity_codes,
        version_scope=version_scope,
        source_scope=source_scope,
        section_scope=section_scope,
        compare_mode=compare_mode,
        from_exact_path=False,
    )


def _failed_partition(reason: AbstentionState) -> PartitionResult:
    return PartitionResult(
        status=PartitionStatus.FAILED,
        failure_reason=reason,
    )


# ---------------------------------------------------------------------------
# Partition-failed propagation
# ---------------------------------------------------------------------------

def test_retrieve_fails_on_partition_failed():
    partition = _failed_partition(AbstentionState.NOT_IN_CORPUS)
    result = retrieve("what are the competencies", partition, use_classifier=False)
    assert result.stop_reason == RetrievalStopReason.PARTITION_FAILED
    assert result.selected_candidates == []


def test_retrieve_rejects_exact_path_partition():
    """Exact-path partition (from_exact_path=True) must not enter fuzzy retrieval."""
    partition = PartitionResult(
        status=PartitionStatus.OK,
        entity_type=EntityType.COURSE,
        entity_codes=["C715"],
        version_scope=["2026-03"],
        source_scope=[SourceFamily.CATALOG],
        from_exact_path=True,
    )
    result = retrieve("C715 description", partition, use_classifier=False)
    assert result.stop_reason == RetrievalStopReason.PARTITION_FAILED


# ---------------------------------------------------------------------------
# Empty candidate pool
# ---------------------------------------------------------------------------

def test_retrieve_empty_pool_when_no_scoped_artifacts():
    """If scoped pool is empty, stop with EMPTY_CANDIDATE_POOL."""
    # Use an entity_code that doesn't exist in the (empty) card dicts
    partition = _ok_partition(
        entity_codes=["NONEXISTENT"],
        entity_type=EntityType.COURSE,
        version_scope=["2026-03"],
        source_scope=[SourceFamily.CATALOG],
    )
    result = retrieve("tell me about NONEXISTENT", partition, use_classifier=False)
    assert result.stop_reason == RetrievalStopReason.EMPTY_CANDIDATE_POOL
    assert result.selected_candidates == []


# ---------------------------------------------------------------------------
# Lexical retrieval scope enforcement
# ---------------------------------------------------------------------------

def test_lexical_retrieval_only_returns_scoped_courses():
    """Lexical retrieval must not return candidates outside entity_codes scope."""
    course_a = _course("C715", description="network security fundamentals and protocols")
    course_b = _course("D426", description="data management and database systems")
    course_cards = {"C715": course_a, "D426": course_b}

    partition = _ok_partition(
        entity_codes=["C715"],
        entity_type=EntityType.COURSE,
        version_scope=["2026-03"],
        source_scope=[SourceFamily.CATALOG],
    )
    request = FuzzyRetrievalRequest(raw_query="network security", partition=partition)

    candidates = lexical_retrieve(
        request,
        course_cards={"C715": course_a},   # only C715 in scoped set
        program_cards={},
        guide_section_cards=[],
        version_diff_cards=[],
    )

    assert all(c.entity_code == "C715" for c in candidates)
    assert not any(c.entity_code == "D426" for c in candidates)


def test_lexical_retrieval_ranks_relevant_doc_higher():
    """The course whose description matches the query should rank above an irrelevant one."""
    matching = _course(
        "C715",
        description="network security intrusion detection firewall protection protocols",
    )
    irrelevant = _course(
        "D426",
        description="spreadsheet formulas data entry pivot tables excel",
    )

    partition = _ok_partition(
        entity_codes=["C715", "D426"],
        entity_type=EntityType.COURSE,
        version_scope=["2026-03"],
        source_scope=[SourceFamily.CATALOG],
    )
    request = FuzzyRetrievalRequest(raw_query="network security", partition=partition)

    candidates = lexical_retrieve(
        request,
        course_cards={"C715": matching, "D426": irrelevant},
        program_cards={},
        guide_section_cards=[],
        version_diff_cards=[],
    )

    assert candidates, "Expected at least one candidate"
    assert candidates[0].entity_code == "C715", "Matching doc should rank first"


def test_lexical_retrieval_returns_empty_on_failed_partition():
    """lexical_retrieve must return empty list when partition is not OK."""
    partition = _failed_partition(AbstentionState.NOT_IN_CORPUS)
    request = FuzzyRetrievalRequest(raw_query="anything", partition=partition)

    candidates = lexical_retrieve(
        request,
        course_cards={"C715": _course("C715")},
        program_cards={},
        guide_section_cards=[],
        version_diff_cards=[],
    )
    assert candidates == []


# ---------------------------------------------------------------------------
# Source-scope enforcement
# ---------------------------------------------------------------------------

def test_guide_candidates_excluded_when_guide_not_in_source_scope():
    """When source_scope is [CATALOG], guide section cards must not appear in pool."""
    program = _program("BSCS", guide_version="202503")
    guide_sec = _guide_section("BSCS", guide_version="202503")

    partition = _ok_partition(
        entity_codes=["BSCS"],
        entity_type=EntityType.PROGRAM,
        version_scope=["202503"],
        source_scope=[SourceFamily.CATALOG],  # guide excluded
    )
    request = FuzzyRetrievalRequest(raw_query="areas of study BSCS", partition=partition)

    candidates = lexical_retrieve(
        request,
        course_cards={},
        program_cards={"BSCS": program},
        guide_section_cards=[guide_sec],
        version_diff_cards=[],
    )

    assert not any(c.artifact_type == "guide_section_card" for c in candidates)


def test_d554_guide_block_via_partition_source_scope():
    """D554's source scope must be CATALOG-only (guide excluded).

    The partition layer already enforces this; retrieval must not add guide candidates
    when the source_scope from partition does not include GUIDE.
    """
    d554 = _course("D554", guide_misrouted=True)
    # Simulate what partition would derive: catalog-only
    partition = _ok_partition(
        entity_codes=["D554"],
        entity_type=EntityType.COURSE,
        version_scope=["2026-03"],
        source_scope=[SourceFamily.CATALOG],  # guide blocked by partition
    )
    request = FuzzyRetrievalRequest(raw_query="advanced financial accounting", partition=partition)

    candidates = lexical_retrieve(
        request,
        course_cards={"D554": d554},
        program_cards={},
        guide_section_cards=[],
        version_diff_cards=[],
    )

    # All candidates must be catalog-scoped; no guide_section_card present
    assert all(c.source_family == SourceFamily.CATALOG for c in candidates)


def test_c179_anomaly_metadata_preserved_in_retrieval():
    """C179 must appear in retrieval candidates with its anomaly metadata accessible.

    The catalog short-text anomaly is encoded in the CourseCard.cat_short_text_flag.
    Retrieval must not suppress C179 from the candidate pool when it is in scope.
    """
    c179 = _course("C179", cat_short_text=True, description="Short text.")
    partition = _ok_partition(
        entity_codes=["C179"],
        entity_type=EntityType.COURSE,
        version_scope=["2026-03"],
        source_scope=[SourceFamily.CATALOG],
    )
    request = FuzzyRetrievalRequest(raw_query="C179 description", partition=partition)

    candidates = lexical_retrieve(
        request,
        course_cards={"C179": c179},
        program_cards={},
        guide_section_cards=[],
        version_diff_cards=[],
    )

    assert any(c.entity_code == "C179" for c in candidates), "C179 must appear in candidates"


# ---------------------------------------------------------------------------
# Version-scope (wrong-version blocking)
# ---------------------------------------------------------------------------

def test_lexical_retrieval_respects_version_scope_via_partition():
    """Program candidates from a non-scoped version must not appear.

    This is enforced by enforce_program_partition upstream; here we verify
    that the retrieval result only contains the version-scoped program.
    """
    prog_v1 = _program("BSCS", version="202409", catalog_version="2024-09", guide_version=None)
    prog_v2 = _program("BSCS", version="202503", catalog_version="2026-03", guide_version=None)

    all_programs = {"BSCS": prog_v2}  # only v2 is in scope (simulated by partition enforcement)

    partition = _ok_partition(
        entity_codes=["BSCS"],
        entity_type=EntityType.PROGRAM,
        version_scope=["202503"],
        source_scope=[SourceFamily.CATALOG],
    )
    request = FuzzyRetrievalRequest(raw_query="BSCS degree requirements", partition=partition)

    candidates = lexical_retrieve(
        request,
        course_cards={},
        program_cards=all_programs,
        guide_section_cards=[],
        version_diff_cards=[],
    )

    versions_seen = {c.version for c in candidates}
    assert "202409" not in versions_seen, "Out-of-scope version must not appear in candidates"


# ---------------------------------------------------------------------------
# Section-scope enforcement
# ---------------------------------------------------------------------------

def test_guide_section_returned_when_guide_in_source_scope():
    """Guide section cards must be returned when GUIDE is in source_scope."""
    program = _program("BSCS", guide_version="202503")
    guide_sec = _guide_section("BSCS", guide_version="202503", section_type="standard_path")

    partition = _ok_partition(
        entity_codes=["BSCS"],
        entity_type=EntityType.PROGRAM,
        version_scope=["202503"],
        source_scope=[SourceFamily.CATALOG, SourceFamily.GUIDE],
        section_scope=SectionScope.COMPETENCIES,
    )
    request = FuzzyRetrievalRequest(raw_query="competencies for BSCS", partition=partition)

    candidates = lexical_retrieve(
        request,
        course_cards={},
        program_cards={"BSCS": program},
        guide_section_cards=[guide_sec],
        version_diff_cards=[],
    )

    artifact_types = {c.artifact_type for c in candidates}
    assert "guide_section_card" in artifact_types


def test_guide_section_wrong_program_excluded():
    """Guide sections for out-of-scope programs must not appear."""
    guide_sec_bscs = _guide_section("BSCS", guide_version="202503")
    guide_sec_other = _guide_section("MBAPM", guide_version="202503")

    partition = _ok_partition(
        entity_codes=["BSCS"],
        entity_type=EntityType.PROGRAM,
        version_scope=["202503"],
        source_scope=[SourceFamily.CATALOG, SourceFamily.GUIDE],
    )
    request = FuzzyRetrievalRequest(raw_query="program structure", partition=partition)

    # Scoped enforcement happens upstream; simulate by only passing BSCS sections
    candidates = lexical_retrieve(
        request,
        course_cards={},
        program_cards={"BSCS": _program("BSCS")},
        guide_section_cards=[guide_sec_bscs],  # MBAPM already filtered by enforce_guide_section_partition
        version_diff_cards=[],
    )

    assert not any(c.entity_code == "MBAPM" for c in candidates)


# ---------------------------------------------------------------------------
# RRF fusion
# ---------------------------------------------------------------------------

def _make_candidate(identity: str, code: str, lex_rank: int | None = None, emb_rank: int | None = None) -> RetrievalCandidate:
    return RetrievalCandidate(
        artifact_type="course_card",
        entity_code=code,
        version="2026-03",
        source_family=SourceFamily.CATALOG,
        content_text="test content",
        source_object_identity=identity,
        rank_lexical=lex_rank,
        rank_embedding=emb_rank,
    )


def test_rrf_fuse_produces_rank_fused():
    """Fused candidates must have rank_fused set."""
    lex = [
        _make_candidate("course_cards/C715", "C715", lex_rank=1),
        _make_candidate("course_cards/D426", "D426", lex_rank=2),
    ]
    emb = [
        _make_candidate("course_cards/D426", "D426", emb_rank=1),
        _make_candidate("course_cards/C715", "C715", emb_rank=2),
    ]
    fused = rrf_fuse(lex, emb)
    assert all(c.rank_fused is not None for c in fused)
    assert len(fused) == 2


def test_rrf_fuse_empty_lists():
    """rrf_fuse with empty lists returns empty."""
    assert rrf_fuse([], []) == []


def test_rrf_fuse_single_list():
    """rrf_fuse with only lexical returns lexical candidates with rank_fused."""
    lex = [
        _make_candidate("course_cards/C715", "C715", lex_rank=1),
        _make_candidate("course_cards/D426", "D426", lex_rank=2),
    ]
    fused = rrf_fuse(lex, [])
    assert all(c.rank_fused is not None for c in fused)
    assert len(fused) == 2


def test_rrf_fuse_candidate_appearing_in_both_lists_ranks_higher():
    """A candidate that appears in both lists should score higher than one in only one list."""
    # C715 appears in both; D426 only in lexical
    lex = [
        _make_candidate("course_cards/C715", "C715", lex_rank=1),
        _make_candidate("course_cards/D426", "D426", lex_rank=2),
    ]
    emb = [
        _make_candidate("course_cards/C715", "C715", emb_rank=1),
    ]
    fused = rrf_fuse(lex, emb)
    assert fused[0].entity_code == "C715", "C715 (in both lists) should rank first"


# ---------------------------------------------------------------------------
# Mixed-version blocking
# ---------------------------------------------------------------------------

def test_retrieve_fails_on_partition_mixed_version_without_compare():
    """Mixed-entity retrieval without compare intent must fail at partition level."""
    # This is enforced by Session 03 scope_partitioning; we verify the
    # partition failure propagates correctly through retrieve().
    partition = _failed_partition(AbstentionState.INSUFFICIENT_EVIDENCE)
    result = retrieve("compare BSCS and MBAPM programs", partition, use_classifier=False)
    assert result.stop_reason == RetrievalStopReason.PARTITION_FAILED


# ---------------------------------------------------------------------------
# RetrievalResult typed output completeness
# ---------------------------------------------------------------------------

def test_retrieval_result_has_all_required_fields():
    """RetrievalResult must expose all fields needed for Session 05."""
    course = _course("C715", description="network security and protocols testing")
    partition = _ok_partition(
        entity_codes=["C715"],
        entity_type=EntityType.COURSE,
        version_scope=["2026-03"],
        source_scope=[SourceFamily.CATALOG],
    )

    # Patch loaders to use our test cards
    import atlas_qa.qa.loaders as loaders_mod
    original_cc = loaders_mod._course_cards_cache
    original_pc = loaders_mod._program_version_cards_cache
    original_gsc = loaders_mod._guide_section_cards_cache
    original_vdc = loaders_mod._version_diff_cards_cache

    loaders_mod._course_cards_cache = {"C715": course}
    loaders_mod._program_version_cards_cache = {}
    loaders_mod._guide_section_cards_cache = []
    loaders_mod._version_diff_cards_cache = []

    try:
        result = retrieve("network security fundamentals", partition, use_classifier=False)
    finally:
        loaders_mod._course_cards_cache = original_cc
        loaders_mod._program_version_cards_cache = original_pc
        loaders_mod._guide_section_cards_cache = original_gsc
        loaders_mod._version_diff_cards_cache = original_vdc

    # Typed output fields must all be present
    assert result.raw_query == "network security fundamentals"
    assert result.request is not None
    assert isinstance(result.lexical_candidates, list)
    assert isinstance(result.embedding_candidates, list)
    assert isinstance(result.fused_candidates, list)
    assert isinstance(result.selected_candidates, list)
    assert isinstance(result.diagnostics, dict)
    # No answer generated
    assert not hasattr(result, "answer_text")


def test_retrieval_result_stop_reason_none_on_success():
    """stop_reason must be None when retrieval succeeds."""
    course = _course("C715", description="network security and protocols testing")
    partition = _ok_partition(
        entity_codes=["C715"],
        entity_type=EntityType.COURSE,
        version_scope=["2026-03"],
        source_scope=[SourceFamily.CATALOG],
    )

    import atlas_qa.qa.loaders as loaders_mod
    orig = {
        "cc": loaders_mod._course_cards_cache,
        "pc": loaders_mod._program_version_cards_cache,
        "gsc": loaders_mod._guide_section_cards_cache,
        "vdc": loaders_mod._version_diff_cards_cache,
    }
    loaders_mod._course_cards_cache = {"C715": course}
    loaders_mod._program_version_cards_cache = {}
    loaders_mod._guide_section_cards_cache = []
    loaders_mod._version_diff_cards_cache = []

    try:
        result = retrieve("network security fundamentals", partition, use_classifier=False)
    finally:
        loaders_mod._course_cards_cache = orig["cc"]
        loaders_mod._program_version_cards_cache = orig["pc"]
        loaders_mod._guide_section_cards_cache = orig["gsc"]
        loaders_mod._version_diff_cards_cache = orig["vdc"]

    assert result.stop_reason is None
    assert len(result.selected_candidates) > 0
