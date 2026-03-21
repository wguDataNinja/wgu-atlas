# teaching_mat Family Rollout Summary

**Date:** 2026-03-21
**Gate guide:** MATELED (HIGH confidence, 0 anomalies, 0 warnings)
**Parser changes:** none

## Results

9/9 guides parsed. 0 failures. **7 HIGH / 0 MEDIUM / 1 LOW.**

| Code | Degree | Confidence | SP Format | SP Rows | AoS Groups | AoS Courses | Notes |
|------|--------|------------|-----------|---------|------------|-------------|-------|
| MATELED | M.A.T., Elementary Education | HIGH | 3-col (with Term) | 28 | 5 | 28 | gate guide |
| MATEES | M.A.T., English Education (Secondary) | HIGH | 2-col (no Term) | 20 | 8 | 20 | |
| MATMES | M.A.T., Mathematics Education (Secondary) | HIGH | 2-col (no Term) | 21 | 8 | 21 | |
| MATSESB | M.A.T., Science Education (Secondary Biology) | HIGH | 2-col (no Term) | 20 | 10 | 20 | |
| MATSESC | M.A.T., Science Education (Secondary Chemistry) | HIGH | 2-col (no Term) | 20 | 9 | 20 | |
| MATSESE | M.A.T., Science Education (Secondary Earth Science) | HIGH | 2-col (no Term) | 20 | 9 | 20 | |
| MATSESP | M.A.T., Science Education (Secondary Physics) | HIGH | 2-col (no Term) | 20 | 9 | 20 | |
| MATSPED | M.A.T., Special Education | **LOW** | 3-col (with Term) — extraction failure | 9 | 7 | 30 | SP unusable; AoS clean |
| MATSSES | M.A.T., Social Studies Education (Secondary) | HIGH | 2-col (no Term) | 19 | 7 | 19 | |

**Quality (HIGH-confidence guides):** 0 empty descriptions, 0 empty competency lists. All 8 HIGH guides: perfect reconciliation.

## LOW Case — MATSPED

**Cause:** PDF column extraction failure in the SP table. `pdftotext` extracted the course titles and CU/Term values in column order rather than row order for this PDF. The first 3 course titles appear in their correct row-interleaved positions; the remaining 27 titles appear as a contiguous block at the end of the SP section, separated entirely from their CU/Term data. Parser found only 9 matchable SP rows of 30.

**Impact:** MATSPED SP data is unusable — 21 reconciliation anomalies, 9/30 SP rows recovered. The AoS content (30 courses, all descriptions, all competency bullets) is **fully intact and usable**.

**Parser change:** None. Fixing requires PDF re-extraction with different column settings or a post-hoc batch-title matcher. Both deferred. This is a source-PDF extraction artifact, not a parser deficiency.

**Prior parallel:** BSITM (LOW, standard_bs) — same PDF column extraction failure class.

## Structural Notes

**SP format split:** The teaching_mat family has two SP format variants:

| Format | Guides |
|--------|--------|
| 3-column multiline (with Term) | MATELED, MATSPED |
| 2-column multiline (no Term) | MATEES, MATMES, MATSESB, MATSESC, MATSESE, MATSESP, MATSSES |

MATELED (Elementary) and MATSPED (Special Education) use 3-col with Term. All 7 secondary subject programs use 2-col without Term. Both formats are pre-validated — no new parser logic needed.

**Metadata:** MATELED uses split-footer format. All 8 remaining guides use header-line format (page_count=0 cosmetic gap).

**No Capstone section** in any guide. All are teacher-licensure programs.

**Course count split:** MATELED has 28 courses (a full elementary program); all secondary programs have 19–21 courses (focused subject-specific programs). MATSPED has 30 AoS courses (extended special ed curriculum). No structural impact.

## Safe Fields for Downstream Use

**All guides (AoS content):**
- Course descriptions (0 empty)
- Competency bullets (0 empty)
- AoS group structure
- Guide metadata (version, pub_date)

**8 HIGH guides only (SP content):**
- Standard Path course titles, CU values

## Fields to Exclude

- MATSPED Standard Path course titles and CU values — unusable (PDF extraction failure)
