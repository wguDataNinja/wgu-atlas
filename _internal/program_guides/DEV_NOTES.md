# Program Guide Extraction — DEV NOTES

---

## Session 15 (continued) — education_ba Sampled Rollout (2026-03-20)

### Sample results

| Code | Confidence | SP Rows | SP Format | AoS Groups | AoS Courses |
|---|---|---|---|---|---|
| BAELED | HIGH | 37 | 2-col (no Term) | 5 | 37 |
| BAESELED | HIGH | 33 | 3-col (Term) | 3 | 33 |
| BAESMES | HIGH | 35 | 3-col (Term) | 6 | 35 |
| BAESSESB | MEDIUM | 36 | 3-col (Term) | 9 | 37 |
| BAESSESC | HIGH | 36 | 3-col (Term) | 8 | 36 |

**4 HIGH / 1 MEDIUM / 0 LOW. No parser changes.**

### BAESSESB — MEDIUM cause

Source PDF artifact: last SP row (Secondary Disciplinary Literacy, CUs=3, Term=8) split across page boundary in PDF. Term value "8" appears after "Total CUs" line in extracted text — parser correctly breaks at Total CUs and never sees it. Course correctly present in AoS. Identical pattern to BSSWE_C (cs_ug). Not a parser bug.

### Key structural finding: education_ba has two subtypes

| Subtype | Programs | SP Format | AoS notes |
|---|---|---|---|
| Teacher licensure | BAELED | 2-column (no Term) | Clinical Experiences + Student Teaching as group labels |
| Educational Studies | BAESELED, BAESMES, BAESSESB, BAESSESC | 3-column (with Term) | Subject-specific group sets; no clinical sections |

Both subtypes handled by existing parser. No branching needed.

### Parser changes this session

**None.**

### Recommendation

**GO for full education_ba rollout.** All 5 sampled guides parsed correctly. Parser handles both SP formats and all observed AoS group patterns. The 1 MEDIUM case is a source artifact, not a structural issue.

### Artifacts produced

- `data/program_guides/parsed/{BAESELED,BAESMES,BAESSESB,BAESSESC}_parsed.json`
- `data/program_guides/validation/{BAESELED,BAESMES,BAESSESB,BAESSESC}_validation.json`
- `data/program_guides/manifest_rows/{BAESELED,BAESMES,BAESSESB,BAESSESC}_manifest_row.json`
- `data/program_guides/family_validation/education_ba_sample_rollout_summary.{json,md}`

---

## Session 15 — education_ba Gate Test: BAELED (2026-03-20)

### Gate result

BAELED (B.A., Elementary Education) parsed at **HIGH confidence, 0 anomalies, 0 warnings**.

| Metric | Value |
|---|---|
| SP rows | 37 |
| CU sum | 120 |
| SP format | 2-column multiline (no Term) |
| AoS groups | 5 |
| AoS courses | 37 |
| SP/AoS reconciliation | 37/37 — perfect match |
| Empty descriptions | 0 |
| Empty competency bullets | 0 |
| Parser changes | **none** |

### AoS group structure

| Group | Courses |
|---|---|
| Professional Core | 7 |
| General Education | 11 |
| Elementary Education | 15 |
| Clinical Experiences | 2 |
| Student Teaching | 2 |

### Key structural findings

- **Standard Path**: 2-column multiline (Course Description + CUs, no Term column). Already fully supported from BSMES work.
- **Clinical Experiences**: Appears as AoS group label with 2 courses (Early Clinical, Advanced Clinical). Same pattern as BSMES "Student Teaching and Clinical Experiences." No new handler needed.
- **Student Teaching**: Appears as AoS group label with 2 courses (Student Teaching I, Student Teaching II). Same pattern. No new handler needed.
- **No Capstone**: Absent. Handled gracefully.
- **State Licensure Requirements**: Appears in boilerplate preamble before Standard Path. Not a parsed section. No structural impact.
- **Metadata**: Header-line format ("Program Code: BAELED Catalog Version: 202603 Published Date: 12/11/2025"). page_count=0 (no page-break footers). Pre-existing behavior for this metadata type.
- **Total CUs line**: "Total CUs" on its own line, followed by "120" on a separate line. SP_TOTAL_RE breaks at "Total CUs" line — correct.

### Prereq false positive (pre-existing)

1 prereq mention captured for Composition: Successful Self-Expression. The description says there is no prerequisite needed "for this course" — the regex matched the "is a prerequisite for this course" pattern inverted. Pre-existing regex behavior; not a new bug.

### Parser changes this session

**None.**

### education_ba compatibility assessment

**Go.** The current parser handles all observed `education_ba` structural features without changes:
- 2-column SP (no Term) ✓
- Clinical Experiences / Student Teaching as AoS group labels ✓
- No Capstone ✓
- Header-line metadata ✓

### Artifacts produced

- `data/program_guides/parsed/BAELED_parsed.json`
- `data/program_guides/validation/BAELED_validation.json`
- `data/program_guides/manifest_rows/BAELED_manifest_row.json`
- `data/program_guides/family_validation/education_ba_gate_report.json`
- `data/program_guides/family_validation/education_ba_gate_report.md`

### Next recommended steps

Gate passed. Proceed to sampled `education_ba` rollout:
1. Sample 3–4 more guides: BAESELED, BAESMES, BAESSESB, BAESSESC
2. Run them individually; check for any SP or AoS deviations
3. If all sample at HIGH/MEDIUM with no structural surprises, proceed to `education_ba --all`

---

## Session 14 (continued) — cs_ug Full Rollout (2026-03-20)

### Full cs_ug rollout results

