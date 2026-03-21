# Program Guides — Technical Readout

**Date:** 2026-03-20
**Status:** Analysis only — no implementation
**Purpose:** Understand `parse_catalog_v11.py` well enough to design a program-guide parser that reuses its good ideas without inheriting its catalog-specific assumptions. Also establishes a manifest-first corpus analysis plan before any parsing begins.

---

## 1. What `parse_catalog_v11.py` Actually Does

### Inputs

- Raw catalog `.txt` files, one per edition (108 editions: 2017-01 through 2026-03)
- Produced upstream by a separate PDF-to-text extraction step (not in this script)
- Each file is a continuous text stream — one line per PDF text row, stripped
- Supporting shared inputs: `college_snapshots.json`, `degree_duplicates_master.json` (external curation artifacts)

### ERA Detection

Before any parsing, the script determines which of two catalog format eras it's dealing with:

- **ERA_B** (2024-08+): `PROGCODE YYYYMM Total CUs: N` all on one line — program code, version, and CU count are co-located at the block terminator
- **ERA_A** (pre-2024-08): `Total CUs: N` is standalone; code and date appear on the next non-blank line as `CODE YYYYMM © ...`

Era is detected by scanning for the first `Total CUs` line and checking its format. This drives branching logic throughout all subsequent passes.

### Pass 0 — Section Location (`locate_sections`)

Scans the entire file for three hard section-header strings:
- `Academic Programs` — uses **last occurrence** (first occurrence is in the TOC; the body is the last one)
- `Program Outcomes` — uses first occurrence; absent in ERA_A
- `Certificates - Standard Paths` — uses first occurrence; absent in early editions

Returns line-number boundaries that constrain subsequent passes.

### Pass 1 — Program Index Parsing (`parse_index`)

Between the `Academic Programs` header and `Program Outcomes`, parses the **bullet-list index** at the top of the section. This is the TOC-style list of programs grouped by college.

- ERA_B: college headers are `School of X Programs` (with suffix)
- ERA_A: college headers are bare college names, but share the same namespace as body body headers — distinguished by looking ahead for a bullet character

Returns: `{ college → [display_name, ...] }` — a cross-reference used later for reconciliation.

### Pass 2 — Body Block Parsing (`parse_body_blocks`)

**The core state machine.** Operates over the same body region (AP → PO).

States: `IDLE → DEGREE_SEEN → IN_COURSES → emit → IDLE`

Transitions:
- `IDLE + school_name` → update school, stay IDLE
- `IDLE + degree_heading` → record deg_line + deg_idx, move to DEGREE_SEEN
- `DEGREE_SEEN + CCN_HEADER` → record ccn_idx, move to IN_COURSES
- `IN_COURSES + CCN_HEADER` → stay IN_COURSES (multi-page tables have repeated CCN headers)
- `IN_COURSES + Total_CUs` → emit block, reset to IDLE

Block output: `{ college, degree, deg_idx, ccn_idx, end, code, version, cus }`

Anomalies are collected: school change mid-block, Total CUs outside a block, CCN header with no preceding degree.

### Pass 3 — `sections_index` Building (`blocks_to_sections_index`)

Converts body blocks to the V10-compatible cross-edition format:
```
{ date: { college: { degree_heading: [start_line, end_line] } } }
```
Duplicate headings (same college + same degree text in one edition) are disambiguated by appending `[PROGRAM_CODE]` to the key.

### Pass 4 — Reconcile (`reconcile`)

Fuzzy-matches the program index (Pass 1) against the body blocks (Pass 2) by college + normalized title.

`normalize_degree()` handles:
- Expanding abbreviations (`B.S.` → `Bachelor of Science`)
- Stripping pathway qualifiers (`(BSN to MSN)`, `(Post-MSN)`)
- Removing `in` as a connector word
- Stripping `Specialization` suffix
- Lowercasing and collapsing whitespace

Reports: matched, missing\_in\_body, extra\_in\_body.

### Step 3 — Degree Snapshots

Loads canonical college ordering from `college_snapshots.json` and canonical program names from `degree_duplicates_master.json`. Produces `degree_snapshots_v10_seed.json` — the ordered, deduplicated program universe by edition.

### Step 4 — Course Index Building

For each block in `sections_index`, re-reads the catalog text and extracts course rows using three patterns in priority order:

| Pattern | Format | Notes |
|---|---|---|
| `CCN_FULL` | `DEPT NNNN CODE Title CUs Term` | Full row with CCN prefix |
| `CODE_ONLY` | `CODE Title CUs Term` | Code only, no CCN dept+number |
| `FALLBACK` | `Title CUs Term` | Title only when code extraction fails |

Builds `course_index_v10.json` (59 MB): one entry per course code, with all instances across all editions.

### Step 5 — CSV Export

Writes two flat CSVs: `courses_flat_v10.csv` (code + name) and `courses_with_college_v10.csv` (code + name + colleges).

### Output Artifacts

| Artifact | Per-edition | Cumulative |
|---|---|---|
| `{YYYY}_{MM}_program_index_v11.json` | ✓ | — |
| `{YYYY}_{MM}_program_blocks_v11.json` | ✓ | — |
| `anomalies_v11_{YYYY}_{MM}.json` | ✓ | — |
| `sections_index_v10.json` | — | ✓ |
| `degree_snapshots_v10_seed.json` | — | ✓ |
| `course_index_v10.json` | — | ✓ |
| CSVs | — | ✓ |

### Important Helpers and Conventions

- `detect_era()` — format-version branching before any structural scan
- `locate_sections()` — hard anchor scan; always returns line indices, not content
- State machine with explicit anomaly collection — never silently drops unexpected content
- `normalize_degree()` — lossy normalization only for matching, not stored in output
- Per-edition anomaly JSON — every anomaly has `type`, `line`, `text`, and context fields
- Verbose printed progress at each pass — shows counts, anomalies, reconcile results

---

## 2. Catalog-Specific Logic — Do Not Reuse Directly

These patterns are fundamental to multi-edition catalog parsing and have no meaningful analogue in per-program guide files.

| Logic | Why it's catalog-specific |
|---|---|
| Era detection (ERA_A/ERA_B) | Guides are point-in-time documents; no cross-edition format variance |
| Multi-edition loop | Guides are parsed once per file, not accumulated across 108 editions |
| Program index parsing (Pass 1) | Guides have no TOC bullet-list index of programs; they ARE the program |
| College/school headers as block separators | Catalog organizes multiple programs per school; each guide is one program |
| `Total CUs: N` as hard block terminator | Guides use a Standard Path table with per-row terms; no Total CUs terminator |
| `PROGCODE YYYYMM Total CUs: N` / `CODE YYYYMM © ...` line formats | Guides use `CODE YYYYMM © [copyright text] [date] [page]` at footers, not as terminators |
| `sections_index` / `degree_snapshots` | Cross-edition data structures; not relevant for per-program guides |
| Degree duplicate resolution | Catalog has inconsistent heading strings across editions; guides are self-consistent |
| Reconcile pass (index ↔ body) | No index to reconcile against in a guide |
| Cross-edition `course_index` building | Course index spans 108 editions; guide parsing is single-document |
| `college_snapshots.json` / `degree_duplicates_master.json` | Shared curation tables specific to the catalog universe |
| CCN header as course-table start anchor | CCN header (`CCN Course Number ...`) is catalog-specific; guides use `Course Description CUs Term` |

---

## 3. Reusable Patterns for Program Guides

These ideas from `parse_catalog_v11.py` transfer cleanly.

### Text loading and cleanup
```python
lines = [l.strip() for l in f]
```
The same clean-read pattern works for guide text files. Empty line filtering and stripped lines are correct assumptions for PDF-extracted text.

### Copyright/footer detection
The catalog skips lines matching `©`. Guide copyright lines take the exact same form:
```
BSDA 202309 © 2019 Western Governors University 5/1/23 20
```
The same `©` anchor skips these. Crucially, guide footers also yield program code, version (YYYYMM), and page number — all parseable from the footer as metadata.

### Footer-as-metadata pattern
In the catalog (ERA_A), `CODE YYYYMM © ...` on the next line after Total CUs gave code + version. In guides, the footer appears at every page break and gives the same fields. Parse footers once to extract:
- `program_code` — first token
- `version` — second token (YYYYMM)
- `pub_date` — date token (MM/DD/YY or similar)
- `page_number` — last token (integer)

### Section header detection via exact string match
```python
if line == 'Standard Path':
if line.startswith('Areas of Study'):
if line == 'Capstone':
```
Same strategy as `locate_sections()`. Exact string or startswith match, scanning full file for known section anchors, collecting line indices before any content parsing.

