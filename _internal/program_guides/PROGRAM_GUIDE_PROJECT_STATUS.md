# Program Guide Project Status

**Date:** 2026-03-21

## Current Status

- Phase C (parse+validation corpus build) is complete at 115/115 guides.
- Post-close verification is complete; reconciled counts and claims are documented.
- Phase D policy/schema planning is complete; implementation is not started.
- No runtime artifacts are published under `public/data/program_guides/`.

## Where To Read First

- Canonical corpus state: `data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md`
- Phase D decision entry point: `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md`
- Phase D publish policy: `data/program_guides/audit/phase_d_publish_policy.md`
- Phase D artifact schema: `data/program_guides/audit/phase_d_artifact_schema.md`
- Claims boundaries: `data/program_guides/audit/program_guide_claims_register.md`
- Adversarial wording check: `data/program_guides/audit/program_guide_adversarial_review.md`
- Existing session history: `_internal/program_guides/DEV_NOTES.md`

## Reconciled Snapshot

- Total guides: 115
- Full-use: 111
- Partial-use: 4 (BSITM, MATSPED, MSCSUG, BSPRN)
- Excluded: 0
- Confidence: 96 HIGH / 17 MEDIUM / 2 LOW
- AoS courses: 2,593; competency sets: 2,591; SP rows: 2,568

## Next Phase

- Proceed to Phase D build-script skeleton implementation using the approved policy/schema pack.
- Keep runtime wiring and Phase E matching out of scope for the next coding session.
