# WORKQUEUE

Purpose: actionable backlog for items that are not canonical spec (`docs/ATLAS_SPEC.md`) and not durable policy (`docs/DECISIONS.md`).

Status legend:
- `now`: active/high-priority execution
- `next`: important, queued soon
- `later`: planned but intentionally deferred
- `blocked`: depends on external input/repo

Core direction:
- Atlas is shifting from archive-first presentation to student-useful navigation.
- History remains important only when it helps users understand the exact course/program/school they are viewing.
- For each page/section, ask:
  - does this help a student understand the current entity?
  - if historical, is it scoped and relevant?
  - if external, is there a clear attachment point?

Operating principle:
- The primary question is: `where on Atlas is this specifically relevant?`
- Not: `how do we surface more content generally?`

---

## A) Official Context (Web)

### A-01 Complete Phase 2 enrichment remainder
- Status: `now`
- Goal: enrich remaining sitemap high-value pages.
- Input: `_internal/workqueue_inputs/official_context_phase2_remaining_batch.json`
- Output: extend `data/official_context_manifest_phase2_test.json` (or successor consolidated enriched manifest)
- Notes: current docs indicate ~262 entries remained from partial run.
- Execution note: process in sub-batches of ~20-30 entries with durable writes after each batch (avoid one large run).

### A-02 Manual review + keep/prune pass
- Status: `now`
- Goal: finalize `keep/status/page_type/official_context_type` for enriched entries.
- Input: `data/official_context_manifest_phase1.csv`, `data/official_context_manifest_phase2_test.json`
- Review rules:
  - prune legal/utility/login/nav/contact pages unless directly entity-relevant
  - keep program pages, program guides, outcomes, specialization/track pages, and scoped accreditation pages
  - mark school-level vs program-level accreditation for attachment scope
  - do not trust URL path alone for page-type classification
- Acceptance:
  - `keep` and type fields set for all reviewed rows
  - notes explain ambiguous keep/no decisions

### A-03 Build deterministic placements generator
- Status: `next`
- Goal: generate `public/data/official_resource_placements.json` from enriched manifest + attachment rules.
- Reason: placements are currently committed artifacts without an in-repo deterministic generator.
- Acceptance:
  - program/school surfaces reproducible from source manifests
  - placement priority and group rules encoded in script

### A-04 Newsroom / press-release discovery pass
- Status: `next`
- Goal: add discovery beyond sitemap for underrepresented newsroom content.
- Inputs: wgu newsroom/press-release sources
- Output: merged inventory rows with provenance tags

### A-05 Taxonomy normalization pass
- Status: `next`
- Goal: normalize page-type and context-type vocab across phase1/phase2 artifacts.
- Acceptance:
  - controlled vocabulary list
  - no mixed synonym drift in final enriched manifest

---

## B) Official Video Layer

### B-01 Import official WGU YouTube inventory (raw manifest)
- Status: `next`
- Dependency: external file path from planning notes
- Goal: load raw inventory into Atlas data layer with source tag `official_wgu_youtube`.

### B-02 Import WGU Career Services YouTube inventory (raw manifest)
- Status: `next`
- Dependency: external file path from planning notes
- Goal: load raw inventory with source tag `official_wgu_careerservices_youtube`.

### B-03 Define shared video schema + validators
- Status: `next`
- Goal: canonical schema for both channels (`video_id`, `title`, `published_date`, `url`, `video_type`, `official_context_type`, candidates, status, notes, source).

### B-04 Run small enrichment/classification pilot
- Status: `next`
- Goal: classify a sample set and test attachment quality to program/school/course surfaces.

### B-05 Decide first page placements for videos
- Status: `later`
- Gate: after B-01..B-04 quality review.

---

## C) Discussion Layer (Reddit/Community)

### C-01 Define v1.1 discussion surface contract
- Status: `later`
- Goal: explicit data model and provenance labels for discussion links/summaries/freshness.
- Constraint: must remain clearly separate from catalog facts and official context.

