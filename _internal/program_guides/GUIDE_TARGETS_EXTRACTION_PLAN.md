# Guide Targets Extraction Plan

**Created:** 2026-03-21
**Purpose:** Execution plan for next-session recovery of three confirmed data targets from the guide corpus.
**Status:** Ready to execute
**Precondition:** Guide corpus fully parsed and validated. cert_prep_mentions and prerequisite_mentions fields already populated in all 115 parsed JSONs. All three targets have been sighted and their signal patterns confirmed.

---

## Mindset contract

If the current extraction detected it — even fragmentarily — the meaning is recoverable.
"Messy" is a description of the current shape, not a verdict on recoverability.
This document explains how to go get cleaner versions of signals that already exist.

---

## 1. Certification Mapping

### Target data model

```
normalized_cert        → canonical cert name (e.g. "CompTIA A+")
source_course_title    → guide course title carrying the mention
matched_course_code    → resolved catalog code for that course
source_program_codes   → list of programs whose guides confirm this mapping
confidence             → high / medium / low
atlas_recommendation   → use / use-with-filter / degree-only / review-required
```

Cert → program membership is derived transitively: if `Course X → Cert Y` and `Course X ∈ Program Z`, then `Program Z → Cert Y`. No separate cert-to-program mapping step needed once course-level is clean.

### How the signals were found

Source field: `certification_prep_mentions` array on each AoS course object in every `parsed/*.json`.
The extractor captured substrings from course description text matching cert-adjacent patterns.
The field is already populated — no re-parsing is needed. The work is normalization and filtering.

### Signal classes — how to separate them

**Class 1: Named CompTIA certifications**
Pattern: String begins with "CompTIA " followed by a cert name.
Clean instances: `CompTIA A+`, `CompTIA Network+`, `CompTIA Security+`, `CompTIA Cloud+`, `CompTIA Project+`, `CompTIA CySA+`, `CompTIA Cybersecurity`
Artifact: `CompTIA Project+.` (trailing period) — same cert, punctuation strip normalizes it.
Recovery: Trim trailing punctuation, then match against a CompTIA cert name whitelist.

**Class 2: AWS certification strings**
Clean instances: `AWS Certified` (exact phrase appears in 7 programs on Cloud Foundations)
Clean but narrow: `AWS Cloud`, `AWS CLI`, `AWS Capstone`, `AWS platform`, `AWS environment` — all from BSCNEAWS, all program-specific
Noise class: `aws in`, `aws that`, `aws and`, `aws of`, `aws to`, `aws upon`, `aws are`, `aws affecting`, `aws from`, `aws on` — these are substring matches from words like "laws", "draws", "straws" appearing in course text. Source word ends in "-aws" and the extractor matched the suffix. There are ~45 of these across the corpus.
Recovery: Whitelist exact clean AWS strings (`AWS Certified`, `AWS Cloud`, `AWS CLI`). Suppress everything matching `^aws [a-z]` (lowercase-aws + space + lowercase word) — this pattern exclusively matches the noise class.

**Class 3: Azure certification strings**
All from BSCNEAZR only. Single-program signal.
Clean: `Azure Fundamentals`, `Azure services`, `Azure platform`, `Azure environment`, `Azure Solution`, `Azure CLI`
Artifact: `Azure services;` (trailing semicolon), `Azure platform.` (trailing period) — strip punctuation.
Recovery: Match against Azure cert/service name whitelist after punctuation stripping.

**Class 4: Cisco certification strings**
All from BSCNECIS only. Single-program signal.
Clean: `Cisco Certified`, `Cisco Cybersecurity`, `Cisco DevNet`
Noisy: `Cisco practices`, `Cisco Environment.`, `Cisco tools` — vendor-adjacent fragments, not cert names.
Recovery: Whitelist `Cisco Certified`, `Cisco Cybersecurity`, `Cisco DevNet` only.

**Class 5: Praxis exam signals**
Education programs only.
Clean codes: `Praxis 5039` (MATEES — Earth Science), `Praxis 5081` (MATSSES — Social Studies)
Artifact: `Praxis exam,` (4 programs — trailing comma), `Praxis prep,` (4 programs — trailing comma), `Praxis Social` (fragment)
Recovery: Normalize `Praxis exam,` → `Praxis` (generic signal), normalize `Praxis 5039` / `Praxis 5081` → specific exam code references. Check whether the program's AoS course title identifies which content-area exam applies.

