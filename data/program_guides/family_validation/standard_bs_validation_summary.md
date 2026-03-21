# Standard BS Family Validation Summary

**Date:** 2026-03-20 (session 12 continuation)
**Purpose:** Confirm that the BSDA thin-slice parser generalizes across the `standard_bs` family before broader `--all` rollout.

---

## Sampled Guides

| Code | Declared Family | Version | Pub Date | Sections | SP Rows | AoS Groups | AoS Courses | Empty Desc | Empty Comp | Anomalies | Warnings | Confidence |
|------|-----------------|---------|----------|----------|---------|------------|-------------|-----------|-----------|-----------|----------|------------|
| BSDA | standard_bs | 202309 | 5/1/23 | SP, AoS, Capstone, Accessibility | 42 | 14 | 41 | 0 | 0 | 0 | 0 | **HIGH** |
| BSCS | cs_ug (IT stretch) | 202412 | 8/2/24 | SP, AoS, Accessibility | 37 | 12 | 37 | 0 | 0 | 0 | 0 | **HIGH** |
| BSIT | standard_bs | 202604 | 11/20/2025 | SP, AoS, Accessibility | 35 | 12 | 35 | 0 | 0 | 0 | 0 | **HIGH** |
| BSMGT | standard_bs | 202605 | 1/12/2026 | SP, AoS, Capstone, Accessibility | 36 | 5 | 35 | 0 | 0 | 0 | 0 | **HIGH** |
| BSPSY | standard_bs | 202404 | 2/16/24 | SP, AoS, Accessibility | 34 | 4 | 34 | 0 | 0 | 0 | 0 | **HIGH** |

**Result: all 5 guides parse at HIGH confidence with 0 anomalies and 0 warnings.**

---

## Standard Path Row Count vs AoS Course Count

| Code | SP Rows | AoS Courses | Delta |
|------|---------|-------------|-------|
| BSDA | 42 | 41 | +1 (capstone counted in SP) |
| BSCS | 37 | 37 | 0 |
| BSIT | 35 | 35 | 0 |
| BSMGT | 36 | 35 | +1 (capstone counted in SP) |
| BSPSY | 34 | 34 | 0 |

SP row count closely matches AoS course count in all cases. The +1 delta in BSDA and BSMGT is expected (capstone is listed in the SP table but handled as a separate section in AoS parsing).

---

## Cert-Prep and Prereq Mentions

| Code | Cert-Prep Mentions | Prereq Mentions |
|------|-------------------|-----------------|
| BSDA | 4 | 7 |
| BSCS | 0 | 7 |
| BSIT | 8 | 4 |
| BSMGT | 2 | 2 |
| BSPSY | 1 | 3 |

Extraction is functional. Cert-prep mentions found inline in descriptions using established patterns.

---

## Structural Variants Discovered

### Footer / Metadata Format
Three formats exist across the sample:

| Format | Example | Guides | Handled |
|--------|---------|--------|---------|
| **Single-line footer** | `BSDA 202309 © 2019 Western Governors University 5/1/23 7` | BSDA, BSPSY | ✓ (existing FOOTER_RE) |
| **Split footer** | `BSCS 202412` / blank / `© 2019 Western Governors University 8/2/24` / blank / `6` | BSCS | ✓ (new FOOTER_CODE_ONLY_RE + is_footer updates) |
| **Header-line metadata** | Line 3: `Program Code: BSIT Catalog Version: 202604 Published Date: 11/20/2025` | BSIT, BSMGT | ✓ (new HEADER_META_RE in extract_metadata) |

### Standard Path Table Format
Two formats exist:

| Format | Structure | Guides | Handled |
|--------|-----------|--------|---------|
| **Single-line row** | `"Title  CUs  Term"` on one line | BSDA | ✓ (original parse_standard_path) |
| **Multi-line row** | Title / CUs / Term each on separate lines | BSCS, BSIT, BSMGT, BSPSY | ✓ (new parse_standard_path_multiline) |

Column header is `"Course Description"` in BSDA/BSCS/BSMGT and `"Course Title"` in BSIT — both handled via updated SP_HEADER_RE.

### Capstone Section
Present in BSDA and BSMGT. Absent in BSCS, BSIT, BSPSY. Parser handles both cases gracefully.

---

## What Assumptions Held

- Standard Path section always present and locatable via `^Standard Path` anchor
- Areas of Study section always present with consistent group → course → description → competencies structure
- Footer lines of all three formats reliably skippable
- Competency trigger string (`"This course covers the following competencies:"`) universal across all 5 guides
- `pending_titles` buffer (1 item = course title; 2 items = group heading + course title) correctly disambiguates all AoS headings
- `looks_like_prose()` (len > 80 OR ends with sentence punctuation) reliably distinguishes intro boilerplate from first group heading
- Cert-prep and prereq extraction functional without changes

