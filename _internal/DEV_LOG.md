# WGU Atlas — Dev Log

Internal working log. Record durable decisions, migration status, blockers, and next steps.
Do not turn this into a transcript. One entry per meaningful phase boundary.

---

## 2026-03-14 — Session 1: Repo hygiene + data migration

### What was done

**Phase 1 — Repo hygiene**

Created foundational repo files:
- `README.md` — public-facing project description, data provenance, structure overview
- `.gitignore` — covers Node, Next.js, Python venv, large build-time files, credentials
- `.editorconfig` — utf-8, LF, 2-space indent (4 for Python), final newline
- `LICENSE` — MIT, copyright WGU-DataNinja

**Phase 2 — Data migration**

Migrated all artifacts specified in `_internal/MIGRATION_HANDOFF.md`.

Source root: `/Users/buddy/Desktop/WGU-Reddit/WGU_catalog/`

Site-ready exports → `public/data/`:
- `courses.json` (712 KB, 1,646 course cards)
- `events.json` (48 KB, 41 events)
- `search_index.json` (392 KB, 1,842 entries)
- `homepage_summary.json` (12 KB)
- `courses/` (838 individual course detail JSON files, 3.4 MB total)

Canonical artifacts → `data/`:
- `canonical_courses.csv`
- `canonical_courses.json` (2.0 MB)
- `title_variant_classification.csv`
- `title_variant_summary.json`
- `named_events.csv`
- `named_events.json`
- `curated_major_events.json`

Build script → `scripts/`:
- `build_site_data.py` — copied from source; paths adapted (env var / CLI arg pattern)

Reference docs → `docs/`:
- `README_INTERNAL.md` — scraper architecture, parser eras, field definitions, validation
- `SCRAPE_LOG.md` — archive coverage, build milestones, deferred items
- `website_design_plan.md` — locked site design, page structure, build phases

### What was intentionally left behind

Everything on the leave-behind list in `MIGRATION_HANDOFF.md §6`. Key items:
- Raw PDF/text archives (many GB)
- All parser scripts (`parse_catalog_v11.py`, `build_change_tracking.py`, etc.)
- `course_index_v10.json` (59 MB — also added to `.gitignore`)
- Full Reddit Analyzer package (`src/wgu_reddit_analyzer/`)
- All Reddit pipeline internals (db, scripts, monitoring, configs)
- Old Hugo site (`site/`, `site.BACKUP_*`)
- Legacy/archive clutter

### Known issues / gotchas carried forward

1. **`build_site_data.py` paths** — Original script uses hard-coded relative paths from its location inside `wgu-reddit`. The migrated version has been adapted to use `WGU_REDDIT_PATH` and `WGU_ATLAS_DATA` env vars. Document this before next catalog update.

2. **Retired/cert course routing** — `exports/courses/` has 838 files (active AP only). Retired (756) and cert (52) codes have entries in `courses.json` but no detail file. Frontend routing must guard against 404s for non-active-AP codes.

3. **`homepage_summary.json` is static** — Pre-computed from 2026-03 catalog state. Must be regenerated each time new catalog data is processed in `wgu-reddit`. Not a bug — expected behavior for a static build.

4. **Curated event text is in `build_site_data.py`** — The `CURATED_EVENTS` dict (~lines 673–778 in original) contains all hand-written event copy. Future improvement: extract to `data/curated_events_editorial.json` to decouple editorial content from code.

5. **D396 title override** — The script contains a `CANONICAL_TITLE_OVERRIDES` dict that corrects a truncated title for D396. Verified present and intact in the migrated script (line 455).

6. **`programs_timeline` uses heading strings, not codes** — Course detail files list programs by raw degree heading text, not by program code. Future linking to program pages will require fuzzy matching or an alias table.

### Next steps (carried to Session 2)

- [x] Review migrated repo structure (Phase 3 pause — approved)
- [x] Phase 4: scaffold Next.js + TypeScript + Tailwind site shell (Session 2)
- [ ] Phase 5: GitHub Actions workflow + GitHub Pages deploy

