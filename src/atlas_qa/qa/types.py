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


# ---------------------------------------------------------------------------
# Fuzzy retrieval types (Session 04)
# ---------------------------------------------------------------------------


class RetrievalStopReason(str, Enum):
    """Reason fuzzy retrieval stopped without producing candidates."""
    PARTITION_FAILED = "partition_failed"
    EMPTY_CANDIDATE_POOL = "empty_candidate_pool"
    OFF_SECTION_CANDIDATES = "off_section_candidates"
    SOURCE_FAMILY_EXHAUSTED = "source_family_exhausted"
    MIXED_VERSION_BLOCKED = "mixed_version_blocked"
    CLASSIFIER_UNUSABLE_NO_FALLBACK = "classifier_unusable_no_fallback"


class ClassifierHint(BaseModel):
    """Advisory-only output from the fuzzy-query structured classifier.

    All fields are hints. None may override upstream deterministic scope.
    """
    query_class_hint: str | None = None          # "class_b" | "class_c" | "unknown"
    entity_type_hint: str | None = None          # "course" | "program" | None
    entity_code_hint: str | None = None          # possible code mention, if any
    explicit_version_hint: str | None = None     # version string if explicitly stated
    requested_section_hint: str | None = None    # section name if apparent
    compare_intent: bool = False                 # true if user is comparing two things
    unsupported_or_advising: bool = False        # true if advising/unsupported intent
    confidence_notes: str | None = None          # plain-language notes from classifier


class FuzzyRetrievalRequest(BaseModel):
    """Typed input to the fuzzy retrieval layer.

    Constructed after partition is established. The partition is binding —
    retrieval must not broaden its scope fields.
    """
    raw_query: str
    partition: PartitionResult           # upstream binding scope — must be status=OK
    classifier_hint: ClassifierHint | None = None   # advisory; may be absent


class RetrievalCandidate(BaseModel):
    """A single candidate document returned from scoped retrieval."""
    artifact_type: Literal[
        "course_card",
        "program_version_card",
        "guide_section_card",
        "version_diff_card",
    ]
    entity_code: str
    version: str | None = None
    source_family: SourceFamily
    content_text: str                    # text used for indexing/retrieval
    score: float = 0.0
    rank_lexical: int | None = None
    rank_embedding: int | None = None
    rank_fused: int | None = None
    source_object_identity: str          # stable identity for downstream evidence refs


class RetrievalResult(BaseModel):
    """Full typed output of the fuzzy retrieval layer (Session 04).

    Suitable as input to Session 05 evidence-bundle construction.
    Does not contain final answers.
    """
    raw_query: str
    request: FuzzyRetrievalRequest | None = None

    # Stop state — set when retrieval cannot produce a safe candidate set
    stop_reason: RetrievalStopReason | None = None

    # Classifier output (if classifier was invoked)
    classifier_output: ClassifierHint | None = None
    classifier_parse_error: bool = False
    classifier_schema_error: bool = False
    classifier_used_fallback: bool = False

    # Retrieval candidate lists
    lexical_candidates: list[RetrievalCandidate] = []
    embedding_candidates: list[RetrievalCandidate] = []
    fused_candidates: list[RetrievalCandidate] = []

    # Final selected candidate set (top-k after fusion or lexical fallback)
    selected_candidates: list[RetrievalCandidate] = []

    # Diagnostics (for tests and traceability)
    diagnostics: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Session 05 — Evidence bundle, answerability gate, generation, post-check
# ---------------------------------------------------------------------------


class EvidenceArtifact(BaseModel):
    """A single vetted artifact included in an evidence bundle."""
    artifact_type: Literal[
        "course_card",
        "program_version_card",
        "guide_section_card",
        "version_diff_card",
    ]
    entity_code: str
    version: str
    source_family: SourceFamily
    content: dict | str                     # canonical object fields used
    source_object_identity: str             # stable identity for citations
    evidence_ref: EvidenceRef


class EvidenceBundle(BaseModel):
    """Pre-assembled, pre-validated set of evidence artifacts for one query.

    Constructed deterministically from RetrievalResult.selected_candidates or
    from an ExactLookupAnswer. Never built from raw LLM output or corpus search.
    """
    entity_code: str
    entity_type: EntityType
    version_used: str
    source_scope: list[SourceFamily]
    artifacts: list[EvidenceArtifact]       # 1–5 items for single-entity
    anomaly_disclosures: list[AnomalyDisclosure]
    notes: list[str]                        # upstream scope notes from partition
    from_exact_path: bool


class AnswerabilityResult(BaseModel):
    """Output of the deterministic answerability/sufficiency gate."""
    answerable: bool
    abstention_reason: AbstentionState | None = None
    gate_notes: list[str] = []


class GenerationOutput(BaseModel):
    """Typed output of one constrained LLM generation call.

    Fields are populated after parsing and validation. On failure, answer_text
    is None and the error flags are set.
    """
    raw_text: str
    answer_text: str | None = None
    cited_evidence_ids: list[str] = []
    version_disclosed: str | None = None
    parse_error: bool = False
    schema_error: bool = False
    llm_failure: bool = False


