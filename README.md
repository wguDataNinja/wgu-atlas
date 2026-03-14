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

## Disclaimer

WGU Atlas is an independent community project and is not affiliated with Western Governors University. All catalog data is derived from WGU's publicly available course catalog. No proprietary or internal WGU data is used.
