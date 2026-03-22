# ATLAS Repo Memory

Last updated: 2026-03-21
Role: stable repo memory, runtime facts, durable decisions  
Use this file for repo orientation, architecture, contracts, and design rationale.  
This is the long-lived reference companion to `_internal/ATLAS_CONTROL.md`.

---

## 1. What this repo is

`wgu-atlas` is a static Next.js site that turns WGU catalog-derived data into a browsable reference product for students and operators.

Primary user value:

- browse degrees, courses, schools, and major timeline changes more easily than catalog PDFs
- see current catalog-backed facts first
- add selective supporting context where it improves navigation and understanding
- keep provenance boundaries clear between source-backed facts, Atlas interpretation, and future enrichment layers

Product posture:

- Atlas is a reference/explainer product, not a community/discussion product
- current catalog-backed navigation is primary
- official WGU resources are the next major context layer after catalog facts
- history/lineage is supporting context, not homepage identity
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
| `/` | entry point, search, school navigation, framing | core live |
| `/courses` | course browse and filtering | core live |
| `/courses/[code]` | course detail with historical/catalog context | core live |
| `/programs` | degree/program browse | core live |
| `/programs/[code]` | program detail with description, roster, outcomes, resources | core live |
| `/schools` | school index and orientation | core live |
| `/schools/[slug]` | school detail with programs/courses/history context | core live |
| `/compare` | bounded degree-comparison tool | supporting live |
| `/timeline` | catalog event/history browsing | supporting live |
| `/data` | downloadable datasets and schema-oriented transparency | supporting live |
| `/methods` | methodology, provenance, caveats | supporting live |
| `/about` | product framing and independence statement | supporting live |

### Page design reference

Current-state page docs, source-baseline analysis, screenshot readings, and homepage design-session conclusions are preserved in `_internal/page_designs/`. Key artifacts added 2026-03-20:

- `compare_page.md` — compare page visual/product reading; established Compare as a flagship homepage-proof surface
- `source_vs_atlas_program_entry.md` — before/after comparison (raw catalog vs Atlas BSCS); documents structural transformation argument
- `screenshot_analysis_log.md` — running log of screenshot-based visual readings
- `homepage_design_session_2026-03.md` — design session conclusions; strongest homepage framing is "Atlas turns a fragmented source into a structured student-use product"; degree pages and Compare are the two lead proof surfaces

See `_internal/page_designs/README.md` for reading order and maintenance notes.

---

### Experimental/prototype surfaces

- `/proto/courses` — course browse/filter UI variants
- `/proto/compare` — degree comparison layout variants
- `/proto/course-preview` — Session 2 enriched course-page cohort preview (10 courses)
  - Index: `/proto/course-preview`
  - Per-course: `/proto/course-preview/[code]` — C178, C480, C169, C165, D426, C170, C176, C824, D118, C216
  - Data loader: `src/lib/coursePreviewData.ts` (reads from `data/program_guides/` at build time)
  - Rendering component: `src/components/proto/CourseEnrichmentPreview.tsx`
  - Content map for review: `_internal/course_pages/content_maps/session2_cohort_preview.txt`
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

---

## 5. Top-level repo map

| Path | Role |
|---|---|
| `_internal/` | control-plane docs, module work logs, internal planning artifacts |
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
| homepage summary | `public/data/homepage_summary.json` | precomputed homepage statistics/modules |
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

### Guide-derived layers (live as of Sessions 29–35, refined Session 38 / Degree-page Session 2)

Program detail pages also consume per-program guide artifacts from `data/program_guides/degree_artifacts/`. These drive:
- `GuideProvenance` badge — source version, pub date, confidence, caveat pill
- `GuideCertBlock` — Licensure Preparation (blue) and Industry Certifications (emerald) blocks
- `GuideFamilyPanel` — Related Programs / track panel (violet)
- `GuideAreasOfStudy` — expandable course-group accordion with descriptions and competency bullets; course titles linked to `/courses/{code}` where a confident title match against the catalog roster exists
- `GuideCapstone` — capstone callout (amber)

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

