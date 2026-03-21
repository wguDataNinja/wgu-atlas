# education_ma — Rollout Summary
**Date:** 2026-03-21
**Result:** COMPLETE — all 9 guides rolled out

---

## Summary

| Code | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone |
|------|------------|---------|------------|-------------|----------|
| MAMES | HIGH | 18 | 3 | 18 | — |
| MAELLP12 | HIGH | 11 | 3 | 11 | — |
| MAMEK6 | HIGH | 10 | 2 | 9+cap | MA, Mathematics Education (K-6) Capstone |
| MAMEMG | HIGH | 14 | 6 | 13+cap | MA, Mathematics Education (5-9) Teacher Performance Assessment |
| MASEMG | HIGH | 14 | 9 | 14 | — |
| MASESB | HIGH | 13 | 7 | 13 | — |
| MASESC | HIGH | 14 | 5 | 14 | — |
| MASESE | HIGH | 12 | 6 | 12 | — |
| MASESP | HIGH | 13 | 6 | 13 | — |

**9/9 HIGH confidence. 0 anomalies. 0 warnings. 0 empty descriptions. 0 empty competency lists.**

---

## Downstream exclusions

None.

---

## Known caveats

- **MAELLP12**: page_count=0 (cosmetic — older guide format, version 201501, lacks page count in footer). Content intact.
- **MAMEK6 / MAMEMG**: have capstone sections. Correctly parsed post-fix (Session 19).

---

## Parser change this session

Session 19 — capstone KeyError fix: `parse_capstone()` was missing `prerequisite_mentions` and `certification_prep_mentions` keys in the capstone dict. MAMEK6 triggered a crash when its capstone description matched a prereq pattern. Fix: initialize both keys as empty lists in the capstone dict before calling `_scan_description_mentions()`. Regression-verified against 23 guides. No confidence or anomaly regressions.

All previously committed guides with capstone sections (BSBAHC, BSDA, BSHHS, BSMGT, MBAHA, MBAITM, MSCSIA, MSITM, MSML) were re-parsed and confirmed HIGH with no regressions.

---

## Corpus status after rollout

- **Artifact coverage:** 89 / 115 guides (77.4%)
- **Family-validated coverage:** 87 / 115 (75.7%)
- **Complete families (12):** standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma
- **Partial families:** accounting_ma (MACC + MACCM usable; MACCA, MACCF, MACCT deferred — parser limitation)
