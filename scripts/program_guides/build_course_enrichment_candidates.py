"""
build_course_enrichment_candidates.py

Strict-unique-only extraction pass for course-level enrichment data.
Reads the pre-built roster bridge and extracts course-level enrichment
data for every uniquely attachable course occurrence.

Inputs:
  data/program_guides/bridge/index.json
  data/program_guides/bridge/guides/{program_code}.json
  data/program_guides/parsed/{program_code}_parsed.json
  data/canonical_courses.csv

Outputs:
  data/program_guides/enrichment/course_enrichment_candidates.json
  data/program_guides/enrichment/course_enrichment_summary.json
"""

import csv
import json
import os
from collections import defaultdict
from datetime import date

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANONICAL_CSV = os.path.join(REPO_ROOT, "data", "canonical_courses.csv")
BRIDGE_INDEX = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "index.json")
BRIDGE_GUIDE_DIR = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "guides")
PARSED_GUIDE_DIR = os.path.join(REPO_ROOT, "data", "program_guides", "parsed")
ENRICHMENT_DIR = os.path.join(REPO_ROOT, "data", "program_guides", "enrichment")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
UNIQUE_ANCHOR_CLASSES = {
    "exact_current_unique",
    "exact_observed_variant_unique",
    "normalization_unique",
}

