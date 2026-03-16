# WGU Catalog Scraper — Internal Reference

*Last updated: 2026-03-14*

---

## Contents

1. [What this is and why it exists](#1-what-this-is-and-why-it-exists)
2. [Archive coverage](#2-archive-coverage)
3. [Source data: how PDFs were obtained](#3-source-data-how-pdfs-were-obtained)
4. [PDF text extraction](#4-pdf-text-extraction)
5. [Catalog structure and the two parsing eras](#5-catalog-structure-and-the-two-parsing-eras)
6. [Parser architecture: parse_catalog_v11.py](#6-parser-architecture-parse_catalog_v11py)
7. [Output files: complete schema reference](#7-output-files-complete-schema-reference)
8. [Validation methodology and trust basis](#8-validation-methodology-and-trust-basis)
9. [Known data quality issues](#9-known-data-quality-issues)
10. [Change tracking layer](#10-change-tracking-layer)
11. [Edition diffs layer](#11-edition-diffs-layer)
12. [College name history](#12-college-name-history)
13. [Script inventory](#13-script-inventory)
14. [What is not yet covered](#14-what-is-not-yet-covered)
15. [Key statistics](#15-key-statistics)

---

## 1. What this is and why it exists

This project extracts structured data from WGU's official academic catalog PDFs and builds a versioned history of WGU's curriculum across 108 monthly catalog editions spanning **January 2017 through March 2026**.

### Operational origin

The scraper began as a dependency for the **WGU Reddit Analyzer** capstone project in this same repository. That pipeline analyzes student Reddit posts and filters them to posts referencing specific WGU courses. Course codes (4-character identifiers like `C175`, `D425`) were the anchor that made course-level analysis possible. Maintaining an accurate, complete, and current list of WGU course codes is therefore an **active operational requirement**, not just historical analysis groundwork: any new course code introduced after the last catalog extraction will be silently missed in Reddit post matching.

### Research expansion

The catalog work has since expanded into a broader goal: building a machine-readable history of WGU's official curriculum — courses, programs, schools, certificates, and structural changes over time. The long-term goal is to answer "what changed at WGU between any two catalog dates" and link those changes to what students were discussing on Reddit at the same time.

### Two value streams

- **Research value**: course-level analysis of student Reddit discussion, historical tracking of curriculum changes
- **Institutional value**: provenance-traced record of every program, course, and school name from 2017 to present

---

## 2. Archive coverage

### Edition date range

- **First edition:** 2017-01 (January 2017)
- **Latest edition:** 2026-03 (March 2026)
- **Total editions on disk:** 108
- **Total unique catalog transitions (adjacent pairs):** 107

### Coverage gaps

Three early editions are missing from the archive and are likely unrecoverable:
- **2017-02** — not available
- **2017-04** — not available
- **2017-06** — not available

All other months from 2017-01 through 2026-03 are present, with one irregular gap:
- **2017-05 → 2017-07**: the 2017-06 gap is bridged; the 2017-05 edition is the last before the gap and the 2017-07 is the first after

### Recent editions (2025-07 → 2026-03)

These 8 editions were acquired manually in March 2026 after programmatic download attempts failed (WGU's CDN blocks non-browser requests with HTTP 406). PDFs were downloaded via browser and renamed to the standard convention.

### File naming convention

```
data/raw_catalog_pdfs/catalog_YYYY_MM.pdf
data/raw_catalog_texts/catalog_YYYY_MM.txt
```

---

## 3. Source data: how PDFs were obtained

PDFs are sourced directly from WGU's public academic catalog URL. The catalogs are publicly accessible documents, not paywalled.

**Acquisition methods used:**
- Bulk download via `scripts/scrape_catalog.py` for older editions (2017–2025-06)
- Manual browser download for 2025-07 through 2026-03 after CDN blocking prevented automation

**Why CDN blocking?** WGU's CDN rejects requests that lack valid browser session cookies or identifiable browser headers. Python `requests`, `curl` with browser headers, and Playwright (headless mode) all returned HTTP 406 for recent editions. The workaround is a manual browser download; there is no known automated bypass that doesn't require an active browser session.

---

## 4. PDF text extraction

All PDFs are converted to plain text using **pdfplumber** before any parsing occurs. The text files are the source of truth for all downstream work; the PDFs are kept only as archival backups.

```
data/raw_catalog_texts/catalog_YYYY_MM.txt
```

**Text file characteristics:**
- Line-stripped (leading/trailing whitespace removed)
- One PDF page boundary per blank line (roughly)
- Size range: ~600 KB–1.3 MB per file
- Average ~13,000 lines per file; larger recent editions reach ~15,000 lines

**Known extraction artifact:** Long course titles occasionally wrap across lines in the PDF layout. When this happens, pdfplumber emits the first segment on the course row and the wrapped portion on the adjacent line. The parser captures only the first segment. This produces apparent "title truncations" in cross-edition comparisons — detected and labeled as artifacts, not genuine renames (see §9).

---

## 5. Catalog structure and the two parsing eras

### Document layout (as of 2026-03)

| Section | Approx. line range | Notes |
|---|---|---|
| Cover / TOC | 0–151 | Program list with page numbers |
| About WGU | 152–467 | Prose |
| Admissions | 468–972 | Prose |
| Tuition and Financial Aid | 973–1305 | Contains college headers and degree-like names — parser trap |
| Academic Policies | 1306–2138 | Prose |
| Standalone Courses and Certificates | 2139–2675 | Narrative cert descriptions, no CCN tables |
| **Academic Programs** | **2676–7635** | Index (TOC bullet list) + all 114 program body blocks |
| Program Outcomes | 7636–13361 | Per-program learning outcome bullets |
| Instructor Directory | 13362–14565 | `Last, First; Degree, University` per line |
| Certificates - Standard Paths | 14566–14780 | 16 cert programs; same CCN/Total CUs structure as AP |

The parser targets the **Academic Programs** section only. Program Outcomes and Instructor Directory are bounded and parseable but not yet integrated.

### Two parsing eras

The catalog has two structurally distinct formats, cleanly distinguished by the `Total CUs` terminator line format:

**ERA_B — 2024-08 to present (40 editions)**

- `Total CUs` line: `PROGCODE YYYYMM Total CUs: N` — program code and version date on the **same** line as the terminator
- Section dividers in the body: `School of X Programs` (with "Programs" suffix)
- School names: School of Business / School of Technology / Leavitt School of Health / School of Education
- Formal `"School of X Tenets:"` bullet blocks precede each school's programs
- Program Outcomes section present (from 2024-09)
- Certificates - Standard Paths section present (from 2024-09)

**ERA_A — 2017-01 to 2024-07 (68 editions)**

- `Total CUs` line: standalone `Total CUs: N` — program code and version date appear on the **following** line
  - Next-line format: `PROGCODE YYYYMM © Western Governors University [date] [page]`
- Section dividers: bare college names (no "Programs" suffix)
- College names vary by sub-era (see §12)
- No Program Outcomes section (parser must not require it)
- No Certificates - Standard Paths section
- Some programs span PDF pages, producing a mid-page `Total CUs` subtotal — distinguished from true terminator by checking if the next non-blank line is a CCN header

**Era auto-detection:** The parser determines era at file-open time by scanning for the first `Total CUs:` occurrence and checking its format. No date-based branching is used.

### Sub-era breakpoints within ERA_A

| Date | What changed |
|---|---|
| 2024-08 | Total CUs format flip; body dividers gain "Programs" suffix; ERA_B begins |
| 2024-02 | "School of Business" replaces "College of Business" |
| 2024-04 | "School of Technology" replaces "College of Information Technology" |
| 2023-01 | "Leavitt School of Health" replaces "College of Health Professions" |
| 2023-03 | "School of Education" replaces "Teachers College" |
| ~2020-11 | Formal `"X Tenets:"` bullet blocks appear |
| ~2019 | Inline college tenets prose paragraphs appear (no formal label) |
| 2017-01 | Index uses `"Online College of X"` prefix (body does not); only Business body divider has "Programs" suffix; copyright date in M/D/YY format |

### Parsing anchors

| Anchor | Pattern | Behavior |
|---|---|---|
| CCN header | `CCN.*Course Number` (case-insensitive) | Starts every course table |
| Course row (full) | `^[A-Z]{2,5} \d{1,4} [A-Z0-9]{2,5} .+ \d+ \d+$` | Standard format: DEPT COURSENUM CODE TITLE CUS TERM |
| Course row (code-only) | `^[A-Z][A-Z0-9]{1,5} .+ \d+ \d+$` | Missing DEPT/COURSENUM — catalog authoring defect |
| Total CUs (ERA_B, AP) | `^([A-Z0-9_\-]+) \d{6} Total CUs: \d+$` | Hard program terminator; underscore needed for `BSSWE_C` |
| Total CUs (ERA_A, AP) | `^Total CUs: \d+$` | Standalone; program code on next line |
| Total CUs (cert section) | `^Total CUs: \d+$` | No program code prefix — same pattern as ERA_A, different context |
| Copyright footer | `^©` | **Skip (continue), never break** — appears mid-table at PDF page boundaries |
| School header (body) | Exact match of current school name or `Name Programs` | Signals college context switch |
| Cert program name | `^Certificate: .+$` | Unique to cert section |

---

## 6. Parser architecture: parse_catalog_v11.py

`parse_catalog_v11.py` is the active parser. All prior versions (V1–V10) are superseded and should not be used.

### Processing pipeline

```
PDF text file
  → detect_era()           # scan first Total CUs line to determine A or B
  → locate_sections()      # find Academic Programs, Program Outcomes, Cert section
  → parse_index()          # extract program list from TOC bullet list
  → parse_body_blocks()    # state machine: extract program blocks from body
  → extract_courses()      # per-block: extract course rows from CCN tables
  → build_course_index()   # aggregate all instances into cross-edition index
```

### `detect_era(lines)`

Scans the first `Total CUs:` occurrence:
- If line matches `^[A-Z0-9_\-]+ \d{6} Total CUs:` → ERA_B
- If line matches `^Total CUs:` → ERA_A
- Default: ERA_B (safe for recent editions)

### `locate_sections(lines)`

Returns `{section_name: line_number}` for:
- `Academic Programs` — always uses the **last** occurrence (handles 2023-12 TOC duplication, where "Academic Programs" appears both in the TOC and in the body)
- `Program Outcomes` — first occurrence; optional (absent in ERA_A)
- `Certificates - Standard Paths` — first occurrence; optional (absent pre-2024-09)

### `parse_index(lines, ap_start, po_start, era)`

Reads the TOC bullet list at the top of the Academic Programs section. Extracts canonical program names grouped by college. ERA_A and ERA_B use slightly different header formats:

- **ERA_B**: `"School of X Programs"` headers introduce each school's bullet list
- **ERA_A**: bare college names serve as headers; lookahead up to 10 non-blank lines to confirm bullets follow (handles Education sub-group headers like "Bachelor's Degrees (Non-Licensure):" that appear between the college name and the first bullet)

Output: `outputs/program_names/YYYY_MM_program_index_v11.json`

### `parse_body_blocks(lines, ap_start, po_start, era)`

State machine that walks the Academic Programs body and emits one record per program:

1. Detects school-level headers (transitions `current_college`)
2. Detects degree headings (lines matching the `RE_DEGREE` pattern, not copyright footers, not bullets)
3. Collects courses under each CCN header until a `Total CUs` terminator fires
4. Extracts program code and version stamp from the terminator line (ERA_B: same line; ERA_A: next line after `©`)
5. For ERA_A: skips mid-page `Total CUs` subtotals (distinguished by checking if next non-blank line is a CCN header, not a program code line)

Output per edition: `outputs/program_names/YYYY_MM_program_blocks_v11.json`

Each block:
```json
{
  "college": "School of Business",
  "degree": "Bachelor of Science, Accounting",
  "deg_idx": 2827,
  "ccn_idx": 2834,
  "end": 2882,
  "code": "BSACC",
  "version": "202503",
  "cus": 121
}
```

### Course extraction

For each block, the parser reads lines between `ccn_idx` and `end`, matching each line against two patterns in priority order:

1. `CCN_FULL`: `^([A-Z]{2,5}) (\d{1,4}) ([A-Z0-9]{2,5}) (.+?) (\d+) (\d+)$`
   - Groups: DEPT, COURSENUM, CODE, TITLE, CUS, TERM
2. `CODE_ONLY`: `^([A-Z][A-Z0-9]{1,5}) (.+?) (\d+) (\d+)$`
   - Groups: CODE, TITLE, CUS, TERM
   - Used only for known catalog defects (e.g., D627 missing DEPT/COURSENUM)

Copyright footer lines (`©`) are skipped (continue); `Total CUs` fires a break.

### Key regex patterns

```python
RE_TOTAL_CUS        = re.compile(r'^([A-Z0-9_\-]+)\s+(\d{6})\s+Total CUs:\s*(\d+)')   # ERA_B
RE_TOTAL_CUS_A      = re.compile(r'^Total CUs:\s*(\d+)')                               # ERA_A
RE_TOTAL_CUS_A_NEXT = re.compile(r'^([A-Z0-9_\-]{2,10})\s+(\d{6})\s+©')              # ERA_A next-line
RE_DEGREE = re.compile(
    r'^(Bachelor|Master|Post.Master|Post-Baccalaureate|Certificate|Endorsement|Doctor|MBA)\b',
    re.IGNORECASE
)
RE_COLLEGE_ANY = re.compile(
    r'^(Online )?(College of (Business|Health Professions|Information Technology)'
    r'|Teachers College|School of (Business|Technology|Education)|Leavitt School of Health)'
)
RE_BULLET = re.compile(r'^[•●\-]\s*(.+)')  # ● is used in ERA_A catalogs
```

### V10 vs V11: what changed

V10 had a critical bug in Step 4 (course extraction): copyright footer lines (`©`) inside a CCN table caused a `break` instead of a `continue`. Every program whose course list spanned a PDF page boundary lost all courses after the first page footer. This affected 49 programs across all four colleges and 142 unique codes.

V11 fixes:
1. `break` → `continue` on copyright footers (recovers 142 missing codes)
2. ERA_A Total CUs handler (standalone terminator + next-line code extraction)
3. Mid-page subtotal detection (ERA_A programs spanning PDF pages)
4. `MBA\b` word boundary in `RE_DEGREE` (prevents MBA program codes like MBAITM matching as degree headings)
5. `Post-Baccalaureate` added to `RE_DEGREE`
6. `©` exclusion in degree detection (prevents ERA_A footer lines matching)
7. Last-occurrence logic for `Academic Programs` header (handles 2023-12 TOC duplication)
8. PO and cert sections made optional (absent in ERA_A)
9. ERA_A 10-line lookahead for Education sub-group headers in `parse_index`
10. College name normalization across all historical name variants

---

## 7. Output files: complete schema reference

### Directory structure

```
outputs/
├── trusted/2026_03/          # Frozen ground-truth reference for 2026-03
├── helpers/                  # Cross-edition aggregates
├── program_names/            # Per-edition parser outputs (index + blocks)
├── raw_course_rows/          # Per-edition raw course row JSON (99 editions)
├── anomalies/                # Per-edition anomaly log from parser run
├── change_tracking/          # Cross-edition course and program history
├── edition_diffs/            # Per-transition change schema
└── validation_report.json    # Results of targeted raw-vs-parsed validation
```

---

### `outputs/trusted/2026_03/` — Frozen ground-truth reference

These files are locked and should not be regenerated. They are the verified baseline for 2026-03 and the reference for all downstream work.

| File | Description |
|---|---|
| `courses_2026_03.csv` | 838 AP course codes with title, CUs, programs, colleges |
| `certs_2026_03.csv` | 52 cert section course codes with title, CUs, cert program membership |
| `manifest_2026_03.json` | Count verification and source file provenance |
| `course_index_2026_03.json` | Full course index with per-instance raw rows |
| `sections_index_2026_03.json` | Program fence boundaries (start/end line per program block) |
| `degree_snapshots_2026_03.json` | Programs grouped by college |
| `program_blocks_2026_03.json` | Body blocks: one per program with college, degree, code, version, CUs |
| `program_index_2026_03.json` | Index names from the TOC bullet list |

**Verified counts (2026-03):**
- AP unique course codes: **838** (all 4-character codes)
- Cert section unique codes: **52** (disjoint from AP)
- Programs (body blocks): **114**
- AP codes in raw scan but not parsed: **0**
- AP codes in parsed but not raw: **0**
- Body-parse anomalies: **0**

---

### `outputs/helpers/course_index_v10.json`

The primary cross-edition course index. One entry per unique course code, aggregated across all 108 editions.

```json
{
  "C175": {
    "canonical_title": "Data Management - Foundations",
    "canonical_cus": 3,
    "instances": [
      {
        "catalog_date": "2017-01",
        "college": "College of Business",
        "degree": "Bachelor of Science, Business - Information Technology Management",
        "pattern": "CCN_FULL",
        "raw": "ITEC 2104 C175 Data Management - Foundations 3 7"
      },
      ...
    ]
  }
}
```

- **canonical_title**: most common title seen across all instances
- **canonical_cus**: most common CU value
- **instances**: every occurrence across every edition; each preserves the raw extracted line, the college and degree heading at parse time, and the match pattern used (CCN_FULL or CODE_ONLY)
- **Total entries**: 1,594 unique codes

---

### `outputs/program_names/YYYY_MM_program_blocks_v11.json`

Per-edition list of program body blocks. 108 files total.

```json
[
  {
    "college": "School of Business",
    "degree": "Bachelor of Science, Accounting",
    "deg_idx": 2827,
    "ccn_idx": 2834,
    "end": 2882,
    "code": "BSACC",
    "version": "202503",
    "cus": 121
  }
]
```

- **college**: raw name from the catalog (not normalized)
- **degree**: raw degree heading as it appears in the body
- **deg_idx / ccn_idx / end**: line numbers in the raw text file for the degree heading, CCN header, and block end — enables raw text lookups
- **code**: program identifier (e.g., `BSACC`) extracted from the Total CUs terminator
- **version**: 6-digit YYYYMM stamp from the terminator — the curriculum version date
- **cus**: total credit units for the program

---

### `outputs/program_names/YYYY_MM_program_index_v11.json`

Per-edition index of program names from the TOC bullet list. Contains abbreviated names and provides the authoritative program count per edition.

---

### `outputs/raw_course_rows/YYYY_MM_raw_course_rows.json`

Per-edition list of every raw course row as extracted, preserving the original text. Available for 99 editions (2017-01 through 2025-06). Used as the evidence layer; the `instances[].raw` field in the course index provides the same data in a more accessible form.

---

### `outputs/anomalies/anomalies_YYYY_MM.json`

Per-edition anomaly log produced during the parser run. Common anomaly types:
- `ccn_no_degree`: a CCN header was found without a preceding degree heading
- `block_no_code`: a block completed without extracting a program code
- `[UNKNOWN]` code: program code extraction failed (filtered from all downstream outputs)

After the ERA_A fixes, the full-archive run produces **0 anomalies** across all 108 editions.

---

### `outputs/change_tracking/course_history.csv`

One row per unique course code across all editions.

| Field | Description |
|---|---|
| course_code | 4-character code |
| status | ACTIVE (in 2026-03) or RETIRED |
| canonical_title | Most common title across all instances |
| canonical_cus | Most common CU value |
| first_seen | Earliest catalog_date (YYYY-MM) |
| last_seen | Latest catalog_date |
| edition_count | Number of editions the code appeared in |
| span_months | Approximate month span (first_seen to last_seen) |
| college_count | Number of distinct colleges (historical union) |
| colleges | Pipe-delimited list of all historical college names |
| title_variant_count | Count of distinct titles other than canonical |
| title_variants | Pipe-delimited list of variant titles |
| first_programs | Up to 4 degree headings from first appearance |
| latest_programs | Up to 4 degree headings from latest appearance |

**Row count:** 1,594 (838 ACTIVE, 756 RETIRED)

---

### `outputs/change_tracking/program_history.csv`

One row per unique program code across all editions.

| Field | Description |
|---|---|
| program_code | Program identifier (e.g., BSACC) |
| status | ACTIVE or RETIRED |
| first_seen | Earliest catalog_date |
| last_seen | Latest catalog_date |
| edition_count | Number of editions present |
| span_months | Approximate month span |
| versions_seen | Pipe-delimited list of all distinct version stamps |
| version_changes | Count of version stamp changes |
| version_progression | Ordered list of `date:version` changes |
| colleges | Pipe-delimited list (first-appearance order, raw names) |
| college_count | |
| cus_values | Pipe-delimited list of all observed total CU values |
| degree_heading_count | Count of distinct degree heading strings |
| degree_headings | Up to 3 degree heading strings (body text) |

**Row count:** 196 (114 ACTIVE, 82 RETIRED)

**Notable:** `version_progression` shows when curriculum was revised. Example for BSCS:
```
2018-05:201806 → 2018-08:201809 → 2020-10:202011 → 2023-05:202306 → 2024-10:202412
```
(4 version changes across 95 editions, 2018–2026)

---

### `outputs/change_tracking/adjacent_diffs.json`

107 adjacent-edition diffs keyed `"YYYY-MM→YYYY-MM"`. Base change layer built from the course index and program blocks.

Per entry:
```json
{
  "from": "2017-05",
  "to": "2017-07",
  "courses_added": ["C551", "C552", ...],
  "courses_removed": ["ABP1", "AEP1", ...],
  "courses_added_count": 101,
  "courses_removed_count": 74,
  "programs_added": ["BSCSIA"],
  "programs_removed": ["MATSC9", ...],
  "programs_added_count": 1,
  "programs_removed_count": 6,
  "version_changes": [
    {"program_code": "BAISK8", "from_version": "201708", "to_version": "201709"},
    ...
  ],
  "version_changes_count": 22,
  "notes": ""
}
```

---

### `outputs/change_tracking/adjacent_diffs_summary.csv`

Count-only flat table of the same 107 pairs. Columns: from, to, courses_added, courses_removed, net_course_change, programs_added, programs_removed, net_program_change, version_changes, notes.

---

### `outputs/change_tracking/summary_stats.json`

Archive-wide aggregate statistics including top-5 course addition/removal/version-change months and smallest/largest course edition by unique code count.

---

### `outputs/edition_diffs/edition_diffs_full.json`

The fully enriched per-transition schema. 107 entries.

Per entry (additional fields beyond `adjacent_diffs`):

| Field | Description |
|---|---|
| course_churn | courses_added + courses_removed |
| net_course_change | |
| courses_with_title_changes | List of {code, from_title, to_title} — genuine renames only |
| courses_with_title_truncations | Same structure — PDF line-wrap artifacts excluded from severity |
| title_changes_count | Genuine renames |
| title_truncations_count | Artifacts |
| courses_with_cu_changes | List of {code, from_cus, to_cus} |
| cu_changes_count | |
| program_churn | programs_added + programs_removed |
| net_program_change | |
| programs_with_version_changes | List of program codes |
| version_changes_detail | List of {program_code, from_version, to_version} |
| affected_colleges | Normalized college names (Business/Health/Technology/Education) |
| affected_college_count | |
| severity_score | Weighted composite (documented below) |

**Severity score formula:**
```
course_churn × 1
+ program_churn × 10
+ version_changes × 3
+ title_changes × 2
+ cu_changes × 2
+ extra_colleges × 5     (each college beyond first)
```

---

### `outputs/edition_diffs/edition_diffs_summary.csv`

Flat CSV with all scalar metrics from `edition_diffs_full.json`. 107 rows.

---

### `outputs/edition_diffs/edition_diffs_rollups.json`

Top-20 transitions by each dimension:
- `top20_by_severity`
- `top20_by_course_churn`
- `top20_by_program_churn`
- `top20_by_version_changes`
- `top20_by_title_changes`
- `top20_by_cu_changes`
- `top20_by_colleges_affected`

---

### `outputs/edition_diffs/edition_diffs_events.json`

41 "major event candidates" — transitions that crossed at least one significance threshold:
- `course_churn ≥ 20`
- `program_churn ≥ 4`
- `version_changes_count ≥ 10`
- `title_changes_count ≥ 5`
- `affected_college_count ≥ 3`

Each entry includes a `flags` array listing which thresholds were crossed, the severity score, and affected colleges.

---

### `outputs/validation_report.json`

Results of independent raw-vs-parsed validation across 14 target editions. All 14 show status `CLEAN`. See §8 for full methodology.

---

## 8. Validation methodology and trust basis

### Independent raw scan

For each target edition, an independent scanner (`validate_editions.py`) re-reads the raw text file without using the parser state machine and finds all lines matching course row patterns:

1. **Primary (CCN_FULL)**: `^([A-Z]{2,5}) (\d{1,4}) ([A-Z0-9]{2,5}) .+ \d+ \d+$`
2. **Secondary (CODE_ONLY)**: `^([A-Z][A-Z0-9]{1,5}) [A-Za-z].+ \d+ \d+$`

The raw code set is then compared to the set produced by the parser. Any AP-shape code (exactly 4 characters) in one set but not the other is flagged.

### Target edition selection

14 editions were chosen to cover every structural boundary in the archive:

| Edition | Era | Reason selected | Status |
|---|---|---|---|
| 2017-01 | A | Oldest; unique "Online College of X" format | CLEAN |
| 2019-01 | A | Pre-formal-tenets ERA_A | CLEAN |
| 2021-06 | A | Formal-tenets ERA_A | CLEAN |
| 2022-06 | A | +7 program count jump | CLEAN |
| 2023-01 | A | Leavitt School of Health rename | CLEAN |
| 2023-03 | A | School of Education rename | CLEAN |
| 2023-12 | A | TOC duplication; mixed school names | CLEAN |
| 2024-02 | A | School of Business rename | CLEAN |
| 2024-04 | A | School of Technology rename | CLEAN |
| 2024-07 | A | Last ERA_A | CLEAN |
| 2024-08 | B | First ERA_B; Total CUs format flip | CLEAN |
| 2024-09 | B | First cert section | CLEAN |
| 2025-02 | B | +12 program count jump (largest) | CLEAN |
| 2025-03 | B | −5 program count jump | CLEAN |

**Result:** 14/14 CLEAN.

### Trust basis for unvalidated editions

The 94 editions that were not individually validated sit between validated neighbors. Every structural boundary in the archive (era flip, all four school renames, all major program count jumps) was covered by a directly validated edition. Clean results at all boundary editions give strong implied validity for intermediate editions.

### What "CLEAN" means

- The raw independent scan and the parser output agree on every AP-shape (4-character) code
- Zero codes are in the raw scan but not in the parser output
- Zero codes are in the parser output but not in the raw scan
- Any non-AP-shape codes in the raw scan (e.g., cert codes, spurious matches) are expected and documented

---

## 9. Known data quality issues

### D627 — catalog authoring defect

`D627` (Public Health Education and Promotion, 2cu) appears in 22 editions from 2024-06 onward as a CODE_ONLY row — it is missing its DEPT and COURSENUM fields. Every adjacent row in the same table has the full CCN format. This is a WGU catalog authoring error, not a parser error. The parser correctly captures D627 via the CODE_ONLY fallback pattern. The validation scanner was updated to use CODE_ONLY as a secondary pattern; all affected editions validate CLEAN.

**No action needed.** D627 is captured and included correctly.

### Title truncation at ERA boundary (2024-07 → 2024-08)

141 course titles appear shorter in the 2024-08 edition than in 2024-07 because the ERA_B PDF layout caused certain long titles to wrap to adjacent lines. pdfplumber emits the course row with only the first segment; the wrapped word(s) appear on the preceding or following line and are not captured. These are **not genuine renames**.

Detection method: if the shorter title string is a strict prefix of the longer one, the "change" is classified as a truncation artifact. Archive-wide: 144 truncations identified and labeled separately from the 31 genuine title renames. Truncations are stored in `courses_with_title_truncations` and excluded from the severity score.

### Index/body naming inconsistencies (18 programs in 2026-03)

WGU uses different naming conventions in the TOC bullet list vs. the body block headers. 18 programs in 2026-03 cannot be automatically matched between the index and the body due to these inconsistencies:

| Pattern | Index example | Body example |
|---|---|---|
| Parens vs dash for specializations | `M.S. Data Analytics (Data Science)` | `Master of Science, Data Analytics - Data Science` |
| "Endorsement X" vs. full form | `Endorsement Middle Grades Math` | `Endorsement Preparation Program, Middle Grades Math` |
| SE tracks: named in index, unnamed in body | `B.S. Software Engineering (Java Track)` | `Bachelor of Science, Software Engineering` |
| "in" connector | `M.S. Marketing (...)` | `Master of Science in Marketing, ...` |
| MBA abbreviated vs spelled | `MBA Information Technology Management` | `MBA, IT Management` |

These are catalog inconsistencies, not parser errors. The program body blocks are the authoritative source for program identity (via the `code` field from the Total CUs terminator). The index names are supplemental.

### `BSSWE_C` — underscore in program code

The C# track of Software Engineering uses the code `BSSWE_C` (underscore included). The `RE_TOTAL_CUS` pattern explicitly includes `_` and `-` in the program code character class to handle this. If new programs with unusual code characters are introduced, the regex may need updating.

### 3 missing early editions

2017-02, 2017-04, and 2017-06 are not on disk. The 2017-05 to 2017-07 transition in the diff data bridges the 2017-06 gap; changes attributed to that pair may in fact have occurred in two distinct steps across 2017-05→2017-06 and 2017-06→2017-07. This is unresolvable without the missing PDFs.

---

## 10. Change tracking layer

Built by `build_change_tracking.py` from the course index and program blocks. Produces the lifecycle view for every course and program in the archive.

### Course history (`course_history.csv`)

- 1,594 unique course codes, 2017-01 through 2026-03
- **838 active** (present in 2026-03), **756 retired**
- 167 codes have at least one title variant (genuine title change or cosmetic rename)
- 113 codes appear in all 108 editions (all are performance-task assessment codes: AFT2, AIT2, etc.) — these have been stable since 2017
- 94 codes retired before 2018 (almost all are old AXX-format assessment codes retired in the 2017-05→2017-07 restructuring)

### Program history (`program_history.csv`)

- 196 unique program codes, 2017-01 through 2026-03
- **114 active**, **82 retired**
- 100 programs have at least one version stamp change
- **Most volatile program**: BSHIM (B.S. Health Information Management) — 11 version changes across the archive
- Version progression tracks exact month-year of each curriculum revision, useful for correlating catalog changes with student discussion

### What the version stamp means

Each program block carries a 6-digit YYYYMM version stamp (e.g., `202503`). This is WGU's internal curriculum version date — the month the current curriculum was formalized. When the stamp changes between adjacent editions, WGU has released a new curriculum version. This does not necessarily mean course content changed; it may reflect:
- New courses added or removed from the program
- Course CU weights changed
- Accreditation review artifacts
- Internal documentation updates (version bump with no visible course change)

---

## 11. Edition diffs layer

Built by `build_edition_diffs.py` from the change tracking outputs and the raw course index. Produces the per-transition change view across all 107 adjacent pairs.

### What this adds over adjacent_diffs

- Title changes: identifies genuine course renames between editions (separated from PDF truncation artifacts)
- CU changes: identifies courses that changed credit unit values
- Affected colleges: derives which schools were touched by any change in the transition
- Severity score: weighted composite enabling data-driven ranking of transitions by overall magnitude

### Archive-wide totals

| Metric | Value |
|---|---|
| Total course churn | 1,934 (sum of all adds + removes across 107 transitions) |
| Genuine title changes | 31 |
| PDF truncation artifacts (not counted) | 144 |
| CU changes | 10 |
| Total version changes | 239 |
| Zero-change transitions | 24 |
| Major event candidates (≥1 threshold) | 41 |

### Top 10 transitions by severity

| Transition | Severity | Course churn | Prog churn | Ver changes | Colleges |
|---|---|---|---|---|---|
| 2025-01→2025-02 | 347 | 158 | 14 | 13 | Education, Health, Technology |
| 2017-05→2017-07 | 318 | 175 | 7 | 22 | Education, Technology |
| 2018-04→2018-05 | 301 | 61 | 23 | 0 | Education, Health, Technology |
| 2024-08→2024-09 | 240 | 91 | 13 | 3 | Business, Education, Technology |
| 2024-09→2024-10 | 187 | 101 | 5 | 7 | All 4 colleges |
| 2022-12→2023-01 | 184 | 80 | 9 | 0 | Business, Health, Technology |
| 2020-06→2020-07 | 183 | 119 | 0 | 18 | Business, Education, Health |
| 2020-01→2020-02 | 171 | 41 | 13 | 0 | Business only |
| 2020-10→2020-11 | 134 | 53 | 4 | 8 | All 4 colleges |
| 2018-05→2018-06 | 124 | 4 | 12 | 0 | Education only |

### Event type taxonomy (from data-driven analysis)

| Type | Signature | Example |
|---|---|---|
| Domain reorganization | High program churn; old taxonomy codes → new taxonomy codes; 0 version changes | 2018-04→2018-05 (grade-band → subject-discipline) |
| Program family rebuild | Namespace migration; shared core introduced; 0 version changes | 2020-01→2020-02 (BSBA rebuild) |
| Graduate specialization split | 1 generic program → N subject-specific programs; new course series | 2025-01→2025-02 (MSCS/MSSWE tracks) |
| Curriculum version wave | High version changes; near-zero course churn; same-school coordination | 2026-02→2026-03 (18 Education + Business programs) |
| Rename cleanup | High title-change count; minimal structural change | 2017-01→2017-03 ("Pre-Clinical" → "Preclinical") |
| Course weight consolidation | Old 1-2cu stubs → fewer 3cu consolidated courses; same topics | 2017-01→2017-03 (MSIHCM projects) |
| New program family launch | New program namespace; large new course series | 2024-08→2024-09 (BAES programs) |
| Certificate section restructuring | Cert programs retire from AP scope; cert section reorganizes | 2024-08→2024-09 |
| Composite / multi-event | Multiple types fire together | 2017-01→2017-03, 2024-08→2024-09 |

---

## 12. College name history

WGU renamed all four colleges between 2023 and 2024. The parser normalizes historical names to four canonical schools for downstream use. Raw names are preserved in all output files.

| Effective date | Business | Health | Technology | Education |
|---|---|---|---|---|
| 2017-01 | College of Business | College of Health Professions | College of Information Technology | Teachers College |
| 2023-01 | College of Business | **Leavitt School of Health** | College of Information Technology | Teachers College |
| 2023-03 | College of Business | Leavitt School of Health | College of Information Technology | **School of Education** |
| 2024-02 | **School of Business** | Leavitt School of Health | College of Information Technology | School of Education |
| 2024-04 | School of Business | Leavitt School of Health | **School of Technology** | School of Education |
| 2024-08+ | School of Business | Leavitt School of Health | School of Technology | School of Education |

**Special case (2017-01 only):** The program index uses "Online College of X" prefixes (e.g., "Online College of Business") but the body uses bare names. The parser handles this via the `RE_COLLEGE_ANY` pattern which optionally matches the "Online " prefix.

**Cert section (2024-09+):** The PDF adds a fifth section labeled "Certificates - Standard Paths" which appears in some college snapshots as a fifth entity. It is not a college but a structural section.

**Normalization map used in `edition_diffs`:**
```python
COLLEGE_MAP = {
    "College of Business":               "Business",
    "School of Business":                "Business",
    "College of Health Professions":     "Health",
    "Leavitt School of Health":          "Health",
    "College of Information Technology": "Technology",
    "School of Technology":              "Technology",
    "Teachers College":                  "Education",
    "School of Education":               "Education",
}
```

---

## 13. Script inventory

| Script | Purpose | Input | Output |
|---|---|---|---|
| `parse_catalog_v11.py` | Main parser; processes all 108 editions | `data/raw_catalog_texts/` | `outputs/program_names/`, `outputs/helpers/`, `outputs/anomalies/`, `outputs/raw_course_rows/` |
| `validate_editions.py` | Independent raw-vs-parsed validation | Raw text files + parser internals | `outputs/validation_report.json` |
| `build_change_tracking.py` | Course and program lifecycle tables | `outputs/helpers/course_index_v10.json`, `outputs/program_names/*_program_blocks_v11.json` | `outputs/change_tracking/` |
| `build_edition_diffs.py` | Per-transition enriched change schema | `outputs/change_tracking/adjacent_diffs.json`, course index, program blocks | `outputs/edition_diffs/` |
| `scripts/scrape_catalog.py` | PDF acquisition | WGU catalog URLs | `data/raw_catalog_pdfs/` |
| `run_parser.py` | Batch runner for parse_catalog_v11 | All text files | All outputs |

**Deprecated (do not use):**
- `parse_catalog.py` — V1–V9 (no ERA_A support, copyright-break bug)
- `parse_catalog copy.py` — working copy artifact
- `Scraper_V10_config.py` — V10 configuration (superseded)
- Anything in `shared/` or `lib/config.py` — pre-V11 support files

**Experimental / separate scope:**
- `instructor_directory/` — instructor profile and publication scraping (separate pipeline, not integrated into catalog parsing)
- `geomapping/` — instructor alma mater geographic visualization
- `course list merge/` — one-off merge utility

---

## 14. What is not yet covered

### Program Outcomes (lines 7636–13361 in 2026-03)

The program outcomes section contains per-program learning outcome bullets. The section is bounded and has a consistent structure. Parsing it would enable tracking when WGU changed stated learning outcomes for each program — not yet implemented.

### Instructor Directory (lines 13362–14565 in 2026-03)

The instructor directory lists `Last, First; Degree, University` per line, grouped by department. A separate pipeline (`instructor_directory/`) was built to process this data and enrich it with publication records and affiliation data. It is not yet integrated with the catalog change-tracking layer.

### Certificate courses (Certificates - Standard Paths, 2024-09+)

The cert section contains 52 unique course codes in 2026-03, all disjoint from the Academic Programs course set. The parser can extract cert codes but they are not yet included in `course_index_v10.json` or `course_history.csv`. They are stored in `outputs/trusted/2026_03/certs_2026_03.csv` for the 2026-03 baseline but not tracked across editions.

### Historical cert section tracking (pre-2024-09)

Before 2024-09, certs were described narratively in the "Standalone Courses and Certificates" section — no CCN tables, no course codes. The cert section as a structured data source only exists from 2024-09 onward.

### Cross-edition course identity resolution

The current layer uses exact code matching for course identity. This means:
- A course that was retired and a new course introduced with different codes but identical content appear as two separate entities
- No fuzzy matching on title similarity is applied
- Program renaming (e.g., BSAC → BSBAAC) is recorded as a retirement + new program, not a rename

Resolving these identities would require alias tables and is explicitly deferred pending more complete analysis.

---

## 15. Key statistics

### Archive summary

| Metric | Value |
|---|---|
| Editions | 108 (2017-01 → 2026-03) |
| Missing editions | 3 (2017-02, 2017-04, 2017-06) |
| Total adjacent transitions | 107 |
| Zero-change transitions | 24 |
| Total course churn across archive | 1,934 |

### Course inventory

| Metric | Value |
|---|---|
| Total unique course codes ever | 1,594 |
| Currently active (in 2026-03) | 838 |
| Retired | 756 |
| Codes in all 108 editions | 113 |
| Codes with title variants | 167 |
| Codes with genuine title renames across transitions | 31 |
| Codes with CU changes | 10 |

### Program inventory

| Metric | Value |
|---|---|
| Total unique program codes ever | 196 |
| Currently active | 114 |
| Retired | 82 |
| Programs with ≥1 version change | 100 |
| Most version changes (single program) | BSHIM — 11 |

### Cert inventory (2026-03 only)

| Metric | Value |
|---|---|
| Cert program count | 16 |
| Cert unique course codes | 52 |
| Overlap with AP codes | 0 |

### Parser validation

| Metric | Value |
|---|---|
| Editions independently validated | 14 |
| Clean (raw/parsed match) | 14/14 |
| Full-archive anomalies | 0 |
| Known catalog authoring defects | 1 (D627 CODE_ONLY) |


---

## Appendix — Website data layer status (added 2026-03-14)

This appendix records the current website-data-layer outputs built on top of the validated catalog-history pipeline. It is intended as a temporary addendum to the scraper reference until the document is fully reorganized.

### Website data layer: current status

The project now has enough canonical, site-ready data to begin building the first public-facing website pages:

- homepage
- course explorer
- course page
- timeline
- methods
- data page

These outputs live under:

```text
outputs/site_data/

Newly built artifacts

1. Title variant classification
Files:
	•	outputs/site_data/title_variant_classification.csv
	•	outputs/site_data/title_variant_summary.json

This layer classifies course-title variation across the archive so the website does not overstate harmless title drift as substantive change.

Counts by class:

Class	Count	Notes
extraction_noise	145	PDF line-wrap truncations, Unicode quote variants, same-edition oscillations
punctuation_only	16	Hyphen removal, dash normalization, punctuation cleanup
wording_refinement	3	Small wording changes with similar meaning
substantive_change	2	Meaning/scope visibly changed
formatting_only	1	Spacing-only correction
unresolved	1	Requires manual review (D344)

Important result: most apparent title changes are extraction or formatting artifacts, not genuine curricular renames.

⸻

2. Canonical course intelligence table
Files:
	•	outputs/site_data/canonical_courses.csv
	•	outputs/site_data/canonical_courses.json

This is the primary website-ready course artifact and should drive:
	•	course explorer
	•	course pages
	•	homepage course modules
	•	future discussion linkage

Row counts:
	•	total rows: 1,646
	•	active AP courses: 838
	•	retired AP courses: 756
	•	cert codes: 52

Key added fields include:
	•	contexts_seen
	•	current_programs
	•	historical_programs
	•	historical_program_count
	•	ghost_flag
	•	single_appearance_flag
	•	stability_class
	•	title_variant_class
	•	current_title_confidence
	•	notes_confidence

Definitions currently used:
	•	ghost_flag: retired and edition_count <= 2
	•	single_appearance_flag: edition_count == 1
	•	stability_class:
	•	perpetual
	•	stable
	•	moderate
	•	ephemeral
	•	single
	•	cert_only

Counts by stability class:
	•	perpetual: 113
	•	stable: 488
	•	moderate: 820
	•	ephemeral: 160
	•	single: 13
	•	cert_only: 52

Edge cases:
	•	D396 canonical title was explicitly overridden because the latest extracted title was truncated
	•	D344 remains a manual-review case
	•	cert context is conservative and based on observed structured data, not inferred pre-2024-09 narrative mentions

⸻

3. Named event layer
Files:
	•	outputs/site_data/named_events.csv
	•	outputs/site_data/named_events.json
	•	outputs/site_data/curated_major_events.json

This is the curated event artifact for the website Timeline page.

Counts:
	•	total events: 41
	•	curated major events: 10

The event layer preserves a strict distinction between:
	•	observed_summary
	•	interpreted_summary

The 10 curated events have:
	•	stable event_id
	•	human-readable event_title
	•	event type classification
	•	confidence
	•	homepage/timeline suitability

The remaining 31 machine-ranked events currently have:
	•	factual / observed summaries
	•	severity and metadata
	•	no full interpreted summary yet

This is sufficient for v1 timeline drill-down, but not yet for a fully editorialized event archive.

⸻

4. Static site-ready exports
Files:
	•	outputs/site_data/exports/courses.json
	•	outputs/site_data/exports/courses/{code}.json
	•	outputs/site_data/exports/events.json
	•	outputs/site_data/exports/search_index.json
	•	outputs/site_data/exports/homepage_summary.json

Current export counts:

File	Count
courses.json	1,646 course cards
courses/{code}.json	838 active AP detail files
events.json	41 events
search_index.json	1,842 entries (courses + programs)
homepage_summary.json	1 summary file

These exports are intended for a static site build and do not require a database.

⸻

What this unlocks

The website data layer is now sufficient to begin building:
	•	homepage
	•	course explorer
	•	course page
	•	timeline
	•	methods
	•	data page

The course page is now the flagship build target because the required course-level data is available in canonical and site-ready form.

⸻

What remains deferred

The following items are still intentionally deferred:
	•	cert section cross-edition tracking beyond the current snapshot model
	•	program page full course-roster-per-edition matrix
	•	Reddit integration
	•	frontend implementation
	•	predecessor/successor inference
	•	full interpreted summaries for all 41 events
	•	manual resolution of D344

⸻

Important note on counts

This document previously treated the historical pipeline as the final layer. That is no longer true.

There is now a distinct website data layer on top of the scraper/history pipeline. Future updates should integrate this appendix into the main document structure rather than leaving it as a temporary addendum.





Append this section to the top-level README.md:

⸻

Official WGU Context Layer

WGU Atlas is not only built from the public catalog archive. It is also planned to surface relevant official WGU website resources that help students understand courses, programs, schools, and major institutional changes.

This is a distinct product layer and is intentionally separate from both:
	•	official catalog facts
	•	student/community discussion

The goal is to help users discover useful official WGU pages that are often hard to find through the main website navigation, such as:
	•	program guide pages and PDFs
	•	school rename announcements
	•	program launch pages
	•	comparison articles
	•	certification-related advice pages
	•	other relevant official WGU resources discoverable from the sitemap

These links will eventually appear as a first-class supporting layer on Atlas pages under headings like:
	•	Related official WGU resources
	•	Official context
	•	Helpful official WGU pages

This comes before broad Reddit integration in the product roadmap. The intended content hierarchy for Atlas is:
	1.	Official catalog facts
	2.	Related official WGU resources
	3.	Student/community discussion (later, clearly secondary)

Internal planning for this work lives in:
	•	_internal/OFFICIAL_CONTEXT_LAYER_PLAN.md

That document defines:
	•	why this layer matters
	•	how official WGU links should be discovered and classified
	•	how they should be matched to Atlas entities
	•	how they should be surfaced without compromising trust or provenance

⸻
