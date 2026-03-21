# Program Guide — No-Use / Internal-Only List

**Date:** 2026-03-21
**Coverage basis:** 115/115 guides parsed (Phase C complete)

This document catalogs all program-guide data elements that should NOT be surfaced in Atlas, along with the rationale and alternative handling.

---

## Hard Exclusions (Do Not Publish)

These items have known quality or reliability issues that make surface use unsafe.

| Item | Guides affected | Why excluded | Alternative |
|------|----------------|-------------|------------|
| BSITM Standard Path | BSITM | Source PDF column extraction failure; SP titles garbled or concatenated | AoS content usable; show AoS only |
| MSCSUG Standard Path | MSCSUG | Source PDF column extraction failure; SP titles concatenated | AoS content usable; show AoS only |
| Prereq mentions as structured data | All 115 | Known false-positive rate in prereq regex; field has not been spot-check validated | Internal reference only; do not surface |
| Guide-sourced degree titles | MSRNNUED, MSRNNULM, MSRNNUNI, MSCSAIML | Truncated in parsed output (cosmetic parser artifact) | Use catalog degree title as primary |
| BSITM competency bullets (1 course) | BSITM | Empty bullet set due to PDF format artifact | Suppress that one course's bullet display |
| BSSWE_C competency bullets (1 course) | BSSWE_C | Empty bullet set due to PDF format artifact | Suppress that one course's bullet display |

---

## Soft Exclusions (Use With Caveat or Delay)

These items have known quality concerns but may be usable with documentation or future fixes.

| Item | Guides affected | Current status | Recommended handling |
|------|----------------|---------------|---------------------|
| BSPRN Standard Path | BSPRN | Pre-Nursing track only (19 courses); 15 Nursing-track courses not in SP | Label SP as "Pre-Nursing Standard Path" if displayed |
| BSNU metadata (version/date/pages) | BSNU | Not recoverable (no footer in source PDF) | Omit version/date/pages fields for BSNU; content intact |
| MACCM "Corporate Financial Analysis" | MACCM | Title/first-sentence quality issue (cosmetic) | Content usable; verify display looks acceptable |
| MEDETID capstone (2 of 3 courses) | MEDETID | Only first of 3 capstone courses parsed | Surface capstone with caveat about partial coverage |
| MAELLP12 page_count | MAELLP12 | page_count=0 (cosmetic, older format) | Omit page_count display for MAELLP12 |
| MSRNNUED/LM/NI degree_title | nursing_rn_msn | Truncated combined-guide title | Use catalog degree title |
| MATSPED Standard Path | MATSPED | SP broken at source (all courses in one concatenated row); AoS intact | Show AoS content only; exclude SP display |

---

## Internal-Only Artifacts

These files are build/pipeline artifacts and should never be published to the public data directory.

| Artifact | Location | Purpose | Why internal |
|----------|----------|---------|-------------|
| `*_parsed.json` | `data/program_guides/parsed/` | Parser output — source-of-truth for content | Phase D build script will produce site-ready format |
| `*_validation.json` | `data/program_guides/validation/` | QA validation reports | Internal QA; not student-facing |
| `*_manifest_row.json` | `data/program_guides/manifest_rows/` | Corpus accounting | Internal corpus metadata |
| Family gate reports + rollout summaries | `data/program_guides/family_validation/` | Session records | Internal build history |
| Enrichment planning artifacts | `data/program_guides/audit/` | Phase D design inputs | Internal planning |

---

## Items Not Yet Ready (Phase E Dependency)

| Item | Why not ready | Blocker |
|------|--------------|--------|
| Course descriptions on course detail pages | Requires title → code matching | Phase E not started |
| Competency bullets on course detail pages | Same Phase E dependency | Phase E not started |
| Per-course cert-prep attributes | Would need structured extraction pass from description text | Requires Phase E + additional extraction |
| Per-course prereq attributes | Known false-positive risk | Requires validation pass + Phase E |

---

## Summary Counts

| Category | Count |
|----------|-------|
| Hard SP exclusions | 2 programs (BSITM, MSCSUG) |
| Hard field exclusions | 3 fields (prereq structured data, 2 empty bullet sets) |
| Soft exclusions / caveats | 7 programs or fields |
| Internal-only artifact types | 5 types |
| Items blocked on Phase E | 4 item types |
