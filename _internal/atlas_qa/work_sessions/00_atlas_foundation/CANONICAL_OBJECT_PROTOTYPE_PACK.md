# Canonical Object Prototype Pack

**Purpose:** Concrete field-level prototypes for the four first-class QA canonical objects. These are representative examples, not generated from live data. Field values are plausible given the known corpus shape. Use these to react to actual object designs rather than abstract descriptions.

**Version:** 2026-03-23 — created for RFI v4 external review round

**Cross-references:**
- Object type definitions: `LOCAL_8B_RAG_SYSTEM_DESIGN.md` §7
- Source-authority field definitions: `POLICY_IMPLEMENTATION_PLAN.md` §Stage 5
- Block authority policy: `BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md`

---

## Object type: `course_card`

A course_card is a synthetic view of a canonical course. One card per course code. Not version-specific (courses appear across versions; version membership is recorded inside the card). Source-authority fields are set deterministically from the policy artifact.

### Source-authority fields (all course_cards)

| Field | Type | What it does |
|---|---|---|
| `description_display_source` | `"cat" \| "guide_only" \| "none"` | Controls which description the QA layer uses as default answer source |
| `description_cat_present` | bool | Whether catalog description exists |
| `description_cat_char_length` | int | Used to detect suspiciously short catalog text |
| `description_guide_alternate_count` | int | Number of guide description variants stored |
| `description_multi_variant` | bool | True when more than 1 guide description variant |
| `anomaly_flags` | list[str] | Hard anomaly codes; controls QA behavior at retrieval time |
| `description_review_flag` | bool | Human review pending; does not change default behavior |

---

### Prototype 1 — Normal course (D426: Database Management Applications)

```json
{
  "object_type": "course_card",
  "course_code": "D426",
  "canonical_title": "Database Management Applications",
  "canonical_cus": 3,
  "title_variants": [],
  "is_active": true,
  "instances_by_version": [
    {"catalog_version": "2025_06", "line_span": "p.182–184"},
    {"catalog_version": "2026_03", "line_span": "p.184–186"}
  ],
  "program_codes": ["BSCS", "BSSWE", "BSCSIA", "BSITM", "BSDA"],
  "description_cat": "Database Management Applications introduces students to the concepts of database management systems...",
  "description_display_source": "cat",
  "description_cat_present": true,
  "description_cat_char_length": 412,
  "description_guide_alternate_count": 0,
  "description_multi_variant": false,
  "anomaly_flags": [],
  "description_review_flag": false,
  "competency_variants": [],
  "cert_signal": null,
  "prereqs": ["C170"],
  "guide_enrichment_summary": {
    "enriched": false,
    "source_programs": []
  },
  "evidence_refs": [
    {"source": "CAT", "artifact": "trusted/2026_03/program_index.json", "entity": "D426"},
    {"source": "CANON", "artifact": "canonical_courses.json", "entity": "D426"}
  ]
}
```

**Notes:**
- Clean case: catalog present, no guide alternates, no anomalies.
- `description_display_source: "cat"` → QA uses catalog text by default, no disclosure needed.
- `competency_variants: []` → this course has no guide enrichment; if asked about competencies, QA abstains (no guide data for this course).

---

### Prototype 2 — Multi-variant course (D358: Learning and Development)

D358 appears in BSHR (Business Administration — Human Resources) and MSHRM. The BSHR cluster had a catalog rewrite; guide text is locked to an older authoring event. This is one of the ~25 review-flagged courses.

