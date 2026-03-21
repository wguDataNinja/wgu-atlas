# endorsement — Gate Report
**Date:** 2026-03-21
**Family size:** 8 guides
**Gate guide:** ENDECE
**Gate result:** PASS — all 8 guides HIGH confidence, 0 anomalies, 0 warnings

---

## Gate summary

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | SP Format | Anomalies |
|------|--------|------------|---------|------------|-------------|-----------|-----------|
| ENDECE | Endorsement Preparation Program, Early Childhood Education | HIGH | 6 | 3 | 6 | 2-col (no Term) | 0 |
| ENDELL | Endorsement Preparation Program, English Language Learning | HIGH | 8 | 1 | 8 | 3-col (with Term) | 0 |
| ENDMEMG | Endorsement Preparation Program, Middle Grades Math | HIGH | 2 | 1 | 2 | 2-col (no Term) | 0 |
| ENDSEMG | Endorsement Preparation Program, Middle Grades Science | HIGH | 2 | 1 | 2 | 2-col (no Term) | 0 |
| ENDSESB | Endorsement Preparation Program, Biology | HIGH | 9 | 2 | 9 | 2-col (no Term) | 0 |
| ENDSESC | Endorsement Preparation Program, Chemistry | HIGH | 7 | 3 | 7 | 2-col (no Term) | 0 |
| ENDSESE | Endorsement Preparation Program, Earth Science | HIGH | 9 | 4 | 9 | 2-col (no Term) | 0 |
| ENDSESP | Endorsement Preparation Program, Physics | HIGH | 7 | 3 | 7 | 2-col (no Term) | 0 |

---

## ENDECE (HIGH) — gate passed

Clean parse. 6/6 courses. 0 anomalies. 3 AoS groups (Elementary Education, Clinical Experiences, Early Childhood Education). No capstone. SP is 2-column (no Term — education format). Clinical Experiences appears as a regular AoS group with 2 courses; no structural anomaly.

---

## Structural notes

**SP format:** 7 of 8 endorsement guides use 2-column SP format (no Term column). ENDELL (oldest guide, version 201112) uses 3-column format with Term. Both formats are handled correctly by the existing parser without changes.

**Metadata format:** All 8 endorsement guides store metadata in a header line on line 3 (`Program Code: ENDECE Catalog Version: 202509 Published Date: 6/17/2025`) rather than in footer lines. The parser reads code, version, and pub_date from this format correctly. `page_count=0` across all 8 guides is a cosmetic consequence of the header-line metadata format — page count is not available in the header. Content is intact.

**ENDELL pages=0 and version=201112:** Oldest guide in the family. Same cosmetic gap as other endorsement guides. Content correct.

**Clinical Experiences / Field Experience sections:** The Phase A manifest flagged these as potential structural anomalies. In practice, they are ordinary AoS groups and the parser handles them without issue. No parser changes required.

**Guide sizes:** ENDMEMG (295 lines) and ENDSEMG (295 lines) are the smallest guides in the corpus. 2 SP rows each. Structurally valid — endorsement programs are short by design.

**Phase A manifest confidence:** Flagged all 8 endorsement guides as MEDIUM with "HIGH UNCERTAINTY" about structure. This was unfounded. All 8 parse cleanly as HIGH.

---

## Rollout decision

**Full rollout — all 8 guides usable downstream.**

0 parser changes required. 0 anomalies. 0 empty descriptions. 0 empty competency lists. SP and AoS intact across all 8 guides.

---

## Coverage impact

After endorsement rollout:
- Artifact coverage: 99 / 115 guides (86.1%)
- Family-validated coverage: 95 / 115 guides (82.6%) — 13 complete families + accounting_ma partial
- Downstream-usable full (SP+AoS): approximately 92 guides (adding to ~84 pre-session)
