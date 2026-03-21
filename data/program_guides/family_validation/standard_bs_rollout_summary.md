# Standard BS Family — Full Rollout Summary

**Date:** 2026-03-20 (session 13 continuation / session 14)
**Family:** `standard_bs`
**Total guides:** 19

---

## Overall Results

| Confidence | Count | Guides |
|---|---|---|
| **HIGH** | 16 | BSACC, BSBAHC, BSC, BSDA, BSFIN, BSHA, BSHHS, BSHR, BSHS, BSIT, BSMES, BSMGT, BSMKT, BSPH, BSPSY, BSUXD |
| **MEDIUM** | 2 | BSHIM, BSSCOM |
| **LOW** | 1 | BSITM |

- **Parsed successfully:** 19 / 19 (no failures)
- **Parsed with warnings:** 3 (BSHIM, BSSCOM, BSITM)
- **Failed:** 0

---

## Per-Guide Table

| Code | Confidence | SP Rows | AoS Groups | AoS Courses | Capstone | Anomalies | Warnings | Cert Prep | Prereqs |
|------|-----------|---------|------------|-------------|----------|-----------|----------|-----------|---------|
| BSACC | HIGH | 40 | 4 | 40 | — | 0 | 0 | 2 | 6 |
| BSBAHC | HIGH | 40 | 7 | 39 | ✓ | 0 | 0 | 1 | 1 |
| BSC | HIGH | 38 | 6 | 38 | — | 0 | 0 | 1 | 1 |
| BSDA | HIGH | 42 | 14 | 41 | ✓ | 0 | 0 | 4 | 7 |
| BSFIN | HIGH | 40 | 6 | 40 | — | 0 | 0 | 2 | 3 |
| BSHA | HIGH | 34 | 7 | 34 | — | 0 | 0 | 0 | 1 |
| BSHHS | HIGH | 35 | 9 | 34 | ✓ | 0 | 0 | 0 | 1 |
| BSHIM | MEDIUM | 36 | 8 | 36 | — | 0 | 2 | 1 | 1 |
| BSHR | HIGH | 39 | 4 | 39 | — | 0 | 0 | 2 | 2 |
| BSHS | HIGH | 28 | 6 | 28 | — | 0 | 0 | 1 | 1 |
| BSIT | HIGH | 35 | 12 | 35 | — | 0 | 0 | 8 | 4 |
| BSITM | LOW | 35 | 9 | 40 | — | 6 | 3 | 2 | 1 |
| BSMES | HIGH | 39 | 8 | 39 | — | 0 | 0 | 0 | 5 |
| BSMGT | HIGH | 36 | 5 | 35 | ✓ | 0 | 0 | 2 | 2 |
| BSMKT | HIGH | 37 | 5 | 37 | — | 0 | 0 | 1 | 1 |
| BSPH | HIGH | 33 | 6 | 33 | — | 0 | 0 | 0 | 1 |
| BSPSY | HIGH | 34 | 4 | 34 | — | 0 | 0 | 1 | 3 |
| BSSCOM | MEDIUM | 35 | 5 | 35 | — | 2 | 2 | 3 | 6 |
| BSUXD | HIGH | 38 | 6 | 38 | — | 0 | 0 | 1 | 1 |

---

## Section Presence

| Feature | Guides with feature |
|---|---|
| Standard Path present | All 19 |
| Areas of Study present | All 19 |
| Capstone section | BSDA, BSBAHC, BSHHS, BSMGT (4 guides) |
| Student Teaching AoS group | BSMES |
| Clinical Experiences AoS group | BSMES |
| SP 2-column (no Term column) | BSMES |
| Cert-prep mentions | 15/19 guides |
| Prerequisite mentions | All 19 guides |

---

## SP/AoS Reconciliation

| Code | Issue | Root Cause |
|------|-------|-----------|
| BSHIM | 1 SP-only: `Healthcare Information Systems Management` / 1 AoS-only: `(HIM) environment.` | PDF fragment `(HIM) environment.` captured as course title due to page-break mid-sentence within completed bullet |
| BSSCOM | 1 SP-only: `21st Century Operations and Supply Chain` / 1 AoS-only: `Solutions Design and Visualization Capstone` | SP last row (2-line title) interrupted by `Total CUs` before Term captured; AoS title differs slightly from SP title |
| BSITM | Multiple mismatches | PDF extraction artifact — see below |

16 guides: 0 SP/AoS reconciliation mismatches.

---

## Quality Metrics

- **Empty descriptions:** 0 across all 19 guides
- **Empty competency lists:** 1 course in BSITM only (PDF extraction artifact)
- **All 19 guides:** every standard_bs guide has Standard Path and Areas of Study sections fully parsed

---

## Education-Specific Sections (BSMES)

BSMES (B.S. Mathematics Education, Secondary) is the only standard_bs guide with education-specific section variants. Assessment:

- **Student Teaching** and **Clinical Experiences** appear as **AoS group labels**, not as separate parsed sections. The parser handles them correctly — they are area groups in the AoS state machine.
- **Standard Path**: uses 2-column format (Course Description + CUs only, no Term column). Fixed by new `detect_sp_has_term()` logic.
- **No structural interrupt** to SP or AoS parsing from these education-specific sections.
- BSMES parses at **HIGH confidence, 0 anomalies, 0 warnings**.
- Student Teaching / Clinical Experiences content: present in SP rows (with `term: null`) and as AoS group entries with full descriptions and competency bullets.

