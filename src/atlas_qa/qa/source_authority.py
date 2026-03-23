"""Source-authority logic and hard-coded anomaly rules for Atlas QA."""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Hard anomaly registry
# ---------------------------------------------------------------------------

# Courses with catalog description that is too short to be authoritative.
# C179: "This course introduces IT students..." is ~293 chars, below 300 threshold.
CAT_SHORT_TEXT_THRESHOLD = 300
CAT_SHORT_TEXT_COURSES: set[str] = {"C179"}  # pre-seeded; runtime check also applied

# Courses whose guide text is misrouted (wrong course description found in guide).
# D554: guide text begins with "D554: Advanced Financial Accounting I …" which is
# the catalog text, not an independent guide narrative — flag and suppress.
GUIDE_MISROUTED_TEXT_COURSES: set[str] = {"D554"}

# ---------------------------------------------------------------------------
# Version-conflict programs
# Catalog version vs. guide version mismatch known at the time of this build.
# catalog_version uses the raw string from program_blocks (e.g. "202412").
# guide_version uses the version field from the parsed guide JSON.
# ---------------------------------------------------------------------------
VERSION_CONFLICT_PROGRAMS: dict[str, dict] = {
    "MACCA": {"catalog_version": "202412", "guide_version": "202409"},
    "MACCF": {"catalog_version": "202412", "guide_version": "202409"},
    "MACCM": {"catalog_version": "202412", "guide_version": "202409"},
    "MACCT": {"catalog_version": "202412", "guide_version": "202409"},
    "MSHRM": {"catalog_version": "202311", "guide_version": "202507"},
}

# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def is_cat_short_text(course_code: str, description: str | None) -> bool:
    """Return True if the catalog description is too short to be authoritative."""
    if description is None:
        return False
    return len(description) <= CAT_SHORT_TEXT_THRESHOLD


def is_guide_misrouted(course_code: str) -> bool:
    """Return True if the guide text for this course should be suppressed."""
    return course_code in GUIDE_MISROUTED_TEXT_COURSES


def get_version_conflict(program_code: str) -> dict | None:
    """Return conflict metadata dict if program has a known version conflict, else None."""
    return VERSION_CONFLICT_PROGRAMS.get(program_code)
