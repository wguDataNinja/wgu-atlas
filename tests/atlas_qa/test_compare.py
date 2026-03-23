"""Tests for Session 06 compare mode (compare.py).

Covers:
- compare intent detection (explicit keywords + two version strings)
- version extraction from compare queries
- compare request resolution
- compare bundle construction (diff card path + two-version fallback)
- compare post-check (both versions named, citations, schema)
- answer_compare orchestrator (with injected generate fn)
- edge cases: one missing version, ambiguous entity, no diff card, conflict programs
"""
from __future__ import annotations

import pytest

from atlas_qa.qa.compare import (
    answer_compare,
    build_compare_bundle,
    compare_post_check,
    detect_compare_intent,
    extract_compare_versions,
    resolve_compare_request,
)
from atlas_qa.qa.types import (
    AbstentionState,
    AnomalyDisclosure,
    CompareAnswer,
    CompareEvidenceBundle,
    CompareGenerationOutput,
    CompareSide,
    EntityType,
    EvidenceArtifact,
    EvidenceRef,
    SourceFamily,
    VersionDiffCard,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_artifact(entity_code: str, version: str, identity: str) -> EvidenceArtifact:
    return EvidenceArtifact(
        artifact_type="program_version_card",
        entity_code=entity_code,
        version=version,
        source_family=SourceFamily.CATALOG,
        content={"program_code": entity_code, "catalog_version": version},
        source_object_identity=identity,
        evidence_ref=EvidenceRef(source_type="catalog", artifact_id=identity, version=version),
    )


# Artifact identities that do NOT embed a version string, so post-check citation
# tests can cleanly separate "version token present in text" from "artifact ID in text".
_FROM_ARTIFACT_ID = "pvc:BSCS:from"
_TO_ARTIFACT_ID = "pvc:BSCS:to"


def _make_compare_bundle(
    entity_code: str = "BSCS",
    from_version: str = "2025-06",
    to_version: str = "2026-03",
    with_diff_card: bool = False,
) -> CompareEvidenceBundle:
    from_artifact = _make_artifact(entity_code, from_version, _FROM_ARTIFACT_ID)
    to_artifact = _make_artifact(entity_code, to_version, _TO_ARTIFACT_ID)

    diff_card = None
    if with_diff_card:
        diff_card = VersionDiffCard(
            entity_type="program",
            entity_id=entity_code,
            from_version=from_version,
            to_version=to_version,
            added=["D999"],
            removed=["C100"],
            changed=[],
            evidence_refs=[EvidenceRef(
                source_type="catalog_diff",
                artifact_id="edition_diffs_full",
                version=f"{from_version}→{to_version}",
            )],
        )

    return CompareEvidenceBundle(
        entity_code=entity_code,
        entity_type=EntityType.PROGRAM,
        from_version=from_version,
        to_version=to_version,
        source_scope=[SourceFamily.CATALOG],
        from_side=CompareSide(version=from_version, artifacts=[from_artifact]),
        to_side=CompareSide(version=to_version, artifacts=[to_artifact]),
        diff_card=diff_card,
        anomaly_disclosures=[],
        notes=[],
    )


def _make_gen_output(
    answer_text: str = "Between 2025-06 and 2026-03, D999 was added.",
    from_version: str = "2025-06",
    to_version: str = "2026-03",
    cited_ids: list[str] | None = None,
) -> CompareGenerationOutput:
    return CompareGenerationOutput(
        raw_text=answer_text,
        answer_text=answer_text,
        cited_evidence_ids=[_FROM_ARTIFACT_ID, _TO_ARTIFACT_ID] if cited_ids is None else cited_ids,
        from_version_disclosed=from_version,
        to_version_disclosed=to_version,
    )


# ---------------------------------------------------------------------------
# detect_compare_intent
# ---------------------------------------------------------------------------


class TestDetectCompareIntent:
    def test_changed_with_two_catalog_versions(self):
        q = "What changed in BSCS between the 2025-06 and 2026-03 catalog editions?"
        assert detect_compare_intent(q) is True

    def test_added_with_two_catalog_versions(self):
        q = "What was added to BSDA in the 2026-03 edition compared to 2025-06?"
        assert detect_compare_intent(q) is True

    def test_removed_with_guide_versions(self):
        q = "What courses were removed from BSCS between guide versions 202409 and 202503?"
        assert detect_compare_intent(q) is True

    def test_compare_keyword_with_versions(self):
        q = "Compare the 2025-06 and 2026-03 versions of BSACC for me."
        assert detect_compare_intent(q) is True

    def test_difference_keyword(self):
        q = "What is the difference between the 2025-06 and 2026-03 course lists for BSACC?"
        assert detect_compare_intent(q) is True

    def test_how_has_changed(self):
        q = "How has MSHRM's program guide changed from version 202311 to 202507?"
        assert detect_compare_intent(q) is True

    def test_no_keyword_returns_false(self):
        q = "What is BSCS?"
        assert detect_compare_intent(q) is False

    def test_keyword_but_only_one_version_returns_false(self):
        q = "What changed in BSCS in the 2026-03 catalog?"
        assert detect_compare_intent(q) is False

    def test_two_versions_but_no_keyword_returns_false(self):
        q = "BSCS 2025-06 2026-03"
        assert detect_compare_intent(q) is False

    def test_plain_factual_returns_false(self):
        q = "What are the competencies for C715?"
        assert detect_compare_intent(q) is False

    def test_out_of_scope_returns_false(self):
        q = "Which WGU class is the easiest?"
        assert detect_compare_intent(q) is False


# ---------------------------------------------------------------------------
# extract_compare_versions
# ---------------------------------------------------------------------------


class TestExtractCompareVersions:
    def test_two_catalog_versions(self):
        q = "What changed in BSCS between the 2025-06 and 2026-03 catalog editions?"
        from_v, to_v = extract_compare_versions(q)
        assert from_v == "2025-06"
        assert to_v == "2026-03"

    def test_two_guide_versions(self):
        q = "How has MSHRM changed from version 202311 to 202507?"
        from_v, to_v = extract_compare_versions(q)
        assert from_v == "202311"
        assert to_v == "202507"

    def test_no_versions(self):
        q = "What is BSCS?"
        from_v, to_v = extract_compare_versions(q)
        assert from_v is None
        assert to_v is None

    def test_one_version_only(self):
        q = "What changed in BSCS in the 2026-03 catalog?"
        from_v, to_v = extract_compare_versions(q)
        assert from_v == "2026-03"
        assert to_v is None

    def test_versions_preserved_in_order(self):
        q = "What changed from 202409 to 202412 for MACCA?"
        from_v, to_v = extract_compare_versions(q)
        assert from_v == "202409"
        assert to_v == "202412"


# ---------------------------------------------------------------------------
# resolve_compare_request
# ---------------------------------------------------------------------------


class TestResolveCompareRequest:
    def test_returns_request_when_two_versions_found(self):
        q = "What changed in BSCS between the 2025-06 and 2026-03 catalog editions?"
        req = resolve_compare_request(q, "BSCS", EntityType.PROGRAM)
        assert req is not None
        assert req.entity_code == "BSCS"
        assert req.from_version == "2025-06"
        assert req.to_version == "2026-03"

    def test_returns_none_when_one_version_missing(self):
        q = "What changed in BSCS in the 2026-03 catalog?"
        req = resolve_compare_request(q, "BSCS", EntityType.PROGRAM)
        assert req is None

    def test_returns_none_when_no_versions(self):
        q = "What is BSCS?"
        req = resolve_compare_request(q, "BSCS", EntityType.PROGRAM)
        assert req is None


# ---------------------------------------------------------------------------
# build_compare_bundle — diff card path
# ---------------------------------------------------------------------------


class TestBuildCompareBundleWithDiffCard:
    def test_uses_diff_card_when_available(self, monkeypatch):
        diff_card = VersionDiffCard(
            entity_type="program",
            entity_id="BSCS",
            from_version="2025-06",
            to_version="2026-03",
            added=["D999"],
            removed=[],
            changed=[],
            evidence_refs=[EvidenceRef(
                source_type="catalog_diff",
                artifact_id="edition_diffs_full",
                version="2025-06→2026-03",
            )],
        )
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [diff_card],
        )

        from atlas_qa.qa.compare import CompareRequest
        req = CompareRequest(
            raw_query="What changed in BSCS between 2025-06 and 2026-03?",
            entity_code="BSCS",
            entity_type=EntityType.PROGRAM,
            from_version="2025-06",
            to_version="2026-03",
        )
        result = build_compare_bundle(req)

        assert isinstance(result, CompareEvidenceBundle)
        assert result.diff_card is not None
        assert result.diff_card.entity_id == "BSCS"
        assert result.from_side.version == "2025-06"
        assert result.to_side.version == "2026-03"
        assert result.from_side.artifacts[0].artifact_type == "version_diff_card"

    def test_diff_card_wrong_entity_not_used(self, monkeypatch):
        """A diff card for a different entity must not be used."""
        diff_card = VersionDiffCard(
            entity_type="program",
            entity_id="BSDA",  # different entity
            from_version="2025-06",
            to_version="2026-03",
            added=[],
            removed=[],
            changed=[],
            evidence_refs=[],
        )
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [diff_card],
        )
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_program_version_cards",
            lambda: {},
        )

        from atlas_qa.qa.compare import CompareRequest
        req = CompareRequest(
            raw_query="What changed in BSCS between 2025-06 and 2026-03?",
            entity_code="BSCS",
            entity_type=EntityType.PROGRAM,
            from_version="2025-06",
            to_version="2026-03",
        )
        result = build_compare_bundle(req)

        # Falls through to two-version fallback; both sides empty → abstain.
        assert isinstance(result, CompareAnswer)
        assert result.abstention == AbstentionState.INSUFFICIENT_EVIDENCE


