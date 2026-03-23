# Policy Implementation Plan — Block Authority and Display

**Version:** 1.0
**Date:** 2026-03-23
**Status:** Design artifact — not yet implemented
**Grounded in:** `BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md` v1.0 (post-synthesis), `LOCAL_8B_RAG_SYSTEM_DESIGN.md`, repo data contracts in `ATLAS_REPO_MEMORY.md`

---

## 1. Scope and Goal

Turn the settled block-authority/display policy into actual Atlas behavior, in the smallest safe stages.

Two distinct concerns are addressed in sequence:
1. **Website display** — course pages explicitly select catalog as default description source; guide alternates are stored accessibly but not displayed by default
2. **QA source authority** — QA canonical objects carry source-selection fields so the QA system can apply the policy programmatically at retrieval time

Program-side overlap is explicitly out of scope for early stages: the prefix-artifact finding means catalog text is already the display copy, and no new artifact work is needed unless MATSPED/BAESSPMM require specific handling.

---

## 2. Settled Policy Inputs

From `BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md`:

| Block | Default source | Stored alternate | Anomaly/flag |
|---|---|---|---|
| Course description | `description_cat` (WGU Catalog 2026-03) | `description_guide_alternates[]` keyed by source_program_codes | C179 (cat short text), D554 (guide misrouted) |
| Program description | catalog text already in `program_enriched.json` | not needed (prefix artifact; body-identical after strip) | MATSPED (guide abridged), BAESSPMM (guide has extra sentence) |
| Competency bullets | guide only (no catalog overlap) | per-program-code variants | none blocking |
| Cert signal | guide only | n/a | none blocking |
| Prerequisites | CANON | n/a | none blocking |
| CU / title / code | CANON | n/a | OV-5/OV-6 deferred |
| Areas of Study / capstone / PLOs | guide-only or cat-only | n/a | none blocking |

**Critical policy rule for all stages:** `display_source` for course descriptions is always `"cat"` when catalog text is present. Guide text is never promoted to default display without explicit human override. The LLM is not permitted to select source.

---

## 3. Stage Sequence Overview

| Stage | Name | Concern | Output |
|---|---|---|---|
| **1** | Source-authority annotation artifact | Data shape | `data/atlas_qa/course_description_authority.json` |
| **2** | Artifact validation | Data integrity | Passing test suite (no app changes) |
| **3** | Course-page display hardening | Website display | Production page wired to authority artifact |
| **4** | Guide alternate storage | Alternate access | `data/atlas_qa/course_guide_alternates.json` |
| **5** | QA canonical object augmentation | QA source wiring | `course_card` extended with source-authority fields |

Stages 1–4 are website/data concerns. Stage 5 is QA-only. Stages 1–2 must complete before 3; Stage 4 can be done in parallel with 3. Stage 5 depends on Stage 1.

---

## 4. Stage-by-Stage Plan

---

### Stage 1 — Source-Authority Annotation Artifact

**Purpose:** Build a single, policy-grounded artifact that records the authoritative display source and stored alternates for every course description. This artifact becomes the single source of truth for source selection in all downstream stages.

**Scope included:**
- All courses with a catalog description (`public/data/course_descriptions.json`, 838 entries)
- All courses with guide descriptions (`data/program_guides/enrichment/course_enrichment_candidates.json`, `courses[]` array — 751 guide-enriched courses)
- Hard-coded anomaly flags for C179 and D554
- Hard-coded review flags for ~25 batch-annotation-flagged courses (see §8)

**Scope excluded:**
- Program descriptions (program-side overlap resolved; no new artifact needed)
- Competency sets, cert signals, AoS, capstone — guide-only blocks, no authority question
- CU conflicts (OV-5/OV-6) — deferred
- QA-specific fields (added in Stage 5)

**Inputs:**
- `public/data/course_descriptions.json` — catalog descriptions, keyed by course code: `{title, description}`
- `data/program_guides/enrichment/course_enrichment_candidates.json` — `courses[]` array with `descriptions[]` per course: `{text, char_length, source_guides, source_program_codes}`

**Output:**
- `data/atlas_qa/course_description_authority.json`

