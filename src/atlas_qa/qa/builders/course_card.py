"""Builder for CourseCard canonical objects."""
from __future__ import annotations

import glob
import json
import os
from collections import defaultdict
from pathlib import Path

from ..source_authority import (
    get_version_conflict,
    is_cat_short_text,
    is_guide_misrouted,
)
from ..types import (
    CertPrepSignal,
    CompetencyVariant,
    CourseCard,
    EvidenceRef,
    GuideDescriptionAlternate,
    GuideEnrichmentSummary,
    InstancesByVersion,
    VersionConflictProgram,
)

# ---------------------------------------------------------------------------
# Repo root helper
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[4]  # …/wgu-atlas


def _data(relative: str) -> Path:
    return _REPO_ROOT / relative


# ---------------------------------------------------------------------------
# Data loaders (called once)
# ---------------------------------------------------------------------------


def _load_canonical_courses() -> dict:
    with open(_data("data/canonical_courses.json")) as f:
        return json.load(f)


def _load_course_descriptions() -> dict:
    with open(_data("public/data/course_descriptions.json")) as f:
        return json.load(f)


def _load_course_index() -> dict:
    with open(_data("data/catalog/trusted/2026_03/course_index_2026_03.json")) as f:
        return json.load(f)


def _load_program_blocks() -> list:
    with open(_data("data/catalog/trusted/2026_03/program_blocks_2026_03.json")) as f:
        return json.load(f)


def _load_enrichment_candidates() -> dict:
    """Return dict keyed by course_code from enrichment candidates list."""
    with open(_data("data/program_guides/enrichment/course_enrichment_candidates.json")) as f:
        raw = json.load(f)
    return {entry["course_code"]: entry for entry in raw["courses"]}


def _load_cert_mapping() -> dict[str, list[dict]]:
    """Return dict keyed by course_code → list of cert entries."""
    with open(_data("data/program_guides/cert_course_mapping.json")) as f:
        raw = json.load(f)
    lookup: dict[str, list[dict]] = defaultdict(list)
    for entry in raw.get("auto_accepted", []) + raw.get("review_needed", []):
        lookup[entry["matched_course_code"]].append(entry)
    return dict(lookup)


def _load_guide_versions() -> dict[str, str]:
    """Return dict {program_code: version_string} from all parsed guide files."""
    parsed_dir = _data("data/program_guides/parsed")
    versions: dict[str, str] = {}
    for filepath in glob.glob(str(parsed_dir / "*_parsed.json")):
        with open(filepath) as f:
            data = json.load(f)
        prog_code = data.get("program_code") or data.get("inferred_program_code", "")
        version = data.get("version") or ""
        if prog_code:
            versions[prog_code] = str(version) if version else "unknown"
    return versions


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_degree_to_program_code(program_blocks: list) -> dict[str, str]:
    return {block["degree"]: block["code"] for block in program_blocks}


def _get_title_variants(entry: dict) -> list[str]:
    if entry.get("title_variant_class", "none") == "none":
        return []
    raw = entry.get("observed_titles", "")
    if not raw:
        return []
    parts = [t.strip() for t in raw.split("|") if t.strip()]
    canonical = entry.get("canonical_title_current", "")
    return [p for p in parts if p != canonical]


def _build_cert_prep_signal(
    course_code: str,
    cert_lookup: dict[str, list[dict]],
    guide_versions: dict[str, str],
) -> CertPrepSignal:
    entries = cert_lookup.get(course_code, [])
    if not entries:
        return CertPrepSignal(
            status="not_found_in_observed_guides",
            label=None,
            guide_versions_observed=[],
        )
    # Aggregate cert labels and source guide versions
    labels = list({e["normalized_cert"] for e in entries})
    label_str = "; ".join(sorted(labels))
    observed_versions: list[str] = []
    for entry in entries:
        for prog in entry.get("source_programs", []):
            v = guide_versions.get(prog)
            if v and v not in observed_versions:
                observed_versions.append(v)
    return CertPrepSignal(
        status="present",
        label=label_str,
        guide_versions_observed=sorted(observed_versions),
    )


def _build_instances_by_version(
    instances: list[dict],
    degree_to_code: dict[str, str],
) -> list[InstancesByVersion]:
    """Group catalog instances by catalog_date, collect distinct program codes."""
    version_map: dict[str, set[str]] = defaultdict(set)
    for inst in instances:
        catalog_date = inst.get("catalog_date", "unknown")
        degree = inst.get("degree", "")
        prog_code = degree_to_code.get(degree)
        if prog_code:
            version_map[catalog_date].add(prog_code)
    return [
        InstancesByVersion(
            catalog_version=version,
            program_codes=sorted(codes),
        )
        for version, codes in sorted(version_map.items())
    ]


# ---------------------------------------------------------------------------
# Primary builder
# ---------------------------------------------------------------------------