# ---------------------------------------------------------------------------
# build_compare_bundle — two-version fallback
# ---------------------------------------------------------------------------


class TestBuildCompareBundleFallback:
    def _make_program_card(self, program_code: str, catalog_version: str):
        from atlas_qa.qa.types import ProgramVersionCard
        return ProgramVersionCard(
            program_code=program_code,
            degree_title="Test Degree",
            college="Test College",
            version=catalog_version,
            is_latest=True,
            total_cus=120,
            catalog_version=catalog_version,
            course_codes=["C001"],
            section_presence={},
            guide_version=None,
            guide_pub_date=None,
            evidence_refs=[],
        )

    def test_fallback_builds_two_sides(self, monkeypatch):
        from_card = self._make_program_card("BSCS", "2025-06")
        to_card = self._make_program_card("BSCS", "2026-03")
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [],
        )
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_program_version_cards",
            lambda: {
                "BSCS:2025-06": from_card,
                "BSCS:2026-03": to_card,
            },
        )

        from atlas_qa.qa.compare import CompareRequest
        req = CompareRequest(
            raw_query="What changed in BSCS between 2025-06 and 2026-03?",
            entity_code="BSCS",
            entity_type=EntityType.PROGRAM,
            from_version="2025-06",
            to_version="2026-03",
        )
        result = build_compare_bundle(req)

        assert isinstance(result, CompareEvidenceBundle)
        assert result.diff_card is None
        assert len(result.from_side.artifacts) == 1
        assert len(result.to_side.artifacts) == 1
        assert "two-version fallback used" in result.notes[0]

    def test_one_side_missing_records_note(self, monkeypatch):
        from_card = self._make_program_card("BSCS", "2025-06")
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [],
        )
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_program_version_cards",
            lambda: {"BSCS:2025-06": from_card},
        )

        from atlas_qa.qa.compare import CompareRequest
        req = CompareRequest(
            raw_query="What changed in BSCS between 2025-06 and 2026-03?",
            entity_code="BSCS",
            entity_type=EntityType.PROGRAM,
            from_version="2025-06",
            to_version="2026-03",
        )
        result = build_compare_bundle(req)

        assert isinstance(result, CompareEvidenceBundle)
        assert len(result.from_side.artifacts) == 1
        assert len(result.to_side.artifacts) == 0
        assert any("no corpus card found" in n and "to_version" in n for n in result.notes)

    def test_both_sides_empty_returns_abstain(self, monkeypatch):
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [],
        )
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_program_version_cards",
            lambda: {},
        )

        from atlas_qa.qa.compare import CompareRequest
        req = CompareRequest(
            raw_query="What changed in BSCS between 2025-06 and 2026-03?",
            entity_code="BSCS",
            entity_type=EntityType.PROGRAM,
            from_version="2025-06",
            to_version="2026-03",
        )
        result = build_compare_bundle(req)

        assert isinstance(result, CompareAnswer)
        assert result.abstention == AbstentionState.INSUFFICIENT_EVIDENCE

    def test_conflict_program_carries_disclosure(self, monkeypatch):
        """Known conflict programs (MSHRM, MACC) must carry anomaly disclosures."""
        from_card = self._make_program_card("MSHRM", "202311")
        to_card = self._make_program_card("MSHRM", "202507")
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [],
        )
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_program_version_cards",
            lambda: {
                "MSHRM:202311": from_card,
                "MSHRM:202507": to_card,
            },
        )

        from atlas_qa.qa.compare import CompareRequest
        req = CompareRequest(
            raw_query="How has MSHRM changed from version 202311 to 202507?",
            entity_code="MSHRM",
            entity_type=EntityType.PROGRAM,
            from_version="202311",
            to_version="202507",
        )
        result = build_compare_bundle(req)

        assert isinstance(result, CompareEvidenceBundle)
        assert any(d.anomaly_type == "version_conflict" for d in result.anomaly_disclosures)
        assert any("MSHRM" in d.message for d in result.anomaly_disclosures)


