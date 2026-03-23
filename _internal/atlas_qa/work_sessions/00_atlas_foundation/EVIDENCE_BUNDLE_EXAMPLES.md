# Evidence Bundle Examples

**Purpose:** Show concretely what the QA control layer constructs and passes to answer assembly for each major query class. These examples make the pipeline concrete enough for reviewers to react to, and for implementors to use as construction targets.

**Version:** 2026-03-23 — created for RFI v4 external review round

**Cross-references:**
- Pipeline design: `LOCAL_8B_RAG_SYSTEM_DESIGN.md` §5–§8
- Query class taxonomy: `LOCAL_8B_RAG_SYSTEM_DESIGN.md` §6
- Canonical object shapes: `CANONICAL_OBJECT_PROTOTYPE_PACK.md`

---

## Bundle structure (shared across all examples)

```
evidence_bundle:
  query_class: A | B | C | D | E
  user_query: <string>
  resolved_entity: <course_code | program_code | null>
  resolved_version: <YYYY_MM | "latest" | null>
  source_scope: <list of source families in scope>
  section_scope: <section type(s) in scope, or null>
  answer_contract: "templated" | "bounded_synthesis" | "abstain"
  evidence_objects: [ ... ]
  excluded_evidence: [ ... ]
  pre_generation_gate:
    sufficient: true | false
    reason: <string if false>
```

---

## Example 1 — Exact course lookup (Class A)

**User query:** "What is D426?"

**Pipeline:**
- Pre-router recognizes `D426` as an exact course code → Class A
- Entity resolved: D426 (canonical)
- Version: not applicable (course_card is not version-scoped)
- Source scope: CANON, CAT-TEXT (description default is cat)
- No guide retrieval needed for a basic "what is this course" query

```
evidence_bundle:
  query_class: A
  user_query: "What is D426?"
  resolved_entity: "D426"
  resolved_version: null
  source_scope: ["CANON", "CAT-TEXT"]
  section_scope: null
  answer_contract: "templated"
  evidence_objects:
    - object_type: course_card
      course_code: D426
      canonical_title: "Database Management Applications"
      canonical_cus: 3
      description_cat: "Database Management Applications introduces students to the concepts of database management systems..."
      description_display_source: "cat"
      anomaly_flags: []
      evidence_refs: [CAT-TEXT/trusted/2026_03, CANON/canonical_courses.json]
  excluded_evidence:
    - type: guide_section_card
      reason: "Guide enrichment not in source_scope for Class A course lookup; no competency question present"
  pre_generation_gate:
    sufficient: true
answer_contract_notes:
  - answer is templated: title, CU, description from cat, version disclosure not needed (course_card is not version-scoped)
  - model optional: may format the output; may not add facts not in evidence
  - citation required: evidence_refs listed in answer
```

---

## Example 2 — Exact program lookup (Class A)

**User query:** "How many CUs is BSCS?"

**Pipeline:**
- Pre-router recognizes `BSCS` as a program code → Class A
- Entity resolved: BSCS, version: latest → 2026_03
- Source scope: CAT (total_cus is a CAT field)
- No text generation needed; answer is a single structured fact

```
evidence_bundle:
  query_class: A
  user_query: "How many CUs is BSCS?"
  resolved_entity: "BSCS"
  resolved_version: "2026_03"
  source_scope: ["CAT"]
  section_scope: null
  answer_contract: "templated"
  evidence_objects:
    - object_type: program_version_card
      program_code: BSCS
      version: "2026_03"
      is_latest: true
      total_cus: 120
      version_conflict: false
      evidence_refs: [CAT/trusted/2026_03/program_index.json]
  excluded_evidence:
    - type: guide_section_card
      reason: "total_cus is a CAT field; source scope excludes GUIDE"
    - type: course_card (multiple)
      reason: "CU question resolved at program level; individual course cards not needed"
  pre_generation_gate:
    sufficient: true
answer_contract_notes:
  - answer: "BSCS (Bachelor of Science, Computer Science) requires 120 credit units as of the 2026-03 catalog."
  - fully templated — no model generation needed
  - version disclosure required because entity is version-scoped: "as of the 2026-03 catalog"
```

---

## Example 3 — Section-grounded NL question (Class B/C)

**User query:** "What is the capstone for BSCS?"

**Pipeline:**
- Pre-router recognizes `BSCS` as a program code; "capstone" detected → Class B/C
- Entity resolved: BSCS, version: latest → 2026_03
- Source scope: GUIDE (capstone is a guide-only field)
- CAT and CANON not retrieved for this field

