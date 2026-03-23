# Initial Atlas QA Foundation State

**Last updated:** 2026-03-23 (Stage 0 baseline completion pass)

## 1) Governing docs in force
1. `LOCAL_8B_RAG_SYSTEM_DESIGN.md`
2. `STAGE_0_OWNERSHIP_CONTRACT.md`
3. `STAGE_1_DEPENDENCY_INVENTORY.md`

These three documents are the active control set for Atlas QA foundation planning and Stage 2 readiness.

---

## 2) Current Atlas QA workspace state

- Workspace root: `/Users/buddy/projects/wgu-atlas/_internal/atlas_qa/`
- Work session root: `/Users/buddy/projects/wgu-atlas/_internal/atlas_qa/work_sessions/`
- Session directories present:
  - `00_atlas_foundation`
  - `01_canonical_objects`
  - `02_exact_lookup_path`
  - `03_scope_partitioning`
  - `04_fuzzy_retrieval`
  - `05_compare_and_eval`
- Governing docs co-located in Atlas:
  - `_internal/atlas_qa/LOCAL_8B_RAG_SYSTEM_DESIGN.md`
  - `_internal/atlas_qa/STAGE_0_OWNERSHIP_CONTRACT.md`
  - `_internal/atlas_qa/STAGE_1_DEPENDENCY_INVENTORY.md`

---

## 3) Dependency snapshot

Counts by strategy from `STAGE_1_DEPENDENCY_INVENTORY.md`:
- already in Atlas: `6`
- mirror (build-time): `6` — **now executed; all 6 artifact families present in `data/catalog/`**
- port (rewrite into Atlas): `6` — **now executed; all 6 LLM utility modules in `src/atlas_qa/llm/` and `src/atlas_qa/utils/`**
- keep as-is (build tool): `3`
- exclude (raw corpus): `2`
- total dependencies: `23` (all classified, no uncategorized)

---

## 4) Atlas-local paths — confirmed present

### LLM substrate (ported)

| Module | Atlas path | Status |
|---|---|---|
| Provider dispatch / client | `src/atlas_qa/llm/client.py` | Present, verified |
| Model registry | `src/atlas_qa/llm/registry.py` | Present, verified |
| Structured call result type | `src/atlas_qa/llm/types.py` | Present, verified |
| JSON extraction + schema validation | `src/atlas_qa/llm/structured.py` | Present, verified |
| Run artifact capture | `src/atlas_qa/llm/artifacts.py` | Present, verified |
| Logging wrapper | `src/atlas_qa/utils/logging.py` | Present, verified |
| Substrate test script | `src/atlas_qa/llm/test_substrate.py` | Present |
| Package init files | `src/atlas_qa/__init__.py`, `src/atlas_qa/llm/__init__.py`, `src/atlas_qa/utils/__init__.py` | Present |

### Catalog artifacts (mirrored)

| Artifact family | Atlas path | Status |
|---|---|---|
| Trusted current edition | `data/catalog/trusted/2026_03/` | **Mirrored 2026-03-23** — 8 files, ~1 MB total |
| Change tracking | `data/catalog/change_tracking/` | **Mirrored 2026-03-23** — 5 files, ~644 KB total |
| Edition diffs | `data/catalog/edition_diffs/` | **Mirrored 2026-03-23** — 4 files, ~244 KB total |
| Helper: course_index_v10.json | `data/catalog/helpers/course_index_v10.json` | **Mirrored 2026-03-23** — 58 MB, gitignored |
| Helper: degree_snapshots_v10_seed.json | `data/catalog/helpers/degree_snapshots_v10_seed.json` | **Mirrored 2026-03-23** — 524 KB, gitignored |
| Helper: sections_index_v10.json | `data/catalog/helpers/sections_index_v10.json` | **Mirrored 2026-03-23** — 824 KB, gitignored |

### Pre-existing artifacts (already in Atlas before Stage 0)

