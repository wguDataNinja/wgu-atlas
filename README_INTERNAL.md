# README_INTERNAL — wgu-atlas

> Created: 2026-05-21 | Tenant: hermes-lab | Branch: homepage-redesign

## agent_context
```yaml
project: wgu-atlas
repo: https://github.com/wguDataNinja/wgu-atlas
purpose: Public-facing reference explorer for WGU courses, programs, catalog history (108 editions, 2017–2026)
tech: Next.js 15 (App Router) + TypeScript + Tailwind + static export → GitHub Pages
qa_subsystem: Python (atlas_qa) — retrieval, compare, eval, intent gating
deploy: GitHub Actions CI (static export to out/)
python_venv: src/atlas_qa/ requires .venv + pip install -r requirements.txt
```

## IVY Summary
- **Next.js site**: 55 TS/TSX files across App Router pages (courses, programs, schools, compare, timeline, data, methods, about, proto)
- **Atlas QA subsystem**: Python Q&A over catalog data — retrieval (BM25 + embedding + fusion), compare mode, answer generation, evidence extraction, post-check, eval harness (100-question gold set)
- **Data layer**: canonical CSVs/JSONs in `data/`, frontend JSON in `public/data/` — 838 active AP courses, 52 cert codes, 1,646 total course codes, 114 program blocks, 41 catalog events
- **3-doc internal system**: `_internal/ATLAS_CONTROL.md` (execution control), `_internal/ATLAS_REPO_MEMORY.md` (durable facts), `_internal/DEV_LOG.md` (dated ledger)

## Current Work
| Track | Status | Detail |
|---|---|---|
| QA eval + F-089 retry regression | Active | 87/100 gold eval (run 4). F-089: generation retry fires on correct model abstention for out-of-scope queries |
| Homepage redesign | Primary product track | Define research-first homepage for student curriculum inspection, degree comparison, catalog history |
| Course-page enrichment | Partial — landed | Incremental rollout of certification/prereq/capstone blocks |
| Official resource attachment | Active queue | Conservative expansion with provenance clarity |
| Cross-degree description reconciliation | Initiated — BSDA pass done | Compare degree-homepage text vs catalog for policy adoption |

## Open Loops
1. **F-089 regression**: Remove or restrict Fix 3 retry (fires on correct abstention); re-run eval
2. **Homepage redesign**: Convert strategy into section-level messaging and implementation plan
3. **Course cert/prereq blocks**: Implement variant handling; no core design reopens
4. **3 missing catalog editions**: 2017-02, 2017-04, 2017-06
5. **Certificate codes**: Only tracked from 2024-09 forward
6. **Continuity review**: 4-card validation batch not yet created
7. **Program lineage export/routing**: Not implemented (not active)

## Durable Decisions
- **basePath**: `/wgu-atlas` in next.config.ts — all routes prefixed
- **Data attribution**: Official catalog, community discussion signals, and LLM-generated content never mixed in same field
- **Ollama-dependent**: QA subsystem requires Ollama running locally for generation
- **`src.` → `atlas_qa.` imports**: Python scripts use `atlas_qa.` prefix (not `src.`) for script-path compatibility (commit e97af19)
- **3-doc authority**: CONTROL.md > REPO_MEMORY.md > DEV_LOG.md for execution; project_overview/ for product scope
- **Static export only**: `output: "export"` in next.config — no SSR, no API routes
- **No secrets tracked**: `.env*`, `.venv/` gitignored; no env-like files tracked or untracked

## Git Status
- **Branch**: `homepage-redesign` (ahead of origin by 2 commits)
- **Other branches**: `main` (stable/deployed), `docs-cleanup-local`
- **Remote**: `origin` (github.com/wguDataNinja/wgu-atlas)
- **Recent changes**: 45+ modified files (pages, components, QA subsystem, internal docs), 20+ new untracked files (proto compare-3 page, qa modules, BSDA scripts, archive artifacts)

## Recent Work (last 10 commits)
```
64ff87b AGENTS.md: fix test command — npm test -> pytest (276 tests)
0c854f5 Add AGENTS.md — project orientation for AI agents
bee389f UI polish: compare, course, and degree pages
98663a9 Session 12b: remove generation retry (F-089 regression); update control/repo docs
db5e806 Post-session 12: update control docs with gold eval run 4 results
e2762ba Add requirements.txt (pydantic, rank-bm25, sentence-transformers)
e97af19 Fix src. prefix imports → atlas_qa. for script-path compat
dd5e507 Session 12: citation reliability hardening (prompt fix, postcheck fallback, retry)
e7c680c Post-session 11: update control docs with gold eval run 3
39d3332 Session 11: fix source_object_identity derivation + guide-presence gate
```