**Output schema:**
```json
{
  "generated_on": "<ISO datetime>",
  "policy_version": "1.0",
  "policy_doc": "BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md",
  "counts": {
    "total_courses": 0,
    "cat_present": 0,
    "guide_present": 0,
    "both_present": 0,
    "cat_only": 0,
    "guide_only": 0,
    "multi_variant_guide": 0,
    "anomaly_flagged": 0,
    "review_flagged": 0
  },
  "entries": {
    "<course_code>": {
      "description_cat": "<string or null>",
      "description_cat_source": "WGU Catalog 2026-03",
      "description_guide_alternates": [
        {
          "text": "<string>",
          "source_program_codes": ["<program_code>", ...],
          "source_guides": ["<guide_id>", ...],
          "char_length": 0
        }
      ],
      "display_source": "cat | guide_only | none",
      "has_guide_alternates": true,
      "multi_variant": false,
      "anomaly_flag": null,
      "anomaly_detail": null,
      "review_flag": false,
      "review_reason": null
    }
  }
}
```

**Deterministic rules (no LLM):**

1. `display_source`:
   - `"cat"` when `description_cat` is not null
   - `"guide_only"` when `description_cat` is null and at least one guide alternate exists
   - `"none"` when both are absent

2. `multi_variant`:
   - `true` when `description_guide_alternates` has more than 1 entry

3. `has_guide_alternates`:
   - `true` when `description_guide_alternates` is non-empty

4. `anomaly_flag` (hard-coded, not inferred):
   - `C179`: `"cat_short_text"`, `anomaly_detail`: `"Catalog text is 293 chars — unusually short for this course type; may be truncated. Guide text is longer and adds routing/switching/automation specifics. Verify catalog extract before relying on catalog-default for this course."`
   - `D554`: `"guide_misrouted_text"`, `anomaly_detail`: `"Guide description text appears to be from D560 (Internal Auditing I). Do not use guide description for this course until source data is investigated."` — and the script must also set `description_guide_alternates: []` for D554 (block misrouted text from the alternates array entirely)

5. `review_flag` (hard-coded list, not inferred): see §8 for the full list of ~25 course codes.

**Script target:** `scripts/build_course_description_authority.py`

**Definition of done:**
- `data/atlas_qa/course_description_authority.json` is written
- counts in `counts` block match known values: ~838 total, ~571 both_present, ~74 multi_variant_guide, 2 anomaly_flagged, ~25 review_flagged
- no `display_source: "guide"` entries exist (catalog is always default when present)
- D554 has empty `description_guide_alternates`

---

### Stage 2 — Artifact Validation

**Purpose:** Confirm the Stage 1 artifact is correct before any app code touches it.

**Scope included:** Data integrity checks only. No app code changes.

**Inputs:** `data/atlas_qa/course_description_authority.json`

**Tests / checks (all deterministic):**

| Check | Expected value |
|---|---|
| `counts.total_courses` | ≥ 838 (catalog-side upper bound) |
| `counts.both_present` | 571 (±2 for known edge cases) |
| `counts.multi_variant_guide` | 74 |
| `counts.anomaly_flagged` | 2 (C179, D554) |
| No entry has `display_source == "guide"` | 0 |
| D554 `description_guide_alternates` | empty list |
| C179 `anomaly_flag` | `"cat_short_text"` |
| D554 `anomaly_flag` | `"guide_misrouted_text"` |
| All entries in `counts.review_flagged` list | present in entries with `review_flag: true` |
| All `description_cat` values for catalog entries | non-null, non-empty string |
| All `description_guide_alternates[*].source_program_codes` | non-empty lists |
| Schema: every entry has all required keys | pass |

**Script target:** `scripts/validate_course_description_authority.py` (or pytest module)

**Failure modes:**
- Count mismatch: re-run Stage 1 script; check input file paths
- D554 guide alternate not cleared: script did not apply anomaly-based override; fix in Stage 1 script
- `display_source: "guide"` entry found: policy bug in Stage 1 logic; fix before proceeding

**Definition of done:** All checks pass with no failures. Exit code 0 from validation script.

---

### Stage 3 — Course-Page Display Hardening

**Purpose:** Make the course page's description source selection explicit and policy-driven, replacing any implicit assumption that the correct source is already being used.

