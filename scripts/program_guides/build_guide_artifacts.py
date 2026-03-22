#!/usr/bin/env python3
"""
build_guide_artifacts.py — Session 31
Emits degree-facing guide artifacts for all 115 WGU programs.

Reads:
  - data/program_guides/parsed/*.json
  - data/program_guides/validation/*.json
  - data/program_guides/sp_family_classification.json
  - data/program_guides/sp_families.json
  - data/program_guides/cert_course_mapping.json
  - data/program_guides/prereq_relationships.json
  - data/program_guides/guide_anomaly_registry.json

Writes:
  - data/program_guides/degree_artifacts/<PROGRAM_CODE>_degree_artifact.json (one per program)
  - data/program_guides/degree_artifacts/manifest.json

Follows PHASE_D policy:
  - Category A: full SP with term grouping
  - Category B: SP as ordered list, no term grouping, sp_display_mode: "advisor-guided"
  - Category C: SP for track, family reference
  - Category D (MATSPED): sp_display_mode: "suppressed"
  - Partial-use guide overrides (BSITM, MATSPED, MSCSUG, BSPRN) from policy
  - Anomaly entries only for program-specific anomalies (ANOM-001 to ANOM-003, ANOM-006, ANOM-007)
  - Corpus-wide anomalies (ANOM-004, ANOM-005, ANOM-008, ANOM-009) excluded from per-program flags
"""

import json
import os
import glob
import datetime
import sys
from collections import defaultdict

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARSED_DIR = os.path.join(BASE, "data/program_guides/parsed")
VALIDATION_DIR = os.path.join(BASE, "data/program_guides/validation")
OUTPUT_DIR = os.path.join(BASE, "data/program_guides/degree_artifacts")
SP_FAMILY_CLASSIFICATION = os.path.join(BASE, "data/program_guides/sp_family_classification.json")
SP_FAMILIES = os.path.join(BASE, "data/program_guides/sp_families.json")
CERT_COURSE_MAPPING = os.path.join(BASE, "data/program_guides/cert_course_mapping.json")
DEGREE_LEVEL_CERT_SIGNALS = os.path.join(BASE, "data/program_guides/degree_level_cert_signals.json")
PREREQ_RELATIONSHIPS = os.path.join(BASE, "data/program_guides/prereq_relationships.json")
ANOMALY_REGISTRY = os.path.join(BASE, "data/program_guides/guide_anomaly_registry.json")

SCHEMA_VERSION = "phase_d_v1"
# Corpus-wide anomaly IDs (extraction-side issues; excluded from per-program flags)
CORPUS_WIDE_ANOMALY_IDS = {"ANOM-004", "ANOM-005", "ANOM-008", "ANOM-009"}

# ─── SP anomaly title length threshold ───────────────────────────────────────
ANOMALY_TITLE_LENGTH_THRESHOLD = 150

# ─── Special program override rules from phase_d_publish_policy.json ─────────
# Programs where SP is fully suppressed regardless of SP category
SP_SUPPRESS_PROGRAMS = {"BSITM", "MATSPED", "MSCSUG"}

# ─── load helpers ─────────────────────────────────────────────────────────────

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_parsed():
    """Return dict of program_code -> parsed JSON."""
    result = {}
    for path in glob.glob(os.path.join(PARSED_DIR, "*_parsed.json")):
        d = load_json(path)
        code = d.get("program_code")
        if code:
            result[code] = d
    return result


def load_all_validation():
    """Return dict of program_code -> validation JSON."""
    result = {}
    for path in glob.glob(os.path.join(VALIDATION_DIR, "*_validation.json")):
        d = load_json(path)
        code = d.get("program_code")
        if code:
            result[code] = d
    return result


def load_sp_family_classification():
    """Return dict of program_code -> classification record."""
    data = load_json(SP_FAMILY_CLASSIFICATION)
    return {r["program_code"]: r for r in data["classifications"]}


