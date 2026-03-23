"""Builder for GuideSectionCard canonical objects."""
from __future__ import annotations

import glob
import json
from pathlib import Path

from ..types import EvidenceRef, GuideSectionCard

_REPO_ROOT = Path(__file__).resolve().parents[4]


def _data(relative: str) -> Path:
    return _REPO_ROOT / relative


def _load_course_index() -> dict:
    with open(_data("data/catalog/trusted/2026_03/course_index_2026_03.json")) as f:
        return json.load(f)


def _build_title_to_course_code(course_index: dict) -> dict[str, str]:
    """Build a lookup from canonical_title (lowercased) -> course_code."""
    lookup: dict[str, str] = {}
    for code, entry in course_index.items():
        title = entry.get("canonical_title", "")
        if title:
            lookup[title.lower().strip()] = code
    return lookup


def _resolve_course_codes(titles: list[str], title_lookup: dict[str, str]) -> list[str]:
    """Resolve a list of course titles to course codes where possible."""
    codes: list[str] = []
    seen: set[str] = set()
    for title in titles:
        code = title_lookup.get(title.lower().strip())
        if code and code not in seen:
            codes.append(code)
            seen.add(code)
    return codes


def build_guide_section_cards() -> list[GuideSectionCard]:
    """Build GuideSectionCard objects for all parsed guides."""
    course_index = _load_course_index()
    title_lookup = _build_title_to_course_code(course_index)

    parsed_dir = _data("data/program_guides/parsed")
    cards: list[GuideSectionCard] = []

    for filepath in sorted(glob.glob(str(parsed_dir / "*_parsed.json"))):
        with open(filepath) as f:
            guide = json.load(f)

        prog_code = guide.get("program_code") or guide.get("inferred_program_code", "")
        guide_version = str(guide.get("version", "") or "unknown")

        evidence_refs = [
            EvidenceRef(
                source_type="program_guide",
                artifact_id=f"{prog_code}_parsed",
                version=guide_version,
            )
        ]

        # --- standard_path card ---
        standard_path = guide.get("standard_path")
        if standard_path:
            sp_titles = [item["title"] for item in standard_path if "title" in item]
            sp_codes = _resolve_course_codes(sp_titles, title_lookup)
            cards.append(
                GuideSectionCard(
                    program_code=prog_code,
                    guide_version=guide_version,
                    section_type="standard_path",
                    linked_course_codes=sp_codes,
                    section_data={"items": standard_path},
                    evidence_refs=evidence_refs,
                )
            )

        # --- areas_of_study card ---
        areas_of_study = guide.get("areas_of_study")
        if areas_of_study:
            aos_titles: list[str] = []
            for group in areas_of_study:
                for course in group.get("courses", []):
                    if "title" in course:
                        aos_titles.append(course["title"])
            aos_codes = _resolve_course_codes(aos_titles, title_lookup)
            cards.append(
                GuideSectionCard(
                    program_code=prog_code,
                    guide_version=guide_version,
                    section_type="areas_of_study",
                    linked_course_codes=aos_codes,
                    section_data={"groups": areas_of_study},
                    evidence_refs=evidence_refs,
                )
            )

        # --- capstone card ---
        capstone = guide.get("capstone")
        if capstone:
            capstone_title = capstone.get("title", "")
            cap_codes = _resolve_course_codes(
                [capstone_title] if capstone_title else [], title_lookup
            )
            cards.append(
                GuideSectionCard(
                    program_code=prog_code,
                    guide_version=guide_version,
                    section_type="capstone",
                    linked_course_codes=cap_codes,
                    section_data=capstone,
                    evidence_refs=evidence_refs,
                )
            )

    return cards
