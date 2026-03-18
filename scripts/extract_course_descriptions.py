#!/usr/bin/env python3
"""
extract_course_descriptions.py
================================
Extracts course descriptions from the WGU catalog text file.

The catalog contains a "Courses" section (distinct from the earlier
"Course Descriptions" section for standalone/certificate offerings)
where every degree-program course is described in the format:

    CODE - Title - Description paragraph...
    [continuation lines...]

This section runs from the "Courses" section header to "Instructor Directory".

Usage:
    python3 scripts/extract_course_descriptions.py \
        --catalog /path/to/WGU-Reddit/WGU_catalog/data/raw_catalog_texts/catalog_2026_03.txt \
        --out     /path/to/wgu-atlas/public/data/course_descriptions.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# A new course entry: CODE - Title - Description start
# CODE is the Atlas course code (e.g. C100, D286, ORA1, C957A)
# We require at least one letter and one digit to avoid matching headings
_ENTRY_RE = re.compile(
    r"^([A-Z][A-Z0-9]{1,6})\s+-\s+(.+?)\s+-\s+(.+)"
)

# Lines to skip: copyright lines, URLs, page numbers, headers
_SKIP_RE = re.compile(
    r"^(©|www\.|https?://|Toll Free|Local Phone|Fax:|info@|"
    r"CCN Course|Total CUs:|ENDS[A-Z]|Elective Options)"
)

# Section headers that end the Courses block
_STOP_RE = re.compile(r"^(Instructor Directory|Program Outcomes|Course Descriptions)")

# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def find_courses_section(lines: list[str]) -> int:
    """
    Find the line index of the 'Courses' section header that precedes the
    CODE - Title - Description format entries.
    This is the second occurrence of a courses-like header, after page ~258.
    We identify it by looking for the section URL that immediately follows it.
    """
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "Courses":
            # Check the next few lines for the WGU student policy URL
            context = " ".join(l.strip() for l in lines[i:i+5])
            if "wgu.edu" in context or "cm.wgu.edu" in context:
                return i + 1  # start parsing from the line after the header
    return -1


def parse_courses(lines: list[str], start: int) -> dict[str, dict]:
    """
    Parse CODE - Title - Description entries from lines[start:].
    Returns dict: code → {title, description}
    """
    descriptions: dict[str, dict] = {}
    current_code: str | None = None
    current_title: str | None = None
    current_lines: list[str] = []

    def flush():
        nonlocal current_code, current_title, current_lines
        if current_code and current_lines:
            desc = " ".join(current_lines).strip()
            # Clean up any remaining line-wrap artifacts
            desc = re.sub(r"\s+", " ", desc).strip()
            if desc:
                # Fix artifact: the catalog format is "CODE - Full Title - Description"
                # where Full Title may contain " - " (e.g. "Network and Security - Foundations").
                # The regex captures only the first segment as title, leaving the subtitle
                # as a leading fragment in the description (e.g. "Foundations - real desc...").
                # Detect and strip this artifact when:
                #   1. Description starts with a short Title-Case phrase followed by " - "
                #   2. The phrase doesn't look like prose (no common sentence openers)
                #   3. The phrase doesn't overlap with the start of the captured title
                #      (which would mean the description prose starts with the course name)
                subtitle_m = re.match(r"^([A-Z][^-]{0,60}?)\s+-\s+", desc)
                if subtitle_m:
                    potential_sub = subtitle_m.group(1).strip()
                    _prose_openers = re.compile(
                        r"^(This|In |The |Students|A |An |Each|Through|Using|By |These|For )"
                    )
                    if (
                        len(potential_sub.split()) <= 6
                        and not _prose_openers.match(potential_sub)
                        and not (current_title or "").lower().startswith(potential_sub.lower())
                    ):
                        current_title = f"{current_title} - {potential_sub}"
                        desc = desc[subtitle_m.end():]
                descriptions[current_code] = {
                    "title": current_title or "",
                    "description": desc,
                }
        current_code = None
        current_title = None
        current_lines = []

    for i in range(start, len(lines)):
        raw = lines[i].rstrip()
        stripped = raw.strip()

        if not stripped:
            continue

        # Stop conditions
        if _STOP_RE.match(stripped):
            break

        # Skip copyright/footer/header lines
        if _SKIP_RE.match(stripped) or stripped.startswith("©") or stripped.startswith("http"):
            continue

        # Skip lines that look like page number footers (bare integers)
        if re.match(r"^\d{1,4}$", stripped):
            continue

        # Try to match a new entry
        m = _ENTRY_RE.match(stripped)
        if m:
            flush()
            current_code = m.group(1)
            current_title = m.group(2).strip()
            current_lines = [m.group(3).strip()]
        else:
            # Continuation line
            if current_code and stripped:
                # Skip lines that look like CCN course rows (CCN CODE Title CUs Term)
                if re.match(r"^[A-Z]+ \d+[A-Z]?\s+[A-Z]\d{3}", stripped):
                    continue
                current_lines.append(stripped)

    flush()
    return descriptions


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, help="Path to catalog_YYYY_MM.txt")
    parser.add_argument("--out", required=True, help="Output path for course_descriptions.json")
    args = parser.parse_args()

    catalog_path = Path(args.catalog)
    out_path = Path(args.out)

    if not catalog_path.exists():
        sys.exit(f"ERROR: catalog file not found: {catalog_path}")

    print(f"Loading catalog: {catalog_path}")
    with open(catalog_path, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    print(f"  {len(lines):,} lines")

    start = find_courses_section(lines)
    if start < 0:
        sys.exit("ERROR: Could not locate 'Courses' section in catalog")
    print(f"  Found Courses section at line {start}")

    print("Parsing course descriptions...")
    descriptions = parse_courses(lines, start)
    print(f"  Extracted {len(descriptions)} course descriptions")

    # Count Atlas-style codes (single letter + 3-4 digits + optional letter)
    atlas_re = re.compile(r"^[A-Z]\d{3,4}[A-Z]?$")
    atlas_count = sum(1 for c in descriptions if atlas_re.match(c))
    print(f"  Atlas-format codes (C100/D286-style): {atlas_count}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(descriptions, f, indent=2, ensure_ascii=False)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
