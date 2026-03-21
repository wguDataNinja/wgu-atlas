# DEV LOG

Terse dated ledger. One entry per session.
Each entry records what changed, decisions locked, what's blocked, and the next starting task.

---

## 2026-03-21 (session 20 — gap analysis: remaining families; Phase D readiness)

**Done**
- Diagnostic parse of all 24 remaining unvalidated guides (artifacts deleted post-diagnosis — not committed).
- Gap analysis written: `_internal/program_guides/PHASE_D_READINESS_GAP_ANALYSIS.md`
- Updated ATLAS_CONTROL.md next-session order with revised picture.

**Key findings**
- endorsement (8) and nursing_msn (5): ZERO parser issues. All HIGH in diagnostic. Phase A "high risk" assessment was unfounded. Immediate rollout candidates.
- education_grad/MSEDL (1): HIGH. Immediate rollout candidate.
- nursing_pmc (4): SP=0 rows (page layout puts "Changes to Curriculum" before SP table). AoS intact. degree_title wrong. Targeted fix required.
- education_grad/MEDETID (1): 3 embedded SP sub-tables (2 specializations). AoS intact (9 courses). SP overcounts and includes sub-table headers as courses. Moderate fix required.
- nursing_ug/BSNU (1): 4-column SP format (Option A / Option B). SP=0. AoS=22 intact. Non-trivial format work.
- nursing_ug/BSPRN (1): Dual-track 1783-line guide with embedded catalog refs. MEDIUM. Complex.
- nursing_rn_msn (3): LOW. Running page headers, non-course SP rows, multi-component structure. Major work for 3 guides.

**Decisions locked**
- "Risky" family risk was overstated: endorsement and nursing_msn are clean.
- nursing_rn_msn and nursing_ug (BSNU) are the genuine hard cases, not endorsement/nursing_msn.
- Phase D sequence: roll out clean 14 first → design schema/policy → build artifacts.
- Do not start Phase D artifacts before schema and inclusion/exclusion policy are defined.

**No parser changes. No commits (diagnostic only).**

**Next starting task**
- Gate and roll out endorsement (8) + nursing_msn (5) + MSEDL (1). See gap analysis Scenario A.

---

## 2026-03-21 (session 19 — education_ma gate/rollout; coverage accounting; capstone bug fix)

**Done**
- Established coverage accounting model: artifact coverage vs family-validated vs downstream-usable (full/partial) — see DEV_NOTES Session 19.
- Gated and rolled out education_ma: 9/9 HIGH, 0 anomalies, 0 warnings. Cleanest family to date.
- Fixed `parse_capstone` KeyError: capstone dict was missing `prerequisite_mentions`/`certification_prep_mentions` before `_scan_description_mentions()` call. MAMEK6 triggered crash. Regression-verified against 23 guides.
- Re-parsed 9 previously committed capstone guides (BSBAHC, BSDA, BSHHS, BSMGT, MBAHA, MBAITM, MSCSIA, MSITM, MSML) to apply fix consistently.
- Proposed looks_like_prose verb-presence heuristic for accounting_ma specializations (not implemented — requires dedicated session).

**Files changed**
- `scripts/program_guides/parse_guide.py` (capstone fix)
- `data/program_guides/parsed/{MAMES,MAELLP12,MAMEK6,MAMEMG,MASEMG,MASESB,MASESC,MASESE,MASESP,BSBAHC,BSDA,BSHHS,BSMGT,MBAHA,MBAITM,MSCSIA,MSITM,MSML,MBA,MHA,BSCSIA}_parsed.json`
- `data/program_guides/validation/{education_ma 9 codes}_validation.json`
- `data/program_guides/manifest_rows/{education_ma 9 codes}_manifest_row.json`
- `data/program_guides/family_validation/education_ma_gate_report.{json,md}`
- `data/program_guides/family_validation/education_ma_rollout_summary.{json,md}`
- `_internal/program_guides/DEV_NOTES.md`, `_internal/ATLAS_CONTROL.md`, `_internal/ATLAS_REPO_MEMORY.md`

**Decisions locked**
- Coverage accounting must use three distinct layers. Never cite artifact coverage as validation coverage.
- education_ma fully rolled out. No exclusions.
- accounting_ma specializations remain deferred. Fix requires dedicated session with full regression.
- Phase D numeric threshold is crossed but Phase D readiness requires separate conservative assessment.

