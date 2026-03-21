# accounting_ma — Rollout Summary
**Date:** 2026-03-21
**Result:** COMPLETE — all 5 guides rolled out

---

## Summary

| Code | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone |
|------|------------|---------|------------|-------------|----------|
| MACC | HIGH | 10 | 4 | 10 | — |
| MACCM | HIGH | 10 | 2 | 10 | — |
| MACCA | HIGH | 10 | 2 | 10 | — |
| MACCF | HIGH | 11 | 2 | 11 | — |
| MACCT | HIGH | 10 | 2 | 10 | — |

**5/5 HIGH confidence. 0 anomalies. 0 warnings. 0 empty descriptions. 0 empty competency lists. 51/51 SP/AoS reconciliation across all 5 guides.**

---

## Downstream exclusions

None. All 5 guides are fully usable.

Note: the Session 20–22 gate report deferred MACCA, MACCF, MACCT as "parser limitation — looks_like_prose failure for short wrapped lines." This session resolved that limitation with targeted fixes (see Parser changes below). All 5 guides are now HIGH.

---

## Known caveats

- MACCM "Corporate Financial Analysis" course: title/first-sentence quality issue noted in Session 20 (cosmetic; description content intact).
- MACC has 4 AoS groups (broader cross-specialization structure) vs 2 groups for each specialization guide — expected structural difference.

---

## Parser changes this session

Four fixes applied (all general scope):

1. **`looks_like_prose()` lowercase-start heuristic**: Lines beginning with a lowercase letter now return True. Handles short wrapped description lines that start mid-sentence (e.g. "demand. As the business world continues").

2. **`looks_like_prose()` continuation-particle end heuristic**: Lines ending with particles like "in", "the", "and", "of" return True. Handles wrapped lines at mid-noun-phrase (e.g. "skills are in high").

3. **`looks_like_prose()` prose-verb heuristic**: Lines ≥20 chars containing standalone prose verbs (is, are, describes, covers, prepares, etc.) return True. Handles lines like "Corporate Taxation describes federal income".

4. **`_is_bullet_continuation()` terminal-punctuation override**: Lines ending with `.?!,:;` are always sentence continuations — course titles never end with terminal punctuation. This fix handles multi-line bullets where the continued line is Title Case (e.g. "International Professional Practices Framework (IPPF)."). Applied before the Title Case guard, resolving a cascade misparse in MACCA and MACCM.

**Regression check:** 20 guides from all completed families — zero confidence regressions. MACCM improved from MEDIUM to HIGH (unexpected positive cascade from fix #4).

---

## Corpus status after rollout

- **Artifact coverage:** 115 / 115 guides (100.0%)
- **Family-validated coverage:** 115 / 115 (100.0%)
- **Complete families (18):** standard_bs, cs_ug, education_ba, graduate_standard, mba, healthcare_grad, education_bs, teaching_mat, cs_grad, swe_grad, data_analytics_grad, education_ma, endorsement, nursing_msn, nursing_pmc, accounting_ma, nursing_ug, nursing_rn_msn
- **education_grad:** fully complete (MSEDL=HIGH + MEDETID=MEDIUM)
- **Partial families:** none