def load_sp_families():
    """Return dict of family_code -> family record."""
    data = load_json(SP_FAMILIES)
    return {f["family_code"]: f for f in data["families"]}


def load_cert_mapping():
    """Return list of auto_accepted cert rows only."""
    data = load_json(CERT_COURSE_MAPPING)
    return data.get("auto_accepted", [])


def load_degree_level_cert_signals():
    """Return list of degree-level cert signal rows, keyed by program for fast lookup."""
    rows = load_json(DEGREE_LEVEL_CERT_SIGNALS)
    # Build a dict: program_code -> list of degree-level signal rows
    by_program = defaultdict(list)
    for row in rows:
        for prog in row.get("source_programs", []):
            by_program[prog].append(row)
    return by_program


def load_anomaly_registry():
    """Return dict of program_code -> list of anomaly records (program-specific only)."""
    data = load_json(ANOMALY_REGISTRY)
    result = defaultdict(list)
    for anom in data.get("anomalies", []):
        if anom.get("program_code") and anom["anomaly_id"] not in CORPUS_WIDE_ANOMALY_IDS:
            result[anom["program_code"]].append(anom)
    return result


# ─── policy classifier ────────────────────────────────────────────────────────

def classify_disposition(program_code, sp_category, parsed):
    """
    Determine disposition and caveat_flags for a program per PHASE_D policy.
    Returns (disposition, sp_status, caveat_flags, caveat_messages_ui, sp_display_mode,
             sp_suppression_reason, sp_label)
    """
    caveat_flags = []
    caveat_messages_ui = []
    sp_display_mode = None
    sp_suppression_reason = None
    sp_label = None

    # Special per-program overrides
    if program_code == "MATSPED":
        disposition = "partial-use"
        sp_status = "unusable"
        sp_display_mode = "suppressed"
        sp_suppression_reason = "sp_unusable_source_extraction_failure"
        caveat_flags.append("sp_unusable_source_extraction_failure")
        caveat_messages_ui.append(
            "Program map shown from Areas of Study; standard sequence unavailable from source guide formatting."
        )
        return disposition, sp_status, caveat_flags, caveat_messages_ui, sp_display_mode, sp_suppression_reason, sp_label

    if program_code == "BSITM":
        disposition = "partial-use"
        # ANOM-002: suppress single bad entry, rest usable — Category A with one suppressed entry
        sp_status = "usable"
        caveat_flags.append("sp_entry_suppressed_concatenation")
        caveat_messages_ui.append(
            "One course sequence entry is unavailable due to a guide format limitation; remaining terms shown."
        )
        return disposition, sp_status, caveat_flags, caveat_messages_ui, sp_display_mode, sp_suppression_reason, sp_label

    if program_code == "MSCSUG":
        disposition = "full-use"
        sp_status = "usable"
        sp_label = "Accelerated B.S./M.S. pathway — term sequence spans both degree levels."
        caveat_flags.append("sp_bridge_program_semantics")
        caveat_messages_ui.append(
            "Accelerated B.S./M.S. pathway — term sequence spans both degree levels."
        )
        return disposition, sp_status, caveat_flags, caveat_messages_ui, sp_display_mode, sp_suppression_reason, sp_label

    if program_code == "BSPRN":
        disposition = "partial-use"
        sp_status = "partial"
        sp_label = "Pre-Nursing Standard Path"
        caveat_flags.append("sp_partial_dual_track")
        caveat_messages_ui.append(
            "Standard sequence shown for Pre-Nursing segment; nursing-track sequencing is reflected in Areas of Study."
        )
        return disposition, sp_status, caveat_flags, caveat_messages_ui, sp_display_mode, sp_suppression_reason, sp_label

    if program_code == "MEDETID":
        disposition = "full-use"
        sp_status = "usable"
        caveat_flags.append("capstone_partial_sequence")
        caveat_messages_ui.append(
            "Capstone shown is the first of a multi-course capstone sequence; full sequence not available from this guide."
        )
        return disposition, sp_status, caveat_flags, caveat_messages_ui, sp_display_mode, sp_suppression_reason, sp_label

    if program_code == "BSNU":
        disposition = "full-use"
        sp_status = "usable"
        caveat_flags.append("metadata_missing_no_footer")
        caveat_messages_ui.append(
            "Guide version information unavailable for this program."
        )
        return disposition, sp_status, caveat_flags, caveat_messages_ui, sp_display_mode, sp_suppression_reason, sp_label

    # Category D (should be just MATSPED, handled above, but defensive)
    if sp_category == "D":
        disposition = "partial-use"
        sp_status = "unusable"
        sp_display_mode = "suppressed"
        sp_suppression_reason = "sp_unusable_source_extraction_failure"
        caveat_flags.append("sp_unusable_source_extraction_failure")
        caveat_messages_ui.append(
            "Program map shown from Areas of Study; standard sequence unavailable from source guide formatting."
        )
        return disposition, sp_status, caveat_flags, caveat_messages_ui, sp_display_mode, sp_suppression_reason, sp_label

    # Default: full-use
    disposition = "full-use"
    sp_rows = parsed.get("standard_path", [])
    if sp_rows:
        sp_status = "usable"
    else:
        sp_status = "unusable"

    # Category B: no term grouping
    if sp_category == "B":
        sp_display_mode = "advisor-guided"

    return disposition, sp_status, caveat_flags, caveat_messages_ui, sp_display_mode, sp_suppression_reason, sp_label


