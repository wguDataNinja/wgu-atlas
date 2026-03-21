# Program Guide Project Status

**Date:** 2026-03-21

## Current Status

- Phase C (parse+validation corpus build) is complete at 115/115 guides.
- Phase E roster bridge is complete: 115/115 guides bridged to canonical courses.
- Phase E resolution is complete: all 1,599 originally-ambiguous rows resolved or explicitly handled.
- Post-merge enrichment extraction is complete: 751 courses with enrichment data.
- Scraping/extraction phase is **closed**.
- Phase D policy/schema planning is complete; implementation is not started.
- No runtime artifacts are published under `public/data/program_guides/`.

## Human Entry Point

**Start here:** `data/program_guides/README.md`

That README explains the full directory, all subdirectories, key artifacts, and what comes next.

## Where To Read For Specific Needs

| Need | Go to |
|------|-------|
| Full human entry point | `data/program_guides/README.md` |
| Canonical corpus state | `data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md` |
| Phase D decision entry point | `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` |
| Post-merge enrichment counts | `data/program_guides/enrichment/course_enrichment_summary.json` |
| Post-merge bridge state | `data/program_guides/bridge/merge_summary.json` |
| Claims boundaries | `data/program_guides/audit/program_guide_claims_register.md` |
| Adversarial wording check | `data/program_guides/audit/program_guide_adversarial_review.md` |
| Session history | `_internal/program_guides/DEV_NOTES.md` |

## Reconciled Snapshot

- Total guides: 115
- Full-use: 111
- Partial-use: 4 (BSITM, MATSPED, MSCSUG, BSPRN)
- Excluded: 0
- Confidence: 96 HIGH / 17 MEDIUM / 2 LOW
- AoS courses: 2,593; competency sets: 2,591; SP rows: 2,568

## Post-Merge Enrichment Coverage

- 751 courses with enrichment data (descriptions + competencies + program context)
- 730 courses with descriptions; 729 with competencies
- 542 rows still unmapped (titles not in canonical course database — irreducible)
- 6 rows unresolvable (both candidates inactive, no decisive signal)
- 2 medium-confidence LLM resolutions accepted and tracked (`llm_resolved_medium_reviewed`)

## Next Phase

- **Phase D:** Implement `build_guide_artifacts.py` skeleton using the approved policy/schema pack.
  Start from `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md`.
- No runtime wiring or Phase E course-page shipping yet.
