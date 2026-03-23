# Session 05 — Evidence Bundle, Answerability Gate, Constrained Generation, Post-Check

**Status:** Queued / after Session 04 complete
**Intent:** Implementation
**Dependency:** Sessions 01–04 must be complete and passing before this session starts

---

## Folder note

The previous `05_compare_and_eval` folder held a stale stub spec that described Session 01
(canonical object generation) work. That folder has been renamed to `06_compare_and_eval`
where compare mode and the eval harness will live. This is the correct Session 05 spec.

---

## Session 04 dependency note

Session 05 takes `RetrievalResult` from Session 04 as its primary input. The following must
already exist and be treated as fixed upstream dependencies:

- Session 01 canonical artifacts in `data/atlas_qa/`
- Session 02 exact/simple deterministic path
- Session 03 typed partition/scope contract and hard partition enforcement
- Session 04 `RetrievalResult` with typed selected_candidates, stop_reason, and diagnostics

Session 05 must not reimplement retrieval logic, re-derive scope, or re-run the classifier.
It consumes the typed outputs of Sessions 02–04 and builds the answer layer on top of them.

If Session 04 is incomplete or its typed outputs are missing, stop. Do not recreate retrieval
or scope-partitioning inside this session.

---

## LLM use

Session 05 is the first session that uses the LLM for **constrained answer generation** (not
just classification). This is a meaningfully different use than Session 04's advisory
classifier.

LLM use is allowed only for:

- constrained surface realization of a pre-assembled, pre-validated evidence bundle
- the LLM receives only vetted evidence artifacts and a strict prompt contract
- it must cite the evidence IDs it uses, state the version, and abstain if the evidence is
  insufficient

LLM use is not allowed for:

- source selection
- version arbitration
- scope broadening
- deciding answerability or sufficiency (those gates are deterministic)
- deciding absence claims
- choosing which evidence artifacts to include in the bundle
- post-check verification (that is deterministic)
- reranking or reordering evidence
- any role in the control plane

### Custom instructions for this session

- Default local model: `llama3:latest` via Ollama.
- Use deterministic settings for generation calls (temperature effectively `0`).
- The prompt contract is strict: provide only the pre-assembled evidence bundle. The model
  must not be asked to search, reason across sources, or fill gaps.
- Generation output must be schema-validated before use.
- If the model output is invalid, unparsable, or schema-invalid, the answer path must
  abstain rather than emit an unchecked response.
- Codex may run only short bounded generation checks during implementation. Any larger
  generation quality sweep must be emitted as a manual operator-run command.

---

## Locked implementation decisions for this session

1. **Session 05 does not own the control plane**
   The upstream retrieval result, partition scope, and entity/version resolution are fixed
   inputs. Session 05 must not re-derive, broaden, or override any upstream decision.

2. **The answerability gate is deterministic**
   The sufficiency/answerability check must be a deterministic function over the evidence
   bundle — not a model call. It checks for: non-empty bundle, version coverage, section
   match, completeness flags. If the gate fails, the answer path returns an abstention state.

3. **Evidence bundle construction is deterministic**
   The evidence bundle is assembled from Session 04's typed `selected_candidates` using
   deterministic field extraction from canonical objects. The LLM never selects which
   candidates to include.

4. **Generation is constrained and post-checked**
   The LLM receives a strict prompt contract. Its output is schema-validated. The post-check
   is then a deterministic structural check (citation IDs present, version token present,
   schema compliance). Post-check failure triggers abstention, not retry.

5. **Exact-path queries may also reach generation**
   Class A exact queries (Session 02) produce `ExactLookupAnswer` objects with all needed
   evidence. Session 05 should support assembling an evidence bundle from an
   `ExactLookupAnswer` as well as from a `RetrievalResult`. Both should be passable to the
   same generation and post-check path.

6. **No compare mode in this session**
   Class D (explicit version comparison) belongs to Session 06. Session 05 handles
   single-entity queries (Class A, B, C) only. If a compare-mode retrieval result is
   passed in, Session 05 must reject it rather than attempt mixed-version generation.

7. **Codex may run only short bounded LLM calls**
   Short sanity checks on generation output shape, citation presence, and abstention
   behavior are permitted. Larger generation quality sweeps must be emitted as manual
   operator commands.

---

## Objective

Build the first complete end-to-end single-entity QA answer path. Given a typed
`RetrievalResult` (or `ExactLookupAnswer` from the exact path), produce a typed `QAResponse`
that either contains a grounded, citation-bearing answer or an explicit abstention state.

This session should produce:

- evidence bundle construction from typed retrieval results
- a deterministic answerability / sufficiency gate
- a constrained generation call with a strict prompt contract
- a deterministic post-check for citation presence, version disclosure, and schema compliance
- typed `QAResponse` output suitable for final display or downstream use
- explicit abstention at every failure mode

This session does **not** implement compare mode or the eval harness. Those belong to
Session 06.

---

## Why this session exists

Sessions 01–04 produce canonical artifacts, exact lookup, scope partitioning, and a typed
retrieval result. Session 05 closes the loop by building the answer layer on top of those
outputs. Without it, the system can retrieve but cannot answer.

The primary risk remains: plausible, citation-bearing, wrong-version synthesis. Sessions
03–04 prevent unsafe scope at retrieval time. Session 05 must preserve those protections at
generation time: the prompt contract must supply only scoped evidence, and the post-check
must verify that the output respects the evidence boundary.

---

## Dependencies

- **Session 01 complete:** canonical artifacts in `data/atlas_qa/` exist and are validated.
- **Session 02 complete:** `ExactLookupAnswer` and `ExactLookupResponse` are the typed
  output of the exact path and must be consumable by the evidence bundle assembler.
- **Session 03 complete:** `PartitionResult` is fixed upstream scope; used to verify
  answerability gate context.
- **Session 04 complete:** `RetrievalResult` with `selected_candidates` and `stop_reason`
  is the primary input to evidence bundle construction.
- **LLM substrate available:** `src/atlas_qa/llm/` is already ported and verified.
- **Abstention states:** `not_in_corpus`, `insufficient_evidence`, `ambiguous_entity`,
  `ambiguous_version`, `out_of_scope` already exist. The gate should reuse them.

---

## Codex execution instructions

Read these files first, in this order:

1. `_internal/atlas_qa/WORK_SESSION_RULES.md`
2. `_internal/atlas_qa/work_sessions/05_evidence_and_generation/SESSION_SPEC.md`
3. `_internal/atlas_qa/LOCAL_8B_RAG_SYSTEM_DESIGN.md` §§ 12–13 (context construction,
   answerability/abstention)
4. `_internal/atlas_qa/PM_CONTEXT_PACKET.md`

Also inspect these implemented components before making changes:

5. `src/atlas_qa/qa/types.py`
6. `src/atlas_qa/qa/retrieval.py`
7. `src/atlas_qa/qa/retrieval_lexical.py` (for RetrievalCandidate field shapes)
8. `src/atlas_qa/qa/scope_partitioning.py`
9. `src/atlas_qa/qa/coordinator.py`
10. `src/atlas_qa/qa/lookup.py`
11. `src/atlas_qa/qa/response.py`
12. `src/atlas_qa/llm/client.py`
13. `src/atlas_qa/llm/structured.py`
14. `src/atlas_qa/llm/types.py`
15. `tests/atlas_qa/test_retrieval.py` (for fixture patterns)

Treat `WORK_SESSION_RULES.md` as the process control document and this `SESSION_SPEC.md`
as the execution contract.

### Required execution order

1. **Inspect the repo first**
   - Inspect Session 01–04 typed outputs.
   - Identify the full shape of `RetrievalResult`, `ExactLookupAnswer`, and
     `PartitionResult` before writing any new types.
   - Identify all existing abstention states and reuse them.
   - Inspect existing test fixtures before creating new ones.

2. **Write a short implementation plan before editing**
   - Record a concise 5–10 bullet plan in `DEV_LOG.md`.
   - Include: target files, evidence bundle interface, gate interface, prompt contract,
     post-check approach, short-turn LLM checks, and any blockers.

3. **Implement Session 05 only**
   - Evidence bundle construction from `RetrievalResult` or `ExactLookupAnswer`.
   - Deterministic answerability gate.
   - Constrained generation with strict prompt contract.
   - Deterministic post-check.
   - Typed `QAResponse` output.
   - Explicit failure/abstention at every stop point.

4. **Run only the checks allowed by this spec**
   - Short bounded LLM checks if model calls are necessary during implementation.
   - Do not launch large or long-running LLM jobs automatically.

5. **Update `DEV_LOG.md` before finishing**
   - Log implementation steps, files changed, checks run, LLM checks attempted, results,
     blockers/deviations.
   - Clearly separate Codex-run LLM checks from operator-run manual commands.

### Do not

- Reopen design decisions
- Modify `src/app/`
- Implement Session 06 work (compare mode, eval harness, launch gates)
- Let the model decide source, version, or evidence selection
- Run large or long-polling LLM jobs inside Codex
- Re-derive scope or re-run the classifier
- Produce a compare-mode answer

