# Atlas Spec

## 1) Contract
- Purpose: factual implementation spec for this repo.
- Scope: structure, artifacts, scripts, runtime data flow, operational runbooks, known implementation gaps.
- Out of scope: normative product/policy rules (in `docs/DECISIONS.md`).
- MECE split:
  - `ATLAS_SPEC.md` = what exists and how it runs.
  - `DECISIONS.md` = what is allowed/required and why.

## 2) Snapshot (repo-observed)
- Stack: Next.js 15 (`output: export`), React 19, TypeScript, Tailwind, static JSON artifacts.
- Deploy: GitHub Pages (`.github/workflows/deploy.yml`), base path `/wgu-atlas`.
- Core counts (current committed data):
  - `data/canonical_courses.csv`: 1,646 rows.
  - `data/program_history.csv`: 196 rows.
  - `data/named_events.csv`: 41 rows.
  - `data/program_transition_universe.csv`: 107 rows.
  - `data/program_link_candidates.json`: 48 boundaries, 123 candidates.
  - `data/program_lineage_enriched.json`: 28 events.
  - `data/program_history_enrichment.json`: 28 events.
  - `data/official_context_manifest_phase1.csv`: 604 rows.
  - `data/official_context_manifest_phase2_test.json`: 122 records.
  - `public/data/courses.json`: 1,646 cards.
  - `public/data/programs.json`: 196 programs.
  - `public/data/events.json`: 41 events.
  - `public/data/search_index.json`: 1,842 records.
  - `public/data/courses/*.json`: 838 detail files.
  - `public/data/program_enriched.json`: 114 program keys.
  - `public/data/official_resource_placements.json`: 116 placements.

## 3) Repo topology
- `src/`: Next app/router pages, UI components, file-based data access in `src/lib/data.ts`.
- `public/data/`: frontend-consumed exports.
- `data/`: canonical artifacts, review artifacts, enrichment artifacts.
- `scripts/`: deterministic generators/transforms/utilities.
- `docs/`: canonical docs + legacy docs pending retirement.
- `_internal/`: planning/dev docs, official-context work logs, YouTube source workstream.
  - `_internal/SOURCE_ENRICHMENT_AUDIT.md`: master audit and operating doc for all source-enrichment work.
  - `_internal/youtube/`: YouTube workstream (raw inventories, filtered working copies, worklog).
  - `_internal/workqueue_inputs/`: active work queue inputs for ongoing enrichment passes.

## 4) Data domains

### 4.1 Catalog baseline domain
- Purpose: historical course/program/event facts.
- Primary artifacts:
  - `data/canonical_courses.csv|json`
  - `data/program_history.csv`
  - `data/named_events.csv|json`
  - `data/title_variant_classification.csv`
  - `data/title_variant_summary.json`

### 4.2 Program lineage domain
- Purpose: detect and enrich logical program transitions.
- Artifact ladder:
  - Recall: `data/program_transition_universe.csv`
  - Review: `data/program_link_candidates.json`
  - Stage 1 output (LLM/HITL input/output family): `data/program_lineage_events*.json`
  - Deterministic pair enrichment: `data/program_lineage_enriched.json`
  - Final event-level page enrichment: `data/program_history_enrichment.json`
  - Optional program-centric derivative: `data/program_history.json`

### 4.3 Official-context domain
- Purpose: attach official WGU resources to program/school surfaces.
- Audit and operating doc: `_internal/SOURCE_ENRICHMENT_AUDIT.md` — single reference for current state, pass log, next actions.
- Work surfaces:

| Source type | Raw universe | Active candidate manifest | Notes/log | Live placements |
|---|---|---|---|---|
| WGU sitemap pages | `data/official_context_manifest_phase1.csv|json` | `data/source_enrichment_manifest.json` | `_internal/SOURCE_ENRICHMENT_AUDIT.md` §5 | `public/data/official_resource_placements.json` |
| Official WGU YouTube | `_internal/youtube/raw/wgu_official_titles_raw.txt` | `_internal/youtube/working/wgu_official_titles_filtered.txt` | `_internal/youtube/YOUTUBE_WORKLOG.md` | — (not yet placed) |
| WGU Career Services YouTube | `_internal/youtube/raw/wgu_career_services_titles_raw.txt` | `_internal/youtube/working/wgu_career_services_titles_filtered.txt` | `_internal/youtube/YOUTUBE_WORKLOG.md` | — (not yet placed) |
| Reddit/community | — (external project) | — (future) | `_internal/SOURCE_ENRICHMENT_AUDIT.md` §5 | — (future) |

