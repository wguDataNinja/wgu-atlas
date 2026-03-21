#!/usr/bin/env python3
"""
analyze_guide_manifest.py
=========================
Corpus-level structural probe for all WGU program guide text files.

Scans each guide text for section presence, counts, metadata, and
structural signals WITHOUT performing content extraction. Produces
manifest and matrix artifacts that drive parser design decisions.

Usage:
    WGU_GUIDES_TEXT_DIR=/path/to/raw_texts \\
    WGU_GUIDES_DATA_DIR=/path/to/wgu-atlas/data/program_guides \\
    python3 scripts/program_guides/analyze_guide_manifest.py

Defaults:
    Text dir:  ~/Desktop/WGU-Reddit/WGU_catalog/program_guides/raw_texts/
    Data dir:  <repo_root>/data/program_guides/

Outputs:
    guide_manifest.json         — one row per guide, all structural fields
    section_presence_matrix.csv — boolean presence flags per guide
    manifest_summary.json       — corpus-level aggregate stats
"""

import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).parent
_REPO_ROOT  = _SCRIPT_DIR.parent.parent
_HOME = Path.home()

_DEFAULT_TEXT_DIR = _HOME / "Desktop" / "WGU-Reddit" / "WGU_catalog" / "program_guides" / "raw_texts"
_DEFAULT_DATA_DIR = _REPO_ROOT / "data" / "program_guides"

TEXT_DIR = Path(os.environ.get("WGU_GUIDES_TEXT_DIR", str(_DEFAULT_TEXT_DIR)))
DATA_DIR = Path(os.environ.get("WGU_GUIDES_DATA_DIR", str(_DEFAULT_DATA_DIR)))

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Footer: "BSDA 202309 © 2019 Western Governors University 5/1/23 2"
FOOTER_RE = re.compile(
    r'^([A-Z][A-Z0-9_\-]+)\s+(\d{6})\s+©\s+\d{4}\s+Western Governors University\s+'
    r'(\d{1,2}/\d{1,2}/\d{2,4})\s+(\d+)\s*$'
)
# Looser footer for guides that vary wording slightly
FOOTER_LOOSE_RE = re.compile(r'^([A-Z][A-Z0-9_\-]+)\s+(\d{6})\s+©')

# Section anchors
STANDARD_PATH_RE    = re.compile(r'^Standard Path(\s+for\s+.+)?$')
AREAS_OF_STUDY_RE   = re.compile(r'^Areas of Study\b')
CAPSTONE_RE         = re.compile(r'^Capstone$', re.IGNORECASE)
ACCESSIBILITY_RE    = re.compile(r'^Accessibility and Accommodations')
STUDENT_SERVICES_RE = re.compile(r'^Need More Information\?')

# Standard Path table
SP_HEADER_RE = re.compile(r'^Course\s+Description\s+CUs?\s+Term', re.IGNORECASE)
SP_ROW_RE    = re.compile(r'^(.+?)\s+(\d{1,2})\s+(\d{1,2})\s*$')
SP_CHANGES_RE = re.compile(r'^Changes to Curriculum')

# AoS content signals
COMPETENCY_TRIGGER_RE = re.compile(
    r'^This course covers the following competencies:', re.IGNORECASE
)
BULLET_RE = re.compile(r'^[●•]\s*')

# Cert prep / prereq mentions
CERT_PREP_RE = re.compile(
    r'certification exam|prepares students for|CompTIA|Praxis|NCLEX|CPA exam|'
    r'certification preparation|exam prep',
    re.IGNORECASE,
)
PREREQ_RE = re.compile(r'prerequisite|pre-requisite', re.IGNORECASE)

# Accreditation section
ACCREDITATION_RE = re.compile(r'^Accreditation$')

# Known boilerplate section headings to skip/flag
BOILERPLATE_HEADINGS = {
    'Understanding the Competency-Based Approach',
    'The Degree Plan', 'How You Will Interact with Faculty',
    'Connecting with Other Mentors and Fellow Students',
    'Orientation', 'Transferability of Prior College Coursework',
    'Continuous Enrollment, On Time Progress, and Satisfactory Academic Progress',
    'Courses', 'Learning Resources', 'Mobile Compatibility:',
    'Changes to Curriculum',
}

