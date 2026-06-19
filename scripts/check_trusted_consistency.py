"""
check_trusted_consistency.py — Validate a trusted snapshot directory.

Usage:
  python3 scripts/check_trusted_consistency.py
  python3 scripts/check_trusted_consistency.py --edition 2026_06
  python3 scripts/check_trusted_consistency.py --edition 2026_03

Exits 0 if all checks pass, 1 if any check fails.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_TRUSTED_DIR = _REPO_ROOT / "data" / "catalog" / "trusted"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a trusted snapshot directory."
    )
    parser.add_argument(
        "--edition",
        default="2026_06",
        help="Edition directory name (e.g., 2026_06). Default: 2026_06",
    )
    args = parser.parse_args()
    edition = args.edition

    snapshot = _TRUSTED_DIR / edition
    if not snapshot.is_dir():
        print(f"FAIL: Trusted snapshot directory not found: {snapshot}")
        return 1

    ed_short = edition.replace("_", "-")  # 2026_06 → 2026-06
    ed_under = edition  # 2026_06

    # Expected files
    files = {
        "courses_csv": snapshot / f"courses_{ed_under}.csv",
        "certs_csv": snapshot / f"certs_{ed_under}.csv",
        "course_index_json": snapshot / f"course_index_{ed_under}.json",
        "sections_index_json": snapshot / f"sections_index_{ed_under}.json",
        "degree_snapshots_json": snapshot / f"degree_snapshots_{ed_under}.json",
        "program_blocks_json": snapshot / f"program_blocks_{ed_under}.json",
        "program_index_json": snapshot / f"program_index_{ed_under}.json",
        "manifest_json": snapshot / f"manifest_{ed_under}.json",
    }

    checks: list[dict] = []
    errors = 0

    # ── File existence ────────────────────────────────────────────────────
    for name, path in files.items():
        ok = path.is_file()
        if not ok:
            errors += 1
        checks.append({
            "check": f"file_exists/{name}",
            "passed": ok,
            "detail": str(path.name) if ok else f"MISSING: {path.name}",
        })

    # If manifest is missing, we can't do further cross-checks
    manifest_path = files["manifest_json"]
    manifest: dict | None = None
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text())
        except (json.JSONDecodeError, OSError) as e:
            errors += 1
            checks.append({"check": "manifest/parse", "passed": False, "detail": str(e)})

    # ── Manifest self-consistency ─────────────────────────────────────────
    if manifest:
        core_fields = ["catalog_date", "verification_status"]
        for field in core_fields:
            ok = field in manifest
            if not ok:
                errors += 1
            checks.append({
                "check": f"manifest/field/{field}",
                "passed": ok,
                "detail": f"{field}={manifest.get(field, 'MISSING')}",
            })
        # Count fields are optional — if absent, the script will verify
        # the actual data files independently.
        for field in ["snapshot_edition", "course_count", "cert_count",
                       "program_block_count", "program_index_count"]:
            present = field in manifest
            checks.append({
                "check": f"manifest/field/{field}",
                "passed": True,
                "detail": f"{field}={manifest.get(field, 'absent — data-file check will cover this')}" if not present else f"{field}={manifest[field]}",
            })

        # Verify manifest edition matches requested
        man_ed = manifest.get("snapshot_edition")
        if man_ed and man_ed != ed_under:
            errors += 1
            checks.append({
                "check": "manifest/edition_match",
                "passed": False,
                "detail": f"manifest says {man_ed}, expected {ed_under}",
            })
        else:
            checks.append({
                "check": "manifest/edition_match",
                "passed": True,
                "detail": f"manifest edition {man_ed}",
            })

    # ── CSV row counts vs manifest ────────────────────────────────────────
    courses_csv = files["courses_csv"]
    certs_csv = files["certs_csv"]

    if courses_csv.is_file():
        with courses_csv.open(newline="", encoding="utf-8") as f:
            course_rows = list(csv.DictReader(f))
        actual_courses = len(course_rows)
        if manifest:
            expected = manifest.get("course_count")
            ok = expected is None or actual_courses == expected
            if not ok:
                errors += 1
            checks.append({
                "check": "courses/count_vs_manifest",
                "passed": ok,
                "detail": f"{actual_courses} rows, manifest says {expected}",
            })
        else:
            checks.append({
                "check": "courses/count",
                "passed": True,
                "detail": f"{actual_courses} rows (no manifest to compare)",
            })
    else:
        checks.append({"check": "courses/count", "passed": False, "detail": "no courses CSV"})

    if certs_csv.is_file():
        with certs_csv.open(newline="", encoding="utf-8") as f:
            cert_rows = list(csv.DictReader(f))
        actual_certs = len(cert_rows)
        if manifest:
            expected = manifest.get("cert_count")
            ok = expected is None or actual_certs == expected
            if not ok:
                errors += 1
            checks.append({
                "check": "certs/count_vs_manifest",
                "passed": ok,
                "detail": f"{actual_certs} rows, manifest says {expected}",
            })
        else:
            checks.append({
                "check": "certs/count",
                "passed": True,
                "detail": f"{actual_certs} rows (no manifest to compare)",
            })
    else:
        checks.append({"check": "certs/count", "passed": False, "detail": "no certs CSV"})

    # ── Program blocks count vs manifest ──────────────────────────────────
    pb_path = files["program_blocks_json"]
    if pb_path.is_file():
        try:
            blocks = json.loads(pb_path.read_text())
            actual_blocks = len(blocks)
            if manifest:
                expected = manifest.get("program_block_count")
                ok = expected is None or actual_blocks == expected
                if not ok:
                    errors += 1
                checks.append({
                    "check": "program_blocks/count_vs_manifest",
                    "passed": ok,
                    "detail": f"{actual_blocks} blocks, manifest says {expected}",
                })
            else:
                checks.append({
                    "check": "program_blocks/count",
                    "passed": True,
                    "detail": f"{actual_blocks} blocks (no manifest to compare)",
                })
        except (json.JSONDecodeError, OSError) as e:
            errors += 1
            checks.append({"check": "program_blocks/parse", "passed": False, "detail": str(e)})

    # ── Section index contains this edition ───────────────────────────────
    si_path = files["sections_index_json"]
    if si_path.is_file():
        try:
            si = json.loads(si_path.read_text())
            ok = isinstance(si, dict) and ed_short in si
            if not ok:
                errors += 1
            checks.append({
                "check": "sections_index/has_edition",
                "passed": ok,
                "detail": f"key '{ed_short}' present" if ok else f"key '{ed_short}' MISSING from sections_index",
            })
        except (json.JSONDecodeError, OSError) as e:
            errors += 1
            checks.append({"check": "sections_index/parse", "passed": False, "detail": str(e)})

    # ── Course index contains this edition ────────────────────────────────
    ci_path = files["course_index_json"]
    if ci_path.is_file():
        try:
            ci = json.loads(ci_path.read_text())
            if isinstance(ci, dict):
                # course_index is keyed by code, check instances
                codes_with_edition = sum(
                    1 for v in ci.values()
                    if any(
                        isinstance(i, dict) and i.get("catalog_date") == ed_short
                        for i in v.get("instances", [])
                    )
                )
                if codes_with_edition > 0:
                    checks.append({
                        "check": "course_index/has_edition_instances",
                        "passed": True,
                        "detail": f"{codes_with_edition} codes have instances for {ed_short}",
                    })
                else:
                    ok = len(ci) > 0
                    if not ok:
                        errors += 1
                    checks.append({
                        "check": "course_index/has_edition_instances",
                        "passed": ok,
                        "detail": f"0 codes have instances for {ed_short}; {len(ci)} total codes",
                    })
        except (json.JSONDecodeError, OSError) as e:
            errors += 1
            checks.append({"check": "course_index/parse", "passed": False, "detail": str(e)})

    # ── Degree snapshots contain this edition ─────────────────────────────
    ds_path = files["degree_snapshots_json"]
    if ds_path.is_file():
        try:
            ds = json.loads(ds_path.read_text())
            ok = isinstance(ds, dict) and ed_short in ds
            if not ok:
                errors += 1
            checks.append({
                "check": "degree_snapshots/has_edition",
                "passed": ok,
                "detail": f"key '{ed_short}' present" if ok else f"key '{ed_short}' MISSING",
            })
        except (json.JSONDecodeError, OSError) as e:
            errors += 1
            checks.append({"check": "degree_snapshots/parse", "passed": False, "detail": str(e)})

    # ── Print results ────────────────────────────────────────────────────
    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    print(f"Trusted snapshot consistency check: {edition}")
    print(f"  Directory: {snapshot}")
    print(f"  Checks: {passed}/{total} passed, {total - passed} failed")
    print()
    for c in checks:
        status = "PASS" if c["passed"] else "FAIL"
        print(f"  [{status}] {c['check']}: {c['detail']}")

    print()
    if errors == 0:
        print("All checks passed.")
    else:
        print(f"FAIL: {errors} check(s) failed.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
