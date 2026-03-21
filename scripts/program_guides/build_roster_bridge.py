#!/usr/bin/env python3
"""
build_roster_bridge.py

Builds the program guide roster bridge: a per-guide artifact that links
every AoS and SP course mention to canonical_courses.csv codes, classifies
each row by anchorability, and captures program-history alignment metadata.

Outputs:
  data/program_guides/bridge/program_guide_roster_bridge.json  (full combined)
  data/program_guides/bridge/index.json                        (summary index)
  data/program_guides/bridge/guides/{program_code}.json        (per-guide split)

Usage:
  python scripts/program_guides/build_roster_bridge.py
"""

import csv
import json
import os
import re
import unicodedata
from collections import defaultdict
from datetime import date

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
REPO_ROOT = os.path.normpath(REPO_ROOT)

CANONICAL_COURSES_CSV = os.path.join(REPO_ROOT, "data", "canonical_courses.csv")
PROGRAM_HISTORY_CSV   = os.path.join(REPO_ROOT, "data", "program_history.csv")
PARSED_DIR            = os.path.join(REPO_ROOT, "data", "program_guides", "parsed")
CORPUS_MANIFEST_JSON  = os.path.join(REPO_ROOT, "data", "program_guides", "audit", "PROGRAM_GUIDE_CORPUS_MANIFEST.json")
BRIDGE_DIR            = os.path.join(REPO_ROOT, "data", "program_guides", "bridge")
BRIDGE_GUIDES_DIR     = os.path.join(BRIDGE_DIR, "guides")

# ---------------------------------------------------------------------------
# Alias crosswalk: guide program_code → effective program_code
# (for guides whose PDF code doesn't match program_history.csv directly)
# ---------------------------------------------------------------------------
ALIAS_CROSSWALK = {
    "BSSWE_Java":  "BSSWE",
    "MSRNNUED":    "MSRNNUEDGR",
    "MSRNNULM":    "MSRNNULMGR",
    "MSRNNUNI":    "MSRNNUNIGR",
    "BSPRN":       None,   # no direct program_history match; flag as missing
}

# ---------------------------------------------------------------------------
# Title normalization
# ---------------------------------------------------------------------------
_PUNC_RE = re.compile(r"[^\w\s]")