**Scope included:**
- `src/app/courses/[code]/page.tsx` — production course detail page
- The data-loading layer that feeds this page (currently: `public/data/course_descriptions.json` + `public/data/courses/{code}.json`)
- A guard ensuring guide descriptions from `course_enrichment_candidates.json` are NOT currently surfaced on production pages

**Scope excluded:**
- Any UI changes (no new sections, no new components)
- Guide alternate display (Stage 4)
- Proto/preview routes (these are experimental and may already use guide text intentionally)

**Current state to verify first (read before touching):**
1. Confirm `src/app/courses/[code]/page.tsx` reads description from `course_descriptions.json` (catalog source), not from guide enrichment data
2. Confirm no production data loader currently reads from `course_enrichment_candidates.json` for description fields
3. If guide description is present anywhere in production course detail output, flag it as a policy violation and remove it in this stage

**If current state is already correct (catalog-only on production):**
The stage is a hardening-only change:
- Add a comment in the data loader citing the authority policy
- Add a build-time assertion that the description field in `public/data/courses/{code}.json` (if present) matches catalog source, not guide source
- No behavioral change

**If guide text is found on production course pages:**
- Remove it from the production data pipeline
- Verify removal does not break existing tests

**Tests:**
- Spot-check 10 courses (including D358 BSHR cluster course) — description displayed on production page matches `description_cat` in authority artifact
- C179 production page shows catalog text (293 chars) — no guide text; anomaly not yet surfaced to user
- D554 production page shows catalog text; guide text is absent

**Definition of done:**
- Production course pages serve only catalog descriptions
- No guide description text appears in any production-path data file for description fields
- Spot-checks pass

---

### Stage 4 — Guide Alternate Storage

**Purpose:** Make guide description alternates accessible for program-context display (future UI) and QA retrieval, without touching the production page.

**Scope included:**
- Build a separate lookup artifact for guide alternates
- Apply anomaly blocks: D554 guide alternate is absent; C179 alternate is present but flagged

**Scope excluded:**
- Any UI changes to the production course page
- QA canonical object wiring (Stage 5)
- Proto/preview pages (use existing enrichment data directly; not production-path)

**Output:**
- `data/atlas_qa/course_guide_alternates.json`

**Schema:**
```json
{
  "generated_on": "<ISO datetime>",
  "source_artifact": "data/atlas_qa/course_description_authority.json",
  "entries": {
    "<course_code>": {
      "alternates": [
        {
          "text": "<string>",
          "source_program_codes": ["<program_code>", ...],
          "source_guides": ["<guide_id>", ...],
          "char_length": 0,
          "review_flag": false,
          "anomaly_flag": null
        }
      ],
      "alternate_count": 0,
      "multi_variant": false
    }
  }
}
```

**Derivation:** This artifact is derived directly from `course_description_authority.json` — it is a reshaped view of the `description_guide_alternates` field for courses where `has_guide_alternates == true`. The script is a transform, not a new data source.

**Anomaly handling:**
- D554: `alternates: []` (blocked; propagates from Stage 1 authority artifact)
- C179: alternate present, each entry tagged with `anomaly_flag: "cat_short_text"` — consumer must handle

**Script target:** `scripts/build_course_guide_alternates.py`

**Tests:**
- Entry count matches `counts.guide_present` from authority artifact
- D554 has `alternates: []`
- C179 has non-empty alternates with `anomaly_flag` set
- All 74 multi-variant courses have `alternate_count > 1`
- No course has an alternate with null/empty `text`

**Definition of done:**
- `data/atlas_qa/course_guide_alternates.json` written and validated
- D554 blocked; C179 flagged
- Artifact is usable as a lookup table for program-context queries (by course code → alternates by source_program_codes)

---

### Stage 5 — QA Canonical Object Source-Authority Fields

**Purpose:** Extend the `course_card` canonical object (per `LOCAL_8B_RAG_SYSTEM_DESIGN.md §7.1`) with source-authority fields so the QA system can apply the display policy programmatically at retrieval time.

**Dependencies:** Stage 1 artifact must be complete and validated. This stage does not touch the website display path.

**Scope included:**
- Extend the `course_card` schema with source-authority fields
- Derive values from `course_description_authority.json`
- Define QA-specific decision rules using these fields

