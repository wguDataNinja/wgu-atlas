# nursing_msn — Gate Report
**Date:** 2026-03-21
**Family size:** 5 guides
**Gate guide:** MSNUED
**Gate result:** PASS — all 5 guides HIGH confidence, 0 anomalies, 0 warnings

---

## Gate summary

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Anomalies |
|------|--------|------------|---------|------------|-------------|-----------|
| MSNUED | Master of Science, Nursing - Education (BSN to MSN) | HIGH | 15 | 2 | 15 | 0 |
| MSNUFNP | Master of Science, Nursing - Family Nurse Practitioner (BSN to MSN) | HIGH | 16 | 3 | 16 | 0 |
| MSNULM | Master of Science, Nursing - Leadership and Management (BSN to MSN) | HIGH | 15 | 2 | 15 | 0 |
| MSNUNI | Master of Science, Nursing - Nursing Informatics (BSN to MSN) | HIGH | 14 | 2 | 14 | 0 |
| MSNUPMHNP | Master of Science, Nursing - Psychiatric Mental Health Nurse | HIGH | 17 | 3 | 17 | 0 |

---

## MSNUED (HIGH) — gate passed

Clean parse. 15/15 courses. 0 anomalies. 2 AoS groups: MSN Core (8 courses) and Nursing Education Specialty (7 courses). No capstone. SP is 3-column (with Term). Selected as gate guide: solid size, representative MSN structure, BSN-to-MSN track.

---

## Structural notes

**SP format:** All 5 guides use 3-column SP format (Course / CUs / Term). Consistent with graduate-family format. No format anomalies.

**AoS group structure:** All 5 guides share an "MSN Core" group (6–8 courses) plus one or two specialty groups. FNP and PMHNP guides have 3 groups (adding "Nurse Practitioner Core"). This is structurally expected for this family.

**Clinical / preceptor sections:** The Phase A manifest flagged nursing clinical/preceptor sections as a concern. In practice, these appear as ordinary named courses within AoS groups (e.g., "Nursing Practicum" or "Clinical Practice" as course titles), not as separate structural sections. The parser handles them correctly without any changes.

**Metadata:** All 5 guides have footer metadata with valid version and pub_date. MSNUED, MSNUFNP, MSNUNI all show version=202003; MSNULM shows version=202011; MSNUPMHNP shows version=202203. Page counts: 13–15 pages (all valid).

**Phase A manifest confidence:** Flagged all 5 guides as MEDIUM with "unknown" section variants and clinical handling concern. This was unfounded. All 5 parse cleanly as HIGH.

---

## Rollout decision

**Full rollout — all 5 guides usable downstream.**

0 parser changes required. 0 anomalies. 0 empty descriptions. 0 empty competency lists. SP and AoS intact across all 5 guides.

---

## Coverage impact

After nursing_msn rollout:
- Artifact coverage: 104 / 115 guides (90.4%)
- Family-validated coverage: 100 / 115 guides (87.0%) — 14 complete families + partials
- Downstream-usable full (SP+AoS): approximately 97 guides