### Final report requirement

At the end of the run, report:

- files created or updated
- checks run and outcomes
- which LLM checks were run by Codex
- which LLM commands were emitted for manual operator execution
- whether Session 05 is complete, partial, or blocked
- exact interfaces introduced (evidence bundle, gate, generation, post-check, QAResponse)
- any small repo-layout recommendations, without applying unrelated cleanups

---

## In scope

- [ ] Evidence bundle construction from `RetrievalResult.selected_candidates`
- [ ] Evidence bundle construction from `ExactLookupAnswer` (exact path)
- [ ] Deterministic answerability / sufficiency gate
- [ ] Constrained LLM generation with strict prompt contract
- [ ] Schema-validated generation output
- [ ] Deterministic post-check (citation IDs present, version token present, schema valid)
- [ ] Typed `QAResponse` output (answer or abstention, with evidence refs and version disclosure)
- [ ] Explicit abstention at every failure mode
- [ ] Tests for gate failures, generation schema failures, post-check failures, abstention
      propagation, citation presence enforcement, version token enforcement

---

## Out of scope

- Compare mode (Class D queries) — Session 06
- `version_diff_card` generation path — Session 06
- Eval harness and launch gates — Session 06
- Multi-entity narrative synthesis
- Any broadening of Session 03/04 scope guarantees
- LLM-based evidence selection
- LLM-based source arbitration
- LLM-based version arbitration
- Negative-claim completeness logic beyond what already exists
- Long-running or bulk LLM evaluation loops inside Codex
- Cross-repo runtime dependencies

---

## Architecture invariants (enforce in this path)

1. **No answer without an evidence bundle.** If the bundle is empty or fails the gate,
   the answer path must return an abstention state.
2. **The answerability gate is deterministic.** No model call may substitute for or
   override the gate.
3. **The LLM receives only vetted evidence.** The prompt must contain only the pre-assembled
   bundle. The model must not be given the full corpus or asked to search for additional
   information.
4. **Post-check is deterministic.** Citation ID presence, version token presence, and
   schema compliance are checked structurally — not by asking the model to verify itself.
5. **Post-check failure triggers abstention.** Do not emit a partially-checked answer.
6. **Version token must appear in the answer.** Every non-abstained answer must include
   the version of the source used.
7. **Compare mode must be rejected.** If a compare-mode retrieval result or partition enters
   Session 05, return an abstention rather than attempting mixed-version generation.
8. **Source-policy drift is not permitted.** The evidence bundle must respect locked
   source-authority rules. A generation prompt must not ask the model to reason across
   catalog and guide content as if they were interchangeable.

---

## Expected implementation locations

| Concern | Suggested location |
|---|---|
| Evidence bundle types | `src/atlas_qa/qa/types.py` |
| Evidence bundle construction | `src/atlas_qa/qa/evidence.py` |
| Answerability / sufficiency gate | `src/atlas_qa/qa/gate.py` |
| Generation prompt contract | `src/atlas_qa/qa/generation_prompts.py` |
| Constrained generation | `src/atlas_qa/qa/generation.py` |
| Post-check | `src/atlas_qa/qa/postcheck.py` |
| QAResponse / final typed output | `src/atlas_qa/qa/types.py` |
| End-to-end orchestration (optional thin wrapper) | `src/atlas_qa/qa/answer.py` |
| Tests | `tests/atlas_qa/test_evidence.py`, `tests/atlas_qa/test_gate.py`,
           `tests/atlas_qa/test_generation.py`, `tests/atlas_qa/test_postcheck.py` |

Do not implement answer logic in `src/atlas_qa/llm/`. That module remains the generic model
substrate only.

---

## Required typed outputs

At minimum, Session 05 must introduce:

### `EvidenceBundle`
- `entity_code`: str
- `entity_type`: EntityType
- `version_used`: str
- `source_scope`: list[SourceFamily]
- `artifacts`: list[EvidenceArtifact]     # 2–5 items for single-entity
- `anomaly_disclosures`: list[AnomalyDisclosure]
- `notes`: list[str]                       # carries upstream scope notes
- `from_exact_path`: bool

### `EvidenceArtifact`
- `artifact_type`: one of the four canonical object types
- `entity_code`: str
- `version`: str
- `source_family`: SourceFamily
- `content`: dict | str                    # the canonical object fields used
- `source_object_identity`: str
- `evidence_ref`: EvidenceRef

