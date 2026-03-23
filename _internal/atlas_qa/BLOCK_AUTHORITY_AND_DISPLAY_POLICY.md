# Block Authority and Display Policy

**Version:** 1.0
**Date:** 2026-03-23
**Status:** Active — primary policy artifact for course-page and program-page implementation
**Grounded in:** SOURCE_COVERAGE_MATRIX, COURSE_TEXT_COMPARISON_INDEX, PROGRAM_TEXT_COMPARISON_INDEX, COURSE_TEXT_COMPARISON_BATCHES 1–4 (all annotated; Batches 2–4 re-annotated via strong-model pass 2026-03-23)

---

## 1. Scope and Purpose

This document defines, block by block:
- Which source family is authoritative for each user-facing content block
- How overlap between sources is resolved for display
- When alternate sources are surfaced, suppressed, or disclosed
- How multi-variant cases are handled
- What Atlas QA should use as its default answer source per block

This is not a technical spec. It does not define data models, API shapes, or rendering details. It defines the policy that governs those choices.

**Block families covered:**
- Course blocks: description/overview, guide description variants, competency bullets, cert signal, prerequisites, reverse prerequisites, capstone callout, course identity facts, history/appearances
- Program blocks: description, identity facts, total CU, course roster, Areas of Study, capstone, program learning outcomes, licensure notes, certification notes, history/edition context

---

## 2. Policy Principles

**P1 — Field authority is determined per block, not per source family.**
No single source family is authoritative for everything. CAT owns identity and PLOs. GUIDE owns competencies and AoS. For description text, evidence determines the authority decision.

**P2 — Catalog is the default authority for description text where both sources exist.**
For course overviews: 78% of paired courses have identical or near-identical catalog and guide text. In the material-difference cases, the catalog tends to carry more complete, more current text (evidence: BSHR cluster rewrite, CNE locked-text cases, D560 truncation). Guide description text is treated as an alternate that is stored but not displayed by default.

**P3 — The guide prefix artifact does not constitute a genuine program description difference.**
63 of 65 STRONG program mat-diff rows are explained entirely by the guide prepending a metadata header (`Program Code / Catalog Version / Published Date`). Strip-normalized, the body texts are identical. These are not display authority conflicts — catalog text is the display copy.

**P4 — GUIDE is authoritative for guide-only blocks.**
Competency bullets, cert signals, Areas of Study, and capstone content exist only in GUIDE (no catalog overlap). There is no authority question for these blocks — GUIDE is the only source.

**P5 — CANON is authoritative for identity facts.**
Course codes, titles, CU values, program codes, and canonical status come from CANON. These override both CAT and GUIDE for identity resolution purposes. CU conflicts between guide SP sums and catalog totals are resolved in favor of CAT (see OV-5, OV-6).

**P6 — Version must be disclosed when relevant to the answer.**
Source version is tracked independently per source family. QA answers that draw on text content must cite the source version. Mixed-version retrieval is forbidden by the system design; version mismatches are flagged explicitly rather than silently blended.

---

## 3. Course Block Authority and Display Policy

### 3.1 Course Overview / Description

