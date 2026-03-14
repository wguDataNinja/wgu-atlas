# WGU Atlas — Site Design Plan

**Site name:** WGU Atlas
**Subtitle:** Explore courses, programs, catalog changes, and student discussion
**Creator:** WGU-DataNinja
**Public repo:** `wgu-atlas` (separate from the internal `wgu-reddit` research repo)

*Design reference for the WGU Atlas public-facing catalog history and course/program intelligence site*

---

## 1. Purpose

This document defines the design plan for a website built from the validated WGU public catalog archive and the related WGU Reddit course-discussion dataset.

The site should present information clearly, responsibly, and usefully. It should help users understand:

- what courses and programs exist now
- what changed over time
- when major historical events happened
- how official catalog history relates to ongoing student discussion

The site should not feel like a raw data browser. It should feel like a trustworthy, explorable public reference.

---

## 2. Project framing

### What this site is

A **public catalog history and course/program intelligence site** for WGU.

It combines:

- official public catalog history
- validated course/program extraction
- historical change tracking
- major event interpretation
- discussion context from Reddit where useful

### What this site is not

- not an official WGU site
- not a complete internal institutional system
- not a guarantee of exact implementation timing for students
- not a claim that course-code changes always imply learning-experience changes
- not a Reddit site with a catalog sidebar

### Positioning statement

**WGU Atlas** is framed as:

> A student-usable public reference built on research-grade historical catalog data.

That captures both accessibility and rigor. The name "Atlas" reflects what the site does: it maps a territory — courses, programs, schools, history, and the student conversation that surrounds them — across time.

---

## 3. Current project state

### Archive
- **108 public catalog editions** on disk
- Coverage: **2017-01 through 2026-03**
- Missing: **2017-02, 2017-04, 2017-06**
  - likely unpublished based on the public WGU catalog page

### Parser
- active parser: `parse_catalog_v11.py`
- full archive run:
  - **0 skipped editions**
  - **0 body-parse anomalies**
- two confirmed structural eras:
  - **ERA_A:** `2017-01` through `2024-07`
  - **ERA_B:** `2024-08` through `2026-03`

### Validation
- trusted reference edition: **2026-03**
- 2026-03 validated deeply after an initial incomplete scrape was corrected
- targeted validation across **14 structurally critical editions**
- result: **14/14 clean**

### Current historical outputs
- `course_history.csv`
- `program_history.csv`
- `adjacent_diffs.json`
- `adjacent_diffs_summary.csv`
- `summary_stats.json`
- `edition_diffs_full.json`
- `edition_diffs_summary.csv`
- `edition_diffs_rollups.json`
- `edition_diffs_events.json`

### Current counts
- 2026-03 AP codes: **838**
- 2026-03 cert codes: **52**
- 2026-03 total current codes: **890**
- archive-wide unique course codes: **1,594**

### Major historical capability now available
The project can already surface and narrate:
- rename-cleanup events
- structural program-family rebuilds
- specialization splits
- version-only review waves
- school rename history
- certificate formalization
- large expansion months
- course/title/CU changes

---

## 4. Site goals

The site should answer five kinds of questions.

### A. Current truth
- What is this course now?
- What is this program now?
- Which school is this under now?
- Is this code active or retired?

### B. Entity history
- When did this course first appear?
- When was it last seen?
- What titles has it had?
- Which programs used it?
- When did this program version change?

### C. Change over time
- What changed between two editions?
- Was this a minor update or a major restructuring?
- Which schools/programs were affected?

### D. Major historical moments
- When did the schools change names?
- When did certificates become a first-class structure?
- When were the largest expansion/rebuild waves?

### E. Discussion context
- Is there active recent discussion about this course?
- Does existing discussion predate major catalog change?
- What are the recurring student discussion themes for this course?

---

## 5. Audience strategy

## Recommendation

Build a **layered public product**, not separate products for different audiences.

Do **not** force users to choose:
- student
- institution
- researcher

Instead, make one site with progressive depth.

### Surface layer
For most users:
- search
- drilldown
- current snapshot
- course and program pages
- major events
- recent discussion context

### Deep layer
For researchers, reviewers, and institutional users:
- transition explorer
- methods
- downloadable data
- validation
- inference/confidence details

### Why this is right
A student-only framing would underuse the dataset.
An institution-only framing would make the site too abstract.
A layered design lets the same underlying facts serve multiple audiences without duplication.

---

## 6. Product principles