Program pages should lead with current, useful catalog-backed student navigation. Historical/lineage context should support understanding, not dominate the page.

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

The official-resource layer is the next major context system after catalog facts.

Its job is to attach useful official WGU-authored or WGU-owned materials to existing Atlas entities without changing Atlas into a content-aggregation product.

### Current status

- module initialized and active
- first bounded regulatory/licensure queue artifact exists (`_internal/official_resource/regulatory_candidate_queue.md`)
- runtime placements already include selected regulatory/licensure resources in `public/data/official_resource_placements.json`
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
| `data/program_transition_universe.csv` | transition universe |
| `data/program_link_candidates.json` | candidate links |
| `data/program_lineage_enriched.json` | enriched pair/event layer |
| `data/program_history_enrichment.json` | program-history enrichment support |
| `scripts/validate_lineage_decisions.py` | validation gate |

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

Extract structured content from WGU program guide PDFs (115 guides, one per active program) and make it available as parsed runtime artifacts.

This is distinct from the URL-placement system in `official_resource_placements.json`. That layer already links guide URLs as sidebar resources. This system extracts the guide content itself.

### Status

**CLOSED OUT (Sessions 29–35).** Guide-derived content is live on Atlas degree pages. This section is a reference record.

- All 115 guidebooks parsed, validated, and built into degree artifacts. Parser stable.
- **`build_guide_artifacts.py` is built and run** — 115 per-program artifacts in `data/program_guides/degree_artifacts/`.
- **Guide data is live on degree pages** — Licensure Preparation block, Industry Certifications block, Family/track panel, Areas of Study, Capstone callout, Guide provenance badge, Caveat banners, Advisor-sequenced label.
- NCLEX-RN (BSPRN), Certified Public Accountant (CPA) Exam (MAcc family), and Praxis exam (8 education programs) extracted from program descriptions and live with correct licensure framing.
- 751 canonical courses have guide-derived enrichment data — descriptions, competency bullets, program context. Not yet on course pages.
- Human entry point: `data/program_guides/README.md`
- Canonical counts and claim boundaries: `data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.{md,json}` and `program_guide_claims_register.{md,json}`.
- Full product handoff: `_internal/program_guides/GUIDE_ARTIFACTS_PRODUCT_HANDOFF.md`.

**Remaining follow-ups (not active — non-blocking):**
- Cert review queue: 21 rows needing editorial judgment before surfacing.
- Prereq display on course pages: 50 auto-accepted relationships ready; course-page component not built.
- Multi-description/competency variant selection: 74/185 courses need a policy decision before course-page use.
- Education content-area sub-families: not captured as named families.

**Durable coverage model (do not collapse these states):**
- Extracted texts: PDF-to-text corpus available as parser input.
- Parsed guides: structural content extracted into `*_parsed.json` (canonical; do not regenerate without a parser fix).
- Validated guides: per-guide quality report in `*_validation.json` with confidence and anomaly counts.
- Course title matching: three-stage pipeline — original bridge → deterministic resolution → final merged state (`bridge/guides_merged/`). Final merged state is canonical.
- Course enrichment candidates: 751 courses in `data/program_guides/enrichment/course_enrichment_candidates.json`.
- Atlas site artifacts: not yet generated; pending the degree-enrichment artifact generator build.

### BSDA guide structure (confirmed)

Document order: title block → program description → boilerplate intro (CBE, accreditation, degree plan, faculty, orientation, transfer, SAP, courses, learning resources) → **Standard Path table** → Changes to Curriculum → **Areas of Study** (groups > courses > descriptions > competency bullets) → **Capstone** → closing boilerplate

Footer format (page break marker): `CODE YYYYMM © [copyright text] DATE PAGE`
- Yields: program_code, version, pub_date, page_count