| Field | Value |
|---|---|
| **Block name** | Course overview / description |
| **Source families available** | CAT-TEXT (catalog description), ENRICH (guide description) |
| **Default / authoritative source** | CAT-TEXT |
| **Alternate-source behavior** | ENRICH description is stored in the canonical course object as `description_guide`. It is not displayed by default. It is available to QA for synthesis if needed. |
| **Suppression rule** | When CAT-TEXT and ENRICH are exact or near-duplicate (diff ≤ 5), the ENRICH copy is fully suppressed — no disclosure needed. When materially different, ENRICH is retained internally but not displayed unless explicitly requested. |
| **Variant rule** | When a course has multiple guide description variants (74 courses; see §5), CAT-TEXT remains the display default. Guide variants are keyed by source program and stored per-variant. |
| **QA default answer source** | CAT-TEXT. If CAT-TEXT is absent and ENRICH exists, ENRICH is used with source disclosure. |
| **Review trigger** | Courses where `llm_review_flag: yes` in the completed annotation pass (~25 rows across Batches 2–3). Primary clusters: BSPRN clinical nursing courses (guide adds clinical assessment/diagnosis/management structure catalog lacks), BSHR pre-rewrite content delta, MSHRM program-degree-specific framing, select FNP/PMHNP variants. Anomaly flags requiring data inspection before canonical object construction: C179 (catalog text 293 chars — suspiciously short, guide adds routing/switching/automation detail — see §8.9) and D554 (guide text appears to be from a different course — see §8.10). |
| **Rationale** | Catalog descriptions are current-edition text. Guide descriptions are often locked to an older authoring event (BSHR cluster, CNE cluster) or are program-family-specific variants. 78% of paired courses are identical anyway. For the 103 mat-diff courses, no row across the full corpus produced a clear guide preference — catalog-default is confirmed safe. BSPRN-cluster guide text adds genuine clinical framing value and should be stored as labeled program-context alternates. |

---

### 3.2 Guide Description Variants

| Field | Value |
|---|---|
| **Block name** | Guide description variants (program-family-specific) |
| **Source families available** | ENRICH only (74 courses have 2–4 variants, each keyed to one or more source programs) |
| **Default / authoritative source** | Not displayed. Variants are stored per-program-family, keyed by source program code(s). |
| **Alternate-source behavior** | If a user's question is explicitly scoped to a specific program (e.g., "how does BSHR describe this course"), the program-family variant is the appropriate cite. |
| **Suppression rule** | All guide variants are suppressed from default display. CAT-TEXT is the display copy. |
| **Variant rule** | When program context is known, the matching guide variant is preferred for guide-sourced answers. When program context is unknown, the first or most-common variant is used, with a note that program-specific wording may differ. |
| **QA default answer source** | CAT-TEXT unless program context explicitly provided. |
| **Review trigger** | Courses where guide variants conflict with each other in substantive ways (not yet systematically catalogued; flag for future pass). |
| **Rationale** | Guide description variants represent program-specific authoring events, not canonical course definitions. Displaying them by default would be misleading for cross-program course search. |

---

### 3.3 Competency Bullets / What You'll Learn

| Field | Value |
|---|---|
| **Block name** | Competency bullets / what you'll learn |
| **Source families available** | ENRICH (guide) only — no catalog overlap |
| **Default / authoritative source** | ENRICH (guide) — sole source |
| **Alternate-source behavior** | N/A |
| **Suppression rule** | Show when available. If absent for a course, omit the block entirely (do not show empty). |
| **Variant rule** | 185 courses have 2–6 competency variants keyed to source programs. When program context is known, use the matching variant. When unknown, use the most-common variant (by source program count). Flag multi-variant cases in the canonical object so QA can disclose the variant count if queried. |
| **QA default answer source** | ENRICH. When queried without program context and variants exist, answer with the most-common variant and disclose: "This course appears in multiple programs; competencies may vary slightly by program." |
| **Review trigger** | Courses where competency variants are substantively different across programs (not just cosmetically different). Not yet systematically catalogued. |
| **Rationale** | Guide-only field. No authority question exists. |

---

### 3.4 Cert Prep / Cert Signal

| Field | Value |
|---|---|
| **Block name** | Cert prep / certification signal |
| **Source families available** | ENRICH (guide) only |
| **Default / authoritative source** | ENRICH (guide) — sole source |
| **Alternate-source behavior** | N/A |
| **Suppression rule** | Show only when present. Do not infer cert prep status from course title or description. |
| **Variant rule** | If cert signal differs across guide variants for the same course, surface all distinct cert signals with their source programs. Do not collapse conflicting signals. |
| **QA default answer source** | ENRICH. If absent, answer: "No certification preparation signal is present for this course in available sources." |
| **Review trigger** | Courses where cert signal appears in one program's guide but not another's (potential program-specific cert prep relationship). |
| **Rationale** | Guide-only field. No authority question. |

