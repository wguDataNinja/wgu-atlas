# Official Context Layer — Phase 2 Test Notes

This file captures findings from the Phase 2 enrichment test pass.

Test completed: 2026-03-14
Test batch size: 15 entries
Source: `data/official_context_manifest_phase1.json` (604 entries)
Output: `data/official_context_manifest_phase2_test.json`

---

## Test batch composition

| Type | Count | Examples |
|---|---|---|
| `program_guide_page` | 8 | B.S. CS, B.S. CSIA, Java Track, B.S. Data Analytics, M.S. Data Analytics (Decision Process Engineering), B.S. Business Management, MSN-FNP, M.A. Science Ed |
| `outcomes_page` | 2 | B.S. CS Outcomes, B.S. CSIA Outcomes |
| `program_subpage` | 2 | Data Science Specialization (M.S. Data Analytics), AI Engineering Specialization (M.S. SE) |
| `accreditation_page` | 3 | ACBSP (Business), CAHIIM (Health Info Mgmt), CAEP (Education) |

All 15 pages: `keep=yes`, `status=active`. No broken or redirected URLs.

---

## Workflow validation

The enrichment workflow is validated. The schema holds cleanly. No new fields are needed for the test entries.

Process per entry:
1. Fetch page with WebFetch
2. Read content
3. Fill in all blank fields
4. Update descriptive title when original was generic ("Program Guide")
5. Write to `phase2_test.json` immediately

---

## Key findings

### Program guide pages are thin wrappers

All 8 program guide pages follow the same pattern:
- Breadcrumb nav
- Apply Now / Request Info CTAs
- "Download PDF" link to the actual guide document
- Minimal curriculum content on the HTML page itself

**Implication:** These pages are valid to keep as `program_guide` entries and link to from Atlas program pages. The PDF is the real artifact — but the HTML page is the canonical landing point for it.

**For full pass:** When enriching program guide pages, note the PDF filename in `notes` if visible.

### Outcomes pages are rich

The two outcomes pages (`outcomes.html`) contain structured data:
- Program learning outcomes with competency codes (ABET CAC-style for CS)
- Assessment result tables and multi-year charts
- Student satisfaction and retention metrics
- Pass rate data

These are high-value for Atlas entity enrichment. All `outcomes.html` pages should be `keep=yes`.

### Specialization/variant subpages are substantive

The `program_subpage` entries (Data Science specialization, AI Engineering specialization) contain full curriculum listings, career paths, salary data, and admission requirements — much richer than guide pages.

**Implication:** These are higher-value than program guide pages for Atlas course/program enrichment. Should be prioritized.

### Accreditation pages vary by scope

| Page | Scope | Notes |
|---|---|---|
| ACBSP (Business) | School-level | Covers all Business programs |
| CAEP (Education) | School-level | Covers all Education programs |
| CAHIIM (Health Info Mgmt) | Program-specific | B.S. HIM only; also covers RHIA/RHIT exam eligibility |

**Implication:** School-level accreditation pages → attach to school page, not individual program pages. Program-specific accreditation → attach to the specific program page.

### URL pattern alert: `successful-student-learning-outcomes.html`

Two entries use the path `/successful-student-learning-outcomes.html` — one under Business, one under Education. Despite the URL suggesting "outcomes," these are actually **accreditation pages** (ACBSP and CAEP), not per-program outcomes pages.

**For full pass:** Flag all `successful-student-learning-outcomes.html` entries as `accreditation_page`, not `outcomes_page`.

### Title enrichment worked well

Generic titles like "Program Guide" were successfully updated to descriptive titles like:
- "B.S. Computer Science Program Guide"
- "B.S. Software Engineering (Java Track) Program Guide"
- "M.S. Data Analytics – Decision Process Engineering Program Guide"

This is essential for Phase 2 — the manifest will be much more legible with real titles.

---

## school_candidates assignment was straightforward

| URL prefix | school_candidates |
|---|---|
| `online-it-degrees/` | Technology |
| `online-business-degrees/` | Business |
| `online-nursing-health-degrees/` | Health |
| `online-teaching-degrees/` | Education |

This can be inferred automatically in the full pass from the URL path segment.

---

## Recommendations for full enrichment pass

1. **Auto-assign school_candidates from URL path** — derive from the first path segment. No need to fetch the page for this field.

2. **Flag all `program-guide.html` URLs as `program_guide_page` / `program_guide` without fetching** — their structure is consistent. Fetch only to confirm PDF availability and get the real program name.

3. **Prioritize `outcomes.html` pages** — they are the richest per-page and most useful for entity context.

4. **Prioritize specialization/variant subpages** — richer than guide pages.

5. **School-level accreditation pages** → attach to school entities, not individual programs.

6. **Program-specific accreditation pages** (like CAHIIM) → attach to specific program entity.

7. **Newsroom pages will need a separate discovery pass** — the sitemap has almost no newsroom links. Newsroom content is a separate enrichment track.

---

## Status

Phase 2 test complete. Workflow validated. Ready to plan the full enrichment pass scope.

Next step: decide how many of the 604 Phase 1 entries to run through full Phase 2 enrichment, and in what priority order.
