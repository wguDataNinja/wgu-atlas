# Atlas QA — Gold Question Set v1

**Created:** 2026-03-23
**Status:** Active — first-pass eval artifact
**Grounded in:** `LOCAL_8B_RAG_SYSTEM_DESIGN.md`, `BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md`, Session 05 typed outputs
**Total questions:** 100
**Intended use:** Launch-gate evaluation, regression testing, abstention calibration

---

## 1. Scope and Purpose

This question set is the primary evaluation corpus for Atlas QA v1. It covers the full in-scope product surface: exact identifier lookup, single-entity factual lookup, section-grounded natural language queries, explicit version comparison, disambiguation, out-of-scope abstention, and known corpus anomalies.

**What this is:**
- A curated, human-readable set of 100 representative questions, each with a declared expected behavior, entity type, source scope, and version-sensitivity flag.
- The primary input to the Session 06 eval harness. Questions here drive fixture creation and gate thresholds.
- A stable reference point for regression runs as the system evolves.

**What this is not:**
- A generated or Reddit-scraped question set. Every question is grounded in the actual Atlas QA answerable universe.
- An exhaustive test harness. The harness scaffolding, running infrastructure, and launch-gate thresholds belong to Session 06.
- A product FAQ or user-facing content.

**Corpus bounds:**
- Catalog: WGU Catalog 2026-03 (current edition). Previous edition referenced: 2025-06.
- Program guides: 115 parsed guides. Guide versions referenced: 202503, 202412, 202409, 202507, 202311.
- Canonical course index: 1,594 course codes.

---

## 2. Coverage Plan

### 2.1 Composition by query class

| Class | Description | Count |
|---|---|---|
| **A** | Exact identifier lookup — deterministic, code-based | 15 |
| **B** | Single-entity factual — one entity, no section-scoping required | 20 |
| **C** | Section-grounded NL — requires guide section card (competencies, AoS, capstone, standard path, PLOs) | 18 |
| **D** | Explicit version comparison — two catalog editions or two guide versions of the same entity | 12 |
| **E** | Ambiguity / disambiguation — natural-language entity references that may match multiple entities | 10 |
| **F** | Abstain / out-of-scope — advising, opinion, external facts, structurally unsupported | 15 |
| **G** | Known anomaly / conflict — C179, D554, MSHRM, MACC family, multi-variant without program context | 10 |
| **Total** | | **100** |

### 2.2 Coverage of known failure modes

| Failure mode | Questions covering it |
|---|---|
| Wrong-version contamination | D questions, G-094, G-095, G-098 |
| Version-conflict program disclosure | G-093, G-094, G-095, G-097, G-098, G-100 |
| Guide anomaly carry-through (C179) | G-091, G-096 |
| Guide anomaly abstention (D554 guide block) | G-092, G-099 |
| Abstention on out-of-scope / advising | All F questions |
| Entity ambiguity (no code) | All E questions |
| Section scope enforcement (guide required, not present) | C-041, C-042, C-053 |
| Multi-variant without program context | B-035, C-046, C-047 |
| Negative claim completeness (absence assertion) | B-028, F-080 |
| Compare mode rejection in single-entity path | D questions (gate boundary) |
| PLO source (catalog only, guides have none) | C-044, C-049 |
| Guide standard path qualification ("as listed in guide") | C-038, C-045, C-051 |

### 2.3 Entity coverage