Key structural facts:
- No course codes in guides — courses are title-only in both Standard Path and Areas of Study
- Standard Path rows: `[Title] [CUs] [Term]` — simpler than catalog rows
- Areas of Study: group heading → course title → description → "This course covers the following competencies:" → bullet list
- Capstone is a named section, last before closing boilerplate
- `"Accessibility and Accommodations"` is a reliable end-of-content marker

### Pipeline phases (planned)

| Phase | Purpose |
|---|---|
| A | Corpus manifest: scan all 115 guide texts, emit `guide_manifest.json` + `section_presence_matrix.csv` |
| B | Thin-slice parser: BSDA → `BSDA_parsed.json` + `BSDA_validation.json` |
| C | Full corpus parser with family branching |
| D | Site artifact build: `public/data/program_guides/{code}.json` |
| E | Course title → Atlas code matching (separate downstream step) |

### Validated families and guide counts
Current family-level completion and confidence distributions are execution-state facts and should be read from:
- `_internal/ATLAS_CONTROL.md` (current snapshot and next sequence)
- `data/program_guides/family_validation/` (gate and rollout summaries)
- `_internal/program_guides/DEV_NOTES.md` (session-level change log)

### Known source-artifact SP failures (SP unusable, AoS intact)

- BSITM, MATSPED, MSCSUG — column ordering failure in pdftotext extraction

### Known parser limitations (not source artifacts)

None outstanding. All identified limitations were resolved in Session 22–23.

### Parser changes log

| Session | Change | Scope |
|---------|--------|-------|
| 17 | `extract_metadata()` date regex fix (no-space before date) | General |
| 18 | `_is_bullet_continuation` Title Case guard (≥80% cap ratio → False) | General |
| 19 | `parse_capstone` KeyError fix — added `prerequisite_mentions` and `certification_prep_mentions` to capstone dict | General (capstone guides) |
| 22 | `SP_CHANGES_RE` conditional break — only breaks if table started (not BEFORE_TABLE) | General |
| 22 | `STANDARD_PATH_RE` second-table break — stops at second "Standard Path for..." heading after table start | General |
| 22 | `extract_title_and_description` Certificate Guidebook skip | General (PMC guides) |
| 23 | `looks_like_prose()` lowercase-start heuristic | General |
| 23 | `looks_like_prose()` continuation-particle end heuristic | General |
| 23 | `looks_like_prose()` prose-verb heuristic (`_PROSE_VERB_RE`) | General |
| 23 | `_is_bullet_continuation()` terminal-punctuation override (before Title Case guard) | General |
| 23 | `ACCESSIBILITY_RE` typo tolerance (`Accomm?odations`) | General |
| 23 | `extract_metadata()` combined-program `no_footer` suppression | General (combined guides) |
| 23 | `parse_standard_path_multiline()` "Advanced Standing" silent skip | General |

### Key files