### 1. Search first
Most users will arrive wanting to find:
- a course
- a program
- a school

Search and drilldown must be primary.

### 2. History should be understandable
Do not make raw diffs the main experience.

Use:
- current truth
- timelines
- named events
- curated summaries

### 3. Keep three information types separate
This is a hard design rule that applies everywhere on the site, not only on course pages.

Always separate:

- **Official catalog facts** — sourced from the WGU public catalog archive
- **Discussion signals** — sourced from Reddit and other public student discussion spaces
- **LLM-generated summaries** — clearly labeled, dated, and attributed to the generation process

These three categories must be visually, textually, and structurally distinct. They should never appear in the same paragraph or appear to blend together. This is central to the site's trust proposition.

Student discussion is a **real, planned product feature** of WGU Atlas, not a speculative future possibility. It is deliberately secondary to official catalog history, but it is intended from the start. Pages that surface Reddit discussion should be designed with the separation rule in place from day one, not patched in later.

### 4. Distinguish observation from inference
Every page and data model should respect:
- observed fact
- inferred relationship
- confidence

### 5. Public usefulness over dashboard clutter
The site should feel useful, not like an analytics console.

---

## 7. Top-level site architecture

### Recommended navigation
- **Home**
- **Courses**
- **Programs**
- **Timeline**
- **Methods**
- **Data**

Possible later additions:
- **Transitions**
- **Discussion**
- **Guides**

---

## 8. Homepage design

The homepage should do four jobs:

1. **Search**
2. **Orient**
3. **Surface what’s new**
4. **Connect to discussion**

## Homepage wireframe

### Section 1: Header / search
Primary entry surface.

Include:
- course search
- program search
- clickable school/college cards

Examples:
- “Search by course code or title”
- “Search programs”
- school cards:
  - Business
  - Health
  - Technology
  - Education

This is the top user-control layer.

---

### Section 2: Intro / orientation band
Very short.

Include:
- one-paragraph explanation of the site
- what archive it covers
- what it helps users do
- one sentence on what makes it different:
  - official public catalog history
  - course/program lookup
  - discussion context

Optional:
- mini school-lineage preview or era summary

Do not let this section get long.

---

### Section 3: Activity and current-state modules
Dashboard-style but curated.

**Committed entry modules for v1:**
- **Newest programs** — programs added in the most recent editions
- **Programs with recent version updates** — programs whose curriculum version stamp changed recently
- **Recently changed courses** — courses added or removed in recent transitions
- **Recent major catalog changes** — links to curated events from the Timeline

**Planned for v1.1+ (requires Reddit integration):**
- **Courses with active recent discussion**
- **Courses where discussion may be outdated after catalog change**

All modules derive from `homepage_summary.json`, which is already built and populated.

### Important rule
Keep this to about **4–6 compact modules**.
Do not let the homepage become a cluttered dashboard.

---

### Section 4: Timeline preview
A short preview of major historical moments.

Show:
- 3–5 major events
- event title
- date
- one-sentence summary
- link to full timeline

This establishes historical depth immediately.

---

### Section 5: Discussion preview
A planned discussion layer on the homepage (v1.1+).

Intended modules:
- recently discussed courses
- courses with active recent discussion
- courses whose main discussion predates a major change event

This must not become a Reddit feed.
It must stay course-centered and curated.
Each discussion signal must be clearly separated from official catalog facts.

This section will be empty or omitted in v1 until the Reddit integration layer is built.

---

### Section 6: Around the WGU web
A persistent utility module.

This should not be the hero, but it is useful.

Break into labeled groups:

#### Official WGU channels
- official website
- official YouTube
- Career Services YouTube
- Instagram
- TikTok
- official Facebook presence

#### Community discussion spaces
- top subreddits
- notable Facebook groups if appropriate

#### Career / support channels
- links to career support resources where appropriate

### Important note
Clearly separate:
- official
- unofficial community
- student discussion spaces

Do not flatten them into one undifferentiated list.

---

### Section 7: Footer
Include:
- methods
- data
- caveats
- archive scope
- version/date of site data

---

## 9. Course explorer

### Purpose
Allow users to search and browse course entities.

### Features
- search by course code
- search by title
- fuzzy search
- filters:
  - active / retired
  - AP / certificate / both
  - school
  - current / historical
  - recently changed
  - has discussion / no discussion

### Result card fields
- course code
- canonical title
- active / retired
- first seen / last seen
- current contexts
- current program count
- recent discussion count if available

---

## 10. Course page design

