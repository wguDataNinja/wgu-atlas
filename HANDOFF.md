# HANDOFF

Updated: 2026-06-19 (post-program-runtime-export fix)
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
- `data/catalog/trusted/` now contains **two** frozen snapshots: `trusted/2026_03/` (original) and `trusted/2026_06/` (new, created via `scripts/freeze_trusted_snapshot.py`).
- `trusted/2026_06/` is validated and locally consumed. It is **not yet publicly deployed**.

**Public/data state (local):**
- `public/data/homepage_summary.json` locally reports `data_date: "2026-06"`, archive span 2017-01 to 2026-06, 111 editions.
- Local public/data has been regenerated from trusted/2026_06.
- `public/data/programs.json` now exports 198 program records: 116 active and 82 retired. Active program records match `trusted/2026_06/program_blocks_2026_06.json`.
- `BSAIE` and `BSPM` are present in `programs.json`, active in `search_index.json`, included in homepage `newest_programs` / `recent_version_changes`, and generated as static program routes. They render with an intentional "Current Catalog Record" fallback because guide-derived roster/outcomes/resources are not yet attached for those new programs.
- The earlier 2026-06 refresh commit is `9fa38e1`; the program-runtime export correction is local and must be reviewed/staged/committed before push/deploy.
- Deployed site (GitHub Pages) remains at 2026-03 until push + deploy.

**Deployment:**
- Static export via Next.js build, deployed via GitHub Pages + GitHub Actions on push.
- `basePath: /wgu-atlas` in Next.js config.

**Known recent catalog changes:**
- 2026-03 to 2026-04: no course or program changes.
- 2026-04 to 2026-05: 28 course additions, 2 program additions (BSAIE, BSPM).
- 2026-05 to 2026-06: E200 added, D436 removed, no program additions/removals, 2 version changes.

## Current priority

1. ~~Git-steward review and stage/commit~~ ✅ Done — commit `9fa38e1`.
2. **Review/stage/commit the program-runtime export correction** — includes `build_site_data.py`, regenerated `public/data/{programs,search_index,homepage_summary}.json`, program-route fallback, footer currentness wiring, and docs.
3. **Push** `homepage-redesign` branch to origin.
4. **Deploy** — GitHub Actions auto-deploys on push. Verify the workflow runs clean.
5. **Post-deploy smoke checks** on the live site.
6. Defer `wgu-catalog` repo split until parser guardrails and output contract are documented.

## Next safe actions

1. **Git-steward review/stage/commit** the local program-runtime export correction. Do not include unrelated dirty UI/QA files.
2. **Push** — `git push origin homepage-redesign` (manual/operator).
3. **Deploy** — Triggered automatically on push via GitHub Actions `.github/workflows/`. Verify the build + deploy workflow succeeds.
4. **Post-deploy smoke-check** — visit these routes on the live site:
   - `/wgu-atlas/` — homepage shows 2026-06 current, active_ap=866, active_programs=116
   - `/wgu-atlas/courses/E200` — MSHRM Capstone renders
   - `/wgu-atlas/courses/D436` — 404 or clearly retired (removed in 2026-06)
   - `/wgu-atlas/programs/BSAIE` — Bachelor of Science, AI Engineering; shows Current Catalog Record fallback
   - `/wgu-atlas/programs/BSPM` — Bachelor of Science, Project Management; shows Current Catalog Record fallback
   - `/wgu-atlas/schools/business` — includes BSPM in current degrees
   - `/wgu-atlas/schools/technology` — includes BSAIE in current degrees
   - `/wgu-atlas/data` — download links reflect 2026-06 data
   - `/wgu-atlas/methods` — copy still accurate
5. **Document data currency matrix** in `docs/data_currency.md` (deferred — low urgency).
6. **Resume product work** after deploy: homepage redesign, official resource layer, course-page enrichment, Atlas QA F-089 regression fix.

## Do not do

- ~~Do not update public copy to claim 2026-06~~ ✅ Done — public/data committed at 2026-06.
- ~~Do not run `build_site_data.py` as publish step~~ ✅ Done — edition-configurable, deploy-blockers fixed.
- ~~Do not regenerate public runtime before trusted/2026_06 exists~~ ✅ Done — snapshot exists.
- Do not start actual `wgu-catalog` repo split unless explicitly activated.
- Do not run long full upstream pipeline jobs without operator approval.
- Do not commit raw PDFs or raw catalog text files.
- Do not clean unrelated dirty files opportunistically.
- Do not redesign homepage around stale/ambiguous current data (still relevant — deploy first).
- Do not push or deploy without verifying the GitHub Actions workflow is ready.

## Key paths

- `src/app/`, `src/components/`, `src/lib/` — **source code**: Next.js App Router, React components, shared utilities.
- `src/atlas_qa/` — **source code**: Python QA subsystem (retrieval, generation, eval).
- `public/data/` — **public/publishable outputs**: site-consumed JSON (courses, events, search index). Tracked, deployed with site.
- `data/catalog/trusted/2026_03/` — **source inputs**: frozen site-current snapshot (8 files). Currently the only trusted snapshot.
- `data/catalog/trusted/2026_06/` — **source inputs**: next trusted snapshot (created, 8 files, committed).
- `data/catalog/change_tracking/`, `edition_diffs/`, `program_names/` — **generated outputs**: mirrored history/diff artifacts (tracked).
- `data/catalog/helpers/` — **local-only/ignored**: large JSON build tools (course_index_v10.json 58MB, etc.).
- `data/catalog/raw_catalog_texts/` — **local-only/ignored**: raw scraped edition texts (gitignored .txt files).
- `scripts/` — **scripts/tools**: ~22 Python data build and validation scripts.
- `tests/` — **tests/QA**: pytest test suite (276 tests for atlas_qa).
- `_internal/` — **docs/control docs**: CONTROL, REPO_MEMORY, DEV_LOG, CODEX_*, WORKQUEUE. Tracked; classify by specific doc.
- `artifacts/` — **pipeline run artifacts**: JSONL outputs (in `.gitignore`).