All 8 cs_ug guides parsed. No parser bugs found or fixed.

| Confidence | Count | Guides |
|---|---|---|
| HIGH | 4 | BSCS, BSCNE, BSCNEAWS, BSCNEAZR |
| MEDIUM | 4 | BSCNECIS, BSCSIA, BSSWE_C, BSSWE_Java |
| LOW | 0 | — |

All MEDIUM cases are source-data quality issues:
- **BSCNECIS**: double-word typo in SP table ("and and" vs "and") — source guide error
- **BSCSIA**: hyphen variant between SP ("Scripting and Programming Foundations") and AoS ("Scripting and Programming - Foundations")
- **BSSWE_C / BSSWE_Java**: old guide format with no footer metadata; version/pub_date unknown. BSSWE_C has 1 truncated last course with no competency bullets.

### Key structural findings

- All 8 guides use multi-line 3-column SP format — no variant needed
- "Prerequisites" manifest flag on BSCSIA was a false positive (inline description text only)
- Capstone present only in BSCSIA; correctly detected
- Track variants (BSCNE/AWS/AZR/CIS, BSSWE C#/Java) share identical structure; parser handles all tracks without branching
- High cert-prep density: BSCNEAZR=13, BSCNEAWS=11, BSCSIA=10, BSCNECIS=10
- Parser changes this session: **none**

### Artifacts produced

- `data/program_guides/parsed/{CODE}_parsed.json` — 7 new files (BSCNE, BSCNEAWS, BSCNEAZR, BSCNECIS, BSCSIA, BSSWE_C, BSSWE_Java)
- `data/program_guides/validation/{CODE}_validation.json` — 7 new files
- `data/program_guides/manifest_rows/{CODE}_manifest_row.json` — 7 new files
- `data/program_guides/family_validation/cs_ug_rollout_summary.{json,md}`

### Next recommended steps

cs_ug complete. Candidate next families:
1. `education_ba` (11 guides) — needs gate test (BAELED) before rollout; likely new section handlers
2. `graduate_standard` (9 guides) — structurally similar to standard_bs
3. `teaching_mat` (9 guides) — may share structure with education_ba

---

## Session 14 — standard_bs Full Rollout + BSMES Gate (2026-03-20)

### BSMES gate result

BSMES (B.S. Mathematics Education, Secondary) parsed at **HIGH confidence, 0 anomalies, 0 warnings** after one new bug fix.

Key findings:
- Student Teaching and Clinical Experiences appear as **AoS group labels**, not separate parsed sections. Parser handles them correctly.
- Standard Path uses **2-column format** (Course Description + CUs, no Term column). Fixed by `detect_sp_has_term()` + `has_term` parameter in multiline SP parser.
- No new parser branch needed for BSMES within standard_bs.

### Full standard_bs rollout results

All 19 standard_bs guides parsed:

| Confidence | Count | Guides |
|---|---|---|
| HIGH | 16 | BSACC, BSBAHC, BSC, BSDA, BSFIN, BSHA, BSHHS, BSHR, BSHS, BSIT, BSMES, BSMGT, BSMKT, BSPH, BSPSY, BSUXD |
| MEDIUM | 2 | BSHIM, BSSCOM |
| LOW | 1 | BSITM |

- 0 failures (all 19 parsed)
- 0 empty descriptions across all guides
- Cert-prep extraction: 15/19 guides have mentions; prereq: all 19

### 5 additional parser bugs fixed this session

1. `locate_sections()` false Capstone detection — "Capstone" as second line of 2-line SP course title (BSC, BSHIM, BSSCOM) was triggering `CAPSTONE_RE`, cutting off AoS parsing. Fix: discard Capstone entry if it precedes Areas of Study.
2. `_is_bullet_continuation()` missed short sentence completions — `(GAAP).`, `Commercial Code.` not recognized as in-progress bullet continuations. Fix: if pending ends mid-sentence and line ends with `.,:;`, treat as continuation.
3. `_is_bullet_continuation()` lone bullet character — `●` alone on a line left empty pending; next line failed continuation check. Fix: if `len(pending) < 5`, treat as continuation unconditionally.
4. `parse_capstone()` captured page number as title — standalone page number after footer treated as capstone course title. Fix: added `PAGE_NUM_RE` check.
5. SP 2-column format — `detect_sp_has_term()` + `has_term=False` path added to `parse_standard_path_multiline()` for education guides with no Term column.

### Guides requiring custom handling notes

- **BSITM** (LOW): PDF layout artifact in SP table — first 5 courses have missing titles; 4 titles concatenated mid-table. AoS (40 courses) is correct and usable. SP rows require manual review before downstream use.
- **BSHIM** (MEDIUM): 1 PDF fragment `(HIM) environment.` captured as course title. Minor; AoS otherwise correct.
- **BSSCOM** (MEDIUM): Final SP row (2-line capstone course) interrupted by `Total CUs` before Term captured. AoS (35 courses) correct.

### Artifacts produced

All 19 standard_bs guides:
- `data/program_guides/parsed/{CODE}_parsed.json`
- `data/program_guides/validation/{CODE}_validation.json`
- `data/program_guides/manifest_rows/{CODE}_manifest_row.json`
- `data/program_guides/family_validation/standard_bs_rollout_summary.json`
- `data/program_guides/family_validation/standard_bs_rollout_summary.md`

### Next steps

standard_bs family is complete. Recommended next family order:
1. `cs_ug` (8 guides) — BSCS already validated as HIGH; straightforward
2. `education_ba` (11 guides) — education-specific sections need new handlers
3. `graduate_standard` (9 guides) — graduate CU/term expectations differ

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
