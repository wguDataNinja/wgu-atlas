## 2026-03-23 — preflight

**Scope:** Folder and spec created. Session not yet started.

**Context:** The previous `05_compare_and_eval/` folder held a stale stub spec describing
Session 01 (canonical object generation) work — work already completed in Sessions 01–04.
That folder was renamed to `06_compare_and_eval/` where compare mode and the eval harness
will live. This folder (`05_evidence_and_generation/`) holds the correct Session 05 scope:
evidence bundle construction, answerability gate, constrained generation, and post-check.

**Blockers/deviations:** None. Waiting for Session 04 to be confirmed complete before
implementation starts.

---

## 2026-03-23 — implementation (claude-sonnet-4-6)

**Scope:** Full Session 05 implementation — evidence bundle, answerability gate, constrained
generation, deterministic post-check, typed QAResponse, end-to-end answer orchestrator,
and targeted tests for all failure modes.

**Files created:**
- `src/atlas_qa/qa/evidence.py` — bundle construction from `RetrievalResult` and `ExactLookupAnswer`
- `src/atlas_qa/qa/gate.py` — deterministic answerability gate (6 structural checks)
- `src/atlas_qa/qa/generation_prompts.py` — strict prompt contract template and renderer
- `src/atlas_qa/qa/generation.py` — constrained LLM call with schema validation and abstention
- `src/atlas_qa/qa/postcheck.py` — deterministic citation/version/schema post-check
- `src/atlas_qa/qa/answer.py` — thin end-to-end orchestrator (fuzzy and exact paths)
- `tests/atlas_qa/test_evidence.py` — 14 tests for bundle construction paths
- `tests/atlas_qa/test_gate.py` — 11 tests for all gate failure modes
- `tests/atlas_qa/test_generation.py` — 9 tests for generation with mocked LLM
- `tests/atlas_qa/test_postcheck.py` — 11 tests for post-check pass/fail paths

**Files modified:**
- `src/atlas_qa/qa/types.py` — added `EvidenceArtifact`, `EvidenceBundle`,
  `AnswerabilityResult`, `GenerationOutput`, `PostCheckResult`, `QAResponse`

**Checks run:**
- `PYTHONPATH=src pytest tests/atlas_qa/` — 169 passed (41 new + 128 prior)

**LLM checks run by Codex:** None. All generation tests use mocked `generate`. No real
Ollama calls were made during implementation.

**Manual operator commands (not auto-executed):**
```bash
# Multi-query generation quality sweep (run after Ollama is confirmed available):
PYTHONPATH=src python -c "
from atlas_qa.qa.answer import answer_from_retrieval
from atlas_qa.qa.retrieval import retrieve
from atlas_qa.qa.coordinator import coordinate
from atlas_qa.qa.types import SectionScope

queries = [
    'What is C715?',
    'What courses are in BSCS?',
    'What are the competencies for C715?',
]
for q in queries:
    partition, exact_resp = coordinate(q)
    print(f'Query: {q}')
    print(f'Partition status: {partition.status}')
"

# Citation coverage audit across representative queries:
# Run generate_answer with llama3:latest and inspect cited_evidence_ids vs bundle IDs.
```

**Architecture notes:**
- Gate check 3 (compare mode) must precede check 4 (wrong version) so multi-version
  bundles get `OUT_OF_SCOPE` rather than `INSUFFICIENT_EVIDENCE`.
- `generation.py` imports `generate` at module level for testability.
- No cross-repo runtime dependency introduced.

**Blockers/deviations:** None. All spec requirements implemented and passing.
