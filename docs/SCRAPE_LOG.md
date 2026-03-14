# WGU Catalog Scrape Log
*Session memory — updated 2026-03-14*

---

## Trusted reference edition: 2026-03 ✅ VERIFIED AND FROZEN

`parse_catalog_v11.py` is the active script. The 2026-03 run is the first fully verified
edition and is the baseline for all future comparison work.

| Metric | Value |
|---|---|
| Programs found (body blocks) | 114 / 114 ✅ |
| AP unique course codes | **838** ✅ |
| AP codes in raw but not parsed | 0 ✅ |
| AP codes in parsed but not in raw | 0 ✅ |
| Body-parse anomalies | 0 |
| Reconciliation (index ↔ body name match) | 96/114 matched — 18 gaps are catalog naming inconsistencies, not data gaps |
| Cert scope unique codes | 52 (disjoint from AP, intentionally out of AP scope) |
| Combined AP + cert unique codes | 890 |

**Prior count of 696 AP codes is obsolete.** It resulted from a bug (see below) and should
not appear in any downstream reference.

### Frozen outputs: `outputs/trusted/2026_03/`

| File | Contents |
|---|---|
| `courses_2026_03.csv` | AP course inventory: 838 codes with title, CUs, programs, colleges |
| `certs_2026_03.csv` | Cert inventory: 52 codes with title, CUs, cert program membership |
| `manifest_2026_03.json` | Counts, verification status, source file list |
| `course_index_2026_03.json` | Full course index with per-instance raw rows |
| `sections_index_2026_03.json` | Program fence boundaries (start/end line per program) |
| `degree_snapshots_2026_03.json` | Programs grouped by college using 2024-09 snapshot |
| `program_blocks_2026_03.json` | Body blocks with program codes and version dates |
| `program_index_2026_03.json` | Index (abbreviated) names from the TOC bullet list |

Working outputs in `outputs/helpers/` and `outputs/*.csv` are regenerated on each run and
not treated as archival. The `trusted/` copies are the durable reference.

---

## Project origin, purpose, and stakeholder value

This catalog-scraping work began as part of the **WGU Reddit Analyzer** capstone project
in this same repository (`WGU-Reddit`). The original operational need was reliable
**WGU course codes** so Reddit posts could be filtered and analyzed at the course level.
In that pipeline, posts were filtered to cases referencing exactly one identifiable WGU
course, and course codes were the anchor that made that possible.

The catalog work has since expanded into a broader goal: building a **versioned history of
WGU's official curriculum and structure** across catalog editions. Two value streams now run
in parallel:

- **Research value** — course-level analysis of student Reddit discussion
- **Institutional value** — historical tracking of courses, programs, schools, certificates,
  and structural changes over time

Course codes are the bridge between student discussion, official catalog entities, and
historical curricular change. This is why code completeness, provenance, and cross-edition
consistency are critical requirements for the scraper — not incidental quality goals.

The frozen analysis corpus referenced in the Reddit project: **~1,103 posts, 242 WGU
courses, 51 subreddits**. That dataset already depends on the catalog-derived code list.

Long-term goal: answer "what changed at WGU between any two catalog dates" for programs,
courses, outcomes, and faculty — and link those changes to what students were discussing on
Reddit at the time.

---

## Operational dependency: current course-code inventory

The current course-code inventory is not only historically useful — it is an **active
dependency** for the Reddit pipeline. New Reddit posts continue to arrive and are processed
for course code at scrape time.

Any WGU course codes introduced after the capstone-era canonical list will be silently
missed in post matching unless the catalog-derived code list is kept current. Maintaining a
verified and current course list is therefore an **operational requirement**, not just
historical-analysis groundwork.

Concretely: if a new course is added to the catalog after our last extraction, Reddit posts
mentioning that course will not be recognized and will be excluded from course-level
analysis without any error signal.

---

## Debugging / verification rule (standing)

When diagnosing any parser discrepancy, always show representative raw-text context before
acting on the diagnosis. Do not rely on counts or extracted token lists alone.

Context to show:
- Enclosing section and fence (program name, line range)
- The triggering anchor or failure point
- Several rows before the anomaly
- The anomaly itself (the bad line)
- Several rows after the anomaly
- The block terminator (Total CUs or equivalent)
- What was parsed vs what was missed

This was established in the 2026-03-14 session: a raw-scan count discrepancy (890 vs 696)
was confirmed as a real bug only after showing actual raw lines from four programs across
four colleges, all exhibiting the same mid-table copyright footer pattern. The count alone
would not have been sufficient to distinguish a parsing gap from a scan methodology
difference.

Apply this rule when pairing with any fresh CC instance on parser work.

---

## Bug history: what was wrong and what was fixed

### V10 Steps 0–2 (all catalogs, fixed in V11)
- **Step 0** scanned lines before the first CCN only → captured 1 correct Business program,
  then pulled the rest from the Tuition section (wrong college assignments, tuition strings
  in program names).
- **Step 2 (sections_index)** depended on Step 0's wrong list → fence boundaries were
  miscalculated → course extraction was incomplete and misassigned across colleges.