- Current sitemap execution state:
  - Phase 1 sitemap manifest: 604 unique entries.
  - Phase 2 enriched set: 122 entries (115 program guides + 7 other types).
  - Remaining batch input: `_internal/workqueue_inputs/official_context_phase2_remaining_batch.json` (262 entries: 138 program landing pages, 123 specialization subpages, 1 accreditation).
  - Program guides: **solved** — 109/114 active programs have live placements. 6 programs missing (BSNPLTR, BSPNTR, MASEMG, MEDETID, MEDETIDA, MEDETIDK12).
  - Validated enrichment heuristics from Phase 2:
    - `program-guide.html` pages are canonical wrapper pages for downloadable guide PDFs.
    - `outcomes.html` and specialization/track subpages are higher-signal than guide wrappers.
    - School candidate seed inferred from first URL path segment (`online-it-degrees`, `online-business-degrees`, `online-nursing-health-degrees`, `online-teaching-degrees`).
- Current YouTube state:
  - Raw inventories imported 2026-03-18 from external yt-video-analysis repo.
  - Official WGU: 1,535 raw → 818 after commencement/graduation filter.
  - Career Services: 441 raw → 267 after first-pass junk filter.
  - No candidate artifacts or placements yet. Next pass: YT-1 (school-level, Official WGU).

### 4.4 Frontend export domain
- Frontend directly consumes:
  - `public/data/courses.json`
  - `public/data/courses/{code}.json`
  - `public/data/programs.json`
  - `public/data/program_enriched.json`
  - `public/data/events.json`
  - `public/data/search_index.json`
  - `public/data/homepage_summary.json`
  - `public/data/official_resource_placements.json`
- Exception: course fallback reads internal artifact `data/canonical_courses.json` from server-side `src/lib/data.ts`.

## 5) Artifact registry (schema-level)

### 5.1 Canonical tabular/json artifacts (`data/`)
- `data/canonical_courses.csv` columns:
  - `course_code`, `canonical_title_current`, `observed_titles`, `first_seen_edition`, `last_seen_edition`, `active_current`, `contexts_seen`, `current_programs`, `current_program_count`, `historical_programs`, `historical_program_count`, `edition_count`, `ghost_flag`, `single_appearance_flag`, `stability_class`, `title_variant_class`, `current_title_confidence`, `canonical_cus`, `current_college`, `colleges_seen`, `notes_confidence`.
- `data/program_history.csv` columns:
  - `program_code`, `status`, `first_seen`, `last_seen`, `edition_count`, `span_months`, `versions_seen`, `version_changes`, `version_progression`, `colleges`, `college_count`, `cus_values`, `degree_heading_count`, `degree_headings`.
- `data/named_events.csv` columns:
  - `event_id`, `start_edition`, `end_edition`, `event_title`, `event_type_primary`, `event_type_secondary`, `severity_score`, `course_churn`, `courses_added_count`, `courses_removed_count`, `program_churn`, `version_changes_count`, `title_changes_count`, `affected_schools`, `affected_programs_added`, `affected_programs_removed`, `affected_courses_added_sample`, `affected_courses_removed_sample`, `observed_summary`, `interpreted_summary`, `confidence`, `is_curated_major_event`.
- `data/official_context_manifest_phase1.csv` columns:
  - `title`, `url`, `keep`, `status`, `page_type`, `official_context_type`, `summary`, `school_candidates`, `program_candidates`, `course_candidates`, `notes`, `source`.

### 5.2 Program-lineage artifacts (`data/`)
- `data/program_transition_universe.csv` columns:
  - `boundary_index`, `start_edition`, `end_edition`, `programs_removed_count`, `programs_added_count`, `programs_removed`, `programs_added`, `removed_titles`, `added_titles`, `removed_colleges`, `added_colleges`, `removed_cus_values`, `added_cus_values`, `total_program_churn`, `net_program_delta`, `has_churn`.
- `data/program_link_candidates.json` top-level:
  - `metadata`, `boundary_reviews[]`, `candidates[]`.
  - `candidates[]` keys:
    - `candidate_id`, `transition_type_guess`, `confidence_guess`, `start_edition`, `end_edition`, `removed_programs`, `added_programs`, `same_college_or_school_signal`, `title_similarity_notes`, `degree_heading_similarity_notes`, `cu_similarity_notes`, `adjacency_notes`, `overlap_metrics`, `rationale`, `review_status`.
