# Course-Page Enrichment — Work Log

Reverse-chronological. One top-level section per session.

---

## Session 1 — 2026-03-21

**Objective:** Establish starting artifact set and preserve planning inputs for course-page design.

**Inputs reviewed:**
- Context packet: top-level goals, core artifacts needed, current course-page surfaces, what the session needs to decide
- Current `/courses/[code]` page structure: full content inventory from `src/app/courses/[code]/page.tsx` and `content_map.txt`
- Guide-layer enrichment data: `course_enrichment_candidates.json`, `cert_course_mapping.json`, `prereq_relationships.json`, `course_enrichment_summary.json`
- Design cohort: 10 representative courses selected by data shape

**Conclusions:**
- Course pages are the active next Atlas surface after degree-page guide enrichment (closed out)
- Current course pages are catalog/history-first; no guide-layer content is published yet
- Available guide-layer inputs: guide descriptions (751 courses), competency bullets, cert signals (9 auto-accepted), prereq requirements (50 auto-accepted), reverse-prereq relationships, capstone signals
- Page design depends on course-shape groups — not a uniform single template
- The 10-course cohort covers all relevant shapes and is sufficient for design work

**Open questions carried forward:**
- Multi-variant description policy (meaningful vs. cosmetic variants)
- Multi-variant competency policy
- Capstone publication rule (explicit guide signal vs. title-only inference)
- Cumulative-sequence nursing prereq handling (defer or surface a descriptive note)
- Prereq/description redundancy (some guide descriptions already contain prereq text)

**Artifacts created:**
- `_internal/course_pages/COURSE_PAGE_ENRICHMENT_SESSION_1_ARTIFACT.md` — full planning input record
- `_internal/course_pages/WORK_LOG.md` — this file

**Next step:**
Produce a shape-disposition / display-policy artifact that answers the open questions and defines exact display rules per shape group. Gate before implementation planning begins.
