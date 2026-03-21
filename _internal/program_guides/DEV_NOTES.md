# Program Guide Extraction — DEV NOTES

---

## Session 13 — standard_bs Family Validation (2026-03-20)

### Guides sampled
BSDA (thin-slice baseline), BSCS (cs_ug stretch), BSIT, BSMGT, BSPSY — all at HIGH confidence, 0 anomalies, 0 warnings after parser fixes.

### Whether BSDA assumptions generalized

Most AoS assumptions held. The pending-titles buffer, looks_like_prose(), and state machine (INTRO → SEEKING → IN_DESCRIPTION → IN_COMPETENCIES) worked correctly across all 5 guides without any changes.

The Standard Path parser required significant extension:
- BSDA's single-line SP row format is not universal. 4/5 sampled guides use multi-line format (title, CUs, term each on separate lines). Added `parse_standard_path_multiline()` with format detection.
- Column headers across guides: "Course Description" (BSDA/BSCS/BSMGT) vs "Course Title" (BSIT).

Footer/metadata format also varies:
- BSDA: single-line `"CODE YYYYMM © Western Governors University date page"`
- BSCS/BSPSY: split-footer — code+version on one line, © on another, page number on a third
- BSIT/BSMGT: header-line metadata on document line 3: `"Program Code: X Catalog Version: Y Published Date: Z"`

### Newly discovered structural variants

| Variant | Guides | Impact |
|---------|--------|--------|
| Multi-line SP table format | BSCS, BSIT, BSMGT, BSPSY | Required new SP parser |
| Split footer (code + © + page number on separate lines) | BSCS, BSPSY | Required FOOTER_CODE_ONLY_RE, is_footer() update |
| Header-line metadata (line 3 of document) | BSIT, BSMGT | Required HEADER_META_RE in extract_metadata |
| Column header "Course Title" instead of "Course Description" | BSIT | Required SP_HEADER_RE update |
| No Capstone section | BSCS, BSIT, BSPSY | Already handled gracefully |
| Page numbers between footer lines (split format) | BSCS | Required prev_was_footer flag in SP parser |
| "Total CUs N" at end of SP table | BSIT, BSMGT | Required SP_TOTAL_RE break |
| Column headers repeated at top of new pages | BSCS | Required HEADER_LINE_RE mid-table skip |

### 5 parser bugs fixed during family validation

1. `PAGE_NUM_RE` skipping CU/term values in multi-line SP parser — removed from SP parser
2. `"Course Description"` mid-table treated as title — added HEADER_LINE_RE skip
3. Page number after footer consumed as CU value — added `prev_was_footer` tracking
4. `"Total CUs 110"` (3 digits) treated as title — added SP_TOTAL_RE break
5. Blank lines reset footer-proximity in metadata extractor — fixed by not resetting on blank lines

### Recommendation: READY for standard_bs `--all`

All 5 sampled guides: HIGH confidence, 0 anomalies, 0 warnings. Both SP formats handled. All 3 footer formats handled. AoS state machine robust across 4–14 groups and 34–42 courses.

**Open items before `--all`:**
- BSMES (standard_bs with Student Teaching / Clinical Experiences) — run specifically before batch
- Page count extraction for header-line format guides returns 0 — cosmetic, non-blocking
- SP/AoS title reconciliation uses exact string match — minor differences may appear in batch output

### Artifacts produced

- `data/program_guides/parsed/BSCS_parsed.json` + BSIT, BSMGT, BSPSY
- `data/program_guides/validation/BSCS_validation.json` + BSIT, BSMGT, BSPSY (all HIGH)
- `data/program_guides/manifest_rows/BSCS_manifest_row.json` + BSIT, BSMGT, BSPSY
- `data/program_guides/family_validation/standard_bs_validation_summary.json`
- `data/program_guides/family_validation/standard_bs_validation_summary.md`

---

## Session 12 — Phase A + BSDA Thin-Slice DEV NOTES (2026-03-20)

