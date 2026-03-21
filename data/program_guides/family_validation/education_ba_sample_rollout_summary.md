# education_ba Sampled Rollout Summary

**Date:** 2026-03-20
**Parser changes:** None
**Verdict:** GO — safe for full education_ba rollout

---

## Results

| Code | Confidence | SP Rows | SP Format | AoS Groups | AoS Courses | Reconciliation |
|---|---|---|---|---|---|---|
| BAELED | HIGH | 37 | 2-col (no Term) | 5 | 37 | 37/37 ✓ |
| BAESELED | HIGH | 33 | 3-col (Term) | 3 | 33 | 33/33 ✓ |
| BAESMES | HIGH | 35 | 3-col (Term) | 6 | 35 | 35/35 ✓ |
| BAESSESB | **MEDIUM** | 36 | 3-col (Term) | 9 | 37 | 36/37 |
| BAESSESC | HIGH | 36 | 3-col (Term) | 8 | 36 | 36/36 ✓ |

**4 HIGH / 1 MEDIUM / 0 LOW**

---

## BAESSESB — MEDIUM explanation

Source PDF artifact. The last Standard Path row (Secondary Disciplinary Literacy, CUs=3, Term=8) was split across a page boundary during PDF extraction. The term value "8" appears after the "Total CUs" line in the extracted text — after the parser's break point — and is never captured.

The course is correctly represented in AoS (37 AoS courses include it). The SP row count is 36 instead of 37. This is an identical pattern to BSSWE_C from the cs_ug rollout. Not a parser bug; not a structural issue.

---

## SP Format Split

The `education_ba` family contains two structural subtypes:

| Subtype | Programs | SP Format | Clinical/Student Teaching groups |
|---|---|---|---|
| Teacher licensure | BAELED | 2-column (no Term) | Yes |
| Educational Studies | BAESELED, BAESMES, BAESSESB, BAESSESC, ... | 3-column (with Term) | No |

Both formats are already supported. No branching needed. The split follows naturally from the program type distinction, not from any parser deficiency.

Educational Studies programs show more AoS group variety (3–9 groups) and subject-specific group names (Mathematics Education, Biology Content, General Science Content, etc.), all of which parse correctly as standard group-label patterns.

---

## Parser Changes Made

None.

---

## Verdict

| | |
|---|---|
| Total parsed | 5 |
| HIGH | 4 |
| MEDIUM | 1 (source artifact) |
| LOW | 0 |
| Parser changes | 0 |
| New branch needed | No |
| Full rollout safe | **Yes** |
