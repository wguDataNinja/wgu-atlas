# Session 08 — Runtime Blocker Fixes

**Status:** Ready to activate
**Intent:** Implementation
**Dependency:** Session 07 (`07_runtime_validation`) must be complete before this starts

---

## Naming note

Follows the established work-session structure:

- `06_compare_and_eval/`
- `07_runtime_validation/`
- `08_runtime_blocker_fixes/`

Uses only:
- `SESSION_SPEC.md`
- `DEV_LOG.md`

---

## Purpose

Fix the two blockers identified in Session 07 runtime validation, then re-run the session 07 query sample to confirm the fixes unlock the expected behavior.

This session is surgical. It touches the minimum code needed to unblock the pipeline for the classes of queries that Session 07 proved are broken. No new features, no architecture changes.

---

## Why this session exists

Session 07 ran 10 representative queries through the real Ollama-backed pipeline and found two immediate blockers:

1. **Post-check version token failure** — the model correctly populates `version_disclosed` in its JSON output but does not embed the version string in `answer_text`. The post-check (`postcheck.py`) requires the version token to appear verbatim in `answer_text`. This caused all 5 generation-invoked queries to abstain.

2. **Router first-candidate bias** — the pre-router extracts all `[A-Z]{3,8}` tokens as program code candidates. Common English words (WHAT, HOW, THE, FOR, WHICH, MANY) match this pattern and precede actual identifiers in the candidate list. The router tries only the first candidate; when it fails entity resolution, it returns `OUT_OF_SCOPE` without trying the remaining candidates. This silently dropped 4 of 10 queries before they could reach the corpus.

Neither blocker requires architecture changes. Both have clear, minimal fixes.

---

## Objective

1. Fix Blocker 1: update the answer generation prompt so the model embeds the version token in `answer_text`.
2. Fix Blocker 2: update the router/lookup path to try all candidate codes before returning `OUT_OF_SCOPE`.
3. Re-run the session 07 sample (same 10 queries) to confirm both fixes work under real Ollama.
4. Write updated runtime trace artifacts.
5. Record results in `DEV_LOG.md`.

---

## LLM use policy

Same as Session 07: use the real local Ollama-backed answer path. No prompt experimentation outside the existing system design.

---

## Locked implementation decisions

1. Fix only the two identified blockers. Do not change other pipeline behavior.
2. Blocker 1 fix must be in `generation_prompts.py` (prompt content) — do not relax the post-check contract.
3. Blocker 2 fix must be in `lookup.py` or `coordinator.py` — do not change the router regex or the partition layer.
4. Re-run must use the same `SESSION07_QUERIES` sample from `runtime_runner.py`.
5. Updated trace artifacts go to `data/atlas_qa/runtime_checks/session07_rerun/` (separate from the session 07 baseline).
6. Tests must still pass after both fixes.

---

## Dependencies

Must already exist and be stable:
- Session 07 implementation and artifacts
- `src/atlas_qa/qa/runtime_runner.py`
- `src/atlas_qa/qa/generation_prompts.py`
- `src/atlas_qa/qa/lookup.py`
- `src/atlas_qa/qa/coordinator.py`
- `data/atlas_qa/runtime_checks/session07/` (baseline to compare against)

Read first:
- `_internal/atlas_qa/work_sessions/07_runtime_validation/DEV_LOG.md`
- `src/atlas_qa/qa/postcheck.py` (understand the version token check)
- `src/atlas_qa/qa/generation_prompts.py` (understand current prompt contract)
- `src/atlas_qa/qa/lookup.py` (understand route_and_lookup candidate logic)

---

## In scope

### Blocker 1 — Post-check version token

- Update `generation_prompts.py` so the rendered prompt explicitly instructs the model to include the version token verbatim in `answer_text` (e.g., "As of version 2026-03, ...")
- Do not change `postcheck.py` — the post-check contract is correct
- Do not change `generation.py` or `answer.py`

### Blocker 2 — Router first-candidate bias

- Update `route_and_lookup()` in `lookup.py` (or the caller in `coordinator.py`) to iterate through all candidate codes and return the first one that resolves successfully in the corpus
- Stop at the first successful resolution — do not change multi-candidate behavior beyond that
- Common English words that are not in the corpus must not block subsequent candidates from being tried

### Verification run

- Re-run `SESSION07_QUERIES` against real Ollama after both fixes
- Write trace artifacts to `data/atlas_qa/runtime_checks/session07_rerun/`
- Record per-query pass/fail comparison against session 07 baseline