### C-02 Build entity-to-discussion linking pass
- Status: `later`
- Goal: attach relevant discussion links to course/program pages with freshness metadata.

### C-03 Discussion summarization policy + guardrails
- Status: `later`
- Goal: implement cautious summary labels and source transparency before broad surfacing.

---

## D) Program History / Lineage Operations

### D-01 Wire final enrichment into program page runtime
- Status: `next`
- Goal: consume `data/program_history_enrichment.json` in `src/app/programs/[code]/page.tsx`.
- Current gap: file is generated but not rendered.

### D-02 Align heuristic `site_worthy` with reviewed curation set
- Status: `next`
- Goal: ensure display logic is driven by reviewed include/exclude decisions, not heuristic-only values.

### D-03 Stage 1 artifact naming hardening
- Status: `next`
- Goal: remove long-term reliance on typo fallback (`program_ineage_events.json`) once canonical input naming is stable.

### D-04 Incremental monthly runbook automation
- Status: `next`
- Goal: wrap lineage commands for monthly mode (`--baseline-end-edition`) into a single repeatable task.

---

## E) Site Data Pipeline Hardening

### E-01 Generate `public/data/programs.json` deterministically in-repo
- Status: `next`
- Goal: remove manual/provenance ambiguity for this core runtime file.

### E-02 Reconcile homepage summary count mismatch
- Status: `next`
- Issue: `homepage_summary.total_course_codes_ever` vs canonical table count mismatch.
- Goal: define intended metric and make consistent.

### E-03 Move schema-reference pointer from legacy doc to canon
- Status: `next`
- Current: some user-facing/schema-reference copy still points to legacy docs.
- Goal: point all field-reference copy to canonical docs (`docs/ATLAS_SPEC.md`).

### E-04 Externalize curated event editorial copy from script
- Status: `next`
- Goal: move hardcoded curated event text out of `scripts/build_site_data.py` into a data artifact.
- Reason: editorial updates should not require script edits.
- Candidate output:
  - `data/curated_events_editorial.json`

---

## F) Upstream/Extraction Backlog (Cross-Repo Dependent)

### F-01 Cross-edition Program Outcomes extraction
- Status: `blocked`
- Dependency: upstream parser/extraction repo.
- Goal: track outcomes changes over time, not just 2026-03 extraction.

### F-02 Cross-edition certificate tracking
- Status: `blocked`
- Dependency: upstream cert history extraction pipeline.
- Goal: longitudinal cert course/program history.

### F-03 Preserve term sequencing across editions
- Status: `blocked`
- Dependency: upstream extraction model updates.
- Goal: retain program term placement as first-class historical field.

### F-04 Instructor-directory integration decision
- Status: `later`
- Goal: decide whether instructor data is in Atlas scope and, if yes, define separate integration surface.

---

## G) Documentation Consolidation Follow-through

### G-01 Add deprecation banners to legacy docs
- Status: `next`
- Goal: make non-canonical docs self-identify as source material and point to canon.

### G-02 Legacy doc retirement checklist
- Status: `next`
- Goal: controlled archive/delete plan after bannering and verification.

### G-03 Keep canonical docs MECE
- Status: `ongoing`
- Rule:
  - implementation/process facts -> `docs/ATLAS_SPEC.md`
  - normative rules -> `docs/DECISIONS.md`
  - actionable backlog -> `_internal/WORKQUEUE.md`

---

## Quick candidates you explicitly asked about
- Official WGU web-resource enrichment: `A-01`..`A-05`
- YouTube channel ingestion/classification (WGU + Career Services): `B-01`..`B-05`
- Reddit/discussion linkage from Atlas pages: `C-01`..`C-03`

---

## H) Student-facing cleanup / positioning pass

### H-01 Homepage orientation rewrite
- Status: `now`
- Goal: replace archive-project framing in homepage hero/orientation band with student-useful framing.
- Current issue:
  - current copy emphasizes catalog archive/history framing.
  - product voice reads archive/reference first, student guide second.
- Source:
  - `src/app/page.tsx`