**Blocked**
- Phase D not started (needs readiness assessment).
- accounting_ma specializations blocked on looks_like_prose fix.

**Next starting task**
- Phase D readiness assessment memo (conservative — evaluate downstream coverage, risky-family gaps, safe-field boundaries before deciding).

---

## 2026-03-20 (session 13 — standard_bs family validation)

**Done**
- Ran parse_guide.py on BSCS, BSIT, BSMGT, BSPSY (4 new guides + BSDA baseline = 5 total)
- Found and fixed 5 parser bugs across two root-cause groups: SP table format assumptions and footer detection
  1. Multi-line SP format (BSCS/BSIT/BSMGT/BSPSY): added `parse_standard_path_multiline()` with `detect_sp_multiline()` format routing
  2. Split-footer format: added `FOOTER_CODE_ONLY_RE`, updated `is_footer()` to catch "CODE YYYYMM" lines and "©..." lines
  3. Header-line metadata format (BSIT/BSMGT): added `HEADER_META_RE` in `extract_metadata()`
  4. `PAGE_NUM_RE` was skipping CU/term values in multi-line SP parser: removed from SP parser, kept for AoS only
  5. Page number after footer consumed as CU value: added `prev_was_footer` flag
  6. "Total CUs 110" treated as title: added `SP_TOTAL_RE` terminator
  7. Column header repeated at page tops: added `HEADER_LINE_RE` mid-table skip
- Final results: all 5 guides at HIGH confidence, 0 anomalies, 0 warnings
- Created `data/program_guides/family_validation/standard_bs_validation_summary.json` and `.md`
- Updated `_internal/program_guides/DEV_NOTES.md` with session 13 section

**Decisions locked**
- standard_bs family READY for `--all` rollout
- Multi-line SP and split-footer format handling is now the default path; single-line (BSDA) is the legacy exception
- `prev_was_footer` flag is the correct mechanism for distinguishing page numbers from data values in the SP parser
- Do not run `--all` until BSMES is specifically validated (it has Student Teaching / Clinical Experiences variant sections)

**Blocked / open**
- BSMES specific validation (standard_bs with education-style variant sections) — run before `--all`
- Page count extraction for header-line format guides returns 0 — cosmetic, non-blocking
- SP/AoS title reconciliation uses exact string match — may surface minor mismatches in batch

**Next starting task**
Run `parse_guide.py --program BSMES`, inspect for education-variant section handling, then run `--all` for standard_bs family (or full corpus if BSMES is clean).

---

## 2026-03-20 (session 12 — Phase A execution + BSDA thin-slice parser)

**Done**
- Ran `extract_guide_texts.py`: 114 PDFs converted to .txt (1 skipped — BSDA pre-existing), 0 failures
- Ran `analyze_guide_manifest.py`: produced `guide_manifest.json` (115 rows), `section_presence_matrix.csv`, `manifest_summary.json` — 19 families identified, 29 guides with variant section headings
- Debugged and fixed 3 bugs in `parse_guide.py` AoS state machine:
  1. INTRO boilerplate detection: replaced word-count heuristic with `intro_prose_seen` flag + `looks_like_prose()` check
  2. SEEKING→IN_DESCRIPTION transition: added prose-line detection with `pending_titles` buffer resolve
  3. `elif in_bullet` fall-through: added `emit_course()` + `state='SEEKING'` so group heading lines aren't silently discarded; fixed `emit_course()` to not overwrite already-flushed descriptions
- BSDA thin-slice parse: confidence=HIGH, 0 anomalies, 0 warnings; 14 groups, 41 courses, all with descriptions and bullets
- Created `_internal/program_guides/DEV_NOTES.md` with full session accounting

**Decisions locked**
- `pdftotext` (poppler) confirmed as extraction tool; output matches pre-existing BSDA.txt exactly
- `looks_like_prose()` (len > 80 OR ends with sentence punctuation) is the reliable discriminator for intro boilerplate vs group/course headings
- Pending-titles buffer (1 item = course, 2 items = group+course) is correct; the bug was in missing the IN_DESCRIPTION transition and in the `elif in_bullet` fall-through path
- `--all` mode should not be run until standard_bs family is validated on 3–5 additional programs