This should be the flagship feature.

## Course page structure

### Section A: Official catalog history
Observed facts only.

Include:
- course code
- canonical current title
- active / retired
- first seen
- last seen
- contexts seen:
  - academic programs
  - certificates
  - both
- current programs
- historical program count
- title history
- CU history
- major related events

### Section B: Discussion signals
Not summaries yet; just signals.

Include:
- total linked Reddit posts
- recent linked posts
- discussion recency
- discussion activity trend if available
- warnings such as:
  - discussion predates major change
  - title changed after main discussion period
  - code retired after main discussion period

### Section C: Student discussion summary
LLM-generated and clearly labeled as such.

Possible elements:
- common pain points
- recurring advice themes
- recurring confusion points
- current themes
- “what students seem to struggle with”
- “what may be outdated”

### Section D: Related entities
- current and historical programs
- possible predecessor/successor relationships
- related events
- related discussion

### Hard separation rule
Use explicit headings like:
- **Official catalog history**
- **Discussion signals**
- **Student discussion summary**

This is critical for trust.

### LLM guide requirements
If a generated course guide exists, show:
- last generated date
- source post count
- source time window
- note that it is based on public student discussion and is not official guidance

---

## 11. Program explorer

### Purpose
Allow users to search and browse programs.

### Features
- search by program name
- search by school
- filters:
  - active / retired
  - degree family
  - school
  - recently updated
  - recently changed
  - licensure / non-licensure if derivable

### Result card fields
- program name
- school
- active / retired
- first seen / last seen
- current version
- change intensity summary

---

## 12. Program page design

## Program page structure

### Section A: Official catalog history
Include:
- canonical program name
- school
- active / retired
- first seen
- last seen
- current version
- observed name variants
- school lineage
- version history
- current course count

### Section B: Change summary
- number of version changes
- periods of highest churn
- notable events
- active vs retired courses in lineage
- current / historical certificate relationships if applicable

### Section C: Course roster over time
- summary of adds/removes
- major structural changes
- expandable detailed matrix / heatmap

### Section D: Related discussion
Later, possibly:
- most discussed courses in the program
- discussion concentrated before/after change events

---

## 13. Timeline page

This should be the second flagship feature.

## Purpose
Present major historical change in understandable form.

### Default experience
Curated major events, not all 107 transitions equally.

### Core elements
- major event cards
- filters by:
  - year
  - school
  - event type
  - severity

### Card fields
- date range
- event title
- event type
- affected schools
- key counts
- one-sentence summary
- link to detail view

### Event detail view
Should include:
- observed changes
- interpreted summary
- affected programs
- affected courses
- version changes
- evidence excerpts or tables
- confidence/caveat notes

### Era summaries
Add short summaries above or between event groups, such as:
- early code/cleanup era
- rename transition era
- modern catalog structure era
- certificate formalization era
- expansion wave era

This prevents the timeline from feeling like a pile of adjacent transitions.

---

## 14. Methods page

This page is essential.

## Purpose
Explain why the site is trustworthy and what its limits are.

### Must include
- archive coverage
- parser eras
- validation approach
- the 696 → 838 correction story
- targeted breakpoint validation
- D627 anomaly example
- observed vs inferred framework
- publication date vs implementation date
- catalog history vs student experience
- Reddit limitations
- public archive completeness caveat

### Why include the 696 → 838 story
It is a strong trust-building example.
It shows:
- the project did not simply trust its own parser
- validation changed conclusions
- the current counts are hard-won

### Methods page tone
Clear and credible, not defensive.

---

## 15. Data page

### Purpose
Serve deeper users.

### Include
- downloadable datasets
- schema notes
- data version/date
- release notes or change log
- explanation of what each file is for

Possible files exposed:
- canonical course table
- canonical program table
- named event layer
- lineage snapshots
- summary exports
- possibly site-ready JSONs for transparency

---

## 16. Future: Transitions explorer

### Purpose
Let advanced users inspect any adjacent edition pair.

### Use cases
- researchers
- reviewers
- institutional users
- deep dives

### Why later
It is valuable, but not the clearest first public proof.

---

## 17. Visual design plan

## Priority visuals

### 1. Annotated major-events timeline
**Most important visual**

Show:
- date
- event title
- event type
- severity band
- affected schools
- one-line interpretation

This should anchor the Timeline page and likely appear in preview form on the homepage.

---

### 2. Course lifecycle timeline
**Primary course-page visual**

