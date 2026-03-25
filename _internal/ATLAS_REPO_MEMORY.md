# ATLAS Repo Memory

Last updated: 2026-03-22  
Role: stable repo memory, runtime facts, durable decisions  
Use this file for repo orientation, architecture, contracts, and design rationale.  
This is the long-lived reference companion to `_internal/ATLAS_CONTROL.md`.

---

## 1. What this repo is

`wgu-atlas` is a static Next.js academic reference and research surface that reorganizes WGU public degree, course, guide, and official-context material into a clearer system for curriculum inspection, program comparison, and catalog history.

Primary user value:

- research what a degree actually contains
- follow courses across programs
- compare related degrees by actual coursework
- inspect historical continuity and first-offered context
- use official context without hunting across multiple WGU surfaces
- keep provenance boundaries clear between source-backed facts, official attachments, and Atlas interpretation

Product posture:

- Atlas is a reference/explainer product, not a community/discussion product
- Atlas supports student research, not enrollment-funnel behavior
- current catalog-backed and guide-backed academic surfaces are primary
- curriculum structure is primary
- official WGU resources are the next major context layer after core academic facts
- history/lineage is supporting context, not homepage identity
- homepage identity is research-first, not generic browse-first
- WGU’s public site already provides many useful pieces; Atlas’s durable value is structural clarity and research usability
- simplicity, reproducibility, and low-maintenance updating are hard constraints

---

## 2. Minimal doc system

This repo is being compressed to a 3-document operating system:

1. `_internal/ATLAS_CONTROL.md`
   - active control surface
   - priorities, workstream state, blockers, next steps

2. `_internal/ATLAS_REPO_MEMORY.md`
   - stable repo memory
   - runtime architecture, data flow, contracts, durable decisions

3. `_internal/DEV_LOG.md`
   - terse reverse-chronological ledger
   - changes, decisions, touched files, next starting point

This file wraps the durable content that would otherwise be split across a spec doc and a decisions doc.

### Project-overview grounding set

- `_internal/project_overview/01_SITE_DESIGN_SPEC.md`
- `_internal/project_overview/02_SCOPE_AND_ACCOMPLISHMENTS.md`
- `_internal/project_overview/03_DATA_QUALITY_AND_VALIDATION.md`
- `_internal/project_overview/04_SCRAPING_CHALLENGES.md`

Role:

- current product/scope snapshot
- accomplishment and coverage claims
- validation/trust posture
- parser/scraping difficulty record

These are not control-plane canon, but they are now the primary long-form factual grounding set.

---

## 3. Live product surfaces

### Core public routes

- `/`
- `/courses`
- `/courses/[code]`
- `/programs`
- `/programs/[code]`
- `/schools`
- `/schools/[slug]`
- `/compare`
- `/timeline`
- `/data`
- `/methods`
- `/about`

### Surface roles

| Route | Role | Maturity |
|---|---|---|
| `/` | homepage / search / framing / research entry surface | core live |
| `/courses` | course browse and filtering | core live |
| `/courses/[code]` | course detail with catalog/history context and future guide-enrichment target | core live |
| `/programs` | degree/program browse | core live |
| `/programs/[code]` | guide-enriched degree detail with description, roster, outcomes, official resources, history context, cert/licensure handling, and course-linked Areas of Study | core live |
| `/schools` | school index and orientation | core live |
| `/schools/[slug]` | school detail with programs/courses/history context | core live |
| `/compare` | bounded degree-comparison tool; flagship differentiated comparison surface | flagship supporting live |
| `/timeline` | catalog event/history browsing | supporting live |
| `/data` | downloadable datasets and schema-oriented transparency | supporting live |
| `/methods` | methodology, provenance, caveats | supporting live |
| `/about` | product framing and independence statement | supporting live |

### Page design reference

Current-state page docs, source-baseline analysis, screenshot readings, and homepage design-session conclusions are preserved in `_internal/page_designs/`. Key artifacts:

- `homepage.md` — current-state visual inventory of `/`; the active "before redesign" baseline; documents `SchoolCards.tsx`, `Nav.tsx`, `Footer.tsx`
- `catalog_raw_analysis.md` — analysis of the raw WGU 2026-03 catalog PDF structure; the clearest articulation of what Atlas improves over (catalog splits degree information across three disconnected sections with no cross-referencing); grounding doc for the research-first homepage framing
- `compare_page.md` — compare page visual/product reading; established Compare as a flagship homepage-proof surface
- `source_vs_atlas_program_entry.md` — before/after comparison (raw catalog vs Atlas BSCS); documents structural transformation argument
- `screenshot_analysis_log.md` — running log of screenshot-based visual readings
- `homepage_design_session_2026-03.md` — earlier homepage design-session record
- `homepage_design_session_2026_03_22.md` — updated homepage strategy; Atlas is explicitly framed as a research surface for inspecting degree structure, following courses across programs, comparing actual coursework, and understanding catalog history
- `wgu_public_site_student_experience.md` — current official-site baseline and product-story input

Research-first positioning is now the locked homepage direction. Degree pages and Compare remain the two lead proof surfaces.

See `_internal/page_designs/README.md` for reading order and maintenance notes.

### Experimental/prototype surfaces

- `/proto/courses` — course browse/filter UI variants
- `/proto/compare` — degree comparison layout variants
- `/proto/course-preview` — Session 2 enriched course-page cohort preview (10 courses)
  - Index: `/proto/course-preview`
  - Per-course: `/proto/course-preview/[code]` — C178, C480, C169, C165, D426, C170, C176, C824, D118, C216
  - Data loader: `src/lib/coursePreviewData.ts` (reads from `data/program_guides/` at build time)
  - Rendering component: `src/components/proto/CourseEnrichmentPreview.tsx`
  - Content map for review: `_internal/course_pages/content_maps/session2_cohort_preview.txt`
  - Workstream status: design/prototype phase closed; implementation not yet started
- `/proto/degree-preview` — Degree-page Sessions 1–2 cohort review surface (7 programs; CLOSED workstream)
  - Index: `/proto/degree-preview`
  - Per-degree: `/proto/degree-preview/[code]` — BSCS, BSSWE, BSSESC, MATSPED, BSDA, MEDETID, BSITM
  - Data loader: `src/lib/degreePreviewData.ts` (cohort codes + shape metadata; uses production loaders)
  - Mirrors production `/programs/[code]` exactly; cohort-gated with proto banner
  - Content map: `_internal/degree_pages/content_maps/session1_degree_cohort_preview.txt`
  - Tracking: `_internal/degree_pages/WORK_LOG.md` — Sessions 1–2 complete

These are explicitly experimental and not the production UI.

