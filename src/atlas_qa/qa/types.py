"""Pydantic v2 schemas for Atlas QA canonical objects."""
from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Abstention and entity types (Session 02)
# ---------------------------------------------------------------------------


class AbstentionState(str, Enum):
    NOT_IN_CORPUS = "not_in_corpus"
    AMBIGUOUS_ENTITY = "ambiguous_entity"
    AMBIGUOUS_VERSION = "ambiguous_version"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    OUT_OF_SCOPE = "out_of_scope"


class EntityType(str, Enum):
    COURSE = "course"
    PROGRAM = "program"


# ---------------------------------------------------------------------------
# Response types (Session 02)
# ---------------------------------------------------------------------------


class AnomalyDisclosure(BaseModel):
    anomaly_type: Literal["cat_short_text", "guide_misrouted_text", "version_conflict"]
    message: str


class ExactLookupQuery(BaseModel):
    raw_query: str
    entity_code: str
    entity_type: EntityType | None = None
    requested_field: str | None = None
    explicit_version: str | None = None


class ExactLookupAnswer(BaseModel):
    entity_code: str
    entity_type: EntityType
    resolved_version: str
    field_name: str | None
    field_value: Any
    source_object_identity: str
    evidence_refs: list[EvidenceRef]
    anomaly_disclosures: list[AnomalyDisclosure]


class ExactLookupResponse(BaseModel):
    query: ExactLookupQuery
    abstention: AbstentionState | None = None
    answer: ExactLookupAnswer | None = None


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


# ---------------------------------------------------------------------------
# Scope partitioning types (Session 03)
# ---------------------------------------------------------------------------


class SectionScope(str, Enum):
    """Explicit section intent for partitioning. Only set when structurally known upstream."""
    COURSE_OVERVIEW = "course_overview"
    COMPETENCIES = "competencies"
    CAPSTONE = "capstone"
    AREAS_OF_STUDY = "areas_of_study"
    PROGRAM_DESCRIPTION = "program_description"
    TOTAL_CU_IDENTITY = "total_cu_identity"
    CERTIFICATION_LICENSURE = "certification_licensure"


class SourceFamily(str, Enum):
    """Artifact source families for scope enforcement."""
    CATALOG = "catalog"
    GUIDE = "guide"


class PartitionStatus(str, Enum):
    OK = "ok"
    FAILED = "failed"


class PartitionInput(BaseModel):
    """Typed input to the scope partitioning layer.

    Two construction paths:
    - from_exact_path=True: built from a Session 02 ExactLookupResponse; entity_code,
      entity_type, and resolved_version are populated.
    - from_exact_path=False: built from partial/NL upstream context; candidate_codes
      is populated; entity_type and resolved_version may be absent.
    """
    from_exact_path: bool

    # Exact-path fields (populated when from_exact_path=True)
    entity_code: str | None = None
    entity_type: EntityType | None = None
    resolved_version: str | None = None

    # Partial-context fields (populated when from_exact_path=False)
    candidate_codes: list[str] = []

    # Shared optional fields
    section_scope: SectionScope | None = None
    compare_intent: bool = False
    upstream_abstention: AbstentionState | None = None


class PartitionResult(BaseModel):
    """Typed output of scope partitioning — the handoff contract for Session 04 retrieval.

    When status=OK all scope fields are populated and safe to use.
    When status=FAILED, failure_reason explains why safe scope could not be derived.
    """
    status: PartitionStatus
    failure_reason: AbstentionState | None = None

    # Scope fields (populated when status=OK)
    entity_type: EntityType | None = None
    entity_codes: list[str] = []
    version_scope: list[str] = []
    source_scope: list[SourceFamily] = []
    section_scope: SectionScope | None = None
    compare_mode: bool = False
    from_exact_path: bool = False

    # Downstream safe-handling notes (disclosures, anomaly flags)
    notes: list[str] = []