### `AnswerabilityResult`
- `answerable`: bool
- `abstention_reason`: AbstentionState | None
- `gate_notes`: list[str]

### `GenerationOutput`
- `raw_text`: str
- `answer_text`: str | None                # extracted from raw_text after validation
- `cited_evidence_ids`: list[str]
- `version_disclosed`: str | None
- `parse_error`: bool
- `schema_error`: bool
- `llm_failure`: bool

### `PostCheckResult`
- `passed`: bool
- `citation_ids_present`: bool
- `version_token_present`: bool
- `schema_valid`: bool
- `failure_reasons`: list[str]

### `QAResponse`
- `raw_query`: str
- `entity_code`: str | None
- `entity_type`: EntityType | None
- `version_used`: str | None
- `abstention`: AbstentionState | None
- `answer_text`: str | None
- `evidence_bundle`: EvidenceBundle | None
- `generation_output`: GenerationOutput | None
- `postcheck`: PostCheckResult | None
- `diagnostics`: dict

Exact class names are flexible, but behavior is not.

---

## Evidence bundle requirements

- Bundle must be assembled from `RetrievalResult.selected_candidates` (fuzzy path) or from
  an `ExactLookupAnswer` (exact path). No other inputs.
- Maximum 5 artifacts for single-entity queries. Minimum 1 to proceed past the gate.
- Each artifact must carry: artifact_type, entity_code, version, source_family,
  source_object_identity, and the content fields used.
- Upstream anomaly disclosures (C179 short-text, D554 guide block, version-conflict notes)
  must be preserved in the bundle and passed through to the final response.
- Compare-mode bundles (multi-version) must be rejected at bundle construction time.

---

## Answerability gate requirements

The gate is a deterministic function over the `EvidenceBundle`. It must check:

1. Bundle is non-empty
2. At least one artifact matches the resolved entity code
3. Version coverage: all artifacts are within the resolved version scope
4. If a section scope is required (e.g., competencies), at least one guide section card
   artifact is present for that section type
5. No unresolvable conflict flag that blocks this query type (e.g., D554 guide block when
   guide content was requested)
6. Compare mode is not present (single-entity session only)

Failure at any check returns `AnswerabilityResult(answerable=False, abstention_reason=...)`.

---

## Generation prompt contract

The prompt must:

1. Supply only the pre-assembled evidence artifacts — no raw corpus, no unvetted text
2. Instruct the model to cite the `source_object_identity` of each artifact it uses
3. Instruct the model to state the version used in its answer
4. Instruct the model to abstain rather than guess if evidence is insufficient
5. Not instruct the model to search, infer, or reason beyond the provided artifacts
6. Not ask the model to resolve version conflicts or choose sources
7. Be short enough for an 8B model to handle reliably (target: fit in ~2K tokens of context)

The prompt contract must be a standalone string template — no logic embedded in the template
itself. Logic lives in `generation.py`, not in the prompt string.

---

## Post-check requirements

Post-check is deterministic and must verify:

1. **Citation IDs present:** at least one `source_object_identity` from the bundle appears
   in the answer text (or in the `cited_evidence_ids` field of the parsed output)
2. **Version token present:** the version string used (from `EvidenceBundle.version_used`)
   appears somewhere in the answer text
3. **Schema valid:** the parsed `GenerationOutput` validates against its Pydantic schema

If any check fails, `PostCheckResult.passed = False` and the `QAResponse` must carry an
abstention state rather than the unchecked answer text.

---

## Retrieval sufficiency / stop behavior

Session 05 must fail closed at every gate:

| Failure point | Behavior |
|---|---|
| `RetrievalResult.stop_reason` is set | Propagate stop, return abstention |
| `RetrievalResult.selected_candidates` is empty | `insufficient_evidence` abstention |
| Bundle construction produces empty bundle | `insufficient_evidence` abstention |
| Answerability gate fails | Return gate's `abstention_reason` |
| LLM call fails | `insufficient_evidence` abstention (do not retry in answer path) |
| Generation output parse/schema error | `insufficient_evidence` abstention |
| Post-check fails | `insufficient_evidence` abstention |
| Compare mode detected | `out_of_scope` abstention |

---

## Allowed checks

- Repo inspection limited to files and directories relevant to this session
- Loading canonical artifacts from `data/atlas_qa/` and inspecting structure locally
- Targeted test runs for evidence bundle construction, gate logic, generation schema
  validation, and post-check enforcement
- Running short bounded LLM generation checks for prompt contract shape and citation
  enforcement
- Inspecting `QAResponse` outputs locally

