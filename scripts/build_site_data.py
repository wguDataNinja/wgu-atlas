"""
build_site_data.py
==================
Builds all four site-ready data artifacts for the WGU catalog history website.

Steps:
  1. Title variant classification
  2. Canonical course intelligence table (CSV + JSON)
  3. Named event layer (CSV + JSON)
  4. Static site-ready JSON exports

Usage (from wgu-atlas repo):
  WGU_REDDIT_PATH=/path/to/wgu-reddit/WGU_catalog/outputs \
  WGU_ATLAS_DATA=/path/to/wgu-atlas/data \
  python3 scripts/build_site_data.py

Environment variables:
  WGU_REDDIT_PATH  Path to the wgu-reddit WGU_catalog/outputs/ directory
                   (contains change_tracking/, trusted/, edition_diffs/, helpers/)
  WGU_ATLAS_DATA   Path to the wgu-atlas output root
                   Defaults to ../data relative to this script

Note: The v1 site build does NOT require running this script.
Pre-generated exports are committed in public/data/. Re-run only when
new catalog data has been processed in the wgu-reddit repo.

Note on course_index_v10.json: This 59 MB file (in helpers/) must exist
in the wgu-reddit outputs directory at runtime. It is not committed to git.
Runtime is approximately 30-60 seconds, dominated by loading that file.
"""

import csv
import json
import os
import re
import unicodedata
from collections import defaultdict, Counter

# ---------------------------------------------------------------------------
# Paths — configurable via environment variables
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT  = os.path.dirname(_SCRIPT_DIR)

# Upstream: wgu-reddit WGU_catalog/outputs/
BASE  = os.environ.get("WGU_REDDIT_PATH",
                       os.path.join(_SCRIPT_DIR, "outputs"))  # fallback for local runs
TRUST = os.path.join(BASE, "trusted", "2026_03")
CT    = os.path.join(BASE, "change_tracking")
ED    = os.path.join(BASE, "edition_diffs")
HELP  = os.path.join(BASE, "helpers")

# Output: wgu-atlas data/
_ATLAS_DATA = os.environ.get("WGU_ATLAS_DATA",
                              os.path.join(_REPO_ROOT, "data"))
OUT  = _ATLAS_DATA
EXP  = os.path.join(_REPO_ROOT, "public", "data")
CDIR = os.path.join(EXP, "courses")

for d in [OUT, EXP, CDIR]:
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return path

def write_json(path, obj, indent=2):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)
    return path

# ---------------------------------------------------------------------------
# Load source data
# ---------------------------------------------------------------------------
print("Loading source data...")
course_hist_rows = load_csv(os.path.join(CT, "course_history.csv"))
prog_hist_rows   = load_csv(os.path.join(CT, "program_history.csv"))
courses_2026     = load_csv(os.path.join(TRUST, "courses_2026_03.csv"))
certs_2026       = load_csv(os.path.join(TRUST, "certs_2026_03.csv"))
diffs_full       = load_json(os.path.join(ED,  "edition_diffs_full.json"))
events_raw       = load_json(os.path.join(ED,  "edition_diffs_events.json"))
course_index     = load_json(os.path.join(HELP, "course_index_v10.json"))
summary_stats    = load_json(os.path.join(CT,  "summary_stats.json"))

# Index lookups
course_hist = {r["course_code"]: r for r in course_hist_rows}
prog_hist   = {r["program_code"]: r for r in prog_hist_rows}
courses2026_by_code = {r["course_code"]: r for r in courses_2026}
certs2026_by_code   = {r["course_code"]: r for r in certs_2026}

# Active AP codes in 2026-03
active_ap_codes = set(courses2026_by_code.keys())
active_cert_codes = set(certs2026_by_code.keys())

# Collect genuine title changes and truncation artifacts per code
genuine_changes_by_code  = defaultdict(list)  # code -> [{transition,from,to}]
truncation_codes = set()

for d in diffs_full:
    tr = f"{d['from_catalog']}→{d['to_catalog']}"
    for ch in d.get("courses_with_title_changes", []):
        genuine_changes_by_code[ch["code"]].append({
            "transition": tr,
            "from_title": ch["from_title"],
            "to_title":   ch["to_title"]
        })
    for ch in d.get("courses_with_title_truncations", []):
        truncation_codes.add(ch["code"])

# All unique observed titles per code from course_index
observed_titles_by_code = {}
for code, entry in course_index.items():
    titles = set()
    for inst in entry.get("instances", []):
        raw = inst.get("raw", "")
        # Title is between the 3rd token group (code) and the trailing "CUS TERM"
        # Simpler: just use canonical and what changed
        titles.add(entry["canonical_title"])
    # Also pull from history
    if code in course_hist:
        h = course_hist[code]
        titles.add(h["canonical_title"])
        if h.get("title_variants"):
            for tv in h["title_variants"].split(" | "):
                if tv.strip():
                    titles.add(tv.strip())
    observed_titles_by_code[code] = sorted(titles)

# ---------------------------------------------------------------------------
# STEP 1 — Title variant classification
# ---------------------------------------------------------------------------
print("\n=== STEP 1: Title variant classification ===")

def unicode_normalize(s):
    """Replace smart quotes/dashes with ASCII equivalents."""
    return (s.replace("\u2019", "'").replace("\u2018", "'")
             .replace("\u201c", '"').replace("\u201d", '"')
             .replace("\u2013", "-").replace("\u2014", "--"))

def whitespace_normalize(s):
    return re.sub(r"\s+", " ", s.strip()).lower()

def punct_normalize(s):
    """Remove punctuation differences: hyphens, commas, & → and, em-dashes."""
    s = s.lower()
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"\bpre-clinical\b", "preclinical", s)
    s = re.sub(r" & ", " and ", s)
    # Remove all hyphens
    s = s.replace("-", " ")
    # Remove serial commas differences — strip all commas
    s = s.replace(",", "")
    return re.sub(r"\s+", " ", s).strip()