- `data/program_lineage_enriched.json` top-level:
  - `metadata`, `events[]` where each event has `event_id`, `transition_type`, `start_edition`, `end_edition`, `pairs[]`.
  - pair keys:
    - `from_program`, `to_program`, `metrics`, `courses_removed`, `courses_added`.
  - `metrics` keys:
    - `shared_course_count`, `removed_course_count`, `added_course_count`, `old_retained_pct`, `new_inherited_pct`, `jaccard_overlap`.
- `data/program_history_enrichment.json` top-level:
  - `events[]` where each event has:
    - `event_id`, `transition_type`, `start_edition`, `end_edition`, `from_programs`, `to_programs`, `importance`, `site_worthy`, `pairs[]`.
  - pair keys in final artifact:
    - `from_program`, `to_program`, `shared_course_count`, `removed_course_count`, `added_course_count`, `old_retained_pct`, `new_inherited_pct`, `jaccard_overlap`, `courses_added`, `courses_removed`.
- `data/lineage/lineage_decisions.json` top-level:
  - `schema_version`, `last_updated`, `event_decisions[]`, `program_decisions[]`.
  - `event_decisions[]` keys:
    - `event_id`, `decision`, `display_state`, `decided_by`, `decided_at`, `wording_guard`, `change_summary_template`, `zero_overlap_rationale`, `notes`.
  - `decision` values: `approve_history`, `reject_history`, `pending_hitl`, `pending_gap_check`.
  - `display_state` values: `show`, `suppress`, `hide_pending`.
  - `program_decisions[]` keys:
    - `program_code`, `program_state`, `history_ui_state`, `linked_event_id`, `decided_by`, `decided_at`, `notes`.
  - `program_state` values: `history_approved`, `history_excluded`, `new_from_scratch`, `pathway_variant`, `no_meaningful_history`, `pending_hitl`, `pending_gap_check`.
  - `history_ui_state` values: `show`, `hide_new`, `hide_no_history`, `hide_excluded`, `hide_pending`.
  - Curation overlay and display authority for the Program History feature.
  - `display_state` overrides `program_history_enrichment.json` `site_worthy` at export time.
  - Durable: survives pipeline reruns; must not be regenerated by scripts.
  - Events absent from this file are suppressed at export regardless of `site_worthy`.
  - Validated by `scripts/validate_lineage_decisions.py`.

### 5.3 Source enrichment manifest (`data/source_enrichment_manifest.json`)
- Durable candidate manifest spanning all enrichment source families (sitemap, YouTube, Reddit/community).
- Generated once by `scripts/bootstrap_source_enrichment_manifest.py` (2026-03-18); updated incrementally by review sessions.
- Field groups:
  - **Identity/source:** `source_key` (stable row ID), `source_family`, `source_subtype`, `url`, `title`
  - **Classification:** `candidate_type` (`program_guide | program_landing | specialization | accreditation | outcomes | school_context | youtube_video | other`), `target_scope` (`program | school | course`)
  - **Review decision:** `review_status` (`unreviewed | keep | skip | defer`), `decision_reason`, `notes`
  - **Candidate hints:** `program_candidates[]`, `school_candidates[]`, `course_candidates[]`
  - **Placement targets:** `program_targets[]`, `school_targets[]`, `course_targets[]`
  - **Lifecycle:** `is_currently_present`, `first_seen_at`, `last_seen_at`, `last_reviewed_at`
- Bootstrap totals: 384 rows (122 `keep` from sitemap Phase 2, 262 `unreviewed` from remaining queue).
- Supersedes `data/official_context_manifest_phase2_test.json` as the active enrichment artifact. That file is now a historical transitional artifact.

### 5.4 Frontend exports (`public/data/`)
- `courses.json`: 1,646 lightweight course cards (`code`, `title`, `active`, `scope`, `first_seen`, `last_seen`, `edition_count`, `current_college`, `current_program_count`, `stability_class`, `ghost_flag`, `single_appearance_flag`, `title_variant_class`).
- `courses/{code}.json`: 838 rich AP course details incl. `programs_timeline`.
- `programs.json`: 196 program records.
- `program_enriched.json`: code-keyed map with `description`, `roster`, `outcomes` for 114 active programs (2026-03 extraction).
- `events.json`: 41 timeline events.
- `search_index.json`: course + program search records.
- `homepage_summary.json`: site summary + preview modules.
- `official_resource_placements.json`: curated placements for program/school sidebars.

## 6) Script registry (actual code)

