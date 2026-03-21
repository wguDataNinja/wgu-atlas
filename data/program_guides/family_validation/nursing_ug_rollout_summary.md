# nursing_ug — Rollout Summary
**Date:** 2026-03-21
**Result:** COMPLETE — both guides rolled out at MEDIUM

---

## Summary

| Code | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone | Anomalies | Warnings |
|------|------------|---------|------------|-------------|----------|-----------|---------|
| BSNU | MEDIUM | 22 | 2 | 22 | — | 1 | 0 |
| BSPRN | MEDIUM | 19 | 3 | 34 | — | 0 | 1 |

**0/2 HIGH. 2/2 MEDIUM. Content fully parsed; metadata limitations and structural complexity prevent HIGH.**

---

## Guide details

### BSNU — Bachelor of Science, Nursing (prelicensure)
- **Confidence:** MEDIUM
- **Anomaly:** `no_footer_lines_found` — source PDF has no version/date/page footer lines. Program code extracted from filename. Version=None, pub_date=None, page_count=0.
- **Content:** 22 SP rows (terms 1–6), 22 AoS courses across 2 groups (Nursing Core × 10, General Education × 12). Perfect SP/AoS reconciliation (22/22).
- **SP format:** 4-column layout (Option A term / Option B term) with no "Course Description" header.
- **Downstream use:** SP + AoS fully usable. Version/date metadata unavailable.

### BSPRN — Bachelor of Science, Nursing – Prelicensure (Pre-Nursing/Nursing)
- **Confidence:** MEDIUM
- **Warning:** 15 AoS courses not in SP (dual-track structural mismatch — pre-nursing SP has 19 courses; Nursing-track courses are AoS-only).
- **Content:** 19 SP rows (Pre-Nursing track), 34 AoS courses across 3 groups (General Education × 16, Prelicensure Nursing × 14, Nursing Core × 4). 19/19 SP courses match in AoS.
- **SP format:** Standard 3-column multiline.
- **Downstream use:** AoS content fully usable (34 courses with descriptions and competency bullets). SP represents Pre-Nursing track only. The 15 Nursing-track AoS courses have no SP placement.

---

## Downstream exclusions

None. Both guides are usable with documented limitations.

---

## Known caveats

- **BSNU:** Footer-less source PDF — version/pub_date/page_count are not recoverable. AoS content and SP are intact.
- **BSPRN:** Dual-track guide (Pre-Nursing + Nursing). SP covers Pre-Nursing track only (19 courses). The Nursing track (15 courses) appears in AoS but not SP. This is a structural property of the guide, not a parser defect. SP/AoS reconciliation will always show 15 AoS-only courses for BSPRN.
- **BSPRN:** "Advanced Standing for RN License" appears as a 50-CU block in the SP (term=0) — silently skipped by parser; individual courses are listed separately.

---

## Parser changes this session

Five fixes applied (all general scope; none nursing_ug-specific):

1. **`ACCESSIBILITY_RE` typo tolerance** (`r'^Accessibility and Accomm?odations'`): handles both "Accommodations" and "Accomodations" (single-m typo common in older guides). BSNU uses correct spelling; no direct effect on BSNU.

2. **`no_footer_lines_found` combined-program suppression**: When `codes` is empty but `versions` is non-empty (combined-program footers were found), return available metadata without the anomaly. BSPRN benefits (version=202303 now extracted).

3. **`sp_row_invalid` "Advanced Standing" silent skip**: SP rows with "Advanced Standing" in the title and CU/term values outside the normal range are silently dropped (no anomaly). Applied in both 2-column and 3-column SP paths. Removes false anomalies for block-credit placeholder rows.

4. **`SP_CU_ONLY_RE` alternative BEFORE_TABLE trigger**: Allows SP parsing to begin when a standalone "CUs" header line is found (no "Course Description" header present). Required for BSNU 4-column format.

5. **Stray-integer skip in `EXPECTING_TITLE`**: Integers encountered with an empty `title_buf` are skipped. Handles second-term values in 4-column tables (BSNU Option A/Option B).

**Regression check:** 20 guides from all completed families — zero confidence regressions. MATSPED improved from LOW to MEDIUM (unexpected positive from stray-integer fix).

---

## Corpus status after rollout

- **Artifact coverage:** 115 / 115 guides (100.0%)
- **Family-validated coverage:** 115 / 115 (100.0%)
- **Complete families (18):** standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma, endorsement, nursing_msn, nursing_pmc, accounting_ma, nursing_ug, nursing_rn_msn
