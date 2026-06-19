# HANDOFF

Updated: 2026-06-18
Repo: wgu-atlas
Role: Current assistant/coding-agent entry point.

This file is the current entry point; the detailed planning rationale lives in the linked Codex/session files below.

## Read first

1. [`_internal/CODEX_ROADMAP.md`](_internal/CODEX_ROADMAP.md) — Latest forward-looking execution roadmap (753 lines, generated 2026-06-18). Covers current state, strategic priorities, decision forks, risk register, and execution timeline. **Not a replacement for ATLAS_CONTROL.md.**
2. [`_internal/ATLAS_CONTROL.md`](_internal/ATLAS_CONTROL.md) — Current execution control (483 lines). Active workstream status and next steps. Authoritative for current work.
3. [`_internal/ATLAS_REPO_MEMORY.md`](_internal/ATLAS_REPO_MEMORY.md) — Durable architecture facts, data flow, contracts, and design rationale (1384 lines). Long-lived reference companion to CONTROL.
4. [`_internal/CODEX_SESSION.md`](_internal/CODEX_SESSION.md) — Codex CLI session brief that drove the 2026-06-18 catalog mirror refresh (522 lines). Two priorities: bring catalog pipeline forward through 2026-04/05/06 editions, prepare for future `wgu-catalog` split.
5. [`_internal/CODEX_SESSION_LOG.md`](_internal/CODEX_SESSION_LOG.md) — Record of what Codex did during that session (71 lines).
6. [`AGENTS.md`](AGENTS.md) — Agent contract, directory map, commands, and watchouts.
7. [`README.md`](README.md) — Public-facing orientation, data provenance, current status.
8. [`data/catalog/README.md`](data/catalog/README.md) — Catalog mirror documentation (121 lines). Directory layout, mirror state, file conventions.

## Current state

Next.js static site (public-facing) for WGU course, program, and catalog history exploration. Built from validated WGU public catalog archives. Also contains an Atlas QA subsystem (Python, local 8B models) for intelligent course/program Q&A.

**Catalog state:**
- 111 catalog editions mirrored in `data/catalog/` (2017-01 through 2026-06).
- Three editions missing from archive: 2017-02, 2017-04, 2017-06.
- Mirrored families: `change_tracking/`, `edition_diffs/`, `helpers/`, `program_names/`, `raw_catalog_texts/` (local, gitignored).
- `data/catalog/trusted/` contains only `trusted/2026_03/` — the frozen site-current snapshot.

**Public/data mismatch:**
- `public/data/homepage_summary.json` reports `data_date: "2026-03"`, archive span 2017-01 to 2026-03, 108 editions.
- README says 111 editions through 2026-06. The 2026-04/05/06 editions exist in catalog mirror but not promoted to trusted.
- Public site still uses 2026-03 as current edition. No trusted 2026-06 snapshot exists.

**Deployment:**
- Static export via Next.js build, deployed via GitHub Pages + GitHub Actions on push.
- `basePath: /wgu-atlas` in Next.js config.

**Known recent catalog changes:**
- 2026-03 to 2026-04: no course or program changes.
- 2026-04 to 2026-05: 28 course additions, 2 program additions (BSAIE, BSPM).
- 2026-05 to 2026-06: E200 added, D436 removed, no program additions/removals, 2 version changes.

## Current priority

1. Preserve/checkpoint current 2026-06 mirror state.
2. Create trusted 2026-06 current snapshot (`data/catalog/trusted/2026_06/`).
3. Make `scripts/build_site_data.py` edition-configurable with `WGU_CATALOG_CURRENT_EDITION`.
4. Regenerate `public/data/` only after trusted 2026-06 validation passes.
5. Defer actual `wgu-catalog` repo split until parser guardrails and output contract are documented.

## Next safe actions

1. Review/checkpoint dirty working tree and mirror docs. The 2026-06-18 session may have left uncommitted catalog changes.
2. Inventory how `trusted/2026_03/` was produced — what scripts, what validation, what acceptance criteria.
3. Create/validate `data/catalog/trusted/2026_06/` following the same pattern.
4. Add `WGU_CATALOG_CURRENT_EDITION` support to `scripts/build_site_data.py`.
5. Run 2026-03 baseline build as safe reference — verify `public/data/` matches current deployed state.
6. Do not publish 2026-06 until trusted snapshot exists and edition config is ready.
7. Document data currency matrix in `docs/data_currency.md`.

## Do not do

- Do not update public copy to claim 2026-06 current active state until `public/data/` is regenerated from trusted 2026-06.
- Do not run `scripts/build_site_data.py` as a publish step until trusted 2026-06 exists and edition config is ready.
- Do not regenerate public runtime from 2026-06 before `trusted/2026_06/` exists.
- Do not start actual `wgu-catalog` repo split unless explicitly activated.
- Do not run long full upstream pipeline jobs without operator approval.
- Do not commit raw PDFs or raw catalog text files.
- Do not clean unrelated dirty files opportunistically.
- Do not redesign homepage around stale/ambiguous current data.

## Key paths