| Entity | ID | Used in |
|---|---|---|
| C715 | Business of IT — Applications | A-002, B-021, C-036 |
| D426 | Data Management — Foundations | A-001, B-016, B-028, D-055, D-060 |
| C179 | Advanced Networking Concepts (short-text anomaly) | A-006, B-022, C-050, G-091, G-096 |
| D554 | Advanced Financial Accounting I (guide misrouted) | A-008, B-026, G-092, G-099 |
| C949 | Data Structures and Algorithms II | C-041 |
| C845 | Cybersecurity Capstone | A-013, B-035 |
| D432, D435 | MSHRM cluster courses | A-011, B-033, B-034 |
| D358, D354 | BSHR cluster courses (review-flagged) | B-031 |
| C947 | BSPRN nursing course | C-051 |
| BSCS | B.S. Computer Science | A-003, B-017, C-038, C-043, C-048, D-054, D-062 |
| BSACC | B.S. Accounting | A-003 (ref), B-020, C-049, D-059, D-065 |
| BSDA | B.S. Data Analytics | A-007, B-019, B-023, C-037, C-040, C-042, C-045, D-056, D-061 |
| BSHR | B.S. Human Resource Management | B-031, C-047 |
| BSPRN | B.S. Nursing | B-031 (ref), C-051 |
| MSHRM | M.S. Human Resource Management | A-004, B-025, C-052, D-063, G-093, G-094 |
| MACCA, MACCF, MACCM, MACCT | MACC family (version conflict) | A-009, A-015, B-029, D-058, G-095, G-097, G-098, G-100 |

---

## 3. Gold Question Table

Column key:
- **ID** — stable identifier
- **Query** — question text
- **Class** — A/B/C/D/E/F/G
- **Behavior** — `answer` / `abstain` / `clarify`
- **Entity type** — `course` / `program` / `section` / `compare` / `none`
- **Source scope** — `catalog` / `guide` / `canon` / `both` / `none`
- **V-sens** — version-sensitive (`Y`/`N`)
- **Notes**

---

### Class A — Exact Identifier Lookup

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| A-001 | What is D426? | A | answer | course | catalog | N | Deterministic path; catalog description + identity fields |
| A-002 | How many CUs is C715? | A | answer | course | canon | N | CU from CANON; guide CU not authoritative |
| A-003 | What is BSACC? | A | answer | program | catalog | N | Degree title + college from catalog |
| A-004 | What is MSHRM? | A | answer | program | catalog | Y | Must disclose version conflict: cat=202311, guide=202507 |
| A-005 | How many total CUs does BSCS require? | A | answer | program | catalog | N | Total CU from catalog; guide SP sum not authoritative |
| A-006 | What is C179? | A | answer | course | catalog | N | Short catalog text (293 chars); anomaly must be disclosed; do not default to guide |
| A-007 | What college is BSDA in? | A | answer | program | catalog | N | Identity field from catalog |
| A-008 | What is D554? | A | answer | course | catalog | N | Guide description is misrouted; answer from catalog only |
| A-009 | What is MACCA? | A | answer | program | catalog | Y | Degree title from catalog; version conflict disclosure required (cat=202412, guide=202409) |
| A-010 | How many credit units does D335 carry? | A | answer | course | canon | N | CU identity lookup; deterministic |
| A-011 | What degree is MSHRM? | A | answer | program | catalog | Y | Master's in HR Management; version conflict note required |
| A-012 | What is the current catalog version for BSCS? | A | answer | program | catalog | Y | Must return WGU Catalog 2026-03 |
| A-013 | What is C845? | A | answer | course | catalog | N | Cybersecurity Capstone; deterministic identity lookup |
| A-014 | Is D426 a course or a program? | A | answer | course | canon | N | Identity type lookup; purely deterministic |
| A-015 | What is MACCM? | A | answer | program | catalog | Y | MACC variant; version conflict disclosure required |

---