### State machine for boundary-delimited content
The IDLE → DEGREE_SEEN → IN_COURSES → emit pattern is the right approach for guides too, adapted for guide-specific states. Example for Areas of Study:

`IDLE → GROUP_SEEN → COURSE_SEEN → IN_DESCRIPTION → IN_COMPETENCIES → emit → IDLE`

### Anomaly collection with typed records
The pattern of `anomalies.append({'type': ..., 'line': ..., 'text': ..., ...})` should be preserved exactly. Every unexpected condition should have a named type.

### Three-tier course row pattern (for Standard Path)
The Standard Path table rows have a simpler structure than catalog rows:
```
[Title] [CUs] [Term]
```
This is analogous to the `FALLBACK` pattern in `anchors.py`:
```python
PATTERN_FALLBACK = re.compile(r'^(.+?)\s+(\d+)\s+(\d+)$')
```
Use this pattern (adapted for guide context) to parse Standard Path rows. The table header line `Course Description CUs Term` serves as the CCN_HEADER analogue — its presence signals the start of the table.

### Prerequisite and certification mentions via in-description scan
The catalog doesn't extract these, but the pattern of scanning block content for known phrases is the same technique. Look for:
- `"is a prerequisite"` / `"prerequisites"` in description text
- `"certification exam"` / `"prepares students for"` in description text

### Per-file output with consistent naming
`{CODE}_parsed.json`, `{CODE}_validation.json` — same naming convention as `{YYYY}_{MM}_program_blocks_v11.json`.

### Verbose progress reporting
The `print(f" ...")` pattern with counts and anomaly summaries should be preserved. Especially important during corpus analysis to surface outliers.

### JSON output format
```python
json.dump(obj, f, indent=2, ensure_ascii=False)
```
Same everywhere.

---

## 4. Proposed Program-Guide Parser Design

### What one script should do

`parse_guide.py` — the per-guide content parser:

**Input:** A single guide text file (`BSDA.txt`)
**Outputs:** `{CODE}_parsed.json`, `{CODE}_validation.json`

Passes:
1. **Metadata extraction** — scan all footer lines for program code, version, pub_date, page_count
2. **Section location** — scan for section anchors: title line, Standard Path, Areas of Study, Capstone, closing boilerplate
3. **Standard Path parsing** — extract `[title, cus, term]` rows from the Standard Path table
4. **Areas of Study parsing** — state machine over the AoS body, yielding area groups, course entries (title, description, competency bullets), prerequisite flags, cert-prep flags
5. **Capstone extraction** — special handling for the Capstone section (usually one course with a distinct competency format)
6. **Validation** — cross-check Standard Path course count against Areas of Study course count; flag mismatches, missing competencies, unexpected sections

### What should be split into separate scripts

`analyze_guide_manifest.py` — corpus-level structural probe (see §6):

- Reads all guide text files (or PDFs)
- Emits a manifest row per guide with structural presence flags
- Does NOT parse content — only characterizes presence/absence

`match_guide_courses.py` — title-to-code matching (separate from parsing):

- Takes `{CODE}_parsed.json` outputs
- Fuzzy-matches guide course titles against `data/canonical_courses.json`
- Emits a match report — not part of the structural parser

`build_guide_site_data.py` — downstream site artifact builder:

- Reads validated parsed guide JSONs
- Writes `public/data/program_guides/{code}.json` (runtime artifacts)
- Analogous to `build_site_data.py` in the catalog pipeline

### What the BSDA-only thin-slice parser should include

A minimal `parse_guide.py --program BSDA` (or `parse_guide_thin_slice.py`) that:

1. Reads `raw_texts/BSDA.txt`
2. Extracts metadata from footer lines
3. Locates section boundaries (Standard Path, Areas of Study, Capstone, closers)
4. Parses Standard Path rows into `[{title, cus, term}]`
5. Parses Areas of Study into `[{group, title, description, competencies[], has_prereq, has_cert_prep}]`
6. Parses Capstone course
7. Writes `BSDA_parsed.json` with all extracted fields
8. Writes `BSDA_validation.json` with:
   - section presence flags
   - course count (Standard Path vs AoS)
   - competency count per course
   - anomalies found
   - parseability confidence
9. Does NOT attempt code matching — that's a downstream step

---

## 5. Conventions Worth Keeping from `parse_catalog_v11.py`