def classify_variant_pair(a, b):
    """
    Return the classification of the difference between title strings a and b.
    Returns one of the schema values or None if identical.
    """
    if a == b:
        return None

    # Unicode normalization check
    ua, ub = unicode_normalize(a), unicode_normalize(b)
    if ua == ub:
        return "extraction_noise"

    # Whitespace-only diff
    wa, wb = whitespace_normalize(a), whitespace_normalize(b)
    if wa == wb:
        return "formatting_only"
    if unicode_normalize(wa) == unicode_normalize(wb):
        return "extraction_noise"

    # Punctuation normalization check
    pa, pb = punct_normalize(wa), punct_normalize(wb)
    if pa == pb:
        return "punctuation_only"

    # Truncation check (shorter is strict prefix of longer normalized)
    srt, lng = (wa, wb) if len(wa) <= len(wb) else (wb, wa)
    if lng.startswith(srt) and len(lng) > len(srt) + 3:
        return "extraction_noise"  # line-wrap artifact

    # Word-level similarity
    words_a = set(wa.split())
    words_b = set(wb.split())
    union = words_a | words_b
    inter = words_a & words_b
    jaccard = len(inter) / len(union) if union else 1.0

    if jaccard >= 0.75:
        return "wording_refinement"
    elif jaccard >= 0.4:
        return "substantive_change"
    else:
        return "unresolved"

# Priority ordering for merging multiple variant pairs
CLASS_PRIORITY = [
    "extraction_noise",   # lowest — we handle these separately
    "formatting_only",
    "punctuation_only",
    "abbreviation_change",
    "wording_refinement",
    "substantive_change",
    "unresolved",
]
# We want the MOST SEVERE class to win when multiple pairs exist
# (except extraction_noise which is structural, not semantic)
SEMANTIC_PRIORITY = [
    "unresolved",
    "substantive_change",
    "wording_refinement",
    "abbreviation_change",
    "punctuation_only",
    "formatting_only",
    "extraction_noise",
]

def dominant_class(classes):
    """Return the most severe non-None class from a list."""
    for cls in SEMANTIC_PRIORITY:
        if cls in classes:
            return cls
    return "unresolved"

# Hand-coded overrides for known edge cases
MANUAL_OVERRIDES = {
    # These back-and-forth oscillations in adjacent months are catalog noise
    "C764": {
        "class":             "formatting_only",
        "notes":             "Missing space between ')' and 'Teacher' in some extractions ('...Physics)Teacher Performance' vs '...Physics) Teacher Performance'). One variant is also a truncated form ('...Physics)Teach'). Core difference is a space insertion — formatting_only. Retired course.",
        "manual_review_needed": False,
    },
    "C820": {
        "class":             "extraction_noise",
        "notes":             "Title oscillated 'Professional Leadership and Communication for Healthcare' ↔ 'Inter-professional Communication and Leadership in Healthcare' across Oct→Nov 2017 in adjacent catalog editions; reverted by Nov 2017. Consistent with a brief catalog edit that was rolled back.",
        "manual_review_needed": False,
    },
    "D344": {
        "class":             "extraction_noise",
        "notes":             "Three title strings observed, all truncated at different points due to PDF line-wrap. Canonical is itself a truncation artifact ('of Psychiatric Nurse' cuts off mid-phrase). All variants shorter than or mismatched from canonical by wrap boundary.",
        "manual_review_needed": True,
    },
    "D346": {
        "class":             "substantive_change",
        "notes":             "Genuine rename: 'Advanced Psychological Care...' → 'Advanced Psychiatric Mental Health Care...'. The to-title strings are truncated (PDF line-wrap) but the 'Psychological' → 'Psychiatric Mental Health' word change is confirmed across 2022-12→2023-01.",
        "manual_review_needed": False,
    },
    "D347": {
        "class":             "substantive_change",
        "notes":             "Genuine rename: 'Advanced Psychological Care...' → 'Advanced Psychiatric Mental Health Care...'. To-title truncated at line-wrap boundary but core rename is confirmed across 2022-12→2023-01.",
        "manual_review_needed": False,
    },
    "D396": {
        "class":             "wording_refinement",
        "notes":             "Typo correction: 'Evidenced-Based' → 'Evidence-Based' (grammatically correct form). Transition confirmed in 2023-01→2023-02. Current 2026-03 catalog extraction is truncated ('Evidence-Based Practice for Health and'); full title is 'Evidence-Based Practice for Health and Human Services' — use the full form from history.",
        "manual_review_needed": False,
    },
    "D480": {
        "class":             "extraction_noise",
        "notes":             "Title oscillated 'Software Design and Quality Assurance' ↔ 'Software Quality Assurance' across Jan→Feb→Mar 2023 in adjacent editions; reverted. Consistent with a brief catalog edit that was rolled back.",
        "manual_review_needed": False,
    },
    "D578": {
        "class":             "wording_refinement",
        "notes":             "Title shortened from 'Capstone for BS in Psychology' to 'Capstone in Psychology' (transition 2024-02→2024-03). Same course concept, title simplified. Current title 'Capstone in Psychology' confirmed in 2026-03.",
        "manual_review_needed": False,
    },
    "D601": {
        "class":             "wording_refinement",
        "notes":             "Synonym substitution: 'Data Storytelling for Diverse Audiences' → 'Data Storytelling for Varied Audiences' (transition 2024-07→2024-08). Semantically equivalent; 'Varied' replaces 'Diverse'. Current title 'Data Storytelling for Varied Audiences' confirmed in 2026-03.",
        "manual_review_needed": False,
    },
}

