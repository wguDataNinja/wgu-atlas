# Program Guide Enrichment — Final Recommendation Memo

**Date:** 2026-03-21
**Author:** Atlas data pipeline
**Basis:** Phase C complete (115/115 guides parsed)

---

## What Just Happened

Phase C of the program-guide extraction pipeline is complete. Every WGU program guide in the corpus (115 guides across 19 families) now has three on-disk artifacts:
- `*_parsed.json` — structured course, description, and competency data
- `*_validation.json` — quality report with confidence level
- `*_manifest_row.json` — corpus-accounting row

The corpus contains:
- **2,593 course entries** across 115 programs, each with a full course description
- **2,591 competency bullet sets** (99.9% coverage)
- **2,568 Standard Path course-term rows** for 113 programs
- **96 HIGH confidence** guides (83.5%), **17 MEDIUM** (14.8%), **2 LOW** (1.7%)

This is the richest structured per-program data Atlas has produced. No comparable source exists in the current product.

---

## Recommended Rollout Sequence

### Phase D: Program-Page Enrichment (Next)

**What:** Build a `public/data/program_guides/` directory of site-ready artifacts, one JSON per program, containing the fields ready for Atlas program pages.

**Scope:** 113 programs with usable SP + 115 programs with usable AoS content.

**Schema recommendation for each published artifact:**
```json
{
  "program_code": "BSCS",
  "version": "202412",
  "pub_date": "...",
  "standard_path": [
    { "title": "...", "cus": 3, "term": 1 }
  ],
  "areas_of_study": [
    {
      "group": "Core",
      "courses": [
        {
          "title": "...",
          "description": "...",
          "competency_bullets": ["..."]
        }
      ]
    }
  ]
}
```

**Quality gate:** Include HIGH + MEDIUM guides. Exclude SP for BSITM, MSCSUG, MATSPED (AoS still included). See `enrichment_no_use_list.md` for full exclusion catalog.

**Build approach:** A script reads `data/program_guides/parsed/` + `data/program_guides/validation/`, applies the exclusion policy, and writes `public/data/program_guides/{CODE}.json` for each eligible program.

**Site wiring:** Program detail pages (`/programs/{code}`) read the guide artifact if present. If absent (BSITM SP, etc.), the program page degrades gracefully to the current catalog display. Guide content supplements the current display; it does not replace it.

**Risk:** Low. Guide data is additive — it enriches existing pages without changing the underlying catalog data model. No route changes, schema changes to core data, or breaking changes.

---

### Phase E: Course-Page Enrichment (After Phase D)

**What:** Build a course-code → description mapping by matching guide-extracted course titles to Atlas course codes.

**Why it matters:** Descriptions and competency bullets become available on individual course pages (`/courses/{CODE}`), not just on program pages.

**Estimated yield:** ~700–900 distinct Atlas courses gaining descriptions and competency bullets.

**Risk:** Medium. Title matching introduces potential for mismatches. Gate test on a sample is required before full-corpus run.

**Dependency:** Phase D must be live first. Phase E adds an additional enrichment layer on top of Phase D.

---

## What to Do Right Now

1. **Design Phase D schema** (one session): Define the exact output format, the build script logic, and the inclusion/exclusion policy. Validate against 5–10 sample programs.

2. **Build Phase D script** (one session): Write `scripts/program_guides/build_guide_artifacts.py`. Run on full corpus. Spot-check 10 programs.

3. **Wire Phase D to program pages** (one session): Add guide-data display to `/programs/{code}`. Decide UI treatment (standard path table, AoS group sections, competency bullets collapsed by default).

---

## Risk Summary

| Risk | Level | Mitigation |
|------|-------|-----------|
| Phase D build introduces regressions to program pages | Low | Guide data is additive; existing catalog data unchanged |
| SP data wrong for BSITM / MSCSUG | None | Hard-excluded from SP output |
| MEDIUM-confidence guides producing incorrect content | Low | All MEDIUM guides were manually reviewed; content issues are structural (missing metadata, dual-track SP), not content quality |
| Guide descriptions outdated (guide version ≠ current catalog) | Medium | Version fields available for most guides; date comparison with catalog version possible |
| Phase E title-matching errors | Medium | Gate test on sample required; fuzzy-matching with manual review of non-matches |

---

## Key Numbers to Carry Forward

| Metric | Value |
|--------|-------|
| Guides ready for Phase D (AoS) | 115/115 |
| Guides ready for Phase D (SP) | 113/115 |
| Guides excluded from SP display | 3 (BSITM, MSCSUG, MATSPED) |
| Course descriptions available | 2,593 |
| Competency bullet sets available | 2,591 |
| SP course-term rows | 2,568 |
| Families fully validated | 18 + education_grad |
| Families with any LOW-confidence guide | 2 (standard_bs: BSITM LOW; cs_grad: MSCSUG LOW) |