# Headings that signal non-standard guide structure
VARIANT_HEADINGS = {
    'Clinical Experiences', 'Clinical Information', 'Practicum',
    'Field Experience', 'Student Teaching', 'Licensure',
    'Prior Learning', 'RN to MSN', 'Post-Master',
    'Prerequisites', 'Elective Options',
}


# ---------------------------------------------------------------------------
# Family classification
# ---------------------------------------------------------------------------

def classify_family(code: str) -> str:
    c = code.upper()
    if c.startswith('END'):
        return 'endorsement'
    if c.startswith('PMCN'):
        return 'nursing_pmc'
    if c.startswith('MSNRN') or c.startswith('MSRNN'):
        return 'nursing_rn_msn'
    if c.startswith('MSNUED') or c.startswith('MSNUFNP') or c.startswith('MSNULM') \
            or c.startswith('MSNUNI') or c.startswith('MSNUP'):
        return 'nursing_msn'
    if c.startswith('BSPRN') or c.startswith('BSNU'):
        return 'nursing_ug'
    if c in ('MBA', 'MBAHA', 'MBAITM'):
        return 'mba'
    if c in ('MHA', 'MPH'):
        return 'healthcare_grad'
    if c.startswith('MACC'):
        return 'accounting_ma'
    if c.startswith('MSCS'):
        return 'cs_grad'
    if c.startswith('MSSWE'):
        return 'swe_grad'
    if c.startswith('MSDAD'):
        return 'data_analytics_grad'
    if c.startswith('MSED') or c.startswith('MEDET'):
        return 'education_grad'
    if c.startswith('MSCIN') or c.startswith('MSIT') or c.startswith('MSHR') \
            or c.startswith('MSML') or c.startswith('MSMK'):
        return 'graduate_standard'
    if c.startswith('MA') and 'T' in c[2:4]:
        return 'teaching_mat'
    if c.startswith('MA') or c.startswith('MSED') or c.startswith('MSEDL'):
        return 'education_ma'
    if c.startswith('BAE') or c.startswith('BAS') and len(c) > 3:
        return 'education_ba'
    if c.startswith('BSSWE') or c.startswith('BSCNE') or c.startswith('BSCSIA') \
            or c.startswith('BSCS'):
        return 'cs_ug'
    if 'SES' in c or ('SE' in c[2:] and c.startswith('BS')):
        return 'education_bs'
    if c.startswith('BS'):
        return 'standard_bs'
    if c.startswith('MS'):
        return 'graduate_standard'
    return 'unknown'


# ---------------------------------------------------------------------------
# Core probe: analyze one text file
# ---------------------------------------------------------------------------