---

## 4. Tech/runtime architecture

### Stack

- Next.js App Router
- React
- TypeScript
- Tailwind CSS
- static export deployment model
- GitHub Pages deployment under `/wgu-atlas`

### Runtime model

The site is a static-exported app that reads prebuilt JSON artifacts from `public/data/` and selected supporting artifacts from `data/`.

High-level pattern:

1. scripts generate or enrich artifacts
2. artifacts are committed into repo
3. runtime code loads those artifacts
4. pages render statically or with client-side filtering/searching over loaded data

### Deployment/path assumptions

- deployment target is GitHub Pages
- base path is `/wgu-atlas`
- client-side fetches and plain asset links must respect base path handling
- local development uses empty base path
- static export behavior is part of the repo’s operating assumptions

Important config facts:

- `next.config.ts` uses static export output
- images are configured for GitHub Pages compatibility
- GitHub Actions deploy with `NEXT_PUBLIC_BASE_PATH=/wgu-atlas`

### Upstream build dependency

Site data builds depend on a separate repo: `wgu-reddit` (specifically `WGU_catalog/outputs/`).

Key environment variables for running build scripts:
- `WGU_REDDIT_PATH` — path to `wgu-reddit/WGU_catalog/outputs/`
- `WGU_ATLAS_DATA` — path to this repo's `data/` directory (defaults to `../data` relative to scripts/)

Pre-generated artifacts are committed in `public/data/` and `data/`. Re-running build scripts is only needed when new catalog data has been processed in the `wgu-reddit` repo. A new maintainer cannot run a full data rebuild without the external repo present.

---

## 5. Top-level repo map

| Path | Role |
|---|---|
| `_internal/` | control-plane docs, module work logs, internal planning artifacts |
| `_internal/project_overview/` | current long-form product/scope/validation/challenges grounding set |
| `data/` | core build artifacts; subdirs: `data/site/`, `data/lineage/`, `data/enrichment/` |
| `public/data/` | runtime JSON artifacts consumed by site |
| `scripts/` | Python and JS generators/enrichment/build utilities |
| `src/` | Next.js app, components, runtime libraries |
| `screenshots/` | visual project captures (PNG snapshots of live pages) |
| `content_map.txt` | generated full-site content reference; regenerate with `generate_content_map.js` after major UI changes |
| `_internal/youtube/` | YouTube workstream notes and filtered title artifacts |
| `_internal/WGU_ONLINE_ECOSYSTEM_INDEX.md` | ecosystem reference map — official, unofficial, and external discussion/community/media surfaces related to WGU |
| `_internal/page_designs/` | text-based design reference artifacts for each live route — layout, content, visual tokens, interactions, functional inventory, planning observations |

---

## 6. Runtime data model

### Main runtime artifact families

| Artifact family | Location | Purpose |
|---|---|---|
| course cards/listing | `public/data/courses.json` | browse/filter cards for courses |
| course detail files | `public/data/courses/{code}.json` | rich detail files for active AP courses |
| canonical course table | `data/canonical_courses.json` / `.csv` | full canonical course intelligence and fallback source |
| programs | `public/data/programs.json` | core program metadata |
| program enrichment | `public/data/program_enriched.json` | descriptions, rosters, outcomes |
| events | `public/data/events.json` | timeline-ready event layer |
| homepage summary | `public/data/homepage_summary.json` | precomputed homepage statistics/modules for the current live homepage |
| search index | `public/data/search_index.json` | cross-entity search entries |
| official resource placements | `public/data/official_resource_placements.json` | curated official-resource attachment layer |
| named events / curated major events | `data/site/` and `public/data/` | event curation/build support |
| lineage artifacts | `data/lineage/` and `data/` | continuity/lineage analysis and enrichment |

### Runtime principle

The live app should prefer committed, deterministic, prebuilt artifacts over runtime computation or live external dependency.

---

## 7. Course data contract

### Two-tier course model

The site uses a two-tier course-detail system:

1. **rich individual detail files**
   - `public/data/courses/{code}.json`
   - used for active AP courses
   - currently 838 individual files

2. **canonical fallback**
   - `data/canonical_courses.json`
   - used for broader coverage, including retired/cert-only cases

This design preserves rich detail where available without losing whole-repo code coverage.

### Course coverage facts

- `public/data/courses/` contains 838 active individual course detail files
- `courses.json` contains ~1,646 course cards
- the wider code universe is larger than the rich-detail set
- retired/cert-only codes rely more heavily on canonical fallback behavior

### Course detail page inputs

Primary route:
- `src/app/courses/[code]/page.tsx`

Primary data sources:
- `public/data/courses/{code}.json`
- `data/canonical_courses.json` fallback
- `public/data/course_descriptions.json`
- related program data for relationship/context display

### Important course contract behavior

- individual detail files are the preferred source when present
- canonical fallback keeps non-rich-detail codes accessible
- runtime normalization exists for fields that may vary in shape
- course detail pages are designed to preserve catalog/history context without requiring all historical complexity to surface equally

### Important course insight

Credit units are already present in underlying course detail data (`canonical_cus` / equivalent surfaced CUs) and represent a high-value, low-effort UI enhancement opportunity.

---

## 8. Program data contract

Program pages are currently the strongest live research surface on the site.

### Core program layers

Program pages are built from multiple layers:

1. `public/data/programs.json`
   - core program record layer
   - codes, names, status, school/college associations, editions/history-oriented metadata

2. `public/data/program_enriched.json`
   - enriched layer
   - descriptions
   - rosters
   - learning outcomes

3. `public/data/official_resource_placements.json`
   - curated official resource attachments

### Program detail page

Primary route:
- `src/app/programs/[code]/page.tsx`

Program detail role:
- present current program identity
- show official description where available
- show grouped roster data
- show learning outcomes
- attach official resources when relevant

### Program enrichment facts

- `program_enriched.json` is the enriched support layer for active program detail pages
- roster entries are grouped by term and contain course references
- outcomes are an active production surface, not a placeholder concept
- learning outcomes already have dedicated rendering logic

### Guide-derived layers (live)

Program detail pages also consume per-program guide artifacts from `data/program_guides/degree_artifacts/`. These drive:
- `GuideProvenance` badge — source version, pub date, confidence, caveat pill
- `GuideCertBlock` — Licensure Preparation (blue) and Industry Certifications (emerald) blocks
- `GuideFamilyPanel` — Related Programs / track panel (violet); backed by `data/program_guides/sp_families.json` and `sp_family_classification.json`
- `GuideAreasOfStudy` — expandable course-group accordion with descriptions and competency bullets; course titles linked to `/courses/{code}` where a confident title match against the catalog roster exists
- `GuideCapstone` — capstone callout (amber)
- Caveat/degraded logic backed by `data/program_guides/guide_anomaly_registry.json` — 9 anomaly records with Atlas handling rules

