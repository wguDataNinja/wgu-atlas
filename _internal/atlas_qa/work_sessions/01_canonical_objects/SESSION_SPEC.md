# Session 01 — Canonical Object Generation

**Status:** Active
**Intent:** Implementation, not design

**Design docs:** `_internal/atlas_qa/LOCAL_8B_RAG_SYSTEM_DESIGN.md` (v1.4), `_internal/atlas_qa/PM_CONTEXT_PACKET.md`

## Codex execution instructions

Read these files first, in this order:

1. `_internal/atlas_qa/WORK_SESSION_RULES.md`
2. `_internal/atlas_qa/work_sessions/01_canonical_objects/SESSION_SPEC.md`
3. `_internal/atlas_qa/LOCAL_8B_RAG_SYSTEM_DESIGN.md`
4. `_internal/atlas_qa/PM_CONTEXT_PACKET.md`

Treat `WORK_SESSION_RULES.md` as the process control document and this `SESSION_SPEC.md` as the execution contract. The design doc and PM packet provide locked context; they do not authorize scope expansion.

### Required execution order

1. **Inspect the repo first**
   - Inspect current relevant layout under `src/atlas_qa/`, `scripts/`, test/fixture locations, and the Atlas-local data inputs referenced by this session.
   - Identify any existing QA/canonical-object code or adjacent patterns before creating new files.

2. **Do the Session 01 preflight before substantive implementation**
   - Perform the Appendix A checks.
   - Record the result in `DEV_LOG.md`.
   - If required local inputs are missing or unusable, stop and report blockers instead of inventing workarounds.

3. **Write a short implementation plan before editing**
   - Record a concise 5–10 bullet implementation plan in `DEV_LOG.md` after inspection/preflight and before substantive code changes.
   - Include target files, intended outputs, validation approach, and any blockers discovered.

4. **Implement Session 01 only**
   - Define canonical object schemas/types.
   - Implement `course_card` generation first.
   - Implement required source-authority and anomaly handling.
   - Validate representative fixtures.
   - Then implement the remaining canonical object families.

5. **Run only the checks allowed by this spec**
   - Do not run broad repo-wide checks unless this session genuinely requires them.

6. **Update `DEV_LOG.md` before finishing**
   - Log preflight results, implementation steps, files changed, checks run, results, and blockers/deviations.

### Do not

- Reopen design decisions
- Reinterpret source-authority policy
- Modify `src/app/`
- Modify `wgu-reddit` or any upstream repo
- Implement Session 02+ work in this pass
- Introduce model use into canonical object generation

### Final report requirement

At the end of the run, report:

- files created or updated
- whether preflight passed
- checks run and outcomes
- whether Session 01 is complete, partial, or blocked
- any small repo-layout recommendations, without applying unrelated cleanups

---

## Objective

Build deterministic canonical synthetic objects from already-local Atlas artifacts, with no model use during object generation. Outputs are Atlas-local structured artifacts that serve as the primary retrieval surface for all downstream QA paths.

---

## Why this session exists

Stages 0–2 established the substrate and confirmed the import boundary. Stage 3 (this session) is the first implementation work against the Atlas-local artifact layer. Canonical objects are the foundation for everything downstream: the exact/simple lookup path (Session 02) depends on them, the later retrieval path will query them, and evaluation will validate against them. This session is where the deterministic data layer becomes real. Do not proceed to Session 02 until these objects are generated and validated.

---

## In scope

- [ ] Define schemas/types for all four canonical object families:
  - `course_card`
  - `program_version_card`
  - `guide_section_card`
  - `version_diff_card`
