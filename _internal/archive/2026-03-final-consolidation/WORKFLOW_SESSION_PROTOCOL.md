# Workflow Session Protocol — GPT + Codex Collaboration

_Reusable. Project-agnostic. Optimized for quota constraints._

---

## Purpose

Define a repeatable session shape for work that requires planning, analysis, and artifact production across multiple sessions where context is not fully persistent.

---

## Roles

| Role | Responsibility |
|---|---|
| **Human** | Prioritizes work, locks decisions, accepts or rejects proposals, provides HITL answers |
| **GPT (Claude)** | Proposes, drafts, analyzes, writes artifacts to files; does not self-approve |
| **Codex/Claude Code** | Executes file writes and edits under human approval; reads repo state on demand |

**Rule:** GPT proposes. Human accepts. Codex executes. GPT does not promote draft → canonical without explicit human confirmation.

---

## Session Shape

### Start-of-session checklist
1. Run `git status --short` to know unstaged/untracked state.
2. State the active workstream and goal in one sentence.
3. Read the active continuity doc (`_internal/PROJECT_CONTINUITY_*.md`) if picking up from prior session.
4. Read any open ledgers / pending-decision files for this workstream.
5. Do not restate prior analysis — reference the continuity doc and proceed.

### Per-iteration loop

```
Human: task or question
Codex: reads necessary files → produces output → saves to _internal/ drafts → pastes compact summary
Human: accepts / rejects / redirects
Codex: updates in place if accepted; discards if rejected
```

**Per-iteration rules:**
- Save full output to a file; paste back only compact review info.
- If the output is an artifact (JSON, markdown patch), save it under `_internal/` with `draft_` prefix until promoted.
- If the output is a policy decision or ledger entry, write it into the relevant ledger file directly.
- Do not re-derive facts already in a ledger or continuity doc. Reference them by file name.
- Do not restate prior analysis in the paste-back summary.

### End-of-session checklist
1. Confirm all accepted artifacts are saved (not just pasted in conversation).
2. Append a session log entry to `_internal/SESSION_LOG.md`.
3. Update `_internal/PROJECT_CONTINUITY_*.md` with any locked decisions or new pending items.
4. List the recommended next session's starting task explicitly.

---

## What Codex saves to files

| Content type | Where to save |
|---|---|
| Full draft artifacts (JSON, markdown) | `_internal/draft_<name>.md` or `data/lineage/draft_<name>.json` |
| Finalized canonical artifacts | `data/lineage/<name>.json` or `docs/<name>.md` (only after human promotion) |
| Policy ledgers / decision logs | `_internal/<workstream>_decisions.md` |
| Continuity doc | `_internal/PROJECT_CONTINUITY_<project>.md` |
| Session log | `_internal/SESSION_LOG.md` |
| Validation specs / plans | `_internal/<name>_plan.md` |

**Never save to:** `public/data/` during planning sessions. That directory is for committed, export-ready artifacts only.

---

## What Codex pastes back only

- File paths of saved artifacts (not content)
- Compact enum/schema lists
- Small decision tables or check lists
- Single unresolved issue per topic
- Recommended next step (one sentence)

Do not paste back: full JSON, full markdown files, re-derived analysis, prior decision summaries.

---

## Artifact naming conventions

| Stage | Convention |
|---|---|
| Active draft | `draft_<name>.<ext>` |
| Promoted to canonical | `<name>.<ext>` (drop `draft_` prefix) |
| Superseded | Move to `_internal/archive/` |

**Promotion rule:** A draft is promoted to canonical only when the human explicitly confirms it. Codex does not self-promote.

---

## Logging rules

Log at:
- Session start (brief): current state, goal
- Session end: decisions locked, artifacts created, next step
- Decision-lock moments only: when a HITL answer resolves a pending item, record it immediately in the relevant ledger

Do not log:
- Every iteration
- Analysis that's already in an artifact
- Decisions that are self-evident from artifact content

---

## Rules for keeping Codex turns cheap

1. **One ask per turn.** Do not combine unrelated questions.
2. **Reference, don't re-derive.** If the answer is in an artifact, cite the file; don't re-read and re-summarize.
3. **Paste compact summaries.** Never paste a full artifact back into conversation.
4. **Batch file writes.** When multiple files need updating, do them in one turn.
5. **Skip confirmation for trivial writes.** If the output is a direct execution of an accepted plan, write and move on.
6. **Defer non-blocking items.** If something doesn't block the current task, add it to the pending-items ledger and continue.

---

## Unresolved items

Unresolved items go into the relevant ledger or continuity doc under a `## Pending` section. They do not recur in prose. The pending section is reviewed at session start.

---

## Policy: GPT proposes, human accepts

Codex does not promote decisions, approve its own proposals, or mark items as "done" without human confirmation. Every artifact starts as a draft. Every policy decision requires a human decision-lock before it is considered final.
