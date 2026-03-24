# Session 07 — Runtime Validation and Observability

**Status:** Ready to activate  
**Intent:** Implementation  
**Dependency:** Session 06 (`06_compare_and_eval`) must be complete before this starts

---

## Naming note

This session follows the now-established work-session structure:

- `05_evidence_and_generation/`
- `06_compare_and_eval/`
- `07_runtime_validation/`

Like Sessions 05 and 06, this session should use only:
- `SESSION_SPEC.md`
- `DEV_LOG.md`

No additional session docs should be created unless a real blocker requires them.

---

## Purpose

Run a small, real, end-to-end validation pass through the Atlas QA pipeline using live Ollama, and add enough structured trace/verbose output that pipeline behavior can be inspected without guesswork.

This session is not about expanding architecture.  
It is about proving the implemented system works under real runtime conditions and making failures diagnosable.

---

## Why this session exists

Sessions 01–06 implemented the full planned v1 stack:

- canonical objects
- exact lookup path
- scope partitioning
- fuzzy retrieval
- evidence bundle construction
- deterministic answerability gate
- constrained generation
- post-check
- compare mode
- eval harness
- launch-gate measurement plumbing

What is still missing is a **live-runtime pass** through the real local model using representative queries, with trace visibility across:

- routing
- resolution
- scope control
- retrieval
- evidence bundle construction
- gating
- generation
- post-check
- final outcome

Without this session, the system is heavily tested but still under-validated in real end-to-end mode.

---

## Objective

1. Run the real Atlas QA pipeline end to end against a small representative query sample using live Ollama.
2. Add a bounded verbose/debug mode that exposes internal pipeline decisions per query.
3. Save runtime traces and results as Atlas-local artifacts.
4. Identify any immediate runtime blockers before broader eval execution.

---

## LLM use policy

This session must use the real local Ollama-backed answer path already built in Atlas.

Allowed model use:
- the existing classifier path when the pipeline invokes it
- the existing constrained answer-generation path
- the existing compare-generation path for explicit compare cases

Disallowed model use:
- bypassing control-layer logic to “make answers work”
- ad hoc interactive prompt experimentation as a substitute for the real pipeline
- changing source authority, version scope, or anomaly handling inside prompts
- introducing new free-form generation behavior outside the existing system design

The purpose is to validate the real system, not to improvise a new one.

---

## Locked implementation decisions

1. This session validates the existing runtime pipeline; it does not redesign it.
2. The live model must be exercised through the same code paths used by Atlas QA, not through one-off prompt calls.
3. Verbose/debug output must reflect control-layer state, not only final answer text.
4. Failures must be recorded explicitly and not masked by fallback prose.
5. Runtime artifacts must be written locally in Atlas for later audit.
6. The query sample must include answer, abstain, clarify, compare, and anomaly/conflict cases.

---

## Dependencies

Must already exist and be stable:
- Session 01 canonical objects
- Session 02 exact lookup path
- Session 03 scope partitioning
- Session 04 fuzzy retrieval
- Session 05 evidence/generation/post-check
- Session 06 compare/eval harness
- `_internal/atlas_qa/QA_GOLD_QUESTION_SET.md`

Read first:
- `_internal/atlas_qa/LOCAL_8B_RAG_SYSTEM_DESIGN.md`
- `_internal/atlas_qa/QA_GOLD_QUESTION_SET.md`
- `_internal/atlas_qa/work_sessions/05_evidence_and_generation/SESSION_SPEC.md`
- `_internal/atlas_qa/work_sessions/05_evidence_and_generation/DEV_LOG.md`
- `_internal/atlas_qa/work_sessions/06_compare_and_eval/SESSION_SPEC.md`
- `_internal/atlas_qa/work_sessions/06_compare_and_eval/DEV_LOG.md`

---

## In scope

### Live end-to-end runs
- run the real pipeline against a small representative query sample using live Ollama
- exercise exact, section-grounded, compare, abstain, clarify, and anomaly/conflict paths

### Runtime observability
- add a structured verbose/debug mode
- ensure the trace shows control-layer decisions and final outcomes

### Runtime artifacts
- save per-query runtime traces/results
- save one session-level summary artifact

### Small operational checks
- verify the real model path is callable from the current runtime environment
- verify generation outputs survive schema validation and post-check in real runs

---

## Out of scope

- broad architecture changes
- source-authority policy changes
- prompt redesign except for surgical runtime-blocker fixes
- UI work
- full 100-question evaluation run
- launch decision
- post-v1 feature work

---

## Required live query sample

At minimum, run representative queries covering these classes:

### Exact lookup
- `What is D426?`
- `How many CUs is BSACC?`

### Single-entity factual
- `What is the capstone for BSDA?`

### Section-grounded
- `What competencies are listed for C949?`

### Compare
- `How does D335 compare with D522?`

### Ambiguity / clarify
- `What courses are in the MBA program?`

### Abstain / out-of-scope
- `Which WGU class is easiest?`

### Known anomaly / conflict
- `Tell me about C179`
- `Tell me about D554`
- `What is the current version of MSHRM?`

Additional queries are allowed, but keep the session bounded.

---

## Architecture invariants

1. All real runs must pass through the existing deterministic control layer.
2. Exact/simple queries must not be diverted into uncontrolled fuzzy behavior.
3. Compare mode activates only on explicit compare intent.
4. Version scope remains locked before retrieval.
5. Source authority remains enforced exactly as currently designed.
6. Ambiguous queries must clarify or abstain, not guess.
7. Anomaly/conflict disclosures must survive to final output where required.
8. Runtime validation must distinguish:
   - answer
   - abstain
   - clarify
   - failure

