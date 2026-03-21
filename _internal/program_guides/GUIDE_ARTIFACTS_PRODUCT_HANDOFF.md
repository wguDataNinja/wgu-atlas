# Guide Artifacts Product Handoff

**Created:** 2026-03-21 (Session 30)
**Purpose:** Make the guide artifact layer concrete and product-usable for future build and design sessions.
**Audience:** Future build sessions, design sessions, and anyone assessing what the guide layer can actually provide.
**Status:** Current as of guide targets extraction completion (Session 29, 2026-03-21).

---

## Section 1: Executive State

### What now exists

The guide extraction workstream is complete. The pipeline ran from raw PDFs through parse, match, enrich, and target-extract phases. Five new target artifacts were produced in Session 29. Together with earlier artifacts, the guide layer now has real, Atlas-ready content across multiple signal types.

Nothing from this data has yet been published to the Atlas site. The artifact generator (`build_guide_artifacts.py`) has not been built. All data is internal.

### Layer-by-layer status

**Parsed guide corpus — 115 programs**
Complete and canonical. Every active WGU program has a structured JSON representing its full guide content: degree title, Standard Path rows (course, CUs, term), Areas of Study (course descriptions and competency bullets), capstone, cert prep mentions, and prereq mentions. Parser is stable; no rewrites planned. 4 programs have partial usability caveats (BSITM, MATSPED, MSCSUG, BSPRN) — AoS content is intact for all, SP is problematic or suppressed for these four.

**Degree enrichment payload**
Policy designed and ready. The PHASE_D policy and schema pack defines exactly what gets published to degree pages, at what confidence, and with what caveats. The artifact generator script has not been built yet. This is the immediate next implementation step.

**Course enrichment payload**
751 canonical courses have guide-derived enrichment — descriptions, competency bullets, and program context. 185 courses have multiple competency variant sets (same course appears in multiple programs with different bullets); 74 courses have multiple description variants. This data is in `enrichment/course_enrichment_candidates.json`. No course-page surfacing decision has been made yet.

**Cert mapping — `cert_course_mapping.json`**
Complete. 9 auto-accepted cert→course mappings (all high confidence, confirmed across 3+ programs). 21 review-needed rows (mostly single-program, vendor-specific, or ambiguous vendor fragment strings). The 9 auto-accepted rows are ready to drive cert badges on course and degree pages immediately.

**Prereq relationships — `prereq_relationships.json`**
Complete. 50 auto-accepted prereq relationships (high confidence, explicit course-to-course or code-anchored). 21 review-needed rows (single-program, inverted capture, or cumulative nursing sequences). The 50 auto-accepted rows are ready to drive prereq display on course pages.

**SP family / specialization classification — `sp_family_classification.json` + `sp_families.json`**
Complete. All 115 programs classified. 7 named families defined with member lists, shared course counts, and display recommendations. The classification is deterministic and fully auditable.

**Anomaly registry — `guide_anomaly_registry.json`**
Complete. 9 anomaly records covering all known issue types, with Atlas handling rules. This feeds the caveat/provenance layer and partial-use rules in PHASE_D policy.

### Summary table

| Layer | Status | Ready for Atlas |
|---|---|---|
| Parsed guide corpus (115 programs) | Complete | Yes (internal use) |
| Degree enrichment payload design | Designed, not built | Pending artifact generator |
| Course enrichment payload (751 courses) | Complete | Pending course-page decision |
| Cert mapping (9 auto-accepted, 21 review) | Complete | 9 rows ready now |
| Prereq relationships (50 auto-accepted, 21 review) | Complete | 50 rows ready now |
| SP family classification (115 programs) | Complete | Ready now |
| Anomaly registry (9 records) | Complete | Ready now |

---

## Section 2: Artifact Inventory

### New guide target artifacts (Session 29, 2026-03-21)

**`data/program_guides/cert_course_mapping.json`**
- What it contains: cert→course mappings extracted from `certification_prep_mentions` across all 115 parsed guides. 139 raw mentions, 51 suppressed as AWS noise, 9 auto-accepted (high confidence, 3+ programs each), 21 review-needed (medium confidence, single-program or fragment).
- Granularity: course-level mapping with program provenance. Each row is (normalized_cert, course_title, course_code, source_programs, confidence, atlas_recommendation).
- Confidence: HIGH for auto-accepted rows (cross-program confirmed). MEDIUM for review rows.
- Likely Atlas uses: cert badges on course pages (e.g., "Helps prepare for CompTIA A+"); cert signal blocks on degree pages ("This program includes CompTIA A+, CompTIA Network+, AWS Certified course prep").
- Caveats: Review queue includes vendor-specific strings that are tool/platform mentions rather than cert-prep signals (e.g., "AWS platform", "Azure environment"). These need editorial judgment before surfacing. NCLEX (nursing) is not in this file — that signal exists in program descriptions only, not course-level extraction.

**`data/program_guides/prereq_relationships.json`**
- What it contains: prereq relationships extracted from `prerequisite_mentions` across all 115 parsed guides. 264 raw mentions, 135 false positives suppressed (boilerplate no-prereq language), 12 soft-preparedness suppressed, 71 meaningful records remaining. 50 auto-accepted, 21 review-needed.
- Granularity: course-level relationship (target_course_code, prerequisite_code, relationship type, source_programs, confidence, review_status). Type distribution: 51 explicit-course-prereq, 3 code-anchored, 16 cumulative-sequence (nursing), 1 inverted-capture.
- Confidence: HIGH for 50 auto-accepted rows. MEDIUM for 21 review rows.
- Likely Atlas uses: prereq display on course pages ("Requires: Data Management - Foundations"); prereq chain visualization for sequenced programs (BSCS, BSDA, BSACC).
- Caveats: Cumulative nursing sequence prereqs (16 rows) model "all prior terms" plus a specific code — these require a different display treatment than simple single-prereq relationships. The 21 review rows include the inverted-capture case and nursing sequences requiring manual verification.

