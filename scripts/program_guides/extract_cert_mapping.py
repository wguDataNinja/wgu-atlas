"""
extract_cert_mapping.py

Phase 1 of guide targets extraction: certification prep mention normalization.

Reads all data/program_guides/parsed/*.json, extracts certification_prep_mentions
from every AoS course across all programs, normalizes and filters them, groups by
(normalized_cert, course_title), resolves course titles to catalog codes, and
separates auto-accepted from review-needed records.

Inputs:
  data/program_guides/parsed/*_parsed.json
  data/program_guides/enrichment/course_enrichment_candidates.json
  public/data/courses.json

Outputs:
  data/program_guides/cert_course_mapping.json
"""

import json
import os
import re
from collections import defaultdict
from datetime import date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARSED_DIR = os.path.join(REPO_ROOT, "data", "program_guides", "parsed")
ENRICHMENT_CANDIDATES = os.path.join(REPO_ROOT, "data", "program_guides", "enrichment", "course_enrichment_candidates.json")
COURSES_JSON = os.path.join(REPO_ROOT, "public", "data", "courses.json")
OUTPUT_PATH = os.path.join(REPO_ROOT, "data", "program_guides", "cert_course_mapping.json")

# ---------------------------------------------------------------------------
# Normalization rules (from GUIDE_TARGETS_EXTRACTION_PLAN.md Section 1)
# ---------------------------------------------------------------------------

# Full whitelist after punctuation stripping — all canonical cert names
WHITELIST = [
    "CompTIA A+",
    "CompTIA Network+",
    "CompTIA Security+",
    "CompTIA Cloud+",
    "CompTIA Project+",
    "CompTIA CySA+",
    "CompTIA Cybersecurity",
    "AWS Certified",
    "AWS Cloud",
    "AWS CLI",
    "AWS Capstone",
    "AWS platform",
    "AWS environment",
    "Azure Fundamentals",
    "Azure services",
    "Azure platform",
    "Azure environment",
    "Azure Solution",
    "Azure CLI",
    "Cisco Certified",
    "Cisco Cybersecurity",
    "Cisco DevNet",
    "Praxis 5039",
    "Praxis 5081",
    "Praxis exam",
    "Praxis prep",
    "Praxis Social",
    "CPA Code",
]

WHITELIST_SET = set(WHITELIST)
WHITELIST_LOWER = {w.lower(): w for w in WHITELIST}

# Suppress pattern: lowercase "aws [word]" — these are substring matches from
# words like "laws", "draws", "straws" in course text (extraction artifact)
SUPPRESS_PATTERN = re.compile(r'^aws [a-z]', re.IGNORECASE)


def strip_trailing_punct(s: str) -> str:
    """Strip trailing punctuation characters from a string."""
    return s.rstrip(".,;:!?")


def normalize_cert(raw: str) -> tuple[str | None, str]:
    """
    Returns (normalized_cert_or_None, disposition).
    disposition: 'whitelist_exact' | 'whitelist_after_strip' | 'suppressed_aws_noise' | 'noise'
    """
    stripped = strip_trailing_punct(raw).strip()

    # Suppress lowercase-aws fragments (e.g. "aws in", "aws that")
    # Rule: starts with lowercase 'aws ' (not uppercase AWS)
    if re.match(r'^aws [a-z]', stripped) and not stripped.startswith("AWS"):
        return None, "suppressed_aws_noise"

    # Normalize Praxis variants first (before whitelist check to ensure canonical form)
    if stripped.lower().startswith("praxis exam"):
        return "Praxis exam", "whitelist_after_strip"
    if stripped.lower().startswith("praxis prep"):
        # "Praxis prep" and "Praxis exam" both mean generic Praxis prep signal
        return "Praxis exam", "whitelist_after_strip"
    # "Praxis Social" — fragment, send to noise (not specific enough)
    if stripped.lower().startswith("praxis social"):
        return None, "noise"

    # Exact match against whitelist (case-sensitive)
    if stripped in WHITELIST_SET:
        return stripped, "whitelist_exact"

    # Case-insensitive match
    if stripped.lower() in WHITELIST_LOWER:
        return WHITELIST_LOWER[stripped.lower()], "whitelist_after_strip"

    # Starts with a recognizable vendor but didn't match — noise bucket
    return None, "noise"


def build_title_to_code_map() -> dict:
    """
    Build a guide-title → resolved_code mapping from course_enrichment_candidates.json.
    Also include canonical_title_current from courses.json as fallback.
    Returns {lowercase_title: course_code}.
    """
    title_map = {}

    # From enrichment candidates: each course has guide_titles_seen with raw_title
    try:
        cands = json.load(open(ENRICHMENT_CANDIDATES))
        for course in cands.get("courses", []):
            code = course.get("course_code")
            canonical = course.get("canonical_title_current", "")
            if code and canonical:
                title_map[canonical.strip().lower()] = code
            # Also map guide titles seen
            for gs in course.get("guide_titles_seen", []):
                raw = gs.get("raw_title", "").strip()
                if raw and code:
                    title_map[raw.lower()] = code
    except Exception as e:
        print(f"  Warning: Could not load enrichment candidates: {e}")

    # From courses.json: canonical titles
    try:
        courses = json.load(open(COURSES_JSON))
        for c in courses:
            code = c.get("code")
            title = c.get("title", "").strip()
            if code and title:
                title_map[title.lower()] = code
    except Exception as e:
        print(f"  Warning: Could not load courses.json: {e}")

    return title_map


