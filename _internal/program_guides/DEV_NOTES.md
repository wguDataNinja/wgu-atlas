# Program Guide Extraction — DEV NOTES

---

## Session 27 — Ambiguous-resolution merge + enrichment rerun + documentation consolidation (2026-03-21)

### Summary

Scraping/extraction phase closed. Merged all resolved ambiguous rows into bridge, reran course-enrichment extraction, wrote the human-readable `data/program_guides/README.md`, and updated canonical docs to reflect true post-merge state.

### Core output

- `scripts/program_guides/merge_resolved_ambiguous.py` — new script; merges LLM adjudication results into `bridge/guides_merged/`
- `data/program_guides/bridge/guides_merged/` — 115 final merged per-guide bridge files; no `ambiguous_residual` rows remain
- `data/program_guides/bridge/merge_summary.json` — post-merge coverage summary with explicit medium and unresolvable case records
- `data/program_guides/enrichment/course_enrichment_candidates.json` — updated; 751 courses (was 501 before merge)
- `data/program_guides/enrichment/course_enrichment_summary.json` — updated counts
- `data/program_guides/README.md` — new human entry point for the entire `data/program_guides/` area
- `_internal/program_guides/PROGRAM_GUIDE_PROJECT_STATUS.md` — updated to post-merge state
- `scripts/program_guides/build_course_enrichment_candidates.py` — updated to read from `guides_merged/` and include all resolved anchor classes

### Key decisions

- 163 LLM high-confidence resolutions: applied as `llm_resolved_high`; included in enrichment
- 2 LLM medium-confidence resolutions: applied as `llm_resolved_medium_reviewed`; included with distinct auditable status
  - `BSIT__introduction_to_it__aos` → E004
  - `BSPRN__community_health_and_population_focused_nursing__aos` → C826
- 6 unresolvable cases: all "Health Equity and Social Determinants of Health" (BSHS/BSPH/BSPSY AoS+SP); status `unresolvable`; candidates preserved; excluded from enrichment
- `guides_merged/` is the canonical bridge output; `guides/` and `guides_resolved/` are preserved pipeline stages

### Post-merge enrichment counts

- 751 courses with enrichment data (was 501 before merge — +50% gain)
- 730 with descriptions, 729 with competencies
- 542 rows unmapped (unchanged — titles not in canonical course database)
- 6 unresolvable (excluded from enrichment)

### Anchor class vocabulary (post-merge)

| Class | Count | Included in enrichment |
|-------|-------|----------------------|
| `exact_current_unique` | 2,570 | Yes |
| `exact_observed_variant_unique` | 382 | Yes |
| `deterministic_resolved_multi` | 1,071 | Yes |
| `deterministic_resolved_one_active` | 131 | Yes |
| `deterministic_resolved_degree_title` | 198 | Yes |
| `deterministic_resolved_degree_level` | 4 | Yes |
| `deterministic_resolved_cu_match` | 21 | Yes |
| `deterministic_resolved_a_suffix_cert` | 3 | Yes |
| `llm_resolved_high` | 163 | Yes |
| `llm_resolved_medium_reviewed` | 2 | Yes |
| `unmapped` | 536 | No |
| `unresolvable` | 6 | No |

### Scraping/extraction phase — closed

All work through Phase E (roster bridge, resolution, enrichment extraction) is complete. The phase stops here. Next phase is Phase D artifact generation.

### Next recommended implementation step

**Phase D build-script skeleton:** read `parsed/`, `validation/`, `manifest_rows/` + Phase D policy/schema JSON, apply publish policy, emit schema-valid draft index/per-guide artifacts for verification.

Start from `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md`.

---

## Session 25 — Phase D policy/schema planning pack (2026-03-21)

### Summary

Large planning-only session after corpus close. No parser expansion. No runtime integration. No Phase E matching. Produced implementation-ready Phase D policy/schema/build planning artifacts with conservative publish boundaries.

### Core output

- `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` (single human-readable decision entry point)
- `data/program_guides/audit/phase_d_publish_policy.{md,json}`
- `data/program_guides/audit/phase_d_artifact_schema.{md,json}`
- `data/program_guides/audit/phase_d_degree_course_ownership_matrix.{md,json}`
- `data/program_guides/audit/phase_d_build_plan.{md,json}`

### Key decisions locked

- Phase D v1 publishes guide-derived enrichment to **degree pages only** (program-level payload); no guide-derived course-page fields in Phase D.
- Partial-use handling is explicit and encoded in artifact schema (`disposition`, `sp_status`, `caveat_flags`) rather than dropping guides.
- SP unusable guides (`BSITM`, `MATSPED`, `MSCSUG`) are AoS-only publishes.
- `BSPRN` is SP-partial and must be labeled as Pre-Nursing-only if SP is shown.
- `MEDETID` capstone is publishable with partial flag.
- Parsed prerequisite mentions remain internal-only in v1.

### Next recommended implementation step

Build **schema + build-script skeleton only** (no runtime wiring in same session):
- read parsed/validation/manifest + manifest anchors + phase_d policy/schema JSON
- enforce hard-fail policy/schema checks
- emit draft index/per-guide artifacts for verification

---

## Session 24 — Post-close verification and consolidation (2026-03-21)

### Summary

Verification-and-reconciliation pass completed after Phase C close. No new exploratory parser work. No Phase D build work. Consolidated a durable corpus truth source and tightened claim language to avoid overstatement.

### Reconciled corpus counts (filesystem-derived)

- Artifact coverage: 115/115 parsed + 115/115 validation + 115/115 manifest rows
- Family-validated coverage: 115/115 guides (19 families total)
- Downstream-usable full: 111
- Downstream-usable partial: 4 (`BSITM`, `MATSPED`, `MSCSUG`, `BSPRN`)
- Excluded/not usable: 0
- Confidence: 96 HIGH / 17 MEDIUM / 2 LOW
- AoS course descriptions: 2,593/2,593
- Competency sets: 2,591/2,593
- Standard Path rows extracted: 2,568

### Inconsistencies corrected

- `family_validation/graduate_standard_rollout_summary.{json,md}` had stale confidence totals (8H/1M). Reconciled to 9H/0M based on current validation artifacts.
- `family_validation/teaching_mat_rollout_summary.{json,md}` had stale confidence totals (7H/0M/1L). Reconciled to 8H/1M/0L based on current validation artifacts.
- Enrichment planning artifacts tightened for SP eligibility and exclusions (`BSITM`, `MATSPED`, `MSCSUG`) and for conservative term-availability counts.

### Canonical outputs added

- `data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.{md,json}`
- `data/program_guides/audit/program_guide_adversarial_review.{md,json}`
- `data/program_guides/audit/program_guide_claims_register.{md,json}`
- `_internal/program_guides/PROGRAM_GUIDE_PROJECT_STATUS.md`

### Locked next step

Proceed to **Phase D schema definition + inclusion/exclusion policy only**. Do not start `build_guide_artifacts.py` yet.

---

## Session 23 — Final corpus close: accounting_ma (5) + nursing_ug (2) + nursing_rn_msn (3); 7 targeted parser fixes (2026-03-21)

### Summary

Final corpus-closing session. 8 remaining/deferred guides resolved. 7 targeted parser fixes applied and regression-verified. **115/115 artifact coverage. 115/115 family-validated coverage. 18 complete families.**

**Results:**
- accounting_ma (5 guides): all 5 HIGH — `looks_like_prose` and `_is_bullet_continuation` fixes resolved short-wrapped description line misparse
- nursing_ug (2 guides): BSNU (MEDIUM — no footer metadata), BSPRN (MEDIUM — dual-track structural)
- nursing_rn_msn (3 guides): all 3 HIGH — ACCESSIBILITY_RE typo fix + `no_footer` combined-program fix + "Advanced Standing" silent skip