- `src/app/`, `src/components/`, `src/lib/` — **source code**: Next.js App Router, React components, shared utilities.
- `src/atlas_qa/` — **source code**: Python QA subsystem (retrieval, generation, eval).
- `public/data/` — **public/publishable outputs**: site-consumed JSON (courses, events, search index). Tracked, deployed with site.
- `data/catalog/trusted/2026_03/` — **source inputs**: frozen site-current snapshot (8 files). Currently the only trusted snapshot.
- `data/catalog/trusted/2026_06/` — **intended source inputs**: next trusted snapshot (does not exist yet).
- `data/catalog/change_tracking/`, `edition_diffs/`, `program_names/` — **generated outputs**: mirrored history/diff artifacts (tracked).
- `data/catalog/helpers/` — **local-only/ignored**: large JSON build tools (course_index_v10.json 58MB, etc.).
- `data/catalog/raw_catalog_texts/` — **local-only/ignored**: raw scraped edition texts (gitignored .txt files).
- `scripts/` — **scripts/tools**: ~22 Python data build and validation scripts.
- `tests/` — **tests/QA**: pytest test suite (276 tests for atlas_qa).
- `_internal/` — **docs/control docs**: CONTROL, REPO_MEMORY, DEV_LOG, CODEX_*, WORKQUEUE. Tracked; classify by specific doc.
- `artifacts/` — **unknown/ambiguous**: pipeline run artifacts (JSONL). Not in gitignore — inspect before publishing.

## Current data/status

- 111 catalog editions mirrored (2017-01 through 2026-06), 3 missing.
- 838 active AP course codes (2026-03 baseline), 52 active certificate codes.
- Public data frozen at 2026-03 (108 editions in published JSON vs 111 mirrored).
- No trusted 2026-04/05/06 snapshot exists.
- `build_site_data.py` currently reads from `trusted/2026_03/` — hardcoded.
- 3 catalog editions missing from archive: 2017-02, 2017-04, 2017-06.
- Certificate codes tracked only from 2024-09 forward.
- Active branch: `homepage-redesign` (UI polish). `main` is stable deployed baseline.
- Atlas QA subsystem: 276 tests, local 8B RAG model, compare mode, eval harness.

## Safe commands

- `npm run lint` — ESLint
- `pytest` — run Python QA tests (276 tests)
- `python3 scripts/validate_canonical_objects.py` — validate canonical course/program objects
- `python3 scripts/validate_lineage_decisions.py` — validate program lineage
- `python3 scripts/build_course_cards.py` — build QA course cards (no side effects)
- `python3 -m py_compile scripts/build_site_data.py` — syntax check without executing
- `npm run build` — safe to run (generates `out/`), but verify deployment coupling before treating as non-risky

## Gated commands

The following require approval or caution:

- `python3 scripts/build_site_data.py` when generating publishable `public/data/` — especially if targeting 2026_06 before trusted snapshot exists
- Any run targeting `WGU_CATALOG_CURRENT_EDITION=2026_06` before trusted snapshot exists
- Upstream catalog acquisition/parser/change-tracking pipeline runs (lives in wgu-reddit repo)
- Parser guardrail changes
- Actual `wgu-catalog` repo split
- Deploy/publish decisions (GitHub Actions auto-deploys on push)
- Destructive cleanup in dirty working tree (mirror changes mixed with unrelated work)
- `python3 scripts/compare_models.py` — if it invokes local 8B models
- Any `run_gold_eval.py` or model comparison commands that invoke inference

## Known risks

1. **108 vs 111 edition mismatch**: `homepage_summary.json` reports 108 editions through 2026-03. README says 111 through 2026-06. Public data is stale.
2. **No trusted 2026-06 snapshot**: The 2026-04/05/06 editions exist in catalog mirror but were never validated/promoted to `trusted/`. Any claim of current data currency is inaccurate.
3. `build_site_data.py` variable names and hardcoded trusted paths remain misleading — inspect before modifying.
4. `summary_stats.json` reports active counts cautiously; upstream schema review needed before relying on counts.
5. Raw/helper catalog files (`helpers/`, `raw_catalog_texts/`) are large and must stay gitignored.
6. Dirty working tree can mix mirror changes with unrelated work — checkpoint before new work.
7. `_internal/` is tracked and contains design docs, session notes, QA plans. These would become public on deploy.
8. `artifacts/` at repo root contains pipeline run outputs (JSONL) and is not in gitignore — inspect before publishing.
9. `_internal/` also exists at `\_internal/` (with backslash prefix) — possible filename encoding artifact.

## Latest planning sources

### Primary

- [`_internal/CODEX_ROADMAP.md`](_internal/CODEX_ROADMAP.md) — Latest forward-looking execution roadmap (753 lines, 2026-06-18). 10 sections: current state, priority, strategic phases, decision forks, delegation guidance, risk register, execution timeline, top recommendations, non-goals.

### Supporting

- [`_internal/CODEX_GPT_PROMPT.md`](_internal/CODEX_GPT_PROMPT.md) — ChatGPT-facing prompt that started the Codex workflow (50 lines).
- [`_internal/CODEX_SESSION.md`](_internal/CODEX_SESSION.md) — Codex CLI session brief that drove the 2026-06-18 catalog mirror work (522 lines).
- [`_internal/CODEX_SESSION_LOG.md`](_internal/CODEX_SESSION_LOG.md) — Record of Codex actions during that session (71 lines).
- [`_internal/ATLAS_CONTROL.md`](_internal/ATLAS_CONTROL.md) — Current execution control, authority map, workstream status (483 lines).
- [`_internal/ATLAS_REPO_MEMORY.md`](_internal/ATLAS_REPO_MEMORY.md) — Durable architecture facts, data flow, design rationale (1384 lines).
- [`_internal/DEV_LOG.md`](_internal/DEV_LOG.md) — Reverse-chronological session ledger (679 lines).
- [`_internal/WORKQUEUE.md`](_internal/WORKQUEUE.md) — Active working backlog with `now`/`next`/`later`/`blocked` sections (509 lines).
- [`data/catalog/README.md`](data/catalog/README.md) — Catalog mirror layout and conventions (121 lines).
- [`AGENTS.md`](AGENTS.md) — Agent contract and watchouts.
- [`README.md`](README.md) — Public orientation and data provenance.