**`data/program_guides/sp_family_classification.json`**
- What it contains: Per-program SP classification for all 115 programs. Fields: program_code, sp_category (A/B/C/D), sp_category_label, sp_length, term_status, family_code, anomaly_entry_count, longest_title_length, notes, track_declaration.
- Granularity: program-level. 72 Category A (structured term path), 23 Category B (null-term / advisor-guided), 19 Category C (track/specialization member), 1 Category D (anomalous — MATSPED).
- Confidence: Fully deterministic. HIGH across the board.
- Likely Atlas uses: Drives how degree pages display Standard Path (term-grouped vs. ordered-list vs. track-variant); drives the "Advisor-sequenced" label for education licensure programs; enables family relationship display on track member pages.
- Caveats: Category D (MATSPED) means SP is fully suppressed. Category A with BSITM means SP is used with one entry suppressed (ANOM-002). MSCSUG is Category A but requires an "Accelerated B.S./M.S. pathway" label.

**`data/program_guides/sp_families.json`**
- What it contains: 7 named family definitions. Each family has: family_code, family_label, family_type, declaration_text (when extractable from program_description), members (with track_labels), member_count, sp_relationship, shared_course_count, display_recommendation.
- Granularity: family-level. 7 families covering 19 programs total.
- Confidence: HIGH (structure verified against parsed data; shared course counts computed).
- Likely Atlas uses: Family relationship panels on degree pages ("This program is one of 4 tracks in the Master of Accounting family — see also: Financial Reporting, Taxation, Management Accounting"); related-degree navigation.
- Caveats: BSCNE family has no explicit parent-guide declaration — inferred from code prefix and shared courses. PMCNU family has 0 shared courses (each specialization is fully distinct). MSMK family has no extracted declaration text.

**`data/program_guides/guide_anomaly_registry.json`**
- What it contains: 9 anomaly records, each with anomaly_id, program_code (when program-specific), issue_type, affected_surface, description, detection_method, source_side (extraction vs. structural), atlas_handling, sp_category_assigned, wgu_feedback_candidate, notes.
- Granularity: issue-level. Covers MATSPED (catastrophic SP concatenation), BSITM (partial SP concatenation), MSCSUG (bridge program semantics), AWS noise suppression, no-prereq boilerplate suppression, BSNU missing metadata, MEDETID partial capstone, Praxis trailing comma, degree title truncations.
- Confidence: Fully documented, handling rules specified.
- Likely Atlas uses: Caveat/provenance rules for partial-use guides; suppression signals for the artifact generator; transparency layer for methods/methodology page.
- Caveats: MATSPED and BSITM are WGU feedback candidates (source PDF structure issues). Others are extraction-side issues already handled.

---

### Existing guide infrastructure artifacts

**`data/program_guides/parsed/` — 115 `*_parsed.json` files**
- What it contains: Structured output from `parse_guide.py` for each of the 115 guides. Per-guide: degree_title, version, pub_date, standard_path rows (title, CUs, term), areas_of_study (grouped courses with descriptions and competency bullets), capstone, prereq/cert mentions.
- Granularity: Program-level container with course-level detail.
- Confidence: 96 HIGH / 17 MEDIUM / 2 LOW (by guide).
- Likely Atlas uses: Source of truth for all guide content. The artifact generator reads from here.
- Caveats: Do not regenerate unless a parser fix is applied. Four partial-use guides noted above.

**`data/program_guides/enrichment/course_enrichment_candidates.json`**
- What it contains: The primary deliverable of the data extraction phase. 751 canonical courses with all guide-derived content: descriptions (with multi-program variants), competency sets (with variants), SP context, program group context, anchor class.
- Granularity: Course-level, with multi-program variant tracking.
- Confidence: High for exactly-matched courses; medium for LLM-resolved or variant-matched.
- Likely Atlas uses: Course-page descriptions and competency bullets; degree AoS content blocks.
- Caveats: 74 courses have multiple description variants (need policy decision on which to surface). 185 courses have multiple competency set variants. 542 courses remain unmatched (irreducible without catalog changes).

**`data/program_guides/enrichment/course_enrichment_summary.json`**
- Coverage counts: 751 courses, 730 descriptions, 729 competency sets, 723 SP context, 730 AoS context, 74 multi-description, 185 multi-competency. Anchor class distribution breakdown. SP CU conflict count: 41.

**`data/program_guides/bridge/merge_summary.json`**
- What it contains: Post-merge coverage counts, anchor class distribution, medium-confidence case rationales, and unresolvable case documentation. The final audit record for all 5,087 bridge rows across 115 guides.
- Granularity: Corpus-level summary with case-by-case records for medium and unresolvable decisions.
- Confidence: Audit-complete.
- Likely Atlas uses: Provenance reference; methods/methodology page documentation.

**`data/program_guides/bridge/guides_merged/` — 115 merged per-guide bridge files**
- The canonical bridge output. Each file maps guide course titles to resolved catalog codes. Downstream enrichment reads from here.

**`data/program_guides/validation/` — 115 `*_validation.json` files**
- Per-guide quality scores: confidence rating, anomaly flags, warning counts, AoS vs. SP course count reconciliation.
- Gate artifact: the artifact generator should respect these signals for inclusion/exclusion.

**`data/program_guides/manifest_rows/` — 115 `*_manifest_row.json` files**
- Compact per-guide summary rows. Input to corpus manifest and the artifact generator's per-guide inclusion/exclusion logic.

**`data/program_guides/guide_manifest.json`**
- Earlier-phase manifest (pre-extraction-targets). Covers guide structure presence flags (has_standard_path, has_areas_of_study, has_cert_prep_mentions, etc.) and per-guide structural counts.

**`data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` (+ companion files)**
- The design pack for the Atlas degree-enrichment artifact generator. Defines publish policy, artifact schema, and build plan. This is the primary reference for implementing `build_guide_artifacts.py`.
- Companion files: `phase_d_publish_policy.{md,json}`, `phase_d_artifact_schema.{md,json}`, `phase_d_build_plan.{md,json}`

**`data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.{md,json}`**
- Canonical corpus facts: 115 guides, per-guide counts, coverage, confidence, caveats. The authoritative "what is in this corpus" document.

**`data/program_guides/audit/program_guide_claims_register.{md,json}`**
- Approved vs. disallowed claims about the corpus. What language is safe to use about the guide data; what is overstated. Gate artifact for communications and product copy.

