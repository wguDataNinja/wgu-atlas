"""Deterministic scope partitioning for Atlas QA.

Derives and enforces hard retrieval scope constraints from a PartitionInput.
No LLM calls. No fuzzy retrieval. No answer generation.

Session 03 implementation.
"""
from __future__ import annotations

import re

from atlas_qa.qa.source_authority import (
    GUIDE_MISROUTED_TEXT_COURSES,
    VERSION_CONFLICT_PROGRAMS,
    is_cat_short_text,
)
from atlas_qa.qa.types import (
    AbstentionState,
    CourseCard,
    EntityType,
    ExactLookupResponse,
    GuideSectionCard,
    PartitionInput,
    PartitionResult,
    PartitionStatus,
    ProgramVersionCard,
    SectionScope,
    SourceFamily,
)

# ---------------------------------------------------------------------------
# Section-scope policy tables
# ---------------------------------------------------------------------------

# Section scopes that are guide-authoritative (require GUIDE source family).
_GUIDE_ONLY_SECTIONS: frozenset[SectionScope] = frozenset({
    SectionScope.COMPETENCIES,
    SectionScope.AREAS_OF_STUDY,
    SectionScope.CAPSTONE,
    SectionScope.CERTIFICATION_LICENSURE,
})

# Section scopes that are catalog-authoritative (GUIDE is not needed).
_CATALOG_ONLY_SECTIONS: frozenset[SectionScope] = frozenset({
    SectionScope.COURSE_OVERVIEW,
    SectionScope.PROGRAM_DESCRIPTION,
    SectionScope.TOTAL_CU_IDENTITY,
})

# Mapping from SectionScope to guide_section_cards section_type strings.
# None means the section scope does not map to guide artifact types.
_SECTION_TO_GUIDE_TYPE: dict[SectionScope, str | None] = {
    SectionScope.COMPETENCIES: "standard_path",
    SectionScope.AREAS_OF_STUDY: "areas_of_study",
    SectionScope.CAPSTONE: "capstone",
    SectionScope.CERTIFICATION_LICENSURE: "standard_path",
    SectionScope.COURSE_OVERVIEW: None,
    SectionScope.PROGRAM_DESCRIPTION: None,
    SectionScope.TOTAL_CU_IDENTITY: None,
}

_SEP_RE = re.compile(r"[-_]")


def _compact(version: str) -> str:
    """Normalize version string by stripping separators."""
    return _SEP_RE.sub("", version)


# ---------------------------------------------------------------------------
# PartitionInput construction helpers
# ---------------------------------------------------------------------------


def from_exact_result(
    response: ExactLookupResponse,
    section_scope: SectionScope | None = None,
    compare_intent: bool = False,
) -> PartitionInput:
    """Build a PartitionInput from a Session 02 ExactLookupResponse.

    If the response carries an abstention, it is preserved in upstream_abstention
    and the partition layer will propagate it as a failure.
    """
    if response.abstention is not None:
        return PartitionInput(
            from_exact_path=True,
            upstream_abstention=response.abstention,
            section_scope=section_scope,
            compare_intent=compare_intent,
        )
    assert response.answer is not None
    return PartitionInput(
        from_exact_path=True,
        entity_code=response.answer.entity_code,
        entity_type=response.answer.entity_type,
        resolved_version=response.answer.resolved_version,
        section_scope=section_scope,
        compare_intent=compare_intent,
    )


def from_partial_context(
    candidate_codes: list[str],
    section_scope: SectionScope | None = None,
    compare_intent: bool = False,
    upstream_abstention: AbstentionState | None = None,
) -> PartitionInput:
    """Build a PartitionInput from a partial/NL upstream context.

    section_scope must only be passed when it is explicitly known from
    structured upstream input — not inferred from raw NL text.
    """
    return PartitionInput(
        from_exact_path=False,
        candidate_codes=candidate_codes,
        section_scope=section_scope,
        compare_intent=compare_intent,
        upstream_abstention=upstream_abstention,
    )


# ---------------------------------------------------------------------------
# Core scope derivation
# ---------------------------------------------------------------------------


def derive_partition(
    partition_input: PartitionInput,
    course_cards: dict[str, CourseCard],
    program_cards: dict[str, ProgramVersionCard],
) -> PartitionResult:
    """Deterministically derive a typed PartitionResult from a PartitionInput.

    All scope decisions are made here. No LLM calls, no fuzzy logic.
    Returns status=FAILED with a failure_reason if safe scope cannot be established.
    """
    pi = partition_input

    # --- Propagate upstream abstention ---
    if pi.upstream_abstention is not None:
        return PartitionResult(
            status=PartitionStatus.FAILED,
            failure_reason=pi.upstream_abstention,
        )

    # --- Exact-path derivation ---
    if pi.from_exact_path:
        return _derive_exact_path_partition(pi, course_cards, program_cards)

    # --- Partial/NL context derivation ---
    return _derive_partial_partition(pi, course_cards, program_cards)


