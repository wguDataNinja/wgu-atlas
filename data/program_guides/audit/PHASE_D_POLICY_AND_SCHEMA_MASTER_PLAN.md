# Phase D Policy And Schema Master Plan

**Date:** 2026-03-21
**Scope:** Conservative Phase D policy + schema planning only (no parser expansion, no runtime integration, no Phase E matching)

## 1. Executive Summary
Phase C corpus work is complete and verified. Atlas now has a claim-bounded, fully parsed/validated guide corpus, but none of that guide-derived payload is live on program or course pages yet. Phase D exists to define exactly what can be safely published, in what shape, and with what caveat handling, before any build/integration work begins.

This plan sets a conservative publish policy, ownership model (degree vs course), artifact schema direction, and implementation gates so the next coding step is obvious and low-risk.

## 2. Verified Corpus Result
- Total guides: 115
- Artifact coverage: parsed 115/115, validation 115/115, manifest rows 115/115
- Family-validated coverage: 115/115
- Downstream-usable full: 111
- Downstream-usable partial: 4
- Excluded/not usable: 0
- Confidence: 96 HIGH / 17 MEDIUM / 2 LOW
- Parsed course descriptions: 2593
- Competency sets: 2591
- Standard Path rows: 2568
- Standard Path status: 111 usable / 1 partial / 3 unusable

Why this is complete enough for Phase D: corpus-wide extraction/validation is done, caveat classes are explicit, and no unresolved parser blockers remain for current source corpus.

## 3. What Atlas Can Publish From Guides
### Degree-page publishable payload (Phase D v1)
- Standard Path (title, CU, term when present) for guides with usable/partial SP
- AoS groups and AoS course list
- AoS course descriptions
- Competency bullets (with known empty-course suppression)
- Capstone block where present (with partial flag where needed)
- Optional guide metadata (version/publication/page count) when present

### Course-page publishable payload (Phase D v1)
- **None from guides yet** as first-class guide-derived fields, because course-page attachment depends on Phase E course-code matching.

### Internal-only in Phase D v1
- Parsed prerequisite mentions
- Structured cert-prep attributes (until extraction is formalized)
- Family-specific specialty sections beyond core SP/AoS/capstone model
- Cross-program course appearance context derived from guide titles

## 4. Caveat And Partial-Use Policy
Partial-use means: publish the safe subset, explicitly suppress unsafe subset, and carry machine-readable caveat flags.

- `BSITM`: publish AoS payload; suppress all SP fields.
- `MATSPED`: publish AoS payload; suppress all SP fields.
- `MSCSUG`: publish AoS payload; suppress all SP fields.
- `BSPRN`: publish AoS payload + SP payload labeled as Pre-Nursing-only; do not imply full-program SP coverage.
- `MEDETID`: publish normally but mark capstone as partial.
- `BSNU`: publish normally; metadata omissions are non-blocking.

Never surface as public structured fields in v1: parsed prerequisite mentions.

## 5. Artifact Schema Summary
Recommended output strategy:
- `public/data/program_guides/index.json`
- `public/data/program_guides/guides/{program_code}.json`

Why this shape:
- Per-guide files keep runtime payloads scoped and cacheable.
- Index provides manifest-level discovery and integrity checks.
- Schema encodes disposition + caveats directly so partial-use guides are first-class, not hidden.

Record design principles:
- Separate identity/provenance/quality/payload.
- Preserve source fields (`source_degree_title`) while allowing safe display substitutions (`degree_title_display`).
- Encode SP availability explicitly (`available`, `partial`) to prevent accidental UI overclaim.

Representative examples are formalized in `phase_d_artifact_schema.{md,json}` for:
- normal full-use guide
- partial-use dual-track guide
- capstone-caveat guide
- SP-unusable but AoS-usable guide

## 6. Implementation Plan
Build step should read parsed+validation+manifest plus policy+schema docs, then emit index + per-guide artifacts with strict validations.

Hard-fail conditions:
- corpus count mismatches
- schema-required field omissions
- policy violations (e.g., SP emitted for SP-unusable guide)
- output count divergence from corpus manifest anchors

Warn-only conditions:
- expected known caveat guides
- missing optional metadata
- known empty competency exceptions

Tests required before any runtime wiring:
- policy classifier unit tests
- serializer/schema unit tests
- full-corpus integration count test
- regression test against manifest count anchors

## 7. Exact Recommended Next Step
**Recommended next step: schema + build-script skeleton (only).**

Bounded scope for next coding session:
1. Create `scripts/program_guides/build_guide_artifacts.py` skeleton that loads inputs and validates anchors.
2. Implement schema serializer + policy classifier with unit tests.
3. Emit non-runtime test output to a temporary path for verification.
4. Do **not** wire program pages in the same session.

This keeps risk low while moving directly from planning into implementation readiness.

## 8. Supporting Artifacts From This Session
- `data/program_guides/audit/phase_d_publish_policy.md`
- `data/program_guides/audit/phase_d_publish_policy.json`
- `data/program_guides/audit/phase_d_artifact_schema.md`
- `data/program_guides/audit/phase_d_artifact_schema.json`
- `data/program_guides/audit/phase_d_degree_course_ownership_matrix.md`
- `data/program_guides/audit/phase_d_degree_course_ownership_matrix.json`
- `data/program_guides/audit/phase_d_build_plan.md`
- `data/program_guides/audit/phase_d_build_plan.json`
