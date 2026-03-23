# Session 04 — Fuzzy Retrieval

**Status:** Queued / after Session 03 complete  
**Intent:** Implementation  
**Dependency:** Session 03 (`03_scope_partitioning`) must be complete and passing before this session starts

## Session 03 dependency note

Session 04 assumes the deterministic control layer is already in place before retrieval begins.

By the time this session starts, the following must already exist and be treated as fixed upstream dependencies:

- Session 01 canonical artifacts in `data/atlas_qa/`
- Session 02 exact/simple deterministic path
- Session 03 typed partition/scope contract and hard partition enforcement

Session 04 must consume the typed scope/partition outputs from Session 03. It must not invent broader scope on its own, and it must not weaken upstream exact-path guarantees.

If Session 03 is incomplete, stop. Do not partially recreate scope partitioning inside retrieval code.

## LLM use

Session 04 is the first session that may use the LLM.

LLM use is allowed only for:

- structured intent/entity extraction for fuzzy queries that are not already handled by the exact path
- bounded, schema-validated outputs that help the retrieval layer construct a safe retrieval request
- short, bounded prompt/response checks needed to verify schema compliance and retrieval-oriented behavior

LLM use is not allowed for:

- source selection
- version arbitration
- scope partitioning
- conflict resolution against deterministic policy
- deciding absence claims
- freeform answering
- retrieval ranking by opaque model judgment
- long-running bulk evaluation loops inside Codex

### Reserved space for custom LLM instructions

Use this block to add or revise session-specific model instructions before implementation starts.

**Custom instructions for this session:**
- Default local model: `llama3:latest` via Ollama.
- Use deterministic settings for classifier calls (temperature effectively `0` or nearest supported equivalent).
- The model is used only for schema-bound fuzzy-query classification on the non-exact path.
- The classifier is advisory input only. It must not determine final entity resolution, final version resolution, final source scope, final section scope, or final answer content.
- Preferred classifier output fields in plain language:
  - `query_class_hint`
  - `entity_type_hint`
  - `entity_code_hint`
  - `explicit_version_hint`
  - `requested_section_hint`
  - `compare_intent`
  - `unsupported_or_advising`
  - `confidence_notes`
- If the model output is invalid, unparsable, schema-invalid, or low-utility, retrieval must fall back safely without broadening hard scope.
- Codex may run only short bounded classifier checks during implementation. Any larger prompt sweep, eval set, or long-running model job must be emitted as a manual operator-run command.

---

## Locked implementation decisions for this session

These decisions are settled for Session 04 and should not be redesigned during implementation:

1. **Session 04 does not own the control plane**
   - Session 04 consumes upstream routing, resolution, and partition outputs.
   - Retrieval must operate only within the hard scopes provided by Session 03.
   - Session 04 must not broaden entity/version/source/section scope.

2. **LLM outputs are untrusted until parsed and validated**
   - All model outputs used in this session must be schema-validated.
   - Parse failure, schema failure, and fallback behavior must be explicit and testable.

3. **The LLM is used only on the fuzzy path**
   - Exact identifiers must continue to bypass this session and stay on the deterministic exact/simple path from Session 02.
   - Session 04 may handle Class B/C fuzzy queries, but must not absorb Class A exact lookup behavior.

4. **Codex may run only short bounded LLM calls**
   - Codex may perform short-turn, limited validation calls explicitly allowed by this spec.
   - Codex must not launch long or bulk LLM jobs, large eval sweeps, or polling-heavy runs.
   - Any expensive or long-running LLM invocation must be emitted as a command for the operator to run manually.

5. **Retrieval quality is allowed to iterate, but only inside hard guardrails**
   - It is valid to optimize toward subjective goals like “best section match” or “best intent extraction behavior.”
   - That iteration must still respect deterministic scope, schema validation, bounded test size, and operator/manual boundaries for expensive runs.

6. **Retrieval substrate decisions**
   - Lexical retrieval for Session 04 uses `rank_bm25`.
   - Embedding retrieval for Session 04 uses a local sentence-transformers model.
   - Document embeddings are precomputed and stored under `data/atlas_qa/embeddings/`.
   - Query embeddings may be computed on demand.
   - Session 04 must not invent an alternate retrieval substrate without explicit owner approval.

---

## Objective

Implement the bounded fuzzy retrieval layer for NL queries. Given a query that is not handled by the exact/simple path, use a constrained structured classifier where needed, then retrieve candidate canonical objects only within the hard scopes established by Session 03.