def build_course_cards() -> dict[str, CourseCard]:
    """Build all CourseCard objects and return as dict keyed by course_code."""
    canonical_courses = _load_canonical_courses()
    course_descriptions = _load_course_descriptions()
    course_index = _load_course_index()
    program_blocks = _load_program_blocks()
    enrichment = _load_enrichment_candidates()
    cert_lookup = _load_cert_mapping()
    guide_versions = _load_guide_versions()

    degree_to_code = _build_degree_to_program_code(program_blocks)

    cards: dict[str, CourseCard] = {}

    for course_code, can_entry in canonical_courses.items():
        # --- Identity ---
        canonical_title = can_entry.get("canonical_title_current", "")
        canonical_cus = str(can_entry.get("canonical_cus", ""))
        title_variants = _get_title_variants(can_entry)

        # --- Catalog description ---
        desc_entry = course_descriptions.get(course_code)
        catalog_description: str | None = desc_entry["description"] if desc_entry else None
        catalog_description_version = "2026-03"
        cat_short_text_flag = is_cat_short_text(course_code, catalog_description)

        # --- Guide description alternates ---
        guide_misrouted_text_flag = is_guide_misrouted(course_code)
        if guide_misrouted_text_flag:
            guide_description_alternates: list[GuideDescriptionAlternate] = []
        else:
            guide_description_alternates = []
            enrich_entry = enrichment.get(course_code)
            if enrich_entry:
                for desc in enrich_entry.get("descriptions", []):
                    src_programs = desc.get("source_program_codes", [])
                    src_prog = src_programs[0] if src_programs else "unknown"
                    g_version = guide_versions.get(src_prog, "unknown")
                    guide_description_alternates.append(
                        GuideDescriptionAlternate(
                            source_program_code=src_prog,
                            guide_version=g_version,
                            description_text=desc.get("text", ""),
                        )
                    )

        # --- Competency variants ---
        competency_variants: list[CompetencyVariant] = []
        enrich_entry = enrichment.get(course_code)
        if enrich_entry:
            for comp_set in enrich_entry.get("competency_sets", []):
                src_programs = comp_set.get("source_program_codes", [])
                src_prog = src_programs[0] if src_programs else "unknown"
                g_version = guide_versions.get(src_prog, "unknown")
                competency_variants.append(
                    CompetencyVariant(
                        source_program_code=src_prog,
                        guide_version=g_version,
                        bullets=comp_set.get("bullets", []),
                    )
                )
        competency_variant_count = len(competency_variants)

        # --- Cert prep signal ---
        cert_prep_signal = _build_cert_prep_signal(course_code, cert_lookup, guide_versions)

        # --- Prerequisites (no structured source available) ---
        prerequisite_course_codes: list[str] = []
        is_prereq_for: list[str] = []

        # --- Program association from course_index ---
        index_entry = course_index.get(course_code)
        if index_entry:
            instances = index_entry.get("instances", [])
        else:
            instances = []

        program_codes_set: set[str] = set()
        for inst in instances:
            degree = inst.get("degree", "")
            prog_code = degree_to_code.get(degree)
            if prog_code:
                program_codes_set.add(prog_code)
        program_codes = sorted(program_codes_set)

        instances_by_version = _build_instances_by_version(instances, degree_to_code)

        # --- Guide enrichment summary ---
        has_guide_desc = len(guide_description_alternates) > 0
        has_competencies = competency_variant_count > 0
        has_cert = cert_prep_signal.status == "present"
        program_count_enriched = 0
        if enrich_entry:
            # Count distinct programs that contributed any enrichment
            enriched_progs: set[str] = set()
            for desc in enrich_entry.get("descriptions", []):
                enriched_progs.update(desc.get("source_program_codes", []))
            for comp in enrich_entry.get("competency_sets", []):
                enriched_progs.update(comp.get("source_program_codes", []))
            program_count_enriched = len(enriched_progs)

        guide_enrichment_available = has_guide_desc or has_competencies or has_cert
        guide_enrichment_summary = GuideEnrichmentSummary(
            has_guide_description_alternates=has_guide_desc,
            has_competencies=has_competencies,
            competency_variant_count=competency_variant_count,
            has_cert_prep_signal=has_cert,
            program_count_with_guide_enrichment=program_count_enriched,
        )

        # --- Version conflict programs ---
        version_conflict_programs: list[VersionConflictProgram] = []
        for prog in program_codes:
            conflict = get_version_conflict(prog)
            if conflict:
                version_conflict_programs.append(
                    VersionConflictProgram(
                        program_code=prog,
                        catalog_version=conflict["catalog_version"],
                        guide_version=conflict["guide_version"],
                        conflict_type="catalog_guide_version_mismatch",
                    )
                )

        # --- Evidence refs (placeholder) ---
        evidence_refs: list[EvidenceRef] = [
            EvidenceRef(
                source_type="catalog",
                artifact_id="course_index_2026_03",
                version="2026-03",
            )
        ]

        cards[course_code] = CourseCard(
            course_code=course_code,
            canonical_title=canonical_title,
            canonical_cus=canonical_cus,
            title_variants=title_variants,
            catalog_description=catalog_description,
            catalog_description_version=catalog_description_version,
            cat_short_text_flag=cat_short_text_flag,
            guide_description_alternates=guide_description_alternates,
            guide_misrouted_text_flag=guide_misrouted_text_flag,
            competency_variants=competency_variants,
            competency_variant_count=competency_variant_count,
            cert_prep_signal=cert_prep_signal,
            prerequisite_course_codes=prerequisite_course_codes,
            is_prereq_for=is_prereq_for,
            program_codes=program_codes,
            instances_by_version=instances_by_version,
            guide_enrichment_available=guide_enrichment_available,
            guide_enrichment_summary=guide_enrichment_summary,
            version_conflict_programs=version_conflict_programs,
            evidence_refs=evidence_refs,
        )

    return cards