### Guide pipeline artifacts — pending downstream use

These artifacts exist and are ready for course-page and cert-display work but are not yet wired into production:

| Artifact | Contents | Status |
|---|---|---|
| `data/program_guides/prereq_relationships.json` | 50 auto-accepted prereq relationships (high confidence, code-anchored); 21 review-needed rows | Ready for course-page prereq display |
| `data/program_guides/cert_course_mapping.json` | 9 auto-accepted cert→course mappings; 21 review-needed rows | Ready for cert badge display on course/degree pages |
| `data/program_guides/section_presence_matrix.csv` | Section coverage across all 115 guides | Reference for course-page enrichment quality assessment |

For full artifact inventory including review-needed row counts and issue types, see `_internal/program_guides/GUIDE_ARTIFACTS_PRODUCT_HANDOFF.md`.

**Current live section order (as of Degree-page Session 2, 2026-03-22):**
1. Breadcrumb
2. Header (code · status · CUs; H1; school; GuideProvenance badge)
3. Degraded quality warning block (amber callout — shown for low confidence or caveat-bearing artifacts; replaces inline chip)
4. About This Degree
5. Degree History
6. Program Learning Outcomes (or fallback placeholder if absent)
7. GuideCertBlock (licensure + industry certs)
8. GuideFamilyPanel (related programs)
9. GuideAreasOfStudy (moved above roster — richest guide content before the CU table)
10. Course Roster (normal) or Suppressed roster block
11. GuideCapstone
12. Capstone-in-AoS discovery hint (if capstone only accessible via AoS group)
13. Back link

**Key behavioral notes:**
- When `quality.caveat_messages_ui.length > 0`, the GuideProvenance caveat pill is suppressed and the degraded warning block (which shows all caveat messages) appears instead.
- `GuideCapstone` suppresses the "Part of a multi-course capstone sequence." note when caveats are present (the degraded block already covers it).
- Suppressed-roster programs (MATSPED): AoS appears above the suppressed block, which tells users to expand AoS groups for the complete course listing.
- Missing outcomes: renders a lightweight placeholder rather than silently omitting the section.

### Important program principle

Program pages should lead with current, useful catalog-backed and guide-backed student navigation. Historical/lineage context should support understanding, not dominate the page.

---

## 9. School data contract

### School/schools surfaces

Primary routes:
- `src/app/schools/page.tsx`
- `src/app/schools/[slug]/page.tsx`

Role:
- organize the program/course universe by college/school
- provide school-level orientation and browsing support
- preserve useful historical naming context where relevant

### School data behavior

School pages are assembled from:

- program records filtered by school/college
- course records filtered by college/school mappings
- homepage summary / recent change support data
- shared canonical school/college utilities

### Important school principle

School surfaces are navigation and orientation surfaces, not merely decorative category pages.

---

## 10. Search, browse, and compare systems

### Search

Primary component:
- `src/components/home/HomeSearch.tsx`

Primary artifact:
- `public/data/search_index.json`

Facts:
- search index is separate from `courses.json`
- search is cross-entity, not just course-list filtering
- search is client-side against prebuilt entries

### Course browse

Primary component:
- `src/components/courses/CourseExplorer.tsx`

Behavior:
- client-side filtering over prebuilt course cards
- no live API dependency
- filters include college/level/degree-oriented views

### Program browse

Primary component:
- `src/components/programs/ProgramExplorer.tsx`

Behavior:
- client-side filtering for programs
- search and classification utilities are shared through lib code

### Compare

Primary route/component system:
- `/compare`
- `src/components/compare/CompareSelector.tsx`
- `src/components/compare/CompareView.tsx`
- `src/lib/compareUtils.ts`
- `src/lib/families.ts`

Bounded scope facts:

- compare is a V1 bounded feature
- compare is also a flagship differentiated user-facing surface
- compares selected programs with course-roster overlap logic
- built around exact code matching, not fuzzy aliasing
- uses curated family logic / exclusions for sane pairings
- term-lane grouping powers the visual compare view
- not intended to sprawl into a broad lineage engine

Important compare principle:
- compare is a user-facing degree-roster comparison tool, not a general-purpose historical equivalency system

### Compare V1 constraints

Comparable family must satisfy all:
- 2-way comparison only
- same school, same degree level, active programs only
- human-curated as a real student choice
- pairwise Jaccard ≥ 0.25; each side contributes ≥ 2 unique courses

Core compare object: exact course roster from `program_enriched.json`. No aliasing or fuzzy matching.

### Two-name model

- `canonical_name`: from catalog body heading; use everywhere by default
- `index_name`: from WGU TOC/index; use only in compare UI (selector, column headers, header cards)

Current curated `index_name` values (stored in `src/lib/families.ts`):
- `BSSWE` → `B.S. Software Engineering (Java Track)`
- `BSSWE_C` → `B.S. Software Engineering (C# Track)`
- `MSDADE` → `M.S. Data Analytics (Data Engineering)`
- `MSDADS` → `M.S. Data Analytics (Data Science)`
- `MSDADPE` → `M.S. Data Analytics (Decision Process Engineering)`

Pipeline gap: `build_site_data.py` does not propagate `index_name` into `programs.json`; track labels are manually curated in `src/lib/families.ts`.

---

## 11. Official-resource system

### Purpose

The official-resource layer is the next major context system after catalog and guide-backed academic facts.

Its job is to attach useful official WGU-authored or WGU-owned materials to existing Atlas entities without changing Atlas into a content-aggregation product.

### Current status

- module initialized and active
- first bounded regulatory/licensure queue artifact exists (`_internal/official_resource/regulatory_candidate_queue.md`)
- runtime placements already include selected regulatory/licensure resources in `public/data/official_resource_placements.json`
- homepage redesign is the current primary product/design track; official-resource work remains the next major content-expansion layer
- broader attachment expansion and completeness auditing remain in progress

### Main runtime artifact

- `public/data/official_resource_placements.json`

This is the placement layer that lets pages attach curated resources in controlled locations.

### Current priority order

1. regulatory / licensure / disclosure
2. outcomes + accreditation completeness audit
3. specialization / track / variant resources
4. school governance / context
5. Official WGU YouTube
6. Career Services YouTube
7. selective program landing pages

### Important decisions

- official resources come before Reddit/community enrichment
- official-resource attachment should be narrow, curation-first, and provenance-clear
- YouTube is useful but should follow tighter attachment rules, not lead the system
- attachment quality matters more than volume