**Query class taxonomy (reminder):** Class A = exact identifier lookup (handled by Session 02; never enters this session). Class B = single-entity factual NL lookup. Class C = section-grounded NL lookup.

This session should produce the retrieval layer that:

- supports Class B/C fuzzy lookup over canonical objects
- operates strictly inside entity/version/source/section scopes
- uses deterministic retrieval first within the scoped candidate pool
- adds BM25 and embedding-based candidate generation inside scope
- optionally fuses ranked candidate lists deterministically
- returns a small retrieval result suitable for later evidence-bundle construction
- fails closed when scope or retrieval sufficiency is unsafe

This session does **not** generate final answers.

---

## Why this session exists

Sessions 01–03 establish the canonical artifact layer, exact deterministic path, and hard partitioning/control-plane safeguards. Session 04 is the first retrieval session that must operate inside those safeguards.

The main system risk remains plausible, citation-bearing, wrong-version synthesis. Session 03 prevents unsafe scope. Session 04 must preserve that protection while enabling NL access to canonical objects.

This session is where NL retrieval becomes real, but still without opening answer generation.

---

## Dependencies

- **Session 01 complete:** canonical artifacts in `data/atlas_qa/` exist and are validated.
- **Session 02 complete:** exact identifiers and exact/simple deterministic lookup already work and must remain the front door for Class A queries.
- **Session 03 complete:** typed partition outputs and hard scope enforcement exist and must be consumed directly.
- **LLM substrate available:** `src/atlas_qa/llm/` and `src/atlas_qa/utils/` are already ported and verified.
- **Existing abstention states:** `not_in_corpus`, `insufficient_evidence`, `ambiguous_entity`, `ambiguous_version`, `out_of_scope` already exist and should be reused unless there is a concrete, necessary reason to extend them.
- **Known artifact limitations:** structured prerequisite support is still absent in canonical objects; retrieval must not pretend unsupported fields are covered.

Do not begin implementation until Session 03’s definition of done is fully satisfied.

---

## Codex execution instructions

Read these files first, in this order:

1. `_internal/atlas_qa/WORK_SESSION_RULES.md`
2. `_internal/atlas_qa/work_sessions/04_fuzzy_retrieval/SESSION_SPEC.md`
3. `_internal/atlas_qa/LOCAL_8B_RAG_SYSTEM_DESIGN.md`
4. `_internal/atlas_qa/PM_CONTEXT_PACKET.md`

Also inspect these implemented components before making changes:

5. `src/atlas_qa/qa/types.py`
6. `src/atlas_qa/qa/loaders.py`
7. `src/atlas_qa/qa/router.py`
8. `src/atlas_qa/qa/entity_resolution.py`
9. `src/atlas_qa/qa/version_resolution.py`
10. `src/atlas_qa/qa/lookup.py`
11. `src/atlas_qa/qa/source_authority.py`
12. `src/atlas_qa/qa/scope_partitioning.py`
13. `src/atlas_qa/qa/coordinator.py`
14. `src/atlas_qa/llm/client.py`
15. `src/atlas_qa/llm/registry.py`
16. `src/atlas_qa/llm/structured.py`
17. `src/atlas_qa/llm/types.py`
18. `src/atlas_qa/llm/artifacts.py`

Treat `WORK_SESSION_RULES.md` as the process control document and this `SESSION_SPEC.md` as the execution contract. The design doc and PM packet provide locked context; they do not authorize scope expansion.

### Required execution order

1. **Inspect the repo first**
   - Inspect Session 01–03 outputs and current `src/atlas_qa/qa/` layout.
   - Inspect current LLM substrate shape and structured parsing utilities.
   - Identify where the retrieval layer can be added cleanly without duplicating exact-path or scope-partition logic.
   - Inspect existing test locations before creating new ones.

2. **Write a short implementation plan before editing**
   - Record a concise 5–10 bullet implementation plan in `DEV_LOG.md`.
   - Include target files, intended retrieval interfaces, validation approach, short-turn LLM checks, and any blockers discovered.

3. **Implement Session 04 only**
   - Add the fuzzy-path structured classification interface if needed.
   - Add scoped retrieval over canonical objects.
   - Add deterministic candidate fusion/ranking logic if used.
   - Add typed retrieval outputs for later evidence construction.
   - Add explicit failure behavior and tests.

