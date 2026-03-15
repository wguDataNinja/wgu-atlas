#!/usr/bin/env python3
"""
generate_program_history_enrichment.py
======================================
Builds the final Atlas-ready event-level program history enrichment artifact.

Input:
  data/program_lineage_enriched.json

Output:
  data/program_history_enrichment.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_TYPES = {
    "successor",
    "split",
    "merge",
    "family_restructure",
    "namespace_migration",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate final Atlas program history enrichment artifact"
    )
    parser.add_argument(
        "--input",
        default="data/program_lineage_enriched.json",
        help="Input lineage-enriched JSON path",
    )
    parser.add_argument(
        "--output",
        default="data/program_history_enrichment.json",
        help="Output final enrichment JSON path",
    )
    parser.add_argument(
        "--stage1",
        default="",
        help=(
            "Optional Stage 1 event file path with title metadata. "
            "If omitted, script tries metadata.source_file_used then known defaults."
        ),
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        return {}
    return data


def uniq_programs_with_titles(programs: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for item in programs:
        code = str(item.get("program_code") or "").strip().upper()
        if not code or code in seen:
            continue
        seen.add(code)
        out.append({"program_code": code, "title": str(item.get("title") or "").strip()})
    return out


def build_stage1_index(stage1_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    events = stage1_payload.get("events", [])
    if not isinstance(events, list):
        return {}
    index: dict[str, dict[str, Any]] = {}
    for ev in events:
        if not isinstance(ev, dict):
            continue
        event_id = str(ev.get("event_id") or "").strip()
        if not event_id:
            continue
        index[event_id] = ev
    return index


def as_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def as_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def compute_event_stats(pairs: list[dict[str, Any]]) -> dict[str, float]:
    if not pairs:
        return {
            "pair_count": 0,
            "max_jaccard": 0.0,
            "avg_jaccard": 0.0,
            "max_shared": 0.0,
            "max_old_retained": 0.0,
            "max_new_inherited": 0.0,
        }

    jaccards = [as_float(p.get("jaccard_overlap", 0)) for p in pairs]
    shared = [as_int(p.get("shared_course_count", 0)) for p in pairs]
    old_retained = [as_float(p.get("old_retained_pct", 0)) for p in pairs]
    new_inherited = [as_float(p.get("new_inherited_pct", 0)) for p in pairs]
    return {
        "pair_count": len(pairs),
        "max_jaccard": max(jaccards),
        "avg_jaccard": sum(jaccards) / len(jaccards),
        "max_shared": float(max(shared)),
        "max_old_retained": max(old_retained),
        "max_new_inherited": max(new_inherited),
    }


def infer_importance_and_site_worthy(
    transition_type: str,
    stats: dict[str, float],
) -> tuple[str, bool]:
    pair_count = int(stats["pair_count"])
    max_jaccard = stats["max_jaccard"]
    avg_jaccard = stats["avg_jaccard"]
    max_shared = stats["max_shared"]
    max_old_retained = stats["max_old_retained"]
    max_new_inherited = stats["max_new_inherited"]

    if pair_count == 0:
        return "low", False

    importance = "medium"
    if transition_type == "successor":
        if (
            max_jaccard >= 0.35
            or (max_old_retained >= 0.60 and max_new_inherited >= 0.60)
            or max_shared >= 12
        ):
            importance = "high"
        elif max_jaccard < 0.15 and max_shared < 5:
            importance = "low"
    elif transition_type in {"split", "merge"}:
        if max_jaccard >= 0.20 or max_shared >= 8:
            importance = "high"
        elif max_jaccard < 0.08 and max_shared < 4:
            importance = "medium"
    elif transition_type == "family_restructure":
        if pair_count >= 3 and (avg_jaccard >= 0.25 or max_shared >= 12):
            importance = "high"
        elif max_jaccard < 0.12 and max_shared < 4:
            importance = "low"
    elif transition_type == "namespace_migration":
        if max_jaccard >= 0.50 and max_shared >= 10:
            importance = "high"
        elif max_jaccard < 0.10 and max_shared < 4:
            importance = "low"
        else:
            importance = "medium"
    else:
        if max_jaccard < 0.10 and max_shared < 4:
            importance = "low"
        elif max_jaccard >= 0.30 or max_shared >= 10:
            importance = "high"
        else:
            importance = "medium"

    site_worthy = True
    if importance == "low":
        site_worthy = False
    elif (
        importance == "medium"
        and transition_type == "namespace_migration"
        and max_jaccard < 0.15
        and max_shared < 5
    ):
        site_worthy = False

    return importance, site_worthy


def choose_stage1_path(args_stage1: str, enriched: dict[str, Any]) -> Path | None:
    candidates: list[Path] = []
    if args_stage1:
        candidates.append(Path(args_stage1))

    meta = enriched.get("metadata", {})
    if isinstance(meta, dict):
        source_file_used = str(meta.get("source_file_used") or "").strip()
        if source_file_used:
            candidates.append(Path(source_file_used))

    candidates.extend(
        [
            Path("data/program_lineage_events.json"),
            Path("data/program_ineage_events.json"),
            Path("data/program_lineage_events_normalized.json"),
        ]
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    enriched = load_json(input_path)
    enriched_events = enriched.get("events", [])
    if not isinstance(enriched_events, list):
        enriched_events = []

    stage1_path = choose_stage1_path(args.stage1, enriched)
    stage1_index: dict[str, dict[str, Any]] = {}
    if stage1_path:
        stage1_payload = load_json(stage1_path)
        stage1_index = build_stage1_index(stage1_payload)

    out_events: list[dict[str, Any]] = []
    for ev in enriched_events:
        if not isinstance(ev, dict):
            continue

        event_id = str(ev.get("event_id") or "").strip()
        transition_type = str(ev.get("transition_type") or "").strip()
        if transition_type not in ALLOWED_TYPES:
            transition_type = "family_restructure"

        start_edition = str(ev.get("start_edition") or "").strip()
        end_edition = str(ev.get("end_edition") or "").strip()

        pairs_raw = ev.get("pairs", [])
        if not isinstance(pairs_raw, list):
            pairs_raw = []

        compact_pairs: list[dict[str, Any]] = []
        inferred_from_codes: list[str] = []
        inferred_to_codes: list[str] = []
        for pair in pairs_raw:
            if not isinstance(pair, dict):
                continue
            metrics = pair.get("metrics", {}) or {}
            from_program = str(pair.get("from_program") or "").strip().upper()
            to_program = str(pair.get("to_program") or "").strip().upper()
            if not from_program or not to_program:
                continue

            inferred_from_codes.append(from_program)
            inferred_to_codes.append(to_program)

            compact_pairs.append(
                {
                    "from_program": from_program,
                    "to_program": to_program,
                    "shared_course_count": as_int(metrics.get("shared_course_count", 0)),
                    "removed_course_count": as_int(metrics.get("removed_course_count", 0)),
                    "added_course_count": as_int(metrics.get("added_course_count", 0)),
                    "old_retained_pct": as_float(metrics.get("old_retained_pct", 0)),
                    "new_inherited_pct": as_float(metrics.get("new_inherited_pct", 0)),
                    "jaccard_overlap": as_float(metrics.get("jaccard_overlap", 0)),
                    "courses_added": pair.get("courses_added", []) or [],
                    "courses_removed": pair.get("courses_removed", []) or [],
                }
            )

        stage1_event = stage1_index.get(event_id, {})
        from_programs_stage1 = uniq_programs_with_titles(
            stage1_event.get("from_programs", []) if isinstance(stage1_event, dict) else []
        )
        to_programs_stage1 = uniq_programs_with_titles(
            stage1_event.get("to_programs", []) if isinstance(stage1_event, dict) else []
        )

        if from_programs_stage1:
            from_programs = from_programs_stage1
        else:
            from_programs = uniq_programs_with_titles(
                [{"program_code": code, "title": ""} for code in inferred_from_codes]
            )

        if to_programs_stage1:
            to_programs = to_programs_stage1
        else:
            to_programs = uniq_programs_with_titles(
                [{"program_code": code, "title": ""} for code in inferred_to_codes]
            )

        stats = compute_event_stats(compact_pairs)
        importance, site_worthy = infer_importance_and_site_worthy(transition_type, stats)

        out_events.append(
            {
                "event_id": event_id,
                "transition_type": transition_type,
                "start_edition": start_edition,
                "end_edition": end_edition,
                "from_programs": from_programs,
                "to_programs": to_programs,
                "importance": importance,
                "site_worthy": site_worthy,
                "pairs": compact_pairs,
            }
        )

    out_events.sort(
        key=lambda ev: (
            str(ev.get("start_edition") or ""),
            str(ev.get("end_edition") or ""),
            str(ev.get("event_id") or ""),
        )
    )

    output = {"events": out_events}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(f"Wrote {output_path} ({len(out_events)} events)")


if __name__ == "__main__":
    main()
