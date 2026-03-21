# education_grad — Gate Report (MSEDL)
**Date:** 2026-03-21
**Family size:** 2 guides (MSEDL + MEDETID)
**Gate guide:** MSEDL
**Gate result:** PASS for MSEDL — HIGH confidence, 0 anomalies, 0 warnings
**Note:** This is a partial gate. MEDETID has multi-path SP structure and is deferred to Bucket 2.

---

## MSEDL gate summary

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Anomalies |
|------|--------|------------|---------|------------|-------------|-----------|
| MSEDL | Master of Science, Educational Leadership | HIGH | 13 | 3 | 13 | 0 |

---

## MSEDL (HIGH) — gate passed

Clean parse. 13/13 courses. 0 anomalies. 3 AoS groups: Educational Leadership (9 courses), Education (1 course), Graduate Core (3 courses). No capstone. SP is 3-column (with Term). Pages=13, valid footer metadata.

Phase A manifest flagged a "Practicum section" as a potential parser gap for MSEDL. In the actual parse, no Practicum structural section was detected — the Practicum course appears as an ordinary named course within the Educational Leadership AoS group. No parser changes required.

---

## MEDETID — deferred to Bucket 2

MEDETID has 3 embedded Standard Path sub-tables (combined specialization + K-12 + Adult Learner tracks). The parser produces 32 SP rows by concatenating all 3 tables, including sub-table header lines as course rows and duplicate shared courses. AoS is clean (4 groups, 9 courses, 0 anomalies). SP is overcounted and not usable without a targeted fix.

MEDETID is assigned to Bucket 2 (contained anomaly work) for a dedicated session. It is excluded from this rollout.

---

## Structural notes

**Family split:** education_grad is a 2-guide family. The two guides have fundamentally different structures: MSEDL is a standard graduate guide; MEDETID embeds specialization sub-tables requiring targeted parser handling.

---

## Rollout decision

**Partial rollout — MSEDL usable downstream. MEDETID deferred.**

---

## Coverage impact

After MSEDL rollout (partial education_grad):
- Artifact coverage: 105 / 115 guides (91.3%)
- Family-validated coverage: 101 / 115 guides (87.8%) — counting MSEDL as validated; MEDETID deferred
- Downstream-usable full (SP+AoS): approximately 98 guides
