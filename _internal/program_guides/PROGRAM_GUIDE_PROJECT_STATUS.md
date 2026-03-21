# Program Guide Project Status

**Date:** 2026-03-21

## Current Status

Guide data collection and extraction is **complete**.

- All 115 WGU program guidebooks have been collected, parsed, and validated.
- Per-course structured data (descriptions, competency bullets, program schedule context) has been extracted for all guides.
- Guide-derived enrichment data is now available for 751 canonical courses — ready to inform Atlas degree pages and, later, course pages.
- The next step is building the first Atlas-facing output layer: artifacts that publish approved guide content to degree pages.
- Nothing is yet published to the site from this data.

**Post-program-guides direction:** The project is now centered on three tracks:
1. **Degrees** - immediate implementation target using completed guide data
2. **Courses** - major follow-on opportunity with 751 enriched courses
3. **Homepage** - sequenced after inner-surface strengthening

**Guide targets extraction complete (2026-03-21):** Cert mapping, prereq relationships, SP family classification, and anomaly registry are all produced. See new artifacts below.

## Human Entry Point

**Start here:** `data/program_guides/README.md`

That README explains the full directory, what each area contains, what is canonical vs internal, and what comes next.

## Where To Read For Specific Needs

| Need | Go to |
|------|-------|
| Full human entry point | `data/program_guides/README.md` |
| What the corpus covers (counts, confidence, caveats) | `data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md` |
| What claims are safe to make about this data | `data/program_guides/audit/program_guide_claims_register.md` |
| How to build Atlas degree-page artifacts from this data | `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` |
| Current enrichment coverage numbers | `data/program_guides/enrichment/course_enrichment_summary.json` |
| Course-matching audit (which courses resolved, which did not) | `data/program_guides/bridge/merge_summary.json` |
| Cert → course mapping (Phase 1 targets output) | `data/program_guides/cert_course_mapping.json` |
| Prereq relationships (Phase 2 targets output) | `data/program_guides/prereq_relationships.json` |
| SP family classification (Phase 3 targets output) | `data/program_guides/sp_family_classification.json` |
| SP family definitions (Phase 3 targets output) | `data/program_guides/sp_families.json` |
| Guide anomaly registry (Phase 4 targets output) | `data/program_guides/guide_anomaly_registry.json` |
| Session history | `_internal/program_guides/DEV_NOTES.md` |

## Corpus Snapshot

- Total guides: 115 (100% of active programs)
- Fully usable: 111 guides
- Partially usable: 4 guides (BSITM, MATSPED, MSCSUG, BSPRN — see README for caveats)
- Excluded: 0
- Parse confidence: 96 HIGH / 17 MEDIUM / 2 LOW
- Descriptions extracted: 2,593 (100% of guide courses)
- Competency sets: 2,591
- Program schedule rows: 2,568

## Course Enrichment Coverage

- **751 canonical courses** now have guide-derived enrichment (descriptions + competency bullets + program context)
- 730 with descriptions; 729 with competency bullets
- 542 courses remain unmatched (guide titles not in the canonical course catalog — not resolvable without catalog updates)
- 6 courses excluded due to ambiguous inactive candidates with no decisive signal

## Guide Targets Extraction Results (2026-03-21)

| Artifact | Content | Status |
|---|---|---|
| `cert_course_mapping.json` | 9 auto-accepted cert→course mappings (≥3 programs each), 21 review-needed | Complete |
| `prereq_relationships.json` | 50 auto-accepted prereq relationships, 21 review-needed, 71 total | Complete |
| `sp_family_classification.json` | 115 programs classified A(72)/B(23)/C(19)/D(1) | Complete |
| `sp_families.json` | 7 named family definitions with member lists and shared course counts | Complete |
| `guide_anomaly_registry.json` | 9 anomaly records covering all known issue types | Complete |

**Cert mapping highlights:** CompTIA A+ (7 programs), AWS Certified (6), CompTIA Network+ (6), CompTIA Project+ (6), CompTIA Security+ (6), CompTIA Cloud+ (4), Praxis exam (4 programs, 2 courses).

**Prereq chain highlights:** Data Management chain (8 programs), Introduction to Business Accounting (6), Network/Security chain (6), CS/math chains (Calculus I→II→III, Discrete Math I→II, Applied Algebra→Discrete Math).

**SP families:** BSSWE (2 tracks, 33 shared courses), MACC (4 tracks, 6 shared), MSRNN (3 specializations, 25 shared), BSCNE (4 vendor tracks, 26 shared), PMCNU (4 specializations, 0 shared), MSMK (2 specializations, 8 shared), BAELED (licensure variant, 33 shared).

## What Is Next

Build the **Atlas degree-enrichment artifact generator**: a script that reads the extracted guide data, applies the approved inclusion policy, and produces Atlas-ready JSON for degree pages.

- Policy and schema decisions are already settled — see `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md`.
- Guide targets extraction outputs (cert mapping, prereq relationships, SP families) unlock cert badges, prereq display, and family relationship surfaces on degree and course pages.
- No runtime wiring or course-page publishing in this next step.
- College-level uses of this data remain possible later.
