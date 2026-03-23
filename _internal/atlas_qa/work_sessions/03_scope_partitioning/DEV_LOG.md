# DEV_LOG — Session 03: Scope Partitioning

Append-only. Each entry records what was actually done, not what was planned.

---

## 2026-03-23 — Claude (implementation pass)

**Scope:** Full Session 03 implementation — deterministic scope partitioning

**Pre-implementation plan (5–10 bullets):**

1. Add `SectionScope`, `SourceFamily`, `PartitionStatus`, `PartitionInput`, `PartitionResult` to `src/atlas_qa/qa/types.py`.
2. Create `src/atlas_qa/qa/scope_partitioning.py` with:
   - `from_exact_result()` — build `PartitionInput` from a Session 02 `ExactLookupResponse`
   - `from_partial_context()` — build `PartitionInput` from partial/NL upstream context
   - `derive_partition()` — deterministic scope derivation (entity/version/source/section)
   - `enforce_course_partition()`, `enforce_program_partition()`, `enforce_guide_section_partition()` — hard enforcement filters
3. Source-scope rules: guide-only sections → `[GUIDE]`; catalog-default sections → `[CATALOG]`; default unspecified → both where available; D554 guide path blocked; version-conflict programs add disclosure note.
4. Version-scope rules: single-version default; explicit version from upstream; compare_intent flag for future two-version support (no mixed-version blending without explicit flag).
5. Partition failure mapped to existing `AbstentionState` where possible (AMBIGUOUS_ENTITY, AMBIGUOUS_VERSION, OUT_OF_SCOPE, INSUFFICIENT_EVIDENCE); no new states needed.
6. Create `src/atlas_qa/qa/coordinator.py` — thin orchestration: route → lookup → partition_from_exact_result (exact path) or partition_from_partial_context (NL path).
7. Add `tests/atlas_qa/test_scope_partitioning.py` covering: wrong-version blocking, section leakage blocking, source-scope enforcement, entity collision, mixed-version rejection, exact-path preservation, D554 guide block, version-conflict disclosure, C179 anomaly metadata, compare_intent flag.

**Target files:**
- `src/atlas_qa/qa/types.py` — modified (add 5 new types)
- `src/atlas_qa/qa/scope_partitioning.py` — created
- `src/atlas_qa/qa/coordinator.py` — created
- `tests/atlas_qa/test_scope_partitioning.py` — created

**Blockers discovered in inspection:** None. Session 02 is complete and passing. Guide section cards have section_type values: `standard_path`, `areas_of_study`, `capstone`. Competency and cert-prep data lives within `standard_path` section_data. Program cards are keyed by program_code (one card per program, at the most recent version).

**Files created:**
- `src/atlas_qa/qa/scope_partitioning.py` — `from_exact_result()`, `from_partial_context()`, `derive_partition()`, `enforce_course_partition()`, `enforce_program_partition()`, `enforce_guide_section_partition()`
- `src/atlas_qa/qa/coordinator.py` — thin orchestration: `coordinate()`, `get_scoped_course_cards()`, `get_scoped_program_cards()`, `get_scoped_guide_sections()`
- `tests/atlas_qa/test_scope_partitioning.py` — 50 tests

**Files modified:**
- `src/atlas_qa/qa/types.py` — added `SectionScope`, `SourceFamily`, `PartitionStatus`, `PartitionInput`, `PartitionResult`

**Design decisions:**
- Reused existing `AbstentionState` values for all partition failure reasons; no new typed states needed.
- `_GUIDE_ONLY_SECTIONS` = {COMPETENCIES, AREAS_OF_STUDY, CAPSTONE, CERTIFICATION_LICENSURE}; `_CATALOG_ONLY_SECTIONS` = {COURSE_OVERVIEW, PROGRAM_DESCRIPTION, TOTAL_CU_IDENTITY}.
- D554 guide path blocked at source-scope derivation regardless of section_scope input.
- C179 anomaly: partition succeeds but adds a note; downstream can prefer guide if available.
- Version-conflict programs (MACCA, MACCF, MACCM, MACCT, MSHRM): both CATALOG and GUIDE included in source_scope but a note is added disclosing the mismatch — no silent blending.
- Mixed-entity retrieval (multiple distinct candidates without compare_intent) fails with INSUFFICIENT_EVIDENCE.
- compare_intent sets the `compare_mode` flag on PartitionResult but does not enable mixed-version blending; that is Session 04's concern.
- Guide section version matching uses compact normalization (strips `-` `_`) so "2025-03" matches "202503".

**Checks run:**
```
PYTHONPATH=src python3 -m pytest tests/atlas_qa/test_scope_partitioning.py -v
```
50 passed, 0 failed.

```
PYTHONPATH=src python3 -m pytest tests/atlas_qa/test_lookup.py -v
```
42 passed, 0 failed. Session 02 guarantees preserved.

**Session 03 status:** Complete. All definition-of-done criteria satisfied.

**Scope API introduced:**

Input construction:
- `from_exact_result(ExactLookupResponse, section_scope, compare_intent) → PartitionInput`
- `from_partial_context(candidate_codes, section_scope, compare_intent, upstream_abstention) → PartitionInput`

Derivation:
- `derive_partition(PartitionInput, course_cards, program_cards) → PartitionResult`

Enforcement:
- `enforce_course_partition(PartitionResult, course_cards) → dict[str, CourseCard]`
- `enforce_program_partition(PartitionResult, program_cards) → dict[str, ProgramVersionCard]`
- `enforce_guide_section_partition(PartitionResult, guide_sections) → list[GuideSectionCard]`

Coordinator entry point:
- `coordinate(raw_query, section_scope, compare_intent) → (PartitionResult, ExactLookupResponse | None)`

**Repo-layout recommendations (not applied):** None. Layout is clean; Session 04 should add `retrieval.py` alongside existing modules.

---