# Build classification rows for codes with title_variant_count > 0
tv_rows = []
for row in course_hist_rows:
    code = row["course_code"]
    tv_count = int(row.get("title_variant_count", 0))
    if tv_count == 0:
        continue

    canonical = row["canonical_title"]
    variants_raw = row.get("title_variants", "")
    variant_list = [v.strip() for v in variants_raw.split(" | ") if v.strip()]
    all_observed = sorted(set([canonical] + variant_list))

    # Use manual override if available
    if code in MANUAL_OVERRIDES:
        ov = MANUAL_OVERRIDES[code]
        tv_class = ov["class"]
        notes    = ov["notes"]
        manual_review = ov.get("manual_review_needed", False)
        confidence = "high" if not manual_review else "moderate"
    else:
        # Classify by comparing each variant to canonical
        pair_classes = set()
        for v in variant_list:
            cls = classify_variant_pair(canonical, v)
            if cls:
                pair_classes.add(cls)

        # Also factor in genuine_changes evidence
        if code in genuine_changes_by_code:
            for ch in genuine_changes_by_code[code]:
                cls = classify_variant_pair(ch["from_title"], ch["to_title"])
                if cls:
                    pair_classes.add(cls)

        if not pair_classes:
            pair_classes = {"unresolved"}

        # If ALL variants are in truncation_codes and no genuine changes → extraction_noise
        if code in truncation_codes and code not in genuine_changes_by_code:
            pair_classes = {"extraction_noise"}
            tv_class = "extraction_noise"
            notes = "PDF line-wrap artifact: shorter variant is a strict prefix of the canonical title."
            manual_review = False
            confidence = "high"
        elif code in truncation_codes and code in genuine_changes_by_code:
            # Mixed: truncation + genuine change
            genuine_cls = dominant_class(pair_classes - {"extraction_noise"})
            tv_class = genuine_cls if genuine_cls != "unresolved" else "unresolved"
            notes = f"Both PDF truncation artifacts and a genuine title transition detected. Classified as {tv_class} for the genuine change; extraction_noise variants excluded."
            manual_review = (tv_class in ("unresolved", "substantive_change"))
            confidence = "moderate" if tv_class != "unresolved" else "low"
        else:
            tv_class = dominant_class(pair_classes)
            notes = ""
            manual_review = tv_class in ("unresolved", "substantive_change")
            confidence = "high" if tv_class in ("punctuation_only", "formatting_only", "extraction_noise") else \
                         "moderate" if tv_class in ("wording_refinement", "abbreviation_change") else "low"

    tv_rows.append({
        "course_code":            code,
        "canonical_title_current": canonical,
        "observed_titles":        " | ".join(all_observed),
        "title_variant_class":    tv_class,
        "variant_count":          tv_count,
        "in_genuine_changes":     (code in genuine_changes_by_code),
        "in_truncation_set":      (code in truncation_codes),
        "genuine_change_detail":  "; ".join(
            f"[{c['transition']}] '{c['from_title']}' → '{c['to_title']}'"
            for c in genuine_changes_by_code.get(code, [])
        ),
        "notes":                  notes,
        "confidence":             confidence,
        "manual_review_needed":   manual_review,
    })

# Sort by class severity for readability
CLASS_ORDER = {c: i for i, c in enumerate(SEMANTIC_PRIORITY)}
tv_rows.sort(key=lambda r: (CLASS_ORDER.get(r["title_variant_class"], 99), r["course_code"]))

TVC_FIELDS = [
    "course_code", "canonical_title_current", "observed_titles",
    "title_variant_class", "variant_count",
    "in_genuine_changes", "in_truncation_set", "genuine_change_detail",
    "notes", "confidence", "manual_review_needed",
]
p = write_csv(os.path.join(OUT, "title_variant_classification.csv"), tv_rows, TVC_FIELDS)
print(f"  → {p}")

# Build summary
tv_by_class = Counter(r["title_variant_class"] for r in tv_rows)
tv_summary = {
    "total_codes_with_variants":  len(tv_rows),
    "counts_by_class":            dict(tv_by_class.most_common()),
    "manual_review_needed_count": sum(1 for r in tv_rows if r["manual_review_needed"]),
    "substantive_change_codes":   sorted(r["course_code"] for r in tv_rows if r["title_variant_class"] == "substantive_change"),
    "manual_review_codes":        sorted(r["course_code"] for r in tv_rows if r["manual_review_needed"]),
    "method_notes": [
        "extraction_noise: PDF line-wrap truncations (shorter is strict prefix of longer) OR Unicode quote differences OR catalog oscillations that reverted within 1-2 editions",
        "formatting_only:  whitespace differences only",
        "punctuation_only: differences in hyphens, commas, em-dashes, '&' vs 'and'",
        "wording_refinement: typo corrections, synonym swaps, minor rewordings preserving core meaning",
        "substantive_change: genuine semantic rename with meaningfully different wording",
        "unresolved: insufficient evidence to classify confidently",
        "Codes appearing in edition_diffs truncation set are classified extraction_noise unless a genuine change is also confirmed"
    ]
}
write_json(os.path.join(OUT, "title_variant_summary.json"), tv_summary)
print(f"  Classified {len(tv_rows)} codes. Counts: {dict(tv_by_class.most_common())}")
print(f"  Substantive changes: {tv_summary['substantive_change_codes']}")
print(f"  Manual review needed: {tv_summary['manual_review_needed_count']} codes")

# Build lookup for step 2
tvc_by_code = {r["course_code"]: r for r in tv_rows}

# ---------------------------------------------------------------------------
# STEP 2 — Canonical course intelligence table
# ---------------------------------------------------------------------------
print("\n=== STEP 2: Canonical course intelligence table ===")

# Definitions
# ghost_flag: RETIRED AND edition_count <= 3 AND span_months <= 5
#   Captures courses that appeared briefly and suggest a catalog error or experimental entry.
#   Excludes the large batch of AXX-format codes retired in 2017-07 (those are structural).
# single_appearance_flag: edition_count == 1
# stability_class:
#   perpetual  — appeared in all 108 editions (the 113 assessment codes)
#   stable     — edition_count >= 50
#   moderate   — edition_count 10–49
#   ephemeral  — edition_count 2–9
#   single     — edition_count == 1

TOTAL_EDITIONS = 108

def stability_class(edition_count):
    n = int(edition_count)
    if n >= TOTAL_EDITIONS:
        return "perpetual"
    elif n >= 50:
        return "stable"
    elif n >= 10:
        return "moderate"
    elif n >= 2:
        return "ephemeral"
    else:
        return "single"

def ghost_flag(row):
    """
    Flags courses that appeared only once or twice and then vanished,
    suggesting a catalog error, experiment, or course that never fully launched.
    Threshold: RETIRED AND edition_count <= 2.
    Deliberately excludes the well-documented AXX/legacy code waves from 2017
    (those had edition_count >= 3 and represent a known structural event, not ghosts).
    """
    if row["status"] != "RETIRED":
        return False
    n = int(row["edition_count"])
    return n <= 2

# Canonical title overrides: cases where the 2026-03 extraction is a known truncation artifact
# and the full correct title is available from historical data.
CANONICAL_TITLE_OVERRIDES = {
    # 2026-03 extraction is truncated to "Evidence-Based Practice for Health and"
    # Full title confirmed in multiple prior editions: "Evidence-Based Practice for Health and Human Services"
    "D396": "Evidence-Based Practice for Health and Human Services",
}

# Derive current_programs from courses_2026_03.csv
def get_current_programs(code):
    r = courses2026_by_code.get(code)
    if not r:
        return []
    return [p.strip() for p in r.get("programs", "").split(";") if p.strip()]

