# WGU Atlas — Migration Handoff

**From:** `wgu-reddit` (internal research repo)
**To:** `wgu-atlas` (new public-facing site repo)
**Date:** 2026-03-14
**Purpose:** Give the first agent working in `wgu-atlas` an exact, operational map of what to take, what to skip, and what to watch out for.

---

Locked decisions for wgu-atlas

These decisions are already made and should not be re-litigated during migration unless explicitly requested.

Branding
	•	Site name: WGU Atlas
	•	Subtitle: Explore courses, programs, catalog changes, and student discussion
	•	Creator attribution: Created by WGU-DataNinja

Repo
	•	Repo name: wgu-atlas

Product direction
	•	WGU Atlas is a public-facing reference and explorer
	•	It is catalog-history first, but discussion-aware
	•	Student discussion, especially Reddit, is a planned product feature layer
	•	The site must preserve a hard separation between:
	•	official catalog facts
	•	discussion signals
	•	LLM-generated summaries

Technical direction
	•	Preferred stack: Next.js + TypeScript + Tailwind
	•	Deployment target: GitHub Pages via GitHub Actions
	•	Site architecture: static/data-driven; v1 can build entirely from pre-generated JSON/CSV artifacts

Repo scope

This repo is for:
	•	the website source
	•	canonical site data artifacts
	•	minimal reproducible scripts needed to regenerate website data
	•	public-facing documentation and deployment config

This repo is not for:
	•	the full wgu-reddit research pipeline
	•	raw catalog PDF/text archives
	•	obsolete parser versions
	•	legacy/debugging clutter
	•	unrelated Reddit Analyzer internals

Immediate operational goal

The next agent should:
	1.	migrate only the necessary code/data/docs from wgu-reddit
	2.	keep the new repo clean and auditable
	3.	prepare the repo for the first site build
	4.	avoid unnecessary carryover from the old repo


  

## 1. Purpose

`wgu-atlas` is the public-facing website for WGU course/program history and student discussion context. It is completely separate from the Reddit Analyzer research pipeline that lives in `wgu-reddit`. The two repos share data artifacts but not code.

The site can be built entirely from pre-generated static files. **The v1 site build does not require running any Python scripts.** The build script (`build_site_data.py`) is a regeneration tool — it only needs to be re-run when the underlying catalog data is updated.

This document covers what to transfer to `wgu-atlas`, in what form, and what to leave behind.

---

## 2. Source-of-truth documents

These three files in `wgu-reddit` define the project. Read them before doing anything else. They are the session memory for the catalog data layer.

| File | Location | Action |
|---|---|---|
| `README_INTERNAL.md` | `WGU_catalog/README_INTERNAL.md` | Copy into `wgu-atlas/docs/` — reference document for the scraper architecture, parser eras, validation methodology, and all field definitions |
| `SCRAPE_LOG.md` | `WGU_catalog/SCRAPE_LOG.md` | Copy into `wgu-atlas/docs/` — tracks what was built, what is stable, what is deferred |
| `website_design_plan.md` | `WGU_catalog/website_design_plan.md` | Copy into `wgu-atlas/docs/` — the locked-in site design, page structure, and build phases |

These are reference documents in `wgu-atlas`. They do not need to be kept in sync; they describe the state of the data layer as of the transfer date.

---

## 3. Migration inventory

### 3a. Site-ready export files — copy as-is

These are the primary deliverables. The v1 site consumes these directly with no further processing.

All live under:
```
wgu-reddit/WGU_catalog/outputs/site_data/exports/
```

| File / Path | Size | Description | Action |
|---|---|---|---|
| `exports/courses.json` | 712 KB | 1,646 course cards (all AP active + retired + cert). Fields: code, title, active, scope, first/last_seen, edition_count, school, stability_class, ghost_flag, single_appearance_flag, title_variant_class | **Copy as-is** |
| `exports/courses/{code}.json` | 3.4 MB total, 838 files | Individual course detail files for all active AP courses. Fields: canonical_title, observed_titles, programs_timeline (full chronological), current_programs, historical_program_count, edition_count, stability_class, ghost_flag, title_variant_class, title_variant_detail, confidence, notes, colleges_seen | **Copy as-is** |
| `exports/events.json` | 48 KB | 41 events (chronological). Fields: event_id, start/end_edition, event_title, event_type_primary/secondary, severity_score, affected_schools, program/course lists, observed_summary, interpreted_summary, confidence, is_curated_major_event | **Copy as-is** |
| `exports/search_index.json` | 392 KB | 1,842 entries (1,646 courses + 196 programs) for client-side search. Fields: type, code, title, active, scope, school, alt_titles | **Copy as-is** |
| `exports/homepage_summary.json` | 12 KB | Pre-assembled homepage module data. Includes: archive stats, active_by_school counts, recent_version_changes (8 entries), newest_programs (8 entries), recent_course_additions (12 entries), curated_major_events_preview (10 entries) | **Copy as-is** |