```
evidence_bundle:
  query_class: B
  user_query: "What is the capstone for BSCS?"
  resolved_entity: "BSCS"
  resolved_version: "2026_03"
  source_scope: ["GUIDE"]
  section_scope: "capstone"
  answer_contract: "bounded_synthesis"
  evidence_objects:
    - object_type: guide_section_card
      program_code: BSCS
      guide_version: "2026_03"
      section_type: "capstone"
      is_complete: true
      content:
        capstone_course: "C856"
        capstone_title: "Cybersecurity Graduate Capstone"
        capstone_description: "Students demonstrate mastery of program competencies by completing a supervised capstone project..."
        capstone_credit_units: 4
      evidence_refs: [GUIDE/program_guides/parsed/BSCS_guide_2026_03.json]
  excluded_evidence:
    - type: program_version_card (CAT fields)
      reason: "capstone is GUIDE sole source; CAT evidence excluded by source_scope"
    - type: course_card (CAT-TEXT description)
      reason: "source_scope restricted to GUIDE for capstone block"
  pre_generation_gate:
    sufficient: true
answer_contract_notes:
  - bounded synthesis: model phrases the answer from the guide_section_card content
  - required disclosure: "As listed in the BSCS program guide (2026-03)."
  - model must not assert capstone status without naming the program (BSCS)
  - citation: GUIDE/BSCS_guide_2026_03.json
```

---

## Example 4 — Multi-variant course question (Class C)

**User query:** "What are the competencies for D358?"

**Scenario A — no program context in query:**

```
evidence_bundle:
  query_class: C
  user_query: "What are the competencies for D358?"
  resolved_entity: "D358"
  resolved_version: null
  resolved_program_context: null
  source_scope: ["ENRICH"]
  section_scope: "competencies"
  answer_contract: "bounded_synthesis"
  evidence_objects:
    - object_type: course_card (competency_variants excerpt)
      course_code: D358
      selected_variant:
        source_program_codes: ["BSHR"]
        competencies: [
          "Analyzes training needs using established assessment frameworks.",
          "Designs instructional content aligned to organizational competency models."
        ]
        selection_basis: "most_common_by_source_program_count"
      other_variant_count: 1
      multi_variant_disclosure: "This course appears in 2 programs (BSHR, MSHRM). Competencies shown are from the most common source program (BSHR). Competency wording may differ for MSHRM."
      evidence_refs: [ENRICH/program_guides/parsed/BSHR_guide_2025_09.json]
  excluded_evidence:
    - type: MSHRM competency variant
      reason: "no program context; most-common variant selected per policy; MSHRM variant stored but not surfaced as primary"
    - type: CAT-TEXT description
      reason: "source_scope is ENRICH only for competency questions"
  pre_generation_gate:
    sufficient: true
answer_contract_notes:
  - multi_variant_disclosure string MUST appear in answer, generated deterministically — not by model
  - model phrases the competency list from the selected variant
  - OPEN QUESTION: is surfacing the most-common variant defensible here, or should this be an abstain + ask-for-program-context case?
```

**Scenario B — program context provided ("in the MSHRM program"):**

```
evidence_bundle:
  query_class: C
  user_query: "What are the competencies for D358 in the MSHRM program?"
  resolved_entity: "D358"
  resolved_version: null
  resolved_program_context: "MSHRM"
  source_scope: ["ENRICH"]
  section_scope: "competencies"
  answer_contract: "bounded_synthesis"
  evidence_objects:
    - object_type: course_card (competency_variants excerpt)
      course_code: D358
      selected_variant:
        source_program_codes: ["MSHRM"]
        competencies: [
          "Evaluates talent development strategy against organizational objectives.",
          "Applies adult learning theory to design of executive development programs."
        ]
        selection_basis: "program_context_match"
      multi_variant_disclosure: null
      evidence_refs: [ENRICH/program_guides/parsed/MSHRM_guide_2026_01.json]
  pre_generation_gate:
    sufficient: true
answer_contract_notes:
  - no disclosure needed: program context provided, exact match found
  - citation: ENRICH/MSHRM_guide_2026_01.json, scoped to MSHRM
```

---

## Example 5 — Version-conflicted program question (Class B)

**User query:** "What programs are required for MSHRM?"