**Class 6: Accounting**
`CPA Code` — one instance in BSACC. Thin extraction. The CPA connection is richer in the program description than in the course-level extraction. Add to review table; do not auto-accept.

### Normalization whitelist (first pass)

Apply this whitelist to all `certification_prep_mentions` values across the corpus:

```
WHITELIST_EXACT_MATCH = [
  "CompTIA A+",
  "CompTIA Network+",
  "CompTIA Security+",
  "CompTIA Cloud+",
  "CompTIA Project+",
  "CompTIA CySA+",
  "CompTIA Cybersecurity",
  "AWS Certified",
  "AWS Cloud",
  "AWS CLI",
  "Azure Fundamentals",
  "Cisco Certified",
  "Cisco Cybersecurity",
  "Cisco DevNet",
  "Praxis 5039",
  "Praxis 5081",
]

WHITELIST_AFTER_PUNCT_STRIP = [
  "CompTIA Project+",  # catches "CompTIA Project+."
  "Azure services",    # catches "Azure services;"
  "Azure platform",    # catches "Azure platform."
]

SUPPRESS_PATTERN = r'^aws [a-z]'  # catches all lowercase "aws [word]" fragments
```

After stripping trailing punctuation from all values, apply exact match against combined whitelist. Anything not matching goes to the noise bucket — log it, don't discard, it may surface new cert families.

### High-confidence cert → course candidate table

These have been confirmed by cross-program consistency (≥5 independent programs):

| normalized_cert | source_course_title | source_program_count | example_programs | confidence | atlas_recommendation | recovery_method |
|---|---|---|---|---|---|---|
| CompTIA A+ | IT Applications | 7 | BSCNE, BSCSIA, BSIT, BSCNEAWS, BSCNEAZR, BSCNECIS, MSITUG | HIGH | use | Whitelist exact match; cross-program confirmed |
| CompTIA A+ | IT Foundations | 7 | BSCNE, BSCSIA, BSIT, BSCNEAWS, BSCNEAZR, BSCNECIS, MSITUG | HIGH | use | Whitelist exact match; cross-program confirmed |
| CompTIA Network+ | Networks | 6 | BSCNE, BSCSIA, BSIT, BSCNEAWS, BSCNEAZR, BSCNECIS | HIGH | use | Whitelist exact match; cross-program confirmed |
| CompTIA Security+ | Network and Security - Applications | 5 | BSCNE, BSCSIA, BSIT, BSCNEAWS, BSCNEAZR | HIGH | use | Whitelist exact match; cross-program confirmed |
| CompTIA Project+ | Business of IT - Applications | 6 | BSDA, BSIT, BSCSIA, BSSWE_C, BSSWE_Java, MSSWEUG | HIGH | use | Whitelist after punct-strip; cross-program confirmed |
| AWS Certified | Cloud Foundations | 7 | BSCNEAWS, BSDA, BSIT, BSSWE_C, BSSWE_Java, MSCSAIML, MSITUG | HIGH | use | Whitelist exact match; cross-program confirmed |
| CompTIA Cloud+ | Cloud Applications / Cloud Security | 3 | BSCNE, BSCNECIS, BSIT | MEDIUM | use | Whitelist exact match; confirm course title mapping |
| CompTIA CySA+ | Cyber Defense and Countermeasures | 1 | BSCSIA | MEDIUM | use | Whitelist exact match; single-program but clean |
| Azure Fundamentals | Various cloud courses | 1 | BSCNEAZR | MEDIUM | degree-only | Single-program; surface at degree level only |
| Cisco Certified | Various Cisco courses | 1 | BSCNECIS | MEDIUM | degree-only | Single-program; surface at degree level only |
| Praxis 5039 | Earth Science content courses | 1 | MATEES | MEDIUM | use | Exact code match; exam code is official |
| Praxis 5081 | Social Studies content courses | 1 | MATSSES | MEDIUM | use | Exact code match; exam code is official |
| Praxis exam | Various content area courses | 4 | BAESSESC, BAESSESP, ENDSESC, ENDSESP | MEDIUM | degree-only | Normalize from "Praxis exam," after punct-strip |

