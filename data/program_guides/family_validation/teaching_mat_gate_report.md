# teaching_mat Family Gate Report

**Date:** 2026-03-21
**Gate guide:** MATELED
**Family size:** 9 guides
**Parser changes:** 1 bug fix (© line date extraction — see below)

## Gate Result

**PASS — MATELED HIGH confidence, 0 anomalies, 0 warnings. 28/28 perfect reconciliation.**

| Code | Degree | Confidence | SP Format | SP Rows | AoS Groups | AoS Courses | Capstone |
|------|--------|------------|-----------|---------|------------|-------------|---------|
| MATELED | M.A.T., Elementary Education | HIGH | 3-col multiline (with Term) | 28 | 5 | 28 | — |

**Quality:** 0 empty descriptions, 0 empty competency lists.

## AoS Group Structure

| Group | Courses |
|-------|---------|
| Professional Core | 7 |
| General Education | 1 |
| Elementary Education | 15 |
| Clinical Experiences | 3 |
| Student Teaching | 2 |

## Parser Bug Fixed — © Line Date Extraction

**Bug:** `extract_metadata()` extracted `"University8/16/24"` instead of `"8/16/24"` for MATELED. The last © footer line in the file (`line 1037`) had no space between "University" and "8/16/24" — a source PDF formatting artifact. The old handler used `parts[-1]` (last whitespace-split token), which in this case was `"University8/16/24"`.

**Fix:** Replaced `parts[-1]` with `re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', line).group(1)`. Extracts the date pattern directly regardless of surrounding whitespace. No change for guides where the date is correctly space-delimited.

**Regression check:** BSDA, BSMGT, BSCSIA, MBA, MBAITM, BSCS, BSPSY — all verified unchanged after fix.

## Structural Notes

- **SP format:** 3-column multiline (with Term). MATELED is a graduate degree — same SP format as graduate_standard and mba families. Differs from education_ba teacher-licensure guides (2-column, no Term).
- **Clinical Experiences / Student Teaching:** Appear as AoS group labels — same pattern as education_ba (BAELED, BASPEE). No new handler needed.
- **Metadata format:** Split footer (code+version / © line / page number on separate lines). Same as BSCS, BSPSY.
- **No Capstone section.** Handled gracefully.

## Rollout Recommendation

**Proceed with teaching_mat full rollout.** Risk is low — all observed patterns are extensions of validated behavior. Watch for during rollout:
- Non-Elementary subject variants (Math, Science, Special Ed) may have different AoS group sets, but core structure should be identical.
- Confirm whether all 9 guides use 3-column SP (expected for graduate MAT degree) or whether any use 2-column.
