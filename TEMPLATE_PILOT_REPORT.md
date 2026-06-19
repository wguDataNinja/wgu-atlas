# Template Pilot Report — wgu-atlas

## Status: PASS

## Current vs Proposed

### README_INTERNAL.md

| Dimension | Current (155 lines, tracked) | Proposed (draft, 201 lines) |
|-----------|------------------------------|-----------------------------|
| agent_context | Present | Kept + branch info |
| IVY Summary | Present | Kept |
| Current Work | Present | Kept |
| Open Loops | Present | Kept |
| Durable Decisions | Present | Kept |
| Related Repos / Ecosystem Context | Ecosystem link in Source References | Full Related Repos section |
| Important Files | Present | Trimmed to most critical |
| Safe Commands | Missing | Added |
| Agent Cautions | Present | Refined |
| Public / Private Boundary | Implicit in Watchouts | Explicit section |
| Runtime Notes | Present | Kept + pilot context |
| Source References | Present | Kept |
| Session Log Index | Implicit (DEV_LOG.md referenced) | Explicit |
| IVY Memory Export | Present (paragraph notes) | Schema-fixed YAML |

### AGENTS.md

| Dimension | Current (41 lines, tracked) | Proposed (draft, 108 lines) |
|-----------|------------------------------|-----------------------------|
| Role | Implicit in Purpose | Explicit |
| Read First | Not structured | Formalized reading order |
| Allowed Work | Implicit | Explicit |
| Forbidden Work | Some in Watchouts | Full list |
| Safety Boundaries | Missing | Added secrets, git, data boundary |
| Related Context | Missing | Added priority chain |
| Logging / Closeout | Missing | Added |
| Stop Conditions | Missing | Added (incl data boundary rule) |

## Tracking Status

| File | Status |
|------|--------|
| README_INTERNAL.md | Tracked |
| AGENTS.md | Tracked |

Both files are tracked and durable.

## Ecosystem Context Captured

- WGU/Reddit ecosystem context linked from `ivy-control/docs/project-context/reddit-wgu-ecosystem.md`
- Local role stated: catalog reference explorer, does NOT consume Reddit data
- Related repos listed: Desktop/WGU-Reddit, wgu-reddit-intel, bsda_courses, wgu-course-insights
- Data boundary documented: catalog and discussion signals never mixed

## Risks

- **Current AGENTS (41 lines) is already close to template quality**: Tracked, concise, no durable facts. Low migration risk.
- **Dirty git**: Multiple modified tracked files + 1 deleted. 2 commits ahead of origin.
- **Branch divergence**: homepage-redesign is ahead of origin. Any write needs branch awareness.
- **Public/private boundary**: The repo is public-facing. Care needed to keep internal working docs in `_internal/`.

## Direct Replacement Recommended: Yes.

Current README_INTERNAL is strong (155 lines). Main gaps are Safe Commands, explicit Public/Private Boundary, and ecosystem context section. Current AGENTS (41 lines) is the best existing AGENTS in the pilot — just needs safety boundaries, stop conditions, and context routing.