### Auto-accept vs review queue

**Auto-accept (emit to cert-course mapping output):**
All HIGH confidence rows above. Cross-program confirmation is sufficient validation.

**Review queue (human checks before Atlas use):**
- MEDIUM confidence rows
- CPA Code (BSACC) — richer signal in program description text; needs manual confirmation
- NCLEX (nursing) — not captured at course level; present in program description; requires dedicated treatment
- Any cert string in the noise bucket that begins with a recognizable vendor name but didn't match the whitelist

### Output artifact

`data/program_guides/cert_course_mapping.json`
Schema: array of `{normalized_cert, source_course_title, matched_course_code, source_programs, confidence, atlas_recommendation}`

This file drives: cert badges on course pages, cert signals in AoS blocks on degree pages, cert-to-program transitive mapping.

---

## 2. Prerequisite Relationships

### Target data model

```
target_course_title      → the course that has the prerequisite
target_course_code       → resolved catalog code (when matchable)
prerequisite_value       → the raw extracted string (preserved)
prerequisite_type        → see types below
normalized_prereq_title  → matched course title from catalog (if resolvable)
normalized_prereq_code   → matched course code from catalog (if resolvable)
source_programs          → list of programs whose guides contain this prereq mention
confidence               → high / medium / low
review_status            → auto-accepted / review-required / suppress
notes                    → any manual annotation needed
recovery_method          → how it was or should be recovered
```

### Prerequisite relationship types

**Type 1: explicit-course-prereq**
A named course title appears as a stated prerequisite.
Example: "Calculus I is a prerequisite for this course."
Extraction: `"Calculus I"` — clean course name, directly matchable to catalog.

**Type 2: code-anchored-prereq**
A WGU course code appears in the prereq mention.
Example: `"D445"`, `"C955: Applied Probability and Statistics"`
These are the highest-confidence class — the code is already a catalog identifier.

**Type 3: cumulative-sequence-prereq**
Nursing-style: completion of all prior terms required, plus specific course codes.
Example: `"Courses: All prelicensure nursing curriculum courses from previous terms and D445"`
Not a single-course prereq. Requires different data model: program-sequence + specific code.

**Type 4: soft-preparedness**
Vague prior-experience language. No specific course named.
Example: "prior knowledge of Python is helpful", "general education math is preferred"
Not actionable as a structural prerequisite. Log and suppress for v1.

**Type 5: no-prereq-declaration (false positive class)**
The guide states explicitly that no prerequisite exists.
Canonical false positive string: `"for this course and there is no specific technical knowledge needed"`
Also: `"for this course"` (standalone), boilerplate no-prereq endings.
**These must be filtered first, before any other processing.**

**Type 6: inverted-capture**
The extraction caught a prerequisite relationship but captured the wrong direction.
Example: `"for Financial Management I is Corporate Finance"` — this means Corporate Finance is the prereq FOR Financial Management I, but the extraction captured the inverted relationship framing.
Recovery path: parse the sentence to identify which named course is the prereq and which is the target.

### How the current findings were located

Source field: `prerequisite_mentions` array on each AoS course object in `parsed/*.json`.
The extractor matched patterns in course description text near the word "prerequisite."
The field is already populated — re-parsing is not needed. The work is classification and normalization.

### First-pass filter: suppress all no-prereq false positives

Before doing anything else, remove every instance matching these patterns:

```
SUPPRESS_EXACT = [
    "for this course and there is no specific technical knowledge needed",
    "for this course",
]

SUPPRESS_PATTERN = [
    "^There is no prerequisite",
    "^No prerequisite",
    "^no prerequisite",
    "has no prerequisites",
    "are no prerequisites",
]
```

After this filter, the false positive count (currently 62+) drops to near-zero and the remaining corpus is meaningful prereq language.

### Recovery strategy by type

**Type 1 (explicit course name):**
Match extracted string against `canonical_title_current` in the course catalog.
Allow fuzzy match (Levenshtein distance ≤ 3) to catch minor wording variations.
If matched: emit with `confidence: high`, `normalized_prereq_code` populated.
If unmatched: emit with `confidence: medium`, flag for review.

**Type 2 (code-anchored):**
Extract course code pattern `[A-Z]\d{3,4}` or `[A-Z]\d{3}-[A-Z0-9]+` from the string.
Look up in catalog. If found: `confidence: high`, auto-accept.