Show:
- first seen
- title changes
- CU changes
- active/retired period
- major events intersecting the course lifecycle

This is likely the strongest single student-facing visual.

---

### 3. School / college lineage timeline
**High-value orientation visual**

Built from `college_snapshots.json`.

Show:
- school/college rename transitions
- certificate formalization appearance
- possible ERA_A / ERA_B shading

This is ideal for the homepage and/or an archive overview page.

---

### 4. Program history matrix / heatmap
**Advanced program-page visual**

Use on one program at a time.

Suggested layout:
- x-axis = program courses
- y-axis = editions / time
- green = added
- red = removed
- neutral = present
- optional overlays = version bump, title change, CU change

This directly supports the “full degree history” concept.

---

### 5. Churn / change-intensity charts
**Supporting summary visuals**

Show:
- change intensity by school
- version activity by school
- program churn over time
- event count by year

Use neutral framing.
Do not imply that change is inherently negative.

---

## Possible later visuals

- successor/predecessor flow diagrams
- current vs historical program-membership map for a course
- certificate-to-degree overlap visuals
- discussion-over-time aligned to course/event timeline
- era-wise event-type distribution

---

## 18. Required core data products before build

## 1. Canonical course intelligence table
Highest priority.

Suggested fields:
- `course_code`
- `canonical_title_current`
- `observed_titles`
- `first_seen_edition`
- `last_seen_edition`
- `active_current`
- `contexts_seen`
- `current_programs`
- `historical_programs`
- `historical_program_count`
- `title_variant_class`
- `ghost_flag`
- `discussion_count`
- `discussion_last_seen`
- `notes_confidence`

---

## 2. Canonical program intelligence table
Second priority.

Suggested fields:
- `program_id`
- `canonical_program_name`
- `observed_name_variants`
- `school_lineage`
- `first_seen_edition`
- `last_seen_edition`
- `active_current`
- `versions_seen`
- `version_change_count`
- `course_count_by_edition`
- `change_intensity_summary`
- `identity_confidence`
- `discussion_coverage` if later desired
- `notes`

---

## 3. Named event layer
Third priority.

Suggested fields:
- `event_id`
- `start_edition`
- `end_edition`
- `event_title`
- `event_type_primary`
- `event_type_secondary`
- `severity_score`
- `affected_schools`
- `affected_programs`
- `affected_courses`
- `observed_summary`
- `interpreted_summary`
- `confidence`
- `is_curated_major_event`

---

## 4. Title variant classification
Very important for trust.

Classes:
- formatting only
- punctuation only
- extraction noise
- wording refinement
- substantive title change
- unresolved

---

## 5. Certificate integration
Needed early for complete current truth.

Track:
- AP only
- certificate only
- both
- transitions between contexts

---

## 6. Successor / predecessor inference layer
Later, after canonicalization.

Should support:
- multiple candidates
- evidence fields
- confidence
- no forced one-to-one assumptions

---

## 19. Trust and caveat design

## Core UI rule
The site must make it easy to distinguish:

- **Observed**
- **Inferred**
- **Confidence level**

### Global lightweight framing
A reusable “How to read this” panel:
- based on public WGU catalog archive
- catalogs reflect official published structure
- timing may not equal exact student implementation
- inferred relationships are labeled as inference

### Per-claim labeling
For interpretive content, show:
- Observed
- Inferred
- High confidence
- Moderate confidence
- Tentative

### Visual treatment
Examples:
- solid connectors = observed continuity
- dashed connectors = inferred possible successor
- badges for uncertain or one-off entities

---

## 20. Key limitations to communicate

### 1. Catalog date is not implementation date
The catalog reflects publication, not guaranteed student rollout timing.

### 2. Catalog presence is not lived experience
An official structure does not perfectly capture actual student pathways or exposure.

### 3. Reddit is not representative
It is useful supplementary context, not institutional truth.

### 4. Code change is not always substantive change
Could mean renumbering, reorganization, or administrative cleanup.

### 5. Title change is not always substantive change
Could be formatting, punctuation, or small wording standardization.

### 6. One-off courses require caution
Single-appearance or low-persistence codes should be visibly flagged.

---

## 21. Reddit and discussion integration

Reddit / student discussion is a **planned product layer** for WGU Atlas, not a speculative feature. It is intended from the start and will be integrated in a controlled, phased way.

The site is official-history-first and discussion-aware. Discussion never replaces or overrides catalog facts.

