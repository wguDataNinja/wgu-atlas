# Program Guides — Data Directory

**Human entry point for the WGU program-guide data area.**

---

## Current status

**The program-guides workstream has reached its current stopping point.**

- Guide extraction, artifact generation, degree-page wiring, cert framing, and caveat handling are all complete.
- Guide-derived content is live on Atlas degree pages.
- `data/program_guides/` is no longer the active working directory.
- Next major work is in the official-resource layer and course-page enrichment — not here.

**To resume guide-adjacent work later:** narrow follow-ups are listed at the bottom of this file. None are urgent.

---

## What this directory is

WGU publishes a Program Guidebook PDF for every active degree. This directory contains everything produced by extracting structured data from those PDFs — 115 guides covering every active program.

The extracted data includes:
- Course descriptions and competency bullets (per course, per program)
- Program schedule context (Standard Path: term, credit units)
- Course-to-program mappings (which courses appear in which programs)

---

## What is built and wired

| Layer | Status |
|---|---|
| Guide corpus collected and parsed | **Complete** — 115/115 guides |
| Per-course descriptions and competency bullets extracted | **Complete** — 2,593 courses covered |
| Guide courses matched to Atlas catalog codes | **Complete** — 751 matched; 542 unmatched (irreducible) |
| Cert → course mapping | **Complete** — 9 auto-accepted, 21 review-needed |
| Prereq relationship artifact | **Complete** — 50 auto-accepted, 21 review-needed |
| SP family classification | **Complete** — 115 programs, 7 named families |
| Anomaly registry | **Complete** — 9 records with handling rules |
| Degree-level cert signals (NCLEX-RN, CPA Exam, Praxis) | **Complete** — program-description pass done |
| Degree artifact generator (`build_guide_artifacts.py`) | **Built and run** — 115 per-program artifacts in `degree_artifacts/` |
| Guide data wired to Atlas degree pages | **Live** — Sessions 32–35 |

**Nothing in this directory needs to be rebuilt or re-run** unless new guides are added or a bug is found.

---

## What is on degree pages now

The following guide-derived sections appear on `programs/[code]` pages:

- **Licensure Preparation block** — for programs with NCLEX-RN or Praxis exam signals (9 programs)
- **Industry Certifications block** — cert badges with course links (19 programs; 9 auto-accepted cert→course rows)
- **Family/track panel** — sibling program links for all 19 Category C programs across 7 families
- **Areas of Study** — guide-derived course descriptions and competency bullets (collapsible, per-group)
- **Capstone callout** — capstone course identification with description (15 programs)
- **Guide provenance badge** — source version and date in degree header
- **Caveat banners** — specific messages for BSITM, MATSPED, MSCSUG, BSPRN, MEDETID, BSNU
- **Advisor-sequenced label** — for all 23 Category B (null-term) education/licensure programs

---

## Artifact inventory

### Degree artifact files (the live output)

| File / Directory | Contents | Status |
|---|---|---|
| `degree_artifacts/` | 115 per-program degree artifact JSONs + manifest | **Live — wired to degree pages** |
| `degree_artifacts/manifest.json` | Corpus-level summary: SP categories, cert/family/capstone/anomaly counts | Complete |
| `degree_level_cert_signals.json` | Degree-level cert signals from program descriptions: NCLEX-RN (BSPRN), Certified Public Accountant (CPA) Exam (MAcc family) | Complete |

### Target extraction artifacts (Session 29)

| File | Contents | Status |
|---|---|---|
| `cert_course_mapping.json` | 9 auto-accepted cert→course rows + 21 review-needed | Complete |
| `prereq_relationships.json` | 50 auto-accepted prereq relationships + 21 review-needed | Complete |
| `sp_family_classification.json` | Per-program SP classification A/B/C/D for all 115 programs | Complete |
| `sp_families.json` | 7 named family definitions with member lists and shared course counts | Complete |
| `guide_anomaly_registry.json` | 9 anomaly records with detection, source-side classification, and Atlas handling rules | Complete |
| `guide_manifest.json` | Earlier-phase guide structure manifest (presence flags and structural counts per guide) | Complete |

### Source and pipeline artifacts

| Directory | Contents |
|---|---|
| `parsed/` | 115 `*_parsed.json` files — canonical guide content. Do not regenerate without a parser fix. |
| `validation/` | 115 `*_validation.json` files — per-guide confidence and anomaly flags |
| `manifest_rows/` | 115 `*_manifest_row.json` files — compact per-guide summary rows |
| `bridge/guides_merged/` | Final course-matching output — canonical. Downstream enrichment reads from here. |
| `enrichment/course_enrichment_candidates.json` | 751 courses with guide-derived enrichment data |
| `enrichment/course_enrichment_summary.json` | Coverage counts and match-tier distribution |
| `audit/` | Policy docs, schemas, claims register, corpus manifest, degree-enrichment design pack |
| `family_validation/` | Historical per-family gate reports and rollout summaries |