def get_current_college(code):
    r = courses2026_by_code.get(code)
    if not r:
        return ""
    return r.get("colleges", "")

# Build historical program set from course_index instances
# (degree heading, not program code — that's what we have in instances)
def get_historical_programs(code):
    entry = course_index.get(code, {})
    progs = set()
    for inst in entry.get("instances", []):
        deg = inst.get("degree", "")
        if deg:
            progs.add(deg)
    return sorted(progs)

# Contexts seen: for AP codes only (cert codes handled separately)
# AP codes only appear in academic programs — contexts = "AP"
# If cert codes are added to canonical table, contexts = "cert"

canonical_rows = []
canonical_dict = {}

# --- AP codes ---
for row in course_hist_rows:
    code = row["course_code"]
    h = course_hist.get(code, row)
    tvc = tvc_by_code.get(code, {})

    # Canonical title: use 2026-03 current if active, else course_history canonical
    if code in courses2026_by_code:
        canonical_title = CANONICAL_TITLE_OVERRIDES.get(code, courses2026_by_code[code]["title"])
        active_current = True
    else:
        canonical_title = h["canonical_title"]
        active_current = False

    current_progs = get_current_programs(code) if active_current else []
    hist_progs    = get_historical_programs(code)
    # Historical program count = distinct degree headings seen across all editions
    # (union of current and historical)
    all_prog_set = set(hist_progs) | set(current_progs)

    entry = course_index.get(code, {})
    ed_count = int(h["edition_count"])
    is_ghost  = ghost_flag(h)
    is_single = (ed_count == 1)
    stab = stability_class(ed_count)

    # Observed titles (canonical + variants)
    all_titles = [h["canonical_title"]]
    if h.get("title_variants"):
        for tv in h["title_variants"].split(" | "):
            t = tv.strip()
            if t and t not in all_titles:
                all_titles.append(t)

    # Current title confidence
    if not active_current:
        title_conf = "n/a"
    elif tvc.get("title_variant_class") in ("substantive_change", "unresolved"):
        title_conf = "moderate"
    elif tvc.get("title_variant_class") in ("wording_refinement",):
        title_conf = "high"
    else:
        title_conf = "high"

    rec = {
        "course_code":              code,
        "canonical_title_current":  canonical_title,
        "observed_titles":          " | ".join(all_titles),
        "first_seen_edition":       h["first_seen"],
        "last_seen_edition":        h["last_seen"],
        "active_current":           active_current,
        "contexts_seen":            "AP",
        "current_programs":         "; ".join(current_progs),
        "current_program_count":    len(current_progs),
        "historical_programs":      "; ".join(hist_progs),
        "historical_program_count": len(all_prog_set),
        "edition_count":            ed_count,
        "ghost_flag":               is_ghost,
        "single_appearance_flag":   is_single,
        "stability_class":          stab,
        "title_variant_class":      tvc.get("title_variant_class", "none"),
        "current_title_confidence": title_conf,
        "canonical_cus":            h["canonical_cus"],
        "current_college":          get_current_college(code) if active_current else h.get("colleges", "").split("|")[0].strip(),
        "colleges_seen":            h.get("colleges", ""),
        "notes_confidence":         tvc.get("notes", ""),
    }
    canonical_rows.append(rec)
    canonical_dict[code] = rec

# --- Cert codes ---
for row in certs_2026:
    code = row["course_code"]
    cert_progs = [p.strip() for p in row.get("cert_programs", "").split(";") if p.strip()]
    rec = {
        "course_code":              code,
        "canonical_title_current":  row["title"],
        "observed_titles":          row["title"],
        "first_seen_edition":       "2024-09",   # cert section started 2024-09; we don't track earlier
        "last_seen_edition":        "2026-03",
        "active_current":           True,
        "contexts_seen":            "cert",
        "current_programs":         "; ".join(cert_progs),
        "current_program_count":    len(cert_progs),
        "historical_programs":      "; ".join(cert_progs),
        "historical_program_count": len(cert_progs),
        "edition_count":            "cert_untracked",
        "ghost_flag":               False,
        "single_appearance_flag":   False,
        "stability_class":          "cert_only",
        "title_variant_class":      "none",
        "current_title_confidence": "high",
        "canonical_cus":            row["cus"],
        "current_college":          "Certificates - Standard Paths",
        "colleges_seen":            "Certificates - Standard Paths",
        "notes_confidence":         "Cert section began 2024-09; no cross-edition cert tracking yet. first_seen_edition is the section launch date, not the course introduction date.",
    }
    canonical_rows.append(rec)
    canonical_dict[code] = rec

# Sort: active AP first, then retired AP, then cert
def sort_key(r):
    scope = 0 if r["contexts_seen"] == "AP" else 1
    active = 0 if r["active_current"] else 1
    return (scope, active, r["course_code"])

canonical_rows.sort(key=sort_key)

CC_FIELDS = [
    "course_code", "canonical_title_current", "observed_titles",
    "first_seen_edition", "last_seen_edition",
    "active_current", "contexts_seen",
    "current_programs", "current_program_count",
    "historical_programs", "historical_program_count",
    "edition_count", "ghost_flag", "single_appearance_flag",
    "stability_class", "title_variant_class", "current_title_confidence",
    "canonical_cus", "current_college", "colleges_seen", "notes_confidence",
]
p = write_csv(os.path.join(OUT, "canonical_courses.csv"), canonical_rows, CC_FIELDS)
print(f"  → {p}")

# JSON version
write_json(os.path.join(OUT, "canonical_courses.json"), canonical_dict)
print(f"  → {os.path.join(OUT, 'canonical_courses.json')}")

# Summary counts
ap_active   = sum(1 for r in canonical_rows if r["contexts_seen"] == "AP" and r["active_current"])
ap_retired  = sum(1 for r in canonical_rows if r["contexts_seen"] == "AP" and not r["active_current"])
cert_count  = sum(1 for r in canonical_rows if r["contexts_seen"] == "cert")
ghost_count = sum(1 for r in canonical_rows if r["ghost_flag"])
single_count= sum(1 for r in canonical_rows if r["single_appearance_flag"])
stab_counts = Counter(r["stability_class"] for r in canonical_rows)

print(f"  AP active: {ap_active}, AP retired: {ap_retired}, Cert: {cert_count}")
print(f"  Ghost codes: {ghost_count}, Single-appearance codes: {single_count}")
print(f"  Stability classes: {dict(stab_counts.most_common())}")