4. **Run only the checks allowed by this spec**
   - Use only short bounded LLM checks if model calls are necessary during implementation.
   - Do not launch large or long-running LLM jobs automatically.

5. **Update `DEV_LOG.md` before finishing**
   - Log implementation steps, files changed, checks run, LLM checks attempted, results, and blockers/deviations.
   - Clearly separate Codex-run LLM checks from operator-run manual commands.

### Do not

- Reopen design decisions
- Reinterpret source-authority policy
- Modify `src/app/`
- Modify `wgu-reddit` or any upstream repo
- Implement Session 05+ work in this pass
- Generate final answers in this session
- Let the model decide source/version/section scope
- Run large or long-polling LLM jobs inside Codex

### Final report requirement

At the end of the run, report:

- files created or updated
- checks run and outcomes
- which LLM checks were run by Codex
- which LLM commands were emitted for manual operator execution
- whether Session 04 is complete, partial, or blocked
- exact retrieval interfaces and typed outputs introduced
- any small repo-layout recommendations, without applying unrelated cleanups

---

## In scope

- [ ] Fuzzy-path intake for non-exact queries that fall outside Session 02 exact/simple handling
- [ ] Optional structured classifier for fuzzy queries, using schema-validated LLM output only where needed
- [ ] Retrieval request typing for downstream retrieval within Session 03 partition outputs
- [ ] Scoped retrieval over canonical artifacts:
  - `course_card`
  - `program_version_card`
  - `guide_section_card`
  - `version_diff_card` only where relevant to explicit compare preparation, not compare answering
- [ ] BM25-style lexical retrieval within the already-partitioned candidate space
- [ ] Embedding-based retrieval within the already-partitioned candidate space
- [ ] Deterministic fusion of lexical + embedding candidate lists if both are used
- [ ] Retrieval result typing suitable for later evidence-bundle construction
- [ ] Retrieval failure/sufficiency stop behavior when candidate quality is inadequate
- [ ] Targeted tests for wrong-version blocking, section leakage blocking, source-scope enforcement, classifier schema validation, and retrieval-scope enforcement
- [ ] Short bounded LLM validation calls for prompt/response shape if classifier integration is implemented

---

## Out of scope

- Final answer generation
- Final answer phrasing
- Compare-mode answer generation
- Open-ended multi-entity narrative synthesis
- Any broadening of Session 03 hard scope
- LLM-based source arbitration
- LLM-based version arbitration
- Negative-claim completeness decisions
- Long-running or bulk LLM evaluation loops inside Codex
- Repo-wide retrieval benchmarking sweeps unless explicitly approved as manual operator runs

---

## LLM execution policy for this session

This section is mandatory for Session 04.

### Codex may run directly

Only bounded, short-turn LLM calls such as:

- a few schema-validation checks for structured classifier output
- a few prompt/response sanity checks on representative fuzzy queries
- a few short latency calls to verify fallback and parse behavior
- a small, explicitly limited test batch where the session spec or implementation plan says this is required

### Codex must not run directly

- long-polling jobs
- large eval sweeps
- multi-minute or bulk prompt-comparison runs
- “optimize until best” jobs that require many model calls
- anything that is expected to sit and wait for a long time

### Manual operator-run boundary

If a larger LLM run would be useful, Codex must:

1. write the command
2. explain in `DEV_LOG.md` why it should be operator-run
3. stop short of executing it automatically

This boundary is part of the session contract.

---

## Architecture invariants (enforce in this path)

1. **Exact identifiers never start in fuzzy retrieval.** Session 02 exact lookup remains the entry path for exact IDs.
2. **Hard scope is upstream and binding.** Session 04 must operate only inside the scope supplied by Session 03.
3. **Default retrieval is single-version only.** No mixed-version retrieval unless compare intent is already explicit and upstream scope permits it.
4. **Model output is untrusted until validated.** Structured classifier output must be parsed, schema-validated, and safely fallbackable.
5. **No answer without evidence bundle.** Session 04 does not yet generate answers; it produces retrieval outputs to support later evidence bundling.
6. **No source-policy drift.** Retrieval must respect locked source-authority rules.
7. **No negative claim without completeness logic.** Session 04 must not infer unsupported absence claims from retrieval misses.
8. **Unsafe retrieval must fail closed.** If scoped retrieval cannot provide adequate support, return an explicit stop state rather than inventing coverage.

---

## Expected implementation locations