```json
{
  "object_type": "course_card",
  "course_code": "D358",
  "canonical_title": "Learning and Development",
  "canonical_cus": 3,
  "title_variants": [],
  "is_active": true,
  "instances_by_version": [
    {"catalog_version": "2025_06", "line_span": "p.214–215"},
    {"catalog_version": "2026_03", "line_span": "p.217–218"}
  ],
  "program_codes": ["BSHR", "MSHRM"],
  "description_cat": "Learning and Development explores organizational training strategy, instructional design methods, needs analysis, and evaluation of training effectiveness...",
  "description_display_source": "cat",
  "description_cat_present": true,
  "description_cat_char_length": 389,
  "description_guide_alternates": [
    {
      "text": "Learning and Development introduces the fundamentals of employee training...",
      "source_program_codes": ["BSHR"],
      "source_guides": ["BSHR_guide_2025_09"],
      "char_length": 271
    },
    {
      "text": "Learning and Development examines strategic human capital development practices...",
      "source_program_codes": ["MSHRM"],
      "source_guides": ["MSHRM_guide_2026_01"],
      "char_length": 318
    }
  ],
  "description_guide_alternate_count": 2,
  "description_multi_variant": true,
  "anomaly_flags": [],
  "description_review_flag": true,
  "competency_variants": [
    {
      "source_program_codes": ["BSHR"],
      "competencies": [
        "Analyzes training needs using established assessment frameworks.",
        "Designs instructional content aligned to organizational competency models."
      ]
    },
    {
      "source_program_codes": ["MSHRM"],
      "competencies": [
        "Evaluates talent development strategy against organizational objectives.",
        "Applies adult learning theory to design of executive development programs."
      ]
    }
  ],
  "cert_signal": null,
  "guide_enrichment_summary": {
    "enriched": true,
    "source_programs": ["BSHR", "MSHRM"],
    "description_variant_count": 2,
    "competency_variant_count": 2
  },
  "evidence_refs": [
    {"source": "CAT-TEXT", "artifact": "trusted/2026_03/program_blocks.json", "entity": "D358"},
    {"source": "ENRICH", "artifact": "program_guides/parsed/BSHR_guide_2025_09.json", "entity": "D358"},
    {"source": "ENRICH", "artifact": "program_guides/parsed/MSHRM_guide_2026_01.json", "entity": "D358"},
    {"source": "CANON", "artifact": "canonical_courses.json", "entity": "D358"}
  ]
}
```

**Notes:**
- `description_display_source: "cat"` → even with 2 guide alternates, catalog is the display default.
- `description_multi_variant: true` → QA must not silently pick one guide variant; must disclose or require program context.
- `description_review_flag: true` → human review pending; does not change default behavior.
- When program context is provided (e.g., query is about BSHR), QA selects the BSHR guide alternate for guide-sourced fields; uses catalog for description.

---

### Prototype 3 — Anomaly course: cat_short_text (C179: Advanced Networking Concepts)

```json
{
  "object_type": "course_card",
  "course_code": "C179",
  "canonical_title": "Advanced Networking Concepts",
  "canonical_cus": 3,
  "title_variants": ["Network Technology Foundations"],
  "is_active": true,
  "instances_by_version": [
    {"catalog_version": "2025_06", "line_span": "p.198"},
    {"catalog_version": "2026_03", "line_span": "p.201"}
  ],
  "program_codes": ["BSITM", "BSCSIA"],
  "description_cat": "Advanced Networking Concepts covers routing and switching fundamentals.",
  "description_display_source": "cat",
  "description_cat_present": true,
  "description_cat_char_length": 293,
  "description_guide_alternates": [
    {
      "text": "Advanced Networking Concepts provides an in-depth examination of routing protocols, switching architectures, automation frameworks, and advanced network design principles used in enterprise environments...",
      "source_program_codes": ["BSITM"],
      "source_guides": ["BSITM_guide_2026_03"],
      "char_length": 567,
      "anomaly_flag": "cat_short_text"
    }
  ],
  "description_guide_alternate_count": 1,
  "description_multi_variant": false,
  "anomaly_flags": ["cat_short_text"],
  "anomaly_detail": "Catalog text is 293 chars — unusually short for this course type. Completeness has not been confirmed. Guide text adds routing/switching/automation specifics not present in catalog. Verify catalog extract before relying on catalog-default for this course.",
  "description_review_flag": true,
  "competency_variants": [
    {
      "source_program_codes": ["BSITM"],
      "competencies": [
        "Configures advanced routing protocols in simulated enterprise environments.",
        "Evaluates switching design choices for network performance and redundancy."
      ]
    }
  ],
  "guide_enrichment_summary": {
    "enriched": true,
    "source_programs": ["BSITM"],
    "description_variant_count": 1,
    "competency_variant_count": 1
  },
  "evidence_refs": [
    {"source": "CAT-TEXT", "artifact": "trusted/2026_03/program_blocks.json", "entity": "C179"},
    {"source": "ENRICH", "artifact": "program_guides/parsed/BSITM_guide_2026_03.json", "entity": "C179"},
    {"source": "CANON", "artifact": "canonical_courses.json", "entity": "C179"}
  ]
}
```