def _derive_exact_path_partition(
    pi: PartitionInput,
    course_cards: dict[str, CourseCard],
    program_cards: dict[str, ProgramVersionCard],
) -> PartitionResult:
    """Derive partition for an exact-path-resolved input.

    Preserves the exact entity/version scope from Session 02. Does not broaden.
    """
    if pi.entity_code is None or pi.entity_type is None or pi.resolved_version is None:
        return PartitionResult(
            status=PartitionStatus.FAILED,
            failure_reason=AbstentionState.INSUFFICIENT_EVIDENCE,
        )

    code = pi.entity_code
    notes: list[str] = []

    # --- Version scope: single, exact ---
    version_scope = [pi.resolved_version]

    # --- Source scope derivation ---
    source_scope, source_notes = _derive_source_scope(
        code, pi.entity_type, pi.section_scope, course_cards, program_cards
    )
    notes.extend(source_notes)

    # --- Compare mode ---
    # compare_intent on exact path sets the flag for downstream; no mixed-version
    # blending is permitted without an explicit second entity/version.
    compare_mode = pi.compare_intent

    return PartitionResult(
        status=PartitionStatus.OK,
        entity_type=pi.entity_type,
        entity_codes=[code],
        version_scope=version_scope,
        source_scope=source_scope,
        section_scope=pi.section_scope,
        compare_mode=compare_mode,
        from_exact_path=True,
        notes=notes,
    )


def _derive_partial_partition(
    pi: PartitionInput,
    course_cards: dict[str, CourseCard],
    program_cards: dict[str, ProgramVersionCard],
) -> PartitionResult:
    """Derive partition for a partial/NL upstream context.

    Resolves candidate codes against the corpus and derives the narrowest
    safe scope available.
    """
    if not pi.candidate_codes:
        return PartitionResult(
            status=PartitionStatus.FAILED,
            failure_reason=AbstentionState.OUT_OF_SCOPE,
        )

    # Resolve each candidate to a known entity type
    resolved: list[tuple[str, EntityType]] = []
    for code in pi.candidate_codes:
        in_courses = code in course_cards
        in_programs = code in program_cards
        if in_courses and in_programs:
            # Ambiguous — cannot safely narrow; fail
            return PartitionResult(
                status=PartitionStatus.FAILED,
                failure_reason=AbstentionState.AMBIGUOUS_ENTITY,
            )
        if in_courses:
            resolved.append((code, EntityType.COURSE))
        elif in_programs:
            resolved.append((code, EntityType.PROGRAM))
        # Codes not in corpus are silently dropped

    if not resolved:
        return PartitionResult(
            status=PartitionStatus.FAILED,
            failure_reason=AbstentionState.NOT_IN_CORPUS,
        )

    # All resolved codes must be the same entity type
    entity_types = {et for _, et in resolved}
    if len(entity_types) > 1:
        return PartitionResult(
            status=PartitionStatus.FAILED,
            failure_reason=AbstentionState.AMBIGUOUS_ENTITY,
        )
    entity_type = entity_types.pop()

    # Mixed-version retrieval without compare intent is forbidden
    if len(resolved) > 1 and not pi.compare_intent:
        return PartitionResult(
            status=PartitionStatus.FAILED,
            failure_reason=AbstentionState.INSUFFICIENT_EVIDENCE,
            notes=["Mixed-entity retrieval requires explicit compare intent."],
        )

    entity_codes = [code for code, _ in resolved]
    notes: list[str] = []

    # --- Version scope: most recent per entity (partial context default) ---
    version_scope = _derive_version_scope_partial(entity_type, entity_codes, course_cards, program_cards)

    # --- Source scope ---
    source_scope, source_notes = _derive_source_scope(
        entity_codes[0], entity_type, pi.section_scope, course_cards, program_cards
    )
    notes.extend(source_notes)

    return PartitionResult(
        status=PartitionStatus.OK,
        entity_type=entity_type,
        entity_codes=entity_codes,
        version_scope=version_scope,
        source_scope=source_scope,
        section_scope=pi.section_scope,
        compare_mode=pi.compare_intent,
        from_exact_path=False,
        notes=notes,
    )


def _derive_version_scope_partial(
    entity_type: EntityType,
    entity_codes: list[str],
    course_cards: dict[str, CourseCard],
    program_cards: dict[str, ProgramVersionCard],
) -> list[str]:
    """Return the version scope for partial-context inputs (most recent per entity)."""
    versions: list[str] = []
    for code in entity_codes:
        if entity_type == EntityType.COURSE:
            card = course_cards[code]
            ivs = [iv.catalog_version for iv in card.instances_by_version]
            v = sorted(ivs)[-1] if ivs else card.catalog_description_version
            versions.append(v)
        else:
            card = program_cards[code]
            versions.append(card.version)
    # Deduplicate while preserving order
    return list(dict.fromkeys(versions))


