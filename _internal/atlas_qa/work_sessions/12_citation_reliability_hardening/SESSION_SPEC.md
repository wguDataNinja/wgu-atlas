# Session 12 — Citation Reliability Hardening

**Status:** Ready to activate
**Intent:** Implementation
**Dependency:** Sessions 07–11 complete ✅; gold eval run 3 complete ✅
**Input artifact:** `data/atlas_qa/runtime_checks/gold_eval/2026-03-25T04-06-00_llama3_latest_results.json`

---

## Purpose

Harden citation reliability for the single-entity exact path. After session 11, four
queries fail postcheck because the model does not include `source_object_identity` in
`cited_evidence_ids`, and one query fails because the model returns `abstain=true` for
a question the evidence bundle can clearly answer. Both are surgical fixes. No
architecture changes, no model swap, no broad provenance relaxation.

---

## Why this session exists

Gold eval run 3 (2026-03-25T04-06, `llama3:latest`) scored **82/100**. Gates for B, C,
E, F pass. Three gates fail:

| Class | Rate | Gate | Status |
|-------|------|------|--------|
| A | 93.3% | 95% | FAIL — 1 failure (A-008) |
| D | 8.3% | 80% | **DEFERRED — corpus gap, not code** |
| G | 90.0% | 100% | FAIL — 1 failure (G-100) |

Class D is explicitly deferred. Its 11 failures are a data gap (missing 2025-06 program
version cards), not a code problem. Do not touch Class D this session.

The remaining addressable failures from the run 3 artifact are:

| ID | Class | Failure mode | Postcheck failure |
|----|-------|-------------|-------------------|
| A-008 | A | citation non-determinism | `course_cards/D554` not in cited_evidence_ids or answer_text |
| B-018 | B | model-level abstention | generation returned `abstain=true`; postcheck not reached |
| B-029 | B | citation non-determinism | `program_version_cards/MACCA` not in cited_evidence_ids or answer_text |
| C-053 | C | citation non-determinism | `course_cards/D554` not in cited_evidence_ids or answer_text |
| G-100 | G | citation non-determinism | `program_version_cards/MACCA` not in cited_evidence_ids or answer_text |

Note: B-031 and C-051 (BSPRN not in corpus) are not pipeline bugs — they are gold
question set issues. Do not treat them as targets for this session.

**Root cause 1 — Citation omission (~20% rate, LLM non-determinism)**

The generation prompt instructs the model to cite artifact IDs but does not show it how
to find those IDs or what they look like. The artifact header reads:

```
[course_cards/D554]
type=... entity=... version=... source=...
<content>
```

The model must extract `course_cards/D554` from the bracket header and put it in
`cited_evidence_ids`. Rule 1 in the current prompt says "Cite every artifact you use by
including its ID in `cited_evidence_ids`" but does not show an example and does not
explicitly point the model to the bracket header as the source.

Fix: extend the system instruction with an explicit example showing how to lift the ID
from the bracket header. Add the example inline, before the output schema. Keep the
prompt tight — ~2K token constraint still applies.

**Root cause 2 — Model-level abstention for answerable BSACC query (B-018)**

B-018 ("What is the total CU requirement for BSACC?") passed in run 2 and failed in
run 3. `postcheck_passed` is null, which means `generation.py` received `abstain=true`
from the model before postcheck was reached. The BSACC program version card contains
`total_cus: 121` — the evidence bundle can answer this question.

This is LLM non-determinism. The model occasionally returns `abstain=true` for
answerable queries when uncertain about how to handle numeric values.

Fix: add a single retry in `generation.py` when the model returns `abstain=true` (or
`answer_text=None`) and the bundle is non-empty. Retry only once, only on the exact
path, only when abstain is the sole failure mode (not parse error, not schema error).
Record the retry attempt in the `GenerationOutput`. If the retry also abstains, treat
as abstain (no further retries).

---

## Objective

1. Harden `generation_prompts.py`: add an explicit artifact-ID citation example in the
   system instructions showing the model how to copy the bracket header ID.
2. Add a narrow postcheck fallback in `postcheck.py`: if `cited_evidence_ids` is empty
   but the bundle has exactly one artifact and the entity code appears in `answer_text`,
   treat the citation check as passing. Guard this to single-artifact bundles only.
3. Investigate and fix B-018: add a single retry in `generation.py` when the model
   returns `abstain=true` for a non-empty bundle on the exact path.