**Notes:**
- `anomaly_flags: ["cat_short_text"]` → QA behavior at retrieval time:
  - Still uses catalog as default source
  - Must add disclosure: "Catalog description for this course is unusually brief; completeness is unconfirmed."
  - May offer guide alternate as supplemental: "The program guide contains additional detail."
- `description_cat_char_length: 293` → QA control layer can detect this without LLM involvement.
- Guide alternate tagged with `anomaly_flag: "cat_short_text"` on the alternate itself so consumers know why it's being surfaced.

---

### Prototype 4 — Anomaly course: guide_misrouted_text (D554: Advanced Financial Accounting I)

```json
{
  "object_type": "course_card",
  "course_code": "D554",
  "canonical_title": "Advanced Financial Accounting I",
  "canonical_cus": 3,
  "title_variants": [],
  "is_active": true,
  "instances_by_version": [
    {"catalog_version": "2025_06", "line_span": "p.244"},
    {"catalog_version": "2026_03", "line_span": "p.247"}
  ],
  "program_codes": ["MACCA", "MACCF"],
  "description_cat": "Advanced Financial Accounting I examines complex accounting topics including business combinations, consolidated financial statements, and partnership accounting...",
  "description_display_source": "cat",
  "description_cat_present": true,
  "description_cat_char_length": 398,
  "description_guide_alternates": [],
  "description_guide_alternate_count": 0,
  "description_multi_variant": false,
  "anomaly_flags": ["guide_misrouted_text"],
  "anomaly_detail": "Guide description for this course contains text from D560 (Internal Auditing I) — a data anomaly in the extraction pipeline. Guide description has been blocked from the alternates array and must not be used for any QA answer.",
  "description_review_flag": false,
  "competency_variants": [],
  "guide_enrichment_summary": {
    "enriched": false,
    "source_programs": [],
    "anomaly_note": "Guide description blocked due to misrouted text (D560 content). No competency data available."
  },
  "evidence_refs": [
    {"source": "CAT-TEXT", "artifact": "trusted/2026_03/program_blocks.json", "entity": "D554"},
    {"source": "CANON", "artifact": "canonical_courses.json", "entity": "D554"}
  ]
}
```

**Notes:**
- `anomaly_flags: ["guide_misrouted_text"]` → QA behavior:
  - Catalog text is fine and used as default.
  - `description_guide_alternates: []` — guide description is blocked at the artifact layer, not just filtered at generation time.
  - If a user asks about guide-sourced competencies for D554: abstain with note: "Guide data for this course contains a known data anomaly and cannot be used."
- No `ENRICH` evidence_ref because the guide data is blocked.
- Blocking is hard (at the artifact layer), not soft (a prompt instruction).

---

## Object type: `program_version_card`

One card per (program_code, version) pair. This is the version-scoped unit. A program with 3 catalog appearances has 3 cards; the latest is flagged `is_latest: true`.

### Prototype 5 — Normal program (BSCS: B.S. Computer Science, 2026_03)

```json
{
  "object_type": "program_version_card",
  "program_code": "BSCS",
  "degree_title": "Bachelor of Science, Computer Science",
  "college": "College of IT",
  "version": "2026_03",
  "is_latest": true,
  "total_cus": 120,
  "description_cat": "The Bachelor of Science in Computer Science program prepares students to apply mathematical foundations, algorithm design, systems-level thinking, and software engineering principles...",
  "description_display_source": "cat",
  "version_conflict": false,
  "course_list_summary": {
    "total_courses": 42,
    "required_courses": 38,
    "elective_slots": 4
  },
  "section_presence": {
    "standard_path": true,
    "areas_of_study": false,
    "capstone": true
  },
  "guide_links": [
    {
      "guide_id": "BSCS_guide_2026_03",
      "guide_version": "2026_03",
      "version_match": true
    }
  ],
  "plo_source": "CAT-TEXT",
  "plo_count": 7,
  "evidence_refs": [
    {"source": "CAT", "artifact": "trusted/2026_03/program_index.json", "entity": "BSCS", "version": "2026_03"},
    {"source": "CAT-TEXT", "artifact": "trusted/2026_03/program_blocks.json", "entity": "BSCS", "version": "2026_03"},
    {"source": "GUIDE", "artifact": "program_guides/parsed/BSCS_guide_2026_03.json", "entity": "BSCS"}
  ]
}
```