**Type 3 (cumulative sequence — nursing):**
The sentence template is consistent: `"Courses: All prelicensure nursing curriculum courses from previous terms and [CODE]"`
Parse: (a) extract trailing course code(s), (b) tag prereq_type as `cumulative-sequence-prereq`.
Store as: `prerequisite_value: "ALL_PRIOR_TERMS"` + `additional_codes: ["D445"]` or similar.
Do not try to expand "all prior terms" into individual courses — the tag is sufficient for Atlas display.

**Type 6 (inverted capture):**
Pattern: string contains two course-name-like substrings and a "for X is Y" or "for X, Y is required" structure.
Recovery: split on "is " or "is required" or ", Y" and identify which noun phrase is the prereq.
The sentence `"for Financial Management I is Corporate Finance"` → target = Financial Management I, prereq = Corporate Finance.
Flag these for human review after automated parse attempt. Do not auto-accept.

### Program families to target first (highest prereq density and quality)

**BSCS** — 7 courses with prereqs, clean math/CS chain. Highest quality.
Chains: Applied Algebra → statistics → Calculus I → Discrete Math I → Discrete Math II → Data Structures II
Also: Data Management - Foundations → Data Management - Applications; Introduction to Python → Back-End Programming

**BSDA** — 6 courses, similar data/math chains. Second priority.

**BSACC** — 6 courses, clean accounting sequence: Principles → Financial Accounting → Intermediate I → Intermediate II.
This is the clearest sequential chain outside of CS/math.

**BSIT** — 6 courses, data management and networking prereqs.

**BSPRN** — 10 courses, nursing cumulative type. Different model; target after the code-anchored families.

**BSCSIA / BSCNE family** — moderate prereq density, mixed clean and fragment types.

### Proposed output schema (example rows)

```json
[
  {
    "target_course_title": "Data Structures and Algorithms II",
    "target_course_code": "C950",
    "prerequisite_value": "Data Structures and Algorithms I",
    "prerequisite_type": "explicit-course-prereq",
    "normalized_prereq_title": "Data Structures and Algorithms I",
    "normalized_prereq_code": "C949",
    "source_programs": ["BSCS"],
    "confidence": "high",
    "review_status": "auto-accepted",
    "notes": null,
    "recovery_method": "catalog_title_match"
  },
  {
    "target_course_title": "Discrete Mathematics I",
    "target_course_code": "C959",
    "prerequisite_value": "Calculus I",
    "prerequisite_type": "explicit-course-prereq",
    "normalized_prereq_title": "Calculus I",
    "normalized_prereq_code": "C958",
    "source_programs": ["BSCS", "BSDA"],
    "confidence": "high",
    "review_status": "auto-accepted",
    "notes": null,
    "recovery_method": "catalog_title_match"
  },
  {
    "target_course_title": "Medical Dosage Calculations",
    "target_course_code": "D220",
    "prerequisite_value": "Courses: All prelicensure nursing curriculum courses from previous terms and D445",
    "prerequisite_type": "cumulative-sequence-prereq",
    "normalized_prereq_title": null,
    "normalized_prereq_code": "D445",
    "source_programs": ["BSPRN"],
    "confidence": "medium",
    "review_status": "review-required",
    "notes": "Cumulative sequence prereq; D445 is additional specific requirement",
    "recovery_method": "template_parse + code_extraction"
  },
  {
    "target_course_title": "Financial Management I",
    "target_course_code": null,
    "prerequisite_value": "for Financial Management I is Corporate Finance",
    "prerequisite_type": "inverted-capture",
    "normalized_prereq_title": "Corporate Finance",
    "normalized_prereq_code": null,
    "source_programs": ["BSACC"],
    "confidence": "medium",
    "review_status": "review-required",
    "notes": "Inverted capture — prereq = Corporate Finance, target = Financial Management I. Verify against catalog.",
    "recovery_method": "sentence_inversion_parse"
  }
]
```

### Output artifact

`data/program_guides/prereq_relationships.json`

After first-pass recovery, expected output size: 50–100 confirmed relationships, concentrated in CS/math/data/accounting chains. That is a usable product layer — not complete coverage, but real and defensible.

---

## 3. Standard Path Family and Track Structure