**Target path in `wgu-atlas`:** `public/data/` or `static/data/` depending on the framework. Use whatever the static site generator treats as its public-served directory.

---

### 3b. Canonical data artifacts — copy as-is

Intermediate artifacts one level above the exports. Used to rebuild exports if needed and useful as downloadable datasets for the Data page.

All live under:
```
wgu-reddit/WGU_catalog/outputs/site_data/
```

| File | Size | Description | Action |
|---|---|---|---|
| `canonical_courses.csv` | — | 1,646-row course intelligence table (human-readable, for the Data page download) | **Copy as-is** |
| `canonical_courses.json` | 2.0 MB | Same content keyed by course_code (machine-readable) | **Copy as-is** |
| `title_variant_classification.csv` | — | 167 classified title-variant codes | **Copy as-is** |
| `title_variant_summary.json` | — | Counts by class + manual review list | **Copy as-is** |
| `named_events.csv` | — | 41 events (CSV form, for Data page download) | **Copy as-is** |
| `named_events.json` | — | 41 events (JSON form) | **Copy as-is** |
| `curated_major_events.json` | — | 10 curated events with hand-written titles and interpreted summaries (chronological) | **Copy as-is** |

**Target path in `wgu-atlas`:** `data/` (not served publicly) or alongside exports depending on the site architecture.

---

### 3c. Build script — copy and adapt

| File | Location | Action |
|---|---|---|
| `build_site_data.py` | `WGU_catalog/build_site_data.py` | **Copy, then adapt paths** — see §5 for details |

This script regenerates all site_data artifacts from the upstream source files. It does not need to run for v1 but should be in `wgu-atlas` so future catalog updates can be applied.

---

### 3d. Reference-only (do not copy)

These files are the data sources that `build_site_data.py` reads. They live in `wgu-reddit` and should stay there. The `wgu-atlas` build script will reference them via a configurable upstream path — or the outputs from the last run can simply be treated as stable until the next catalog update.

| File | Size | Role |
|---|---|---|
| `outputs/change_tracking/course_history.csv` | 496 KB | Lifecycle table — 1,594 course codes with status, title variants, first/last seen, college history |
| `outputs/change_tracking/program_history.csv` | 40 KB | Lifecycle table — 196 program codes with version progression, college history |
| `outputs/trusted/2026_03/courses_2026_03.csv` | 200 KB | Frozen 2026-03 ground truth — 838 AP codes with current titles, programs, colleges |
| `outputs/trusted/2026_03/certs_2026_03.csv` | 4 KB | Frozen 2026-03 cert inventory — 52 codes |
| `outputs/edition_diffs/edition_diffs_full.json` | 184 KB | Per-transition enriched change schema (107 transitions) |
| `outputs/edition_diffs/edition_diffs_events.json` | 24 KB | 41 major event candidates |
| `outputs/helpers/course_index_v10.json` | **59 MB** | Cross-edition course index — 1,594 codes × all instances across 108 editions |

**Key point on `course_index_v10.json`:** This 59 MB file is the source for `programs_timeline` in each individual course detail file. That data is already baked into `exports/courses/{code}.json`. The v1 site does not need this file at all — it only matters if `build_site_data.py` is re-run.

---

## 4. Required for first site build

The v1 site needs only the items in §3a. Everything else is optional for the build phase.

**Minimum transfer for v1:**

```
wgu-atlas/
└── public/data/                    ← or static/data/ depending on framework
    ├── courses.json                 (1,646 course cards)
    ├── events.json                  (41 events)
    ├── search_index.json            (1,842 search entries)
    ├── homepage_summary.json        (pre-assembled homepage modules)
    └── courses/
        ├── C455.json
        ├── C175.json
        └── ... (838 total)
```

**What each page needs:**

