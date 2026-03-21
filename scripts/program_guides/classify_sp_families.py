"""
classify_sp_families.py

Phase 3 of guide targets extraction: Standard Path family and track structure classification.

Reads all data/program_guides/parsed/*.json and classifies each program's
standard_path into one of four categories:
  A: structured-term-path      — all courses have populated term numbers
  B: null-term-advisor-path    — all courses have term: null
  C: track-specialization-member — program is one track of a multi-track family
  D: anomalous-suppress        — SP malformed (concatenated titles, etc.)

Also builds a family grouping table for Category C programs.

Inputs:
  data/program_guides/parsed/*_parsed.json

Outputs:
  data/program_guides/sp_family_classification.json
  data/program_guides/sp_families.json
"""

import json
import os
import re
from datetime import date
from collections import defaultdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARSED_DIR = os.path.join(REPO_ROOT, "data", "program_guides", "parsed")
OUTPUT_CLASSIFICATION = os.path.join(REPO_ROOT, "data", "program_guides", "sp_family_classification.json")
OUTPUT_FAMILIES = os.path.join(REPO_ROOT, "data", "program_guides", "sp_families.json")

# ---------------------------------------------------------------------------
# Anomaly thresholds
# ---------------------------------------------------------------------------

# SP entry title length threshold for anomaly detection
ANOMALY_TITLE_LENGTH = 150

# ---------------------------------------------------------------------------
# Known family definitions (from GUIDE_TARGETS_EXTRACTION_PLAN.md Section 3)
# ---------------------------------------------------------------------------

# Family definitions: family_code → {label, type, member_prefixes, member_codes}
# member_codes: explicit list of program codes that belong to this family
KNOWN_FAMILIES = {
    "BSSWE": {
        "family_code": "BSSWE",
        "family_label": "B.S. Software Engineering",
        "family_type": "track_specialization",
        "members_explicit": ["BSSWE_C", "BSSWE_Java"],
        "track_labels": {"BSSWE_C": "C# Track", "BSSWE_Java": "Java Track"},
        "sp_relationship": "shared_core_diverging_track",
        "display_recommendation": "surface family relationship on both degree pages; link to each track as variant",
    },
    "MACC": {
        "family_code": "MACC",
        "family_label": "Master of Accounting",
        "family_type": "track_specialization",
        "member_prefix": "MACC",
        "members_explicit": ["MACCA", "MACCF", "MACCM", "MACCT"],
        "track_labels": {
            "MACCA": "Auditing Track",
            "MACCF": "Financial Reporting Track",
            "MACCM": "Management Accounting Track",
            "MACCT": "Taxation Track",
        },
        "sp_relationship": "shared_foundation_diverging_track",
        "display_recommendation": "surface family relationship on all four degree pages; shared 5-course foundation identified",
    },
    "MSRNN": {
        "family_code": "MSRNN",
        "family_label": "M.S. Nursing — RN to MSN",
        "family_type": "specialization",
        "member_prefix": "MSRNN",
        "members_explicit": ["MSRNNUED", "MSRNNULM", "MSRNNUNI"],
        "track_labels": {
            "MSRNNUED": "Education Specialization",
            "MSRNNULM": "Leadership and Management Specialization",
            "MSRNNUNI": "Nursing Informatics Specialization",
        },
        "sp_relationship": "shared_core_diverging_specialization",
        "display_recommendation": "surface family relationship on all three degree pages; note degree_title truncation (cosmetic)",
    },
    "BSCNE": {
        "family_code": "BSCNE",
        "family_label": "B.S. Cloud and Network Engineering",
        "family_type": "vendor_track",
        "member_prefix": "BSCNE",
        "members_explicit": ["BSCNE", "BSCNEAWS", "BSCNEAZR", "BSCNECIS"],
        "track_labels": {
            "BSCNE": "Vendor-Agnostic Track",
            "BSCNEAWS": "AWS Track",
            "BSCNEAZR": "Azure Track",
            "BSCNECIS": "Cisco Track",
        },
        "sp_relationship": "shared_core_diverging_vendor_track",
        "display_recommendation": "surface family relationship on all four degree pages; note shared core + vendor-specific divergence",
    },
    "PMCNU": {
        "family_code": "PMCNU",
        "family_label": "Post-Master's Certificate, Nursing",
        "family_type": "specialization",
        "member_prefix": "PMCNU",
        "members_explicit": ["PMCNUED", "PMCNUFNP", "PMCNULM", "PMCNUPMHNP"],
        "track_labels": {
            "PMCNUED": "Nursing Education",
            "PMCNUFNP": "Family Nurse Practitioner",
            "PMCNULM": "Leadership and Management",
            "PMCNUPMHNP": "Psychiatric Mental Health Nurse Practitioner",
        },
        "sp_relationship": "parallel_specialization_short_sp",
        "display_recommendation": "surface family relationship; each cert is a distinct specialization on the same base credential",
    },
    "BAELED": {
        "family_code": "BAELED",
        "family_label": "B.A., Elementary Education",
        "family_type": "licensure_variant",
        "members_explicit": ["BAELED", "BAESELED"],
        "track_labels": {
            "BAELED": "Licensure variant (advisor-sequenced)",
            "BAESELED": "Educational Studies non-licensure (term-sequenced)",
        },
        "sp_relationship": "structural_variant",
        "display_recommendation": "show both with explicit labels; SP term status IS the distinguishing signal between licensure and non-licensure",
    },
    "MSMK": {
        "family_code": "MSMK",
        "family_label": "M.S. Marketing",
        "family_type": "specialization",
        "member_prefix": "MSMK",
        "members_explicit": ["MSMK", "MSMKA"],
        "track_labels": {
            "MSMK": "Digital Marketing Specialization",
            "MSMKA": "Marketing Analytics Specialization",
        },
        "sp_relationship": "parallel_specialization",
        "display_recommendation": "surface family relationship on both degree pages",
    },
}

