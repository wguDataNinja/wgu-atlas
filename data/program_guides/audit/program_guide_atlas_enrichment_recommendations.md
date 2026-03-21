# Program Guide Atlas Enrichment Recommendations

**Audit date:** 2026-03-21
**Scope:** Based on 38 fully parsed guides (standard_bs / cs_ug / education_ba)

---

## What Should Enrich Atlas First

### 1. Course Descriptions

**Value to students:** High. Students get zero inline course descriptions from the raw WGU catalog. Program guides contain a paragraph description per course explaining what it covers and why it matters. This is the single biggest student-facing gap Atlas can close.

**Reliability / parse confidence:** HIGH. 0 empty descriptions across 38 parsed guides (532+ courses). Robust across all three structurally different families. No known systematic accuracy issues.

**Suggested Atlas use:** Surface course descriptions on program detail pages, grouped by AoS area. Optionally surface on individual course detail pages (requires Phase E course-code matching first).

**Priority:** HIGH

**Caveats:** Phase E (course-code matching) is required before descriptions can be wired to existing `courses/{code}` detail pages. On program pages, descriptions can be displayed without course codes.

---

### 2. Certification-Prep Mentions

**Value to students:** Very high for tech-oriented programs. Students in cs_ug programs (Cloud/Network Engineering, Cybersecurity, etc.) often choose WGU specifically for industry certification alignment. Surfacing which courses prepare for specific certification exams (CompTIA A+, AWS Solutions Architect, Azure Administrator, etc.) is high-signal information not available in the catalog.

**Reliability / parse confidence:** HIGH. Inline text extraction is reliable. Cert exam names are explicitly stated in guide descriptions. 27/38 parsed guides have mentions. High density in cs_ug (10–13 mentions per guide).

**Suggested Atlas use:** Per-course cert-prep attribute on program pages ("Prepares for: CompTIA Project+"). Could also drive a cross-program cert alignment view in the future.

**Priority:** HIGH (especially for cs_ug, tech-adjacent standard_bs)

**Caveats:** Only meaningful for parsed families. Not yet available for grad CS, SWE grad, etc. — those will add more cert density when parsed.

---

### 3. Standard Path — Ordered Course List with CU Values

**Value to students:** The Standard Path table shows the official recommended course sequence with CU values per course. This helps students understand pacing and total CUs per term. The catalog shows course rosters but not this structured term-lane sequence.

**Reliability / parse confidence:** HIGH for 3-col format guides (standard_bs + cs_ug + educational_studies education_ba). LOW for BSITM (must be excluded). For 2-col education guides, CU values are present but Term is absent.

**Suggested Atlas use:** Display Standard Path table on program detail pages. Group by term (where Term column present) or as flat ordered list (where Term absent). Show CUs per course. This complements or replaces the current roster display.

**Priority:** HIGH

**Caveats:** BSITM must be excluded. Teacher licensure education_ba guides (BAELED, BASPEE, BASPMM) have CUs but no term numbers — render as ordered list rather than term-grouped view. Only available for 38 parsed programs until corpus coverage increases.

---

### 4. Areas of Study Group Structure

**Value to students:** AoS groupings reveal how WGU organizes courses into subject areas (e.g., "Data Analytics / Business Core / General Education"). This gives students a mental model for the program structure that the flat roster does not provide.

**Reliability / parse confidence:** HIGH. 0 empty groups across 38 parsed guides. Group names are program-specific and consistently extracted.

**Suggested Atlas use:** Display AoS group labels on program pages as a section-organization layer alongside or instead of the flat term-lane roster. Group courses visually by subject area.

**Priority:** MEDIUM

**Caveats:** AoS group names vary considerably across programs (expected). Not yet available for 77 untouched guides. Rendering design should degrade gracefully for unparsed programs.

---

### 5. Competency Bullets

**Value to students:** Competency bullets are the learning-outcome statements per course ("Upon completing this course, students will be able to..."). This is the most granular learning-expectations data available from guides.

