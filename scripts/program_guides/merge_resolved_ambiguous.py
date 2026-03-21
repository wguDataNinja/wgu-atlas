"""
merge_resolved_ambiguous.py

Merges all resolved ambiguous rows back into the bridge guide files.

This script applies two layers of resolution:
  1. Deterministic resolutions (from resolve_ambiguous_deterministic.py, stored in
     resolution_log_deterministic.json — already applied to guides_resolved/).
  2. LLM adjudication results (from write_adjudication_results.py, stored in
     llm_packets/adjudication_results.json).

Inputs:
  data/program_guides/bridge/guides_resolved/{program_code}.json
    (output of resolve_ambiguous_deterministic.py — deterministic tier already applied;
     residual rows carry anchor_class="ambiguous_residual")
  data/program_guides/bridge/llm_packets/adjudication_results.json
    (171 packets: 163 high, 2 medium, 6 unresolvable)
  data/program_guides/bridge/index.json

Outputs:
  data/program_guides/bridge/guides_merged/{program_code}.json
    (fully merged per-guide files; no ambiguous_residual rows remain)
  data/program_guides/bridge/merge_summary.json
    (counts, coverage, explicit lists of medium and unresolvable cases)

Anchor class vocabulary after merge:
  exact_current_unique           — original unique match (unchanged)
  exact_observed_variant_unique  — original variant-unique match (unchanged)
  deterministic_resolved_multi   — resolved by deterministic multi-signal resolver
  deterministic_resolved_cu_match — resolved by CU-match signal alone
  llm_resolved_high              — LLM adjudication, high confidence, auto-accepted
  llm_resolved_medium_reviewed   — LLM adjudication, medium confidence, human-reviewed
  unresolvable                   — both candidates inactive / no decisive signal; excluded
  unmapped                       — no canonical match found (unchanged)

Policy:
  - 163 high-confidence LLM results: applied as llm_resolved_high
  - 2 medium-confidence results: applied as llm_resolved_medium_reviewed
      (included in unique set; explicitly tracked for auditability)
  - 6 unresolvable results: anchor_class set to "unresolvable";
      canonical_candidate_codes preserved for future reference;
      excluded from enrichment extraction
"""

import json
import os
from collections import Counter, defaultdict
from datetime import date

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RESOLVED_GUIDE_DIR = os.path.join(
    REPO_ROOT, "data", "program_guides", "bridge", "guides_resolved"
)
MERGED_GUIDE_DIR = os.path.join(
    REPO_ROOT, "data", "program_guides", "bridge", "guides_merged"
)
ADJUDICATION_RESULTS = os.path.join(
    REPO_ROOT, "data", "program_guides", "bridge", "llm_packets", "adjudication_results.json"
)
BRIDGE_INDEX = os.path.join(
    REPO_ROOT, "data", "program_guides", "bridge", "index.json"
)
MERGE_SUMMARY_OUT = os.path.join(
    REPO_ROOT, "data", "program_guides", "bridge", "merge_summary.json"
)


