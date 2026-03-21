# mba Family Rollout Summary

**Date:** 2026-03-21
**Gate guide:** MBA (served as gate for graduate_standard; mba family is all-HIGH manifest)
**Parser changes:** 1 bug fix — `locate_sections()` Capstone detection (see below)

## Results

3/3 guides parsed. 0 failures. **3 HIGH / 0 MEDIUM / 0 LOW.**

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone | Notes |
|------|--------|------------|---------|------------|-------------|---------|-------|
| MBA | M.B.A. | HIGH | 11 | 7 | 10 | ✓ (2 bullets) | footer metadata |
| MBAHA | M.B.A., Healthcare Administration | HIGH | 11 | 8 | 10 | ✓ (2 bullets) | header-line metadata; re-parsed after fix |
| MBAITM | M.B.A., IT Management | HIGH | 11 | 9 | 10 | ✓ (2 bullets) | footer metadata |

**Quality:** 0 empty descriptions, 0 empty competency lists. All 3 guides: 11/11 perfect reconciliation.

## Parser Bug Fixed

**Bug:** `locate_sections()` Capstone detection had a blind spot when a guide contains both a bare "Capstone" row in the Standard Path table *and* a real "Capstone" section heading after Areas of Study.

**Cause:** The old implementation used an early-stop guard (`'Capstone' not in found`) so only the first occurrence was recorded. The post-scan filter then deleted this pre-AoS entry — but the real Capstone section (occurring later) was never recorded.

**Fix:** Collect all `Capstone` line indices during the scan; after scanning, filter to only those appearing after Areas of Study; take the first. No behavioral change for guides with only one Capstone occurrence.

**Regression check:** BSDA, BSMGT, BSCSIA, MBA — all verified unchanged after fix.

**MBAHA impact:** MBAHA parsed as MEDIUM (1 SP/AoS warning) before the fix, HIGH after. Re-parsed and updated artifacts reflect the corrected output.

## Structural Notes

- All 3 MBA guides use 3-column multiline SP format. No format variants.
- All 3 have explicit Capstone sections with competency bullets. MBA family capstones use the full competency trigger block — unlike graduate_standard where capstones had 0 bullets.
- Metadata formats: MBA and MBAITM use old footer format (version 201404, 201408 respectively); MBAHA uses modern header-line format.

## Safe Fields for Downstream Use

All fields are clean for all 3 MBA guides:
- Standard Path course titles, CU values, term sequence
- AoS group structure
- Course descriptions (0 empty)
- Competency bullets (0 empty)
- Capstone title, description, competency bullets
- Guide metadata (version, pub_date)
