"""
extract_prereq_relationships.py

Phase 2 of guide targets extraction: prerequisite relationship recovery.

Reads all data/program_guides/parsed/*.json, extracts prerequisite_mentions from
every AoS course, filters false positives, classifies by type, resolves course
titles/codes to catalog codes, and emits structured prerequisite relationship records.

Prerequisite type taxonomy (from GUIDE_TARGETS_EXTRACTION_PLAN.md Section 2):
  explicit-course-prereq       — named course title as stated prereq
  code-anchored-prereq         — WGU course code present in the mention
  cumulative-sequence-prereq   — nursing-style: all prior terms + specific code
  inverted-capture             — extraction captured prereq from wrong direction
  soft-preparedness            — vague prior knowledge language (log, suppress)
  false-positive               — no-prereq declarations (filter before all else)

Inputs:
  data/program_guides/parsed/*_parsed.json
  data/program_guides/enrichment/course_enrichment_candidates.json
  public/data/courses.json

Outputs:
  data/program_guides/prereq_relationships.json
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
OUTPUT_PATH = os.path.join(REPO_ROOT, "data", "program_guides", "prereq_relationships.json")

# ---------------------------------------------------------------------------
# False positive filter — exact strings and patterns (filter FIRST)
# ---------------------------------------------------------------------------

SUPPRESS_EXACT = {
    "for this course and there is no specific technical knowledge needed",
    "for this course",
    "to this course",
    "The following",
}

# "for this course is X" — means X is the prereq for the current course_title (not inverted)
# These are extracted as explicit-course-prereq, not inverted-capture
FOR_THIS_COURSE_IS_PATTERN = re.compile(r'^for this course is (.+)$', re.IGNORECASE)

SUPPRESS_PATTERNS = [
    re.compile(r'^There is no prerequisite', re.IGNORECASE),
    re.compile(r'^No prerequisite', re.IGNORECASE),
    re.compile(r'^no prerequisite', re.IGNORECASE),
    re.compile(r'has no prerequisites', re.IGNORECASE),
    re.compile(r'are no prerequisites', re.IGNORECASE),
    # Completion phrases without a specific course name
    re.compile(r'^Completion of the specialty courses', re.IGNORECASE),
]

# Soft-preparedness patterns — vague prior knowledge, no specific course
SOFT_PREP_PATTERNS = [
    re.compile(r'^Successful completion of a college level', re.IGNORECASE),
    re.compile(r'^Previous coursework in', re.IGNORECASE),
    re.compile(r'should be completed prior to beginning', re.IGNORECASE),
]

# Code-anchored patterns
CODE_PATTERN = re.compile(r'\b([A-Z]\d{3,4}(?:-[A-Z0-9]+)?)\b')

# Cumulative sequence patterns
CUMULATIVE_PATTERN = re.compile(
    r'Courses:\s*All prelicensure nursing curriculum courses from previous terms(?: and (\w+))?',
    re.IGNORECASE,
)
MSN_CUMULATIVE_PATTERN = re.compile(
    r'courses are required prior to taking this course:\s*All MSN Core courses and NP Core courses',
    re.IGNORECASE,
)

# Inverted capture pattern: "for [Course A] is [Course B]" or "to this course is [Course B]"
INVERTED_CAPTURE_PATTERN = re.compile(
    r'^(?:for|to) (?:this course is|Financial Management I is|Composition II|[A-Z])'
)
INVERTED_FOR_PATTERN = re.compile(
    r'^for (\w[\w\s\-:]+?) is ([A-Z][\w\s\-:]+)$'
)
INVERTED_TO_PATTERN = re.compile(
    r'^to this course is (.+)$'
)


def build_catalog_lookup() -> tuple[dict, dict]:
    """
    Build two lookups:
      title_to_code: {lowercase_title: code}
      code_to_title: {code: canonical_title}
    """
    title_to_code = {}
    code_to_title = {}

    # From enrichment candidates
    try:
        cands = json.load(open(ENRICHMENT_CANDIDATES))
        for course in cands.get("courses", []):
            code = course.get("course_code")
            canonical = course.get("canonical_title_current", "").strip()
            if code and canonical:
                title_to_code[canonical.lower()] = code
                code_to_title[code] = canonical
            for gs in course.get("guide_titles_seen", []):
                raw = gs.get("raw_title", "").strip()
                if raw and code:
                    title_to_code[raw.lower()] = code
    except Exception as e:
        print(f"  Warning: Could not load enrichment candidates: {e}")

    # From courses.json
    try:
        courses = json.load(open(COURSES_JSON))
        for c in courses:
            code = c.get("code")
            title = c.get("title", "").strip()
            if code and title:
                if title.lower() not in title_to_code:
                    title_to_code[title.lower()] = code
                if code not in code_to_title:
                    code_to_title[code] = title
    except Exception as e:
        print(f"  Warning: Could not load courses.json: {e}")

    return title_to_code, code_to_title


def levenshtein(s1: str, s2: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]


def fuzzy_title_match(title: str, title_to_code: dict, max_dist: int = 3) -> tuple[str | None, str | None]:
    """
    Try to match `title` against catalog titles.
    Returns (matched_title, code) or (None, None).
    """
    tl = title.strip().lower()

    # Exact match first
    if tl in title_to_code:
        code = title_to_code[tl]
        return title, code

    # Fuzzy match
    best_dist = max_dist + 1
    best_code = None
    best_title = None
    for catalog_title, code in title_to_code.items():
        dist = levenshtein(tl, catalog_title)
        if dist <= max_dist and dist < best_dist:
            best_dist = dist
            best_code = code
            best_title = catalog_title
    if best_title:
        return best_title, best_code
    return None, None


def is_false_positive(mention: str) -> bool:
    """Returns True if the mention is a no-prereq false positive."""
    m = mention.strip()
    if m in SUPPRESS_EXACT:
        return True
    for pattern in SUPPRESS_PATTERNS:
        if pattern.search(m):
            return True
    return False


def is_soft_prep(mention: str) -> bool:
    """Returns True if mention is vague soft-preparedness language."""
    m = mention.strip()
    for pattern in SOFT_PREP_PATTERNS:
        if pattern.search(m):
            return True
    return False


def classify_and_extract(
    mention: str,
    course_title: str,
    program_code: str,
    title_to_code: dict,
    code_to_title: dict,
) -> dict | None:
    """
    Classify a prereq mention and return a structured record, or None if suppressed.
    """
    m = mention.strip()

    # --- Type: cumulative-sequence-prereq (nursing) ---
    cm = CUMULATIVE_PATTERN.search(m)
    if cm:
        additional_code = cm.group(1)
        prereq_code = additional_code if additional_code else None
        prereq_title = code_to_title.get(prereq_code) if prereq_code else None
        return {
            "prereq_value": m,
            "prereq_type": "cumulative-sequence-prereq",
            "normalized_prereq_title": prereq_title,
            "normalized_prereq_code": prereq_code,
            "confidence": "medium",
            "review_status": "review-required",
            "notes": f"Cumulative sequence prereq; all prior nursing terms required{'; additional code: ' + prereq_code if prereq_code else ''}",
            "recovery_method": "template_parse + code_extraction",
        }

    # MSN Core cumulative
    if MSN_CUMULATIVE_PATTERN.search(m):
        return {
            "prereq_value": m,
            "prereq_type": "cumulative-sequence-prereq",
            "normalized_prereq_title": None,
            "normalized_prereq_code": None,
            "confidence": "medium",
            "review_status": "review-required",
            "notes": "Cumulative sequence prereq: all MSN Core + NP Core courses required",
            "recovery_method": "template_parse",
        }

    # --- "for this course is X" — direct prereq statement ---
    ftci = FOR_THIS_COURSE_IS_PATTERN.match(m)
    if ftci:
        prereq_title_raw = ftci.group(1).strip()
        matched_title, prereq_code = fuzzy_title_match(prereq_title_raw, title_to_code)
        return {
            "prereq_value": m,
            "prereq_type": "explicit-course-prereq",
            "normalized_prereq_title": matched_title or prereq_title_raw,
            "normalized_prereq_code": prereq_code,
            "confidence": "high" if prereq_code else "medium",
            "review_status": "auto-accepted" if prereq_code else "review-required",
            "notes": None,
            "recovery_method": "for_this_course_is_pattern",
        }

    # --- Type: code-anchored-prereq ---
    codes = CODE_PATTERN.findall(m)
    # Filter to codes that look like WGU course codes (letter + digits)
    valid_codes = [c for c in codes if re.match(r'^[A-Z]\d{3,4}', c)]
    if valid_codes:
        # Use first resolvable code as the main prereq
        for code_candidate in valid_codes:
            base_code = code_candidate.split("-")[0]
            if base_code in code_to_title:
                prereq_title = code_to_title[base_code]
                return {
                    "prereq_value": m,
                    "prereq_type": "code-anchored-prereq",
                    "normalized_prereq_title": prereq_title,
                    "normalized_prereq_code": base_code,
                    "confidence": "high",
                    "review_status": "auto-accepted",
                    "notes": f"Code {base_code} found in catalog",
                    "recovery_method": "code_extraction",
                }
        # Code found but not in catalog
        return {
            "prereq_value": m,
            "prereq_type": "code-anchored-prereq",
            "normalized_prereq_title": None,
            "normalized_prereq_code": valid_codes[0],
            "confidence": "medium",
            "review_status": "review-required",
            "notes": f"Code(s) {valid_codes} extracted but not found in current catalog",
            "recovery_method": "code_extraction",
        }

    # --- Type: inverted-capture ---
    # Pattern: "for X is Y" — extraction captured inverted direction
    ic_for = INVERTED_FOR_PATTERN.match(m)
    if ic_for:
        target_title = ic_for.group(1).strip()
        prereq_title_raw = ic_for.group(2).strip()
        _, prereq_code = fuzzy_title_match(prereq_title_raw, title_to_code)
        return {
            "prereq_value": m,
            "prereq_type": "inverted-capture",
            "normalized_prereq_title": prereq_title_raw,
            "normalized_prereq_code": prereq_code,
            "confidence": "medium",
            "review_status": "review-required",
            "notes": f"Inverted capture — prereq={prereq_title_raw}, actual target={target_title}. Verify direction.",
            "recovery_method": "sentence_inversion_parse",
        }

    # Pattern: "to this course is X"
    ic_to = INVERTED_TO_PATTERN.match(m)
    if ic_to:
        prereq_title_raw = ic_to.group(1).strip()
        matched_title, prereq_code = fuzzy_title_match(prereq_title_raw, title_to_code)
        return {
            "prereq_value": m,
            "prereq_type": "explicit-course-prereq",
            "normalized_prereq_title": matched_title or prereq_title_raw,
            "normalized_prereq_code": prereq_code,
            "confidence": "high" if prereq_code else "medium",
            "review_status": "auto-accepted" if prereq_code else "review-required",
            "notes": f"Prereq extracted from 'to this course is X' pattern",
            "recovery_method": "inversion_pattern_parse",
        }

    # "for Composition II" pattern — course being listed as having this prereq
    if m.startswith("for Composition II"):
        return {
            "prereq_value": m,
            "prereq_type": "explicit-course-prereq",
            "normalized_prereq_title": "Composition I",
            "normalized_prereq_code": title_to_code.get("composition i"),
            "confidence": "medium",
            "review_status": "review-required",
            "notes": "Extracted as 'for Composition II' — likely means Composition I is prereq for Composition II",
            "recovery_method": "pattern_parse",
        }

    # --- Type: explicit-course-prereq — multi-course strings ---
    # Handle patterns like "A, B, and C" or "A and B"
    # First try direct fuzzy match on the whole string
    matched_title, prereq_code = fuzzy_title_match(m, title_to_code)
    if matched_title and prereq_code:
        return {
            "prereq_value": m,
            "prereq_type": "explicit-course-prereq",
            "normalized_prereq_title": matched_title,
            "normalized_prereq_code": prereq_code,
            "confidence": "high",
            "review_status": "auto-accepted",
            "notes": None,
            "recovery_method": "catalog_title_match",
        }

    # Try splitting on "and" / "," for multi-course strings
    parts = re.split(r',\s*|\s+and\s+', m)
    parts = [p.strip() for p in parts if p.strip() and len(p.strip()) > 3]
    if len(parts) > 1:
        resolved_parts = []
        for part in parts:
            pt, pc = fuzzy_title_match(part, title_to_code)
            if pt and pc:
                resolved_parts.append({"title": pt, "code": pc})
        if resolved_parts:
            return {
                "prereq_value": m,
                "prereq_type": "explicit-course-prereq",
                "normalized_prereq_title": "; ".join(r["title"] for r in resolved_parts),
                "normalized_prereq_code": "; ".join(r["code"] for r in resolved_parts),
                "confidence": "high" if len(resolved_parts) == len(parts) else "medium",
                "review_status": "auto-accepted" if len(resolved_parts) == len(parts) else "review-required",
                "notes": f"Multi-prereq: {len(resolved_parts)}/{len(parts)} resolved",
                "recovery_method": "multi_title_split + catalog_title_match",
            }

    # Unresolved explicit title
    return {
        "prereq_value": m,
        "prereq_type": "explicit-course-prereq",
        "normalized_prereq_title": None,
        "normalized_prereq_code": None,
        "confidence": "low",
        "review_status": "review-required",
        "notes": "Could not resolve to catalog code — may be retired course or wording variation",
        "recovery_method": "unresolved",
    }


def main():
    print("Phase 2: Prerequisite relationship extraction")
    print(f"  Parsed dir: {PARSED_DIR}")

    title_to_code, code_to_title = build_catalog_lookup()
    print(f"  Title-to-code: {len(title_to_code)} entries, Code-to-title: {len(code_to_title)} entries")

    parsed_files = sorted(f for f in os.listdir(PARSED_DIR) if f.endswith("_parsed.json"))
    print(f"  Parsed files: {len(parsed_files)}")

    total_raw = 0
    false_positive_count = 0
    soft_prep_count = 0
    soft_prep_log = []
    records = []

    # Accumulate (prereq_value, course_title) → list of program codes
    # so we can merge multi-program occurrences
    key_to_data: dict[tuple, dict] = {}
    key_to_programs: dict[tuple, set] = defaultdict(set)

    for fname in parsed_files:
        program_code = fname.replace("_parsed.json", "")
        data = json.load(open(os.path.join(PARSED_DIR, fname)))
        aos = data.get("areas_of_study", [])

        for group in aos:
            for course in group.get("courses", []):
                course_title = course.get("title", "").strip()
                raw_mentions = course.get("prerequisite_mentions", []) or []

                for mention in raw_mentions:
                    if not mention or not mention.strip():
                        continue
                    total_raw += 1

                    # Step 1: Filter false positives
                    if is_false_positive(mention):
                        false_positive_count += 1
                        continue

                    # Step 2: Filter soft preparedness
                    if is_soft_prep(mention):
                        soft_prep_count += 1
                        soft_prep_log.append({
                            "prereq_value": mention,
                            "course_title": course_title,
                            "program_code": program_code,
                        })
                        continue

                    # Step 3: Classify and extract
                    record = classify_and_extract(
                        mention, course_title, program_code, title_to_code, code_to_title
                    )
                    if record is None:
                        continue

                    key = (mention.strip(), course_title)
                    key_to_programs[key].add(program_code)

                    if key not in key_to_data:
                        # Need to resolve target course code too
                        target_code = title_to_code.get(course_title.lower())
                        record["target_course_title"] = course_title
                        record["target_course_code"] = target_code
                        key_to_data[key] = record

    # Merge source programs into each record
    auto_accepted = []
    review_needed = []

    for key, record in key_to_data.items():
        programs = sorted(key_to_programs[key])
        record["source_programs"] = programs
        record["source_program_count"] = len(programs)

        # Upgrade confidence if cross-program confirmed
        if len(programs) >= 3 and record["confidence"] == "medium":
            record["confidence"] = "high"
        if len(programs) >= 2 and record["review_status"] == "review-required" and record["normalized_prereq_code"]:
            record["review_status"] = "auto-accepted"

        if record["review_status"] == "auto-accepted":
            auto_accepted.append(record)
        else:
            review_needed.append(record)

    # Sort: auto-accepted first by program count desc, then by course title
    auto_accepted.sort(key=lambda r: (-r["source_program_count"], r["target_course_title"]))
    review_needed.sort(key=lambda r: (-r["source_program_count"], r["target_course_title"]))

    print(f"\n  Total raw prereq mentions: {total_raw}")
    print(f"  False positives suppressed: {false_positive_count}")
    print(f"  Soft preparedness suppressed: {soft_prep_count}")
    remaining = total_raw - false_positive_count - soft_prep_count
    print(f"  Remaining actionable mentions: {remaining}")
    print(f"  Auto-accepted: {len(auto_accepted)}")
    print(f"  Review needed: {len(review_needed)}")

    # Count by type
    from collections import Counter
    type_counts = Counter(r["prereq_type"] for r in auto_accepted + review_needed)
    print(f"\n  By type: {dict(type_counts)}")

    print(f"\n  Auto-accepted prerequisites:")
    for r in auto_accepted:
        print(f"    {r['target_course_title'][:35]:35s}  ←prereq—  {r.get('normalized_prereq_title', r['prereq_value'])[:35]:35s}  ({r['source_program_count']} progs)  [{r['prereq_type']}]")

    output = {
        "generated_on": str(date.today()),
        "source": "data/program_guides/parsed/*_parsed.json",
        "total_raw_prereq_mentions": total_raw,
        "false_positives_suppressed": false_positive_count,
        "soft_preparedness_suppressed": soft_prep_count,
        "unique_prereq_records": len(key_to_data),
        "auto_accepted_count": len(auto_accepted),
        "review_needed_count": len(review_needed),
        "type_distribution": dict(type_counts),
        "auto_accepted": auto_accepted,
        "review_needed": review_needed,
        "soft_prep_log": soft_prep_log,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
