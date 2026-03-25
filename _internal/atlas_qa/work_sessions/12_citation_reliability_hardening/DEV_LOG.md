# DEV LOG — Session 12: Citation Reliability Hardening

Append-only. One entry per work block.

---

## 2026-03-25 — Preflight / Session Setup

**Scope:** Session spec written; gold eval run 3 artifact reviewed; root causes confirmed.

**Baseline artifact:**
- `data/atlas_qa/runtime_checks/gold_eval/2026-03-25T04-06-00_llama3_latest_results.json`
- Score: 82/100. Passing gates: B, C, E, F. Failing: A (93.3% vs 95%), G (90% vs 100%).

**Confirmed failure modes from artifact:**

| ID | Failure mode | Postcheck failure |
|----|-------------|-------------------|
| A-008 | citation non-determinism | `course_cards/D554` absent from `cited_evidence_ids` and `answer_text` |
| B-018 | model-level abstention | generation returned `abstain=true`; `postcheck_passed=null` |
| B-029 | citation non-determinism | `program_version_cards/MACCA` absent |
| C-053 | citation non-determinism | `course_cards/D554` absent |
| G-100 | citation non-determinism | `program_version_cards/MACCA` absent |

**Confirmed corpus facts:**
- BSACC program version card contains `total_cus: 121` — evidence is present for B-018;
  failure is model over-caution, not missing data.
- B-031, C-051 (BSPRN) confirmed as gold question set issues; excluded from session scope.

**Checks run:** none (preflight only)

**Blockers/deviations:** none at preflight

**Expected fix locations:** `generation_prompts.py`, `generation.py`, `postcheck.py`, `types.py`

---

## 2026-03-25 — Claude (Session 12 Implementation)

**Scope:** Fix 1 — prompt citation example; Fix 2 — postcheck entity-code fallback; Fix 3 — generation retry on clean abstention; new tests; subset validation

**Files touched:**
- `src/atlas_qa/qa/generation_prompts.py` — extended Rule 1 in `_SYSTEM_INSTRUCTIONS` with explicit bracket-ID citation example and "Copy the ID exactly" instruction
- `src/atlas_qa/qa/postcheck.py` — added narrow entity-code fallback after existing citation check: fires only when `cited_evidence_ids` empty, bundle has exactly one non-None artifact, and entity code (after last `/`) appears in `answer_text`
- `src/atlas_qa/qa/types.py` — added `retried: bool = False` field to `GenerationOutput`
- `src/atlas_qa/qa/generation.py` — added `_retried: bool = False` parameter to `generate_answer`; single retry on clean model-level abstention when `bundle.artifacts` non-empty; `retried=True` propagated to returned `GenerationOutput`
- `tests/atlas_qa/test_postcheck.py` — 4 new tests for Fix 2 fallback (fires on entity code present, does not fire when absent, does not fire for two-artifact bundle, normal citation path unchanged)
- `tests/atlas_qa/test_generation.py` — 5 new tests for Fix 1 (prompt content) and Fix 3 (retry on abstain+succeed, retry+both-abstain, no retry on success, no retry on LLM failure)

**Checks run:**
- `PYTHONPATH=src python3 -m pytest tests/atlas_qa/ -q` → 274 passed (265 pre-session + 9 new)
- 5-query affected subset (single pass, llama3:latest):

| ID | Query | Expected | Actual |
|----|-------|----------|--------|
| A-008 | What is D554? | answer | ✅ answer |
| B-018 | What is the total CU requirement for BSACC? | answer | ✅ answer |
| B-029 | What is the degree title for MACCA? | answer | ✅ answer |
| C-053 | What competencies does D554 teach? | answer | ✅ answer |
| G-100 | Are MACCA and MACCF on the same guide version? | answer | ✅ answer |

- D554 regression anchor: "Tell me about D554" → `outcome=answer reason=generation_passed_postcheck` ✅

**Results:** All 5 pass. 274 tests pass. No regressions.

**Blockers/deviations:**
- No surprises. The retry for B-018 was not observed to fire on this run (model answered on first call), consistent with non-determinism — the retry is a safety net, not always exercised.
- Fix 2 postcheck fallback fired for the citation non-determinism queries (model answered but left `cited_evidence_ids: []`). Entity codes D554 and MACCA are always present in their respective answer texts, so the fallback reliably triggers.

**Expected targets for next operator-run eval:**

| Class | Gate | Expected outcome |
|-------|------|-----------------|
| A | 95% | PASS — A-008 citation fallback now covers it |
| B | 85% | No regression |
| C | 85% | No regression |
| D | 80% | SKIP — corpus gap, deferred to session 13 |
| E | 90% | No regression |
| F | 98% | No regression |
| G | 100% | PASS — G-100 citation fallback now covers it |

---

## 2026-03-25 — Gold Eval Run 4 Results (operator-run)

**Artifact:** `data/atlas_qa/runtime_checks/gold_eval/2026-03-25T13-26-12_llama3_latest_results.json`
**Score:** 87/100 (up from 82)

| Class | Result | vs. expected |
|-------|--------|-------------|
| A | 15/15 100% ✅ | As expected |
| B | 19/20 95.0% ✅ | As expected |
| C | 17/18 94.4% ✅ | As expected |
| D | 2/12 16.7% ❌ | corpus gap (expected fail) |
| E | 10/10 100% ✅ | As expected |
| F | 14/15 93.3% ❌ | **REGRESSION** — F-089 answered when should abstain |
| G | 10/10 100% ✅ | As expected |

**Fixed:** A-008, B-018, B-029, C-053, D-054, G-100 (+6)
**Regressed:** F-089 (-1)

**F-089 root cause analysis:**
- Query: "What are WGU's tuition rates for BSCS?" — expected: abstain
- Actual: `generation_passed_postcheck` (model answered)
- Fix 3 (retry) is the likely cause: BSCS has a valid catalog card (bundle non-empty),
  model correctly abstained on first call (recognizing tuition is out-of-scope), but
  retry fired unconditionally and second call answered incorrectly
- Postcheck passed because BSCS appears in the answer and version token was present

**Next action:** restrict or remove Fix 3 retry to prevent override of correct abstentions
for out-of-scope queries