### SP family classification

Every program's SP falls into exactly one of four categories:

**Category A: structured-term-path**
All courses have populated term numbers. 91 programs.
These are production-ready for term-sequenced display.

**Category B: null-term-advisor-path**
All courses have `term: null`. 23 programs.
All are education licensure, MAT, or endorsement families.
Display as: ordered course list, no term grouping. Label: "Advisor-sequenced — individual pacing varies."

**Category C: track-specialization-member**
The program is one track of a named multi-track family.
The family relationship is declared in the program's `program_description` text.
The SP is single-path (representing this track), but the degree belongs to a named family.
Requires a family grouping table (see below).

**Category D: anomalous-suppress**
SP is malformed or contains extraction failures that make it unsuitable for display.
Currently confirmed: MATSPED (catastrophic title concatenation), BSITM (partial title concatenation in one entry — verify extent), MSCSUG (accelerated bridge — SP blends bachelor's and master's terms; needs caveat label, not full suppression).

### How the family patterns were found

Source fields:
- `standard_path` array length and `term` values → Category A/B identification
- `program_description` text → Category C family declarations
- SP entry content inspection → Category D anomaly detection

The program_description field is the authoritative location for track/specialization family declarations. The JSON doesn't carry a `track_family` field — the relationship is encoded in prose.

### Family declaration language — extraction approach

For Category C programs, the program_description contains explicit language of the form:
- "offered in two tracks that utilize either Java or C#..."
- "After completing five foundational courses, learners will have the option to pursue one of four tracks: Financial Reporting, Taxation, Auditing, or Management Accounting"
- Similar language for nursing specializations

**Recovery method:** Scan `program_description` for trigger phrases: "track", "specialization", "option to pursue", "offered in", "four tracks", "two tracks". For each match, extract the family declaration sentence and identify the named tracks.

Then: cross-reference with the set of sibling program codes that share a parent program name or code prefix (e.g., MACC → MACCA, MACCF, MACCM, MACCT; MSRNN → MSRNNUED, MSRNNULM, MSRNNUNI).

### Known track/specialization families — confirmed

**BSSWE family (2 tracks):**
Members: BSSWE_Java, BSSWE_C
Declaration (both guides): "offered in two tracks that utilize either Java or C# to achieve similar objectives"
Family label: "B.S. Software Engineering"
Relationship: shared core path (33+ identical courses, same terms), diverging track-specific courses in later terms
Caveat: Both guides have independent Standard Paths; the shared courses can be derived by intersection

**MAcc family (4 tracks):**
Members: MACCA (Auditing), MACCF (Financial Reporting), MACCM (Management Accounting), MACCT (Taxation)
Declaration (MACCA guide): "After completing five foundational courses, learners will have the option to pursue one of four tracks: Financial Reporting, Taxation, Auditing, or Management Accounting"
Family label: "Master of Accounting"
Relationship: shared 5-course foundation, then track-specific divergence
Recovery: Extract the 5 foundational courses appearing in all four guides' SPs, identify divergence point

**MSRNN family (3 specializations):**
Members: MSRNNUED (Education), MSRNNULM (Leadership/Management), MSRNNUNI (Nursing Informatics)
Declaration: Graduate nursing with named specialization tracks
Family label: "M.S. Nursing — RN to MSN"
Note: degree_title truncation known; content intact

**BSCNE family (3 cloud/vendor tracks):**
Members: BSCNE (vendor-agnostic), BSCNEAWS (AWS track), BSCNEAZR (Azure track), BSCNECIS (Cisco track)
Declaration: BSCNE program description states students demonstrate competencies via "specific industry certification exams that are vendor agnostic"; the variant guides (AWS/Azure/Cisco) are vendor-specialized tracks
This family is NOT explicitly declared in a single parent guide — it's inferable from program code structure and shared course core
Recovery method: Code-prefix grouping (BSCNE*) + shared-course intersection analysis

**Education licensure vs. non-licensure families:**
Pattern: BAELED (licensure, null-term SP) vs. BAESELED (Educational Studies non-licensure, populated-term SP)
These are not the same program with a formatting difference — they are structurally different programs. The licensure program has advisor-guided pacing; the non-licensure variant has a standard term path. The SP term status IS the signal that distinguishes them.
Family: "Bachelor of Arts, Elementary Education" family
Display recommendation: Show both, with explicit label distinguishing licensure vs. non-licensure and pacing model difference.