# ---------------------------------------------------------------------------
# STEP 3 — Named event layer
# ---------------------------------------------------------------------------
print("\n=== STEP 3: Named event layer ===")

# Event type taxonomy (from SCRAPE_LOG analysis)
EVENT_TYPE_TAXONOMY = {
    "domain_reorganization":        "High program churn; old taxonomy codes retired and new ones added; near-zero version changes",
    "program_family_rebuild":       "Namespace migration; shared core curriculum introduced; near-zero version changes",
    "graduate_specialization_split":"One generic program splits into N subject-specific tracks; new course series introduced",
    "curriculum_version_wave":      "High version changes; near-zero course churn; same-school coordination indicating accreditation or review cycle",
    "rename_cleanup":               "High genuine title-change count; minimal structural change; batch standardization of naming conventions",
    "course_weight_consolidation":  "Old 1-2 CU stub courses replaced by fewer consolidated 3 CU courses on same topics",
    "new_program_family_launch":    "New program code namespace introduced; large new course series accompanying new programs",
    "cert_section_restructuring":   "Certificate programs exit or enter Academic Programs scope; Certificates - Standard Paths section reorganized",
    "school_rename":                "WGU renames a college or school; structural header changes across catalog; no course-content change",
    "composite":                    "Multiple event types fire in the same transition",
}

def infer_event_type(ev, diffs_entry):
    """Infer primary event type from metrics."""
    flags  = ev.get("flags", [])
    pc     = ev.get("program_churn", 0)
    vc     = ev.get("version_changes_count", 0)
    cc     = ev.get("course_churn", 0)
    tc     = ev.get("title_changes_count", 0)
    nac    = ev.get("affected_college_count", len(ev.get("affected_colleges", [])))
    notes  = diffs_entry.get("notes", "") if diffs_entry else ""

    types = []

    if vc >= 10 and cc <= 10:
        types.append("curriculum_version_wave")
    if tc >= 5 and cc <= 20 and pc <= 4:
        types.append("rename_cleanup")
    if pc >= 8 and vc == 0:
        types.append("domain_reorganization")
    if pc >= 8 and vc > 0:
        types.append("program_family_rebuild")
    if pc >= 6 and cc >= 40:
        types.append("new_program_family_launch")
    if "cert" in notes.lower():
        types.append("cert_section_restructuring")

    if len(types) == 0:
        if cc >= 50:
            types.append("program_family_rebuild")
        elif pc >= 4:
            types.append("domain_reorganization")
        elif vc >= 5:
            types.append("curriculum_version_wave")
        else:
            types.append("curriculum_version_wave")

    primary = types[0]
    secondary = types[1] if len(types) > 1 else ""
    if len(types) > 1:
        primary = "composite"
        secondary = ", ".join(types)
    return primary, secondary

# Build diffs_full lookup by transition string
diffs_by_transition = {}
for d in diffs_full:
    key = f"{d['from_catalog']}→{d['to_catalog']}"
    diffs_by_transition[key] = d

