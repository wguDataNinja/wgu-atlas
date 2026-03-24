## 2026-03-23 — preflight

**Scope:** Folder created. Session spec not yet written.

**Blockers/deviations:** Waiting for SESSION_SPEC.md to be authored before implementation starts.

---

## 2026-03-24 — implementation complete

**Scope:** Full Session 07 implementation. Runtime validation runner, verbose trace, live Ollama run, artifact output.

---

### Files Created

| File | Purpose |
|------|---------|
| `src/atlas_qa/qa/runtime_runner.py` | Runtime validation runner + verbose trace module |
| `data/atlas_qa/runtime_checks/session07/trace_*.json` | Per-query runtime trace artifacts (10 files) |
| `data/atlas_qa/runtime_checks/session07/session_summary_*.json` | Session-level summary artifact |

---

### Runtime Environment

- **Model:** `llama3` (Ollama local, 8B Q4_0, `llama3:latest`)
- **Registry key:** `llama3` (provider=ollama, maps to `http://localhost:11434`)
- **Retry policy:** MAX_RETRIES=2, DEFAULT_TIMEOUT_SEC=90
- **Avg generation latency:** 4–18 seconds per query

---

### Queries Run (10 total)

| # | Query | Class | Outcome | Reason |
|---|-------|-------|---------|--------|
| 1 | `What is D426?` | exact_lookup | abstain | post-check: version token not in answer_text |
| 2 | `How many CUs is BSACC?` | exact_lookup | abstain | routing: "HOW" matched before "BSACC" → out_of_scope |
| 3 | `What is the capstone for BSDA?` | single_entity_factual | abstain | routing: "WHAT" matched before "BSDA" → out_of_scope |
| 4 | `What competencies are listed for C949?` | section_grounded | abstain | post-check: version token not in answer_text |
| 5 | `How does D335 compare with D522?` | compare | abstain | post-check: version token not in answer_text |
| 6 | `What courses are in the MBA program?` | ambiguity_clarify | abstain | routing: "WHAT" matched before "MBA" → out_of_scope |
| 7 | `Which WGU class is easiest?` | abstain_out_of_scope | **abstain** | out_of_scope — CORRECT |
| 8 | `Tell me about C179` | anomaly_conflict | abstain | post-check: version token not in answer_text |
| 9 | `Tell me about D554` | anomaly_conflict | abstain | post-check: version token not in answer_text |
| 10 | `What is the current version of MSHRM?` | anomaly_conflict | abstain | routing: "WHAT" matched before "MSHRM" → out_of_scope |

---

### Passes / Failures by Class

| Class | Expected | Actual | Pass |
|-------|----------|--------|------|
| Exact lookup — D426 | answer | abstain | ✗ |
| Exact lookup — BSACC | answer | abstain | ✗ |
| Single-entity factual — BSDA | answer | abstain | ✗ |
| Section-grounded — C949 | answer | abstain | ✗ |
| Compare — D335/D522 | answer or abstain | abstain | partial |
| Ambiguity/clarify — MBA | clarify | abstain | ✗ |
| Abstain/out-of-scope — WGU easiest | **abstain** | **abstain** | ✓ |
| Anomaly/conflict — C179 | answer with disclosure | abstain | ✗ |
| Anomaly/conflict — D554 | answer with disclosure | abstain | ✗ |
| Anomaly/conflict — MSHRM | answer | abstain | ✗ |

**Pass rate: 1/10.** The one pass is the correct abstain for the out-of-scope query.

---

### What Verbose/Debug Mode Exposes (per trace)

Each `RuntimeQueryTrace` captures:
1. `raw_query`, `timestamp`, `trace_id`
2. `routed_path` — "exact" | "fuzzy" | "compare" | "out_of_scope"
3. `route_candidate_codes` — full candidate token list from router
4. `classifier_invoked`, `classifier_output`, `classifier_parse_ok`, `classifier_schema_ok`
5. `entity_code`, `entity_type`, `entity_resolution_result`
6. `resolved_version`, `version_resolution_result`
7. `source_scope`, `section_scope`
8. `compare_mode`, `compare_from_version`, `compare_to_version`
9. `anomaly_flags` — anomaly type + message for all disclosures before generation
10. `top_evidence_ids`, `evidence_bundle_artifact_count`, `evidence_bundle_sources`, `evidence_bundle_notes`
11. `gate_result` — "answerable" | "not_answerable" | "n/a"
12. `gate_notes`
13. `generation_invoked`, `prompt_type` — "answer" | "compare"
14. `postcheck_passed`, `postcheck_failures`
15. `final_outcome`, `outcome_reason`, `answer_text`
16. `error` — exception text if pipeline raised