- [ ] Implement deterministic builder for `course_card` (first priority — see First implementation slice)
- [ ] Incorporate source-authority fields into `course_card` (required before Session 02)
- [ ] Implement deterministic builders for `program_version_card`, `guide_section_card`, `version_diff_card`
- [ ] Support evidence reference placeholders in all objects (final `evidence_refs` schema is TBD; use a placeholder shape consistent with §2.2 open items)
- [ ] Generation is deterministic-only from Atlas-local inputs — no model calls during object generation
- [ ] Schema validation for all object families
- [ ] Uniqueness: exactly one `course_card` per `course_code`; no duplicate `course_code` objects in final output
- [ ] Version-isolation checks (no mixed-version content in a single object)
- [ ] Representative golden fixtures for at least one object per family
- [ ] Anomaly checks for C179 and D554
- [ ] Deterministic reproducibility check: re-running generators must produce identical output
- [ ] Preflight input inventory and sanity check before builder implementation; log results in `DEV_LOG.md`

---

## Out of scope

- Fuzzy or semantic retrieval of any kind
- Answer generation or LLM-based synthesis
- Routing or classifier implementation
- Compare narrative generation beyond deterministic `version_diff_card` construction
- Finalizing the `evidence_refs` schema (TBD; placeholder is acceptable here)
- Any change to source-authority policy or block-authority decisions
- App/page changes (`src/app/`)
- Changes to `wgu-reddit` or any upstream repo
- Broad repo-wide test runs unless shared code is genuinely modified

---

## Inputs

All inputs are Atlas-local. No cross-repo reads required.

| Input | Path |
|---|---|
| Catalog trusted artifacts | `data/catalog/trusted/2026_03/` |
| Catalog change tracking | `data/catalog/change_tracking/` |
| Catalog edition diffs | `data/catalog/edition_diffs/` |
| Large helper files (gitignored) | `data/catalog/helpers/course_index_v10.json`, `degree_snapshots_v10_seed.json`, `sections_index_v10.json` — must be present locally; acquire from `wgu-reddit` if absent (see `data/catalog/README.md`) |
| Parsed program guides | `data/program_guides/parsed/` (115 files) |
| Guide manifest + anomaly registry | `data/program_guides/guide_manifest.json`, `guide_anomaly_registry.json` |
| Canonical courses | `data/canonical_courses.csv`, `data/canonical_courses.json` (1594 codes) |
| LLM substrate | `src/atlas_qa/llm/`, `src/atlas_qa/utils/` — available for context; **not used during object generation** |

---

## Architecture invariants (enforce in generated objects)

These rules from the design doc must be reflected in object shape and generation logic:

1. **Exact identifiers never start in semantic retrieval.** Objects must be keyed on exact identifiers.
2. **Object identity and version labeling.** `course_card` primary key is `course_code`. `program_version_card` remains a single-version object keyed by program × version. `course_card` may contain version-labeled or program-labeled subfields, but it must not contain unlabeled blended content across versions or programs.
3. **No free-form merged summaries.** `course_card` must not contain free-form merged summaries that combine multiple versions or multiple program variants into one unlabeled text field.
4. **Mixed-version content is forbidden** in any single canonical object unless it is a `version_diff_card` (which is explicitly multi-version by design).
5. **No source selection by model.** Authority rules are encoded in builder logic, not LLM output.
6. **Canonical generation is deterministic only.** Same inputs → same outputs, always.
7. **Hard anomaly handling is encoded in the object**, not deferred to answer time.

---

## Required source-authority fields for `course_card`

The following fields (derived from `BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md` and the PM packet) must be present in `course_card`. These are not optional.

### Locked identity rule

- `course_card` primary key is `course_code`.
- There is exactly one canonical `course_card` per `course_code`.
- Version-specific and program-specific differences must be stored in explicitly labeled subfields on that object.
- Do not create multiple final `course_card` objects for the same `course_code`.

### Identity and core facts (CANON authoritative)
- `course_code` — canonical code
- `canonical_title` — from canonical course index
- `canonical_cus` — from canonical course index; note: guide CU not authoritative
- `title_variants` — any alternate titles observed across catalog editions or guide references

### Catalog description (CAT-TEXT default)
- `catalog_description` — full text from catalog (default display source)
- `catalog_description_version` — version token for catalog source
- `cat_short_text_flag` — boolean; `true` if catalog description is ≤ 300 chars (C179 trigger)

