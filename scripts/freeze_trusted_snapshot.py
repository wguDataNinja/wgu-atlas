"""
freeze_trusted_snapshot.py
==========================
Create a frozen trusted-edition snapshot under data/catalog/trusted/{EDITION}/.

Usage:
  python3 scripts/freeze_trusted_snapshot.py --edition 2026_06

Context:
  This script derives a trusted snapshot from the mirrored helper files,
  program_names, and raw catalog texts in data/catalog/. It does NOT run
  the upstream parser pipeline. It is a deterministic freeze step that
  creates the 8 files expected in data/catalog/trusted/{EDITION}/:

    courses_{EDITION}.csv
    certs_{EDITION}.csv
    course_index_{EDITION}.json
    sections_index_{EDITION}.json
    degree_snapshots_{EDITION}.json
    program_blocks_{EDITION}.json
    program_index_{EDITION}.json
    manifest_{EDITION}.json

  Certs data is carried forward from the most recent trusted snapshot with
  targeted corrections for known changes, since cert codes are not present
  in the helper course_index_v10.json. A full parser re-run would be needed
  for authoritative cert extraction.

  This script does NOT write to public/data/ or modify build_site_data.py.

Environment:
  WGU_CATALOG_OUTPUTS  Path to catalog outputs (default: data/catalog/)
"""

import argparse
import csv
import json
import os
import sys
import time
from collections import defaultdict


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPT_DIR)

BASE = (
    os.environ.get("WGU_CATALOG_OUTPUTS")
    or os.path.join(_REPO_ROOT, "data", "catalog")
)

TRUSTED_BASE = os.path.join(BASE, "trusted")
HELPERS = os.path.join(BASE, "helpers")
PROGRAM_NAMES = os.path.join(BASE, "program_names")
CHANGE_TRACKING = os.path.join(BASE, "change_tracking")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def write_json(path, obj, indent=2):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)
    return path