| Convention | Application in guides |
|---|---|
| `lines = [l.strip() for l in f]` | Same clean-read pattern |
| Section anchors as line indices, not content | `locate_sections()` returns `{'Standard Path': N, 'Areas of Study': M, ...}` |
| State machine with named states | Use in AoS parsing: `IDLE → GROUP → COURSE → DESC → COMPETENCIES` |
| Typed anomaly records | `{'type': 'missing_standard_path', 'file': ..., ...}` |
| Verbose pass-by-pass print output | Show section indices, course counts, anomaly counts |
| Per-file output with program-code prefix | `BSDA_parsed.json`, `BSDA_manifest_row.json` |
| `indent=2, ensure_ascii=False` | Same JSON output style |
| ERA detection before anything else | Guide-equivalent: "guide family" detection before structural parsing |
| Anomaly log separate from parsed output | `{CODE}_validation.json` is separate from `{CODE}_parsed.json` |
| Collect ALL anomalies, don't stop on first | Same — continue parsing, collect every irregular line |
| `matched / missing / extra` reconciliation | In guides: Standard Path rows that have no matching AoS entry, and vice versa |
| `lib/anchors.py` as a separate constants file | `guide_anchors.py` for guide-specific regex patterns |
| Config via env vars or config module | `WGU_GUIDES_PATH`, `WGU_GUIDES_OUT` env vars |

---

## 6. Program-Guide Structure Understanding Requirements

### The BSDA guide structure (confirmed from raw text)

**Document structure (top to bottom):**

| Section | Lines (approx) | Key signals |
|---|---|---|
| Title block | 1–2 | `"Program Guidebook"` then degree name |
| Program description | 3–13 | Freeform paragraphs, degree-specific |
| Boilerplate intro | 14–188 | Fixed sections: CBE explanation, Accreditation, Degree Plan, Faculty, Orientation, Transfer, SAP, Courses, Learning Resources |
| **Standard Path** | 189–252 | `"Standard Path"` / `"Standard Path for [Degree]"` then `"Course Description CUs Term"` header; rows are `[Title] [CUs] [Term]` |
| Changes to Curriculum | 246–252 | Boilerplate, appears at end of Standard Path |
| **Areas of Study** | 255–826 | `"Areas of Study [Degree Name]"` then `"for"` on next line; groups > courses > descriptions > competency bullets |
| **Capstone** | 826–834 | Named section heading "Capstone", one course entry |
| Boilerplate closing | 836–859 | Accessibility, Student Services |

**Footer format (page break marker):**
```
BSDA 202309 © 2019 Western Governors University 5/1/23 N
```
Tokens: `CODE  VERSION  ©  [copyright text]  DATE  PAGE`
Regex: `^([A-Z][A-Z0-9_\-]+)\s+(\d{6})\s+©\s+.+\s+(\d{1,2}/\d{1,2}/\d{2,4})\s+(\d+)$`

**Standard Path table:**
- Header: `"Standard Path for [Degree Name]"` or `"Standard Path"`
- Sub-header: `"Course Description CUs Term"` (may repeat at page breaks)
- Row pattern: `^(.+?)\s+(\d{1,2})\s+(\d{1,2})$`
- CUs: 1–12 typical; Term: 1–N
- No course codes in this section
- "Changes to Curriculum" appears at end

**Areas of Study structure:**
- Section header: `"Areas of Study [Degree Name]"` + `"for"` next line (or inline variant)
- Intro boilerplate paragraph (2–3 lines, fixed text)
- Area/group headings: bare capitalized labels (e.g., `"Data Analytics"`, `"General Education"`)
- Per-course entry:
  - Course title (standalone line)
  - Description paragraph (possibly multi-line, wraps across lines)
  - `"This course covers the following competencies:"` (trigger line)
  - Competency bullets: `● [text]` (bullet may split across lines)
- Prerequisite mentions: in-description text, e.g., `"is a prerequisite for this course"` or `"The following course is a prerequisite: ..."`
- Cert-prep mentions: in-description text, e.g., `"prepares students for the following certification exam: CompTIA Project+"`

**Closing sections (boilerplate, end of every guide):**
- `"Accessibility and Accommodations"`
- `"Need More Information? WGU Student Services"`
- These bound the end of AoS/Capstone content

### Manifest fields — design for all 115 guides

Each manifest row covers one guide file. Fields:

```
source_pdf_filename       str    BSDA.pdf
program_code              str    BSDA (inferred from footer)
page_count                int    20 (from max page number in footers)
version                   str    202309
pub_date                  str    5/1/23
effective_date_inferred   str    2023-09 (YYYYMM → YYYY-MM)

# Section presence (boolean)
has_standard_path         bool
has_areas_of_study        bool
has_capstone_section      bool
has_course_descriptions   bool
has_competency_bullets    bool
has_term_structure        bool   (Standard Path has a Term column)
has_cu_values             bool   (Standard Path has a CUs column)
has_cert_prep_mentions    bool
has_prereq_mentions       bool
has_accreditation_section bool
has_boilerplate_closing   bool

# Counts
standard_path_course_count  int
aos_group_count             int
aos_course_count            int
competency_bullet_count     int
cert_prep_mention_count     int
prereq_mention_count        int

# Section headings detected (list)
section_headings_detected   list[str]

# Area/group names (list)
inferred_course_groups      list[str]

# Classification
likely_guide_family         str    e.g. "standard_bs" | "education_licensure" | "endorsement" | "nursing" | "graduate" | "certificate" | "track_variant"
template_type               str    e.g. "full" | "abbreviated" | "track_supplement"
parseability_confidence     str    "high" | "medium" | "low"

# Warnings
warnings                    list[str]
irregularities              list[str]
outlier_notes               str
```

---

## 7. Corpus-Level Structural Analysis Plan

### Questions the analysis must answer

1. Which sections are present in every guide? (safe to parse universally)
2. Which sections are present in most guides but not all? (parse conditionally)
3. Which sections are guide-family-specific? (parse with family branch)
4. Which individual guides are structural outliers? (may need custom handling)
5. What guide families / template types exist? (drives branching strategy)
6. Which fields are safe to extract universally? Which need guards?

### Guide families — hypothesis before analysis

Based on filename patterns:

| Family | Example codes | Hypothesis |
|---|---|---|
| `standard_ug` | BSDA, BSCS, BSIT, BSHA, BSACC | Full structure: Standard Path + AoS + Capstone |
| `education_ug` | BSSESB, BSSESC, BAELED, BAESELED | May have licensure/clinical sections, different AoS groups |
| `endorsement` | ENDECE, ENDELL, ENDSEMG | Likely abbreviated — may lack full AoS or Capstone |
| `graduate_standard` | MBA, MHA, MPH, MSHRM, MSITM | Full structure but graduate framing (8 CU/term SAP) |
| `graduate_track` | MSDADE, MSDADS, MSDADPE, MSSWEAIE, MSSWEDDD | Track variants — may share a common base with a track-specific section |
| `graduate_cs` | MSCSAIML, MSCSCS, MSCSHCI, MSCSIA, MSCSUG | CS graduate family |
| `nursing_msn` | MSNUED, MSNUFNP, MSNULM, MSNUPMHNP | Likely clinical/preceptor sections |
| `nursing_rn_msn` | MSRNNUED, MSRNNULM, MSRNNUNI | RN-to-MSN pathway variants |
| `nursing_pmc` | PMCNUED, PMCNUFNP, PMCNULM, PMCNUPMHNP | Post-Master's Certificate — possibly abbreviated |
| `macc_track` | MACC, MACCA, MACCF, MACCM, MACCT | Accounting specialization tracks |
| `mat` | MATEES, MATELED, MATMES, MATSESB, MATSESP, MATSSES | Master of Arts in Teaching |
| `mat_sped` | MATSPED | Special Education — possibly unusual structure |
| `education_grad` | MAMEK6, MAMEMG, MAMES, MASEMG, MASESB | Education graduate programs |
| `bs_prn` | BSPRN | Prelicensure nursing — likely clinical sections |
| `undergraduate_track` | BSCNEAWS, BSCNEAZR, BSCNECIS, BSSWE_C, BSSWE_Java | Track variants of base programs |

### Analysis approach

**Step 1 — Text extraction for all 115 guides** (one-time, outside the parser)

Use `pdftotext` (pdfminer or similar) to extract all 115 PDFs to `.txt`. BSDA.txt already exists. This step runs once; outputs committed to `raw_texts/`.

**Step 2 — `analyze_guide_manifest.py` (the corpus probe)**