def resolve_course_code(title: str, title_map: dict) -> str | None:
    """Attempt to resolve a course title to a catalog code."""
    return title_map.get(title.strip().lower())


def main():
    print("Phase 1: Cert mapping extraction")
    print(f"  Parsed dir: {PARSED_DIR}")

    title_map = build_title_to_code_map()
    print(f"  Title-to-code map: {len(title_map)} entries")

    # Collect all cert mentions grouped by (normalized_cert, course_title)
    # Value: set of program codes that carry this cert on this course
    cert_course_programs: dict[tuple, set] = defaultdict(set)
    # Also track raw -> normalized for noise log
    noise_log: list[dict] = []
    suppressed_count = 0
    total_raw = 0

    parsed_files = sorted(f for f in os.listdir(PARSED_DIR) if f.endswith("_parsed.json"))
    print(f"  Parsed files: {len(parsed_files)}")

    for fname in parsed_files:
        program_code = fname.replace("_parsed.json", "")
        data = json.load(open(os.path.join(PARSED_DIR, fname)))
        aos = data.get("areas_of_study", [])

        for group in aos:
            for course in group.get("courses", []):
                course_title = course.get("title", "").strip()
                raw_mentions = course.get("certification_prep_mentions", []) or []

                for raw in raw_mentions:
                    if not raw or not raw.strip():
                        continue
                    total_raw += 1
                    normalized, disposition = normalize_cert(raw)

                    if disposition == "suppressed_aws_noise":
                        suppressed_count += 1
                        continue
                    elif normalized is None:
                        noise_log.append({
                            "raw": raw,
                            "stripped": strip_trailing_punct(raw).strip(),
                            "course_title": course_title,
                            "program_code": program_code,
                            "disposition": disposition,
                        })
                        continue

                    cert_course_programs[(normalized, course_title)].add(program_code)

    print(f"  Total raw cert mentions: {total_raw}")
    print(f"  Suppressed (aws noise): {suppressed_count}")
    print(f"  Noise bucket: {len(noise_log)}")
    print(f"  Unique (cert, course) pairs: {len(cert_course_programs)}")

    # Build output records
    auto_accepted = []
    review_needed = []

    for (normalized_cert, course_title), programs in sorted(
        cert_course_programs.items(), key=lambda x: (-len(x[1]), x[0][0], x[0][1])
    ):
        program_list = sorted(programs)
        program_count = len(programs)
        matched_code = resolve_course_code(course_title, title_map)

        # Determine confidence and recommendation
        if program_count >= 3:
            confidence = "high"
        elif program_count >= 1:
            confidence = "medium"
        else:
            confidence = "low"

        # Atlas recommendation logic
        if normalized_cert in ("Azure Fundamentals", "Azure services", "Azure platform",
                                "Azure environment", "Azure Solution", "Azure CLI",
                                "Cisco Certified", "Cisco Cybersecurity", "Cisco DevNet",
                                "AWS Capstone", "AWS platform", "AWS environment"):
            atlas_recommendation = "degree-only"
        elif normalized_cert in ("Praxis exam",):
            atlas_recommendation = "degree-only"
        elif normalized_cert == "CPA Code":
            atlas_recommendation = "review-required"
        elif confidence == "high":
            atlas_recommendation = "use"
        elif confidence == "medium":
            atlas_recommendation = "use"
        else:
            atlas_recommendation = "review-required"

        record = {
            "normalized_cert": normalized_cert,
            "source_course_title": course_title,
            "matched_course_code": matched_code,
            "source_programs": program_list,
            "source_program_count": program_count,
            "confidence": confidence,
            "atlas_recommendation": atlas_recommendation,
        }

        if program_count >= 3 and matched_code:
            auto_accepted.append(record)
        else:
            review_needed.append(record)

    print(f"\n  Auto-accepted (≥3 programs + resolved code): {len(auto_accepted)}")
    print(f"  Review needed: {len(review_needed)}")

    # Print high-confidence summary
    print("\n  High-confidence cert → course mappings:")
    for r in auto_accepted:
        print(f"    {r['normalized_cert']:30s}  {r['source_course_title']:45s}  {r['matched_course_code']:6s}  ({r['source_program_count']} programs)")

    # Build output artifact
    output = {
        "generated_on": str(date.today()),
        "source": "data/program_guides/parsed/*_parsed.json",
        "total_raw_cert_mentions": total_raw,
        "suppressed_aws_noise_count": suppressed_count,
        "noise_bucket_count": len(noise_log),
        "unique_cert_course_pairs": len(cert_course_programs),
        "auto_accepted_count": len(auto_accepted),
        "review_needed_count": len(review_needed),
        "auto_accepted": auto_accepted,
        "review_needed": review_needed,
        "noise_log": noise_log,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