- `_internal/program_guides/GUIDE_ARTIFACTS_PRODUCT_HANDOFF.md` — **product handoff doc** (Session 30): surface-by-surface payload reference, shape families, gaps, merge planning, concrete examples
- `_internal/program_guides/TECHNICAL_READOUT.md` — full design rationale, schemas, pipeline
- `_internal/program_guides/DEV_NOTES.md` — session history and parser change log
- `_internal/program_guides/README.md` — module orientation
- `data/program_guides/parsed/` — parser outputs (execution truth for parsed state)
- `data/program_guides/validation/` — per-guide validation outputs (execution truth for validated state)
- `data/program_guides/manifest_rows/` — per-guide manifest snapshots for corpus accounting
- `data/program_guides/family_validation/` — gate reports and rollout summaries
- `data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.{md,json}` — canonical post-close corpus truth
- `data/program_guides/audit/program_guide_claims_register.{md,json}` — approved/disallowed claims and safe wording
- `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` — implementation-ready Phase D decision document
- `data/program_guides/audit/phase_d_publish_policy.{md,json}` — publishability and caveat handling policy
- `data/program_guides/audit/phase_d_artifact_schema.{md,json}` — output shape and partial-use encoding
- `data/program_guides/audit/phase_d_degree_course_ownership_matrix.{md,json}` — degree/course ownership decisions
- `data/program_guides/audit/phase_d_build_plan.{md,json}` — implementation gates and checks
- `data/program_guides/cert_course_mapping.json` — cert→course mapping (9 auto-accepted, 21 review-needed)
- `data/program_guides/prereq_relationships.json` — prereq relationships (50 auto-accepted, 21 review-needed)
- `data/program_guides/sp_family_classification.json` — SP classification per program (A/B/C/D)
- `data/program_guides/sp_families.json` — 7 named family definitions
- `data/program_guides/guide_anomaly_registry.json` — 9 anomaly records with Atlas handling rules
- `data/program_guides/degree_level_cert_signals.json` — degree-level cert signals (NCLEX-RN, CPA Exam)
- `data/program_guides/degree_artifacts/` — **115 live per-program degree artifacts** (wired to degree pages)

### Important design decisions

- Manifest-first: characterize the full corpus before writing a content parser
- Course code matching is a separate phase, not part of structural parsing
- Guide family classification (standard_ug, education, endorsement, nursing, graduate, etc.) drives parser branching
- Reusable from `parse_catalog_v11.py`: footer-as-metadata pattern, section anchor scanning, state machine approach, typed anomaly collection, verbose progress reporting
- Not reusable: era detection, multi-edition loop, program index parsing, Total CUs as block terminator, sections_index / degree_snapshots structures

---

## 12b. Course-page enrichment system

### Purpose

Publish guide-derived content — descriptions, competency bullets, cert signals, prereq relationships, capstone signals — to `/courses/[code]` pages. This is the next major surface improvement after degree-page guide enrichment.

### Status

**Active — Session 1 planning complete (2026-03-21).** Starting artifact and design cohort created. No implementation started. Shape-disposition / display-policy artifact is the next required step before implementation planning.

### Available inputs (from closed program-guides workstream)

| Artifact | What it provides | Ready |
|---|---|---|
| `data/program_guides/enrichment/course_enrichment_candidates.json` | 751 courses with guide descriptions and competency bullets | yes |
| `data/program_guides/cert_course_mapping.json` | 9 auto-accepted cert→course mappings | yes |
| `data/program_guides/prereq_relationships.json` | 50 auto-accepted prereq relationships | yes |
| `data/program_guides/parsed/*_parsed.json` | full per-program guide content | yes (reference) |

### Coverage numbers

- 751 canonical courses have guide-derived enrichment data
- 730 with at least one description; 729 with at least one competency set
- 74 with multiple description variants; 185 with multiple competency variants
- 21 with zero descriptions (sparse)
- 9 cert mappings ready; 21 in review queue
- 50 prereq relationships ready; 16 cumulative-sequence nursing rows deferred

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

### Design conclusions (Sessions 1–2, closed out 2026-03-22)

The course-page design/prototype phase is complete. Key conclusions:

- The block/component system works. Most enrichment elements (cert, prereq, reverse-prereq, capstone, sparse fallback) are straightforward optional-display choices — show if present, omit if absent.
- The main remaining challenge is same-type multi-variant guide content (description or competency set with multiple guide-derived versions from different programs).
- Preferred direction: show one primary view by default; provide toggle/disclosure for alternate variants. Collapse only when variants are truly duplicate or cosmetic. Preserve materially distinct variants.
- Capstone display: use strong course-level evidence (title, catalog); do not foreground internal sourcing gaps to the reader.
- Cumulative-sequence prereqs: surface the structure honestly; do not flatten into a fake single-course prereq. Wording to be polished at implementation time.
- Prereq/description redundancy: display-order and wording cleanup at implementation time, not a structural blocker.