Scan each text file with lightweight pattern matching only. No content extraction. For each file:
- Find all footer lines → extract code, version, pub_date, page count
- Scan for section header strings → record presence/absence and line index
- Count Standard Path rows (lines matching the row pattern)
- Count competency bullet lines
- Count cert-prep and prereq mention lines
- Record all detected standalone heading lines (candidate section headings)
- Assign a preliminary family classification based on code prefix

Output: `data/program_guides/guide_manifest.json` (115 rows)

**Step 3 — Section presence matrix**

From the manifest, build a CSV:
```
program_code | has_standard_path | has_aos | has_capstone | has_cu_values | ...
```
Sort by family. This makes outliers and family patterns visible at a glance.

**Step 4 — Family classification review**

Read the section presence matrix and manifest. Identify:
- Which hypothesized families hold up
- Which programs are outliers
- Which sections are universal, common-optional, or family-specific

**Step 5 — Manual spot-check of outliers**

For guides flagged `parseability_confidence: "low"` or with unusual section patterns, read the raw text directly before attempting to parse them.

---

## 8. Recommended Artifacts for the Analysis Phase

| Artifact | Location | Purpose |
|---|---|---|
| `guide_manifest.json` | `data/program_guides/` | Full corpus manifest — one row per guide, all structural fields |
| `section_presence_matrix.csv` | `data/program_guides/` | Boolean presence flags per guide, sorted by family — human-readable |
| `guide_family_classification.md` | `_internal/program_guides/` | Written classification report — families, outliers, branching decisions |
| `irregularities_report.md` | `_internal/program_guides/` | Specific guides with unusual structures, custom handling notes |
| `parseability_report.md` | `_internal/program_guides/` | Confidence levels, what is safe to parse universally vs conditionally |
| `BSDA_parsed.json` | `data/program_guides/` | First fully-parsed guide — validates the thin-slice parser |
| `BSDA_validation.json` | `data/program_guides/` | Validation report for BSDA — section presence, counts, anomalies |
| `BSDA_manifest_row.json` | `data/program_guides/` | Single manifest row for BSDA — seeds the manifest schema |

---

## 9. Recommended Pipeline Shape

### Phase A — Corpus understanding (manifest generation)

```
raw_pdfs/
   BSDA.pdf  BSCS.pdf  ...  (115 PDFs)
        ↓  [pdftotext — one-time, manual or scripted]
raw_texts/
   BSDA.txt  BSCS.txt  ...  (115 txt files)
        ↓  [analyze_guide_manifest.py]
data/program_guides/
   guide_manifest.json
   section_presence_matrix.csv
        ↓  [human review]
_internal/program_guides/
   guide_family_classification.md
   irregularities_report.md
   parseability_report.md
```

Purpose: characterize the entire corpus before assuming anything about parser structure.
Output: confidence that we know what we have before we try to parse it.

### Phase B — Thin-slice content parsing (BSDA first)

```
raw_texts/BSDA.txt
        ↓  [parse_guide.py --program BSDA]
data/program_guides/
   BSDA_parsed.json
   BSDA_validation.json
```

Purpose: validate parser design against a known-structure guide before scaling.
Gate: only proceed to Phase C if BSDA output validates cleanly.

### Phase C — Full corpus parsing

```
raw_texts/*.txt  (all 115)
guide_family_classification.md  (drives branching)
        ↓  [parse_guide.py --all OR parse_guide.py --family standard_ug]
data/program_guides/
   {CODE}_parsed.json  (per guide)
   {CODE}_validation.json  (per guide)
   parse_run_summary.json  (corpus-level: successes, failures, anomaly counts)
```

### Phase D — Site artifact build

```
data/program_guides/{CODE}_parsed.json  (validated)
        ↓  [build_guide_site_data.py]
public/data/program_guides/{code}.json  (runtime artifact)
public/data/program_guides_index.json   (all guides, lightweight listing)
```

### Phase E — Course code matching (separate)

```
data/program_guides/{CODE}_parsed.json
data/canonical_courses.json
        ↓  [match_guide_courses.py]
data/program_guides/{CODE}_course_matches.json
```

Course codes are absent from guide text. Matching titles to Atlas codes is a separate post-parsing step using fuzzy matching. Do not conflate with structural parsing.

### Pipeline visibility at every stage

After Phase A: know what sections are present in which guides; know the family structure.
After Phase B: know the parser works on a clean case.
After Phase C: know which guides parsed cleanly, which failed, which have anomalies.
After Phase D: know which guides are runtime-ready.
After Phase E: know which guide courses matched to Atlas codes.

