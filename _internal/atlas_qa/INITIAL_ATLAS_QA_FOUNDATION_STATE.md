# Initial Atlas QA Foundation State

## 1) Governing docs in force
1. `LOCAL_8B_RAG_SYSTEM_DESIGN.md`
2. `STAGE_0_OWNERSHIP_CONTRACT.md`
3. `STAGE_1_DEPENDENCY_INVENTORY.md`

These three documents are the active control set for Atlas QA foundation planning and Stage 2 readiness.

## 2) Current Atlas QA workspace state
- Workspace root: `/Users/buddy/projects/wgu-atlas/_internal/atlas_qa/`
- Work session root: `/Users/buddy/projects/wgu-atlas/_internal/atlas_qa/work_sessions/`
- Current session directories present:
  - `00_atlas_foundation`
  - `01_canonical_objects`
  - `02_exact_lookup_path`
  - `03_scope_partitioning`
  - `04_fuzzy_retrieval`
  - `05_compare_and_eval`
- Governing docs now located in Atlas:
  - `_internal/atlas_qa/LOCAL_8B_RAG_SYSTEM_DESIGN.md`
  - `_internal/atlas_qa/STAGE_0_OWNERSHIP_CONTRACT.md`
  - `_internal/atlas_qa/STAGE_1_DEPENDENCY_INVENTORY.md`

## 3) Dependency snapshot
Counts by strategy from `STAGE_1_DEPENDENCY_INVENTORY.md`:
- already in Atlas: `6`
- mirror: `6`
- port: `6`
- keep as-is: `3`
- exclude: `2`
- total dependencies: `23` (all classified)

## 4) Atlas target path contract
- Mirrored catalog artifacts target:
  - `data/catalog/trusted/2026_03/`
  - `data/catalog/change_tracking/`
  - `data/catalog/edition_diffs/`
  - `data/catalog/helpers/course_index_v10.json`
  - `data/catalog/helpers/degree_snapshots_v10_seed.json`
  - `data/catalog/helpers/sections_index_v10.json`
- Future Atlas QA code target:
  - `src/atlas_qa/llm/`
  - `src/atlas_qa/utils/`
  - `src/atlas_qa/qa/`
- Work session docs target:
  - `_internal/atlas_qa/work_sessions/<session_name>/`

## 5) Runtime boundary contract
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

## 6) LLM utility port contract
Minimum viable port only (no benchmark migration):
- provider/client entry point
- model registry/config surface
- structured call result type
- JSON extraction
- schema validation + fallback
- failure/flag recording fields
- run artifact capture pattern

Foundation expectation before broader QA implementation:
- Atlas-local structured-output substrate must be working in-repo (Ollama-first path), while preserving provider abstraction so model/provider choice remains swappable.

Required failure/flag surface (or equivalent):
- `raw_text`
- `llm_failure`
- `parse_failure`
- `schema_failure`
- `num_retries`
- `error_message`

Explicit exclusions:
- benchmark runners and panel builders
- Reddit-specific classifier prompts/labels
- cost/latency benchmarking helpers
- Reddit-specific config/env plumbing

## 7) Catalog mirror contract
Exact artifact families to mirror from dependency inventory:
1. trusted catalog outputs (`trusted/2026_03`)
2. change tracking
3. edition diffs
4. helper index: `course_index_v10.json`
5. helper index: `degree_snapshots_v10_seed.json`
6. helper index: `sections_index_v10.json`

Atlas targets are under `data/catalog/...` as listed in Section 4.

Repo policy note for large helper JSONs:
- `course_index_v10.json` is large (documented as ~59 MB).
- Large helper JSON handling (commit vs ignore + reproducible acquisition path) is pending file/size/reproducibility inspection and must be decided before Stage 2 migration execution.

## 8) Explicit non-goals for this phase
- No code or data migration.
- No parser rewrites.
- No canonical object generation.
- No retrieval implementation.
- No eval harness implementation.

## 9) Stage 2 entry criteria (checklist only)
- [ ] Governing docs confirmed in force and co-located in Atlas QA workspace.
- [ ] Dependency classification remains complete (no uncategorized dependency).
- [ ] Atlas target paths confirmed for all mirror and port items.
- [ ] Runtime boundary/forbidden import rule approved.
- [ ] Minimum viable LLM utility port scope approved.
- [ ] Catalog mirror policy approved, including large-file handling.
- [ ] Open design risks adjudicated or assigned explicit decision owners.

## 10) Open design risks
- Large-file repo policy for mirrored helper JSONs remains a decision gate pending inspection evidence.
- Evidence reference ID format is explicitly TBD/RFI; no long-term citation ID standard is frozen in this phase.
- Minimum viable LLM port boundary can creep without a locked include/exclude list.