**`data/program_guides/family_validation/`**
- Historical rollout record: per-family gate reports and rollout summaries from each of the 19 program families. Shows validated state at Phase C close.

---

## Section 3: Product Payload by Surface

### Degree pages (`/programs/[code]`)

**Areas of Study (course list with guide-derived content)**

Ready to use now:
- Course descriptions per degree for every AoS course. 2,593 guide courses have descriptions; 751 of these are matched to canonical catalog codes.
- Competency bullets per course. Same coverage.
- AoS group labels (the section headings that organize courses, e.g., "Computer Science Core", "General Education").
- SP term numbers for Category A programs (72 programs): each course's term placement is known.

Needs policy/design decision before use:
- For courses appearing in multiple programs (up to 185 competency variants, 74 description variants): which variant to surface per degree? Policy options: use the guide description from this specific program's guide (most accurate), use a consensus/primary description (simpler), or show the per-program variant with a provenance note.
- SP CU values: 41 courses have CU conflicts across programs. Need a display decision (show per-program CU vs. catalog CU).

Review-backed / partial:
- SP for 3 programs (BSITM, MATSPED, MSCSUG): MATSPED is fully suppressed; BSITM is used with one entry suppressed; MSCSUG is used with a bridge-program label.
- BSPRN: SP shows Pre-Nursing track only; Nursing-track courses are AoS-only.

Still missing entirely:
- Guide provenance badge design (what text/label signals that content is guide-sourced).

**Guide provenance badge**

Ready to use now:
- version and pub_date are available for 114 programs (BSNU is the one exception per ANOM-006).

Still missing entirely:
- Badge component design and placement on the degree page.

**Cert signals (cert badges / mentions per degree)**

Ready to use now:
- 9 auto-accepted cert→course mappings. Transitive derivation: if a course is in a degree and that course maps to a cert, the degree carries that cert signal. Example: BSCNE carries CompTIA A+, CompTIA Network+, CompTIA Security+, CompTIA Cloud+, AWS Certified (via its courses).

Needs policy/design decision before use:
- At what threshold do certs appear in a degree cert block? (All confirmed certs? Only top-N? Only multi-program confirmed ones?)
- How to handle degree-only recommendations vs. course-level cert badges (the `atlas_recommendation` field in cert_course_mapping.json distinguishes these).
- Review queue (21 rows): vendor-platform strings (Azure CLI, Cisco DevNet, etc.) need editorial decision before Atlas display.

Still missing entirely:
- NCLEX for nursing programs (present in program description text, not course-level extraction — see Section 5).
- CPA Exam signal for BSACC (only "CPA Code" captured, mapped to BSACC Auditing course — thin extraction; see Section 5).

**Standard Path shape (term-structured vs. advisor-guided)**

Ready to use now:
- Category A (72 programs): term-structured. Display as term-grouped course list.
- Category B (23 programs): null-term / advisor-guided. Display as ordered course list with label "Advisor-sequenced — individual pacing varies." All are education licensure, MAT, or endorsement families.
- Category C (19 programs): track/specialization member. Display with family relationship panel.
- Category D (1 program — MATSPED): SP suppressed. Display AoS-only with a note.

**Track/specialization family membership**

Ready to use now:
- 7 families fully defined with member lists, track labels, shared course counts, and sp_relationship type.
- Display recommendation for each family is documented in sp_families.json.

Needs policy/design decision before use:
- What does the family panel look like on a degree page? (Link list to siblings? Shared core course count display? Track comparison table?)
- For BSCNE: the vendor track family is inferred from code structure, not declared in a single guide. Need to decide whether to display this relationship and with what confidence label.

**Capstone course identification**

Ready to use now:
- Capstone field is populated for guides that have a capstone section. Present for the majority of programs.

Review-backed / partial:
- MEDETID (ANOM-007): only the first of 3 capstone courses is captured. Display with `partial: true` flag or suppress.

**Anomaly caveats**

Ready to use now:
- Anomaly registry specifies Atlas handling rules for each known issue. The artifact generator should implement these rules directly.
- For MATSPED, BSITM, MSCSUG, BSNU, MEDETID: specific suppression or labeling rules are documented in guide_anomaly_registry.json.

---

### Course pages (`/courses/[code]`)

**Guide-derived descriptions**

Ready to use now:
- 730 of 751 enriched courses have descriptions. For courses with a single description variant (656 courses), this is directly usable.

Needs policy/design decision before use:
- 74 courses have multiple description variants (same course appears in multiple programs with different descriptions). Need a policy: use the "primary" description (most programs? alphabetically first?), or show the most common one, or show one with a provenance note ("As described in the BSCS guide").
- Relationship between guide description and catalog description already in `course_descriptions.json`. These may overlap or differ.

Still missing entirely:
- Integration design for course detail pages — where guide content appears relative to catalog-sourced content.

**Competency bullets**

Ready to use now:
- 729 enriched courses have competency sets.

Needs policy/design decision before use:
- 185 courses have multiple competency variants across programs. Same policy question as descriptions.

**Cert relationships**

Ready to use now:
- 9 auto-accepted cert mappings link courses to certs. Example: C394 (IT Applications) → CompTIA A+; C393 (IT Foundations) → CompTIA A+; D282A (Cloud Foundations) → AWS Certified.

**Prereq relationships**

Ready to use now:
- 50 auto-accepted prereq relationships. Each links a target course code to a prerequisite course code. Ready for prereq display on course pages.

Review-backed / partial:
- 21 review-needed rows including 16 cumulative-sequence nursing prereqs (require "all prior terms" display logic, not a simple single-course prereq badge).
- 1 inverted-capture row (Financial Management I / Corporate Finance — direction needs manual confirmation).

**Cross-program variability notes**

Ready to use now:
- The enrichment candidates file tracks which programs each course appears in and how many description/competency variants exist. This enables "This course appears in N programs" and "Description may vary by program" notes.

**Program context**

Ready to use now:
- SP context and AoS group context are tracked per course in the enrichment candidates file. Each course knows which program(s) it appears in, what AoS group it belongs to, and what its SP term was in each program.

