# WORKQUEUE

Purpose: active working backlog for WGU Atlas.

Use this file for:
- current execution priorities
- near-term queued work
- deferred but still relevant work

Do not use this file for:
- durable policy → belongs in `_internal/ATLAS_REPO_MEMORY.md`
- implementation/spec canon → belongs in `_internal/ATLAS_REPO_MEMORY.md`
- old planning residue that is no longer driving execution

Note: `docs/DECISIONS.md` and `docs/ATLAS_SPEC.md` are archived in `_internal/archive/2026-03-final-consolidation/docs/`. They are not active canon.

Status legend:
- `now`: active / highest-priority execution
- `next`: important and likely soon
- `later`: planned but intentionally deferred
- `blocked`: depends on external input, upstream data, or unresolved product decision

---

## Core direction

Atlas is now being shaped as:

- a student-useful catalog viewer
- a degree/course/college guide
- a comparison and context surface
- a place to attach relevant official and later community resources to the right entity

Primary product sequence:

1. functional catalog viewer
2. richer catalog-derived content on the right pages
3. relevant official WGU resources and videos
4. relevant community/discussion layer later

Core operating question:

**Where on Atlas is this specifically useful?**

Not:
- how do we expose more data generally
- how do we surface more links generally
- how do we show more history generally

---

# A) Browse / navigation system

## A-01 Finalize shared browse/filter system
- Status: `now`
- Goal: stabilize the shared browse language across Degrees and Courses.
- Current direction:
  - College as primary filter
  - Level as secondary filter
  - Search as refinement
  - Degree selector only on Courses
- Acceptance:
  - same filter logic and language on Courses and Degrees
  - visual hierarchy clearly College first, Level second
  - no internal taxonomy leakage

## A-02 Degrees page polish after shared filter rollout
- Status: `next`
- Goal: review the production Degrees page after the new filter system landed.
- Review:
  - filter clarity
  - default state usefulness
  - result-card density/readability
  - retired toggle wording/placement
- Acceptance:
  - Degrees feels like guided browse, not a raw list

## A-03 Colleges rename and browse alignment
- Status: `next`
- Goal: decide and implement whether `Schools` should become `Colleges` across student-facing product surfaces.
- Scope:
  - nav
  - page titles
  - subtext
  - metadata
  - internal consistency across homepage / Degrees / Courses / compare copy
- Acceptance:
  - one consistent public-facing term

## A-04 Homepage search/results consistency
- Status: `next`
- Goal: fix or redesign the homepage search/results path so the promise matches behavior.
- Current issue:
  - homepage search is broader in wording than some follow-through destinations
- Acceptance:
  - search behavior and copy are aligned

---

# B) Compare Degrees

## B-01 Production rollout of chosen compare UI
- Status: `now`
- Goal: adopt the selected compare prototype as the main Compare Degrees experience.
- Current chosen direction:
  - lane-based visual compare
  - persistent/sticky header context
  - compact top summary
- Acceptance:
  - compare page uses chosen design in production
  - top clutter removed
  - roster starts much sooner
  - sticky context works on long comparisons

## B-02 Broaden compare universe in production
- Status: `now`
- Goal: move compare beyond the tiny pilot and support the broader same-college same-level compare universe, with explicit exclusions where needed.
- Known exclusions:
  - pathway programs
  - identical-name groups lacking safe disambiguation until label handling is ready
- Acceptance:
  - compare is no longer effectively pilot-only
  - invalid/bad-fit compares are still restrained

## B-03 Compare label / short-name hardening
- Status: `now`
- Goal: ensure compare-safe short labels work across the compare universe.
- Problem:
  - current labels may be good for sampled pairs but must scale to all compare-eligible degrees
- Needs:
  - base + differentiator logic
  - fallback disambiguators
  - no generic Track A / Track B model
- Acceptance:
  - compact compare UI remains readable across long-name and awkward-name cases

## B-04 Compare universe qualification / exclusion rules
- Status: `next`
- Goal: formalize current compare-eligibility and exclusion behavior into current implementation and canon.
- Include:
  - same college
  - same level
  - pathway exclusion
  - known bad-fit exclusions
  - identical-name handling until disambiguation is ready
- Acceptance:
  - compare gating is intentional and documented

## B-05 Compare page feature follow-ups
- Status: `next`
- Goal: evaluate post-rollout quality-of-life features.
- Candidates:
  - show only differences toggle
  - jump to first difference
  - expand/collapse shared curriculum
  - compact metadata drawer
- Acceptance:
  - only features that materially improve student use are added

## B-06 Compare policy capture in `_internal/ATLAS_REPO_MEMORY.md`
- Status: `next`
- Goal: ensure compare policy is fully captured in ATLAS_REPO_MEMORY.md.
- Note: `docs/DECISIONS.md` is archived; compare policy now belongs in ATLAS_REPO_MEMORY.md locked decisions section.
- Current issue:
  - Compare model has evolved beyond what was in DECISIONS.md
- Acceptance:
  - ATLAS_REPO_MEMORY.md reflects current compare model and exclusion rules