## What Assumptions Failed

- **BSDA's single-line SP format is not universal** — 4/5 non-BSDA guides use multi-line format. Required new `parse_standard_path_multiline()`.
- **BSDA's single-line footer is not universal** — split-footer and header-line formats exist in newer guides. Required `FOOTER_CODE_ONLY_RE` and `HEADER_META_RE`.
- **SP column header `"Course Description"` is not universal** — BSIT uses `"Course Title"`. Required updated `SP_HEADER_RE`.
- **Capstone section is not universal** — absent in 3/5 sampled guides. (Already handled gracefully.)
- **Page numbers in split-footer format appear between footer lines** — must track footer proximity (`prev_was_footer`) to avoid consuming page numbers as CU values.

---

## Parser Bugs Fixed During Validation

5 bugs found and fixed, all during session 12 (this session):

1. `PAGE_NUM_RE` was incorrectly skipping CU and term values in the multi-line SP parser (1-3 digit numbers are ambiguous with page numbers in that context). Removed from SP parser; kept for AoS.
2. `"Course Description"` repeated at page-top column headers caused `sp_expected_term_got_text` (the header was treated as a course title). Added `HEADER_LINE_RE` skip mid-table.
3. Page number after footer was consumed as CU value (page break between title and CU). Added `prev_was_footer` flag; page numbers immediately following footer lines are skipped.
4. `"Total CUs 110"` treated as title because 3-digit number doesn't match `INT_RE = r'^\d{1,2}$'`. Added `SP_TOTAL_RE` break.
5. Blank lines reset footer-proximity tracking in metadata extractor, causing pub_date/page_count to be lost for split-footer guides. Fixed by not resetting `prev_code_seen` on blank lines.

---

## Rollout Recommendation

### READY for `standard_bs --all`

All conditions met:
- All 5 sampled guides parse at HIGH confidence with 0 anomalies and 0 warnings
- Both SP table formats (single-line and multi-line) are handled
- All 3 footer/metadata formats are handled
- AoS state machine is robust across 4–14 groups and 34–42 courses per guide
- No structural edge cases remain unhandled in the sample
- Cert-prep and prereq extraction operational

### Caveats / Open Items Before `--all`

| Item | Risk | Action |
|------|------|--------|
| BSMES (standard_bs with Student Teaching / Clinical Experiences sections) not sampled | Medium — variant sections after capstone may cause parse artifacts | Run BSMES specifically; inspect before including in `--all` if desired |
| Page count extraction missing for header-line format guides | Low — cosmetic only | Known issue; non-blocking |
| SP/AoS title reconciliation uses string exact-match | Medium — minor title differences (US vs U.S.) may cause false mismatches | Non-blocking but should be reviewed in `--all` output |

### Suggested `--all` invocation

Filter to standard_bs family codes using the guide_manifest.json family classification, verify, then run:

```bash
python3 scripts/program_guides/parse_guide.py --all
```

Review `manifest_summary.json` after to confirm all standard_bs guides show HIGH confidence.

---

## Files Produced

| File | Description |
|------|-------------|
| `data/program_guides/parsed/BSCS_parsed.json` | Full parse output |
| `data/program_guides/parsed/BSIT_parsed.json` | Full parse output |
| `data/program_guides/parsed/BSMGT_parsed.json` | Full parse output |
| `data/program_guides/parsed/BSPSY_parsed.json` | Full parse output |
| `data/program_guides/validation/BSCS_validation.json` | Confidence=HIGH |
| `data/program_guides/validation/BSIT_validation.json` | Confidence=HIGH |
| `data/program_guides/validation/BSMGT_validation.json` | Confidence=HIGH |
| `data/program_guides/validation/BSPSY_validation.json` | Confidence=HIGH |
| `data/program_guides/manifest_rows/BSCS_manifest_row.json` | Manifest row |
| `data/program_guides/manifest_rows/BSIT_manifest_row.json` | Manifest row |
| `data/program_guides/manifest_rows/BSMGT_manifest_row.json` | Manifest row |
| `data/program_guides/manifest_rows/BSPSY_manifest_row.json` | Manifest row |
| `data/program_guides/family_validation/standard_bs_validation_summary.json` | This summary (JSON) |
| `data/program_guides/family_validation/standard_bs_validation_summary.md` | This summary (Markdown) |