---

### Family / related-degree layer

**Track family membership**

Ready to use now:
- BSSWE (2 tracks, 33 shared courses): Java and C# tracks.
- MACC (4 tracks, 6 shared courses): Auditing, Financial Reporting, Management Accounting, Taxation.
- MSRNN (3 specializations, 25 shared courses): Education, Leadership/Management, Nursing Informatics.
- BSCNE (4 vendor tracks, 26 shared courses): Vendor-Agnostic, AWS, Azure, Cisco.
- PMCNU (4 specializations, 0 shared courses): Nursing Education, FNP, Leadership/Management, Psychiatric Mental Health NP.
- MSMK (2 specializations, 8 shared courses): Digital Marketing, Marketing Analytics.
- BAELED (2 structural variants, 33 shared courses): Licensure/advisor-guided and Educational Studies/term-structured.

**Shared-core vs. diverging-track structure**

Ready to use now:
- Shared course counts and sp_relationship type are specified for each family.
- BSSWE: shared_core_diverging_track (33 shared, language/implementation diverges).
- MACC: shared_foundation_diverging_track (6 shared foundation courses, then track-specific divergence).
- MSRNN: shared_core_diverging_specialization (25 shared core, then specialization courses).
- BSCNE: shared_core_diverging_vendor_track (26 shared, then vendor-specific courses).
- PMCNU: parallel_specialization_short_sp (each specialization is independent; 0 shared).
- MSMK: parallel_specialization (8 shared).
- BAELED: structural_variant (licensure vs. non-licensure — SP term status IS the distinguishing signal).

**Licensure vs. non-licensure variant structure**

Ready to use now:
- BAELED family has explicit display_recommendation: "show both with explicit labels; SP term status IS the distinguishing signal between licensure and non-licensure."
- Category B (null-term, 23 programs) reliably identifies the education licensure set.

Needs policy/design decision before use:
- What does the "related programs" section of a family member's degree page look like? (Simple link list? Side-by-side comparison? Shared core call-out?)

---

## Section 4: Payload Shape Families

### Degree shape families

**Normal structured-term guide**

What it is: A program with a clean Standard Path (all courses have term numbers) and complete AoS content. The large majority of programs.

Representative programs: BSCS, BSIT, BSDA, BSHA, BSC, MSMBA.

Why it matters: The default degree page display. Term-grouped course list, AoS descriptions, competency bullets, guide provenance badge. No special handling needed.

Atlas display: Full SP display with term grouping. Full AoS content blocks. Optional cert badge block. Optional prereq display per course.

---

**Null-term / advisor-guided guide**

What it is: A program whose Standard Path has all `term: null` entries. Not a structured term sequence — pacing is individually determined with an advisor. Concentrated entirely in education licensure, MAT, and endorsement families (23 programs).

Representative programs: BAELED, MATEES, MATSPED (AoS-only due to ANOM-001), ENDSESC.

Why it matters: Displaying a term-grouped sequence for these programs would be actively misleading. The SP exists but carries no term structure. AoS content (descriptions, competency bullets) is intact and usable.

Atlas display: Ordered course list (no term grouping). Label: "Advisor-sequenced — individual pacing varies." Full AoS content. For MATSPED: suppress SP entirely; AoS only.

---

**Track/specialization member**

What it is: A program that is explicitly one track of a multi-track family. The program's Standard Path is single-track (for this track), but the degree belongs to a named sibling group.

Representative programs: BSSWE_Java, BSSWE_C, MACCA, MACCF, MACCM, MACCT, MSRNNUED, MSRNNULM, MSRNNUNI, BSCNEAWS, BSCNEAZR, BSCNECIS.

Why it matters: Displaying only the single-track SP without the family context undersells the degree's relationship to its siblings. Students researching one track need to see the others.

Atlas display: Normal SP display for this track, plus a family relationship panel showing siblings, shared course count, and divergence point. For MACC: call out the 6-course shared foundation explicitly. For BSSWE: note the 33-course shared core.

---

**Cert-heavy degree**

What it is: A program with multiple confirmed cert→course mappings — the program is explicitly oriented around industry certification preparation.

Representative programs: BSCNE (A+, Network+, Security+, Cloud+), BSCNEAWS (A+, Network+, AWS Certified), BSCSIA (A+, Network+, Security+, CompTIA CySA+, CompTIA Project+), BSIT (A+, Network+, Security+, Cloud+, AWS Certified, CompTIA Project+).

Why it matters: These programs have a distinct identity as cert-prep programs. A cert badge block on the degree page is a key differentiating signal for students evaluating these programs.

Atlas display: Standard SP + AoS content, plus a cert prep signal block at the degree level showing all confirmed cert → course mappings. For vendor-track programs (BSCNEAZR, BSCNECIS), the vendor-specific cert signals (Azure Fundamentals, Cisco Certified) should display at the degree level only (not course-level badges) until review queue is resolved.

---

**Capstone-rich degree**

What it is: A program with a prominent capstone section in its guide. Most programs have a single capstone course; some have structured capstone sequences.

Representative programs: BSCS (C964 Computer Science Capstone), BSIT (D498 IT Capstone), MEDETID (3 capstone courses — partial capture, ANOM-007).

Why it matters: Capstone identification signals the degree's culminating applied learning component. Students value knowing what the end-of-program experience looks like.

Atlas display: Capstone highlighted in the AoS or SP section. For MEDETID: display captured capstone with caveat ("Part of a multi-course capstone sequence").

---

**Anomaly/caveat degree**

What it is: A program where one or more guide signals is suppressed, labeled, or partially usable due to extraction or structural issues.

Representative programs: MATSPED (SP suppressed — ANOM-001), BSITM (one SP entry suppressed — ANOM-002), MSCSUG (bridge program label — ANOM-003), MEDETID (partial capstone — ANOM-007), BSNU (no guide metadata — ANOM-006).

Why it matters: These programs need explicit Atlas handling rules so that incomplete data is not displayed as complete, and so that extraction artifacts don't reach students.

Atlas display: Per-anomaly handling as specified in guide_anomaly_registry.json. Suppress what must be suppressed. Add labels where appropriate. Never display concatenated garbage strings.

