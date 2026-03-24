"""Exact lookup handler for Atlas QA.

Wires together pre-routing, entity resolution, version resolution, field
extraction, and response assembly into the deterministic exact/simple path.

No LLM calls. No fuzzy retrieval.
"""
from __future__ import annotations

from atlas_qa.qa.entity_resolution import normalize_code, resolve_entity_type
from atlas_qa.qa.loaders import get_course_cards, get_program_version_cards
from atlas_qa.qa.response import abstain, assemble_course_answer, assemble_program_answer
from atlas_qa.qa.router import RouteClass, route
from atlas_qa.qa.source_authority import get_version_conflict
from atlas_qa.qa.types import (
    AbstentionState,
    AnomalyDisclosure,
    EntityType,
    ExactLookupQuery,
    ExactLookupResponse,
)
from atlas_qa.qa.version_resolution import resolve_version

# ---------------------------------------------------------------------------
# Supported fetchable fields per entity type
# ---------------------------------------------------------------------------

_COURSE_FIELDS: frozenset[str] = frozenset({
    "canonical_title",
    "canonical_cus",
    "catalog_description",
    "cat_short_text_flag",
    "guide_enrichment_available",
    "competency_variant_count",
    "cert_prep_signal",
    "prerequisite_course_codes",
    "is_prereq_for",
    "program_codes",
    "instances_by_version",
})

_PROGRAM_FIELDS: frozenset[str] = frozenset({
    "degree_title",
    "college",
    "version",
    "total_cus",
    "course_codes",
    "section_presence",
    "guide_version",
    "guide_pub_date",
    "catalog_version",
})

_MISSING = object()

# Fields that are always empty in the current corpus (Session 01 known limitation)
_ALWAYS_EMPTY_COURSE_FIELDS: frozenset[str] = frozenset({
    "prerequisite_course_codes",
    "is_prereq_for",
})


# ---------------------------------------------------------------------------
# Core lookup
# ---------------------------------------------------------------------------


def lookup(query: ExactLookupQuery) -> ExactLookupResponse:
    """Execute a deterministic exact lookup given a fully-formed ExactLookupQuery.

    All failure modes are encoded as abstention states — no exceptions raised.
    """
    course_cards = get_course_cards()
    program_cards = get_program_version_cards()

    code = normalize_code(query.entity_code)

    # --- Entity resolution ---
    entity_type_or_abstention = resolve_entity_type(code, course_cards, program_cards)
    if isinstance(entity_type_or_abstention, AbstentionState):
        return abstain(query, entity_type_or_abstention)
    entity_type: EntityType = entity_type_or_abstention

    # --- Version resolution ---
    version_or_abstention = resolve_version(
        entity_type,
        code,
        course_cards,
        program_cards,
        explicit_version=query.explicit_version,
    )
    if isinstance(version_or_abstention, AbstentionState):
        return abstain(query, version_or_abstention)
    resolved_version: str = version_or_abstention

    # --- Field fetch and response assembly ---
    if entity_type == EntityType.COURSE:
        card = course_cards[code]
        field_name = query.requested_field

        if field_name is not None:
            if field_name not in _COURSE_FIELDS:
                return abstain(query, AbstentionState.INSUFFICIENT_EVIDENCE)
            # Prereq fields are structurally empty in the current corpus
            if field_name in _ALWAYS_EMPTY_COURSE_FIELDS:
                return abstain(query, AbstentionState.INSUFFICIENT_EVIDENCE)
            field_value = getattr(card, field_name, _MISSING)
            if field_value is _MISSING:
                return abstain(query, AbstentionState.INSUFFICIENT_EVIDENCE)
        else:
            field_value = card.model_dump()

        answer = assemble_course_answer(query, card, resolved_version, field_name, field_value)
        return ExactLookupResponse(query=query, abstention=None, answer=answer)

    else:  # PROGRAM
        card = program_cards[code]
        field_name = query.requested_field

        if field_name is not None:
            if field_name not in _PROGRAM_FIELDS:
                return abstain(query, AbstentionState.INSUFFICIENT_EVIDENCE)
            field_value = getattr(card, field_name, _MISSING)
            if field_value is _MISSING:
                return abstain(query, AbstentionState.INSUFFICIENT_EVIDENCE)
        else:
            field_value = card.model_dump()

        # Version-conflict disclosure sourced from source_authority registry
        conflict = get_version_conflict(code)
        extra_disclosures: list[AnomalyDisclosure] = []
        if conflict:
            extra_disclosures.append(AnomalyDisclosure(
                anomaly_type="version_conflict",
                message=(
                    f"{code}: catalog/guide version mismatch "
                    f"(catalog={conflict['catalog_version']}, "
                    f"guide={conflict['guide_version']})."
                ),
            ))

        answer = assemble_program_answer(
            query, card, resolved_version, field_name, field_value, extra_disclosures
        )
        return ExactLookupResponse(query=query, abstention=None, answer=answer)


# ---------------------------------------------------------------------------
# High-level convenience: route + lookup from raw text
# ---------------------------------------------------------------------------


def route_and_lookup(
    raw_query: str,
    requested_field: str | None = None,
) -> ExactLookupResponse:
    """Route a raw query string and execute an exact lookup.

    Extracts the first candidate code from the query. If no code is detected,
    returns an OUT_OF_SCOPE abstention. For multi-code queries, build an
    ExactLookupQuery directly and call lookup() instead.
    """
    decision = route(raw_query)
    if decision.route_class == RouteClass.OUT_OF_SCOPE or not decision.candidate_codes:
        placeholder = ExactLookupQuery(
            raw_query=raw_query,
            entity_code="",
            requested_field=requested_field,
        )
        return abstain(placeholder, AbstentionState.OUT_OF_SCOPE)

    for raw_code in decision.candidate_codes:
        code = normalize_code(raw_code)
        query = ExactLookupQuery(
            raw_query=raw_query,
            entity_code=code,
            requested_field=requested_field,
            explicit_version=decision.explicit_version,
        )
        result = lookup(query)

        # Successful resolution — return immediately.
        if result.abstention is None:
            return result

        # All-alpha code not in corpus: likely a common English word — try next candidate.
        if (
            result.abstention == AbstentionState.NOT_IN_CORPUS
            and not any(ch.isdigit() for ch in code)
        ):
            continue

        # Any other abstention (AMBIGUOUS_ENTITY, AMBIGUOUS_VERSION, INSUFFICIENT_EVIDENCE)
        # is a meaningful corpus signal — return it.
        return result

    # All candidates exhausted without resolution.
    placeholder = ExactLookupQuery(
        raw_query=raw_query,
        entity_code="",
        requested_field=requested_field,
    )
    return abstain(placeholder, AbstentionState.OUT_OF_SCOPE)