**PMCNU family (Post-Master's Certificates):**
Members: PMCNUED, PMCNUFNP, PMCNULM, PMCNUPMHNP
Short SPs (8 courses), populated terms
Likely a specialization family; confirm with program_description text

### Target Atlas-facing family data model

```json
{
  "family_code": "BSSWE",
  "family_label": "B.S. Software Engineering",
  "family_type": "track_specialization",
  "declaration_text": "offered in two tracks that utilize either Java or C# to achieve similar objectives",
  "declaration_source_programs": ["BSSWE_Java", "BSSWE_C"],
  "members": [
    {"program_code": "BSSWE_Java", "track_label": "Java Track"},
    {"program_code": "BSSWE_C", "track_label": "C# Track"}
  ],
  "sp_relationship": "shared_core_diverging_track",
  "shared_course_count": 33,
  "display_recommendation": "surface family relationship on both degree pages; link to each track as variant"
}
```

### SP classification output table (first-pass target)

For all 115 programs, emit:

| program_code | sp_category | sp_length | term_status | family_code | notes |
|---|---|---|---|---|---|
| BSCS | A | 30 | populated | — | standard |
| BAELED | B | 37 | null | BAELED_family | licensure variant |
| BAESELED | A | 33 | populated | BAELED_family | non-licensure variant |
| BSSWE_Java | C | 40 | populated | BSSWE | track: Java |
| BSSWE_C | C | 38 | populated | BSSWE | track: C# |
| MACCA | C | ~30 | populated | MACC | track: Auditing |
| MATSPED | D | 9 | populated | — | SP malformed — suppress |
| ... | ... | ... | ... | ... | ... |

### Output artifact

`data/program_guides/sp_family_classification.json`
Array of per-program SP classification records.
Separate: `data/program_guides/sp_families.json` — family grouping definitions.

---

## 4. Known Anomaly and Issue Tracking

These are preserved findings that need explicit handling rules, not silent suppression.

### Issue 1: MATSPED — catastrophic SP concatenation

**Affected program:** MATSPED (M.A.T., Special Education)
**Issue:** SP entry at term 7, position 8 contains 20+ course titles concatenated into a single string with 4 CU. The remaining 8 SP entries are clean.
**Detection:** Inspection of SP entry title length (>500 characters). No legitimate course title is this long.
**Source-side vs extraction-side:** Extraction-side — the parser merged a multi-column or multi-row table section into one field.
**Atlas handling:** Suppress SP display entirely for MATSPED. AoS payload is intact and usable.
**WGU feedback candidate:** Yes — the source PDF structure for this program appears to have a non-standard table layout that confounded extraction. Worth preserving if reporting back.

### Issue 2: BSITM — SP title concatenation (verify extent)

**Affected program:** BSITM (B.S., Information Technology Management)
**Issue:** At least one SP entry contains concatenated course titles. The SP spans 10 terms (unusual).
**Detection:** Same pattern as MATSPED but may be more limited in scope.
**Action:** Inspect BSITM SP for all entries exceeding 100 characters. Determine whether the concatenation affects one entry or multiple. If one entry: suppress that entry only and use remaining SP. If multiple: suppress full SP.
**Atlas handling:** Pending inspection — likely usable with one bad entry suppressed.

### Issue 3: MSCSUG — bridge program SP semantics

**Affected program:** MSCSUG (B.S./M.S. Computer Science accelerated bridge)
**Issue:** SP blends bachelor's-level and master's-level content in a single term sequence spanning 10+ terms. The program is an accelerated pathway from bachelor's to master's — it is not a standard bachelor's or master's program in isolation.
**Detection:** Term span (1–10+), program name includes "UG" accelerated bridge designation.
**Atlas handling:** SP is structurally valid. Display with label: "Accelerated B.S./M.S. pathway — term sequence spans both degree levels." Do not suppress.
**Note:** MSCSUG is in LAB_EXCLUSIONS for the Compare tool for unrelated reasons (program naming).

### Issue 4: "aws [preposition]" — systematic cert extraction false positives

**Affected programs:** ~20 programs, ~45 false positive mentions
**Issue:** The cert extractor matched substrings of words containing "-aws" (laws, draws, flaws, etc.) as AWS certification references.
**Detection:** All false positives begin with lowercase "aws " (lowercase-a, w, s, space, then another lowercase word). All genuine AWS mentions begin with "AWS " (uppercase).
**Suppression rule:** `if mention.lower().startswith("aws ") and not mention.startswith("AWS ")` → suppress.
**Source-side vs extraction-side:** Extraction-side — the regex pattern was case-insensitive and matched substrings rather than requiring whole-word boundaries.
**WGU feedback candidate:** No — this is an extraction artifact, not a guide authoring issue.

### Issue 5: "no-prereq" boilerplate captured as prerequisites

**Affected programs:** Broad — appears across most program families
**Issue:** The string `"for this course and there is no specific technical knowledge needed"` appears 62 times as an extracted prerequisite mention. It is the terminal clause of WGU's standard no-prerequisite declaration.
**Detection:** Frequency analysis of `prerequisite_mentions` values — this single string is the most common entry in the corpus.
**Suppression rule:** Exact string match against no-prereq declaration list (defined in Section 2 above).
**Source-side vs extraction-side:** Extraction-side — the extractor matched the word "prerequisite" and captured the trailing sentence fragment without checking for negation context.
**WGU feedback candidate:** No.

### Issue 6: BSNU — missing guide metadata

**Affected program:** BSNU (B.S., Nursing)
**Issue:** `version`, `pub_date`, `page_count` are null or zero. Content intact.
**Detection:** Manifest row inspection.
**Source-side:** Older guide format with no footer pagination/version block.
**Atlas handling:** Surface AoS and SP content normally. Omit guide provenance badge (source badge shows "WGU Program Guide — version not available").

### Issue 7: MEDETID — partial capstone capture

**Affected program:** MEDETID (M.Ed., Education Technology and Instructional Design)
**Issue:** Capstone field captures only the first of three capstone courses.
**Detection:** Session 23 notes, confirmed in manifest validation.
**Source-side:** Multi-capstone structural format not handled by current parser.
**Atlas handling:** Display the captured capstone with `partial: true` flag. Do not imply this is the complete capstone picture. Suppress if displaying an incomplete list would mislead more than help.

### Issue 8: Praxis "exam," with comma — cert extraction artifact

**Affected programs:** BAESSESC, BAESSESP, ENDSESC, ENDSESP
**Issue:** Cert mention extracted as `"Praxis exam,"` with trailing comma rather than `"Praxis exam"`.
**Detection:** Frequency analysis of cert mentions.
**Suppression/normalization rule:** Strip trailing punctuation from all cert strings before whitelist match.
**WGU feedback candidate:** No.

---

## 5. Next-Session Execution Plan

### Execution order

**Phase 1 — Cert mapping (start here — highest confidence, fastest win)**

1. Write `scripts/program_guides/extract_cert_mapping.py`
   - Reads all `data/program_guides/parsed/*.json`
   - Extracts all `certification_prep_mentions` from all AoS courses
   - Applies whitelist normalization and punct-strip
   - Applies `^aws [a-z]` suppression pattern
   - Groups by (normalized_cert, course_title) → count of source programs
   - For each group, resolves course title to catalog code via bridge/merged guide data
   - Emits high-confidence (≥3 programs) to auto-accept table
   - Emits lower-confidence to review table
   - Outputs `data/program_guides/cert_course_mapping.json`

2. Validate against known ground truth:
   - CompTIA A+ → IT Applications, IT Foundations: should appear in 7 programs
   - AWS Certified → Cloud Foundations: should appear in 7 programs
   - CompTIA Network+ → Networks: should appear in 6 programs

3. Cross-reference with `public/data/program_enriched.json` to confirm course codes are in current catalog.

**Phase 2 — Prereq relationships (second — requires more cleaning but the data is there)**

1. Write `scripts/program_guides/extract_prereq_relationships.py`
   - Reads all `data/program_guides/parsed/*.json`
   - Extracts all `prerequisite_mentions` from all AoS courses
   - Applies no-prereq suppression filter first (exact strings + patterns)
   - Classifies remaining mentions by type (explicit-course, code-anchored, cumulative-sequence, inverted-capture, soft-preparedness)
   - For type `explicit-course`: fuzzy-match against catalog course title list
   - For type `code-anchored`: extract course code pattern, look up in catalog
   - For type `cumulative-sequence`: parse template, extract specific codes
   - For type `inverted-capture`: flag for review queue, attempt sentence parse
   - Emits high-confidence to auto-accept table
   - Emits review candidates to review table
   - Suppresses `soft-preparedness` (log, don't emit to output)
   - Outputs `data/program_guides/prereq_relationships.json`

2. Focus validation on BSCS, BSDA, BSACC chains first — highest density and quality. Verify each recovered prereq relationship against course page to confirm both courses are in the catalog and the relationship direction is correct.

**Phase 3 — SP family classification (third — deterministic, low ambiguity)**

1. Write `scripts/program_guides/classify_sp_families.py`
   - Reads all parsed JSONs
   - Emits per-program SP classification (Category A/B/C/D)
   - A/B is fully deterministic: check if any `term` value is non-null
   - D: check SP entry title length — flag any entry >150 characters as anomalous
   - C: scan `program_description` for track declaration language; extract declaration sentence
   - Cross-reference program codes for known family prefixes (BSCNE*, MACC*, MSRNN*)
   - Outputs `data/program_guides/sp_family_classification.json`
   - Outputs `data/program_guides/sp_families.json`

2. Validate family groupings:
   - BSSWE: should have 2 members (Java, C#), shared course count ~33
   - MAcc: should have 4 members, 5 shared foundation courses
   - BSCNE family: 4 members (base + AWS, Azure, Cisco)
   - BAELED family: 2 structural variants (licensure=null-term, non-licensure=populated)

**Phase 4 — Anomaly registry (last — no new analysis needed, just formalize)**

1. Write `data/program_guides/guide_anomaly_registry.json`
   - One entry per known anomaly/issue (from Section 4 above)
   - Fields: program_code, issue_type, description, detection_method, atlas_handling, wgu_feedback_candidate
   - This feeds the Atlas caveat/provenance layer and the partial-use rules in PHASE_D policy

### What to validate against catalog/runtime data

For every recovered cert mention, prereq relationship, and family classification:
- Confirm the course title resolves to an active or historically-present catalog code
- Use `public/data/program_enriched.json` for current active programs
- Use `public/data/courses.json` (or equivalent) for course code lookup
- Flag anything that resolves to a course code not in the current catalog — it may be a retired course that was a prereq in an older guide version

### What waits until after first-pass recovery

- Course-page cert badge display (wait for cert_course_mapping.json to be validated)
- Course-page prereq display (wait for prereq_relationships.json to be validated and review queue resolved)
- BSCNE family cert degree-page surface (wait for family classification so the per-degree cert context is clean)
- Praxis exam code → specific education program surface (wait for Education program AoS structure to be reviewed — the exam code is in a course context that needs to be understood before display)
- NCLEX treatment for nursing (separate investigation — not part of this pass)

### Scripts involved

| Script | Input | Output | Phase |
|---|---|---|---|
| `extract_cert_mapping.py` | `parsed/*.json` | `cert_course_mapping.json` | 1 |
| `extract_prereq_relationships.py` | `parsed/*.json` | `prereq_relationships.json` | 2 |
| `classify_sp_families.py` | `parsed/*.json` | `sp_family_classification.json`, `sp_families.json` | 3 |
| (inline) | above outputs | `guide_anomaly_registry.json` | 4 |

All four scripts read from already-parsed artifacts. No re-parsing. No guide PDFs needed.

---

## Summary: what this session will produce

| Artifact | Content | Confidence at completion |
|---|---|---|
| `cert_course_mapping.json` | ~12 clean cert→course relationships, with cross-program confidence counts | HIGH for top 6 rows |
| `prereq_relationships.json` | 50–100 prereq relationships, concentrated in CS/math/data/accounting | HIGH for clean extractions; MEDIUM for review queue |
| `sp_family_classification.json` | All 115 programs classified A/B/C/D with family codes | HIGH — fully deterministic |
| `sp_families.json` | ~6 named family definitions with member lists and declaration text | HIGH |
| `guide_anomaly_registry.json` | 8 known anomaly types with handling rules | Complete as currently known |

These five artifacts complete the guide enrichment inventory and unlock the degree-page build, cert-signal layer, and prereq display layer.