---

## 10. Immediate First Implementation Target — BSDA Thin Slice

**Milestone definition:**

| Artifact | Description |
|---|---|
| `raw_texts/BSDA.txt` | Already exists |
| `BSDA_parsed.json` | Fully structured parsed output for BSDA |
| `BSDA_validation.json` | Validation report: section presence, counts, anomaly list |
| `BSDA_manifest_row.json` | Single manifest row seeding the full manifest schema |

**`BSDA_parsed.json` target schema:**
```json
{
  "program_code": "BSDA",
  "version": "202309",
  "pub_date": "5/1/23",
  "page_count": 20,
  "degree_title": "Bachelor of Science, Data Analytics",
  "program_description": "...",
  "standard_path": [
    {"title": "Introduction to Analytics", "cus": 2, "term": 1},
    ...
  ],
  "areas_of_study": [
    {
      "group": "Data Analytics",
      "courses": [
        {
          "title": "Introduction to Analytics",
          "description": "...",
          "competencies": ["...", "..."],
          "has_prereq": false,
          "prereq_text": null,
          "has_cert_prep": false,
          "cert_prep_text": null
        }
      ]
    }
  ],
  "capstone": {
    "title": "Data Analytics Capstone",
    "description": "...",
    "competencies": ["..."]
  },
  "anomalies": []
}
```

**`BSDA_manifest_row.json` target schema:**
```json
{
  "source_pdf_filename": "BSDA.pdf",
  "program_code": "BSDA",
  "page_count": 20,
  "version": "202309",
  "pub_date": "5/1/23",
  "has_standard_path": true,
  "has_areas_of_study": true,
  "has_capstone_section": true,
  "has_course_descriptions": true,
  "has_competency_bullets": true,
  "has_term_structure": true,
  "has_cu_values": true,
  "has_cert_prep_mentions": true,
  "has_prereq_mentions": true,
  "standard_path_course_count": 41,
  "aos_group_count": 8,
  "aos_course_count": 41,
  "competency_bullet_count": 130,
  "section_headings_detected": ["Standard Path", "Areas of Study", "Capstone", "Accessibility and Accommodations"],
  "inferred_course_groups": ["Data Analytics", "Business of IT", "Scripting and Programming", "Business Core", "Data Management", "Business Management", "General Education", "Computer Science"],
  "likely_guide_family": "standard_bs",
  "template_type": "full",
  "parseability_confidence": "high",
  "warnings": [],
  "irregularities": [],
  "outlier_notes": ""
}
```

**Framing:** The BSDA thin slice is not a one-off. Every design decision — state machine states, section anchor strings, anomaly type names, output schema fields — must be made with the full 115-guide corpus in mind. BSDA validates the design; the manifest analysis validates that the design generalizes.

---

## Key Structural Notes for Parser Design

### No course codes in guides
This is the biggest difference from catalog parsing. The Standard Path table and Areas of Study section both reference courses by title only. Matching to Atlas course codes is a downstream step, not a parser responsibility.

### Boilerplate is structural noise
Pages 1–5 (approx) of every guide are fixed boilerplate: CBE explanation, accreditation block, degree plan overview, faculty interaction, orientation, transfer credit, SAP rules, Courses section, Learning Resources. These sections contain no program-specific data and should be skipped entirely. The section anchor for Standard Path is the practical start of useful content.

### Multi-page table handling
Both Standard Path and Areas of Study span multiple pages. Footer lines (`CODE YYYYMM © ...`) appear at page breaks mid-table. Parser must skip footer lines without ending the current section parse.

### "Course Description CUs Term" is a repeated table header
This line appears at the top of Standard Path and may repeat at page breaks within the table (PDF layout artifact). Parser must detect and skip repeated header lines.

### Areas of Study header variant
BSDA uses:
```
Areas of Study Bachelor of Science, Data Analytics
for
```
(Two lines — degree name inline with "Areas of Study", then "for" on the next line.) Other guides may vary. The anchor should match `line.startswith("Areas of Study")`.

### Capstone is a named section
"Capstone" appears as a standalone heading before the capstone course entry. It's the last content section before boilerplate closing. This provides a clean upper bound for Areas of Study parsing.

### Closing boilerplate as AoS end bound
`"Accessibility and Accommodations"` is a reliable end-of-content marker. Parsers should stop AoS extraction when this line is encountered.