---

## 2026-03-14 — Session 2: Next.js site scaffold (Phase 4)

### What was done

Scaffolded the site manually (create-next-app refused non-empty directory).

**Stack:**
- Next.js 15 + TypeScript + Tailwind CSS
- App Router with `src/app/` structure
- `output: 'export'` configured for GitHub Pages static export
- `images: { unoptimized: true }` for static export compatibility
- `basePath: "/wgu-atlas"` present but commented out — enable when deploying to GitHub Pages

**Pages created:**

| Route | Page | Data source |
|---|---|---|
| `/` | Homepage | `homepage_summary.json` |
| `/courses` | Course Explorer | `courses.json` (1,646 cards), `search_index.json` |
| `/courses/[code]` | Course Detail | `courses/{code}.json` (838 pre-generated pages) |
| `/timeline` | Timeline | `events.json` (41 events) |
| `/methods` | Methods | Static content |
| `/data` | Data page | `homepage_summary.json` (for metadata); CSV/JSON download links |

**Key components:**
- `HomeSearch.tsx` — client-side search with live dropdown, loads `search_index.json` on mount
- `SchoolCards.tsx` — 4 school drilldown cards with active course counts from `homepage_summary.json`
- `EventPreview.tsx` — curated event preview cards on homepage
- `CourseExplorer.tsx` — client-side filter/search over 1,646 courses; paginated 50/load
- `Nav.tsx` — sticky nav with active link highlight
- `Footer.tsx` — provenance + data date + disclaimer

**Architecture decisions:**
- Homepage, course explorer listing page, timeline, methods, data — server components; data loaded from `fs` at build time
- Course explorer filter/search — client component (1,646 records; too large for URL-based server rendering)
- Course detail pages — `generateStaticParams` from 838 active AP codes; all pre-generated at build time
- Retired/cert codes — handled gracefully: Course Explorer lists them (no link) or shows broken link; detail route returns `notFound()` which renders the custom `not-found.tsx` page

**Build result:**
- 846 static pages generated cleanly
- `next build` → `output: 'export'` — output in `.next/` (needs `out/` for GitHub Pages, but not wired yet)

### Data quirk discovered and fixed

`colleges_seen` field in course detail JSON is sometimes a string, sometimes an array. Fixed with `Array.isArray()` guard in `[code]/page.tsx`. Type updated in `lib/types.ts`.

### What was intentionally deferred

- GitHub Pages deployment workflow (Phase 5 — next session)
- Program pages (Phase 4 later)
- Reddit discussion layer (Phase 5/v1.1)
- Course lifecycle timeline visual
- School/college lineage visual
- Transition explorer
- `basePath` activation — leave commented until GitHub Pages repo is confirmed

### Next steps (carried to Session 3)

- [x] Phase 5: Deployment configuration + GitHub Actions workflow

---

## 2026-03-14 — Session 6: Entity-navigation and program-page pass

### Canonical entity-page rule adopted

Every course and every program shown on the site now resolves to a real Atlas entity page.

- **Current entities**: show latest catalog-backed state; labeled `Current`
- **Deprecated entities**: show final known catalog-backed state; labeled `Deprecated · Last seen: YYYY-MM · Final source: WGU Catalog (YYYY-MM)`
- No redirect for deprecated entities; no broken links

### Navigation/link audit completed

All major dead-end navigation fixed:
- Homepage `Newest Programs` module: items now link to `/programs/[code]` (was unlinked)
- Homepage `Programs with Recent Updates` module: items now link to `/programs/[code]` (was unlinked)
- Homepage `Recent Course Additions` module: already linked to `/courses/[code]` — confirmed intact
- Homepage module "See all →" links for program modules updated to `/programs`
- Search results: program results now link to `/programs/[code]` (was a dead fake-search link)
- Search: deprecated programs now labeled "deprecated" (was "retired")
- Course detail `programs_timeline`: entries now linked to `/programs/[code]` via heading→code map
- Course detail `current_programs`: entries now linked to `/programs/[code]`
- Course detail `historical_programs`: entries linked to `/programs/[code]` where matched
- Nav: added `Programs` link between Courses and Timeline