- Desired direction:
  - lead with helping students explore programs/courses/schools and relevant supporting resources.
  - keep catalog-history capability as secondary context.
  - avoid archive-first homepage identity.
- Acceptance:
  - lead copy is student-friendly.
  - history is framed as supporting context.
  - stat pills/attribution preserve provenance without dominating tone.

### H-02 Homepage section-order audit
- Status: `now`
- Goal: validate homepage module order against student priorities.
- Current structure:
  - New Programs
  - New Courses
  - Browse by School
  - Official WGU Resources
  - WGU Catalog History
- Questions:
  - should generic `Official WGU Resources` stay on homepage vs shift to entity-level attachments?
  - should `WGU Catalog History` preview stay/reduce/reframe as recent relevant changes?
- Acceptance:
  - module order justified by student relevance.
  - generic archive/timeline framing reduced where it competes with useful navigation.

### H-03 Global copy audit for archive-centric wording
- Status: `now`
- Goal: audit user-facing copy and rewrite toward student usefulness.
- Priority surfaces:
  - `/`
  - `/courses`
  - `/programs`
  - `/schools`
  - `/timeline`
  - `/methods`
  - `/data`
  - route metadata/descriptions
- Examples to review:
  - `tracked across the WGU catalog archive`
  - `active and retired, with catalog history for each`
  - `catalog history`
  - `deprecated`
  - `archive coverage`
  - `full timeline`
- Acceptance:
  - archive/history language remains only where it adds direct user meaning.
  - browse/search pages read as student-facing product pages.

### H-04 Metadata and SEO language cleanup
- Status: `next`
- Goal: revise page titles/meta descriptions to match student use cases and reduce archive/research tone.
- Priority routes:
  - `/courses`
  - `/programs`
  - `/schools`
  - `/timeline`
  - `/methods`
  - `/data`
  - dynamic course/program pages
- Acceptance:
  - metadata aligns with student intent.
  - history appears only where it improves search usefulness.

---

## I) Page-level relevance model for history

### I-01 Define history-as-supporting-context rule in implementation
- Status: `next`
- Goal: convert product direction into page-section implementation guidance.
- Principle:
  - history is useful when scoped to the current entity.
  - history should answer `what changed here?`, not narrate the full archive.
- Surfaces:
  - course pages
  - program pages
  - school pages
  - homepage recent/new modules
- Acceptance:
  - section-order guidance documented in `docs/ATLAS_SPEC.md`.
  - component/runtime queue items created where needed.

### I-02 Course page history cleanup
- Status: `next`
- Goal: review `/courses/[code]` history framing for practical student usefulness.
- Questions:
  - rename `Official Catalog History` to a more student-readable label?
  - which fields are genuinely useful vs archival noise?
  - should first/last seen be deemphasized relative to status, membership, and meaningful title/program changes?
- Acceptance:
  - history framing is practical and readable.
  - low-value archival phrasing reduced.

### I-03 Program page history cleanup
- Status: `now`
- Goal: make `/programs/[code]` context decision-supportive for current-degree evaluation.
- Current sections:
  - About This Program
  - Official Catalog History
  - Program Learning Outcomes
  - Version History
  - Course Roster
- Opportunity:
  - reframe historical sections toward recent meaningful changes.
  - wire in page-relevant Program History enrichment.
- Acceptance:
  - hierarchy remains current-program-first.
  - history is supporting context for the viewed degree.
  - archive-first tone removed.

### I-04 School page history cleanup
- Status: `next`
- Goal: keep school pages current-understanding-first, not archive-narration-first.
- Current headings:
  - School History
  - Recent Activity
  - Newest Programs
  - Recent Version Updates
  - Recent Course Additions
- Questions:
  - should `School History` be reframed/deemphasized?
  - should recent relevant changes be primary?
- Acceptance:
  - school pages prioritize current overview + recent relevant change context.

### I-05 Timeline page positioning review
- Status: `next`
- Goal: define timeline role in student-friendly Atlas posture.
- Issue:
  - timeline is archive-oriented and useful for explicit change-seeking users.
- Questions:
  - specialist destination vs broader site tone driver?
  - should homepage timeline teaser be reduced/reframed?