**Scope excluded:**
- QA retrieval implementation (that's Stage 4+ in the LOCAL_8B_RAG_SYSTEM_DESIGN.md sequence)
- Fuzzy retrieval, embedding, ranking — not needed here
- CU conflict fields (OV-5/OV-6) — deferred

**Source-authority fields to add to `course_card`:**

```json
{
  "description_display_source": "cat | guide_only | none",
  "description_cat_present": true,
  "description_cat_char_length": 0,
  "description_guide_alternate_count": 0,
  "description_multi_variant": false,
  "anomaly_flags": [],
  "description_review_flag": false
}
```

**QA retrieval rules (deterministic, derived from these fields):**

| Condition | QA behavior |
|---|---|
| `description_display_source == "cat"` | Default answer source: `description_cat`. Cite: `WGU Catalog 2026-03`. |
| `description_display_source == "guide_only"` | Default answer source: guide alternate (any variant). Disclose: no catalog description available; source is program guide. |
| `description_display_source == "none"` | Abstain: description not available in current sources. |
| Program context provided AND `description_guide_alternate_count > 0` | Select guide alternate matching `source_program_codes`. Fall back to catalog if no match. |
| `"guide_misrouted_text" in anomaly_flags` (D554) | Do not cite guide description. Catalog only. Add abstention note if guide answer is requested: "Guide description for this course contains a data anomaly and is not available." |
| `"cat_short_text" in anomaly_flags` (C179) | Cite catalog with disclosure: "Catalog description for this course is unusually brief; completeness has not been confirmed. Guide text may provide additional detail." Offer guide alternate if available. |
| `description_review_flag == true` | Standard catalog-default still applies. No special QA behavior yet — review_flag is metadata only until human review completes. |

**Tests:**
- `course_card` for D358 (BSHR cluster): `description_display_source: "cat"`, `description_guide_alternate_count: 1`, `description_multi_variant: false`, `description_review_flag: true`
- `course_card` for C179: `description_display_source: "cat"`, `anomaly_flags: ["cat_short_text"]`
- `course_card` for D554: `description_display_source: "cat"`, `anomaly_flags: ["guide_misrouted_text"]`, `description_guide_alternate_count: 0`
- A guide-only course (no catalog entry): `description_display_source: "guide_only"`
- A course with no sources: `description_display_source: "none"`

**Definition of done:**
- `course_card` schema includes all source-authority fields
- QA retrieval rule table is encoded in the QA control layer (not as LLM instructions)
- All test cases pass

---

## 5. Data / Model Changes Needed

| Artifact | Stage | Change type | Notes |
|---|---|---|---|
| `data/atlas_qa/course_description_authority.json` | 1 (create) | New artifact | Output of `build_course_description_authority.py` |
| `data/atlas_qa/course_guide_alternates.json` | 4 (create) | New artifact | Derived from authority artifact |
| `src/app/courses/[code]/page.tsx` | 3 (harden) | Source comment + build assertion | Only if current state is already catalog-only; remove guide text if found |
| `course_card` schema | 5 (extend) | Schema extension | Add source-authority fields |

**No changes to:**
- `public/data/course_descriptions.json` — already catalog text; read-only input
- `data/program_guides/enrichment/course_enrichment_candidates.json` — read-only input
- `public/data/courses/{code}.json` — not modified in these stages
- `data/canonical_courses.json` — not modified in these stages

---

## 6. File / Module Ownership Proposal

| Concern | Path |
|---|---|
| Authority artifact | `data/atlas_qa/course_description_authority.json` |
| Guide alternates artifact | `data/atlas_qa/course_guide_alternates.json` |
| Stage 1 build script | `scripts/build_course_description_authority.py` |
| Stage 2 validation script | `scripts/validate_course_description_authority.py` |
| Stage 4 build script | `scripts/build_course_guide_alternates.py` |
| QA source-authority rules | `src/atlas_qa/qa/source_authority.py` |
| QA `course_card` schema | `src/atlas_qa/qa/types.py` (extend existing `course_card` type) |
| Hard-coded anomaly/review lists | defined as module-level constants in `build_course_description_authority.py` |

---

## 7. Verification and Tests

### Per-stage gates (summary)

| Stage | Gate | Blocking? |
|---|---|---|
| 1 | `data/atlas_qa/course_description_authority.json` exists and has correct structure | Yes |
| 2 | All validation checks pass (exit 0) | Yes — Stage 3 blocked until this passes |
| 3 | Production course pages serve only catalog text; spot-checks pass | Yes — Stage 4/5 can proceed in parallel |
| 4 | `data/atlas_qa/course_guide_alternates.json` exists; D554 blocked; C179 flagged | Yes for Stage 5 alt-lookup |
| 5 | All `course_card` source-authority field tests pass | Yes for QA source routing |

### Cross-stage regression check
After Stage 3: confirm `public/data/course_descriptions.json` content has not been modified (it is a read-only input; any modification is a bug).

---

## 8. Known Anomaly Gates / Deferred Items

### Hard-coded anomaly cases (must be in Stage 1 artifact before Stages 3–5)

| Course | Flag | Required handling |
|---|---|---|
| C179 | `cat_short_text` | Stage 1: flag in authority artifact. Stage 5: QA discloses brief catalog text, offers guide alternate. Website: no change (catalog text is still served, even if brief). |
| D554 | `guide_misrouted_text` | Stage 1: clear `description_guide_alternates` (set to `[]`). Stage 5: QA abstains on guide description for this course. |

### Review-flagged courses (~25 rows, not blocking)
These courses have `review_flag: true` in the authority artifact. They are candidates for program-context alternate display once human review completes. They do not block any stage.

Hard-coded `review_flag: true` list (from batch annotation):

**BSHR cluster (pre-rewrite content delta):** D358, D356, D354, D360

**MSHRM cluster (program-degree-specific framing):** D432, D433, D435, D436

**BSPRN clinical nursing (guide adds clinical structure):** D218, D348, C947 — and others from the BSPRN/MSNULM/PMCNUPMHNP cluster flagged in Batch 3 annotation. Complete list: see Batch 2 and Batch 3 `llm_review_flag: yes` rows. The script should use a module-level constant for this list.

**Other flagged individual rows:** C236 (Compensation and Benefits — framing emphasis difference), E011 v1/3 (Technical Communication — audience framing difference), D255 (PPE I: Technical — competency framing difference), D118, D119, D124 (FNP clinical courses), C845 (Cybersecurity Capstone)

### Deferred items (not in scope for Stages 1–5)

| Item | Deferred reason |
|---|---|
| OV-5: 41 courses with guide-internal CU conflicts | CU conflicts are CANON-authority questions, not description-display questions. Requires a separate CANON audit pass. |
| OV-6: 7 programs with CAT total vs guide SP sum discrepancy | Same as OV-5; CANON-side issue. |
| Competency variant conflict detection (185 courses) | Current placeholder policy (most-common variant) is acceptable for v1. A substantive-vs-cosmetic pass is needed but not blocking. |
| MATSPED / BAESSPMM program description edge cases | Catalog is already the display copy; no new artifact needed. Flag in program-level QA logic when implemented. |
| MSHRM version freshness | Body text is currently identical after prefix strip; no display conflict today. Monitor for future guide updates. |
| Human review of ~25 `review_flag: true` courses | Gate for setting program-context display alternates. Not blocking catalog-default implementation. |

---

## 9. Definition of Implementation Readiness

**Stage 1 ready to start:** Immediately. Both input artifacts exist. Script does not touch any app code.

**Stage 2 ready to start:** After Stage 1 script produces output.

**Stage 3 ready to start:** After Stage 2 validation passes. Requires reading the current production page data loader first — do not assume current state.

**Stage 4 ready to start:** After Stage 1 artifact exists. Can run in parallel with Stage 3.

**Stage 5 ready to start:** After Stage 1 artifact exists and `course_card` type is available to extend. Does not depend on Stages 3 or 4.

**Overall implementation is ready when:**
- Stages 1 and 2 are complete (authority artifact exists and is validated)
- Stage 3 production page is hardened (catalog-only confirmed in production path)
- Stage 4 guide alternates are stored and accessible
- Stage 5 `course_card` fields are defined and test cases pass

**What can ship before QA concerns are fully resolved:**
- Stages 1–4 (website display hardening + guide alternate storage) can ship independently of Stage 5
- The catalog-default display behavior is likely already correct on the production site; Stage 3 may be a documentation/assertion-only change
- Stage 5 is QA-internal and does not require any website changes