CANDIDATES_OUT = os.path.join(ENRICHMENT_DIR, "course_enrichment_candidates.json")
SUMMARY_OUT = os.path.join(ENRICHMENT_DIR, "course_enrichment_summary.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_canonical_courses(csv_path):
    """Return dict keyed by course_code with relevant fields."""
    courses = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            courses[row["course_code"]] = {
                "canonical_title_current": row.get("canonical_title_current", ""),
                "canonical_cus": row.get("canonical_cus", ""),
                "current_college": row.get("current_college", ""),
            }
    return courses


def build_aos_lookup(parsed_guide):
    """
    Build title -> {description, competency_bullets, aos_group} from parsed guide.
    Uses exact title as key (case-sensitive, as found in guide).
    """
    lookup = {}
    for aos in parsed_guide.get("areas_of_study", []):
        group = aos.get("group", "")
        for course in aos.get("courses", []):
            title = course.get("title", "")
            if title:
                lookup[title] = {
                    "description": course.get("description", ""),
                    "competency_bullets": course.get("competency_bullets", []),
                    "aos_group": group,
                }
    return lookup


def make_bullets_key(bullets):
    """Hashable key for a competency bullet list."""
    return tuple(bullets)


def add_to_desc_set(desc_set, text, program_code, guide_key):
    """
    desc_set: list of {text, char_length, source_guides, source_program_codes}
    Deduplicate by exact text; merge sources.
    """
    for entry in desc_set:
        if entry["text"] == text:
            if guide_key not in entry["source_guides"]:
                entry["source_guides"].append(guide_key)
            if program_code not in entry["source_program_codes"]:
                entry["source_program_codes"].append(program_code)
            return
    desc_set.append({
        "text": text,
        "char_length": len(text),
        "source_guides": [guide_key],
        "source_program_codes": [program_code],
    })


def add_to_comp_set(comp_set, bullets, program_code, guide_key):
    """
    comp_set: list of {bullets, bullet_count, source_guides, source_program_codes}
    Deduplicate by exact bullet list; merge sources.
    """
    key = make_bullets_key(bullets)
    for entry in comp_set:
        if make_bullets_key(entry["bullets"]) == key:
            if guide_key not in entry["source_guides"]:
                entry["source_guides"].append(guide_key)
            if program_code not in entry["source_program_codes"]:
                entry["source_program_codes"].append(program_code)
            return
    comp_set.append({
        "bullets": list(bullets),
        "bullet_count": len(bullets),
        "source_guides": [guide_key],
        "source_program_codes": [program_code],
    })


def add_guide_title(guide_titles_seen, raw_title, program_code, guide_key):
    """
    guide_titles_seen: list of {raw_title, source_guides, source_program_codes}
    """
    for entry in guide_titles_seen:
        if entry["raw_title"] == raw_title:
            if guide_key not in entry["source_guides"]:
                entry["source_guides"].append(guide_key)
            if program_code not in entry["source_program_codes"]:
                entry["source_program_codes"].append(program_code)
            return
    guide_titles_seen.append({
        "raw_title": raw_title,
        "source_guides": [guide_key],
        "source_program_codes": [program_code],
    })


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(ENRICHMENT_DIR, exist_ok=True)

    # ---- Load canonical courses ----
    canonical = load_canonical_courses(CANONICAL_CSV)
    print(f"Loaded {len(canonical)} canonical courses.")

    # ---- Load bridge index ----
    with open(BRIDGE_INDEX, encoding="utf-8") as f:
        bridge_index = json.load(f)

    guide_index = bridge_index["guide_index"]
    print(f"Bridge index: {len(guide_index)} guides.")

    # ---- Per-course accumulator ----
    # courses[course_code] = {
    #   course_code, canonical_title_current, canonical_cus, current_college,
    #   aos_mention_count, sp_mention_count,
    #   guide_titles_seen: [...],
    #   descriptions: [...],
    #   competency_sets: [...],
    #   aos_groups_seen: set -> list,
    #   programs_in_aos: [...],
    #   programs_in_sp: [...],
    #   sp_cus_values_seen: set -> list,
    #   anchor_classes_seen: set -> list,
    # }
    courses = {}

    # ---- Counters ----
    total_aos_included = 0
    total_sp_included = 0
    total_skipped_ambiguous = 0
    total_skipped_unmapped = 0
    aos_join_misses = []  # (program_code, guide_title_raw)

    # ---- Iterate guides ----
    for guide_entry in guide_index:
        program_code = guide_entry["program_code"]
        program_code_effective = guide_entry.get("program_code_effective", program_code)
        family = guide_entry.get("family", "")

        # Load bridge guide — files are stored under program_code (not effective)
        bridge_path = os.path.join(BRIDGE_GUIDE_DIR, f"{program_code}.json")
        if not os.path.exists(bridge_path):
            print(f"  WARN: bridge guide not found: {bridge_path}")
            continue
        with open(bridge_path, encoding="utf-8") as f:
            bridge_guide = json.load(f)

        # Load parsed guide — files are stored under program_code (not effective)
        parsed_path = os.path.join(PARSED_GUIDE_DIR, f"{program_code}_parsed.json")
        if not os.path.exists(parsed_path):
            print(f"  WARN: parsed guide not found: {parsed_path}")
            continue
        with open(parsed_path, encoding="utf-8") as f:
            parsed_guide = json.load(f)

        # Build AoS title lookup
        aos_lookup = build_aos_lookup(parsed_guide)

        # guide key for provenance
        guide_key = program_code_effective

        # Process roster rows
        for row in bridge_guide.get("roster_rows", []):
            anchor_class = row.get("anchor_class", "")
            surface = row.get("surface", "")
            guide_title_raw = row.get("guide_title_raw", "")

            # Skip/count non-unique
            if anchor_class.startswith("ambiguous"):
                total_skipped_ambiguous += 1
                continue
            if anchor_class == "unmapped":
                total_skipped_unmapped += 1
                continue
            if anchor_class not in UNIQUE_ANCHOR_CLASSES:
                # unknown class — skip defensively
                total_skipped_unmapped += 1
                continue

            # Get course code
            candidates = row.get("canonical_candidate_codes", [])
            if not candidates:
                total_skipped_unmapped += 1
                continue
            course_code = candidates[0]

            # Initialize course record if needed
            if course_code not in courses:
                cc_info = canonical.get(course_code, {})
                courses[course_code] = {
                    "course_code": course_code,
                    "canonical_title_current": cc_info.get("canonical_title_current", ""),
                    "canonical_cus": cc_info.get("canonical_cus", ""),
                    "current_college": cc_info.get("current_college", ""),
                    "aos_mention_count": 0,
                    "sp_mention_count": 0,
                    "guide_titles_seen": [],
                    "descriptions": [],
                    "competency_sets": [],
                    "_aos_groups_seen": set(),
                    "programs_in_aos": [],
                    "programs_in_sp": [],
                    "_sp_cus_values_seen": set(),
                    "_anchor_classes_seen": set(),
                }

            c = courses[course_code]
            c["_anchor_classes_seen"].add(anchor_class)

            # Add guide title
            add_guide_title(c["guide_titles_seen"], guide_title_raw, program_code, guide_key)

            if surface == "aos":
                total_aos_included += 1
                c["aos_mention_count"] += 1

                # Join to AoS lookup by guide_title_raw (exact)
                aos_data = aos_lookup.get(guide_title_raw)
                if aos_data is None:
                    aos_join_misses.append((program_code, guide_title_raw, course_code))
                    # Still record AoS group from bridge row
                    aos_group = row.get("aos_group", "")
                else:
                    aos_group = aos_data["aos_group"]
                    description = aos_data["description"]
                    comp_bullets = aos_data["competency_bullets"]

                    # Add description (preserve zero-length)
                    if description is not None:
                        add_to_desc_set(c["descriptions"], description, program_code, guide_key)

                    # Add competency set
                    if comp_bullets is not None and len(comp_bullets) > 0:
                        add_to_comp_set(c["competency_sets"], comp_bullets, program_code, guide_key)

                if aos_group:
                    c["_aos_groups_seen"].add(aos_group)

                # programs_in_aos
                c["programs_in_aos"].append({
                    "program_code": program_code,
                    "family": family,
                    "aos_group": row.get("aos_group", ""),
                })

            elif surface == "sp":
                total_sp_included += 1
                c["sp_mention_count"] += 1

                sp_cus = row.get("sp_cus")
                if sp_cus is not None:
                    c["_sp_cus_values_seen"].add(str(sp_cus))

                c["programs_in_sp"].append({
                    "program_code": program_code,
                    "family": family,
                    "sp_term": row.get("sp_term"),
                    "sp_cus": sp_cus,
                })

    # ---- Post-process: convert sets to sorted lists, sort program lists ----
    for course_code, c in courses.items():
        c["aos_groups_seen"] = sorted(c.pop("_aos_groups_seen"))
        c["sp_cus_values_seen"] = sorted(c.pop("_sp_cus_values_seen"))
        c["anchor_classes_seen"] = sorted(c.pop("_anchor_classes_seen"))
        c["programs_in_aos"] = sorted(c["programs_in_aos"], key=lambda x: x["program_code"])
        c["programs_in_sp"] = sorted(c["programs_in_sp"], key=lambda x: x["program_code"])
        c["coverage_note"] = ["strict_unique_subset_only", "ambiguous_rows_excluded"]

    # ---- Sort courses by course_code ----
    sorted_courses = dict(sorted(courses.items()))

    # ---- Build main output ----
    candidates_out = {
        "generated_on": str(date.today()),
        "extraction_scope": "strict_unique_only",
        "total_courses_with_enrichment": len(sorted_courses),
        "total_aos_mentions_included": total_aos_included,
        "total_sp_mentions_included": total_sp_included,
        "total_rows_skipped_ambiguous": total_skipped_ambiguous,
        "total_rows_skipped_unmapped": total_skipped_unmapped,
        "courses": list(sorted_courses.values()),
    }

    with open(CANDIDATES_OUT, "w", encoding="utf-8") as f:
        json.dump(candidates_out, f, indent=2, ensure_ascii=False)

    # ---- Build summary output ----
    courses_with_descriptions = sum(1 for c in sorted_courses.values() if c["descriptions"])
    courses_with_competencies = sum(1 for c in sorted_courses.values() if c["competency_sets"])
    courses_with_sp = sum(1 for c in sorted_courses.values() if c["sp_mention_count"] > 0)
    courses_with_aos = sum(1 for c in sorted_courses.values() if c["aos_mention_count"] > 0)

    courses_with_multi_desc = sum(1 for c in sorted_courses.values() if len(c["descriptions"]) > 1)
    courses_with_multi_comp = sum(1 for c in sorted_courses.values() if len(c["competency_sets"]) > 1)
    courses_with_multi_title = sum(1 for c in sorted_courses.values() if len(c["guide_titles_seen"]) > 1)

    # SP CUS conflicts: course has sp mentions and more than one distinct CUS value
    sp_cus_conflict_count = sum(
        1 for c in sorted_courses.values()
        if c["sp_mention_count"] > 0 and len(c["sp_cus_values_seen"]) > 1
    )

    # Distributions
    def count_dist(values):
        dist = defaultdict(int)
        for v in values:
            dist[v] += 1
        return dict(sorted(dist.items()))

    desc_dist = count_dist(len(c["descriptions"]) for c in sorted_courses.values())
    comp_dist = count_dist(len(c["competency_sets"]) for c in sorted_courses.values())
    title_dist = count_dist(len(c["guide_titles_seen"]) for c in sorted_courses.values())

    anchor_dist = defaultdict(int)
    for c in sorted_courses.values():
        for ac in c["anchor_classes_seen"]:
            anchor_dist[ac] += 1

    # Examples for multi-variants (up to 5 each)
    multi_desc_examples = [
        {"course_code": c["course_code"], "variant_count": len(c["descriptions"])}
        for c in sorted_courses.values() if len(c["descriptions"]) > 1
    ][:5]

    multi_comp_examples = [
        {"course_code": c["course_code"], "variant_count": len(c["competency_sets"])}
        for c in sorted_courses.values() if len(c["competency_sets"]) > 1
    ][:5]

    multi_title_examples = [
        {
            "course_code": c["course_code"],
            "variant_count": len(c["guide_titles_seen"]),
            "titles": [t["raw_title"] for t in c["guide_titles_seen"]],
        }
        for c in sorted_courses.values() if len(c["guide_titles_seen"]) > 1
    ][:5]

    summary_out = {
        "generated_on": str(date.today()),
        "extraction_scope": "strict_unique_only",
        "total_courses": len(sorted_courses),
        "courses_with_descriptions": courses_with_descriptions,
        "courses_with_competencies": courses_with_competencies,
        "courses_with_sp_context": courses_with_sp,
        "courses_with_aos_context": courses_with_aos,
        "courses_with_multiple_description_variants": courses_with_multi_desc,
        "courses_with_multiple_competency_variants": courses_with_multi_comp,
        "courses_with_multiple_guide_titles": courses_with_multi_title,
        "description_variant_distribution": {str(k): v for k, v in desc_dist.items()},
        "competency_variant_distribution": {str(k): v for k, v in comp_dist.items()},
        "guide_title_variant_distribution": {str(k): v for k, v in title_dist.items()},
        "sp_cus_conflict_count": sp_cus_conflict_count,
        "anchor_class_distribution": dict(anchor_dist),
        "rows_skipped_ambiguous": total_skipped_ambiguous,
        "rows_skipped_unmapped": total_skipped_unmapped,
        "multi_description_examples": multi_desc_examples,
        "multi_competency_examples": multi_comp_examples,
        "multi_title_examples": multi_title_examples,
    }

    with open(SUMMARY_OUT, "w", encoding="utf-8") as f:
        json.dump(summary_out, f, indent=2, ensure_ascii=False)

    # ---- Stdout report ----
    print()
    print("=" * 60)
    print("COURSE ENRICHMENT CANDIDATES — BUILD COMPLETE")
    print("=" * 60)
    print(f"  Guides processed:              {len(guide_index)}")
    print(f"  Total courses with enrichment: {len(sorted_courses)}")
    print()
    print(f"  AoS mentions included:         {total_aos_included}")
    print(f"  SP mentions included:          {total_sp_included}")
    print(f"  Rows skipped (ambiguous):      {total_skipped_ambiguous}")
    print(f"  Rows skipped (unmapped):       {total_skipped_unmapped}")
    print()
    print(f"  Courses with descriptions:     {courses_with_descriptions} / {len(sorted_courses)}")
    print(f"  Courses with competencies:     {courses_with_competencies} / {len(sorted_courses)}")
    print(f"  Courses with SP context:       {courses_with_sp} / {len(sorted_courses)}")
    print(f"  Courses with AoS context:      {courses_with_aos} / {len(sorted_courses)}")
    print()
    print(f"  Multi-description variants:    {courses_with_multi_desc} courses")
    print(f"  Multi-competency variants:     {courses_with_multi_comp} courses")
    print(f"  Multi-title variants:          {courses_with_multi_title} courses")
    print(f"  SP CUS conflicts:              {sp_cus_conflict_count} courses")
    print()
    if aos_join_misses:
        print(f"  AoS join misses ({len(aos_join_misses)}):")
        for prog, title, cc in aos_join_misses[:20]:
            print(f"    [{prog}] '{title}' -> {cc}")
        if len(aos_join_misses) > 20:
            print(f"    ... and {len(aos_join_misses) - 20} more")
    else:
        print("  AoS join misses: 0")
    print()
    print(f"  Output: {CANDIDATES_OUT}")
    print(f"  Output: {SUMMARY_OUT}")
    print("=" * 60)


if __name__ == "__main__":
    main()