def probe_guide(txt_path: Path) -> dict:
    """
    Lightweight structural probe of a single guide text file.
    Returns a manifest row dict.
    """
    stem = txt_path.stem  # e.g. "BSDA"

    with open(txt_path, encoding='utf-8', errors='replace') as f:
        raw_lines = f.readlines()

    lines = [l.rstrip('\n') for l in raw_lines]
    stripped = [l.strip() for l in lines]

    warnings      = []
    irregularities = []

    # ── Metadata from footer lines ──────────────────────────────────────────
    program_codes    = []
    version_strings  = []
    pub_dates        = []
    page_numbers     = []

    for line in stripped:
        m = FOOTER_RE.match(line)
        if m:
            program_codes.append(m.group(1))
            version_strings.append(m.group(2))
            pub_dates.append(m.group(3))
            page_numbers.append(int(m.group(4)))
        elif FOOTER_LOOSE_RE.match(line):
            # Looser match for variant footers
            parts = line.split()
            if len(parts) >= 2:
                program_codes.append(parts[0])
                version_strings.append(parts[1])

    # Infer program code (most common in footer, or fallback to filename)
    code_counts = Counter(program_codes)
    inferred_code = code_counts.most_common(1)[0][0] if code_counts else stem

    if inferred_code != stem:
        warnings.append(f"code_mismatch: footer says '{inferred_code}', filename is '{stem}'")

    unique_versions = sorted(set(version_strings))
    unique_dates    = sorted(set(pub_dates))
    page_count      = max(page_numbers) if page_numbers else 0

    if len(unique_versions) > 1:
        warnings.append(f"multiple_versions: {unique_versions}")

    # ── Section presence scan ───────────────────────────────────────────────
    has_standard_path    = False
    has_areas_of_study   = False
    has_capstone         = False
    has_accreditation    = False
    has_boilerplate_closing = False
    has_competency_bullets  = False
    has_sp_header        = False

    sp_row_count        = 0
    competency_bullet_count = 0
    cert_prep_count     = 0
    prereq_count        = 0
    competency_trigger_count = 0

    detected_headings   = []
    in_standard_path    = False
    variant_headings_found = []

    # After Standard Path header and before AoS header, count SP rows
    sp_zone = False
    sp_ended = False

    for i, line in enumerate(stripped):
        if not line:
            continue

        # Footer — skip
        if FOOTER_LOOSE_RE.match(line) and '©' in line:
            continue

        # Standard Path detection
        if STANDARD_PATH_RE.match(line):
            has_standard_path = True
            sp_zone = True
            detected_headings.append(line)
            continue

        # Repeated SP header (page break artifact) — also signals CU/term structure
        if SP_HEADER_RE.match(line):
            has_sp_header = True
            continue

        # Count SP rows if in SP zone
        if sp_zone and not sp_ended:
            if AREAS_OF_STUDY_RE.match(line):
                sp_zone = False
                sp_ended = True
            elif SP_CHANGES_RE.match(line):
                sp_zone = False
                sp_ended = True
            elif SP_ROW_RE.match(line) and not SP_HEADER_RE.match(line):
                sp_row_count += 1

        # Areas of Study
        if AREAS_OF_STUDY_RE.match(line):
            has_areas_of_study = True
            detected_headings.append(line)
            continue

        # Capstone
        if CAPSTONE_RE.match(line):
            has_capstone = True
            detected_headings.append(line)
            continue

        # Accreditation
        if ACCREDITATION_RE.match(line):
            has_accreditation = True
            detected_headings.append(line)
            continue

        # Closing boilerplate
        if ACCESSIBILITY_RE.match(line) or STUDENT_SERVICES_RE.match(line):
            has_boilerplate_closing = True
            detected_headings.append(line)
            continue

        # Competency trigger
        if COMPETENCY_TRIGGER_RE.match(line):
            competency_trigger_count += 1
            continue

        # Competency bullets
        if BULLET_RE.match(line):
            has_competency_bullets = True
            competency_bullet_count += 1
            continue

        # Cert prep / prereq mentions (in prose)
        if CERT_PREP_RE.search(line):
            cert_prep_count += 1
        if PREREQ_RE.search(line):
            prereq_count += 1

        # Variant / non-standard headings
        for vh in VARIANT_HEADINGS:
            if line == vh or line.startswith(vh):
                if vh not in variant_headings_found:
                    variant_headings_found.append(vh)
                    irregularities.append(f"variant_heading: '{vh}'")
                break

    # Detect AoS group headings (after AoS header, before Capstone)
    inferred_groups = _detect_aos_groups(stripped)

    # ── Derived flags ───────────────────────────────────────────────────────
    has_course_descriptions = competency_trigger_count > 0  # proxy: trigger implies descriptions
    has_term_structure = has_sp_header or (sp_row_count > 0 and has_standard_path)
    has_cu_values      = has_term_structure  # CUs and Term appear together

    # Validate counts
    if has_standard_path and sp_row_count == 0:
        warnings.append("standard_path_detected_but_no_rows_parsed")
    if has_areas_of_study and competency_trigger_count == 0:
        warnings.append("areas_of_study_detected_but_no_competency_triggers")
    if not has_standard_path:
        irregularities.append("no_standard_path_detected")
    if not has_areas_of_study:
        irregularities.append("no_areas_of_study_detected")

    # ── Confidence and family ───────────────────────────────────────────────
    family = classify_family(inferred_code)

    if has_standard_path and has_areas_of_study and has_capstone and has_boilerplate_closing:
        confidence = "high"
        template_type = "full"
    elif has_standard_path and has_areas_of_study:
        confidence = "medium"
        template_type = "partial"
        if not has_capstone:
            warnings.append("no_capstone_section")
    else:
        confidence = "low"
        template_type = "abbreviated_or_unknown"
        warnings.append("missing_major_sections")

    # Endorsement programs may legitimately not have all sections
    if family == 'endorsement':
        confidence = "medium" if confidence == "low" else confidence
        template_type = "endorsement"

    return {
        "source_pdf_filename":     stem + ".pdf",
        "source_text_filename":    stem + ".txt",
        "inferred_program_code":   inferred_code,
        "page_count":              page_count,
        "version_strings":         unique_versions,
        "publication_dates":       unique_dates,
        # Section presence
        "has_standard_path":       has_standard_path,
        "has_areas_of_study":      has_areas_of_study,
        "has_capstone_section":    has_capstone,
        "has_course_descriptions": has_course_descriptions,
        "has_competency_bullets":  has_competency_bullets,
        "has_term_structure":      has_term_structure,
        "has_cu_values":           has_cu_values,
        "has_cert_prep_mentions":  cert_prep_count > 0,
        "has_prereq_mentions":     prereq_count > 0,
        "has_accreditation_section": has_accreditation,
        "has_boilerplate_closing": has_boilerplate_closing,
        # Counts
        "standard_path_row_count":     sp_row_count,
        "competency_trigger_count":    competency_trigger_count,
        "competency_bullet_count":     competency_bullet_count,
        "cert_prep_mention_count":     cert_prep_count,
        "prereq_mention_count":        prereq_count,
        # Headings
        "detected_section_headings":   detected_headings,
        "inferred_course_groups":      inferred_groups,
        "variant_headings_found":      variant_headings_found,
        # Classification
        "likely_guide_family":         family,
        "template_type":               template_type,
        "parseability_confidence":     confidence,
        # Diagnostics
        "warnings":                    warnings,
        "irregularities":              irregularities,
    }