### V11 fixes to Steps 0–2
1. Parse the program **index** (bullet list at top of Academic Programs) for canonical names
2. Parse **body blocks** via state machine anchored on `Total CUs` as hard terminator
3. Restrict section scan to `Academic Programs → Program Outcomes` (avoids tuition section
   and standalone courses/certificates)
4. Two regex fixes: `MBA` added to degree-heading pattern; `_` added to Total CUs code
   pattern (needed for `BSSWE_C`)

### Step 4 copyright-break bug (fixed 2026-03-14)
Mid-table PDF page footers (`© Western Governors University...`) appear in CCN course tables
wherever a program's course list spans a PDF page boundary. Step 4's extraction loop used a
single `break` for both copyright footers and `Total CUs` terminators. Every time a footer
fired, all remaining rows in that table were silently dropped.

- **Affected:** 49 programs across all four colleges; 142 unique codes missing.
- **Fix:** `parse_catalog_v11.py` line ~542 — split the condition:
  - `if FOOTER_COPYRIGHT.search(line): continue`
  - `if FOOTER_TOTAL_CUS.search(line): break`
- **Confirmed:** changing `break` → `continue` on copyright recovers all 142 codes;
  post-fix raw scan shows 838/838 match with 0 discrepancy.
- **Applies to all catalogs** — this bug was present for every edition V10 processed.
  V11 is now correct for 2026-03. Older-catalog runs must be re-verified.

---

## Catalog structure: 2026-03

### Section map (line numbers)
| Section | Lines | Notes |
|---|---|---|
| Cover / TOC | 0–151 | TOC has authoritative program list with page numbers |
| About WGU | 152–467 | Prose |
| Admissions | 468–972 | Prose |
| Tuition and Financial Aid | 973–1305 | **Parser trap** — college headers + degree-like names with tuition appended |
| Academic Policies | 1306–2138 | Prose |
| Standalone Courses and Certificates | 2139–2675 | Single courses, bundles, cert descriptions |
| **Academic Programs** | **2676–7635** | Index (bullet list) + all 114 program body blocks |
| Program Outcomes | 7636–13361 | Per-program bullet outcomes |
| Instructor Directory | 13362–14565 | `Last, First; Degree, University` by department |
| Certificates - Standard Paths | 14566–14780 | 16 cert programs, same CCN/Total CUs structure |

### Parsing anchors
| Anchor | Pattern | Notes |
|---|---|---|
| CCN header | `CCN Course Number Course Description CUs Term` | Starts every course table |
| Course row (full) | `^[A-Z]{2,5} \d{1,4} [A-Z0-9]{2,5} .+ \d+ \d+$` | May wrap to next line |
| Total CUs (AP) | `^([A-Z0-9_\-]+) \d{6} Total CUs: \d+$` | Hard program end; `_` needed for `BSSWE_C` |
| Total CUs (cert) | `^Total CUs: \d+$` | Cert section — no program code prefix |
| School header (body) | Exact match of 4 bare school names | NOT "School of X Programs" or "Tenets:" |
| School header (index) | `[School Name] Programs` | Index only |
| Copyright footer | `^©` | **Skip (continue), never break** — appears mid-table |
| Cert program name | `^Certificate: .+$` | Unique to cert section; identifies each cert block |

### Catalog naming inconsistencies (index vs body) — 18 unresolved
Not parser bugs — catalog authors used different conventions in the TOC/index vs body:

| Pattern | Index example | Body example |
|---|---|---|
| Parens vs dash for specializations | `M.S. Data Analytics (Data Science)` | `Master of Science, Data Analytics - Data Science` |
| "Endorsement X" vs "Endorsement Preparation Program, X" | `Endorsement Middle Grades Math` | `Endorsement Preparation Program, Middle Grades Math` |
| SE tracks: named in index, unnamed in body | `B.S. Software Engineering (Java Track)` | `Bachelor of Science, Software Engineering` |
| "in" connector in body | `M.S. Marketing (...)` | `Master of Science in Marketing, ...` |
| MBA abbreviated vs spelled | `MBA Information Technology Management` | `MBA, IT Management` |

These 18 gaps need a code-based alias table to resolve permanently.

