# Lineage Decisions Validation Spec

_2026-03-20. Spec for `scripts/validate_lineage_decisions.py`._

---

## 1. Validation Contract

The validator takes two inputs:
- `data/lineage/lineage_decisions.json` (required)
- `data/lineage/program_history_enrichment.json` (optional; enables cross-checks)

It is a read-only script. It mutates no files.

### Group A — Structure

**A1.** File is valid JSON. (Error on parse failure; abort all further checks.)

**A2.** Top-level keys present: `schema_version`, `last_updated`, `event_decisions`, `program_decisions`.

**A3.** `event_decisions` is a non-empty array; `program_decisions` is a non-empty array.

**A4.** Every `event_decisions` entry has all required keys:
`event_id`, `decision`, `display_state`, `decided_by`, `decided_at`, `wording_guard`, `change_summary_template`, `zero_overlap_rationale`, `notes`.

**A5.** Every `program_decisions` entry has all required keys:
`program_code`, `program_state`, `history_ui_state`, `linked_event_id`, `decided_by`, `decided_at`, `notes`.

**A6.** `wording_guard` is a boolean (not null, not string) on every event entry.

### Group B — Enum values

**B1.** `decision` is one of: `approve_history`, `reject_history`, `pending_hitl`, `pending_gap_check`.

**B2.** `display_state` is one of: `show`, `suppress`, `hide_pending`.

**B3.** `program_state` is one of: `history_approved`, `history_excluded`, `new_from_scratch`, `pathway_variant`, `no_meaningful_history`, `pending_hitl`, `pending_gap_check`.

**B4.** `history_ui_state` is one of: `show`, `hide_new`, `hide_no_history`, `hide_excluded`, `hide_pending`.

### Group C — Uniqueness

**C1.** No duplicate `event_id` values across `event_decisions`.

**C2.** No duplicate `program_code` values across `program_decisions`.

### Group D — Internal cross-references

**D1.** Every non-null `linked_event_id` in `program_decisions` must exist as an `event_id` in `event_decisions`.

**D2.** `history_approved` program → `linked_event_id` must be non-null and present in `event_decisions`.

### Group E — Decision/display_state consistency

**E1.** `decision: approve_history` → `display_state` must be `show`.

**E2.** `decision: reject_history` → `display_state` must be `suppress`.

**E3.** `decision: pending_hitl` → `display_state` must be `hide_pending`.

**E4.** `decision: pending_gap_check` → `display_state` must be `hide_pending`.

### Group F — Export safety (public-display guards)

**F1.** Every `approve_history` event must have a non-null, non-empty `change_summary_template`.

**F2.** Every event with `wording_guard: true` AND `decision: approve_history` must have a non-null, non-empty `change_summary_template`.
(Subset of F1; stated explicitly for audit trail. Both checks run independently.)

**F3.** Every `approve_history` event where any pair in `program_history_enrichment.json` has `jaccard_overlap == 0.0` must have a non-null, non-empty `zero_overlap_rationale`.
- Trigger: **any** pair for this event has `jaccard_overlap == 0.0` — not min, not all.
- One zero-overlap displayed relationship is sufficient to require rationale.
- If enrichment file is absent: emit WARNING that F3 was skipped; do not error.
- Template content is NOT validated for pending events — F3 only applies to `approve_history`.

**F4.** `history_ui_state: show` → `program_state` must be `history_approved`. No other program_state may produce `show`.

**F5.** `history_approved` program → the referenced event must have `decision: approve_history`. A program cannot be `history_approved` while its event is `reject_history` or pending.

**F6.** `history_excluded` program with non-null `linked_event_id` → the referenced event must NOT have `decision: approve_history`.

**F7.** `pathway_variant` program → `linked_event_id` must be null.

**F8.** `pending_hitl` or `pending_gap_check` program → `history_ui_state` must be `hide_pending`.

**F9.** `new_from_scratch`, `no_meaningful_history`, or `pathway_variant` program → `history_ui_state` must be one of `hide_new`, `hide_no_history`.

**F10.** `history_excluded` program → `history_ui_state` must be `hide_excluded`.

### Group G — Cross-checks against enrichment (requires enrichment file)

**G1.** Every `event_id` in `event_decisions` should exist in `program_history_enrichment.json`.
- Result: WARNING (not error). Could be stale ID, typo, or forward-reference.
- Will not be elevated to error until pipeline process is stable.

**G2.** Every event in `program_history_enrichment.json` with `site_worthy: true` that has no entry in `event_decisions`:
- Result: INFO notice (unreviewed; will be suppressed on export per the default-suppress rule).

**G3.** Every `approve_history` event in decisions where the corresponding enrichment entry has `site_worthy: false`:
- Result: WARNING. Decisions override enrichment, but this is unusual and warrants confirmation.

