#!/usr/bin/env python3
"""
bootstrap_source_enrichment_manifest.py

One-time migration script. Creates data/source_enrichment_manifest.json from:
  - data/official_context_manifest_phase2_test.json   (122 reviewed rows)
  - _internal/workqueue_inputs/official_context_phase2_remaining_batch.json  (262 unreviewed rows)

Run from the repo root:
    python3 scripts/bootstrap_source_enrichment_manifest.py

NOTE: Bootstrap dates are approximate (based on session history), not precise scrape timestamps.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

PHASE2_TEST = REPO_ROOT / "data" / "enrichment" / "official_context_manifest_phase2_test.json"
REMAINING_BATCH = REPO_ROOT / "_internal" / "workqueue_inputs" / "official_context_phase2_remaining_batch.json"
PLACEMENTS = REPO_ROOT / "public" / "data" / "official_resource_placements.json"
OUTPUT = REPO_ROOT / "data" / "enrichment" / "source_enrichment_manifest.json"

# Approximate dates based on session history. Not precise.
DATE_PHASE2_REVIEWED = "2026-03-15"
DATE_PHASE2_FIRST_SEEN = "2026-03-14"
DATE_REMAINING_SEEN = "2026-03-15"


# ── Mappings ──────────────────────────────────────────────────────────────────

PAGE_TYPE_TO_CANDIDATE_TYPE = {
    "program_guide_page": "program_guide",
    "outcomes_page": "outcomes",
    "accreditation_page": "accreditation",
    "program_subpage": "specialization",
    "program_variant_page": "specialization",
    "school_page": "program_landing",
    "other": "other",
}

CAT_TO_SUBTYPE = {
    "accreditation": "accreditation_page",
    "specialization": "specialization_page",
    "school_page": "school_page",
}

CAT_TO_CANDIDATE_TYPE = {
    "accreditation": "accreditation",
    "specialization": "specialization",
    "school_page": "program_landing",
}

CANDIDATE_TYPE_TO_DECISION_REASON = {
    "program_guide": "core_program_context",
    "outcomes": "official_outcomes_context",
    "accreditation": "accreditation_context",
    "specialization": "variant_explainer",
    "program_landing": "core_program_context",
    "other": "",
}


def to_str_array(val):
    """Normalize a string or list to a list of non-empty strings."""
    if not val:
        return []
    if isinstance(val, list):
        return [v.strip() for v in val if v and v.strip()]
    # String: may be comma-separated
    return [v.strip() for v in str(val).split(",") if v.strip()]


def school_candidates_from_url(url: str) -> list[str]:
    """Infer school slug from URL path prefix."""
    mapping = {
        "online-it-degrees": "technology",
        "online-business-degrees": "business",
        "online-nursing-health-degrees": "health",
        "online-teaching-degrees": "education",
    }
    for segment, slug in mapping.items():
        if segment in url:
            return [slug]
    return []


def load_placements_index(path: Path) -> dict:
    """Build a lookup: url -> list of (surface, key) tuples."""
    data = json.loads(path.read_text())
    index = {}
    for row in data:
        url = row.get("resource_url", "")
        surface = row.get("show_on_surface", "")
        key = row.get("surface_key", "")
        if url not in index:
            index[url] = []
        index[url].append((surface, key))
    return index


def build_phase2_rows(phase2_data: list, placements_index: dict) -> list:
    rows = []
    unmatched_urls = []

    for item in phase2_data:
        url = item.get("url", "").strip()
        if not url:
            continue

        page_type = item.get("page_type", "other") or "other"
        candidate_type = PAGE_TYPE_TO_CANDIDATE_TYPE.get(page_type, "other")
        official_context_type = item.get("official_context_type", "") or ""

        # school/program candidates
        school_str = item.get("school_candidates", "") or ""
        school_cands = to_str_array(school_str.lower().strip()) if school_str else school_candidates_from_url(url)
        program_cands = to_str_array(item.get("program_candidates", ""))

        # target scope
        target_scope = "school" if (school_cands and not program_cands) else "program"

        # decision reason
        decision_reason = CANDIDATE_TYPE_TO_DECISION_REASON.get(candidate_type, "")

        # placement targets from live placements file
        program_targets = []
        school_targets = []
        matched = placements_index.get(url, [])
        if not matched:
            unmatched_urls.append(url)
        for surface, key in matched:
            if surface == "program_detail":
                program_targets.append(key)
            elif surface == "school_detail":
                school_targets.append(key)

        row = {
            "source_key": url,
            "source_family": "sitemap",
            "source_subtype": page_type,
            "url": url,
            "title": item.get("title", ""),
            "candidate_type": candidate_type,
            "target_scope": target_scope,

            "review_status": "keep",
            "decision_reason": decision_reason,
            "notes": item.get("notes", "") or "",

            "program_candidates": program_cands,
            "school_candidates": school_cands,
            "course_candidates": [],

            "program_targets": sorted(set(program_targets)),
            "school_targets": sorted(set(school_targets)),
            "course_targets": [],

            "is_currently_present": True,
            "first_seen_at": DATE_PHASE2_FIRST_SEEN,
            "last_seen_at": DATE_PHASE2_FIRST_SEEN,
            "last_reviewed_at": DATE_PHASE2_REVIEWED,
        }
        rows.append(row)

    return rows, unmatched_urls


def build_remaining_rows(remaining_data: list) -> list:
    rows = []
    for item in remaining_data:
        url = item.get("url", "").strip()
        if not url:
            continue

        cat = item.get("cat", "other") or "other"
        source_subtype = CAT_TO_SUBTYPE.get(cat, cat)
        candidate_type = CAT_TO_CANDIDATE_TYPE.get(cat, "other")
        school_cands = school_candidates_from_url(url)

        row = {
            "source_key": url,
            "source_family": "sitemap",
            "source_subtype": source_subtype,
            "url": url,
            "title": item.get("title", ""),
            "candidate_type": candidate_type,
            "target_scope": "",

            "review_status": "unreviewed",
            "decision_reason": "",
            "notes": "",

            "program_candidates": [],
            "school_candidates": school_cands,
            "course_candidates": [],

            "program_targets": [],
            "school_targets": [],
            "course_targets": [],

            "is_currently_present": True,
            "first_seen_at": DATE_REMAINING_SEEN,
            "last_seen_at": DATE_REMAINING_SEEN,
            "last_reviewed_at": "",
        }
        rows.append(row)

    return rows


def validate_and_report(all_rows: list, phase2_count: int, remaining_count: int, unmatched_urls: list):
    keep_rows = [r for r in all_rows if r["review_status"] == "keep"]
    unreviewed_rows = [r for r in all_rows if r["review_status"] == "unreviewed"]
    with_program_targets = [r for r in all_rows if r["program_targets"]]
    with_school_targets = [r for r in all_rows if r["school_targets"]]

    # Check for duplicates
    keys = [r["source_key"] for r in all_rows]
    dupes = [k for k in keys if keys.count(k) > 1]

    print("=" * 60)
    print("Bootstrap validation summary")
    print("=" * 60)
    print(f"  Total rows written:              {len(all_rows)}")
    print(f"  From phase2_test.json:           {phase2_count}")
    print(f"  From remaining_batch.json:       {remaining_count}")
    print(f"  review_status=keep:              {len(keep_rows)}")
    print(f"  review_status=unreviewed:        {len(unreviewed_rows)}")
    print(f"  Rows with program_targets:       {len(with_program_targets)}")
    print(f"  Rows with school_targets:        {len(with_school_targets)}")
    print(f"  phase2 URLs without placements:  {len(unmatched_urls)}")
    print(f"  Duplicate source_key values:     {len(set(dupes))}")
    print()

    if unmatched_urls:
        print("phase2 rows with no matching placement (expected for some):")
        for u in unmatched_urls[:10]:
            print(f"  - {u}")
        if len(unmatched_urls) > 10:
            print(f"  ... and {len(unmatched_urls) - 10} more")
        print()

    if dupes:
        print("WARNING: Duplicate source_key values found:")
        for k in sorted(set(dupes)):
            print(f"  - {k}")
        print()

    print("=" * 60)


def main():
    print(f"Reading {PHASE2_TEST.name}...")
    phase2_data = json.loads(PHASE2_TEST.read_text())

    print(f"Reading {REMAINING_BATCH.name}...")
    remaining_data = json.loads(REMAINING_BATCH.read_text())

    print(f"Reading {PLACEMENTS.name}...")
    placements_index = load_placements_index(PLACEMENTS)

    print("Building rows from phase2_test.json...")
    phase2_rows, unmatched_urls = build_phase2_rows(phase2_data, placements_index)

    print("Building rows from remaining_batch.json...")
    remaining_rows = build_remaining_rows(remaining_data)

    all_rows = phase2_rows + remaining_rows

    print(f"Writing {OUTPUT.name}...")
    OUTPUT.write_text(json.dumps(all_rows, indent=2, ensure_ascii=False) + "\n")

    validate_and_report(all_rows, len(phase2_rows), len(remaining_rows), unmatched_urls)
    print(f"Written: {OUTPUT}")


if __name__ == "__main__":
    main()
