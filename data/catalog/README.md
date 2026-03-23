# data/catalog — Atlas-Local Catalog Artifact Mirror

## Purpose

This directory contains catalog data artifacts mirrored from the upstream
`wgu-reddit` repo (`WGU_catalog/outputs/`) for Atlas-local use.

These are **build-time inputs and QA runtime inputs**. Atlas QA runtime resolves
all catalog data from this directory — no runtime reads from `wgu-reddit` paths.

Mirrored per `_internal/atlas_qa/STAGE_1_DEPENDENCY_INVENTORY.md` (§1 and §8).

---

## Directory layout

```
data/catalog/
  trusted/
    2026_03/              ← current edition structured outputs (committed)
      certs_2026_03.csv
      course_index_2026_03.json
      courses_2026_03.csv
      degree_snapshots_2026_03.json
      manifest_2026_03.json
      program_blocks_2026_03.json
      program_index_2026_03.json
      sections_index_2026_03.json
  change_tracking/        ← edition-level change records (committed)
      adjacent_diffs.json
      adjacent_diffs_summary.csv
      course_history.csv
      program_history.csv
      summary_stats.json
  edition_diffs/          ← per-edition diff artifacts (committed)
      edition_diffs_events.json
      edition_diffs_full.json
      edition_diffs_rollups.json
      edition_diffs_summary.csv
  helpers/
      course_index_v10.json         ← NOT committed (gitignored, 58 MB)
      degree_snapshots_v10_seed.json ← NOT committed (gitignored, 524 KB)
      sections_index_v10.json        ← NOT committed (gitignored, 824 KB)
```

---

## Large-file policy (helpers/)

The three v10 helper files are gitignored per `.gitignore` (lines 27–30):
- `course_index_v10.json` — 58 MB
- `degree_snapshots_v10_seed.json` — 524 KB
- `sections_index_v10.json` — 824 KB

These files must be copied manually from:
```
/path/to/wgu-reddit/WGU_catalog/outputs/helpers/
```

To acquire them after a fresh clone, run from the repo root:
```bash
cp <wgu-reddit>/WGU_catalog/outputs/helpers/course_index_v10.json data/catalog/helpers/
cp <wgu-reddit>/WGU_catalog/outputs/helpers/degree_snapshots_v10_seed.json data/catalog/helpers/
cp <wgu-reddit>/WGU_catalog/outputs/helpers/sections_index_v10.json data/catalog/helpers/
```

The `trusted/2026_03/` edition files are committed and do not require separate acquisition.

---

## Source

Upstream: `wgu-reddit/WGU_catalog/outputs/`

Mirrored as build-time inputs. Atlas QA code imports from these paths, not from upstream.
Per `STAGE_0_OWNERSHIP_CONTRACT.md` §2 and §4.
