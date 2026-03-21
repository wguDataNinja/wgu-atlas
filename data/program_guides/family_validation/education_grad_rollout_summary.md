# education_grad — Rollout Summary (Partial — MSEDL only)
**Date:** 2026-03-21
**Result:** PARTIAL — 1 of 2 guides rolled out; MEDETID deferred to Bucket 2

---

## Summary

| Code | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone | Status |
|------|------------|---------|------------|-------------|----------|--------|
| MSEDL | HIGH | 13 | 3 | 13 | — | COMPLETE |
| MEDETID | — | — | — | — | — | DEFERRED — Bucket 2 |

**1/2 guides completed this session. MSEDL: HIGH, 0 anomalies, 0 warnings, 0 empty descriptions, 0 empty competency lists.**

---

## Downstream exclusions

- **MEDETID**: excluded from this rollout. Deferred to Bucket 2 (contained anomaly work). AoS is intact (4 groups, 9 courses); SP is overcounted due to 3 embedded sub-tables.

---

## Known caveats

- **MSEDL**: Phase A manifest flagged a Practicum section as a potential parser gap. In the actual parse, no Practicum structural section exists — the Practicum course is an ordinary named course within the Educational Leadership AoS group. No parser issue.
- **MEDETID**: Multi-path SP structure (3 sub-tables: combined, K-12, Adult Learner). Parser concatenates all 3, producing 32 rows with duplicates and sub-table header rows as course entries. AoS is unaffected. Requires a targeted SP fix (select one canonical path, or deduplicate) before rollout. Deferred to Bucket 2.

---

## Parser changes this session

None.

---

## Corpus status after rollout

- **Artifact coverage:** 105 / 115 guides (91.3%)
- **Family-validated coverage:** 101 / 115 (87.8%) — counting MSEDL; MEDETID remains unvalidated
- **Complete families (14):** standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma, endorsement, nursing_msn
- **Partial families:** accounting_ma (MACC + MACCM usable; MACCA, MACCF, MACCT deferred — parser limitation), education_grad (MSEDL done; MEDETID deferred — Bucket 2)
