## 2026-03-24 — implementation complete

**Scope:** Both fixes implemented. 244/244 tests pass. Control-layer verification
confirms correct entity code extraction for primary fix-target query. Live Ollama
re-run pending operator execution.

---

### Changes Made

#### Fix 1 — resolve_entity_code_from_candidates() (`entity_resolution.py`)

**Problem:** The compare path used `candidate_codes[0]` to select the entity code.
For program-entity compare queries, all-alpha tokens (`[A-Z]{3,8}`) precede the actual
program code in `candidate_codes` because common English words match the regex. Example:

```
"What changed in BSCS between the 2025-06 and 2026-03 catalog editions?"
candidates: ['WHAT', 'CHANGED', 'BSCS', 'BETWEEN', 'THE', 'AND', 'CATALOG', 'EDITIONS']
candidate_codes[0] = 'WHAT'  ← bug
```

`answer_compare("WHAT", ...)` found no corpus cards for `WHAT` and returned
`INSUFFICIENT_EVIDENCE` before generation was ever reached.

**Fix:** Added `resolve_entity_code_from_candidates()` to `entity_resolution.py`.
Iterates candidates in order, skipping all-alpha codes not in the corpus (English words).
Returns the first code found in either `course_cards` or `program_version_cards`.
Alphanumeric codes (course shapes) are returned immediately even if not in corpus
(preserves existing best-guess behavior for course-shaped tokens).

**Verified (no Ollama):**
```
candidates: ['WHAT', 'CHANGED', 'BSCS', 'BETWEEN', 'THE', 'AND', 'CATALOG', 'EDITIONS']
candidate_codes[0] (old bug): WHAT
resolve_entity_code_from_candidates (fix): BSCS
```

**Files changed:** `src/atlas_qa/qa/entity_resolution.py`

---

#### Fix 2 — Compare path entity_code selection (`runtime_runner.py`)

**Problem (secondary):** Even though `coordinate()` already calls the Session 08–fixed
`route_and_lookup()` internally, the resolved `entity_code` from
`exact_resp.answer.entity_code` was not used. The `entity_code` variable was set to
`candidate_codes[0]` before the `coordinate()` call and never updated.

**Fix:** The compare path block now:
1. Initializes `entity_code = None` and `entity_type = EntityType.PROGRAM`.
2. Calls `coordinate(raw_query)` first.
3. When `exact_resp.answer` is present, reads `entity_code` and `entity_type` directly
   from the resolved answer — no candidate iteration needed.
4. When `coordinate()` does not resolve (fallback), calls
   `resolve_entity_code_from_candidates()` with the real corpus.
5. Checks `entity_code is None` after the coordinate pass and abstains if all candidates
   are exhausted.
6. Passes `entity_type` (now always an `EntityType` enum) directly to `answer_compare` —
   removed the `EntityType(entity_type) if isinstance(entity_type, str)` coercion.

Also added lazy imports of `resolve_entity_code_from_candidates` and corpus loaders to
the `run_query` import block.

**Files changed:** `src/atlas_qa/qa/runtime_runner.py`

---

### Tests

6 new tests added to `TestResolveEntityCodeFromCandidates` in
`tests/atlas_qa/test_lookup.py`:

- `test_returns_first_corpus_match` — WHAT/CHANGED skipped, BSCS returned
- `test_skips_english_words_not_in_corpus` — all all-alpha, none in corpus → None
- `test_alphanumeric_code_returned_even_if_not_in_corpus` — D999 not in corpus → D999
- `test_returns_first_when_multiple_in_corpus` — BSDA before BSCS → BSDA
- `test_empty_candidates_returns_none`
- `test_normalizes_input_codes` — lowercase input → normalized lookup

```
244 passed in 10.74s  (238 prior + 6 new)
```

---

### Live re-run — pending operator execution

The live Ollama re-run (Class D subset) must be executed by the operator. Control-layer
verification confirms the routing fix is correct. Command:

```python
from atlas_qa.qa.runtime_runner import run_session, save_artifacts
from pathlib import Path

CLASS_D_SUBSET = [
    ("What changed in BSCS between the 2025-06 and 2026-03 catalog editions?", "compare"),
    ("What was added to BSDA in the 2026-03 edition compared to 2025-06?", "compare"),
    ("What changed in MACCA between catalog versions 202409 and 202412?", "compare"),
    ("Did D426 change between the 2025-06 and 2026-03 catalog editions?", "compare"),
    ("Compare the 2025-06 and 2026-03 versions of BSACC for me.", "compare"),
]

summary = run_session(CLASS_D_SUBSET, model_name="llama3:latest")
save_artifacts(summary, output_dir=Path("data/atlas_qa/runtime_checks/session09"))
```

Expected: at least two queries show `generation_invoked: true` with correct `entity_code`
(BSCS, BSDA, MACCA, D426, or BSACC). Routing failures caused by WHAT/CHANGED/etc as
entity_code must be absent from all five traces.

Post-check or evidence-quality abstentions are acceptable as open issues.

---

### Definition of Done — Verification

| Criterion | Status |
|-----------|--------|
| `resolve_entity_code_from_candidates()` added to `entity_resolution.py` | ✅ |
| Compare path reads `entity_code` from `coordinate()` when available | ✅ |
| Fallback uses `resolve_entity_code_from_candidates()` | ✅ |
| Deterministic control-layer verification: BSCS extracted correctly | ✅ |
| 244/244 tests pass (6 new) | ✅ |
| Live Ollama re-run (Class D subset) | ⏳ pending operator |

---

## 2026-03-24 — preflight

**Scope:** Folder created. SESSION_SPEC.md authored from Session 08 open-issue analysis.

**Context:** Session 08 fixed first-candidate bias in `route_and_lookup()` for the
single-entity path. The compare path in `runtime_runner.py` was not updated — it still
uses `candidate_codes[0]`, causing program-entity Class D queries (e.g., "What changed in
BSCS between...") to pass `WHAT` as the entity code to `answer_compare`, which immediately
abstains with `INSUFFICIENT_EVIDENCE` before reaching generation.

The secondary observation: even when `coordinate()` internally resolves the entity correctly
via the Session 08 fix, the resolved `entity_code` from `exact_resp.answer.entity_code`
is not used — the unresolved first-candidate is still passed to `answer_compare`.

**Blockers/deviations:** None. Session 08 complete. Bug is confirmed by code inspection.

**Status:** Ready to activate.
