# Program Guide Roster Bridge Assessment

Date: 2026-03-21

Scope: evaluate whether to pre-build a per-guide course-roster bridge before the larger course-enrichment extraction session.

## Part A — Program ↔ Guide Alignment

- Guides analyzed: `115`.
- Direct `program_history.csv` match by `program_code`: `110/115`.
- Missing direct matches: `5` -> `BSSWE_Java, MSRNNUED, MSRNNUNI, MSRNNULM, BSPRN`.
- Degree heading match classes: `{'exact_heading_match': 93, 'partial_heading_match': 14, 'missing_program_history': 5, 'no_heading_match': 3}`.
- Version alignment classes: `{'version_present_in_program_history': 103, 'version_not_in_program_history': 5, 'missing_program_history': 5, 'guide_version_missing': 2}`.

Notable edge cases:
- No heading match: `PMCNUFNP, BSITM, PMCNULM`.
- Version not in `program_history`: `MACCM, MACCA, MACCT, MACCF, MSHRM`.
- Guide version missing in parsed output: `BSNU, BSSWE_C`.

Likely code-alias crosswalk needed:
- `BSSWE_Java` -> BSSWE (program_history code exists).
- `MSRNNUED` -> MSRNNUEDGR (program_history code exists).
- `MSRNNULM` -> MSRNNULMGR (program_history code exists).
- `MSRNNUNI` -> MSRNNUNIGR / MSRNNUNIFGR (program_history codes exist).
- `BSPRN` -> No direct program_history code; likely related historical code is BSRN.

Judgment: `usable with caveats`.
- Program-side anchoring is strong enough for a bridge artifact, but should include explicit alias/crosswalk and drift flags.

## Part B — Per-Guide Roster Extractability

- AoS roster occurrences available: `2593`.
- SP roster occurrences available: `2568`.
- SP status distribution: `{'usable-with-term': 88, 'usable-no-term': 23, 'unusable': 3, 'partial': 1}`.
- AoS strict unique-attachable rate: `57.81%`.
- SP strict unique-attachable rate: `58.26%`.

Judgment: `strong for prep artifact`.
- We can reliably precompute per-guide course rosters with context and anchorability classing, even before final ambiguous-title resolution.

## Part C — Prep Artifact Proposal

- Recommended artifact path: `data/program_guides/bridge/program_guide_roster_bridge.json`.
- Optional split for scale:
  - `data/program_guides/bridge/index.json`
  - `data/program_guides/bridge/guides/{program_code}.json`
- Structure: one guide record containing metadata + roster rows (`aos` and `sp`) + alignment flags + anchorability fields.

Recommended per-guide fields:
- Guide/program identity: `program_code`, `program_code_effective`, `family`, `disposition`, `sp_status`.
- Guide metadata: `degree_title_guide`, `guide_version`, `guide_pub_date`.
- Program-history linkage: `program_history_status`, `program_history_colleges`, `program_history_degree_headings`.
- Alignment flags: program-history match class, title-heading match class, version match class.
- Roster rows: `surface`, `guide_title_raw`, `guide_title_normalized`, `aos_group`, `sp_term`, `sp_cus`, `anchor_class`, `canonical_candidate_codes`.

Why this helps materially:
- The next long enrichment pull can work from a precomputed roster+anchorability substrate instead of re-running identity and title matching loops.
- It isolates unresolved policy work to explicit buckets (`ambiguous`, `unmapped`, cert/prereq quality classes).

What remains unresolved after bridge build:
- Ambiguous-title disambiguation policy (~31% of occurrences).
- Unmapped-title triage/alias curation (~10-11% of occurrences).
- Certification/prerequisite publish-safety hardening.
- Ongoing maintenance of program-code alias crosswalk.