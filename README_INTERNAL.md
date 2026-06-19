<!--
Last updated: 2026-06-18T06:35 UTC
Status: active
Owner: Buddy
-->

# README_INTERNAL — wgu-atlas

> Generated: 2026-06-17 | Branch: homepage-redesign | Sweep: full-backfill-001

## agent_context

```yaml
project: wgu-atlas
repo: https://github.com/wguDataNinja/wgu-atlas
purpose: "Public-facing reference explorer for WGU courses, programs, catalog history (111 mirrored editions, 2017-01 through 2026-06)"
status: active
ecosystem: wgu
tech: "Next.js 15 (App Router) + TypeScript + Tailwind + static export → GitHub Pages"
home: /Users/buddy/projects/wgu-atlas
git:
  branch: homepage-redesign
  policy: no direct git writes by workers
deploy: GitHub Actions CI (static export to out/)
```

## IVY Summary

- **Next.js site**: 55+ TS/TSX files across App Router pages (courses, programs, schools, compare, timeline, data, methods, about, proto)
- **Atlas QA subsystem**: Python Q&A over catalog data — retrieval (BM25 + embedding + fusion), compare mode, answer generation, evidence extraction, post-check, eval harness (100-question gold set)
- **Data layer**: catalog mirror in `data/catalog/` spans 111 editions through 2026-06; frontend JSON in `public/data/` still uses the frozen 2026-03 current-site snapshot — 838 active AP courses, 52 cert codes, 1,646 total course codes, 114 program blocks, 41 catalog events
- **3-doc internal system**: `_internal/ATLAS_CONTROL.md` (execution control), `_internal/ATLAS_REPO_MEMORY.md` (durable facts), `_internal/DEV_LOG.md` (dated ledger)
- **Ecosystem role**: Catalog-only reference explorer. **Does NOT consume Reddit/community data.** Explicit boundary with Reddit/WGU ecosystem repos.

## Current Work

| Track | Status | Detail |
|---|---|---|
| Atlas QA eval + F-089 retry regression | Active | 87/100 gold eval (run 4). Generation retry fires on correct model abstention for out-of-scope queries |
| Homepage redesign | Primary product track | Define research-first homepage for student curriculum inspection, degree comparison, catalog history |
| Course-page enrichment | Partial — landed | Incremental rollout of certification/prereq/capstone blocks |
| Official resource attachment | Active queue | Conservative expansion with provenance clarity |
| Cross-degree description reconciliation | Initiated — BSDA pass done | Compare degree-homepage text vs catalog for policy adoption |
| Continuity review | Initialized, lightweight | Validate compact review method; no validation batch created yet |

## Open Loops

1. **F-089 regression** — Remove or restrict Fix 3 retry (fires on correct abstention); re-run eval
2. **Homepage redesign** — Convert strategy into section-level messaging and implementation plan
3. **Course cert/prereq blocks** — Implement variant handling; no core design reopens
4. **3 missing catalog editions** — 2017-02, 2017-04, 2017-06
5. **Certificate codes** — Only tracked from 2024-09 forward
6. **Continuity review** — 4-card validation batch not yet created
7. **Program lineage export/routing** — Not implemented (not active)
8. **Catalog site-current refresh** — 2026-04/05/06 history mirror is present, but a trusted 2026-06 current snapshot is not yet available for public runtime exports

## Durable Decisions

- **basePath**: `/wgu-atlas` in `next.config.ts` — all routes prefixed
- **Data boundary**: Official catalog, community discussion signals, and LLM-generated content never mixed in same field
- **Ollama-dependent**: QA subsystem requires Ollama running locally for generation
- **`src.` → `atlas_qa.` imports**: Python scripts use `atlas_qa.` prefix for script-path compatibility (commit e97af19)
- **3-doc authority**: `CONTROL.md` > `REPO_MEMORY.md` > `DEV_LOG.md` for execution; `project_overview/` for product scope
- **Static export only**: `output: "export"` in next.config — no SSR, no API routes
- **No secrets tracked**: `.env*`, `.venv/` gitignored; no env-like files tracked or untracked
- **Catalog mirror boundary**: `data/catalog/` is the Atlas-local mirror. Prefer `WGU_CATALOG_OUTPUTS=/Users/buddy/projects/wgu-atlas/data/catalog` for Atlas-side site-data builds; `WGU_REDDIT_PATH` remains a backward-compatible alias.
- **Parser full-corpus rule**: `parse_catalog_v11.py` is authoritative only when run over the full corpus. Single-edition parser runs rebuild global indexes from incomplete input and invalidate change tracking/diffs.