**G4.** Active programs (status = active in `public/data/programs.json`, if provided) with a matching candidate in `data/lineage/program_link_candidates.json` but no entry in `program_decisions`:
- Result: WARNING. Active programs with unreviewed candidates may generate false matches in future pipeline runs.
- Only emitted for active programs. Retired programs with unreviewed candidates: INFO only.
- Requires both `public/data/programs.json` and `program_link_candidates.json` as additional optional inputs.

### Group H — Completeness reminders (informational only)

**H1.** Any `pending_hitl` or `pending_gap_check` event with `wording_guard: true`: INFO notice that `change_summary_template` will be required before approval.

**H2.** Summary line: `N event_decisions (A approve / R reject / P pending); M program_decisions (X show / Y hide_pending / Z other)`.

---

## 2. Severity Model

| Level | Meaning | Exit code |
|---|---|---|
| ERROR | Would produce wrong public display, blocked export, or broken reference | 1 |
| WARNING | Data quality issue; does not directly affect display safety | 0 |
| INFO | Coverage stats and reminders | 0 |

| Group | Severity |
|---|---|
| A (structure) | ERROR |
| B (enums) | ERROR |
| C (uniqueness) | ERROR |
| D (cross-references) | ERROR |
| E (decision/display consistency) | ERROR |
| F (export safety) | ERROR |
| G1 (event ID not in enrichment) | WARNING |
| G2 (enrichment unreviewed site_worthy:true event) | INFO |
| G3 (approve overrides site_worthy:false) | WARNING |
| G4 (active program with candidate, no decisions entry) | WARNING |
| H (reminders, coverage) | INFO |

---

## 3. Test Matrix

| # | Test case | Input state | Expected | Why |
|---|---|---|---|---|
| T01 | Clean valid file | All required fields, valid enums, no duplicates, all approve events have templates | All pass, exit 0 | Baseline |
| T02 | Approved event with null `change_summary_template` | `decision: approve_history`, `change_summary_template: null` | ERROR F1 | Empty history block on live site |
| T03 | Approved event, any pair Jaccard=0.0, null rationale | `decision: approve_history`, enrichment has one pair at 0.0, `zero_overlap_rationale: null` | ERROR F3 | One zero-overlap pair is sufficient to require rationale |
| T04 | Invalid enum in `decision` | `decision: "reviewed"` | ERROR B1 | Unknown state bypasses all downstream guards |
| T05 | Orphan `linked_event_id` | Program has `linked_event_id: "PLE-099"`, PLE-099 not in event_decisions | ERROR D1 | Dangling reference |
| T06 | Duplicate event_id | Two entries with same `event_id` | ERROR C1 | Ambiguous decision at export time |
| T07 | Duplicate program_code | Two entries with same `program_code` | ERROR C2 | Ambiguous display state |
| T08 | `pathway_variant` with non-null `linked_event_id` | `program_state: pathway_variant`, `linked_event_id: "PLE-010"` | ERROR F7 | Pathway variants are not lineage events |
| T09 | `history_approved` linked to `reject_history` event | Program `history_approved`, event `reject_history` | ERROR F5 | Program overrides explicit rejection |
| T10 | Event in decisions not in enrichment | `event_id: "PLE-099"` in decisions, absent from enrichment | WARNING G1 | Possible stale ID or typo; not a blocker |
| T11 | `pending_gap_check` event with `display_state: show` | `decision: pending_gap_check`, `display_state: show` | ERROR E4 | Unresolved history exposed to students |
| T12 | `pending_hitl` program with `history_ui_state: show` | `program_state: pending_hitl`, `history_ui_state: show` | ERROR F4 + F8 | Unresolved candidate displayed |
| T13 | `reject_history` event with `display_state: show` | `decision: reject_history`, `display_state: show` | ERROR E2 | Rejected event reaches export |
| T14 | `history_excluded` program linked to `approve_history` event | `history_excluded`, event `approve_history` | ERROR F6 | Contradictory excluded/approved state |
| T15 | `wording_guard: true` + `pending_hitl` (no template) | `wording_guard: true`, `decision: pending_hitl`, `change_summary_template: null` | INFO H1 only | Pending; reminder only, not an error yet |
| T16 | `approve_history` overriding enrichment `site_worthy: false` | Decisions `approve_history`, enrichment `site_worthy: false` | WARNING G3 | Unusual override; confirm before export |
| T17 | Event entry missing `wording_guard` field | Event lacks `wording_guard` key | ERROR A4 | F2 cannot run; incomplete entry |
| T18 | `wording_guard: null` instead of boolean | `wording_guard: null` | ERROR A6 | Null guard silently disables F2 |
| T19 | Approved event with mixed pair Jaccards (some 0.0, some > 0.0), null rationale | One pair 0.3, one pair 0.0; `zero_overlap_rationale: null` | ERROR F3 | Confirms "any pair" trigger, not "all pairs" |
| T20 | Active program with candidate in link_candidates, no program_decisions entry | Program active, candidate exists, absent from decisions | WARNING G4 | May produce false match in future pipeline runs |