4. Run the 6-query affected subset (A-008, B-018, B-029, C-053, G-100, plus the D554
   regression anchor) and confirm behavior.
5. Hand back the full 100-question eval command for the operator to run after the
   subset is clean.

---

## LLM use policy

- Fix 1 (`generation_prompts.py`): deterministic — no LLM needed to implement the
  prompt change.
- Fix 2 (`postcheck.py`): deterministic — structural fallback, no LLM needed.
- Fix 3 (`generation.py`): modifies when LLM is called (adds one possible retry), but
  is itself deterministic logic. Requires Ollama for testing.
- Subset validation requires Ollama. Verify with
  `curl -s http://localhost:11434/api/tags` before starting.

**Operator run rule:**
- Codex may run short single-query live Ollama checks to validate each fix.
- Codex must not run the full 100-question gold eval.
- After the subset is clean and tests pass, Codex must output the full eval command for
  the operator to run.

---

## Locked implementation decisions

1. **Fix 1 (prompt):** Extend `_SYSTEM_INSTRUCTIONS` only — do not change the template
   structure, the `_PROMPT_TEMPLATE` string, or `render_generation_prompt`. Add one
   concrete example showing: `[course_cards/D554]` → `"cited_evidence_ids":
   ["course_cards/D554"]`. Keep the example inline; do not add a separate section.
2. **Fix 2 (postcheck fallback):** The fallback triggers only when ALL of the following
   are true: (a) `cited_evidence_ids` is empty, (b) the bundle has exactly one artifact,
   (c) the artifact's `source_object_identity` is not None, (d) the entity code derived
   from `source_object_identity` (everything after the last `/`) appears in
   `answer_text`. Do not broaden beyond these four guards.
3. **Fix 2 must not weaken multi-artifact bundles.** Compare-path bundles carry two
   artifacts. The fallback must not fire for them.
4. **Fix 3 (retry):** One retry maximum. Retry only when `parsed.abstain=True` and
   `not gen_output.parse_error and not gen_output.schema_error and not gen_output.llm_failure`
   (i.e., the model responded cleanly but chose to abstain). Do not retry on parse errors
   or schema errors. Add `retried: bool = False` field to `GenerationOutput` so callers
   can observe whether a retry occurred.
5. **Do not change `postcheck.py` check 3 (version token).** Version disclosure
   requirement stays. The fixes in this session target citation only and model abstention.
6. **Do not add corpus data.** No 2025-06 cards. Class D remains deferred.
7. Tests must pass throughout. Add targeted tests for each new behavior; do not add
   broad coverage sweeps.

---

## Dependencies

Must already exist and be stable:
- Sessions 07–11 complete; 265 tests passing
- `src/atlas_qa/qa/generation_prompts.py`
- `src/atlas_qa/qa/generation.py`
- `src/atlas_qa/qa/postcheck.py`
- `src/atlas_qa/qa/types.py` (for `GenerationOutput`)
- `data/atlas_qa/program_version_cards.json`
- `scripts/run_gold_eval.py`

Read first:
- `_internal/atlas_qa/work_sessions/12_citation_reliability_hardening/SESSION_SPEC.md`
  (this file)
- `src/atlas_qa/qa/generation_prompts.py` — current `_SYSTEM_INSTRUCTIONS` and template
- `src/atlas_qa/qa/generation.py` — `generate_answer()`, `_ModelOutput`, abstention
  handling
- `src/atlas_qa/qa/postcheck.py` — check 2 (citation), current fallback logic
- `src/atlas_qa/qa/types.py` — `GenerationOutput` fields
- `data/atlas_qa/runtime_checks/gold_eval/2026-03-25T04-06-00_llama3_latest_results.json`
  — trace entries for A-008, B-018, B-029, C-053, G-100

---

## In scope

### Fix 1 — `generation_prompts.py`: explicit citation example

**File:** `src/atlas_qa/qa/generation_prompts.py`
**Location:** `_SYSTEM_INSTRUCTIONS`, after Rule 1

Current Rule 1:
```
1. Cite every artifact you use by including its ID in "cited_evidence_ids".
```

Extended Rule 1 (replace with):
```
1. Cite every artifact you use by including its ID in "cited_evidence_ids". The ID is
   the text inside the leading brackets of each artifact, e.g., for an artifact starting
   with "[course_cards/D554]", the cited ID is "course_cards/D554". Copy the ID exactly.
```

This change is additive — does not alter the schema, template structure, or any other
rule.

---