---

## What was built

### Scripts created

| Script | Purpose |
|--------|---------|
| `scripts/program_guides/extract_guide_texts.py` | Converts PDFs to .txt via pdftotext subprocess; skips existing unless --force |
| `scripts/program_guides/analyze_guide_manifest.py` | Lightweight structural probe of all guide texts; produces manifest, presence matrix, summary |
| `scripts/program_guides/parse_guide.py` | Full content parser; thin-slice targeting BSDA; multi-pass pipeline with AoS state machine |

### Data artifacts created

| Artifact | Location | Notes |
|----------|----------|-------|
| 114 extracted .txt files | `~/Desktop/WGU-Reddit/.../raw_texts/` | External; not committed |
| `guide_manifest.json` | `data/program_guides/` | 115 rows; 30+ fields per guide |
| `section_presence_matrix.csv` | `data/program_guides/` | Section flags across all 115 guides |
| `manifest_summary.json` | `data/program_guides/` | Summary stats, family breakdown, variant headings |
| `BSDA_parsed.json` | `data/program_guides/parsed/` | Full parse result for BSDA |
| `BSDA_validation.json` | `data/program_guides/validation/` | Confidence=high, 0 anomalies, 0 warnings |
| `BSDA_manifest_row.json` | `data/program_guides/manifest_rows/` | Per-guide manifest row for BSDA |

---

## Extraction results

- **Total PDFs**: 115
- **Converted**: 114 (all succeeded)
- **Skipped**: 1 (BSDA — already extracted previously)
- **Failed**: 0
- **Tool**: `pdftotext` (Homebrew poppler); output matches pre-existing BSDA.txt format exactly

---

## Manifest overview (115 guides)

**By family:**

| Family | Count |
|--------|-------|
| standard_bs | 19 |
| education_ba | 11 |
| education_ma | 9 |
| teaching_mat | 9 |
| graduate_standard | 9 |
| cs_ug | 8 |
| endorsement | 8 |
| accounting_ma | 5 |
| cs_grad | 5 |
| nursing_msn | 5 |
| education_bs | 4 |
| swe_grad | 4 |
| nursing_pmc | 4 |
| mba | 3 |
| data_analytics_grad | 3 |
| nursing_rn_msn | 3 |
| nursing_ug | 2 |
| education_grad | 2 |
| healthcare_grad | 2 |

**By confidence:**
- HIGH: 18 guides
- MEDIUM: 97 guides

The 97 MEDIUM guides have 2 warnings each in the manifest probe. The most common warning is `no_sp_rows_found` and `no_aos_groups_found` — the lightweight manifest prober uses simpler heuristics than the full parser and will be updated in Phase C once the content parser covers more families.

**Notable variant sections (29 guides):**
- `Student Teaching`, `Clinical Experiences` — education programs (BAELED, BSMES, MATSPED, etc.)
- `Field Experience` — ENDELL, MAELLP12
- `Prerequisites` — BSCSIA, BSFIN, BSPRN, MSCSIA
- `Practicum` — MSEDL
- `Post-Master` — PMCNUED, PMCNUFNP, PMCNULM, PMCNUPMHNP
- `Licensure` — BASPEE

---

## BSDA thin-slice parse results

```
Metadata:      code=BSDA  version=202309  pub_date=5/1/23  pages=21
Sections:      Standard Path, Areas of Study, Capstone, Accessibility
Standard Path: 42 rows, 0 anomalies
Areas of Study: 14 groups, 41 courses, 0 anomalies
Capstone:      'Data Analytics Capstone', 1 bullet
Confidence:    HIGH — 0 anomalies, 0 warnings
```

**AoS groups detected (14):**
Data Analytics (2), Business of IT (2), Scripting and Programming (2), Business Core (1),
Data Management (3), Business Management (1), General Education (15), Network and Security (1),
Full Stack Engineering (1), Web Development (1), Information Technology Management (1),
Software (2), Data Science (8), Computer Science (1)