**Notes:**
- `version_conflict: false` → single-version retrieval is safe; no dual-token disclosure needed.
- `section_presence` tells the QA control layer which guide section cards are available before retrieval.
- `plo_source: "CAT-TEXT"` — confirms guides do not contain PLOs; no retrieval from guide for PLO queries.
- `is_latest: true` → used to implement "default to most recent version" policy.

---

### Prototype 6 — Version-conflicted program (MSHRM: M.S. Human Resource Management)

MSHRM has a guide dated 8 months newer than the catalog. Body text is currently identical after prefix strip, but the freshness gap is real.

```json
{
  "object_type": "program_version_card",
  "program_code": "MSHRM",
  "degree_title": "Master of Science, Human Resource Management",
  "college": "College of Business",
  "version": "2026_03",
  "is_latest": true,
  "total_cus": 36,
  "description_cat": "The Master of Science in Human Resource Management program develops advanced competencies in talent management, organizational development, employment law, and strategic HR leadership...",
  "description_display_source": "cat",
  "version_conflict": true,
  "version_conflict_detail": {
    "catalog_version": "2026_03",
    "guide_version": "2026_11",
    "gap_months": 8,
    "gap_direction": "guide_newer",
    "body_text_status": "identical_after_prefix_strip",
    "disclosure_required": true,
    "disclosure_text": "Program data is drawn from the 2026-03 catalog and the 2026-11 program guide. No content differences were found between sources at this time, but a freshness gap of 8 months exists."
  },
  "course_list_summary": {
    "total_courses": 12,
    "required_courses": 12,
    "elective_slots": 0
  },
  "section_presence": {
    "standard_path": true,
    "areas_of_study": false,
    "capstone": true
  },
  "guide_links": [
    {
      "guide_id": "MSHRM_guide_2026_11",
      "guide_version": "2026_11",
      "version_match": false,
      "version_gap_months": 8
    }
  ],
  "plo_source": "CAT-TEXT",
  "plo_count": 5,
  "evidence_refs": [
    {"source": "CAT", "artifact": "trusted/2026_03/program_index.json", "entity": "MSHRM", "version": "2026_03"},
    {"source": "CAT-TEXT", "artifact": "trusted/2026_03/program_blocks.json", "entity": "MSHRM", "version": "2026_03"},
    {"source": "GUIDE", "artifact": "program_guides/parsed/MSHRM_guide_2026_11.json", "entity": "MSHRM", "guide_version": "2026_11"}
  ]
}
```

**Notes:**
- `version_conflict: true` triggers automatic dual-version disclosure in any answer about this program — no LLM decision needed.
- `disclosure_text` is a pre-composed deterministic string, not generated by the model.
- `body_text_status: "identical_after_prefix_strip"` lets the QA layer know there is no content conflict today, only a freshness gap.
- Open question: should `disclosure_text` appear in every answer, or only when the question involves content that could plausibly differ between versions? (See RFI §5.4 Q3.)

---

## Object type: `guide_section_card`

One card per (program_code, guide_version, section_type). Canonical view of a parsed guide section. This is the primary retrieval object for section-grounded questions.

### Prototype 7 — Standard path section (BSCS standard_path)