# Curated major event set — hand-identified from SCRAPE_LOG narratives
# These are given curated titles and interpreted summaries
CURATED_EVENTS = {
    "2017-01→2017-03": {
        "event_id":         "EVT-001",
        "event_title":      "Pre-Clinical Title Standardization",
        "event_type_primary": "rename_cleanup",
        "event_type_secondary": "",
        "is_curated_major_event": True,
        "observed_summary": "14 genuine title changes; all are 'Pre-Clinical Experiences' → 'Preclinical Experiences' (hyphen removal). 13 program version changes also in this transition.",
        "interpreted_summary": "WGU standardized the hyphenation of 'Preclinical' across all teacher-education preclinical experience course titles. A concurrent wave of 13 program version bumps suggests this was part of a broader Education curriculum review cycle.",
        "confidence": "high",
    },
    "2017-05→2017-07": {
        "event_id":         "EVT-002",
        "event_title":      "2017 Assessment Code Migration and Teacher Program Rationalization",
        "event_type_primary": "composite",
        "event_type_secondary": "domain_reorganization, rename_cleanup",
        "is_curated_major_event": True,
        "observed_summary": "175 course churn (largest in archive): 101 added, 74 removed. 22 program version changes. 7 net program change. Grade-band teacher programs retired; subject-discipline format introduced. Old AXX-format assessment codes retired; C-codes expand.",
        "interpreted_summary": "The single most structurally disruptive transition in the 2017–2026 archive. WGU simultaneously retired the legacy assessment code taxonomy (AXX-format codes such as ABP1, AEP1) and reorganized the Education school from grade-band programs (K-8, 5-12) toward subject-specific teacher programs. The 22 program version changes suggest comprehensive curriculum review coincided with this structural shift.",
        "confidence": "high",
    },
    "2018-04→2018-05": {
        "event_id":         "EVT-003",
        "event_title":      "Education School Domain Reorganization — Grade-Band to Subject-Discipline",
        "event_type_primary": "domain_reorganization",
        "event_type_secondary": "",
        "is_curated_major_event": True,
        "observed_summary": "23 program churn (largest in archive): 11 grade-band teacher programs retired (BASC9, BASCB12, BASCCH12…), 12 new subject-discipline programs added (BSCS, BSSEMG, BSSESB…). 61 course churn, 0 version changes.",
        "interpreted_summary": "WGU reorganized teacher education program structure from grade-band taxonomy (K-9, 5-12 etc.) to subject-discipline taxonomy (Science, Math, Social Studies, etc.). The structural change retired 11 programs and launched 12 replacements. Zero version changes indicates this was a program-taxonomy reorganization rather than a curriculum content revision.",
        "confidence": "high",
    },
    "2018-05→2018-06": {
        "event_id":         "EVT-004",
        "event_title":      "Education School Follow-On Reorganization Wave",
        "event_type_primary": "domain_reorganization",
        "event_type_secondary": "",
        "is_curated_major_event": True,
        "observed_summary": "12 program churn in Education; 4 course churn. Follow-on wave from the April→May 2018 domain reorganization.",
        "interpreted_summary": "Continuation of the 2018 Education school reorganization. Additional programs added and retired in the month immediately following the primary restructuring event, suggesting the April→May reorganization was rolled out in two phases.",
        "confidence": "high",
    },
    "2020-01→2020-02": {
        "event_id":         "EVT-005",
        "event_title":      "Business School Program Family Rebuild (BSBA)",
        "event_type_primary": "program_family_rebuild",
        "event_type_secondary": "",
        "is_curated_major_event": True,
        "observed_summary": "13 program churn in Business only. 41 course churn. 0 version changes. Net program change: Business restructuring.",
        "interpreted_summary": "WGU restructured the Business school program family, retiring older BSBA variants and introducing new program codes with shared core curriculum. The zero version change count is consistent with a namespace migration rather than a content revision — the underlying curriculum may have been unchanged while programs were reorganized.",
        "confidence": "moderate",
    },
    "2020-06→2020-07": {
        "event_id":         "EVT-006",
        "event_title":      "Mid-Archive Curriculum Version Wave — Business, Education, Health",
        "event_type_primary": "curriculum_version_wave",
        "event_type_secondary": "",
        "is_curated_major_event": True,
        "observed_summary": "119 course churn, 18 version changes, 0 program count change. Affects Business, Education, Health schools.",
        "interpreted_summary": "A large curriculum-content refresh wave affecting three schools simultaneously with no structural program additions or removals. The 18 version changes indicate formal curriculum revision across many programs in the same cycle. The 119 course churn with zero program churn suggests course substitutions within existing programs rather than new program launches.",
        "confidence": "high",
    },
    "2022-12→2023-01": {
        "event_id":         "EVT-007",
        "event_title":      "Leavitt School of Health Rename and Curriculum Restructuring",
        "event_type_primary": "composite",
        "event_type_secondary": "school_rename, domain_reorganization",
        "is_curated_major_event": True,
        "observed_summary": "80 course churn, 9 program churn, 2 genuine title changes. Affects Business, Health, Technology. Health school renamed from 'College of Health Professions' to 'Leavitt School of Health' effective this edition.",
        "interpreted_summary": "The Leavitt School of Health rename coincided with significant structural changes in the Health school — 9 program churn and 80 course churn together suggest the rename accompanied a broader health curriculum reorganization rather than being a pure administrative rename. The title changes for D346 and D347 ('Psychological Care' → 'Psychiatric Mental Health Care') reflect genuine course renaming within the health restructuring.",
        "confidence": "high",
    },
    "2024-08→2024-09": {
        "event_id":         "EVT-008",
        "event_title":      "Certificate Formalization and BAES Program Launch",
        "event_type_primary": "composite",
        "event_type_secondary": "new_program_family_launch, cert_section_restructuring",
        "is_curated_major_event": True,
        "observed_summary": "91 course churn, 13 program churn, 3 version changes. New 'Certificates - Standard Paths' section added with 16 cert programs and 52 unique course codes. Endorsement program restructuring; new D6xx course series. Notes: cert_section_added.",
        "interpreted_summary": "WGU added a formal 'Certificates - Standard Paths' section to the catalog for the first time, introducing 16 certificate programs with 52 dedicated course codes (all disjoint from Academic Programs). Simultaneously, endorsement programs in the Education school were restructured, introducing a new D6xx course code series and retiring older endorsement codes.",
        "confidence": "high",
    },
    "2024-09→2024-10": {
        "event_id":         "EVT-009",
        "event_title":      "Post-Cert-Launch Curriculum Integration Wave",
        "event_type_primary": "curriculum_version_wave",
        "event_type_secondary": "program_family_rebuild",
        "is_curated_major_event": True,
        "observed_summary": "101 course churn, 5 program churn, 7 version changes. All 4 colleges affected.",
        "interpreted_summary": "The month following the certificate section launch saw the highest four-college course churn in the recent archive, suggesting a broad curriculum integration across all four schools that may have been coordinated with the structural changes from the prior month.",
        "confidence": "moderate",
    },
    "2025-01→2025-02": {
        "event_id":         "EVT-010",
        "event_title":      "Graduate CS/SWE Specialization Split and Education/Health Expansion",
        "event_type_primary": "composite",
        "event_type_secondary": "graduate_specialization_split, new_program_family_launch",
        "is_curated_major_event": True,
        "observed_summary": "Severity 347 — highest in archive. 158 course churn (110 added, 48 removed), 14 program churn, 13 version changes. Education, Health, Technology schools affected.",
        "interpreted_summary": "The largest single-month expansion in the 2017–2026 archive by severity score. WGU launched multiple new graduate specialization tracks in Computer Science and Software Engineering (MSCS and MSSWE family programs), each with dedicated course series. Concurrent Health and Education program additions suggest a coordinated multi-school expansion rather than a single isolated program launch.",
        "confidence": "high",
    },
}

# Also add notable but non-top events that crossed thresholds
# Generate event rows from the 41 candidates
event_rows = []
event_dict = {}
used_ids = set(e["event_id"] for e in CURATED_EVENTS.values())
ev_counter = 11

for ev in events_raw:
    tr    = ev["transition"]
    fr    = ev["from_catalog"]
    to    = ev["to_catalog"]
    diffs = diffs_by_transition.get(tr, {})

    if tr in CURATED_EVENTS:
        curated = CURATED_EVENTS[tr]
        eid     = curated["event_id"]
        is_curated = curated["is_curated_major_event"]
        title   = curated["event_title"]
        ep      = curated["event_type_primary"]
        es      = curated["event_type_secondary"]
        obs     = curated["observed_summary"]
        interp  = curated["interpreted_summary"]
        conf    = curated["confidence"]
    else:
        eid    = f"EVT-{ev_counter:03d}"
        ev_counter += 1
        is_curated = False
        ep, es = infer_event_type(ev, diffs)
        obs    = (f"course_churn={ev['course_churn']}, "
                  f"programs_added={ev['programs_added_count']}, "
                  f"programs_removed={ev['programs_removed_count']}, "
                  f"version_changes={ev['version_changes_count']}, "
                  f"title_changes={ev['title_changes_count']}, "
                  f"flags={ev['flags']}")
        interp = ""
        conf   = "moderate"
        title  = (f"{fr}→{to} — "
                  f"{ep.replace('_',' ').title()} "
                  f"({', '.join(ev.get('affected_colleges',[]))})")

    # Programs and courses (abbreviated for large events)
    progs_added   = diffs.get("programs_added", [])
    progs_removed = diffs.get("programs_removed", [])
    courses_added = diffs.get("courses_added", [])
    courses_removed = diffs.get("courses_removed", [])

    row = {
        "event_id":              eid,
        "start_edition":         fr,
        "end_edition":           to,
        "event_title":           title,
        "event_type_primary":    ep,
        "event_type_secondary":  es,
        "severity_score":        ev["severity_score"],
        "course_churn":          ev["course_churn"],
        "courses_added_count":   ev["courses_added_count"],
        "courses_removed_count": ev["courses_removed_count"],
        "program_churn":         ev["program_churn"],
        "version_changes_count": ev["version_changes_count"],
        "title_changes_count":   ev["title_changes_count"],
        "affected_schools":      "; ".join(ev.get("affected_colleges", [])),
        "affected_programs_added":   "; ".join(progs_added[:20]),
        "affected_programs_removed": "; ".join(progs_removed[:20]),
        "affected_courses_added_sample": "; ".join(courses_added[:15]),
        "affected_courses_removed_sample": "; ".join(courses_removed[:15]),
        "observed_summary":      obs,
        "interpreted_summary":   interp,
        "confidence":            conf,
        "is_curated_major_event": is_curated,
    }
    event_rows.append(row)
    event_dict[eid] = row

