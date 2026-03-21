# Program Guide — Course-Page Enrichment Matrix

**Date:** 2026-03-21
**Coverage basis:** 115/115 guides parsed (Phase C complete)
**Scope:** Which program-guide fields can enrich Atlas course detail pages (`/courses/{code}`)

---

## The Phase E Dependency

All course-page enrichment requires **Phase E: Course-Code Matching** — a step that links guide-extracted course descriptions and competency bullets to the Atlas course codes used in the URL structure (`/courses/{CODE}`). Without Phase E, guide data can only appear on program pages (aggregated by program), not on individual course detail pages.

Phase E is NOT started as of Phase C completion.

---

## Available Content for Course Pages (Post–Phase E)

### 1. Course Descriptions
- **Source:** `areas_of_study[*].courses[*].description`
- **Volume:** 2,593 course-description records across 115 guides
- **Unique courses (estimate):** WGU has ~1,100+ catalog courses. Many courses appear in multiple guides. A single course code may have 1–N descriptions (from N programs that include it); these should be deduped or merged.
- **Content quality:** HIGH. 100% of AoS courses have non-empty descriptions. Descriptions average ~2–4 sentences.
- **Caveat:** Description text is program-specific context in some cases ("In this course, [program students] will..."). Dedup/merge strategy needed.

### 2. Competency Bullets
- **Source:** `areas_of_study[*].courses[*].competency_bullets`
- **Volume:** 2,591 competency-bullet sets (99.9% of AoS courses)
- **Average bullets per course:** ~5–6 (varies 1–13)
- **Content quality:** HIGH. Competency bullets are the most detailed learning-outcome data available.
- **Render recommendation:** Progressive disclosure ("View learning objectives") — dense content.

### 3. Standard Path Placement
- **Source:** `standard_path[*].{title, cus, term}`
- **Value:** Shows which programs include this course, at what term, and for how many CUs
- **Volume:** 2,568 SP rows
- **Caveat:** Same course may appear in multiple programs at different terms and CU counts. Aggregated view needed.

---

## Phase E Design Considerations

Phase E must produce a mapping from guide-extracted course titles to Atlas course codes. Key challenges:

1. **Title matching:** Guide course titles use the full course name (e.g., "Composition: Writing with a Strategy"). Atlas codes are short (e.g., `C100`). Matching requires a title → code lookup table from the catalog data.

2. **Multi-program dedup:** A single course (e.g., "Introduction to Psychology") appears in many programs. The description text may be identical or vary slightly. Phase E must handle both.

3. **Coverage:** Phase E will match a subset of the 2,593 guide course records to a subset of the ~1,100+ Atlas course codes. Not all guide courses have corresponding Atlas pages; not all Atlas courses are in any guide.

4. **Trust level:** Course descriptions extracted from guides are the primary source of truth for content. They should be used directly.

---

## Pre–Phase E Enrichment (No Matching Required)

These can be surfaced on course pages WITHOUT Phase E, using only the catalog's existing course code:

| Enrichment type | How to surface | Notes |
|----------------|----------------|-------|
| Which programs include this course | Catalog already has this (course → program relationships) | No guide data needed |
| Guide-sourced descriptions on program pages | Already in scope for degree-page matrix | Not course-page enrichment |

**Bottom line:** There is no course-page enrichment from program guides that bypasses Phase E. All guide-based course-page enrichment requires the title → code mapping.

---

## Coverage Estimate for Phase E Output

Given 2,593 AoS course records across 115 guides, and assuming WGU has ~1,100 catalog courses of which ~900 appear in guides:

| Metric | Estimate |
|--------|----------|
| Distinct course titles in guide corpus | ~800–1,000 (many courses repeat across programs) |
| Atlas course codes with at least one matched description | ~700–900 (70–90% of guide-accessible courses) |
| Guides contributing descriptions per popular course | 2–15+ (general education courses appear frequently) |

---

## Recommended Phase E Approach

1. **Build title → code lookup** using Atlas catalog data (course titles from `public/data/`).
2. **Fuzzy-match** guide course titles against catalog titles (allow minor spelling/punctuation differences).
3. **Flag non-matches** for manual review or exclusion (specialty courses, WGU-unique names).
4. **Dedup descriptions:** For courses with multiple guide-sourced descriptions, either select the highest-quality instance or present the most recently dated version.
5. **Gate test:** Validate on a 10-course sample before full-corpus run.

Phase E is a separate workstream from Phase D. Phase D should build program-page artifacts; Phase E can be pursued independently after Phase D.
