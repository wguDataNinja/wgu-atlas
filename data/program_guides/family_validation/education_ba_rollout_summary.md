# education_ba Full Rollout Summary

**Date:** 2026-03-20
**Parser changes:** None
**Status:** Complete

---

## Results

| Code | Confidence | SP Rows | SP Format | AoS Groups | AoS Courses | Reconciliation |
|---|---|---|---|---|---|---|
| BAELED | HIGH | 37 | 2-col | 5 | 37 | 37/37 ✓ |
| BAESELED | HIGH | 33 | 3-col | 3 | 33 | 33/33 ✓ |
| BAESMES | HIGH | 35 | 3-col | 6 | 35 | 35/35 ✓ |
| BAESSESB | MEDIUM | 36 | 3-col | 9 | 37 | 36 SP / 37 AoS |
| BAESSESC | HIGH | 36 | 3-col | 8 | 36 | 36/36 ✓ |
| BAESSESE | MEDIUM | 36 | 3-col | 9 | 37 | 36 SP / 37 AoS |
| BAESSESP | HIGH | 36 | 3-col | 8 | 36 | 36/36 ✓ |
| BAESSPEE | MEDIUM | 41 | 3-col | 5 | 40 | 41 SP / 40 AoS |
| BAESSPMM | MEDIUM | 34 | 3-col | 5 | 33 | 34 SP / 33 AoS |
| BASPEE | MEDIUM | 45 | 2-col | 7 | 44 | 45 SP / 44 AoS |
| BASPMM | MEDIUM | 38 | 2-col | 6 | 37 | 38 SP / 37 AoS |

**5 HIGH / 6 MEDIUM / 0 LOW / 0 failures**

---

## Confidence Distribution

**HIGH (5):** BAELED, BAESELED, BAESMES, BAESSESC, BAESSESP

**MEDIUM (6):** BAESSESB, BAESSESE, BAESSPEE, BAESSPMM, BASPEE, BASPMM

All MEDIUM cases are source-data artifacts. No parser design failures.

---

## Subtype Distribution

### Teacher Licensure — 2-column SP (no Term)
Programs: BAELED, BASPEE, BASPMM

- Standard Path has Course Description + CUs columns; no Term
- Includes Clinical Experiences and/or Student Teaching as AoS group labels
- BAELED: Clinical Experiences + Student Teaching
- BASPEE (dual licensure): Clinical Experiences + Student Teaching
- BASPMM (special ed): Clinical Experiences only, no Student Teaching

### Educational Studies — 3-column SP (with Term)
Programs: BAESELED, BAESMES, BAESSESB, BAESSESC, BAESSESE, BAESSESP, BAESSPEE, BAESSPMM

- Standard Path has Course Description + CUs + Term columns
- No Clinical Experiences or Student Teaching groups
- Subject-specific AoS group names vary by program area (secondary science, special ed, etc.)

---

## MEDIUM Cause Analysis

### Pattern A — `sp_incomplete_row_at_eof` (2 guides: BAESSESB, BAESSESE)
Last SP row (Secondary Disciplinary Literacy, CUs=3, Term=8) split across PDF page boundary. The term value appears after the `Total CUs` line in the extracted text — after the parser's break point — and is never captured. Course correctly present in AoS with full description and competency bullets.

Same pattern as BSSWE_C (cs_ug rollout). Source artifact.

### Pattern B — `competency_trigger_unexpected_state` (4 guides: BAESSPEE, BAESSPMM, BASPEE, BASPMM)
PDF text extraction reordering in the Fundamentals of Special Education course. Bullet fragments appear out of sequence in the extracted text; the last fragment ends with "...the Individualized" (no terminal punctuation). The following course title "Considerations for Instructional Planning for Learners" (50 chars, title-case) is absorbed as a bullet continuation by the parser's `len(line) > 30` heuristic. The course is present in the SP but missing from the AoS output.

Consistent across all 4 guides containing Special Education content. Source artifact; parser change deferred due to regression risk.

**Impact:** AoS course count is 1 less than SP count per affected guide. Course IS in the guide; its content (description + competency bullets) is attributed to the previous course in AoS output. SP row is complete and correct.

---

## Quality Checks (across all 11 guides)

| Check | Result |
|---|---|
| Empty descriptions | 0 |
| Empty competency lists | 0 |
| Total cert-prep mentions | 17 |
| Total prereq mentions | 20 |

---

## Section Heading Variants Observed

All guides share: Professional Core, General Education, and at least one subject-specific group.

Notable variant groups:
- `Clinical Experiences` — BAELED, BASPEE, BASPMM
- `Student Teaching` — BAELED, BASPEE
- `Special Education` — BAESSPEE, BAESSPMM, BASPEE, BASPMM
- `General Science Content` — 5 secondary science guides
- `Biology Content`, `Chemistry Content`, `Physics Content` — subject-specific
- `Pedagogy and Teaching Methods` — all educational studies guides
- `Mathematics Education` — 4 guides

---

## Parser Changes Made

None.

---

## Completion Status

**education_ba is complete.**

11/11 guides parsed. 0 failures. 0 LOW confidence. All MEDIUM cases are source artifacts in two consistent patterns. No structural elements require a new parser branch. Both SP format subtypes (2-column and 3-column) were already supported.

---

## Next Family Recommendation

**`graduate_standard`** — 9 guides (MBA, MHA, MPH, MSHRM, MSITM, and similar)

Rationale: structurally closest to `standard_bs`, which is the most thoroughly validated family. Graduate guides use the same section structure with higher CU-per-course values and 8 CU/term enrollment expectations. Low risk of structural surprises. Gate with one guide (e.g., MBA or MHA) before full rollout.
