# education_bs Family Rollout Summary

**Date:** 2026-03-21
**Gate guide:** BSSESB (HIGH confidence, 0 anomalies, 0 warnings)
**Parser changes:** none

## Results

4/4 guides parsed. 0 failures. **4 HIGH / 0 MEDIUM / 0 LOW.**

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Notes |
|------|--------|------------|---------|------------|-------------|-------|
| BSSESB | B.S., Science Education (Secondary Biological Science) | HIGH | 41 | 11 | 41 | gate guide |
| BSSESC | B.S., Science Education (Secondary Chemistry) | HIGH | 40 | 10 | 40 | |
| BSSESE | B.S., Science Education (Secondary Earth Science) | HIGH | 41 | 11 | 41 | |
| BSSESP | B.S., Science Education (Secondary Physics) | HIGH | 40 | 10 | 40 | |

**Quality:** 0 empty descriptions, 0 empty competency lists. All 4 guides: perfect reconciliation.

## Structural Notes

**SP format:** All 4 guides use 2-column multiline (no Term). Consistent with education_ba teacher-licensure guides. No parser branching needed.

**Metadata:** All header-line format (page_count=0 cosmetic gap — pre-existing behavior). All version 202603 — family was published as a cohort in December 2025.

**AoS structure:** Shared skeleton across all 4 guides:
- Professional Core: 7 courses (identical across all)
- General Science Content: 8 courses (identical across all)
- Clinical Experiences: 2 courses (identical across all)
- Student Teaching: 2 courses (identical across all)

Subject-specific content group names vary by discipline:

| Guide | Subject Content Group | Courses |
|-------|-----------------------|---------|
| BSSESB | Biology Content | 8 |
| BSSESC | Chemistry Content | 5 |
| BSSESE | (distributed: Biology Content 1, Science Education 7) | 8 total |
| BSSESP | (via Science Education group) | 6 |

The AoS state machine handles arbitrary group names — no branching needed for subject variants.

**No Capstone section** in any guide. All are teacher-licensure programs.

## Safe Fields for Downstream Use

All fields are clean for all 4 guides:
- Standard Path course titles, CU values
- AoS group structure
- Course descriptions (0 empty)
- Competency bullets (0 empty)
- Guide metadata (version, pub_date)