---

# C) Course pages

## C-01 Add catalog-sourced course description/content
- Status: `next`
- Goal: enrich course detail pages with official catalog course information where available.
- Direction:
  - likely `About This Course`
  - source-labeled catalog text
  - expandable if long
- Acceptance:
  - course pages are no longer structurally thin compared to degree pages

## C-02 Course page content placement review
- Status: `next`
- Goal: decide what course-derived or course-adjacent data belongs on course pages.
- Review candidates:
  - description text
  - CU prominence
  - status/history summary
  - program membership context
  - official resource placement
- Acceptance:
  - course page feels intentional, not just a metadata shell

## C-03 Surface more useful course data from catalog-derived artifacts
- Status: `next`
- Goal: identify course-level data already available or derivable but not yet surfaced.
- Acceptance:
  - list of missing course data fields
  - placement decisions for each
  - implementation queue created where appropriate

## C-04 Course-name shortening / compare-safe display maintenance
- Status: `next`
- Goal: make sure any manual or semi-manual shortening/compare-label treatment scales to new courses/degrees over time.
- Requirement:
  - if shorthand is required for compare or dense browse surfaces, new catalog additions must receive equivalent treatment
- Acceptance:
  - repeatable workflow exists for new catalog refreshes
  - shorthand does not depend on one-off manual drift

---

# D) Degree pages

## D-01 Degree page top-section simplification review
- Status: `next`
- Goal: verify degree page top hierarchy after recent cleanup.
- Review:
  - information density
  - relevance of metadata
  - history/supporting-context balance
- Acceptance:
  - degree page leads with current degree understanding, not metadata clutter

## D-02 Missing degree data / content inventory
- Status: `next`
- Goal: identify catalog-derived degree data not yet surfaced and decide where it belongs.
- Includes:
  - page body content not yet used
  - useful derived fields
  - content that may need a new section/surface
- Acceptance:
  - explicit inventory of degree data still missing from Atlas pages

## D-03 Program History integration cleanup
- Status: `next`
- Goal: finish integrating reviewed program-history enrichment on degree pages in a current-entity-relevant way.
- Acceptance:
  - degree history context is useful and supporting, not archive-first

---

# E) College pages

## E-01 Replace static college descriptions with better sourced content
- Status: `next`
- Goal: use catalog/public WGU material to create better college descriptions.
- Current state:
  - duplicated short descriptions across multiple files
- Acceptance:
  - stronger college intros
  - one shared source of truth for repeated description text

## E-02 College page informative sidebar / resource panel
- Status: `next`
- Goal: define and implement the informative sidebar/resource area for college pages.
- Candidates:
  - official resources
  - college-specific context
  - future official videos
- Acceptance:
  - college pages feel like real hubs, not thin list pages

## E-03 College-page content inventory
- Status: `next`
- Goal: identify what college-level data/content exists or could be derived but currently has no good home.
- Acceptance:
  - placement decisions for college-level content
  - new section ideas captured intentionally

---

# F) Catalog-derived data expansion

## F-01 Inventory missing catalog-derived content across all entity types
- Status: `now`
- Goal: systematically identify catalog data that exists but is not yet surfaced where it should be.
- Scope:
  - course data
  - degree data
  - college data
  - compare-relevant data
- Acceptance:
  - entity-by-entity inventory of missing content
  - explicit `put it here / no home yet / maybe new surface` decisions

## F-02 Create placement map for missing catalog data
- Status: `next`
- Goal: for each missing data type, decide:
  - where it belongs now
  - whether it needs a new page section
  - whether it needs a new product surface later
- Acceptance:
  - no “interesting data with no plan” limbo

## F-03 Evaluate “data with no home yet”
- Status: `next`
- Goal: identify valuable catalog-derived information that may deserve entirely new surfaces.
- Examples:
  - cross-program patterns
  - derived groupings
  - historical/current insights that don’t fit existing pages
- Acceptance:
  - explicit backlog items for new-surface candidates

---

# G) Official context / official resources

## G-01 Official resource placement expansion
- Status: `next`
- Goal: continue mapping relevant official WGU pages to the right Atlas entities.
- Priority entities:
  - degree pages
  - college pages
  - selected course pages
- Acceptance:
  - stronger, more relevant official-resource coverage without generic link dumping

## G-02 Official-resource generator / reproducibility
- Status: `next`
- Goal: make official-resource placements reproducible and low-maintenance.
- Acceptance:
  - deterministic generator exists
  - placement artifacts are not manual black boxes

## G-03 Newsroom / long-tail official content discovery
- Status: `later`
- Goal: expand beyond sitemap bootstrap where relevant.
- Acceptance:
  - official context inventory is broader than the basic sitemap set

---

# H) Official video layer

## H-01 Import and structure official WGU video inventories
- Status: `next`
- Goal: ingest official WGU YouTube + Career Services YouTube inventories into Atlas planning/data model.
- Acceptance:
  - raw manifests in Atlas space
  - sources kept distinct
  - common schema defined

