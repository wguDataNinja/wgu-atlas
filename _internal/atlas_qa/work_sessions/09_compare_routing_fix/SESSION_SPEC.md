# Session 09 — Compare Routing Fix

**Status:** Ready to activate
**Intent:** Implementation
**Dependency:** Session 08 (`08_runtime_blocker_fixes`) must be complete before this starts

---

## Purpose

Apply the Session 08 candidate-exhaustion fix to the compare path's entity resolution step.
Then re-run a targeted subset of Class D queries to verify the compare pipeline reaches
generation for program-entity compare queries where common English words precede the entity
code in the candidate list.

This session is surgical. It touches the minimum code needed to unblock Class D queries that
fail because the compare path uses `candidate_codes[0]` rather than the first corpus-resident
candidate.

---

## Why this session exists

Session 08 fixed first-candidate bias in `route_and_lookup()` (the single-entity path).
The compare path in `runtime_runner.py` was not updated. It still takes the first candidate
code unconditionally:

```python
entity_code = candidate_codes[0] if candidate_codes else None
```

For a query like `"What changed in BSCS between the 2025-06 and 2026-03 catalog editions?"`,
the normalized query contains tokens `[WHAT, CHANGED, BSCS, BETWEEN, THE, AND, CATALOG,
EDITIONS]` in that order. All are program-shaped (`[A-Z]{3,8}`). The first candidate is
`WHAT`, not `BSCS`. `answer_compare("WHAT", ...)` calls `build_compare_bundle` for `WHAT`,
which finds no corpus cards, and returns `INSUFFICIENT_EVIDENCE` abstention before
generation is ever reached.

Course-code compare queries (e.g., `"Did D426 change between..."`) are not affected because
course codes (`[A-Z]{1,3}\d{1,4}`) appear in `course_candidates` and are concatenated first,
so they survive as `candidate_codes[0]`.

A secondary issue exists in the same compare block: even when `coordinate()` resolves the
entity correctly via `route_and_lookup()`, the resolved `entity_code` from
`exact_resp.answer.entity_code` is not used. Instead the unresolved `candidate_codes[0]`
is passed to `answer_compare`. The `coordinate()` call is effectively ignored for entity
code selection.

---

## Objective

1. Fix the compare path entity code selection in `runtime_runner.py` to use the
   already-resolved `entity_code` from `coordinate()` when available.
2. For the fallback case (exact path did not resolve), iterate candidates to find the
   first one present in the program corpus before giving up.
3. Re-run a targeted Class D subset against real Ollama to confirm compare queries
   with program codes now route correctly.
4. Record results in `DEV_LOG.md`.

---

## LLM use policy

Same as Sessions 07–08: use the real local Ollama-backed answer path for the re-run.
No prompt experimentation. All new code is deterministic control logic.

---

## Locked implementation decisions

1. Fix only the entity code selection step in the compare path. Do not change
   `detect_compare_intent`, `extract_compare_versions`, `build_compare_bundle`, or
   `compare_post_check`.
2. The primary fix is to read `entity_code` from `exact_resp.answer.entity_code` when
   the `coordinate()` pass resolves successfully. This is the cleanest path and reuses the
   Session 08 fix already in `route_and_lookup()`.
3. For the fallback case (coordinate does not resolve), add a helper
   `resolve_entity_code_from_candidates()` in `entity_resolution.py` that iterates
   candidates and returns the first one found in either `course_cards` or
   `program_version_cards`, skipping all-alpha codes absent from the corpus.
4. The compare path in `runtime_runner.py` is the only required change site. Do not
   change `compare.py` or `coordinator.py`.
5. Tests must still pass after the fix.
6. Trace artifacts go to `data/atlas_qa/runtime_checks/session09/`.

---

## Dependencies

Must already exist and be stable:
- Session 08 implementation (all tests passing, `route_and_lookup` fix in place)
- `src/atlas_qa/qa/runtime_runner.py`
- `src/atlas_qa/qa/entity_resolution.py`
- `src/atlas_qa/qa/coordinator.py` and `compare.py`
- `data/atlas_qa/runtime_checks/session08/` (baseline)

Read first:
- `_internal/atlas_qa/work_sessions/08_runtime_blocker_fixes/DEV_LOG.md`
- `src/atlas_qa/qa/runtime_runner.py` lines 230–303 (compare path block)
- `src/atlas_qa/qa/entity_resolution.py` (understand existing helper structure)

---

## In scope

### Fix 1 — Use resolved entity_code from coordinate()

In `runtime_runner.py`, compare path block (around line 240):

**Current:**
```python
entity_code = candidate_codes[0] if candidate_codes else None
...
try:
    _, exact_resp = coordinate(raw_query)
    if exact_resp and exact_resp.answer:
        entity_type = exact_resp.answer.entity_type.value
        ...
    else:
        entity_type = EntityType.PROGRAM
```

**Fix:** Extract `entity_code` from `exact_resp.answer.entity_code` when `coordinate()`
resolves:
```python
try:
    _, exact_resp = coordinate(raw_query)
    if exact_resp and exact_resp.answer:
        entity_code = exact_resp.answer.entity_code   # ← use resolved code
        entity_type = exact_resp.answer.entity_type
        ...
    else:
        # fallback: iterate candidates
        entity_code = resolve_entity_code_from_candidates(candidate_codes, ...)
        entity_type = EntityType.PROGRAM
```

### Fix 2 — Candidate-iteration fallback helper

Add `resolve_entity_code_from_candidates()` to `entity_resolution.py`:

```python
def resolve_entity_code_from_candidates(
    candidates: list[str],
    course_cards: dict,
    program_version_cards: dict,
) -> str | None:
    """Return the first candidate code present in either corpus.

    Skips all-alpha codes absent from both corpora (likely English words).
    Returns None if all candidates are exhausted.
    """
    for raw_code in candidates:
        code = normalize_code(raw_code)
        in_corpus = code in course_cards or code in program_version_cards
        if in_corpus:
            return code
        if any(ch.isdigit() for ch in code):
            # alphanumeric code not in corpus — return anyway as best guess
            return code
    return None
```

### Re-run subset

Run a targeted subset of Class D queries from the gold question set. Required:

| ID | Query | Why |
|----|-------|-----|
| D-054 | What changed in BSCS between the 2025-06 and 2026-03 catalog editions? | Primary fix target — BSCS preceded by WHAT/CHANGED |
| D-056 | What was added to BSDA in the 2026-03 edition compared to 2025-06? | BSDA preceded by WHAT |
| D-058 | What changed in MACCA between catalog versions 202409 and 202412? | MACC family + conflict program |
| D-060 | Did D426 change between the 2025-06 and 2026-03 catalog editions? | Course code first in candidates — should already work; regression check |
| D-065 | Compare the 2025-06 and 2026-03 versions of BSACC for me. | Program code; no English words precede it — regression check |

Optional: re-run the full SESSION07_QUERIES sample (10 queries) as a quick regression
check that single-entity path is unaffected.

### Tests

- Existing tests must still pass.
- Add a targeted unit test for `resolve_entity_code_from_candidates` covering: first
  candidate in corpus, first candidate is English word (skip), all candidates exhausted,
  course-code candidate not in corpus (numeric code — return anyway).

---

## Out of scope

- Changes to `compare.py`, `compare_prompts.py`, `coordinator.py`, or `lookup.py`
- Changes to `detect_compare_intent` or version extraction logic
- Compare prompt fixes (separate concern — would be Session 09b if needed)
- Citation failure for MBA/D554 (open issue from Session 08, not caused by this fix)
- Class E / clarify path (Session 10)

---

## Expected fix locations

| File | Change |
|------|--------|
| `src/atlas_qa/qa/entity_resolution.py` | Add `resolve_entity_code_from_candidates()` |
| `src/atlas_qa/qa/runtime_runner.py` | Compare path: use `exact_resp.answer.entity_code` when available; call new helper for fallback |
| `tests/atlas_qa/test_lookup.py` or new `test_entity_resolution.py` | Add tests for new helper |

---

## Required re-run behavior

After the fix, the targeted Class D subset should produce:

| Query | Expected outcome |
|-------|-----------------|
| D-054 (BSCS, 2025-06 → 2026-03) | answer or meaningful abstain (not routing failure) |
| D-056 (BSDA, added) | answer or meaningful abstain |
| D-058 (MACCA, 202409 → 202412) | answer or meaningful abstain |
| D-060 (D426, no change case) | answer or meaningful abstain |
| D-065 (BSACC compare) | answer or meaningful abstain |

"Meaningful abstain" means the abstention reason is `INSUFFICIENT_EVIDENCE` or
`AMBIGUOUS_VERSION` — not `OUT_OF_SCOPE` (which would indicate the routing bug persists).

If a query reaches generation but fails the compare post-check, the trace must explain why.
Post-check failures for Class D are acceptable as open issues if the routing fix is
confirmed by the trace showing correct entity_code and generation attempt.

---

## Architecture invariants

All Session 07–08 invariants remain in force:
1. Deterministic control layer must not be bypassed.
2. Version scope remains locked before retrieval.
3. Source authority enforcement unchanged.
4. Ambiguous queries must clarify or abstain — this fix must not cause guessing.
5. Anomaly/conflict disclosures must survive.
6. Post-check contract is not relaxed.

---

## Definition of done

This session is complete when:

1. `resolve_entity_code_from_candidates()` is added to `entity_resolution.py`
2. Compare path in `runtime_runner.py` uses resolved `entity_code` from `coordinate()`
   when available; falls back to new helper for the unresolved case
3. Re-run of Class D subset shows at least two queries reaching generation (trace shows
   `generation_invoked: true` and correct `entity_code`) — no more routing failures
   caused by `WHAT`/`CHANGED`/etc as entity code
4. Existing tests still pass; targeted new tests for new helper pass
5. `DEV_LOG.md` records:
   - exact changes made
   - re-run results by query
   - comparison to session 08 baseline
   - any remaining open issues

---

## Escalation rules

Escalate instead of guessing if:
- The `coordinate()` call inside the compare path is slow (it performs a full lookup) and
  causes observable latency — consider caching or short-circuiting
- The candidate-iteration fallback returns a wrong entity code for a previously working
  course-code compare query
- Tests start failing due to unexpected interactions with the entity resolution changes

---

## Recommended implementation order

1. Read `runtime_runner.py` lines 230–303 to understand the full compare block.
2. Read `entity_resolution.py` to understand existing helper signatures.
3. Add `resolve_entity_code_from_candidates()` to `entity_resolution.py`.
4. Add unit tests for the new helper.
5. Update the compare block in `runtime_runner.py` to use `exact_resp.answer.entity_code`
   and the new fallback helper.
6. Run existing test suite — confirm no regressions.
7. Re-run Class D subset against real Ollama.
8. Write trace artifacts to `data/atlas_qa/runtime_checks/session09/`.
9. Update `DEV_LOG.md`.