---

**Licensure vs. non-licensure structural variant**

What it is: Two related programs with fundamentally different SP structures — one is advisor-guided (licensure), one is term-structured (non-licensure). They share most course content but differ in pacing model and regulatory scope.

Representative family: BAELED (B.A., Elementary Education — licensure, Category B) and BAESELED (B.A. Education Studies: Elementary — non-licensure, Category A). 33 shared courses.

Why it matters: Students choosing between licensure and non-licensure variants need explicit signals about what the structural difference means — not just different program names. The null-term SP is the proxy signal for licensure programs; the term-structured SP signals the non-licensure variant.

Atlas display: Both programs in the family panel with explicit labels. "Licensure pathway — advisor-sequenced." "Educational Studies (non-licensure) — standard term sequence." Show shared course count.

---

### Course shape families

**Stable single-context course**

A course appearing in one or a few programs, with a clean, single description and single competency set. The simplest case.

Examples: Most education-specific content courses (e.g., Secondary Chemistry Curriculum, D872). Most graduate-only courses.

Atlas display: Single description, single competency set, cert badge if applicable, prereq badge if applicable. No variant caveat needed.

---

**Multi-program course**

A course appearing in many programs (e.g., 6–8+), potentially with multiple description variants or competency variants across those programs.

Examples: IT Applications (C394, 7 programs), Cloud Foundations (D282A, 6+ programs), Network and Security - Applications (C178, 6 programs), Data Management - Foundations (D426, 8+ programs).

Atlas display: Single primary description (most-common or designated variant). Competency set from the designated variant. Note "This course appears in N programs" if useful. Variant tracking in internal artifacts for policy review.

74 courses have multiple description variants. 185 have multiple competency variants. Policy for which variant to surface is not yet decided.

---

**Cert-mapped course**

A course with a confirmed cert→course mapping in cert_course_mapping.json.

Examples: IT Applications (C394) → CompTIA A+; Cloud Foundations (D282A) → AWS Certified; Networks (C480) → CompTIA Network+; Business of IT - Project Management (C176) → CompTIA Project+.

Atlas display: Cert badge on the course page. "Helps prepare for [cert]." Only auto-accepted rows (9 total) should display without further review.

---

**Prereq-bearing course**

A course with incoming or outgoing prereq relationships in prereq_relationships.json.

Examples: Data Management - Applications (C170) requires Data Management - Foundations (D426). Calculus II (D891) requires Calculus I (D890). Discrete Mathematics I (C959) requires Calculus I. Data Structures and Algorithms II (C950) requires Data Structures and Algorithms I (C949).

Atlas display: Prereq relationship badge ("Requires: [course name]") and/or "This course is a prerequisite for: [course name]". The 50 auto-accepted rows are ready for this display. Nursing cumulative-sequence prereqs need distinct display logic ("Requires completion of all prior nursing curriculum courses").

---

**Cumulative-sequence / nursing course**

A course in the BSPRN nursing program that requires completion of all prior nursing curriculum courses plus a specific code. These are not simple A-requires-B relationships.

Examples: Medical Dosage Calculations (D220) — requires all prior nursing curriculum courses plus D445.

Atlas display: Do not display as a simple prereq badge. Use a distinct label: "Requires prior completion of nursing curriculum sequence." This type is flagged as review-required in the prereq relationships artifact.

---

**Weak / sparse payload course**

A course where the enrichment payload is thin: description is missing, competency set is empty, or the course was unmatched entirely.

Examples: 21 courses have no descriptions; 22 have no competency sets; 542 guide titles are unmatched entirely.

Atlas display: Fall back to catalog description or no guide-enriched content. Do not surface empty fields. The enrichment candidates file has `courses_with_descriptions: 730` of 751 — 21 enriched courses still have null descriptions.

---

### Family shape families

**Shared-core diverging-track (BSSWE)**

Two tracks share 33 identical courses across the same terms, then diverge on language-specific courses. The guide descriptions for shared courses are essentially the same; the track-specific courses are distinct.

Display: Show shared core count. Link to both tracks from each degree page. For shared courses: single description is accurate for both contexts.

**Post-foundation specialization (MACC)**

Four tracks share a 6-course foundation ("five foundational courses" in the guide declaration, plus a sixth per the actual count), then each track follows its own curriculum. The foundation is the same regardless of which track a student chooses.

Display: Call out the shared foundation explicitly. Show divergence point. Each track page links to all four tracks.

**Vendor track (BSCNE)**

Four programs sharing 26 courses from a networking/cloud engineering core, then adding vendor-specific courses for AWS, Azure, or Cisco. The family relationship is not declared in a single guide — it is inferred from code prefix structure and shared course intersection.

Display: Vendor track family panel on all four degree pages. Note that this is an inferred relationship (not declared in a single parent guide). Cert signals are strongly differentiated by track (AWS Certified for BSCNEAWS, Azure Fundamentals for BSCNEAZR, Cisco Certified for BSCNECIS).

**Licensure / non-licensure paired (BAELED)**

Two programs with the same general content area but fundamentally different pacing structures and regulatory scopes. The null-term SP is the structural marker of licensure.

Display: Both appear in a family panel with explicit labels. The pacing distinction is as important as the content distinction. Students need to understand which variant leads to a teaching license.

---

## Section 5: What We Do NOT Yet Have Cleanly

### NCLEX for nursing programs

Signal presence: The NCLEX examination is referenced in nursing program descriptions. It is the licensure exam for nurses and a key signal for BSPRN, BSNU, BSRN.

Why it's incomplete: NCLEX was not captured at course level in the `certification_prep_mentions` field. The signal lives in program-level description text ("prepares students to pass the NCLEX-RN examination") rather than in individual course descriptions. The cert extraction pipeline operates at the course level, so NCLEX was not recovered.

What would recover it: A dedicated program-description pass for nursing programs — scan `program_description` text for NCLEX mentions, extract program-level signal, emit as a degree-only cert signal (not course-level). This is a 1-program-family extraction step, not a full re-parse.

**Assessment:** This is missing from cert_course_mapping.json entirely. The nursing degree pages cannot show an NCLEX signal without this step.

