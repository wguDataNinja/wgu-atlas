# Official Context Layer — Dev Log

Internal log for the official-context workstream.
Record durable decisions, phase completions, review notes, and blockers.
Do not turn this into a transcript.

---

## 2026-03-14 — Phase 1: Raw sitemap manifest extraction

### What was done

- Created `_internal/official_context/` folder with README, DEV_LOG, REVIEW_QUEUE
- Fetched https://www.wgu.edu/sitemap.html
- Extracted 806 raw hyperlinks
- Filtered: removed portal links, logo links, blank anchors, fragment anchors → 797
- Deduplicated by URL → **604 unique entries**
- Wrote raw Phase 1 manifest to:
  - `data/official_context_manifest_phase1.csv`
  - `data/official_context_manifest_phase1.json`

### Phase 1 rules applied

- Captured: visible link text + URL
- Excluded: non-links, blank/empty links, fragment-only anchors, apply portal, obvious logo/nav links
- Did NOT inspect target pages
- Did NOT summarize target pages
- Did NOT classify deeply
- All other manifest fields left blank for human review

### Manifest counts and patterns observed

| Category | Approx. count |
|---|---|
| Financial aid / tuition / scholarships | ~145 |
| IT school program pages | ~88 |
| Program guide HTML pages | ~94 (84 standard + 10 variant) |
| Business school program pages | ~73 |
| Health/nursing program pages | ~73 |
| Teaching school program pages | ~56 |
| About WGU pages | ~32 |
| Admissions | ~18 |
| Other (root, alumni, landing, etc.) | ~25 |

Notable: **zero PDFs found directly in the sitemap** — program guides are HTML pages (`/program-guide.html`), not PDF links. PDF program guides may be linked from within those pages (Phase 2 will surface them).

Newsroom coverage is sparse (only ~1-2 entries from sitemap). Blog/newsroom content may need a separate discovery pass.

### Status

Phase 1 extraction complete. Awaiting manual review before Phase 2 enrichment.

### Cleanup issues to expect before Phase 2

1. **Financial aid / scholarships bloat** — ~145 entries in the financial-aid-tuition path. Most are scholarship eligibility pages or state-specific aid info. These are real pages but unlikely to be entity-relevant. Flag as low-priority in review.
2. **Generic "Program Guide" titles** — 94 program guide entries all have the same or similar title ("Program Guide"). The URL disambiguates them, but the title field will need enrichment in Phase 2.
3. **Duplicate program entries at different depth levels** — e.g., a program overview page + its variants (MAT vs MA) all appear. Correct behavior for Phase 1; prune or consolidate in review.
4. **Phone number URL** — one entry has a tel: link (`866.225.5948`). Should be pruned in review.
5. **Newsroom under-coverage** — sitemap has minimal newsroom links. Newsroom discovery should be a separate Phase 2+ task.

### Next steps

- Human reviews `data/official_context_manifest_phase1.csv`
- Mark each row: keep / skip / maybe
- Prune: financial aid bloat, utility pages, phone links, duplicates
- Keep: program pages, program guides, school pages, about pages, career/comparison pages
- Then proceed to Phase 2: page fetch and enrichment pass

---

## 2026-03-14 — Phase 2 test enrichment pass (15 entries)

### What was done

- Selected 15 high-value entries from Phase 1 manifest (program guides, outcomes pages, specialization subpages, accreditation pages — all 4 schools represented)
- Fetched each page and enriched all blank fields
- Wrote incrementally to `data/official_context_manifest_phase2_test.json` (15 entries, all `keep=yes`)

### Key findings (see PHASE2_TEST_NOTES.md for full detail)

- All 15 URLs active — no broken or redirected pages
- All program guide pages confirmed downloadable PDF links on the HTML page
- `outcomes.html` pages are rich: structured competency data, assessment tables, pass rates
- Specialization subpages are more substantive than guide pages
- Accreditation pages vary: school-level (ACBSP/CAEP) vs program-specific (CAHIIM)
- URL pattern alert: `successful-student-learning-outcomes.html` = accreditation page, not outcomes page
- `school_candidates` can be auto-assigned from URL path prefix — no page fetch needed

### Status

Phase 2 test complete. Workflow validated. Schema holds cleanly.
Ready to plan scope for full enrichment pass.

---

## 2026-03-15 — Phase 2 partial enrichment pass (session cut short — quota)

### What was done

- Template-enriched all 107 program guide pages using parent-title lookup from Phase 1 manifest (no fetches required — all parent titles resolvable)
- Combined with 15 fetched entries from Phase 2 test → **122 entries total** written to `data/official_context_manifest_phase2_test.json`
- Launched background agent to fetch remaining 262 entries; agent was stopped early to preserve quota

### Current file state: 122 entries

| page_type | count | method |
|---|---|---|
| `program_guide_page` | 115 | 8 fetched + 107 template-enriched |
| `accreditation_page` | 3 | fetched |
| `outcomes_page` | 2 | fetched |
| `program_subpage` | 2 | fetched |

### Remaining work (262 entries not yet enriched)

These are identified in `/tmp/phase2_batch.json` and should be processed next session:

| category | count | notes |
|---|---|---|
| `accreditation` | 1 | CAE-CDE Program Designation (CSIA) |
| `specialization` | 123 | 20 stackable cert pages + 103 track/variant/endorsement pages |
| `school_page` | 138 | Main program landing pages (Business: 43, Education: 36, Health: 36, Technology: 23) |

### Batch list saved durably

The 262-entry remaining batch has been saved to `_internal/official_context/phase2_remaining_batch.json` — this survives reboots. At session start, filter this list against already-done URLs in `phase2_test.json` to get the true remaining set.

### Recommended next session approach

Do NOT re-run a single large 262-page agent. Instead:
1. Process the 1 accreditation entry manually (fast)
2. Process specialization pages in sub-batches of 20-30
3. Process school/program pages in sub-batches of 20-30
4. Write after each sub-batch to preserve progress

### Status

Paused. 122/384 target entries enriched. Safe to resume next session.