| Artifact | Atlas path | Status |
|---|---|---|
| Parsed guide artifacts (115 files) | `data/program_guides/parsed/` | Present (pre-existing) |
| Guide manifest | `data/program_guides/guide_manifest.json` | Present (pre-existing) |
| Guide anomaly registry | `data/program_guides/guide_anomaly_registry.json` | Present (pre-existing) |
| Section presence matrix | `data/program_guides/section_presence_matrix.csv` | Present (pre-existing) |
| Canonical course index (CSV) | `data/canonical_courses.csv` | Present (pre-existing) |
| Canonical course index (JSON) | `data/canonical_courses.json` | Present (pre-existing) |

---

## 5) LLM substrate verification status

| Path | Status |
|---|---|
| `safe_parse_structured_response` — valid JSON | VERIFIED |
| `safe_parse_structured_response` — parse failure (invalid JSON) | VERIFIED |
| `safe_parse_structured_response` — schema failure (wrong type) | VERIFIED |
| `validate_and_fallback` with defaults | VERIFIED |
| `ArtifactCapture.capture_call` — all flags written to JSONL | VERIFIED |
| `client.generate()` — llm_failure path | VERIFIED |
| `registry.get_model_info('llama3')` — provider=ollama, is_local=True | VERIFIED |
| `client.py` — no cost_latency import | VERIFIED |
| Real Ollama call (llama3, structured JSON output, end-to-end) | **VERIFIED LIVE — 2026-03-23** |
| Real OpenAI call | Pending — OPENAI_API_KEY not set in environment |

**Ollama live call result summary:**
- Model: `llama3:latest` (8B Q4)
- Full path verified: `generate()` → real Ollama HTTP call → `safe_parse_structured_response()` → Pydantic schema validation → `capture_call()` with correct flags → JSONL artifact on disk
- Artifact written to `artifacts/test_runs/run_20260323_034740/artifacts.jsonl`
- `elapsed_sec`: 13.467, `llm_failure`: False, `parse_error`: False, `schema_error`: False

**OpenAI path status:**
- The guard in `_call_openai()` fires before any HTTP call when key is absent — clean failure captured correctly
- Retry loop retries even on permanent key-missing failure (pre-existing behavior from source; noted, not fixed — out of scope for Stage 0)

**Available Ollama models on this machine:**
`llama3:latest` (8B Q4), `llama3.1:latest` (8B Q4), `qwen3.5:9b` (9.7B Q4), `mistral:7b-instruct`, `qwen2.5-coder:7b`, `codestral:latest`
Only `llama3` is registered in `registry.py` at this time.

---

## 6) Catalog mirror policy — resolved

### File size inspection results (2026-03-23)

| File | Size | Policy |
|---|---|---|
| `course_index_v10.json` | 58 MB | **gitignored** — too large; acquire from upstream (see `data/catalog/README.md`) |
| `degree_snapshots_v10_seed.json` | 524 KB | **gitignored** — `.gitignore` already covered all three v10 helpers pre-mirror |
| `sections_index_v10.json` | 824 KB | **gitignored** — see above |
| `trusted/2026_03/` total | ~1 MB | **committed** — all edition files are small and safe |
| `change_tracking/` total | ~644 KB | **committed** |
| `edition_diffs/` total | ~244 KB | **committed** |

**Decision:** `.gitignore` already contained entries for all three v10 helper files before this session (`course_index_v10.json`, `degree_snapshots_v10_seed.json`, `sections_index_v10.json` at lines 27–30). Large-file policy was already implicit; this session confirms and documents it explicitly.

Acquisition path documented in `data/catalog/README.md`.

---

## 7) Runtime boundary contract

Allowed runtime dependency types:
- Atlas-local normalized artifacts under `wgu-atlas/data/...`
- Atlas-local runtime modules under `wgu-atlas/src/...`
- Atlas-local configs/schemas/contracts defined for Atlas QA