### Class B — Single-Entity Factual Lookup

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| B-016 | What is the catalog description for D426? | B | answer | course | catalog | Y | CAT-TEXT default; version citation required |
| B-017 | What courses are required in the BSCS program? | B | answer | program | guide | Y | GUIDE standard_path; qualify as "as listed in the program guide" |
| B-018 | What is the total CU requirement for BSACC? | B | answer | program | catalog | N | Total CU from catalog; straightforward |
| B-019 | What program learning outcomes does BSDA list? | B | answer | program | catalog | Y | PLOs from CAT-TEXT only; guides do not contain PLOs |
| B-020 | What is the capstone course for BSACC? | B | answer | section | guide | Y | Guide-only field; program-scoped |
| B-021 | What programs include C715? | B | answer | course | guide | N | Program membership from guide; list of source programs |
| B-022 | What is the catalog description for C179? | B | answer | course | catalog | Y | Must disclose cat_short_text anomaly (293 chars); cite WGU Catalog 2026-03 |
| B-023 | Does BSDA have an Areas of Study section? | B | answer | program | guide | Y | Section presence check; guide-only field |
| B-024 | What is the guide version for BSCS? | B | answer | program | guide | Y | Guide version token; cite source |
| B-025 | What college houses the MSHRM program? | B | answer | program | catalog | Y | Identity from catalog; version conflict note required |
| B-026 | What is the description for D554? | B | answer | course | catalog | Y | Catalog text only; must not use guide (D554 guide anomaly); anomaly disclosure required |
| B-027 | What is the total CU for BSCS? | B | answer | program | catalog | N | Total CU from catalog |
| B-028 | What programs include D426? | B | answer | course | guide | N | Course→program membership; do not assert completeness without confirmation |
| B-029 | What is the degree title for MACCA? | B | answer | program | catalog | Y | Catalog identity; version conflict disclosure required |
| B-030 | What is the canonical title of C715? | B | answer | course | canon | N | CANON title; deterministic |
| B-031 | Does BSPRN have a standard path section? | B | answer | program | guide | Y | Section presence from guide; boolean + guide version |
| B-032 | What is the guide publication date for BSDA? | B | answer | program | guide | Y | Guide pub date field |
| B-033 | How many credit units does D432 carry? | B | answer | course | canon | N | MSHRM-cluster course; CU from CANON |
| B-034 | What is the catalog description for D435? | B | answer | course | catalog | Y | MSHRM-cluster course; standard catalog lookup |
| B-035 | What programs use C845 as a capstone course? | B | answer | section | guide | Y | Capstone is program-scoped; must name programs, not assert universally |

---

### Class C — Section-Grounded NL Lookup

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| C-036 | What competencies are listed for C715? | C | answer | section | guide | Y | GUIDE sole source for competencies; most-common variant if no program context; disclose variant count |
| C-037 | What does the Areas of Study section say for BSDA? | C | answer | section | guide | Y | GUIDE AoS; program-scoped; cite guide version |
| C-038 | What courses are in the standard path for BSCS? | C | answer | section | guide | Y | GUIDE standard_path; qualify "as listed in the BSCS program guide" |
| C-039 | What competencies does D426 develop? | C | answer | section | guide | Y | Competency bullets from GUIDE; program-context variant selection if context provided |
| C-040 | What is the capstone requirement for BSDA? | C | answer | section | guide | Y | GUIDE capstone section; program-scoped |
| C-041 | What competencies are listed for C949? | C | answer | section | guide | Y | Competencies from GUIDE; if multi-variant, disclose |
| C-042 | What are the Areas of Study tracks in BSDA? | C | answer | section | guide | Y | GUIDE AoS structure; list named tracks |
| C-043 | What does the program guide say about capstone requirements for BSCS? | C | answer | section | guide | Y | GUIDE capstone section; cite guide version |
| C-044 | What learning outcomes are listed for BSCS? | C | answer | section | catalog | Y | PLOs from CAT-TEXT only; cite WGU Catalog 2026-03; guides do not contain PLOs |
| C-045 | What is listed in the standard path for BSDA? | C | answer | section | guide | Y | GUIDE standard_path; qualify as one path through elective structure |
| C-046 | What competencies does the BSCS program list for C949? | C | answer | section | guide | Y | Program context supplied → select BSCS-specific variant; cite guide |
| C-047 | What does the BSHR program guide say about Areas of Study? | C | answer | section | guide | Y | GUIDE AoS; BSHR-specific; cite guide version |
| C-048 | What courses appear in the capstone section for BSCS? | C | answer | section | guide | Y | GUIDE capstone; cite guide + version |
| C-049 | What are the program learning outcomes for BSACC? | C | answer | section | catalog | Y | PLOs from CAT-TEXT; guide has none for this block |
| C-050 | What competencies are listed for C179? | C | answer | section | guide | Y | Guide competencies are a separate block from catalog description; short-text anomaly does not block competency lookup; disclose anomaly context |
| C-051 | What does the standard path section say for BSPRN? | C | answer | section | guide | Y | GUIDE standard_path; BSPRN; cite guide + version; qualify as guide path |
| C-052 | What are the Areas of Study options in MSHRM? | C | answer | section | guide | Y | GUIDE AoS; MSHRM; version conflict disclosure required alongside answer |
| C-053 | What competencies does D554 list? | C | answer | section | guide | Y | Competency bullets are a separate guide field from the description; guide description anomaly (D554) does not block competency lookup — but must note D554 guide description anomaly in context if relevant |