### Fix 2 — `postcheck.py`: entity-code fallback for empty cited_evidence_ids

**File:** `src/atlas_qa/qa/postcheck.py`
**Function:** `post_check()`

After the existing citation check:

```python
bundle_ids = {a.source_object_identity for a in bundle.artifacts}
cited = set(gen_output.cited_evidence_ids)
answer_text = gen_output.answer_text or ""

citation_ids_present = bool(
    (cited & bundle_ids)
    or any(bid in answer_text for bid in bundle_ids)
)
```

Add a narrow fallback when `citation_ids_present` is still False:

```python
if not citation_ids_present and not gen_output.cited_evidence_ids:
    # Narrow fallback: single-artifact bundle, entity code appears in answer_text.
    non_none_artifacts = [a for a in bundle.artifacts if a.source_object_identity]
    if len(non_none_artifacts) == 1:
        identity = non_none_artifacts[0].source_object_identity
        entity_code = identity.rsplit("/", 1)[-1]  # "course_cards/D554" -> "D554"
        if entity_code and entity_code in answer_text:
            citation_ids_present = True
```

This fallback is intentionally narrow:
- Only fires when `cited_evidence_ids` is empty (not when it contains wrong IDs)
- Only fires for single-artifact bundles (exact/single-entity path)
- Only fires when the entity code literally appears in the answer text
- Does not fire for compare-path bundles (which have two artifacts)

---

### Fix 3 — `generation.py`: single retry on model-level abstention

**File:** `src/atlas_qa/qa/generation.py`
**Function:** `generate_answer()`

Add `retried: bool = False` to `GenerationOutput` in `types.py` first.

In `generate_answer()`, after the existing abstention check:

```python
# Step 5 — Check model-level abstention.
if parsed.abstain or not parsed.answer_text:
    # Retry once if the model abstained cleanly (no parse/schema/LLM error).
    # This handles non-deterministic over-cautious abstention on answerable queries.
    if not retried_already:
        retry_result = generate_answer(bundle, question, model_name, _retried=True)
        return dataclasses.replace(retry_result, retried=True)
    return GenerationOutput(...)
```

Implement by adding a private `_retried: bool = False` parameter to `generate_answer`.
On the first call, `_retried=False`. If abstain occurs and `_retried=False`, call self
recursively with `_retried=True`. If abstain occurs on the retry, return the abstain
result with `retried=True`. Do not recurse further.

---

### Affected question subset validation

Run these queries individually and confirm expected behavior:

| ID | Query | Expected after fixes |
|----|-------|---------------------|
| A-008 | What is D554? | answer ✅ |
| B-018 | What is the total CU requirement for BSACC? | answer ✅ |
| B-029 | What is the degree title for MACCA? | answer ✅ |
| C-053 | What competencies does D554 teach? | answer ✅ |
| G-100 | Are MACCA and MACCF on the same guide version? | answer ✅ |

Regression anchors (must not change):
- "Tell me about D554" → must still answer (catalog path unaffected)
- Any Class E/F query → unchanged (clarify and abstain paths unaffected)
- Any Class B/C passing query → no regression

Note: A-008 and B-029/G-100 have ~20% LLM non-determinism even after fixes. If one
still fails on a single run, note it but do not escalate immediately — re-run once
before escalating.

---

### Tests

**For Fix 1 (prompt):**
- Verify the rendered prompt for a sample bundle contains the phrase "Copy the ID
  exactly" or equivalent citation example text. This is a string-content assertion, not
  a behavior test.

**For Fix 2 (postcheck fallback):**
- Single-artifact bundle, `cited_evidence_ids=[]`, entity code in `answer_text` →
  `citation_ids_present=True`, `passed=True` (assuming version token also present)
- Single-artifact bundle, `cited_evidence_ids=[]`, entity code NOT in `answer_text` →
  `citation_ids_present=False`, `passed=False`
- Two-artifact bundle, `cited_evidence_ids=[]`, entity code in `answer_text` →
  fallback does NOT fire → `citation_ids_present=False` (multi-artifact guard holds)
- Single-artifact bundle, `cited_evidence_ids` contains correct ID (normal path) →
  no change in behavior; fallback not reached

**For Fix 3 (retry):**
- Mock `generate` to return abstain=True on first call, valid answer on second →
  `generate_answer` returns the valid answer with `retried=True`
- Mock `generate` to return abstain=True on both calls →
  `generate_answer` returns abstain with `retried=True`