| Page | Primary data file(s) |
|---|---|
| Homepage search | `search_index.json` |
| Homepage modules | `homepage_summary.json` |
| Homepage timeline preview | `homepage_summary.json` → `curated_major_events_preview` |
| Course explorer listing | `courses.json` |
| Course explorer filters | `courses.json` fields: `active`, `scope`, `current_college`, `stability_class`, `ghost_flag` |
| Course detail page | `courses/{code}.json` |
| Timeline page | `events.json` |
| Data page downloads | `canonical_courses.csv`, `named_events.csv`, `title_variant_classification.csv` |
| Methods page | Static content — no data file needed |

---

## 5. Scripts and dependencies

### `build_site_data.py`

**What it does:** Reads 7 source files from the `wgu-reddit` repo structure and writes all `site_data/` artifacts. Standalone Python 3 script; no package imports beyond stdlib.

**Current path dependencies (hard-coded relative to script location):**

```python
BASE  = os.path.join(os.path.dirname(__file__), "outputs")
TRUST = os.path.join(BASE, "trusted", "2026_03")
CT    = os.path.join(BASE, "change_tracking")
ED    = os.path.join(BASE, "edition_diffs")
HELP  = os.path.join(BASE, "helpers")
OUT   = os.path.join(BASE, "site_data")
```

When moved to `wgu-atlas`, this path chain breaks immediately because the script will no longer sit next to an `outputs/` directory. **Required adaptation:**

Replace the path block with configurable source/output paths, for example:

```python
import os
UPSTREAM = os.environ.get("WGU_REDDIT_PATH", "/path/to/wgu-reddit/WGU_catalog/outputs")
SITE_OUT = os.environ.get("WGU_ATLAS_DATA", os.path.join(os.path.dirname(__file__), "data"))
```

Or accept them as CLI arguments. The simplest approach: add a `config.py` at the repo root with the two paths set explicitly.

**Inputs the script reads:**

| Variable | Source path | File |
|---|---|---|
| `course_hist_rows` | `CT/` | `course_history.csv` |
| `prog_hist_rows` | `CT/` | `program_history.csv` |
| `courses_2026` | `TRUST/` | `courses_2026_03.csv` |
| `certs_2026` | `TRUST/` | `certs_2026_03.csv` |
| `diffs_full` | `ED/` | `edition_diffs_full.json` |
| `events_raw` | `ED/` | `edition_diffs_events.json` |
| `course_index` | `HELP/` | `course_index_v10.json` ← 59 MB, slow to load |
| `summary_stats` | `CT/` | `summary_stats.json` (loaded but unused in current build) |

**Runtime:** Approximately 30–60 seconds, dominated by loading `course_index_v10.json`.

**No other scripts need to be migrated.** The upstream data-production scripts (`parse_catalog_v11.py`, `build_change_tracking.py`, `build_edition_diffs.py`, etc.) belong entirely in `wgu-reddit`.

---

## 6. Leave-behind list

These items live in `wgu-reddit` and should NOT appear in `wgu-atlas` under any circumstances.

### Entire directories — leave behind

| Path | Reason |
|---|---|
| `data/raw_catalog_pdfs/` | Source PDFs, many GB. Production data, not for a public site repo. |
| `data/raw_catalog_texts/` | Extracted text files from all 108 PDFs. Large and internal. |
| `outputs/raw_course_rows/` | Per-edition raw extracted course rows. Parser internals. |
| `outputs/program_names/` | Per-edition parser block outputs. Parser internals. |
| `outputs/anomalies/` | Per-edition parser anomaly logs. Parser internals. |
| `outputs/change_tracking/adjacent_diffs.json` | Intermediate change-tracking file. Superseded by edition_diffs_full.json. |
| `src/wgu_reddit_analyzer/` | The entire Reddit Analyzer Python package — scrapers, NLP, database models, etc. |
| `db/` | Database migrations and schema for the Reddit pipeline. |
| `scripts/` | Reddit acquisition scripts, deployment utilities. |
| `notebooks/` | Research and exploration notebooks. |
| `monitoring/` | Application health monitoring. Unrelated to the catalog site. |
| `healthkit/` | Unrelated to the catalog site. |
| `site/` | Old Hugo site build (pre-Atlas, unrelated). |
| `site.BACKUP_*` | Old site backup. |
| `_demo/`, `archive_legacy/` | Legacy/archived material. |
| `llm-sql/` | Unrelated research tooling. |
| `monthly_report/` | Reddit Analyzer reporting pipeline. |
| `WGU_catalog/instructor_directory/` | Separate pipeline for instructor data. Not integrated. |
| `WGU_catalog/geomapping/` | Instructor geomapping. Separate scope. |
| `WGU_catalog/docs/` | Old pre-v11 working notes and drafts. Superseded by README_INTERNAL.md. |

