"""Tests for Atlas QA Session 03 — scope partitioning.

Covers: PartitionInput construction, scope derivation (exact and partial paths),
hard partition enforcement, wrong-version blocking, section leakage blocking,
source-scope enforcement, entity collision, mixed-version rejection, D554 guide
block, version-conflict program disclosure, C179 anomaly metadata, and compare
intent flag.
"""
from __future__ import annotations

import pytest

from atlas_qa.qa.scope_partitioning import (
    derive_partition,
    enforce_course_partition,
    enforce_guide_section_partition,
    enforce_program_partition,
    from_exact_result,
    from_partial_context,
)
from atlas_qa.qa.types import (
    AbstentionState,
    AnomalyDisclosure,
    CertPrepSignal,
    CourseCard,
    EntityType,
    EvidenceRef,
    ExactLookupAnswer,
    ExactLookupQuery,
    ExactLookupResponse,
    GuideSectionCard,
    GuideEnrichmentSummary,
    InstancesByVersion,
    PartitionInput,
    PartitionResult,
    PartitionStatus,
    ProgramVersionCard,
    SectionScope,
    SourceFamily,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_EVIDENCE = [EvidenceRef(source_type="catalog", artifact_id="test", version="2026-03")]


def _course(
    code: str,
    versions: list[str] | None = None,
    guide_available: bool = False,
    guide_misrouted: bool = False,
    cat_short_text: bool = False,
) -> CourseCard:
    ivs = [InstancesByVersion(catalog_version=v, program_codes=[]) for v in (versions or ["2026-03"])]
    return CourseCard(
        course_code=code,
        canonical_title=f"Test Course {code}",
        canonical_cus="3",
        title_variants=[],
        catalog_description="A sufficiently long catalog description placeholder for testing purposes here." * 4,
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
        linked_course_codes=[],
        section_data={},
        evidence_refs=_EVIDENCE,
    )


def _exact_response_ok(
    code: str,
    entity_type: EntityType,
    version: str = "2026-03",
) -> ExactLookupResponse:
    query = ExactLookupQuery(raw_query=code, entity_code=code)
    answer = ExactLookupAnswer(
        entity_code=code,
        entity_type=entity_type,
        resolved_version=version,
        field_name=None,
        field_value={},
        source_object_identity=f"{code}@{version}",
        evidence_refs=_EVIDENCE,
        anomaly_disclosures=[],
    )
    return ExactLookupResponse(query=query, abstention=None, answer=answer)


def _exact_response_abstained(abstention: AbstentionState) -> ExactLookupResponse:
    query = ExactLookupQuery(raw_query="test", entity_code="test")
    return ExactLookupResponse(query=query, abstention=abstention, answer=None)


# ---------------------------------------------------------------------------
# PartitionInput construction — from_exact_result
# ---------------------------------------------------------------------------


class TestFromExactResult:
    def test_successful_response_builds_exact_path_input(self):
        resp = _exact_response_ok("D426", EntityType.COURSE, "2026-03")
        pi = from_exact_result(resp)
        assert pi.from_exact_path is True
        assert pi.entity_code == "D426"
        assert pi.entity_type == EntityType.COURSE
        assert pi.resolved_version == "2026-03"
        assert pi.upstream_abstention is None

    def test_abstained_response_captures_upstream_abstention(self):
        resp = _exact_response_abstained(AbstentionState.NOT_IN_CORPUS)
        pi = from_exact_result(resp)
        assert pi.from_exact_path is True
        assert pi.upstream_abstention == AbstentionState.NOT_IN_CORPUS
        assert pi.entity_code is None

    def test_section_scope_passed_through(self):
        resp = _exact_response_ok("D426", EntityType.COURSE)
        pi = from_exact_result(resp, section_scope=SectionScope.COMPETENCIES)
        assert pi.section_scope == SectionScope.COMPETENCIES

    def test_compare_intent_passed_through(self):
        resp = _exact_response_ok("BSCS", EntityType.PROGRAM)
        pi = from_exact_result(resp, compare_intent=True)
        assert pi.compare_intent is True


# ---------------------------------------------------------------------------
# PartitionInput construction — from_partial_context
# ---------------------------------------------------------------------------


class TestFromPartialContext:
    def test_builds_partial_input(self):
        pi = from_partial_context(["BSCS", "D426"])
        assert pi.from_exact_path is False
        assert pi.candidate_codes == ["BSCS", "D426"]
        assert pi.upstream_abstention is None

    def test_section_scope_only_when_explicitly_supplied(self):
        pi = from_partial_context(["BSCS"], section_scope=SectionScope.AREAS_OF_STUDY)
        assert pi.section_scope == SectionScope.AREAS_OF_STUDY

    def test_no_section_scope_by_default(self):
        pi = from_partial_context(["BSCS"])
        assert pi.section_scope is None


# ---------------------------------------------------------------------------
# Exact-path partition derivation
# ---------------------------------------------------------------------------


class TestDeriveExactPath:
    def test_exact_course_scope_preserved(self):
        courses = {"D426": _course("D426", ["2026-03"])}
        programs: dict = {}
        pi = PartitionInput(
            from_exact_path=True,
            entity_code="D426",
            entity_type=EntityType.COURSE,
            resolved_version="2026-03",
        )
        result = derive_partition(pi, courses, programs)
        assert result.status == PartitionStatus.OK
        assert result.entity_codes == ["D426"]
        assert result.version_scope == ["2026-03"]
        assert result.from_exact_path is True

    def test_exact_program_scope_preserved(self):
        courses: dict = {}
        programs = {"BSCS": _program("BSCS", version="202503")}
        pi = PartitionInput(
            from_exact_path=True,
            entity_code="BSCS",
            entity_type=EntityType.PROGRAM,
            resolved_version="202503",
        )
        result = derive_partition(pi, courses, programs)
        assert result.status == PartitionStatus.OK
        assert result.entity_codes == ["BSCS"]
        assert result.version_scope == ["202503"]

    def test_upstream_abstention_propagates_as_failure(self):
        pi = PartitionInput(
            from_exact_path=True,
            upstream_abstention=AbstentionState.NOT_IN_CORPUS,
        )
        result = derive_partition(pi, {}, {})
        assert result.status == PartitionStatus.FAILED
        assert result.failure_reason == AbstentionState.NOT_IN_CORPUS

    def test_missing_exact_path_fields_fail(self):
        pi = PartitionInput(from_exact_path=True)  # no entity_code/type/version
        result = derive_partition(pi, {}, {})
        assert result.status == PartitionStatus.FAILED
        assert result.failure_reason == AbstentionState.INSUFFICIENT_EVIDENCE

    def test_compare_intent_sets_compare_mode_flag(self):
        courses = {"D426": _course("D426")}
        pi = PartitionInput(
            from_exact_path=True,
            entity_code="D426",
            entity_type=EntityType.COURSE,
            resolved_version="2026-03",
            compare_intent=True,
        )
        result = derive_partition(pi, courses, {})
        assert result.status == PartitionStatus.OK
        assert result.compare_mode is True


# ---------------------------------------------------------------------------
# Source-scope enforcement
# ---------------------------------------------------------------------------


class TestSourceScope:
    def test_course_without_guide_gets_catalog_only(self):
        courses = {"C715": _course("C715", guide_available=False)}
        pi = PartitionInput(
            from_exact_path=True,
            entity_code="C715",
            entity_type=EntityType.COURSE,
            resolved_version="2026-03",
        )
        result = derive_partition(pi, courses, {})
        assert result.source_scope == [SourceFamily.CATALOG]

    def test_course_with_guide_gets_both_sources(self):
        courses = {"D426": _course("D426", guide_available=True)}
        pi = PartitionInput(
            from_exact_path=True,
            entity_code="D426",
            entity_type=EntityType.COURSE,
            resolved_version="2026-03",
        )
        result = derive_partition(pi, courses, {})
        assert SourceFamily.CATALOG in result.source_scope
        assert SourceFamily.GUIDE in result.source_scope

    def test_d554_guide_path_blocked(self):
        """D554 guide path must remain blocked regardless of section scope."""
        courses = {"D554": _course("D554", guide_available=True, guide_misrouted=True)}
        pi = PartitionInput(
            from_exact_path=True,
            entity_code="D554",
            entity_type=EntityType.COURSE,
            resolved_version="2026-03",
        )
        result = derive_partition(pi, courses, {})
        assert SourceFamily.GUIDE not in result.source_scope
        assert SourceFamily.CATALOG in result.source_scope
        assert any("D554" in note for note in result.notes)

    def test_d554_guide_blocked_even_with_guide_section_scope(self):
        """D554 guide must be blocked even when section_scope targets guide-only section."""
        courses = {"D554": _course("D554", guide_available=True, guide_misrouted=True)}
        pi = PartitionInput(
            from_exact_path=True,
            entity_code="D554",
            entity_type=EntityType.COURSE,
            resolved_version="2026-03",
            section_scope=SectionScope.COMPETENCIES,
        )
        result = derive_partition(pi, courses, {})
        assert SourceFamily.GUIDE not in result.source_scope

    def test_guide_only_section_restricts_to_guide(self):
        courses = {"D426": _course("D426", guide_available=True)}
        for section in [SectionScope.COMPETENCIES, SectionScope.AREAS_OF_STUDY, SectionScope.CAPSTONE]:
            pi = PartitionInput(
                from_exact_path=True,
                entity_code="D426",
                entity_type=EntityType.COURSE,
                resolved_version="2026-03",
                section_scope=section,
            )
            result = derive_partition(pi, courses, {})
            assert result.source_scope == [SourceFamily.GUIDE], f"Failed for {section}"

    def test_catalog_only_section_restricts_to_catalog(self):
        courses = {"D426": _course("D426", guide_available=True)}
        for section in [SectionScope.COURSE_OVERVIEW, SectionScope.TOTAL_CU_IDENTITY]:
            pi = PartitionInput(
                from_exact_path=True,
                entity_code="D426",
                entity_type=EntityType.COURSE,
                resolved_version="2026-03",
                section_scope=section,
            )
            result = derive_partition(pi, courses, {})
            assert result.source_scope == [SourceFamily.CATALOG], f"Failed for {section}"

    def test_c179_anomaly_note_present(self):
        courses = {"C179": _course("C179", cat_short_text=True)}
        pi = PartitionInput(
            from_exact_path=True,
            entity_code="C179",
            entity_type=EntityType.COURSE,
            resolved_version="2026-03",
        )
        result = derive_partition(pi, courses, {})
        assert result.status == PartitionStatus.OK
        assert any("C179" in note for note in result.notes)

    def test_version_conflict_program_adds_note(self):
        """Version-conflict programs must have source conflict noted, not blended."""
        programs = {"MACCA": _program("MACCA", version="202412", catalog_version="202412", guide_version="202409")}
        pi = PartitionInput(
            from_exact_path=True,
            entity_code="MACCA",
            entity_type=EntityType.PROGRAM,
            resolved_version="202412",
        )
        result = derive_partition(pi, {}, programs)
        assert result.status == PartitionStatus.OK
        assert any("MACCA" in note for note in result.notes)
        # Both catalog and guide are in scope (but with provenance separation noted)
        assert SourceFamily.CATALOG in result.source_scope

    def test_program_without_guide_gets_catalog_only(self):
        programs = {"BSCS": _program("BSCS", guide_version=None)}
        pi = PartitionInput(
            from_exact_path=True,
            entity_code="BSCS",
            entity_type=EntityType.PROGRAM,
            resolved_version="202503",
        )
        result = derive_partition(pi, {}, programs)
        assert result.source_scope == [SourceFamily.CATALOG]


# ---------------------------------------------------------------------------
# Partial-context partition derivation
# ---------------------------------------------------------------------------


class TestDerivePartialContext:
    def test_valid_single_course(self):
        courses = {"D426": _course("D426")}
        pi = from_partial_context(["D426"])
        result = derive_partition(pi, courses, {})
        assert result.status == PartitionStatus.OK
        assert result.entity_codes == ["D426"]
        assert result.entity_type == EntityType.COURSE
        assert result.from_exact_path is False

    def test_valid_single_program(self):
        programs = {"BSCS": _program("BSCS", version="202503")}
        pi = from_partial_context(["BSCS"])
        result = derive_partition(pi, {}, programs)
        assert result.status == PartitionStatus.OK
        assert result.entity_codes == ["BSCS"]
        assert result.version_scope == ["202503"]

    def test_empty_candidates_returns_out_of_scope(self):
        pi = from_partial_context([])
        result = derive_partition(pi, {}, {})
        assert result.status == PartitionStatus.FAILED
        assert result.failure_reason == AbstentionState.OUT_OF_SCOPE

    def test_codes_not_in_corpus_returns_not_in_corpus(self):
        pi = from_partial_context(["ZZZZZ"])
        result = derive_partition(pi, {}, {})
        assert result.status == PartitionStatus.FAILED
        assert result.failure_reason == AbstentionState.NOT_IN_CORPUS

    def test_entity_collision_fails(self):
        """Code appears in both course_cards and program_cards → AMBIGUOUS_ENTITY."""
        courses = {"XYZ": _course("XYZ")}
        programs = {"XYZ": _program("XYZ")}
        pi = from_partial_context(["XYZ"])
        result = derive_partition(pi, courses, programs)
        assert result.status == PartitionStatus.FAILED
        assert result.failure_reason == AbstentionState.AMBIGUOUS_ENTITY

    def test_mixed_entity_types_fail(self):
        """Candidate set with courses AND programs (no compare intent) fails."""
        courses = {"D426": _course("D426")}
        programs = {"BSCS": _program("BSCS")}
        pi = from_partial_context(["D426", "BSCS"])
        result = derive_partition(pi, courses, programs)
        assert result.status == PartitionStatus.FAILED
        assert result.failure_reason == AbstentionState.AMBIGUOUS_ENTITY

    def test_multiple_entities_without_compare_intent_fail(self):
        """Two programs without compare_intent → mixed-entity retrieval blocked."""
        programs = {"BSCS": _program("BSCS"), "BSIT": _program("BSIT")}
        pi = from_partial_context(["BSCS", "BSIT"], compare_intent=False)
        result = derive_partition(pi, {}, programs)
        assert result.status == PartitionStatus.FAILED
        assert result.failure_reason == AbstentionState.INSUFFICIENT_EVIDENCE

    def test_section_scope_not_inferred_from_partial_context(self):
        """section_scope stays None if not explicitly supplied."""
        courses = {"D426": _course("D426")}
        pi = from_partial_context(["D426"])  # no section_scope supplied
        result = derive_partition(pi, courses, {})
        assert result.section_scope is None

    def test_explicit_section_scope_preserved(self):
        courses = {"D426": _course("D426")}
        pi = from_partial_context(["D426"], section_scope=SectionScope.COMPETENCIES)
        result = derive_partition(pi, courses, {})
        assert result.section_scope == SectionScope.COMPETENCIES


# ---------------------------------------------------------------------------
# Hard partition enforcement — course cards
# ---------------------------------------------------------------------------


class TestEnforceCoursePartition:
    def _ok_result(self, entity_codes: list[str], version_scope: list[str] | None = None) -> PartitionResult:
        return PartitionResult(
            status=PartitionStatus.OK,
            entity_type=EntityType.COURSE,
            entity_codes=entity_codes,
            version_scope=version_scope or ["2026-03"],
            source_scope=[SourceFamily.CATALOG],
        )

    def test_filters_to_entity_codes_only(self):
        cards = {"D426": _course("D426"), "C715": _course("C715")}
        result = self._ok_result(["D426"])
        filtered = enforce_course_partition(result, cards)
        assert set(filtered.keys()) == {"D426"}

    def test_wrong_entity_type_returns_empty(self):
        cards = {"D426": _course("D426")}
        result = PartitionResult(
            status=PartitionStatus.OK,
            entity_type=EntityType.PROGRAM,
            entity_codes=["D426"],
            version_scope=["2026-03"],
            source_scope=[SourceFamily.CATALOG],
        )
        assert enforce_course_partition(result, cards) == {}

    def test_failed_partition_returns_empty(self):
        cards = {"D426": _course("D426")}
        result = PartitionResult(
            status=PartitionStatus.FAILED,
            failure_reason=AbstentionState.NOT_IN_CORPUS,
        )
        assert enforce_course_partition(result, cards) == {}


# ---------------------------------------------------------------------------
# Hard partition enforcement — program cards
# ---------------------------------------------------------------------------


class TestEnforceProgramPartition:
    def _ok_result(self, entity_codes: list[str], version_scope: list[str]) -> PartitionResult:
        return PartitionResult(
            status=PartitionStatus.OK,
            entity_type=EntityType.PROGRAM,
            entity_codes=entity_codes,
            version_scope=version_scope,
            source_scope=[SourceFamily.CATALOG],
        )

    def test_filters_to_entity_codes_only(self):
        cards = {"BSCS": _program("BSCS", version="202503"), "BSIT": _program("BSIT", version="202503")}
        result = self._ok_result(["BSCS"], ["202503"])
        filtered = enforce_program_partition(result, cards)
        assert set(filtered.keys()) == {"BSCS"}

    def test_wrong_version_excluded(self):
        """Program card with a version not in version_scope must be excluded."""
        cards = {"BSCS": _program("BSCS", version="202503", catalog_version="202503")}
        result = self._ok_result(["BSCS"], ["202412"])  # different version
        filtered = enforce_program_partition(result, cards)
        assert filtered == {}

    def test_matching_catalog_version_included(self):
        """Card included if catalog_version matches version_scope."""
        cards = {"BSCS": _program("BSCS", version="202503", catalog_version="202412")}
        result = self._ok_result(["BSCS"], ["202412"])
        filtered = enforce_program_partition(result, cards)
        assert "BSCS" in filtered

    def test_failed_partition_returns_empty(self):
        cards = {"BSCS": _program("BSCS")}
        result = PartitionResult(
            status=PartitionStatus.FAILED,
            failure_reason=AbstentionState.AMBIGUOUS_VERSION,
        )
        assert enforce_program_partition(result, cards) == {}

    def test_wrong_entity_type_returns_empty(self):
        cards = {"BSCS": _program("BSCS")}
        result = PartitionResult(
            status=PartitionStatus.OK,
            entity_type=EntityType.COURSE,
            entity_codes=["BSCS"],
            version_scope=["202503"],
            source_scope=[SourceFamily.CATALOG],
        )
        assert enforce_program_partition(result, cards) == {}


# ---------------------------------------------------------------------------
# Hard partition enforcement — guide section cards
# ---------------------------------------------------------------------------


class TestEnforceGuideSectionPartition:
    def _ok_result(
        self,
        entity_codes: list[str],
        version_scope: list[str],
        source_scope: list[SourceFamily],
        section_scope: SectionScope | None = None,
    ) -> PartitionResult:
        return PartitionResult(
            status=PartitionStatus.OK,
            entity_type=EntityType.PROGRAM,
            entity_codes=entity_codes,
            version_scope=version_scope,
            source_scope=source_scope,
            section_scope=section_scope,
        )

    def test_guide_not_in_source_scope_returns_empty(self):
        cards = [_guide_section("BSCS", "202503")]
        result = self._ok_result(["BSCS"], ["202503"], [SourceFamily.CATALOG])
        assert enforce_guide_section_partition(result, cards) == []

    def test_filters_by_program_code(self):
        cards = [
            _guide_section("BSCS", "202503"),
            _guide_section("BSIT", "202503"),
        ]
        result = self._ok_result(["BSCS"], ["202503"], [SourceFamily.CATALOG, SourceFamily.GUIDE])
        filtered = enforce_guide_section_partition(result, cards)
        assert all(c.program_code == "BSCS" for c in filtered)

    def test_filters_by_version_scope(self):
        cards = [
            _guide_section("BSCS", "202503"),
            _guide_section("BSCS", "202412"),
        ]
        result = self._ok_result(["BSCS"], ["202503"], [SourceFamily.CATALOG, SourceFamily.GUIDE])
        filtered = enforce_guide_section_partition(result, cards)
        assert len(filtered) == 1
        assert filtered[0].guide_version == "202503"

    def test_section_scope_filters_by_section_type(self):
        cards = [
            _guide_section("BSCS", "202503", "standard_path"),
            _guide_section("BSCS", "202503", "areas_of_study"),
            _guide_section("BSCS", "202503", "capstone"),
        ]
        result = self._ok_result(
            ["BSCS"], ["202503"], [SourceFamily.GUIDE], SectionScope.AREAS_OF_STUDY
        )
        filtered = enforce_guide_section_partition(result, cards)
        assert len(filtered) == 1
        assert filtered[0].section_type == "areas_of_study"

    def test_catalog_only_section_scope_returns_empty(self):
        """COURSE_OVERVIEW is catalog-only; guide section cards not needed."""
        cards = [_guide_section("BSCS", "202503")]
        result = self._ok_result(
            ["BSCS"], ["202503"], [SourceFamily.GUIDE], SectionScope.COURSE_OVERVIEW
        )
        assert enforce_guide_section_partition(result, cards) == []

    def test_failed_partition_returns_empty(self):
        cards = [_guide_section("BSCS", "202503")]
        result = PartitionResult(
            status=PartitionStatus.FAILED,
            failure_reason=AbstentionState.NOT_IN_CORPUS,
        )
        assert enforce_guide_section_partition(result, cards) == []

    def test_version_normalized_matching(self):
        """Version scope '2025-03' should match guide_version '202503'."""
        cards = [_guide_section("BSCS", "202503")]
        result = self._ok_result(["BSCS"], ["2025-03"], [SourceFamily.GUIDE])
        filtered = enforce_guide_section_partition(result, cards)
        assert len(filtered) == 1


# ---------------------------------------------------------------------------
# Integration: from_exact_result → derive_partition (round-trip)
# ---------------------------------------------------------------------------


class TestRoundTrip:
    def test_exact_course_round_trip(self):
        resp = _exact_response_ok("D426", EntityType.COURSE, "2026-03")
        courses = {"D426": _course("D426", versions=["2026-03"])}
        pi = from_exact_result(resp)
        result = derive_partition(pi, courses, {})
        assert result.status == PartitionStatus.OK
        assert result.entity_codes == ["D426"]
        assert result.version_scope == ["2026-03"]
        assert result.from_exact_path is True

    def test_exact_program_round_trip(self):
        resp = _exact_response_ok("BSCS", EntityType.PROGRAM, "202503")
        programs = {"BSCS": _program("BSCS", version="202503")}
        pi = from_exact_result(resp)
        result = derive_partition(pi, {}, programs)
        assert result.status == PartitionStatus.OK
        assert result.entity_codes == ["BSCS"]

    def test_abstained_exact_response_round_trip(self):
        resp = _exact_response_abstained(AbstentionState.AMBIGUOUS_VERSION)
        pi = from_exact_result(resp)
        result = derive_partition(pi, {}, {})
        assert result.status == PartitionStatus.FAILED
        assert result.failure_reason == AbstentionState.AMBIGUOUS_VERSION

    def test_exact_path_scope_not_broadened(self):
        """Exact-path entity/version must not be widened to a broader corpus set."""
        courses = {"D426": _course("D426"), "C715": _course("C715")}
        resp = _exact_response_ok("D426", EntityType.COURSE, "2026-03")
        pi = from_exact_result(resp)
        result = derive_partition(pi, courses, {})
        assert result.entity_codes == ["D426"]  # NOT ["D426", "C715"]

    def test_enforce_removes_out_of_scope_courses_after_exact_partition(self):
        courses = {"D426": _course("D426"), "C715": _course("C715")}
        resp = _exact_response_ok("D426", EntityType.COURSE, "2026-03")
        pi = from_exact_result(resp)
        result = derive_partition(pi, courses, {})
        filtered = enforce_course_partition(result, courses)
        assert set(filtered.keys()) == {"D426"}
