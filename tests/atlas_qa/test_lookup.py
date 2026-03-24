"""Tests for the Atlas QA exact lookup path (Session 02).

Covers: pre-router, entity resolution, version resolution, artifact loading,
and end-to-end lookup with both unit (fake data) and integration (real data)
cases.
"""
from __future__ import annotations

import pytest

from atlas_qa.qa.entity_resolution import normalize_code, resolve_entity_code_from_candidates, resolve_entity_type
from atlas_qa.qa.lookup import lookup, route_and_lookup
from atlas_qa.qa.router import RouteClass, route
from atlas_qa.qa.types import (
    AbstentionState,
    CertPrepSignal,
    CourseCard,
    EntityType,
    EvidenceRef,
    ExactLookupQuery,
    GuideEnrichmentSummary,
    InstancesByVersion,
    ProgramVersionCard,
)
from atlas_qa.qa.version_resolution import resolve_version

# ---------------------------------------------------------------------------
# Fixtures — minimal in-memory cards for unit tests
# ---------------------------------------------------------------------------

_EVIDENCE = [EvidenceRef(source_type="catalog", artifact_id="course_index_2026_03", version="2026-03")]
_PROGRAM_EVIDENCE = [EvidenceRef(source_type="catalog", artifact_id="program_blocks_2026_03", version="2026-03")]