## H-02 Official video curation model
- Status: `next`
- Goal: define what types of videos are useful on which surfaces.
- Principle:
  - helpful official context
  - not feed dumping
  - not generic job-search noise on unrelated pages
- Acceptance:
  - restrained, entity-first placement rules

## H-03 Pilot official video placements
- Status: `later`
- Goal: place a small set of high-confidence official videos on degree/college/course pages where strongly relevant.
- Acceptance:
  - placements feel useful and restrained

---

# I) Community / discussion layer

## I-01 Entity-scoped community model
- Status: `later`
- Goal: define how Reddit/community links or summaries attach to Atlas entities.
- Principle:
  - entity-scoped
  - clearly secondary to official/catalog facts
  - provenance-labeled and cautious
- Acceptance:
  - discussion does not become a generic feed layer

## I-02 Community resource pilot
- Status: `later`
- Goal: test a small set of strongly relevant discussion attachments.
- Acceptance:
  - value demonstrated without diluting product posture

---

# J) Low-maintenance site operations

## J-01 Monthly catalog refresh workflow
- Status: `now`
- Goal: establish a low-maintenance monthly refresh workflow for Atlas.
- Requirement:
  - if new catalog editions are available, Atlas should be easy to refresh without heroic manual work
- Workflow should cover:
  - detecting new catalog editions
  - regenerating site data
  - validating key outputs
  - handling new degrees/courses
  - updating freshness indicators
- Acceptance:
  - a repeatable monthly runbook exists
  - a maintainer can follow it without rediscovering steps

## J-02 New-catalog delta checklist
- Status: `now`
- Goal: define what must be checked whenever a new catalog is ingested.
- Includes:
  - new programs
  - retired programs
  - new courses
  - renamed content
  - compare label/shorthand implications
  - official-resource attachment implications
- Acceptance:
  - refreshes are not just data rebuilds; they include content-impact checks

## J-03 Shorthand / label maintenance for new data
- Status: `now`
- Goal: ensure any manually or semi-manually shortened degree/course compare labels receive maintenance when new catalog items appear.
- Applies to:
  - compare labels
  - compact browse surfaces
  - any manual label overrides
- Acceptance:
  - new catalog additions do not silently skip shorthand treatment where required

## J-04 Deterministic build/rebuild hardening
- Status: `next`
- Goal: continue reducing ambiguity around how core runtime data files are generated.
- Acceptance:
  - core site data artifacts are reproducible in-repo
  - refresh workflow is less fragile

---

# K) Documentation / canon refresh

## K-01 ~~Refresh `docs/DECISIONS.md`~~
- Status: `superseded`
- Note: `docs/DECISIONS.md` is archived. Durable policy now lives in `_internal/ATLAS_REPO_MEMORY.md`. No refresh needed.

## K-02 ~~Refresh `docs/ATLAS_SPEC.md`~~
- Status: `superseded`
- Note: `docs/ATLAS_SPEC.md` is archived. Implementation canon now lives in `_internal/ATLAS_REPO_MEMORY.md`. No refresh needed.

## K-03 Archive stale planning docs
- Status: `next`
- Goal: move old planning documents out of the active mental path while preserving useful source material.
- Candidates:
  - stale workqueue
  - merged strategy docs
  - pilot-era compare planning artifacts
- Acceptance:
  - active docs are leaner and more trustworthy

---

# L) Cleanup / quality

## L-01 Shared constants / duplication cleanup
- Status: `next`
- Goal: reduce drift-prone repeated constants and repeated copy.
- Known example:
  - repeated college descriptions across multiple files
- Acceptance:
  - fewer duplicated text/config sources

## L-02 Product wording consistency pass
- Status: `next`
- Goal: continue normalizing student-facing wording.
- Focus:
  - college/school terminology
  - current/retired terminology
  - compare language
  - history/supporting-context language
- Acceptance:
  - student-facing copy is consistent across major surfaces

## L-03 Visual QA after major compare rollout
- Status: `next`
- Goal: run a final QA pass on compare, browse, and responsive layouts after recent UI shifts.
- Acceptance:
  - no obvious density/spacing/sticky regressions across desktop and smaller widths

---

# Current execution priority snapshot

## Now
- A-01 Finalize shared browse/filter system
- B-01 Production rollout of chosen compare UI
- B-02 Broaden compare universe in production
- B-03 Compare label / short-name hardening
- F-01 Inventory missing catalog-derived content across all entity types
- J-01 Monthly catalog refresh workflow
- J-02 New-catalog delta checklist
- J-03 Shorthand / label maintenance for new data

## Next
- A-02 Degrees page polish after shared filter rollout
- A-03 Colleges rename and browse alignment
- C-01 Add catalog-sourced course description/content
- D-02 Missing degree data / content inventory
- E-01 Replace static college descriptions with better sourced content
- G-01 Official resource placement expansion
- H-01 Import and structure official WGU video inventories

## Later
- G-03 Newsroom / long-tail official content discovery
- H-03 Pilot official video placements
- I-01 Entity-scoped community model
- I-02 Community resource pilot