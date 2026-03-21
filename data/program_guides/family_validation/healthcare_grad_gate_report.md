# healthcare_grad Family Gate Report

**Date:** 2026-03-21
**Gate approach:** Both guides parsed (family is only 2 guides — gate test covers full family)
**Parser changes:** none

## Results

2/2 guides parsed. 0 failures. **2 HIGH / 0 MEDIUM / 0 LOW.**

| Code | Degree | Confidence | SP Rows | SP Format | AoS Groups | AoS Courses | Capstone | Notes |
|------|--------|------------|---------|-----------|------------|-------------|---------|-------|
| MHA | Master of Healthcare Administration | HIGH | 10 | 3-col multiline | 1 | 9 | ✓ (3 bullets) | header-line metadata |
| MPH | Master of Public Health | HIGH | 12 | 3-col multiline | 1 | 12 | — (embedded in AoS) | header-line metadata |

**Quality:** 0 empty descriptions, 0 empty competency lists, 0 anomalies, 0 warnings across both guides.

## Structural Notes

- Both guides use 3-column multiline SP format (Course Description / CUs / Term). Consistent with all other graduate families validated to date (graduate_standard, mba). No variant needed.
- Both use header-line metadata format; page_count=0 cosmetic gap (pre-existing behavior).
- MHA has an explicit Capstone section ("MHA Capstone") with 3 competency bullets.
- MPH capstone course ("Public Health Graduate Capstone") is embedded in the AoS section rather than a separate Capstone section. MPH parsed correctly with capstone_present=false.
- Both guides have only 1 AoS group — the entire program is one area. Unusual but correct; reflects these programs' tight curriculum focus.

## Gate Result

**PASS — 2/2 HIGH confidence, 0 anomalies, 0 warnings. No parser changes required.**

healthcare_grad is a 2-guide family; this gate test constitutes full rollout. Family complete.

## Corpus Status After healthcare_grad

| Metric | Value |
|--------|-------|
| Guides parsed | 50 / 115 |
| Corpus coverage | **43.5%** |
| Families complete | 5: standard_bs (19), cs_ug (8), education_ba (11), graduate_standard (9), mba (3) |
| Families fully parsed, rollout pending commit | 1: healthcare_grad (2) |
| Phase D threshold (≥70%) | 81 guides — **31 guides short** |

## Next Recommended Families

**teaching_mat** (9 guides) or **education_bs** (4 guides). Both expected to share validated patterns from education_ba (Clinical Experiences, Student Teaching, 2-column SP format). Gate test MATELED or BSSESB before full rollout.
