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
