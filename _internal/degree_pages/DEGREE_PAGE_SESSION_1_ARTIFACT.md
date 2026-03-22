# Degree Pages — Session 1 Artifact

**Date:** 2026-03-22
**Status:** CLOSED — Session 2 implemented all priority fixes (2026-03-22). See `WORK_LOG.md` for Session 2 detail.
**Working area:** `_internal/degree_pages/`
**Prototype surface:** `/proto/degree-preview`
**Production route:** `/programs/[code]`

---

## 1. Workstream Scope

This workstream is **distinct from the closed program-guides extraction/wiring track** (Sessions 29–35, closed 2026-03-22). That workstream is complete: all 115 guide artifacts are built and wired to degree pages.

This workstream asks: **given that guide content is now live on degree pages, is the page design good enough?**

The focus is product review and targeted improvement, not new data extraction. All guide data is already available. The question is whether the current page layout, hierarchy, and provenance treatment serve a student effectively.

---

## 2. Current Live Degree-Page Inventory

### Route and files

- Main route: `src/app/programs/[code]/page.tsx`
- Local component: `src/app/programs/[code]/LearningOutcomes.tsx`
- Guide components: `src/components/programs/Guide{Provenance,CertBlock,FamilyPanel,AreasOfStudy,Capstone}.tsx`
- Data loaders: `src/lib/data.ts` — `getProgramDetail`, `getProgramEnrichedByCode`, `getDegreeGuideByCode`, `getOfficialResourcePlacementsForSurface`, `getSchools`
- Code alias: `BSSWE` → `BSSWE_Java` artifact via `GUIDE_CODE_ALIASES` in `data.ts`

**Note:** `_internal/page_designs/program_detail.md` is stale (last updated 2026-03-20, pre-guide wiring). Do not use it as a reference for the current page state.

### Live sections (in render order)

1. **Breadcrumb** — `Degrees › {code}`
2. **Header** — inline `{code} · Current|Retired · N CUs`; H1 canonical_name; school link (or plain text if unrecognized); retired last-seen note if applicable
3. **GuideProvenance badge** — shown if `guideArtifact` exists; renders version, pub date, confidence level (amber for medium, red for low), first caveat message as amber pill
4. **About This Degree** — `enriched.description` in blockquote; `description_source` badge; conditional on description being present
5. **Degree History** — compact pill row: first_seen, status, last_seen (if retired), CUs with change note if changed; college name history chain if `colleges.length > 1`
6. **Learning Outcomes** — `enriched.outcomes`; collapsed to first 3, expand button for rest; `outcomes_source` badge; section omitted entirely if `outcomes` absent
7. **Licensure Preparation** (if cert_signals has licensure entries with `atlas_recommendation: use|degree-only`)
8. **Industry Certifications** (if cert_signals has non-licensure entries with `atlas_recommendation: use|degree-only`) — emerald styling, with course links
9. **Related Programs** — `guideArtifact.family`; violet styling; shows track label + sibling links; omitted if `family` is null
10. **Course Roster** — `enriched.roster` grouped by term; rendered when `sp_display_mode` is NOT `suppressed`; advisor-guided caveat banner shown when `sp_display_mode === "advisor-guided"`
11. **Suppressed Roster block** — alternative when `sp_display_mode === "suppressed"`; shows caveat message box in place of table
12. **Areas of Study** — `guideArtifact.areas_of_study`; collapsible group accordion; each group shows course descriptions and competency bullets; omitted if empty
13. **Capstone** — `guideArtifact.capstone`; amber callout; shows "Part of a multi-course capstone sequence." note if `capstone.partial === true`; omitted if `capstone` is null or `capstone.present === false`
14. **Back link** — `← Back to Degrees`
15. **RelevantResources sidebar** — conditional on `official_resource_placements` having sidebar entries for this program code; triggers 2-column layout

---

## 3. What Is Present in Artifacts But Not Surfaced on the Page

These fields exist in every `*_degree_artifact.json` but are never read by the current page:

| Field | What it contains | Why it matters |
|---|---|---|
| `disposition` | `"full-use"` for all current artifacts | Intended as a display gate; currently unused |
| `quality.sp_category` | A / B / C / D classification of SP quality | Could inform a student-facing note about sequence confidence |
| `quality.sp_status` / `quality.aos_status` | `"usable"` or degraded | Same |
| `standard_path.rows` | Full term-by-term SP with CUs (titles only, no codes) | Page renders `enriched.roster` instead; SP rows are unused |
| `guide_provenance.source_page_count` | Page count of source PDF | Low value; informational only |
| `family.display_recommendation` | Text note for how to surface family | Already handled by GuideFamilyPanel; field is redundant |
| `cert_signals[].confidence` | `"high"` etc. | Not shown to student |
| `cert_signals[].source_type` | `"course_mention"` etc. | Not shown to student |
| `anomaly_flags[]` | Specific anomaly codes, e.g. `ANOM-006` | Triggers a generic fallback caveat in GuideProvenance but the specific code is never resolved to a human-readable description |

**Key gap:** `standard_path.rows` exists for all category-A programs and contains term-sequenced CU data per course, but the page never uses it. The roster display comes entirely from `enriched.roster` (matched catalog codes). This is correct behavior — `enriched.roster` has real catalog codes and real CUs — but it means the guide's SP term sequence is only used for `sp_display_mode` detection, not for any display value.

---

## 4. Unresolved / Policy-Needed

| Issue | Description | Default if unresolved |
|---|---|---|
| **AoS placement** | AoS is always below the full course roster. On programs with 37–42 courses (9–10 terms), AoS — which has the richest guide content — is buried deep below the fold. | No change; keep current order |
| **AoS course-code links** | AoS course entries show title + description + competency bullets but have no link to the course's `/courses/{code}` page. The roster above does link course codes. | No links in AoS |
| **Missing outcomes treatment** | When `enriched.outcomes` is absent, the Learning Outcomes section simply disappears. BSSESC (and other education programs) have no outcomes in the enriched data. Is this a product decision or a data gap? | Section absent = data gap; no fallback |
| **Advisor-guided framing** | The advisor-guided caveat says "Advisor-sequenced — individual pacing varies." above the roster. Is this the right framing for a student trying to understand the program? Does it belong above the roster or elsewhere? | Current position: above roster |
| **Caveat visibility** | GuideProvenance badge is small header text. Caveat pill (amber) is the most visible warning but still small. For BSITM (low confidence), the red "low confidence" label in the badge may be easy to miss. | Current: inline badge |
| **Multiple caveat messages** | `quality.caveat_messages_ui` can have multiple entries; only `[0]` is shown. MEDETID has one caveat; no multi-caveat program exists in the current dataset, but the truncation is a latent bug. | Show only first |
| **Capstone caveat double-mention** | MEDETID has a partial capstone: GuideProvenance shows the caveat AND GuideCapstone shows "Part of a multi-course capstone sequence." A student sees the same warning twice in different places. | Current: both visible |
| **Section heading: "Learning Outcomes"** | The section says "Learning Outcomes" but content_map.txt and WGU catalog language says "Program Learning Outcomes." Minor label inconsistency. | Current: "Learning Outcomes" |
| **Known degree names (degree_headings)** | `ProgramRecord.degree_headings` is used internally for heading→code lookup but not displayed on the degree detail page. Some programs have been offered under different degree headings over time. | Not displayed |
| **College rename dates** | College name history shows chain (e.g., College of IT → School of Technology) but without year ranges. The date data exists in `getSchools()` lineage records but is not threaded to degree detail pages. | No dates shown |

---

## 5. What Is Already Strong vs. Weak

### Strong

- **Description + roster + outcomes** render cleanly and are well-sourced. The core factual layer is solid.
- **GuideCertBlock** clearly distinguishes Licensure Preparation (blue) from Industry Certifications (emerald) — visually distinct and well-labeled.
- **GuideFamilyPanel** (violet) is unambiguous. Track label + sibling links are clear.
- **GuideProvenance badge** is present on all guide-wired programs and correctly signals confidence level.
- **College name history chain** is a clean rendering of a complex fact.
- **Suppressed SP handling** (MATSPED) routes the user to AoS as the primary content layer — correct behavior for that edge case.