# ---------------------------------------------------------------------------
# compare_post_check
# ---------------------------------------------------------------------------


class TestComparePostCheck:
    def test_passes_when_all_checks_met(self):
        bundle = _make_compare_bundle()
        gen = _make_gen_output(
            answer_text=(
                "Between 2025-06 and 2026-03, D999 was added to BSCS. "
                f"[{_FROM_ARTIFACT_ID}] [{_TO_ARTIFACT_ID}]"
            ),
            cited_ids=[_FROM_ARTIFACT_ID, _TO_ARTIFACT_ID],
        )
        result = compare_post_check(gen, bundle)
        assert result.passed is True
        assert result.from_version_named is True
        assert result.to_version_named is True
        assert result.citation_ids_present is True
        assert result.schema_valid is True

    def test_fails_when_from_version_missing_from_answer(self):
        bundle = _make_compare_bundle()
        # Answer names only the to_version; from_version ("2025-06") is absent.
        gen = _make_gen_output(
            answer_text="In the 2026-03 edition, D999 was added.",
            cited_ids=[_FROM_ARTIFACT_ID],
        )
        result = compare_post_check(gen, bundle)
        assert result.passed is False
        assert result.from_version_named is False
        assert any("from_version" in r for r in result.failure_reasons)

    def test_fails_when_to_version_missing_from_answer(self):
        bundle = _make_compare_bundle()
        gen = _make_gen_output(
            answer_text="Compared to 2025-06, D999 was added. [pvc:BSCS:2025-06]",
            cited_ids=["pvc:BSCS:2025-06"],
        )
        result = compare_post_check(gen, bundle)
        assert result.passed is False
        assert result.to_version_named is False

    def test_fails_when_no_citations(self):
        bundle = _make_compare_bundle()
        # cited_ids=[] and answer text contains no bundle artifact IDs.
        gen = _make_gen_output(
            answer_text="Between 2025-06 and 2026-03, D999 was added.",
            cited_ids=[],
        )
        result = compare_post_check(gen, bundle)
        assert result.passed is False
        assert result.citation_ids_present is False

    def test_fails_on_llm_failure(self):
        bundle = _make_compare_bundle()
        gen = CompareGenerationOutput(
            raw_text="",
            answer_text=None,
            llm_failure=True,
        )
        result = compare_post_check(gen, bundle)
        assert result.passed is False
        assert result.schema_valid is False

    def test_diff_card_artifact_id_counts_as_citation(self):
        bundle = _make_compare_bundle(with_diff_card=True)
        gen = _make_gen_output(
            answer_text="Between 2025-06 and 2026-03, D999 was added. [edition_diffs_full]",
            cited_ids=["edition_diffs_full"],
        )
        result = compare_post_check(gen, bundle)
        assert result.citation_ids_present is True


