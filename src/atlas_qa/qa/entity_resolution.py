"""Entity resolution for Atlas QA exact lookup path.

Normalizes identifiers and determines whether a code refers to a course,
a program, or is ambiguous/absent.
"""
from __future__ import annotations

from atlas_qa.qa.types import AbstentionState, CourseCard, EntityType, ProgramVersionCard


def normalize_code(code: str) -> str:
    """Strip whitespace and uppercase a raw identifier."""
    return code.strip().upper()


def resolve_entity_code_from_candidates(
    candidates: list[str],
    course_cards: dict[str, "CourseCard"],
    program_version_cards: dict[str, "ProgramVersionCard"],
) -> str | None:
    """Return the first candidate code present in either corpus.

    Iterates candidates in order. Skips all-alpha codes absent from both
    corpora (likely common English words). Returns immediately on the first
    alphanumeric code regardless of corpus membership (best-effort for
    course-shaped tokens). Returns None if all candidates are exhausted.
    """
    for raw_code in candidates:
        code = normalize_code(raw_code)
        if code in course_cards or code in program_version_cards:
            return code
        if any(ch.isdigit() for ch in code):
            # Alphanumeric code not in corpus — return as best guess rather
            # than skipping (course codes should not be silently dropped).
            return code
    return None


def resolve_entity_type(
    code: str,
    course_cards: dict[str, CourseCard],
    program_version_cards: dict[str, ProgramVersionCard],
) -> EntityType | AbstentionState:
    """Determine whether *code* refers to a course, a program, or is ambiguous/absent.

    Returns:
        EntityType.COURSE           — found only in course_cards
        EntityType.PROGRAM          — found only in program_version_cards
        AbstentionState.AMBIGUOUS_ENTITY  — found in both
        AbstentionState.NOT_IN_CORPUS     — found in neither
    """
    in_courses = code in course_cards
    in_programs = code in program_version_cards
    if in_courses and in_programs:
        return AbstentionState.AMBIGUOUS_ENTITY
    if in_courses:
        return EntityType.COURSE
    if in_programs:
        return EntityType.PROGRAM
    return AbstentionState.NOT_IN_CORPUS