### Tests

- Existing tests must still pass after both changes
- Add minimal targeted tests only if needed to cover the specific fix paths; do not add broad new test coverage

---

## Out of scope

- Relaxing or changing the post-check contract
- Changing the router regex or token extraction logic
- Adding new entity resolution heuristics beyond trying all candidates in order
- Prompt redesign beyond what is needed to embed the version token
- Fuzzy retrieval changes
- Compare mode changes
- Any other pipeline layer

---

## Expected fix locations

### Blocker 1

`src/atlas_qa/qa/generation_prompts.py`

The rendered prompt should instruct the model to embed the version string in the answer text, not only in the `version_disclosed` field. The instruction should be explicit: include the version token verbatim in `answer_text` (e.g., "As of version 2026-03, ...").

Do not change the JSON output schema. `version_disclosed` should still be populated — the post-check requires the version in `answer_text` as well.

### Blocker 2

`src/atlas_qa/qa/lookup.py` — `route_and_lookup()` function

Currently:
```python
first_code = normalize_code(decision.candidate_codes[0])
result = lookup(query)
if result.abstention == NOT_IN_CORPUS and not any(ch.isdigit() for ch in first_code):
    return abstain(query, OUT_OF_SCOPE)
return result
```

The fix: iterate through all candidate codes in order. Return the first result that resolves without abstention. Only return `OUT_OF_SCOPE` when all candidates have been tried and none resolved.

---

## Required re-run behavior

After both fixes, the re-run of `SESSION07_QUERIES` should produce:

| Query | Expected outcome after fix |
|-------|---------------------------|
| `What is D426?` | answer |
| `How many CUs is BSACC?` | answer |
| `What is the capstone for BSDA?` | answer |
| `What competencies are listed for C949?` | answer or abstain (section gate may still block) |
| `How does D335 compare with D522?` | answer or abstain |
| `What courses are in the MBA program?` | clarify or abstain |
| `Which WGU class is easiest?` | abstain (unchanged — correct) |
| `Tell me about C179` | answer (with cat_short_text disclosure) |
| `Tell me about D554` | answer (with anomaly disclosure) |
| `What is the current version of MSHRM?` | answer |

If a query still abstains after both fixes, the trace must explain why.

---

## Architecture invariants

All invariants from Session 07 remain in force:
1. Deterministic control layer must not be bypassed.
2. Version scope remains locked before retrieval.
3. Source authority enforcement unchanged.
4. Ambiguous queries must clarify or abstain — fixes must not cause guessing.
5. Anomaly/conflict disclosures must survive to final response.
6. Post-check contract is not relaxed.

---

## Definition of done

This session is complete when:

1. Blocker 1 is fixed in `generation_prompts.py` and verified to produce version-in-answer-text output
2. Blocker 2 is fixed in `lookup.py` and verified to route BSACC, BSDA, MSHRM to the corpus
3. Re-run of `SESSION07_QUERIES` against real Ollama produces at minimum:
   - one exact answer case (D426 or BSACC)
   - one single-entity factual answer (BSDA)
   - one anomaly/conflict answer with disclosure (C179 or D554)
   - correct continued abstain for out-of-scope (WGU easiest)
4. Existing tests still pass
5. `DEV_LOG.md` records:
   - exact changes made
   - re-run results by query
   - comparison to session 07 baseline
   - any remaining open issues

---

## Escalation rules

Escalate instead of guessing if:
- The prompt fix causes the model to refuse to answer or produce malformed JSON
- The routing fix causes ambiguous entity resolution for queries that should clarify
- Tests start failing due to prompt or routing changes in unexpected ways
- The re-run reveals a third blocker not visible from session 07 traces

---

## Recommended implementation order

1. Read `generation_prompts.py` to understand current prompt structure.
2. Apply Blocker 1 fix — add explicit version-in-answer-text instruction.
3. Run one generation-invoked query (D426) to confirm post-check now passes.
4. Read `lookup.py` — `route_and_lookup()` — to understand current candidate logic.
5. Apply Blocker 2 fix — iterate all candidates before returning `OUT_OF_SCOPE`.
6. Test BSACC and MSHRM routing locally to confirm they resolve.
7. Run existing test suite — confirm no regressions.
8. Re-run full `SESSION07_QUERIES` sample against real Ollama.
9. Write trace artifacts to `data/atlas_qa/runtime_checks/session07_rerun/`.
10. Update `DEV_LOG.md`.