### Course page coverage expanded

Previously: 838 active AP course pages only.
Now: **1,641 course entity pages** (all known course codes).

- Active AP (838): served from individual `courses/{code}.json` — rich, includes `programs_timeline`
- Retired AP (751) + active cert (52): served from `canonical_courses.json` fallback — full fields except `programs_timeline`; shows `historical_programs` list instead
- All deprecated course pages show: `Deprecated` badge, `Last seen: YYYY-MM`, final source attribution
- Field normalization: `observed_titles` (` | ` separated) and `current_programs` (`; ` separated) normalized to arrays at load time for canonical fallback

### Program pages added

New routes:
- `/programs` — Programs explorer (client-side filter by status, school, text search)
- `/programs/[code]` — Program detail page (196 pages: 114 active, 82 deprecated)

Each program detail page shows:
- Status badge (Current / Deprecated)
- Canonical name, school, first/last seen
- Edition count, version change count
- School lineage with → progression
- Known name variants (if multiple degree_headings)
- Version history table (date → version stamp)
- Total CUs with change flag if CU values varied

Data source: `data/program_history.csv` (copied from wgu-reddit) → `public/data/programs.json` (generated at migration time).

### Data added

- `data/program_history.csv` — copied from wgu-reddit change_tracking outputs
- `public/data/programs.json` — generated from CSV (196 programs, 114 active / 82 retired)

### Heading→code map

Built `getHeadingToProgramCode()` in `data.ts`. Resolves `programs_timeline` heading strings to program codes. ACTIVE programs win over RETIRED on conflict; latest `last_seen` wins among same status. Best-effort: some renamed programs may not match.

### Build result

2,043 static pages generated cleanly (was 846).

### Known limitations / deferred

- `programs_timeline` heading→code map is best-effort; some historical headings won't match any current program code
- Program pages have no course roster yet (program_history.csv does not include per-program course list)
- Cert-only courses lack `programs_timeline`; show `historical_programs` list without per-program first-seen dates
- Program descriptions and learning outcomes still not extracted (requires parser work — deferred per session scope)

### Next steps

- [ ] Extract program descriptions (parser work, well-bounded, moderate effort)
- [ ] Build school/college pages
- [ ] Push to GitHub and verify live deployment

---

## 2026-03-14 — Session 7: Big data-surfacing pass

### What was done

#### New extraction script

Added `scripts/extract_program_enriched.py` — a standalone script that reads the 2026-03 catalog text and program_blocks file from `wgu-reddit` and extracts:
- **Program descriptions**: paragraph text between the degree heading and the CCN table (lines `deg_idx+1` to `ccn_idx`)
- **Course rosters**: per-program ordered course list with `{term, code, title, cus}`, handles title wrap-across-lines
- **Program learning outcomes**: from the "Program Outcomes" section (ERA_B / 2024-08+), matched to program codes by fuzzy name overlap

Results written to `public/data/program_enriched.json` (keyed by program_code, 114 active programs).

**Extraction results:**
- Descriptions: 114/114 (all active programs)
- Rosters: 113/114 (one program has no CCN table)
- Outcomes: 74/114 (ERA_B only; 40 programs unmatched due to label variations)
- Total roster course rows: 2,519

**Run command:**
```bash
python3 scripts/extract_program_enriched.py \
  --catalog  /path/to/wgu-reddit/WGU_catalog/data/raw_catalog_texts/catalog_2026_03.txt \
  --blocks   /path/to/wgu-reddit/WGU_catalog/outputs/program_names/2026_03_program_blocks_v11.json \
  --programs /path/to/wgu-atlas/public/data/programs.json \
  --out      /path/to/wgu-atlas/public/data/program_enriched.json
```