---

### Class D — Explicit Version Comparison

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| D-054 | What changed in BSCS between the 2025-06 and 2026-03 catalog editions? | D | answer | compare | both | Y | version_diff_card if available; added/removed/changed courses; cite both editions |
| D-055 | What changed in D426 between the 2025-06 and 2026-03 catalog editions? | D | answer | compare | catalog | Y | Course-level diff; description change detection; cite both version tokens |
| D-056 | What was added to BSDA in the 2026-03 edition compared to 2025-06? | D | answer | compare | both | Y | Added courses; deterministic diff; cite both editions |
| D-057 | What courses were removed from BSCS between guide versions 202409 and 202503? | D | answer | compare | guide | Y | Guide-level diff; removed rows in standard_path; cite both guide versions |
| D-058 | What changed in MACCA between catalog versions 202409 and 202412? | D | answer | compare | catalog | Y | MACC family; catalog 3 months newer than guide; version conflict context; cite both |
| D-059 | What is the difference between the 2025-06 and 2026-03 course lists for BSACC? | D | answer | compare | both | Y | Course roster diff across editions; deterministic |
| D-060 | Did D426 change between the 2025-06 and 2026-03 catalog editions? | D | answer | compare | catalog | Y | May be no change; must state explicitly if unchanged; cite both editions |
| D-061 | What was different about BSDA in the 2025-06 catalog vs 2026-03? | D | answer | compare | both | Y | Full diff; not just courses; cite both editions |
| D-062 | What courses were added to BSCS in the 2026-03 catalog edition? | D | answer | compare | both | Y | Added courses only; cite 2025-06 as baseline and 2026-03 as current |
| D-063 | How has MSHRM's program guide changed from version 202311 to 202507? | D | answer | compare | guide | Y | Guide-level diff; body text is currently identical after prefix strip; must state accurately if no content change; do not assert "no change" without verification; cite both guide versions |
| D-064 | What changed for BSDA between guide versions 202409 and 202503? | D | answer | compare | guide | Y | Guide diff for BSDA; cite both versions |
| D-065 | Compare the 2025-06 and 2026-03 versions of BSACC for me. | D | answer | compare | both | Y | Full compare; cite both editions; version_diff_card preferred over freeform narrative |

---

### Class E — Ambiguity / Disambiguation

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| E-066 | What courses are in the MBA program? | E | clarify | program | none | N | "MBA" may match multiple program codes; system must not arbitrarily select one; request clarification with candidate list |
| E-067 | What is the capstone for the accounting master's? | E | clarify | section | none | N | MACCA, MACCF, MACCM, MACCT — four candidates; disambiguation required before capstone lookup |
| E-068 | What is the degree in data analytics? | E | clarify | program | none | N | Multiple data analytics programs may exist (BSDA and others); must not collapse to first match |
| E-069 | Tell me about the nursing program. | E | clarify | program | none | N | Multiple nursing programs (BSPRN + graduate); must request clarification |
| E-070 | What program covers cybersecurity? | E | clarify | program | none | N | Multiple security programs; must surface candidates, not arbitrarily select |
| E-071 | What is the business analytics capstone? | E | clarify | section | none | N | Ambiguous program reference; multiple candidates possible |
| E-072 | What courses are in the human resources master's program? | E | clarify | program | none | Y | MSHRM is likely the match but must confirm code before retrieving; version conflict note if confirmed |
| E-073 | What version is the BSCS guide on? | E | answer | program | guide | Y | Unambiguous once entity resolved; answer with guide version token |
| E-074 | What are the Areas of Study in the data science program? | E | clarify | section | none | N | "Data science program" is ambiguous; must clarify before section lookup |
| E-075 | What competencies does the accounting program teach? | E | clarify | section | none | N | Multiple accounting programs (BSACC, MACCA, MACCF, MACCM, MACCT); disambiguation required |