---

### 3.5 Prerequisites

| Field | Value |
|---|---|
| **Block name** | Prerequisites |
| **Source families available** | CANON (canonical prereq relationships), CAT (if prereq text appears in catalog description) |
| **Default / authoritative source** | CANON for structured prereq relationships. CAT-TEXT prereq mentions are informal and should not be parsed as structured data. |
| **Alternate-source behavior** | Guide prereq mentions (if any) are not treated as authoritative — guide prereq information may be program-path-specific and is not a canonical constraint. |
| **Suppression rule** | If CANON has no prereq record, do not assert absence of prerequisites without confirming the field is populated for that course. Abstain on completeness claims. |
| **Variant rule** | N/A for structured prereqs. |
| **QA default answer source** | CANON. |
| **Review trigger** | Cases where catalog description mentions a prereq that conflicts with or is absent from CANON. |
| **Rationale** | Prereqs are identity/policy data, not description text. CANON is the resolution source for identity fields. |

---

### 3.6 Reverse Prerequisites (Course Unlocks)

| Field | Value |
|---|---|
| **Block name** | Reverse prerequisites ("this course is required before…") |
| **Source families available** | Derivable from CANON prereq graph |
| **Default / authoritative source** | CANON (derived, not stored as a direct field) |
| **Alternate-source behavior** | N/A |
| **Suppression rule** | Only show when the CANON graph contains the relationship. Do not infer from description text. |
| **Variant rule** | N/A |
| **QA default answer source** | CANON-derived. Abstain on negative claims ("this course has no dependents") unless completeness is confirmed. |
| **Review trigger** | N/A |
| **Rationale** | Derived structural field. |

---

### 3.7 Capstone Callout

| Field | Value |
|---|---|
| **Block name** | Capstone callout / designation |
| **Source families available** | ENRICH (guide) — capstone section parsed from guide PDFs |
| **Default / authoritative source** | ENRICH (guide) — sole source with structured capstone designation |
| **Alternate-source behavior** | N/A |
| **Suppression rule** | Show only when present. Do not infer capstone status from title or description. |
| **Variant rule** | Capstone designation is program-specific — a course may be a capstone in one program and not in another. Always disclose the program context for capstone claims. |
| **QA default answer source** | ENRICH, always scoped to program context. Never assert "X is a capstone course" without specifying the program. |
| **Review trigger** | Cases where a course is designated capstone in some programs and not others (should be the normal case; just requires proper scoping). |
| **Rationale** | Guide-only field. Program-scoped by nature. |

---

### 3.8 CU / Title / Course Identity Facts

| Field | Value |
|---|---|
| **Block name** | Credit units, course title, course code, canonical status |
| **Source families available** | CANON (primary), CAT (secondary confirmation), GUIDE (has CU values per SP but conflicts with CANON in 41 courses) |
| **Default / authoritative source** | CANON for all identity fields. CAT for CU when CANON is absent. GUIDE CU is not authoritative (OV-5: 41 courses have guide-internal CU conflicts). |
| **Alternate-source behavior** | If CAT CU disagrees with CANON CU, flag for review. Do not surface the conflict to users without resolution. |
| **Suppression rule** | N/A for identity facts — always display. |
| **Variant rule** | N/A |
| **QA default answer source** | CANON. |
| **Review trigger** | OV-5 courses (41 with guide-internal CU conflicts). These are not yet individually catalogued. |
| **Rationale** | Identity is a single-authority domain. CANON exists precisely to resolve cross-source identity conflicts. |

---

### 3.9 History / Appearances / Aliases