#### New pages / routes

| Route | Description |
|---|---|
| `/schools` | School index — 4 school cards with program/course counts |
| `/schools/[slug]` | School detail pages (4 static pages: business, health, technology, education) |

Each school page includes:
- School name + current/active badge + source label
- **School history table** — compact lineage from README_INTERNAL.md §12 (effective date + name, current highlighted)
- **Recent Activity module** (3-column grid): Newest Programs, Recent Version Updates, Recent Course Additions — all filtered to that school, all linked
- **Active Programs** table grouped by degree level (Doctoral / Master's / Bachelor's / Certificates & Endorsements), with program code, name, CUs, first seen
- **Active Courses** table (collapsible) — all active courses in that school, linked to course pages
- **Deprecated Programs** table (collapsible) — retired programs that were in that school, linked

#### Program pages enriched

`/programs/[code]` now shows:
- **About This Program** — official catalog description text, blockquote with provenance label
- **Program Learning Outcomes** — bullet list of WGU-authored outcomes where available (ERA_B)
- **Course Roster** — grouped by term, with code (linked), title, CUs; total CU sum shown

School name on program page now links to `/schools/[slug]`.

#### Navigation updated

- Nav: added `Schools` link between Programs and Timeline
- Homepage school cards: now link to `/schools/[slug]` instead of `/courses?school=...`

#### Data added

- `public/data/program_enriched.json` — 114 active programs with description, roster, outcomes (740 KB)

#### Types added

- `RosterCourse` — `{term, code, title, cus}`
- `ProgramEnriched` — `{program_code, description, description_source, roster, roster_source, outcomes, outcomes_source}`
- `SchoolRecord` — `{slug, current_name, canonical_key, lineage, historical_names}`
- `SchoolLineageEntry` — `{date, name}`

#### Data functions added to `data.ts`

- `getProgramEnriched()`, `getProgramEnrichedByCode(code)`
- `getSchools()`, `getSchoolBySlug(slug)`
- `getProgramsBySchool(canonicalKey)`, `getCoursesBySchool(historicalNames)`
- School lineage constants derived from README_INTERNAL.md §12

#### Build result

1,851 static pages generated cleanly (up from 1,641 + 196 + other prior counts; new pages: 4 school routes + 1 school index).

### Provenance approach used

- Section-level source labels on all new sections: `Source: WGU Catalog 2026-03` or `Source: WGU public catalog archive`
- Program descriptions shown as `<blockquote>` with explicit "Official catalog text — WGU-authored" footnote
- Learning outcomes section labeled "Official WGU-authored outcomes from the catalog Program Outcomes section. Present in ERA_B catalogs (2024-08+)."
- School history table attributed to "WGU public catalog archive"
- Recent activity modules labeled "Based on 2026-03 catalog"

### Known limitations / deferred

- **40 programs without outcomes** — outcome label matching uses fuzzy word overlap; some programs (especially those with generic or abbreviated labels in the outcomes section) aren't matched. No outcomes are fabricated; blank = genuinely not matched.
- **Outcomes limited to ERA_B (2024-08+)** — the Program Outcomes section is not present in ERA_A catalogs (pre-2024-08). Historical outcomes are not available.
- **Course CUs not on CourseCard** — the active courses table on school pages shows "—" for CUs because `courses.json` course cards don't carry CU values (only individual detail files do). This is a minor gap; the roster on program pages shows CUs correctly.
- **School activity modules are catalog-snapshot** — recent_version_changes, newest_programs, and recent_course_additions all come from `homepage_summary.json` which is a pre-computed static artifact. Some entries use historical school names; normalized via `schoolNormMap` on the school page.
- **1 program with no roster** — one active program block had no parseable CCN table (likely a structural edge case). Shown as no roster section.
- **`program_enriched.json` is 2026-03 only** — descriptions and rosters are current snapshot only; historical roster changes are not tracked.