# ---------------------------------------------------------------------------
# answer_compare — orchestrator
# ---------------------------------------------------------------------------


class TestAnswerCompare:
    def _make_generate_fn(self, answer_text: str, from_v: str, to_v: str):
        """Return a generate_fn that produces a valid CompareGenerationOutput."""
        def fn(bundle, question):
            artifact_ids = [
                a.source_object_identity
                for a in bundle.from_side.artifacts + bundle.to_side.artifacts
            ]
            cited = artifact_ids[:2] if artifact_ids else []
            return CompareGenerationOutput(
                raw_text=answer_text,
                answer_text=answer_text,
                cited_evidence_ids=cited,
                from_version_disclosed=from_v,
                to_version_disclosed=to_v,
            )
        return fn

    def test_full_pipeline_produces_answer(self, monkeypatch):
        diff_card = VersionDiffCard(
            entity_type="program",
            entity_id="BSCS",
            from_version="2025-06",
            to_version="2026-03",
            added=["D999"],
            removed=[],
            changed=[],
            evidence_refs=[EvidenceRef(
                source_type="catalog_diff",
                artifact_id="edition_diffs_full",
                version="2025-06→2026-03",
            )],
        )
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [diff_card],
        )

        gen_fn = self._make_generate_fn(
            "Between 2025-06 and 2026-03 for BSCS, D999 was added. [edition_diffs_full]",
            "2025-06",
            "2026-03",
        )
        result = answer_compare(
            "What changed in BSCS between 2025-06 and 2026-03?",
            "BSCS",
            EntityType.PROGRAM,
            _generate_fn=gen_fn,
        )

        assert result.abstention is None
        assert result.answer_text is not None
        assert "2025-06" in result.answer_text
        assert "2026-03" in result.answer_text
        assert result.postcheck is not None
        assert result.postcheck.passed is True

    def test_abstains_when_one_version_missing_from_query(self, monkeypatch):
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [],
        )
        result = answer_compare(
            "What changed in BSCS in the 2026-03 catalog?",  # only one version
            "BSCS",
            EntityType.PROGRAM,
            _generate_fn=lambda b, q: CompareGenerationOutput(raw_text=""),
        )
        assert result.abstention == AbstentionState.AMBIGUOUS_VERSION

    def test_abstains_when_generation_fails(self, monkeypatch):
        diff_card = VersionDiffCard(
            entity_type="program",
            entity_id="BSCS",
            from_version="2025-06",
            to_version="2026-03",
            added=[],
            removed=[],
            changed=[],
            evidence_refs=[EvidenceRef(
                source_type="catalog_diff",
                artifact_id="edition_diffs_full",
                version="2025-06→2026-03",
            )],
        )
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [diff_card],
        )

        def failing_gen(bundle, question):
            return CompareGenerationOutput(raw_text="", answer_text=None, llm_failure=True)

        result = answer_compare(
            "What changed in BSCS between 2025-06 and 2026-03?",
            "BSCS",
            EntityType.PROGRAM,
            _generate_fn=failing_gen,
        )
        assert result.abstention == AbstentionState.INSUFFICIENT_EVIDENCE

    def test_abstains_when_postcheck_fails(self, monkeypatch):
        diff_card = VersionDiffCard(
            entity_type="program",
            entity_id="BSCS",
            from_version="2025-06",
            to_version="2026-03",
            added=[],
            removed=[],
            changed=[],
            evidence_refs=[EvidenceRef(
                source_type="catalog_diff",
                artifact_id="edition_diffs_full",
                version="2025-06→2026-03",
            )],
        )
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [diff_card],
        )

        def gen_missing_versions(bundle, question):
            # Answer text is missing both version tokens — post-check must fail.
            return CompareGenerationOutput(
                raw_text="D999 was added.",
                answer_text="D999 was added.",  # no version tokens
                cited_evidence_ids=["edition_diffs_full"],
            )

        result = answer_compare(
            "What changed in BSCS between 2025-06 and 2026-03?",
            "BSCS",
            EntityType.PROGRAM,
            _generate_fn=gen_missing_versions,
        )
        assert result.abstention == AbstentionState.INSUFFICIENT_EVIDENCE
        assert result.postcheck is not None
        assert result.postcheck.passed is False

    def test_conflict_program_disclosure_in_bundle(self, monkeypatch):
        """MACCA compare must carry version_conflict anomaly disclosure in bundle."""
        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_version_diff_cards",
            lambda: [],
        )

        from atlas_qa.qa.types import ProgramVersionCard
        def _card(v):
            return ProgramVersionCard(
                program_code="MACCA",
                degree_title="Master of Accounting",
                college="Business",
                version=v,
                is_latest=True,
                total_cus=30,
                catalog_version=v,
                course_codes=[],
                section_presence={},
                guide_version=None,
                guide_pub_date=None,
                evidence_refs=[],
            )

        monkeypatch.setattr(
            "atlas_qa.qa.compare.get_program_version_cards",
            lambda: {"MACCA:202409": _card("202409"), "MACCA:202412": _card("202412")},
        )

        gen_fn = self._make_generate_fn(
            "Between 202409 and 202412, no changes found for MACCA. "
            "[program_version_card:MACCA:202409] [program_version_card:MACCA:202412]",
            "202409", "202412",
        )
        result = answer_compare(
            "What changed in MACCA between catalog versions 202409 and 202412?",
            "MACCA",
            EntityType.PROGRAM,
            _generate_fn=gen_fn,
        )

        assert result.compare_bundle is not None
        assert any(
            d.anomaly_type == "version_conflict"
            for d in result.compare_bundle.anomaly_disclosures
        )