## Related Repos / Ecosystem Context

Ecosystem context: `ivy-control/docs/project-context/reddit-wgu-ecosystem.md`

This repo's role: Public-facing catalog reference explorer. Uses WGU official catalog data only. **Does NOT consume Reddit data.** Explicit boundary: catalog and discussion signals never mixed.

Related repos:
- `/Users/buddy/Desktop/WGU-Reddit` — Primary Reddit ingestion (live SQLite DB, launchd fetch jobs). Atlas does NOT consume this data.
- `/Users/buddy/Desktop/WGU-Reddit/WGU_catalog` — Current home of the catalog acquisition/parser/change-tracking pipeline; expected future split target is `wgu-catalog`.
- `/Users/buddy/projects/wgu-reddit-intel` — WGU Reddit research workspace. Separate codebase from Atlas.
- `/Users/buddy/projects/bsda_courses` — Per-course Reddit post guide generation (consumes WGU-Reddit.db). Separate data boundary.
- `/Users/buddy/Desktop/projects/wgu-course-insights` — Reddit Qualitative Research Engine. Independent pipeline, own fetcher.

## Important Files

| File | Purpose |
|---|---|
| `README.md` | Public-facing entrypoint (170 lines) |
| `AGENTS.md` | Worker routing rules (41 lines) |
| `next.config.ts` | Static export config, basePath `/wgu-atlas` |
| `data/catalog/README.md` | Atlas-local catalog mirror policy and current 2026-06 mirror state |
| `src/atlas_qa/qa/generation.py` | Answer generation + retry logic (F-089 regression site) |
| `src/atlas_qa/qa/eval_runner.py` | Gold eval harness (100 questions) |
| `src/atlas_qa/qa/runtime_runner.py` | Orchestration runner (27KB) |
| `src/atlas_qa/qa/compare.py` | Compare mode (21KB) |
| `src/atlas_qa/qa/intent_gate.py` | Query intent classification |
| `src/atlas_qa/qa/router.py` | Query-to-module routing |
| `_internal/ATLAS_CONTROL.md` | Active execution control (454+ lines) |
| `_internal/ATLAS_REPO_MEMORY.md` | Architecture/runtime facts (62KB) |
| `_internal/project_overview/01_SITE_DESIGN_SPEC.md` | Product scope grounding |

## Safe Commands

```bash
pytest                          # QA subsystem tests (276 tests)
npm run lint                    # ESLint
npm run dev                     # Next.js dev server (port 3000, basePath /wgu-atlas)
npm run build                   # Static export to out/ (requires Ollama for QA gen)
npm run start                   # Production preview (requires build first)
```

## Agent Cautions

- Do NOT read `.env*` or other private-config file contents — check gitignore/status only
- Do NOT modify files outside `_internal/` or `src/` without explicit task scope
- Do NOT mix catalog data, discussion signals, and LLM-generated content in the same field
- Do NOT treat `trusted/2026_03/` as a rolling latest-edition directory; it is the frozen current-site snapshot until a newer trusted snapshot exists
- Do NOT run `parse_catalog_v11.py` for a single edition as an authoritative refresh; use full-corpus processing for cross-edition outputs
- Use `_internal/project_overview/` for current product grounding, not `_internal/archive/`
- BSDA investigation scripts are one-off tools, not production pipeline
- Ollama must be running locally for QA subsystem generation
- Python scripts require `.venv` + `requirements.txt`; run from repo root

## Public / Private Boundary

This repo is **public-facing**. The Next.js site deploys to GitHub Pages. Code in `src/` and configurations are public. `_internal/` contains working docs that should remain internal. `.env*` and `.venv/` are gitignored.

## Source References

- `README.md` — public entrypoint, data provenance (170 lines)
- `AGENTS.md` — worker routing rules (41 lines)
- `_internal/ATLAS_CONTROL.md` — active execution control (454+ lines)
- `_internal/ATLAS_REPO_MEMORY.md` — stable architecture/runtime facts (62KB)
- `_internal/DEV_LOG.md` — dated session ledger (654+ lines)
- `_internal/project_overview/01_SITE_DESIGN_SPEC.md` — product scope
- `package.json` — scripts, deps (Next.js 15, React 19, Tailwind 3)
- `next.config.ts` — static export config
- `ivy-control/docs/project-context/reddit-wgu-ecosystem.md` — Reddit/WGU ecosystem context
- `context/projects/wgu-atlas/context_packet.yaml` — assembled context packet
- `context/projects/wgu-atlas/smart_tree.md` — full directory tree