| Field | Value |
|---|---|
| **Block name** | Program appearances, course aliases, retired status |
| **Source families available** | GUIDE (which programs a course appears in), CANON (canonical status), CAT (edition in which course appeared) |
| **Default / authoritative source** | CANON for status. GUIDE for program-appearance membership. CAT for catalog-edition presence. |
| **Alternate-source behavior** | N/A — these are non-overlapping sub-fields. |
| **Suppression rule** | Retired/inactive courses: surface status clearly. Do not suppress program-appearance data for inactive courses — it has historical research value. |
| **Variant rule** | N/A |
| **QA default answer source** | CANON for status. GUIDE for "which programs include this course." CAT for "was this course in the [year] catalog." |
| **Review trigger** | N/A |
| **Rationale** | Each sub-field has a natural owner. |

---

## 4. Program Block Authority and Display Policy

### 4.1 Program Description

| Field | Value |
|---|---|
| **Block name** | Program description / overview |
| **Source families available** | CAT-TEXT (catalog PDF extraction, field `description`), GUIDE (`program_description` field with prefix artifact) |
| **Default / authoritative source** | CAT-TEXT |
| **Alternate-source behavior** | GUIDE `program_description` is stored but not displayed. For 63 of 65 STRONG mat-diff programs, the guide body text is identical to catalog text after stripping the guide metadata prefix (`Program Code / Catalog Version / Published Date`). No display conflict exists for these cases. |
| **Suppression rule** | GUIDE program description is suppressed from display in all cases where CAT-TEXT is available. The prefix pattern makes GUIDE text misleading without stripping, and stripping is unnecessary when CAT-TEXT already provides the clean version. |
| **Variant rule** | N/A — one description per program per catalog edition. |
| **QA default answer source** | CAT-TEXT. Version: WGU Catalog 2026-03 (current). |
| **Review trigger** | MATSPED (guide text is abridged, ~1401 chars vs catalog 2051 chars — genuine truncation; catalog is more complete and authoritative). BAESSPMM (guide has additional sentence(s) not in catalog — catalog is still the display source, but QA should not assert the guide sentences are absent from the course; file for future review). |
| **Rationale** | Catalog text is clean, current, and strip-normalized identical to guide body in 97% of cases. Prefix artifact in guide makes guide text unsuitable as a display source without additional processing. Two genuine differences resolved in favor of catalog completeness. |

---

### 4.2 Degree Title / Program Identity Facts

| Field | Value |
|---|---|
| **Block name** | Degree title, program code, program type (bachelor's / master's / etc.), college/school |
| **Source families available** | CAT (authoritative), CANON (cross-reference), GUIDE (confirming) |
| **Default / authoritative source** | CAT |
| **Alternate-source behavior** | GUIDE program code / title is used for cross-reference only. Conflicts between CAT and GUIDE identity fields are flagged, not auto-resolved. |
| **Suppression rule** | N/A |
| **Variant rule** | N/A |
| **QA default answer source** | CAT |
| **Review trigger** | Any case where GUIDE program code or title differs from CAT. Not systematically catalogued; currently no known instances. |
| **Rationale** | Identity is CAT-authoritative. |

---

### 4.3 Total CU

| Field | Value |
|---|---|
| **Block name** | Program total credit units |
| **Source families available** | CAT (explicit total), GUIDE (derivable from SP sum — unreliable) |
| **Default / authoritative source** | CAT |
| **Alternate-source behavior** | GUIDE-derived SP sum is not used as authoritative. |
| **Suppression rule** | N/A |
| **Variant rule** | N/A |
| **QA default answer source** | CAT. If queried about discrepancy between guide SP sum and catalog total: cite CAT as authoritative and note that guide SP sums may include elective placeholders or optional paths. |
| **Review trigger** | OV-6: 7 programs with CAT total vs guide SP sum discrepancy >1 CU. Not yet individually catalogued. |
| **Rationale** | CAT explicitly states the program's required total CU. Guide SP sums may reflect one pathway through an elective structure, not the program total. |

---

### 4.4 Course Roster / Standard Path