### Supporting workstream facts

- official context work extracted hundreds of sitemap entries
- enrichment/testing work already validated a phase-based workflow
- there is a substantial remaining batch queue for phase-2-style official context review
- YouTube source work identified two major official channel families with large candidate sets

### Existing research for outcomes/accreditation tier

`data/enrichment/outcomes/` contains curated research for the Tier 2 outcomes + accreditation pass:
- `README.md` — explains what WGU outcomes/accreditation pages exist and why they're high-value
- `outcomes_links.json` — curated entries for BSCS (ABET), BSCSIA (ABET + CAE-CDE), BSHIM (CAHIIM), Teachers College (CAEP), School of Business (ACBSP)
- Per-program subdirs (bscs/, bscsia/, caep/) with screenshots

This is the existing research foundation for the outcomes/accreditation completeness audit. Start here before running a new pass against the sitemap.

### Design principle

Official-resource work should strengthen existing program/school/course surfaces, not create a separate content universe.

### Source enrichment manifest

The durable enrichment candidate manifest is `data/enrichment/source_enrichment_manifest.json`.

Key field groups:
- `source_family`: `sitemap | youtube_official | youtube_cs | reddit`
- `candidate_type`: `program_guide | program_landing | specialization | accreditation | outcomes | school_context | youtube_video | other`
- `review_status`: `unreviewed | keep | skip | defer`
- `program_targets[]`, `school_targets[]`, `course_targets[]` — placement targets set at review time

Keep reasons: `core_program_context`, `variant_explainer`, `official_outcomes_context`, `school_context`, `accreditation_context`

Skip reasons: `marketing_only`, `duplicate_of_existing`, `too_generic`, `weak_student_value`, `not_surface_relevant`

### Official-resource review queue snapshot (as of 2026-03-18)

Sitemap:
- 262 unreviewed rows: 138 program landing pages, 123 specialization subpages, 1 accreditation (CAE-CDE)
- 109/114 active programs have live guide placements
- 6 programs missing guide placements: `BSNPLTR`, `BSPNTR`, `MASEMG`, `MEDETID`, `MEDETIDA`, `MEDETIDK12`

YouTube filtered candidates (no placements yet):
- Official WGU: 818 (after commencement/graduation filter from 1,535 raw)
- Career Services: 267 (after junk filter from 441 raw)
- Next pass: YT-1 school-level Official WGU

### Official-resource attachment rules

- Preferred density: 1–3 strong links per surface; do not dump full sitemap sets
- URL path alone is never sufficient for classification; evaluate page content
- `outcomes.html` and specialization/track subpages are higher-signal than guide-wrapper pages

---

## 12. Lineage / continuity / program history system

### Purpose

Lineage and continuity work exists to provide careful supporting context for program evolution. It is not the primary site identity.

### System state

- structurally real
- meaningful curation/validation work already completed
- safe to pause
- not automatically the next implementation track

### Important lineage artifacts

| Artifact | Role |
|---|---|
| `data/lineage/lineage_decisions.json` | curation/display authority |
| `data/lineage/program_transition_universe.csv` | transition universe |
| `data/lineage/program_link_candidates.json` | candidate links |
| `data/lineage/program_lineage_enriched.json` | enriched pair/event layer |
| `data/lineage/program_history_enrichment.json` | program-history enrichment support |
| `scripts/validate_lineage_decisions.py` | validation gate |

### Lineage build pipeline

The lineage data is built by a 5-stage pipeline. Run stages in order when lineage decisions change or a full rebuild is needed.

| Stage | Script | Output |
|---|---|---|
| 1 | `scripts/build_program_lineage_artifacts.py` | `data/lineage/program_transition_universe.csv`, `data/lineage/program_link_candidates.json` |
| 2 | `scripts/compare_program_courses.py` | `data/lineage/program_lineage_events_normalized.json`, `data/lineage/program_lineage_enriched.json` |
| 3 | `scripts/generate_program_history_artifacts.py` | `data/lineage/program_history.json` |
| 4 | `scripts/generate_program_history_enrichment.py` | `data/lineage/program_history_enrichment.json` |
| 5 | `scripts/add_program_history_enrichment.py` | merges enrichment into `program_history.json` |
| — | `scripts/validate_lineage_decisions.py` | validation gate; run after editing `lineage_decisions.json` |

Stages 1–2 depend on `WGU_REDDIT_PATH` (external repo). Stages 3–5 operate on artifacts already in this repo. For validation-only passes (after editing decisions without changing the transition universe), run `validate_lineage_decisions.py` alone.

### Key decisions

- lineage decisions are durable curation overlay
- suppressed/unresolved events do not surface by default
- zero-overlap approved cases require explicit rationale
- low-confidence approved cases require wording guards
- if a predecessor remains active, default toward pathway-variant logic rather than lineage
- Program History is a supporting enrichment layer, not a standalone product

### Unresolved lineage IDs still important to remember

- `PLE-012`
- `PLE-023`
- `PLE-028`

### Wording guard terms

Permitted: replaced, rebuilt, restructured, retitled, carried forward, redesigned

Forbidden: evolved from, descended from, builds on, updated version of, successor to (unqualified), continuation of, expanded, continuing within

Gap rule threshold: > 6 catalog editions between predecessor `last_seen` and successor `first_seen` → gap investigation required before lineage approval

### Additional unresolved lineage notes

- `PLE-015`, `PLE-026`: `wording_guard: true` with unconfirmed Jaccard values — verify pair metrics before export

### Pending export scope (when lineage is selected as next track)

- Add `export_program_lineage()` to `scripts/build_site_data.py` → `public/data/program_lineage.json`
- Extend `src/lib/types.ts` (ProgramRecord or new ProgramLineageRecord)
- Add `getProgramLineage(code)` to `src/lib/data.ts`
- Add Degree History section to `src/app/programs/[code]/page.tsx`
- Tentative output schema: `{ program_code, event_id, change_summary, from_programs, to_programs, transition_date }`

### Design principle

Lineage should help explain meaningful continuity when it exists, while resisting the temptation to overstate continuity.

---

## 12a. Program guide extraction system

### Purpose

Guide-derived academic enrichment for degree pages is now live. The guide corpus and derived outputs also preserve downstream inputs for future course-page enrichment and related academic-context work.

### Status

**CLOSED OUT.**

- 115/115 program guides parsed, validated, and artifacted
- 115 per-program degree artifacts live in `data/program_guides/degree_artifacts/`
- guide-derived content is live on degree pages
- 751 canonical courses have guide-derived enrichment data available for downstream course-page use

### Durable outputs

