# Program Guide — No-Use / Internal-Only List

**Date:** 2026-03-21

## Hard Exclusions (Do Not Publish)

| Item | Why excluded | Alternative |
|---|---|---|
| BSITM `standard_path` | Source PDF column extraction failure — SP unusable | Show AoS content only |
| MSCSUG `standard_path` | Source PDF column extraction failure — SP unusable | Show AoS content only |
| MATSPED `standard_path` | SP broken at source (all courses in one concatenated SP row) | Show AoS content only |
| all guides `prerequisite_mentions` | Known false-positive rate in prereq regex; not spot-check validated | Internal reference only |
| BSITM `competency_bullets` | Empty bullet set — PDF format artifact | Suppress that course's bullet display |
| BSSWE_C `competency_bullets` | Empty bullet set — PDF format artifact | Suppress that course's bullet display |
| MSRNNUED,MSRNNULM,MSRNNUNI,MSCSAIML `degree_title` | Truncated in parsed output | Use catalog degree title |

## Soft Exclusions / Caveats

| Item | Current status | Handling |
|---|---|---|
| BSPRN `standard_path` | Pre-Nursing track only; 15 Nursing-track courses AoS-only | Label as 'Pre-Nursing Standard Path' if displayed |
| BSNU `metadata` | version/pub_date/page_count unavailable | Omit those fields; content intact |
| MACCM `description` | Corporate Financial Analysis title/first-sentence quality issue (cosmetic) | Verify display looks acceptable |
| MEDETID `capstone` | Only first of 3 capstone courses captured | Surface with partial-coverage caveat |
| MAELLP12 `page_count` | page_count=0 (cosmetic) | Omit page_count display |

## Internal-Only Artifacts

- `data/program_guides/parsed/*_parsed.json`: Phase D build will produce site-ready format
- `data/program_guides/validation/*_validation.json`: Internal QA artifacts
- `data/program_guides/manifest_rows/*_manifest_row.json`: Internal corpus metadata
- `data/program_guides/family_validation/`: Internal build history
- `data/program_guides/audit/`: Internal planning artifacts

## Phase E Dependencies

- Course descriptions on course detail pages
- Competency bullets on course detail pages
- Per-course cert-prep attributes (structured)
- Per-course prereq attributes (structured)
