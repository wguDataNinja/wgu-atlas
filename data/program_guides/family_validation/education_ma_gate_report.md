# education_ma — Gate Report
**Date:** 2026-03-21
**Family size:** 9 guides
**Gate guide:** MAMES
**Gate result:** PASS — all 9 guides HIGH confidence, 0 anomalies, 0 warnings

---

## Gate summary

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone | Anomalies |
|------|--------|------------|---------|------------|-------------|----------|-----------|
| MAMES | M.A. in Mathematics Education (Secondary) | HIGH | 18 | 3 | 18 | no | 0 |
| MAELLP12 | M.A., English Language Learning (PreK-12) | HIGH | 11 | 3 | 11 | no | 0 |
| MAMEK6 | M.A., Mathematics Education (K-6) | HIGH | 10 | 2 | 9+cap | yes | 0 |
| MAMEMG | M.A. in Mathematics Education (Middle Grades 5-9) | HIGH | 14 | 6 | 13+cap | yes | 0 |
| MASEMG | M.A. in Science Education (Middle Grades) | HIGH | 14 | 9 | 14 | no | 0 |
| MASESB | M.A. in Science Education (Secondary Biology) | HIGH | 13 | 7 | 13 | no | 0 |
| MASESC | M.A. in Science Education (Secondary Chemistry) | HIGH | 14 | 5 | 14 | no | 0 |
| MASESE | M.A. in Science Education (Secondary Earth Science) | HIGH | 12 | 6 | 12 | no | 0 |
| MASESP | M.A. in Science Education (Secondary Physics) | HIGH | 13 | 6 | 13 | no | 0 |

---

## MAMES (HIGH) — gate passed

Clean parse. 18/18 courses. 0 anomalies. 3 AoS groups (Mathematics Content, Mathematics Education, Teacher Work Sample). No capstone. SP is 3-column with CUs and Term. Selected as gate guide: solid size, no capstone, representative of the main mathematics sub-family.

---

## MAELLP12 (HIGH) — notable: old version, page_count=0

Version 201501 (oldest in family). page_count=0 because older guide format lacks page count in the footer. Content is intact: 11 SP rows, 11 AoS courses, 0 anomalies. Phase A manifest flagged a possible Field Experience section for this guide — the actual parse found no such section. Sections detected: Standard Path, Areas of Study, Accessibility. Content correct and usable.

---

## MAMEK6 and MAMEMG (HIGH) — capstone parser bug found and fixed

MAMEK6 triggered a KeyError in `parse_capstone()` during this session. The capstone dict was missing `prerequisite_mentions` and `certification_prep_mentions` keys. When the capstone description matched a prerequisite pattern, `_scan_description_mentions()` attempted to access a non-existent key.

**Fix (Session 19):** Added `prerequisite_mentions: []` and `certification_prep_mentions: []` to the capstone dict before calling `_scan_description_mentions()`. Regression-verified against 23 previously validated guides including all guides with capstone sections. All returned identical confidence and anomaly counts.

MAMEK6 post-fix: 10/10 reconciliation (9 AoS courses + 1 capstone = 10 SP rows). MAMEMG post-fix: 14/14. Both HIGH.

---

## Structural notes

**SP format:** 3-column with CUs and Term — consistent with standard_bs and graduate families. Phase A manifest incorrectly flagged education_ma guides as having no CU values and no term structure. The actual parsed data contains correct CU and Term fields in every SP row. Phase A detection was imperfect for these older guide versions.

**AoS group structure:** Subject-specific groups (Mathematics Content, Science, Biology Content, Chemistry Content, Geosciences Content, etc.) plus Research and Teacher Performance Assessment groups. Group counts vary (2–9 per guide) reflecting the subject specialization of each degree. This is structurally expected.

**No source-artifact SP failures.** No parser limitations affect this family.

**No Field Experience section** was present in any of the 9 guides. The Phase A manifest flag for MAELLP12 was not triggered by the actual guide content.

---

## Rollout decision

**Full rollout — all 9 guides usable downstream.**

education_ma is the cleanest family in the corpus to date: 9/9 HIGH, 0 anomalies, 0 warnings, 0 empty descriptions, 0 empty competency lists. No deferred guides. No exclusions.

---

## Coverage impact

After education_ma rollout:
- Artifact coverage: 89 / 115 guides (77.4%)
- Family-validated coverage: 87 / 115 guides (75.7%) — 12 complete families + MACC partial
- Downstream-usable full (SP+AoS): approximately 84 guides
- Families remaining unvalidated: endorsement (8), nursing sub-families (8+), education_grad (2), accounting_ma specializations (3 deferred)
