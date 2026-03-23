# Session 03 — Scope Partitioning

**Status:** Queued / next (after Session 02 complete)  
**Intent:** Implementation  
**Dependency:** Session 02 (`02_exact_lookup_path`) must be complete and passing before this session starts

## Session 02 completion note

Session 02 is complete and validated. Session 03 must build on the exact/simple path and canonical artifact layer already implemented.

Relevant completed components now exist in:

- `src/atlas_qa/qa/router.py`
- `src/atlas_qa/qa/entity_resolution.py`
- `src/atlas_qa/qa/version_resolution.py`
- `src/atlas_qa/qa/loaders.py`
- `src/atlas_qa/qa/response.py`
- `src/atlas_qa/qa/lookup.py`
- `src/atlas_qa/qa/types.py`
- `src/atlas_qa/qa/source_authority.py`

Relevant Atlas-local canonical artifacts already exist in:

- `data/atlas_qa/course_cards.json`
- `data/atlas_qa/program_version_cards.json`
- `data/atlas_qa/guide_section_cards.json`
- `data/atlas_qa/version_diff_cards.json`

Session 02 also established this intentional behavior:

- exact identifiers are intercepted before any broader retrieval logic
- all-alpha candidates that miss the corpus may return `out_of_scope` rather than `not_in_corpus` in the exact path

Session 03 must preserve those guarantees. It must not reopen or weaken the exact-path behavior already validated in Session 02.

## LLM use

None in Session 03.

This session is fully deterministic. Do not call the LLM substrate for scope derivation, partitioning, validation, fallback behavior, or filtering.

### Reserved space for future custom LLM instructions

Not used in this session.

If later sessions introduce a structured classifier upstream of partitioning, add custom model instructions in a separate session appendix or dedicated prompt-contract file. Do not introduce that work here.

---

## Locked implementation decisions for this session

These decisions are settled for Session 03 and should not be redesigned during implementation:

1. **Partition input type**
   - Session 03 must define a typed `PartitionInput` model in `src/atlas_qa/qa/types.py`.
   - `PartitionInput` must support two construction paths:
     - from an exact-path resolved result produced by Session 02
     - from a partially resolved upstream context for NL/future retrieval flow
   - The model must make it explicit which fields are populated in each path.

2. **Section scope behavior for NL queries**
   - Session 03 does **not** infer section scope from raw NL text.
   - For NL/partial inputs, `section_scope` remains unspecified unless it is already explicitly supplied by structured upstream input.
   - Section leakage tests in this session apply only when `section_scope` is already specified.

3. **Coordinator placement**
   - Session 03 should introduce a thin coordinator module rather than expanding `lookup.py` beyond its exact/simple responsibility.
   - Prefer `src/atlas_qa/qa/coordinator.py` as the orchestration point for:
     - upstream route/resolution context
     - partition input construction
     - scope derivation
     - partition enforcement handoff

---

## Objective

Implement hard retrieval partitioning for downstream QA. Given a typed `PartitionInput` built from either exact-path resolution or partially resolved upstream context, derive and enforce deterministic scope constraints before any retrieval or context packing occurs.

This session should produce the control-plane layer that decides:

- which entity or entities are in scope
- which version or versions are in scope
- which source families are allowed
- which section types are allowed
- whether compare mode is permitted
- whether the query must abstain before retrieval

No fuzzy retrieval, no ranking, no answer generation, and no LLM use in this session.

---

## Why this session exists

Sessions 01–02 established the deterministic data layer and the exact/simple QA path. Session 03 is the next control-layer safeguard.

The system’s primary failure risk remains plausible, citation-bearing, wrong-version synthesis. The primary control against that risk is hard partitioning before retrieval. This session exists to make that safeguard explicit, typed, and enforceable.

Session 04 retrieval must consume the outputs of this session rather than inventing scope on the fly.

---

## Dependencies

- **Session 01 complete:** canonical artifacts in `data/atlas_qa/` are the retrieval substrate.
- **Session 02 complete:** deterministic routing, entity resolution, version resolution, response typing, and abstention states already exist and must be reused rather than reimplemented.
- **Existing abstention states:** `not_in_corpus`, `insufficient_evidence`, `ambiguous_entity`, `ambiguous_version`, `out_of_scope` are already defined and should be extended only if absolutely necessary.
- **Known Session 01 limitation:** `prerequisite_course_codes` is `[]` for all courses; do not design partition logic around unsupported structured prerequisite retrieval.