- Acceptance:
  - timeline remains available without defining overall product voice.

---

## J) Degree Compare feature workstream

Session model:
- Session 1 [2026-03-15]: canonical helper foundation — COMPLETE.
- Session 2 [2026-03-15]: pilot families, compare payload, v1 content contract — COMPLETE.
- Session 3 [2026-03-16]: standalone compare page MVP — COMPLETE.
- Session 4 [2026-03-16]: two-name model, index plumbing, layout redesign — COMPLETE.
- Session 5+ [TBD]: program-page affordances, advanced capabilities.

Policy for this feature: `docs/DECISIONS.md §15`.

### J-00 Session 1: Canonical helper and taxonomy foundation
- Status: `complete` (2026-03-15)
- What was done:
  - Created `src/lib/programs.ts` with:
    - `classifyDegreeLevel(program)` — canonical degree-level classifier from `canonical_name`.
    - `groupProgramsByLevel(programs)` — groups by level in canonical order; extracted from school page.
    - `compareRosters(left, right): CompareResult` — V1 compare contract using exact code identity (DECISIONS §4.6).
    - `DegreeLevel` type, `DEGREE_LEVEL_ORDER` constant, `CompareResult` interface.
  - Added `getSchoolSlugByName(name)` to `src/lib/data.ts` — resolves any historical/current school name to slug via `SchoolRecord.historical_names`.
  - Fixed school filter drift in `ProgramExplorer` (was: "Health Professions", matched nothing in current health school; now: "Health", matches "Leavitt School of Health" and historical names).
  - Replaced ad-hoc `schoolNormMap` in `src/app/schools/[slug]/page.tsx` with `getSchoolSlugByName()`.
  - Replaced local `groupProgramsByLevel` fn in school page with import from `src/lib/programs`.
  - Added Degree Compare section (§15) to `docs/DECISIONS.md` with phased rollout checklist.
  - Added §12 helper registry to `docs/ATLAS_SPEC.md`.

### J-01 Session 2: Pilot families, compare payload, v1 content contract
- Status: `complete` (2026-03-15)
- What was done:
  - Ran full roster comparisons across all candidate families to select pilots.
  - Selected primary pilot: BSSWE vs BSSWE_C (Jaccard 0.80; 33 shared, 5+3 unique).
  - Selected secondary pilot: MSDADE vs MSDADS (Jaccard 0.47; 7 shared, 4+4 unique).
  - Documented pilot compare reviews with full shared/unique course lists (see DECISIONS §15.14).
  - Confirmed v1 scope constraints: 2-way only, same school + same level, ACTIVE programs only.
  - Defined comparable-family qualification rules (DECISIONS §15.12): same school, same level, Jaccard ≥ 0.25, ≥ 2 unique per side, ACTIVE, curated affirmation.
  - Defined v1 content contract (DECISIONS §15.13): ComparePayload schema with all fields.
  - Created `src/lib/families.ts` with:
    - `ProgramFamily` type + `PILOT_FAMILIES` constant (bsswe-tracks, msda-tracks).
    - `CompareCourseEntry`, `CompareProgramMeta`, `ComparePayload` interfaces.
    - `getFamilyByCode()`, `getSiblingCodes()`, `areProgramsComparable()` helpers.
    - `buildComparePayload()` assembler function.
  - Updated DECISIONS.md §15 and ATLAS_SPEC.md §12B.