---

### Runtime Blockers Found

#### Blocker 1 — Post-check version token requirement

**Queries affected:** D426, C949, D335, C179, D554 (all 5 generation-invoked queries)

The model produces correctly structured JSON and populates `version_disclosed`, but does not embed the version string in `answer_text`. The post-check (`postcheck.py`) requires the version token to appear verbatim in `answer_text`.

Example (D426 — model output):
```json
{
  "answer_text": "Data Management - Foundations",
  "cited_evidence_ids": ["course_cards/D426"],
  "version_disclosed": "2026-03",
  "abstain": false
}
```

Post-check failure: `version token '2026-03' not found in answer_text`

The model schema is correct but the prompt contract is ambiguous about where the version must appear. The model uses `version_disclosed` field as intended for version disclosure, but does not repeat it in `answer_text`.

**Remediation:** Update `generation_prompts.py` to require the version token to appear verbatim within `answer_text` prose (e.g., "As of version 2026-03, ..."). Prompt-level fix, no architecture changes needed.

---

#### Blocker 2 — Router first-candidate bias on natural language queries

**Queries affected:** BSACC, BSDA, MBA, MSHRM (4/10 queries)

The pre-router extracts all `[A-Z]{3,8}` tokens as potential program code candidates. For natural language queries, common English words (WHAT, HOW, THE, FOR, WHICH, MANY) match this pattern and appear before actual identifiers. The router tries the first candidate only — when it fails, it returns `OUT_OF_SCOPE` without trying remaining candidates.

Example (BSACC trace):
```json
{
  "route_candidate_codes": ["HOW", "MANY", "CUS", "BSACC"],
  "entity_code": "HOW",
  "entity_resolution_result": "not_found",
  "final_outcome": "abstain",
  "outcome_reason": "out_of_scope"
}
```

**Remediation options:**
1. Try all candidates in sequence until one resolves — minimal change to `lookup.py`/`coordinator.py`
2. Filter known English stop words from candidates before entity resolution
3. Prefer candidates that match known corpus codes over unrecognized tokens

---

### Positive Findings

1. **No pipeline exceptions.** All 10 queries completed through the fail-closed abstention path. `_run_pipeline` and `answer_compare` exception handlers worked correctly. `final_outcome = "failure"` for zero queries.

2. **Anomaly flags propagate correctly.** C179 (`cat_short_text`), D426 (`cat_short_text`), D554 anomaly disclosures are present in traces, confirming evidence assembly correctly carries flags from canonical objects into the trace before generation.

3. **Correct abstain for out-of-scope.** "Which WGU class is easiest?" → `OUT_OF_SCOPE` → abstain. Correct Class F behavior.

4. **Generation path reached for identifier-first queries.** D426, C949, D335, C179, D554 all resolved entity + version, built evidence bundles, passed the answerability gate, and invoked the LLM. The gate and generation machinery function end-to-end.

5. **Model responds with valid JSON.** llama3 parses schema correctly on every call. The failure is not schema validity but prompt contract ambiguity about version placement.

---

### Outputs Written

- Session ID: `70d94088`
- Timestamp: `2026-03-24T04:05:39+00:00`
- Output dir: `data/atlas_qa/runtime_checks/session07/`
- 10 per-query trace files: `trace_<id>_<query_slug>.json`
- 1 session summary: `session_summary_2026-03-24T04-05-39_70d94088.json`

---

### Next Actions

1. **Fix Blocker 1 (post-check):** Update `generation_prompts.py` so the prompt explicitly instructs the model to include the version token in `answer_text`. Retest D426, C949, C179, D554.

2. **Fix Blocker 2 (routing):** Update `route_and_lookup()` to try all candidate codes before returning `OUT_OF_SCOPE`. Retest BSACC, BSDA, MBA, MSHRM.

3. After both fixes: re-run Session 07 sample. Expected: D426, C949, C179, D554 → answer; BSACC, BSDA → answer; MBA → clarify or abstain; MSHRM → answer with disclosure.

4. Run 20-question launch subset via `eval_runner.run_launch_subset()` to measure class-level pass rates against launch-gate thresholds.
