"""Builder for ProgramVersionCard canonical objects."""
from __future__ import annotations

import glob
import json
from pathlib import Path

from ..types import EvidenceRef, ProgramVersionCard

_REPO_ROOT = Path(__file__).resolve().parents[4]


def _data(relative: str) -> Path:
    return _REPO_ROOT / relative


def _load_program_blocks() -> list:
    with open(_data("data/catalog/trusted/2026_03/program_blocks_2026_03.json")) as f:
        return json.load(f)


def _load_course_index() -> dict:
    with open(_data("data/catalog/trusted/2026_03/course_index_2026_03.json")) as f:
        return json.load(f)


def _load_guide_manifest() -> list:
    with open(_data("data/program_guides/guide_manifest.json")) as f:
        return json.load(f)


def _load_parsed_guides() -> dict[str, dict]:
    """Return dict {program_code: parsed_data} for all parsed guide files."""
    parsed_dir = _data("data/program_guides/parsed")
    result: dict[str, dict] = {}
    for filepath in glob.glob(str(parsed_dir / "*_parsed.json")):
        with open(filepath) as f:
            data = json.load(f)
        prog_code = data.get("program_code") or data.get("inferred_program_code", "")
        if prog_code:
            result[prog_code] = data
    return result


def _extract_section_presence(manifest_entry: dict | None) -> dict[str, bool]:
    if manifest_entry is None:
        return {
            "has_standard_path": False,
            "has_areas_of_study": False,
            "has_capstone_section": False,
            "has_course_descriptions": False,
            "has_competency_bullets": False,
        }
    return {
        "has_standard_path": manifest_entry.get("has_standard_path", False),
        "has_areas_of_study": manifest_entry.get("has_areas_of_study", False),
        "has_capstone_section": manifest_entry.get("has_capstone_section", False),
        "has_course_descriptions": manifest_entry.get("has_course_descriptions", False),
        "has_competency_bullets": manifest_entry.get("has_competency_bullets", False),
    }


def build_program_version_cards() -> dict[str, ProgramVersionCard]:
    """Build all ProgramVersionCard objects, keyed by program_code."""
    program_blocks = _load_program_blocks()
    course_index = _load_course_index()
    guide_manifest = _load_guide_manifest()
    parsed_guides = _load_parsed_guides()

    # Build lookups
    manifest_by_code: dict[str, dict] = {
        e["inferred_program_code"]: e for e in guide_manifest
    }

    # Build degree -> program_code mapping for course lookup
    degree_to_code: dict[str, str] = {b["degree"]: b["code"] for b in program_blocks}

    # Build program_code -> course_codes from course_index
    code_to_course_codes: dict[str, set[str]] = {b["code"]: set() for b in program_blocks}
    for course_code, entry in course_index.items():
        for inst in entry.get("instances", []):
            prog_code = degree_to_code.get(inst.get("degree", ""))
            if prog_code and prog_code in code_to_course_codes:
                code_to_course_codes[prog_code].add(course_code)

    cards: dict[str, ProgramVersionCard] = {}

    for block in program_blocks:
        prog_code = block["code"]
        degree_title = block["degree"]
        college = block["college"]
        version = str(block.get("version", ""))
        total_cus = int(block.get("cus", 0))

        manifest_entry = manifest_by_code.get(prog_code)
        section_presence = _extract_section_presence(manifest_entry)

        # Guide version and pub_date from parsed guide
        parsed = parsed_guides.get(prog_code)
        if parsed:
            guide_version = str(parsed.get("version", "") or "")
            guide_pub_date = parsed.get("pub_date") or None
            if not guide_version:
                guide_version = None
        else:
            guide_version = None
            guide_pub_date = None

        course_codes = sorted(code_to_course_codes.get(prog_code, set()))

        evidence_refs = [
            EvidenceRef(
                source_type="catalog",
                artifact_id="program_blocks_2026_03",
                version="2026-03",
            )
        ]

        cards[prog_code] = ProgramVersionCard(
            program_code=prog_code,
            degree_title=degree_title,
            college=college,
            version=version,
            is_latest=True,  # Only 2026-03 catalog is loaded
            total_cus=total_cus,
            catalog_version="2026-03",
            course_codes=course_codes,
            section_presence=section_presence,
            guide_version=guide_version or None,
            guide_pub_date=guide_pub_date,
            evidence_refs=evidence_refs,
        )

    return cards