# ---------------------------------------------------------------------------
# Packet-id reconstruction
# ---------------------------------------------------------------------------
def make_packet_id(program_code: str, guide_title_normalized: str, surface: str) -> str:
    slug = guide_title_normalized.replace(" ", "_")
    return f"{program_code}__{slug}__{surface}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    os.makedirs(MERGED_GUIDE_DIR, exist_ok=True)

    # ---- Load LLM adjudication results ----
    with open(ADJUDICATION_RESULTS, encoding="utf-8") as f:
        adj_data = json.load(f)

    # Build lookup: packet_id -> adjudication entry
    adj_by_id = {}
    for entry in adj_data["adjudications"]:
        adj_by_id[entry["packet_id"]] = entry

    print(f"Loaded {len(adj_by_id)} LLM adjudication results.")

    # ---- Load bridge index ----
    with open(BRIDGE_INDEX, encoding="utf-8") as f:
        bridge_index = json.load(f)
    guide_index = bridge_index["guide_index"]

    # ---- Counters ----
    total_guides = 0
    total_rows = 0
    total_applied_high = 0
    total_applied_medium = 0
    total_marked_unresolvable = 0
    total_deterministic = 0
    total_exact_unique = 0
    total_unmapped = 0
    unresolvable_cases = []   # explicit list for audit
    medium_cases = []         # explicit list for audit
    anchor_class_totals = Counter()

    # ---- Process each guide ----
    program_codes_seen = set()
    for fn in sorted(os.listdir(RESOLVED_GUIDE_DIR)):
        if not fn.endswith(".json"):
            continue

        in_path = os.path.join(RESOLVED_GUIDE_DIR, fn)
        with open(in_path, encoding="utf-8") as f:
            guide = json.load(f)

        program_code = guide["program_code"]
        program_codes_seen.add(program_code)
        total_guides += 1

        new_rows = []
        for row in guide.get("roster_rows", []):
            total_rows += 1
            ac = row["anchor_class"]

            if ac == "ambiguous_residual":
                # Look up in adjudication results
                packet_id = make_packet_id(
                    program_code,
                    row.get("guide_title_normalized", ""),
                    row.get("surface", ""),
                )
                adj = adj_by_id.get(packet_id)
                if adj is None:
                    raise ValueError(
                        f"No adjudication result for packet_id={packet_id!r} "
                        f"in guide {program_code}"
                    )

                confidence = adj["confidence"]
                selected_code = adj.get("selected_code")

                if confidence == "unresolvable":
                    new_ac = "unresolvable"
                    # Keep original candidates; log the case
                    total_marked_unresolvable += 1
                    unresolvable_cases.append({
                        "packet_id": packet_id,
                        "program_code": program_code,
                        "surface": row.get("surface"),
                        "guide_title_raw": row.get("guide_title_raw"),
                        "original_candidates": row.get("canonical_candidate_codes", []),
                        "unresolvable_reason": adj.get("unresolvable_reason", ""),
                    })
                    row = dict(row)
                    row["anchor_class"] = new_ac
                    # candidates preserved as-is

                elif confidence == "medium":
                    new_ac = "llm_resolved_medium_reviewed"
                    total_applied_medium += 1
                    medium_cases.append({
                        "packet_id": packet_id,
                        "program_code": program_code,
                        "surface": row.get("surface"),
                        "guide_title_raw": row.get("guide_title_raw"),
                        "selected_code": selected_code,
                        "original_candidates": row.get("canonical_candidate_codes", []),
                        "rationale": adj.get("rationale", ""),
                    })
                    row = dict(row)
                    row["anchor_class"] = new_ac
                    row["canonical_candidate_codes"] = [selected_code]

                elif confidence == "high":
                    new_ac = "llm_resolved_high"
                    total_applied_high += 1
                    row = dict(row)
                    row["anchor_class"] = new_ac
                    row["canonical_candidate_codes"] = [selected_code]

                else:
                    raise ValueError(
                        f"Unexpected confidence={confidence!r} for {packet_id!r}"
                    )

            else:
                # Pass through unchanged; count for summary
                if ac in ("deterministic_resolved_multi", "deterministic_resolved_cu_match"):
                    total_deterministic += 1
                elif ac in ("exact_current_unique", "exact_observed_variant_unique"):
                    total_exact_unique += 1
                elif ac == "unmapped":
                    total_unmapped += 1

            anchor_class_totals[row["anchor_class"]] += 1
            new_rows.append(row)

        # ---- Rebuild roster_summary ----
        def _ac_counts(surface_filter):
            c = Counter()
            for r in new_rows:
                if r["surface"] == surface_filter:
                    c[r["anchor_class"]] += 1
            return dict(c)

        guide["roster_rows"] = new_rows
        guide["roster_summary"] = {
            "aos_course_count": sum(1 for r in new_rows if r["surface"] == "aos"),
            "sp_row_count": sum(1 for r in new_rows if r["surface"] == "sp"),
            "anchor_class_counts_aos": _ac_counts("aos"),
            "anchor_class_counts_sp": _ac_counts("sp"),
        }

        out_path = os.path.join(MERGED_GUIDE_DIR, fn)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(guide, f, indent=2, ensure_ascii=False)

    print(f"Processed {total_guides} guides.")
    print(f"  LLM high applied:     {total_applied_high}")
    print(f"  LLM medium applied:   {total_applied_medium}")
    print(f"  Marked unresolvable:  {total_marked_unresolvable}")
    print(f"  Deterministic (pass): {total_deterministic}")
    print(f"  Exact unique (pass):  {total_exact_unique}")
    print(f"  Unmapped (pass):      {total_unmapped}")
    print()
    print("Final anchor_class distribution across all guides:")
    for ac, n in sorted(anchor_class_totals.items()):
        print(f"  {ac}: {n}")

    # ---- Build merge summary ----
    summary = {
        "generated_on": str(date.today()),
        "source_resolved_guide_dir": "data/program_guides/bridge/guides_resolved",
        "output_merged_guide_dir": "data/program_guides/bridge/guides_merged",
        "adjudication_source": "data/program_guides/bridge/llm_packets/adjudication_results.json",
        "total_guides_processed": total_guides,
        "total_rows_processed": total_rows,
        "anchor_class_distribution": dict(sorted(anchor_class_totals.items())),
        "llm_applied": {
            "high_confidence_auto_accepted": total_applied_high,
            "medium_confidence_human_reviewed": total_applied_medium,
            "unresolvable_excluded": total_marked_unresolvable,
        },
        "policy": {
            "llm_resolved_high": "auto-accepted; included in unique enrichment extraction",
            "llm_resolved_medium_reviewed": (
                "medium-confidence LLM result; included with distinct status for auditability"
            ),
            "unresolvable": (
                "both candidates inactive / no decisive signal; "
                "excluded from enrichment extraction; original candidates preserved"
            ),
        },
        "medium_confidence_cases": medium_cases,
        "unresolvable_cases": unresolvable_cases,
    }

    with open(MERGE_SUMMARY_OUT, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\nMerge summary written to {MERGE_SUMMARY_OUT}")


if __name__ == "__main__":
    main()