# ─── standard_path builder ────────────────────────────────────────────────────

def build_standard_path(program_code, sp_category, parsed, sp_status, sp_display_mode,
                        sp_suppression_reason, sp_label):
    """
    Build the standard_path block per policy.
    Category A: emit with term grouping (term field present)
    Category B: emit as ordered list (no term grouping, flag advisor-guided)
    Category C: emit for this track
    Category D: emit suppressed block
    """
    raw_sp = parsed.get("standard_path", [])

    if sp_status == "unusable" or sp_display_mode == "suppressed":
        return {
            "available": False,
            "partial": False,
            "label": None,
            "sp_display_mode": "suppressed",
            "sp_suppression_reason": sp_suppression_reason,
            "rows": []
        }

    # Filter anomalous titles (>= 150 chars)
    filtered_rows = []
    suppressed_count = 0
    for row in raw_sp:
        title = row.get("title", "")
        if len(title) >= ANOMALY_TITLE_LENGTH_THRESHOLD:
            suppressed_count += 1
            continue
        filtered_rows.append(row)

    is_partial = sp_status == "partial"

    block = {
        "available": True,
        "partial": is_partial,
        "label": sp_label,
        "rows": [
            {
                "title": r.get("title"),
                "cus": r.get("cus"),
                "term": r.get("term")
            }
            for r in filtered_rows
        ]
    }

    if sp_display_mode:
        block["sp_display_mode"] = sp_display_mode

    if suppressed_count > 0:
        block["suppressed_entry_count"] = suppressed_count

    return block


# ─── areas_of_study builder ───────────────────────────────────────────────────

def build_areas_of_study(parsed):
    """
    Build areas_of_study array from parsed guide.
    For each course: title, description, competency_bullets, competency_available.
    Does NOT use cross-program enrichment; uses per-program parsed content only.
    """
    raw_aos = parsed.get("areas_of_study", [])
    result = []
    for group_entry in raw_aos:
        group_name = group_entry.get("group", "")
        courses_out = []
        for course in group_entry.get("courses", []):
            bullets = course.get("competency_bullets", [])
            courses_out.append({
                "title": course.get("title"),
                "description": course.get("description"),
                "competency_bullets": bullets,
                "competency_available": len(bullets) > 0
            })
        result.append({
            "group": group_name,
            "courses": courses_out
        })
    return result