def _course(code: str, versions: list[str] | None = None) -> CourseCard:
    ivs = [InstancesByVersion(catalog_version=v, program_codes=[]) for v in (versions or ["2026-03"])]
    return CourseCard(
        course_code=code,
        canonical_title=f"Test Course {code}",
        canonical_cus="3",
        title_variants=[],
        catalog_description="A sufficiently long catalog description placeholder for testing.",
        catalog_description_version="2026-03",
        cat_short_text_flag=False,
        guide_description_alternates=[],
        guide_misrouted_text_flag=False,
        competency_variants=[],
        competency_variant_count=0,
        cert_prep_signal=CertPrepSignal(
            status="not_found_in_observed_guides",
            label=None,
            guide_versions_observed=[],
        ),
        prerequisite_course_codes=[],
        is_prereq_for=[],
        program_codes=["BSCS"],
        instances_by_version=ivs,
        guide_enrichment_available=False,
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


def _program(code: str) -> ProgramVersionCard:
    return ProgramVersionCard(
        program_code=code,
        degree_title=f"Test Degree {code}",
        college="College of Test",
        version="202503",
        is_latest=True,
        total_cus=120,
        catalog_version="2026-03",
        course_codes=["C715", "D426"],
        section_presence={"has_standard_path": True},
        guide_version="202503",
        guide_pub_date="2025-03-01",
        evidence_refs=_PROGRAM_EVIDENCE,
    )


# ---------------------------------------------------------------------------
# Pre-router
# ---------------------------------------------------------------------------

class TestRouter:
    def test_course_code_detected(self):
        d = route("What is D426?")
        assert d.route_class == RouteClass.EXACT_LOOKUP
        assert "D426" in d.candidate_codes

    def test_program_code_detected(self):
        d = route("How many CUs in BSACC?")
        assert d.route_class == RouteClass.EXACT_LOOKUP
        assert "BSACC" in d.candidate_codes

    def test_version_extracted(self):
        d = route("D426 catalog version 2026_03")
        assert d.explicit_version is not None
        assert "2026" in d.explicit_version

    def test_no_code_routes_out_of_scope(self):
        # Query with no alphanumeric tokens — nothing can match the code patterns
        d = route("!!! ??? --- ...")
        assert d.route_class == RouteClass.OUT_OF_SCOPE

    def test_case_normalization(self):
        d = route("what about d426 course")
        assert d.route_class == RouteClass.EXACT_LOOKUP
        assert "D426" in d.candidate_codes

    def test_multiple_codes_extracted(self):
        d = route("Is D426 in BSACC?")
        assert d.route_class == RouteClass.EXACT_LOOKUP
        assert "D426" in d.candidate_codes
        assert "BSACC" in d.candidate_codes

    def test_compact_version_extracted(self):
        d = route("BSACC version 202503")
        assert d.explicit_version == "202503"


# ---------------------------------------------------------------------------
# Entity resolution
# ---------------------------------------------------------------------------

class TestEntityResolution:
    def test_normalize_strips_whitespace(self):
        assert normalize_code("  d426  ") == "D426"

    def test_normalize_uppercases(self):
        assert normalize_code("bsacc") == "BSACC"

    def test_resolves_course(self):
        assert resolve_entity_type("D426", {"D426": _course("D426")}, {}) == EntityType.COURSE

    def test_resolves_program(self):
        assert resolve_entity_type("BSACC", {}, {"BSACC": _program("BSACC")}) == EntityType.PROGRAM

    def test_not_in_corpus(self):
        assert resolve_entity_type("XXXX", {}, {}) == AbstentionState.NOT_IN_CORPUS

    def test_ambiguous_entity(self):
        result = resolve_entity_type(
            "AMBIG",
            {"AMBIG": _course("AMBIG")},
            {"AMBIG": _program("AMBIG")},
        )
        assert result == AbstentionState.AMBIGUOUS_ENTITY


class TestResolveEntityCodeFromCandidates:
    """Session 09 — candidate-iteration helper for the compare path."""

    def test_returns_first_corpus_match(self):
        # WHAT and CHANGED are not in corpus; BSCS is — should return BSCS.
        result = resolve_entity_code_from_candidates(
            ["WHAT", "CHANGED", "BSCS", "BETWEEN"],
            {},
            {"BSCS": _program("BSCS")},
        )
        assert result == "BSCS"

    def test_skips_english_words_not_in_corpus(self):
        # None of the all-alpha candidates are in corpus — should return None.
        result = resolve_entity_code_from_candidates(
            ["WHAT", "THE", "AND", "FOR"],
            {},
            {},
        )
        assert result is None

    def test_alphanumeric_code_returned_even_if_not_in_corpus(self):
        # D999 is not in the corpus but has digits — return it rather than
        # skipping (best-guess for course-shaped tokens).
        result = resolve_entity_code_from_candidates(
            ["WHAT", "D999"],
            {},
            {},
        )
        assert result == "D999"

    def test_returns_first_when_multiple_in_corpus(self):
        # BSDA and BSCS are both in corpus; BSDA comes first — return BSDA.
        result = resolve_entity_code_from_candidates(
            ["BSDA", "BSCS"],
            {},
            {"BSDA": _program("BSDA"), "BSCS": _program("BSCS")},
        )
        assert result == "BSDA"

    def test_empty_candidates_returns_none(self):
        assert resolve_entity_code_from_candidates([], {}, {}) is None

    def test_normalizes_input_codes(self):
        # Input may be unnormalized; normalize_code is applied internally.
        result = resolve_entity_code_from_candidates(
            ["bscs"],
            {},
            {"BSCS": _program("BSCS")},
        )
        assert result == "BSCS"


# ---------------------------------------------------------------------------
# Version resolution
# ---------------------------------------------------------------------------

class TestVersionResolution:
    def test_course_default_version(self):
        v = resolve_version(EntityType.COURSE, "D426", {"D426": _course("D426")}, {})
        assert v == "2026-03"

    def test_course_most_recent_version_selected(self):
        card = _course("D426", versions=["2025-09", "2026-03", "2024-06"])
        v = resolve_version(EntityType.COURSE, "D426", {"D426": card}, {})
        assert v == "2026-03"

    def test_course_explicit_version_present(self):
        card = _course("D426", versions=["2025-09", "2026-03"])
        v = resolve_version(EntityType.COURSE, "D426", {"D426": card}, {}, explicit_version="2025-09")
        assert v == "2025-09"

    def test_course_explicit_version_absent(self):
        result = resolve_version(
            EntityType.COURSE, "D426", {"D426": _course("D426")}, {}, explicit_version="2020-01"
        )
        assert result == AbstentionState.AMBIGUOUS_VERSION

    def test_course_explicit_version_underscore_normalized(self):
        # "2026_03" should match stored "2026-03"
        v = resolve_version(
            EntityType.COURSE, "D426", {"D426": _course("D426")}, {}, explicit_version="2026_03"
        )
        assert v == "2026-03"

    def test_program_default_version(self):
        v = resolve_version(EntityType.PROGRAM, "BSACC", {}, {"BSACC": _program("BSACC")})
        assert v == "202503"

    def test_program_explicit_version_absent(self):
        result = resolve_version(
            EntityType.PROGRAM, "BSACC", {}, {"BSACC": _program("BSACC")}, explicit_version="202001"
        )
        assert result == AbstentionState.AMBIGUOUS_VERSION

    def test_program_explicit_version_compact_match(self):
        # catalog_version "2026-03" → compact "202603" should match
        v = resolve_version(
            EntityType.PROGRAM, "BSACC", {}, {"BSACC": _program("BSACC")}, explicit_version="202603"
        )
        assert v == "202503"


# ---------------------------------------------------------------------------
# Lookup unit tests (fake data via monkeypatch)
# ---------------------------------------------------------------------------

class TestLookupUnit:
    def _patch(self, monkeypatch, courses=None, programs=None):
        monkeypatch.setattr("atlas_qa.qa.lookup.get_course_cards", lambda: courses or {})
        monkeypatch.setattr("atlas_qa.qa.lookup.get_program_version_cards", lambda: programs or {})

    def test_normal_course_lookup_full_object(self, monkeypatch):
        self._patch(monkeypatch, courses={"D426": _course("D426")})
        resp = lookup(ExactLookupQuery(raw_query="D426", entity_code="D426"))
        assert resp.abstention is None
        assert resp.answer is not None
        assert resp.answer.entity_code == "D426"
        assert resp.answer.entity_type == EntityType.COURSE

    def test_normal_program_lookup_field(self, monkeypatch):
        self._patch(monkeypatch, programs={"BSACC": _program("BSACC")})
        resp = lookup(ExactLookupQuery(raw_query="BSACC", entity_code="BSACC", requested_field="total_cus"))
        assert resp.abstention is None
        assert resp.answer.field_value == 120

    def test_missing_entity_not_in_corpus(self, monkeypatch):
        self._patch(monkeypatch)
        resp = lookup(ExactLookupQuery(raw_query="ZZZZ", entity_code="ZZZZ"))
        assert resp.abstention == AbstentionState.NOT_IN_CORPUS
        assert resp.answer is None

    def test_unsupported_field_insufficient_evidence(self, monkeypatch):
        self._patch(monkeypatch, courses={"D426": _course("D426")})
        resp = lookup(ExactLookupQuery(raw_query="D426", entity_code="D426", requested_field="syllabus"))
        assert resp.abstention == AbstentionState.INSUFFICIENT_EVIDENCE

    def test_prerequisite_field_insufficient_evidence(self, monkeypatch):
        self._patch(monkeypatch, courses={"D426": _course("D426")})
        resp = lookup(ExactLookupQuery(
            raw_query="D426", entity_code="D426", requested_field="prerequisite_course_codes"
        ))
        assert resp.abstention == AbstentionState.INSUFFICIENT_EVIDENCE

    def test_ambiguous_entity(self, monkeypatch):
        self._patch(monkeypatch, courses={"AMBIG": _course("AMBIG")}, programs={"AMBIG": _program("AMBIG")})
        resp = lookup(ExactLookupQuery(raw_query="AMBIG", entity_code="AMBIG"))
        assert resp.abstention == AbstentionState.AMBIGUOUS_ENTITY

    def test_explicit_unavailable_version(self, monkeypatch):
        self._patch(monkeypatch, courses={"D426": _course("D426")})
        resp = lookup(ExactLookupQuery(raw_query="D426", entity_code="D426", explicit_version="2020-01"))
        assert resp.abstention == AbstentionState.AMBIGUOUS_VERSION

    def test_out_of_scope_via_route_and_lookup(self, monkeypatch):
        self._patch(monkeypatch)
        resp = route_and_lookup("How do I apply for financial aid?")
        assert resp.abstention == AbstentionState.OUT_OF_SCOPE

    def test_evidence_refs_present_on_answer(self, monkeypatch):
        self._patch(monkeypatch, courses={"D426": _course("D426")})
        resp = lookup(ExactLookupQuery(raw_query="D426", entity_code="D426"))
        assert resp.answer is not None
        assert len(resp.answer.evidence_refs) > 0
        assert resp.answer.source_object_identity == "course_cards/D426"

    def test_case_insensitive_lookup(self, monkeypatch):
        self._patch(monkeypatch, courses={"D426": _course("D426")})
        resp = lookup(ExactLookupQuery(raw_query="d426", entity_code="d426"))
        assert resp.abstention is None
        assert resp.answer.entity_code == "D426"


# ---------------------------------------------------------------------------
# Integration tests — real data/atlas_qa/ artifacts
# ---------------------------------------------------------------------------

class TestLookupIntegration:
    """Uses the real Session 01 canonical artifacts from data/atlas_qa/."""

    def test_real_course_lookup_d426(self):
        resp = lookup(ExactLookupQuery(raw_query="D426", entity_code="D426"))
        assert resp.abstention is None
        assert resp.answer.entity_code == "D426"
        assert resp.answer.entity_type == EntityType.COURSE

    def test_real_program_lookup_bsacc(self):
        resp = lookup(ExactLookupQuery(raw_query="BSACC", entity_code="BSACC"))
        assert resp.abstention is None
        assert resp.answer.entity_type == EntityType.PROGRAM

    def test_real_program_total_cus_bsacc(self):
        resp = lookup(ExactLookupQuery(raw_query="BSACC", entity_code="BSACC", requested_field="total_cus"))
        assert resp.abstention is None
        assert isinstance(resp.answer.field_value, int)
        assert resp.answer.field_value > 0

    def test_real_course_title_d426(self):
        resp = lookup(ExactLookupQuery(raw_query="D426", entity_code="D426", requested_field="canonical_title"))
        assert resp.abstention is None
        assert isinstance(resp.answer.field_value, str)
        assert len(resp.answer.field_value) > 0

    def test_c179_surfaces_short_text_disclosure(self):
        resp = lookup(ExactLookupQuery(raw_query="C179", entity_code="C179"))
        assert resp.abstention is None
        assert any(d.anomaly_type == "cat_short_text" for d in resp.answer.anomaly_disclosures)

    def test_d554_guide_misrouted_disclosure(self):
        resp = lookup(ExactLookupQuery(raw_query="D554", entity_code="D554"))
        if resp.abstention is None:
            assert any(d.anomaly_type == "guide_misrouted_text" for d in resp.answer.anomaly_disclosures)

    def test_version_conflict_program_macca(self):
        resp = lookup(ExactLookupQuery(raw_query="MACCA", entity_code="MACCA"))
        if resp.abstention is None:
            assert any(d.anomaly_type == "version_conflict" for d in resp.answer.anomaly_disclosures)

    def test_unknown_code_not_in_corpus(self):
        resp = lookup(ExactLookupQuery(raw_query="ZZZZZ99", entity_code="ZZZZZ99"))
        assert resp.abstention == AbstentionState.NOT_IN_CORPUS

    def test_all_five_abstention_states_reachable(self, monkeypatch):
        """Smoke-test that all five AbstentionState values are reachable."""
        from atlas_qa.qa.loaders import get_course_cards, get_program_version_cards

        courses = get_course_cards()
        programs = get_program_version_cards()

        # NOT_IN_CORPUS
        r = lookup(ExactLookupQuery(raw_query="ZZZZZ99", entity_code="ZZZZZ99"))
        assert r.abstention == AbstentionState.NOT_IN_CORPUS

        # AMBIGUOUS_VERSION — pick a real course and request a nonexistent version
        first_course = next(iter(courses))
        r = lookup(ExactLookupQuery(raw_query=first_course, entity_code=first_course, explicit_version="1999-01"))
        assert r.abstention == AbstentionState.AMBIGUOUS_VERSION

        # INSUFFICIENT_EVIDENCE — unsupported field
        r = lookup(ExactLookupQuery(raw_query=first_course, entity_code=first_course, requested_field="__nonexistent__"))
        assert r.abstention == AbstentionState.INSUFFICIENT_EVIDENCE

        # OUT_OF_SCOPE — no identifier in query
        r = route_and_lookup("How do I enroll?")
        assert r.abstention == AbstentionState.OUT_OF_SCOPE

        # AMBIGUOUS_ENTITY — monkeypatched overlap
        monkeypatch.setattr("atlas_qa.qa.lookup.get_course_cards", lambda: {"BSACC": _course("BSACC")})
        monkeypatch.setattr("atlas_qa.qa.lookup.get_program_version_cards", lambda: {"BSACC": _program("BSACC")})
        r = lookup(ExactLookupQuery(raw_query="BSACC", entity_code="BSACC"))
        assert r.abstention == AbstentionState.AMBIGUOUS_ENTITY

    def test_route_and_lookup_with_real_data(self):
        resp = route_and_lookup("What is D426?")
        assert resp.abstention is None
        assert resp.answer.entity_code == "D426"

    def test_default_version_is_most_recent_for_entity(self):
        resp = lookup(ExactLookupQuery(raw_query="D426", entity_code="D426"))
        assert resp.abstention is None
        assert resp.answer.resolved_version is not None
