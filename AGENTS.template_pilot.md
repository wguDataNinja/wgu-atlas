# wgu-atlas — AGENTS

> **AGENTS.md is a router, not a manual.** Keep only the rules needed to decide what to do next; put details in `README_INTERNAL.md` and linked docs.
>
> **Do NOT store durable project facts here.** Durable facts (architecture, decisions, open loops) belong in `README_INTERNAL.md`.

## Role

Public-facing reference explorer for WGU courses, programs, and catalog history. Workers perform read-only inspection, documentation updates, and report drafting. No application code edits unless explicitly scoped.

## Read First

Before doing any work, read these in order:

1. `README_INTERNAL.md` — Durable repo memory
2. `README.md` — Public entrypoint
3. `ivy-control/docs/project-context/reddit-wgu-ecosystem.md` — WGU/Reddit ecosystem context
4. `_internal/ATLAS_CONTROL.md` — Active execution control (if task requires QA or product work)

## Allowed Work

- Read-only inspection, status checks, validation runs
- Documentation updates within explicit scope
- Running safe commands listed in `README_INTERNAL.md`
- Drafting reports from source-backed evidence
- Running Python QA tests (`pytest`) for verification

## Forbidden Work

- Read `.env`, credentials, secret files, or private config
- Access raw GPT exports, raw transcripts, email bodies, private datasets
- Run model jobs, batch inference, or long LLM pipelines
- Install packages, modify dependencies, or change environment config
- Edit application code unless explicitly in scope
- Create automatic commits, push, checkout, reset, merge, rebase, or clean
- Use `git add .`, `git add -A`, or `git commit -a`
- Delete or move files without explicit approval
- Mix catalog data, discussion signals, and LLM-generated content in the same field
- Write to external repos
- Deploy to GitHub Pages

## Safety Boundaries

### Secrets and Sensitive Data

```
SENSITIVE PATH — Do not read:
- .env, *.env
- credentials, config/tokens
- identity/
- raw GPT exports, raw transcripts, email bodies
- private datasets, DB rows containing user data
```

### Git

```
Git Steward gates all commits. No direct git writes by workers.
- Allowed: git status, git diff, git log (read-only)
- Blocked: git add, git commit, git push, git checkout, git reset, git clean, git merge, git rebase
```

### Data Boundary

```
Official catalog data, community discussion signals, and LLM-generated content are never mixed in the same field.
Always check attribution before modifying content fields.
```

## Related Context

1. `ivy-control/docs/project-context/reddit-wgu-ecosystem.md` — Canonical WGU/Reddit ecosystem map
2. `ivy-control/context/project_index.md` — Human repo index
3. `_internal/ATLAS_REPO_MEMORY.md` — Stable architecture and runtime facts

## Logging / Closeout

After meaningful work:
1. Append worker log entry at `runtime/logs/workers/YYYY-MM-DD/wgu-atlas.md`
2. Update `README_INTERNAL.md` if state changed
3. Update `_internal/DEV_LOG.md` if session work
4. Report changed files — do not initiate git writes unless explicitly asked
5. Report concise result: status, files changed, worker log path

## Stop Conditions

Stop and report blocker if:
- The task requires secrets, credentials, or private datasets
- The task requires raw GPT exports, raw transcripts, or email bodies
- The task requires running model jobs or long LLM pipelines
- The task requires editing application code outside explicit scope
- The task requires git operations beyond read-only inspection
- The task requires deploying to GitHub Pages
- The task requires mixing catalog and discussion data in the same field
- The repo's `README_INTERNAL.md` is missing or too stale to trust, unless the task is to create or refresh it
- The approval boundary is unclear
