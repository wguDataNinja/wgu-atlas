# WGU Atlas

## Purpose
Public-facing reference explorer for WGU courses, programs, and catalog history. Built from 108 scraped catalog editions (2017–2026). Next.js static site deployed via GitHub Pages + GitHub Actions. Also contains an Atlas QA subsystem (Python) for intelligent course/program Q&A over the archived data.

## Status
- Active branch: `homepage-redesign` (UI polish in progress)
- Stable deployed baseline: `main`
- Atlas QA subsystem in active development (retrieval, compare mode, eval harness)

## Directories
| Path | Purpose |
|---|---|
| `src/` | Next.js site source (App Router, components, pages) |
| `src/app/proto/` | Prototype pages (compare-3, degree-preview, course-preview) |
| `src/atlas_qa/` | Python QA subsystem (retrieval, generation, routing, eval) |
| `src/components/` | React components (courses, programs, compare, layout, proto) |
| `src/lib/` | Shared data utilities & types |
| `data/` | Canonical datasets (CSV/JSON), catalog lineage, enrichment, QA cards |
| `public/data/` | Frontend-consumed JSON (courses, events, search index) |
| `scripts/` | Python data build & validation scripts |
| `tests/` | Pytest test suite (atlas_qa subsystem) |
| `_internal/` | Working docs: control docs, repo memory, dev log, designs |

## Commands
```bash
npm run dev     # Next.js dev server (port 3000, basePath: /wgu-atlas)
npm run build   # Static export to out/
npm run lint    # ESLint
npm run start   # Production preview (requires build first)
npm test        # pytest (Python QA subsystem)
```

## Watchouts
- **basePath**: All routes are prefixed `/wgu-atlas` — local URLs must include it
- **Stale internal docs**: If internal docs conflict, trust `_internal/ATLAS_CONTROL.md` (execution control), then `_internal/ATLAS_REPO_MEMORY.md` (architecture/runtime)
- **Data boundary**: Official catalog data, community discussion signals, and LLM-generated content are never mixed in the same field — always check attribution
- **Python deps**: QA subsystem needs its own `.venv` (see `requirements.txt`). Scripts use `src.` imports but are run from the repo root
- **Data provenance**: 3 catalog editions missing (2017-02, 2017-04, 2017-06). Certificate codes only tracked from 2024-09 forward
- **No secrets**: `.env*` and `.venv/` are gitignored — never commit credentials
- **Large artifacts**: `node_modules/` is excluded; `.next/`, `out/`, `__pycache__/` are build output
