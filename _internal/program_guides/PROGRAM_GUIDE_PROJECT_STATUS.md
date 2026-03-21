# Program Guide Project Status

**Date:** 2026-03-21

## Current Status

Guide data collection and extraction is **complete**.

- All 115 WGU program guidebooks have been collected, parsed, and validated.
- Per-course structured data (descriptions, competency bullets, program schedule context) has been extracted for all guides.
- Guide-derived enrichment data is now available for 751 canonical courses — ready to inform Atlas degree pages and, later, course pages.
- The next step is building the first Atlas-facing output layer: artifacts that publish approved guide content to degree pages.
- Nothing is yet published to the site from this data.

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

## What Is Next

Build the **Atlas degree-enrichment artifact generator**: a script that reads the extracted guide data, applies the approved inclusion policy, and produces Atlas-ready JSON for degree pages.

- Policy and schema decisions are already settled — see `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md`.
- No runtime wiring or course-page publishing in this next step.
- College-level uses of this data remain possible later.