| Script | Role | Inputs | Outputs |
|---|---|---|---|
| `scripts/build_site_data.py` | baseline site-data build (legacy but functional) | upstream `WGU_catalog/outputs/*` (`course_history.csv`, `program_history.csv`, `edition_diffs*`, `course_index_v10.json`, trusted 2026-03 CSVs) | `data/canonical_courses*`, `data/named_events*`, `data/curated_major_events.json`, `data/title_variant_*`, plus `public/data/courses.json`, `public/data/courses/{code}.json`, `public/data/events.json`, `public/data/search_index.json`, `public/data/homepage_summary.json`; (pending) `public/data/program_lineage.json` — merge of `program_history_enrichment.json` (metrics source) + `lineage_decisions.json` (display authority); export step not yet implemented |
| `scripts/extract_program_enriched.py` | parse 2026-03 program descriptions/rosters/outcomes | `catalog_2026_03.txt`, `2026_03_program_blocks_v11.json`, `public/data/programs.json` | `public/data/program_enriched.json` |
| `scripts/build_program_lineage_artifacts.py` | lineage recall + candidate generation | `data/program_history.csv`, `data/canonical_courses.csv`, catalog text+blocks dirs | `data/program_transition_universe.csv`, `data/program_link_candidates.json` |
| `scripts/compare_program_courses.py` | lineage Stage 2 deterministic overlap/diffs + resilient JSON normalize | `data/program_lineage_events.json` (or typo fallback), `data/canonical_courses.csv`, catalog text+blocks dirs | `data/program_lineage_events_normalized.json`, `data/program_lineage_enriched.json` |
| `scripts/generate_program_history_enrichment.py` | lineage final event-level transform | `data/program_lineage_enriched.json` (+ optional Stage1 titles) | `data/program_history_enrichment.json` |
| `scripts/generate_program_history_artifacts.py` | optional program-centric derivative | `data/program_lineage_enriched.json` | `data/program_history.json` |
| `scripts/add_program_history_enrichment.py` | helper backfill of importance/site_worthy into program-centric file | `data/program_history.json`, `data/program_history_enrichment.json` | in-place `data/program_history.json` update |
| `scripts/validate_lineage_decisions.py` | integrity check for curation overlay before export | `data/lineage/lineage_decisions.json` (required); `data/lineage/program_history_enrichment.json`, `public/data/programs.json`, `data/lineage/program_link_candidates.json` (all optional) | stdout validation report; exit 1 on ERROR findings |
| `scripts/bootstrap_source_enrichment_manifest.py` | one-time migration: merge phase2_test + remaining_batch into durable manifest | `data/official_context_manifest_phase2_test.json`, `_internal/workqueue_inputs/official_context_phase2_remaining_batch.json`, `public/data/official_resource_placements.json` | `data/source_enrichment_manifest.json` |
| `scripts/generate_content_map.js` | content/proofreading utility | `src/*`, `public/data/*` | stdout / `content_map.txt` |

## 7) Operational pipelines

### 7.1 Baseline site-data refresh pipeline
1. Upstream parser/change-tracking run in external catalog repo.
2. Run `build_site_data.py` with environment paths:
   - `WGU_REDDIT_PATH=/path/to/WGU_catalog/outputs`
   - `WGU_ATLAS_DATA=/path/to/wgu-atlas/data`
3. Commit refreshed `data/*` and `public/data/*` exports.

### 7.2 Program-enriched extraction pipeline
1. Ensure `public/data/programs.json` exists.
2. Run `extract_program_enriched.py` against 2026-03 catalog text and blocks.
3. Commit `public/data/program_enriched.json`.

### 7.3 Program-lineage pipeline (current stage model)
1. Stage 0 recall: `build_program_lineage_artifacts.py`.
2. Stage 1 semantic review (LLM/HITL) produces `program_lineage_events.json`.
3. Stage 1.5 curation overlay: `data/lineage/lineage_decisions.json`.
   - Human-reviewed decisions per event and program.
   - `display_state` overrides `site_worthy` at export time.
   - Survives pipeline reruns; must not be regenerated.
   - Validate before any export: `python3 scripts/validate_lineage_decisions.py`.
4. Stage 2 deterministic overlap: `compare_program_courses.py`.
5. Final deterministic transform: `generate_program_history_enrichment.py`.
6. Optional derivative: `generate_program_history_artifacts.py`.
7. Export (pending): `build_site_data.py` merges enrichment + decisions → `public/data/program_lineage.json`.

### 7.4 Incremental behavior
- `build_program_lineage_artifacts.py --baseline-end-edition YYYY-MM` emits only new boundaries/candidates where `end_edition > baseline`.
- Intended usage: full backfill once, then monthly incremental review.