### Next steps

- [ ] Improve outcomes matching for remaining 40 programs (lower threshold or alternative label patterns)
- [ ] Add CU values to course cards so school course tables can show CUs
- [ ] Add `stability_class` badge to course cards (course explorer and school course list)
- [ ] Add school tenet text (once parsed from catalog)
- [ ] Consider extracting program descriptions from earlier catalogs for deprecated programs
- [ ] Push to GitHub and deploy

---

## 2026-03-14 — Session 8: Student-facing re-centering and cleanup pass

### What was done

A focused cleanup pass to re-center Atlas around student usefulness rather than archival novelty.

#### Homepage (`src/app/page.tsx`)

- Subtitle simplified: "Search courses, programs, and WGU catalog history"
- Orientation stats band: removed "Retired codes" and "Named events"; kept Active courses + Active programs + data date + methods link
- Removed "Programs with Recent Updates" module (archive-facing, low student value)
- Added "Browse by School" module: 4 school tiles with program count, each linking to `/schools/[slug]`
- Renamed "Around the WGU Web" → "Official WGU Resources"
- Timeline preview heading reduced in visual weight; moved to bottom of page
- Added `cleanHeading()` and `shortSchool()` helpers to reduce clutter in module listings

#### Course detail (`src/app/courses/[code]/page.tsx`)

- Removed "Discussion Signals — Coming in v1.1" placeholder section
- Removed `ghost_flag` badge from header
- Status badge wording: "Deprecated" → "Retired", "Current" → "Active"
- Renamed primary section "Official Catalog History" → "Course Details" (blue left bar)
- Reordered primary stats: `{credit units, current programs, total programs, offered in}` + programs list + school chips + other names
- Archive stats (first/last seen, editions, catalog presence) moved to secondary "Catalog History" section (slate left bar, lower visual weight)
- Simplified label maps: stability, variant, and context labels now use plain language ("Present in all editions", "Formatting variation only", "Degree programs", etc.)
- Removed repeated source badge from primary section; source badge kept only on secondary "Catalog History" section

#### Course explorer (`src/app/courses/page.tsx`, `src/components/courses/CourseExplorer.tsx`)

- Page title: "Courses" (was "Course Explorer")
- Removed `ghost_flag` visual badge from course rows in `CourseExplorer`

#### School pages (`src/app/schools/[slug]/page.tsx`)