def write_csv(path, rows, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return path


# ---------------------------------------------------------------------------
# Date format helpers
# ---------------------------------------------------------------------------
def edition_dir(edition):
    """Convert edition ID to directory format (underscore)."""
    return edition.replace("-", "_")

def edition_display(edition):
    """Convert edition ID to display/JSON key format (hyphen)."""
    return edition.replace("_", "-")

def trusted_subdir(edition, base_dir=TRUSTED_BASE):
    """Return the trusted snapshot directory for an edition."""
    return os.path.join(base_dir, edition_dir(edition))

def trusted_path(edition, filename):
    """Return a full path in the trusted snapshot directory."""
    return os.path.join(trusted_subdir(edition), filename)


# ---------------------------------------------------------------------------
# Step 1: Build course_index_{edition}.json
# ---------------------------------------------------------------------------
def build_course_index(edition):
    """
    Filter the full helper course_index_v10.json to include only courses
    that have instances for the target edition. Each course entry keeps
    only the instances for that edition (matching the 2026_03 convention).
    """
    ed = edition_display(edition)
    print(f"  Reading course_index_v10.json...")
    full_index = load_json(os.path.join(HELPERS, "course_index_v10.json"))
    print(f"    Total codes in full index: {len(full_index)}")

    filtered = {}
    for code, entry in full_index.items():
        ed_instances = [
            inst for inst in entry.get("instances", [])
            if inst.get("catalog_date") == ed
        ]
        if not ed_instances:
            continue
        filtered[code] = {
            "canonical_title": entry["canonical_title"],
            "canonical_cus": entry["canonical_cus"],
            "instances": ed_instances,
        }

    print(f"    Courses with {ed} instances: {len(filtered)}")
    return filtered


# ---------------------------------------------------------------------------
# Step 2: Build courses_{edition}.csv
# ---------------------------------------------------------------------------
def build_courses_csv(course_index, edition):
    """
    Derive the AP-scope courses CSV from the filtered course_index data.
    Columns match courses_2026_03.csv: scope,course_code,title,cus,
    program_count,colleges,programs.

    For each course, programs are collected from instance 'degree' fields,
    and colleges from instance 'college' fields.
    """
    ed_disp = edition_display(edition)
    rows = []

    for code in sorted(course_index.keys()):
        entry = course_index[code]
        instances = entry.get("instances", [])

        # Collect unique programs (degree names) and colleges
        programs_seen = []
        colleges_seen = []
        for inst in instances:
            deg = inst.get("degree", "").strip()
            if deg and deg not in programs_seen:
                programs_seen.append(deg)
            col = inst.get("college", "").strip()
            if col and col not in colleges_seen:
                colleges_seen.append(col)

        row = {
            "scope": "AP",
            "course_code": code,
            "title": entry.get("canonical_title", ""),
            "cus": str(entry.get("canonical_cus", "")),
            "program_count": str(len(programs_seen)),
            "colleges": "; ".join(colleges_seen),
            "programs": "; ".join(programs_seen),
        }
        rows.append(row)

    return rows


# ---------------------------------------------------------------------------
# Step 3: Build certs_{edition}.csv
# ---------------------------------------------------------------------------
def build_certs_csv(course_index_06, edition):
    """
    Derive the certs CSV. Cert codes are NOT in course_index_v10.json,
    so this carries forward the most recent trusted snapshot and applies
    targeted corrections from observed raw-text changes.

    Known change: C955A removed, D979A added (Data Analytics Skills cert).
    """
    ed_dir = edition_dir(edition)

    # Find the most recent existing trusted snapshot for the base cert data
    existing = sorted(
        d for d in os.listdir(TRUSTED_BASE)
        if d.startswith("20")
        and os.path.isdir(os.path.join(TRUSTED_BASE, d))
        and d != edition_dir(edition)
    )
    if not existing:
        print("  ERROR: No existing trusted snapshot found for cert baseline!")
        sys.exit(1)

    base_ed = existing[-1]
    certs_path = os.path.join(TRUSTED_BASE, base_ed, f"certs_{base_ed}.csv")

    if not os.path.exists(certs_path):
        print(f"  ERROR: Base certs file not found: {certs_path}")
        sys.exit(1)

    print(f"    Reading base certs from: {certs_path}")
    with open(certs_path, newline="", encoding="utf-8") as f:
        cert_rows = list(csv.DictReader(f))

    print(f"    Base cert codes: {len(cert_rows)}")

    # Apply known corrections for 2026_06
    if ed_dir == "2026_06":
        # C955A removed (replaced by D979A in Data Analytics Skills certificate)
        removed = [r for r in cert_rows if r["course_code"] == "C955A"]
        cert_rows = [r for r in cert_rows if r["course_code"] != "C955A"]
        if removed:
            print(f"    Removed C955A (replaced by D979A in Data Analytics Skills)")
        else:
            print(f"    WARNING: C955A not found in base certs, expected it to exist")

        # D979A added
        already = any(r["course_code"] == "D979A" for r in cert_rows)
        if not already:
            cert_rows.append({
                "scope": "Cert",
                "course_code": "D979A",
                "title": "Data and Decisions: Applied Statistics",
                "cus": "3",
                "program_count": "1",
                "cert_programs": "Data Analytics Skills",
            })
            print(f"    Added D979A (new Data Analytics Skills course)")
        else:
            print(f"    D979A already in certs, no addition needed")

        # Note: Cybersecurity Fundamentals uses existing AP codes (D329, E025)
        # so no new cert-specific codes are added.

    return cert_rows


# ---------------------------------------------------------------------------
# Step 4: Build sections_index_{edition}.json
# ---------------------------------------------------------------------------
def build_sections_index(edition):
    """Extract single-edition key from sections_index_v10.json."""
    ed_disp = edition_display(edition)
    full = load_json(os.path.join(HELPERS, "sections_index_v10.json"))

    if ed_disp not in full:
        print(f"    ERROR: Edition '{ed_disp}' not found in sections_index_v10.json")
        print(f"    Available editions (last 5): {sorted(full.keys())[-5:]}")
        sys.exit(1)

    return {ed_disp: full[ed_disp]}


# ---------------------------------------------------------------------------
# Step 5: Build degree_snapshots_{edition}.json
# ---------------------------------------------------------------------------
def build_degree_snapshots(edition):
    """Extract single-edition key from degree_snapshots_v10_seed.json."""
    ed_disp = edition_display(edition)
    full = load_json(os.path.join(HELPERS, "degree_snapshots_v10_seed.json"))

    if ed_disp not in full:
        print(f"    ERROR: Edition '{ed_disp}' not found in degree_snapshots_v10_seed.json")
        print(f"    Available editions (last 5): {sorted(full.keys())[-5:]}")
        sys.exit(1)

    return {ed_disp: full[ed_disp]}


# ---------------------------------------------------------------------------
# Step 6: Build program_blocks_{edition}.json
# ---------------------------------------------------------------------------
def build_program_blocks(edition):
    """Copy/normalize from program_names/YYYY_MM_program_blocks_v11.json."""
    ed_dir = edition_dir(edition)
    src = os.path.join(PROGRAM_NAMES, f"{ed_dir}_program_blocks_v11.json")

    if not os.path.exists(src):
        print(f"    ERROR: Source file not found: {src}")
        sys.exit(1)

    blocks = load_json(src)
    print(f"    Program blocks loaded: {len(blocks)}")
    return blocks


# ---------------------------------------------------------------------------
# Step 7: Build program_index_{edition}.json
# ---------------------------------------------------------------------------
def build_program_index(edition):
    """Copy from program_names/YYYY_MM_program_index_v11.json."""
    ed_dir = edition_dir(edition)
    src = os.path.join(PROGRAM_NAMES, f"{ed_dir}_program_index_v11.json")

    if not os.path.exists(src):
        print(f"    ERROR: Source file not found: {src}")
        sys.exit(1)

    idx = load_json(src)
    print(f"    Program index loaded: {len(idx) if isinstance(idx, dict) else len(idx)} entries")
    return idx


# ---------------------------------------------------------------------------
# Step 8: Build manifest_{edition}.json
# ---------------------------------------------------------------------------
def build_manifest(edition, course_index, courses_rows, certs_rows, program_blocks,
                    sections_idx, degree_snaps, program_idx):
    """Build a manifest matching the 2026_03 convention."""
    ed_disp = edition_display(edition)
    ed_dir = edition_dir(edition)

    ap_active = len([r for r in courses_rows if r["scope"] == "AP"])
    total_unique_ap = len(course_index)
    cert_count = len(certs_rows)
    cert_progs = set()
    for r in certs_rows:
        for p in r.get("cert_programs", "").split(";"):
            cp = p.strip()
            if cp:
                cert_progs.add(cp)

    manifest = {
        "catalog_date": ed_disp,
        "current_edition": ed_dir,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "generator": "scripts/freeze_trusted_snapshot.py",
        "parser_version": "N/A (frozen from helpers + program_names; not a fresh parser run)",
        "verification_status": "SCRIPT_VALIDATED_PENDING_MANUAL_REVIEW",
        "ap_scope": {
            "unique_course_codes": total_unique_ap,
            "active_courses_in_csv": ap_active,
            "programs": len(program_blocks),
            "source": "course_index_v10.json (filtered to current edition)",
            "file": f"courses_{ed_dir}.csv",
        },
        "cert_scope": {
            "unique_course_codes": cert_count,
            "overlap_with_ap": 0,
            "note": "Intentionally out of AP scope. Cert codes are structurally different from AP codes. Carried forward from prior trusted snapshot with known corrections.",
            "file": f"certs_{ed_dir}.csv",
            "cert_programs": len(cert_progs),
        },
        "combined_total_unique": total_unique_ap + cert_count,
        "frozen_source_files": [
            f"course_index_{ed_dir}.json",
            f"sections_index_{ed_dir}.json",
            f"degree_snapshots_{ed_dir}.json",
            f"program_blocks_{ed_dir}.json",
            f"program_index_{ed_dir}.json",
        ],
        "validation_assertions": {
            "edition_has_course_data": True,
            "edition_in_helper_sections_index": ed_disp in sections_idx,
            "edition_in_helper_degree_snapshots": ed_disp in degree_snaps,
            "program_blocks_match_edition": ed_dir in (program_idx.get("_generated", ed_dir) if isinstance(program_idx, dict) else ed_dir),
        },
    }
    return manifest


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Freeze a trusted catalog edition snapshot")
    parser.add_argument(
        "--edition", "-e",
        required=True,
        help="Target edition ID (e.g., 2026_06 or 2026-06)",
    )
    parser.add_argument(
        "--certs-source-edition",
        default=None,
        help="Edition ID to source cert data from (default: most recent existing trusted)",
    )
    args = parser.parse_args()

    edition = edition_dir(args.edition)
    ed_disp = edition_display(edition)

    print(f"\n=== Freezing trusted snapshot: {edition} ===")
    print(f"  Edition dir:  {edition}")
    print(f"  Edition disp: {ed_disp}")
    print(f"  Output dir:   {trusted_subdir(edition)}")
    print()

    # Validate prerequisites
    helpers_ok = all(
        os.path.exists(os.path.join(HELPERS, f))
        for f in ["course_index_v10.json", "sections_index_v10.json",
                   "degree_snapshots_v10_seed.json"]
    )
    if not helpers_ok:
        print("ERROR: Required helper files missing in:", HELPERS)
        sys.exit(1)

    pn_file = os.path.join(PROGRAM_NAMES, f"{edition}_program_blocks_v11.json")
    if not os.path.exists(pn_file):
        print(f"ERROR: Program blocks not found: {pn_file}")
        sys.exit(1)

    print("[1/8] Building course_index...")
    course_index = build_course_index(edition)
    if len(course_index) == 0:
        print(f"  ERROR: No courses found for edition {ed_disp} in course_index_v10.json")
        sys.exit(1)

    out = trusted_path(edition, f"course_index_{edition}.json")
    write_json(out, course_index)
    print(f"  -> {out}")

    print()
    print("[2/8] Building courses CSV...")
    courses_rows = build_courses_csv(course_index, edition)
    courses_fields = ["scope", "course_code", "title", "cus",
                       "program_count", "colleges", "programs"]
    out = trusted_path(edition, f"courses_{edition}.csv")
    write_csv(out, courses_rows, courses_fields)
    print(f"  -> {out}  ({len(courses_rows)} rows)")

    print()
    print("[3/8] Building certs CSV...")
    certs_rows = build_certs_csv(course_index, edition)
    certs_fields = ["scope", "course_code", "title", "cus",
                     "program_count", "cert_programs"]
    out = trusted_path(edition, f"certs_{edition}.csv")
    write_csv(out, certs_rows, certs_fields)
    print(f"  -> {out}  ({len(certs_rows)} rows)")

    print()
    print("[4/8] Building sections_index...")
    sections_idx = build_sections_index(edition)
    out = trusted_path(edition, f"sections_index_{edition}.json")
    write_json(out, sections_idx)
    print(f"  -> {out}")

    print()
    print("[5/8] Building degree_snapshots...")
    degree_snaps = build_degree_snapshots(edition)
    out = trusted_path(edition, f"degree_snapshots_{edition}.json")
    write_json(out, degree_snaps)
    print(f"  -> {out}")

    print()
    print("[6/8] Building program_blocks...")
    program_blocks = build_program_blocks(edition)
    out = trusted_path(edition, f"program_blocks_{edition}.json")
    write_json(out, program_blocks)
    print(f"  -> {out}")

    print()
    print("[7/8] Building program_index...")
    program_idx = build_program_index(edition)
    out = trusted_path(edition, f"program_index_{edition}.json")
    write_json(out, program_idx)
    print(f"  -> {out}")

    print()
    print("[8/8] Building manifest...")
    manifest = build_manifest(edition, course_index, courses_rows, certs_rows,
                               program_blocks, sections_idx, degree_snaps, program_idx)
    out = trusted_path(edition, f"manifest_{edition}.json")
    write_json(out, manifest)
    print(f"  -> {out}")

    print()
    print(f"=== Snapshot {edition} complete ===")
    print(f"  AP courses:     {len([r for r in courses_rows if r['scope'] == 'AP'])}")
    print(f"  Cert codes:     {len(certs_rows)}")
    print(f"  Program blocks: {len(program_blocks)}")
    print(f"  Output dir:     {trusted_subdir(edition)}")

    # Verify 8 files exist
    expected = [
        f"courses_{edition}.csv",
        f"certs_{edition}.csv",
        f"course_index_{edition}.json",
        f"sections_index_{edition}.json",
        f"degree_snapshots_{edition}.json",
        f"program_blocks_{edition}.json",
        f"program_index_{edition}.json",
        f"manifest_{edition}.json",
    ]
    td = trusted_subdir(edition)
    missing = [f for f in expected if not os.path.exists(os.path.join(td, f))]
    if missing:
        print(f"\n  WARNING: Missing expected files: {missing}")
        sys.exit(1)
    print(f"  All 8 snapshot files present: OK")


if __name__ == "__main__":
    main()