**Blocked / open**
- Standard_bs family validation: need BSCS, BSITM, BSHA, BSFIN test runs before running `--all`
- Education/MAT/endorsement/nursing variants: detected in manifest but not yet handled by parser
- Course-code matching: deferred (Phase E)
- Site integration: deferred

**Next starting task**
Run `parse_guide.py --program BSCS` (and 2–3 more standard_bs programs) to validate parser generalizes within the family before broader rollout.

---

## 2026-03-20 (session 11 — program guide extraction workstream initialized)

**Done**
- Read `parse_catalog_v11.py` in full (all 742 lines), including `lib/anchors.py` and `lib/config.py`
- Read BSDA.txt in full (860 lines) to confirm actual guide document structure
- Produced full technical readout: `_internal/program_guides/TECHNICAL_READOUT.md`
  - What `parse_catalog_v11.py` does step by step (era detection, 4 passes, 3 downstream steps, output artifacts)
  - Catalog-specific logic to not reuse (12 items)
  - Reusable patterns (10 items: footer metadata, section anchors, state machine, anomaly collection, JSON style, etc.)
  - Proposed parser design: `analyze_guide_manifest.py`, `parse_guide.py`, `build_guide_site_data.py`, `match_guide_courses.py`
  - Manifest-first corpus analysis plan with 30-field manifest schema
  - 15 guide family hypotheses based on filename patterns
  - Recommended artifacts for analysis phase (8 artifacts)
  - Full pipeline shape: Phase A through E
  - BSDA thin-slice first milestone with target JSON schemas
  - Key structural notes: no course codes, boilerplate skip zones, multi-page table handling, Areas of Study header variant, Capstone as section boundary, closing boilerplate as end anchor
- Created `_internal/program_guides/README.md` — workstream control doc
- Updated `_internal/ATLAS_CONTROL.md`: added program guide extraction workstream to §5 table, full §6.0 snapshot, updated next-session order, updated artifact map
- Updated `_internal/ATLAS_REPO_MEMORY.md`: added §12a Program guide extraction system

**Decisions locked**
- Manifest-first approach: analyze all 115 guides before writing a content parser
- BSDA is the thin-slice validation case for Phase B
- Course title → Atlas code matching is a separate downstream step (Phase E), not part of structural parsing
- Guide family classification drives parser branching; do not assume one parser fits all 115 guides
- Reuse `parse_catalog_v11.py` patterns: footer metadata, section anchor scan, state machine, anomaly collection; do NOT reuse: era detection, multi-edition structures, Total CUs terminator, index/body reconcile

**Blocked / open**
- 114 of 115 guide PDFs not yet extracted to text
- No parsing scripts exist yet
- Guide family structure is hypothetical pending manifest analysis
- Correct runtime attachment model for parsed guide content on program pages not yet decided

**Next starting task**
Extract all 115 PDFs to text using pdftotext or equivalent; commit all texts; write `analyze_guide_manifest.py`.

---

## 2026-03-20 (session 10 — public site baseline expanded)

**Done**
- Substantially expanded `_internal/page_designs/wgu_public_site_student_experience.md` from initial stub into a full baseline document
- Added confirmed findings for: Online Degrees expanded submenu taxonomy and cross-listing patterns; Explore Your Options quiz/recommendation flow; All Degrees browse surface (default state + card expansion); official compare flow (confirmed real, narrow, headline-metrics-only); official program-detail template scaffold (18 observed elements); three representative program pages (BSCS, Nursing Informatics RN-to-MSN, BSDA); education official-resource standalone pages (student teaching, licensure, state compliance); official page-type taxonomy (12 types); alternative-start, advanced-course, cert-mapping, and accelerated page types; program guides as a major official artifact layer with worked BSDA example
- Updated Atlas implications: revised away from "WGU has no compare tool" to more truthful contrast (WGU compares headline outcomes, Atlas compares program structure)
- Preserved and updated open questions and session handoff

**Decisions locked**
- Official compare exists and is real — do not claim Atlas is the only compare surface; claim structural/curriculum comparison as the differentiator
- Program guides are a major official artifact layer, not just supplemental PDFs — should be treated as a high-value harvest target
- Public site is broad and information-rich in places but fragmented; the limitation is packaging and synthesis, not lack of data
- Atlas homepage claim: restructure official WGU information into a clearer student-use guide without enrollment-funnel wrapping

