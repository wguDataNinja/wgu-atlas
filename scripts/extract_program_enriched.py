#!/usr/bin/env python3
"""
extract_program_enriched.py
============================
Extracts program descriptions, course rosters, and program learning outcomes
from the 2026-03 WGU catalog text, cross-referenced with the program_blocks
file produced by parse_catalog_v11.py.

Outputs:  <wgu_atlas_data>/program_enriched.json

Usage:
    python3 scripts/extract_program_enriched.py \
        --catalog  /path/to/WGU-Reddit/WGU_catalog/data/raw_catalog_texts/catalog_2026_03.txt \
        --blocks   /path/to/WGU-Reddit/WGU_catalog/outputs/program_names/2026_03_program_blocks_v11.json \
        --programs /path/to/wgu-atlas/public/data/programs.json \
        --out      /path/to/wgu-atlas/public/data/program_enriched.json

All four arguments are required.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Course roster parsing
# ---------------------------------------------------------------------------

# Pattern: "CCN CODE Title CUs Term"
# e.g.  "MGMT 3000 C715 Organizational Behavior 3 1"
# CCN   = uppercase letters + space + digits  (e.g. "MGMT 3000", "IT 1010")
# CODE  = letter + 3 digits + optional letter (e.g. "C715", "D072", "ORA1")
_COURSE_ROW_RE = re.compile(
    r"^([A-Z]+ \d+[A-Z]?)\s+([A-Z]\d{3}[A-Z]?)\s+(.+?)\s+(\d+)\s+(\d+)\s*$"
)
_SKIP_LINE_RE = re.compile(
    r"^(©|CCN Course|Total CUs:|ENDS[A-Z]|Elective Options)"
)
_CODE_ONLY_RE = re.compile(r"^[A-Z]\d{3}[A-Z]?\s+\S")


def _parse_roster(lines: list[str], ccn_idx: int, end: int) -> list[dict]:
    """
    Parse the course roster table from catalog lines[ccn_idx:end].
    Handles title wrap-to-next-line, copyright footers, and ENDS* markers.
    Returns list of {term, code, title, cus}.
    """
    courses = []
    pending: dict | None = None

    for i in range(ccn_idx, end):
        raw = lines[i].rstrip()
        stripped = raw.strip()

        if not stripped:
            continue
        if _SKIP_LINE_RE.match(stripped):
            continue

        m = _COURSE_ROW_RE.match(stripped)
        if m:
            # Flush any pending continuation
            if pending:
                courses.append(pending)
            _, code, title, cus, term = m.groups()
            pending = {
                "term": int(term),
                "code": code,
                "title": title,
                "cus": int(cus),
            }
        else:
            # Could be a title continuation (no leading CCN pattern)
            # Only attach if it looks like plain prose (not a new structural line)
            if (
                pending
                and stripped
                and not re.match(r"^[A-Z]+ \d+", stripped)
                and not re.match(r"^[A-Z]{2,}\s*$", stripped)  # bare school name
            ):
                pending["title"] = pending["title"] + " " + stripped

    if pending:
        courses.append(pending)

    return courses


# ---------------------------------------------------------------------------
# Description extraction
# ---------------------------------------------------------------------------


def _extract_description(lines: list[str], deg_idx: int, ccn_idx: int) -> str:
    """
    Collect description lines between the degree heading and the CCN table.
    Join with a single space (PDF line-wraps create mid-sentence breaks).
    """
    text_lines = []
    for i in range(deg_idx + 1, ccn_idx):
        stripped = lines[i].rstrip().strip()
        if stripped:
            text_lines.append(stripped)
    return " ".join(text_lines).strip()


# ---------------------------------------------------------------------------
# Outcome extraction
# ---------------------------------------------------------------------------

_OUTCOME_BULLET_RE = re.compile(r"^[•\-]\s+(.+)")
_SCHOOL_HEADER_RE = re.compile(
    r"^(School of Business|School of Technology|School of Education"
    r"|Leavitt School of Health|College of Business|College of Information Technology"
    r"|College of Health Professions|Teachers College)$"
)
# Program headings in the outcomes section look like:
#   "B.S. Accounting", "M.S. Cybersecurity...", "B.A., Elementary Education"
# They start with a known degree abbreviation followed by a period/comma.
_DEGREE_PREFIX_RE = re.compile(
    r"^(B\.S\.|M\.S\.|B\.A\.|M\.A\.|M\.B\.A\.|B\.S\.N\.|M\.S\.N\.|"
    r"Ph\.D\.|Ed\.D\.|M\.Ed\.|B\.A\.S\.|Certificate[:\s]|Graduate Certificate|"
    r"Associate of\s|Bachelor of\s|Master of\s|Doctor of\s)"
)
_PROGRAM_OUTCOMES_START = "Program Outcomes"


def _parse_outcomes(lines: list[str]) -> dict[str, list[str]]:
    """
    Parse the Program Outcomes section.
    Returns a dict mapping abbreviated degree label → list of outcome strings.
    e.g. {"B.S. Accounting": ["The graduate explains...", ...], ...}
    """
    # Find the start line
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == _PROGRAM_OUTCOMES_START:
            start_idx = i + 1
            break
    if start_idx is None:
        return {}

    outcomes: dict[str, list[str]] = {}
    current_program: str | None = None
    current_bullets: list[str] = []
    in_bullet = False
    pending_bullet = ""

    def flush_program():
        nonlocal current_program, current_bullets
        if current_program and current_bullets:
            outcomes[current_program] = list(current_bullets)
        current_program = None
        current_bullets = []

    def flush_bullet():
        nonlocal in_bullet, pending_bullet
        if in_bullet and pending_bullet.strip():
            current_bullets.append(pending_bullet.strip())
        in_bullet = False
        pending_bullet = ""

    for i in range(start_idx, len(lines)):
        raw = lines[i].rstrip()
        stripped = raw.strip()

        # Stop at instructor directory
        if stripped.startswith("Instructor Directory"):
            break

        if not stripped or "©" in stripped:
            continue

        # School header — no-op
        if _SCHOOL_HEADER_RE.match(stripped):
            flush_bullet()
            continue

        # Bullet line (must check before program heading)
        m = _OUTCOME_BULLET_RE.match(stripped)
        if m:
            flush_bullet()
            in_bullet = True
            pending_bullet = m.group(1)
            continue

        # Program heading: must match degree prefix pattern
        if _DEGREE_PREFIX_RE.match(stripped):
            flush_bullet()
            flush_program()
            current_program = stripped
            current_bullets = []
            continue

        # Continuation of an open bullet (lowercase continuation, no degree prefix)
        if in_bullet and stripped and not _DEGREE_PREFIX_RE.match(stripped):
            pending_bullet += " " + stripped
            continue

    flush_bullet()
    flush_program()

    return outcomes


# ---------------------------------------------------------------------------
# Match outcomes to program codes
# ---------------------------------------------------------------------------


def _normalize_for_match(s: str) -> str:
    """Lowercase and strip leading degree-type prefixes / punctuation for fuzzy matching."""
    s = s.lower()
    # Remove leading abbreviated prefixes
    leading_abbrev = (
        r"^(b\.s\.|m\.s\.|b\.a\.|m\.a\.|m\.b\.a\.|m\.ed\.|b\.s\.n\.|m\.s\.n\.|"
        r"ph\.d\.|ed\.d\.|b\.a\.s\.|b\.a\.,|m\.a\.,|b\.s\.,|graduate certificate[:\s]*"
        r"|certificate[:\s]*)\s*"
    )
    s = re.sub(leading_abbrev, "", s).strip()
    # Remove leading long-form degree type (anchored to start)
    leading_long = (
        r"^(bachelor of science in nursing|master of science in nursing|"
        r"doctor of education|doctor of philosophy|"
        r"bachelor of science,?\s*|master of science,?\s*|bachelor of arts,?\s*|"
        r"master of arts,?\s*|master of business administration,?\s*)\s*"
    )
    s = re.sub(leading_long, "", s).strip()
    s = re.sub(r"[,\-\(\)]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _match_outcome_to_code(
    outcome_label: str,
    programs: list[dict],
) -> str | None:
    """
    Try to match an outcome section label to a program_code.
    Strategy: normalize both sides and find the program whose canonical_name
    best overlaps the label.
    """
    norm_label = _normalize_for_match(outcome_label)
    # If normalization stripped everything (e.g. "Master of Business Administration"),
    # use the raw lowercased label words for matching
    if not norm_label.strip():
        norm_label = re.sub(r"[,\-\(\)]", " ", outcome_label.lower())
        norm_label = re.sub(r"\s+", " ", norm_label).strip()

    best_code = None
    best_score = 0

    for p in programs:
        if p["status"] != "ACTIVE":
            continue
        for heading in p.get("degree_headings", [p["canonical_name"]]):
            norm_heading = _normalize_for_match(heading)
            if not norm_heading.strip():
                # Also fall back for canonical name
                norm_heading = re.sub(r"[,\-\(\)]", " ", heading.lower())
                norm_heading = re.sub(r"\s+", " ", norm_heading).strip()
            # Simple word overlap score
            label_words = set(norm_label.split())
            heading_words = set(norm_heading.split())
            if not label_words:
                continue
            overlap = len(label_words & heading_words)
            score = overlap / len(label_words)  # precision
            if score > best_score and score >= 0.5:
                best_score = score
                best_code = p["program_code"]

    return best_code


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, help="Path to catalog_2026_03.txt")
    parser.add_argument("--blocks", required=True, help="Path to 2026_03_program_blocks_v11.json")
    parser.add_argument("--programs", required=True, help="Path to programs.json")
    parser.add_argument("--out", required=True, help="Output path for program_enriched.json")
    args = parser.parse_args()

    catalog_path = Path(args.catalog)
    blocks_path = Path(args.blocks)
    programs_path = Path(args.programs)
    out_path = Path(args.out)

    if not catalog_path.exists():
        sys.exit(f"ERROR: catalog file not found: {catalog_path}")
    if not blocks_path.exists():
        sys.exit(f"ERROR: blocks file not found: {blocks_path}")
    if not programs_path.exists():
        sys.exit(f"ERROR: programs file not found: {programs_path}")

    print(f"Loading catalog: {catalog_path}")
    with open(catalog_path, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    print(f"  {len(lines):,} lines")

    print(f"Loading program blocks: {blocks_path}")
    with open(blocks_path) as f:
        blocks = json.load(f)
    print(f"  {len(blocks)} blocks")

    print(f"Loading programs: {programs_path}")
    with open(programs_path) as f:
        programs = json.load(f)
    print(f"  {len(programs)} programs")

    # Build a code → program map for quick lookup
    code_to_program = {p["program_code"]: p for p in programs}

    # Parse outcomes section
    print("Parsing program outcomes...")
    outcomes_by_label = _parse_outcomes(lines)
    print(f"  Found {len(outcomes_by_label)} outcome blocks")

    # Match outcome labels to program codes
    outcomes_by_code: dict[str, list[str]] = {}
    unmatched_labels: list[str] = []
    for label, bullets in outcomes_by_label.items():
        code = _match_outcome_to_code(label, programs)
        if code:
            # Prefer the longest-matching outcome set if multiple labels hit same code
            if code not in outcomes_by_code or len(bullets) > len(outcomes_by_code[code]):
                outcomes_by_code[code] = bullets
        else:
            unmatched_labels.append(label)

    print(f"  Matched {len(outcomes_by_code)} programs to outcome blocks")
    if unmatched_labels:
        print(f"  Unmatched labels ({len(unmatched_labels)}): {unmatched_labels[:5]}")

    # Process each program block
    enriched: dict[str, dict] = {}

    for block in blocks:
        code = block["code"]
        deg_idx = block["deg_idx"]
        ccn_idx = block["ccn_idx"]
        end = block["end"]

        # Description
        description = _extract_description(lines, deg_idx, ccn_idx)

        # Course roster
        roster = _parse_roster(lines, ccn_idx, end)

        # Outcomes (matched earlier)
        outcomes = outcomes_by_code.get(code, [])

        enriched[code] = {
            "program_code": code,
            "description": description,
            "description_source": "WGU Catalog 2026-03",
            "roster": roster,
            "roster_source": "WGU Catalog 2026-03",
            "outcomes": outcomes,
            "outcomes_source": "WGU Catalog 2026-03" if outcomes else None,
        }

    # Summary
    with_desc = sum(1 for v in enriched.values() if v["description"])
    with_roster = sum(1 for v in enriched.values() if v["roster"])
    with_outcomes = sum(1 for v in enriched.values() if v["outcomes"])
    total_courses = sum(len(v["roster"]) for v in enriched.values())

    print(f"\nExtraction summary:")
    print(f"  Programs with description: {with_desc}/{len(enriched)}")
    print(f"  Programs with roster:      {with_roster}/{len(enriched)}")
    print(f"  Programs with outcomes:    {with_outcomes}/{len(enriched)}")
    print(f"  Total roster course rows:  {total_courses}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(enriched, f, indent=2)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
