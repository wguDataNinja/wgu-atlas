#!/usr/bin/env python3
"""
build_program_lineage_artifacts.py
==================================
Builds lineage review artifacts for WGU Atlas.

Artifacts:
  1) data/program_transition_universe.csv
  2) data/program_link_candidates.json

Design:
  - Full historical backfill by default
  - Optional incremental filter via --baseline-end-edition
  - Course overlap is a first-class signal using:
      * removed program roster at boundary start_edition (last roster)
      * added program roster at boundary end_edition (first roster)
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


DEFAULT_START_EDITION = "2017-01"
DEFAULT_END_EDITION = "2026-03"
DEFAULT_MISSING_EDITIONS = {"2017-02", "2017-04", "2017-06"}
DEFAULT_CATALOG_ROOT = "/Users/buddy/Desktop/WGU-Reddit/WGU_catalog"

STOPWORDS = {
    "a",
    "and",
    "arts",
    "bachelor",
    "certificate",
    "degree",
    "engineering",
    "in",
    "management",
    "master",
    "masters",
    "of",
    "program",
    "science",
    "specialization",
    "the",
    "to",
}

DEGREE_PREFIXES = ("bs", "ba", "ms", "ma", "mba", "med", "msn", "phd", "edd")

COURSE_ROW_FULL_RE = re.compile(
    r"^[A-Z]{2,5}\s+\d{1,4}[A-Z]?\s+([A-Z][A-Z0-9]{1,5})\s+.+\s+\d+\s+\d+\s*$"
)
COURSE_ROW_CODE_ONLY_RE = re.compile(
    r"^([A-Z][A-Z0-9]{1,5})\s+.+\s+\d+\s+\d+\s*$"
)


@dataclass(frozen=True)
class ProgramEntry:
    code: str
    status: str
    first_seen: str
    last_seen: str
    primary_heading: str
    headings: tuple[str, ...]
    colleges: tuple[str, ...]
    cu_values: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build program lineage artifacts")
    parser.add_argument(
        "--program-history",
        default="data/program_history.csv",
        help="Path to program_history.csv",
    )
    parser.add_argument(
        "--canonical-courses",
        default="data/canonical_courses.csv",
        help="Path to canonical_courses.csv (used to validate course codes)",
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
        "--out-transition",
        default="data/lineage/program_transition_universe.csv",
        help="Output CSV path for exhaustive adjacent transitions",
    )
    parser.add_argument(
        "--out-candidates",
        default="data/lineage/program_link_candidates.json",
        help="Output JSON path for link candidates",
    )
    parser.add_argument(
        "--start-edition",
        default=DEFAULT_START_EDITION,
        help="First edition to include (YYYY-MM)",
    )
    parser.add_argument(
        "--end-edition",
        default=DEFAULT_END_EDITION,
        help="Last edition to include (YYYY-MM)",
    )
    parser.add_argument(
        "--missing-editions",
        default=",".join(sorted(DEFAULT_MISSING_EDITIONS)),
        help="Comma-separated editions to exclude from the monthly sequence",
    )
    parser.add_argument(
        "--baseline-end-edition",
        default="",
        help=(
            "Optional incremental cutoff. If set, only boundaries with "
            "end_edition > baseline are emitted."
        ),
    )
    return parser.parse_args()


def split_pipe_list(raw: str) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split("|") if part.strip()]


def parse_edition(edition: str) -> tuple[int, int]:
    year_s, month_s = edition.split("-")
    year = int(year_s)
    month = int(month_s)
    if month < 1 or month > 12:
        raise ValueError(f"Invalid edition month: {edition}")
    return year, month


def format_edition(year: int, month: int) -> str:
    return f"{year:04d}-{month:02d}"


def format_edition_underscore(edition: str) -> str:
    year, month = parse_edition(edition)
    return f"{year:04d}_{month:02d}"


def month_iter(start_edition: str, end_edition: str) -> Iterable[str]:
    sy, sm = parse_edition(start_edition)
    ey, em = parse_edition(end_edition)
    y, m = sy, sm
    while (y < ey) or (y == ey and m <= em):
        yield format_edition(y, m)
        m += 1
        if m == 13:
            y += 1
            m = 1


def normalize_school_college(name: str) -> str:
    s = (name or "").strip().lower()
    s = s.replace("college of ", "")
    s = s.replace("school of ", "")
    return re.sub(r"\s+", " ", s).strip()


def parse_cu_values(raw_values: Iterable[str]) -> set[int]:
    values: set[int] = set()
    for raw in raw_values:
        for match in re.findall(r"\d+", raw):
            values.add(int(match))
    return values


def normalize_text(value: str) -> str:
    s = value.lower()
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


def get_degree_level(heading: str) -> str:
    normalized = normalize_text(heading)
    token0 = normalized.split(" ", 1)[0] if normalized else ""
    if token0 in DEGREE_PREFIXES:
        return token0
    if "bachelor" in normalized:
        return "bachelor"
    if "master" in normalized:
        return "master"
    if "certificate" in normalized:
        return "certificate"
    return "other"


def heading_similarity(headings_a: Iterable[str], headings_b: Iterable[str]) -> tuple[float, set[str]]:
    tokens_a = set().union(*(tokenize(h) for h in headings_a)) if headings_a else set()
    tokens_b = set().union(*(tokenize(h) for h in headings_b)) if headings_b else set()
    union = tokens_a | tokens_b
    if not union:
        return 0.0, set()
    overlap = tokens_a & tokens_b
    return len(overlap) / len(union), overlap


def primary_heading_similarity(a: str, b: str) -> tuple[float, set[str]]:
    tokens_a = tokenize(a)
    tokens_b = tokenize(b)
    union = tokens_a | tokens_b
    if not union:
        return 0.0, set()
    overlap = tokens_a & tokens_b
    return len(overlap) / len(union), overlap


def code_alpha_prefix(code: str) -> str:
    return re.sub(r"[^A-Z]+", "", code.upper())


def common_prefix_len(a: str, b: str) -> int:
    length = 0
    for ca, cb in zip(a, b):
        if ca != cb:
            break
        length += 1
    return length


def csv_write(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def json_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def load_program_history(path: Path) -> dict[str, ProgramEntry]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        output: dict[str, ProgramEntry] = {}
        for row in reader:
            code = (row.get("program_code") or "").strip()
            if not code:
                continue
            headings = split_pipe_list(row.get("degree_headings", ""))
            primary = headings[0] if headings else code
            output[code] = ProgramEntry(
                code=code,
                status=(row.get("status") or "").strip(),
                first_seen=(row.get("first_seen") or "").strip(),
                last_seen=(row.get("last_seen") or "").strip(),
                primary_heading=primary,
                headings=tuple(headings),
                colleges=tuple(split_pipe_list(row.get("colleges", ""))),
                cu_values=tuple(split_pipe_list(row.get("cus_values", ""))),
            )
    return output


def load_valid_course_codes(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return {
            (row.get("course_code") or "").strip().upper()
            for row in reader
            if (row.get("course_code") or "").strip()
        }


def build_edition_sequence(
    start_edition: str,
    end_edition: str,
    missing_editions: set[str],
) -> list[str]:
    all_months = list(month_iter(start_edition, end_edition))
    return [edition for edition in all_months if edition not in missing_editions]


def build_transition_rows(
    programs: dict[str, ProgramEntry],
    editions: list[str],
    baseline_end_edition: str,
) -> list[dict]:
    rows: list[dict] = []
    for idx in range(len(editions) - 1):
        start_edition = editions[idx]
        end_edition = editions[idx + 1]
        if baseline_end_edition and end_edition <= baseline_end_edition:
            continue

        removed_codes = sorted(
            code for code, entry in programs.items() if entry.last_seen == start_edition
        )
        added_codes = sorted(
            code for code, entry in programs.items() if entry.first_seen == end_edition
        )
        removed_titles = [
            f"{code}: {programs[code].primary_heading}" for code in removed_codes
        ]
        added_titles = [f"{code}: {programs[code].primary_heading}" for code in added_codes]
        removed_colleges = sorted(
            {
                college
                for code in removed_codes
                for college in programs[code].colleges
                if college.strip()
            }
        )
        added_colleges = sorted(
            {
                college
                for code in added_codes
                for college in programs[code].colleges
                if college.strip()
            }
        )
        removed_cus_values = sorted(
            {
                value
                for code in removed_codes
                for value in programs[code].cu_values
                if value.strip()
            },
            key=lambda value: int(re.search(r"\d+", value).group()) if re.search(r"\d+", value) else 9999,
        )
        added_cus_values = sorted(
            {
                value
                for code in added_codes
                for value in programs[code].cu_values
                if value.strip()
            },
            key=lambda value: int(re.search(r"\d+", value).group()) if re.search(r"\d+", value) else 9999,
        )

        total_churn = len(removed_codes) + len(added_codes)
        rows.append(
            {
                "boundary_index": idx + 1,
                "start_edition": start_edition,
                "end_edition": end_edition,
                "programs_removed_count": len(removed_codes),
                "programs_added_count": len(added_codes),
                "programs_removed": " | ".join(removed_codes),
                "programs_added": " | ".join(added_codes),
                "removed_titles": " | ".join(removed_titles),
                "added_titles": " | ".join(added_titles),
                "removed_colleges": " | ".join(removed_colleges),
                "added_colleges": " | ".join(added_colleges),
                "removed_cus_values": " | ".join(removed_cus_values),
                "added_cus_values": " | ".join(added_cus_values),
                "total_program_churn": total_churn,
                "net_program_delta": len(added_codes) - len(removed_codes),
                "has_churn": "yes" if total_churn > 0 else "no",
            }
        )
    return rows


def ensure_catalog_sources(catalog_root: Path) -> tuple[Path, Path]:
    blocks_dir = catalog_root / "outputs" / "program_names"
    texts_dir = catalog_root / "data" / "raw_catalog_texts"
    if not blocks_dir.exists():
        raise FileNotFoundError(f"Missing program blocks directory: {blocks_dir}")
    if not texts_dir.exists():
        raise FileNotFoundError(f"Missing raw catalog text directory: {texts_dir}")
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
        if code.startswith("ENDS"):
            continue
        if valid_course_codes and code not in valid_course_codes:
            continue
        roster.add(code)
    return roster


def build_program_rosters_by_edition(
    needed_editions: set[str],
    blocks_dir: Path,
    texts_dir: Path,
    valid_course_codes: set[str],
) -> dict[str, dict[str, set[str]]]:
    rosters: dict[str, dict[str, set[str]]] = {}
    for edition in sorted(needed_editions):
        edition_us = format_edition_underscore(edition)
        blocks_path = blocks_dir / f"{edition_us}_program_blocks_v11.json"
        text_path = texts_dir / f"catalog_{edition_us}.txt"
        if not blocks_path.exists() or not text_path.exists():
            rosters[edition] = {}
            continue

        blocks = json.loads(blocks_path.read_text(encoding="utf-8"))
        lines = text_path.read_text(encoding="utf-8", errors="replace").splitlines()
        edition_rosters: dict[str, set[str]] = {}
        for block in blocks:
            code = (block.get("code") or "").strip()
            if not code:
                continue
            ccn_idx = int(block.get("ccn_idx", 0))
            end_idx = int(block.get("end", 0))
            roster = parse_program_roster(lines, ccn_idx, end_idx, valid_course_codes)
            edition_rosters[code] = roster
        rosters[edition] = edition_rosters
    return rosters


def overlap_metrics_from_sets(removed_set: set[str], added_set: set[str]) -> dict:
    shared = sorted(removed_set & added_set)
    removed_only = sorted(removed_set - added_set)
    added_only = sorted(added_set - removed_set)
    removed_count = len(removed_set)
    added_count = len(added_set)
    shared_count = len(shared)
    union_count = len(removed_set | added_set)

    old_retained_pct = round((shared_count / removed_count), 4) if removed_count else 0.0
    new_inherited_pct = round((shared_count / added_count), 4) if added_count else 0.0
    jaccard_overlap = round((shared_count / union_count), 4) if union_count else 0.0

    return {
        "removed_course_count": removed_count,
        "added_program_course_count": added_count,
        "shared_course_count": shared_count,
        "courses_removed_count": len(removed_only),
        "courses_added_count": len(added_only),
        "old_retained_pct": old_retained_pct,
        "new_inherited_pct": new_inherited_pct,
        "jaccard_overlap": jaccard_overlap,
        "shared_course_codes": shared,
        "removed_only_course_codes": removed_only,
        "added_only_course_codes": added_only,
    }


def compute_overlap_metrics(
    removed_codes: Iterable[str],
    added_codes: Iterable[str],
    start_edition: str,
    end_edition: str,
    rosters: dict[str, dict[str, set[str]]],
) -> dict:
    removed_union: set[str] = set()
    added_union: set[str] = set()
    start_rosters = rosters.get(start_edition, {})
    end_rosters = rosters.get(end_edition, {})

    for code in removed_codes:
        removed_union |= set(start_rosters.get(code, set()))
    for code in added_codes:
        added_union |= set(end_rosters.get(code, set()))
    return overlap_metrics_from_sets(removed_union, added_union)


def summarize_college_overlap(removed: ProgramEntry, added: ProgramEntry) -> tuple[bool, str]:
    removed_norm = {normalize_school_college(name) for name in removed.colleges if name.strip()}
    added_norm = {normalize_school_college(name) for name in added.colleges if name.strip()}
    overlap = sorted(removed_norm & added_norm)
    if overlap:
        return True, f"shared_college_or_school={', '.join(overlap)}"
    return False, "shared_college_or_school=none"


def summarize_cu_overlap(removed: ProgramEntry, added: ProgramEntry) -> tuple[bool, str]:
    removed_cus = parse_cu_values(removed.cu_values)
    added_cus = parse_cu_values(added.cu_values)
    overlap = sorted(removed_cus & added_cus)
    if overlap:
        return True, f"overlap={overlap}"
    return False, f"removed={sorted(removed_cus)}; added={sorted(added_cus)}"


def guess_group_pattern(removed_count: int, added_count: int, overlap: dict) -> str:
    if removed_count == 1 and added_count > 1:
        return "split"
    if removed_count > 1 and added_count == 1:
        return "merge"
    if removed_count > 0 and added_count > 0:
        if overlap["shared_course_count"] >= 8 or overlap["jaccard_overlap"] >= 0.15:
            return "family_restructure"
        if overlap["shared_course_count"] > 0:
            return "namespace_migration"
        return "ambiguous"
    return "ambiguous"


def guess_pair_transition(
    overlap: dict,
    heading_jaccard: float,
    primary_jaccard: float,
    code_similarity: float,
    shared_college: bool,
    same_degree_level: bool,
) -> str:
    if overlap["jaccard_overlap"] >= 0.25 or (
        overlap["old_retained_pct"] >= 0.55 and overlap["new_inherited_pct"] >= 0.45
    ):
        return "successor"
    if code_similarity >= 0.75 and (shared_college or overlap["shared_course_count"] >= 2):
        return "namespace_migration"
    if overlap["shared_course_count"] >= 4 and same_degree_level:
        return "family_restructure"
    if heading_jaccard >= 0.22 or primary_jaccard >= 0.22:
        return "family_restructure"
    if shared_college:
        return "family_restructure"
    return "ambiguous"


def confidence_from_score(score: float) -> str:
    if score >= 5.0:
        return "high"
    if score >= 3.0:
        return "medium"
    return "low"


def pair_plausibility(
    overlap: dict,
    heading_jaccard: float,
    primary_jaccard: float,
    code_similarity: float,
    shared_college: bool,
    removed_code: str,
    added_code: str,
) -> bool:
    overlap_signal = (
        overlap["shared_course_count"] >= 4
        or overlap["jaccard_overlap"] >= 0.08
        or overlap["old_retained_pct"] >= 0.15
        or overlap["new_inherited_pct"] >= 0.15
    )
    title_signal = heading_jaccard >= 0.18 or primary_jaccard >= 0.22
    alpha_prefix_removed = code_alpha_prefix(removed_code)
    alpha_prefix_added = code_alpha_prefix(added_code)
    family_signal = (
        code_similarity >= 0.65
        or common_prefix_len(alpha_prefix_removed, alpha_prefix_added) >= 3
    )
    return shared_college or title_signal or overlap_signal or family_signal


def pair_score(
    overlap: dict,
    heading_jaccard: float,
    code_similarity: float,
    shared_college: bool,
) -> float:
    score = 0.0
    if overlap["shared_course_count"] >= 8:
        score += 3.0
    elif overlap["shared_course_count"] >= 4:
        score += 2.0
    elif overlap["shared_course_count"] > 0:
        score += 1.0

    if overlap["jaccard_overlap"] >= 0.30:
        score += 2.0
    elif overlap["jaccard_overlap"] >= 0.10:
        score += 1.0

    if shared_college:
        score += 1.5
    if heading_jaccard >= 0.30:
        score += 1.0
    elif heading_jaccard >= 0.15:
        score += 0.5

    if code_similarity >= 0.75:
        score += 1.0
    elif code_similarity >= 0.60:
        score += 0.5
    return score


def build_boundary_reviews(
    transition_rows: list[dict],
    programs: dict[str, ProgramEntry],
    rosters: dict[str, dict[str, set[str]]],
) -> list[dict]:
    reviews: list[dict] = []
    for row in transition_rows:
        if row["has_churn"] != "yes":
            continue

        start_edition = row["start_edition"]
        end_edition = row["end_edition"]
        removed_codes = split_pipe_list(row["programs_removed"])
        added_codes = split_pipe_list(row["programs_added"])
        overlap = compute_overlap_metrics(removed_codes, added_codes, start_edition, end_edition, rosters)
        pattern_guess = guess_group_pattern(len(removed_codes), len(added_codes), overlap)

        if overlap["shared_course_count"] >= 8:
            review_priority = "high"
        elif overlap["shared_course_count"] >= 2 or (removed_codes and added_codes):
            review_priority = "medium"
        else:
            review_priority = "low"

        removed_programs = [
            {
                "program_code": code,
                "title": programs[code].primary_heading,
                "course_count": len(rosters.get(start_edition, {}).get(code, set())),
            }
            for code in removed_codes
        ]
        added_programs = [
            {
                "program_code": code,
                "title": programs[code].primary_heading,
                "course_count": len(rosters.get(end_edition, {}).get(code, set())),
            }
            for code in added_codes
        ]

        reviews.append(
            {
                "boundary_id": f"PLB-{start_edition.replace('-', '')}-{end_edition.replace('-', '')}",
                "start_edition": start_edition,
                "end_edition": end_edition,
                "removed_programs": removed_programs,
                "added_programs": added_programs,
                "pattern_guess": pattern_guess,
                "review_priority": review_priority,
                "notes": (
                    f"Boundary churn removed={len(removed_codes)}, added={len(added_codes)}, "
                    f"shared_courses={overlap['shared_course_count']}, "
                    f"jaccard={overlap['jaccard_overlap']:.2f}."
                ),
            }
        )
    return reviews


def build_candidates(
    transition_rows: list[dict],
    programs: dict[str, ProgramEntry],
    rosters: dict[str, dict[str, set[str]]],
) -> list[dict]:
    candidates: list[dict] = []
    candidate_index = 1

    def next_candidate_id(start: str, end: str) -> str:
        nonlocal candidate_index
        cid = f"PLC-{start.replace('-', '')}-{end.replace('-', '')}-{candidate_index:04d}"
        candidate_index += 1
        return cid

    for row in transition_rows:
        if row["has_churn"] != "yes":
            continue

        start_edition = row["start_edition"]
        end_edition = row["end_edition"]
        removed_codes = split_pipe_list(row["programs_removed"])
        added_codes = split_pipe_list(row["programs_added"])

        if removed_codes and added_codes and (len(removed_codes) > 1 or len(added_codes) > 1):
            group_overlap = compute_overlap_metrics(
                removed_codes,
                added_codes,
                start_edition,
                end_edition,
                rosters,
            )
            title_jaccard, title_overlap = heading_similarity(
                [programs[c].primary_heading for c in removed_codes],
                [programs[c].primary_heading for c in added_codes],
            )
            group_plausible = (
                group_overlap["shared_course_count"] >= 5
                or group_overlap["jaccard_overlap"] >= 0.05
                or title_jaccard >= 0.20
            )
            if group_plausible:
                transition_guess = guess_group_pattern(
                    len(removed_codes), len(added_codes), group_overlap
                )
                score = (
                    group_overlap["jaccard_overlap"] * 10.0
                    + min(group_overlap["shared_course_count"] / 4.0, 3.0)
                    + (1.0 if title_jaccard >= 0.20 else 0.0)
                )
                candidates.append(
                    {
                        "candidate_id": next_candidate_id(start_edition, end_edition),
                        "transition_type_guess": transition_guess,
                        "confidence_guess": confidence_from_score(score),
                        "start_edition": start_edition,
                        "end_edition": end_edition,
                        "removed_programs": [
                            {
                                "program_code": code,
                                "title": programs[code].primary_heading,
                                "course_count": len(rosters.get(start_edition, {}).get(code, set())),
                            }
                            for code in removed_codes
                        ],
                        "added_programs": [
                            {
                                "program_code": code,
                                "title": programs[code].primary_heading,
                                "course_count": len(rosters.get(end_edition, {}).get(code, set())),
                            }
                            for code in added_codes
                        ],
                        "same_college_or_school_signal": (
                            f"removed_colleges={row['removed_colleges'] or 'none'}; "
                            f"added_colleges={row['added_colleges'] or 'none'}"
                        ),
                        "title_similarity_notes": (
                            f"group_heading_jaccard={title_jaccard:.2f}; "
                            f"shared_tokens={sorted(title_overlap)}"
                        ),
                        "degree_heading_similarity_notes": (
                            "Group-level candidate across adjacent boundary with multi-program churn."
                        ),
                        "cu_similarity_notes": (
                            f"removed_cus={row['removed_cus_values'] or 'none'}; "
                            f"added_cus={row['added_cus_values'] or 'none'}"
                        ),
                        "adjacency_notes": (
                            f"Removed in {start_edition} and added in adjacent {end_edition}."
                        ),
                        "overlap_metrics": group_overlap,
                        "rationale": (
                            f"This boundary appears to show a {transition_guess} pattern with "
                            "course overlap evidence across removed/added program groups."
                        ),
                        "review_status": "unreviewed",
                    }
                )

        scored_pairs: list[dict] = []
        for removed_code in removed_codes:
            for added_code in added_codes:
                removed = programs[removed_code]
                added = programs[added_code]
                overlap = compute_overlap_metrics(
                    [removed_code],
                    [added_code],
                    start_edition,
                    end_edition,
                    rosters,
                )
                primary_jaccard, primary_overlap = primary_heading_similarity(
                    removed.primary_heading, added.primary_heading
                )
                heading_jaccard, heading_overlap = heading_similarity(
                    removed.headings, added.headings
                )
                code_similarity = SequenceMatcher(None, removed_code, added_code).ratio()
                shared_college, college_note = summarize_college_overlap(removed, added)
                shared_cu, cu_note = summarize_cu_overlap(removed, added)
                same_degree_level = get_degree_level(removed.primary_heading) == get_degree_level(
                    added.primary_heading
                )

                if not pair_plausibility(
                    overlap=overlap,
                    heading_jaccard=heading_jaccard,
                    primary_jaccard=primary_jaccard,
                    code_similarity=code_similarity,
                    shared_college=shared_college,
                    removed_code=removed_code,
                    added_code=added_code,
                ):
                    continue

                transition_guess = guess_pair_transition(
                    overlap=overlap,
                    heading_jaccard=heading_jaccard,
                    primary_jaccard=primary_jaccard,
                    code_similarity=code_similarity,
                    shared_college=shared_college,
                    same_degree_level=same_degree_level,
                )
                score = pair_score(
                    overlap=overlap,
                    heading_jaccard=heading_jaccard,
                    code_similarity=code_similarity,
                    shared_college=shared_college,
                )
                confidence_guess = confidence_from_score(score)

                scored_pairs.append(
                    {
                        "removed_code": removed_code,
                        "added_code": added_code,
                        "score": score,
                        "payload": {
                            "candidate_id": "",
                            "transition_type_guess": transition_guess,
                            "confidence_guess": confidence_guess,
                            "start_edition": start_edition,
                            "end_edition": end_edition,
                            "removed_programs": [
                                {
                                    "program_code": removed_code,
                                    "title": removed.primary_heading,
                                    "course_count": len(rosters.get(start_edition, {}).get(removed_code, set())),
                                }
                            ],
                            "added_programs": [
                                {
                                    "program_code": added_code,
                                    "title": added.primary_heading,
                                    "course_count": len(rosters.get(end_edition, {}).get(added_code, set())),
                                }
                            ],
                            "same_college_or_school_signal": college_note,
                            "title_similarity_notes": (
                                f"primary_heading_jaccard={primary_jaccard:.2f}; "
                                f"shared_tokens={sorted(primary_overlap)}"
                            ),
                            "degree_heading_similarity_notes": (
                                f"all_headings_jaccard={heading_jaccard:.2f}; "
                                f"shared_heading_tokens={sorted(heading_overlap)}; "
                                f"degree_level_match={same_degree_level}"
                            ),
                            "cu_similarity_notes": cu_note,
                            "adjacency_notes": (
                                f"Removed in {start_edition}, added in immediately adjacent {end_edition}."
                            ),
                            "overlap_metrics": overlap,
                            "rationale": (
                                f"{removed_code} appears to "
                                f"{'replace' if transition_guess in ('successor', 'namespace_migration') else 'relate to'} "
                                f"{added_code} based on adjacent timing, course overlap, and program-family signals."
                            ),
                            "review_status": "unreviewed",
                        },
                    }
                )

        scored_pairs.sort(key=lambda item: item["score"], reverse=True)
        per_removed_limit = 2
        per_added_limit = 2
        total_limit = max(6, min(16, len(removed_codes) + len(added_codes)))
        removed_counts: dict[str, int] = {}
        added_counts: dict[str, int] = {}
        selected_pairs: list[dict] = []

        for item in scored_pairs:
            if len(selected_pairs) >= total_limit:
                break
            removed_code = item["removed_code"]
            added_code = item["added_code"]
            if removed_counts.get(removed_code, 0) >= per_removed_limit:
                continue
            if added_counts.get(added_code, 0) >= per_added_limit:
                continue
            removed_counts[removed_code] = removed_counts.get(removed_code, 0) + 1
            added_counts[added_code] = added_counts.get(added_code, 0) + 1
            selected_pairs.append(item)

        # Ensure each removed/added gets at least one plausible pairing if available.
        best_by_removed: dict[str, dict] = {}
        best_by_added: dict[str, dict] = {}
        for item in scored_pairs:
            best_by_removed.setdefault(item["removed_code"], item)
            best_by_added.setdefault(item["added_code"], item)

        selected_keys = {
            (item["removed_code"], item["added_code"]) for item in selected_pairs
        }
        for removed_code, item in best_by_removed.items():
            key = (item["removed_code"], item["added_code"])
            if key in selected_keys:
                continue
            selected_pairs.append(item)
            selected_keys.add(key)

        for added_code, item in best_by_added.items():
            key = (item["removed_code"], item["added_code"])
            if key in selected_keys:
                continue
            selected_pairs.append(item)
            selected_keys.add(key)

        for item in selected_pairs:
            payload = item["payload"]
            payload["candidate_id"] = next_candidate_id(start_edition, end_edition)
            candidates.append(payload)

    return candidates


def main() -> None:
    args = parse_args()
    missing_editions = {part.strip() for part in args.missing_editions.split(",") if part.strip()}

    program_history_path = Path(args.program_history)
    canonical_courses_path = Path(args.canonical_courses)
    catalog_root = Path(args.catalog_root)
    out_transition_path = Path(args.out_transition)
    out_candidates_path = Path(args.out_candidates)

    programs = load_program_history(program_history_path)
    valid_course_codes = load_valid_course_codes(canonical_courses_path)
    blocks_dir, texts_dir = ensure_catalog_sources(catalog_root)

    editions = build_edition_sequence(
        args.start_edition,
        args.end_edition,
        missing_editions,
    )
    transition_rows = build_transition_rows(
        programs=programs,
        editions=editions,
        baseline_end_edition=args.baseline_end_edition.strip(),
    )

    needed_editions = {
        row["start_edition"]
        for row in transition_rows
    } | {
        row["end_edition"]
        for row in transition_rows
    }
    rosters_by_edition = build_program_rosters_by_edition(
        needed_editions=needed_editions,
        blocks_dir=blocks_dir,
        texts_dir=texts_dir,
        valid_course_codes=valid_course_codes,
    )

    transition_columns = [
        "boundary_index",
        "start_edition",
        "end_edition",
        "programs_removed_count",
        "programs_added_count",
        "programs_removed",
        "programs_added",
        "removed_titles",
        "added_titles",
        "removed_colleges",
        "added_colleges",
        "removed_cus_values",
        "added_cus_values",
        "total_program_churn",
        "net_program_delta",
        "has_churn",
    ]
    csv_write(out_transition_path, transition_rows, transition_columns)

    boundary_reviews = build_boundary_reviews(transition_rows, programs, rosters_by_edition)
    candidates = build_candidates(transition_rows, programs, rosters_by_edition)

    payload = {
        "metadata": {
            "source_program_history": str(program_history_path),
            "source_canonical_courses": str(canonical_courses_path),
            "catalog_root": str(catalog_root),
            "course_roster_sources": {
                "program_blocks_dir": str(blocks_dir),
                "raw_catalog_text_dir": str(texts_dir),
            },
            "start_edition": args.start_edition,
            "end_edition": args.end_edition,
            "missing_editions": sorted(missing_editions),
            "baseline_end_edition": args.baseline_end_edition.strip() or None,
            "transition_row_count": len(transition_rows),
            "boundary_review_count": len(boundary_reviews),
            "candidate_count": len(candidates),
            "notes": (
                "Review artifact with exhaustive boundary context plus plausible lineage "
                "candidates. Course overlap is computed from last-removed and first-added rosters."
            ),
        },
        "boundary_reviews": boundary_reviews,
        "candidates": candidates,
    }
    json_write(out_candidates_path, payload)

    print(f"Wrote {out_transition_path} ({len(transition_rows)} rows)")
    print(f"Wrote {out_candidates_path} ({len(boundary_reviews)} boundaries, {len(candidates)} candidates)")


if __name__ == "__main__":
    main()
