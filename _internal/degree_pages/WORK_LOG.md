# Degree Pages — Work Log

Reverse-chronological. One top-level section per session.

---

## Session 2 — 2026-03-22

**Objective:** Implement cross-cohort degree-page improvements identified in Session 1 review. Get all fixes live on production degree pages. Close the degree-pages workstream.

**Scope:** Production degree page and prototype only. No guide extraction, no course-page work, no homepage.

**Decisions confirmed:**
- AoS moves above the roster (richest guide content before the CU table)
- AoS course entries link to `/courses/{code}` where a title match against the program roster is confident
- Missing outcomes shows a fallback section rather than silent absence
- Advisor-guided banner copy improved to explain what advisor-sequenced means
- Suppressed roster message updated to point "above" (since AoS now precedes it)
- Degraded quality (low confidence or caveat messages) gets a prominent amber callout block, not just a small inline chip
- Duplicate caveat messaging reduced: caveat pill suppressed in GuideProvenance when the degraded block handles it; GuideCapstone partial note suppressed when caveats already covered by the block
- Capstone-in-AoS hint added for programs where `capstone.present=false` but an AoS group contains "capstone"
- Section label normalized to "Program Learning Outcomes" everywhere

**What changed:**

| File | Change |
|---|---|
| `src/app/programs/[code]/page.tsx` | Reordered: AoS now before Course Roster. Added degraded quality warning block. Missing outcomes fallback. Improved advisor-guided banner. Updated suppressed roster text (says "above"). Capstone AoS discovery hint. `suppressCaveatPill` and `suppressPartialNote` passed to components. |
| `src/app/proto/degree-preview/[code]/page.tsx` | Mirrored all changes from production page. |
| `src/components/programs/GuideAreasOfStudy.tsx` | Added `rosterCourses` prop; normalizes titles and links matched course entries to `/courses/{code}`. Added `Link` import. |
| `src/components/programs/GuideProvenance.tsx` | Added `suppressCaveatPill` prop; when true, omits the amber caveat pill (degraded block handles it instead). |
| `src/components/programs/GuideCapstone.tsx` | Added `suppressPartialNote` prop; when true, omits "Part of a multi-course capstone sequence." note. |
| `src/app/programs/[code]/LearningOutcomes.tsx` | Section heading renamed from "Learning Outcomes" to "Program Learning Outcomes". |

**Cohort validation (all confirmed live):**

| Program | Shape | Key checks |
|---|---|---|
| BSCS | plain baseline | AoS above roster ✓; no degraded warning ✓; no outcomes fallback (has outcomes) ✓ |
| BSSWE | family + cert | AoS above roster ✓; medium confidence badge (no prominent block — no caveats) ✓; AoS course links where matched ✓ |
| BSSESC | advisor-guided + licensure | AoS above roster ✓; missing outcomes fallback visible ✓; improved advisor-guided banner ✓ |
| MATSPED | suppressed SP | AoS above suppressed block ✓; suppressed block says "Areas of Study above" ✓; degraded warning block (caveat) ✓; caveat pill suppressed ✓ |
| BSDA | capstone + cert | AoS above roster ✓; capstone at bottom ✓; no caveats so no degraded block ✓ |
| MEDETID | caveat capstone | Degraded warning block visible ✓; caveat pill suppressed ✓; capstone partial note suppressed ✓ (deduplication resolved) |
| BSITM | low confidence | Degraded warning block (low confidence + caveat) ✓; caveat pill suppressed ✓; capstone AoS hint visible ✓ |

**Deferred follow-ups (documented, not implemented):**
- Capstone-in-AoS normalization is implemented via the hint note but a full GuideCapstone block for AoS-only programs would require either a new data field or AoS-group scraping. Left as hint note.
- AoS course linking relies on exact title normalization. Some guide titles differ from catalog titles; unmatched entries stay as plain text (correct behavior, acceptable coverage gap).
- College name history date ranges (data exists in lineage, not threaded to degree page).
- All-caveat-messages display for multi-caveat programs: the degraded block now shows all `caveat_messages_ui` entries (previously only `[0]` was shown). Resolved.