### J-02 Session 3: Standalone compare page MVP
- Status: `complete` (2026-03-16)
- What was done:
  - Chose standalone `/compare` route over inline program-page affordance — better fit for "sit down and choose two programs" user flow.
  - Created `src/app/compare/page.tsx` (server component, static export). Loads all programs + pilot enriched data (5 programs only). Passes to CompareSelector.
  - Created `src/components/compare/CompareSelector.tsx` (client component):
    - School + degree-level filters narrow the program list.
    - Step 1: pick Program A from eligible programs (ACTIVE, in pilot families).
    - Step 2: pick Program B — shows only family siblings of A.
    - Calls `buildComparePayload()` in useMemo when both selected.
    - States: empty, A-selected-awaiting-B (dashed prompt), both-selected (shows CompareView), reset.
  - Created `src/components/compare/CompareView.tsx` (presentational):
    - Program header cards (A=blue, B=amber) with code badge, name linked to program page, school, level, CUs, first_seen, course count.
    - Overlap bar: emerald=shared / blue=left-only / amber=right-only, proportional to union.
    - Shared course table with Term(A) and Term(B) columns; term-drift rows highlighted in yellow.
    - Left-only and right-only tables (Term | Code | Title | CUs). Course codes link to /courses/[code].
    - Provenance footnote: 2026-03 catalog, exact code identity, Atlas-derived.
  - Added "Compare" to primary nav (`Nav.tsx`) for MVP discoverability.
  - Build passes cleanly: `npm run build` ✓, 1852 static pages, /compare at 4.77 kB.
  - Updated ATLAS_SPEC.md §8 (data-consumption map) and §13 (new frontend surfaces section).
  - Updated DECISIONS.md Phase 3 status to complete + nav override rationale.
- Pilot comparisons verified at build time: BSSWE/BSSWE_C, MSDADE/MSDADS, MSDADE/MSDADPE, MSDADS/MSDADPE.
- Desktop-first: two-column selector works well on desktop; mobile layout is functional but not polished.

### J-04-session4 Session 4: Two-name model + layout redesign
- Status: `complete` (2026-03-16)
- What was done:
  - Investigated full pipeline for BSSWE/BSSWE_C naming. Confirmed: `program_index_2026_03.json` in WGU_catalog trusted outputs already has distinguishing track names. `build_site_data.py` does not forward them. Pipeline gap documented in ATLAS_SPEC §12C.3.
  - Added `track_labels?: Record<string, string>` to `ProgramFamily` in `src/lib/families.ts`. Curated index names for both pilot families (BSSWE/BSSWE_C, MSDADE/MSDADS/MSDADPE).
  - Added `index_name: string | null` to `CompareProgramMeta`; populated in `buildComparePayload` from `family.track_labels`.
  - Added `getIndexName(code)` and `extractTrackLabel(indexName)` helpers to `src/lib/families.ts`.
  - Updated `CompareSelector`: uses index names in program list items (index name primary, canonical name as subtitle); compact selection bar collapses selectors when both programs chosen; "Change" and "Reset" in compact bar.
  - Redesigned `CompareView`: term-aware three-lane layout (left-only | shared | right-only per term). Column headers show track label + course count + code. Term sub-headers divide the layout. Term-drift notes for shared courses where term placement differs.
  - Program header cards: index_name as primary, canonical_name as subtitle. "Program A/B" → "Track A/Track B".
  - Documented two-name model in DECISIONS §15.17 and ATLAS_SPEC §12C. Documented BSSWE_C outcomes gap in DECISIONS §15.17.
  - Build passes: `npm run build` ✓.

### J-03 Session 3: Standalone compare page MVP
- Status: `complete` (2026-03-16)
- See previous WORKQUEUE entry.

### J-05 Session 5: Program-page compare affordance (inline entry point)
- Status: `next`
- Goal: add compare affordances on individual program pages so users can enter compare directly from a program they're viewing.
- Scope: NO homepage changes. ONLY: /programs/[code] for family members.
- Steps:
  1. In `src/app/programs/[code]/page.tsx`:
     - Import `getFamilyByCode`, `getSiblingCodes` from `@/lib/families`.
     - Detect family membership; for family members, show a "Compare tracks" affordance in the header or after Course Roster.
     - Affordance: "Compare with [sibling name] →" link to `/compare?a=[code]&b=[sibling_code]`.
  2. On `/compare` page: read `?a` and `?b` URL params and pre-select both programs.
     - This requires CompareSelector to accept optional `initialA` / `initialB` props and pre-populate state.
  3. For non-family pages: no affordance.