# ─── cert signals builder ─────────────────────────────────────────────────────

LICENSURE_CERTS = {"NCLEX-RN", "NCLEX-PN", "Praxis exam", "Praxis 5039", "Praxis 5081"}


def _cert_category(normalized_cert):
    if normalized_cert in LICENSURE_CERTS:
        return "licensure"
    return "professional_cert"


def build_cert_signals(program_code, parsed, cert_mapping_rows, degree_signals_by_program):
    """
    Build cert_signals from auto_accepted cert rows (course-level) and degree-level signals.
    Course-level: cert is included if this program_code appears in source_programs of the cert row.
    Degree-level: cert is included if this program_code appears in source_programs of a degree signal row.
    Returns list of {normalized_cert, via_course_title, via_course_code, confidence,
                     atlas_recommendation, source_type, cert_category}.
    """
    signals = []
    for row in cert_mapping_rows:
        if program_code in row.get("source_programs", []):
            cert = row.get("normalized_cert")
            signals.append({
                "normalized_cert": cert,
                "via_course_title": row.get("source_course_title"),
                "via_course_code": row.get("matched_course_code"),
                "confidence": row.get("confidence"),
                "atlas_recommendation": row.get("atlas_recommendation"),
                "source_type": "course_mention",
                "cert_category": _cert_category(cert),
            })
    for row in degree_signals_by_program.get(program_code, []):
        cert = row.get("normalized_cert")
        signals.append({
            "normalized_cert": cert,
            "via_course_title": None,
            "via_course_code": None,
            "confidence": row.get("confidence"),
            "atlas_recommendation": row.get("atlas_recommendation"),
            "source_type": "program_description",
            "cert_category": _cert_category(cert),
        })
    return signals


# ─── family builder ───────────────────────────────────────────────────────────

def build_family(program_code, classification, families_by_code):
    """
    Build family block from sp_family_classification + sp_families.
    Returns family dict or None.
    """
    family_code = classification.get("family_code")
    if not family_code:
        return None

    family_def = families_by_code.get(family_code)
    if not family_def:
        return None

    # Track label for THIS program
    track_label = None
    siblings = []
    for member in family_def.get("members", []):
        if member["program_code"] == program_code:
            track_label = member["track_label"]
        else:
            siblings.append({
                "program_code": member["program_code"],
                "track_label": member["track_label"]
            })

    return {
        "family_code": family_code,
        "family_label": family_def.get("family_label"),
        "family_type": family_def.get("family_type"),
        "sp_relationship": family_def.get("sp_relationship"),
        "track_label": track_label,
        "display_recommendation": family_def.get("display_recommendation"),
        "siblings": siblings
    }


# ─── capstone builder ─────────────────────────────────────────────────────────

def build_capstone(program_code, parsed):
    """
    Build capstone block. MEDETID gets partial: true.
    """
    raw_cap = parsed.get("capstone")
    if not raw_cap:
        return None

    is_partial = program_code == "MEDETID"
    bullets = raw_cap.get("competency_bullets", [])

    return {
        "present": True,
        "partial": is_partial,
        "title": raw_cap.get("title"),
        "description": raw_cap.get("description"),
        "competency_bullets": bullets,
        "competency_available": len(bullets) > 0
    }


# ─── provenance builder ───────────────────────────────────────────────────────

def build_provenance(parsed, validation):
    """
    Build guide_provenance block.
    """
    confidence = "unknown"
    if validation:
        confidence = validation.get("parseability_confidence", "unknown")

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "source_version": parsed.get("version"),
        "source_pub_date": parsed.get("pub_date"),
        "source_page_count": parsed.get("page_count"),
        "confidence": confidence,
    }


# ─── anomaly flags builder ────────────────────────────────────────────────────

def build_anomaly_flags(program_code, anomalies_by_program):
    """
    Return list of anomaly_ids that apply to this specific program.
    Excludes corpus-wide anomalies (ANOM-004, -005, -008, -009).
    """
    records = anomalies_by_program.get(program_code, [])
    return [r["anomaly_id"] for r in records]