| Field | Value |
|---|---|
| **Block name** | Course roster — which courses are required, elective, or part of a program path |
| **Source families available** | GUIDE (`standard_path` sections), CAT (degree plan tables, not always machine-parseable) |
| **Default / authoritative source** | GUIDE `standard_path` for structured course membership. CAT for official policy (accreditation-level requirements). |
| **Alternate-source behavior** | CAT course roster data (where parseable) is a cross-reference, not a display replacement. |
| **Suppression rule** | Do not surface GUIDE course roster as "complete program requirements" — it reflects the guide's SP layout, which may be one path through an elective structure. Always qualify: "as listed in the [program code] program guide." |
| **Variant rule** | Programs with AoS branching: GUIDE contains distinct SP rows per AoS or specialty. Roster queries should be scoped to the specific path unless user is asking about the whole program. |
| **QA default answer source** | GUIDE `standard_path`. Scoped to the specific guide version. |
| **Review trigger** | Cases where GUIDE SP lists a course not found in CANON (retired course, alias, error). |
| **Rationale** | GUIDE is the only machine-parseable source for structured course membership. CAT roster data is typically rendered in PDF tables that require significant extraction work. |

---

### 4.5 Areas of Study

| Field | Value |
|---|---|
| **Block name** | Areas of Study (specialization tracks / emphases) |
| **Source families available** | GUIDE only |
| **Default / authoritative source** | GUIDE — sole source |
| **Alternate-source behavior** | N/A |
| **Suppression rule** | Show only when AoS data is present for that program. Do not infer AoS structure from program title. |
| **Variant rule** | Each AoS is a named section in the guide with its own course list. Display as distinct sections. |
| **QA default answer source** | GUIDE. |
| **Review trigger** | N/A |
| **Rationale** | Guide-only field. |

---

### 4.6 Capstone

| Field | Value |
|---|---|
| **Block name** | Program capstone course and requirements |
| **Source families available** | GUIDE (capstone section) |
| **Default / authoritative source** | GUIDE — sole source |
| **Alternate-source behavior** | N/A |
| **Suppression rule** | Show only when capstone data is present. |
| **Variant rule** | N/A |
| **QA default answer source** | GUIDE. |
| **Review trigger** | N/A |
| **Rationale** | Guide-only field. |

---

### 4.7 Program Learning Outcomes (PLOs)

| Field | Value |
|---|---|
| **Block name** | Program learning outcomes |
| **Source families available** | CAT-TEXT only — confirmed that guides do NOT contain PLOs |
| **Default / authoritative source** | CAT-TEXT — sole source |
| **Alternate-source behavior** | N/A |
| **Suppression rule** | If PLOs are absent from CAT-TEXT for a program, do not assert or infer PLOs. Abstain. |
| **Variant rule** | N/A |
| **QA default answer source** | CAT-TEXT. |
| **Review trigger** | N/A |
| **Rationale** | CAT-only field. Confirmed in SOURCE_COVERAGE_MATRIX pass. |

---

### 4.8 Licensure Notes

| Field | Value |
|---|---|
| **Block name** | Licensure preparation or disclosure notes |
| **Source families available** | CAT-TEXT (program descriptions sometimes mention licensure); GUIDE (may mention licensure context in description or SP notes) |
| **Default / authoritative source** | CAT-TEXT for any official licensure disclosure language. |
| **Alternate-source behavior** | GUIDE licensure mentions are supplemental context, not policy statements. |
| **Suppression rule** | Do not surface GUIDE licensure language as a policy claim. |
| **Variant rule** | N/A |
| **QA default answer source** | CAT-TEXT. Abstain on specifics not present in CAT-TEXT. |
| **Review trigger** | Any GUIDE licensure claim that contradicts or extends beyond what CAT-TEXT says. |
| **Rationale** | Licensure implications have legal/policy weight. Catalog language is the authoritative statement. |

---

### 4.9 Certification Notes