Not permitted without explicit justification:

- app build runs
- broad repo-wide test suites
- long-polling or bulk LLM jobs
- large generation quality sweeps
- checks outside `src/atlas_qa/`, `tests/atlas_qa/`, and Atlas-local data inputs

---

## Manual operator-run commands

If larger generation quality runs are useful, emit manual commands for:

- multi-query generation quality sweeps
- citation coverage audits across a representative query set
- latency measurement across model variants

These must be authored but not auto-executed.

---

## Definition of done

All must be true:

- [ ] Evidence bundle construction works from both `RetrievalResult` and `ExactLookupAnswer`
- [ ] Deterministic answerability gate is implemented and tested
- [ ] Constrained generation call is implemented with strict prompt contract
- [ ] Generation output is schema-validated before use
- [ ] Post-check is deterministic and enforced before any answer is emitted
- [ ] `QAResponse` is typed and carries answer text, abstention state, evidence bundle,
      and version disclosure
- [ ] Every failure mode returns an explicit abstention state
- [ ] Compare mode is rejected at the bundle or gate level
- [ ] C179 and D554 anomaly disclosures survive to `QAResponse`
- [ ] Version-conflict program disclosures survive to `QAResponse`
- [ ] No final answer is emitted without a passing post-check
- [ ] Only bounded short-turn LLM calls, if any, were run automatically by Codex
- [ ] Any larger LLM/eval jobs are emitted as manual operator commands
- [ ] No cross-repo runtime dependency introduced
- [ ] `DEV_LOG.md` updated with actual work performed

---

## Edge cases

| Edge case | Required handling |
|---|---|
| `RetrievalResult.stop_reason` is set | Propagate — do not attempt generation |
| `selected_candidates` is empty | `insufficient_evidence` abstention |
| All candidates are from wrong version | Gate fails — `insufficient_evidence` |
| Section scope required but no guide section artifact | Gate fails — `insufficient_evidence` |
| D554 guide content requested | Gate fails — surface D554 guide block note |
| C179 short-text present | Pass through anomaly disclosure in `QAResponse` |
| Version-conflict program (MACCA/MACCF/MACCM/MACCT/MSHRM) | Carry both version tokens and conflict note in bundle; do not blend |
| LLM call times out | Abstain — `insufficient_evidence` |
| LLM returns empty text | Abstain — `insufficient_evidence` |
| Generation output fails schema validation | Abstain — do not emit partial output |
| Post-check: citation IDs absent from answer text | `PostCheckResult.passed=False` → abstain |
| Post-check: version token absent | `PostCheckResult.passed=False` → abstain |
| Compare mode retrieval result passed in | `out_of_scope` abstention — reject at bundle construction |
| `ExactLookupAnswer` abstention passed in | Propagate upstream abstention |

---

## Recommended implementation order

1. Inspect Session 01–04 typed outputs thoroughly before writing any new types.
2. Define `EvidenceBundle`, `EvidenceArtifact`, `AnswerabilityResult`, `GenerationOutput`,
   `PostCheckResult`, `QAResponse` in `types.py`.
3. Implement `evidence.py`: bundle construction from `RetrievalResult` and from
   `ExactLookupAnswer`. Test with real canonical artifacts.
4. Implement `gate.py`: deterministic answerability gate over `EvidenceBundle`.
   Test all failure modes before proceeding.
5. Implement `generation_prompts.py`: prompt template and rendering function.
   Keep the template simple and 8B-model-sized.
6. Implement `generation.py`: LLM call + schema validation. Test parse failure and
   LLM failure paths with mock inputs before testing with real Ollama.
7. Implement `postcheck.py`: deterministic citation + version + schema check.
8. Implement `answer.py` (optional thin orchestrator): wires steps 2–7 into a single
   `answer(query, retrieval_result) -> QAResponse` call.
9. Add targeted tests covering every failure mode, gate condition, and edge case.
10. Emit manual operator commands for any larger generation quality checks.

---

## Escalation rules

- If evidence bundle construction seems to require re-running retrieval or re-deriving
  scope, stop and flag it.
- If the answerability gate logic starts to look like model-based reasoning, stop and
  narrow it to structural checks.
- If the prompt contract cannot be kept to ~2K tokens with the evidence bundle included,
  log the tradeoff and stop short of a design change.
- If generation post-check produces too many false failures on representative queries,
  emit the failure rate as a manual operator review item — do not weaken the check.
- If compare mode keeps surfacing as a dependency for testing single-entity paths, stop.
  Test with single-entity fixtures only.