Do not begin implementation until Session 02’s definition of done is fully satisfied.

---

## Codex execution instructions

Read these files first, in this order:

1. `_internal/atlas_qa/WORK_SESSION_RULES.md`
2. `_internal/atlas_qa/work_sessions/03_scope_partitioning/SESSION_SPEC.md`
3. `_internal/atlas_qa/LOCAL_8B_RAG_SYSTEM_DESIGN.md`
4. `_internal/atlas_qa/PM_CONTEXT_PACKET.md`

Also inspect these implemented components before making changes:

5. `src/atlas_qa/qa/router.py`
6. `src/atlas_qa/qa/entity_resolution.py`
7. `src/atlas_qa/qa/version_resolution.py`
8. `src/atlas_qa/qa/loaders.py`
9. `src/atlas_qa/qa/lookup.py`
10. `src/atlas_qa/qa/types.py`
11. `src/atlas_qa/qa/source_authority.py`

Treat `WORK_SESSION_RULES.md` as the process control document and this `SESSION_SPEC.md` as the execution contract. The design doc and PM packet provide locked context; they do not authorize scope expansion.

### Required execution order

1. **Inspect the repo first**
   - Inspect the current `src/atlas_qa/qa/` layout and existing typed models, loaders, router behavior, entity/version resolution behavior, and lookup flow.
   - Identify where scope partitioning can be added cleanly without duplicating Session 02 logic.
   - Inspect current tests under `tests/atlas_qa/` or adjacent locations before creating new ones.

2. **Write a short implementation plan before editing**
   - Record a concise 5–10 bullet implementation plan in `DEV_LOG.md` before substantive code changes.
   - Include target files, intended typed outputs, validation approach, and any blockers discovered.

3. **Implement Session 03 only**
   - Define typed scope/partition objects.
   - Implement deterministic scope derivation.
   - Implement hard partition enforcement against canonical objects or candidate sets.
   - Implement explicit failure/abstention behavior when safe scope cannot be derived.
   - Add targeted tests.

4. **Run only the checks allowed by this spec**
   - Do not run broad repo-wide checks unless this session genuinely requires them.

5. **Update `DEV_LOG.md` before finishing**
   - Log implementation steps, files changed, checks run, results, and blockers/deviations.

### Do not

- Reopen design decisions
- Reinterpret source-authority policy
- Modify `src/app/`
- Modify `wgu-reddit` or any upstream repo
- Implement Session 04+ work in this pass
- Introduce LLM/model calls of any kind
- Implement retrieval ranking, BM25, embeddings, fusion, reranking, or answer synthesis here

### Final report requirement

At the end of the run, report:

- files created or updated
- checks run and outcomes
- whether Session 03 is complete, partial, or blocked
- exact scope object(s) and partition API introduced
- any small repo-layout recommendations, without applying unrelated cleanups

---

## In scope

- [ ] Define `PartitionInput` and typed partition output models
- [ ] Deterministic derivation of:
  - `entity_scope`
  - `version_scope`
  - `section_scope` only when explicitly supplied by structured upstream input; otherwise leave unspecified
  - `source_scope`
  - `compare_mode` flag or equivalent
- [ ] Hard partition enforcement: objects or candidates outside allowed scope are excluded before retrieval/context packing
- [ ] Partitioning behavior for exact-path-resolved queries: do not broaden beyond the resolved entity/version from Session 02
- [ ] Partitioning behavior for partially resolved queries: derive the narrowest safe scope available without guessing
- [ ] Explicit failure/abstention handling when safe partitioning cannot be established
- [ ] Typed handoff contract for Session 04 retrieval to consume
- [ ] Tests for wrong-version blocking, section leakage blocking, source-scope enforcement, and entity collision handling
- [ ] Deterministic handling of explicit compare intent only as a partition flag/input contract; do not implement compare retrieval or compare answers in this session

---

## Out of scope