| Field | Value |
|---|---|
| **Block name** | Program-level certification alignment notes |
| **Source families available** | ENRICH/GUIDE (cert signals parsed from guide content) |
| **Default / authoritative source** | GUIDE — primary source for cert signals at both program and course level |
| **Alternate-source behavior** | N/A |
| **Suppression rule** | Show only when cert signal is explicit in source. Do not infer. |
| **Variant rule** | N/A |
| **QA default answer source** | GUIDE. Cite specific source program guide and version. |
| **Review trigger** | Cert signals that conflict across guide versions for the same program. |
| **Rationale** | GUIDE contains structured cert prep signals extracted from guide content. |

---

### 4.10 History / Edition Context

| Field | Value |
|---|---|
| **Block name** | Program edition, catalog version, guide version, publication history |
| **Source families available** | CAT (catalog version token), GUIDE (guide version token) |
| **Default / authoritative source** | Each source tracks its own version independently. Version tokens are not merged. |
| **Alternate-source behavior** | N/A — version tracking is per-source-family |
| **Suppression rule** | N/A |
| **Variant rule** | N/A |
| **QA default answer source** | Cite both version tokens when relevant. |
| **Review trigger** | OV-7: 5 programs with cat/guide version mismatch. MACCA/MACCF/MACCM/MACCT (cat=202412, guide=202409; catalog 3 months newer). MSHRM (cat=202311, guide=202507; guide 8 months newer — most acute case). QA must not blend content from these without disclosing the version gap. |
| **Rationale** | Version disclosures are an architecture invariant in the QA system design. |

---

## 5. Variant Handling Policy

### 5.1 Course Description Variants (Guide)

- 74 courses have 2–4 guide description variants, each tied to one or more source program codes.
- **Display rule:** CAT-TEXT is displayed; all guide variants are stored but not displayed.
- **QA rule:** When program context is supplied, prefer the guide variant matching that program's code. When program context is absent, use CAT-TEXT for the description answer.
- **Conflict rule:** If guide variants conflict with each other substantively (not just cosmetically), note the conflict exists in a `variant_conflict` flag on the canonical course object. Do not silently blend.

### 5.2 Competency Bullet Variants

- 185 courses have 2–6 competency variants per program source.
- **Display rule:** Show the variant matching the user's current program context. If no context, show the most-common variant (by source program count).
- **QA rule:** Same as display. Disclose multi-variant status when variant count > 1.
- **Conflict rule:** Competency variants are expected to differ slightly by program family — this is a feature, not an error. Only flag as a conflict if the variants appear to describe fundamentally different learning outcomes.

### 5.3 Exact / Near-Duplicate Variant Handling

- When a course has both an exact-match variant and a mat-diff variant (e.g., D312: v1/2 exact, v2/2 near-dup; appears in both §5A and §5B of the comparison index), the catalog description is authoritative for display regardless. The variant classification affects internal QA indexing only.
- Near-duplicate variants (diff ≤ 5) are treated as equivalent to exact for display and QA purposes.

---

## 6. Version / Conflict Handling Notes

### 6.1 Confirmed Version Conflicts (Program Level)

| Program(s) | cat_version | guide_version | Gap | Implication |
|---|---|---|---|---|
| MACCA, MACCF, MACCM, MACCT | 202412 | 202409 | Catalog 3 months newer | Catalog is more current. Use CAT-TEXT for description. Note guide version in QA cite. |
| MSHRM | 202311 | 202507 | Guide 8 months newer | Guide may reflect program updates not yet in catalog extract. Body text is identical after prefix strip, but freshness gap is acute. QA must disclose: catalog version is 2023-11; guide version is 2025-07. Do not assert catalog is current for this program without verification. |

### 6.2 Course-Level Version Tracking