---

### Class F — Abstain / Out-of-Scope

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| F-076 | Which WGU class is the easiest? | F | abstain | none | none | N | Opinion / advising; out_of_scope |
| F-077 | Should I take C715 before D426? | F | abstain | none | none | N | Personal advising; out_of_scope |
| F-078 | Will WGU accept my transfer credits for D426? | F | abstain | none | none | N | Admissions / policy question; out_of_scope |
| F-079 | What should I study to pass D426? | F | abstain | none | none | N | Study advising; out_of_scope |
| F-080 | Which path is best for me given my background? | F | abstain | none | none | N | Personalized recommendation; out_of_scope; no negative-claim completeness either |
| F-081 | Can I test out of C715? | F | abstain | none | none | N | Competency testing / prior learning policy; out_of_scope |
| F-082 | How hard is the BSCS program? | F | abstain | none | none | N | Subjective difficulty assessment; out_of_scope |
| F-083 | What is WGU's reputation compared to traditional universities? | F | abstain | none | none | N | External opinion / comparison; out_of_scope |
| F-084 | What are the average salaries for BSCS graduates? | F | abstain | none | none | N | Outcomes data not in corpus; out_of_scope |
| F-085 | How long does BSCS typically take to complete? | F | abstain | none | none | N | Completion time / pacing; out_of_scope for v1 |
| F-086 | What is the passing rate for the D426 objective assessment? | F | abstain | none | none | N | Assessment pass rate not in corpus; out_of_scope |
| F-087 | Should I choose BSACC or BSDA? | F | abstain | none | none | N | Personal choice recommendation; out_of_scope |
| F-088 | Is BSCS accredited? | F | abstain | none | none | N | Accreditation data not in QA-indexed content for v1; insufficient_evidence or out_of_scope |
| F-089 | What are WGU's tuition rates for BSCS? | F | abstain | none | none | N | Tuition data not in corpus; out_of_scope |
| F-090 | What WGU program should I enroll in? | F | abstain | none | none | N | Open-ended enrollment recommendation; out_of_scope |

---

### Class G — Known Anomaly / Conflict

| ID | Query | Class | Behavior | Entity type | Source scope | V-sens | Notes |
|---|---|---|---|---|---|---|---|
| G-091 | What is the catalog description for C179? | G | answer | course | catalog | Y | Must answer from catalog; must disclose cat_short_text anomaly (293-char description); cite WGU Catalog 2026-03; offer that guide text is available but not the catalog-default |
| G-092 | What does the program guide say about D554? | G | abstain | course | catalog | Y | Guide description for D554 is misrouted (D560 text); system must not serve guide description; abstain on guide description with data anomaly note; catalog description is unaffected and can be offered |
| G-093 | What is the guide version for MSHRM? | G | answer | program | both | Y | Guide version is 202507; catalog version is 202311; both tokens must be cited; do not assert one is "current" without qualification |
| G-094 | Is the MSHRM program guide current? | G | answer | program | both | Y | Version conflict: guide is 8 months newer than catalog extract; must disclose both version tokens; body text is currently identical after prefix strip; do not assert currency without citing both |
| G-095 | What is the description of MACCA? | G | answer | program | catalog | Y | Catalog is 3 months newer than guide (cat=202412, guide=202409); use CAT-TEXT; disclose both version tokens in the answer |
| G-096 | What competencies are listed for C179? | G | answer | section | guide | Y | Competency bullets are a separate block from catalog description; short-text anomaly does not block competency lookup; answer from GUIDE; note anomaly in context; cite guide program + version |
| G-097 | What guide version does MACCF use? | G | answer | program | both | Y | Guide version: 202409; catalog version: 202412; cite both; do not blend without disclosure |
| G-098 | What catalog version is MACCT on? | G | answer | program | catalog | Y | Catalog version: 202412; guide version: 202409; catalog is more current; cite both |
| G-099 | What does D554's program guide description say? | G | abstain | course | catalog | Y | D554 guide description contains text from D560 (data anomaly); system must abstain and explain the anomaly; catalog description may be offered as the available alternative |
| G-100 | Are MACCA and MACCF on the same guide version? | G | answer | compare | guide | Y | Both use guide version 202409; answer is "yes, both use guide version 202409 as of the current corpus"; cite source; note catalog version (202412) is different from guide version |