- Mock `generate` to return valid answer on first call →
  no retry; `retried=False`

---

## Out of scope

- Class D corpus build — 2025-06 program version cards, deferred to session 13
- Relaxing postcheck check 3 (version token)
- Model swap or model comparison work
- Rewriting the generation prompt beyond the targeted citation example
- Broadening the postcheck fallback to multi-artifact bundles
- Broadening the retry logic to parse errors or schema errors
- Gold question set annotation updates (B-031, C-051 are gold set issues, not pipeline)
- Any compare path changes
- New retrieval or ranking logic
- E-066 gold question note (wrong note, correct behavior — leave as-is)

---

## Architecture invariants

All session 07–11 invariants remain in force, plus:

1. The postcheck citation fallback must never fire for compare-path bundles. A bundle
   with two or more artifacts must pass through the original citation check only.
2. The generation retry must be self-limiting: exactly one retry maximum, never more.
   The `_retried` guard prevents any recursion beyond depth 1.
3. `GenerationOutput.retried` is an observable field. Eval runners and trace artifacts
   may log it. It must not be used for downstream control flow beyond logging.
4. The citation example added to `_SYSTEM_INSTRUCTIONS` must not exceed the ~2K token
   context budget when combined with a typical single-artifact bundle. Verify rendered
   prompt length for a representative query before committing.
5. All 265 existing tests must pass after all three fixes.

---

## Expected fix locations

| Fix | File | Location |
|-----|------|----------|
| 1 — citation example | `src/atlas_qa/qa/generation_prompts.py` | `_SYSTEM_INSTRUCTIONS` Rule 1 |
| 2 — postcheck fallback | `src/atlas_qa/qa/postcheck.py` | `post_check()` check 2 |
| 3 — generation retry | `src/atlas_qa/qa/generation.py` | `generate_answer()` abstention branch |
| 3 — retried field | `src/atlas_qa/qa/types.py` | `GenerationOutput` |

---

## Required outputs

- Updated `src/atlas_qa/qa/generation_prompts.py`
- Updated `src/atlas_qa/qa/postcheck.py`
- Updated `src/atlas_qa/qa/generation.py`
- Updated `src/atlas_qa/qa/types.py` (add `retried` field)
- New/updated tests in `tests/atlas_qa/`
- Updated `DEV_LOG.md` in this session folder (changes made, subset results, expected
  targets for next eval)
- Full eval command handed to operator for execution

The following happen **after** the operator runs the full eval and reviews the artifact
— not in this session:
- `_internal/ATLAS_CONTROL.md` §6.0b gold eval table update
- One-line entry in `_internal/DEV_LOG.md`

---

## Deterministic rules

- Do not run the full 100-question eval until the 5-query subset is clean.
- Do not commit changes until tests pass.
- Artifact timestamp is set by `run_gold_eval.py` — do not rename artifacts manually.
- Save eval artifacts to `data/atlas_qa/runtime_checks/gold_eval/` — not anywhere else.
- Do not modify the `_retried` parameter to allow more than one recursive call.

---

## Required validation behavior

After all three fixes are implemented:

1. Run `PYTHONPATH=src python3 -m pytest tests/atlas_qa/ -q` — all 265+ tests must pass.
2. Run each of the 5 affected queries individually through `run_query`. Record outcome and
   `postcheck_failures`.
3. Run "Tell me about D554" regression check.
4. If any affected query still fails on a single run (non-determinism), run it once more
   before escalating.
5. After subset is clean, output the full eval command for the operator.

---

## Definition of done

1. `generation_prompts.py` contains explicit citation example in `_SYSTEM_INSTRUCTIONS`
2. `postcheck.py` contains narrow single-artifact fallback for empty `cited_evidence_ids`
3. `generation.py` retries once on model-level abstention for non-empty bundles
4. `types.py` `GenerationOutput` has `retried: bool = False` field
5. 5-query subset: A-008, B-018, B-029, C-053, G-100 all return `answer` (with LLM
   non-determinism tolerance — see note above)
6. "Tell me about D554" still answers (no regression)
7. All 265+ tests pass including new tests for each fix
8. `DEV_LOG.md` records: changes made, subset results, retried flag observed or not,
   expected targets for next eval
9. Full eval command handed to operator for execution

---

## Edge cases to watch

- **Multi-artifact bundle postcheck fallback:** The compare path builds bundles with two
  artifacts. Verify that Fix 2 does not alter behavior for G-100 (compare query) on the
  first run — G-100 should pass through the original check, not the fallback. If the
  fallback somehow fires for a two-artifact bundle, the guard is wrong.
