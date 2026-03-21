# Program Guides — Workstream Control

**Module:** Program Guide Content Extraction
**Status:** Initialized — analysis phase, not yet implemented
**Last updated:** 2026-03-20

---

## Purpose

Extract structured content from WGU program guide PDFs (115 guides) and make it available as parsed runtime artifacts for the Atlas site.

This is a content extraction workstream, not a URL-placement workstream. The existing `official_resource_placements.json` already handles guide URLs as sidebar links. This workstream extracts the guide content itself: Standard Path tables, course descriptions, competency bullets, prerequisite mentions, certification prep mentions.

---

## Current status

- Technical readout complete: `_internal/program_guides/TECHNICAL_READOUT.md`
- BSDA.txt already extracted (one of 115)
- All 115 PDFs exist at `/WGU-Reddit/WGU_catalog/program_guides/raw_pdfs/`
- No parsing scripts written yet
- No parsed artifacts yet

---

## Locked decisions

- **Manifest-first approach.** Do not write a content parser before characterizing the full 115-guide corpus. The manifest analysis runs first; parser design is confirmed against it before implementation begins.
- **BSDA is the thin-slice validation case.** First parsed output will be BSDA. Gate: BSDA validates cleanly before scaling to all guides.
- **No course codes in guides.** Course title-to-Atlas-code matching is a separate downstream step, not part of the structural parser.
- **Phase A output gates Phase B.** Do not implement the content parser until the manifest and family classification are complete.

---

## Pipeline phases

| Phase | Name | Status |
|---|---|---|
| A | Corpus understanding (manifest generation) | Not started — text extraction needed for 114 remaining PDFs |
| B | Thin-slice parsing (BSDA) | Not started |
| C | Full corpus parsing | Not started |
| D | Site artifact build | Not started |
| E | Course code matching | Not started |

---

## Scripts to write (in order)

| Script | Purpose | Phase |
|---|---|---|
| `analyze_guide_manifest.py` | Scan all 115 guide texts; produce `guide_manifest.json` and `section_presence_matrix.csv` | A |
| `parse_guide.py` | Per-guide content parser; thin-slice first, then full corpus | B, C |
| `build_guide_site_data.py` | Build runtime artifacts from validated parsed JSONs | D |
| `match_guide_courses.py` | Fuzzy-match guide course titles to Atlas canonical codes | E |

---

## Artifact map

| Artifact | Location | Status |
|---|---|---|
| `guide_manifest.json` | `data/program_guides/` | Planned |
| `section_presence_matrix.csv` | `data/program_guides/` | Planned |
| `guide_family_classification.md` | `_internal/program_guides/` | Planned |
| `irregularities_report.md` | `_internal/program_guides/` | Planned |
| `parseability_report.md` | `_internal/program_guides/` | Planned |
| `BSDA_parsed.json` | `data/program_guides/` | Planned |
| `BSDA_validation.json` | `data/program_guides/` | Planned |
| `BSDA_manifest_row.json` | `data/program_guides/` | Planned |
| `{CODE}_parsed.json` (all) | `data/program_guides/` | Planned |
| `public/data/program_guides/{code}.json` | `public/data/program_guides/` | Planned |

---

## Open questions

| ID | Question | Default if unresolved |
|---|---|---|
| Q-PG-001 | Do endorsement (END*) and PMC guides follow the standard structure or are they abbreviated? | Treat as unknown until manifest analysis confirms |
| Q-PG-002 | Do nursing guides (MSN*, BSPRN, BSNU) have clinical-specific sections not present in standard guides? | Treat as unknown until manifest confirms |
| Q-PG-003 | Do track-variant guides (MSDADE, BSSWE_Java, etc.) have a "track supplement" structure rather than a standalone full guide? | Treat as unknown until manifest confirms |
| Q-PG-004 | Does the course title → Atlas code matching yield acceptable coverage without manual intervention? | Unknown until matching phase runs |
| Q-PG-005 | What is the correct runtime attachment model for parsed guide content on program pages? | Defer until Phase C completes |

---

## Next bounded step

Extract the remaining 114 guide PDFs to text (using `pdftotext` or equivalent). Commit all texts to `raw_texts/`. Then write `analyze_guide_manifest.py`.

See `TECHNICAL_READOUT.md` for full design rationale and schema.
