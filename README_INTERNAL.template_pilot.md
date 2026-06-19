# README_INTERNAL — wgu-atlas

> Branch: homepage-redesign

```yaml
agent_context:
  project: wgu-atlas
  repo: https://github.com/wguDataNinja/wgu-atlas
  purpose: "Public-facing reference explorer for WGU courses, programs, catalog history (108 editions, 2017–2026)"
  status: active
  ecosystem: wgu
  tech: "Next.js 15 (App Router) + TypeScript + Tailwind + static export → GitHub Pages"
  home: /Users/buddy/projects/wgu-atlas
  git:
    branch: homepage-redesign
    policy: no direct git writes by workers
```

## IVY Summary

Public-facing catalog reference explorer for WGU. Next.js static site deployed via GitHub Actions. Contains Atlas QA subsystem (Python) for intelligent course/program Q&A over archived catalog data. Uses official WGU catalog only (CSV/JSON). **Does NOT consume Reddit/community data.** 108 catalog editions from 2017–2026.

## Current Work

- **QA eval + F-089 retry regression** — Active: 87/100 gold eval (run 4). Retry fires on correct model abstention for out-of-scope queries.
- **Homepage redesign** — Primary product track: research-first homepage for student curriculum inspection, degree comparison, catalog history.
- **Course-page enrichment** — Partial: incremental rollout of certification/prereq/capstone blocks.
- **Official resource attachment** — Active queue: conservative expansion with provenance clarity.
- **Cross-degree description reconciliation** — Initiated: BSDA pass done.

## Open Loops

1. **F-089 regression** — Remove or restrict Fix 3 retry (fires on correct abstention); re-run eval.
2. **Homepage redesign** — Convert strategy into section-level messaging and implementation plan.
3. **Course cert/prereq blocks** — Implement variant handling; no core design reopens.
4. **3 missing catalog editions** — 2017-02, 2017-04, 2017-06.
5. **Certificate codes** — Only tracked from 2024-09 forward.
6. **Continuity review** — 4-card validation batch not yet created.
7. **Program lineage export/routing** — Not implemented (not active).

## Durable Decisions

- **basePath**: `/wgu-atlas` in next.config.ts — all routes prefixed.
- **Data boundary**: Official catalog, community discussion signals, and LLM-generated content never mixed in same field.
- **Ollama-dependent**: QA subsystem requires Ollama running locally for generation.
- **`src.` → `atlas_qa.` imports**: Python scripts use `atlas_qa.` prefix for script-path compatibility.
- **3-doc authority**: CONTROL.md > REPO_MEMORY.md > DEV_LOG.md for execution; project_overview/ for product scope.
- **Static export only**: `output: "export"` in next.config — no SSR, no API routes.
- **No secrets tracked**: `.env*`, `.venv/` gitignored; no env-like files tracked or untracked.

## Related Repos / Ecosystem Context

Ecosystem context: `ivy-control/docs/project-context/reddit-wgu-ecosystem.md`

This repo's role: Public-facing catalog reference explorer. Uses WGU official catalog data only. **Does NOT consume Reddit data.** Explicit boundary: catalog and discussion signals never mixed.

Related repos:
- `/Users/buddy/Desktop/WGU-Reddit` — Primary Reddit ingestion. This repo does NOT consume its data.
- `/Users/buddy/projects/wgu-reddit-intel` — WGU Reddit research workspace. Separate pipeline.
- `/Users/buddy/projects/bsda_courses` — Reddit post guide generation (consumes WGU-Reddit.db). Separate data boundary.
- `/Users/buddy/Desktop/projects/wgu-course-insights` — Reddit Qualitative Research Engine. Independent pipeline.

## Important Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Worker routing rules |
| `README.md` | Public-facing readme |
| `next.config.ts` | Static export, basePath `/wgu-atlas` |
| `src/atlas_qa/qa/generation.py` | Answer generation + retry logic (F-089 regression) |
| `src/atlas_qa/qa/eval_runner.py` | Gold eval harness (100 questions) |
| `src/atlas_qa/qa/intent_gate.py` | Query intent classification |
| `src/atlas_qa/qa/router.py` | Query-to-module routing |
| `_internal/ATLAS_CONTROL.md` | Active execution control |
| `_internal/ATLAS_REPO_MEMORY.md` | Architecture/runtime facts |
| `_internal/DEV_LOG.md` | Session ledger |

## Safe Commands

```bash
pytest                          # QA subsystem tests (276 tests)
npm run lint                    # ESLint
npm run dev                     # Next.js dev server (port 3000, basePath /wgu-atlas)
npm run build                   # Static export to out/ (requires Ollama for QA gen)
```

## Agent Cautions

- Do NOT read `.env*` or other private-config file contents — check gitignore/status only
- Do NOT modify files outside `_internal/` or `src/` without explicit task scope
- Do NOT mix catalog data, discussion signals, and LLM-generated content in the same field
- Use `_internal/project_overview/` for current product grounding, not `_internal/archive/`
- BSDA investigation scripts are one-off tools, not production pipeline

## Public / Private Boundary

This repo is **public-facing**. The Next.js site deploys to GitHub Pages. Code in `src/` and configurations are public. `_internal/` contains working docs that should remain internal. `.env*` and `.venv/` are gitignored.

## Runtime Notes

- Created: 2026-05-28 (template pilot draft — no files overwritten)
- Working directory: `/Users/buddy/projects/wgu-atlas`
- Current README_INTERNAL.md: 155 lines, TRACKED
- Branch: homepage-redesign (ahead of origin by 2 commits)

## Source References

- Existing README_INTERNAL.md (155 lines, tracked)
- Existing AGENTS.md (41 lines, tracked)
- ivy-control/docs/project-context/reddit-wgu-ecosystem.md
- _internal/ATLAS_CONTROL.md
- _internal/ATLAS_REPO_MEMORY.md

## Session Log Index

- `_internal/DEV_LOG.md` — dated session ledger

## IVY Memory Export

```yaml
<!-- IVY_MEM_START -->
memories:
  - id: wgu-atlas-role
    type: repo_context
    scope: repo
    privacy: public_eligible
    source_ref: README.md, README_INTERNAL.md
    approval_state: approved
    content: "wgu-atlas is a public-facing WGU catalog reference explorer. Uses official catalog data only. Does NOT consume Reddit data."
    review_date: 2026-05-28
  - id: wgu-atlas-data-boundary
    type: boundary
    scope: repo
    privacy: public_eligible
    source_ref: README_INTERNAL.md
    approval_state: approved
    content: "Catalog data, community discussion signals, and LLM-generated content are never mixed in the same field."
    review_date: 2026-05-28
  - id: wgu-atlas-f089-regression
    type: workflow
    scope: repo
    privacy: internal
    source_ref: README_INTERNAL.md, ATLAS_CONTROL.md
    approval_state: needs_review
    content: "F-089: generation retry fires on correct model abstention. Active regression."
    review_date: 2026-05-28
  - id: wgu-atlas-qa-eval
    type: workflow
    scope: repo
    privacy: internal
    source_ref: ATLAS_CONTROL.md
    approval_state: needs_review
    content: "Gold eval 87/100 (run 4). Retry logic may inflate score for out-of-scope queries."
    review_date: 2026-05-28
<!-- IVY_MEM_END -->
```
