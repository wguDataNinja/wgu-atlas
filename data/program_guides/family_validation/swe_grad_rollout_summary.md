# swe_grad — Full Rollout Summary
**Date:** 2026-03-21
**Family size:** 4 guides
**Result:** 3 HIGH / 1 MEDIUM / 0 LOW

---

## Guide inventory

| Code | Degree | Confidence | Version | SP Rows | AoS Groups | AoS Courses | Reconciliation |
|------|--------|------------|---------|---------|------------|-------------|----------------|
| MSSWEAIE | M.S., Software Engineering – AI Engineering | HIGH | 202504 | 10 | 2 | 10 | 10/10 clean |
| MSSWEDDD | M.S., Software Engineering – Domain Driven Design | HIGH | 202504 | 10 | 2 | 10 | 10/10 clean |
| MSSWEDOE | M.S., Software Engineering – DevOps Engineering | HIGH | 202504 | 10 | 2 | 10 | 10/10 clean |
| MSSWEUG | B.S., Software Engineering (BSSWE to MSSWE bridge) | MEDIUM | 202504 | 38 | 10 | 38 | 37/38 (1 hyphen variant) |

All 4 guides: 0 empty descriptions, 0 empty competency lists, 0 AoS anomalies.

---

## Structure summary

- SP format: 3-column multiline (with Term), all 4 guides
- Metadata format: header-line (page_count=0), all 4 guides
- Capstone: absent in all 4 guides
- 3 pure graduate guides share identical 2-group structure: `[Software]=9`, `[Risk Management]=1`
- MSSWEUG: bridge guide, 10 groups, 38 courses

---

## Parser change required

`_is_bullet_continuation` Title Case guard was implemented before this family could reach HIGH confidence. All 3 pure graduate guides initially parsed as MEDIUM due to "Software Quality Assurance and Deployment" being lost as a bullet continuation. Fix is general and regression-verified. See gate report for detail.

---

## Outliers and anomalies

**MSSWEUG MEDIUM — title hyphen variant:**
SP title "Scripting and Programming Foundations" ≠ AoS title "Scripting and Programming - Foundations". Same course; formatting variant only. 0 AoS anomalies; 38/38 courses present with full content.

---

## Safe fields for downstream use

All fields safe for all 4 guides. Minor note: prefer AoS title for the Scripting/Programming course in MSSWEUG.

---

## Parser changes

- `_is_bullet_continuation`: Title Case ratio guard (≥80% capitalized words → not a continuation)
- Scope: general
- Regression verified: 8 guides from 6 previously-validated families — no changes

---

## Go/no-go

**GO.** 3/4 HIGH, 1/4 MEDIUM (cosmetic title variant). Parser fix safe and general. No downstream exclusions except the noted title variant.