- Course descriptions are sourced from the 2026-03 catalog (CAT-TEXT) and from guide PDFs whose version varies by source program.
- A course's guide description version is not a single value — it is the version of the guide(s) from which that description was extracted.
- For QA answers, cite: "Source: WGU Catalog 2026-03" for CAT-TEXT descriptions. For GUIDE descriptions, cite the relevant guide program and version.

### 6.3 Mixed-Version Retrieval Prohibition

Per the architecture invariants in LOCAL_8B_RAG_SYSTEM_DESIGN.md:
- Mixed-version context is forbidden unless query intent is explicit comparison.
- For version-conflicted programs (MACCA etc.), do not blend catalog and guide content in the same answer without explicit version disclosure.
- MSHRM is the most acute case: guide is 8 months newer. If a student asks about MSHRM requirements, the guide is likely more current — but QA should cite the guide version explicitly and note the catalog version gap.

---

## 7. QA Default-Answer Policy by Block

| Block | QA Default Source | Abstain Condition | Version Cite Required |
|---|---|---|---|
| Course description / overview | CAT-TEXT (WGU Catalog 2026-03) | No CAT-TEXT and no ENRICH | Yes |
| Course competency bullets | ENRICH (guide), most-common variant | Not present in ENRICH | Yes (guide program + version) |
| Cert signal | ENRICH (guide) | Not present | Yes |
| Prerequisites | CANON | Field not populated | No (structural) |
| Reverse prerequisites | CANON-derived | Not derivable | No |
| Capstone callout | ENRICH (guide), program-scoped | Not present for that program | Yes (guide) |
| CU value | CANON, fallback CAT | Not in CANON | No |
| Course title | CANON | — | No |
| Program appearances | ENRICH (guide) | — | Yes (guide) |
| Program description | CAT-TEXT (WGU Catalog 2026-03) | No CAT-TEXT | Yes |
| Program identity (title, code) | CAT | — | No |
| Total CU | CAT | — | No |
| Course roster / SP | GUIDE (standard_path) | No guide SP data | Yes (guide + version) |
| Areas of Study | GUIDE | Not present | Yes |
| Capstone (program) | GUIDE | Not present | Yes |
| PLOs | CAT-TEXT | Not present | Yes |
| Licensure notes | CAT-TEXT | Not present in CAT | Yes |
| Certification notes | GUIDE | Not present | Yes |
| Edition / version info | Per-source token | — | N/A (is the answer itself) |

**General QA rules:**
- Never assert absence ("this course has no prerequisites") without confirmed completeness in the source.
- Always cite the source family and version when providing text-content answers.
- For multi-variant fields (competencies, guide descriptions), disclose variant count if > 1 when it's relevant to the question.
- For version-conflicted programs (MACCA, MACCF, MACCM, MACCT, MSHRM), always cite both version tokens when the answer draws on description content.

---

## 8. Open Issues / Deferred Review Items

### 8.1 Batch Annotation — Resolved

**Resolved.** All 110 rows across Batches 2–4 were annotated via strong-model re-annotation pass (2026-03-23). No row across the full 110-row corpus produced `llm_preference_for_research_tool: guide` as a clear winner. Catalog-default confirmed safe.

**Key findings from batch annotation:**
- **BSHR cluster** (D354–D360): catalog is the modern rewrite; guide is locked to an older pre-rewrite authoring event. Catalog is the display default. Several rows flagged `yes` for the pre-rewrite content delta — candidates for labeled alternate storage, not display overrides.
- **MSHRM cluster** (D432–D436): guide has program-degree-specific framing. Catalog is the correct default; guide text is a useful labeled program-context alternate.
- **BSPRN cluster**: guide consistently adds clinical assessment/diagnosis/management framing that catalog lacks. Strongest case for storing guide text as a labeled alternate for program-context display. No catalog override warranted.
- **CNE cluster** (C172, C175): catalog is longer and more complete; guide is exam-locked. Except C179 — see §8.9.
- **MOD rows** (Batch 4, diff 6–50): majority `either` at diffs ≤25. No display overrides warranted.