## 8) Frontend data-consumption map

| Route/surface | Loader(s) | Artifact(s) |
|---|---|---|
| `/` | `getHomepageSummary`, `getSchools`, `getProgramsBySchool` | `public/data/homepage_summary.json`, hardcoded school lineage constants, `public/data/programs.json` |
| `/courses` | `getCourses`, `getAllCourseCodes` | `public/data/courses.json`, `data/canonical_courses.json` (code completeness check) |
| `/courses/[code]` | `getCourseDetail`, `getHeadingToProgramCode` | `public/data/courses/{code}.json` else `data/canonical_courses.json`; program heading map from `public/data/programs.json` |
| `/programs` | `getPrograms` | `public/data/programs.json` |
| `/programs/[code]` | `getProgramDetail`, `getProgramEnrichedByCode`, `getOfficialResourcePlacementsForSurface`, `getSchools` | `public/data/programs.json`, `public/data/program_enriched.json`, `public/data/official_resource_placements.json`, hardcoded school lineage constants |
| `/schools` | `getSchools`, `getProgramsBySchool`, `getCoursesBySchool` | hardcoded school lineage constants + `public/data/programs.json` + `public/data/courses.json` |
| `/schools/[slug]` | `getSchoolBySlug`, `getSchoolSlugByName`, `getProgramsBySchool`, `getCoursesBySchool`, `getHomepageSummary`, `getOfficialResourcePlacementsForSurface`, `groupProgramsByLevel` | same as above + `public/data/homepage_summary.json` + `public/data/official_resource_placements.json`; `groupProgramsByLevel` from `src/lib/programs.ts` |
| `/timeline` | `getEvents` | `public/data/events.json` |
| `/compare` | `getPrograms`, `getProgramEnriched` (pilot codes only), `PILOT_FAMILIES` | `public/data/programs.json`, `public/data/program_enriched.json` (5 pilot codes only serialized to client) |
| `/data` | `getHomepageSummary` | `public/data/homepage_summary.json`; links static download files in `public/data/downloads/` |
| `RelevantResources` component | `getOfficialResourcePlacementsForSurface` | `public/data/official_resource_placements.json` |

## 9) Build/deploy runbook
- Local dev: `npm run dev`.
- Local static build: `npm run build` (Next export to `out/`).
- Python scripts are regeneration tools only; committed JSON artifacts are sufficient for frontend build/export.
- GitHub Pages deploy:
  - workflow: `.github/workflows/deploy.yml`.
  - build env: `NEXT_PUBLIC_BASE_PATH=/wgu-atlas`.
  - deployed artifact: `out/`.

## 10) Known implementation gaps (factual)

<!-- Updated 2026-03-15: Session 1 fixes noted inline. -->

- Canonical-doc migration happened after initial repo setup; legacy docs are archived and reference cleanup remains ongoing.
- `build_site_data.py` does not generate `public/data/programs.json`, `public/data/program_enriched.json`, or `public/data/official_resource_placements.json`; those are currently produced by other/manual workflows and committed artifacts.
- `build_site_data.py` still keeps editorial/override logic in code (`CURATED_EVENTS`, `CANONICAL_TITLE_OVERRIDES`) instead of external data files.
- Program-history enrichment (`data/program_history_enrichment.json`) is generated but not yet consumed by current Next routes.
- `compare_program_courses.py` includes typo fallback from `program_lineage_events.json` to `program_ineage_events.json`.
- School lineage in site runtime is hardcoded in `src/lib/data.ts` constants, not generated from a dedicated artifact. A canonical slug lookup helper (`getSchoolSlugByName`) now exists, but the underlying constants remain hardcoded.
- `build_site_data.py` homepage summary uses `total_course_codes_ever: 1594` while canonical table currently has 1,646 rows (AP+cert); this is a known semantic/count mismatch across artifacts.
- `ProgramExplorer` school filter previously used "Health Professions" as a substring filter, which failed to match "Leavitt School of Health" (current canonical school name). Fixed 2026-03-15: filter now uses "Health".
- Course list rows still omit high-value surfaced fields already present in data (`canonical_cus` on detail artifacts, visible `stability_class` badges on list cards).
- `public/data/program_enriched.json` outcomes coverage is partial (74/114 programs populated; 40 empty outcomes arrays in current artifact).
- Regeneration pipeline depends on external upstream helper artifact `course_index_v10.json` (~59 MB), which is intentionally not committed in this repo.
- Known catalog/parser caveats from legacy trust docs:
  - `D627` title defect in source catalog authoring exists in archive history.
  - 2024-07 -> 2024-08 era boundary has known title truncation artifact patterns.
  - Index/body naming inconsistencies exist (program identity remains code/body anchored).
  - Archive has 3 missing early editions (`2017-02`, `2017-04`, `2017-06`).