### Individual files — leave behind

| File | Reason |
|---|---|
| `wgu_reddit.db` | SQLite database for the Reddit Analyzer pipeline. |
| `WGU_catalog/parse_catalog_v11.py` | Parser. `wgu-reddit` only. |
| `WGU_catalog/parse_catalog.py`, `parse_catalog copy.py` | Deprecated parsers. |
| `WGU_catalog/run_parser.py` | Parser batch runner. |
| `WGU_catalog/validate_editions.py` | Raw-vs-parsed validation script. |
| `WGU_catalog/build_change_tracking.py` | Generates `course_history.csv` and `program_history.csv`. |
| `WGU_catalog/build_edition_diffs.py` | Generates `edition_diffs_full.json` and related files. |
| `WGU_catalog/Scraper_V10_config.py`, `Scraper_V10_config copy.py` | Deprecated. |
| `WGU_catalog/outputs/helpers/course_index_v10.json` | 59 MB — too large for git; only needed at build time. |
| `WGU_catalog/outputs/helpers/sections_index_v10.json` | Parser internals. |
| `WGU_catalog/outputs/helpers/degree_snapshots_v10_seed.json` | Parser internals. |
| `WGU_catalog/outputs/trusted/2026_03/course_index_2026_03.json` | Full per-instance index for 2026-03. Superseded by the site exports. |
| `WGU_catalog/outputs/trusted/2026_03/sections_index_2026_03.json` | Parser fence boundaries. |
| `WGU_catalog/outputs/trusted/2026_03/degree_snapshots_2026_03.json` | Parser internals. |
| `WGU_catalog/catalog-march-2026.pdf` | Archival PDF. |
| `REDDIT_CLIENT_SETUP_EXAMPLE.py` | Reddit API client setup. Unrelated. |
| `REDDIT_FETCH_DOCUMENTATION.md` | Reddit scraper docs. Unrelated. |
| `URS_TEMPLATE.txt`, `URS_WGU_REDDIT.txt`, `WGU_REDDIT_STATUS.txt` | Reddit Analyzer tooling. |
| `configs/` | Reddit Analyzer configuration. |
| `.env` / any credential files | Never migrate. |

---

## 7. Migration risks and gotchas

### 1. `build_site_data.py` path chain breaks on relocation
**Risk:** All 7 input paths are derived from `os.path.dirname(__file__)`. Move the script one directory level and every `open()` call fails silently or raises `FileNotFoundError`.
**Fix:** Refactor to accept `UPSTREAM_OUTPUTS` and `SITE_DATA_OUT` as env vars or CLI arguments before running the script in `wgu-atlas`.

### 2. `course_index_v10.json` is 59 MB — do not commit to git
**Risk:** If the migration blindly copies `outputs/` into `wgu-atlas`, this file will bloat the repo and likely exceed GitHub's push limits.
**Fix:** Add it to `.gitignore` in `wgu-atlas`. If the build script needs to run, either point it at the `wgu-reddit` copy via an env var, or use git-LFS.

### 3. Curated event text is embedded in the script, not a data file
**Risk:** The `CURATED_EVENTS` dict in `build_site_data.py` (lines ~673–778) contains all 10 hand-written event titles, observed summaries, and interpreted summaries. If a site editor wants to update event copy without re-running the build, there is no separate editorial file to edit — they have to edit the script.
**Fix (recommended before v1):** Extract `CURATED_EVENTS` into `data/curated_events_editorial.json` in `wgu-atlas`. `build_site_data.py` reads from it; site editors update the JSON directly. This decouples editorial content from code.

### 4. Individual course files cover only active AP codes
**Risk:** `exports/courses/` contains 838 files — one per active AP code. Retired codes (756) and cert codes (52) have entries in `courses.json` (the card listing) but no detail file. If the frontend routing attempts to load `courses/{code}.json` for a retired or cert code, it will 404.
**Fix:** Decide before building routing: either generate detail files for all 1,646 codes (requires a `build_site_data.py` run with that scope), or ensure the frontend guards against routing to detail pages for non-active-AP codes.

