# Program Guide Section/Component Matrix

**Audit date:** 2026-03-21
**Basis:** 38 fully parsed guides (standard_bs + cs_ug + education_ba) + manifest structural data for all 115

---

## Reading this table

- **Universality:** universal = all 115 guides; common = >50%; common-optional = varies; family-specific = only certain families; rare = <10%
- **Parseability confidence:** reflects content-parse quality, not manifest probe confidence
- **Atlas use:** YES / CONDITIONAL / NO — reflecting current evidence
- **Priority:** for YES/CONDITIONAL only

---

## Section/Component Matrix

| Section / Component | Corpus Coverage | Universality | Parseability Confidence | Atlas Use | Priority | Risk / Notes |
|---------------------|----------------|-------------|------------------------|-----------|---------|-------------|
| **Guide metadata** (version, pub_date) | 84/115 (73%) | common | MEDIUM — reliable where present; absent in ~27% | YES | MEDIUM | Render gracefully when absent; do not block display |
| **Degree title** | 115/115 | universal | HIGH | CONDITIONAL | LOW | Already in Atlas via catalog; only use if catalog version missing |
| **Standard Path — course titles** | 115/115 | universal | HIGH (37/38 parsed); LOW (BSITM) | YES | HIGH | BSITM SP excluded; untouched families not yet validated |
| **Standard Path — CU values** | validated 38/115 | common | HIGH for 24 3-col guides; unknown for rest | YES — validated guides only | HIGH | Do not extrapolate to untouched families |
| **Standard Path — Term values** | ~30/38 parsed (3-col format only) | common-optional | HIGH for 3-col guides; absent in 2-col | YES — where present | HIGH | Render gracefully when absent (2-col education format) |
| **Areas of Study — group structure** | 38/38 parsed | universal in parsed | HIGH | YES | MEDIUM | Not yet validated for 77 untouched guides |
| **Course descriptions** | 38/38 parsed; 0 empty | universal in parsed | **HIGH — strongest field in corpus** | **YES** | **HIGH** | Highest-confidence content; 0 empties across 532+ courses |
| **Competency bullets** | 38/38 parsed; near-zero empty | universal in parsed | HIGH (37/38); MEDIUM for BSITM/BSSWE_C | YES | MEDIUM | Consider progressive disclosure — content is long |
| **Prerequisite mentions** (inline) | 38/38 parsed | universal in parsed | MEDIUM — known false-positive regex | CONDITIONAL | MEDIUM | Show as flag only; do not render raw extracted text |
| **Cert-prep mentions** (inline) | 27/38 parsed; 53/115 manifest | common-optional | HIGH — inline extraction reliable | **YES** | **HIGH** (cs_ug / tech) | Highest student value in tech programs; cert names explicitly stated |
| **Capstone** | 4/38 parsed; 18/115 manifest | rare-optional | HIGH — when present | CONDITIONAL | LOW | Absent in most guides; flag when present only |
| **Clinical Experiences** (AoS group) | 15+ guides estimated | family-specific | HIGH for parsed families | YES — education programs | MEDIUM | Handled as normal AoS group; no special parser needed |
| **Student Teaching** (AoS group) | 12+ guides estimated | family-specific | HIGH for parsed families | YES — education programs | MEDIUM | Same as Clinical Experiences |
| **Field Experience** | 2 confirmed | rare-subtype-specific | UNKNOWN — not yet parsed | **NO** | Deferred | Parser not yet tested; section format unknown |
| **Practicum** | 1 confirmed (MSEDL) | rare-subtype-specific | UNKNOWN — not yet parsed | **NO** | Deferred | |
| **Post-Master section** | 4 guides (nursing_pmc) | family-specific | UNKNOWN — silently skipped | **NO** | Deferred | Current parser skips without extracting |
| **Prerequisites section heading** | 4 confirmed | optional | MEDIUM — BSFIN has real section; BSCSIA is inline text only | CONDITIONAL | LOW | Requires per-guide investigation before surfacing |
| **Licensure heading** | 1 (BASPEE only) | rare | LOW — boilerplate preamble | **NO** | N/A | |
| **Accreditation section** | 115/115 | universal | N/A — boilerplate | **NO** | N/A | Parser skip |
| **Boilerplate intro** (CBE, degree plan, faculty) | 115/115 | universal | N/A — boilerplate | **NO** | N/A | Parser skip |
| **Boilerplate closing** (Accessibility, Student Services) | 115/115 | universal | N/A — anchor | **NO** | N/A | Used as end-of-content parser anchor only |

---

## Section confidence rationale

### Highest confidence
- **Course descriptions:** 0 empty descriptions across 38 parsed guides (532+ courses). Robust across 3 structurally different families. This is the cleanest field in the entire pipeline.
- **Competency bullets:** Near-zero empty (2 cases, both known PDF artifact sources). Robust across all guide structures.
- **Cert-prep mentions:** Inline text extraction. Highly reliable where present. Particularly valuable in cs_ug.

### Medium confidence
- **Standard Path course titles:** Reliable for 37/38 parsed. BSITM is excluded (LOW confidence). Untouched families need gate testing.
- **CU values:** Parsed correctly for all 3-col guides. 2-col education guides have CU but no Term. Untouched families untested.
- **Prerequisite mentions:** Extraction works but a known false-positive regex pattern exists. Do not surface raw text — use as a flag only.

### Lower confidence / deferred
- **Field Experience, Practicum, Post-Master:** Section formats unknown. Parser has not been run against these guides.
- **Prerequisites section (as dedicated heading):** Confirmed for BSFIN but content format not fully characterized.
- **Endorsement family structure:** Unknown. May differ substantially from degree program format.

---

## Sections that should NOT be used yet

| Section | Reason |
|---------|--------|
| BSITM Standard Path course/title data | LOW confidence — PDF column extraction failure; SP titles are garbled |
| SP data for 4 Sped education_ba guides | 1 course missing from AoS per guide; cross-reference SP count |
| Any section from untouched families | Not yet validated; 77 guides with 0 content parses |
| Field Experience content | Parser not yet run against guides with this section |
| Post-Master content | Silently skipped by current parser |
| Practicum content | Parser not yet run against MSEDL |
| Raw prereq text | False-positive regex; display as flag only |
