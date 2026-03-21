# graduate_standard Family Rollout Summary

**Date:** 2026-03-21
**Gate guide:** MBA (HIGH confidence, 0 anomalies, 0 warnings)
**Parser changes:** none

## Results

9/9 guides parsed. 0 failures. 8 HIGH / 1 MEDIUM / 0 LOW.

| Code | Degree | Confidence | SP Format | SP Rows | AoS Groups | AoS Courses | Capstone | Notes |
|------|--------|------------|-----------|---------|------------|-------------|---------|-------|
| MSCIN | M.S. Curriculum and Instruction | HIGH | 3-col multiline | 10 | 4 | 10 | — | header-line metadata |
| MSHRM | M.S. Human Resource Management | HIGH | 3-col multiline | 10 | 4 | 10 | — | header-line metadata |
| MSIT | M.S. Information Technology | HIGH | 3-col multiline | 11 | 2 | 11 | — | header-line metadata |
| MSITM | M.S. IT Management | **MEDIUM** | 3-col multiline | 10 | 4 | 9 | ✓ | capstone description polluted (see below) |
| MSITPM | M.S. IT — Product Management | HIGH | 3-col multiline | 10 | 2 | 10 | — | header-line metadata |
| MSITUG | B.S. IT (BSIT to MSIT pathway) | HIGH | 3-col multiline | **35** | 12 | 35 | — | bridge guide; 35 courses (all clean) |
| MSMK | M.S. Marketing, Digital Marketing | HIGH | 3-col multiline | 11 | 2 | 11 | — | |
| MSMKA | M.S. Marketing, Analytics | HIGH | 3-col multiline | 11 | 2 | 11 | — | |
| MSML | M.S. Management and Leadership | HIGH | 3-col multiline | 10 | 4 | 9 | ✓ | capstone: 0 bullets (no trigger in source) |

**Quality:** 0 empty descriptions, 0 empty competency lists across all 9 guides.

## MEDIUM Case — MSITM

**Cause:** Source PDF typo. The closing section reads "Accessibility and Accomodations" (single 'm') instead of "Accessibility and Accommodations" (double 'm'). `ACCESSIBILITY_RE` does not match. The capstone section has no competency trigger block. Result: the capstone parser accumulates `description_buf` through the boilerplate and to EOF. Capstone title is correct; opening description paragraph is correct; remainder is polluted with accessibility/student-services boilerplate text.

**Impact:** Capstone description for MSITM is not usable. AoS content (9 courses, all descriptions, all competencies) is entirely unaffected.

**Parser change:** None made. Fixing requires either relaxing ACCESSIBILITY_RE to tolerate the typo or adding a secondary anchor. Deferred — isolated to 1 guide; AoS content is the primary value and is clean.

## Structural Notes

**SP format:** All 9 guides use 3-column multiline (Course Description / CUs / Term). No 2-column or single-line format variant found. No parser branching needed.

**Metadata formats:** MSCIN, MSHRM, MSIT, MSITPM, MSITUG use header-line metadata (page_count=0 cosmetic gap); MSITM, MSMK, MSMKA, MSML use footer-based metadata.

**Capstone bullet behavior:** MSITM and MSML both have capstones with 0 competency bullets. Graduate capstone sections in this family do not include the "This course covers the following competencies:" trigger. This is a source-guide format property, not a parser deficiency. Capstone titles and descriptions (excluding MSITM) are clean.

**MSITUG pathway note:** MSITUG covers a BSIT-to-MSIT bridge curriculum with 35 courses — significantly larger than the typical 10-11 course graduate guide. Parser handles it identically; no branching needed. Family classification as `graduate_standard` is accurate.

## Safe Fields for Downstream Use

- Standard Path course titles, CU values, term sequence — all 9 guides
- AoS group structure — all 9 guides
- Course descriptions — all 9 guides, 0 empty
- Competency bullets — all 9 guides, 0 empty
- Guide metadata (version, pub_date) — all 9 guides (MSITM version 201808 is old but present)

## Fields to Exclude

- MSITM capstone description — polluted with boilerplate text
- Capstone competency bullets for MSITM and MSML — 0 bullets is source-guide property; not extractable