| Concern | Suggested location |
|---|---|
| Fuzzy query intake / retrieval request types | `src/atlas_qa/qa/types.py` |
| Structured classifier contract | `src/atlas_qa/qa/classifier.py` |
| Prompt contract / model-specific retrieval prompts | `src/atlas_qa/qa/prompts.py` or `src/atlas_qa/qa/classifier_prompts.py` |
| Retrieval orchestration | `src/atlas_qa/qa/retrieval.py` |
| Lexical retrieval | `src/atlas_qa/qa/retrieval_lexical.py` |
| Embedding retrieval | `src/atlas_qa/qa/retrieval_embedding.py` |
| Fusion / deterministic rank merge | `src/atlas_qa/qa/retrieval_fusion.py` |
| Integration with Session 03 coordinator/partition outputs | `src/atlas_qa/qa/coordinator.py` or a focused retrieval coordinator module |
| Retrieval result typing / stop states | `src/atlas_qa/qa/response.py` or `src/atlas_qa/qa/types.py` |
| Tests | `tests/atlas_qa/test_retrieval.py`, `tests/atlas_qa/test_classifier.py`, or similar |

Do not implement retrieval logic in `src/atlas_qa/llm/`. That module remains the generic model substrate only.

---

## Required typed outputs

Session 04 should introduce typed outputs suitable for Session 05 evidence-bundle construction and later answer generation.

At minimum, the retrieval output should be capable of representing:

- original user query
- normalized fuzzy retrieval request
- upstream partition/scope used
- classifier output, if any
- lexical candidates
- embedding candidates
- fused/ranked candidates
- selected scoped retrieval set
- retrieval stop/failure reason
- retrieval diagnostics needed for testing
- evidence-ref placeholders or source-object identities needed downstream

Exact class names are flexible, but behavior is not.

---

## Structured classifier requirements

If a classifier is implemented in this session, it must be narrow and schema-bound.

At minimum, it may extract only retrieval-relevant fields such as:

- likely entity type
- likely requested section
- explicit compare signal
- possible entity code mention
- possible explicit version mention
- whether the query appears to ask for unsupported/advising content

It must not decide:

- final entity resolution
- final version resolution
- final source scope
- final section scope when deterministic upstream scope disagrees
- final answer content

Classifier output is advisory input to retrieval request construction, not the control plane.

If a classifier is not needed for a first retrieval slice, that is acceptable. The session may start with deterministic fuzzy retrieval scaffolding and add the classifier only if required.

---

## Source-scope requirements

Retrieval must preserve the locked source-authority policy.

At minimum:

- catalog-default description/identity queries must not drift into guide-default answers
- guide-only blocks must stay guide-scoped
- version-conflicted programs must preserve per-source version provenance
- D554 guide description remains blocked
- C179 anomaly-supporting metadata must survive retrieval selection
- unsupported prerequisite absence claims must not be inferred from retrieval misses

This session does not generate answers, but it must preserve the conditions required for safe answers later.

---

## Retrieval sufficiency / stop behavior

Session 04 must have a bounded stop behavior when retrieval quality is clearly inadequate.

This is not the full Session 05 evidence-bundle or answerability system yet, but retrieval must still fail closed when:

- scoped candidate pool is empty
- scoped candidate pool is obviously off-section
- source-family restrictions leave no valid candidates
- retrieval cannot produce a credible small candidate set inside scope
- classifier output is unusable and no deterministic fallback exists

Use existing abstention/stop concepts where possible. Introduce a new retrieval-specific typed stop state only if it is concretely necessary.

---

## Allowed checks

This spec explicitly permits:

- Repo inspection limited to files and directories relevant to this session
- Loading canonical artifacts from `data/atlas_qa/` and inspecting their structure locally
- Targeted test runs for classifier schema validation, retrieval request construction, scoped lexical retrieval, scoped embedding retrieval, fusion, and integration with Session 03 outputs
- Running short, bounded LLM checks for schema-bound classifier validation and prompt sanity checks
- Running small representative fuzzy-query retrieval checks locally
- Inspecting retrieval outputs and ranked candidates locally

Not permitted without explicit session-level justification:

- app build runs
- broad repo-wide test suites
- long-polling or bulk LLM jobs
- large retrieval eval sweeps
- final answer generation experiments
- checks outside `src/atlas_qa/`, `tests/atlas_qa/`, and the Atlas-local data inputs required by this session

---

## Manual operator-run commands

