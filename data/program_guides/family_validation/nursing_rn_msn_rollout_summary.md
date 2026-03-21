# nursing_rn_msn — Rollout Summary
**Date:** 2026-03-21
**Result:** COMPLETE — all 3 guides rolled out HIGH

---

## Summary

| Code | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone |
|------|------------|---------|------------|-------------|----------|
| MSRNNUED | HIGH | 32 | 4 | 32 | — |
| MSRNNULM | HIGH | 32 | 4 | 32 | — |
| MSRNNUNI | HIGH | 31 | 4 | 31 | — |

**3/3 HIGH confidence. 0 anomalies. 0 warnings. 0 empty descriptions. 0 empty competency lists. 95/95 SP/AoS reconciliation across all 3 guides.**

---

## Guide details

These are combined BS+MSN guides ("RN to MSN" bridge programs). Each document contains content for both a BS nursing degree and an MSN specialization. The combined-footer format (`MSRNNUUG + MSNUED 202202`) is specific to these guides.

**AoS structure (all 3 guides):**
1. Advanced Standing for RN License (5 courses — awarded for existing RN license, but courses also appear in SP)
2. General Education (12 courses)
3. MSN Core (8 courses)
4. Specialty group (8/8/7 courses for NUE/NLM/NNI respectively)

**SP structure:** 32/32/31 rows with full term assignments. "Advanced Standing for RN License" (50 CUs, term=0) appears as a block-credit summary row but is silently skipped — the individual courses are listed separately with normal term assignments.

---

## Downstream exclusions

None. All 3 guides are fully usable.

---

## Known caveats

- Combined BS+MSN format: `degree_title` is truncated — extracted as "Bachelor of Science and Post-Baccalaureate Certificate, Nursing +" (the "+" comes from the combined-plus footer pattern preceding the degree title section). Correct MSN degree titles are in the AoS section headers.
- Version/date metadata is extracted from the combined-program footer (e.g. "202202"), not a per-program footer. All 3 guides share version 202202, pub_date 12/15/21.
- "Advanced Standing for RN License" SP row (50 CUs, term=0): silently skipped as block-credit placeholder. Its 5 individual courses appear in SP at their normal term positions.

---

## Parser changes this session

Three fixes applied (general scope; all three benefit nursing_rn_msn):

1. **`ACCESSIBILITY_RE` typo tolerance** (`r'^Accessibility and Accomm?odations'`): Guides use "Accomodations" (single-m typo). The corrected regex detects the Accessibility section boundary, preventing it from being captured as the last AoS course group. Without this fix: "Accessibility and Accomodations" appeared as the last AoS group with 0 competency bullets (false positive), causing 2 warnings per guide.

2. **`no_footer_lines_found` combined-program suppression**: Combined-plus footer (`MSRNNUUG + MSNUED 202202`) provides version but not program code. Fix: when `codes` is empty but `versions` is non-empty, return available metadata without the `no_footer_lines_found` anomaly. Removes 1 anomaly per guide.

3. **`sp_row_invalid` "Advanced Standing" silent skip**: "Advanced Standing for RN License" (50 CUs, term=0) is silently skipped rather than flagged as an invalid SP row. Removes 1 anomaly per guide.

**Combined effect per guide:** 2 anomalies + 2 warnings → 0 anomalies + 0 warnings → HIGH.

**Regression check:** 20 guides from all completed families — zero confidence regressions.

---

## Corpus status after rollout

- **Artifact coverage:** 115 / 115 guides (100.0%)
- **Family-validated coverage:** 115 / 115 (100.0%)
- **Complete families (18):** standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma, endorsement, nursing_msn, nursing_pmc, accounting_ma, nursing_ug, nursing_rn_msn
