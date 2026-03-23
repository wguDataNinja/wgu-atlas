"""Thin coordinator for Atlas QA — orchestrates routing, resolution, and partitioning.

Wires together:
1. Upstream route/resolution context (Session 02 lookup)
2. PartitionInput construction
3. Scope derivation (Session 03 partitioning)

No LLM calls. No fuzzy retrieval. No answer generation.

Session 03 implementation.
"""
from __future__ import annotations

from atlas_qa.qa.loaders import get_course_cards, get_guide_section_cards, get_program_version_cards
from atlas_qa.qa.lookup import route_and_lookup
from atlas_qa.qa.scope_partitioning import (
    derive_partition,
    enforce_course_partition,
    enforce_guide_section_partition,
    enforce_program_partition,
    from_exact_result,
    from_partial_context,
)
from atlas_qa.qa.types import (
    ExactLookupResponse,
    GuideSectionCard,
    CourseCard,
    PartitionInput,
    PartitionResult,
    ProgramVersionCard,
    SectionScope,
)


def coordinate(
    raw_query: str,
    section_scope: SectionScope | None = None,
    compare_intent: bool = False,
) -> tuple[PartitionResult, ExactLookupResponse | None]:
    """Route a raw query, execute exact lookup if possible, then derive partition.

    Returns:
        (PartitionResult, ExactLookupResponse | None)

    The ExactLookupResponse is included when the exact lookup path was taken.
    It is None when the query entered the partial/NL context path.

    The PartitionResult is always present. Check result.status before consuming
    scope fields.
    """
    exact_response = route_and_lookup(raw_query)

    if exact_response.abstention is None and exact_response.answer is not None:
        # Exact path resolved successfully
        pi = from_exact_result(exact_response, section_scope=section_scope, compare_intent=compare_intent)
    else:
        # Exact path abstained — fall through to partial context
        # Pass the abstention upstream so the partition layer can propagate it
        from atlas_qa.qa.router import route as _route, RouteClass
        decision = _route(raw_query.strip().upper())
        candidate_codes = decision.candidate_codes if decision.route_class == RouteClass.EXACT_LOOKUP else []
        pi = from_partial_context(
            candidate_codes=candidate_codes,
            section_scope=section_scope,
            compare_intent=compare_intent,
            upstream_abstention=exact_response.abstention,
        )

    course_cards = get_course_cards()
    program_cards = get_program_version_cards()
    result = derive_partition(pi, course_cards, program_cards)

    exact_resp = exact_response if (exact_response.answer is not None) else None
    return result, exact_resp


def build_partition_input_from_exact(
    exact_response: ExactLookupResponse,
    section_scope: SectionScope | None = None,
    compare_intent: bool = False,
) -> PartitionInput:
    """Build a PartitionInput from an already-executed ExactLookupResponse."""
    return from_exact_result(exact_response, section_scope=section_scope, compare_intent=compare_intent)


def get_scoped_course_cards(result: PartitionResult) -> dict[str, CourseCard]:
    """Return course cards filtered to the partition scope."""
    return enforce_course_partition(result, get_course_cards())


def get_scoped_program_cards(result: PartitionResult) -> dict[str, ProgramVersionCard]:
    """Return program cards filtered to the partition scope."""
    return enforce_program_partition(result, get_program_version_cards())


def get_scoped_guide_sections(result: PartitionResult) -> list[GuideSectionCard]:
    """Return guide section cards filtered to the partition scope."""
    return enforce_guide_section_partition(result, get_guide_section_cards())
