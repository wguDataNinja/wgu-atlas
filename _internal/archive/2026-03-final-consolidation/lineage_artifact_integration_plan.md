# Lineage Artifact Integration Plan

_2026-03-20. Conservative scope: curation overlay only. No frontend integration._

---

## 1. Final Artifact Placement

**Recommended path:** `data/lineage/lineage_decisions.json`

**Rationale:**
- `data/lineage/` already exists and holds all other lineage artifacts
- Flat, predictable path; consistent with sibling files
- No subdirectory needed for a single decisions file

**Action:** Rename `data/lineage/draft_lineage_decisions.json` → `data/lineage/lineage_decisions.json`.
No companion artifact is needed at this stage. The single JSON file with `event_decisions[]` and `program_decisions[]` is sufficient. Companion files (e.g., a per-program export, a frontend-ready summary) belong to a later export step and should not be created until the export logic is implemented.

---

## 2. Merge / Precedence Model

### Sources

| File | Role | Authority |
|---|---|---|
| `data/lineage/program_history_enrichment.json` | Computed truth — Jaccard metrics, pair-level stats, heuristic `site_worthy` | Overlap metrics only |
| `data/lineage/lineage_decisions.json` | Curation truth — human decisions, `change_summary_template`, `display_state` | Display authority |
| `public/data/program_lineage.json` _(future)_ | Frontend export — read-only site artifact | Derived; never authoritative |

`program_history_enrichment.json`'s `site_worthy` field is heuristic-computed by `infer_importance_and_site_worthy()` in `generate_program_history_enrichment.py`. It is NOT a display decision. It is an input signal only.

### Precedence rules

1. If `lineage_decisions.json` contains an `event_decisions` entry for an event ID, that entry's `display_state` is the final display decision. It overrides `site_worthy` from enrichment.
2. If an event exists in `program_history_enrichment.json` but has NO entry in `lineage_decisions.json`, treat it as unreviewed: do NOT export it to the frontend. Default: suppress.
3. If a `program_decisions` entry references a `linked_event_id` and that event is `approve_history`, the program's `history_ui_state` must be `show`. If the event is `reject_history` or pending, the program's `history_ui_state` must not be `show` — treat as a validation error.
4. If a `program_decisions` entry has no `linked_event_id` (e.g., `new_from_scratch`, `pathway_variant`, `no_meaningful_history`), its `history_ui_state` alone governs the frontend. These programs are never exported with a history block.
5. Export of an approved event requires both:
   - `display_state: "show"` on the event
   - Non-null `change_summary_template` on the event
   If either is missing, block the export for that event (do not silently skip).
6. Export of an approved event with `wording_guard: true` additionally requires non-null `change_summary_template`. Same block behavior.
7. Export of an approved event with Jaccard = 0.0 across all pairs additionally requires non-null `zero_overlap_rationale`. Same block behavior.

### State → export behavior

| `program_state` | `history_ui_state` | Export behavior |
|---|---|---|
| `history_approved` | `show` | Export history block with `change_summary_template` |
| `history_excluded` | `hide_excluded` | No history block. Do not surface predecessor info. |
| `new_from_scratch` | `hide_new` | No history block |
| `pathway_variant` | `hide_new` | No history block |
| `no_meaningful_history` | `hide_no_history` | No history block |
| `pending_hitl` | `hide_pending` | No history block. Internal tracking only. |
| `pending_gap_check` | `hide_pending` | No history block. Internal tracking only. |

`hide_pending`, `hide_excluded`, `hide_new`, and `hide_no_history` all render identically on the live site: no history section. The distinction is internal-artifact-only.

### Default behavior (unreviewed events/programs)

- An event in `program_history_enrichment.json` with no entry in `lineage_decisions.json`: **suppress**. Do not export. Do not infer display from heuristic `site_worthy`.
- A program with no entry in `lineage_decisions.json` and no history block needed: no action required. The majority of bedrock/stable programs do not need explicit entries.
- A program with no entry in `lineage_decisions.json` that has a candidate in `program_link_candidates.json`: treat as unreviewed; suppress. Same rule as events.

---

## 3. Exact Repo-Touch Plan

### Required now (before first export)

#### `data/lineage/lineage_decisions.json` — rename from draft
- Action: `git mv data/lineage/draft_lineage_decisions.json data/lineage/lineage_decisions.json`
- Scope: file rename only; no content change
- Note: This file must be tracked in git and must not be listed in `.gitignore`. It is a durable curation artifact, not a generated file.

#### `docs/DECISIONS.md` — patches per `_internal/draft_lineage_doc_patch_plan.md`
- Actions: edit §6.1, §6.2, §6.3; add §5.10, §5.11, §6.5, §6.6, §6.7
- Scope: exactly the patch list in draft plan; no other sections
- Required now so the curation record is self-consistent before lineage data ships

