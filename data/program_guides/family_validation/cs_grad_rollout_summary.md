# cs_grad — Full Rollout Summary
**Date:** 2026-03-21
**Family size:** 5 guides
**Result:** 4 HIGH / 0 MEDIUM / 1 LOW

---

## Guide inventory

| Code | Degree | Confidence | Version | SP Rows | AoS Groups | AoS Courses | Reconciliation |
|------|--------|------------|---------|---------|------------|-------------|----------------|
| MSCSIA | M.S., Cybersecurity and Information Assurance | HIGH | 202306 | 10 | 9 | 9+cap | 10/10 clean |
| MSCSCS | M.S., Computer Science, Computing Systems | HIGH | 202504 | 10 | 3 | 10 | 10/10 clean |
| MSCSAIML | M.S., Computer Science, AI and Machine Learning | HIGH | 202504 | 10 | 2 | 10 | 10/10 clean |
| MSCSHCI | M.S., Computer Science, Human-Computer Interaction | HIGH | 202504 | 10 | 4 | 10 | 10/10 clean |
| MSCSUG | B.S., Computer Science (BSCS to MSCS bridge) | **LOW** | 202504 | 30* | 11 | 37 | FAILED |

*MSCSUG: SP column extraction failure (source artifact). 30 rows recovered but invalid CU/Term values throughout.

4 HIGH guides: 0 empty descriptions, 0 empty competency lists, 0 anomalies.

---

## Structure summary

- SP format: 3-column multiline (with Term) for all 5 guides (MSCSUG format correct but columns corrupted)
- Metadata format: header-line (page_count=0) for all 5 guides
- Capstone: MSCSIA only (1 bullet)
- No new parser logic needed

---

## Outliers and anomalies

**MSCSUG — SP column extraction failure (LOW confidence):**
Source PDF artifact — same failure class as BSITM and MATSPED. Column ordering during pdftotext extraction produced interleaved title/CU/Term values. 14 SP anomalies, invalid term values (87, 45, etc.). SP data is unusable.

AoS for MSCSUG is intact: 11 groups, 37 courses, 0 anomalies, 0 empty descriptions, 0 empty competency lists. This is a bridge guide covering the full BSCS-to-MSCS curriculum (37 courses). AoS content is safe for downstream use.

**MSCSAIML degree title truncation (cosmetic):**
Parsed degree_title reads "...Artificial Intelligence and" (truncated). The AoS section header line wraps across two lines in the source PDF, and only the first line is captured in the title field. SP, AoS content, and metadata are correct.

---

## Safe fields for downstream use

- SP course titles, CU values, term sequence: **MSCSIA, MSCSCS, MSCSAIML, MSCSHCI** only
- AoS group structure, course descriptions, competency bullets: **all 5 guides**
- Capstone title and content: **MSCSIA** only

## Downstream exclusions

- **MSCSUG SP data** — column extraction failure, unusable
- **MSCSAIML degree_title field** — truncated, use source catalog for full title

---

## Parser changes

None.

---

## Go/no-go

**GO with exclusions.** 4/5 HIGH confidence. MSCSUG SP is excluded (source artifact). AoS content for all 5 guides is safe.
