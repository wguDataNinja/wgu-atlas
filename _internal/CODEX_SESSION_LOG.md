# Codex Session Log

Instructions for Codex:
- Write all decisions, changes, discoveries, and progress here.
- Timestamp each entry.
- Use this structure for each entry:
  ```
  ## YYYY-MM-DD HH:MM — Short summary
  - Decision: ...
  - Changed: ...
  - Discovered: ...
  - Next: ...
  ```
- Keep entries terse. This is the session's single source of truth
  for what happened.
- If a task is deferred or blocked, say why.

---

## 2026-06-18 — Session start

No entries yet. Codex will write here.

## 2026-06-18 19:04 EDT — Preflight and source discovery
- Inspected: `_internal/CODEX_SESSION.md`, `_internal/ATLAS_CONTROL.md`, `_internal/ATLAS_REPO_MEMORY.md`, initial `git status --short`, and local repo locations.
- Discovered: the session objective is catalog mirror + docs/split-readiness, not a repo split; mandatory log is append-only. Atlas working tree already has many modified/untracked files before this pass.
- Discovered: likely catalog pipeline source is `/Users/buddy/Desktop/WGU-Reddit/WGU_catalog`.
- Decision: avoid unrelated cleanup and touch only files needed for catalog mirror/docs/logging.
- Next: verify source and target artifact freshness/counts before copying.

## 2026-06-18 19:05 EDT — Mirrored catalog outputs into Atlas
- Inspected: source raw PDF/text counts and output families under `/Users/buddy/Desktop/WGU-Reddit/WGU_catalog`.
- Discovered: source has 111 raw PDFs and 111 raw text files, including `catalog_2026_04`, `catalog_2026_05`, and `catalog_2026_06`.
- Changed: refreshed `data/catalog/change_tracking/`, `data/catalog/edition_diffs/`, and `data/catalog/helpers/` from source outputs.
- Changed: added Atlas mirror directories `data/catalog/program_names/` and `data/catalog/raw_catalog_texts/`; copied 321 program-name artifacts and 111 raw catalog text files.
- Decision: did not mirror raw PDFs into Atlas; the session mirror target names raw text plus derived output families, and PDFs are large archival source files.
- Validation: `summary_stats.json` reports 111 editions and date range `2017-01 → 2026-06`; copied `edition_diffs_full.json` and `catalog_2026_06.txt` match source by `cmp`.
- Discovered: on-disk artifacts differ from prompt on program changes. `2026-04→2026-05` reports 28 course additions plus 2 program additions (`BSAIE`, `BSPM`); `2026-05→2026-06` reports `E200` added and `D436` removed with 0 program additions/removals and 2 version changes.
- Next: update Atlas docs to reflect verified mirror state, acquisition workflow, parser full-corpus footgun, and future `wgu-catalog` boundary.

## 2026-06-18 19:15 EDT — Updated docs and build path boundary
- Changed: `scripts/build_site_data.py` now prefers `WGU_CATALOG_OUTPUTS`, keeps `WGU_REDDIT_PATH` as compatibility, and defaults to `data/catalog/`.
- Changed: `data/catalog/README.md` now documents the 2026-06 mirror, mirror families, raw-PDF skip policy, recent verified transitions, future `wgu-catalog` boundary, and full-corpus parser rule.
- Changed: `README.md`, `README_INTERNAL.md`, `_internal/ATLAS_CONTROL.md`, `_internal/ATLAS_REPO_MEMORY.md`, and `_internal/DEV_LOG.md` now distinguish the 2026-06 history mirror from the frozen 2026-03 public site-current snapshot.
- Changed: `.gitignore` now ignores `data/catalog/raw_catalog_texts/*.txt`; raw texts remain locally mirrored but should not be committed as a 92 MB artifact set.
- Decision: did not run `scripts/build_site_data.py`; it still depends on `trusted/2026_03` for current-course/program exports and no trusted 2026-06 snapshot exists yet.
- Next: run focused verification and record remaining operator action.

## 2026-06-18 19:24 EDT — Final verification
- Ran: `python3 -m py_compile scripts/build_site_data.py` successfully.
- Verified: `data/catalog/change_tracking/summary_stats.json` reports 111 editions and date range `2017-01 → 2026-06`.
- Verified: final three transitions are `2026-03→2026-04` no changes, `2026-04→2026-05` 28 course additions / 2 program additions / 1 version change, and `2026-05→2026-06` 1 course added / 1 removed / 2 version changes.
- Verified: local mirror contains 111 raw text files and 321 program-name artifacts.
- Verified: `data/catalog/raw_catalog_texts/*.txt` and helper JSONs are ignored; `data/catalog/program_names/` remains visible to Git.
- Remaining operator action: create/freeze a trusted 2026-06 current snapshot before regenerating `public/data/` as a 2026-06 current-site baseline.

## 2026-06-18 19:39 EDT — Roadmap preflight
- Inspected: current session log, ATLAS control/memory docs, DEV_LOG, `data/catalog/README.md`, `scripts/build_site_data.py`, `data/catalog/`, `public/data/`, upstream `acquire_catalog.py`, and `parse_catalog_v11.py` entry point.
- Discovered: `public/data/homepage_summary.json`, `public/data/courses.json`, and `public/data/programs.json` still expose 2026-03 as site-current; `data/catalog/change_tracking/summary_stats.json` exposes 111 editions through 2026-06.
- Discovered: `data/catalog/trusted/` only has `2026_03`; no `trusted/2026_06` current snapshot exists.
- Discovered: `parse_catalog_v11.py` still defaults to processing only 2026-03 unless `--all` is passed; this is the concrete implementation source of the single-edition footgun.
- Decision: create a new roadmap artifact rather than changing execution control priorities or running long pipelines.
- Next: write `_internal/CODEX_ROADMAP.md` with phased priorities, dependencies, delegation guidance, risks, and recommended execution order.

## 2026-06-18 19:45 EDT — Roadmap artifact complete
- Changed: created `_internal/CODEX_ROADMAP.md`.
- Contents: current-state summary, immediate operational priorities, six strategic phases, decision forks, cleanup/polish backlog, delegation guidance, risk register, 2-6 week execution order, top recommended next actions, and explicit non-goals.
- Decision: roadmap recommends catalog currency stabilization before broad homepage implementation unless trusted 2026-06 snapshot work becomes a time sink.
- Decision: roadmap keeps the repo split deferred; it prioritizes parser guardrails and output-contract definition before creating `wgu-catalog`.
- Verified: roadmap includes required sections and explicitly separates weaker-agent work, strong Codex work, and operator/manual-only work.
- Next: use the roadmap to start with checkpointing mirror changes, creating `trusted/2026_06/`, then making site-data builds edition-configurable.