# Sort by severity descending
event_rows.sort(key=lambda r: (-int(r["severity_score"]), r["start_edition"]))

EV_FIELDS = [
    "event_id", "start_edition", "end_edition", "event_title",
    "event_type_primary", "event_type_secondary",
    "severity_score", "course_churn", "courses_added_count", "courses_removed_count",
    "program_churn", "version_changes_count", "title_changes_count",
    "affected_schools",
    "affected_programs_added", "affected_programs_removed",
    "affected_courses_added_sample", "affected_courses_removed_sample",
    "observed_summary", "interpreted_summary", "confidence",
    "is_curated_major_event",
]
p = write_csv(os.path.join(OUT, "named_events.csv"), event_rows, EV_FIELDS)
print(f"  → {p}")

write_json(os.path.join(OUT, "named_events.json"), event_rows)
print(f"  → {os.path.join(OUT, 'named_events.json')}")

# Curated major events subset (for homepage/timeline)
curated_events = [r for r in event_rows if r["is_curated_major_event"]]
curated_events.sort(key=lambda r: r["start_edition"])  # chronological for timeline
write_json(os.path.join(OUT, "curated_major_events.json"), curated_events)
print(f"  → {os.path.join(OUT, 'curated_major_events.json')}")

# Counts by event type
ev_type_counts = Counter(r["event_type_primary"] for r in event_rows)
print(f"  Total events: {len(event_rows)}, curated: {len(curated_events)}")
print(f"  Type counts: {dict(ev_type_counts.most_common())}")
ambiguous = [r for r in event_rows if r["confidence"] == "low" or (not r["is_curated_major_event"] and not r["interpreted_summary"])]
print(f"  Events needing manual review / interpretation: {len(ambiguous)}")

# ---------------------------------------------------------------------------
# STEP 4 — Static site-ready JSON exports
# ---------------------------------------------------------------------------
print("\n=== STEP 4: Static site-ready JSON exports ===")

# Build course cards (lightweight, for explorer + search)
course_cards = []
for r in canonical_rows:
    code = r["course_code"]
    card = {
        "code":           code,
        "title":          r["canonical_title_current"],
        "active":         r["active_current"],
        "scope":          r["contexts_seen"],
        "first_seen":     r["first_seen_edition"],
        "last_seen":      r["last_seen_edition"],
        "edition_count":  r["edition_count"],
        "current_college": r["current_college"],
        "current_program_count": r["current_program_count"],
        "stability_class": r["stability_class"],
        "ghost_flag":     r["ghost_flag"],
        "single_appearance_flag": r["single_appearance_flag"],
        "title_variant_class": r["title_variant_class"],
    }
    course_cards.append(card)

p = write_json(os.path.join(EXP, "courses.json"), course_cards)
print(f"  → {p}  ({len(course_cards)} course cards)")

# Individual course detail files (active AP codes only — 838 files)
active_ap = [r for r in canonical_rows if r["contexts_seen"] == "AP" and r["active_current"]]
for r in active_ap:
    code = r["course_code"]
    tvc  = tvc_by_code.get(code, {})

    # Gather instances from course_index for history
    entry = course_index.get(code, {})
    instances = entry.get("instances", [])

    # Programs timeline: distinct programs by earliest date
    programs_timeline = {}
    for inst in instances:
        deg = inst.get("degree", "")
        dt  = inst.get("catalog_date", "")
        if deg and dt:
            if deg not in programs_timeline or dt < programs_timeline[deg]["first_seen"]:
                programs_timeline[deg] = {"program": deg, "first_seen": dt}

    # Sort by first_seen
    prog_timeline_list = sorted(programs_timeline.values(), key=lambda x: x["first_seen"])

    detail = {
        "course_code":              code,
        "canonical_title_current":  r["canonical_title_current"],
        "observed_titles":          [t.strip() for t in r["observed_titles"].split(" | ") if t.strip()],
        "first_seen_edition":       r["first_seen_edition"],
        "last_seen_edition":        r["last_seen_edition"],
        "active_current":           True,
        "contexts_seen":            "AP",
        "current_college":          r["current_college"],
        "current_programs":         [p.strip() for p in r["current_programs"].split(";") if p.strip()],
        "current_program_count":    r["current_program_count"],
        "historical_program_count": r["historical_program_count"],
        "programs_timeline":        prog_timeline_list,
        "edition_count":            r["edition_count"],
        "canonical_cus":            r["canonical_cus"],
        "ghost_flag":               r["ghost_flag"],
        "single_appearance_flag":   r["single_appearance_flag"],
        "stability_class":          r["stability_class"],
        "title_variant_class":      r["title_variant_class"],
        "title_variant_detail":     tvc.get("genuine_change_detail", ""),
        "current_title_confidence": r["current_title_confidence"],
        "notes":                    r["notes_confidence"],
        "colleges_seen":            r["colleges_seen"],
    }
    write_json(os.path.join(CDIR, f"{code}.json"), detail, indent=None)

print(f"  → {CDIR}/  ({len(active_ap)} individual course files)")

# events.json — full event layer sorted chronologically
events_export = sorted(event_rows, key=lambda r: r["start_edition"])
p = write_json(os.path.join(EXP, "events.json"), events_export)
print(f"  → {p}  ({len(events_export)} events)")