- degree artifacts
- cert mapping
- prereq relationships
- standard-path family classification
- anomaly registry
- degree-level cert signals
- audit manifests and claims/wording boundaries

### Live product use

Degree pages consume guide artifacts for:

- guide provenance and caveat handling
- Areas of Study
- licensure and industry certifications
- related-program/family panels
- capstone display
- degraded-quality warnings and partial-use behavior

### Remaining non-active follow-ups

- cert review queue: 21 rows needing editorial judgment before surfacing
- course-page prereq display: 50 auto-accepted relationships ready; production course-page component not built
- multi-variant course description/competency policy for downstream course pages
- education content-area sub-family refinements not captured as named families

### Key files

- `_internal/program_guides/GUIDE_ARTIFACTS_PRODUCT_HANDOFF.md`
- `_internal/program_guides/TECHNICAL_READOUT.md`
- `_internal/program_guides/DEV_NOTES.md`
- `data/program_guides/README.md`
- `data/program_guides/degree_artifacts/`
- `data/program_guides/enrichment/course_enrichment_candidates.json`
- `data/program_guides/cert_course_mapping.json`
- `data/program_guides/prereq_relationships.json`
- `data/program_guides/sp_family_classification.json`
- `data/program_guides/guide_anomaly_registry.json`
- `data/program_guides/degree_level_cert_signals.json`
- `data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.{md,json}`
- `data/program_guides/audit/program_guide_claims_register.{md,json}`

### Important design decisions

- manifest-first corpus understanding preceded parser hardening
- guide family classification drives parser branching
- course code matching is downstream from structural parsing, not part of it
- guide-derived content is supplementary academic context and must preserve provenance and caveat signaling

---

## 12b. Course-page enrichment system

### Purpose

Publish guide-derived content — descriptions, competency bullets, cert signals, prereq relationships, capstone signals, and related context — to `/courses/[code]` pages.

### Status

**READY, NOT ACTIVE.**

- design/prototype phase closed on 2026-03-22
- implementation path is known, but no production wiring has started
- next time this workstream is selected, begin from prototype conclusions and implementation targets rather than reopening core design questions

### Available inputs (from closed program-guides workstream)

| Artifact | What it provides | Ready |
|---|---|---|
| `data/program_guides/enrichment/course_enrichment_candidates.json` | 751 courses with guide descriptions and competency bullets | yes |
| `data/program_guides/cert_course_mapping.json` | 9 auto-accepted cert→course mappings | yes |
| `data/program_guides/prereq_relationships.json` | 50 auto-accepted prereq relationships | yes |
| `data/program_guides/parsed/*_parsed.json` | full per-program guide content | yes (reference) |

### Coverage numbers

- 751 canonical courses have guide-derived enrichment data
- 730 with at least one description
- 729 with at least one competency set
- 74 with multiple description variants
- 185 with multiple competency variants
- 21 with zero descriptions
- 9 cert mappings ready; 21 in review queue
- 50 prereq relationships ready
- 16 cumulative-sequence nursing rows deferred

### Course shapes (design-relevant)

| Shape | Key characteristic |
|---|---|
| Stable enriched | 1 description, 1 competency set |
| Meaningful multi-variant | 2–4 descriptions with real content difference |
| Cosmetic multi-variant | 2–4 descriptions differing only superficially |
| Cert-mapped | auto-accepted cert→course mapping present |
| Prereq-bearing | explicit course-to-course prereq |
| Reverse-prereq | this course is listed as prereq for downstream courses |
| Capstone | capstone signal from guide |
| Cumulative-sequence | nursing "all prior terms + code" prereq — not a standard prereq |
| Sparse | 0 descriptions and 0 competency sets |

### Design conclusions

- The block/component system works.
- Most enrichment elements (cert, prereq, reverse-prereq, capstone, sparse fallback) are straightforward optional-display choices.
- The main remaining challenge is same-type multi-variant guide content.
- Preferred direction: show one primary view by default; provide toggle/disclosure for alternate variants.
- Collapse only when variants are duplicate or cosmetic; preserve materially distinct variants.
- Capstone display should use strong course-level evidence and not foreground internal sourcing gaps.
- Cumulative-sequence prereqs should be surfaced honestly and not flattened into fake single-course prereqs.
- Prereq/description redundancy is an implementation cleanup issue, not a structural blocker.

### Stable implementation path

- build variant-toggle/disclosure UI for multi-variant guide content
- wire guide-derived content into the production course page
- add cert / prereq / reverse-prereq / capstone blocks
- handle cumulative-sequence wording carefully
- preserve guide provenance at the display level

### Working area

- `_internal/course_pages/WORK_LOG.md`
- `_internal/course_pages/content_maps/session2_cohort_preview.txt`
- prototype surface: `src/app/proto/course-preview/`
- prototype component: `src/components/proto/CourseEnrichmentPreview.tsx`
- production target: `src/app/courses/[code]/page.tsx`

### Important principle

Guide-derived content must be labeled with guide provenance (source, version/date). Catalog description remains authoritative; guide description is supplementary context. Never surface guide content without attribution.

### Multi-source overlap resolution pattern

Atlas has real overlap between catalog and guide descriptions: 571 courses with paired text, 106 programs with paired text, and variant corpora (74 courses with 2–4 guide description variants, 185 with 2–6 competency variants). The established workflow for resolving this:

1. Build deterministic comparison artifacts first — character-diff indexes with no LLM involvement.
2. Batch the materially-different subset into annotation-sized files.
3. Run bounded LLM annotation with explicit structured fields (`llm_difference_summary`, `llm_preference_for_research_tool`, `llm_review_flag`, etc.) — LLM as comparison aid, not policy-maker.
4. Synthesize batch evidence into an explicit block authority and display policy document.

This is the established pattern for any future overlap-heavy or variant-rich content decision. Do not let LLMs improvise policy directly on raw source corpora.

Resolution artifacts: `_internal/atlas_qa/COURSE_TEXT_COMPARISON_INDEX.md`, `_internal/atlas_qa/PROGRAM_TEXT_COMPARISON_INDEX.md`, `_internal/atlas_qa/BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md`, and `_internal/atlas_qa/course_text_comparison_batches/` (4 annotated batch files).

---

## 13. Atlas QA runtime system

### What it is

A local Python pipeline for answering structured natural-language questions about WGU
programs and courses. Runs entirely locally using Ollama (8B model). Not part of the
Next.js site build — a separate offline research and evaluation tool.

### Pipeline architecture

