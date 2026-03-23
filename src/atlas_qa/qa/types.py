"""Pydantic v2 schemas for Atlas QA canonical objects."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class GuideDescriptionAlternate(BaseModel):
    source_program_code: str
    guide_version: str
    description_text: str


class CompetencyVariant(BaseModel):
    source_program_code: str
    guide_version: str
    bullets: list[str]


class CertPrepSignal(BaseModel):
    status: Literal["present", "not_found_in_observed_guides", "unknown"]
    label: str | None
    guide_versions_observed: list[str]


class VersionConflictProgram(BaseModel):
    program_code: str
    catalog_version: str | None
    guide_version: str | None
    conflict_type: Literal["catalog_guide_version_mismatch"]


class GuideEnrichmentSummary(BaseModel):
    has_guide_description_alternates: bool
    has_competencies: bool
    competency_variant_count: int
    has_cert_prep_signal: bool
    program_count_with_guide_enrichment: int


class InstancesByVersion(BaseModel):
    catalog_version: str
    program_codes: list[str]


class EvidenceRef(BaseModel):
    source_type: str
    artifact_id: str
    version: str


class CourseCard(BaseModel):
    # Identity
    course_code: str
    canonical_title: str
    canonical_cus: str
    title_variants: list[str]

    # Catalog description (CAT-TEXT)
    catalog_description: str | None
    catalog_description_version: str
    cat_short_text_flag: bool

    # Guide description alternates (ENRICH, program-scoped)
    guide_description_alternates: list[GuideDescriptionAlternate]
    guide_misrouted_text_flag: bool

    # Competencies (ENRICH)
    competency_variants: list[CompetencyVariant]
    competency_variant_count: int

    # Cert prep (ENRICH)
    cert_prep_signal: CertPrepSignal

    # Prerequisites (CANON)
    # NOTE: catalog structured data does not include prereq relationships.
    # prereq_relationships.json from guides is not per-course (no source course field).
    # Populated as [] pending a structured prereq data source.
    prerequisite_course_codes: list[str]
    is_prereq_for: list[str]

    # Program association
    program_codes: list[str]
    instances_by_version: list[InstancesByVersion]

    # Guide enrichment summary
    guide_enrichment_available: bool
    guide_enrichment_summary: GuideEnrichmentSummary

    # Version conflicts
    version_conflict_programs: list[VersionConflictProgram]

    # Evidence refs (placeholder)
    evidence_refs: list[EvidenceRef]


class ProgramVersionCard(BaseModel):
    program_code: str
    degree_title: str
    college: str
    version: str
    is_latest: bool
    total_cus: int
    catalog_version: str
    course_codes: list[str]
    section_presence: dict[str, bool]
    guide_version: str | None
    guide_pub_date: str | None
    evidence_refs: list[EvidenceRef]


class GuideSectionCard(BaseModel):
    program_code: str
    guide_version: str
    section_type: str  # "standard_path", "areas_of_study", "capstone"
    linked_course_codes: list[str]
    section_data: dict  # raw normalized section content
    evidence_refs: list[EvidenceRef]


class VersionDiffCard(BaseModel):
    entity_type: str  # "course" or "program"
    entity_id: str
    from_version: str
    to_version: str
    added: list[str]
    removed: list[str]
    changed: list[dict]
    evidence_refs: list[EvidenceRef]
