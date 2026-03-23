#!/usr/bin/env python3
"""Validate canonical objects produced by the build scripts.

Checks:
1. Uniqueness: no duplicate course_codes in course_cards.json
2. C179: cat_short_text_flag=True
3. D554: guide_description_alternates=[], guide_misrouted_text_flag=True
4. All objects conform to their Pydantic schema
5. Output files exist (determinism prerequisite)
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from atlas_qa.qa.types import (
    CourseCard,
    GuideSectionCard,
    ProgramVersionCard,
    VersionDiffCard,
)

DATA_DIR = REPO_ROOT / "data" / "atlas_qa"
COURSE_CARDS_FILE = DATA_DIR / "course_cards.json"
PROGRAM_CARDS_FILE = DATA_DIR / "program_version_cards.json"
GUIDE_SECTION_FILE = DATA_DIR / "guide_section_cards.json"
VERSION_DIFF_FILE = DATA_DIR / "version_diff_cards.json"

_errors: list[str] = []
_passed: int = 0


def _fail(msg: str) -> None:
    _errors.append(msg)
    print(f"  FAIL: {msg}")


def _ok(msg: str) -> None:
    global _passed
    _passed += 1
    print(f"  OK  : {msg}")


# ---------------------------------------------------------------------------
# 1. File existence
# ---------------------------------------------------------------------------
def check_files_exist() -> dict:
    print("\n[1] File existence checks")
    results = {}
    for label, path in [
        ("course_cards.json", COURSE_CARDS_FILE),
        ("program_version_cards.json", PROGRAM_CARDS_FILE),
        ("guide_section_cards.json", GUIDE_SECTION_FILE),
        ("version_diff_cards.json", VERSION_DIFF_FILE),
    ]:
        if path.exists():
            _ok(f"{label} exists")
            results[label] = True
        else:
            _fail(f"{label} missing at {path}")
            results[label] = False
    return results


# ---------------------------------------------------------------------------
# 2. Load and parse course_cards
# ---------------------------------------------------------------------------
def check_course_cards() -> dict:
    print("\n[2] course_cards.json schema + anomaly checks")
    if not COURSE_CARDS_FILE.exists():
        _fail("Skipping — file missing")
        return {}

    with open(COURSE_CARDS_FILE) as f:
        raw = json.load(f)

    # Uniqueness (dict keyed by course_code is inherently unique, but verify)
    if len(raw) == len(set(raw.keys())):
        _ok(f"No duplicate course_codes (total {len(raw)})")
    else:
        _fail("Duplicate course_codes found in dict keys")

    # Schema compliance — parse all
    parse_errors = 0
    cards = {}
    for code, data in raw.items():
        try:
            card = CourseCard.model_validate(data)
            cards[code] = card
        except Exception as e:
            parse_errors += 1
            if parse_errors <= 5:
                _fail(f"Schema error for {code}: {e}")
    if parse_errors == 0:
        _ok(f"All {len(raw)} course_cards parse against CourseCard schema")
    else:
        _fail(f"{parse_errors} course_card(s) failed schema validation")

    # C179 anomaly
    c179 = cards.get("C179")
    if c179:
        if c179.cat_short_text_flag:
            _ok("C179.cat_short_text_flag=True (correct)")
        else:
            _fail("C179.cat_short_text_flag should be True but is False")
        if c179.catalog_description and len(c179.catalog_description) <= 300:
            _ok(f"C179 description is ≤300 chars ({len(c179.catalog_description)})")
        else:
            desc_len = len(c179.catalog_description) if c179.catalog_description else 0
            _fail(f"C179 description length is {desc_len}, expected ≤300")
    else:
        _fail("C179 not found in course_cards")

    # D554 anomaly
    d554 = cards.get("D554")
    if d554:
        if d554.guide_misrouted_text_flag:
            _ok("D554.guide_misrouted_text_flag=True (correct)")
        else:
            _fail("D554.guide_misrouted_text_flag should be True but is False")
        if d554.guide_description_alternates == []:
            _ok("D554.guide_description_alternates=[] (correct)")
        else:
            _fail(
                f"D554.guide_description_alternates should be [] but has "
                f"{len(d554.guide_description_alternates)} entries"
            )
    else:
        _fail("D554 not found in course_cards")

    return cards


# ---------------------------------------------------------------------------
# 3. Program version cards
# ---------------------------------------------------------------------------
def check_program_version_cards() -> None:
    print("\n[3] program_version_cards.json schema checks")
    if not PROGRAM_CARDS_FILE.exists():
        _fail("Skipping — file missing")
        return

    with open(PROGRAM_CARDS_FILE) as f:
        raw = json.load(f)

    parse_errors = 0
    for code, data in raw.items():
        try:
            ProgramVersionCard.model_validate(data)
        except Exception as e:
            parse_errors += 1
            if parse_errors <= 5:
                _fail(f"Schema error for program {code}: {e}")
    if parse_errors == 0:
        _ok(f"All {len(raw)} program_version_cards parse against schema")
    else:
        _fail(f"{parse_errors} program_version_card(s) failed schema validation")


# ---------------------------------------------------------------------------
# 4. Guide section cards
# ---------------------------------------------------------------------------
def check_guide_section_cards() -> None:
    print("\n[4] guide_section_cards.json schema checks")
    if not GUIDE_SECTION_FILE.exists():
        _fail("Skipping — file missing")
        return

    with open(GUIDE_SECTION_FILE) as f:
        raw = json.load(f)

    parse_errors = 0
    for i, data in enumerate(raw):
        try:
            GuideSectionCard.model_validate(data)
        except Exception as e:
            parse_errors += 1
            if parse_errors <= 5:
                _fail(f"Schema error for guide_section_card[{i}]: {e}")
    if parse_errors == 0:
        _ok(f"All {len(raw)} guide_section_cards parse against schema")
    else:
        _fail(f"{parse_errors} guide_section_card(s) failed schema validation")


# ---------------------------------------------------------------------------
# 5. Version diff cards
# ---------------------------------------------------------------------------
def check_version_diff_cards() -> None:
    print("\n[5] version_diff_cards.json schema checks")
    if not VERSION_DIFF_FILE.exists():
        _fail("Skipping — file missing")
        return

    with open(VERSION_DIFF_FILE) as f:
        raw = json.load(f)

    parse_errors = 0
    for i, data in enumerate(raw):
        try:
            VersionDiffCard.model_validate(data)
        except Exception as e:
            parse_errors += 1
            if parse_errors <= 5:
                _fail(f"Schema error for version_diff_card[{i}]: {e}")
    if parse_errors == 0:
        _ok(f"All {len(raw)} version_diff_cards parse against schema")
    else:
        _fail(f"{parse_errors} version_diff_card(s) failed schema validation")


# ---------------------------------------------------------------------------
# 6. Determinism check: file already exists = idempotency asserted by caller
# ---------------------------------------------------------------------------
def check_determinism() -> None:
    print("\n[6] Determinism (file presence implies idempotency)")
    all_exist = all(
        p.exists()
        for p in [COURSE_CARDS_FILE, PROGRAM_CARDS_FILE, GUIDE_SECTION_FILE, VERSION_DIFF_FILE]
    )
    if all_exist:
        _ok("All output files present — run build scripts again and diff to verify idempotency")
    else:
        _fail("Not all output files present; run build scripts first")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("=" * 60)
    print("Atlas QA: Canonical Object Validation")
    print("=" * 60)

    check_files_exist()
    check_course_cards()
    check_program_version_cards()
    check_guide_section_cards()
    check_version_diff_cards()
    check_determinism()

    print("\n" + "=" * 60)
    total = _passed + len(_errors)
    print(f"Results: {_passed}/{total} passed, {len(_errors)} failure(s)")
    if _errors:
        print("\nFailures:")
        for e in _errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("All checks passed.")


if __name__ == "__main__":
    main()
