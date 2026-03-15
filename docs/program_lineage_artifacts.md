# Program Lineage Artifacts

## Why this exists

WGU Atlas needs a high-recall review layer for logical program transitions that matter to students, including:

- successor or replacement
- split
- merge
- namespace or family migration
- specialization expansion

This layer is intentionally broader than finalized site content. It is meant for LLM/HITL review and curation.

## Why `named_events` is not the recall base

`data/named_events.csv` is a thresholded summary layer for notable change moments. It is useful for timeline storytelling, but it is not exhaustive by design.

For lineage detection, thresholded event selection can miss low-volume or localized program churn. To maximize recall, lineage artifacts should be derived from:

- `data/program_history.csv` (program lifecycle base)
- exhaustive adjacent edition boundaries (non-thresholded)

## Artifact roles

### `data/program_transition_universe.csv`

Purpose: exhaustive churn context across all adjacent catalog edition boundaries.

Properties:

- one row per adjacent edition boundary
- non-thresholded
- includes every same-boundary add/remove event from program history
- includes helper context (titles, colleges/schools, CU values)

This is the recall backbone for later lineage reasoning.

### `data/program_link_candidates.json`

Purpose: review artifact for lineage triage.

Properties:

- derived from `program_history` + transition universe boundaries + program course rosters
- includes both:
  - `boundary_reviews` (one review object per churn boundary)
  - `candidates` (plausible pair/group lineage candidates)
- pair/group candidates include overlap evidence using literal course-code sets:
  - removed program last roster (`start_edition`)
  - added program first roster (`end_edition`)
- transition guesses are conservative (`successor`, `split`, `merge`, `namespace_migration`, `family_restructure`, `ambiguous`)
- includes evidence notes and `review_status: "unreviewed"` for downstream triage

This artifact is still recall-oriented, but pairwise noise is reduced by suppressing implausible direct pairings that have no meaningful signal.

## Course overlap signal

`overlap_metrics` is a core lineage-validation signal in each candidate:

- `removed_course_count`
- `added_program_course_count`
- `shared_course_count`
- `courses_removed_count`
- `courses_added_count`
- `old_retained_pct`
- `new_inherited_pct`
- `jaccard_overlap`
- `shared_course_codes`
- `removed_only_course_codes`
- `added_only_course_codes`

Overlap is literal by course code only (no inferred course renames/replacements in this phase).

## Generator

Script:

- `scripts/build_program_lineage_artifacts.py`

Roster source used by the generator:

- `WGU_catalog/outputs/program_names/*_program_blocks_v11.json`
- `WGU_catalog/data/raw_catalog_texts/catalog_YYYY_MM.txt`

Default behavior:

- full historical backfill
- editions from `2017-01` through `2026-03`
- excludes missing archive months: `2017-02`, `2017-04`, `2017-06`

Outputs:

- `data/program_transition_universe.csv`
- `data/program_link_candidates.json`

## Full vs incremental refresh

### Full regenerate (backfill or re-baseline)

```bash
python3 scripts/build_program_lineage_artifacts.py \
  --catalog-root /path/to/WGU_catalog
```

### Incremental candidate refresh

Use the last reviewed catalog edition as a baseline cutoff:

```bash
python3 scripts/build_program_lineage_artifacts.py \
  --catalog-root /path/to/WGU_catalog \
  --baseline-end-edition YYYY-MM
```

When `--baseline-end-edition` is set, only boundaries with `end_edition` later than the baseline are emitted. This keeps future review scoped to newly introduced transition candidates while preserving the option to rerun full history at any time.

## Next artifact (future)

After review confirms lineage links, a second artifact can be generated for public-facing pages with focused course-list deltas (retained/removed/added) for confirmed transitions only.
