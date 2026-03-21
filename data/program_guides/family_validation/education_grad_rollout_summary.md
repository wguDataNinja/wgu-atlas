# education_grad — Rollout Summary (Complete — MSEDL + MEDETID)
**Date:** 2026-03-21 (MSEDL); 2026-03-21 (MEDETID via Bucket 2)
**Result:** COMPLETE — both guides rolled out

---

## Summary

| Code | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone | Status |
|------|------------|---------|------------|-------------|----------|--------|
| MSEDL | HIGH | 13 | 3 | 13 | — | COMPLETE (Session 21) |
| MEDETID | MEDIUM | 12 | 4 | 9 | yes | COMPLETE (Session 22) |

**MSEDL: HIGH, 0 anomalies, 0 warnings. MEDETID: MEDIUM, 0 anomalies, 1 warning (2 capstone sequence courses in SP but not in AoS — structural, not a parser failure).**

---

## Downstream exclusions

None. Both guides are usable downstream, with caveats for MEDETID noted below.

---

## Known caveats

- **MSEDL**: Phase A manifest flagged a Practicum section as a potential parser gap. Practicum is an ordinary AoS course — no parser issue.
- **MEDETID**: Multi-specialization guide with 3 embedded SP sub-tables. Fixed in Bucket 2: parser now stops after the first canonical table ("K-12 and Adult Learner Specializations", 12 courses). AoS: 4 groups, 9 courses, 0 anomalies. Capstone: 3-course sequence — parser captures only the first course ("Identifying Learner Needs and a Research Problem"); the other two capstone courses ("Developing an E-Learning Solution..." and "Implementing and Evaluating E-Learning Solutions") are in the SP but not reconciled into the AoS output. This is a structural limitation of the multi-course capstone sequence, not a data loss — the capstone section contains all three. MEDETID is downstream-usable with this caveat.
- **MEDETID degree_title**: "Master of Education, Education Technology and Instructional Design" — correctly extracted.

---

## Parser changes (Bucket 2 session)

Three parser fixes applied in Session 22 (all general-scope, not MEDETID-local):

1. `parse_standard_path_multiline()` — SP_CHANGES_RE: changed `break` to conditional `break if state != BEFORE_TABLE else continue`. This allows "Changes to Curriculum" to appear before the SP table (nursing_pmc layout) without prematurely ending the scan.

2. `parse_standard_path_multiline()` — STANDARD_PATH_RE: added `break if state != BEFORE_TABLE` when a second "Standard Path for..." heading is detected. This stops extraction after the first canonical sub-table (MEDETID layout).

3. `extract_title_and_description()` — added "Certificate Guidebook" to the document-type header skip list alongside "Program Guidebook". This corrects degree_title extraction for PMC guides.

All three fixes applied to `parse_standard_path()` (non-multiline) as well for completeness.

Regression-verified against 19 guides from across all completed families — no confidence or anomaly regressions.

---

## Corpus status after rollout

- **Artifact coverage:** 110 / 115 guides (95.7%)
- **Family-validated coverage:** 106 / 115 (92.2%) — education_grad now complete
- **Complete families (15):** standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma, endorsement, nursing_msn, education_grad
- **Partial families:** accounting_ma (MACC + MACCM usable; MACCA, MACCF, MACCT deferred — parser limitation), nursing_pmc (complete — see separate summary)