- Removed broken CUs column from active courses table (CourseCard doesn't carry CU values — removed rather than show "—")
- Fixed "Deprecated Programs" → "Retired Programs" section heading
- Consolidated repeated source badge clutter: moved provenance to page header level

#### Navigation (`src/components/layout/Nav.tsx`)

- Split nav into `primaryLinks` (Home / Courses / Programs / Schools) and `secondaryLinks` (Timeline / Methods / Data)
- Visual divider separates the two groups
- Secondary links styled lighter (`text-slate-400` base, `text-slate-600` hover) vs. primary (`text-slate-600` base, `text-slate-900` hover)
- Secondary active state: `bg-slate-100 text-slate-700` (not the blue highlight used for primary)

### Build result

1,851 static pages — identical count to Session 7, no regressions.

### Next steps

- [ ] Improve outcomes matching for remaining 40 programs
- [ ] Add CU values to `CourseCard` so school course tables can show CUs
- [ ] Add `stability_class` badge to course cards
- [ ] Add school tenet text (once parsed from catalog)

---

## 2026-03-14 — Session 5: Product direction review

### What was done

Produced `_internal/PRODUCT_REVIEW_2026_03.md` — a structured product direction memo responding to a shift in emphasis: the site should lead with **useful catalog-backed course/program information**, not with the change-history/event layer.

Memo covers six questions: (1) what's extracted but not yet surfaced, (2) what's in the catalog but not yet extracted, (3) effort classification table, (4) page-by-page recommendations, (5) provenance/citation pattern, (6) monthly update workflow.

### Main direction

**Lead with catalog facts, not events.** Events remain but are secondary.

### Priority order going forward

1. Add CUs to course card and course detail page (no new data, high value)
2. Build program pages from existing `program_history.csv`
3. Build school/college pages (needs only existing data + school tenets text)
4. Extract program descriptions (new parsing, well-bounded, moderate effort)
5. Extract program learning outcomes (ERA_B only, new parsing)
6. Surface `stability_class` as visible badge on course cards
7. Extract certificate descriptions (minor parser extension)

### Key finding

`canonical_cus` is present in all 838 active course detail JSON files and `canonical_courses.csv`. CUs are **not shown anywhere in the current UI**. This is the highest-value zero-effort improvement.

### Next steps

- [ ] Add CUs to course card and detail page (Session 6)
- [ ] Build program pages (Session 7+)

---

## 2026-03-14 — Session 3: GitHub Pages deployment (Phase 5)

### What was done

**`next.config.ts` changes:**
- `basePath: "/wgu-atlas"` activated (was commented out)
- `output: "export"` and `images: { unoptimized: true }` unchanged

**basePath-sensitive paths fixed:**

Three categories of broken paths found and corrected:

1. `HomeSearch.tsx` — `fetch("/data/search_index.json")` → `fetch(\`${BASE_PATH}/data/search_index.json\``)`
2. `data/page.tsx` — all `<a href>` download links prefixed with `BASE_PATH`
3. `Footer.tsx` — `<a href="/methods">` and `<a href="/data">` converted to Next.js `<Link>` (auto-handles basePath)

**New `src/lib/basePath.ts`:**
- Exports `BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? ""`
- Used by client components and server-rendered download links
- Set to `/wgu-atlas` in the GitHub Actions workflow via env var; empty string for local dev

**Bug found and fixed — download files not publicly served:**
- `data/` directory is not served by Next.js static export (only `public/` is served)
- Downloadable CSVs and canonical JSONs copied from `data/` → `public/data/downloads/`
- Data page paths updated from `/data/canonical_courses.csv` → `/data/downloads/canonical_courses.csv`
- Both `data/` (internal reference) and `public/data/downloads/` (served) now exist

**`.nojekyll` added to `public/`:**
- Copied automatically to `out/` during `next build`
- Prevents GitHub Pages Jekyll processing from hiding `_next/` directories
- Verified present in `out/.nojekyll` after build

**`.github/workflows/deploy.yml` created:**
- Triggers on push to `main` and `workflow_dispatch`
- Permissions: `pages: write`, `id-token: write` (required for deploy-pages)
- Sets `NEXT_PUBLIC_BASE_PATH=/wgu-atlas` during build
- Uploads `./out` via `actions/upload-pages-artifact@v3`
- Deploys via `actions/deploy-pages@v4`
- One concurrent deployment enforced (cancel-in-progress: false)

**Build verified:**
- `NEXT_PUBLIC_BASE_PATH=/wgu-atlas npm run build` exits clean
- 846 static pages generated
- `out/index.html` asset references use `/wgu-atlas/_next/...` ✓
- `out/.nojekyll` present ✓
- `out/data/downloads/` contains downloadable CSVs ✓

### What is still required on GitHub side (manual steps)

1. Push this repo to `https://github.com/wguDataNinja/wgu-atlas`
2. In repo Settings → Pages:
   - Source: **GitHub Actions** (not "Deploy from a branch")
3. The first push to `main` will trigger the workflow and deploy the site

Expected live URL: `https://wgudataninja.github.io/wgu-atlas/`

### Next steps

- [ ] Push repo to GitHub and verify first deployment
- [ ] Confirm live URL works at `https://wgudataninja.github.io/wgu-atlas/`
- [ ] Phase 6: public hardening pass (code cleanup, provenance clarity, trust docs)
- [ ] Phase 7 (later): program pages, visual improvements, Reddit integration

---