### v1 — no discussion integration
v1 launches without any live Reddit data. The site should be designed from the start so that discussion surfaces (course pages, homepage modules) are placeholder-ready but empty or absent in v1.

### v1.1 — discussion integration on course pages and homepage
Add:

**On course pages:**
- discussion count
- recency of most recent linked post
- optional trend indicator (activity rising/falling)
- LLM-generated course guide (clearly labeled: source count, date range, disclaimer)
- freshness warnings where catalog change postdates main discussion period

**On homepage:**
- recently discussed courses module
- courses with active recent discussion
- courses whose main discussion predates a major catalog change

### Hard separation rule (non-negotiable)
Never blend:
- official catalog facts
- discussion signals
- LLM summaries

These must be under separate labeled headings on every page where they coexist.

### What to avoid
- homepage dominated by Reddit
- treating Reddit discussion as evidence of official curricular truth
- mixing discussion and official history into one undifferentiated block
- surfacing raw Reddit posts as the primary interaction — discussion should always be course-centered and curated

---

## 22. Around the WGU web module

This is a **committed design element** for v1. It appears on the homepage as a persistent utility section, not a hero module.

Its purpose is to position WGU Atlas as a navigator across the broader WGU information landscape — not just its own data.

### Structure

#### Official WGU channels
- official WGU website
- official WGU YouTube
- WGU Career Services YouTube
- WGU Instagram
- WGU TikTok
- official WGU Facebook

#### Community discussion spaces
- r/WGU and other relevant subreddits
- notable Facebook groups where appropriate

#### Career / support channels
- career-related or student support resources where appropriate

### Design rule
Always use labeled section headers to clearly separate:
- **Official** (WGU-produced)
- **Community** (student-run or third-party)
- **Support/career** (adjacent resources)

Do not flatten everything into one undifferentiated list. The separation is both a trust and a clarity requirement.

---

## 23. Information architecture for v1

## Recommended v1 pages
1. **Home**
2. **Courses**
3. **Course page**
4. **Timeline**
5. **Methods**
6. **Data**

If capacity allows:
7. **Programs**
8. **Program page**

---

## 24. Build phases

### Phase 0 — Create the `wgu-atlas` repo ← **next step**
Move the website code, site data artifacts, and build scripts out of `wgu-reddit` into a dedicated public repo:
- **Repo name:** `wgu-atlas`
- Public-facing, auditable, separate from unrelated Reddit Analyzer internals
- Transfer: `build_site_data.py`, `outputs/site_data/`, and relevant docs
- The `wgu-reddit` repo remains the internal research and data-production repo

### Phase 1 — Data products ✅ DONE
- ~~canonical course intelligence table~~ — **built** (`canonical_courses.csv/json`)
- ~~title variant classification~~ — **built** (`title_variant_classification.csv`)
- ~~named event layer~~ — **built** (`named_events.json`, `curated_major_events.json`)
- ~~export site-ready data~~ — **built** (`exports/courses.json`, `exports/courses/{code}.json`, `exports/events.json`, `exports/search_index.json`, `exports/homepage_summary.json`)

Remaining data gaps (deferred):
- canonical program intelligence table (program_history.csv is available but not fully flattened for the site)
- cert cross-edition tracking (only 2026-03 snapshot)
- predecessor/successor inference

### Phase 2 — Static site shell (next after repo creation)
- homepage with search, school cards, activity modules, timeline preview
- course explorer with filters
- course detail page (flagship)
- timeline page with curated events
- methods page
- data page

### Phase 3 — Visual / history layer
- annotated major-events timeline visual
- school/college lineage timeline
- course lifecycle timeline on course pages
- homepage activity module visuals

### Phase 4 — Program pages
- program explorer
- program detail page
- program course-roster-over-time matrix / heatmap

### Phase 5 — Discussion integration (v1.1)
- homepage discussion modules
- course-page discussion signals (count, recency, warnings)
- LLM-generated course guides (with metadata and freshness labels)

### Phase 6 — Advanced exploration
- transitions explorer
- successor/predecessor inference
- advanced charts and overlays

---

## 25. Success criteria

The first public version should let a user:
- search for a course
- understand whether it is current
- see its history quickly
- see a few major WGU historical events
- understand what the site is and what it is not
- trust that the data is validated

Later versions should let a user:
- explore programs
- compare periods
- see discussion context
- understand major change waves across schools and programs

---

## 26. Final recommendation

The strongest first public product is:

1. **Homepage with search, drilldown, curated current/recent modules, and discussion preview**
2. **Course page with official history, discussion signals, and student-summary layer**
3. **Major events timeline**
4. **Methods / caveats page**