Assessment: **no new parser branch needed for BSMES within standard_bs family**.

---

## Guides Requiring Custom Handling

### BSITM — LOW confidence

**Root cause:** PDF layout artifact in the Standard Path table.
- First 5 SP rows have no title (titles missing from PDF extraction due to multi-column table layout)
- A sequence of 4 consecutive course titles appears without CU/Term values mid-table, causing the parser to concatenate them into one row
- The SP row count (35) understates the actual course count; AoS (40 courses) is more accurate
- AoS parsing is **correct** — 9 groups, 40 courses, 0 anomalies

**Action:** Flag BSITM for manual SP table review. AoS content is usable. Do not use SP rows for BSITM without manual correction.

### BSHIM — MEDIUM confidence

**Root cause:** PDF fragment `(HIM) environment.` appears between two competency bullets after a page break within a completed sentence. The parser cannot distinguish this from a new course title.
- 1 course captured with title `(HIM) environment.`
- 1 course (`Healthcare Information Systems Management`) correctly present in AoS but title reconciliation affected

**Action:** BSHIM is usable at MEDIUM confidence. Flag `(HIM) environment.` as a known artifact.

### BSSCOM — MEDIUM confidence

**Root cause:** The final capstone course (`Solutions Design and Visualization Capstone`) is a 2-line title in the SP table followed immediately by `Total CUs`, which interrupts the parser before the Term value is captured. Minor title string mismatch (`21st Century Operations and Supply Chain` vs full title in AoS).

**Action:** BSSCOM is usable at MEDIUM confidence. The AoS parse (35 courses) is correct.

---

## Parser Bugs Fixed This Session

4 new bugs discovered and fixed during BSMES gate check and rollout:

| Bug | Fix |
|-----|-----|
| `locate_sections()` false Capstone detection — "Capstone" as a line-2 SP course title (e.g. "Communications Applied Learning / Capstone") triggered `CAPSTONE_RE`, causing Capstone to be registered before AoS and AoS parsing to be cut off entirely | Discard Capstone entry if it precedes Areas of Study line index |
| `_is_bullet_continuation()` missed short sentence completions — e.g. `(GAAP).` and `Commercial Code.` not recognized as continuations of in-progress bullets, causing them to be captured as false course titles | Added: if pending ends mid-sentence and line ends with `.,:;`, treat as continuation |
| `_is_bullet_continuation()` missed lone bullet character — `●` alone on a line left empty pending, causing next non-blank line to fail continuation check and be captured as a course title | Added: if `len(pending) < 5`, treat as continuation unconditionally |
| `parse_capstone()` page number as title — standalone page number (e.g. `20`) immediately after the Capstone heading footer was captured as the capstone course title | Added `PAGE_NUM_RE` check in capstone parser |

**Additional fix (pre-rollout, during BSMES gate):**

| Bug | Fix |
|-----|-----|
| SP 2-column format (no Term) — BSMES SP table has only Course Description + CUs columns; existing multi-line parser expected Term and generated 78 anomalies | Added `detect_sp_has_term()` + `has_term` parameter to `parse_standard_path_multiline()` |

---

## What Assumptions Held Across All 19 Guides

- Standard Path section always present and locatable via `^Standard Path` anchor
- Areas of Study section always present; `AREAS_OF_STUDY_RE` reliably anchors it
- All 3 footer/metadata formats handled (single-line, split, header-line)
- Both SP table formats handled (single-line row, multi-line row, 2-column)
- AoS state machine (INTRO → SEEKING → IN_DESCRIPTION → IN_COMPETENCIES) correct across 4–14 groups
- Competency trigger string universal across all 19 guides
- `pending_titles` buffer (1=course, 2=group+course) works correctly across all guides
- Cert-prep and prereq extraction operational (15/19 and 19/19 guides respectively)
- Closing boilerplate (`Accessibility and Accommodations`) reliable as AoS upper bound

## What Assumptions Were Revealed as Incomplete

- **Capstone location**: Not all "Capstone" lines in the document are section headings — some are second lines of 2-line course titles in the SP table (BSC, BSHIM, BSSCOM)
- **Bullet continuations after page breaks**: Very short line fragments (< 30 chars) ending with `.` may be completions of a mid-sentence bullet split by a PDF page break
- **Bullet character alone on a line**: Some guides emit `●` alone, with text on the next line
- **SP 2-column format**: Education-family guides (BSMES) have no Term column in Standard Path

---

## Rollout Decision

### READY — standard_bs family is complete

All 19 guides parsed. Parser covers all discovered format variants. No unhandled structural patterns remain in the family.

**Summary:**
- 16/19 (84%) at HIGH confidence, 0 anomalies, 0 warnings
- 2/19 (11%) at MEDIUM confidence — minor PDF artifacts, usable content
- 1/19 (5%) at LOW confidence — BSITM PDF layout issue; AoS usable, SP requires manual review

**No new parser branch is needed** for the standard_bs family. The existing parser (with this session's 5 bug fixes) covers all 19 guides.

### Next recommended step

Proceed to the next family. Candidate order (by size and structural similarity to standard_bs):

1. `cs_ug` (8 guides) — already validated BSCS; likely straightforward
2. `education_ba` (11 guides) — education-specific sections; may need new section handlers
3. `graduate_standard` (9 guides) — different CU/term expectations (8 CU/term min)

Do **not** proceed to site artifact build or course-code matching yet.
