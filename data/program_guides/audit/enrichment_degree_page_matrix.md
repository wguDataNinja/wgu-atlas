# Program Guide — Degree-Page Enrichment Matrix

**Date:** 2026-03-21
**Coverage basis:** 115/115 guides parsed (Phase C complete)
**Scope:** Which program-guide fields are ready to surface on Atlas degree/program pages

---

## Summary

| Metric | Value |
|--------|-------|
| Total guides | 115 |
| HIGH confidence | 96 (83.5%) |
| MEDIUM confidence | 17 (14.8%) |
| LOW confidence | 2 (1.7%) — AoS usable, SP excluded |
| Total AoS courses | 2,593 |
| Course descriptions available | 2,593 / 2,593 (100%) |
| Competency bullet sets available | 2,591 / 2,593 (99.9%) |
| Total SP course-term rows | 2,568 |

---

## Field-by-Field Readiness

### 1. Course Descriptions (AoS)
- **Source:** `areas_of_study[*].courses[*].description`
- **Coverage:** 2,593 / 2,593 courses across all 115 guides — **100%**
- **Quality gate for degree-page use:** HIGH + MEDIUM (all 113 usable guides)
- **Notes:** 0 empty descriptions across the entire corpus. This is the strongest, most complete field. Degree-page use is safe for all non-LOW guides.

### 2. AoS Group Structure
- **Source:** `areas_of_study[*].group`
- **Coverage:** All 115 guides — varies 1–9 groups per guide
- **Quality gate:** HIGH + MEDIUM
- **Notes:** Group labels reveal the program's internal subject-area organization. Consistently extracted. Useful for visual organization of the course list on degree pages.

### 3. Standard Path — Course List + CU Values
- **Source:** `standard_path[*].{title, cus}`
- **Coverage:** 113 guides with usable SP (all except BSITM, MSCSUG)
- **Quality gate:** HIGH + MEDIUM (note: LOW guides BSITM and MSCSUG excluded from SP; their AoS is usable)
- **CU availability:** 113/113 usable guides have CU values in SP
- **Notes:** 2,568 SP rows total. CU values are present for all usable SP guides. BSITM and MSCSUG must be excluded from SP display; they can still show AoS content.

### 4. Standard Path — Term Numbers
- **Source:** `standard_path[*].term`
- **Coverage:** Term numbers available in 95 of 113 usable-SP guides (84%)
- **Families WITHOUT term numbers:** education_bs (4 guides, 2-col SP), endorsement (7 of 8 use CU-only format), teaching_mat (7 of 9 use CU-only format)
- **Quality gate:** HIGH + MEDIUM (show term-grouped view when term present; ordered-list fallback when absent)
- **Notes:** When Term is absent, the SP still provides an ordered course sequence. Render as flat ordered list (not term-grouped) for endorsement, education_bs, and most teaching_mat guides.

### 5. Competency Bullets
- **Source:** `areas_of_study[*].courses[*].competency_bullets`
- **Coverage:** 2,591 / 2,593 courses — 99.9%
- **Zero-bullet exceptions:** BSITM (1 course), standard_bs/BSSWE_C (1 course) — PDF format artifacts
- **Quality gate:** HIGH + MEDIUM (with 2-exception suppression)
- **Render recommendation:** Progressive disclosure (show/hide). Dense content; do not expand by default.

### 6. Certification-Prep Mentions
- **Source:** `areas_of_study[*].courses[*].description` (inline text, not a separate field)
- **Density:** Highest in cs_ug (10–15 mentions per guide), cs_grad, data_analytics_grad
- **Notes:** Not a structured field in the parsed JSON. Would require a Phase E text-extraction pass to surface as structured cert-prep attribute. For now, content is present in descriptions.

### 7. Prerequisite Mentions
- **Source:** `areas_of_study[*].courses[*].prerequisite_mentions`
- **Coverage:** Available but known false-positive pattern in prereq regex
- **Recommendation:** Internal reference only — do not surface as structured data without a spot-check validation pass.

---

## Per-Family Summary