---

## 4. Notes on Known Anomaly and Conflict Cases

### 4.1 C179 — Advanced Networking Concepts (cat_short_text)

- Catalog description is 293 characters — the shortest in the CNE cluster and unusually brief for a networking course.
- The guide adds routing/switching/automation specifics not present in the catalog text.
- **Expected QA behavior for description questions (A-006, B-022, G-091):** Serve catalog text with explicit disclosure of the short-text anomaly. Do not default to the guide description without user request.
- **Expected QA behavior for competency questions (C-050, G-096):** Competency bullets are a distinct guide block unaffected by the catalog short-text flag. Answer from GUIDE; note the C179 anomaly context.
- **Post-check implication:** The `cat_short_text` anomaly disclosure must survive to `QAResponse.evidence_bundle.anomaly_disclosures`.

### 4.2 D554 — Advanced Financial Accounting I (guide_misrouted_text)

- Guide description for D554 contains text from D560 (Internal Auditing I) — a suspected pipeline extraction error.
- **Expected QA behavior for description questions (A-008, B-026, G-092):** Answer from catalog only; do not cite or quote guide description. Disclose anomaly with message: "Guide description for this course contains a data anomaly and cannot be used."
- **Expected QA behavior for guide-description explicit questions (G-099):** Abstain with data anomaly explanation. Offer catalog description as available alternative.
- **Expected QA behavior for competency questions (C-053):** Competencies are a distinct guide field. If competency data for D554 exists in the guide separately from the description block, it may be used. If the competency block is also contaminated (indeterminate), abstain on competencies with anomaly note. This case should be tested against actual corpus data.
- **Post-check implication:** `guide_misrouted_text` disclosure must survive to `QAResponse`.

### 4.3 MSHRM — Version Freshness Gap

- Guide version 202507 is 8 months newer than catalog version 202311.
- Body text is currently identical after stripping the guide metadata prefix.
- **Expected QA behavior (A-004, A-011, B-025, G-093, G-094, D-063):** Always cite both version tokens when answering about MSHRM. Do not assert the catalog is current without qualification. Do not assert the guide is current either — the gap must be disclosed explicitly.
- **Version conflict disclosure format:** "Source: WGU Catalog 202311 (catalog) / MSHRM Program Guide 202507 (guide). Note: an 8-month freshness gap exists between these sources. Body text is currently identical after normalizing the guide metadata prefix, but this should be confirmed for any content-sensitive queries."

### 4.4 MACC Family — Catalog Newer Than Guide

- Programs: MACCA, MACCF, MACCM, MACCT
- Catalog version: 202412 (3 months newer); guide version: 202409.
- **Expected QA behavior (A-009, A-015, B-029, D-058, G-095, G-097, G-098, G-100):** Use CAT-TEXT as description default. Cite both version tokens. Do not blend without disclosure.
- **Compare question D-058:** A compare query for MACCA between catalog versions 202409 and 202412 requires two-version evidence bundle with version_diff_card if available; otherwise strict two-version retrieval.

### 4.5 Multi-Variant Courses Without Program Context

- 185 courses have 2–6 competency variants keyed to source programs.
- 74 courses have 2–4 guide description variants.
- **Expected QA behavior (C-036, C-039, C-041, C-046, B-035):** When program context is absent, use the most-common variant by source program count. Disclose: "This course appears in multiple programs; [competencies / description] may vary slightly by program."
- **Questions B-035 and C-046** exercise this: B-035 asks about capstone programs for C845 (requires listing multiple programs without collapsing); C-046 provides BSCS context explicitly (tests program-scoped variant selection).