- Acceptance:
  - BSSWE page has a visible "Compare tracks" link → /compare?a=BSSWE&b=BSSWE_C.
  - MSDADE page has 2 compare links (one per sibling).
  - /compare handles URL params and pre-populates the selection.
  - Non-family program pages unchanged.

### J-03 Visual diff UI
- Status: `next`
- Goal: student-readable visual comparison for similar programs.
- Direction:
  - Lead with shared count and overlap %.
  - List unique-to-left and unique-to-right courses clearly.
  - Maintain accessibility and clarity.
- Acceptance:
  - Pilot diff for SWE + MSDA families renders correctly.

### J-04 Standalone compare route (deferred)
- Status: `later`
- Goal: evaluate `/compare` standalone route after V1 inline version proves utility.

### J-05 Official-resource enrichment in compare mode (deferred)
- Status: `later`
- Goal: test whether compare views should include program-differentiated official resources.
- Gate: after V1 course-diff compare ships and proves useful.

---

## K) Official-context relevance and attachment expansion

### K-01 Replace generic homepage external-link dumping with relevance-first model
- Status: `now`
- Goal: decide if homepage `Official WGU Resources` is too generic.
- Current issue:
  - broad channel/community/support blocks may be weaker than entity-specific attachments.
- Questions:
  - keep vs shrink vs move (footer/global nav)?
  - prioritize richer entity-level contextual links?
- Acceptance:
  - explicit homepage external-link strategy implemented or queued.

### K-02 Article/link placement audit by entity type
- Status: `now`
- Goal: map useful official pages to exact Atlas surfaces.
- Entity targets:
  - program pages
  - school pages
  - selected course pages
  - optional event/timeline later
- Principle:
  - prioritize specific user relevance per entity.
- Acceptance:
  - placement opportunities tracked by entity/surface; broad non-specific placement reduced.

### K-03 Program-page official-resource expansion
- Status: `now`
- Goal: expand high-quality program-specific attachments.
- Priority resource types:
  - program guide
  - outcomes page
  - specialization page
  - accreditation page
  - rename/launch article when directly relevant
- Acceptance:
  - broader program coverage with strong relevance, minimal generic attachments.

### K-04 School-page official-resource model
- Status: `next`
- Goal: define school-page attachment behavior with clearer rules.
- Priority examples:
  - school-level accreditation
  - school-level context pages
  - school-relevant announcements
- Acceptance:
  - school surfaces use explicit model, not link dumping.

### K-05 Event/page-specific resource attachments
- Status: `later`
- Goal: evaluate high-relevance official source links on major event/timeline pages.
- Acceptance:
  - only pursued where relevance is strong and presentation remains restrained.

---

## L) Official video layer - relevance-first ingestion

### L-01 Keep video work tied to entity usefulness
- Status: `next`
- Goal: ensure video ingestion is placement/usefulness-driven, not feed-building.
- Applies to:
  - official WGU YouTube
  - WGU Career Services YouTube
- Acceptance:
  - video backlog references likely entity placements, not only raw manifest import.

### L-02 Program-page video pilot candidates
- Status: `next`
- Goal: identify degree pages where official video helps student understanding.
- Example classes:
  - field/domain explainers
  - track/specialization explainers
- Acceptance:
  - first-pass candidate placements identified.

### L-03 Course-page video pilot candidates
- Status: `later`
- Goal: identify small high-confidence set of course pages with tightly relevant official video.
- Acceptance:
  - small curated pilot only.

---

## M) Discussion layer - relevance-first future planning

### M-01 Entity-scoped discussion model
- Status: `later`
- Goal: ensure future discussion links/summaries attach only where useful to current entity.
- Principle:
  - discussion is contextual support, not site-wide feed content.
- Acceptance:
  - v1.1 discussion contract explicitly entity-scoped.

### M-02 Avoid generic community-link dominance
- Status: `next`
- Goal: reassess homepage community links under relevance-first model.
- Current issue:
  - global Reddit links may be less useful than entity-specific discussion attachments.
- Acceptance:
  - homepage community exposure is intentional and proportionate.

---

## N) Methods/Data page cleanup

