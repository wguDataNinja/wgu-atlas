# Official Context Layer — Internal Workstream

This folder tracks the work of building Atlas's **Official Context Layer**: a curated inventory of relevant official WGU website pages, matched to Atlas entities (courses, programs, schools, events).

See `_internal/OFFICIAL_CONTEXT_LAYER_PLAN.md` for full strategy and rationale.

---

## Workflow overview

### Phase 1 — Raw sitemap manifest extraction (this phase)

- Source: https://www.wgu.edu/sitemap.html
- Extract all hyperlinks: visible text + URL
- Do NOT inspect or summarize target pages yet
- Do NOT classify deeply yet
- Output: `data/official_context_manifest_phase1.csv` and `.json`
- Status: awaiting manual review before Phase 2

### Phase 2 — Manual review and pruning

- Human reviews the Phase 1 manifest
- Mark each entry: keep / skip / review
- Prune obvious junk: utility links, privacy pages, boilerplate nav
- Identify priority pages for Phase 3 enrichment
- Output: curated review queue

### Phase 3 — Page enrichment pass (expensive)

- For each kept entry: fetch and summarize the target page
- Classify: page_type, official_context_type
- Infer: school_candidates, program_candidates, course_candidates
- Output: `data/official_context_links.csv` and `.json` (enriched)

### Phase 4 — Entity matching

- Compare enriched inventory against Atlas entities
- Identify best attachment points per entity
- Output: matching table for integration

### Phase 5 — Curated surfacing

- Surface 1–3 strong links per relevant entity page
- Label clearly as "Related official WGU resources"
- Never blur catalog facts with official context links

---

## Files in this folder

| File | Purpose |
|---|---|
| `README.md` | This file — workflow overview |
| `DEV_LOG.md` | Durable log for this workstream |
| `REVIEW_QUEUE.md` | Tracks Phase 1 → Phase 2 review status |