def _detect_aos_groups(stripped_lines: list) -> list:
    """
    Detect AoS group headings from stripped lines.
    A group heading is a short standalone line inside the AoS body
    that appears before course content and is not a footer or boilerplate.
    """
    in_aos = False
    past_intro = False
    intro_line_count = 0
    groups = []
    last_nonempty = ""

    for i, line in enumerate(stripped_lines):
        if not line:
            continue
        if AREAS_OF_STUDY_RE.match(line):
            in_aos = True
            intro_line_count = 0
            past_intro = False
            continue
        if CAPSTONE_RE.match(line) or ACCESSIBILITY_RE.match(line):
            in_aos = False
            continue
        if not in_aos:
            continue

        # Skip footer lines
        if FOOTER_LOOSE_RE.match(line) and '©' in line:
            continue

        # Skip competency triggers and bullets
        if COMPETENCY_TRIGGER_RE.match(line) or BULLET_RE.match(line):
            past_intro = True
            continue

        # "for" line that follows AoS header
        if line == 'for':
            continue

        # Count intro lines (boilerplate paragraph before first group)
        if not past_intro:
            intro_line_count += 1
            # Intro is prose (long lines); once we see 3+ prose lines, we're past boilerplate
            # The first short, non-prose line after the intro is the first group heading
            if intro_line_count >= 4 and len(line) < 50 and len(line.split()) <= 6:
                past_intro = True
                groups.append(line)
            elif len(line) < 50 and len(line.split()) <= 4 and intro_line_count >= 2:
                # Short line after a couple prose lines = group heading
                past_intro = True
                groups.append(line)
            continue

        # Inside AoS body: candidate group headings are short, title-case lines
        # that precede course descriptions
        words = line.split()
        if (len(words) <= 6
                and len(line) < 55
                and not COMPETENCY_TRIGGER_RE.match(line)
                and not BULLET_RE.match(line)
                and line not in BOILERPLATE_HEADINGS
                and '©' not in line
                and line != 'for'):
            # Look ahead to see if this is followed by another short line (course title)
            # or a long prose line (description after course title)
            # We only care about the GROUP level, not course titles, so be conservative
            # Only add if it looks clearly like a category name (short, ≤ 4 words)
            if len(words) <= 4 and line not in groups:
                # Check: not a competency trigger variant
                if not re.search(r'\bcompeten\b|\blearner\b|\bgraduate\b', line, re.IGNORECASE):
                    groups.append(line)

    return groups


# ---------------------------------------------------------------------------
# Matrix helpers
# ---------------------------------------------------------------------------