**Remaining action (not a blocker):** Human review of ~25 `llm_review_flag: yes` rows before any program-context display alternates are set in canonical course objects. Catalog-default implementation does not require this review to complete first.

### 8.2 D355 — Compensation and Benefits

Flagged `needs_review` in Batch 1. Cat and guide use different framing ("key aspects of building" vs "strategies for building total compensation systems"). Current rule: catalog is displayed. Needs a human judgment call on whether this framing difference is meaningful enough to warrant a disclosure note.

### 8.3 MATSPED Program Description

Guide description is abridged (~1401 vs 2051 catalog chars). Catalog is the more complete version and is the display default. However, QA should not assert the guide text is wrong — it appears to be a legitimate abridgment. No action needed for display policy, but note for QA training: catalog and guide text differ substantively for this program.

### 8.4 BAESSPMM Program Description

Guide has additional sentence(s) not in catalog (diff=109 after prefix strip). Catalog is the display default. The additional guide content is not surfaced. Future review: determine if the guide's additional sentence is accurate supplemental information or a version artifact.

### 8.5 MSHRM Version Freshness

Guide version (202507) is 8 months newer than catalog version (202311). Body text is currently identical after prefix strip — so there is no content difference today. But the gap is the widest in the corpus and is a real freshness risk. Flag for monitoring: if MSHRM content changes in a future guide update, the catalog extract will be stale.

### 8.6 OV-5 and OV-6 CU Conflict Courses Not Individually Catalogued

- OV-5: 41 courses with guide-internal CU conflicts (different programs' guides report different CU). CANON is authoritative; no display issue. But QA answering CU questions from GUIDE context could produce wrong values.
- OV-6: 7 programs with CAT total vs guide SP sum discrepancy >1. CAT is authoritative; same QA risk.
- Both sets need a catalog pass to identify the specific course/program codes and update the canonical objects with explicit `canon_cu_authoritative: true` flags or equivalent.

### 8.7 Competency Variant Conflict Detection Not Done

185 courses with multi-variant competency rows have not been analyzed for substantive vs cosmetic differences. Current policy (most-common variant as default) is a reasonable placeholder. A future pass should identify courses where competency variants are substantively different and flag them for the multi-variant disclosure rule.

### 8.8 Source Coverage Matrix File Not Present

`SOURCE_COVERAGE_MATRIX.md` was created in a prior session per the DEV_LOG but is not present in `_internal/atlas_qa/` as of this session. The policy in this document is grounded in the DEV_LOG record of that artifact's findings. If the file needs to be regenerated, the DEV_LOG entries from 2026-03-23 (SOURCE_COVERAGE_MATRIX session) are the authoritative record of its conclusions.

---

### 8.9 C179 — Advanced Networking Concepts (catalog short-text anomaly)

Catalog text for C179 is 293 chars — unusually short for a networking course and the shortest in the CNE cluster. Guide text is longer and adds routing/switching/automation specifics. This is the only CNE-cluster course where the guide is longer than the catalog; every other CNE course (C172, C175) follows the opposite pattern. Flagged `needs_review + yes` in Batch annotation.

**Required action before canonical object construction:** Verify the catalog extract for C179 is not truncated. If the catalog text is genuinely 293 chars (not a pipeline error), document this as an intentional short description and note that the guide provides substantive supplemental content worth storing as a labeled alternate.

### 8.10 D554 — Advanced Financial Accounting I (data anomaly)

Guide text for D554 in the comparison index contains what appears to be course description text from D560 (Internal Auditing I). This is a suspected source data error in the extraction pipeline, not a legitimate description for D554. Flagged `needs_review + yes` in Batch 3 annotation.

**Required action before canonical object construction:** Investigate the guide source data for D554 to determine whether the D560 text was misrouted during extraction. Do not use the current guide description for D554 in any QA canonical object until the anomaly is resolved. Catalog text for D554 is unaffected and remains the display default.