### 5. The `outputs/trusted/2026_03/` directory is frozen / read-only
**Risk:** If someone copies the full `trusted/` directory to `wgu-atlas` and then treats it as mutable, they may overwrite the canonical reference edition.
**Fix:** Either do not copy `trusted/` to `wgu-atlas` at all (recommended), or mark it clearly as read-only in the repo README. The site does not need the trusted files directly — it uses the pre-built exports.

### 6. `D396` canonical title override is embedded in `build_site_data.py`
**Risk:** The 2026-03 extraction of D396 is truncated to `"Evidence-Based Practice for Health and"`. The script overrides this with the full correct title. This override logic lives in `CANONICAL_TITLE_OVERRIDES` in the script, not in any external data file. If the override is lost during migration, D396's title in the site will be the truncated form.
**Fix:** When migrating the script, verify the `CANONICAL_TITLE_OVERRIDES` dict is present and intact. If editorial content is extracted to JSON (see gotcha #3), include this override in that same file.

### 7. `homepage_summary.json` is pre-computed — not live
**Risk:** The homepage module data (recent version changes, newest programs, etc.) is computed at build time from the March 2026 catalog state. It will not auto-update when new catalog editions are processed. If a site visitor sees "newest programs" that are months old, that may be surprising.
**Fix:** Document clearly in the repo that `homepage_summary.json` must be regenerated each time new catalog data is processed in `wgu-reddit`. This is expected behavior — the site is a static build.

### 8. `programs_timeline` in course detail files uses degree heading strings, not program codes
**Risk:** The `programs_timeline` field in each `courses/{code}.json` file lists programs by their raw degree heading text (e.g., `"Bachelor of Science, Business Management"`) — not by program code. This is what the catalog parser extracts. These strings may have minor wording variations across editions (e.g., "in" vs "," connectors).
**Implication:** If the site later tries to link from a course's program timeline to a program detail page, it will need a fuzzy matching step or an alias table to map heading strings to program codes (`program_history.csv`).

### 9. `wgu-atlas` should not import or depend on the `wgu_reddit_analyzer` Python package
**Risk:** If the wrong copy-paste brings in any `from wgu_reddit_analyzer import ...` references, the site will acquire a dependency on the full Reddit pipeline.
**Fix:** `wgu-atlas` should have no Python package dependencies beyond stdlib for the build script. If a packaging system is set up for the site (Node/Astro/Next.js/etc.), it should have zero Python packages other than `build_site_data.py`'s implicit dependencies (none — stdlib only).

### 10. No authentication or API keys should migrate
**Risk:** `wgu-reddit` contains Reddit API credentials (`.env`, `configs/`). These must never appear in `wgu-atlas`.
**Fix:** Verify `.gitignore` in `wgu-atlas` blocks `.env` and any `*_secret*` / `*_key*` files before the first push.

---

## 8. Quick-start for the first `wgu-atlas` agent

```
1. Create wgu-atlas repo (public)

2. Copy these files:
   FROM wgu-reddit/WGU_catalog/outputs/site_data/exports/
     → wgu-atlas/public/data/courses.json
     → wgu-atlas/public/data/courses/   (all 838 JSON files)
     → wgu-atlas/public/data/events.json
     → wgu-atlas/public/data/search_index.json
     → wgu-atlas/public/data/homepage_summary.json

   FROM wgu-reddit/WGU_catalog/outputs/site_data/
     → wgu-atlas/data/canonical_courses.csv
     → wgu-atlas/data/canonical_courses.json
     → wgu-atlas/data/title_variant_classification.csv
     → wgu-atlas/data/title_variant_summary.json
     → wgu-atlas/data/named_events.csv
     → wgu-atlas/data/named_events.json
     → wgu-atlas/data/curated_major_events.json

   FROM wgu-reddit/WGU_catalog/
     → wgu-atlas/scripts/build_site_data.py    (adapt paths)
     → wgu-atlas/docs/README_INTERNAL.md
     → wgu-atlas/docs/SCRAPE_LOG.md
     → wgu-atlas/docs/website_design_plan.md

3. Add .gitignore:
   course_index_v10.json
   *.env
   .env*

4. Begin site shell build using public/data/ as the data source.
   No Python scripts need to run for the v1 build.
```