**Blocked / open**
- School-level landing page reads not yet done (Business, Education, Technology, Health & Nursing)
- Course-level discovery baseline on the public site not yet documented
- Outcomes/competency-statement visibility on program pages not yet confirmed

**Next starting task**
School-level landing page reads; then course-level discovery baseline; then revisit `homepage_design_session_2026-03.md` synthesis with full dual baseline in hand.

---

## 2026-03-20 (session 9 — public site baseline stub)

**Done**
- Created `_internal/page_designs/wgu_public_site_student_experience.md` — initial baseline doc for how students encounter WGU on the public website; captures confirmed top-nav structure, Online Degrees dropdown options, and public degree hub URL; 14 sections stubbed for next session
- Updated `_internal/page_designs/README.md` to register the new doc in the source-baseline group and file index

**Decisions locked**
- Atlas should be positioned against the public-site experience as well as the raw catalog; both baselines must be documented before homepage framing is finalized
- Public-site baseline doc is intentionally partial; next session continues the official WGU site student journey

**Blocked / open**
- Sections 5–12 of `wgu_public_site_student_experience.md` require a follow-up session with live site observation
- All open items from session 7 still stand

**Next starting task**
Continue `wgu_public_site_student_experience.md`: follow the Online Degrees entry flows, document school-level pages, and capture a representative official program page.

---

## 2026-03-20 (session 8 — page design artifacts)

**Done**
- Created `_internal/page_designs/compare_page.md` — current-state visual/product reading of `/compare`; establishes Compare as a flagship homepage-proof surface
- Created `_internal/page_designs/source_vs_atlas_program_entry.md` — raw catalog vs Atlas BSCS before/after; documents structural transformation argument
- Created `_internal/page_designs/screenshot_analysis_log.md` — running log of screenshot-based design readings from 2026-03-20 session
- Created `_internal/page_designs/homepage_design_session_2026-03.md` — March 2026 design session conclusions; homepage should move from navigation shell to proof-of-value surface
- Replaced `_internal/page_designs/README.md` with expanded version covering all four artifact categories and recommended reading order
- Added `_internal/page_designs/` pointer to `ATLAS_CONTROL.md` artifact map and `ATLAS_REPO_MEMORY.md` surface-roles section

**Decisions locked**
- Homepage strongest claim: "Atlas turns a fragmented source system into a structured student-use product"
- Degree pages and Compare are the two lead homepage-proof surfaces; course-connectedness is third
- Ecosystem material belongs lower on the homepage, not as the lead identity

**Blocked / open**
- Same as session 7

**Next starting task**
Same as session 7: outcomes + accreditation completeness audit (Tier 2).

---

## 2026-03-20 (session 7 — second-pass doc update)