#### `docs/ATLAS_SPEC.md` — patches per `_internal/draft_lineage_doc_patch_plan.md`
- Actions: edit §5.2 (add artifact entry), §7.3 (add Stage 1.5), §6 script registry (add merge logic note to `build_site_data.py` row)
- Scope: exactly the patch list in draft plan

#### `scripts/validate_lineage_decisions.py` — new validation helper
- Purpose: offline integrity check for `lineage_decisions.json` before any export
- Required now so that the rename step can be validated immediately
- Scope: read-only; exits non-zero on any violation; no file mutation
- Checks (in order):
  1. All required fields present on every `event_decisions` entry: `event_id`, `decision`, `display_state`, `decided_by`, `decided_at`, `wording_guard`, `change_summary_template`, `zero_overlap_rationale`
  2. All `decision` values are in allowed enum: `approve_history`, `reject_history`, `pending_hitl`, `pending_gap_check`
  3. All `display_state` values are in allowed enum: `show`, `suppress`, `hide_pending`
  4. All `program_state` values are in allowed enum: `history_approved`, `history_excluded`, `new_from_scratch`, `pathway_variant`, `no_meaningful_history`, `pending_hitl`, `pending_gap_check`
  5. All `history_ui_state` values are in allowed enum: `show`, `hide_new`, `hide_no_history`, `hide_excluded`, `hide_pending`
  6. No duplicate `event_id` values
  7. No duplicate `program_code` values
  8. All `linked_event_id` values in `program_decisions` reference an existing `event_id` in `event_decisions` (or are null)
  9. Every `approve_history` event with `wording_guard: true` has a non-null `change_summary_template`
  10. Every `approve_history` event has a non-null `change_summary_template` (regardless of `wording_guard`)
  11. Cross-check: for every Jaccard-0.0 event in `program_history_enrichment.json` that has `decision: approve_history` in decisions, `zero_overlap_rationale` must be non-null. (Requires loading enrichment file; skip gracefully if enrichment file not present.)
  12. Consistency: for every `program_decisions` entry with `program_state: history_approved`, the `linked_event_id` must exist and have `decision: approve_history`
  13. Consistency: for every `program_decisions` entry with `history_ui_state: show`, the `program_state` must be `history_approved`
- Usage: `python3 scripts/validate_lineage_decisions.py [--decisions data/lineage/lineage_decisions.json] [--enrichment data/lineage/program_history_enrichment.json]`

### Required later (at frontend integration)

#### `scripts/build_site_data.py` — add lineage export step
- Purpose: produce `public/data/program_lineage.json` from merged enrichment + decisions
- Deferred until: frontend types and data loader are designed
- Scope when added: new function `export_program_lineage()` using the merge/precedence rules above; called as a new step in the build pipeline
- Must not touch the decisions file — read-only access only
- Output schema (tentative): array of `{ program_code, event_id, change_summary, from_programs, to_programs, transition_date }`; details to be finalized with frontend types

#### `src/lib/types.ts` — extend `ProgramRecord` or add `ProgramLineageRecord`
- Deferred until: frontend integration sprint

#### `src/lib/data.ts` — add `getProgramLineage(code)` loader
- Deferred until: frontend integration sprint

#### `src/app/programs/[code]/page.tsx` — add history section
- Deferred until: frontend integration sprint

### Not required (ever)

#### `scripts/generate_program_history_enrichment.py` — no change needed
- This script must NOT write to `lineage_decisions.json`. It already doesn't; no change needed.
- Add a one-line comment to the script header: "Does not read or write lineage_decisions.json; see docs/ATLAS_SPEC.md §7.3 Stage 1.5."
- This is a doc-comment touch, not functional change. Can be done during the docs patch pass.

#### `scripts/build_program_lineage_artifacts.py` — no change needed
- Pipeline Stage 0; upstream of decisions file. No interaction.

#### `scripts/compare_program_courses.py` — no change needed
- Pipeline Stage 2; computes overlap metrics only. No interaction.

---

## 4. Validation Approach

To verify the artifact model is self-consistent after the rename:

```
python3 scripts/validate_lineage_decisions.py \
  --decisions data/lineage/lineage_decisions.json \
  --enrichment data/lineage/program_history_enrichment.json
```

Expected clean run output:
```
Loaded 11 event_decisions, 23 program_decisions
All enum values valid
No duplicate IDs
All linked_event_id references resolved
All approve_history events have change_summary_template
PLE-022: zero_overlap_rationale present ✓
Cross-check against enrichment: 28 events; 11 decisions entries; 17 unreviewed (suppress on export)
No violations found.
```

If the script reports violations, resolve before any export step runs.
