# education_bs Family Gate Report

**Date:** 2026-03-21
**Gate guide:** BSSESB
**Family size:** 4 guides
**Parser changes:** none (© line fix made during MATELED gate; no additional changes for BSSESB)

## Gate Result

**PASS — BSSESB HIGH confidence, 0 anomalies, 0 warnings. 41/41 perfect reconciliation.**

| Code | Degree | Confidence | SP Format | SP Rows | AoS Groups | AoS Courses | Capstone |
|------|--------|------------|-----------|---------|------------|-------------|---------|
| BSSESB | B.S., Science Education (Secondary Biological Science) | HIGH | 2-col multiline (no Term) | 41 | 11 | 41 | — |

**Quality:** 0 empty descriptions, 0 empty competency lists.

## AoS Group Structure

| Group | Courses |
|-------|---------|
| Professional Core | 7 |
| General Education | 7 |
| General Science Content | 8 |
| Mathematics Education | 1 |
| Secondary Education | 3 |
| Science Education | 1 |
| Clinical Experiences | 2 |
| Biology Content | 8 |
| Pedagogy and Teaching Methods | 1 |
| Science | 1 |
| Student Teaching | 2 |

## Structural Notes

- **SP format:** 2-column multiline (no Term). Consistent with education_ba teacher-licensure guides (BAELED, BASPEE, BASPMM). education_bs is an undergraduate degree; the no-Term SP format is the expected pattern for undergraduate education programs.
- **Clinical Experiences / Student Teaching:** Appear as AoS group labels — identical to education_ba. No new handler needed.
- **Metadata format:** Header-line format (page_count=0 cosmetic gap — pre-existing behavior).
- **11 AoS groups:** Largest group count in any education family guide validated to date, but the parser handles it without issue.
- **Subject-specific content groups** ("Biology Content", "General Science Content") differ from Elementary education guides — but the AoS state machine handles arbitrary group names correctly.
- **No Capstone section.** Handled gracefully.

## Rollout Recommendation

**Proceed with education_bs full rollout — recommended before teaching_mat.** This is a 4-guide family. All structural patterns are validated extensions of education_ba. Very low risk. The 3 remaining education_bs guides are likely subject-area variants (different science disciplines or other subjects) sharing an identical structural template.