---

### CPA Exam signal for BSACC

Signal presence: "CPA Code" was captured once, mapped to the Auditing course (C240) in BSACC. This is a thin, ambiguous extraction.

Why it's incomplete: The CPA Exam connection is richer in BSACC's program description text than in any individual course description. The course-level capture is a fragment ("CPA Code" as a cert mention) rather than a meaningful "prepares for CPA Exam" statement. The extraction plan noted this as review-required.

What would recover it: A targeted program-description pass for BSACC — extract the CPA Exam signal at the degree level. Then decide whether to surface it as a degree-level cert signal, an AoS-level note, or both.

**Assessment:** Currently in the review queue with `atlas_recommendation: review-required`. Do not surface without resolution.

---

### Prereq review queue (21 rows)

Signal presence: 21 prereq relationships in the review_needed bucket. Includes 16 cumulative nursing sequence prereqs and several others.

Why it's incomplete: These rows require a display policy decision (cumulative sequences), directional verification (inverted-capture), or manual confidence confirmation. They are not suppressed — they exist in the artifact but are flagged.

What would recover it: For nursing sequences: design a display model for "all prior terms" prereqs and emit those 16 rows as a distinct type. For the inverted-capture row (Financial Management I / Corporate Finance): manual verification and direction confirmation. For remaining review rows: human check against the guide source text.

**Assessment:** 21 rows awaiting resolution. Numeric priority: the 16 nursing cumulative-sequence rows benefit from a display design decision, not further extraction.

---

### Cert review queue (21 rows)

Signal presence: 21 cert rows in the review_needed bucket. These include vendor-platform strings (AWS CLI, Azure CLI, Azure environment, Cisco DevNet, etc.) and single-program vendor cert mentions.

Why it's incomplete: Many of these are tool/platform references rather than exam-prep signals (e.g., "AWS platform" appearing in a capstone project description does not mean the course prepares for an AWS exam). Editorial judgment is needed to distinguish product mention from cert prep.

What would recover it: Human review of each row against the source guide text. Likely outcome: some rows get promoted to use, some get promoted to degree-only, some get suppressed.

**Assessment:** 21 rows in review. The most actionable ones are: Azure Fundamentals → D303 (clean cert name, BSCNEAZR is a cert-oriented track, degree-only is the right call), Cisco Certified → D114 (degree-only), Cisco Cybersecurity → D414 (degree-only), Cisco DevNet → D416 (degree-only). The AWS capstone/environment/platform strings for BSCNEAWS should be reviewed and most likely suppressed.

---

### Multi-description / multi-competency variant policy

Signal presence: 74 courses have multiple description variants; 185 have multiple competency variants.

Why it's incomplete: The enrichment candidates file stores all variants. No policy has been established for which variant to surface on a course page or in a degree AoS block.

What would recover it: A policy decision (documented in PHASE_D or a new policy doc). Likely approach: for course pages, use the most-common description variant; for degree AoS blocks, use the description from this specific program's guide. This is a design decision, not additional extraction.

**Assessment:** Missing policy only. Data is complete.

---

### SP CU conflicts (41 cases)

Signal presence: 41 courses where the SP credit unit value in one guide differs from the SP CU value in another guide. The enrichment summary reports `sp_cus_conflict_count: 41`.

Why it's incomplete: When the same course appears in multiple program SPs, its CU assignment is sometimes different across programs. This may reflect actual CU variation by program context, or it may reflect guide authoring inconsistency. No resolution policy exists.

What would recover it: A policy decision: defer to the catalog CU value as the display value; show guide SP CU only when it matches the catalog. Or: surface the conflict as a note ("CU count may vary by program").

**Assessment:** 41 CU conflicts. Likely resolved by "prefer catalog CU value" policy, which avoids surfacing potentially stale guide data.

---

### Family declarations missing for BSCNE and MSMK

Signal presence: BSCNE family and MSMK family are in sp_families.json with `declaration_text: null` — no explicit family declaration text was extractable from any member program's program_description.

Why it's incomplete: BSCNE family is inferred from code prefix structure (BSCNE*) and shared course intersection, not from a single guide declaring the family. MSMK family similarly has no explicit declaration text recovered.

What would recover it: These two families are correctly identified — the inferred relationship is real. What's missing is the declaration text that would serve as a quote or evidence. For Atlas display, the family relationship is still surfable; just don't quote a "declaration" that doesn't exist. Mark these families as `inferred` rather than `declared`.

**Assessment:** Family membership is correct. Declaration text is legitimately unavailable for these two families. Atlas display should not imply a guide-declared family relationship for BSCNE and MSMK.

---

### MEDETID partial capstone (ANOM-007)

Signal presence: MEDETID (M.Ed., Education Technology and Instructional Design) has 3 capstone courses. The parser captures only the first.

Why it's incomplete: Multi-capstone structural format not handled by the current parser. The parser's capstone extraction logic captures the first capstone trigger it finds.

What would recover it: A targeted parser fix for MEDETID — add a multi-capstone extraction mode for this program. Or: manual annotation of all 3 capstone course codes, hardcoded into the anomaly handling layer.

**Assessment:** MEDETID capstone is currently partial (ANOM-007). Suppress or label with `partial: true` until resolved.

---

### Guide-vs-catalog title divergence (1 case)

Signal presence: C173 has two guide titles across programs ("Scripting and Programming - Foundations" and "Scripting and Programming Foundations" — with and without the dash). Resolved as a single course; both titles match to the same code.

Why it's incomplete: The enrichment summary notes `guide_title_variant_distribution: {1: 750, 2: 1}` — one course has two distinct guide titles. This is a cosmetic title inconsistency, not a content difference.

What would recover it: No action needed. The course is already resolved to a single code. Atlas should display the canonical course title from the catalog, not the guide title.

**Assessment:** Not a real gap. Handled correctly in the bridge.

---

### Missing program families — education sub-families not grouped

Signal presence: The 19-member education family group (standard_bs with 4 programs, education_ba with 11, teaching_mat with 9, etc.) likely contains sibling relationships not yet captured as named families.