### Weak

- **AoS is buried.** The richest guide content — per-course descriptions, competency bullets — appears below 37–42 courses and 9–10 terms of roster table. Most users won't scroll there.
- **AoS has no course-code links.** AoS course titles are plain text; the roster above links every course code. This is inconsistent and misses a key navigation opportunity.
- **Provenance/caveat treatment is quiet.** Small badge, small text. For programs with data quality issues (BSITM, MEDETID, MATSPED), the warning is present but may not register.
- **Advisor-guided framing is minimal.** A single amber banner line above the roster. No explanation of what advisor-sequenced means for a student's planning.
- **Missing outcomes is silent.** BSSESC and other education programs show no Learning Outcomes section without any explanation. A student might wonder if outcomes were omitted or simply don't exist.

---

## 6. The 7-Program Review Cohort

Finalized 2026-03-22. These 7 programs cover all distinct live page shapes.

| # | Code | Name | Shape | Why included |
|---|---|---|---|---|
| 1 | BSCS | B.S., Computer Science | Plain baseline | Full enrichment stack; zero guide extras; 37 courses, 9 terms; college rename history. Cleanest possible baseline. |
| 2 | BSSWE | B.S., Software Engineering | Family + professional cert | GuideFamilyPanel (Java/C# tracks) + GuideCertBlock (AWS, CompTIA Project+). Medium confidence (no version/date). Exercises the code-alias mechanism (BSSWE → BSSWE_Java artifact). |
| 3 | BSSESC | B.S., Science Education (Secondary Chemistry) | Advisor-guided + licensure cert | Advisor-guided roster banner + Licensure Preparation block (Praxis exam). No outcomes present — tests the missing-outcomes case. 40 courses, 9 terms. |
| 4 | MATSPED | M.A.T., Special Education | Suppressed SP + anomaly | The only suppressed SP in the entire 115-artifact set. Roster replaced by caveat message; AoS is the primary content layer. Anomaly ANOM-001, medium confidence. |
| 5 | BSDA | B.S., Data Analytics | Capstone + professional cert | GuideCapstone (clean, no caveats) + GuideCertBlock (AWS, CompTIA Project+). High confidence. 42 courses, 10 terms. Baseline for clean capstone rendering. |
| 6 | MEDETID | M.Ed., Education Technology and Instructional Design | Caveat capstone + anomaly | Capstone `partial=true` (first of multi-course sequence). Caveat in both GuideProvenance AND GuideCapstone. Anomaly ANOM-007, medium confidence. Small program: 12 courses, 4 terms. |
| 7 | BSITM | B.S., Information Technology Management | Low confidence + anomaly | Only low-confidence artifact in the dataset. Red "low confidence" badge in GuideProvenance. Roster gap caveat (ANOM-002). "Capstone and Portfolio" AoS group but `capstone.present=false`. |

### Shapes not coverable

- Suppressed SP + cert signals: impossible — MATSPED is the only suppressed program and has no certs.
- Family + capstone: no family program in the dataset has `capstone.present=true`.
- High confidence + anomaly flags: all 5 anomaly programs are medium or low confidence.

---

## 7. Next Step

Review the 7 cohort pages in-browser at `/proto/degree-preview`. Use the content map at `_internal/degree_pages/content_maps/session1_degree_cohort_preview.txt` for discussion without the browser. Record design decisions in Session 2.

Primary questions for the review session:

1. Should AoS move above the roster, or should the roster stay first?
2. Should AoS course entries link to their `/courses/{code}` pages?
3. How should advisor-guided programs frame the sequencing caveat differently from a data-quality caveat?
4. Is the provenance badge visible enough for programs with quality issues?
5. Should missing outcomes trigger a placeholder/explanation, or is absence acceptable?
6. Does the capstone double-mention in MEDETID need to be resolved?
7. Should the roster section be given a source label distinguishing it clearly from the guide-derived AoS?