**Done**
- Completed rev 5 of `_internal/WGU_ONLINE_ECOSYSTEM_INDEX.md`: §13.1 expanded with blog evidence, scale signals (SHRM 760 members, Cybersecurity Club 7,000+), Women in Tech as model club-page template, NBMBAA unlisted YT video evidence, Reddit historical dead-link note; §13.2 table rows updated with model/YT detail
- Added `Homepage / community / social — planning implications` subsection to `_internal/ATLAS_REPO_MEMORY.md` §17: surface priority signal, feature/section directions, things to avoid, club surfacing approach, WHU external benchmark note
- No changes to `_internal/ATLAS_CONTROL.md` (not clearly needed for this session's material)

**Decisions locked**
- Homepage/community planning notes are durable planning-only context in repo memory; do not act on them until explicitly selected as a workstream
- WHU is the clearest external design precedent for compact club/community surfacing

**Blocked / open**
- Same as session 6: Data Club public URL unconfirmed; club ecosystem discoverability fragmented
- 6 programs still missing guide placements in `official_resource_placements.json`

**Next starting task**
Outcomes + accreditation completeness audit (Tier 2): pick up where official-resource workstream left off. Check `official_context_manifest_phase1.csv` for outcomes/accreditation pages not yet in placements.

---

## 2026-03-20 (session 6 — ecosystem index)

**Done**
- Created `_internal/WGU_ONLINE_ECOSYSTEM_INDEX.md` — internal source atlas for official/unofficial/community/media surfaces related to WGU
- Added cross-reference note to `_internal/ATLAS_CONTROL.md` (backlog area)
- Added repo map entry and short subsection to `_internal/ATLAS_REPO_MEMORY.md`
- Added §13 Official clubs / student organizations (8 entries: AMA, Cybersecurity Club, NBMBAA, NSLS, SHRM, Women in Tech, WGU Connect, hub page)
- Added §13.3 dedicated WGU Data Club subsection — active, under-promoted, research_only for now
- Rev 3: elevated Student Communities to first-class official hub entry; resolved Night Owl Network and Career Services URLs; added WGU Alumni LinkedIn; added §6.4 official link hub comparison (Communities page vs Linktree — Communities includes YouTube, Linktree does not)
- Rev 4: added Cyber Education Center community outreach page as de facto buried club hub; upgraded Data Club from `research_only/anecdotal` to `candidate_later/officially referenced`; added WiCyS, Military Alliance Club, Alumni Cybersecurity Club; strengthened discoverability fragmentation note

**Decisions locked**
- Ecosystem index is reference/awareness only; does not change product posture or deferred status of Reddit/community integration
- Clubs classified as `official_adjacent`; not homepage-ready until infrastructure/discoverability stabilizes
- Data Club: `research_only` until a public-facing entry point is confirmed

**Blocked / open**
- Data Club public URL unconfirmed; flagged as `verify_internal_or_public_entry`
- Club ecosystem discoverability fragmented across wgu.edu / careers / WGU Connect; no single authoritative hub yet

**Next starting task**
Outcomes + accreditation completeness audit (Tier 2): pick up where official-resource workstream left off.

---

## 2026-03-20 (session 5 — regulatory gap verification)

**Done**
- Verified 5 follow-up gaps from the regulatory placement pass
- Removed NCLEX from BSNPLTR (page scoped to RN-to-BSN audience; wrong for prelicensure)
- Added clinicals to BSPNTR (page confirmed to cover pre-nursing terms explicitly)
- Net change: 131 entries (−1 +1)

**Decisions locked**
- No BSNPLTR-specific NCLEX page exists in the WGU sitemap (phase1); attach if/when WGU creates one
- BSNPLTR gets clinicals only; BSNU gets NCLEX only; audience split is confirmed
- Education Praxis/Student Teaching degree-level attachments: deferred; too many programs to enumerate without per-program verification

**Blocked / open**
- ACEN/CCNE nursing accreditation: deferred to Tier 2 outcomes/accreditation audit
- Education degree-level Praxis/Student Teaching: deferred; clean defer with rationale

**Next starting task**
Outcomes + accreditation completeness audit (Tier 2): check `official_context_manifest_phase1.csv` for any outstanding outcomes/accreditation pages.

---

## 2026-03-20 (session 4 — regulatory placement pass)

**Done**
- Resolved 3 needs-review items: all 3 → keep (Teacher Licensure Programs, FNP Preceptor, PMHNP Preceptor)
- Added 15 placement entries to `public/data/official_resource_placements.json` (116 → 131)
- New `regulatory_licensure` resource_group introduced (priority 12, label "Licensure & Exams")
- Added GROUP_LABELS entry in `RelevantResources.tsx`
- Coverage: School of Education (3), School of Health (2), BSNPLTR (2), BSNU (1), BSPNTR (1), MSNUFNP (2), MSNUPMHNP (2), School of Business (1), School of Technology (1)

**Decisions locked**
- regulatory_licensure display_priority = 12 (above accreditation at 15, below outcomes at 10)
- All 14 candidates from the queue resolved; none deferred

**Blocked / open**
- NCLEX URL is nested under RN-to-BSN path; verify if BSNPLTR-specific NCLEX page exists
- BSPNTR clinicals: deferred; unclear which clinical pages apply to pre-nursing track
- Education Praxis/Student Teaching degree-level attachments: deferred; need program code enumeration
- ACEN/CCNE nursing accreditation: not found in sitemap pass

**Next starting task**
Outcomes + accreditation completeness audit (Tier 2): check `official_context_manifest_phase1.csv` for any outcomes/accreditation pages not yet in `official_resource_placements.json`.

---

## 2026-03-20 (session 3 — baseline commits + regulatory queue)

**Done**
- Made 3 local commits: data reorg, control-plane docs, src baseline changes
- Built `_internal/official_resource/regulatory_candidate_queue.md` — 14 candidates reviewed; 11 `keep`, 3 `needs-review`, 8 `skip`
- Updated official_resource SESSION_LOG.md and ARTIFACTS.md

**Decisions locked**
- None new this session beyond prior

**Blocked / open**
- 3 `needs-review` items in regulatory queue require page reads before finalizing: #3 Teacher Licensure Programs, #11 FNP Preceptor, #12 PMHNP Preceptor
- NCLEX page for BSNPLTR specifically — verify if degree-specific page exists or if school-level page is the right attachment
- Nursing disclosure/accreditation gaps flagged in queue

**Next starting task**
Curation review: read the 3 `needs-review` pages, confirm or decline, then update `public/data/official_resource_placements.json` with the first round of approved regulatory/licensure placements.

---

## 2026-03-20 (session 2 — housecleaning)

**Done**
- Renamed `data/lineage/program_ineage_events.json` → `program_lineage_events.json` (typo fixed)
- Removed typo fallback from `scripts/generate_program_history_enrichment.py` (line that referenced `program_ineage_events.json`)
- Deleted `scripts/__pycache__/` (junk, already gitignored)
- Deleted empty `docs/` directory (all canon docs live in `_internal/`; docs/ had no purpose)
- Fixed `_internal/ATLAS_REPO_MEMORY.md` repo map: removed stale `docs/` row, updated `data/` to reflect subdirectory structure, added `content_map.txt` entry
- Confirmed `public/screenshots/` does not exist; root-level `screenshots/` is the actual dir (already documented correctly)
- Confirmed `src/app/proto/` and `src/components/proto/` are intentional; already documented in ATLAS_REPO_MEMORY.md as experimental surfaces
- `compare_program_courses.py` typo fallback intentionally left (defensive; harmless now that file is renamed correctly)

**Decisions locked**
- `docs/` removed permanently; all canon lives in `_internal/`
- `content_map.txt` is an active tracked artifact; regenerate after major UI changes

**Blocked / open**
- Same as prior session; data reorg and src changes still uncommitted
- `compare_program_courses.py` typo fallback can be cleaned up in a future script maintenance pass

**Next starting task**
Commit all pending changes (data reorg, src, script fixes, DEV_LOG, ATLAS_CONTROL, ATLAS_REPO_MEMORY), then build `_internal/official_resource/regulatory_candidate_queue.md`.

---

## 2026-03-20 (session 1 — control doc consolidation)

**Done**
- Created `_internal/ATLAS_CONTROL.md` and `_internal/ATLAS_REPO_MEMORY.md` — completed 3-doc control system
- Ran repo readiness scan; identified stale docs, data reorg state, and prep steps
- Fixed authority map: all three control docs now live in `_internal/` (not `docs/`)
- Updated ATLAS_CONTROL.md: stale next-session order replaced, `docs/ATLAS_REPO_MEMORY.md` refs corrected to `_internal/`, lineage artifact paths updated to `data/lineage/`
- Marked K-01 and K-02 in WORKQUEUE.md as superseded (DECISIONS.md and ATLAS_SPEC.md are archived)
- Archived `scripts/bootstrap_source_enrichment_manifest.py` to `_internal/archive/2026-03-final-consolidation/`
- `docs/` directory is intentionally empty; all canon docs live in `_internal/`

**Decisions locked**
- 3-doc system: ATLAS_CONTROL + ATLAS_REPO_MEMORY + DEV_LOG, all in `_internal/`
- official-resource activation is first finish-track after baseline cleanup
- Compare is not the first implementation track; revisit after baseline cleanup
- Lineage export remains deferred; it is not automatic
- `homepage_summary.json` count mismatch: do not patch without confirming it is a true bug vs. semantic count difference

**Blocked / open**
- 15 data file deletions and new `data/site/`, `data/lineage/`, `data/enrichment/` dirs are uncommitted (working tree dirty)
- `LearningOutcomes.tsx`, `programs/[code]/page.tsx`, `CompareSelector.tsx` changes are uncommitted
- `data/lineage/program_ineage_events.json` has a filename typo — verify script references before renaming

**Next starting task**
Commit the pending data reorg + src changes, then build `_internal/official_resource/regulatory_candidate_queue.md`.