---

## Numbers that matter

- 115/115 guides parsed and validated
- 111 fully usable / 4 partially usable / 0 excluded
- Parse confidence: 96 HIGH / 17 MEDIUM / 2 LOW
- 2,593 course descriptions extracted across all guides
- **751 canonical courses** with guide-derived enrichment
- 542 unmatched guide titles — irreducible without catalog changes
- 9 auto-accepted cert→course mappings (degree pages use these)
- 50 auto-accepted prereq relationships (ready; not yet on course pages)
- 7 named program families, 19 family-member programs
- 23 advisor-guided (null-term) programs — all education licensure

---

## Approved vs review-queued vs still missing

### Approved and live on degree pages

- All 9 auto-accepted cert→course rows → cert badges
- NCLEX-RN → Licensure Preparation block on BSPRN
- Certified Public Accountant (CPA) Exam → cert block on MAcc family (5 programs)
- Praxis exam → Licensure Preparation block on 8 education programs
- All 7 family definitions → family panels
- SP category A/B/C/D → drives SP display mode
- Anomaly handling rules → per-program caveat banners

### Review-queued (not yet on site)

- 21 cert review-needed rows — mostly vendor-platform strings (AWS CLI, Azure CLI, Cisco DevNet) needing editorial judgment. See `cert_course_mapping.json`.
- 21 prereq review-needed rows — includes 16 nursing cumulative-sequence prereqs (need display design) and inverted-capture cases. See `prereq_relationships.json`.

### Still missing (would require further work)

- **Prereq display on course pages** — 50 auto-accepted relationships are ready; course-page component not built.
- **Course-page guide enrichment** — 751 courses have descriptions/bullets; course pages don't show them yet. Needs variant selection policy first.
- **Multi-description/competency variant policy** — 74 courses with multiple description variants, 185 with multiple competency variants. One policy decision unblocks course-page use.
- **Education content-area sub-families** — cross-degree-level sibling groupings not captured. Low priority.
- **MEDETID full capstone** — only first of 3 capstone courses captured (ANOM-007). Partial note is shown on the degree page.

---

## Known narrow follow-ups if guide work resumes

These are bounded, completable items — none require re-extraction or re-parsing:

1. **Resolve cert review queue** — 21 rows; editorial review against source text; likely 4–6 get promoted to `degree-only`, rest suppressed.
2. **Prereq display on course pages** — build the course-page prereq component; 50 auto-accepted rows are ready as input.
3. **Nursing cumulative prereq display** — 16 rows need a distinct "all prior terms" display model.
4. **Multi-description variant policy** — one decision unblocks course-page enrichment for 751 courses.

---

## Where to start reading

| Need | Go to |
|---|---|
| What is live on degree pages | `degree_artifacts/manifest.json` |
| Full product handoff | `_internal/program_guides/GUIDE_ARTIFACTS_PRODUCT_HANDOFF.md` |
| Corpus facts (canonical counts, confidence) | `audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md` |
| Safe claim boundaries | `audit/program_guide_claims_register.md` |
| Degree-enrichment policy and schema | `audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` |
| Enrichment coverage counts | `enrichment/course_enrichment_summary.json` |
| Course-matching audit decisions | `bridge/merge_summary.json` |

---

## What is canonical vs intermediate vs historical

| Category | Examples | Notes |
|---|---|---|
| **Canonical — do not modify** | `parsed/`, `validation/`, `manifest_rows/` | Source of truth for guide content |
| **Canonical — live output** | `degree_artifacts/`, `degree_level_cert_signals.json` | What degree pages read |
| **Canonical — current state** | `bridge/guides_merged/`, `enrichment/`, `bridge/merge_summary.json` | Final course-matching and enrichment state |
| **Canonical — decisions** | `audit/PROGRAM_GUIDE_CORPUS_MANIFEST.*`, `audit/program_guide_claims_register.*`, `audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` | What was decided and why |
| **Intermediate — pipeline stages** | `bridge/guides/`, `bridge/guides_resolved/`, `bridge/llm_packets/` | Preserved for auditability |
| **Historical / background** | Most other `audit/` files | Useful reference; not required for ongoing work |

---

## Partial-use and excluded guides

| Guide | Issue | Degree-page handling |
|---|---|---|
| BSITM | SP entry suppressed (concatenation artifact) | Caveat banner; rest of SP shown |
| MATSPED | SP fully suppressed (catastrophic concatenation) | SP replaced by caveat message; AoS shown |
| MSCSUG | SP is accelerated B.S./M.S. bridge | Caveat banner: "term sequence spans both degree levels" |
| BSPRN | SP covers Pre-Nursing track only | SP labeled; nursing-track courses in AoS |
| BSNU | No footer metadata | Content intact; provenance badge shows no version/date |
| MEDETID | Capstone partial (first of 3 courses only) | Caveat banner; capstone shown with partial note |
