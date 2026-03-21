# data_analytics_grad — Gate Report
**Date:** 2026-03-21
**Family size:** 3 guides
**Gate guide:** MSDADE
**Gate result:** PASS

---

## Gate summary

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone | Anomalies |
|------|--------|------------|---------|------------|-------------|---------|-----------|
| MSDADE | M.S., Data Analytics – Data Engineering | HIGH | 11 | 2 | 11 | — | 0 |
| MSDADS | M.S., Data Analytics – Data Science | HIGH | 11 | 2 | 11 | — | 0 |
| MSDADPE | M.S., Data Analytics – Decision Process Engineering | HIGH | 11 | 3 | 11 | — | 0 |

All 3 guides: perfect reconciliation (11/11), 0 empty descriptions, 0 empty competency lists.

---

## Structural findings

- All 3 guides use **3-column multiline SP** (with Term). Consistent with all validated graduate families.
- All 3 guides use **footer metadata** format (version 202408, page_count=11). Footer format already handled.
- No Capstone section in any guide. Absent from source — not a parser gap.
- All guides are **track/specialization variants** of the MSDA program. All share a 7-course Data Analytics core (`[Data Analytics]` group). Specialization content adds the second or third AoS group:
  - MSDADE: `[Data Analytics]=7`, `[Data Engineering]=4`
  - MSDADS: `[Data Analytics]=7`, `[Data Science]=4`
  - MSDADPE: `[Data Analytics]=7`, `[IT Management]=1`, `[Decision Process Engineering]=3`
- No new parser logic needed or applied.

---

## Parser changes

None.

---

## Rollout recommendation

Family rollout approved. All 3 guides HIGH confidence. Roll out in same session.
