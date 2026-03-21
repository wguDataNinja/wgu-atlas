"""
build_ambiguous_resolution_packets.py

For each ambiguous_residual row in the resolved bridge guides, constructs a
self-contained LLM adjudication context packet.

Each packet includes:
  - program_context: program_code, degree_title, family, degree_level, guide_version
  - row_context: surface, guide_title_raw, aos_group, sp_term, sp_cus
  - parsed_description: from the parsed guide AoS section (if available)
  - aos_group_neighbors: other courses in same AoS group that have been resolved
  - candidates: full canonical metadata for each candidate code
  - previously_resolved_in_guide: sample of resolved rows from same guide
  - signals_checked_and_failed: all 5 deterministic signals that did not fire

Packets are grouped by family for batch LLM processing.

Inputs:
  data/program_guides/bridge/guides_resolved/{program_code}.json
  data/program_guides/parsed/{program_code}_parsed.json
  data/canonical_courses.csv
  data/program_guides/bridge/index.json

Output:
  data/program_guides/bridge/llm_packets/packets.json
  data/program_guides/bridge/llm_packets/packets_summary.json
"""

import csv
import json
import os
from collections import defaultdict
from datetime import date

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT          = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANONICAL_CSV      = os.path.join(REPO_ROOT, "data", "canonical_courses.csv")
BRIDGE_INDEX       = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "index.json")
RESOLVED_GUIDE_DIR = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "guides_resolved")
PARSED_GUIDE_DIR   = os.path.join(REPO_ROOT, "data", "program_guides", "parsed")
PACKETS_DIR        = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "llm_packets")
PACKETS_OUT        = os.path.join(PACKETS_DIR, "packets.json")
SUMMARY_OUT        = os.path.join(PACKETS_DIR, "packets_summary.json")

ALL_SIGNAL_IDS = ["cu_match", "one_active", "a_suffix_cert", "degree_level", "degree_title"]

# Family ordering for batched LLM processing
FAMILY_ORDER = [
    "education_ba", "teaching_mat", "education_grad", "education_ma",
    "education_bs", "endorsement",
    "cs_ug", "cs_grad", "swe_grad",
    "standard_bs", "mba", "accounting_ma",
    "healthcare_grad", "nursing_ug", "nursing_msn", "nursing_pmc", "nursing_rn_msn",
    "graduate_standard", "data_analytics_grad",
]


# ---------------------------------------------------------------------------
# Degree-level helper (mirrors resolver)
# ---------------------------------------------------------------------------
def degree_level_of_guide(degree_title: str) -> str:
    dt = degree_title.lower()
    if any(k in dt for k in ["bachelor", "b.a.", "b.s.", "bsn", "associate"]):
        return "undergraduate"
    if any(k in dt for k in ["master", "mba", "m.s.", "m.a.", "mat", "graduate"]):
        return "graduate"
    return "unknown"


# ---------------------------------------------------------------------------
# Build AoS title lookup from parsed guide
# ---------------------------------------------------------------------------
def build_aos_lookup(parsed_guide: dict) -> dict:
    """Return {title: {description, competency_bullets, aos_group}}."""
    lookup = {}
    for aos in parsed_guide.get("areas_of_study", []):
        group = aos.get("group", "")
        for course in aos.get("courses", []):
            title = course.get("title", "")
            if title:
                lookup[title] = {
                    "description":        course.get("description", ""),
                    "competency_bullets": course.get("competency_bullets", []),
                    "aos_group":          group,
                }
    return lookup