def normalize_title(title: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace, strip accents."""
    t = unicodedata.normalize("NFKD", title)
    t = t.encode("ascii", "ignore").decode("ascii")
    t = t.lower()
    t = _PUNC_RE.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


# ---------------------------------------------------------------------------
# Load canonical_courses.csv → build title lookup tables
# ---------------------------------------------------------------------------
def load_canonical_courses(path: str):
    """
    Returns:
      current_title_to_codes: dict[str, list[str]]
          exact canonical_title_current → list of course_codes
      variant_title_to_codes: dict[str, list[str]]
          any observed_title variant (pipe-split) → list of course_codes
      normalized_to_codes: dict[str, list[str]]
          normalized form of any title → list of course_codes
      code_to_row: dict[str, dict]
          course_code → full CSV row
    """
    current_title_to_codes  = defaultdict(list)
    variant_title_to_codes  = defaultdict(list)
    normalized_to_codes     = defaultdict(list)
    code_to_row             = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code    = row["course_code"].strip()
            current = row["canonical_title_current"].strip()
            observed_raw = row.get("observed_titles", "").strip()

            code_to_row[code] = row

            # current title
            if current:
                current_title_to_codes[current].append(code)
                norm = normalize_title(current)
                if norm:
                    normalized_to_codes[norm].append(code)

            # observed variant titles (pipe-separated)
            if observed_raw:
                for variant in observed_raw.split("|"):
                    variant = variant.strip()
                    if variant and variant != current:
                        variant_title_to_codes[variant].append(code)
                        norm = normalize_title(variant)
                        if norm:
                            normalized_to_codes[norm].append(code)

    return (
        dict(current_title_to_codes),
        dict(variant_title_to_codes),
        dict(normalized_to_codes),
        code_to_row,
    )


# ---------------------------------------------------------------------------
# Classify anchor class for a single title
# ---------------------------------------------------------------------------
def classify_anchor(
    title_raw: str,
    current_title_to_codes: dict,
    variant_title_to_codes: dict,
    normalized_to_codes: dict,
) -> tuple[str, list[str]]:
    """
    Returns (anchor_class, candidate_codes_sorted).

    Anchor classes (in priority order):
      exact_current_unique          — exact match on canonical_title_current, 1 code
      exact_observed_variant_unique — exact match on an observed variant, 1 code
      normalization_unique          — normalized match, 1 code
      ambiguous_current_exact       — exact match on canonical_title_current, 2+ codes
      ambiguous_observed_exact      — exact match on observed variant, 2+ codes
      ambiguous_normalized          — normalized match, 2+ codes
      unmapped                      — no match at all
    """
    title_raw = title_raw.strip()
    title_norm = normalize_title(title_raw)

    # 1. Exact match on current title
    if title_raw in current_title_to_codes:
        codes = sorted(set(current_title_to_codes[title_raw]))
        if len(codes) == 1:
            return "exact_current_unique", codes
        return "ambiguous_current_exact", codes

    # 2. Exact match on observed variant
    if title_raw in variant_title_to_codes:
        codes = sorted(set(variant_title_to_codes[title_raw]))
        if len(codes) == 1:
            return "exact_observed_variant_unique", codes
        return "ambiguous_observed_exact", codes

    # 3. Normalized match (covers both current and variant normalizations)
    if title_norm and title_norm in normalized_to_codes:
        codes = sorted(set(normalized_to_codes[title_norm]))
        if len(codes) == 1:
            return "normalization_unique", codes
        return "ambiguous_normalized", codes

    return "unmapped", []


# ---------------------------------------------------------------------------
# Load program_history.csv → lookup by program_code
# ---------------------------------------------------------------------------
def load_program_history(path: str) -> dict[str, dict]:
    """Returns dict keyed by program_code with status, colleges, degree_headings, versions_seen."""
    lookup = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row["program_code"].strip()
            colleges = [c.strip() for c in row.get("colleges", "").split("|") if c.strip()]
            headings_raw = row.get("degree_headings", "").strip()
            headings = [h.strip() for h in headings_raw.split("|") if h.strip()]
            versions_raw = row.get("versions_seen", "").strip()
            versions = [v.strip() for v in versions_raw.split("|") if v.strip()]
            lookup[code] = {
                "status":          row.get("status", "").strip(),
                "first_seen":      row.get("first_seen", "").strip(),
                "last_seen":       row.get("last_seen", "").strip(),
                "colleges":        colleges,
                "degree_headings": headings,
                "versions_seen":   versions,
            }
    return lookup


# ---------------------------------------------------------------------------
# Compute alignment flags for a guide
# ---------------------------------------------------------------------------
def compute_alignment(
    guide_code: str,
    effective_code: str | None,
    degree_title_guide: str,
    guide_version: str | None,
    ph_lookup: dict,
) -> dict:
    """
    Returns alignment dict with program_history_exists, degree_heading_match_class,
    version_alignment_class.
    """
    lookup_code = effective_code or guide_code

    if lookup_code is None or lookup_code not in ph_lookup:
        return {
            "program_history_exists":    False,
            "degree_heading_match_class": "missing_program_history",
            "version_alignment_class":    "missing_program_history",
        }

    ph = ph_lookup[lookup_code]
    headings  = ph["degree_headings"]
    versions  = ph["versions_seen"]

    # Degree heading match
    title_norm = normalize_title(degree_title_guide) if degree_title_guide else ""
    heading_class = "no_heading_match"
    for h in headings:
        if h and degree_title_guide and degree_title_guide.strip() == h.strip():
            heading_class = "exact_heading_match"
            break
        h_norm = normalize_title(h)
        if h_norm and title_norm and (h_norm in title_norm or title_norm in h_norm):
            heading_class = "partial_heading_match"

    # Version alignment
    if not guide_version:
        version_class = "guide_version_missing"
    elif guide_version in versions:
        version_class = "version_present_in_program_history"
    else:
        version_class = "version_not_in_program_history"

    return {
        "program_history_exists":    True,
        "degree_heading_match_class": heading_class,
        "version_alignment_class":    version_class,
    }


# ---------------------------------------------------------------------------
# Build a single GuideRosterRecord
# ---------------------------------------------------------------------------
def build_guide_record(
    manifest_entry: dict,
    ph_lookup: dict,
    current_title_to_codes: dict,
    variant_title_to_codes: dict,
    normalized_to_codes: dict,
) -> dict:
    program_code = manifest_entry["program_code"]
    effective_code = ALIAS_CROSSWALK.get(program_code, program_code)

    # Load parsed artifact
    parsed_path = os.path.join(PARSED_DIR, f"{program_code}_parsed.json")
    if not os.path.exists(parsed_path):
        print(f"  [WARN] parsed artifact missing: {parsed_path}")
        return None

    with open(parsed_path, encoding="utf-8") as f:
        parsed = json.load(f)

    degree_title_guide = parsed.get("degree_title", "")
    guide_version      = parsed.get("version") or None
    guide_pub_date     = parsed.get("pub_date") or None

    # Program history metadata
    lookup_code = effective_code if effective_code else None
    ph_entry = ph_lookup.get(lookup_code, {}) if lookup_code else {}
    ph_status   = ph_entry.get("status") or None
    ph_colleges = ph_entry.get("colleges", [])
    ph_headings = ph_entry.get("degree_headings", [])

    # Alignment flags
    alignment = compute_alignment(
        program_code, effective_code, degree_title_guide, guide_version, ph_lookup
    )

    # Build roster rows
    roster_rows = []

    # --- AoS rows ---
    sp_status_from_manifest = manifest_entry.get("standard_path_status", "unusable")
    for group_entry in parsed.get("areas_of_study", []):
        group_name = group_entry.get("group", "")
        for course in group_entry.get("courses", []):
            title_raw = course.get("title", "").strip()
            if not title_raw:
                continue
            anchor_class, candidates = classify_anchor(
                title_raw, current_title_to_codes, variant_title_to_codes, normalized_to_codes
            )
            roster_rows.append({
                "surface":                  "aos",
                "guide_title_raw":          title_raw,
                "guide_title_normalized":   normalize_title(title_raw),
                "aos_group":                group_name or None,
                "sp_term":                  None,
                "sp_cus":                   None,
                "anchor_class":             anchor_class,
                "canonical_candidate_codes": candidates,
            })

    # --- SP rows (only if SP is usable/partial) ---
    if sp_status_from_manifest not in ("unusable",):
        for sp_row in parsed.get("standard_path", []):
            title_raw = sp_row.get("title", "").strip()
            if not title_raw:
                continue
            anchor_class, candidates = classify_anchor(
                title_raw, current_title_to_codes, variant_title_to_codes, normalized_to_codes
            )
            roster_rows.append({
                "surface":                  "sp",
                "guide_title_raw":          title_raw,
                "guide_title_normalized":   normalize_title(title_raw),
                "aos_group":                None,
                "sp_term":                  sp_row.get("term"),
                "sp_cus":                   sp_row.get("cus"),
                "anchor_class":             anchor_class,
                "canonical_candidate_codes": candidates,
            })

    # Roster summary
    aos_rows = [r for r in roster_rows if r["surface"] == "aos"]
    sp_rows  = [r for r in roster_rows if r["surface"] == "sp"]

    def count_classes(rows):
        counts = defaultdict(int)
        for r in rows:
            counts[r["anchor_class"]] += 1
        return dict(counts)

    record = {
        "program_code":             program_code,
        "program_code_effective":   effective_code,
        "family":                   manifest_entry.get("family", ""),
        "disposition":              manifest_entry.get("disposition", ""),
        "sp_status":                sp_status_from_manifest,
        "degree_title_guide":       degree_title_guide,
        "guide_version":            guide_version,
        "guide_pub_date":           guide_pub_date,
        "program_history_status":   ph_status,
        "program_history_colleges": ph_colleges,
        "program_history_degree_headings": ph_headings,
        "alignment":                alignment,
        "roster_summary": {
            "aos_course_count":        len(aos_rows),
            "sp_row_count":            len(sp_rows),
            "anchor_class_counts_aos": count_classes(aos_rows),
            "anchor_class_counts_sp":  count_classes(sp_rows),
        },
        "roster_rows": roster_rows,
    }
    return record


# ---------------------------------------------------------------------------
# Compute aggregate summary for index
# ---------------------------------------------------------------------------
def compute_index_summary(guides: list[dict]) -> dict:
    total_aos = sum(g["roster_summary"]["aos_course_count"] for g in guides)
    total_sp  = sum(g["roster_summary"]["sp_row_count"] for g in guides)

    agg_aos = defaultdict(int)
    agg_sp  = defaultdict(int)
    for g in guides:
        for cls, cnt in g["roster_summary"]["anchor_class_counts_aos"].items():
            agg_aos[cls] += cnt
        for cls, cnt in g["roster_summary"]["anchor_class_counts_sp"].items():
            agg_sp[cls] += cnt

    attachable_classes = {"exact_current_unique", "exact_observed_variant_unique", "normalization_unique"}

    def attachable_rate(agg, total):
        if total == 0:
            return 0.0
        n = sum(v for k, v in agg.items() if k in attachable_classes)
        return round(n / total, 4)

    return {
        "guide_count":             len(guides),
        "total_aos_rows":          total_aos,
        "total_sp_rows":           total_sp,
        "anchor_class_counts_aos": dict(agg_aos),
        "anchor_class_counts_sp":  dict(agg_sp),
        "aos_unique_attachable_rate": attachable_rate(agg_aos, total_aos),
        "sp_unique_attachable_rate":  attachable_rate(agg_sp, total_sp),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Loading canonical_courses.csv …")
    current_title_to_codes, variant_title_to_codes, normalized_to_codes, _ = \
        load_canonical_courses(CANONICAL_COURSES_CSV)
    print(f"  {len(current_title_to_codes)} unique current titles")
    print(f"  {len(variant_title_to_codes)} unique variant titles")
    print(f"  {len(normalized_to_codes)} normalized forms")

    print("Loading program_history.csv …")
    ph_lookup = load_program_history(PROGRAM_HISTORY_CSV)
    print(f"  {len(ph_lookup)} program records")

    print("Loading corpus manifest …")
    with open(CORPUS_MANIFEST_JSON, encoding="utf-8") as f:
        manifest = json.load(f)
    guide_manifest = manifest["guide_manifest"]
    print(f"  {len(guide_manifest)} guide manifest entries")

    # Build per-guide records
    os.makedirs(BRIDGE_GUIDES_DIR, exist_ok=True)

    all_guide_records = []
    errors = []

    for i, entry in enumerate(guide_manifest, 1):
        code = entry["program_code"]
        print(f"  [{i:3d}/{len(guide_manifest)}] {code} …", end=" ")
        try:
            record = build_guide_record(
                entry, ph_lookup,
                current_title_to_codes, variant_title_to_codes, normalized_to_codes,
            )
            if record is None:
                errors.append(code)
                print("SKIPPED (missing parsed artifact)")
                continue
            all_guide_records.append(record)

            # Write per-guide file
            guide_path = os.path.join(BRIDGE_GUIDES_DIR, f"{code}.json")
            with open(guide_path, "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2, ensure_ascii=False)
            print(f"OK  (aos={record['roster_summary']['aos_course_count']}, sp={record['roster_summary']['sp_row_count']})")
        except Exception as e:
            errors.append(code)
            print(f"ERROR: {e}")

    # Index
    print("\nWriting index …")
    summary = compute_index_summary(all_guide_records)
    index = {
        "generated_on":             str(date.today()),
        "sources": [
            "data/canonical_courses.csv",
            "data/program_history.csv",
            "data/program_guides/parsed/*_parsed.json",
            "data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.json",
        ],
        "program_code_alias_crosswalk": ALIAS_CROSSWALK,
        "summary":   summary,
        "errors":    errors,
        "guide_index": [
            {
                "program_code":           g["program_code"],
                "program_code_effective": g["program_code_effective"],
                "family":                 g["family"],
                "disposition":            g["disposition"],
                "sp_status":              g["sp_status"],
                "alignment_summary":      g["alignment"],
                "roster_summary":         g["roster_summary"],
            }
            for g in all_guide_records
        ],
    }
    index_path = os.path.join(BRIDGE_DIR, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    # Full combined file
    print("Writing full roster bridge …")
    full = {
        "generated_on":             str(date.today()),
        "sources": [
            "data/canonical_courses.csv",
            "data/program_history.csv",
            "data/program_guides/parsed/*_parsed.json",
            "data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.json",
        ],
        "program_code_alias_crosswalk": ALIAS_CROSSWALK,
        "summary":  summary,
        "errors":   errors,
        "guides":   all_guide_records,
    }
    bridge_path = os.path.join(BRIDGE_DIR, "program_guide_roster_bridge.json")
    with open(bridge_path, "w", encoding="utf-8") as f:
        json.dump(full, f, indent=2, ensure_ascii=False)

    # Report
    print("\n" + "="*60)
    print(f"Roster bridge complete.")
    print(f"  Guides processed:        {summary['guide_count']}")
    print(f"  Errors/skipped:          {len(errors)}")
    if errors:
        print(f"  Error codes:             {errors}")
    print(f"  Total AoS rows:          {summary['total_aos_rows']}")
    print(f"  Total SP rows:           {summary['total_sp_rows']}")
    print(f"  AoS unique-attach rate:  {summary['aos_unique_attachable_rate']:.1%}")
    print(f"  SP  unique-attach rate:  {summary['sp_unique_attachable_rate']:.1%}")
    print(f"\nOutputs:")
    print(f"  {bridge_path}")
    print(f"  {index_path}")
    print(f"  {BRIDGE_GUIDES_DIR}/<code>.json  ({summary['guide_count']} files)")

    if errors:
        print(f"\n[WARN] {len(errors)} guides had errors — check output above.")


if __name__ == "__main__":
    main()
