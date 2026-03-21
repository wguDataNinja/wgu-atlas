# endorsement — Rollout Summary
**Date:** 2026-03-21
**Result:** COMPLETE — all 8 guides rolled out

---

## Summary

| Code | Confidence | SP Rows | AoS Groups | AoS Courses | SP Format | Capstone |
|------|------------|---------|------------|-------------|-----------|----------|
| ENDECE | HIGH | 6 | 3 | 6 | 2-col (no Term) | — |
| ENDELL | HIGH | 8 | 1 | 8 | 3-col (with Term) | — |
| ENDMEMG | HIGH | 2 | 1 | 2 | 2-col (no Term) | — |
| ENDSEMG | HIGH | 2 | 1 | 2 | 2-col (no Term) | — |
| ENDSESB | HIGH | 9 | 2 | 9 | 2-col (no Term) | — |
| ENDSESC | HIGH | 7 | 3 | 7 | 2-col (no Term) | — |
| ENDSESE | HIGH | 9 | 4 | 9 | 2-col (no Term) | — |
| ENDSESP | HIGH | 7 | 3 | 7 | 2-col (no Term) | — |

**8/8 HIGH confidence. 0 anomalies. 0 warnings. 0 empty descriptions. 0 empty competency lists.**

---

## Downstream exclusions

None.

---

## Known caveats

- **All 8 guides**: `page_count=0` — cosmetic. Endorsement guides store metadata in a header line (not footer); page count is not recoverable from this format. Content is intact.
- **ENDELL**: version=201112 (oldest guide in the family). pages=0 (same cosmetic cause). Content correct.
- **ENDMEMG / ENDSEMG**: Smallest guides in the corpus — 295 lines, 2 SP rows, 2 AoS courses each. Structurally valid by design (very short endorsement programs).
- **SP format split**: 7 of 8 guides use 2-column SP (no Term). ENDELL uses 3-column. Both formats handled correctly by the existing parser.
- **Phase A manifest uncertainty**: Manifest had classified all 8 as MEDIUM with high structural uncertainty and flagged Clinical Experiences / Field Experience as potential anomalies. In practice, these sections are ordinary AoS groups and parse cleanly.

---

## Parser changes this session

None. No parser changes required or made.

---

## Corpus status after rollout

- **Artifact coverage:** 99 / 115 guides (86.1%)
- **Family-validated coverage:** 95 / 115 (82.6%)
- **Complete families (13):** standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma, endorsement
- **Partial families:** accounting_ma (MACC + MACCM usable; MACCA, MACCF, MACCT deferred — parser limitation)