## 11) Legacy-doc coverage map (all docs reviewed)
- Canonical docs (target state):
  - `docs/ATLAS_SPEC.md` -> implementation canon.
  - `docs/DECISIONS.md` -> policy canon.

- Archived legacy docs moved from `docs/` to `_internal/archive/2026-03-doc-consolidation/docs_legacy/`:
  - `README_INTERNAL.md` -> upstream parser/output schemas and trust basis -> this spec §4–§7 + `DECISIONS` parser guardrails.
  - `SCRAPE_LOG.md` -> scrape/parser chronology, bug history, trust notes -> this spec §7/§10 + `DECISIONS` trust rules.
  - `scraper_spec.md` -> scraper architecture summary -> this spec §4/§6/§7.
  - `program_lineage_artifacts.md` -> lineage artifact design + incremental mode -> this spec §4.2/§5.2/§7.3/§7.4.
  - `program-history-from-catalogs.md` -> stage narrative -> this spec §7.3.
  - `WEBSITE_SPEC.md` -> site architecture placeholder/spec draft -> this spec §3/§8/§9.
  - `website_design_plan.md` -> product UX direction and caveats -> `DECISIONS` product/provenance policy + this spec §8.

- Archived legacy docs in `_internal/archive/2026-03-doc-consolidation/`:
  - `CC_START_HERE.md` -> session bootstrap notes -> absorbed into this spec structure/runbook.
  - `DEV_LOG.md` -> implementation chronology and milestones -> this spec snapshot and known-gaps context.
  - `MIGRATION_HANDOFF.md` -> migration inventory and gotchas -> this spec topology/script/ops sections.
  - `PRODUCT_REVIEW_2026_03.md` -> product surfacing priorities -> `DECISIONS` product ordering + this spec/frontend/workqueue priorities.
  - `OFFICIAL_CONTEXT_LAYER_PLAN.md` -> official-context strategy, outcomes/video expansion -> this spec §4.3 + `DECISIONS` official-context/video rules.
  - `official_context/README.md` -> phase model -> this spec §4.3/§7.
  - `official_context/DEV_LOG.md` -> phase execution state -> this spec §2 snapshot.
  - `official_context/PHASE2_TEST_NOTES.md` -> validated page-type findings -> `DECISIONS` official-context attachment rules.
  - `official_context/REVIEW_QUEUE.md` -> manual review operations -> now encoded in `_internal/WORKQUEUE.md` A-02 rules.
- Active work surfaces retained:
  - `data/source_enrichment_manifest.json` — durable enrichment candidate manifest (all source families).
  - `_internal/SOURCE_ENRICHMENT_AUDIT.md` — master source enrichment audit and operating picture.
  - `_internal/youtube/` — YouTube workstream (raw, filtered, worklog).
- Historical transitional artifacts (data migrated, retained for reference):
  - `data/official_context_manifest_phase2_test.json` — 122 reviewed rows from original enrichment pass.
  - `_internal/workqueue_inputs/official_context_phase2_remaining_batch.json` — original 262-entry input queue.

## 12) Shared program helper library (`src/lib/programs.ts`)

Introduced in Degree Compare Session 1 (2026-03-15). Contains shared runtime helpers used across school pages and the compare feature.

### 12.1 Degree-level classifier
- `classifyDegreeLevel(program: ProgramRecord): DegreeLevel`
  - Classifies any program into a canonical `DegreeLevel` based on `canonical_name` prefix matching.
  - `DegreeLevel` union: `"Doctoral" | "Master's" | "Bachelor's" | "Associate" | "Certificates & Endorsements" | "Other"`.
  - "Other" catches certificates, post-master's specializations, and novel types not yet enumerated.
  - Prefix rules: `doctor`/`ph.d` → Doctoral; `master`/`m.b.a`/`mba` → Master's; `bachelor` → Bachelor's; `associate` → Associate; `endorsement`/`graduate certificate` → Certificates & Endorsements; else → Other.