**Reliability / parse confidence:** HIGH (near-zero empty). Known exceptions: BSITM (1 course) and BSSWE_C (1 course) have empty competency lists due to PDF format artifacts.

**Suggested Atlas use:** Progressive disclosure (show/hide) on program pages or course detail pages. The full competency list per course is long — do not show by default. Could be a "View competencies" expand action.

**Priority:** MEDIUM

**Caveats:** Content is dense; progressive disclosure is required for usability. Phase E (course-code matching) needed before wiring to course detail pages.

---

### 6. Clinical Experiences / Student Teaching as AoS Group Labels

**Value to students:** Students in education and teacher licensure programs need to understand that their program includes clinical/field components. The guide makes this explicit; the catalog does not.

**Reliability / parse confidence:** HIGH for parsed education families (BAELED, BASPEE, BASPMM, BSMES). These appear as normal AoS groups — no special handling needed.

**Suggested Atlas use:** When an AoS group is labeled "Clinical Experiences" or "Student Teaching," surface it distinctly on the program page — perhaps as a highlighted callout indicating field/clinical requirements.

**Priority:** MEDIUM for education programs

**Caveats:** Only 4 education_ba guides and BSMES are currently parsed with these groups. Teaching_mat, education_bs, and education_ma will add more when parsed.

---

## What Should NOT Be Used Yet

| Item | Reason |
|------|--------|
| **BSITM Standard Path data** | LOW confidence; SP titles garbled by PDF extraction failure |
| **4 Sped education_ba AoS outputs** | 1 missing course in AoS per guide (BAESSPEE/BAESSPMM/BASPEE/BASPMM) |
| **Raw prereq text** | Known false-positive pattern in prereq regex; do not display text — flag only |
| **Any data from 77 untouched guides** | No content parse done |
| **Endorsement, nursing, Field Experience, Practicum, Post-Master** | Untested section patterns; parser not validated against these |
| **Course descriptions wired to course detail pages** | Requires Phase E (course-code matching) first |
| **Guide metadata as source of degree title** | Use catalog degree title; guide title is secondary confirmation only |

---

## What Should Remain Internal-Only for Now

| Item | Status |
|------|--------|
| Parsed JSON files (`data/program_guides/parsed/`) | Internal build artifacts; not yet site-ready |
| Validation files (`data/program_guides/validation/`) | Internal QA artifacts |
| Manifest rows (`data/program_guides/manifest_rows/`) | Internal corpus characterization |
| Family validation summaries | Internal rollout records |
| Prereq mentions (raw text) | Internal reference only; do not surface |

---

## What Needs Another Validation Pass Before Use

| Item | What's Needed |
|------|-------------|
| **CU values across untouched families** | Graduate families have different CU-per-term expectations; validate against known graduate guide structure before surfacing |
| **Term values for education_ba teacher licensure** | No Term column; verify that term-grouped display degrades gracefully |
| **Prereq flag accuracy** | Spot-check a sample of prereq-flagged courses to estimate false-positive rate before deciding whether to show as flag |
| **Course-code matching** | Phase E gate test needed before any description/competency data can be linked to Atlas course codes |
| **Phase D build script** | Site artifact generation schema and build logic needs to be designed and validated before integration |

---

## Integration Readiness Summary

| Guide-derived content | Integration-ready now? | Blocker |
|-----------------------|----------------------|---------|
| Course descriptions (38 programs) | Yes — internal artifacts ready | Phase D build script and Phase E matching needed before site wiring |
| Cert-prep mentions (27 programs) | Yes — internal artifacts ready | Same Phase D blocker |
| SP ordered course list (37 programs, BSITM excluded) | Yes — internal artifacts ready | Same Phase D blocker |
| CU values (37 programs) | Yes — internal artifacts ready | Same Phase D blocker |
| Competency bullets (38 programs) | Yes — internal artifacts ready | Same Phase D blocker + UX design for progressive disclosure |
| AoS group structure (38 programs) | Yes — internal artifacts ready | Same Phase D blocker |
| All data for 77 untouched programs | No | Parsing not done |
| Course descriptions wired to course detail pages | No | Phase E (course-code matching) not done |