# ---------------------------------------------------------------------------
# Normalise candidate record for packet
# ---------------------------------------------------------------------------
def candidate_record(course_code: str, canonical: dict) -> dict:
    cc = canonical.get(course_code, {})
    return {
        "course_code":            course_code,
        "canonical_title_current": cc.get("canonical_title_current", ""),
        "canonical_cus":          cc.get("canonical_cus", ""),
        "current_college":        cc.get("current_college", ""),
        "active_current":         cc.get("active_current") == "True",
        "current_programs":       cc.get("current_programs", ""),
        "historical_programs":    cc.get("historical_programs", ""),
        "current_program_count":  int(cc.get("current_program_count") or 0),
        "stability_class":        cc.get("stability_class", ""),
        "title_variant_class":    cc.get("title_variant_class", ""),
        "first_seen_edition":     cc.get("first_seen_edition", ""),
        "last_seen_edition":      cc.get("last_seen_edition", ""),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    os.makedirs(PACKETS_DIR, exist_ok=True)

    # Load canonical courses
    canonical = {}
    with open(CANONICAL_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            canonical[row["course_code"]] = row
    print(f"Loaded {len(canonical)} canonical courses.")

    # Load bridge index for family ordering
    with open(BRIDGE_INDEX, encoding="utf-8") as f:
        bridge_index = json.load(f)
    family_of = {e["program_code"]: e.get("family", "") for e in bridge_index["guide_index"]}

    # Load all resolved guides
    all_guides = {}
    for fname in sorted(os.listdir(RESOLVED_GUIDE_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(RESOLVED_GUIDE_DIR, fname), encoding="utf-8") as f:
            g = json.load(f)
        all_guides[g["program_code"]] = g
    print(f"Loaded {len(all_guides)} resolved guides.")

    # ---------------------------------------------------------------------------
    # Build packets
    # ---------------------------------------------------------------------------
    packets = []
    missing_parsed = []
    missing_description = []
    aos_join_miss = []

    for program_code, guide in sorted(all_guides.items()):
        family       = guide.get("family", "")
        degree_title = guide.get("degree_title_guide", "")
        guide_level  = degree_level_of_guide(degree_title)
        guide_version = guide.get("guide_version", "")
        guide_pub_date = guide.get("guide_pub_date", "")

        # Load parsed guide
        parsed_path = os.path.join(PARSED_GUIDE_DIR, f"{program_code}_parsed.json")
        if not os.path.exists(parsed_path):
            missing_parsed.append(program_code)
            parsed_guide = {}
        else:
            with open(parsed_path, encoding="utf-8") as f:
                parsed_guide = json.load(f)

        aos_lookup = build_aos_lookup(parsed_guide)

        roster = guide.get("roster_rows", [])

        # Build per-AoS-group neighbor lists from resolved rows
        # {aos_group -> [resolved rows]}
        resolved_by_group = defaultdict(list)
        for row in roster:
            ac = row.get("anchor_class", "")
            if ac == "ambiguous_residual" or ac.startswith("ambiguous"):
                continue
            grp = row.get("aos_group")
            if grp and row.get("resolved_code") or row.get("canonical_candidate_codes"):
                code = (row.get("resolved_code")
                        or (row.get("canonical_candidate_codes") or [None])[0])
                if code:
                    resolved_by_group[grp].append({
                        "guide_title_raw": row.get("guide_title_raw", ""),
                        "resolved_code":   code,
                        "anchor_class":    ac,
                    })

        # Build full resolved sample for previously_resolved_in_guide
        all_resolved_rows = []
        for row in roster:
            ac = row.get("anchor_class", "")
            if ac == "ambiguous_residual" or ac.startswith("ambiguous"):
                continue
            code = (row.get("resolved_code")
                    or (row.get("canonical_candidate_codes") or [None])[0])
            if code:
                all_resolved_rows.append({
                    "guide_title_raw": row.get("guide_title_raw", ""),
                    "resolved_code":   code,
                    "anchor_class":    ac,
                })

        # Process residual rows
        for row in roster:
            if row.get("anchor_class") != "ambiguous_residual":
                continue

            surface         = row.get("surface", "")
            guide_title_raw = row.get("guide_title_raw", "")
            guide_title_norm = row.get("guide_title_normalized", "")
            aos_group       = row.get("aos_group")
            sp_term         = row.get("sp_term")
            sp_cus          = row.get("sp_cus")
            cands           = row.get("canonical_candidate_codes", [])

            # Packet ID
            safe_title = guide_title_norm.replace(" ", "_")[:60]
            packet_id  = f"{program_code}__{safe_title}__{surface}"

            # Parsed description (AoS rows only)
            parsed_description = None
            if surface == "aos":
                aos_data = aos_lookup.get(guide_title_raw)
                if aos_data is not None:
                    parsed_description = aos_data.get("description", "")
                else:
                    aos_join_miss.append((program_code, guide_title_raw))
                    missing_description.append(packet_id)

            # AoS group neighbors (up to 5 resolved rows from same group)
            aos_neighbors = []
            if aos_group:
                grp_rows = resolved_by_group.get(aos_group, [])
                # Exclude the packet's own title
                grp_rows = [r for r in grp_rows if r["guide_title_raw"] != guide_title_raw]
                aos_neighbors = grp_rows[:5]

            # Previously resolved in guide (up to 10, prefer same degree_level context)
            prev_resolved = [r for r in all_resolved_rows if r["guide_title_raw"] != guide_title_raw]
            prev_resolved = prev_resolved[:10]

            packet = {
                "packet_id": packet_id,
                "program_context": {
                    "program_code":          program_code,
                    "program_code_effective": guide.get("program_code_effective"),
                    "family":                family,
                    "degree_title":          degree_title,
                    "degree_level":          guide_level,
                    "guide_version":         guide_version,
                    "guide_pub_date":        guide_pub_date,
                },
                "row_context": {
                    "surface":               surface,
                    "guide_title_raw":       guide_title_raw,
                    "guide_title_normalized": guide_title_norm,
                    "aos_group":             aos_group,
                    "sp_term":               sp_term,
                    "sp_cus":                sp_cus,
                },
                "parsed_description": parsed_description,
                "aos_group_neighbors": aos_neighbors,
                "candidates": [candidate_record(c, canonical) for c in cands],
                "previously_resolved_in_guide": prev_resolved,
                "signals_checked_and_failed": ALL_SIGNAL_IDS,
            }
            packets.append(packet)

    # Sort packets by family order, then program_code
    def sort_key(p):
        fam = p["program_context"]["family"]
        try:
            fam_idx = FAMILY_ORDER.index(fam)
        except ValueError:
            fam_idx = 99
        return (fam_idx, p["program_context"]["program_code"], p["packet_id"])

    packets.sort(key=sort_key)

    # ---------------------------------------------------------------------------
    # Write packets
    # ---------------------------------------------------------------------------
    output = {
        "generated_on":    str(date.today()),
        "total_packets":   len(packets),
        "packet_purpose":  "llm_adjudication_residual",
        "signals_all_failed": ALL_SIGNAL_IDS,
        "packets": packets,
    }
    with open(PACKETS_OUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Summary
    by_family   = defaultdict(int)
    by_surface  = defaultdict(int)
    by_cand_ct  = defaultdict(int)
    by_level    = defaultdict(int)
    has_desc    = sum(1 for p in packets if p["parsed_description"])
    has_neighbors = sum(1 for p in packets if p["aos_group_neighbors"])

    for p in packets:
        by_family[p["program_context"]["family"]] += 1
        by_surface[p["row_context"]["surface"]] += 1
        by_cand_ct[len(p["candidates"])] += 1
        by_level[p["program_context"]["degree_level"]] += 1

    summary = {
        "generated_on":     str(date.today()),
        "total_packets":    len(packets),
        "by_family":        dict(sorted(by_family.items(), key=lambda x: -x[1])),
        "by_surface":       dict(by_surface),
        "by_degree_level":  dict(by_level),
        "by_candidate_count": {str(k): v for k, v in sorted(by_cand_ct.items())},
        "packets_with_parsed_description":  has_desc,
        "packets_with_aos_group_neighbors": has_neighbors,
        "packets_missing_parsed_description": len(missing_description),
        "aos_join_misses":  aos_join_miss,
        "missing_parsed_guides": missing_parsed,
    }
    with open(SUMMARY_OUT, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # ---------------------------------------------------------------------------
    # Stdout report
    # ---------------------------------------------------------------------------
    print()
    print("=" * 60)
    print("AMBIGUOUS RESOLUTION PACKET BUILDER — COMPLETE")
    print("=" * 60)
    print(f"  Total packets written:         {len(packets)}")
    print()
    print("  By family:")
    for fam, cnt in sorted(by_family.items(), key=lambda x: -x[1]):
        print(f"    {fam:<30} {cnt}")
    print()
    print(f"  By surface:   aos={by_surface.get('aos',0)}, sp={by_surface.get('sp',0)}")
    print(f"  By level:     ug={by_level.get('undergraduate',0)}, grad={by_level.get('graduate',0)}")
    print(f"  Cand size distribution: {dict(sorted(by_cand_ct.items()))}")
    print()
    print(f"  Packets with parsed description:   {has_desc} / {len(packets)}")
    print(f"  Packets with AoS group neighbors:  {has_neighbors} / {len(packets)}")
    if aos_join_miss:
        print(f"  AoS description join misses: {len(aos_join_miss)}")
        for pc, title in aos_join_miss[:5]:
            print(f"    [{pc}] {title}")
    print()
    print(f"  Output: {PACKETS_OUT}")
    print(f"  Output: {SUMMARY_OUT}")
    print("=" * 60)


if __name__ == "__main__":
    main()