# ─── main artifact builder ────────────────────────────────────────────────────

def build_artifact(program_code, parsed, validation, classification, families_by_code,
                   cert_mapping_rows, degree_signals_by_program, anomalies_by_program):
    """
    Build the full degree artifact for a program.
    """
    sp_category = classification.get("sp_category", "A")

    (disposition, sp_status, caveat_flags, caveat_messages_ui,
     sp_display_mode, sp_suppression_reason, sp_label) = classify_disposition(
        program_code, sp_category, parsed
    )

    standard_path = build_standard_path(
        program_code, sp_category, parsed, sp_status,
        sp_display_mode, sp_suppression_reason, sp_label
    )

    areas_of_study = build_areas_of_study(parsed)

    cert_signals = build_cert_signals(program_code, parsed, cert_mapping_rows, degree_signals_by_program)

    family = build_family(program_code, classification, families_by_code)

    capstone = build_capstone(program_code, parsed)

    provenance = build_provenance(parsed, validation)

    anomaly_flags = build_anomaly_flags(program_code, anomalies_by_program)

    # Quality block (mirrors validation metadata)
    aos_course_count = sum(len(g.get("courses", [])) for g in parsed.get("areas_of_study", []))
    quality = {
        "sp_status": sp_status,
        "sp_category": sp_category,
        "aos_status": "usable" if areas_of_study else "empty",
        "aos_course_count": aos_course_count,
        "caveat_flags": caveat_flags,
        "caveat_messages_ui": caveat_messages_ui,
    }

    artifact = {
        # Identity
        "program_code": program_code,
        "source_degree_title": parsed.get("degree_title"),
        "disposition": disposition,
        # Provenance
        "guide_provenance": provenance,
        # Quality
        "quality": quality,
        # Payload
        "standard_path": standard_path,
        "areas_of_study": areas_of_study,
        "capstone": capstone,
        "cert_signals": cert_signals,
        "family": family,
        "anomaly_flags": anomaly_flags,
    }

    return artifact


# ─── validation checks ────────────────────────────────────────────────────────

def validate_outputs(artifacts, cert_mapping_rows):
    """
    Run PHASE_D policy validation checks.
    Returns (violations, warnings).
    """
    violations = []
    warnings = []

    # Build a lookup: which programs each cert row should appear in
    cert_program_map = defaultdict(set)
    for row in cert_mapping_rows:
        cert = row["normalized_cert"]
        for prog in row.get("source_programs", []):
            cert_program_map[prog].add(cert)

    for code, artifact in artifacts.items():
        q = artifact["quality"]
        sp = artifact["standard_path"]
        family = artifact["family"]
        caveat_flags = q.get("caveat_flags", [])

        # Check: every auto-accepted cert for this program must appear in cert_signals
        expected_certs = cert_program_map.get(code, set())
        actual_certs = {s["normalized_cert"] for s in artifact.get("cert_signals", [])}
        missing = expected_certs - actual_certs
        if missing:
            violations.append(
                f"CERT_MISSING: {code} is missing cert signals: {sorted(missing)}"
            )

        # Check: Category A programs should have non-empty standard_path
        if q["sp_category"] == "A" and not sp.get("available"):
            if code not in SP_SUPPRESS_PROGRAMS:
                violations.append(
                    f"SP_MISSING: Category A program {code} has no available standard_path"
                )

        # Check: MATSPED should have sp_display_mode == "suppressed"
        if code == "MATSPED":
            if sp.get("sp_display_mode") != "suppressed":
                violations.append(
                    f"POLICY_VIOLATION: MATSPED must have sp_display_mode='suppressed', "
                    f"got {sp.get('sp_display_mode')!r}"
                )
            else:
                warnings.append("OK: MATSPED sp_display_mode=suppressed confirmed")

        # Check: Category C programs must have non-null family
        if q["sp_category"] == "C" and family is None:
            violations.append(
                f"FAMILY_MISSING: Category C program {code} has null family"
            )

        # Check: no review-needed rows in cert_signals (by definition we only used auto_accepted,
        # but verify no "review" confidence leaked through)
        for sig in artifact.get("cert_signals", []):
            if sig.get("confidence") not in ("high", "medium"):
                violations.append(
                    f"CERT_POLICY: {code} has cert signal with unexpected confidence "
                    f"{sig['confidence']!r}: {sig['normalized_cert']}"
                )

        # Warn about known caveat guides
        expected_caveats = {
            "BSITM": "sp_entry_suppressed_concatenation",
            "MATSPED": "sp_unusable_source_extraction_failure",
            "MSCSUG": "sp_bridge_program_semantics",
            "BSPRN": "sp_partial_dual_track",
            "MEDETID": "capstone_partial_sequence",
            "BSNU": "metadata_missing_no_footer",
        }
        if code in expected_caveats:
            expected_flag = expected_caveats[code]
            if expected_flag in caveat_flags:
                warnings.append(f"OK: {code} has expected caveat flag '{expected_flag}'")
            else:
                violations.append(
                    f"CAVEAT_MISSING: {code} expected caveat flag '{expected_flag}' not found"
                )

    return violations, warnings