---

## 5. Suggested Launch-Gate Subset

The following 20 questions form the minimal recommended first launch gate. They were selected to cover all major failure modes, all query classes, and both anomaly cases, while remaining tractable for a first eval run.

| ID | Query | Class | Why included |
|---|---|---|---|
| A-001 | What is D426? | A | Baseline exact lookup; should be high-confidence |
| A-002 | How many CUs is C715? | A | CANON CU lookup; deterministic |
| A-005 | How many total CUs does BSCS require? | A | Program-level CU; catalog authority test |
| B-016 | What is the catalog description for D426? | B | Single-entity factual; version citation required |
| B-019 | What program learning outcomes does BSDA list? | B | PLO from catalog only; tests source-scope enforcement |
| B-020 | What is the capstone course for BSACC? | B | Guide-only section block; tests guide section retrieval |
| C-038 | What courses are in the standard path for BSCS? | C | Standard path qualification required; tests guide source scope |
| C-041 | What competencies are listed for C949? | C | Guide competencies; multi-variant disclosure |
| C-044 | What learning outcomes are listed for BSCS? | C | PLO from catalog; tests that guide is not used for PLOs |
| D-054 | What changed in BSCS between the 2025-06 and 2026-03 catalog editions? | D | Baseline compare; version_diff_card path |
| D-060 | Did D426 change between the 2025-06 and 2026-03 catalog editions? | D | No-change case; tests accurate "no change" handling |
| E-066 | What courses are in the MBA program? | E | Entity disambiguation; must not arbitrarily select one program |
| E-067 | What is the capstone for the accounting master's? | E | Multi-entity disambiguation (MACC family) |
| F-076 | Which WGU class is the easiest? | F | Hard out_of_scope case; must not attempt answer |
| F-079 | What should I study to pass D426? | F | Advising abstention; must not provide study plan |
| F-087 | Should I choose BSACC or BSDA? | F | Comparative advising; out_of_scope |
| G-091 | What is the catalog description for C179? | G | C179 anomaly disclosure; answer must include anomaly note |
| G-092 | What does the program guide say about D554? | G | D554 guide abstention; guide description blocked |
| G-094 | Is the MSHRM program guide current? | G | Version freshness disclosure; must cite both tokens |
| G-095 | What is the description of MACCA? | G | MACC version conflict disclosure; catalog default + both version tokens |

**Launch-gate pass criteria (to be set in Session 06):**
- Class A: ≥ 95% correct (exact identity fields, correct CU, no wrong-version contamination)
- Class B/C: ≥ 85% correct with citation and version disclosure present
- Class D: ≥ 80% correct diff accuracy; zero cases of cross-version blending without disclosure
- Class E: ≥ 90% correct disambiguation behavior (clarify or abstain; never arbitrarily pick one entity)
- Class F: ≥ 98% correct abstention (near-zero tolerance for answering out-of-scope questions)
- Class G: 100% anomaly disclosure present on answered questions; 100% guide abstention for blocked guide cases

---

## 6. Maintenance Notes

- This question set is first-pass. It should be reviewed and extended after the first full eval run in Session 06.
- Questions marked `clarify` may need to be split into two sub-questions once the clarification UX is designed: one testing the disambiguation response, one testing the answer after disambiguation.
- The version strings used here (2025-06, 2026-03 for catalog; 202409, 202412, 202503, 202507, 202311 for guides) should be verified against the actual corpus manifest before running automated evals.
- Questions D-054 through D-065 depend on `version_diff_card` availability. If diff cards are not pre-computed for a given entity/version pair, the expected behavior falls back to two-version bundle generation. This fallback behavior should be explicitly tested.
- For Class G questions, post-check must verify that anomaly disclosures (`cat_short_text`, `guide_misrouted_text`, `version_conflict`) survive to the final `QAResponse`. A passing post-check with no anomaly disclosure in the response is a failure for these questions.
