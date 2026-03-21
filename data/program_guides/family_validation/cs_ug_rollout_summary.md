# cs_ug Family — Full Rollout Summary

**Date:** 2026-03-20 (session 14 continuation)
**Family:** `cs_ug`
**Total guides:** 8

---

## Overall Results

| Confidence | Count | Guides |
|---|---|---|
| **HIGH** | 4 | BSCS, BSCNE, BSCNEAWS, BSCNEAZR |
| **MEDIUM** | 4 | BSCNECIS, BSCSIA, BSSWE_C, BSSWE_Java |
| **LOW** | 0 | — |

- **Parsed successfully:** 8 / 8
- **Parsed with warnings:** 3 (BSCNECIS, BSCSIA, BSSWE_C)
- **Failed:** 0
- **Parser bugs fixed this session:** 0

All MEDIUM cases are source-data quality issues — guide typos, punctuation variants, or old guide format without footer metadata. No parser changes were needed.

---

## Per-Guide Table

| Code | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone | Anomalies | Warnings | Cert Prep | Prereqs | Footer |
|------|-----------|---------|------------|-------------|----------|-----------|----------|-----------|---------|--------|
| BSCS | HIGH | 37 | 12 | 37 | — | 0 | 0 | 0 | 7 | ✓ |
| BSCNE | HIGH | 34 | 13 | 34 | — | 0 | 0 | 5 | 3 | ✓ |
| BSCNEAWS | HIGH | 35 | 13 | 35 | — | 0 | 0 | 11 | 3 | ✓ |
| BSCNEAZR | HIGH | 35 | 13 | 35 | — | 0 | 0 | 13 | 5 | ✓ |
| BSCNECIS | MEDIUM | 32 | 11 | 32 | — | 0 | 2 | 10 | 1 | ✓ |
| BSCSIA | MEDIUM | 38 | 21 | 37 | ✓ | 0 | 2 | 10 | 7 | ✓ |
| BSSWE_C | MEDIUM | 38 | 12 | 36 | — | 1 | 1 | 3 | 7 | — |
| BSSWE_Java | MEDIUM | 40 | 12 | 38 | — | 1 | 0 | 3 | 6 | — |

---

## Track Structure

**BSCNE family** (Cloud and Network Engineering, 4 guides):
- `BSCNE` — base track
- `BSCNEAWS` — Amazon Web Services specialization
- `BSCNEAZR` — Microsoft Azure specialization
- `BSCNECIS` — Cisco specialization

**BSSWE family** (Software Engineering, 2 guides):
- `BSSWE_C` — C# track
- `BSSWE_Java` — Java track

**Standalone:**
- `BSCS` — Computer Science
- `BSCSIA` — Cybersecurity and Information Assurance

Track variants share AoS group structure with different course selections. Parser handles all tracks identically — no branching needed.

---

## Standard Path Format

All 8 guides use **multi-line 3-column format** (Course Description / CUs / Term). No 2-column or single-line format variants in this family.

---

## Section Heading Variants

**"Prerequisites" variant (manifest flagged BSCSIA):** Confirmed false positive. The word "prerequisites" appears only as inline text in course descriptions: "No prerequisites are required for this course." Not a standalone section heading. No parser changes needed.

**Capstone:** Present only in BSCSIA. Correctly detected at line 1152 (after AoS at line 559). Parses cleanly.

---

## SP / AoS Reconciliation

| Code | Issue | Root Cause |
|------|-------|-----------|
| BSCNECIS | SP: `Hybrid Cloud Infrastructure and and Orchestration` / AoS: `Hybrid Cloud Infrastructure and Orchestration` | **Source guide typo** — double "and" in SP table. AoS has correct title. Not a parser bug. |
| BSCSIA | SP: `Scripting and Programming Foundations` / AoS: `Scripting and Programming - Foundations` | **Punctuation variant** — hyphen present in AoS title but absent in SP title. Source guide inconsistency. Not a parser bug. |

6 guides: 0 SP/AoS reconciliation mismatches.

---

## Quality Metrics

- **Empty descriptions:** 0 across all 8 guides
- **Empty competency lists:** 1 course in BSSWE_C — "Software Engineering" (last AoS course, old guide format, description truncated at page end, no competency trigger line present in source)
- **Footer metadata available:** 6/8 guides. BSSWE_C and BSSWE_Java are old-format guides with no footer lines; version and pub_date are unknown.

---

## BSSWE_C and BSSWE_Java — Old Guide Format

Both BSSWE track guides use an older format with no footer metadata (no `CODE YYYYMM © ...` lines). Consequences:
- `version` and `pub_date` are `null` — these dates cannot be inferred
- BSSWE_C: last AoS course (Software Engineering) has no competency trigger and no bullets — description is truncated in the source PDF
- BSSWE_Java: SP has 40 rows; AoS has 38 unique courses — 2 SP rows are course repeats across terms (expected pattern, no mismatch)

Content parsing is correct for both. MEDIUM confidence reflects missing metadata and the 1 empty-competency course, not a structural parse failure.

---

## Guides Requiring Custom Handling

None require custom handling beyond what is already documented. All 8 guides parse to usable content:

| Code | Flag | Action |
|------|------|--------|
| BSCNECIS | SP title typo ("and and") | Downstream: use AoS title as canonical |
| BSCSIA | Hyphen variant | Downstream: use AoS title as canonical |
| BSSWE_C | No footer, 1 empty-bullet course | Flag version=null; "Software Engineering" course has description but no competencies |
| BSSWE_Java | No footer | Flag version=null; content otherwise complete |

---

## Parser Changes This Session

**None.** The existing parser handles all 8 cs_ug guides without modification. All MEDIUM issues are source-data quality problems in the original guide PDFs.

---

## Rollout Decision

### READY — cs_ug family is complete

All 8 guides parsed successfully. No parser failures, no structural drift, no new branching needed.

**Summary:**
- 4/8 (50%) at HIGH confidence, 0 anomalies, 0 warnings
- 4/8 (50%) at MEDIUM confidence — all due to source-data quality (typo, punctuation, old format)
- 0/8 at LOW confidence

The cs_ug family has high cert-prep extraction density (BSCNEAWS: 11, BSCNEAZR: 13, BSCSIA: 10, BSCNECIS: 10) — certification preparation is a primary feature of this family.

### Next recommended family

Candidate order:

1. **`education_ba`** (11 guides) — education-specific sections (Student Teaching, Clinical Experiences, Field Experience); likely needs new section handlers
2. **`graduate_standard`** (9 guides) — structurally similar to standard_bs but graduate framing
3. **`teaching_mat`** (9 guides) — M.A.T. programs; may share structure with education_ba

Recommended gate before proceeding to education families: run 1 guide from `education_ba` (e.g. BAELED) as a thin-slice gate, similar to the BSMES gate for standard_bs.
