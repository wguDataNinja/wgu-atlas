# swe_grad — Gate Report
**Date:** 2026-03-21
**Family size:** 4 guides
**Gate guide:** MSSWEAIE
**Gate result:** PASS (after parser fix)

---

## Parser fix — required before gate pass

**Issue:** All 3 pure graduate swe_grad guides initially parsed as MEDIUM. "Software Quality Assurance and Deployment" was consistently missing from AoS output in all 3. The preceding course ("Software Architecture and Design") had a last bullet that ended without terminal punctuation. `_is_bullet_continuation()` treated the new course title as a bullet continuation, causing the course's content to be lost.

**Root cause:** The `len(line) > 30` continuation path in `_is_bullet_continuation` was too broad. Title Case lines (≥80% capitalized words) should not be treated as sentence continuations.

**Fix:** Added a Title Case ratio check: if ≥80% of a line's words start uppercase, `_is_bullet_continuation` returns False (not a continuation). Minimum targeted change; returns False only for lines that look like headings/titles.

**Regression verification:** Re-parsed BSCS, BSCSIA, MBA, MHA, MATELED, BSSESB, BSACC, MSCIN. All returned identical confidence levels and anomaly counts. No regressions.

---

## Gate summary (after fix)

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Anomalies |
|------|--------|------------|---------|------------|-------------|-----------|
| MSSWEAIE | M.S., Software Engineering – AI Engineering | HIGH | 10 | 2 | 10 | 0 |
| MSSWEDDD | M.S., Software Engineering – Domain Driven Design | HIGH | 10 | 2 | 10 | 0 |
| MSSWEDOE | M.S., Software Engineering – DevOps Engineering | HIGH | 10 | 2 | 10 | 0 |
| MSSWEUG | B.S., Software Engineering (BSSWE to MSSWE bridge) | MEDIUM | 38 | 10 | 38 | 0 |

All 4 guides: 0 empty descriptions, 0 empty competency lists.

---

## Structural findings

**Pure MSSWE guides (MSSWEAIE, MSSWEDDD, MSSWEDOE):**
- Identical structure: 10 SP rows, 2 AoS groups (`[Software]=9`, `[Risk Management]=1`). No capstone.
- Header-line metadata (page_count=0). All version 202504, published 11/5/2024.
- "Software Quality Assurance and Deployment" appears as SP row 5 in all 3 guides. Correctly parsed as a full AoS course after fix.

**MSSWEUG (bridge guide):**
- BSSWE-to-MSSWE bridge covering 38 courses across 10 groups. Parser handles identically.
- MEDIUM: "Scripting and Programming Foundations" in SP vs "Scripting and Programming - Foundations" in AoS. Hyphen variant only — same course, complete content. 38/38 courses present.

---

## Rollout recommendation

Family rollout approved. 3 HIGH, 1 MEDIUM (cosmetic title variant in bridge guide). Parser fix is general and safe.
