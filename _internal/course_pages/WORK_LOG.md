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

---

## Session 2 — 2026-03-21

**Objective:** Create a sandboxed enriched course-page preview for all 10 cohort courses, visible in the local site, for design review before any production implementation decisions.

**Prototype surface created:**
- Route: `/proto/course-preview` (index) and `/proto/course-preview/[code]` (per-course)
- Separate from production `/courses/[code]` — no production pages modified

**Files created:**
- `src/lib/coursePreviewData.ts` — build-time data loader; reads from `data/program_guides/` at build; serves only the 10 cohort courses
- `src/app/proto/course-preview/page.tsx` — cohort index page with shape table and shape notes
- `src/app/proto/course-preview/[code]/page.tsx` — per-course preview server component; `generateStaticParams` returns only the 10 cohort codes
- `src/components/proto/CourseEnrichmentPreview.tsx` — shared rendering component; all 10 pages use the same component/block system
- `_internal/course_pages/content_maps/session2_cohort_preview.txt` — comprehensive content map for all 10 cohort pages

**Cohort pages previewed:**
C178, C480, C169, C165, D426, C170, C176, C824, D118, C216

**Section order used (per session brief):**
1. Header (code, CUs, status, shape badge, title, college)
2. Compact facts bar (with guide enrichment count: Nd/Nc)
3. High-signal blocks: Capstone callout → Cert prep → Requires (prereq)
4. Sparse fallback notice (if no enrichment)
5. Guide-derived overview (single blockquote or multi-variant panels)
6. What You'll Learn / competencies (single list or multi-variant panels)
7. Program context notes (if multi-variant)
8. Prerequisite For (reverse prereqs, violet accent)
9. About This Course (existing WGU catalog text)
10. Included in Current Degrees / Retired Degrees
11. Also Known As / Notes

**Build verification:** `next build` completed cleanly; all 10 cohort pages generated as SSG.

**What looked promising:**
- C178/C176: cert block in emerald is clear and well-placed; these are the cleanest enriched cases
- C824: capstone + prereq block combination reads well near the top; indigo + slate is legible
- D426: "Prerequisite For" (violet) block is a clean navigation aid
- D118: cumulative-sequence amber block honestly exposes the limitation without hiding it
- C216: sparse fallback notice + title-only capstone callout clearly communicates absence of enrichment

**What looked too dense / awkward:**
- C169: 3 description panels + 3 competency panels = 6 stacked content panels before catalog history. The page is long and complex. This is the intended stress test, but it confirms variant-policy resolution is urgent.
- C165: competency variant count for a "cosmetically similar" course is still potentially 3 panels — the description collapses but competency collapse depends on actual bullet similarity.
- C480 / C170: guide description text mentions the prereq explicitly, creating double-mention (Requires block + description text). Needs a policy call.

**Policy questions this session surfaces:**
1. Multi-variant description: 85% word-overlap heuristic for cosmetic collapse — robust enough?
2. Multi-variant competency: when should 3 sets collapse vs. show?
3. Prereq program-context gap: C169's prereq applies only in BSDA — shows to all programs without context.
4. Prereq–description redundancy: C480/C170 state prereq in description AND in Requires block.
5. Cumulative-sequence display: amber block with raw text is the honest choice — but is it the right production choice?
6. Title-only capstone (C216): does the inference label add value or noise?
7. High-signal block ordering: is prereq more urgent than cert? Should it come before cert?

**Next step:**
Review cohort previews in browser. Use content map to discuss policy questions. Produce a shape-disposition / display-policy artifact answering the open questions before production implementation begins.