```json
{
  "object_type": "guide_section_card",
  "program_code": "BSCS",
  "guide_version": "2026_03",
  "section_type": "standard_path",
  "section_label": "Standard Program Path",
  "is_complete": true,
  "rows": [
    {
      "semester": 1,
      "courses": [
        {"course_code": "C168", "title": "Discrete Mathematics I", "cus": 3},
        {"course_code": "C170", "title": "Intro to IT", "cus": 3},
        {"course_code": "C172", "title": "Network and Security Foundations", "cus": 3}
      ]
    },
    {
      "semester": 2,
      "courses": [
        {"course_code": "C169", "title": "Scripting and Programming Foundations", "cus": 3},
        {"course_code": "C173", "title": "Scripting and Programming Applications", "cus": 3},
        {"course_code": "C175", "title": "Data Management Foundations", "cus": 3}
      ]
    }
  ],
  "course_count": 42,
  "total_cus_in_path": 120,
  "path_qualifier": "As listed in the BSCS program guide. Reflects one path through the program; elective substitutions may differ.",
  "linked_course_codes": ["C168", "C170", "C172", "C169", "C173", "C175"],
  "evidence_refs": [
    {"source": "GUIDE", "artifact": "program_guides/parsed/BSCS_guide_2026_03.json", "section": "standard_path", "entity": "BSCS", "version": "2026_03"}
  ]
}
```

**Notes:**
- `path_qualifier` is pre-composed and must appear in any answer using this card. The model may not paraphrase this away.
- `is_complete: true` → the parser found the full section; completeness gate is satisfied for this section.
- `linked_course_codes` enables direct join to `course_card` objects at retrieval time.
- Source family: GUIDE sole source. No CAT or CANON evidence retrieved for standard_path questions.

---

## Object type: `version_diff_card`

One card per (entity_type, entity_id, from_version, to_version). Deterministic diff over structured canonical objects. Model may only summarize the diff, not compute it.

### Prototype 8 — Program version diff (BSCS: 2025_06 → 2026_03)

```json
{
  "object_type": "version_diff_card",
  "entity_type": "program",
  "entity_id": "BSCS",
  "from_version": "2025_06",
  "to_version": "2026_03",
  "diff_basis": "course_list + total_cus + description_cat",
  "added": {
    "courses": ["D426", "C191"],
    "notes": "Two new courses added to required sequence."
  },
  "removed": {
    "courses": ["C392"],
    "notes": "One course removed from required sequence."
  },
  "changed": {
    "total_cus": {"from": 118, "to": 120, "delta": 2},
    "description_cat": {"changed": true, "summary": "Program description revised; new sentence added on AI/ML specialization track."}
  },
  "unchanged": {
    "degree_title": true,
    "college": true,
    "section_presence": true
  },
  "version_disclosure": "Comparing BSCS as of catalog edition 2025-06 vs 2026-03. All differences are deterministic; no model inference was used.",
  "evidence_refs": [
    {"source": "CAT", "artifact": "edition_diffs/bscs_diff_2025_06_2026_03.json", "entity": "BSCS"},
    {"source": "CANON", "artifact": "canonical_courses.json"}
  ]
}
```

**Notes:**
- The model may summarize this card but must not recompute or extend the diff.
- `diff_basis` tells the QA layer what fields were diffed. Fields not listed are not covered by this card.
- `version_disclosure` is a required pre-composed string; the model must not omit or paraphrase it.
- If a user asks "what changed between 2025 and 2026 for BSCS", the QA layer fetches this card and the model formats it. No retrieval of raw text blocks needed.

---

## Open questions this pack surfaces for reviewers

1. **Source-authority fields on `course_card`**: are these fields (`description_display_source`, `anomaly_flags`, `description_guide_alternate_count`) sufficient for the QA control layer to apply policy deterministically without LLM involvement? Are there missing fields?

2. **`version_conflict_detail` on `program_version_card`**: is `disclosure_text` the right shape, or should the dual-version disclosure be a structured object that the answer template renders? (The concern is that a pre-composed string may not fit all answer contexts.)

3. **`path_qualifier` on `guide_section_card`**: is a string qualifier sufficient, or should there be a structured field indicating which courses in the path are required vs elective?

4. **`version_diff_card` scope**: this prototype covers course list and description diffs. Should it also cover guide section diffs (AoS added/removed, capstone changed)? Or is that a separate card?