PRESENCE_FIELDS = [
    "has_standard_path", "has_areas_of_study", "has_capstone_section",
    "has_course_descriptions", "has_competency_bullets", "has_term_structure",
    "has_cu_values", "has_cert_prep_mentions", "has_prereq_mentions",
    "has_accreditation_section", "has_boilerplate_closing",
]

COUNT_FIELDS = [
    "standard_path_row_count", "competency_trigger_count",
    "competency_bullet_count", "cert_prep_mention_count", "prereq_mention_count",
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not TEXT_DIR.exists():
        print(f"ERROR: Text directory not found: {TEXT_DIR}")
        sys.exit(1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    txt_files = sorted(TEXT_DIR.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in {TEXT_DIR}")
        sys.exit(1)

    print(f"Text source: {TEXT_DIR}")
    print(f"Data output: {DATA_DIR}")
    print(f"Files found: {len(txt_files)}")
    print()

    manifest = []
    family_counts = Counter()
    confidence_counts = Counter()
    warning_counts = Counter()

    for txt_path in txt_files:
        row = probe_guide(txt_path)
        manifest.append(row)
        family_counts[row["likely_guide_family"]] += 1
        confidence_counts[row["parseability_confidence"]] += 1
        for w in row["warnings"]:
            warning_counts[w] += 1
        status = f"[{row['parseability_confidence'].upper():6}] {row['inferred_program_code']:20} " \
                 f"fam={row['likely_guide_family']}"
        if row["warnings"] or row["irregularities"]:
            status += f"  ⚠ {len(row['warnings'])}W {len(row['irregularities'])}I"
        print(status)

    print()

    # ── Write guide_manifest.json ────────────────────────────────────────────
    manifest_path = DATA_DIR / "guide_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Wrote: {manifest_path}  ({len(manifest)} rows)")

    # ── Write section_presence_matrix.csv ───────────────────────────────────
    matrix_path = DATA_DIR / "section_presence_matrix.csv"
    fieldnames = (
        ["program_code", "likely_guide_family", "parseability_confidence",
         "page_count", "standard_path_row_count", "competency_trigger_count",
         "competency_bullet_count"]
        + PRESENCE_FIELDS
    )
    with open(matrix_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in sorted(manifest, key=lambda r: (r["likely_guide_family"], r["inferred_program_code"])):
            flat = {k: v for k, v in row.items()}
            flat["program_code"] = flat["inferred_program_code"]
            w.writerow(flat)
    print(f"Wrote: {matrix_path}")

    # ── Write manifest_summary.json ──────────────────────────────────────────
    total = len(manifest)
    summary = {
        "total_guides": total,
        "by_family": dict(family_counts.most_common()),
        "by_confidence": dict(confidence_counts.most_common()),
        "universal_sections": {
            field: sum(1 for r in manifest if r[field]) == total
            for field in PRESENCE_FIELDS
        },
        "section_coverage": {
            field: {
                "present": sum(1 for r in manifest if r[field]),
                "absent": sum(1 for r in manifest if not r[field]),
                "pct": round(100 * sum(1 for r in manifest if r[field]) / total, 1),
            }
            for field in PRESENCE_FIELDS
        },
        "common_warnings": dict(warning_counts.most_common(10)),
        "outliers": [
            r["inferred_program_code"]
            for r in manifest
            if r["parseability_confidence"] == "low"
        ],
        "guides_with_variant_headings": [
            {"code": r["inferred_program_code"], "headings": r["variant_headings_found"]}
            for r in manifest
            if r["variant_headings_found"]
        ],
    }
    summary_path = DATA_DIR / "manifest_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Wrote: {summary_path}")

    # ── Console summary ──────────────────────────────────────────────────────
    print()
    print("=== Manifest summary ===")
    print(f"  Total guides:   {total}")
    print(f"  By confidence:  {dict(confidence_counts.most_common())}")
    print(f"  By family:")
    for fam, n in family_counts.most_common():
        print(f"    {fam:30} {n}")
    if summary["outliers"]:
        print(f"  Low-confidence guides: {summary['outliers']}")
    if summary["guides_with_variant_headings"]:
        print(f"  Guides with variant headings:")
        for item in summary["guides_with_variant_headings"]:
            print(f"    {item['code']}: {item['headings']}")


if __name__ == "__main__":
    main()
