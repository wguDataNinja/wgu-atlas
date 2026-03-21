# Phase D Build Plan

**Version:** phase_d_build_plan_v1  
**Date:** 2026-03-21

## Inputs
- parsed/validation/manifest-row artifacts (115 each)
- corpus manifest (count anchors)
- phase_d_publish_policy.json
- phase_d_artifact_schema.json

## Transform
1. Join by `program_code`
2. Apply disposition + caveat policy
3. Materialize safe payload only
4. Emit `index.json` + per-guide files

## Validation Gates
### Hard Fail
- count mismatches
- schema-required key missing
- SP emitted for SP-unusable guide
- output guide count != manifest total

### Warn Only
- expected caveat guides
- optional metadata missing
- expected empty competency exceptions

## Tests
- classifier unit tests
- serializer/schema unit tests
- full-corpus integration count test
- regression against manifest anchors

## Recommended Next Implementation Step
`schema + build-script skeleton` only. No runtime page wiring in the same session.