| Family | Guides | Conf | SP usable | SP has Term | AoS usable | Degree-page recommendation |
|--------|--------|------|-----------|-------------|------------|---------------------------|
| standard_bs | 19 | 16H 2M 1L | 18/19 | 18/19 | 19/19 | Include all; exclude BSITM SP |
| cs_ug | 8 | 4H 4M | 8/8 | 8/8 | 8/8 | Include all |
| education_ba | 11 | 5H 6M | 11/11 | 8/11 | 11/11 | Include all; flat-list for 3 no-term guides |
| graduate_standard | 9 | 9H | 9/9 | 8/9 | 9/9 | Include all |
| mba | 3 | 3H | 3/3 | 3/3 | 3/3 | Include all |
| healthcare_grad | 2 | 2H | 2/2 | 2/2 | 2/2 | Include all |
| education_bs | 4 | 4H | 4/4 | 0/4 | 4/4 | Include all; flat-list (no term column) |
| teaching_mat | 9 | 8H 1M | 9/9 | 2/9 | 9/9 | Include all; flat-list for 7 no-term guides |
| cs_grad | 5 | 4H 1L | 4/5 | 5/5 | 5/5 | Include 4H; exclude MSCSUG SP; AoS for all 5 |
| swe_grad | 4 | 3H 1M | 4/4 | 4/4 | 4/4 | Include all |
| data_analytics_grad | 3 | 3H | 3/3 | 3/3 | 3/3 | Include all |
| education_ma | 9 | 9H | 9/9 | 9/9 | 9/9 | Include all |
| endorsement | 8 | 8H | 8/8 | 1/8 | 8/8 | Include all; flat-list for 7 no-term guides |
| nursing_msn | 5 | 5H | 5/5 | 5/5 | 5/5 | Include all |
| nursing_pmc | 4 | 4H | 4/4 | 4/4 | 4/4 | Include all |
| accounting_ma | 5 | 5H | 5/5 | 5/5 | 5/5 | Include all |
| nursing_ug | 2 | 2M | 2/2 | 2/2 | 2/2 | Include both; BSNU missing metadata; BSPRN dual-track SP caveat |
| nursing_rn_msn | 3 | 3H | 3/3 | 3/3 | 3/3 | Include all; degree_title cosmetic truncation |
| education_grad | 2 | 1H 1M | 2/2 | 2/2 | 2/2 | Include both; MEDETID capstone partial |

---

## Per-Guide Exclusions and Caveats

| Code | Field affected | Caveat / exclusion | Source |
|------|---------------|-------------------|--------|
| BSITM | Standard Path | EXCLUDE SP — source PDF column extraction failure | Source artifact |
| MSCSUG | Standard Path | EXCLUDE SP — source PDF column extraction failure | Source artifact |
| BSPRN | Standard Path | SP = Pre-Nursing track only (19 courses); 15 Nursing-track courses AoS-only | Structural dual-track |
| BSNU | Metadata | version/pub_date/page_count not recoverable (no footer in source PDF) | Source artifact |
| MSRNNUED | degree_title | Truncated: "...Nursing +" (cosmetic) — use catalog degree title | Combined-guide format |
| MSRNNULM | degree_title | Same truncation as MSRNNUED | Combined-guide format |
| MSRNNUNI | degree_title | Same truncation as MSRNNUED | Combined-guide format |
| MSCSAIML | degree_title | Truncated in parsed output (cosmetic) | PDF extraction artifact |
| MACCM | Description | "Corporate Financial Analysis" title/first-sentence quality issue (cosmetic) | Source text |
| MEDETID | Capstone | Only first of 3 capstone courses captured | Multi-capstone structural |
| MAELLP12 | Metadata | page_count=0 (cosmetic) | Older guide format |

---

## Recommended Phase D Quality Gate

**Recommended inclusion policy:**

1. **HIGH confidence:** Include all fields (SP + AoS) without caveats.
2. **MEDIUM confidence:** Include AoS fields (descriptions, groups, competency bullets). Review SP on a per-guide basis — most MEDIUM guides have clean SP with one structural caveat.
3. **LOW confidence (BSITM, MSCSUG):** Include AoS content only. Exclude SP entirely.

**Total guides passing recommended gate:** 115/115 (AoS) + 113/115 (SP)

**Not recommended for Phase D inclusion:**
- BSITM SP, MSCSUG SP (source artifact failures — known, stable exclusions)
- Prereq mentions as structured data (false-positive risk)
- Competency bullets at BSITM and BSSWE_C for one course each (empty — suppress)
