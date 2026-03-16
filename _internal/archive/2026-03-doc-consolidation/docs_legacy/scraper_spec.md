# WGU Catalog Scraper System Specification

*Comprehensive documentation of all files, scripts, and outputs involved in the WGU catalog scraping and parsing system.*

**Last Updated:** March 2026  
**Archive Coverage:** January 2017 - March 2026 (108 editions)

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Source Data Acquisition](#2-source-data-acquisition)
3. [PDF Processing Pipeline](#3-pdf-processing-pipeline)
4. [Parser Architecture](#4-parser-architecture)
5. [Output Data Structure](#5-output-data-structure)
6. [Validation and Quality Assurance](#6-validation-and-quality-assurance)
7. [Change Tracking System](#7-change-tracking-system)
8. [Website Data Layer](#8-website-data-layer)
9. [Configuration and Dependencies](#9-configuration-and-dependencies)
10. [Known Issues and Limitations](#10-known-issues-and-limitations)

## 1. System Overview

The WGU catalog scraper is a multi-stage system that transforms WGU's public academic catalog PDFs into structured, versioned data suitable for analysis and website consumption.

### Core Components

- **Acquisition Layer**: Downloads PDFs from WGU's public catalog
- **Processing Layer**: Converts PDFs to text and parses structured data
- **Validation Layer**: Ensures data quality and consistency
- **Change Tracking Layer**: Tracks curriculum evolution over time
- **Website Layer**: Generates site-ready data exports

### Archive Statistics

- **Total editions**: 108 (2017-01 → 2026-03)
- **Missing editions**: 3 (2017-02, 2017-04, 2017-06)
- **Parser eras**: 2 (ERA_A: 2017-01→2024-07, ERA_B: 2024-08→2026-03)
- **Course codes**: 1,594 unique (838 active, 756 retired)
- **Program codes**: 196 unique (114 active, 82 retired)

## 2. Source Data Acquisition

### Primary Acquisition Script

**File:** `scripts/scrape_catalog.py`
- **Purpose**: Bulk download of historical catalog PDFs
- **Status**: Used for 2017-01 → 2025-06 editions
- **Limitation**: Failed for 2025-07 → 2026-03 due to WGU CDN blocking

### Manual Acquisition Process

**File:** `data/raw_catalog_pdfs/catalog_YYYY_MM.pdf`
- **Purpose**: Manual browser downloads for recent editions
- **Process**: Required due to WGU CDN blocking automated requests
- **Naming convention**: `catalog_YYYY_MM.pdf`

### Text Extraction

**Tool**: pdfplumber
**Output**: `data/raw_catalog_texts/catalog_YYYY_MM.txt`
- **Characteristics**: 
  - 600 KB - 1.3 MB per file
  - ~13,000 - 15,000 lines per file
  - Line-stripped, one PDF page boundary per blank line

## 3. PDF Processing Pipeline

### Main Parser

**File:** `WGU_catalog/parse_catalog_v11.py`
- **Purpose**: Primary parser for all 108 catalog editions
- **Era Support**: Handles both ERA_A and ERA_B formats
- **Output**: Structured program and course data

### Parser Architecture

1. **Era Detection**: Auto-detects catalog format from first Total CUs line
2. **Section Location**: Finds Academic Programs, Program Outcomes, Cert sections
3. **Index Parsing**: Extracts program list from TOC bullet list
4. **Body Parsing**: State machine for program blocks
5. **Course Extraction**: Regex-based course row parsing

### Key Regex Patterns

```python
RE_TOTAL_CUS        = re.compile(r'^([A-Z0-9_\-]+)\s+(\d{6})\s+Total CUs:\s*(\d+)')   # ERA_B
RE_TOTAL_CUS_A      = re.compile(r'^Total CUs:\s*(\d+)')                               # ERA_A
RE_DEGREE = re.compile(r'^(Bachelor|Master|Post.Master|Post-Baccalaureate|Certificate|Endorsement|Doctor|MBA)\b', re.IGNORECASE)
RE_COLLEGE_ANY = re.compile(r'^(Online )?(College of (Business|Health Professions|Information Technology)|Teachers College|School of (Business|Technology|Education)|Leavitt School of Health)')
```

### Supporting Scripts

**File:** `WGU_catalog/run_parser.py`
- **Purpose**: Batch runner for parse_catalog_v11.py
- **Function**: Processes all text files and generates outputs

**File:** `WGU_catalog/validate_editions.py`
- **Purpose**: Independent raw-vs-parsed validation
- **Method**: Re-scans raw text files and compares with parser output
- **Coverage**: 14 structurally critical editions validated

## 4. Parser Architecture

### Processing Pipeline

```
PDF text file
  → detect_era()           # Determine ERA_A or ERA_B
  → locate_sections()      # Find Academic Programs, Program Outcomes, Cert section
  → parse_index()          # Extract program list from TOC bullet list
  → parse_body_blocks()    # State machine: extract program blocks from body
  → extract_courses()      # Per-block: extract course rows from CCN tables
  → build_course_index()   # Aggregate all instances into cross-edition index
```

### Era Differences

**ERA_A (2017-01 → 2024-07):**
- Total CUs line: standalone `Total CUs: N`
- Program code on next line: `PROGCODE YYYYMM © Western Governors University [date] [page]`
- Section dividers: bare college names
- No Program Outcomes section
- No Certificates - Standard Paths section

**ERA_B (2024-08 → 2026-03):**
- Total CUs line: `PROGCODE YYYYMM Total CUs: N`
- Section dividers: `School of X Programs`
- Program Outcomes section present
- Certificates - Standard Paths section present

### Course Extraction Patterns

1. **CCN_FULL**: `^([A-Z]{2,5}) (\d{1,4}) ([A-Z0-9]{2,5}) (.+?) (\d+) (\d+)$`
   - Groups: DEPT, COURSENUM, CODE, TITLE, CUS, TERM
2. **CODE_ONLY**: `^([A-Z][A-Z0-9]{1,5}) (.+?) (\d+) (\d+)$`
   - Groups: CODE, TITLE, CUS, TERM
   - Used for catalog defects (e.g., D627 missing DEPT/COURSENUM)

## 5. Output Data Structure

### Directory Structure

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

### Key Output Files

#### Trusted Reference (2026-03)

**File:** `outputs/trusted/2026_03/courses_2026_03.csv`
- **Content**: 838 AP course codes with title, CUs, programs, colleges
- **Status**: Frozen baseline for all downstream work

**File:** `outputs/trusted/2026_03/certs_2026_03.csv`
- **Content**: 52 cert section course codes with title, CUs, cert program membership
- **Status**: Current snapshot (not yet tracked cross-edition)

#### Cross-Edition Aggregates

**File:** `outputs/helpers/course_index_v10.json`
- **Content**: One entry per unique course code across all 108 editions
- **Fields**: canonical_title, canonical_cus, instances[]
- **Total entries**: 1,594 unique codes

**File:** `outputs/program_names/YYYY_MM_program_blocks_v11.json`
- **Content**: Per-edition list of program body blocks
- **Fields**: college, degree, deg_idx, ccn_idx, end, code, version, cus
- **Count**: 108 files total

#### Change Tracking

**File:** `outputs/change_tracking/course_history.csv`
- **Content**: Lifecycle view for every course code
- **Fields**: course_code, status, canonical_title, first_seen, last_seen, edition_count, span_months, college_count, title_variant_count, etc.
- **Rows**: 1,594 (838 ACTIVE, 756 RETIRED)

**File:** `outputs/change_tracking/program_history.csv`
- **Content**: Lifecycle view for every program code
- **Fields**: program_code, status, first_seen, last_seen, edition_count, version_progression, colleges, etc.
- **Rows**: 196 (114 ACTIVE, 82 RETIRED)

#### Edition Diffs

**File:** `outputs/edition_diffs/edition_diffs_full.json`
- **Content**: 107 adjacent-edition diffs with full change analysis
- **Fields**: course_churn, title_changes, cu_changes, version_changes, affected_colleges, severity_score
- **Total entries**: 107 transitions

## 6. Validation and Quality Assurance

### Validation Methodology

**File:** `outputs/validation_report.json`
- **Method**: Independent raw-vs-parsed validation
- **Coverage**: 14 structurally critical editions
- **Result**: 14/14 CLEAN

### Validation Process

1. **Independent Scan**: Re-reads raw text files without parser state machine
2. **Pattern Matching**: Finds all lines matching course row patterns
3. **Comparison**: Compares raw code set with parser output
4. **Flagging**: Any AP-shape code in one set but not the other is flagged

### Target Editions

| Edition | Era | Reason | Status |
|---------|-----|--------|--------|
| 2017-01 | A | Oldest; unique format | CLEAN |
| 2019-01 | A | Pre-formal-tenets | CLEAN |
| 2021-06 | A | Formal-tenets | CLEAN |
| 2022-06 | A | +7 program jump | CLEAN |
| 2023-01 | A | Leavitt School rename | CLEAN |
| 2023-03 | A | School of Education rename | CLEAN |
| 2023-12 | A | TOC duplication | CLEAN |
| 2024-02 | A | School of Business rename | CLEAN |
| 2024-04 | A | School of Technology rename | CLEAN |
| 2024-07 | A | Last ERA_A | CLEAN |
| 2024-08 | B | First ERA_B | CLEAN |
| 2024-09 | B | First cert section | CLEAN |
| 2025-02 | B | +12 program jump | CLEAN |
| 2025-03 | B | -5 program jump | CLEAN |

### Known Data Quality Issues

1. **D627 Catalog Defect**: Missing DEPT/COURSENUM fields, handled via CODE_ONLY pattern
2. **Title Truncation**: 144 PDF line-wrap artifacts at ERA boundary (2024-07→2024-08)
3. **Index/Body Naming**: 18 programs have inconsistent naming between TOC and body
4. **Missing Editions**: 2017-02, 2017-04, 2017-06 not available

## 7. Change Tracking System

### Built by: `build_change_tracking.py`

**Input**: `outputs/helpers/course_index_v10.json`, `outputs/program_names/*_program_blocks_v11.json`
**Output**: `outputs/change_tracking/`

### Course History Analysis

- **Total course churn**: 1,934 (sum of adds + removes across 107 transitions)
- **Genuine title changes**: 31
- **CU changes**: 10
- **Perpetual courses**: 113 (present in all 108 editions)
- **Retired before 2018**: 94 (mostly old AXX-format assessment codes)

### Program History Analysis

- **Most volatile program**: BSHIM (11 version changes)
- **Programs with version changes**: 100 out of 196
- **Version progression**: Tracks exact month-year of each curriculum revision

### Edition Diff Analysis

**Built by**: `build_edition_diffs.py`
**Input**: `outputs/change_tracking/adjacent_diffs.json`, course index, program blocks
**Output**: `outputs/edition_diffs/`

#### Severity Score Formula

```
course_churn × 1
+ program_churn × 10
+ version_changes × 3
+ title_changes × 2
+ cu_changes × 2
+ extra_colleges × 5     (each college beyond first)
```

#### Top 5 Transitions by Severity

1. **2025-01→2025-02**: 347 (Graduate specialization split)
2. **2017-05→2017-07**: 318 (Domain reorganization)
3. **2018-04→2018-05**: 301 (Program family rebuild)
4. **2024-08→2024-09**: 240 (New program family launch)
5. **2024-09→2024-10**: 187 (Composite multi-event)

## 8. Website Data Layer

### Built by: `scripts/build_site_data.py`

**Purpose**: Generate site-ready data exports for the WGU Atlas website
**Environment Variables**:
- `WGU_REDDIT_PATH`: Path to wgu-reddit WGU_catalog/outputs/
- `WGU_ATLAS_DATA`: Path to wgu-atlas data directory

### Website Outputs

**File:** `outputs/site_data/canonical_courses.csv`
- **Content**: 1,646 course records with stability classifications
- **Fields**: course_code, canonical_title, status, contexts_seen, current_programs, historical_programs, ghost_flag, single_appearance_flag, stability_class, title_variant_class, etc.

**File:** `outputs/site_data/title_variant_classification.csv`
- **Content**: Classification of 167 course codes with title variation
- **Classes**: extraction_noise (145), punctuation_only (16), wording_refinement (3), substantive_change (2), formatting_only (1)

**File:** `outputs/site_data/named_events.csv`
- **Content**: 41 curated major events with severity and metadata
- **Fields**: event_id, from_date, to_date, observed_summary, interpreted_summary, event_type, confidence, homepage_suitable, timeline_suitable

### Static Site Exports

**File:** `outputs/site_data/exports/courses.json`
- **Content**: 1,646 course cards for website consumption

**File:** `outputs/site_data/exports/courses/{code}.json`
- **Content**: 838 active AP detail files

**File:** `outputs/site_data/exports/events.json`
- **Content**: 41 events for timeline page

**File:** `outputs/site_data/exports/search_index.json`
- **Content**: 1,842 entries (courses + programs) for search functionality

## 9. Configuration and Dependencies

### Python Dependencies

**Core Processing**:
- `pdfplumber`: PDF text extraction
- `re`: Regular expression patterns
- `json`: Data serialization
- `csv`: CSV output generation

**Validation**:
- Independent pattern matching for quality assurance

**Website Layer**:
- Environment variable configuration
- Path resolution for cross-repository data

### File Naming Conventions

**PDFs**: `data/raw_catalog_pdfs/catalog_YYYY_MM.pdf`
**Text**: `data/raw_catalog_texts/catalog_YYYY_MM.txt`
**Program Blocks**: `outputs/program_names/YYYY_MM_program_blocks_v11.json`
**Raw Course Rows**: `outputs/raw_course_rows/YYYY_MM_raw_course_rows.json`
**Anomalies**: `outputs/anomalies/anomalies_YYYY_MM.json`

### Version Control

- **Active parser**: `parse_catalog_v11.py` (all prior versions superseded)
- **Deprecated**: `parse_catalog.py`, `parse_catalog copy.py`, `Scraper_V10_config.py`
- **Trusted reference**: `outputs/trusted/2026_03/` (frozen, not regenerated)

## 10. Known Issues and Limitations

### Archive Coverage

- **Missing editions**: 2017-02, 2017-04, 2017-06
- **Impact**: Changes attributed to 2017-05→2017-07 may have occurred in two distinct steps

### Data Quality

- **D627 defect**: Missing DEPT/COURSENUM fields, handled via fallback pattern
- **Title truncations**: 144 PDF line-wrap artifacts at ERA boundary
- **Naming inconsistencies**: 18 programs have different names in index vs. body

### Scope Limitations

- **Program Outcomes**: Not yet parsed (lines 7636–13361 in 2026-03)
- **Instructor Directory**: Separate pipeline, not integrated
- **Certificate tracking**: Only current snapshot (2026-03), not cross-edition
- **Cross-edition identity**: No fuzzy matching for course/program renames

### Technical Constraints

- **CDN blocking**: Recent editions require manual download
- **PDF layout changes**: ERA_A/B format differences require separate handling
- **Memory usage**: Large course index (1,594 entries) requires efficient processing

### Migration Context

- **Source Repository**: `/Users/buddy/Desktop/WGU-Reddit/WGU_catalog/`
- **Target Repository**: `wgu-atlas` (public-facing website)
- **Migration Status**: Scripts and data have been copied to wgu-atlas with path adaptations
- **Build Script**: `scripts/build_site_data.py` adapted to use environment variables for cross-repo references

### Parser Architecture

- **Active Parser**: `parse_catalog_v11.py` handles both catalog eras (ERA_A: 2017-01 through 2024-07, ERA_B: 2024-08 through 2026-03)
- **Validation**: 14 structurally critical editions individually validated, all passed clean
- **Archive Coverage**: 108 public WGU catalog editions processed
- **Data Quality**: Extensive validation including 696 → 838 AP code correction story

### Website Integration

- **Static Build**: v1 site can be built entirely from pre-generated static files
- **No Runtime Dependencies**: Build script only needed when catalog data is updated
- **Data Separation**: Official catalog facts, discussion signals, and LLM-generated summaries kept separate
- **Editorial Content**: Curated event text embedded in build_site_data.py (recommendation to extract to separate JSON file)

### Future Enhancements

1. **Program Outcomes parsing**: Track learning outcome changes over time
2. **Instructor directory integration**: Link courses to instructor profiles
3. **Certificate cross-edition tracking**: Extend beyond current snapshot
4. **Identity resolution**: Implement alias tables for course/program renames
5. **Reddit integration**: Link catalog changes to student discussion

---

## References

- **Main documentation**: `docs/README_INTERNAL.md`
- **Archive coverage**: `docs/SCRAPE_LOG.md`
- **Website design**: `docs/website_design_plan.md`
- **Migration guide**: `docs/_internal/MIGRATION_HANDOFF.md`
- **Data specifications**: `docs/ATLAS_SPEC.md`