- Fuzzy retrieval
- BM25, embedding, hybrid ranking, or reranking
- LLM-based classifier or routing
- Answer generation or answer phrasing
- Evidence-bundle construction beyond defining what the scoped retrieval contract must support
- Sufficiency/completeness gates beyond the minimum abstention/stop behavior required for unsafe scope
- Compare mode retrieval or compare answer generation
- App/UI changes
- Any redesign of Session 02 exact lookup behavior
- Heuristic or keyword-based section inference from raw NL query text

---

## Known behavior inherited from Session 02

- Exact identifiers are already intercepted by deterministic routing before broader retrieval logic.
- `route_and_lookup()` may return `out_of_scope` for all-alpha candidates that miss the corpus.
- Explicit versions are already enforced exactly in the exact/simple path.
- Deterministic anomaly/version-conflict disclosure already exists in exact/simple responses.

Session 03 must not conflict with or weaken any of the above. It should layer on a downstream partition contract, not redesign the upstream exact path.

---

## Architecture invariants (enforce in this path)

1. **Exact identifiers never start in semantic retrieval.** If Session 02 resolves an exact course/program identifier, Session 03 must not send that query into a broader unscoped retrieval flow first.
2. **Default retrieval is single-version only.** Partitioning must default to one resolved version per entity unless explicit compare intent is present.
3. **Mixed-version context is forbidden unless compare intent is explicit.** No silent blending of version-scoped artifacts.
4. **Partitioning is deterministic only.** No model may decide entity scope, version scope, source scope, or section scope.
5. **Hard scope must be enforced before retrieval/context packing.** Out-of-scope objects are discarded before downstream retrieval or evidence assembly.
6. **No broadening after exact resolution.** If Session 02 resolves a specific entity/version, Session 03 must preserve that scope rather than widening it.
7. **No source-policy drift.** Source scope must remain compatible with the locked source-authority policy.
8. **Unsafe scope must stop early.** If the system cannot safely derive scope, return an explicit abstention/partition failure rather than retrieving broadly.

---

## Expected implementation locations

| Concern | Suggested location |
|---|---|
| Scope/partition types | `src/atlas_qa/qa/types.py` |
| Scope derivation logic | `src/atlas_qa/qa/scope_partitioning.py` |
| Section/source scope policy helpers | `src/atlas_qa/qa/scope_policy.py` or `src/atlas_qa/qa/source_authority.py` |
| Coordinator / partition entry point | `src/atlas_qa/qa/coordinator.py` |
| Integration with lookup/resolution outputs | `src/atlas_qa/qa/coordinator.py` |
| Tests | `tests/atlas_qa/test_scope_partitioning.py` or similar |

Do not implement scope partitioning in `src/atlas_qa/llm/`. That module remains the LLM substrate only.

---

## Required typed outputs

Session 03 should introduce a typed output suitable for Session 04 retrieval to consume.

At minimum, the partition output should be capable of representing:

- resolved entity type
- resolved entity identifiers in scope
- resolved version identifiers in scope
- allowed source families in scope
- allowed section types in scope
- whether compare mode is active
- whether exact-path resolution was upstream input
- partition status / abstention reason
- notes or disclosures needed for downstream safe handling

Exact class names are flexible, but behavior is not.

---

## Source-scope requirements

Partitioning must respect the locked source-authority policy.

At minimum:

- catalog-default course description queries must not be widened to guide description defaults
- guide-only blocks (competencies, areas of study, capstone, cert-prep/program-cert sections) must be represented as guide-scoped
- version-conflicted programs must preserve separate version provenance rather than blending source families
- D554 guide description usage remains blocked
- C179 anomaly support must not be lost in downstream handling

This session does not generate answers, but it must preserve the conditions required for safe answers later.

---

## Section-scope requirements

Partitioning must support downstream restriction by section intent, including at minimum the ability to distinguish:

- course overview / description
- competencies
- capstone
- areas of study
- program description
- total CU / identity facts
- certification/licensure-related sections where supported

Do not guess missing section intent. In Session 03, raw NL text does not deterministically produce section scope. If section scope is not explicitly available from structured upstream input, preserve it as unspecified.

---

## Partition failure behavior

Session 03 should use explicit typed failure behavior when safe scope cannot be established.

Expected cases include:

- entity collision that cannot be safely narrowed
- version ambiguity that cannot be safely narrowed
- query requires section-level precision but section scope cannot be established safely
- source-family conflict where policy requires separation
- attempted mixed-version retrieval without explicit compare intent

Reuse existing abstention states where appropriate. Introduce a new typed partition-failure state only if existing states are insufficient and the need is concrete.

---

## Allowed checks

This spec explicitly permits:

- Repo inspection limited to files and directories relevant to this session
- Loading canonical artifacts from `data/atlas_qa/` and inspecting their structure locally
- Targeted test runs for scope derivation, partition enforcement, section/source/version filtering, and integration with Session 02 outputs
- Running scoped end-to-end checks against a small representative NL-oriented query set, provided no fuzzy retrieval or LLM calls are introduced
- Inspecting typed partition outputs locally

Not permitted without explicit session-level justification:

- app build runs
- broad repo-wide test suites
- BM25/embedding/fusion experiments
- LLM/model calls of any kind
- answer generation experiments
- checks outside `src/atlas_qa/`, `tests/atlas_qa/`, and the Atlas-local data inputs required by this session

---

## Definition of done

All must be true:

- [ ] A typed scope/partition contract exists for downstream retrieval
- [ ] Entity scope, version scope, source scope, and section scope are derived deterministically
- [ ] Objects outside hard scope are excluded before downstream retrieval/context packing
- [ ] Exact-path-resolved entity/version scope is preserved and not broadened
- [ ] Default partition behavior is single-version only
- [ ] Explicit compare intent is represented only as a partition flag/input contract, without enabling mixed-version retrieval by default
- [ ] Partition failure/abstention behavior is explicit and tested
- [ ] Tests cover wrong-version blocking, section leakage blocking, entity collision handling, source-scope enforcement, and attempted mixed-version retrieval without compare intent
- [ ] No LLM/model calls are introduced
- [ ] No cross-repo runtime dependency introduced
- [ ] `DEV_LOG.md` updated with actual work performed

---

## Edge cases

These must be covered by tests or explicit handling.

| Edge case | Required handling |
|---|---|
| Exact course code already resolved upstream | Preserve narrow course scope; do not widen |
| Exact program code already resolved upstream | Preserve narrow program/version scope; do not widen |
| All-alpha query that missed exact-path corpus resolution | Preserve `out_of_scope` behavior or pass only a safely narrowable unresolved context; do not reinterpret as a corpus miss automatically |
| Explicit version provided | Restrict version scope to that exact version only |
| No version provided | Restrict to most recent available version for the resolved entity |
| Attempted mixed-version retrieval without compare intent | Reject / abstain before retrieval |
| Version-conflicted programs (MACCA, MACCF, MACCM, MACCT, MSHRM) | Preserve source/version separation for downstream disclosure; do not blend |
| Query has explicit structured section scope for a guide-only block | Restrict source/section scope to the relevant guide family |
| Query appears to target catalog-default description/identity field | Restrict source scope to catalog-authoritative family by default |
| D554 guide description path | Must remain blocked |
| C179 course description path | Preserve anomaly-supporting metadata for downstream handling |

---

## Recommended implementation order

1. Inspect Session 01 and Session 02 typed models, router behavior, resolution behavior, and lookup flow.
2. Define `PartitionInput`, typed partition output, and coordinator entry point.
3. Implement deterministic scope derivation for entity/version/source and explicit section scope only.
4. Implement hard partition enforcement against canonical objects or candidate collections.
5. Integrate partitioning with upstream exact-path outputs without broadening them.
6. Add explicit partition failure behavior.
7. Add targeted tests and run only the checks allowed by this spec.

---

## Escalation rules

- If Session 03 appears to require fuzzy retrieval, classifier work, or answer generation to proceed, stop. That work belongs to later sessions.
- If existing abstention states are insufficient, log the concrete failure case before introducing a new typed state.
- If source-scope enforcement appears to conflict with the locked authority policy, stop and flag it. Do not reinterpret policy locally.
- If integration with Session 02 requires redesigning exact lookup behavior, stop and flag it. Do not redesign upstream behavior in this session.
- If a needed typed contract for Session 04 cannot be defined without reopening design questions, log the tradeoff and stop short of a design change.