Unexpected improvements: MACCM (MEDIUM→HIGH), MATSPED (LOW→MEDIUM from stray-integer skip fix).

### Parser fixes — Session 23

**Fix 1: `looks_like_prose()` lowercase-start heuristic**

- **Affected function:** `looks_like_prose()`
- **Problem:** Short wrapped description lines (40–50 chars, no terminal punctuation, uppercase start) were not recognized as prose. Caused `looks_like_prose()` to return False for mid-paragraph continuation lines. MACCA/MACCF/MACCT low-confidence root cause.
- **Fix:** Added `if words[0][0].islower(): return True`. Lines starting with lowercase are always sentence continuations (course titles are always Title Case).
- **Scope:** General.

**Fix 2: `looks_like_prose()` continuation-particle end heuristic**

- **Affected function:** `looks_like_prose()`
- **Problem:** Lines ending with particles like "in", "the", "and", "of" are always mid-sentence line wraps. Were not detected.
- **Fix:** Added continuation particle set check: if `words[-1].lower() in _CONTINUATION: return True`.
- **Scope:** General.

**Fix 3: `looks_like_prose()` prose-verb heuristic**

- **Affected function:** `looks_like_prose()`
- **Problem:** Lines containing standalone prose verbs (is, are, describes, covers, prepares, introduces, etc.) are always description lines (course titles don't use these verb forms mid-line). Not detected for lines < 80 chars without punctuation.
- **Fix:** Added `_PROSE_VERB_RE` regex; if line ≥ 20 chars and matches, return True.
- **Scope:** General.

**Fix 4: `_is_bullet_continuation()` terminal-punctuation override**

- **Affected function:** `_is_bullet_continuation()`
- **Problem:** The Title Case guard (Session 18) checked capitalization rate before checking punctuation. Lines ending with `.?!,:;` could pass the Title Case guard and return False, treating a sentence continuation (e.g. "International Professional Practices Framework (IPPF).") as a new title. Caused MACCA and MACCM misparsing.
- **Fix:** Added `if line[-1] in '.?!,:;': return True` BEFORE the Title Case guard check.
- **Scope:** General. Course titles and group headings never end with terminal punctuation.

**Fix 5: `ACCESSIBILITY_RE` typo tolerance**

- **Affected function:** regex constant; used in `locate_sections()`, `parse_areas_of_study()`, `parse_capstone()`
- **Problem:** `ACCESSIBILITY_RE = re.compile(r'^Accessibility and Accommodations')` required correct spelling. Nursing RN-to-MSN guides use "Accessibility and Accomodations" (single-m typo). Section not detected → AoS parser ran past the section boundary and captured "Accessibility and Accomodations" as the last AoS course group (0 competency bullets), producing 2 warnings per guide.
- **Fix:** `ACCESSIBILITY_RE = re.compile(r'^Accessibility and Accomm?odations')` — matches both spellings.
- **Scope:** General. Existing guides with correct spelling still match.

**Fix 6: `no_footer_lines_found` combined-program suppression**

- **Affected function:** `extract_metadata()`
- **Problem:** Combined-program guides (BSPRN "BSPNTR/BSNPLTR 202303", MSRNN* "MSRNNUUG + MSNUED 202202") have footers that provide version but not program code. `extract_metadata` appended `no_footer_lines_found` anomaly when `codes` was empty, even when `versions` was non-empty.
- **Fix:** When `codes` is empty but `versions` is non-empty, return available metadata (version, pub_date, pages) without the anomaly.
- **Scope:** General. Standard guides always have `codes` non-empty; no behavior change for them.

**Fix 7: `sp_row_invalid` "Advanced Standing" silent skip**

- **Affected function:** `parse_standard_path_multiline()` — both 2-column and EXPECTING_TERM paths
- **Problem:** "Advanced Standing for RN License" (50 CUs, term=0) appears in BSNU and MSRNN* SPs as a block-credit summary placeholder. CU value (50) and term value (0) fail the normal validation ranges, generating `sp_row_invalid` anomaly. Individual courses are listed separately in the SP; this row is redundant.
- **Fix:** Added `elif title and 'Advanced Standing' in title: pass` to silently skip such rows without anomaly.
- **Scope:** General. "Advanced Standing" in course titles is not a known pattern for any regular course in the corpus.

**Regression verification:** 20 guides from all completed families — zero confidence regressions. Improvements only: MACCA/MACCF/MACCT (LOW→HIGH), MACCM (MEDIUM→HIGH), MATSPED (LOW→MEDIUM).

### Rollout details

**accounting_ma (5 guides) — fully rolled out HIGH**

| Code | SP Rows | AoS Groups | AoS Courses | Version | Pages |
|------|---------|------------|-------------|---------|-------|
| MACC | 10 | 4 | 10 | 202409 | 18 |
| MACCM | 10 | 2 | 10 | 202409 | 11 |
| MACCA | 10 | 2 | 10 | 202409 | 11 |
| MACCF | 11 | 2 | 11 | 202409 | 11 |
| MACCT | 10 | 2 | 10 | 202409 | 11 |

All 5 HIGH. 0 anomalies. 0 warnings. `looks_like_prose` fixes resolved all short-wrapped description issues.

**nursing_ug (2 guides) — both MEDIUM**

| Code | SP Rows | AoS Groups | AoS Courses | Version | Confidence |
|------|---------|------------|-------------|---------|------------|
| BSNU | 22 | 2 | 22 | None | MEDIUM (no footer) |
| BSPRN | 19 | 3 | 34 | 202303 | MEDIUM (dual-track) |

BSNU: 1 anomaly (`no_footer_lines_found` — source PDF has no footer), 0 warnings. SP and AoS clean (22/22 reconciled).
BSPRN: 0 anomalies, 1 warning (15 Nursing-track courses AoS-only — structural dual-track design). SP covers Pre-Nursing track only.

**nursing_rn_msn (3 guides) — all HIGH**

| Code | SP Rows | AoS Groups | AoS Courses | Version |
|------|---------|------------|-------------|---------|
| MSRNNUED | 32 | 4 | 32 | 202202 |
| MSRNNULM | 32 | 4 | 32 | 202202 |
| MSRNNUNI | 31 | 4 | 31 | 202202 |

All 3 HIGH. 0 anomalies. 0 warnings. Combined BS+MSN guides with combined-plus footer format.
degree_title truncated (cosmetic) — shows "Bachelor of Science and Post-Baccalaureate Certificate, Nursing +" for all 3.

### Coverage model after Session 23

| Layer | Count | Notes |
|-------|-------|-------|
| **Artifact coverage** | 115 / 115 (100.0%) | +5 from this session (BSNU, BSPRN, MSRNNUED, MSRNNULM, MSRNNUNI) |
| **Family-validated coverage** | 115 / 115 (100.0%) | +9 newly validated (accounting_ma ×5, nursing_ug ×2, nursing_rn_msn ×3) |
| **Downstream-usable full** | ~111 / 115 | accounting_ma now all 5 HIGH; MSRNN* all 3 HIGH; BSNU/BSPRN MEDIUM |
| **Downstream-usable partial** | 4 | BSITM (SP unusable, AoS intact), MATSPED (SP broken, AoS intact), MSCSUG (SP unusable, AoS intact), BSPRN (dual-track SP incomplete) |
| **Not usable** | 0 | All guides have at minimum usable AoS content |

Complete families (18): standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma, endorsement, nursing_msn, nursing_pmc, accounting_ma, nursing_ug, nursing_rn_msn

education_grad: complete (MSEDL=HIGH + MEDETID=MEDIUM)

No partial families remaining.

### Known downstream exclusions (updated)

- BSITM: SP unusable (source PDF column extraction failure), AoS intact and usable
- MATSPED: SP broken (source PDF issue — all courses concatenated into one SP title), AoS intact and usable
- MSCSUG: SP unusable (source PDF column extraction failure), AoS intact and usable
- BSPRN: SP covers Pre-Nursing track only; 15 Nursing-track courses AoS-only
- BSNU: version/pub_date/page_count not recoverable (no footer in source PDF)
- MSRNNUED/LM/NI: degree_title truncated (cosmetic)
- MEDETID: capstone field captures only first of 3 courses (structural multi-capstone limitation)

### Artifacts produced

- `data/program_guides/parsed/{BSNU,BSPRN,MSRNNUED,MSRNNULM,MSRNNUNI}_parsed.json`
- `data/program_guides/validation/{same}_validation.json`
- `data/program_guides/manifest_rows/{same}_manifest_row.json`
- Re-parsed (improved): `{MACCA,MACCF,MACCT,MACCM,MATSPED}_parsed.json` and matching validation/manifest
- `data/program_guides/family_validation/accounting_ma_rollout_summary.{json,md}`
- `data/program_guides/family_validation/nursing_ug_rollout_summary.{json,md}`
- `data/program_guides/family_validation/nursing_rn_msn_rollout_summary.{json,md}`
- `scripts/program_guides/parse_guide.py` (7 targeted fixes)

---

## Session 22 — Bucket 2: nursing_pmc (4) + MEDETID (1); 3 targeted parser fixes (2026-03-21)

### Summary

Work Session 2 of 3 in the "finish the corpus" push. 5 Bucket 2 guides rolled out. 3 targeted parser fixes applied and regression-verified. No broad redesign.

**Results:**
- nursing_pmc: all 4 HIGH, 0 anomalies — SP layout fix resolved the pre-table "Changes to Curriculum" issue
- MEDETID: MEDIUM, 0 anomalies, 1 warning — second-sub-table break resolved the 3-table concatenation; MEDIUM due to 2-of-3 capstone sequence courses unreconciled in AoS

### Gate results

| Family | Gate Guide | Gate Result | Family Confidence | Notes |
|--------|------------|-------------|------------------|-------|
| nursing_pmc | PMCNUED | PASS | 4 HIGH / 0 MEDIUM / 0 LOW | SP fix confirmed effective; all 4 HIGH |
| education_grad | MEDETID | PASS | MEDIUM | 0 anomalies; 1 warning (2 capstone sequence courses in SP not in AoS — structural) |

### Parser fixes — Session 22

**Fix 1: SP_CHANGES_RE conditional break**

- **Affected function:** `parse_standard_path_multiline()` and `parse_standard_path()`
- **Problem:** `if SP_CHANGES_RE.match(line): break` was unconditional. For nursing_pmc guides, "Changes to Curriculum" boilerplate appears between the bare "Standard Path" intro header and the actual "Standard Path for Post-Master's Certificate..." table. The parser broke before ever finding the table, producing SP=0.
- **Fix:** Changed to `break if state != 'BEFORE_TABLE' else continue` (multiline) and `break if in_table else continue` (non-multiline). The break only fires once the table has started.
- **Scope:** General. For all validated guides, "Changes to Curriculum" appears AFTER the table starts — behavior unchanged. Only new behavior: "Changes to Curriculum" before the table is skipped.

**Fix 2: STANDARD_PATH_RE second-table break**

- **Affected function:** `parse_standard_path_multiline()` and `parse_standard_path()`
- **Problem:** MEDETID has 3 embedded SP sub-tables for 2 specializations. After the first table finished, the next sub-table header ("Standard Path for...") was buffered as a course title continuation, producing a corrupted row at the start of each subsequent table.
- **Fix:** Added `if STANDARD_PATH_RE.match(line) and state != 'BEFORE_TABLE': break` immediately before the `if state == 'BEFORE_TABLE':` block. When a second "Standard Path for..." heading appears after leaving BEFORE_TABLE state, stop — first canonical table is complete.
- **Scope:** General. Safe for all validated guides (no "Standard Path for..." heading appears mid-table in any validated guide).

**Fix 3: Certificate Guidebook title skip**

- **Affected function:** `extract_title_and_description()`
- **Problem:** `if i == 0 and line == 'Program Guidebook': continue` only skipped "Program Guidebook". PMC guides begin with "Certificate Guidebook" on line 0 — this was set as the degree_title.
- **Fix:** Changed to `if i == 0 and line in ('Program Guidebook', 'Certificate Guidebook'): continue`.
- **Scope:** General. Only affects guides with "Certificate Guidebook" on line 0 (the 4 PMC guides in this corpus).

**Regression verification:** 19 guides tested from across all completed families (BSCS, MATELED, MAMES, MSHRM, MBA, MSCSIA, MSSWEAIE, MSDADE, MHA, BSSESB, MACC, ENDECE, MSNUED, MSEDL, BSCSIA, BSHHS, MBAITM, BSDA, MACCM). All maintained identical confidence and anomaly counts. BSCSIA and MACCM both maintained MEDIUM with the same warning strings.

### Rollout details

**nursing_pmc (4 guides) — fully rolled out**

| Code | SP Rows | AoS Groups | AoS Courses | Version | Pages |
|------|---------|------------|-------------|---------|-------|
| PMCNUED | 8 | 2 | 8 | 202110 | 10 |
| PMCNUFNP | 10 | 2 | 10 | 202306 | 12 |
| PMCNULM | 8 | 2 | 8 | 202110 | 11 |
| PMCNUPMHNP | 11 | 2 | 11 | 202306 | 13 |

Notes:
- All 4 HIGH, 0 anomalies. Source SP data was correct all along — parser was just stopping too early.
- "(Post-MSN)" vs "(PostMSN)" in degree titles: source text variant, not a parser issue.
- Phase A "Post-Master section" flag: content is ordinary AoS courses, not a separate structural section.

**MEDETID — rolled out as MEDIUM**

- SP: 12 rows (first canonical table — K-12 and Adult Learner Specializations, combined path)
- AoS: 4 groups (Foundations of Learning Design 4c, K-12 Specialty 2c, Adult Learner Specialty 2c, Design Lab 1c) = 9 courses
- Capstone: first course of 3-course sequence ("Identifying Learner Needs and a Research Problem") — 13 bullets
- Warning: "Developing an E-Learning Solution and Research Methodology" and "Implementing and Evaluating E-Learning Solutions" are in SP rows (term 3-4) but not resolved in AoS output (they're the 2nd and 3rd capstone courses; only the first is captured by parse_capstone). This is a structural limitation of multi-course capstones, not a data loss.
- Downstream usable with caveat: SP and AoS content are clean and trustworthy. Capstone field only captures first course.

### Coverage model after Session 22

| Layer | Count | Notes |
|-------|-------|-------|
| **Artifact coverage** | 110 / 115 (95.7%) | +5 from this session |
| **Family-validated coverage** | 106 / 115 (92.2%) | nursing_pmc (4) + MEDETID (1) = +5 newly validated |
| **Downstream-usable full** | ~103 / 115 | +5 from this session (MEDETID counted as partial-full: AoS clean, capstone partial) |
| **Downstream-usable partial** | 3 | BSITM, MATSPED, MSCSUG (unchanged) |
| **Not usable** | 3 | MACCA, MACCF, MACCT (unchanged) |

Complete families (15): standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma, endorsement, nursing_msn, nursing_pmc

Full completions (both guides done): education_grad (MSEDL=HIGH + MEDETID=MEDIUM)

Partial families:
- accounting_ma: MACC (HIGH) + MACCM (MEDIUM) usable; MACCA, MACCF, MACCT (LOW) deferred

### Remaining after Session 22

5 guides not yet in artifact coverage:
- nursing_ug: BSNU (4-column SP, AoS intact), BSPRN (dual-track, MEDIUM, noisy SP)
- nursing_rn_msn: MSRNNUED, MSRNNULM, MSRNNUNI (LOW structural complexity — running headers, non-course SP blocks, multi-component guide)

### Artifacts produced

- `data/program_guides/parsed/{PMCNUED,PMCNUFNP,PMCNULM,PMCNUPMHNP,MEDETID}_parsed.json`
- `data/program_guides/validation/{same}_validation.json`
- `data/program_guides/manifest_rows/{same}_manifest_row.json`
- `data/program_guides/family_validation/nursing_pmc_gate_report.{json,md}`
- `data/program_guides/family_validation/nursing_pmc_rollout_summary.{json,md}`
- `data/program_guides/family_validation/education_grad_rollout_summary.{json,md}` (updated — MEDETID now complete)
- `data/program_guides/family_validation/education_grad_gate_report.{json,md}` (updated — MEDETID result added)
- `scripts/program_guides/parse_guide.py` (3 targeted fixes)

---

## Session 21 — Bucket 1 rollout: endorsement (8) + nursing_msn (5) + MSEDL (1) (2026-03-21)

### Summary

Work Session 1 of 3 in the "finish the corpus" push. All 14 Bucket 1 guides rolled out. No parser changes required or made. All 14 parsed HIGH with 0 anomalies, 0 warnings, 0 empty descriptions, 0 empty competency lists.

### Gate results

| Family | Gate Guide | Gate Result | Family Confidence | Notes |
|--------|------------|-------------|------------------|-------|
| endorsement | ENDECE | PASS | 8 HIGH / 0 MEDIUM / 0 LOW | pages=0 cosmetic across all 8 (header-line metadata format) |
| nursing_msn | MSNUED | PASS | 5 HIGH / 0 MEDIUM / 0 LOW | Cleanest nursing family |
| education_grad | MSEDL | PARTIAL PASS | 1 HIGH / 0 MEDIUM / 0 LOW | MEDETID deferred — Bucket 2 |

### Rollout details

**endorsement (8 guides) — fully rolled out**

| Code | SP Rows | AoS Groups | AoS Courses | SP Format | Version |
|------|---------|------------|-------------|-----------|---------|
| ENDECE | 6 | 3 | 6 | 2-col (no Term) | 202509 |
| ENDELL | 8 | 1 | 8 | 3-col (with Term) | 201112 |
| ENDMEMG | 2 | 1 | 2 | 2-col (no Term) | 202509 |
| ENDSEMG | 2 | 1 | 2 | 2-col (no Term) | 202509 |
| ENDSESB | 9 | 2 | 9 | 2-col (no Term) | 202509 |
| ENDSESC | 7 | 3 | 7 | 2-col (no Term) | 202509 |
| ENDSESE | 9 | 4 | 9 | 2-col (no Term) | 202509 |
| ENDSESP | 7 | 3 | 7 | 2-col (no Term) | 202509 |

Notes:
- 7 of 8 use 2-column SP (no Term); ENDELL (oldest, 201112) uses 3-column. Both formats handled correctly.
- All 8 have pages=0 — endorsement guides use header-line metadata (line 3: "Program Code: ENDECE Catalog Version: ... Published Date: ..."), not footer lines. page_count is not recoverable from this format. Cosmetic.
- ENDMEMG and ENDSEMG are the smallest guides in the corpus (295 lines, 2 SP rows each).
- Phase A manifest "HIGH UNCERTAINTY" flag was unfounded. Clinical Experiences and Field Experience sections are ordinary AoS groups.

**nursing_msn (5 guides) — fully rolled out**

| Code | SP Rows | AoS Groups | AoS Courses | Version |
|------|---------|------------|-------------|---------|
| MSNUED | 15 | 2 | 15 | 202003 |
| MSNUFNP | 16 | 3 | 16 | 202003 |
| MSNULM | 15 | 2 | 15 | 202011 |
| MSNUNI | 14 | 2 | 14 | 202003 |
| MSNUPMHNP | 17 | 3 | 17 | 202203 |

Notes:
- All 5 use 3-column SP format. Page counts valid (13–15). No anomalies.
- FNP and PMHNP have 3 AoS groups (adding "Nurse Practitioner Core" to MSN Core + Specialty).
- Clinical/preceptor sections are ordinary named courses within AoS groups — no structural concern.
- Phase A manifest MEDIUM classification and clinical concern flag were unfounded.

**education_grad (MSEDL only — 1 guide) — partially rolled out**

| Code | SP Rows | AoS Groups | AoS Courses | Version |
|------|---------|------------|-------------|---------|
| MSEDL | 13 | 3 | 13 | 202404 |

Notes:
- MSEDL: HIGH, clean, no issues. Phase A "Practicum section" flag unfounded — Practicum is an ordinary AoS course.
- MEDETID: deferred to Bucket 2. Has 3 embedded SP sub-tables (combined + K-12 + Adult Learner specializations). Parser concatenates all 3, producing 32 SP rows with duplicates and sub-table headers as course entries. AoS is intact (4 groups, 9 courses). Requires a targeted SP fix to select one canonical path or deduplicate.

### Parser changes this session

None.

### Coverage model after Session 21

| Layer | Count | Notes |
|-------|-------|-------|
| **Artifact coverage** | 105 / 115 (91.3%) | 14 new guides added |
| **Family-validated coverage** | 101 / 115 (87.8%) | endorsement (8) + nursing_msn (5) + MSEDL (1) = 14 newly validated |
| **Downstream-usable full** | ~98 / 115 | +14 from this session |
| **Downstream-usable partial** | 3 | BSITM, MATSPED, MSCSUG (unchanged) |
| **Not usable** | 3 | MACCA, MACCF, MACCT (unchanged) |

Complete families (14): standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma, endorsement, nursing_msn

Partial families:
- accounting_ma: MACC (HIGH) + MACCM (MEDIUM) usable; MACCA, MACCF, MACCT (LOW) deferred — looks_like_prose limitation
- education_grad: MSEDL (HIGH) done; MEDETID deferred — Bucket 2

### Artifacts produced

- `data/program_guides/parsed/{ENDECE,ENDELL,ENDMEMG,ENDSEMG,ENDSESB,ENDSESC,ENDSESE,ENDSESP,MSNUED,MSNUFNP,MSNULM,MSNUNI,MSNUPMHNP,MSEDL}_parsed.json`
- `data/program_guides/validation/{same}_validation.json`
- `data/program_guides/manifest_rows/{same}_manifest_row.json`
- `data/program_guides/family_validation/endorsement_gate_report.{json,md}`
- `data/program_guides/family_validation/endorsement_rollout_summary.{json,md}`
- `data/program_guides/family_validation/nursing_msn_gate_report.{json,md}`
- `data/program_guides/family_validation/nursing_msn_rollout_summary.{json,md}`
- `data/program_guides/family_validation/education_grad_gate_report.{json,md}`
- `data/program_guides/family_validation/education_grad_rollout_summary.{json,md}`

### Remaining after Session 21

10 guides not yet in artifact coverage:
- nursing_pmc: PMCNUED, PMCNUFNP, PMCNULM, PMCNUPMHNP (4) — Bucket 2
- education_grad/MEDETID (1) — Bucket 2
- nursing_ug: BSNU, BSPRN (2) — Bucket 3
- nursing_rn_msn: MSRNNUED, MSRNNULM, MSRNNUNI (3) — Bucket 3

### Bucket 2 still the right next session

Yes. Bucket 2 (nursing_pmc SP layout fix + MEDETID multi-path SP fix) remains the correct next move. Both are contained anomaly work with intact AoS — targeted parser fixes, not architectural changes.

---

## Session 19 — education_ma gate + rollout; coverage accounting clarification (2026-03-21)

### Coverage accounting model (new — established this session)

Three distinct coverage counts must be tracked separately. Do not collapse them.

| Layer | Definition | Count after Session 19 |
|-------|-----------|------------------------|
| **Artifact coverage** | Guides with parsed + validation + manifest_row JSON artifacts on disk | 89 / 115 (77.4%) |
| **Family-validated coverage** | Guides in families that cleared a rollout review (rollout summary exists); partial families count only validated portion | 87 / 115 (75.7%) |
| **Downstream-usable full** | Family-validated guides at HIGH or MEDIUM confidence with both SP and AoS intact | ~84 / 115 |
| **Downstream-usable partial** | Family-validated guides at LOW confidence where AoS is intact but SP is unusable | 3 (BSITM, MATSPED, MSCSUG) |
| **Not usable** | Parsed guides with broken AoS (deferred LOW) | 3 (MACCA, MACCF, MACCT) |

Rules:
- LOW confidence does not automatically mean "not usable" — distinguish SP-only failure (AoS intact, partial use) from AoS failure (not usable).
- Family-validated requires a rollout summary file, not just a gate report. (Note: healthcare_grad has a gate report but no rollout summary file; it is counted as family-validated based on ATLAS_CONTROL status.)
- Artifact coverage includes all guides with parsed artifacts, including deferred-LOW guides and families not yet through rollout.
- Do not cite artifact coverage as validation coverage. They are not the same number.

**Discrepancy note:** ATLAS_CONTROL and previous DEV_NOTES stated "80 / 115" as of Session 18. The actual artifact count was 82 (19+8+11+9+3+2+4+9+5+4+3+5 = 82). The stated count of 80 was off by 2. The discrepancy has not been traced to a specific cause. The filesystem count is authoritative; all 82 pre-existing guides are valid artifacts from the same pipeline.

---

### Gate results

| Family | Gate Guide | Gate Result | Family Confidence | Notes |
|--------|------------|-------------|------------------|-------|
| education_ma | MAMES | PASS | 9 HIGH / 0 MEDIUM / 0 LOW | Cleanest family to date |

### Rollout status

- **education_ma**: fully rolled out. 9 guides. All HIGH. 0 anomalies, 0 warnings, 0 empty descriptions/bullets across all 9. No exclusions.

### Parser change this session — capstone KeyError fix

**Bug:** `parse_capstone()` built a capstone dict without `prerequisite_mentions` or `certification_prep_mentions` keys. `_scan_description_mentions()` accessed `course['prerequisite_mentions']` directly (not via `.get()`), raising KeyError when the capstone description matched a prereq pattern. MAMEK6 triggered the crash; other guides with capsones (MBA, MHA, BSCSIA, etc.) did not crash because their capstone descriptions did not contain prereq-matching text.

**Fix:** Added `'prerequisite_mentions': []` and `'certification_prep_mentions': []` to the capstone dict in `parse_capstone()` before the `_scan_description_mentions()` call.

**Scope:** General — affects all guides with capstone sections.

**Regression verification:** 23 guides tested including all previously committed capstone guides (BSBAHC, BSDA, BSHHS, BSMGT, MBAHA, MBAITM, MSCSIA, MSITM, MSML, MBA, MHA, BSCSIA). All capstone guides re-parsed and confirmed identical confidence/anomaly counts. All 9 previously-committed capstone guides that lacked the fix were re-parsed to apply it consistently.

### Corpus status after Session 19

**89 / 115 guides with parsed artifacts (77.4%).** 12 complete families. 87 family-validated.

Complete families:
- standard_bs (19), cs_ug (8), education_ba (11), graduate_standard (9), mba (3), healthcare_grad (2), education_bs (4), teaching_mat (9), cs_grad (5), swe_grad (4), data_analytics_grad (3), education_ma (9)

Partially validated:
- accounting_ma: 5 guides parsed. MACC (HIGH) + MACCM (MEDIUM) usable. MACCA, MACCF, MACCT (LOW) deferred — looks_like_prose limitation.

### Accounting_ma reassessment (deferred — no fix implemented)

The specialization-guide failure (MACCA, MACCF, MACCT) is isolated to `looks_like_prose()`. The 202409 guides use a narrower PDF column layout producing 40–50 char description lines with no terminal punctuation. The current function requires >80 chars OR terminal punctuation.

**Minimal safe fix strategy (proposed, not implemented):**
- Extend `looks_like_prose()` with a verb-presence heuristic for short lines (30–65 chars): if the line contains " is ", " are ", " provides ", " covers ", " teaches ", " examines ", " focuses ", " explores ", " introduces ", " develops " as standalone word sequences, classify as prose regardless of length or terminal punctuation.
- This targets the failure pattern: "Internal Auditing II is a continuation of", "Corporate Financial Analysis teaches the", etc.
- Group headings ("Accounting", "Mathematics Content", "Teacher Performance Assessment") typically do not contain these verb patterns.

**Regression risks:**
- Any short heading that happens to contain a listed verb could be misclassified as prose: "What Business Analytics Covers" (hypothetical). Risk is low but must be verified.
- Need to test all 80+ currently validated guides without confidence regressions.
- Need to confirm the fix resolves MACCA (1 course), MACCF (2 courses), MACCT (2 courses).

**Decision:** accounting_ma specialization guides remain deferred. A dedicated parser-fix session is required before any attempt at rollout.

### Confidence distribution this session (9 new guides)

- HIGH: MAMES, MAELLP12, MAMEK6, MAMEMG, MASEMG, MASESB, MASESC, MASESE, MASESP = 9 HIGH

### Artifacts produced

- `data/program_guides/parsed/{MAMES,MAELLP12,MAMEK6,MAMEMG,MASEMG,MASESB,MASESC,MASESE,MASESP}_parsed.json`
- `data/program_guides/validation/{same}_validation.json`
- `data/program_guides/manifest_rows/{same}_manifest_row.json`
- `data/program_guides/family_validation/education_ma_gate_report.{json,md}`
- `data/program_guides/family_validation/education_ma_rollout_summary.{json,md}`

Capstone re-parses (content-consistent updates to existing committed files):
- `data/program_guides/parsed/{BSBAHC,BSDA,BSHHS,BSMGT,MBAHA,MBAITM,MSCSIA,MSITM,MSML,MBA,MHA,BSCSIA}_parsed.json`

---

## Session 18 — cs_grad / swe_grad / data_analytics_grad / accounting_ma (2026-03-21)

### Gate results

| Family | Gate Guide | Gate Result | Family Confidence | Notes |
|--------|------------|-------------|------------------|-------|
| cs_grad | MSCSIA | PASS | 4 HIGH / 0 MEDIUM / 1 LOW | MSCSUG LOW = SP column extraction failure (source artifact, same class as BSITM/MATSPED) |
| swe_grad | MSSWEAIE | PASS (after fix) | 3 HIGH / 1 MEDIUM / 0 LOW | Parser fix required (see below); MSSWEUG MEDIUM = title hyphen variant in bridge guide |
| data_analytics_grad | MSDADE | PASS | 3 HIGH / 0 MEDIUM / 0 LOW | Cleanest family this session |
| accounting_ma | MACC | PARTIAL PASS | 1 HIGH / 1 MEDIUM / 3 LOW | Specialization guides (202409) have systematic looks_like_prose failure; deferred |

### Rollout status

- **cs_grad**: fully rolled out. 5 guides. MSCSUG SP excluded (source artifact); AoS usable.
- **swe_grad**: fully rolled out. 4 guides. Parser fix required and verified.
- **data_analytics_grad**: fully rolled out. 3 guides. All HIGH, no exclusions.
- **accounting_ma**: NOT fully rolled out. MACC (HIGH) is safe. MACCM (MEDIUM, 1 title quality issue) is parseable. MACCA/MACCF/MACCT (LOW) deferred — parser limitation. 5 guides parsed, family not complete.

### Parser change this session — `_is_bullet_continuation` Title Case guard

**Bug:** `_is_bullet_continuation()` was treating Title Case course titles (≥80% capitalized words, >30 chars) as bullet continuations when the preceding bullet lacked terminal punctuation. All 3 pure swe_grad guides had "Software Quality Assurance and Deployment" silently lost from AoS because "The learner justifies the software architecture used in a software system" (no period) triggered the continuation path for the next line.

**Fix:** Added a Title Case ratio check before the `len(line) > 30` continuation branch. If ≥80% of a line's words start uppercase, the function returns False (not a continuation).

**Scope:** General — applies to all guides, not swe_grad-specific.

**Regression verification:** BSCS, BSCSIA, MBA, MHA, MATELED, BSSESB, BSACC, MSCIN — all returned identical confidence and anomaly counts after fix.

### Known parser limitation — `looks_like_prose` (accounting_ma, not fixed)

The `looks_like_prose()` function requires lines to be >80 chars OR end with terminal punctuation. The 202409 accounting specialization guides (MACCA, MACCF, MACCT) use a narrower PDF column layout, producing description lines of 40–50 chars without terminal punctuation. These are not recognized as prose, causing description text to be buffered as pending_titles. The result: specialization-specific courses become group names; description fragments become course titles; affected courses have empty descriptions and 0 bullets.

This is a parser limitation (not PDF extraction corruption). SP data for all accounting guides is clean. No fix was attempted this session — a robust `looks_like_prose` extension requires careful evaluation and regression testing.

### Corpus status after Session 18

**80 / 115 guides parsed (69.6%).** 11 families complete or partially validated.

Complete families:
- standard_bs (19), cs_ug (8), education_ba (11), graduate_standard (9), mba (3), healthcare_grad (2), education_bs (4), teaching_mat (9), cs_grad (5), swe_grad (4), data_analytics_grad (3)

Partially validated (not complete):
- accounting_ma: 5 guides parsed, 3 LOW — specialization guides deferred

**Phase D threshold: 81 guides (≥70%).** We are at 80 — **1 guide short** of the numeric threshold.

Note: the remaining 35 unprocessed guides are concentrated in high-risk or unvalidated families (endorsement, nursing, education_grad, education_ma). Crossing the numeric threshold alone is insufficient for Phase D reassessment — risky family coverage and safe-field boundaries must also be understood.

### Confidence distribution this session (17 new guides)

- HIGH: MSCSIA, MSCSCS, MSCSAIML, MSCSHCI, MSSWEAIE, MSSWEDDD, MSSWEDOE, MSDADE, MSDADS, MSDADPE, MACC = 11 HIGH
- MEDIUM: MSSWEUG, MACCM = 2 MEDIUM
- LOW: MSCSUG (source artifact), MACCA, MACCF, MACCT (parser limitation) = 4 LOW

### Artifacts produced

- `data/program_guides/parsed/{MSCSIA,MSCSCS,MSCSAIML,MSCSHCI,MSCSUG,MSSWEAIE,MSSWEDDD,MSSWEDOE,MSSWEUG,MSDADE,MSDADS,MSDADPE,MACC,MACCA,MACCF,MACCM,MACCT}_parsed.json`
- `data/program_guides/validation/{same}_validation.json`
- `data/program_guides/manifest_rows/{same}_manifest_row.json`
- `data/program_guides/family_validation/cs_grad_gate_report.{json,md}`
- `data/program_guides/family_validation/cs_grad_rollout_summary.{json,md}`
- `data/program_guides/family_validation/swe_grad_gate_report.{json,md}`
- `data/program_guides/family_validation/swe_grad_rollout_summary.{json,md}`
- `data/program_guides/family_validation/data_analytics_grad_gate_report.{json,md}`
- `data/program_guides/family_validation/data_analytics_grad_rollout_summary.{json,md}`
- `data/program_guides/family_validation/accounting_ma_gate_report.{json,md}`

---

## Audit Summary — 2026-03-21

### Production-leaning (38 guides across 3 families)

The following fields are internally production-quality for the 38 parsed guides:
- **Course descriptions:** 0 empty across all 38 guides. Strongest field in the pipeline.
- **Competency bullets:** Near-zero empty (2 known PDF artifact cases only).
- **Cert-prep mentions:** Reliable inline extraction; highest value in cs_ug.
- **Standard Path course list + CU values:** Reliable for 37/38 (BSITM excluded).
- **AoS group structure:** Validated across all 38 guides.

The parser's core state machine, section anchor detection, SP format detection (2-col / 3-col / multiline), and metadata extraction (footer + header-line) are all cross-validated and stable.

### Still provisional

- **57% of corpus (65 guides / 13 families) has no content parse** (as of session 16; 50/115 parsed). Do not extrapolate parsed-family results to untouched families.
- **4 Sped education_ba guides** have 1 missing AoS course each (PDF reordering artifact; parser fix deferred). Flag for downstream users.
- **BSITM SP data is LOW confidence** (PDF column extraction failure). AoS for BSITM is correct and usable.
- **Prereq mention extraction** has a known false-positive regex pattern. Use as flag only; do not display raw text.
- **Endorsement, nursing families, and guides with Field Experience / Practicum / Post-Master sections** are entirely unvalidated. Parser is not known to handle these correctly.
- **Phase D (site artifact build)** and **Phase E (course-code matching)** are not started. Internal artifacts are not wired to the site.

### What should happen before integration

1. Continue family rollouts — target ≥70 guides (60–70% corpus) before beginning Phase D.
2. Gate test **graduate_standard** (MBA first — all manifest HIGH, lowest risk). Proceed to full 9-guide rollout if gate passes.
3. Gate test **mba** family (3 guides, all manifest HIGH).
4. Gate test **healthcare_grad** (MHA or MPH).
5. After those (~52 guides, 45%), reassess. Continue with teaching_mat and education_bs (validated patterns from education_ba).
6. Defer endorsement and nursing families until independent gate tests confirm structure.
7. Design Phase D build script when ≥70 guides are parsed.
8. Do not start site integration before Phase D is designed and ≥70% coverage is reached.

### Audit artifacts

Full audit produced in `data/program_guides/audit/`:
- `program_guide_family_inventory.{json,md}` — all 19 families, rollout status, key structural facts
- `program_guide_section_matrix.{csv,md}` — section/component analysis across corpus
- `program_guide_readiness_assessment.{json,md}` — conservative readiness review, concrete next steps
- `program_guide_atlas_enrichment_recommendations.md` — per-section enrichment priority and risk

---

## Session 17 — teaching_mat Full Rollout + education_bs Full Rollout (2026-03-21)

### education_bs full rollout

4/4 guides parsed. **4 HIGH / 0 MEDIUM / 0 LOW.** No parser changes.

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses |
|------|--------|------------|---------|------------|-------------|
| BSSESB | B.S., Science Education (Secondary Biological Science) | HIGH | 41 | 11 | 41 |
| BSSESC | B.S., Science Education (Secondary Chemistry) | HIGH | 40 | 10 | 40 |
| BSSESE | B.S., Science Education (Secondary Earth Science) | HIGH | 41 | 11 | 41 |
| BSSESP | B.S., Science Education (Secondary Physics) | HIGH | 40 | 10 | 40 |

0 empty descriptions, 0 empty competency lists. All 4 guides: perfect reconciliation.

All 4 use 2-col SP (no Term) and header-line metadata. All share: Professional Core (7), General Science Content (8), Clinical Experiences (2), Student Teaching (2). Subject-specific content group name varies (Biology Content, Chemistry Content, etc.) — handled without branching. All version 202603; family was published as a cohort December 2025.

### teaching_mat full rollout

9/9 guides parsed. **7 HIGH / 0 MEDIUM / 1 LOW.** No parser changes.

| Code | Degree | Confidence | SP Format | SP Rows | AoS Courses |
|------|--------|------------|-----------|---------|-------------|
| MATELED | M.A.T., Elementary Education | HIGH | 3-col (with Term) | 28 | 28 |
| MATEES | M.A.T., English Education (Secondary) | HIGH | 2-col (no Term) | 20 | 20 |
| MATMES | M.A.T., Mathematics Education (Secondary) | HIGH | 2-col (no Term) | 21 | 21 |
| MATSESB | M.A.T., Science Education (Secondary Biology) | HIGH | 2-col (no Term) | 20 | 20 |
| MATSESC | M.A.T., Science Education (Secondary Chemistry) | HIGH | 2-col (no Term) | 20 | 20 |
| MATSESE | M.A.T., Science Education (Secondary Earth Science) | HIGH | 2-col (no Term) | 20 | 20 |
| MATSESP | M.A.T., Science Education (Secondary Physics) | HIGH | 2-col (no Term) | 20 | 20 |
| MATSPED | M.A.T., Special Education | **LOW** | 3-col (extraction failure) | 9/30 | 30 |
| MATSSES | M.A.T., Social Studies Education (Secondary) | HIGH | 2-col (no Term) | 19 | 19 |

0 empty descriptions, 0 empty competency lists across all 9.

**SP format split:** MATELED and MATSPED use 3-col (with Term); all 7 secondary guides use 2-col (no Term). Both formats pre-validated; no branching needed. The gate guide (MATELED) happens to be the only 3-col guide among the 8 parseable guides in the family.

### LOW case — MATSPED (PDF column extraction failure)

Same failure class as BSITM. `pdftotext` extracted course titles and CU/Term values in column order rather than row order. First 3 titles appear in correct interleaved positions; remaining 27 appear in a contiguous block at end of SP section, separated from CU/Term values. Parser recovered 9/30 SP rows.

**Impact:** MATSPED SP data unusable (21 anomalies). AoS (30 courses, all descriptions, all competencies) fully intact.

**Parser change:** None. Source-PDF artifact. Fixing requires PDF re-extraction or post-hoc batch-title matcher — both deferred. Same disposition as BSITM.

### Corpus status after education_bs + teaching_mat

63 / 115 guides parsed (54.8%). 8 families complete: standard_bs(19), cs_ug(8), education_ba(11), graduate_standard(9), mba(3), healthcare_grad(2), education_bs(4), teaching_mat(9).

Phase D threshold (≥70%) requires 81 guides — **18 guides short**.

### Parser changes this session

**None** (gate-test © line fix was committed separately in prior step).

### Artifacts produced

- `data/program_guides/parsed/{BSSESC,BSSESE,BSSESP,MATEES,MATMES,MATSESB,MATSESC,MATSESE,MATSESP,MATSPED,MATSSES}_parsed.json`
- `data/program_guides/validation/{same}_validation.json`
- `data/program_guides/manifest_rows/{same}_manifest_row.json`
- `data/program_guides/family_validation/education_bs_rollout_summary.{json,md}`
- `data/program_guides/family_validation/teaching_mat_rollout_summary.{json,md}`

---

## Session 17 — teaching_mat Gate Test (MATELED) + education_bs Gate Test (BSSESB) (2026-03-21)

### Gate results

| Code | Family | Degree | Confidence | SP Format | SP Rows | AoS Groups | AoS Courses | Capstone |
|------|--------|--------|------------|-----------|---------|------------|-------------|---------|
| MATELED | teaching_mat | M.A.T., Elementary Education | HIGH | 3-col multiline (with Term) | 28 | 5 | 28 | — |
| BSSESB | education_bs | B.S., Science Education (Secondary Biological Science) | HIGH | 2-col multiline (no Term) | 41 | 11 | 41 | — |

Both gates: 0 anomalies, 0 warnings, perfect reconciliation.

### Structural findings

**MATELED (teaching_mat):**
- 3-column SP (with Term) — teaching_mat is a graduate family (M.A.T.). Same format as graduate_standard/mba, unlike education_ba teacher-licensure guides (2-col).
- Clinical Experiences (3 courses) + Student Teaching (2 courses) as AoS group labels — same pattern as education_ba. No new handler.
- Split-footer metadata format. 28 courses across 5 groups.

**BSSESB (education_bs):**
- 2-column SP (no Term) — education_bs is undergraduate. Same format as education_ba teacher-licensure guides (BAELED, BASPEE, BASPMM). No new handler.
- 11 AoS groups (largest in any education family to date). Parser handled cleanly.
- Header-line metadata. 41 courses.
- Subject-specific content groups ("Biology Content", "General Science Content") — different names but identical structural pattern.

### Parser bug fixed — `extract_metadata()` © line date extraction

**Bug:** MATELED's last footer © line (`line 1037`) had no space before the date: `"...University8/16/24"`. The old handler used `parts[-1]` (whitespace split), producing `"University8/16/24"`. Source PDF formatting artifact.

**Fix:** Replaced `parts[-1]` check with `re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', line)` — extracts date pattern directly regardless of surrounding whitespace. No behavioral change when space is present.

**Regression verified:** BSDA, BSMGT, BSCSIA, MBA, MBAITM, BSCS, BSPSY — all unchanged after fix.

**Scope:** General fix — benefits any guide with this PDF artifact; not family-specific.

### Rollout recommendation

Both families gate-passed cleanly. Recommend:
1. **education_bs first** — 4-guide family, very low risk, all patterns pre-validated, fast to complete.
2. **teaching_mat second** — 9 guides, slightly larger, watch for SP format consistency across non-Elementary subject variants.

### Artifacts produced

- `data/program_guides/parsed/{MATELED,BSSESB}_parsed.json`
- `data/program_guides/validation/{MATELED,BSSESB}_validation.json`
- `data/program_guides/manifest_rows/{MATELED,BSSESB}_manifest_row.json`
- `data/program_guides/family_validation/teaching_mat_gate_report.{json,md}`
- `data/program_guides/family_validation/education_bs_gate_report.{json,md}`

---

## Session 16 — healthcare_grad Gate Test / Full Rollout (2026-03-21)

### Gate result

Both guides parsed (family size = 2; gate covers full family). **2/2 HIGH, 0 MEDIUM, 0 LOW.**

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone |
|------|--------|------------|---------|------------|-------------|---------|
| MHA | Master of Healthcare Administration | HIGH | 10 | 1 | 9 | ✓ (3 bullets) |
| MPH | Master of Public Health | HIGH | 12 | 1 | 12 | — (embedded in AoS) |

0 empty descriptions, 0 empty competency lists. Both guides: perfect reconciliation.

### Structural notes

- Both guides use 3-column multiline SP format — consistent with graduate_standard and mba.
- Both use header-line metadata format.
- Single AoS group per guide (unusual but valid for tightly focused graduate programs).
- MHA has explicit Capstone section. MPH capstone is embedded in AoS; capstone_present=false is correct.

### Parser changes

**None.**

### Artifacts produced

- `data/program_guides/parsed/{MHA,MPH}_parsed.json`
- `data/program_guides/validation/{MHA,MPH}_validation.json`
- `data/program_guides/manifest_rows/{MHA,MPH}_manifest_row.json`
- `data/program_guides/family_validation/healthcare_grad_gate_report.{json,md}`

### Corpus status after healthcare_grad

50 / 115 guides parsed (43.5%). 6 families complete (standard_bs=19, cs_ug=8, education_ba=11, graduate_standard=9, mba=3, healthcare_grad=2). Phase D threshold (≥70%) requires 81 guides — 31 guides short.

---

## Session 16 — mba Full Rollout (2026-03-21)

### Results

3/3 guides parsed. **3 HIGH / 0 MEDIUM / 0 LOW.**

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone |
|------|--------|------------|---------|------------|-------------|---------|
| MBA | M.B.A. | HIGH | 11 | 7 | 10 | ✓ (2 bullets) |
| MBAHA | M.B.A., Healthcare Administration | HIGH | 11 | 8 | 10 | ✓ (2 bullets) |
| MBAITM | M.B.A., IT Management | HIGH | 11 | 9 | 10 | ✓ (2 bullets) |

0 empty descriptions, 0 empty competency lists. All 3 guides: 11/11 perfect reconciliation.

### Parser bug fixed — `locate_sections()` Capstone detection

**Bug:** MBAHA has a bare "Capstone" row in the Standard Path table (pre-AoS) AND a real "Capstone" section heading after Areas of Study. Old implementation: `'Capstone' not in found` early-stop guard set `found['Capstone']` on first match (the SP row), then the post-scan filter deleted it (pre-AoS). But the deletion left `'Capstone' not in found` True again — and the real section (line 463) had already been scanned past. Never detected.

**Fix:** Collect all `CAPSTONE_RE` matches into `capstone_candidates[]` during scan (no early-stop guard on Capstone). Post-scan: filter to candidates after AoS, take first. If no candidates after AoS, no Capstone section.

**Regression verified:** BSDA, BSMGT, BSCSIA, MBA — all unchanged after fix. MBAHA re-parsed: HIGH, 0 warnings, 11/11 clean.

**Note:** This same pattern (bare "Capstone" SP row + real Capstone section after AoS) may appear in other families.

### Structural notes

- All 3 MBA guides use 3-column multiline SP format.
- MBA and MBAITM use old footer format (version 201404, 201408); MBAHA uses header-line.
- All 3 have Capstone with 2 competency bullets. MBA family capstones include the full competency trigger block (unlike graduate_standard where some capstones had 0 bullets).

### Artifacts produced

- `data/program_guides/parsed/{MBA,MBAHA,MBAITM}_parsed.json`
- `data/program_guides/validation/{MBA,MBAHA,MBAITM}_validation.json`
- `data/program_guides/manifest_rows/{MBA,MBAHA,MBAITM}_manifest_row.json`
- `data/program_guides/family_validation/mba_rollout_summary.{json,md}`

---

## Session 16 — graduate_standard Full Rollout (2026-03-21)

### Gate guide

MBA (all-HIGH manifest; served as gate for graduate_standard). MBA parsed at HIGH confidence, 0 anomalies. Gate passed.

### Full rollout results

9/9 guides parsed. **8 HIGH / 1 MEDIUM / 0 LOW.**

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone | Notes |
|------|--------|------------|---------|------------|-------------|---------|-------|
| MSCIN | M.S. Curriculum and Instruction | HIGH | 10 | 4 | 10 | — | |
| MSHRM | M.S. Human Resource Management | HIGH | 10 | 4 | 10 | — | |
| MSIT | M.S. Information Technology | HIGH | 11 | 2 | 11 | — | |
| MSITM | M.S. IT Management | **MEDIUM** | 10 | 4 | 9 | ✓ (0 bullets) | capstone desc polluted (see below) |
| MSITPM | M.S. IT — Product Management | HIGH | 10 | 2 | 10 | — | |
| MSITUG | B.S. IT (BSIT→MSIT pathway) | HIGH | 35 | 12 | 35 | — | bridge guide; 35 courses |
| MSMK | M.S. Marketing, Digital Marketing | HIGH | 11 | 2 | 11 | — | |
| MSMKA | M.S. Marketing, Analytics | HIGH | 11 | 2 | 11 | — | |
| MSML | M.S. Management and Leadership | HIGH | 10 | 4 | 9 | ✓ (0 bullets) | 0 bullets is source property |

### MEDIUM case — MSITM

Source PDF typo: "Accessibility and Accomodations" (single 'm'). `ACCESSIBILITY_RE` requires double 'm' — no match. Capstone section has no competency trigger block, so parser accumulates `description_buf` to EOF. Capstone title correct; opening description paragraph correct; remainder polluted with accessibility/boilerplate text.

**Impact:** MSITM capstone description unusable. AoS content (9 courses, all descriptions, all competencies) unaffected.

**Parser change:** None. Deferred — fixing `ACCESSIBILITY_RE` broadly carries regression risk; isolated to 1 guide.

### Structural notes

- All 9 guides use 3-column multiline SP format. No variant needed.
- Graduate capstones in this family may have 0 competency bullets (source-guide property, not parser failure).
- MSITUG is a BSIT-to-MSIT bridge guide with 35 courses. Parser handles identically.
- Metadata formats mixed: some header-line, some footer-based.

### Parser changes

**None (mba fix already covered above).**

### Artifacts produced

- `data/program_guides/parsed/{MSCIN,MSHRM,MSIT,MSITM,MSITPM,MSITUG,MSMK,MSMKA,MSML}_parsed.json`
- `data/program_guides/validation/{same}_validation.json`
- `data/program_guides/manifest_rows/{same}_manifest_row.json`
- `data/program_guides/family_validation/graduate_standard_rollout_summary.{json,md}`

---

## Session 15 (continued) — education_ba Full Rollout (2026-03-21)

### Full rollout results

All 11 education_ba guides parsed. 0 failures.

| Confidence | Count | Guides |
|---|---|---|
| HIGH | 5 | BAELED, BAESELED, BAESMES, BAESSESC, BAESSESP |
| MEDIUM | 6 | BAESSESB, BAESSESE, BAESSPEE, BAESSPMM, BASPEE, BASPMM |
| LOW | 0 | — |

### MEDIUM causes

**Pattern A — `sp_incomplete_row_at_eof` (BAESSESB, BAESSESE):**
Last SP row "Secondary Disciplinary Literacy" (CUs=3, Term=8) split across PDF page boundary. Term value appears after Total CUs line; parser breaks correctly at Total CUs. Course present in AoS. Same pattern as BSSWE_C.

**Pattern B — `competency_trigger_unexpected_state` (BAESSPEE, BAESSPMM, BASPEE, BASPMM):**
PDF text extraction reordering artifact in Fundamentals of Special Education course. Last bullet fragment ends with "...the Individualized" (no terminal punctuation). Following 50-char course title "Considerations for Instructional Planning for Learners" absorbed as bullet continuation by `len(line)>30` heuristic. Course present in SP but missing from AoS output. Consistent across all 4 Special Education guides. Parser fix deferred (regression risk).

### Parser changes this session

**None.**

### Subtype distribution

| Subtype | Guides | SP Format | Clinical/ST Groups |
|---|---|---|---|
| Teacher licensure | BAELED, BASPEE, BASPMM | 2-column (no Term) | Clinical Experiences (all 3); Student Teaching (BAELED, BASPEE only) |
| Educational Studies | BAESELED, BAESMES, BAESSESB, BAESSESC, BAESSESE, BAESSESP | 3-column (Term) | None |
| Educational Studies – Sped | BAESSPEE, BAESSPMM | 3-column (Term) | None |

### Quality (all 11 guides)

- 0 empty descriptions
- 0 empty competency lists
- 17 cert-prep mentions total
- 20 prereq mentions total

### Artifacts produced

- `data/program_guides/parsed/{6 new codes}_parsed.json`
- `data/program_guides/validation/{6 new codes}_validation.json`
- `data/program_guides/manifest_rows/{6 new codes}_manifest_row.json`
- `data/program_guides/family_validation/education_ba_rollout_summary.{json,md}`

### Next recommended family

**`graduate_standard`** — structurally closest to standard_bs; 9 guides; gate with MBA or MHA first.

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