# ─── manifest builder ─────────────────────────────────────────────────────────

def build_manifest(artifacts, errors):
    """
    Build summary manifest for all processed programs.
    """
    total = len(artifacts)
    sp_by_category = defaultdict(list)
    with_cert = []
    with_family = []
    with_capstone = []
    with_anomaly_flags = []

    for code, art in artifacts.items():
        cat = art["quality"]["sp_category"]
        sp_by_category[cat].append(code)

        if art.get("cert_signals"):
            with_cert.append(code)
        if art.get("family"):
            with_family.append(code)
        if art.get("capstone"):
            with_capstone.append(code)
        if art.get("anomaly_flags"):
            with_anomaly_flags.append(code)

    total_cert_program_pairs = sum(
        len(art.get("cert_signals", [])) for art in artifacts.values()
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total_programs_processed": total,
        "sp_category_counts": {
            "A": len(sp_by_category.get("A", [])),
            "B": len(sp_by_category.get("B", [])),
            "C": len(sp_by_category.get("C", [])),
            "D": len(sp_by_category.get("D", [])),
        },
        "sp_category_programs": {
            "A": sorted(sp_by_category.get("A", [])),
            "B": sorted(sp_by_category.get("B", [])),
            "C": sorted(sp_by_category.get("C", [])),
            "D": sorted(sp_by_category.get("D", [])),
        },
        "programs_with_cert_signals": len(with_cert),
        "total_cert_program_pairs": total_cert_program_pairs,
        "programs_with_family": len(with_family),
        "programs_with_capstone": len(with_capstone),
        "programs_with_anomaly_flags": len(with_anomaly_flags),
        "programs_with_anomaly_flags_list": sorted(with_anomaly_flags),
        "errors": errors,
    }


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("build_guide_artifacts.py — Phase D artifact emit")
    print("=" * 70)

    # Load all source data
    print("\n[1/7] Loading parsed guides...")
    parsed_all = load_all_parsed()
    print(f"      Loaded {len(parsed_all)} parsed guides")

    print("[2/7] Loading validation files...")
    validation_all = load_all_validation()
    print(f"      Loaded {len(validation_all)} validation files")

    print("[3/7] Loading SP family classification...")
    classification_all = load_sp_family_classification()
    print(f"      Loaded {len(classification_all)} classifications")

    print("[4/7] Loading SP families...")
    families_by_code = load_sp_families()
    print(f"      Loaded {len(families_by_code)} family definitions")

    print("[5/7] Loading cert course mapping (auto-accepted only)...")
    cert_mapping_rows = load_cert_mapping()
    print(f"      Loaded {len(cert_mapping_rows)} auto-accepted cert rows")

    print("[5b] Loading degree-level cert signals...")
    degree_signals_by_program = load_degree_level_cert_signals()
    print(f"      Loaded degree-level signals for programs: {sorted(degree_signals_by_program.keys())}")

    print("[6/7] Loading anomaly registry...")
    anomalies_by_program = load_anomaly_registry()
    print(f"      Loaded anomalies for programs: {sorted(anomalies_by_program.keys())}")

    print("[7/7] Setting up output directory...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"      Output dir: {OUTPUT_DIR}")

    # Hard-fail anchor check
    if len(parsed_all) != 115:
        print(f"\nHARD FAIL: Expected 115 parsed guides, got {len(parsed_all)}", file=sys.stderr)
        sys.exit(1)

    print("\n--- Building artifacts ---")
    artifacts = {}
    errors = []

    for program_code in sorted(parsed_all.keys()):
        try:
            parsed = parsed_all[program_code]
            validation = validation_all.get(program_code)
            classification = classification_all.get(program_code, {
                "program_code": program_code,
                "sp_category": "A",
                "sp_category_label": "structured-term-path",
                "family_code": None
            })

            artifact = build_artifact(
                program_code, parsed, validation, classification,
                families_by_code, cert_mapping_rows, degree_signals_by_program, anomalies_by_program
            )
            artifacts[program_code] = artifact

        except Exception as e:
            err_msg = f"{program_code}: {type(e).__name__}: {e}"
            errors.append(err_msg)
            print(f"  ERROR: {err_msg}")

    print(f"  Built {len(artifacts)} artifacts ({len(errors)} errors)")

    # Write per-program artifacts
    print("\n--- Writing per-program artifacts ---")
    for program_code, artifact in artifacts.items():
        out_path = os.path.join(OUTPUT_DIR, f"{program_code}_degree_artifact.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(artifact, f, indent=2, ensure_ascii=False)

    print(f"  Wrote {len(artifacts)} artifact files")

    # Write manifest
    manifest = build_manifest(artifacts, errors)
    manifest_path = os.path.join(OUTPUT_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"  Wrote manifest: {manifest_path}")

    # ─── Validation ─────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("PHASE_D POLICY VALIDATION REPORT")
    print("=" * 70)

    violations, warnings = validate_outputs(artifacts, cert_mapping_rows)

    if warnings:
        print(f"\n[OK checks — {len(warnings)}]")
        for w in warnings:
            print(f"  ✓ {w}")

    if violations:
        print(f"\n[VIOLATIONS — {len(violations)}]")
        for v in violations:
            print(f"  ✗ {v}")
    else:
        print("\nNo policy violations found.")

    # ─── Summary ─────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("MANIFEST SUMMARY")
    print("=" * 70)
    print(f"  Total programs processed : {manifest['total_programs_processed']}")
    print(f"  SP Category A            : {manifest['sp_category_counts']['A']}")
    print(f"  SP Category B            : {manifest['sp_category_counts']['B']}")
    print(f"  SP Category C            : {manifest['sp_category_counts']['C']}")
    print(f"  SP Category D            : {manifest['sp_category_counts']['D']}")
    print(f"  With cert signals        : {manifest['programs_with_cert_signals']} programs")
    print(f"  Cert-program pairs       : {manifest['total_cert_program_pairs']}")
    print(f"  With family membership   : {manifest['programs_with_family']}")
    print(f"  With capstone            : {manifest['programs_with_capstone']}")
    print(f"  With anomaly flags       : {manifest['programs_with_anomaly_flags']}")
    if errors:
        print(f"\n  ERRORS ({len(errors)}):")
        for e in errors:
            print(f"    {e}")
    else:
        print(f"\n  No errors.")

    print("\nDone.")
    return 0 if not violations and not errors else 1


if __name__ == "__main__":
    sys.exit(main())
