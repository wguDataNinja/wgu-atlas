# Session Spec — 00_atlas_foundation (Stage 0 Implementation Proposal)

## Session type
Implementation proposal only (no code/data/script movement yet).

## Scope
Define the narrow Stage 0 implementation boundary so Codex can execute without interpretation drift.

## 1) Most-recent-entity-version executable rule
Current state from governing docs:
- The policy direction is fixed (`most recent available version for resolved entity`).
- The exact ordering basis is **not fully fixed** yet as a single executable key contract across artifact families.

Stage 0 narrow rule proposal:
1. Build a normalized `version_key` per candidate record using strict `YYYY_MM` parsing.
2. Source of truth for version token, in order:
   - explicit `version` field on entity-linked artifact row/object (if present)
   - manifest-linked version field for that entity (guide/catalog manifest rows)
   - trusted catalog edition token derived from normalized source path segment (for catalog-trusted artifacts only)
3. Select max `version_key` within resolved entity scope only.
4. If no valid `YYYY_MM` token exists for any candidate in scope, return `ambiguous_version` (no silent fallback).

Implementation fields/keys to use first:
- `version` (where present in parsed/manifest artifacts)
- normalized edition token from trusted catalog artifact provenance path
- resolved entity id (`program_code` or `course_code`) for scope filtering before ranking

Known ambiguity still blocking full lock:
- exact fallback precedence between manifest-derived and provenance-derived version when both exist but disagree
- handling legacy/non-`YYYY_MM` version strings if encountered
- tie-breaker contract when multiple source families expose same `version_key`

## 2) Structured-output substrate verification bar (Stage 0 "working")
Stage 0 is only complete when all checks below pass in Atlas-local code:
1. Successful structured parse path: valid JSON payload parsed into typed object.
2. Schema validation path: payload validated against Pydantic schema.
3. Fallback path: malformed/partial model output triggers fallback extraction/repair path.
4. Parse/schema failure flag capture: `parse_failure` and `schema_failure` set correctly on failures.
5. Run artifact capture: per-call artifact written with prompt, raw output, validation/failure flags.

Minimal runnable proof required in Atlas:
- one local command/script invocation that executes:
  - one success case (schema-valid response)
  - one forced-failure case (invalid response) proving fallback + flags
- proof output includes:
  - structured result object
  - failure flags
  - artifact file location(s)

## 3) Minimum viable provider abstraction boundary (Stage 0)
Port first (minimum set only):
- `llm/client` (provider dispatch + text generation entry point)
- `llm/registry` (model/provider mapping surface)
- `llm/types` (`LlmCallResult`-equivalent result envelope)
- `llm/structured` (JSON extraction + schema validation + fallback)
- `llm/artifacts` (run artifact write helper)
- `utils/logging` (minimal runtime logging wrapper)

Must not port in Stage 0:
- benchmark runners/panels and benchmark orchestration
- cost/latency estimation stack
- Reddit-specific classifier prompts/labels
- Reddit-specific env/config loaders
- any non-Atlas analysis/report generation tooling

## 4) Large-file inspection step
Placement:
- Perform file/size/reproducibility inspection as a Stage 0 gate **before** any catalog-mirror execution.
- This gate informs repo policy; it does not mirror files yet.

Inspect first:
1. `WGU_catalog/outputs/helpers/course_index_v10.json`
2. `WGU_catalog/outputs/helpers/degree_snapshots_v10_seed.json`
3. `WGU_catalog/outputs/helpers/sections_index_v10.json`
4. directory-level size/count for:
   - `WGU_catalog/outputs/trusted/2026_03/`
   - `WGU_catalog/outputs/change_tracking/`
   - `WGU_catalog/outputs/edition_diffs/`

Inspection output needed (in session execution, not this proposal):
- file sizes
- file counts for mirrored directories
- reproducibility note (how each artifact can be regenerated/refetched)
- recommendation input for commit-vs-ignore policy

## Out of scope (this proposal pass)
- no implementation
- no `src/atlas_qa` creation
- no mirroring/copying
- no parser/script rewrites
- no QA pipeline/canonical object work

## Stage 0 proposal exit condition
This proposal is accepted when implementation can start with no unresolved boundary questions except explicitly listed blockers.
