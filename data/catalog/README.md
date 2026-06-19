# data/catalog — Atlas-Local Catalog Artifact Mirror

## Purpose

This directory contains catalog data artifacts mirrored from the catalog
pipeline currently housed in the upstream `wgu-reddit` repo
(`WGU_catalog/outputs/`) for Atlas-local use.

These are **build-time inputs and QA runtime inputs**. Atlas QA runtime resolves
all catalog data from this directory — no runtime reads from `wgu-reddit` paths.

Current mirror state:
- mirrored on 2026-06-18 from `/Users/buddy/Desktop/WGU-Reddit/WGU_catalog`
- 111 raw text editions, spanning 2017-01 through 2026-06
- missing archive editions remain 2017-02, 2017-04, and 2017-06
- raw PDFs are intentionally not mirrored here

Mirrored per `_internal/atlas_qa/STAGE_1_DEPENDENCY_INVENTORY.md` (§1 and §8).

---

## Directory layout

```
data/catalog/
  trusted/
    2026_03/              ← frozen current-site structured snapshot (committed)
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
  program_names/          ← per-edition program index/block parser outputs
      YYYY_MM_program_blocks_v11.json
      YYYY_MM_program_index_v11.json
      YYYY_MM_program_names_v10.json where available
  raw_catalog_texts/      ← extracted catalog text, one file per mirrored edition
      catalog_YYYY_MM.txt
```

---

## Mirror notes

`change_tracking/`, `edition_diffs/`, `helpers/`, `program_names/`, and
`raw_catalog_texts/` are the mirrored artifact families. Helper files and raw
catalog text files are local large build inputs and are gitignored. `trusted/2026_03/`
is a frozen site-current snapshot, not a rolling "latest edition" directory.
The Atlas public runtime artifacts in `public/data/` still use this 2026-03
current snapshot until a trusted newer snapshot is created and the site-data
builder is updated to consume it.

Recent verified changes in the mirrored edition diffs:
- `2026-03 -> 2026-04`: no course or program changes
- `2026-04 -> 2026-05`: 28 course additions and 2 program additions (`BSAIE`, `BSPM`)
- `2026-05 -> 2026-06`: `E200` added, `D436` removed, no program additions/removals, 2 version changes

## Large-file policy (helpers/raw text/program names)

The three v10 helper files are gitignored per `.gitignore` (lines 27–30):
- `course_index_v10.json` — 58 MB
- `degree_snapshots_v10_seed.json` — 524 KB
- `sections_index_v10.json` — 824 KB

The helper files, raw catalog texts, and program-name artifacts must be copied
manually from:
```
/path/to/wgu-reddit/WGU_catalog/
```

To acquire them after a fresh clone, run from the Atlas repo root:
```bash
mkdir -p data/catalog/{change_tracking,edition_diffs,helpers,program_names,raw_catalog_texts}
cp <wgu-reddit>/WGU_catalog/outputs/change_tracking/* data/catalog/change_tracking/
cp <wgu-reddit>/WGU_catalog/outputs/edition_diffs/* data/catalog/edition_diffs/
cp <wgu-reddit>/WGU_catalog/outputs/helpers/* data/catalog/helpers/
cp <wgu-reddit>/WGU_catalog/outputs/program_names/* data/catalog/program_names/
cp <wgu-reddit>/WGU_catalog/data/raw_catalog_texts/* data/catalog/raw_catalog_texts/
```

The `trusted/2026_03/` edition files are committed and do not require separate acquisition.

Do not copy raw PDFs into Atlas unless a future task explicitly changes the
storage policy.

---

## Source

Upstream today: `wgu-reddit/WGU_catalog/outputs/`

Future target boundary: `wgu-catalog` should own acquisition, parsing,
validation, change tracking, and edition diffs. Atlas should consume a stable
catalog-output directory or committed mirror, not parser internals.

Mirrored as build-time inputs. Atlas QA code imports from these paths, not from upstream.
Per `STAGE_0_OWNERSHIP_CONTRACT.md` §2 and §4.

Operational caution: `parse_catalog_v11.py` must be treated as authoritative
only when run over the full corpus. Running it for a single edition rebuilds
global indexes from an incomplete input set and invalidates downstream change
tracking and diff outputs. Use full reprocess / `--all` semantics for
authoritative refreshes.
