# Official Context Layer — Review Queue

This file tracks the manual review status between Phase 1 and Phase 2.

---

## Current status

**Phase 1 complete — awaiting manual review**

The raw Phase 1 manifest is ready for human review at:
- `data/official_context_manifest_phase1.csv`
- `data/official_context_manifest_phase1.json`

## What to do in manual review

Open `data/official_context_manifest_phase1.csv` and for each row:

1. Set `keep` = `yes` / `no` / `maybe`
2. Add notes if anything looks interesting or surprising
3. Set `page_type` if it's obvious from the URL/title
4. Flag PDF links for separate handling

## Things to prune (set keep=no)

- Obvious utility/legal pages: privacy policy, accessibility, terms of use, contact forms
- Login/portal links
- Generic navigation targets (e.g. `/about/`, `/contact/`)
- Empty or duplicate entries
- News/blog pages with no clear entity relevance (keep if they mention programs or schools)

## Things to keep (set keep=yes or maybe)

- Program pages
- Program guide pages
- Program guide PDFs
- School/college pages
- Newsroom articles about programs, schools, or significant WGU changes
- Certification advice pages
- Career/pathway explainers
- Comparison articles

## After review

Update this file with:
- total kept / skipped / maybe counts
- notable patterns or surprises
- any new candidate pages discovered during review
- ready-for-Phase-2 confirmation

Then proceed to Phase 2: page fetch and enrichment pass.