This section exists because some useful LLM checks are too expensive or too slow for Codex to run directly.

If larger model runs are useful, Session 04 may include manual commands for:

- broader classifier evaluation sets
- larger retrieval-quality comparison runs
- prompt-comparison experiments across many queries
- latency-sensitive model comparison across different local models

These commands may be authored by Codex but must be run manually by the operator unless the session explicitly states a small bounded run is safe.

Codex should prefer dry-run or bounded settings where supported, and should avoid generating commands that imply indefinite waiting or unbounded polling.

---

## Definition of done

All must be true:

- [ ] Fuzzy retrieval path exists for non-exact queries without weakening Session 02 exact-path guarantees
- [ ] Retrieval operates only within Session 03 hard scopes
- [ ] Lexical and/or embedding retrieval inside scoped candidate space is implemented
- [ ] Any classifier output used in this session is schema-validated and safely fallbackable
- [ ] Retrieval outputs are typed and suitable for later evidence-bundle construction
- [ ] Wrong-version blocking is preserved under fuzzy retrieval
- [ ] Section leakage blocking is preserved under fuzzy retrieval
- [ ] Source-scope enforcement is preserved under fuzzy retrieval
- [ ] D554 guide-description blocking is preserved
- [ ] C179 anomaly-supporting metadata survives retrieval selection
- [ ] No final answers are generated in this session
- [ ] Only bounded short-turn LLM calls, if any, were run automatically by Codex
- [ ] Any larger LLM/eval jobs are emitted as manual operator commands instead of being auto-run
- [ ] No cross-repo runtime dependency introduced
- [ ] `DEV_LOG.md` updated with actual work performed

---

## Edge cases

These must be covered by tests or explicit handling.

| Edge case | Required handling |
|---|---|
| Exact course/program code query enters Session 04 | Must be routed away to Session 02 exact path rather than handled as fuzzy retrieval |
| All-alpha query that is ordinary English and not a corpus entity | Must preserve safe stop/out-of-scope behavior; do not force entity resolution |
| Fuzzy query references a guide-only section | Retrieval must remain guide-scoped if upstream scope says so |
| Fuzzy query references catalog-default description/identity behavior | Retrieval must remain catalog-scoped by default |
| Explicit version in fuzzy query | Retrieval must remain restricted to that exact version |
| No version in fuzzy query | Retrieval must stay single-version by default using upstream resolution/policy |
| Attempted mixed-version retrieval without compare intent | Must fail closed before broader retrieval |
| Version-conflicted programs (MACCA, MACCF, MACCM, MACCT, MSHRM) | Must preserve separate source/version provenance |
| D554 guide description path | Must remain blocked |
| C179 course description path | Must preserve anomaly-supporting metadata |
| Classifier returns invalid JSON / parse failure / schema failure | Must fallback safely and log the failure path |
| Classifier suggests out-of-scope/advising intent | Must stop safely rather than retrieving broadly |
| Scoped candidate pool is empty | Must return explicit stop behavior rather than inventing candidates |

---

## Recommended implementation order

1. Inspect Sessions 01–03 typed models, canonical artifacts, exact-path behavior, and scope-partition outputs.
2. Define fuzzy retrieval request types, retrieval result types, and retrieval stop behavior.
3. Implement a minimal scoped lexical retrieval slice first (BM25 only, no classifier yet).
4. Add embedding retrieval inside the same hard scopes once lexical slice is working.
5. Add deterministic fusion only if it materially improves the bounded retrieval slice.
6. Add the narrow schema-bound classifier after the deterministic retrieval slices work on their own — the classifier is advisory shaping only, not a prerequisite for retrieval.
7. Add targeted tests for wrong-version blocking, section leakage, source-scope enforcement, and classifier validation.
8. Add only short bounded LLM checks; emit larger useful runs as operator commands instead of executing them automatically.

---

## Escalation rules

- If Session 04 appears to require widening or reinterpreting Session 03 hard scope, stop and flag it.
- If retrieval seems to require final answer generation to be testable, stop. That belongs to a later session.
- If classifier behavior begins to act like routing/control-plane logic, stop and narrow it.
- If large model runs seem necessary for meaningful evaluation, emit manual operator commands and do not execute them automatically.
- If source-authority enforcement appears to conflict with retrieval behavior, stop and flag it rather than weakening policy locally.
- If a retrieval result contract for later evidence-bundle construction cannot be defined without reopening design questions, log the tradeoff and stop short of a design change.