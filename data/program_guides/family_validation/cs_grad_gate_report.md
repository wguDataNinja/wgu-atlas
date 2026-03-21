# cs_grad — Gate Report
**Date:** 2026-03-21
**Family size:** 5 guides
**Gate guide:** MSCSIA
**Gate result:** PASS (4/5 HIGH; 1 LOW is source-artifact bridge guide)

---

## Gate summary

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone | Anomalies |
|------|--------|------------|---------|------------|-------------|---------|-----------|
| MSCSIA | M.S., Cybersecurity and Information Assurance | HIGH | 10 | 9 | 9 | ✓ (1 bullet) | 0 |
| MSCSCS | M.S., Computer Science, Computing Systems | HIGH | 10 | 3 | 10 | — | 0 |
| MSCSAIML | M.S., Computer Science, AI/ML | HIGH | 10 | 2 | 10 | — | 0 |
| MSCSHCI | M.S., Computer Science, Human-Computer Interaction | HIGH | 10 | 4 | 10 | — | 0 |
| MSCSUG | B.S., Computer Science (BSCS to MSCS bridge) | **LOW** | 30* | 11 | 37 | — | 14 |

*MSCSUG SP extraction failure — column ordering artifact. 30 rows recovered but many have invalid CU/Term values.

All 4 pure MSCS guides: perfect reconciliation, 0 empty descriptions, 0 empty competency lists.

---

## Structural findings

**Pure MSCS guides (MSCSIA, MSCSCS, MSCSAIML, MSCSHCI):**
- All use 3-column multiline SP (with Term). Consistent with all validated graduate families.
- All use header-line metadata format (page_count=0).
- MSCSIA has unique 1-course-per-group structure: 9 groups, each containing 1 course. Parser handles this via standard 2-item pending_titles resolution.
- MSCSIA has an explicit Capstone section (1 bullet). Only cs_grad guide with a capstone.
- MSCSAIML degree title is truncated in parsed output ("...Artificial Intelligence and") — header wrapping artifact in source. Cosmetic only; content correct.

**MSCSUG (bridge guide):**
- BSCS-to-MSCS pathway guide covering 37 courses (full undergraduate + graduate curriculum).
- SP column extraction failure: same source-PDF artifact as BSITM and MATSPED. Parser recovered 30 SP rows but many have invalid CU/Term values (Term=87, CUs=44, etc.).
- AoS: 11 groups, 37 courses, 0 anomalies. Intact and usable.
- Not a parser regression. Source artifact.

---

## Parser changes

None.

---

## Rollout recommendation

Family rollout approved. Roll out 4 HIGH guides. Include MSCSUG with SP exclusion note. AoS for all 5 guides is safe for downstream use.
