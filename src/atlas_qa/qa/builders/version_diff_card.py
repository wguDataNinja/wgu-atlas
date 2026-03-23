"""Builder for VersionDiffCard canonical objects."""
from __future__ import annotations

import json
from pathlib import Path

from ..types import EvidenceRef, VersionDiffCard

_REPO_ROOT = Path(__file__).resolve().parents[4]


def _data(relative: str) -> Path:
    return _REPO_ROOT / relative


def _load_edition_diffs_full() -> list:
    with open(_data("data/catalog/edition_diffs/edition_diffs_full.json")) as f:
        return json.load(f)


def build_version_diff_cards() -> list[VersionDiffCard]:
    """Build VersionDiffCard objects from edition diff transitions.

    One card is created per course per transition where the course was added,
    removed, or had a title/CU change.
    """
    diffs = _load_edition_diffs_full()
    cards: list[VersionDiffCard] = []

    for diff in diffs:
        from_v = diff.get("from_catalog", "")
        to_v = diff.get("to_catalog", "")

        evidence_refs = [
            EvidenceRef(
                source_type="catalog_diff",
                artifact_id="edition_diffs_full",
                version=f"{from_v}→{to_v}",
            )
        ]

        # Courses added in this transition
        for course_code in diff.get("courses_added", []):
            cards.append(
                VersionDiffCard(
                    entity_type="course",
                    entity_id=course_code,
                    from_version=from_v,
                    to_version=to_v,
                    added=[course_code],
                    removed=[],
                    changed=[],
                    evidence_refs=evidence_refs,
                )
            )

        # Courses removed in this transition
        for course_code in diff.get("courses_removed", []):
            cards.append(
                VersionDiffCard(
                    entity_type="course",
                    entity_id=course_code,
                    from_version=from_v,
                    to_version=to_v,
                    added=[],
                    removed=[course_code],
                    changed=[],
                    evidence_refs=evidence_refs,
                )
            )

        # Title changes
        for change in diff.get("courses_with_title_changes", []):
            code = change.get("code", "")
            if not code:
                continue
            cards.append(
                VersionDiffCard(
                    entity_type="course",
                    entity_id=code,
                    from_version=from_v,
                    to_version=to_v,
                    added=[],
                    removed=[],
                    changed=[
                        {
                            "field": "title",
                            "from": change.get("from_title", ""),
                            "to": change.get("to_title", ""),
                        }
                    ],
                    evidence_refs=evidence_refs,
                )
            )

        # CU changes
        for change in diff.get("courses_with_cu_changes", []):
            code = change.get("code", "")
            if not code:
                continue
            cards.append(
                VersionDiffCard(
                    entity_type="course",
                    entity_id=code,
                    from_version=from_v,
                    to_version=to_v,
                    added=[],
                    removed=[],
                    changed=[
                        {
                            "field": "cus",
                            "from": str(change.get("from_cus", "")),
                            "to": str(change.get("to_cus", "")),
                        }
                    ],
                    evidence_refs=evidence_refs,
                )
            )

        # Program-level version changes (use version_changes_detail for structured data)
        for change in diff.get("version_changes_detail", []):
            prog_code = change.get("program_code", "")
            if not prog_code:
                continue
            cards.append(
                VersionDiffCard(
                    entity_type="program",
                    entity_id=prog_code,
                    from_version=from_v,
                    to_version=to_v,
                    added=[],
                    removed=[],
                    changed=[
                        {
                            "field": "version",
                            "from": str(change.get("from_version", "")),
                            "to": str(change.get("to_version", "")),
                        }
                    ],
                    evidence_refs=evidence_refs,
                )
            )

    return cards