## Directory Overview
```
wgu-atlas/
├── src/                    # Next.js App Router (pages, components, lib)
│   ├── app/                # Route pages (courses, programs, compare, schools, etc.)
│   ├── app/proto/          # Prototype pages (compare-3, degree-preview, course-preview)
│   ├── components/         # React components (layout, courses, programs, compare, home, proto)
│   ├── lib/                # Shared utilities + types
│   └── atlas_qa/           # Python QA subsystem (qa/, llm/, utils/)
│       └── qa/             # Retrieval, generation, compare, eval, routing, gating, evidence
├── data/                   # Canonical datasets (CSV/JSON), catalog lineage, QA cards
├── public/data/            # Frontend-consumed JSON (courses, events, search index)
├── scripts/                # Python data build & validation scripts (25+ files)
├── tests/                  # Pytest suite (atlas_qa subsystem)
├── _internal/              # Working docs (control, repo memory, dev log, designs, archive)
└── docs/                   # Reference documentation (data layer provenance)
```

## Important Files
| File | Purpose |
|---|---|
| `next.config.ts` | Static export, basePath `/wgu-atlas` |
| `src/atlas_qa/qa/lookup.py` | Entity + course lookup (primary entry point) |
| `src/atlas_qa/qa/compare.py` | Compare mode (21KB) |
| `src/atlas_qa/qa/runtime_runner.py` | Orchestration runner (27KB) |
| `src/atlas_qa/qa/generation.py` | Answer generation + retry logic |
| `src/atlas_qa/qa/eval_runner.py` | Gold eval harness (100 questions) |
| `src/atlas_qa/qa/intent_gate.py` | Query intent classification |
| `src/atlas_qa/qa/router.py` | Query-to-module routing |
| `_internal/ATLAS_CONTROL.md` | Active execution control (25KB) |
| `_internal/ATLAS_REPO_MEMORY.md` | Architecture/runtime facts (62KB) |
| `_internal/project_overview/01_SITE_DESIGN_SPEC.md` | Product scope grounding |

## Commands
```bash
npm run dev        # Next.js dev server (port 3000, basePath /wgu-atlas)
npm run build      # Static export to out/
npm run lint       # ESLint
npm run start      # Production preview (requires build first)
pytest             # QA subsystem tests (276 tests)
```

## Watchouts
- **basePath**: All local routes must include `/wgu-atlas` prefix
- **Ollama**: QA subsystem generation requires Ollama running locally
- **Stale internal docs**: If conflict, trust CONTROL.md → REPO_MEMORY.md → DEV_LOG.md
- **Python deps**: Use `.venv` + `requirements.txt`; scripts run from repo root
- **Data boundary**: Catalog data, discussion signals, LLM content never mixed in same field
- **Missing catalog editions**: 3 gaps (2017-02, 2017-04, 2017-06); cert codes only from 2024-09
- **F-089 regression**: Retry logic may fire on correct abstention — pending fix
- **Large artifacts**: `node_modules/`, `.next/`, `out/` excluded from git

## Resume Notes
- F-089 is the active QA subsystem blocker — retry loop fires on out-of-scope queries where the model correctly abstains. Fix: remove or restrict retry on generation.py's abstention path then re-run eval.
- Homepage redesign is primary product track — needs strategy-to-section conversion.
- Course-page enrichment at incremental rollout phase — no core design reopens.
- Tests all pass (276). Run `pytest` before committing QA changes.
- 2 commits ahead of origin/homepage-redesign — push when ready.

## Source References
- `AGENTS.md` — project orientation (41 lines)
- `README.md` — public-facing readme (170 lines)
- `_internal/ATLAS_CONTROL.md` — execution control (454 lines)
- `_internal/ATLAS_REPO_MEMORY.md` — stable architecture/runtime facts (62KB)
- `_internal/DEV_LOG.md` — session ledger (40KB)
- `_internal/project_overview/01_SITE_DESIGN_SPEC.md` — product scope
- `package.json` — scripts, deps (Next.js 15, React 19, Tailwind 3)
- `next.config.ts` — static export config

## Memory Export
- All QA eval runs tracked in ATLAS_CONTROL.md §6. Gold eval 87/100 (run 4). F-089 regression entry in run 4 notes.
- Homepage redesign strategy doc exists in `_internal/page_designs/homepage_design_session_2026_03_22.md`.
- New compare-3 prototype lives in `src/app/proto/compare-3/` + `src/components/proto/Compare3View.tsx`.
- No secrets risk: `.env*` gitignored, no tracked or untracked env-like files exist.

## Agent Cautions
- Do NOT read `.env*` or other private-config file contents — check gitignore/status only
- Do NOT modify files outside `_internal/` or `src/` without explicit task scope
- `_internal/archive/2026-03-final-consolidation/docs/` contains archived spec docs — use project_overview/ for current grounding
- BSDA investigation scripts are one-off tools, not production pipeline

## Runtime Notes
- This file created by kanban task t_773013e2 (2026-05-21)
- Working directory: `/Users/buddy/projects/wgu-atlas` (dir workspace)
- Python: system Python, atlas_qa uses .venv
- Ollama: must be running for QA subsystem