```
evidence_bundle:
  query_class: B
  user_query: "What courses are required for MSHRM?"
  resolved_entity: "MSHRM"
  resolved_version: "2026_03"
  source_scope: ["CAT", "GUIDE"]
  section_scope: "course_roster + standard_path"
  answer_contract: "bounded_synthesis"
  version_conflict_flag: true
  evidence_objects:
    - object_type: program_version_card
      program_code: MSHRM
      version: "2026_03"
      is_latest: true
      total_cus: 36
      version_conflict: true
      version_conflict_detail:
        catalog_version: "2026_03"
        guide_version: "2026_11"
        gap_months: 8
        body_text_status: "identical_after_prefix_strip"
        disclosure_text: "Program data is drawn from the 2026-03 catalog and the 2026-11 program guide. No content differences were found between sources at this time, but a freshness gap of 8 months exists."
      evidence_refs: [CAT/trusted/2026_03/program_index.json]
    - object_type: guide_section_card
      program_code: MSHRM
      guide_version: "2026_11"
      section_type: "standard_path"
      rows: [ ... 12 course rows ... ]
      evidence_refs: [GUIDE/program_guides/parsed/MSHRM_guide_2026_11.json]
  excluded_evidence:
    - type: guide_section_card (other programs)
      reason: "entity scope locked to MSHRM"
  pre_generation_gate:
    sufficient: true
answer_contract_notes:
  - version_conflict_detail.disclosure_text MUST appear in answer — pre-composed, not model-generated
  - model assembles course list from standard_path section card
  - both version tokens must be cited: catalog 2026-03, guide 2026-11
  - OPEN QUESTION: should disclosure appear for all MSHRM answers, or only version-sensitive ones?
```

---

## Example 6 — Abstain / ambiguity case (Class E / disambiguation needed)

**User query:** "Tell me about the capstone for the MBA."

**Pipeline:**
- Pre-router does not find an exact program code match for "MBA"
- Entity resolution: multiple candidates — MBAITM, MBAHCM (at minimum); possibly others
- Ambiguity: entity not uniquely resolved
- Pre-retrieval disambiguation required — do not proceed to retrieval

```
evidence_bundle:
  query_class: E (disambiguation required)
  user_query: "Tell me about the capstone for the MBA."
  resolved_entity: null
  resolved_version: null
  disambiguation_candidates:
    - program_code: "MBAITM"
      degree_title: "Master of Business Administration — IT Management"
      match_basis: "title keyword 'MBA'"
    - program_code: "MBAHCM"
      degree_title: "Master of Business Administration — Healthcare Management"
      match_basis: "title keyword 'MBA'"
  answer_contract: "abstain"
  evidence_objects: []
  excluded_evidence:
    - reason: "entity not resolved; retrieval not initiated"
  pre_generation_gate:
    sufficient: false
    reason: "Multiple program entities match 'MBA'; entity must be resolved before retrieval to prevent entity-collision + version-ambiguity cascade."
answer_contract_notes:
  - output: structured disambiguation response, not a QA answer
  - response presents candidates deterministically: "Multiple programs match 'MBA'. Please specify: MBAITM (IT Management) or MBAHCM (Healthcare Management)."
  - model is not involved in this response; it is fully deterministic
  - this is NOT an error — disambiguation before retrieval is the correct behavior
  - OPEN QUESTION: should disambiguation candidates be ranked by recency or by program enrollment size? (Neither is currently in the canonical object shape.)
```

---

## Summary: answer contract by example

| Example | Query class | Answer contract | Model role |
|---|---|---|---|
| 1 — exact course lookup | A | templated | optional formatting |
| 2 — exact program CU | A | templated | none needed |
| 3 — capstone section | B | bounded synthesis | phrase 1 evidence object |
| 4A — competencies, no context | C | bounded synthesis + disclosure | phrase variants; disclosure is deterministic |
| 4B — competencies, context | C | bounded synthesis | phrase 1 variant |
| 5 — version-conflicted program | B | bounded synthesis + disclosure | phrase course list; disclosure is deterministic |
| 6 — ambiguous entity | E | abstain | none |

---

## Open questions this pack surfaces for reviewers

1. **Example 4A (multi-variant, no context)**: Is the most-common-variant + disclosure contract shown here the right v1 behavior, or should this be an abstain + ask-for-context case? (This is the core §5.4 Q1 question.)

2. **Example 5 (version-conflicted program)**: The `disclosure_text` is pre-composed and appears in every answer about MSHRM. Is this the right shape? Reviewers may have a view on whether the disclosure should always appear or only when the version gap is material to the answer.

3. **Example 6 (disambiguation)**: The bundle shows `evidence_objects: []` because retrieval is not initiated until entity is resolved. Is there a case where partial retrieval (top-1 candidate) is safer than full abstention?

4. **Evidence bundle size**: Examples 3–5 show 1–2 evidence objects. The design target is 2–5 for single-entity, 4–8 for compare. Does this pack suggest the targets are right, or should the upper bound be tighter for the 8B model?