### N-01 Methods page tone audit
- Status: `next`
- Goal: preserve trust/transparency while reducing parser/archive-research tone overload.
- Sections to review:
  - Archive Coverage
  - Parser Eras
  - Validation
  - Title Variant Classification
  - Key Caveats
  - Data Separation Policy
- Questions:
  - what remains public on page vs condensed with canon linkouts?
- Acceptance:
  - methods page remains trustworthy with tighter student-relevant framing.

### N-02 Data page wording cleanup
- Status: `next`
- Goal: keep `/data` transparent/useful without archive-heavy wording.
- Current issues:
  - archive-span phrasing dominance
  - schema note/text must consistently point to `docs/ATLAS_SPEC.md`
  - semantic mismatch around `total_course_codes_ever`
- Acceptance:
  - cleaner wording
  - canon docs referenced
  - count semantics clarified

### N-03 Public-facing terminology normalization
- Status: `next`
- Goal: normalize language:
  - retired vs deprecated
  - archive vs history
  - catalog history vs changes over time
  - current vs active
- Surfaces:
  - programs page
  - program detail
  - courses page
  - metadata
- Acceptance:
  - consistent student-readable terminology across surfaces.

---

## O) Immediate implementation targets from current content map

### O-01 Homepage `Official WGU Resources` section decision
- Status: `now`
- Goal: decide keep/shrink/move/refactor of generic resource block.
- Input:
  - current section in `src/app/page.tsx`
- Acceptance:
  - explicit decision recorded and implemented or queued.

### O-02 Homepage `WGU Catalog History` preview decision
- Status: `now`
- Goal: decide whether preview should become:
  - recent changes
  - notable updates
  - reduced specialist teaser
  - or remain unchanged
- Acceptance:
  - homepage preview aligns with student-facing posture.

### O-03 Program History runtime integration
- Status: `next`
- Goal: wire `data/program_history_enrichment.json` into program pages with current-entity relevance framing.
- Acceptance:
  - program pages show reviewed, page-relevant lineage/history context.

### O-04 Program comparison pilots
- Status: `next`
- Goal: validate pilot compare analyses for SWE Java vs C# and MSDA track family.
- See: `J-01` for full scope and acceptance criteria.
- Acceptance:
  - pilot analysis artifacts available before compare UI.

### O-05 Surface CUs on course browse surfaces
- Status: `next`
- Goal: expose credit units on course explorer/list surfaces (not only course detail).
- Input: `canonical_cus` from canonical/detail artifacts.
- Acceptance:
  - CU appears on student-facing browse rows/cards
  - no placeholder `—` CU cells on primary course lists.

### O-06 Surface stability badges on browse surfaces
- Status: `next`
- Goal: show `stability_class` as student-readable badges where users scan many courses.
- Acceptance:
  - badge text is plain-language
  - no filter/search regression.

### O-07 Improve `program_enriched.json` outcomes coverage
- Status: `next`
- Goal: reduce unmatched program outcomes in current artifact.
- Current state: 40/114 programs have empty `outcomes` arrays.
- Acceptance:
  - matching improvements documented
  - reduced unmatched count (or explicit unresolved reasons recorded).

### O-08 Add visible data-freshness indicators
- Status: `next`
- Goal: surface catalog/data vintage clearly on homepage, methods, and data pages.
- Input: `public/data/homepage_summary.json` (`data_date`).
- Acceptance:
  - freshness is visible without deep navigation
  - wording stays concise and provenance-safe.

---

## Canon sync tasks (required)

### CS-01 Update `docs/DECISIONS.md`
- Status: `next`
- Goal: strengthen rules for:
  - student-friendly/product-first positioning
  - history as supporting context to current entity
  - relevance-first attachment of official resources/videos/discussion
  - comparison features for related degree variants where useful

### CS-02 Update `docs/ATLAS_SPEC.md`
- Status: `next`
- Goal: add implementation notes for:
  - page-level relevance model
  - planned comparison/track-family capability
  - homepage cleanup targets
  - current content-map-driven cleanup hotspots