# Programs that are in known families with their family code
PROGRAM_FAMILY_MAP = {}
for family_code, fdef in KNOWN_FAMILIES.items():
    for prog in fdef.get("members_explicit", []):
        PROGRAM_FAMILY_MAP[prog] = family_code

# Track/specialization declaration patterns in program_description
TRACK_TRIGGER_PATTERNS = [
    re.compile(r'\b(two|three|four|five|multiple)\s+tracks?\b', re.IGNORECASE),
    re.compile(r'option to pursue', re.IGNORECASE),
    re.compile(r'offered in\s+\w+\s+tracks?', re.IGNORECASE),
    re.compile(r'specialization(s)?\s+(options?|tracks?)', re.IGNORECASE),
    re.compile(r'RN.to.MSN track', re.IGNORECASE),
]


def extract_track_declaration(desc: str) -> str | None:
    """Extract the track-declaration sentence from program_description."""
    if not desc:
        return None
    sentences = re.split(r'(?<=[.!?])\s+', desc)
    for s in sentences:
        for pattern in TRACK_TRIGGER_PATTERNS:
            if pattern.search(s):
                return s.strip()[:300]
    return None


def classify_sp(program_code: str, sp: list, program_description: str) -> dict:
    """
    Classify a program's standard_path into category A/B/C/D.
    Returns a classification record dict.
    """
    sp_length = len(sp)
    family_code = PROGRAM_FAMILY_MAP.get(program_code)

    # --- Check for anomalies (Category D) first ---
    anomalous_entries = [e for e in sp if len(str(e.get("title", ""))) > ANOMALY_TITLE_LENGTH]
    if anomalous_entries:
        return {
            "program_code": program_code,
            "sp_category": "D",
            "sp_category_label": "anomalous-suppress",
            "sp_length": sp_length,
            "term_status": "anomalous",
            "family_code": family_code,
            "anomaly_entry_count": len(anomalous_entries),
            "longest_title_length": max(len(str(e.get("title", ""))) for e in anomalous_entries),
            "notes": f"{len(anomalous_entries)} SP entries with title >150 chars (concatenation artifact)",
            "track_declaration": None,
        }

    # --- Special case: MSCSUG — bridge program, treat as structured-term but with caveat ---
    if program_code == "MSCSUG":
        has_terms = any(e.get("term") is not None for e in sp)
        return {
            "program_code": program_code,
            "sp_category": "A",
            "sp_category_label": "structured-term-path",
            "sp_length": sp_length,
            "term_status": "populated",
            "family_code": family_code,
            "anomaly_entry_count": 0,
            "longest_title_length": max((len(str(e.get("title", ""))) for e in sp), default=0),
            "notes": "Accelerated B.S./M.S. bridge pathway — SP term sequence spans both degree levels. Display with caveat label.",
            "track_declaration": None,
        }

    # --- Category B: all terms null ---
    all_null = all(e.get("term") is None for e in sp) if sp else False
    has_terms = any(e.get("term") is not None for e in sp) if sp else False

    if all_null:
        track_decl = extract_track_declaration(program_description)
        # Even if null-term, can still be part of a family
        return {
            "program_code": program_code,
            "sp_category": "B",
            "sp_category_label": "null-term-advisor-path",
            "sp_length": sp_length,
            "term_status": "null",
            "family_code": family_code,
            "anomaly_entry_count": 0,
            "longest_title_length": max((len(str(e.get("title", ""))) for e in sp), default=0),
            "notes": "All SP terms null. Display as ordered course list with advisor-sequenced label.",
            "track_declaration": track_decl,
        }

    # --- Category C: track/specialization member ---
    if family_code and family_code in KNOWN_FAMILIES:
        fdef = KNOWN_FAMILIES[family_code]
        track_label = fdef.get("track_labels", {}).get(program_code)
        track_decl = extract_track_declaration(program_description)
        # Only mark as C if the family is a track/specialization type (not structural variant)
        if fdef.get("family_type") in ("track_specialization", "vendor_track", "specialization"):
            return {
                "program_code": program_code,
                "sp_category": "C",
                "sp_category_label": "track-specialization-member",
                "sp_length": sp_length,
                "term_status": "populated" if has_terms else "null",
                "family_code": family_code,
                "track_label": track_label,
                "anomaly_entry_count": 0,
                "longest_title_length": max((len(str(e.get("title", ""))) for e in sp), default=0),
                "notes": f"Member of {family_code} family. Track: {track_label}.",
                "track_declaration": track_decl,
            }

    # --- Category A: structured term path ---
    if has_terms:
        # Check if this program is part of a licensure variant family (still Cat A)
        notes = None
        if family_code == "BAELED":
            notes = "Non-licensure variant — structured term path (contrast with BAELED null-term licensure variant)"
        return {
            "program_code": program_code,
            "sp_category": "A",
            "sp_category_label": "structured-term-path",
            "sp_length": sp_length,
            "term_status": "populated",
            "family_code": family_code,
            "anomaly_entry_count": 0,
            "longest_title_length": max((len(str(e.get("title", ""))) for e in sp), default=0),
            "notes": notes,
            "track_declaration": None,
        }

    # Fallback — has SP but neither all-null nor any terms
    return {
        "program_code": program_code,
        "sp_category": "D",
        "sp_category_label": "anomalous-suppress",
        "sp_length": sp_length,
        "term_status": "mixed",
        "family_code": family_code,
        "anomaly_entry_count": 0,
        "longest_title_length": max((len(str(e.get("title", ""))) for e in sp), default=0),
        "notes": "SP has mixed null/populated terms — unexpected structure",
        "track_declaration": None,
    }