def _derive_source_scope(
    primary_code: str,
    entity_type: EntityType,
    section_scope: SectionScope | None,
    course_cards: dict[str, CourseCard],
    program_cards: dict[str, ProgramVersionCard],
) -> tuple[list[SourceFamily], list[str]]:
    """Return (source_scope, notes) based on entity, section intent, and policy rules."""
    notes: list[str] = []

    # --- Section-scope-driven source scope ---
    if section_scope in _GUIDE_ONLY_SECTIONS:
        # Guide-only section: block guide for D554
        if entity_type == EntityType.COURSE and primary_code in GUIDE_MISROUTED_TEXT_COURSES:
            notes.append(
                f"{primary_code}: guide description is misrouted/blocked. "
                "Guide source excluded despite guide-scoped section intent."
            )
            return [SourceFamily.CATALOG], notes
        return [SourceFamily.GUIDE], notes

    if section_scope in _CATALOG_ONLY_SECTIONS:
        return [SourceFamily.CATALOG], notes

    # --- Default: derive from entity characteristics ---
    if entity_type == EntityType.COURSE:
        # D554: guide path is always blocked
        if primary_code in GUIDE_MISROUTED_TEXT_COURSES:
            notes.append(f"{primary_code}: guide description is misrouted/blocked. Guide source excluded.")
            return [SourceFamily.CATALOG], notes

        card = course_cards[primary_code]

        # C179: catalog text is short — note the anomaly, include both sources
        if card.cat_short_text_flag or is_cat_short_text(primary_code, card.catalog_description):
            notes.append(
                f"{primary_code}: catalog description is short (anomaly). "
                "Downstream handling should prefer guide description if available."
            )

        if card.guide_enrichment_available:
            return [SourceFamily.CATALOG, SourceFamily.GUIDE], notes
        return [SourceFamily.CATALOG], notes

    else:  # PROGRAM
        card = program_cards[primary_code]
        # Version-conflict programs: preserve separate provenance; do not blend
        if primary_code in VERSION_CONFLICT_PROGRAMS:
            conflict = VERSION_CONFLICT_PROGRAMS[primary_code]
            notes.append(
                f"{primary_code}: catalog/guide version mismatch "
                f"(catalog={conflict['catalog_version']}, guide={conflict['guide_version']}). "
                "Source provenance must not be blended downstream."
            )
        if card.guide_version is not None:
            return [SourceFamily.CATALOG, SourceFamily.GUIDE], notes
        return [SourceFamily.CATALOG], notes


# ---------------------------------------------------------------------------
# Hard partition enforcement
# ---------------------------------------------------------------------------


def enforce_course_partition(
    result: PartitionResult,
    course_cards: dict[str, CourseCard],
) -> dict[str, CourseCard]:
    """Return only course cards within the partition scope.

    All cards outside entity_codes are excluded. Returns empty dict on failure.
    """
    if result.status != PartitionStatus.OK:
        return {}
    if result.entity_type != EntityType.COURSE:
        return {}
    return {code: card for code, card in course_cards.items() if code in result.entity_codes}


def enforce_program_partition(
    result: PartitionResult,
    program_cards: dict[str, ProgramVersionCard],
) -> dict[str, ProgramVersionCard]:
    """Return only program cards within the partition scope.

    Filters to entity_codes and version_scope. Returns empty dict on failure.
    """
    if result.status != PartitionStatus.OK:
        return {}
    if result.entity_type != EntityType.PROGRAM:
        return {}
    scope_compact = {_compact(v) for v in result.version_scope}
    allowed: dict[str, ProgramVersionCard] = {}
    for code, card in program_cards.items():
        if code not in result.entity_codes:
            continue
        if scope_compact:
            card_versions = {_compact(card.version), _compact(card.catalog_version)}
            if not card_versions.intersection(scope_compact):
                continue
        allowed[code] = card
    return allowed


def enforce_guide_section_partition(
    result: PartitionResult,
    guide_section_cards: list[GuideSectionCard],
) -> list[GuideSectionCard]:
    """Return only guide section cards within the partition scope.

    Filters by entity_codes, source_scope, version_scope, and section_scope.
    Returns empty list if GUIDE is not in source_scope or on failure.
    """
    if result.status != PartitionStatus.OK:
        return []
    if SourceFamily.GUIDE not in result.source_scope:
        return []

    scope_compact = {_compact(v) for v in result.version_scope}
    guide_type_filter: str | None = None
    if result.section_scope is not None:
        guide_type_filter = _SECTION_TO_GUIDE_TYPE.get(result.section_scope)
        if guide_type_filter is None:
            # section_scope is catalog-only; no guide section cards needed
            return []

    filtered: list[GuideSectionCard] = []
    for card in guide_section_cards:
        if card.program_code not in result.entity_codes:
            continue
        if scope_compact and _compact(card.guide_version) not in scope_compact:
            continue
        if guide_type_filter is not None and card.section_type != guide_type_filter:
            continue
        filtered.append(card)
    return filtered
