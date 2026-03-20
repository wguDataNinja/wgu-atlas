#!/usr/bin/env python3
"""
compare_program_courses.py
==========================
Stage 2 lineage enrichment:
- Loads Stage 1 lineage events
- Normalizes resiliently for minor LLM JSON formatting drift
- Compares from_program/to_program course rosters
- Emits pair-level overlap and diffs

Primary output:
  data/program_lineage_enriched.json

Normalization output:
  data/program_lineage_events_normalized.json
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable


DEFAULT_CATALOG_ROOT = "/Users/buddy/Desktop/WGU-Reddit/WGU_catalog"
COURSE_ROW_FULL_RE = re.compile(
    r"^[A-Z]{2,5}\s+\d{1,4}[A-Z]?\s+([A-Z][A-Z0-9]{1,5})\s+.+\s+\d+\s+\d+\s*$"
)
COURSE_ROW_CODE_ONLY_RE = re.compile(
    r"^([A-Z][A-Z0-9]{1,5})\s+.+\s+\d+\s+\d+\s*$"
)
STOPWORDS = {
    "a",
    "and",
    "arts",
    "bachelor",
    "certificate",
    "degree",
    "in",
    "management",
    "master",
    "of",
    "program",
    "science",
    "specialization",
    "the",
    "to",
}


@dataclass(frozen=True)
class ProgramRef:
    program_code: str
    title: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare lineage program course rosters")
    parser.add_argument(
        "--input",
        default="data/lineage/program_lineage_events.json",
        help="Stage 1 lineage events JSON input",
    )
    parser.add_argument(
        "--normalized-output",
        default="data/lineage/program_lineage_events_normalized.json",
        help="Normalized Stage 1 JSON output path",
    )
    parser.add_argument(
        "--canonical-courses",
        default="data/canonical_courses.csv",
        help="Path to canonical_courses.csv for valid course code set",
    )
    parser.add_argument(
        "--catalog-root",
        default=os.environ.get("WGU_CATALOG_ROOT", DEFAULT_CATALOG_ROOT),
        help=(
            "Path to WGU_catalog root containing outputs/program_names and "
            "data/raw_catalog_texts"
        ),
    )
    parser.add_argument(
        "--output",
        default="data/lineage/program_lineage_enriched.json",
        help="Output JSON path",
    )
    return parser.parse_args()


def normalize_text(value: str) -> str:
    s = (value or "").lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9\s]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def tokenize(value: str) -> set[str]:
    tokens = set()
    for token in normalize_text(value).split():
        if token in STOPWORDS:
            continue
        if len(token) <= 1:
            continue
        tokens.add(token)
    return tokens


def title_similarity(a: str, b: str) -> float:
    ta = tokenize(a)
    tb = tokenize(b)
    union = ta | tb
    if not union:
        return 0.0
    return len(ta & tb) / len(union)


def format_edition_underscore(edition: str) -> str:
    year, month = edition.split("-")
    return f"{int(year):04d}_{int(month):02d}"


def load_valid_course_codes(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return {
            (row.get("course_code") or "").strip().upper()
            for row in reader
            if (row.get("course_code") or "").strip()
        }


def resolve_input_path(path: Path) -> tuple[Path, list[str]]:
    notes: list[str] = []
    if path.exists():
        return path, notes

    typo_fallback = path.with_name(path.name.replace("_lineage_", "_ineage_"))
    if typo_fallback.exists():
        notes.append(
            f"Input {path} not found; using fallback {typo_fallback}."
        )
        return typo_fallback, notes

    raise FileNotFoundError(f"Input lineage events file not found: {path}")


def strip_trailing_commas(raw: str) -> str:
    prev = raw
    while True:
        cleaned = re.sub(r",\s*(?=[}\]])", "", prev)
        if cleaned == prev:
            return cleaned
        prev = cleaned


def append_missing_closers(raw: str) -> str:
    stack: list[str] = []
    in_string = False
    escaped = False
    for ch in raw:
        if in_string:
            if escaped:
                escaped = False
                continue
            if ch == "\\":
                escaped = True
                continue
            if ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == "{":
            stack.append("}")
        elif ch == "[":
            stack.append("]")
        elif ch in "}]":
            if stack and ch == stack[-1]:
                stack.pop()
    if not stack:
        return raw
    return raw + "".join(reversed(stack))


def normalize_program_ref(value: object) -> ProgramRef | None:
    if isinstance(value, str):
        code = value.strip().upper()
        if not code:
            return None
        return ProgramRef(program_code=code, title="")

    if not isinstance(value, dict):
        return None

    code = (
        str(
            value.get("program_code")
            or value.get("code")
            or value.get("program")
            or value.get("from_program")
            or value.get("to_program")
            or ""
        )
        .strip()
        .upper()
    )
    if not code:
        return None
    title = str(value.get("title") or value.get("program_title") or "").strip()
    return ProgramRef(program_code=code, title=title)


def coerce_program_list(value: object) -> list[dict]:
    if value is None:
        return []
    if isinstance(value, dict):
        value = [value]
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []

    refs: list[ProgramRef] = []
    seen: set[str] = set()
    for item in value:
        ref = normalize_program_ref(item)
        if not ref:
            continue
        if ref.program_code in seen:
            continue
        seen.add(ref.program_code)
        refs.append(ref)
    return [{"program_code": ref.program_code, "title": ref.title} for ref in refs]


def coerce_events_schema(parsed: object) -> dict:
    if isinstance(parsed, dict):
        root = dict(parsed)
        raw_events = root.get("events", [])
    elif isinstance(parsed, list):
        root = {}
        raw_events = parsed
    else:
        root = {}
        raw_events = []

    if not isinstance(raw_events, list):
        raw_events = []

    events: list[dict] = []
    for idx, raw in enumerate(raw_events, start=1):
        if not isinstance(raw, dict):
            continue
        event = dict(raw)
        event.setdefault("event_id", f"PLE-AUTO-{idx:03d}")
        event.setdefault("transition_type", "ambiguous")
        event.setdefault("start_edition", "")
        event.setdefault("end_edition", "")
        event["from_programs"] = coerce_program_list(
            event.get("from_programs", event.get("from_program"))
        )
        event["to_programs"] = coerce_program_list(
            event.get("to_programs", event.get("to_program"))
        )
        if not isinstance(event.get("summary"), str):
            event["summary"] = str(event.get("summary") or "")
        events.append(event)

    root["events"] = events
    return root


def load_events_with_normalization(path: Path) -> tuple[dict, bool, list[str]]:
    notes: list[str] = []
    raw = path.read_text(encoding="utf-8", errors="replace")
    raw = raw.lstrip("\ufeff")

    normalization_applied = False
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        normalization_applied = True
        notes.append(f"Initial JSON parse failed: {exc}. Applying normalization pass.")
        cleaned = strip_trailing_commas(raw)
        cleaned = append_missing_closers(cleaned)
        parsed = json.loads(cleaned)
    coerced = coerce_events_schema(parsed)
    return coerced, normalization_applied, notes


def ensure_catalog_sources(catalog_root: Path) -> tuple[Path, Path]:
    blocks_dir = catalog_root / "outputs" / "program_names"
    texts_dir = catalog_root / "data" / "raw_catalog_texts"
    if not blocks_dir.exists():
        raise FileNotFoundError(f"Missing program blocks directory: {blocks_dir}")
    if not texts_dir.exists():
        raise FileNotFoundError(f"Missing raw catalog texts directory: {texts_dir}")
    return blocks_dir, texts_dir


def parse_program_roster(
    lines: list[str],
    ccn_idx: int,
    end_idx: int,
    valid_course_codes: set[str],
) -> set[str]:
    roster: set[str] = set()
    start = max(ccn_idx, 0)
    end = min(end_idx, len(lines))

    for i in range(start, end):
        stripped = lines[i].strip()
        if not stripped:
            continue
        if stripped.startswith("CCN"):
            continue
        if stripped.startswith("©"):
            continue
        if stripped.startswith("Total CUs:"):
            continue
        if "Total CUs:" in stripped and re.match(r"^[A-Z0-9_\-]+\s+\d{6}\s+Total CUs:", stripped):
            continue
        if stripped.startswith("Elective Options"):
            continue
        if stripped.startswith("ENDS"):
            continue

        code = ""
        match = COURSE_ROW_FULL_RE.match(stripped)
        if match:
            code = match.group(1)
        else:
            match = COURSE_ROW_CODE_ONLY_RE.match(stripped)
            if match:
                code = match.group(1)

        if not code:
            continue
        code = code.upper()
        if valid_course_codes and code not in valid_course_codes:
            continue
        roster.add(code)

    return roster


def build_rosters_by_edition(
    editions: set[str],
    blocks_dir: Path,
    texts_dir: Path,
    valid_course_codes: set[str],
) -> tuple[dict[str, dict[str, set[str]]], list[str]]:
    notes: list[str] = []
    rosters: dict[str, dict[str, set[str]]] = {}
    for edition in sorted(editions):
        if not re.match(r"^\d{4}-\d{2}$", edition):
            continue
        edition_us = format_edition_underscore(edition)
        blocks_path = blocks_dir / f"{edition_us}_program_blocks_v11.json"
        text_path = texts_dir / f"catalog_{edition_us}.txt"
        if not blocks_path.exists() or not text_path.exists():
            notes.append(
                f"Missing source file(s) for edition {edition}: "
                f"{blocks_path.name if not blocks_path.exists() else ''} "
                f"{text_path.name if not text_path.exists() else ''}".strip()
            )
            rosters[edition] = {}
            continue

        blocks = json.loads(blocks_path.read_text(encoding="utf-8"))
        lines = text_path.read_text(encoding="utf-8", errors="replace").splitlines()
        edition_rosters: dict[str, set[str]] = {}
        for block in blocks:
            code = (block.get("code") or "").strip().upper()
            if not code:
                continue
            ccn_idx = int(block.get("ccn_idx", 0))
            end_idx = int(block.get("end", 0))
            roster = parse_program_roster(lines, ccn_idx, end_idx, valid_course_codes)
            edition_rosters[code] = roster
        rosters[edition] = edition_rosters

    return rosters, notes


def pair_metrics(
    old_set: set[str],
    new_set: set[str],
) -> tuple[dict, list[str], list[str]]:
    shared = sorted(old_set & new_set)
    removed_only = sorted(old_set - new_set)
    added_only = sorted(new_set - old_set)

    old_count = len(old_set)
    new_count = len(new_set)
    shared_count = len(shared)
    union_count = len(old_set | new_set)

    old_retained_pct = round(shared_count / old_count, 4) if old_count else 0.0
    new_inherited_pct = round(shared_count / new_count, 4) if new_count else 0.0
    jaccard_overlap = round(shared_count / union_count, 4) if union_count else 0.0

    metrics = {
        "shared_course_count": shared_count,
        "removed_course_count": len(removed_only),
        "added_course_count": len(added_only),
        "old_retained_pct": old_retained_pct,
        "new_inherited_pct": new_inherited_pct,
        "jaccard_overlap": jaccard_overlap,
    }
    return metrics, removed_only, added_only


def build_pair_output(
    from_program: ProgramRef,
    to_program: ProgramRef,
    start_edition: str,
    end_edition: str,
    rosters_by_edition: dict[str, dict[str, set[str]]],
) -> dict:
    old_set = set(rosters_by_edition.get(start_edition, {}).get(from_program.program_code, set()))
    new_set = set(rosters_by_edition.get(end_edition, {}).get(to_program.program_code, set()))
    metrics, removed_only, added_only = pair_metrics(old_set, new_set)
    return {
        "from_program": from_program.program_code,
        "to_program": to_program.program_code,
        "metrics": metrics,
        "courses_removed": removed_only,
        "courses_added": added_only,
    }


def candidate_pair_score(
    from_program: ProgramRef,
    to_program: ProgramRef,
    start_edition: str,
    end_edition: str,
    rosters_by_edition: dict[str, dict[str, set[str]]],
) -> tuple[float, dict]:
    pair = build_pair_output(from_program, to_program, start_edition, end_edition, rosters_by_edition)
    m = pair["metrics"]
    title_sim = title_similarity(from_program.title, to_program.title)
    code_sim = SequenceMatcher(None, from_program.program_code, to_program.program_code).ratio()
    score = (
        m["jaccard_overlap"] * 5.0
        + m["old_retained_pct"] * 2.0
        + m["new_inherited_pct"] * 2.0
        + min(m["shared_course_count"] / 10.0, 1.0)
        + title_sim
        + (code_sim * 0.25)
    )
    plausible = (
        m["shared_course_count"] >= 3
        or m["jaccard_overlap"] >= 0.05
        or title_sim >= 0.20
        or code_sim >= 0.70
    )
    pair["_score"] = round(score, 6)
    pair["_plausible"] = plausible
    return score, pair


def select_likely_pairs(
    from_programs: list[ProgramRef],
    to_programs: list[ProgramRef],
    start_edition: str,
    end_edition: str,
    rosters_by_edition: dict[str, dict[str, set[str]]],
    force_one: bool = False,
) -> list[dict]:
    scored: list[tuple[float, dict]] = []
    for fp in from_programs:
        for tp in to_programs:
            score, pair = candidate_pair_score(fp, tp, start_edition, end_edition, rosters_by_edition)
            if pair["_plausible"]:
                scored.append((score, pair))

    if not scored and force_one and from_programs and to_programs:
        for fp in from_programs:
            for tp in to_programs:
                score, pair = candidate_pair_score(fp, tp, start_edition, end_edition, rosters_by_edition)
                scored.append((score, pair))

    if not scored:
        return []

    scored.sort(
        key=lambda item: (
            item[0],
            item[1]["from_program"],
            item[1]["to_program"],
        ),
        reverse=True,
    )

    best_by_from: dict[str, tuple[float, dict]] = {}
    best_by_to: dict[str, tuple[float, dict]] = {}
    for score, pair in scored:
        best_by_from.setdefault(pair["from_program"], (score, pair))
        best_by_to.setdefault(pair["to_program"], (score, pair))

    selected: dict[tuple[str, str], dict] = {}
    for _, pair in best_by_from.values():
        selected[(pair["from_program"], pair["to_program"])] = pair
    for _, pair in best_by_to.values():
        selected[(pair["from_program"], pair["to_program"])] = pair

    output = list(selected.values())
    output.sort(
        key=lambda pair: (
            pair["_score"],
            pair["from_program"],
            pair["to_program"],
        ),
        reverse=True,
    )
    for pair in output:
        pair.pop("_score", None)
        pair.pop("_plausible", None)
    return output


def to_program_refs(raw_programs: Iterable[dict]) -> list[ProgramRef]:
    refs: list[ProgramRef] = []
    for item in raw_programs:
        code = (item.get("program_code") or "").strip().upper()
        if not code:
            continue
        refs.append(ProgramRef(program_code=code, title=(item.get("title") or "").strip()))
    return refs


def compare_event_pairs(
    event: dict,
    rosters_by_edition: dict[str, dict[str, set[str]]],
) -> list[dict]:
    start_edition = (event.get("start_edition") or "").strip()
    end_edition = (event.get("end_edition") or "").strip()
    transition_type = (event.get("transition_type") or "ambiguous").strip().lower()
    from_programs = to_program_refs(event.get("from_programs", []))
    to_programs = to_program_refs(event.get("to_programs", []))

    if not from_programs or not to_programs:
        return []

    pairs: list[dict] = []
    if transition_type in {"successor", "namespace_migration"}:
        if len(from_programs) == 1 and len(to_programs) == 1:
            pairs = [
                build_pair_output(
                    from_programs[0],
                    to_programs[0],
                    start_edition,
                    end_edition,
                    rosters_by_edition,
                )
            ]
        else:
            pairs = select_likely_pairs(
                from_programs,
                to_programs,
                start_edition,
                end_edition,
                rosters_by_edition,
                force_one=True,
            )
    elif transition_type == "split":
        if len(from_programs) == 1:
            source = from_programs[0]
            pairs = [
                build_pair_output(source, tp, start_edition, end_edition, rosters_by_edition)
                for tp in to_programs
            ]
        else:
            pairs = select_likely_pairs(
                from_programs,
                to_programs,
                start_edition,
                end_edition,
                rosters_by_edition,
                force_one=True,
            )
    elif transition_type == "merge":
        if len(to_programs) == 1:
            target = to_programs[0]
            pairs = [
                build_pair_output(fp, target, start_edition, end_edition, rosters_by_edition)
                for fp in from_programs
            ]
        else:
            pairs = select_likely_pairs(
                from_programs,
                to_programs,
                start_edition,
                end_edition,
                rosters_by_edition,
                force_one=True,
            )
    elif transition_type == "family_restructure":
        pairs = select_likely_pairs(
            from_programs,
            to_programs,
            start_edition,
            end_edition,
            rosters_by_edition,
            force_one=False,
        )
    else:
        pairs = select_likely_pairs(
            from_programs,
            to_programs,
            start_edition,
            end_edition,
            rosters_by_edition,
            force_one=len(from_programs) == 1 and len(to_programs) == 1,
        )

    return pairs


def main() -> None:
    args = parse_args()

    requested_input = Path(args.input)
    normalized_output = Path(args.normalized_output)
    canonical_courses_path = Path(args.canonical_courses)
    output_path = Path(args.output)
    catalog_root = Path(args.catalog_root)

    source_path, source_notes = resolve_input_path(requested_input)
    events_payload, normalization_applied, normalization_notes = load_events_with_normalization(source_path)

    normalized_output.parent.mkdir(parents=True, exist_ok=True)
    normalized_output.write_text(
        json.dumps(events_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    events = events_payload.get("events", [])
    valid_course_codes = load_valid_course_codes(canonical_courses_path)
    blocks_dir, texts_dir = ensure_catalog_sources(catalog_root)

    needed_editions: set[str] = set()
    for event in events:
        start = (event.get("start_edition") or "").strip()
        end = (event.get("end_edition") or "").strip()
        if re.match(r"^\d{4}-\d{2}$", start):
            needed_editions.add(start)
        if re.match(r"^\d{4}-\d{2}$", end):
            needed_editions.add(end)

    rosters_by_edition, roster_notes = build_rosters_by_edition(
        editions=needed_editions,
        blocks_dir=blocks_dir,
        texts_dir=texts_dir,
        valid_course_codes=valid_course_codes,
    )

    output_events: list[dict] = []
    missing_pair_rosters = 0
    for event in events:
        pairs = compare_event_pairs(event, rosters_by_edition)
        for pair in pairs:
            old_roster_empty = len(pair["courses_removed"]) + pair["metrics"]["shared_course_count"] == 0
            new_roster_empty = len(pair["courses_added"]) + pair["metrics"]["shared_course_count"] == 0
            if old_roster_empty or new_roster_empty:
                missing_pair_rosters += 1

        output_events.append(
            {
                "event_id": event.get("event_id"),
                "transition_type": event.get("transition_type"),
                "start_edition": event.get("start_edition"),
                "end_edition": event.get("end_edition"),
                "pairs": pairs,
            }
        )

    edge_case_notes: list[str] = []
    edge_case_notes.extend(source_notes)
    edge_case_notes.extend(normalization_notes)
    edge_case_notes.extend(roster_notes)
    if missing_pair_rosters:
        edge_case_notes.append(
            f"{missing_pair_rosters} pair comparison(s) had an empty old or new roster."
        )

    enriched = {
        "metadata": {
            "generated_from": str(requested_input),
            "source_file_used": str(source_path),
            "normalized_input": str(normalized_output),
            "normalization_applied": normalization_applied,
            "catalog_root": str(catalog_root),
            "events_in_input": len(events),
            "events_out": len(output_events),
            "edge_case_notes": edge_case_notes,
        },
        "events": output_events,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(enriched, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote normalized input: {normalized_output}")
    print(f"Wrote enriched output: {output_path}")
    print(f"Events processed: {len(events)}")
    print(f"Edge-case notes: {len(edge_case_notes)}")


if __name__ == "__main__":
    main()
