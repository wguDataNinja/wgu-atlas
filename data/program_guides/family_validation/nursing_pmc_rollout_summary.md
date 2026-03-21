# nursing_pmc — Rollout Summary
**Date:** 2026-03-21
**Result:** COMPLETE — all 4 guides rolled out

---

## Summary

| Code | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone |
|------|------------|---------|------------|-------------|----------|
| PMCNUED | HIGH | 8 | 2 | 8 | — |
| PMCNUFNP | HIGH | 10 | 2 | 10 | — |
| PMCNULM | HIGH | 8 | 2 | 8 | — |
| PMCNUPMHNP | HIGH | 11 | 2 | 11 | — |

**4/4 HIGH confidence. 0 anomalies. 0 warnings. 0 empty descriptions. 0 empty competency lists. 37/37 SP/AoS reconciliation across all 4 guides.**

---

## Downstream exclusions

None.

---

## Known caveats

- SP layout anomaly was a parser limitation, not a source-artifact failure — fixed this session. Source SP data was always present and correct; the parser was stopping too early.
- Degree title "(Post-MSN)" vs "(PostMSN)" inconsistency across guides is a source text variant, not a parser issue.

---

## Parser changes this session

Three fixes applied (all general scope, not PMC-specific):

1. **SP_CHANGES_RE conditional break** (`parse_standard_path_multiline` and `parse_standard_path`): "Changes to Curriculum" now only triggers a break when the SP table has already started (`state != BEFORE_TABLE`). When it appears before the table (PMC layout), the parser continues scanning. Previously, the unconditional break stopped extraction before the table was found.

2. **STANDARD_PATH_RE second-table break** (`parse_standard_path_multiline` and `parse_standard_path`): A second "Standard Path for..." heading after entering the table now triggers a break — first canonical table is complete. Applied for MEDETID; no effect on PMC guides.

3. **Certificate Guidebook title skip** (`extract_title_and_description`): "Certificate Guidebook" added alongside "Program Guidebook" in the document-type header skip. PMC guides now extract the correct degree title instead of "Certificate Guidebook".

**Regression check:** 19 guides from all completed families — zero confidence or anomaly regressions.

---

## Corpus status after rollout

- **Artifact coverage:** 110 / 115 guides (95.7%)
- **Family-validated coverage:** 106 / 115 (92.2%)
- **Complete families (15):** standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma, endorsement, nursing_msn, nursing_pmc
- **Additional completions this session:** education_grad (MEDETID — MEDIUM, 0 anomalies)
- **Partial families:** accounting_ma (MACC + MACCM usable; MACCA, MACCF, MACCT deferred — parser limitation)