Why it's incomplete: The education licensure programs share content-area patterns (e.g., BAESSESC and MATSESC and BAESSESC are all Secondary Chemistry programs at different degree levels). These cross-degree-level sibling relationships are not captured in sp_families.json.

What would recover it: A content-area family grouping pass for education programs — group by subject area (Secondary Chemistry, Secondary Physics, Special Education, etc.) across degree levels. This is a separate analysis from the track/specialization families already captured.

**Assessment:** Not in current artifacts. Education content-area families would require a separate design and extraction pass. Low priority compared to degree-page implementation.

---

## Section 6: Merge-to-Product Planning Bridge

### What currently exists in Atlas product surfaces

**Degree page data (current)**
- `public/data/programs.json`: core program records (codes, names, status, school/college, editions metadata)
- `public/data/program_enriched.json`: descriptions, rosters (grouped by term), learning outcomes
- `public/data/official_resource_placements.json`: curated official resource attachments

The degree page currently shows: program name, official description, grouped course roster (by term, from catalog data), learning outcomes, official resources. No guide-derived content is present.

**Course page data (current)**
- `public/data/courses/{code}.json`: 838 individual course detail files (active AP courses)
- `data/canonical_courses.json`: canonical fallback for all codes
- `public/data/course_descriptions.json`: existing course description layer

The course page currently shows: course name, code, CU value, catalog description, related programs. No guide-derived cert badges, prereq chains, or enriched descriptions are present.

---

### Potential merges and what each requires

**1. SP term structure to degree pages (degree-first)**
- What it is: Adding guide-derived term grouping to the degree page course roster. Currently, the roster is grouped by term from catalog data — but the guide's Standard Path is the authoritative source for the intended term sequence.
- Additive vs. conflicting: Potentially conflicting. The catalog roster and the guide SP may differ in term assignments or course inclusion. Need to define whose term grouping wins.
- What's needed: Reconcile catalog roster terms vs. guide SP terms for each of the 72 Category A programs. Decide display policy. Build this into `build_guide_artifacts.py`.

**2. AoS course descriptions to degree pages (degree-first)**
- What it is: Adding guide-derived descriptions and competency bullets to each course in the degree's AoS block. This is the richest new content available.
- Additive vs. conflicting: Additive. The degree page currently shows course names in the roster but no per-course description. Guide descriptions fill a real gap.
- What's needed: Build `build_guide_artifacts.py` to emit per-course descriptions + bullets for each degree. Define which variant to use for courses with multiple description variants. Wire to degree page AoS block.

**3. Cert badge block to degree pages (degree-first)**
- What it is: A cert prep signal block on the degree page showing which certs the program's courses prepare for.
- Additive vs. conflicting: Additive. No cert layer currently exists on degree pages.
- What's needed: Cert derivation logic (cert → course → program transitivity). Implement the 9 auto-accepted rows. Design the cert block UI component. Policy decision on which cert recommendation types to show at degree level.

**4. Family relationship panel to degree pages (degree-first)**
- What it is: A panel on track-member degree pages linking to sibling programs, showing shared course count and track distinctions.
- Additive vs. conflicting: Additive. No family relationship display currently exists on degree pages.
- What's needed: The sp_families.json data is ready. Need a family panel UI component. Need to define what the panel shows (links to siblings, shared course count, track label, divergence description).

**5. Guide provenance badge to degree pages (degree-first)**
- What it is: A small provenance label on the degree page indicating that guide content is sourced from the WGU Program Guidebook, including version and pub_date.
- Additive vs. conflicting: Additive.
- What's needed: Badge component. Data comes from parsed guide metadata (version, pub_date) already in the parsed JSONs and manifest_rows. Handle BSNU exception (no metadata).

**6. Prereq badges to course pages (course-page work, later)**
- What it is: Prereq relationship display on course pages. "This course requires: X." "This course is a prerequisite for: Y."
- Additive vs. conflicting: Additive. No prereq layer currently exists on course pages.
- What's needed: Policy on display (all 50 auto-accepted rows? Only highest-confidence? Show nursing sequences differently?). UI component for prereq badge. Integrate prereq_relationships.json into course page data flow.

**7. Cert badges to course pages (course-page work, later)**
- What it is: Cert prep badge on individual course pages. "This course helps prepare for CompTIA A+."
- Additive vs. conflicting: Additive.
- What's needed: The 9 auto-accepted cert mappings are ready. UI component. Policy on display (only auto-accepted? Include review-needed rows with caveats?).

**8. Guide-derived descriptions to course pages (course-page work, later)**
- What it is: Replacing or supplementing the existing catalog description with the guide-derived description.
- Additive vs. conflicting: Potentially conflicting. Catalog descriptions already exist in `course_descriptions.json`. Need a policy on which source is primary and whether to show both.
- What's needed: Policy decision on source priority. UI integration. Variant selection policy for multi-description courses.

**9. SP advisor-guided label for Category B programs (degree-first)**
- What it is: Adding the "Advisor-sequenced — individual pacing varies" label to the 23 null-term education/licensure programs.
- Additive vs. conflicting: Additive.
- What's needed: Category B identification from sp_family_classification.json. Label component on degree page. Trivial once artifact generator is built.

---

## Section 7: Concrete Examples

### BSCNE — cert-heavy, vendor-track degree

BSCNE (B.S. Cloud and Network Engineering, Vendor-Agnostic track) is the clearest cert-prep degree in the corpus. From the guide data:

- Cert prep: CompTIA A+ (via IT Applications C394 and IT Foundations C393), CompTIA Network+ (via Networks C480), CompTIA Security+ (via Network and Security - Applications C178), CompTIA Cloud+ (via Cloud Applications C923). All 4 certs are auto-accepted, high confidence, confirmed across 3–7 programs.
- SP: Category A (structured-term, 72 programs in this category). Full SP display with term grouping.
- Family: Member of the BSCNE family (4 vendor tracks). 26 shared courses with BSCNEAWS, BSCNEAZR, BSCNECIS.
- Family panel: "Part of B.S. Cloud and Network Engineering family. Other tracks: AWS (BSCNEAWS), Azure (BSCNEAZR), Cisco (BSCNECIS). Shares 26 core courses with all tracks."