### Known program code quirks
- `BSSWE_C` — underscore in code (C# track; distinguishes from Java `BSSWE`)
- Both tracks share version date `202303`, versioned together

---

## Course code reference (2026-03 ground truth)

### Academic Programs — 838 unique codes, all exactly 4 characters

| Pattern | Count | Examples | Description |
|---|---|---|---|
| `alpha1_digit3` | 800 | `C175`, `D388`, `E029` | WGU public C/D/E-code series |
| `alpha3_digit1` | 37 | `AFT2`, `QGT1`, `QFT1` | WGU internal competency-task codes |
| `alpha_only` | 1 | `PFIT` | One-off; Business IT Management Portfolio |

No AP code is shorter or longer than 4 characters. All are strict prefix-then-suffix
(letters followed by digits, or all letters — never interleaved).

### Certificates section — 52 unique codes, zero overlap with AP

Cert codes span lengths 2–6 and use shapes not seen in AP codes:

| Shape | Examples |
|---|---|
| 2-char alpha | `QB`, `HS` |
| 3-char alpha | `NLE`, `DMC` |
| alpha2 + digit1 | `BI1–BI3`, `FL1–FL3`, `PM1–PM4` |
| 4-char alpha | `AIRU`, `CSBE`, `CSFE`, `DCDV` |
| 5-char alpha | `AIAPP`, `DCADA` |
| alpha5 + digit1 | `ESHIP1–ESHIP3` |
| C/D-code + A suffix (17 codes) | `C715A`, `D072A`, `D685A`, … — cert-specific variants |
| alphanumeric mixed | `B2BS1–B2BS3` |

### Cert programs (16 total)
Accounting Fundamentals · Business Leadership · B2B Sales Fundamentals ·
Digital Marketing Fundamentals · Entrepreneurship Fundamentals ·
Management Skills for Supervisors · Project Management · Supply Chain Fundamentals ·
Nursing Leadership · AI Skills Fundamentals · Business Intelligence ·
Data Analytics Skills · Data Engineering Professional ·
Front-End Web Developer · Java Developer · ServiceNow Application Developer

---

## Current scope definitions

Two distinct lists exist and must be kept separate in outputs and downstream analysis:

| List | Scope | Unique codes | Source |
|---|---|---|---|
| **Degree-program course list** | Academic Programs section only | **838** | `courses_2026_03.csv` |
| **Full catalog course list** | Academic Programs + Certificates | **890** | AP + `certs_2026_03.csv` |

- Certificates contribute **52** disjoint codes. Zero overlap with AP codes.
- AP and cert code shapes are structurally different (AP: all 4-char; certs: 2–6 chars,
  many patterns). Do not merge them into a single undifferentiated list.
- The Reddit pipeline currently operates on AP-scope codes. If cert-scope codes are later
  added to post matching, that is a deliberate scope expansion, not a correction.

---

## College name history (reference data)
Applied via `pick_snapshot()` (greatest version ≤ catalog date):

| Since | School names |
|---|---|
| 2017-01 | College of Business · College of Health Professions · College of Information Technology · Teachers College |
| 2023-01 | → Leavitt School of Health |
| 2023-03 | → School of Education |
| 2024-02 | → School of Business |
| 2024-04 | → School of Technology |
| 2024-09 | + Certificates - Standard Paths |

2026-03 uses the **2024-09 snapshot**. No new renames since then.

---

## Archive coverage audit (updated 2026-03-14)

108 catalog text files in `data/raw_catalog_texts/`, covering 2017-01 → 2026-03.

### Missing editions (3 total — gap closed)

| Missing | Notes |
|---|---|
| 2017-02, 2017-04, 2017-06 | Early gaps — not present in the WGU HTML snapshot either; likely never published or published without a stable URL |

### Gap closure (2026-03-14)
8 editions added: **2025-07 → 2026-02**.
PDFs downloaded manually from WGU's institutional catalog page (CDN blocks programmatic access with HTTP 406).
Parsed with pdfplumber → `.txt` files in `data/raw_catalog_texts/`.
All 8 files verified: 1 `Academic Programs` header, 1 `Program Outcomes` header, 130–134 `Total CUs` hits, 2,599–2,664 broad course-row hits. Structurally consistent with 2026-03.

| Edition | Lines | TotalCUs hits | Notes |
|---|---|---|---|
| 2025-07 | 14,543 | 134 | |
| 2025-08 | 14,531 | 133 | |
| 2025-09 | 14,536 | 133 | |
| 2025-10 | 14,626 | 133 | |
| 2025-11 | 14,642 | 133 | |
| 2025-12 | 14,686 | 134 | |
| 2026-01 | 14,712 | 134 | |
| 2026-02 | 14,787 | 130 | Slightly lower TotalCUs — worth checking during parse |

### File size progression (structural notes)
- **2017-03 → 2018-10**: 7,400–8,000 lines. Not truncated — older catalogs simply had fewer
  programs. Line count grows steadily with program additions.
- **2024-09 jump**: 11,031 → 13,295 lines. Explained by addition of "Certificates - Standard
  Paths" section (~2,000+ lines). Matches `college_snapshots.json` 2024-09 entry.
- **2025-02 spike**: 13,614 → 14,632 — notable single-month jump. Now confirmed: +12 programs
  in 2025-02, followed by −5 in 2025-03. A large program addition wave, partially reversed.
- **2026-03**: 14,780 lines — consistent with gradual growth from 2025-06 (14,330).

### Program count jumps (from full-archive V11 run, 2026-03-14)
Notable single-month changes in body-block count (≥5):
| Edition | Before | After | Δ | Notes |
|---|---|---|---|---|
| 2017-07 | 67 | 62 | −5 | Program rationalization |
| 2022-06 | 66 | 73 | +7 | Expansion |
| 2024-09 | 93 | 98 | +5 | First certs section; program adds |
| 2025-02 | 101 | 113 | +12 | Largest single-month expansion in archive |
| 2025-03 | 113 | 108 | −5 | Partial reversal |
| 2025-07 | 108 | 115 | +7 | Expansion |

### File structure note on 2026-02
2026-02 shows 130 Total CUs hits vs 134 in adjacent months. Not a parsing failure — confirmed
structurally clean; the slightly lower count likely reflects fewer cert sub-blocks or a program
being removed. Parse it and diff against 2026-03 to confirm.

---

## Structural probe results (2026-03-14)

Probed 9 editions spanning 2017-01 → 2026-02. Key findings below.

### Era classification

Two structural eras exist, cleanly distinguished by the Total CUs terminator format:

**ERA_B — 2024_08 to present** (current V11 target)
- `Total CUs` line: `PROGCODE YYYYMM Total CUs: N` — program code and date on the **same** line
- Body section dividers: `School of X Programs` (with suffix, all 4 schools)
- 4 school names: School of Business / School of Technology / Leavitt School of Health / School of Education
- Formal `"School of X Tenets:"` bullet blocks
- Program Outcomes section: YES (from 2024_09)
- Certificates - Standard Paths section: YES (from 2024_09)
- V11 compatibility: **CLEAN** for all ERA_B editions

**ERA_A — 2017_01 to 2024_07**
- `Total CUs` line: standalone `Total CUs: N` — program code + date + `©` all on the **next** line
  - Next-line format: `PROGCODE YYYYMM © Western Governors University date page`
  - YYYYMM date stamp IS present in all tested ERA_A editions
- Body section dividers: bare college names (no "Programs" suffix) — except 2017_01 which has it for Business only
- College names vary by sub-era (see below)
- No Program Outcomes section
- No Certificates - Standard Paths section
- V11 as-is: **will misparse** ERA_A — current Total CUs regex matches `PROGCODE YYYYMM Total CUs:` and will not fire on standalone `Total CUs:` lines

### Known sub-era breakpoints

| Era boundary | What changed |
|---|---|
| **2024_09** | Program Outcomes section added; Certificates - Standard Paths section added (~2,000+ new lines) |
| **2024_08** | **Total CUs format flips** from standalone to `PROGCODE YYYYMM Total CUs: N`; body dividers gain "Programs" suffix; school renaming complete (all 4 "School of X" names) |
| **~2024_01–2024_07** | Transitional: College of IT → School of Technology rename occurring; school names mixed |
| **2023_01** | Leavitt School of Health name introduced (from College of Health Professions) |
| **2023_03** | School of Education name introduced (from Teachers College) |
| **2024_02** | School of Business name introduced (from College of Business) |
| **2024_04** | School of Technology name introduced (from College of Information Technology) |
| **~2020_11** | Formal `"X Tenets:"` bullet blocks appear (previously inline prose, 2019+; absent 2018 and earlier) |
| **~2019** | Inline college tenets prose paragraphs appear (no formal label) |
| **2017_01** | Index uses `"Online College of X"` prefix (not in body); only Business body divider has "Programs" suffix; no tenets at all |

### TOC duplication of "Academic Programs" header
Starting around 2023_12, "Academic Programs" appears **twice** — once in the TOC (~line 38) and
once in the body (~line 1962). ERA_A editions earlier than this have only one instance.
Parser must use the **last** standalone "Academic Programs" occurrence (or detect body vs TOC by
checking whether the next non-blank line is a page number vs a college/school name).

### Cert section
- **2024_08 and earlier**: no cert CCN tables at all. Certs listed narratively in "Standalone
  Courses and Certificates" section (prices only, no CCN block). V11 cert parser silently finds
  nothing — that is correct behavior, not a failure.
- **2024_09+**: `"Certificates - Standard Paths"` section present. Cert `Total CUs` lines are
  **standalone** (no PROGCODE prefix) even in ERA_B editions — cert programs have no AP code.

### Trust assessment

| Edition | Era | Viability | Notes |
|---|---|---|---|
| 2026_02, 2026_01, 2025_12, 2025_06 | ERA_B | **CLEAN** | Identical to baseline |
| 2024_08 | ERA_B | **CLEAN (degree parse)** | No cert tables — correct; no Program Outcomes — correct |
| 2023_12 | ERA_A | **MINOR FALLBACK** | Standalone Total CUs; TOC "Academic Programs" duplication; mixed school names |
| 2022_06 | ERA_A | **MINOR FALLBACK** | Standalone Total CUs; older college names (College of Health Professions, Teachers College) |
| 2019_01 | ERA_A | **MINOR FALLBACK** | Standalone Total CUs; pre-formal Tenets (inline prose); older names |
| 2017_01 | ERA_A | **MANUAL INSPECTION** | Unique "Online College of X" in index; inconsistent body dividers; no Tenets; copyright date in M/D/YY format |

### Proposed parsing strategy (feature-detection first)

Detect era at file-open time by scanning for the first `Total CUs:` occurrence:

```python
# ERA detection
if re.match(r'^[A-Z]{2,10}\s+\d{6}\s+Total CUs:', line):
    era = "B"   # code+date on same line
else:
    era = "A"   # standalone; code+date on next line
```

For ERA_A, after `Total CUs: N` fires as terminator, read the **next** line and extract the
program code from: `r'^([A-Z0-9_\-]{2,10})\s+(\d{6})\s+©'`

Secondary detection:
- College name normalization: map all historical name variants → BUSINESS / HEALTH / TECHNOLOGY / EDUCATION
- AP-line disambiguation: if "Academic Programs" appears more than once, use the last instance
- Tenets detection: skip blocks matching `r'^.{5,50}Tenets:'` (formal) or inline prose heuristic
  (college name line followed immediately by long prose before a CCN header)
- Cert section: optional; if absent, silently skip

---

## Known issues to resolve in older catalogs

| Issue | Likely affects | Status |
|---|---|---|
| Total CUs format: standalone vs same-line | ERA_A (2017_01–2024_07) | **CONFIRMED** — needs ERA_A handler in V11 |
| Program Outcomes section absent | ERA_A (all) | **CONFIRMED** — parser must not require it |
| Certificates - Standard Paths absent | Pre-2024_09 | **CONFIRMED** — parser must not require it |
| "Academic Programs" in TOC + body | 2023_12+ in ERA_A | **CONFIRMED** — use last occurrence |
| `"Online College of X"` in 2017_01 index only | 2017_01 only | **CONFIRMED** — body uses bare names; needs alias |
| `College of Business Programs` body divider (2017_01 Business only) | 2017_01 only | **CONFIRMED** — other 3 colleges bare |
| `MBA, IT Management` heading vs full name | Unknown crossover | Not verified |
| `BSSWE_C` underscore code | Likely introduced when C# track split | Not verified |
| "Master of Science in X" vs "Master of Science, X" | Unknown crossover | Not verified |
| M.Ed. 3 variants (K-12, Adult, Combined) | Unknown split date | Not verified |
| Step 4 copyright-break bug | **All V10-processed editions** — re-verify after V11 runs | Fixed in V11 |

---

## Immediate next priorities

### 1. ✅ DONE — Freeze trusted 2026-03 outputs
`outputs/trusted/2026_03/` contains the locked artifact set.

### 2. ✅ DONE — Produce current course list as first-class output
`courses_2026_03.csv` (AP, 838 codes) and `certs_2026_03.csv` (52 codes) are the clean
artifacts for downstream use and future diffing.

### 3. ✅ DONE — Archive coverage audit
100 files on disk, 11 editions missing (see above).

### 4. ✅ DONE — Acquire missing recent editions
2025-07 → 2026-02 downloaded and parsed (2026-03-14). 108 editions on disk. Only 3 early gaps remain (2017-02/04/06).

### 5a. ✅ DONE — Targeted raw-vs-parsed validation (2026-03-14)

14 structurally important editions validated. All **14/14 CLEAN** — raw independent scan
and parser output match exactly on all AP-shape course codes.

**Validation methodology:**
- Independent raw scan using two patterns (CCN_FULL + CODE_ONLY), no parser state machine
- AP section bounds: ERA_B ap→po; ERA_A ap→EOF
- Set difference: raw codes ∩ parsed codes; raw only; parsed only
- Any AP-shape discrepancy shown with surrounding raw-text context
- Script: `validate_editions.py`; results: `outputs/validation_report.json`

**One known catalog data defect found (not a parser error):**
`D627` (Public Health Education and Promotion) appears in 22 editions (2024-06 onward)
as a CODE_ONLY row — missing its `DEPT COURSENUM` prefix. All adjacent rows have full
CCN format; this is a catalog authoring error. Parser correctly captures it via CODE_ONLY
fallback. Raw scanner updated to use CODE_ONLY as secondary pattern to match.

**Target editions and trust status:**

| Edition | Era | Codes | Reason selected | Status |
|---|---|---|---|---|
| 2017-01 | A | 538 | Oldest; unique Online College prefix | ✅ CLEAN |
| 2019-01 | A | 609 | Pre-formal-tenets ERA_A | ✅ CLEAN |
| 2021-06 | A | 656 | Formal-tenets ERA_A | ✅ CLEAN |
| 2022-06 | A | 726 | +7 program count jump | ✅ CLEAN |
| 2023-01 | A | 740 | Leavitt School of Health rename | ✅ CLEAN |
| 2023-03 | A | 744 | School of Education rename | ✅ CLEAN |
| 2023-12 | A | 712 | TOC duplication; mixed school names | ✅ CLEAN |
| 2024-02 | A | 749 | School of Business rename | ✅ CLEAN |
| 2024-04 | A | 751 | School of Technology rename | ✅ CLEAN |
| 2024-07 | A | 780 | Last ERA_A | ✅ CLEAN |
| 2024-08 | B | 801 | First ERA_B; Total CUs format flip | ✅ CLEAN |
| 2024-09 | B | 824 | First cert section | ✅ CLEAN |
| 2025-02 | B | 883 | +12 program count jump (largest) | ✅ CLEAN |
| 2025-03 | B | 830 | −5 program count jump | ✅ CLEAN |

**Trust basis for unvalidated editions:**
Editions not individually validated are covered by structural continuity — each unvalidated
edition sits between two validated neighbors with no anomalies in the full-archive run.
The breakpoints, rename transitions, and count-jump editions were explicitly selected to
stress-test the parser assumptions most likely to fail. Clean results at all boundary
editions means intermediate editions carry strong implied validity.

### 5. ✅ DONE — Probe older catalogs strategically + implement ERA_A support
Probed 9 editions (2017-01 → 2026-02). Full breakpoint map in "Structural probe results"
section above. ERA_A support implemented in V11 (2026-03-14):
- Era auto-detected at file-open from first Total CUs format seen
- Standalone `Total CUs: N` handler; code extracted from next line
- Mid-page subtotal detection (next line is CCN header → skip, don't emit)
- `RE_DEGREE` updated: `MBA\b` word boundary; `Post-Baccalaureate` added; `©` exclusion
- `RE_BULLET` extended to include `●` (ERA_A bullet character)
- `parse_index`: ERA_A bare college-name headers with 10-line lookahead for bullets
- `locate_sections`: last AP occurrence (handles TOC duplication); PO optional
- Full archive run: **108 editions, 0 anomalies, 0 skips, 1,594 unique codes**

### 6. ✅ DONE — Build the change-tracking layer (first pass, 2026-03-14)

Script: `build_change_tracking.py`. All outputs in `outputs/change_tracking/`.

| Output | Contents |
|---|---|
| `course_history.csv` | 1,594 rows: code, status, title, CUs, first/last seen, edition count, colleges, title variants, first/latest programs |
| `program_history.csv` | 196 rows: program code, status, first/last seen, version progression, colleges, CU history, degree headings |
| `adjacent_diffs.json` | 107 adjacent-edition diffs: courses added/removed, programs added/removed, version changes |
| `adjacent_diffs_summary.csv` | 107 rows of counts only, for quick scanning |
| `summary_stats.json` | Archive-wide aggregate statistics |

**Key findings from first-pass analysis:**

| Metric | Value |
|---|---|
| Active codes (in 2026-03) | 838 |
| Retired codes (not in 2026-03) | 756 |
| Codes with title variants | 167 |
| Active programs | 114 |
| Retired programs | 82 |
| Programs with ≥1 version change | 100 |
| Codes in all 108 editions | 113 |

**Largest structural events in the archive:**

| Transition | Courses added | Courses removed | Programs Δ | Notes |
|---|---|---|---|---|
| 2017-05→2017-07 | +101 | −74 | +1 prog / −6 progs | Major: old AXX task codes retired; C-codes expand; grade-band teacher programs removed |
| 2025-01→2025-02 | +110 | −48 | +12 progs | Largest single-month program expansion; many new courses introduced with new programs |
| 2024-08→2024-09 | +57 | −55 | +9 progs / −4 progs | Endorsement program restructuring; new D6xx code series introduced |
| 2020-06→2020-07 | +54 | −65 | | Mid-archive significant restructuring |

**Notable historical patterns:**
- 113 course codes appear in all 108 editions — all are performance-task assessment codes (AFT2, AIT2, etc.), stable since 2017
- The 2017-05→2017-07 transition retired the old `AXX1`/`AXX2` format assessment codes and replaced them with C-codes — the most disruptive single event in the archive
- BSHIM (B.S. Health Information Management) has the most version changes: 11 across the archive
- 94 codes were retired before 2018 — almost all are the old performance-task assessment codes

**Data quality note — D627 (catalog authoring defect):**
`D627 Public Health Education and Promotion` appears in 22 editions (2024-06→2026-03) as a
CODE_ONLY row — missing its DEPT/COURSENUM prefix. All adjacent rows in the same table
have full CCN format. The parser captures it correctly via CODE_ONLY fallback. The raw
scanner was updated to use CODE_ONLY as a secondary pattern. Validation confirmed clean
(0 AP-shape codes in raw-but-not-parsed after fix). This is a WGU catalog authoring defect,
not a parser error. No action needed beyond this note.

### 7. ✅ DONE — Full per-edition change view (2026-03-14)

Script: `build_edition_diffs.py`. All outputs in `outputs/edition_diffs/`.

**Schema per transition (107 pairs):**

| Field | Type | Notes |
|---|---|---|
| from_catalog, to_catalog | YYYY-MM | Date range |
| courses_added[], courses_removed[] | lists | Code lists |
| courses_added_count, courses_removed_count | int | |
| course_churn | int | added + removed |
| net_course_change | int | |
| courses_with_title_changes[] | list | Genuine renames only (non-prefix) |
| courses_with_title_truncations[] | list | PDF line-wrap artifacts (shorter is prefix of longer) |
| title_changes_count | int | Genuine renames — severity counted |
| title_truncations_count | int | Artifacts — **excluded from severity** |
| courses_with_cu_changes[] | list | Same code, different CU value |
| cu_changes_count | int | |
| programs_added[], programs_removed[] | lists | |
| programs_added_count, programs_removed_count | int | |
| program_churn | int | added + removed |
| net_program_change | int | |
| programs_with_version_changes[] | list | Program codes with curriculum version bump |
| version_changes_detail[] | list | {program_code, from_version, to_version} |
| version_changes_count | int | |
| affected_colleges[] | list | Normalised: Business / Health / Technology / Education |
| affected_college_count | int | |
| severity_score | int | Documented formula below |
| notes | str | e.g. cert_section_added |

**Severity score formula:**
```
course_churn × 1 + program_churn × 10 + version_changes × 3
+ title_changes × 2 + cu_changes × 2 + extra_colleges × 5
```
(extra_colleges = college_count − 1, so first college is free)

| Output | Contents |
|---|---|
| `edition_diffs_full.json` | Complete schema for all 107 transitions |
| `edition_diffs_summary.csv` | Flat CSV with all scalar metrics |
| `edition_diffs_rollups.json` | Top-20 by each dimension |
| `edition_diffs_events.json` | 41 major event candidates (meet ≥1 threshold) |

**Archive totals:**
- 107 transitions, 24 zero-change pairs
- Total course churn: 1,934 (sum of all additions + removals)
- Total genuine title changes: 31
- Total PDF truncation artifacts (excluded): 144
- Total version changes: 239
- Major event candidates (≥ threshold on any dimension): 41

**PDF truncation artifact (2024-07→2024-08):**
141 apparent "title changes" at the ERA_A→ERA_B boundary are PDF text-extraction
artifacts: long titles in 2024-08 wrap across lines; the course row captures only the
first segment, making the title look shorter. Detected by checking if the shorter
string is a strict prefix of the longer — if so, classified as truncation and excluded
from severity. One genuine rename at this boundary: D601 changed from
"Data Storytelling for Diverse Audiences" → "Data Storytelling for Varied Audiences".

**Top-10 transitions by severity (derived from data, not pre-selected):**

| Transition | Severity | Course churn | Prog churn | Ver changes | Title changes | Colleges |
|---|---|---|---|---|---|---|
| 2025-01→2025-02 | 347 | 158 | 14 | 13 | 0 | Education, Health, Technology |
| 2017-05→2017-07 | 318 | 175 | 7 | 22 | 0 | Education, Technology |
| 2018-04→2018-05 | 301 | 61 | 23 | 0 | 0 | Education, Health, Technology |
| 2024-08→2024-09 | 240 | 91 | 13 | 3 | 0 | Business, Education, Technology |
| 2024-09→2024-10 | 187 | 101 | 5 | 7 | 0 | Business, Education, Health, Technology |
| 2022-12→2023-01 | 184 | 80 | 9 | 0 | 2 | Business, Health, Technology |
| 2020-06→2020-07 | 183 | 119 | 0 | 18 | 0 | Business, Education, Health |
| 2020-01→2020-02 | 171 | 41 | 13 | 0 | 0 | Business |
| 2020-10→2020-11 | 134 | 53 | 4 | 8 | 0 | Business, Education, Health, Technology |
| 2018-05→2018-06 | 124 | 4 | 12 | 0 | 0 | Education |

**Notable findings from data-driven ranking:**
- **2018-04→2018-05** (severity 301, rank 3): Surprise entry — 23 program churn. Eleven grade-band teacher programs (BASC9, BASCB12, BASCCH12, BASCG12, BASCPH12…) retired and 12 new programs added (BSCS, BSSEMG, BSSESB, BSSESC, BSSESE…). Major Education restructuring not visible in course count alone.
- **2018-05→2018-06** (severity 124): 12 more program churn in Education — follow-on wave from the April→May event.
- **2020-06→2020-07** (severity 183): 119 course churn, 18 version changes, 0 program count change — large course-content refresh without structural change.
- **2026-02→2026-03** (severity 60): 18 version changes, 1 course removed, 0 added — curriculum version bump across 18 Education programs simultaneously (most recent edition).
- **2017-01→2017-03** (severity 112): 14 genuine title changes — the "Pre-Clinical" → "Preclinical" batch rename (hyphen removal); also 13 version changes.
- **2020-01→2020-02** (severity 171): 13 program churn all in Business — hidden restructuring that doesn't appear in the headline course count.

**Rollup leaders by dimension:**

| Dimension | Leader | Value |
|---|---|---|
| Course churn | 2017-05→2017-07 | 175 |
| Program churn | 2018-04→2018-05 | 23 |
| Version changes | 2017-05→2017-07 | 22 |
| Title changes (genuine) | 2017-01→2017-03 | 14 |
| CU changes | 2017-05→2017-07 (tie) | 1 each |
| Colleges affected | 2017-01→2017-03 (tie, 5 others) | 4 |

### 8. ✅ DONE — Website data layer (2026-03-14)

Script: `build_site_data.py`. All outputs in `outputs/site_data/`.

**What was built:**

#### Step 1: Title variant classification
`outputs/site_data/title_variant_classification.csv` + `title_variant_summary.json`

- 167 codes with title variation, all classified
- Classification scheme: extraction_noise / formatting_only / punctuation_only / wording_refinement / substantive_change
- Counts: extraction_noise=145, punctuation_only=16, wording_refinement=3, substantive_change=2, formatting_only=1
- Only 2 genuinely substantive renames: **D346** and **D347** ("Psychological Care" → "Psychiatric Mental Health Care", confirmed 2022-12→2023-01 as part of Leavitt Health rename event)
- 1 code still needs manual review: **D344** (three truncated variants, canonical also truncated)
- Key finding: 145 of 167 title variants are PDF extraction artifacts (line-wrap truncations), not real renames
- Key data quality note: **D396** ("Evidenced-Based" → "Evidence-Based") — the canonical title in course_history is the typo form (most common historically); the correct form is in the override. 2026-03 extraction of D396 is also truncated; override corrects to full form.

#### Step 2: Canonical course intelligence table
`outputs/site_data/canonical_courses.csv` + `canonical_courses.json`

- **1,646 total codes**: 838 AP active, 756 AP retired, 52 cert
- Fields: course_code, canonical_title_current, observed_titles, first/last_seen, active_current, contexts_seen (AP/cert), current_programs, current_program_count, historical_programs, historical_program_count, edition_count, ghost_flag, single_appearance_flag, stability_class, title_variant_class, current_title_confidence, canonical_cus, current_college, colleges_seen, notes_confidence
- **ghost_flag** (14 codes): RETIRED AND edition_count ≤ 2. Single-appearance codes (13) are a subset. These are C4xx codes from 2017-01 retired by 2017-03, plus DTMG (2018-08→2018-09).
- **single_appearance_flag** (13 codes): appeared in exactly one catalog edition
- **stability_class** distribution: perpetual=113, stable=488, moderate=820, ephemeral=160, single=13, cert_only=52
- Cert codes have `first_seen_edition=2024-09` (section launch) with note that actual introduction date may differ
- For active AP codes, canonical_title_current uses 2026-03 catalog truth (or override for D396)
- D396 canonical_title override applied: "Evidence-Based Practice for Health and Human Services" (2026-03 extraction truncated)

#### Step 3: Named event layer
`outputs/site_data/named_events.csv` + `named_events.json` + `curated_major_events.json`

- **41 events** total (all threshold-crossing transitions from edition_diffs_events.json)
- **10 curated major events** with hand-written titles, observed/interpreted summaries, confidence ratings
- Event types (41 total): curriculum_version_wave=19, domain_reorganization=9, program_family_rebuild=8, composite=4, rename_cleanup=1
- 31 non-curated events have machine-generated observed_summary only; no interpreted_summary (suitable for v1 timeline with expandable detail)
- Curated events span: EVT-001 (2017-01→2017-03) through EVT-010 (2025-01→2025-02) in chronological order
- Observed/interpreted summaries kept strictly separate per design rules

#### Step 4: Static site-ready JSON exports
`outputs/site_data/exports/`

| File | Contents | Count |
|---|---|---|
| `courses.json` | Course cards (lightweight) for explorer + search | 1,646 |
| `courses/{code}.json` | Individual course detail files (active AP only) | 838 files |
| `events.json` | Full event layer (chronological) | 41 |
| `search_index.json` | Courses + programs for client-side search | 1,842 entries |
| `homepage_summary.json` | Curated data for all homepage modules | — |

`homepage_summary.json` includes: archive stats, active_by_school (multi-school corrected), recent_version_changes, newest_programs, recent_course_additions, curated_major_events_preview.

**Active courses by school** (courses in multiple schools counted in each):
- Business: 190, Health: 193, Technology: 200, Education: 299

**What is now ready for website implementation:**
- Homepage: search, orientation, curated event previews, newest programs, recent version changes
- Course explorer: all course cards with filters (active/retired, school, stability_class)
- Course page: full detail files for 838 active AP courses (title history, programs, stability, confidence)
- Timeline page: 41 events with 10 curated major events with full interpretation
- Methods/Data pages: all source files and field definitions in README_INTERNAL.md

**What remains blocked or deferred:**
- cert codes have no cross-edition tracking (first_seen = 2024-09 for all, actual intro dates unknown)
- 31 non-curated events lack interpreted_summary (acceptable for v1; can add incrementally)
- D344 canonical title is itself a truncation artifact — manual review needed when building course page for that code
- predecessor/successor inference not yet built
- program-page data not yet fully prepared (program_history.csv is sufficient for basic program pages but no per-edition course roster yet)
- Reddit integration not started

### 9. Extend to other sections (future)
- Program Outcomes (7636–13361) — already bounded, same per-program structure
- Instructor Directory (13362–14565) — `Last, First; Degree, University` per line
- Certificates - Standard Paths — per-edition cert tracking (only 2026-03 snapshot exists now)

**Primary goal:** answer "what changed at WGU between any two catalog dates" for programs,
courses, outcomes, and faculty.

**Research linkage goal:** connect course-level Reddit discussion to official catalog
history — tracking when courses first appear, disappear, move between programs, or change
CU weight, and reading student discourse against that timeline of official curricular change.