# search_index.json — lightweight list for client-side search
search_entries = []
for r in canonical_rows:
    entry = {
        "type":    "course",
        "code":    r["course_code"],
        "title":   r["canonical_title_current"],
        "active":  r["active_current"],
        "scope":   r["contexts_seen"],
        "school":  r["current_college"],
    }
    # Include title variants in search
    if r["observed_titles"] and " | " in r["observed_titles"]:
        entry["alt_titles"] = [t.strip() for t in r["observed_titles"].split(" | ") if t.strip() and t.strip() != r["canonical_title_current"]]
    search_entries.append(entry)

# Add programs to search index
for row in prog_hist_rows:
    entry = {
        "type":    "program",
        "code":    row["program_code"],
        "title":   row.get("degree_headings", ""),
        "active":  row["status"] == "ACTIVE",
        "scope":   "AP",
        "school":  row.get("colleges", "").split(" | ")[0].strip(),
    }
    search_entries.append(entry)

p = write_json(os.path.join(EXP, "search_index.json"), search_entries)
print(f"  → {p}  ({len(search_entries)} search entries)")

# homepage_summary.json — curated data for homepage modules
# Count active AP courses per school (courses in multiple schools are counted in each)
SCHOOL_NAMES = {
    "Business":   "School of Business",
    "Health":     "Leavitt School of Health",
    "Technology": "School of Technology",
    "Education":  "School of Education",
}
active_by_college = {short: 0 for short in SCHOOL_NAMES}
for code, r26 in courses2026_by_code.items():
    colleges_str = r26.get("colleges", "")
    for short, full in SCHOOL_NAMES.items():
        if full in colleges_str:
            active_by_college[short] += 1

# Recent version changes — programs with version change in last 3 editions
recent_versions = []
for row in prog_hist_rows:
    if row["status"] == "ACTIVE" and row.get("version_progression"):
        prog = row.get("version_progression", "")
        parts = [p.strip() for p in prog.split("→") if p.strip()]
        if parts:
            last = parts[-1]
            if last.startswith("2026-") or last.startswith("2025-1") or last.startswith("2025-0"):
                recent_versions.append({
                    "program_code": row["program_code"],
                    "last_version_date": last.split(":")[0] if ":" in last else last,
                    "version_stamp": last.split(":")[1] if ":" in last else "",
                    "degree_heading": row.get("degree_headings", ""),
                    "school": row.get("colleges", "").split(" | ")[0].strip(),
                })

recent_versions.sort(key=lambda r: r["last_version_date"], reverse=True)

# Newest programs
newest_programs = []
for row in prog_hist_rows:
    if row["status"] == "ACTIVE" and row["first_seen"] >= "2024-01":
        newest_programs.append({
            "program_code": row["program_code"],
            "first_seen": row["first_seen"],
            "degree_heading": row.get("degree_headings", ""),
            "school": row.get("colleges", "").split(" | ")[0].strip(),
        })
newest_programs.sort(key=lambda r: r["first_seen"], reverse=True)

# Recent course additions
recent_adds = []
for key in sorted(diffs_by_transition.keys(), reverse=True)[:6]:
    d = diffs_by_transition[key]
    for code in d.get("courses_added", [])[:5]:
        if code in canonical_dict and canonical_dict[code]["active_current"]:
            recent_adds.append({
                "code": code,
                "title": canonical_dict[code]["canonical_title_current"],
                "added_in": d["to_catalog"],
                "school": canonical_dict[code]["current_college"],
            })

homepage = {
    "data_date":           "2026-03",
    "archive_span":        "2017-01 to 2026-03",
    "total_editions":      108,
    "total_course_codes_ever": 1594,
    "active_ap_codes":     ap_active,
    "active_cert_codes":   cert_count,
    "retired_ap_codes":    ap_retired,
    "active_programs":     sum(1 for r in prog_hist_rows if r["status"] == "ACTIVE"),
    "retired_programs":    sum(1 for r in prog_hist_rows if r["status"] == "RETIRED"),
    "active_by_school": {
        "Business":   active_by_college["Business"],
        "Health":     active_by_college["Health"],
        "Technology": active_by_college["Technology"],
        "Education":  active_by_college["Education"],
    },
    "active_by_school_note": "Courses in multiple schools are counted in each. Total may exceed active_ap_codes.",
    "curated_major_events_count": len(curated_events),
    "most_recent_curated_event": curated_events[-1]["event_title"] if curated_events else "",
    "recent_version_changes": recent_versions[:8],
    "newest_programs": newest_programs[:8],
    "recent_course_additions": recent_adds[:12],
    "curated_major_events_preview": [
        {
            "event_id":   e["event_id"],
            "date_range": f"{e['start_edition']} → {e['end_edition']}",
            "title":      e["event_title"],
            "type":       e["event_type_primary"],
            "schools":    e["affected_schools"],
            "summary":    e["interpreted_summary"][:200] if e["interpreted_summary"] else e["observed_summary"][:200],
        }
        for e in curated_events
    ],
}
p = write_json(os.path.join(EXP, "homepage_summary.json"), homepage)
print(f"  → {p}")

# ---------------------------------------------------------------------------
# Summary report
# ---------------------------------------------------------------------------
print("\n" + "="*60)
print("BUILD COMPLETE")
print("="*60)
print(f"\nOutputs in: {OUT}/")
print(f"  title_variant_classification.csv   — {len(tv_rows)} classified codes")
print(f"  title_variant_summary.json")
print(f"  canonical_courses.csv              — {len(canonical_rows)} total codes (AP + cert)")
print(f"  canonical_courses.json")
print(f"  named_events.csv                   — {len(event_rows)} events")
print(f"  named_events.json")
print(f"  curated_major_events.json          — {len(curated_events)} curated")
print(f"\nExports in: {EXP}/")
print(f"  courses.json                       — {len(course_cards)} course cards")
print(f"  courses/{{code}}.json              — {len(active_ap)} individual AP files")
print(f"  events.json                        — {len(events_export)} events")
print(f"  search_index.json                  — {len(search_entries)} search entries")
print(f"  homepage_summary.json")

print("\nKey edge cases / manual review items:")
print(f"  Title variant codes needing manual review: {tv_summary['manual_review_codes']}")
print(f"  Substantive title changes: {tv_summary['substantive_change_codes']}")
print(f"  Ghost codes (brief/suspect appearances): {ghost_count}")
print(f"  Single-appearance codes: {single_count}")
print(f"  Events without interpreted_summary: {sum(1 for r in event_rows if not r['interpreted_summary'])}")