- **Retry and abstain count consistency:** If B-018 is observed to retry, verify that the
  trace `outcome_reason` is still `generation_passed_postcheck` (not a new retry-specific
  value). The retry is an internal implementation detail; callers see the final result.
- **Prompt length budget:** After Fix 1, render a prompt for a real bundle and check
  token count. A single program version card prompt with the extended instructions should
  stay under 1500 tokens for an 8B model with 8K context. If over 2K, trim the example.
- **`source_object_identity` with no slash:** The Fix 2 fallback uses `rsplit("/", 1)`.
  If `source_object_identity` contains no slash (unexpected), `rsplit` returns the full
  string. This is safe — it would just attempt to match the full identity string against
  `answer_text`, which is a conservative failure mode.
- **Version token still required:** Fix 2 relaxes the citation check only. The version
  token check (check 3) is unchanged. An answer that mentions the entity code but omits
  the version token still fails postcheck.

---

## Recommended implementation order

1. Read `src/atlas_qa/qa/generation_prompts.py`, `generation.py`, `postcheck.py`,
   `types.py` to baseline current state.
2. Implement Fix 1 (`generation_prompts.py`). Render a sample prompt and verify the
   citation example text appears in the output.
3. Add `retried: bool = False` to `GenerationOutput` in `types.py`.
4. Implement Fix 3 (`generation.py`). Write the retry unit test immediately.
5. Implement Fix 2 (`postcheck.py`). Write the postcheck fallback unit tests immediately.
6. Run existing test suite: `PYTHONPATH=src python3 -m pytest tests/atlas_qa/ -q`
7. Verify Ollama is running: `curl -s http://localhost:11434/api/tags | head -5`
8. Run the 5-query subset individually through `run_query`.
9. Run "Tell me about D554" regression check.
10. Run full test suite with new tests.
11. Hand off full eval command to operator:
    ```
    PYTHONPATH=src python3 scripts/run_gold_eval.py --model llama3:latest
    ```
    (or the correct current entry point if it differs — verify via `scripts/`).
12. Update `DEV_LOG.md` in this session folder.
13. **Stop here.** Control-doc updates (`ATLAS_CONTROL.md`, top-level `DEV_LOG.md`)
    happen after the operator reviews the full eval artifact — not in this session.

---

## Escalation rules

Escalate instead of guessing if:

- Fix 2 fallback fires for a two-artifact bundle — the guard is wrong; stop and read
  the bundle construction logic in `compare.py` before continuing
- B-018 still abstains after Fix 3 (retry added) on both the original and retry call —
  check what the evidence bundle content looks like for BSACC; if `total_cus` is absent
  from the artifact content, the problem is in evidence assembly, not generation
- Any Class B/C/E/F query regresses — stop and compare traces before/after
- A-008, B-029, C-053, or G-100 still fail consistently (>2 runs) after both Fix 1 and
  Fix 2 — check whether the entity code is literally present in the answer_text; if not,
  the fallback trigger is wrong and needs re-examination
- Prompt length after Fix 1 exceeds 2K tokens for a typical bundle — trim the example
  before proceeding

---

## Codex execution instructions

**Start here:**
1. Verify Ollama is running: `curl -s http://localhost:11434/api/tags | python3 -m json.tool | head -20`
2. Verify test baseline: `PYTHONPATH=src python3 -m pytest tests/atlas_qa/ -q`
3. Read `generation_prompts.py`, `generation.py`, `postcheck.py`, `types.py`
4. Implement Fix 1 (prompt), then render a test prompt and verify citation example text
5. Add `retried` field to `types.py`
6. Implement Fix 3 (retry) and write its unit tests
7. Implement Fix 2 (postcheck fallback) and write its unit tests
8. Run full test suite
9. Run the 5-query affected subset
10. Run "Tell me about D554" regression check
11. **Do not run the full 100-question eval yourself.** Output the exact eval command for
    the operator to run. Confirm the current entry point via `scripts/`, then output:
    ```
    PYTHONPATH=src python3 scripts/run_gold_eval.py --model llama3:latest
    ```
12. Update `DEV_LOG.md` in this session folder with: changes made, subset results,
    whether retry fired for B-018, expected targets for next eval.
13. **Stop here.** Control-doc updates happen after the operator reviews the full eval
    artifact.