## Current data/status

- 111 catalog editions mirrored (2017-01 through 2026-06), 3 missing.
- **Trusted snapshots**: `trusted/2026_03/` (original) and `trusted/2026_06/` (created via `scripts/freeze_trusted_snapshot.py`).
- **Local runtime**: public/data regenerated from trusted/2026_06 — 866 active AP courses, 116 active programs, 52 cert codes.
- Program runtime is now consistent: `programs.json` has 198 records, 116 active, 82 retired; active program codes exactly match trusted 2026_06 program blocks.
- **Deployed runtime**: remains 2026-03 until push + deploy completes.
- `build_site_data.py` now supports `WGU_CATALOG_CURRENT_EDITION` env var (default `2026_03`).
- `active_programs` derived from trusted program_blocks, not program_history.csv status field.
- `programs.json`, program search entries, homepage program lists, school program lists, and program route static params now use the same program records/status contract.
- Build script cleans stale `public/data/courses/*.json` before regenerating active per-course files.
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

1. **108 vs 111 edition mismatch**: RESOLVED — `total_editions` is now data-driven from sections_index keys, resolving to 108 for 2026_03 and 111 for 2026_06.
2. **trusted 2026_06 snapshot**: RESOLVED — snapshot exists and validates. Script-validated pending manual review.
3. **hardcoded `build_site_data.py` paths**: RESOLVED — `WGU_CATALOG_CURRENT_EDITION` env var controls snapshot path.
4. **active_programs=0**: RESOLVED — derived from `len(program_blocks)` instead of program_history.csv status field.
5. **stale per-course files**: RESOLVED — build script cleans `public/data/courses/*.json` before regeneration.
6. **total_course_codes_ever**: RESOLVED — now data-driven from `len(canonical_rows)`.
7. **program runtime export gap**: RESOLVED locally — `build_site_data.py` now writes `public/data/programs.json`; `BSAIE`/`BSPM` resolve as active program pages with intentional fallback messaging for missing guide-derived detail.
8. `summary_stats.json` reports active counts cautiously; upstream schema review needed before relying on counts for anything other than edition-count derivation.
9. Raw/helper catalog files (`helpers/`, `raw_catalog_texts/`) are large and must stay gitignored.
10. Dirty working tree can mix mirror changes with unrelated work — checkpoint before new work.
11. `_internal/` is tracked and contains design docs, session notes, QA plans. These would become public on deploy.
12. `artifacts/` at repo root contains pipeline run outputs (JSONL) — already in `.gitignore` (inspected 2026-06-19: two tiny files, safe).

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

---

## What's done (Packages A-E)

| Package | What | Status |
|---|---|---|
| **A** | `scripts/freeze_trusted_snapshot.py` + `data/catalog/trusted/2026_06/` (8 files) | ✅ Committed |
| **B** | `WGU_CATALOG_CURRENT_EDITION` env var; dynamic TRUST path; data-driven homepage fields | ✅ Committed |
| **C** | Local 2026_06 runtime regeneration; blocker identification | ✅ Committed |
| **D** | `active_programs` fix (program_blocks), stale per-course cleanup, `total_course_codes_ever` data-driven, search/program active status fix | ✅ Committed |
| **E** | `programs.json` export from trusted-current program records; BSAIE/BSPM static routes; program fallback messaging; footer archive-span wiring | ✅ Committed (`7058c05`) |
| **Docs** | HANDOFF, ATLAS_CONTROL, ATLAS_REPO_MEMORY, DEV_LOG updated | ✅ Committed |
| **Git** | `9fa38e1` — 889 files staged/committed. No unrelated files included. | ✅ Committed |
| **Release copy** | Public currentness claims advanced 2026-03→2026-06 (about, methods, data, homepage, courses, schools, README) | ✅ Committed (`c725b00`) |
| **Trusted checker** | `scripts/check_trusted_consistency.py` — 22 automated snapshot checks | ✅ Committed (`13a6881`) |
| **UI polish (leftover)** | Punctuation, print-hidden nav, em-dash cleanup, basePath fallback (9 files) | ✅ Committed (`fee6ed1`) |

## What remains

- **Push** (operator): `git push origin homepage-redesign`
- **Deploy**: GitHub Actions auto-deploys on push. Watch the workflow.
- **Smoke-check** the live site on the routes listed above.
- **Resume product roadmap**: homepage redesign, official resource layer, course-page enrichment, Atlas QA.
- **Review/commit pre-existing QA subsystem work**: 6 modified tracked files (QA source + session docs) and ~30 untracked files remain from earlier sessions — needs focused review before staging.

## My thoughts on next steps

**Immediate (pre-deploy):**
- Push + deploy is the next step. The tree is clean except for pre-existing QA subsystem work that is independent of the deploy.
- Pre-deploy smoke-check routes are listed above.

**Medium-term:**
- **Homepage redesign** is the stated primary product track. The catalog-currentness work existed to make homepage stats data-honest before redesign. That foundation is now ready. The next bounded step is converting the homepage strategy into implementation-ready module specs.
- **Official resource layer** and **course-page enrichment** are the next major content-expansion tracks after homepage.
- **Atlas QA** F-089 regression fix is a small bounded fix that's been deferred through this whole catalog-currentness workstream.

**Deferred:**
- `wgu-catalog` repo split — still deferred. Parser guardrails (`--all` requirement enforcement) and output contract documentation are prerequisites.
- `docs/data_currency.md` — a helpful documentation artifact but not blocking anything.