```
raw query
  → entity resolution (deterministic code/name lookup)
  → router (exact / fuzzy / compare / clarify path selection)
  → evidence bundle construction (corpus cards assembled deterministically)
  → answerability gate (deterministic rule checks before any LLM call)
  → constrained generation (LLM with strict prompt contract + JSON schema)
  → post-check (citation IDs + version token verification)
  → RuntimeQueryTrace output
```

All routing, scoping, and versioning is deterministic. The LLM is called only after the
gate clears. Output is validated structurally before emission.

### Python dependencies and venv

A `requirements.txt` exists at the repo root. Third-party deps:
- `pydantic>=2.0`
- `requests>=2.28`
- `rank-bm25>=0.2`
- `sentence-transformers>=2.0`
- `numpy>=1.24`

**Always use the `.venv` at the repo root, not system Python.** `pip install` to system
Python does not affect the venv, and the eval script will fail with import errors.

```
# Create venv (one-time):
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# Run tests:
PYTHONPATH=src .venv/bin/python -m pytest tests/atlas_qa/ -q

# Run full gold eval:
PYTHONPATH=src .venv/bin/python scripts/run_gold_eval.py --model llama3:latest
```

### Import convention

All internal imports use `from atlas_qa...` (not `from src.atlas_qa...`). The `src.`
prefix only works when CWD is in sys.path (pytest adds it; scripts do not). Any new
module added under `src/atlas_qa/` must follow the `from atlas_qa...` convention.

### Corpus cards

QA runtime reads from pre-built JSON cards in `data/atlas_qa/`:
- `program_version_cards.json` — one card per program per catalog version
- `course_cards.json` — one card per course
- `guide_section_cards.json` — parsed guide section artifacts
- `version_diff_cards.json` — inter-version diff artifacts (sparse; 2025-06 not yet built)

### Eval harness

`scripts/run_gold_eval.py` runs all 100 gold questions and writes a timestamped results
JSON to `data/atlas_qa/runtime_checks/gold_eval/`. Results are append-only artifacts —
do not delete or rename them.

Gold question set: `_internal/atlas_qa/QA_GOLD_QUESTION_SET.md` (100 questions, 7 classes A–G)

### Current eval baseline (run 4, 2026-03-25)

| Class | Rate | Gate | Status |
|-------|------|------|--------|
| A | 100% | 95% | PASS ✅ |
| B | 95.0% | 85% | PASS ✅ |
| C | 94.4% | 85% | PASS ✅ |
| D | 16.7% | 80% | FAIL (corpus gap — 2025-06 cards not built) |
| E | 100% | 90% | PASS ✅ |
| F | 93.3% | 98% | FAIL (1 regression from retry — being removed) |
| G | 100% | 100% | PASS ✅ |
| **Total** | **87%** | — | — |

### Durable design decisions

- Deterministic-first: all routing and scoping is deterministic; LLM is generation-only.
- No retry logic in the generation path — session 12 added one and it caused a regression (F-089). Retry was removed in session 12b.
- Postcheck has a narrow entity-code fallback for single-artifact bundles where `cited_evidence_ids` is empty but entity code appears in `answer_text`. Does not apply to multi-artifact (compare-path) bundles.
- Model: `llama3:latest` (8B Q4 via Ollama). Not fine-tuned. Selected for speed + accuracy on session 07 sample.
- Class D failures are a corpus gap (missing 2025-06 program version cards), not a pipeline bug. Deferred to session 13.

### Key files

| Need | File |
|------|------|
| Pipeline source | `src/atlas_qa/qa/` |
| LLM client | `src/atlas_qa/llm/client.py` |
| Eval runner | `scripts/run_gold_eval.py` |
| Tests | `tests/atlas_qa/` (274 passing) |
| Session specs / logs | `_internal/atlas_qa/work_sessions/` |
| Gold question set | `_internal/atlas_qa/QA_GOLD_QUESTION_SET.md` |
| Eval artifacts | `data/atlas_qa/runtime_checks/gold_eval/` |
| Block authority policy | `_internal/atlas_qa/BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md` |

---

## 14. Build and script pipeline

### Core site-data pipeline

The most important site-generation script is:

- `scripts/build_site_data.py`

This is the main deterministic build step for runtime-facing site data.

### Major script roles

| Script | Role | Classification |
|---|---|---|
| `build_site_data.py` | builds core site-ready artifacts | active core |
| `extract_program_enriched.py` | extracts program descriptions/rosters/outcomes | active supporting |
| `extract_course_descriptions.py` | extracts course descriptions | active supporting |
| `validate_lineage_decisions.py` | validates lineage curation overlay | active supporting |
| `build_program_lineage_artifacts.py` | lineage-stage artifact generation | active core for lineage pipeline |
| `compare_program_courses.py` | course-overlap comparison for lineage | active core for lineage pipeline |
| `generate_program_history_artifacts.py` | program-history transformation | active core for lineage pipeline |
| `generate_program_history_enrichment.py` | enrichment layer for history/site use | active core for lineage pipeline |
| `generate_content_map.js` | content-proofing / reference artifact generation | occasional utility |

### Important build principle

Site runtime should depend on committed artifacts, not hidden live preprocessing at request time.

---

## 14. Page design reference

Text-based design artifacts live in `_internal/page_designs/`. Each file covers one route and captures: layout (section-by-section, ASCII diagrams), all visible text, visual design tokens (colors, typography, spacing), interaction behavior, functional inventory, and design observations for planning.

### Purpose

These exist for design and planning work — not for code generation or spec enforcement. They answer "what is actually on this page right now?" without requiring a browser or a code read of every component.

### Durable design conclusions (repo-level)

- Homepage is now the primary active product/design track.
- Homepage framing is locked to a research-first posture.
- Atlas should be presented as a student research surface for curriculum inspection, degree comparison, course-connected navigation, and catalog history.
- Degree pages and Compare are the two co-anchor homepage proof surfaces.
- Course connectedness is best framed as following a course across programs.
- History/continuity is a real research differentiator.
- School navigation and broader ecosystem/community material are secondary to the academic research story.

### Regeneration

Inputs: page component source + child components + `content_map.txt` section for the route + (optionally) live rendered text.

Regenerate when a page changes significantly enough that the existing artifact would mislead a designer.

### Artifact index

| Route / Topic | File | Status |
|---|---|---|
| `/` | `_internal/page_designs/homepage.md` | current (2026-03-20) |
| `/programs/[code]` | `_internal/page_designs/program_detail.md` | current (2026-03-20) — example: BSCS |
| homepage strategy | `_internal/page_designs/homepage_design_session_2026_03_22.md` | current (2026-03-22) |
| official-site baseline | `_internal/page_designs/wgu_public_site_student_experience.md` | current |
| source reference | `_internal/page_designs/catalog_raw_analysis.md` | current (2026-03-20) — raw catalog UX analysis; Atlas value implications; homepage framing input |