### 12.2 Degree-level grouping
- `groupProgramsByLevel(programs: ProgramRecord[]): Record<string, ProgramRecord[]>`
  - Groups a program array by `DegreeLevel` in canonical display order (`DEGREE_LEVEL_ORDER`).
  - Each group is sorted alphabetically by `canonical_name`.
  - Extracted from `src/app/schools/[slug]/page.tsx`; now shared for school pages and compare-family scoping.

### 12.3 Roster compare helper
- `compareRosters(left: RosterCourse[], right: RosterCourse[]): CompareResult`
  - Compares two program rosters by exact course code (per DECISIONS §4.6).
  - No aliasing, fuzzy matching, or semantic linkage; exact code identity only.
  - Inputs: `ProgramEnriched.roster` arrays from `program_enriched.json`.
  - `CompareResult` fields:
    - `shared_codes`: codes in both rosters.
    - `left_only_codes`: codes only in left.
    - `right_only_codes`: codes only in right.
    - `left_count`, `right_count`, `shared_count`: integer counts.
    - `jaccard_overlap`: `shared / (left + right - shared)` — same metric semantics as `program_lineage_enriched.json`.
    - `left_retained_pct`: `shared / left_count`.
    - `right_inherited_pct`: `shared / right_count`.

### 12.4 School slug helper (in `src/lib/data.ts`)
- `getSchoolSlugByName(name: string): string | null`
  - Resolves any historical or current school name to its canonical slug using `SchoolRecord.historical_names`.
  - Returns `null` for unrecognized names.
  - Replaces ad-hoc `schoolNormMap` derivations in route files.
  - Canonical coverage: all names in `SCHOOL_RECORDS.historical_names` (8 historical/current names across 4 schools).

## 12B) Degree Compare family library (`src/lib/families.ts`)

Introduced in Degree Compare Session 2 (2026-03-15). Higher-level layer above `programs.ts` — family definitions and payload assembly.

### 12B.1 ProgramFamily type
- `id`: stable string identifier (e.g. `"bsswe-tracks"`).
- `label`: student-facing family name.
- `school`: canonical school key matching `ProgramRecord.school`.
- `degree_level`: `DegreeLevel` — all members share the same level.
- `program_codes`: string array of all member programs. V1 UI always renders 2-way pairs; the caller selects the pair from this list.
- `compare_note`: student-facing framing explaining why the comparison is useful.

### 12B.2 Pilot families (Session 2 curated set)
- `"bsswe-tracks"`: BSSWE, BSSWE_C — School of Technology / Bachelor's. 33/38 courses shared (Jaccard 0.80).
- `"msda-tracks"`: MSDADE, MSDADS, MSDADPE — School of Technology / Master's. 7/11 courses shared per pair (Jaccard 0.47). 3-member family; v1 renders 2-way pairs only.