### Working area

- `_internal/course_pages/WORK_LOG.md` — full session history and conclusions
- `_internal/course_pages/content_maps/session2_cohort_preview.txt` — Session 2 content map
- Prototype surface: `src/app/proto/course-preview/` and `src/components/proto/CourseEnrichmentPreview.tsx`
- Implementation target (production, not yet modified): `src/app/courses/[code]/page.tsx`

### Important principle

Guide-derived content must be labeled with guide provenance (source, version/date). Catalog description remains authoritative; guide description is supplementary context. Never surface guide content without attribution.

---

## 13. Build and script pipeline

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

- Homepage is an active three-track workstream alongside Degrees and Courses.
- Homepage direction is proof-first: demonstrate Atlas value, not only navigation.
- Strongest proof surfaces so far are degree pages and Compare.
- Additional durable proof surfaces are course connectedness, history/change context, and relevant official resources.
- Ecosystem/community material is secondary to the core academic-reference story.
- Detailed visual analysis and route-level evidence remain local to `_internal/page_designs/`.

### Regeneration

Inputs: page component source + child components + `content_map.txt` section for the route + (optionally) live rendered text.

Regenerate when a page changes significantly enough that the existing artifact would mislead a designer.

### Artifact index

| Route | File | Status |
|---|---|---|
| `/` | `_internal/page_designs/homepage.md` | current (2026-03-20) |
| `/programs/[code]` | `_internal/page_designs/program_detail.md` | current (2026-03-20) — example: BSCS |
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
- Current catalog-backed navigation is primary.
- Official resources are the next major value layer after catalog facts.
- History/lineage is supporting context, not homepage identity.
- Reddit/community enrichment is deferred behind official-resource work.
- **Post-program-guides direction:** The project is now centered on three concurrent tracks:
  1. **Degrees** - immediate implementation target using completed guide data
  2. **Courses** - major follow-on opportunity with 751 enriched courses
  3. **Homepage** - active three-track workstream alongside Degrees and Courses

### Surface-level

- Program History is a program-page enrichment layer, not a standalone product.
- Homepage rethink is deferred until module priorities are clearer.
- Compare remains bounded V1 scope rather than expanding into a broad interpretation engine.
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

These are durable “good bets,” not automatic priorities.

### Very likely high-value

- official-resource regulatory/licensure/disclosure candidate queue
- outcomes/accreditation completeness pass
- surfacing course credit units in UI
- carefully expanding official-resource placements where attachment logic is strong

### Good but not automatic

- lineage export/UI on program pages
- broader official YouTube integration after attachment model hardens
- homepage framing revision after module priorities settle

### Explicitly not-now by default

- Reddit/community layer
- broad homepage redesign first
- continuity/lineage system sprawl
- compare-system expansion beyond current bounded purpose
- cleanup work without clear leverage

### WGU online ecosystem index

- `_internal/WGU_ONLINE_ECOSYSTEM_INDEX.md` inventories official WGU public channels, official student/community surfaces, unofficial Reddit/Facebook/Discord communities, external forums, review platforms, and the creator/media ecosystem
- used for internal research, curation, and future homepage/community/social exploration
- inclusion in the index does not imply product surfacing
- does not change the deferred status of Reddit/community integration

### Homepage / community / social — planning implications

Notes for when homepage or community work becomes active. Do not act on these now.

**Surface priority signal (from informal review):** degree pages are the strongest surface; compare is a major differentiator; Methods is too technical for most visitors; footer and Data sections are power-user territory. Homepage updates should lead with the surfaces that already work.

**Feature/section directions to hold:** a curated "feature teasers" section (showing what Atlas can do, not what WGU offers); an "Around WGU" section for official community/club/resource links; a clear official-vs-unofficial separation in any community or link-hub surface.

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