What Atlas can show today on BSCNE degree page: full guide AoS content, cert badge block (4 certs ready), family panel (4 members, 26 shared courses), structured term SP. Requires only the artifact generator to be built.

---

### BAELED — null-term licensure degree

BAELED (B.A., Elementary Education — licensure variant) is the archetypal null-term program.

- SP: Category B (null-term). All SP courses have `term: null`. The SP exists but has no term structure — it is an ordered course list, not a term sequence.
- Family: Member of BAELED family. 33 shared courses with BAESELED (the non-licensure variant).
- AoS content: Fully intact. Descriptions and competency bullets available for AoS courses.
- Cert signals: None (no cert prep mentions in BAELED guide). This is expected — education licensure programs prepare for Praxis exams, not in courses but at program level.

What Atlas shows: AoS descriptions and competency bullets (ready). Ordered course list with label "Advisor-sequenced — individual pacing varies" (ready). Family panel linking to BAESELED with "Licensure pathway" label (ready). No cert badge block for this program.

---

### BSSWE Java vs. C# — track specialization

BSSWE_Java and BSSWE_C are the two tracks of the B.S. Software Engineering family.

- 33 shared courses across the same terms. The shared core covers programming foundations, data structures, algorithms, web development, software design, and general education.
- Diverging courses: Language-specific courses in later terms (Java-specific or C#-specific implementations).
- SP: Both are Category C (track-specialization-member). Each has a complete, populated SP for its specific track.
- Declaration: "offered in two tracks that utilize either Java or C# to achieve similar objectives" (from BSSWE_C program_description).

What Atlas shows on BSSWE_Java: Full SP for the Java track. Family panel: "Part of B.S. Software Engineering. Also offered as C# track (BSSWE_C). Shares 33 courses with the C# track." For shared courses: single description is accurate for both tracks. For track-specific courses: description from the Java guide.

---

### BSCS — capstone-rich with prereq chain

BSCS (B.S. Computer Science) has the richest prereq chain in the corpus.

- Prereq chain (all auto-accepted, high confidence): Applied Algebra → Discrete Math I; Calculus I → Discrete Math I; Calculus I → Calculus II; Calculus II → Calculus III; Discrete Math I → Discrete Math II; Data Management - Foundations → Data Management - Applications; Introduction to Python → Back-End Programming.
- Capstone: C964 (Computer Science Capstone) — identified in the capstone section.
- SP: Category A, clean term structure. ~30 courses.
- Cert signals: None specific to BSCS (CS is not a cert-prep program).

What Atlas shows: Full term-grouped SP. AoS descriptions + competency bullets. Prereq chain display on each prereq-bearing course page. Capstone callout. No cert badge block needed.

---

### C176 — prereq-bearing, cert-mapped course appearing in many programs

C176 (Business of IT - Project Management) maps to CompTIA Project+ and appears in 6 programs (BSCSIA, BSDA, BSIT, BSSWE_C, BSSWE_Java, MSSWEUG).

- Cert: CompTIA Project+ (auto-accepted, high confidence, source_program_count: 6)
- Programs: 6 programs include this course in their SPs.
- Description variants: Likely 1 or 2 (very stable course definition across IT/SWE programs).

What Atlas shows on the C176 course page: Guide description. Competency bullets. Cert badge: "Helps prepare for CompTIA Project+." Program context: "Appears in 6 programs including B.S. IT, B.S. Software Engineering (Java), B.S. Cybersecurity and Information Assurance, and others."

---

### D426 → C170 — prereq chain anchor (multi-program)

D426 (Data Management - Foundations) is a prerequisite for C170 (Data Management - Applications) in 8 programs (BSCS, BSDA, BSIT, BSSWE_C, BSSWE_Java, MSCSUG, MSITUG, MSSWEUG). This is the most cross-program-confirmed prereq relationship in the corpus.

What Atlas shows on C170 course page: "Requires: Data Management - Foundations (D426)." This relationship is clean enough (8 programs, auto-accepted, catalog_title_match) that no caveats are needed.

What Atlas shows on D426 course page: "This course is a prerequisite for: Data Management - Applications (C170)." Optionally: Advanced Data Management (D191) — 4 programs.

---

### MATSPED — anomaly case

MATSPED (M.A.T., Special Education) has a catastrophic SP extraction failure (ANOM-001). The SP entry at term 7 contains 1,122 characters — over 20 course titles concatenated into a single string.

- SP handling: Suppress SP display entirely. Category D in sp_family_classification.json.
- AoS content: Intact. Descriptions and competency bullets available.
- Anomaly record: ANOM-001 in guide_anomaly_registry.json. WGU feedback candidate: yes (source PDF has non-standard table layout).
- SP category: D (anomalous-suppress).

What Atlas shows: AoS content block with descriptions and competency bullets. No Standard Path display. Provenance note: "Standard Path display not available for this program due to a guide format limitation." No need to expose the underlying extraction issue to students.

---

## Quick reference: artifact locations

| Need | File |
|---|---|
| Cert → course mappings (9 auto-accepted + 21 review) | `data/program_guides/cert_course_mapping.json` |
| Prereq relationships (50 auto-accepted + 21 review) | `data/program_guides/prereq_relationships.json` |
| SP classification for all 115 programs | `data/program_guides/sp_family_classification.json` |
| Family definitions (7 families, member lists, shared counts) | `data/program_guides/sp_families.json` |
| Anomaly handling rules (9 records) | `data/program_guides/guide_anomaly_registry.json` |
| Course enrichment (751 courses, descriptions, bullets) | `data/program_guides/enrichment/course_enrichment_candidates.json` |
| Enrichment coverage summary | `data/program_guides/enrichment/course_enrichment_summary.json` |
| Parsed guides (115 programs, full guide content) | `data/program_guides/parsed/*_parsed.json` |
| Course matching audit (final state) | `data/program_guides/bridge/merge_summary.json` |
| Degree-enrichment artifact generator design | `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` |
| Corpus facts (canonical counts, confidence) | `data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md` |
| What claims are safe to make | `data/program_guides/audit/program_guide_claims_register.md` |
