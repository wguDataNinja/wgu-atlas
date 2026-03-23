## 2026-03-23 — gold question set created

**Scope:** First-pass Atlas QA gold evaluation question set authored.

**Files created:**
- `_internal/atlas_qa/QA_GOLD_QUESTION_SET.md` — 100 questions across 7 query classes (A–G)

**Files updated:**
- `_internal/atlas_qa/work_sessions/06_compare_and_eval/SESSION_SPEC.md` — added primary eval input reference pointing to the question set

**Summary:** Question set covers exact identifier lookups (15), single-entity factual (20),
section-grounded NL (18), explicit version comparison (12), disambiguation (10),
out-of-scope abstention (15), and known anomaly/conflict cases (10). A 20-question
launch-gate subset is defined in §5. All four required anomaly/conflict families are
present: C179, D554, MSHRM, MACC family (MACCA/MACCF/MACCM/MACCT).

**Blockers/deviations:** None. Question set is a design artifact; no implementation required.
Session 06 implementation has not started; spec is still a stub.

---

## 2026-03-23 — implementation (claude-sonnet-4-6)

**Scope:** Full Session 06 implementation — explicit compare mode, version_diff_card path,
compare evidence bundle, compare generation + post-check, Atlas-local eval harness,
launch-gate measurement, and targeted tests for all compare failure modes and eval harness behavior.

**Files created:**
- `src/atlas_qa/qa/compare_prompts.py` — compare-specific prompt template (two-sided evidence blocks,
  requires both version tokens, diff card prepended when available)
- `src/atlas_qa/qa/compare.py` — full compare pipeline: `detect_compare_intent`,
  `extract_compare_versions`, `resolve_compare_request`, `build_compare_bundle` (diff card path
  + two-version fallback), `generate_compare_answer`, `compare_post_check`, `answer_compare`
  orchestrator with injectable `_generate_fn` for testing
- `src/atlas_qa/qa/eval_runner.py` — Atlas-local evaluation harness: `load_gold_questions`
  (parses `QA_GOLD_QUESTION_SET.md`), `eval_question` / `run_eval` / `run_launch_subset`,
  `compute_launch_gate` (per-class thresholds A–G), `save_results` (timestamped JSON artifacts
  to `data/atlas_qa/eval/`)
- `tests/atlas_qa/test_compare.py` — 34 tests covering compare intent detection, version
  extraction, request resolution, bundle construction (diff card + fallback), post-check pass/fail,
  and `answer_compare` orchestrator including conflict-program disclosure and missing-version abstention
- `tests/atlas_qa/test_eval_runner.py` — 35 tests covering gold question set parsing (all 7 classes,
  launch subset flagging), `eval_question` with mock answer_fn, `run_eval` summary, launch-gate
  computation (all class thresholds, pass/fail logic, failure details), and save/round-trip

**Files modified:**
- `src/atlas_qa/qa/types.py` — added Session 06 typed outputs: `CompareRequest`, `CompareSide`,
  `CompareEvidenceBundle`, `CompareGenerationOutput`, `ComparePostCheckResult`, `CompareAnswer`,
  `QueryClass`, `EvalExpectedBehavior`, `GoldQuestion`, `EvalCaseResult`, `ClassGateResult`,
  `LaunchGateSummary`, `EvalRunSummary`

**Checks run:**
- `PYTHONPATH=src pytest tests/atlas_qa/` — 238 passed (69 new + 169 prior)

**LLM checks run by Codex:** None. All compare and eval tests use mocked generate/answer functions.
No real Ollama calls were made during implementation.

**Architecture notes:**
- `detect_compare_intent` requires BOTH explicit keywords AND two version strings — no accidental
  compare routing from queries that only mention one version.
- `build_compare_bundle` tries `version_diff_card` first; falls back to two-version program card
  lookup. One-side-empty is allowed with a note (model must state the gap); both-sides-empty
  returns CompareAnswer abstention immediately.
- `compare_post_check` verifies: schema valid, both version tokens in answer_text,
  at least one bundle artifact ID cited. Diff card artifact ID counts as valid citation.
- Conflict programs (MSHRM, MACC family) automatically receive `version_conflict`
  AnomalyDisclosure in the compare bundle via `_anomaly_disclosures_for_entity`.
- `eval_runner.py` uses injectable `answer_fn` for testability; default calls real pipeline.
- Launch-gate thresholds encoded per gold question set §5: A=95%, B/C=85%, D=80%, E=90%,
  F=98%, G=100%.
- `run_launch_subset()` filters the 20-question subset by `is_launch_subset` flag set at
  parse time from `_LAUNCH_SUBSET_IDS`.

**Remaining gaps / post-v1 work:**
- `_default_answer_fn` in `eval_runner.py` requires real corpus data and Ollama; a full
  automated eval run has not been executed (pending operator confirmation of Ollama availability).
- Compare path covers program-level two-version fallback; course-level compare fallback
  (separate course card lookup by version) not implemented — diff card is the expected path
  for course compares.
- Guide-level compare (comparing two guide versions) has no dedicated retrieval path —
  diff card or two-version guide section card lookup needed as a future extension.
- No deduplication of result artifacts across the two compare sides; this is acceptable for v1.

---

## 2026-03-23 — preflight

**Scope:** Folder renumbered from 05_compare_and_eval to 06_compare_and_eval.
Stale Session 01 stub spec replaced with correct Session 06 stub.

**Context:** The previous spec in this folder described Stage 3 canonical object generation
(Session 01 work, already done). That spec was discarded. Session 06 will cover compare mode,
version_diff_card, eval harness, and launch gates — per LOCAL_8B_RAG_SYSTEM_DESIGN.md Stage 6.

**Blockers/deviations:** Session not active. Write the full spec immediately before
implementation starts (per WORK_SESSION_RULES.md).