**Workstream status after Session 2:** Closed.

---

## Session 1 — 2026-03-22

**Objective:** Open the degree-pages workstream. Establish the review cohort, build the prototype surface, and generate content maps for in-browser and GPT review.

**Context:**
The program-guides extraction/wiring workstream (Sessions 29–35) is complete and closed. Guide-derived content is live on degree pages. This session opens a new, separate workstream to review whether the current degree-page design is good enough, and to identify and prioritize improvements.

**What this session is NOT:**
- Not a continuation of guide extraction or wiring
- Not production implementation on live degree pages
- Not homepage work

**Inputs reviewed:**
- Full live page inventory from `src/app/programs/[code]/page.tsx` and all guide components
- Guide artifact payload shape from `data/program_guides/degree_artifacts/` (115 artifacts, scanned programmatically)
- `public/data/program_enriched.json` and `public/data/programs.json` for all cohort candidates
- `_internal/page_designs/program_detail.md` — confirmed stale (pre-guide wiring, 2026-03-20); not used as current reference
- Prior session inspection work (Sessions 38 handoff)

**Cohort locked:**
7 programs selected to cover all distinct live page shapes:
- BSCS — plain baseline
- BSSWE — family + professional cert (medium confidence, alias)
- BSSESC — advisor-guided + licensure cert (no outcomes)
- MATSPED — suppressed SP + anomaly (only suppressed in dataset)
- BSDA — capstone + professional cert (clean baseline capstone)
- MEDETID — caveat capstone + anomaly (partial capstone, double warning)
- BSITM — low confidence + anomaly (only low-confidence artifact in dataset)

**Prototype surface created:**
- Route: `/proto/degree-preview` (index) and `/proto/degree-preview/[code]` (per-degree)
- Separate from production `/programs/[code]` — no production pages modified
- Renders identical content to production; adds cohort gate, proto banner, and back link

**Files created (prototype):**
- `src/lib/degreePreviewData.ts` — cohort codes + shape metadata
- `src/app/proto/degree-preview/page.tsx` — cohort index
- `src/app/proto/degree-preview/[code]/page.tsx` — per-degree preview

**Content map generated:**
- `_internal/degree_pages/content_maps/session1_degree_cohort_preview.txt`

**Key observations from cohort review:**
1. AoS is buried below the full course roster on every full-roster program (37–42 courses). The richest guide content is at the bottom of a long page.
2. AoS course entries have no links to `/courses/{code}`. The roster above links every code. Inconsistent.
3. MATSPED's AoS section carries the whole page (suppressed roster) — demonstrates AoS as a content layer, not just supplemental detail.
4. BSITM: "Capstone and Portfolio" group in AoS but `capstone.present=false`. The GuideCapstone block is absent; the capstone information is only accessible by expanding the AoS group.
5. BSSESC has no Learning Outcomes section — the page moves from Degree History directly to Licensure Preparation. No explanation of why outcomes are absent.
6. MEDETID caveat appears in two places: GuideProvenance header badge and GuideCapstone block. Same information twice, different framing.
7. Provenance badge is small and header-only. For BSITM (low confidence, red label) and MATSPED (anomaly + caveat pill), the data quality signal may not register with a skimming reader.
8. Advisor-guided banner (BSSESC) is a single amber line above the roster — minimal framing for a significant structural difference.

**Open questions for Session 2:**
- Should AoS move above the roster?
- Should AoS course titles link to `/courses/{code}`?
- How to frame the missing-outcomes case for education programs?
- Is the provenance/caveat treatment prominent enough for degraded-quality programs?
- Does the advisor-guided framing need more explanation?
- Does MEDETID's double caveat need to be resolved?

**Next step:**
Review cohort pages in browser at `/proto/degree-preview`. Use content map for GPT discussion. Write Session 2 with design decisions.

---