**Quality checks:**
- All 41 courses have descriptions: ✓
- All 41 courses have competency bullets: ✓
- SP/AoS title reconciliation: clean (0 mismatches)
- Certification prep extraction: operational (cert mentions extracted from descriptions)
- Prerequisite mention extraction: operational

---

## Parser bugs found and fixed during thin-slice

Three bugs were identified and fixed during BSDA parsing:

**Bug 1 — INTRO boilerplate not correctly skipped**
- Cause: INTRO transition used word count `len <= 6` to detect first group heading, but the last boilerplate sentence ("you purchase them.") is 3 words and incorrectly triggered the transition.
- Fix: Added `intro_prose_seen` flag; transition only when `not looks_like_prose(line)` after prose has been seen.

**Bug 2 — SEEKING never transitioned to IN_DESCRIPTION**
- Cause: The SEEKING state buffered all lines into `pending_titles` without checking `looks_like_prose`. Description paragraphs piled up as title candidates; `process_pending_titles` then misidentified them.
- Fix: Added explicit check in SEEKING: if `pending_titles` is non-empty and line `looks_like_prose`, call `process_pending_titles()`, append line to `description_buf`, transition to `IN_DESCRIPTION`.

**Bug 3 — Line discarded in `elif in_bullet` fall-through + description overwritten**
- Cause A: When a bullet ended on a non-continuation line (e.g., group heading "Business of IT"), the `elif in_bullet` branch only emitted the bullet and cleared `in_bullet`, but did NOT call `emit_course()` or set `state = 'SEEKING'`. The line was then processed in the next iteration's IN_COMPETENCIES, losing the group heading entirely — all courses collapsed into the first group.
- Cause B: `emit_course()` unconditionally overwrote `current_course['description']` with `' '.join(description_buf)`, which was `[]` after the competency trigger handler had already flushed and cleared `description_buf`.
- Fix A: Added `emit_course()` and `state = 'SEEKING'` to the `elif in_bullet` non-continuation case; execution then falls through to the SEEKING block for the current line.
- Fix B: Changed `emit_course()` to only write description if `description_buf` is non-empty (preserve already-flushed value).

---

## Known parser gaps / next steps before broader parsing

1. **MEDIUM confidence across 97 guides** — manifest prober warnings are heuristic; full content parser will produce accurate validation. Do not rely on manifest confidence for parse quality; it's a corpus characterization signal only.

2. **Education / MAT guide variants not yet tested** — Student Teaching, Clinical Experiences, Field Experience, Practicum sections are detected in manifest but not parsed by current `parse_guide.py`. These families need their own section handlers.

3. **Endorsement guides** — likely lack Standard Path entirely or have a different structure; manifest shows some as having SP rows, others not.

4. **Nursing PMC guides** — have "Post-Master" sections; current parser will skip gracefully but not extract them.

5. **Graduate guides with track variants** — MACC/A/F/M/T, MSSWE/MSCS track family splits need testing.

6. **`--all` mode** — not tested yet; thin slice was BSDA only. Running `--all` before parser covers more families will produce partial results for most programs. Run `--all` only after at least standard_bs family is fully validated.

7. **Course-code matching** — deferred; title→code resolution is Phase E, not part of structural parsing.

8. **Site integration** — deferred; `parse_guide.py` outputs are not yet wired to any site data path.

---

## Recommended next steps (Phase B continuation)

1. Run `parse_guide.py` on a sample of 3–5 other `standard_bs` programs (BSCS, BSITM, BSHA, BSFIN) and compare output against BSDA — validate the parser generalizes within the family.
2. Inspect `BSFIN` specifically (has `Prerequisites` section variant) to test prerequisite extraction from a dedicated section rather than description inline.
3. Once standard_bs validates, run `--all` for that family only (filter by code prefix) and check manifest rows.
4. Phase C: add section handlers for education variants (Student Teaching / Clinical Experiences).
5. Phase D: graduate guide variants.
