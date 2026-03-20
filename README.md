# WGU Atlas

**Explore courses, programs, catalog changes, and student discussion**

WGU Atlas is a public-facing reference and explorer built from the validated WGU public catalog archive. It tracks course and program history across 108 catalog editions spanning 2017 through 2026, with a timeline of major catalog events and (planned) student discussion context layered on top.

*Created by WGU-DataNinja*

---

## What's here

| Section | What it does |
|---|---|
| **Course explorer** | Browse and filter all 1,646 courses (active, retired, and certificate) |
| **Course pages** | Per-course history: all observed titles, program memberships, and edition coverage |
| **Timeline** | Chronological view of major catalog events — school reorganizations, mass course changes, program additions |
| **Data** | Download the canonical course and event datasets |
| **Methods** | How the data was collected, validated, and interpreted |

---

## Data provenance

All catalog data is derived from the official WGU public course catalog, scraped and parsed across 108 editions (2017-01 through 2026-03). Three editions are missing from the archive (2017-02, 2017-04, 2017-06).

The underlying archive and parser live in a separate internal research repository. This repo contains only the pre-generated site-ready data artifacts.

Key facts about the current data layer:
- **838** active AP course codes (2026-03 baseline)
- **52** active certificate codes
- **114** program body blocks
- **1,646** total course codes (active + retired + cert)
- **41** named catalog events

---

## Data separation policy

WGU Atlas maintains a hard boundary between:

- **Official catalog facts** — what appears in the public WGU catalog
- **Discussion signals** — Reddit and community data (planned feature layer)
- **LLM-generated content** — clearly labeled where used

These are never mixed in the same data field or presented without attribution.

---

## Tech stack

- [Next.js](https://nextjs.org/) + TypeScript
- [Tailwind CSS](https://tailwindcss.com/)
- Static/data-driven architecture
- Deployed via GitHub Pages + GitHub Actions

---

## Repo structure

```
wgu-atlas/
├── public/data/            # Site-ready JSON (consumed by the frontend)
│   ├── courses.json        # 1,646 course cards
│   ├── events.json         # 41 named events
│   ├── search_index.json   # Client-side search index
│   ├── homepage_summary.json
│   └── courses/            # 838 individual course detail files
├── data/                   # Canonical artifacts (downloadable datasets)
│   ├── canonical_courses.csv
│   ├── canonical_courses.json
│   ├── named_events.csv
│   └── ...
├── docs/                   # Reference documentation (data layer provenance)
├── scripts/                # Build script to regenerate data artifacts
├── src/                    # Next.js site source
└── _internal/              # Internal working docs (not public-facing)
```

---

## Course code confidence

### What we did

- **108 catalog editions** scraped and parsed (2017-01 through 2026-03), covering every program roster across that span
- **Cross-referenced two independent sources:** the edition history and the 2026-03 catalog snapshot; any code missing from the snapshot is flagged retired rather than silently dropped
- **Internal consistency check:** every course code appearing in active program rosters (`program_enriched.json`, scraped from catalog program pages) is present in `canonical_courses.csv` — zero gaps found
- **Per-code trust signals** computed and stored: `ghost_flag`, `single_appearance_flag`, `stability_class`, `current_title_confidence`, `title_variant_class` — each row carries its own confidence indicator rather than a single dataset-wide claim
- **Known truncation and extraction artifacts** manually identified and overridden for affected codes

### Honest assessment

This dataset is **comprehensive for what the scraper saw** but cannot guarantee it saw everything. Structural blind spots remain:

- **Certificate codes only tracked from 2024-09 forward** — cert courses that existed earlier or under different structures may not appear
- **Courses not in any program roster** — if a course exists only as a standalone page the scraper never visited, it would be absent from the entire universe
- **Post-2026-03 additions** — nothing added after the last scrape run is present
- **No independent external cross-check** — there is no WGU API or authoritative public course list to validate against

### Human review path

The most practical completeness check is section-by-section human review. As course codes surface from student discussion or other sources, they can be spot-checked against the dataset:

| What to check | How |
|---|---|
| Is a code in the dataset at all? | Search `canonical_courses.csv` or `canonical_courses.json` by `course_code` |
| Is it marked active? | `active_current = True` and `stability_class` not `single` or `ghost_flag = False` |
| Does the title look right? | Compare `canonical_title_current` against what students actually call it |
| Is it flagged uncertain? | `current_title_confidence = low` or `title_variant_class = unresolved` means manual review was deferred |

Any code that appears in student posts but is absent from the dataset is a genuine discovery worth adding. Over time, community-sourced codes are the most reliable signal for catching what the scraper missed.

---

## Disclaimer

WGU Atlas is an independent community project and is not affiliated with Western Governors University. All catalog data is derived from WGU's publicly available course catalog. No proprietary or internal WGU data is used.