Forbidden runtime dependency types:
- Direct runtime reads from `wgu-reddit` paths
- Runtime imports from `wgu-reddit` parser internals
- Hidden cross-repo imports to utility modules in `wgu-reddit/src/...`

Explicit runtime rule:
- Atlas QA runtime must not import from `wgu-reddit`.
- Default version lookup rule: when a user does not specify a version, resolve to the most recent available version for the resolved entity.

**Import boundary confirmed:** No Atlas QA source file imports from `wgu-reddit`. All substrate modules import from `src.atlas_qa.*` only.

---

## 8) LLM utility port scope — resolved

Minimum viable port executed and verified. In-scope items (all ported):
- provider/client entry point ✓
- model registry/config surface ✓
- structured call result type ✓
- JSON extraction ✓
- schema validation + fallback ✓
- failure/flag recording fields ✓
- run artifact capture pattern ✓
- logging wrapper ✓

Explicit exclusions (confirmed not ported):
- cost/latency benchmarking helpers (`cost_latency.py` was created during port, then deleted in audit) ✓
- benchmark runners and panel builders ✓
- Reddit-specific classifier prompts/labels ✓
- Reddit-specific config/env plumbing ✓

---

## 9) Stage 0 completion status

| Item | Status |
|---|---|
| Governing docs in force and co-located in Atlas QA workspace | **COMPLETE** |
| Dependency classification complete (23/23, no uncategorized) | **COMPLETE** |
| Atlas target paths confirmed for all mirror and port items | **COMPLETE** |
| Runtime boundary/forbidden import rule defined and confirmed | **COMPLETE** |
| Minimum viable LLM utility port scope defined and executed | **COMPLETE** |
| Catalog mirror policy resolved, including large-file handling | **COMPLETE** |
| Catalog artifact families mirrored to `data/catalog/` | **COMPLETE** |
| Atlas LLM substrate ported, audited, and clean | **COMPLETE** |
| Real Ollama provider success path verified end-to-end | **COMPLETE** |
| `data/catalog/README.md` documenting mirror contents and acquisition | **COMPLETE** |
| Baseline state doc updated to reflect real Atlas state | **COMPLETE** |

**Stage 0 is complete.**

---

## 10) Stage 2 entry criteria — resolved

- [x] Governing docs confirmed in force and co-located in Atlas QA workspace.
- [x] Dependency classification remains complete (no uncategorized dependency).
- [x] Atlas target paths confirmed for all mirror and port items.
- [x] Runtime boundary/forbidden import rule approved.
- [x] Minimum viable LLM utility port scope approved and executed.
- [x] Catalog mirror policy approved, including large-file handling.
- [x] Open design risks adjudicated or assigned explicit decision owners (see §11).

**Stage 2 is unblocked.**

---

## 11) Open design risks — current status

| Risk | Status |
|---|---|
| Large-file repo policy for mirrored helper JSONs | **RESOLVED** — gitignored per existing `.gitignore`; acquisition path documented |
| Evidence reference ID format | **TBD/RFI** — explicitly deferred; no long-term citation ID standard frozen in this phase |
| Minimum viable LLM port boundary creep | **RESOLVED** — port executed, audited, and scoped; explicit exclusions confirmed |
| Version token conflict precedence (provenance vs manifest) | Remains an open design question for Stage 3+ canonical object construction |
| Tie-break when multiple source families have identical `version_key` | Remains open for Stage 3+ |

---

## 12) What Stage 2 can assume

Stage 2 implementation can safely assume:
- All catalog artifact families are present under `data/catalog/` on any machine that has run the acquisition step documented in `data/catalog/README.md`
- The three v10 helper files are present locally but gitignored; they must be re-acquired after a fresh clone
- All LLM substrate modules are present and correct under `src/atlas_qa/llm/` and `src/atlas_qa/utils/`
- Ollama provider path is live-verified with `llama3`
- No cross-repo runtime imports exist in Atlas QA code
- The structured parse → schema validation → fallback → artifact capture path is end-to-end verified