def compute_shared_courses(programs: list[str], parsed_dir: str) -> int:
    """Compute the number of SP course titles shared across all programs in a family."""
    if len(programs) < 2:
        return 0
    sets = []
    for prog in programs:
        fname = os.path.join(parsed_dir, f"{prog}_parsed.json")
        if not os.path.exists(fname):
            return 0
        d = json.load(open(fname))
        sp = d.get("standard_path", []) or []
        titles = {e.get("title", "").strip().lower() for e in sp if e.get("title")}
        sets.append(titles)
    shared = sets[0]
    for s in sets[1:]:
        shared = shared & s
    return len(shared)


def main():
    print("Phase 3: SP family classification")
    print(f"  Parsed dir: {PARSED_DIR}")

    parsed_files = sorted(f for f in os.listdir(PARSED_DIR) if f.endswith("_parsed.json"))
    print(f"  Parsed files: {len(parsed_files)}")

    classifications = []
    category_counts = {"A": 0, "B": 0, "C": 0, "D": 0}

    for fname in parsed_files:
        program_code = fname.replace("_parsed.json", "")
        data = json.load(open(os.path.join(PARSED_DIR, fname)))
        sp = data.get("standard_path", []) or []
        program_description = data.get("program_description", "") or ""

        rec = classify_sp(program_code, sp, program_description)
        classifications.append(rec)
        category_counts[rec["sp_category"]] += 1

    # Sort by category then program code
    classifications.sort(key=lambda r: (r["sp_category"], r["program_code"]))

    print(f"\n  Category A (structured-term-path): {category_counts['A']}")
    print(f"  Category B (null-term-advisor-path): {category_counts['B']}")
    print(f"  Category C (track-specialization-member): {category_counts['C']}")
    print(f"  Category D (anomalous-suppress): {category_counts['D']}")
    print(f"  Total: {sum(category_counts.values())}")

    # Print Cat D
    cat_d = [r for r in classifications if r["sp_category"] == "D"]
    print(f"\n  Category D programs:")
    for r in cat_d:
        print(f"    {r['program_code']}: {r['notes']}")

    # Print Cat C families
    cat_c = [r for r in classifications if r["sp_category"] == "C"]
    by_family = defaultdict(list)
    for r in cat_c:
        by_family[r["family_code"]].append(r["program_code"])
    print(f"\n  Category C families:")
    for fc, members in sorted(by_family.items()):
        print(f"    {fc}: {members}")

    # Build sp_families.json with enriched family definitions
    families = []
    for family_code, fdef in KNOWN_FAMILIES.items():
        members_explicit = fdef.get("members_explicit", [])
        # Check which members actually exist in the corpus
        existing_members = [m for m in members_explicit
                            if os.path.exists(os.path.join(PARSED_DIR, f"{m}_parsed.json"))]

        # Get track declarations from program descriptions
        declarations = []
        for prog in existing_members:
            d = json.load(open(os.path.join(PARSED_DIR, f"{prog}_parsed.json")))
            decl = extract_track_declaration(d.get("program_description", "") or "")
            if decl:
                declarations.append({"program_code": prog, "text": decl})
                break  # One declaration per family is enough

        # Compute shared course count
        shared_count = compute_shared_courses(existing_members, PARSED_DIR)

        family_members = []
        for prog in existing_members:
            family_members.append({
                "program_code": prog,
                "track_label": fdef.get("track_labels", {}).get(prog),
            })

        families.append({
            "family_code": family_code,
            "family_label": fdef["family_label"],
            "family_type": fdef["family_type"],
            "declaration_text": declarations[0]["text"] if declarations else None,
            "declaration_source_program": declarations[0]["program_code"] if declarations else None,
            "members": family_members,
            "member_count": len(existing_members),
            "sp_relationship": fdef["sp_relationship"],
            "shared_course_count": shared_count,
            "display_recommendation": fdef["display_recommendation"],
        })

    families.sort(key=lambda f: f["family_code"])

    print(f"\n  Families built: {len(families)}")
    for f in families:
        print(f"    {f['family_code']}: {f['member_count']} members, {f['shared_course_count']} shared SP courses")

    # Build output artifacts
    classification_output = {
        "generated_on": str(date.today()),
        "source": "data/program_guides/parsed/*_parsed.json",
        "total_programs": len(classifications),
        "category_counts": category_counts,
        "anomaly_title_threshold": ANOMALY_TITLE_LENGTH,
        "classifications": classifications,
    }

    families_output = {
        "generated_on": str(date.today()),
        "source": "data/program_guides/parsed/*_parsed.json",
        "total_families": len(families),
        "families": families,
    }

    os.makedirs(os.path.dirname(OUTPUT_CLASSIFICATION), exist_ok=True)
    with open(OUTPUT_CLASSIFICATION, "w") as f:
        json.dump(classification_output, f, indent=2)
    print(f"\n  Output: {OUTPUT_CLASSIFICATION}")

    with open(OUTPUT_FAMILIES, "w") as f:
        json.dump(families_output, f, indent=2)
    print(f"  Output: {OUTPUT_FAMILIES}")


if __name__ == "__main__":
    main()
