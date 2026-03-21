# Program Guide Roster Bridge Schema (Proposed)

Date: 2026-03-21

Status: proposed schema for a prep-build session; not a shipping artifact.

## Recommended paths

- Single-file option: `data/program_guides/bridge/program_guide_roster_bridge.json`.
- Split option for scale:
  - `data/program_guides/bridge/index.json`
  - `data/program_guides/bridge/guides/{program_code}.json`

## Top-level record

- `generated_on`
- `sources`
- `guide_count`
- `program_code_alias_crosswalk`
- `guides[]`

## GuideRosterRecord fields

- Identity/context: `program_code`, `program_code_effective`, `family`, `disposition`, `sp_status`.
- Guide metadata: `degree_title_guide`, `guide_version`, `guide_pub_date`.
- Program-history linkage: `program_history_status`, `program_history_colleges`, `program_history_degree_headings`.
- Alignment flags: `program_history_exists`, `degree_heading_match_class`, `version_alignment_class`.
- Roster summary: counts + anchor class counts.
- `roster_rows[]`.

## RosterRow fields

- `surface`: `aos` or `sp`.
- `guide_title_raw`, `guide_title_normalized`.
- Context: `aos_group`, `sp_term`, `sp_cus`.
- Canonical attachment prep: `anchor_class`, `canonical_candidate_codes`.

## Build constraints

1. Preserve ambiguous rows and candidate code arrays; do not force early collapse.
2. Carry alias crosswalk explicitly for non-1:1 program-code mappings.
3. Keep cert/prereq out of v1 bridge row payload unless downstream analysis needs them.