---

## Expected implementation locations

Atlas-local only.

Likely code locations:
- `src/atlas_qa/qa/` for runtime validation runner / trace support
- `data/atlas_qa/runtime_checks/session07/` for saved runtime artifacts
- tests adjacent to existing QA modules only if a very small amount of support testing is needed

Do not broaden beyond the minimum required for runtime validation and observability.

---

## Required typed/runtime outputs

Session 07 should produce or use deterministic runtime artifacts that capture, per query:

- raw query
- query class / routed path
- classifier result if invoked
- resolved entity/entity type
- resolved version(s)
- source scope
- section scope if relevant
- compare mode status
- anomaly/conflict flags
- retrieved/selected evidence artifact identifiers
- excluded evidence and exclusion reason where available
- evidence bundle summary
- answerability gate result
- generation invoked or not
- post-check result
- final outcome (`answer` | `abstain` | `clarify` | `failure`)

These do not need new public schemas if existing typed outputs can be reused, but the runtime output must be structured and inspectable.

---

## Verbose/debug requirements

Verbose mode must expose, for each query:

1. raw query
2. routed path / query class
3. classifier output and parse/schema status (if classifier used)
4. entity resolution result
5. version resolution result
6. source scope
7. section scope
8. compare mode status
9. anomaly/conflict flags present before generation
10. top evidence selected
11. evidence excluded and why (if available)
12. evidence bundle composition
13. answerability gate result
14. whether generation was invoked
15. prompt type used (`answer` / `compare`)
16. post-check result
17. final outcome and short reason

This can be JSON or another structured machine-readable format.
It does not need polished presentation.

---

## Runtime artifact requirements

Suggested output location:
- `data/atlas_qa/runtime_checks/session07/`

At minimum write:
- one per-query runtime trace/result artifact
- one session summary artifact

The session summary should include:
- exact queries run
- counts by final outcome
- major failure categories
- any immediate blockers before broader eval

---

## Deterministic rules

1. Use the real local Ollama-backed pipeline, not mocked generation.
2. Do not manually edit outputs to make them pass.
3. Do not silently widen scope or relax gates because a query fails.
4. If the system abstains or clarifies correctly, record that as success.
5. If a query fails due to runtime/model behavior, preserve the trace.
6. If a prompt/runtime bug is found, fix only if surgical and clearly within scope; otherwise log it as a blocker.

---

## Required validation behavior

This session must confirm, in real runtime conditions, that the system can handle at least:

- one exact answer case
- one single-entity factual answer case
- one section-grounded answer case
- one explicit compare case
- one ambiguity/clarify case
- one abstain case
- one anomaly/conflict-disclosure case

The goal is not broad coverage.  
The goal is to prove the real stack behaves coherently across the main behavior classes.

---

## Definition of done

This session is complete when:

1. a representative live query sample has been run through the full pipeline using real Ollama
2. verbose/debug mode exists and is usable
3. structured runtime traces are written locally
4. at least one compare, one abstain, one ambiguity, and one anomaly/conflict case are included
5. major runtime failures are captured with enough context to diagnose them
6. `DEV_LOG.md` records:
   - exact queries run
   - runtime environment/model used
   - outputs written
   - passes/failures by class
   - next actions

---

## Edge cases to watch

- ambiguous entity resolved incorrectly instead of clarify
- compare path failing to disclose both versions
- version conflict programs omitting disclosure
- anomaly cases losing their flags between evidence bundle and final response
- post-check rejecting otherwise good live outputs due to overly brittle formatting assumptions
- classifier producing valid but weak hints that lead to wrong entity scope
- real model failing schema more often than mocked tests suggested

---

## Recommended implementation order

1. Add or confirm a runtime validation entrypoint/runner.
2. Add structured verbose/debug trace support.
3. Wire runtime artifact output path.
4. Run a minimal live sample (2–3 queries) to confirm the runner works.
5. Run the full bounded Session 07 sample.
6. Inspect failures and categorize them.
7. Write session summary artifacts.
8. Update `DEV_LOG.md`.

---

## Escalation rules

Escalate instead of guessing if:
- the real model repeatedly fails a prompt contract in a way that suggests design-level prompt issues
- compare mode requires policy not present in current docs
- ambiguity/clarify behavior is under-specified for a live failure
- anomaly/conflict handling appears inconsistent between control layer and final response
- runtime output format conflicts with existing typed output expectations

Do not silently patch policy during runtime validation.

---

## Codex execution instructions

Read first:
- `_internal/atlas_qa/LOCAL_8B_RAG_SYSTEM_DESIGN.md`
- `_internal/atlas_qa/QA_GOLD_QUESTION_SET.md`
- `_internal/atlas_qa/work_sessions/05_evidence_and_generation/SESSION_SPEC.md`
- `_internal/atlas_qa/work_sessions/06_compare_and_eval/SESSION_SPEC.md`

Implement:
- a small runtime validation runner or equivalent entrypoint
- structured verbose/debug tracing
- a bounded representative query sample
- saved runtime-check artifacts

Use real Ollama through the existing Atlas QA pipeline.
Do not broaden scope.
Update only the canonical Session 07 `DEV_LOG.md`.

Output back:
1. exact files created/updated
2. exact queries run
3. what verbose/debug mode shows
4. where runtime artifacts were written
5. major failures or blockers found
6. confirmation that `DEV_LOG.md` was updated