### Guide description alternates (ENRICH, program-scoped, never default)
- `guide_description_alternates` — sorted list of objects `{source_program_code, guide_version, description_text}`; every entry must include both program label and guide version label
  - **D554 hard rule:** this list must be `[]` for D554; do not populate from guide for this course
- `guide_misrouted_text_flag` — boolean; `true` for D554

### Competency bullets (ENRICH — sole source)
- `competency_variants` — sorted list of objects `{source_program_code, guide_version, bullets}`; every entry must include both program label and guide version label
- `competency_variant_count` — integer; used at answer time to decide whether to disclose multi-variant

### Cert prep signal (ENRICH — sole source)
- `cert_prep_signal` — structured object with exactly these fields:
  - `status: "present" | "not_found_in_observed_guides" | "unknown"`
  - `label: str | null`
  - `guide_versions_observed: list[str]`

  `status="not_found_in_observed_guides"` means the signal was not found in the observed guide materials. It does not authorize answer-time absence claims without a separate completeness gate.

  `status="unknown"` means the builder cannot determine observed-guide coverage confidently.

### Prerequisites (CANON — structured only)
- `prerequisite_course_codes` — list of codes from canonical structured data
- `is_prereq_for` — reverse relationships (do not assert absence without completeness confirmation)

### Program association
- `program_codes` — sorted list of all program codes in which this course appears across observed inputs
- `instances_by_version` — sorted list of objects `{catalog_version, program_codes}` describing where this course appears by catalog version; this field is metadata only and does not change `course_card` identity

### Guide enrichment summary
- `guide_enrichment_available` — boolean
- `guide_enrichment_summary` — structured object with exactly these fields:
  - `has_guide_description_alternates: bool`
  - `has_competencies: bool`
  - `competency_variant_count: int`
  - `has_cert_prep_signal: bool`
  - `program_count_with_guide_enrichment: int`

  No prose summary. No free-form text.

### Version-conflict flag
- `version_conflict_programs` — sorted list of objects with exactly these fields:
  - `program_code: str`
  - `catalog_version: str | null`
  - `guide_version: str | null`
  - `conflict_type: "catalog_guide_version_mismatch"`

### Evidence refs (placeholder)
- `evidence_refs` — list of evidence reference objects; exact schema TBD (Stage 2 open item); use a placeholder shape for now, e.g., `{source_type: str, artifact_id: str, version: str}`

---

## Expected implementation locations

These are strongly suggested, not final prescriptions. Choose Atlas-local locations that are consistent with the existing `src/atlas_qa/` layout.

| Concern | Suggested location |
|---|---|
| Object type definitions / schemas | `src/atlas_qa/qa/types.py` |
| Source-authority field logic | `src/atlas_qa/qa/source_authority.py` |
| Builder modules | `src/atlas_qa/qa/builders/course_card.py`, `program_version_card.py`, etc. |
| Generation entrypoints / scripts | `scripts/build_course_cards.py`, `scripts/build_program_version_cards.py`, etc. |
| Generated output artifacts | `data/atlas_qa/course_cards.json`, `data/atlas_qa/program_version_cards.json`, etc. |
| Golden fixtures | `src/atlas_qa/qa/tests/fixtures/` or `tests/atlas_qa/fixtures/` |
| Validation / checks | `scripts/validate_canonical_objects.py` or co-located with builders |

Do not write canonical object code into `src/atlas_qa/llm/` — that module is the LLM substrate only.

---

## Expected outputs

All generated artifacts go under `data/atlas_qa/`. Do not scatter outputs elsewhere.

| Output | Description |
|---|---|
| `data/atlas_qa/course_cards.json` | One canonical `course_card` per `course_code` (1594 total based on current canonical course index) |
| `data/atlas_qa/program_version_cards.json` | One card per program × version |
| `data/atlas_qa/guide_section_cards.json` | One card per program × version × section type |
| `data/atlas_qa/version_diff_cards.json` | One card per entity × version pair with a computed diff |

Builders may process version-partitioned inputs internally, but final `course_card` output must be consolidated to one object per `course_code`.

Large output files should follow the same gitignore policy as other large Atlas data files — check before committing.