## Session Log Index

- `_internal/DEV_LOG.md` — primary session ledger (654+ lines, dated entries)

## IVY Memory Export

```yaml
<!-- IVY_MEM_START -->
memories:
  - id: wgu-atlas-role
    type: repo_context
    scope: repo
    privacy: public_eligible
    source_ref: README.md
    approval_state: approved
    content: "wgu-atlas is a public-facing WGU catalog reference explorer. Uses official catalog data only. Does NOT consume Reddit data."
    review_date: 2026-06-17
  - id: wgu-atlas-data-boundary
    type: boundary
    scope: repo
    privacy: public_eligible
    source_ref: README_INTERNAL.md
    approval_state: approved
    content: "Catalog data, community discussion signals, and LLM-generated content are never mixed in the same field."
    review_date: 2026-06-17
  - id: wgu-atlas-f089-regression
    type: workflow
    scope: repo
    privacy: internal
    source_ref: README_INTERNAL.md, ATLAS_CONTROL.md
    approval_state: needs_review
    content: "F-089: generation retry fires on correct model abstention for out-of-scope queries. Active regression."
    review_date: 2026-06-17
    tags: [bug, qa, blocker]
  - id: wgu-atlas-qa-eval-status
    type: workflow
    scope: repo
    privacy: internal
    source_ref: ATLAS_CONTROL.md
    approval_state: needs_review
    content: "Gold eval 87/100 (run 4). Retry logic may inflate score for out-of-scope queries."
    review_date: 2026-06-17
    tags: [qa, eval]
  - id: wgu-atlas-ecosystem-boundary
    type: boundary
    scope: ecosystem
    privacy: public_eligible
    source_ref: reddit-wgu-ecosystem.md
    approval_state: approved
    content: "wgu-atlas is in the WGU/Reddit ecosystem but is the only repo that uses catalog data only. All other WGU repos consume Reddit data."
    review_date: 2026-06-17
  - id: wgu-atlas-homepage-redesign
    type: workflow
    scope: repo
    privacy: internal
    source_ref: README_INTERNAL.md
    approval_state: needs_review
    content: "Homepage redesign is the primary product track. Needs strategy-to-section conversion. Active branch: homepage-redesign."
    review_date: 2026-06-17
    tags: [product, design]
  - id: wgu-atlas-catalog-mirror-2026-06
    type: workflow
    scope: repo
    privacy: internal
    source_ref: data/catalog/README.md
    approval_state: needs_review
    content: "data/catalog is mirrored through 2026-06 (111 editions). Public runtime exports still use the frozen 2026-03 current-site snapshot until a newer trusted snapshot exists."
    review_date: 2026-06-18
    tags: [catalog, mirror, data]
```
<!-- IVY_MEM_END -->

## Runtime Notes

- Generated: 2026-06-17 by ivy-dev-worker (task full-backfill-001-wgu-atlas)
- Working directory: `/Users/buddy/projects/wgu-atlas`
- Branch: `homepage-redesign` (ahead of origin)
- HEAD: `8367f82` — README_INTERNAL: created/refreshed (wgu-atlas)
- Git: 38 modified + 42 untracked files (pre-existing dirty state; README_INTERNAL.md is modified)
- Python: system Python, atlas_qa uses `.venv`
- Ollama: must be running for QA subsystem generation
- Dependencies: Next.js 15, React 19, Tailwind 3, TypeScript, Python (rank-bm25, sentence-transformers, pydantic)
- Compatibility artifacts (untracked): `README_INTERNAL.template_pilot.md`, `AGENTS.template_pilot.md`, `TEMPLATE_PILOT_REPORT.md` — remnants of prior draft-only pilot


## Active TODO

<!-- Unchecked items for current or near-term work. Use - [ ] unchecked, - [x] done. -->

- [ ] None.


## Recent Checkins

<!-- Markdown table: Checked At | Agent | Status | Summary | Log -->

| Checked At | Agent | Status | Summary | Log |
|---|---|---|---|---|