See `_internal/page_designs/README.md` for generation instructions and full route-to-filename convention.

---

## 15. Standalone-readiness reality

### Current state

The repo is operationally standalone enough to run and maintain the current site, but not fully standalone for full historical regeneration.

### What is self-contained enough now

- current site runtime
- current committed data artifacts
- current Next.js app behavior
- public browsing surfaces
- official-resource placement runtime
- compare/search/browse runtime

### What is not fully self-contained

Some deeper regeneration history still depends on upstream archive/parser context that was not fully migrated into this repo.

Important gap categories:

- raw catalog archive
- parser-era source infrastructure
- some upstream path/data assumptions for regeneration work
- large-file historical inputs not fully carried into this repo

### Practical meaning

Maintain current site from committed artifacts: yes  
Fully rebuild every upstream-derived artifact from scratch using only this repo: not yet fully true

### Design implication

Avoid pretending the repo is more self-contained than it is. Document the boundary honestly.

### Known implementation gaps (factual)

These are repo boundaries or mismatches that matter for rebuild assumptions and maintenance.

- `build_site_data.py` does not generate `public/data/programs.json`, `public/data/program_enriched.json`, or `public/data/official_resource_placements.json` — those are produced by separate scripts and committed as artifacts
- `program_enriched.json` outcomes coverage is partial: 74/114 programs populated; 40 have empty outcomes arrays (2026-03 extraction)
- Full regeneration pipeline depends on non-committed upstream file `course_index_v10.json` (~59 MB)
- School lineage in runtime is hardcoded in `src/lib/data.ts` constants, not derived from a dedicated artifact
- Missing catalog editions: `2017-02`, `2017-04`, `2017-06`
- Homepage summary uses stale `total_course_codes_ever: 1594` vs actual canonical 1,646 rows

---

## 16. Deployment memory

### Key facts

- deploy target: GitHub Pages
- base path: `/wgu-atlas`
- deployment workflow lives under `.github/workflows/`
- static export assumptions are real, not incidental
- local dev and deployed path behavior differ via base-path handling

### Important rule

When making changes that affect asset paths, download links, or client-side fetches, check base-path correctness.

---

## 17. Durable decisions

These decisions are wrapped here as stable repo memory and should not be reopened casually.

### Product-level

- Atlas is a reference/explainer product, not a discussion/community product.
- Atlas supports student research into WGU degree structure.
- Current catalog-backed and guide-backed academic surfaces are primary.
- Official resources are the next major context layer after core academic facts.
- History/lineage is supporting context, not homepage identity.
- WGU’s public site already provides many useful pieces; Atlas’s durable advantage is structural clarity, curriculum-level comparison, and research usability.
- Reddit/community enrichment remains deferred behind official-resource work.

### Surface-level

- Degree pages are currently the strongest live research surface.
- Compare is a bounded but flagship differentiated surface.
- Homepage framing is locked to a research-first, curriculum-inspection posture.
- Degree pages and Compare are the two co-anchor homepage proof surfaces.
- Prototype routes are experimental and not production commitments.

### Data/runtime-level

- Prefer deterministic committed artifacts over runtime generation.
- Course detail uses a two-tier system: rich individual files plus canonical fallback.
- Search index remains a dedicated artifact separate from browse-card artifacts.
- Official resources should be attached through explicit placements, not ad hoc page scraping.

### Lineage/continuity-level

- Lineage decisions are a durable curation overlay.
- Suppressed/unresolved lineage events do not surface by default.
- Approved low-confidence lineage events require wording guards.
- Approved zero-overlap lineage events require explicit rationale.
- Pathway-variant logic should win over lineage when predecessor programs remain active.

---

## 18. Known high-value next opportunities

These are durable good bets, not automatic priorities.

### Very likely high-value

- homepage redesign implementation planning
- official-resource regulatory/licensure/disclosure candidate queue
- outcomes/accreditation completeness pass
- course-page enrichment production implementation when selected
- surfacing course credit units in UI

### Good but not automatic

- lineage export/UI on program pages
- broader official YouTube integration after attachment model hardens
- selective official-resource expansion where attachment logic is strong

### Explicitly not-now by default

- Reddit/community layer
- compare-system expansion beyond current bounded purpose
- continuity/lineage system sprawl
- broad social/community homepage integration
- cleanup work without clear leverage

### WGU online ecosystem index

- `_internal/WGU_ONLINE_ECOSYSTEM_INDEX.md` inventories official WGU public channels, official student/community surfaces, unofficial Reddit/Facebook/Discord communities, external forums, review platforms, and the creator/media ecosystem
- used for internal research, curation, and future homepage/community/social exploration
- inclusion in the index does not imply product surfacing
- does not change the deferred status of Reddit/community integration

### Homepage / community / social — planning implications

Notes for when homepage or community work becomes active. Do not act on these now.

**Surface priority signal:** degree pages are the strongest live research surface; Compare is the clearest differentiated comparison tool; course-connected navigation and history context are major supporting proofs. Homepage work should lead with these research tasks rather than generic site navigation.

**Feature/section directions to hold:** a curated feature-teasers section showing what Atlas can do, not what WGU offers; an "Around WGU" section for official community/club/resource links; a clear official-vs-unofficial separation in any community or link-hub surface.

**Things to avoid by default:** raw social feeds on homepage; a giant Reddit directory as a feature; mixing official and community without clear provenance signals.

**Club surfacing approach:** when clubs become a candidate surface, lean toward a compact card or sidebar pattern rather than a directory. Do not surface clubs that lack a stable, official, publicly accessible landing page.

**Club ecosystem structure:** WGU's club ecosystem is real (large scale, officially endorsed) but structurally fragmented — no unified hub, five separate discovery surfaces. Some clubs have proper public pages (Women in Tech, Cybersecurity Club, SHRM, AMA); others are officially referenced but under-surfaced (Data Club, Military Alliance Club, Alumni Cybersecurity Club). Surface the well-paged clubs first; hold under-surfaced ones until a public landing page exists.

**External benchmark:** Western Hemisphere University / WHU-style compact club listings are the clearest external design precedent for integrating club/community context into an academic reference product without overwhelming the primary catalog-navigation purpose.

**Raw catalog baseline:** `_internal/page_designs/catalog_raw_analysis.md` documents exactly what the raw WGU catalog gives a student (flat table, no outcomes inline, no descriptions inline, no history, no compare, no links). Use this when writing homepage copy or feature framing — Atlas's value is most legible against the catalog baseline.

---

## 19. Fast orientation checklist

When returning to the repo after time away:

1. read `_internal/ATLAS_CONTROL.md`
2. scan the most recent entries in `_internal/DEV_LOG.md`
3. use this file to answer architecture/data/runtime questions
4. verify whether the task is:
   - control-plane
   - runtime/UI
   - script/data build
   - official-resource
   - lineage/continuity
5. prefer the smallest bounded step that reduces a real blocker

---

## 20. File and artifact routing cheatsheet

| Question | Start here |
|---|---|
| What should we do next? | `_internal/ATLAS_CONTROL.md` |
| What changed recently? | `_internal/DEV_LOG.md` |
| What is the current product/site scope? | `_internal/project_overview/01_SITE_DESIGN_SPEC.md` |
| What has Atlas actually built? | `_internal/project_overview/02_SCOPE_AND_ACCOMPLISHMENTS.md` |
| What supports trust/validation claims? | `_internal/project_overview/03_DATA_QUALITY_AND_VALIDATION.md` |
| What were the main scraping/parsing challenges? | `_internal/project_overview/04_SCRAPING_CHALLENGES.md` |
| What is the current homepage strategy? | `_internal/page_designs/homepage_design_session_2026_03_22.md` |
| How does the live app load data? | `src/lib/data.ts` and this doc |
| Where do course/program artifacts live? | `public/data/` and `data/` |
| Where do build artifacts come from? | `scripts/` |
| Where is compare logic? | `src/components/compare/`, `src/lib/compareUtils.ts`, `src/lib/families.ts` |
| Where do official resources attach? | `public/data/official_resource_placements.json` and `_internal/official_resource/` |
| Where does lineage live? | `data/lineage/` plus related lineage artifacts in `data/` |
| Where does course-page enrichment planning live? | `_internal/course_pages/` |
| Where is the guide enrichment data for course pages? | `data/program_guides/enrichment/`, `cert_course_mapping.json`, `prereq_relationships.json` |
| How is deployment configured? | `next.config.ts`, `package.json`, `.github/workflows/` |
| What does a specific page look/do? | `_internal/page_designs/{route}.md` |

---

## 21. Memory discipline

This document should stay:

- factual
- stable
- dense
- non-chatty
- useful after long gaps

Do not turn it into:

- a session log
- a broad planning memo
- a speculative roadmap
- a duplicate of control-state tables better kept in `_internal/ATLAS_CONTROL.md`

Update this file when one of these changes:

- runtime architecture
- artifact contracts
- durable design decisions
- build/deploy behavior
- major workstream meaning or boundaries

---

## 22. Provenance and trust rules

Four distinct information categories — keep visibly separate at all times:

1. Official catalog facts (source-authoritative)
2. Official WGU resources (WGU-authored/owned, curated by Atlas)
3. Student/community discussion (future; explicitly deferred)
4. Atlas interpretation (clearly attributable to Atlas, not source)

Do not present Atlas summaries as source-authored text. Observed vs interpreted distinction applies especially in timeline and history contexts.

### YouTube policy

- Keep Official WGU YouTube and Career Services YouTube separate
- Do not broadly surface videos until import/classification/placement model is stable
- Career Services content: only include when it explains domain/field/role context; exclude generic job-search content

### Outcomes/assessment policy

- Outcomes and pass-rate assets are official-context enrichment, not catalog fact layer
- Do not overstate program/time-window metrics as global pass rates; lower pass rate is descriptive, not causal
- Keep source page URL, asset URL, and extraction status for every metric

### Timeline and lineage separation

Timeline events (`public/data/events.json`) and program-lineage events are separate systems with separate recall logic. Do not merge or conflate them.


## 18a. Doc freshness note (2026-03-24)

This is not a cleanup pass. The purpose of this note is only to preserve what appears current vs. stale across older module docs that are still on disk.

### Current trust posture

When current-state questions arise, prefer:
1. on-disk runtime/data artifacts
2. `_internal/ATLAS_CONTROL.md`
3. `_internal/ATLAS_REPO_MEMORY.md`
4. `_internal/DEV_LOG.md`
5. `_internal/project_overview/` grounding docs
6. module docs / older READMEs / page-design notes

### Docs reviewed recently that appear stale or partially stale

- `_internal/program_guides/README.md`
  - **stale / historical only**
  - still describes the guide workstream as initialized, analysis-phase, not yet implemented
  - superseded by the completed guide pipeline, built artifacts, and live degree-page wiring

- `_internal/program_guides/PROGRAM_GUIDE_PROJECT_STATUS.md`
  - **partly stale**
  - closed-out summary is still useful
  - `What Is Next` section is overtaken by later work; degree-enrichment artifact generator and degree-page wiring are already complete
  - use for historical closeout and artifact map, not for current next-step sequencing

- `_internal/page_designs/README.md`
  - **useful as folder orientation/history, not final status**
  - broad homepage framing is still aligned with current direction
  - workflow/status notes are partly stale, especially references that public-site baseline work was still in progress before homepage decisions could be locked

- `_internal/page_designs/program_detail.md`
  - **stale / archived**
  - pre-guide-wiring page inventory
  - do not use as current program-page reference

### Docs reviewed recently that appear current and still useful

- `_internal/atlas_qa/PROGRAM_TEXT_COMPARISON_INDEX.md`
  - current/useful as a field-level source comparison artifact for program descriptions
  - not a display-policy doc, but still valid provenance/comparison evidence

- `_internal/atlas_qa/COURSE_TEXT_COMPARISON_INDEX.md`
  - current/useful as a field-level source comparison artifact for course descriptions
  - especially important for overlap/variant reasoning

- `_internal/atlas_qa/BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md`
  - current/useful
  - primary source-authority/display-policy artifact for catalog vs guide overlap decisions

- `_internal/atlas_qa/INITIAL_ATLAS_QA_FOUNDATION_STATE.md`
  - current/useful for Atlas QA workspace/runtime-boundary facts
  - not a page/product status doc; use for Atlas QA dependency/runtime assumptions

### Main-doc status note

- `_internal/ATLAS_CONTROL.md`
  - current control-surface canon; trust for priorities, workstream state, blockers, and next-session order

- `_internal/ATLAS_REPO_MEMORY.md`
  - current durable-memory canon overall
  - however, individual reference sections inside this file can lag and should be corrected opportunistically during normal work
  - known example: page-design references may mention docs that are now archived/stale (for example `program_detail.md`)

### Practical rule
(for now)
Do not run cleanup just to normalize older docs. Instead:
- preserve this note as the current memory of what is stale vs. still useful
- when touching a workstream anyway, update only the references that would otherwise mislead execution
- prefer newer project-overview docs and control-plane canon over older module orientation docs when they disagree