---

## Validation requirements

All of the following must pass before this session is done:

- [ ] Schema validation: every generated object conforms to its Pydantic/dataclass schema
- [ ] Uniqueness: exactly one `course_card` per `course_code`; no duplicate primary keys within any object family
- [ ] Version/program labeling: every multi-value field in `course_card` is explicitly labeled by version and/or program as required by schema
- [ ] No unlabeled blending: no `course_card` field contains merged text or merged values synthesized across versions or programs without explicit labels
- [ ] Version isolation: no `program_version_card` contains content from a version other than its declared version
- [ ] Anomaly checks:
  - C179: `cat_short_text_flag` is `true`; catalog text present; guide alternate(s) present if available
  - D554: `guide_description_alternates` is `[]`; `guide_misrouted_text_flag` is `true`
- [ ] Source-authority assertions: `catalog_description` is populated from CAT-TEXT, not guide, for all courses
- [ ] Representative golden fixtures: at least 3–5 `course_card` fixtures covering a normal course, C179, D554, a multi-variant competency course, and a version-conflicted program course
- [ ] Deterministic reproducibility: two sequential runs produce identical output (diff clean)

---

## Allowed checks

This spec explicitly permits:

- Repo inspection limited to files and directories relevant to this session
- Running generation scripts locally against Atlas-local inputs
- Running schema validation scripts
- Running targeted tests for canonical object generation if tests are written as part of this session
- Inspecting generated artifact files locally
- Targeted test runs if shared code in `src/atlas_qa/` is modified

Not permitted without explicit session-level justification:

- broad repo-wide test runs
- app build runs
- checks that span outside `src/atlas_qa/`, `scripts/`, and the Atlas-local data inputs required by this session
- unrelated cleanup or refactor work

---

## Definition of done

All must be true:

- [ ] `course_card`, `program_version_card`, `guide_section_card`, and `version_diff_card` builders exist in Atlas
- [ ] Object outputs can be generated end-to-end from Atlas-local inputs
- [ ] `course_card` includes all required source-authority and anomaly fields
- [ ] All validation checks pass
- [ ] Representative fixtures exist for each object family
- [ ] No cross-repo runtime dependency introduced by this session
- [ ] `DEV_LOG.md` updated with actual work performed

---

## Risks and edge cases

Address these explicitly during implementation — do not treat them as deferred.

| Risk | Handling |
|---|---|
| **C179** — catalog text is only 293 chars, completeness unconfirmed | Set `cat_short_text_flag: true`. Serve catalog text as default. Populate guide alternate if available. Do not suppress or skip this course. |
| **D554** — guide description contains text from D560 (data anomaly) | Set `guide_misrouted_text_flag: true`. Set `guide_description_alternates: []`. Never serve guide description for this course. Catalog text is unaffected. |
| **Version-conflicted programs** (MACCA, MACCF, MACCM, MACCT, MSHRM) | Populate `version_conflict_programs` with structured conflict records containing `program_code`, `catalog_version`, `guide_version`, and `conflict_type`. Do not blend or suppress. |
| **Guide-only blocks** (competencies, AoS, capstone, cert prep) | These have no catalog overlap — no authority question arises. Populate from guide as sole source. Handle absence carefully: absence of cert prep does not confirm absence without a completeness check. |
| **Unresolved `evidence_refs` final format** | Use placeholder shape. This is an explicit Stage 2 open item and must not block canonical object construction. |
| **Large gitignored helper files** | Check that `data/catalog/helpers/` files are present before running builders. Fail loudly if absent with a clear re-acquisition message. |
| **Multi-variant competency sets** (185 courses with 2–6 variants) | Preserve all variants keyed by source program. Default display heuristic (most-common-by-program-count) is one open design question — implement storage now, defer default-selection logic to Session 02 or later. |

---

## Escalation rules

- Do not resolve locked design questions locally. Log them in DEV_LOG.md and continue with the most conservative interpretation.
- Do not reinterpret source-authority policy. The policy in `BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md` is locked.
- If an object-shape tradeoff materially affects Session 02 or later, log it explicitly and stop short of making a design change. Flag to owner.
- Do not change app/page code (`src/app/`) in this session.

