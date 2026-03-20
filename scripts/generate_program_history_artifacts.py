#!/usr/bin/env python3
"""
generate_program_history_artifacts.py
=====================================
Stage 3 deterministic transform:
  data/program_lineage_enriched.json -> data/program_history.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate program-centric history artifact from lineage enriched data"
    )
    parser.add_argument(
        "--input",
        default="data/lineage/program_lineage_enriched.json",
        help="Input lineage-enriched JSON path",
    )
    parser.add_argument(
        "--output",
        default="data/lineage/program_history.json",
        help="Output program-history JSON path",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def normalize_events(events: list[dict]) -> list[dict]:
    # Preserve chronological ordering by start_edition first.
    return sorted(
        events,
        key=lambda ev: (
            str(ev.get("start_edition") or ""),
            str(ev.get("end_edition") or ""),
            str(ev.get("event_id") or ""),
        ),
    )


def build_program_history(events: list[dict]) -> list[dict]:
    by_program: dict[str, list[dict]] = {}

    for event in events:
        transition_type = str(event.get("transition_type") or "")
        start_edition = str(event.get("start_edition") or "")
        end_edition = str(event.get("end_edition") or "")
        pairs = event.get("pairs", [])
        if not isinstance(pairs, list):
            continue

        for pair in pairs:
            if not isinstance(pair, dict):
                continue
            predecessor = str(pair.get("from_program") or "").strip()
            successor = str(pair.get("to_program") or "").strip()
            if not predecessor or not successor:
                continue

            metrics = pair.get("metrics", {}) or {}
            entry = {
                "predecessor": predecessor,
                "transition_type": transition_type,
                "start_edition": start_edition,
                "end_edition": end_edition,
                "shared_course_count": metrics.get("shared_course_count", 0),
                "removed_course_count": metrics.get("removed_course_count", 0),
                "added_course_count": metrics.get("added_course_count", 0),
                "old_retained_pct": metrics.get("old_retained_pct", 0),
                "new_inherited_pct": metrics.get("new_inherited_pct", 0),
                "jaccard_overlap": metrics.get("jaccard_overlap", 0),
                "courses_added": pair.get("courses_added", []) or [],
                "courses_removed": pair.get("courses_removed", []) or [],
            }
            by_program.setdefault(successor, []).append(entry)

    programs: list[dict] = []
    for program_code in sorted(by_program.keys()):
        history = sorted(
            by_program[program_code],
            key=lambda item: (
                str(item.get("start_edition") or ""),
                str(item.get("end_edition") or ""),
                str(item.get("predecessor") or ""),
                str(item.get("transition_type") or ""),
            ),
        )
        programs.append({"program_code": program_code, "history": history})
    return programs


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    payload = load_json(input_path)
    events = payload.get("events", [])
    if not isinstance(events, list):
        events = []

    ordered_events = normalize_events(events)
    programs = build_program_history(ordered_events)

    output = {"programs": programs}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(f"Wrote {output_path} ({len(programs)} programs)")


if __name__ == "__main__":
    main()
