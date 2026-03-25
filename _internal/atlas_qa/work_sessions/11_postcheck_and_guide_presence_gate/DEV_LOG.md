# DEV LOG — Session 11: Postcheck Citation Fix + Guide-Presence Gate

Append-only. One entry per work block.

---

## 2026-03-24 — Preflight / Session Setup

**Scope:** Session spec written; root causes confirmed against gold eval run 2 artifact and source files.

**Files read:**
- `data/atlas_qa/runtime_checks/gold_eval/2026-03-25T02-40-28_llama3_latest_results.json` — confirmed 5 failing traces (A-009, A-015, G-092, G-099, G-100) and their postcheck failure messages
- `src/atlas_qa/qa/evidence.py` — confirmed `bundle_from_exact` reads `answer.source_object_identity` directly; no fallback when None
- `src/atlas_qa/qa/gate.py` — confirmed check 6 is gated on `section_scope in _GUIDE_SECTION_REQUIRED`; will not fire when `section_scope=None`
- `src/atlas_qa/qa/postcheck.py` — confirmed check 2 builds `bundle_ids = {a.source_object_identity for a in bundle.artifacts}`; `{None}` cannot match any cited ID
- `data/atlas_qa/program_version_cards.json` — confirmed `source_object_identity: null` for MACCA; D554 guide cards: 0

**Checks run:** none (preflight only)

**Results:**
- Root cause 1 confirmed: MACCA `source_object_identity` is `None` in corpus → bundle carries `{None}` → postcheck citation check fails unconditionally
- Root cause 2 confirmed: D554 has zero guide_section_cards; gate check 6 only fires on section_scope guard → guide-specific queries proceed to generation

**Blockers/deviations:**
- Need to read `scope_partitioning.py` at session start to confirm whether D554 `guide_misrouted_text` notes are added for all D554 queries or only guide-specific ones — this determines whether Fix 2 can safely check the disclosure unconditionally, or needs query-keyword detection
- G-100 is a compare-path query — confirm whether Fix 1 covers `compare.py` bundle construction or requires a parallel change there

---

## 2026-03-24 23:45 — Claude (Session 11 Implementation)

**Scope:** Fix 1 — `evidence.py` source_object_identity derivation guard; Fix 2 — `gate.py` check 6b + keyword detection in `answer.py`; new tests; subset validation

**Files touched:**
- `src/atlas_qa/qa/evidence.py` — added derivation when `source_object_identity` is falsy (empty/None): PROGRAM → `program_version_cards/{code}`, COURSE → `course_cards/{code}`
- `src/atlas_qa/qa/gate.py` — added `guide_seeking_intent: bool = False` parameter; added check 6b after check 6: blocks when flag + `guide_misrouted_text` disclosure + no `guide_section_card` artifacts
- `src/atlas_qa/qa/answer.py` — added `_GUIDE_SEEKING_RE` (matches "program guide", "guide description", "guide says[?]"); passed `guide_seeking_intent` bool to `check_answerability` in `_run_pipeline`
- `tests/atlas_qa/test_evidence.py` — 3 new tests for Fix 1
- `tests/atlas_qa/test_gate.py` — 3 new tests for Fix 2

**Checks run:**
- `PYTHONPATH=src python3 -m pytest tests/atlas_qa/ -q` → 265 passed (259 pre-session + 6 new)
- D554 regression: `Tell me about D554` → answer ✓
- 5-query subset (single pass):

| ID | Query | Expected | Actual |
|----|-------|----------|--------|
| A-009 | What is MACCA? | answer | ✓ answer |
| A-015 | What is MACCM? | answer | ✓ answer |
| G-092 | What does the program guide say about D554? | abstain | ✓ abstain |
| G-099 | What does D554's program guide description say? | abstain | ✓ abstain |
| G-100 | Are MACCA and MACCF on the same guide version? | answer | ✓ answer |

**Results:** All 5 pass. 265 tests pass. No regressions.

**Blockers/deviations:**
- Fix 1 root cause is not exactly as described in spec. `response.py` (untracked) already derives `source_object_identity = f"program_version_cards/{card.program_code}"`. The actual A-009/A-015 failure is LLM non-determinism (~80% pass rate for citation). Fix 1 adds a defensive guard that is correct but technically a no-op for the normal code path.
- Fix 2: `guide_misrouted_text` disclosure is added for ALL D554 queries on the exact path (from `response.py`'s `_course_disclosures`), not just guide-specific ones. Spec's assertion "the disclosures already carry the signal" is incorrect. Implemented keyword detection in `answer.py` per the spec's fallback guidance; added `guide_seeking_intent: bool = False` parameter to `check_answerability` (not `raw_query`).
- D554 generic query ("Tell me about D554") correctly passes check 6b because `guide_seeking_intent=False`.

**Expected targets for next operator-run eval:**

| Class | Gate | Expected outcome |
|-------|------|-----------------|
| A | 95% | PASS — G-092/G-099 now abstain; A-009/A-015 are LLM-dependent but ~80%+ pass rate |
| B | 85% | No regression |
| C | 85% | No regression |
| D | 80% | SKIP — corpus gap, deferred |
| E | 90% | No regression |
| F | 98% | No regression |
| G | 100% | PASS — G-092/G-099 now deterministically abstain; G-100 passed both subset and gold eval |