---

## First implementation slice

Start here. Do not skip to later object families before this slice is solid.

1. **Define schemas** — Write `types.py` with Pydantic models (or dataclasses) for all four object types. Define the `course_card` schema first. `course_card` identity must be `course_code`. All version-specific and program-specific differences must live in labeled subfields, not separate final `course_card` objects.
2. **Implement `course_card` generator** — Build `builders/course_card.py`. Read from `data/canonical_courses.*`, `data/catalog/trusted/2026_03/`, `data/program_guides/parsed/`.
3. **Add source-authority field logic** — Implement `source_authority.py` with the authority rules for description, competencies, cert prep, prerequisites, and anomaly flags. Wire into the `course_card` builder.
4. **Validate on representative fixtures** — Generate cards for: a normal course, C179, D554, a multi-variant competency course, a course in MACCA/MSHRM. Confirm all flags and field values are correct.
5. **Implement remaining object families** — Once `course_card` is solid, implement `program_version_card`, `guide_section_card`, and `version_diff_card` builders.
6. **Run full generation + validation** — Generate all objects, run schema/uniqueness/version-isolation checks, confirm deterministic reproducibility.

---

## Appendix A — Required preflight before builder implementation

This appendix is part of Session 01 execution. It is required. Its purpose is to confirm that the Atlas-local artifact layer is actually present and usable before canonical object builders are implemented or run. Keep it bounded: enough to de-risk the session, not enough to turn into a corpus archaeology project.

### Preflight outcome required to proceed

Before substantial builder work begins, verify that required Atlas-local inputs exist, are readable, and look structurally plausible. Record the results in `DEV_LOG.md`, including any blockers, missing local artifacts, or reasons the session cannot proceed.

If required local inputs are missing or unusable, stop substantive implementation and report the blocker clearly. Do not invent fallback data sources or alternate workflows.

### Required checks

#### 1. Presence checks

Confirm presence of the required input families listed in the main spec, including:

- `data/catalog/trusted/2026_03/`
- `data/catalog/change_tracking/`
- `data/catalog/edition_diffs/`
- `data/program_guides/parsed/`
- `data/program_guides/guide_manifest.json`
- `data/program_guides/guide_anomaly_registry.json`
- `data/canonical_courses.csv`
- `data/canonical_courses.json`

#### 2. Helper file checks

Explicitly check whether these local helper files are present and readable:

- `data/catalog/helpers/course_index_v10.json`
- `data/catalog/helpers/degree_snapshots_v10_seed.json`
- `data/catalog/helpers/sections_index_v10.json`

If any required helper file is absent, fail loudly with a clear note that it must be re-acquired locally per `data/catalog/README.md`.

#### 3. Basic size and sanity checks

Run only lightweight checks sufficient to catch obviously broken inputs:

- file exists
- non-zero size
- JSON parses where applicable
- CSV opens where applicable
- file counts and rough scale are plausible against known corpus facts

Examples of plausible checks:

- parsed guide file count is roughly consistent with the expected 115 guides
- canonical course count is roughly consistent with the expected 1594 codes
- trusted catalog artifact set is present
- helper JSON files are not suspiciously tiny or truncated

#### 4. Readability and structural plausibility

Confirm that the main input artifacts can be loaded by the intended implementation path without immediate structural failure. This is not the full validation phase; it is only the preflight required to determine whether Session 01 can proceed safely.

### Required logging in `DEV_LOG.md`

Record the preflight before or alongside the first implementation entry. Include:

- date/time
- actor
- files/directories checked
- notable counts or size observations
- missing artifacts, if any
- whether Session 01 can proceed

Also record the short implementation plan required by the Codex execution instructions before substantive edits begin.

### Out of scope for preflight

Do not let preflight expand into:

- a full corpus re-analysis
- a new annotation pass
- a deep reconciliation effort
- re-derivation of design metrics already locked in the PM packet

This is a bounded execution safeguard, not a separate research task.
