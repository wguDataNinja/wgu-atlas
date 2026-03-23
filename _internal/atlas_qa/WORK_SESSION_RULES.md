# Work Session Rules — Atlas QA

## Purpose

Work sessions are the execution unit for Atlas QA implementation. Each session maps to a stage in the build plan and has a bounded scope, explicit inputs, and a definition of done. Sessions are not design forums.

---

## Naming convention

Sessions are numbered linearly: `00_atlas_foundation`, `01_canonical_objects`, `02_exact_lookup_path`, etc. Numbers are stable — do not renumber completed sessions.

---

## Required files per active session

| File | Required | Purpose |
|---|---|---|
| `SESSION_SPEC.md` | Yes | Execution contract. Defines scope, inputs, outputs, invariants, validation, and definition of done. |
| `DEV_LOG.md` | Yes | Append-only work log. Records what was actually done. |
| `HANDOFF.md` | Optional | Add only when a session genuinely needs passalong context not captured in the spec or log — e.g., an unexpected blocker, an open decision deferred to the next session, or an interim state that requires special handling. Do not create it by default. |

---

## Session spec rules

- The spec is the execution contract. Implementation must not expand beyond it.
- Tests, builds, and validation checks are allowed **only when the spec explicitly permits them**.
- If a tradeoff or edge case arises that would require expanding scope or changing design, **stop and log it**. Do not resolve it locally.
- Specs for future sessions are stubs until the prior session is complete. Write the spec before starting work, not in advance of need.

---

## DEV_LOG.md format

Append-only. Each entry includes:

```
## YYYY-MM-DD HH:MM — [actor/agent]

**Scope:** what was worked on
**Files touched:** list
**Checks run:** list (or "none")
**Results:** pass/fail/notes
**Blockers/deviations:** any deviation from spec, any open question surfaced
```

---

## No placeholder sprawl

Do not create spec files, log files, or stub docs for sessions that are not yet active. Write session 03+ specs immediately before starting that work, not ahead of time.

---

## Design lock rules

- The Atlas QA architecture and source-authority policy are locked.
- Implementation agents and sessions may not reopen or reinterpret locked decisions.
- If an external reviewer recommends changes to locked decisions, flag to owner before acting.
- No runtime QA code belongs in `wgu-reddit`. All Atlas QA implementation work belongs in `wgu-atlas`.