### 12B.3 Family lookup helpers
- `getFamilyByCode(programCode: string): ProgramFamily | null` — returns the family containing the program code, or null.
- `getSiblingCodes(programCode: string): string[]` — returns all other program codes in the same family (compare targets for a program's page).
- `areProgramsComparable(codeA: string, codeB: string): boolean` — true if both codes belong to the same family.

### 12B.4 ComparePayload types
- `CompareProgramMeta`: `program_code`, `canonical_name`, `school`, `degree_level`, `total_cus`, `first_seen`, `course_count`.
- `CompareCourseEntry`: `code`, `title`, `cus`, `term_left: number | null`, `term_right: number | null`. Shared courses have both terms set (may differ); unique courses have one term null.
- `ComparePayload`: `family_id`, `left: CompareProgramMeta`, `right: CompareProgramMeta`, `shared_courses[]`, `left_only_courses[]`, `right_only_courses[]`, `metrics: CompareResult`.

### 12B.5 buildComparePayload
- `buildComparePayload(family, leftProgram, rightProgram, leftEnriched, rightEnriched): ComparePayload`
  - Assembles the full compare payload from two `ProgramRecord`s + their `ProgramEnriched` data.
  - Calls `compareRosters()` internally.
  - Sorts: shared by `term_left`; left-only by `term_left`; right-only by `term_right`.
  - Caller precondition: `areProgramsComparable(left.program_code, right.program_code) === true`.
  - Source: `ProgramEnriched.roster` from `public/data/program_enriched.json`.

## 13) Degree Compare frontend surfaces (Session 3 — 2026-03-16)

### 13.1 Compare page (`src/app/compare/page.tsx`)
- Route: `/compare` (static export, listed in primary nav).
- Server component. Loads `getPrograms()` and `getProgramEnriched()` at build time.
- Passes only pilot-family enriched data (5 programs) to the client component as props — full enriched map is not serialized to the client.
- Data-consumption map entry: `getPrograms()` + `getProgramEnriched()` (pilot codes only) + `PILOT_FAMILIES` from `src/lib/families.ts`.

### 13.2 CompareSelector (`src/components/compare/CompareSelector.tsx`)
- `"use client"` component. All selection state lives here.
- Receives: `programs: ProgramRecord[]`, `pilotEnriched: Record<string, ProgramEnriched>`.
- Filters eligible programs to ACTIVE programs in `PILOT_FAMILIES` only.
- School and degree-level filters narrow the program list dynamically.
- Two-step selection: Program A → Program B (B shows only family siblings of A).
- Calls `buildComparePayload()` in `useMemo` when both A and B are selected.
- States handled: empty, A-selected-awaiting-B, both-selected (shows CompareView), reset.

### 13.3 CompareView (`src/components/compare/CompareView.tsx`)
- Presentational component (no "use client" needed; bundled client-side via import tree).
- Receives: `ComparePayload`, `leftProgram: ProgramRecord`, `rightProgram: ProgramRecord`.
- Layout (Session 4 redesign):
  1. Program header cards (2-column): shows `index_name` as primary headline, `canonical_name` as subtitle when index_name is available. Code badge + Track A/B badge. School, level, CUs, first_seen, course_count. Left = blue-tinted, right = amber-tinted.
  2. Overlap summary: shared/left-only/right-only counts with track labels from `extractTrackLabel(index_name)`. Overlap bar (emerald/blue/amber), Jaccard %.
  3. Three-lane term timeline (replaces stacked tables): For each term, a full-width row with three columns — left-only courses | shared courses | right-only courses. Left column = blue background when non-empty; right = amber; center = neutral. Column headers: track label, course count, program code.
  4. Provenance footnote.
- Term-drift: shared courses where `term_left ≠ term_right` show a note "term N in [right code]" under the course title in the center column.
- Course codes linked to `/courses/[code]`.
- Desktop-first: three-lane layout is compact enough to read on desktop; not optimized for small screens.

### 13.4 Nav addition
- "Compare" added to `primaryLinks` in `src/components/layout/Nav.tsx`.
- DECISIONS §15.8 defers top-level nav; MVP overrides this for discoverability. Document as MVP decision pending Phase 4 review.

## 12C) Two-name model for program display (Session 4 — 2026-03-16)

Two name layers are maintained. Neither replaces the other. See DECISIONS §15.17 for normative rules and usage table.

### 12C.1 canonical_name
- Field: `ProgramRecord.canonical_name` from `public/data/programs.json`.
- Source: extracted from the body heading of the WGU catalog program block by the extraction pipeline.
- Used everywhere except compare disambiguation context.
- Unchanged by this session.

### 12C.2 index_name
- Field: `ProgramFamily.track_labels[programCode]` in `src/lib/families.ts`.
- Source: curated from `program_index_[date].json` in WGU_catalog trusted outputs (already generated by `parse_catalog_v11.py`; not yet forwarded by `build_site_data.py`).
- Used only in compare UI contexts: selector items, compact selection bar, program header cards, column headers.
- Access helpers:
  - `getIndexName(programCode: string): string | null` — returns the curated index name for a program, or null.
  - `extractTrackLabel(indexName: string | null): string | null` — extracts the parenthetical qualifier as a short label (e.g., `"Java Track"` from `"B.S. Software Engineering (Java Track)"`).
- Current curated values (2026-03 catalog):
  - BSSWE → `"B.S. Software Engineering (Java Track)"`
  - BSSWE_C → `"B.S. Software Engineering (C# Track)"`
  - MSDADE → `"M.S. Data Analytics (Data Engineering)"`
  - MSDADS → `"M.S. Data Analytics (Data Science)"`
  - MSDADPE → `"M.S. Data Analytics (Decision Process Engineering)"`

### 12C.3 Pipeline gap (index → atlas)
- `program_index_[date].json` is already generated by the upstream parser (in WGU_catalog trusted outputs) and contains distinguishing track names.
- `build_site_data.py` does not currently read this file; index names are not propagated into `programs.json`.
- Current workaround: curate track_labels manually in `src/lib/families.ts` per session.
- Future improvement: add `index_name` to `program_blocks_[date].json` at parse time (in `parse_catalog_v11.py`), then `build_site_data.py` gets it for free when reading blocks.

## 14) Canon maintenance rule
- Any new structural/process detail goes here.
- Any normative rule goes to `docs/DECISIONS.md`.