Then add:
5. **Program page**
6. **School/college lineage visual**
7. **Program history matrix**
8. **Discussion/context expansion**

This design makes the project:
- immediately useful
- historically rich
- student-friendly
- analytically credible
- trustworthy in how it presents evidence and uncertainty



---

## Appendix — Data layer build status (2026-03-14)

*This appendix documents what is built versus what remains planned.*

---

### What is built

All artifacts live in `outputs/site_data/` (internal research repo: `wgu-reddit`).
They will be transferred to the `wgu-atlas` repo as part of Phase 0.

**1. Title variant classification**

| File | Contents |
|---|---|
| `title_variant_classification.csv` | 167 codes classified by variant type |
| `title_variant_summary.json` | Count summary + manual review list |

| Class | Count | Meaning |
|---|---|---|
| extraction_noise | 145 | PDF line-wrap truncations, Unicode quote variants, catalog oscillations |
| punctuation_only | 16 | Hyphen, comma, em-dash, & →and changes |
| wording_refinement | 3 | Typo fix or minor synonym swap (D396, D578, D601) |
| substantive_change | 2 | Genuine semantic renames (D346, D347 only) |
| formatting_only | 1 | Space insertion (C764, retired) |

Key implication: 87% of apparent title variation is extraction noise, not real renames. This is now explicit in the data and directly supports the trust rules in §6 and §19.

Manual review still needed: **D344** (canonical title is itself a truncation artifact).

---

**2. Canonical course intelligence table**

| File | Contents |
|---|---|
| `canonical_courses.csv` | 1,646 rows — 838 AP active, 756 AP retired, 52 cert |
| `canonical_courses.json` | Same content keyed by course_code |

Key fields: `canonical_title_current`, `observed_titles`, `first/last_seen_edition`, `active_current`, `contexts_seen`, `current_programs`, `current_program_count`, `historical_program_count`, `edition_count`, `ghost_flag`, `single_appearance_flag`, `stability_class`, `title_variant_class`, `current_title_confidence`, `notes_confidence`

Definitions locked in:
- `ghost_flag`: RETIRED AND edition_count ≤ 2 → 14 codes
- `single_appearance_flag`: edition_count == 1 → 13 codes
- `stability_class`: perpetual / stable / moderate / ephemeral / single / cert_only

---

**3. Named event layer**

| File | Contents |
|---|---|
| `named_events.csv` + `.json` | 41 events (all threshold-crossing transitions) |
| `curated_major_events.json` | 10 events with hand-written titles and interpretations |

All events separate `observed_summary` from `interpreted_summary`.
The 10 curated events cover 2017-01→2017-03 through 2025-01→2025-02.
The 31 non-curated events have machine-generated observed summaries; editorial interpretation can be added incrementally.

---

**4. Static site exports**

| File | Count |
|---|---|
| `exports/courses.json` | 1,646 course cards |
| `exports/courses/{code}.json` | 838 active AP individual detail files |
| `exports/events.json` | 41 events (chronological) |
| `exports/search_index.json` | 1,842 entries (courses + programs) |
| `exports/homepage_summary.json` | Homepage modules: newest programs, recent version changes, curated event previews, active-by-school |

These are sufficient for a no-database static site build.

**Scope decision for v1:** individual course detail files exist only for active AP courses (838 files). A deliberate choice is needed before building frontend routing: whether retired and cert-only codes get detail pages in v1 or are deferred.

---

### What remains deferred

| Item | Status | Notes |
|---|---|---|
| Canonical program intelligence table | Partial | `program_history.csv` exists; no flat site-ready JSON yet |
| Program course-roster by edition | Not built | Required for program heatmap (Phase 4) |
| Cert cross-edition tracking | Partial | Only 2026-03 snapshot; `first_seen=2024-09` for all cert codes |
| Successor/predecessor inference | Not built | Architecture planned; no inference layer built |
| Reddit / discussion integration | Not built | Site is designed discussion-aware from day one; data layer not started |
| LLM-generated course guides | Not built | Planned for v1.1 |

---

### Immediate next step

1. Create the `wgu-atlas` public repo
2. Transfer `build_site_data.py`, `outputs/site_data/`, and relevant docs into it
3. Begin the static site shell (Phase 2): homepage, course explorer, course page, timeline, methods, data pages
4. Return to `wgu-reddit` for the canonical program intelligence artifact when program pages are next