class PostCheckResult(BaseModel):
    """Result of the deterministic post-check pass over a GenerationOutput."""
    passed: bool
    citation_ids_present: bool
    version_token_present: bool
    schema_valid: bool
    failure_reasons: list[str] = []


class QAResponse(BaseModel):
    """Final typed answer or abstention for a single-entity QA query.

    Produced by the Session 05 answer orchestrator. Carries either a grounded,
    citation-bearing answer or an explicit abstention state — never both.
    """
    raw_query: str
    entity_code: str | None = None
    entity_type: EntityType | None = None
    version_used: str | None = None
    abstention: AbstentionState | None = None
    answer_text: str | None = None
    evidence_bundle: EvidenceBundle | None = None
    generation_output: GenerationOutput | None = None
    postcheck: PostCheckResult | None = None
    diagnostics: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Session 06 — Compare mode types
# ---------------------------------------------------------------------------


class CompareRequest(BaseModel):
    """Typed input for an explicit compare-mode query."""
    raw_query: str
    entity_code: str
    entity_type: EntityType
    from_version: str
    to_version: str
    source_scope: list[SourceFamily] = []


class CompareSide(BaseModel):
    """One version side of a compare evidence bundle."""
    version: str
    artifacts: list[EvidenceArtifact]


class CompareEvidenceBundle(BaseModel):
    """Evidence bundle for a compare-mode query.

    Keeps the two version sides strictly separated.
    No mixed-version merging without explicit disclosure.
    """
    entity_code: str
    entity_type: EntityType
    from_version: str
    to_version: str
    source_scope: list[SourceFamily]
    from_side: CompareSide
    to_side: CompareSide
    diff_card: VersionDiffCard | None = None   # present if version_diff_card was available
    anomaly_disclosures: list[AnomalyDisclosure]
    notes: list[str]


class CompareGenerationOutput(BaseModel):
    """Typed output of one constrained compare generation call."""
    raw_text: str
    answer_text: str | None = None
    cited_evidence_ids: list[str] = []
    from_version_disclosed: str | None = None
    to_version_disclosed: str | None = None
    parse_error: bool = False
    schema_error: bool = False
    llm_failure: bool = False


class ComparePostCheckResult(BaseModel):
    """Post-check result for a compare answer."""
    passed: bool
    from_version_named: bool
    to_version_named: bool
    citation_ids_present: bool
    schema_valid: bool
    failure_reasons: list[str] = []


class CompareAnswer(BaseModel):
    """Final typed compare answer or abstention.

    Produced by the Session 06 compare orchestrator. Carries either a grounded
    compare answer or an explicit abstention — never both.
    """
    raw_query: str
    entity_code: str | None = None
    entity_type: EntityType | None = None
    from_version: str | None = None
    to_version: str | None = None
    abstention: AbstentionState | None = None
    answer_text: str | None = None
    compare_bundle: CompareEvidenceBundle | None = None
    generation_output: CompareGenerationOutput | None = None
    postcheck: ComparePostCheckResult | None = None
    diagnostics: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Session 06 — Evaluation harness types
# ---------------------------------------------------------------------------


class QueryClass(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


class EvalExpectedBehavior(str, Enum):
    ANSWER = "answer"
    ABSTAIN = "abstain"
    CLARIFY = "clarify"


class GoldQuestion(BaseModel):
    """A single question from the gold question set."""
    question_id: str
    query: str
    query_class: QueryClass
    expected_behavior: EvalExpectedBehavior
    entity_type_label: str       # "course" / "program" / "section" / "compare" / "none"
    source_scope_label: str      # "catalog" / "guide" / "canon" / "both" / "none"
    version_sensitive: bool
    notes: str = ""
    is_launch_subset: bool = False


class EvalCaseResult(BaseModel):
    """Result for a single evaluated question."""
    question_id: str
    query: str
    query_class: QueryClass
    expected_behavior: EvalExpectedBehavior
    actual_behavior: str          # "answer" | "abstain" | "clarify" | "error"
    passed: bool
    citation_present: bool | None = None
    version_disclosed: bool | None = None
    anomaly_disclosure_present: bool | None = None
    failure_reason: str | None = None
    diagnostics: dict[str, Any] = {}


class ClassGateResult(BaseModel):
    """Launch-gate result for one query class."""
    query_class: QueryClass
    total: int
    passed: int
    pass_rate: float
    threshold: float
    gate_passed: bool
    failure_details: list[str] = []


class LaunchGateSummary(BaseModel):
    """Aggregated launch-gate result across all query classes."""
    run_id: str
    timestamp: str
    total_questions: int
    total_passed: int
    overall_pass_rate: float
    per_class: list[ClassGateResult]
    gate_passed: bool           # True only if ALL class gates passed
    notes: list[str] = []


class EvalRunSummary(BaseModel):
    """Full typed summary of one evaluation run."""
    run_id: str
    timestamp: str
    question_set: str           # "gold_v1" | "launch_subset"
    total_questions: int
    cases: list[EvalCaseResult]
    launch_gate: LaunchGateSummary | None = None
