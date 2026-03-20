# ATLAS Repo Memory

Last updated: 2026-03-20  
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

2. `docs/ATLAS_REPO_MEMORY.md`
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

### Experimental/prototype surfaces

- `/proto/courses`
- `/proto/compare`

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

- module initialized
- planning is substantially complete
- first bounded queue artifact still needed
- likely next major workstream after doc consolidation

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

## 14. Standalone-readiness reality

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

## 15. Deployment memory

### Key facts

- deploy target: GitHub Pages
- base path: `/wgu-atlas`
- deployment workflow lives under `.github/workflows/`
- static export assumptions are real, not incidental
- local dev and deployed path behavior differ via base-path handling

### Important rule

When making changes that affect asset paths, download links, or client-side fetches, check base-path correctness.

---

## 16. Durable decisions

These decisions are wrapped here as stable repo memory and should not be reopened casually.

### Product-level

- Atlas is a reference/explainer product, not a discussion/community product.
- Current catalog-backed navigation is primary.
- Official resources are the next major value layer after catalog facts.
- History/lineage is supporting context, not homepage identity.
- Reddit/community enrichment is deferred behind official-resource work.

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

## 17. Known high-value next opportunities

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

---

## 18. Fast orientation checklist

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

## 19. File and artifact routing cheatsheet

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
| How is deployment configured? | `next.config.ts`, `package.json`, `.github/workflows/` |

---

## 20. Memory discipline

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

## 21. Provenance and trust rules

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