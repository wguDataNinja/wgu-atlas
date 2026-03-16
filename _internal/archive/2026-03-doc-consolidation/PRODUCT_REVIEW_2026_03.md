# WGU Atlas — Product Direction Review
*2026-03-14 · Internal memo*

---

## Context

This review responds to a product direction shift: the site should lead with **useful catalog-backed information about courses and programs**, not with the change-history/event layer. The event/timeline layer remains valuable but should be secondary.

This memo answers six questions using direct inspection of the catalog text, extracted data artifacts, and current UI state.

---

## 1. What is already extracted but not yet surfaced on the site?

### Credit Units (CUs) — high value, zero new work

**`canonical_cus`** is present in every individual course detail file (`public/data/courses/{code}.json`) and every row of `canonical_courses.csv`. **CUs are not shown anywhere in the current UI.**

- All 838 active AP courses have a CU value
- Distribution: 3 CUs = 537 courses (64%), 4 CUs = 117, 2 CUs = 135, 1 CU = 22, 5–8 CUs = 26, 50 CUs = 1 (the outlier: PFIT portfolio)
- CU history is tracked: `cus_values` in `program_history.csv` can show when a course's CU value changed across editions

This is probably the single most useful fact a prospective student wants about a course. It is already extracted. It just needs to be added to the course card and course detail page.

### Stability classification — extracted, minimally surfaced

`stability_class` (perpetual / stable / moderate / ephemeral / single) is in the course detail files and `canonical_courses.csv`. The course detail page shows it. The course explorer does not surface it as a visible column or meaningful filter.

For students evaluating a course, "this course has been stable across all 108 editions" or "this course appeared in only one edition" is genuinely informative. It should be a visible badge on course cards, not just a filter field.

### `historical_program_count` and `current_program_count` — shown as raw numbers, not contextualized

The course detail page shows these two numbers. What it does not show is *what those numbers mean*. A course in 70 historical programs (like C455 / English Comp I) used to be a general education requirement across the catalog. That context is informative and completely derivable from existing data.

### College history — extracted, partially surfaced

`colleges_seen` is in the detail files and shown as small chips on the course page. This is fine, but the sequence isn't shown. A course that moved from `College of Business` → `School of Business` is just a rename; a course that moved from `Teachers College` to `School of Technology` is a genuine reassignment. The change currently looks identical in the UI.

### Program version progression — extracted, not surfaced at all

`program_history.csv` has full version progression for all 196 programs (active + retired), including:
- `version_progression`: a human-readable date series like `2018-07:201808 → 2020-07:202007 → 2023-07:202308`
- `version_changes`: count of version bumps
- `cus_values`: whether the total CU count for the program changed
- `colleges`: which schools the program has lived under

None of this is surfaced on the site. There are no program pages yet.

### Search index includes programs — not linked

`search_index.json` has 196 program entries alongside the 1,646 course entries. A search for "accounting" will surface programs and courses. But programs have no destination page. Searching for a program name returns a dead search result.

---

## 2. What is in the catalog but not yet extracted?

### Program descriptions — high value, clearly bounded, easy to parse

Every program body block in the catalog contains a description paragraph between the degree heading and the `CCN Course Number` header. A quick probe of the 2026-03 catalog extracted ~110 description blocks.

Sample:
> *"The Bachelor of Science in Human Resource Management is a competency-based program that prepares graduates for a variety of careers in the fields of human capital management and people and talent..."*

These descriptions:
- Are well-bounded (heading line → CCN header)
- Are present in ERA_B catalogs (confirmed 2024-08 through 2026-03)
- Are likely present in most ERA_A editions as well, though format consistency needs verification
- Are 2–5 sentences, useful as program summary text
- Are the most direct answer to "what is this program?"

**Status: not yet extracted. Requires new parsing work (bounded, moderate difficulty).**

### Program learning outcomes — high value, clearly bounded, easy to parse

The `Program Outcomes` section (lines 7636–13361 in 2026-03) contains per-program bullet-point learning outcomes. A quick probe found **85 program blocks and 586 outcome bullets**.

Sample (B.S. Accounting):
- *"The graduate explains the processes and controls for the revenue, expenditure, and general ledger transaction cycles used in business information systems."*
- *"The graduate interprets the statement of cash flows in accordance with generally accepted accounting principles (GAAP)."*

These are:
- Already bounded in the catalog (Program heading → next Program heading)
- High-quality, WGU-authored competency statements
- Present only in ERA_B catalogs (section appeared 2024-09+)
- Not available historically, but current state is fully parseable

For a prospective student evaluating a program, "here is what you will be able to do when you graduate" is exactly what they want to know. This is currently on WGU's own site but not easily comparable, searchable, or cross-referenceable.

**Status: not yet extracted. Requires new parsing work (well-bounded, straightforward).**

### Certificate descriptions — medium value, already partially structured

Each of the 16 certificate programs in the `Certificates - Standard Paths` section (lines 14566–14780) has a 3–5 sentence description. These are already well-bounded (`Certificate: [Name]` → CCN header). The cert section parser already exists; descriptions just aren't being captured.

Sample (Accounting Fundamentals):
> *"For students who aspire to such a career, the courses in this certificate will provide the required knowledge. In addition, students will earn the Intuit QuickBooks Certified User Online credential..."*

**Status: not yet extracted. Requires minor extension of the existing cert parser.**

### Course term sequence — useful for students, not extracted

The catalog shows each course's term number (1–6+) within a program. This is currently **extracted per edition but thrown away** — the parser captures course rows but does not retain the term field.

Term sequence tells a student "this is a first-semester course in this program" vs "this is a senior-year capstone." For a student evaluating whether a course is foundational or advanced, this is useful signal.

This is moderately complex to surface correctly because:
- Term values are per-program, not per-course
- The same course (C455 English Comp I) appears in different terms in different programs
- A useful surface might be "in the Accounting program, appears in term 1"

**Status: data in catalog, not extracted. Requires parser change and new data model.**

### School/College tenets — low-to-medium value, easy to parse

Each of the four schools has a named "Tenets:" block — 4–5 bullet points describing the school's stated educational values and focus areas. These appeared formally starting around 2020-11, and are present and consistent in all ERA_B editions.

Example (School of Business):
- *Impact: We are a global force for good; our shared purpose is to improve the lives of people and society through a transformative business education that emphasizes sustainability and ethical action.*
- *Student Success: We optimize student attainment across a diverse array of learner populations by personalizing learning experiences, building relationships, and customizing support.*

These could populate a school/college context page. They are marketing-adjacent but they are official catalog text, not inferred.

**Status: not extracted. Easy to parse; bounded by `"School Name Tenets:"` header and bullet list.**

### Instructor directory — lower priority, separate scope

Lines 13362–14565 contain an instructor directory structured as `Last, First; Degree, University` entries grouped by department. This already has a separate internal pipeline (`instructor_directory/`) and is explicitly scoped out of wgu-atlas v1.

---

## 3. Classification by effort

| Information | Status | Effort |
|---|---|---|
| Credit Units (CUs) per course | **Already extracted** | UI-only: add to card + detail page |
| Stability class as visible badge | **Already extracted** | UI-only: add to course card |
| Program version history | **Already extracted** (program_history.csv) | Needs program pages + `build_site_data.py` extension |
| Program descriptions | **Not extracted** | New parser work — moderate (well-bounded) |
| Program learning outcomes | **Not extracted** | New parser work — moderate (bounded, ERA_B only) |
| Certificate descriptions | **Not extracted** | Minor parser extension |
| Course term-in-program | **Not extracted** | Moderate parser change + data model design |
| School tenets | **Not extracted** | Easy parser work |
| College lineage with sequence | **Already extracted** | Minor UI improvement |
| Program → site-ready JSON | **Partially built** (program_history.csv) | Moderate scripting (build_site_data.py extension) |
| Instructor directory | In separate pipeline | Out of scope for v1 |

---

## 4. What to surface next, by page

### Course pages — the flagship, needs two immediate additions

**Add now (no new data work):**
1. **Credit units** — show CUs prominently near the course title. "3 CUs" is the first thing a student wants to know. It is already in the detail file.
2. **Stability badge upgrade** — surface `stability_class` as a meaningful, legible label with a tooltip explaining what it means (e.g., "Perpetual — present across all 108 catalog editions").

**Add soon (needs program page to exist first):**
3. Link from current_programs and programs_timeline entries to program detail pages once those exist.

**Defer:**
4. CU change history over time (interesting, low immediate demand).
5. Reddit discussion signals (v1.1).

### Program pages — the biggest gap right now

Program pages don't exist. This is the most significant missing surface. `program_history.csv` already contains enough to build a useful first version:

- Program name, school, first/last seen, active/retired
- Version count and progression (with dates)
- Total CU value (and whether it changed)
- School lineage (college names over time)

What program pages would immediately enable:
- Search results for programs actually lead somewhere
- Course detail pages can link to programs that contain the course
- Students can answer "how has this program changed since I started?"

The missing piece for richer program pages is **the program description** and **learning outcomes**, which require new parsing. But a v1 program page using only existing data would already be highly useful.

**Recommended order:**
1. Build program pages from existing `program_history.csv` data
2. Add program descriptions from new parsing (second pass)
3. Add learning outcomes (third pass)

### Homepage — modest additions needed

The homepage modules are currently driven by the change/event layer (newest programs, recent course additions, recent version changes). These are fine but opaque without context.

**Add:**
- A CU count or "active courses by CU weight" breakdown (useful orientation fact — e.g., "537 of 838 active courses are 3-credit courses")
- A link module for the four schools that goes to the school page (not just the course explorer filtered by school)

**Do not change:**
- The search surface is good
- The school cards are good
- The curated events preview is fine as a secondary module

### School/college pages — new surface, worth building

There are no school pages. A school page could show:
- Current name and historical names (rename timeline)
- Active programs in that school
- Active course count
- School tenets (once parsed)
- Notable recent events (filtered from event layer)

These don't require new parsing beyond tenets. All other data exists. School pages would give the site genuine navigational depth.

### Methods/provenance areas — add a data freshness indicator

The methods page is solid. The main addition is a visible "data freshness" statement: what catalog edition the site reflects, when that edition was published, and when the site data was last regenerated. This should appear on:
- The homepage (in the orientation band or footer)
- The methods page
- The data download page

It is already partially there (data_date field in homepage_summary.json). It just needs to be more prominent.

---

## 5. Provenance and citation pattern

### Recommendation

Use a **two-tier citation system**:

**Tier 1 — Section label** (on every data section heading):

> Official Catalog History · Source: WGU Public Catalog (2026-03)

This is already implemented on course pages as the blue left-border section. Keep it. Make the catalog edition part of the visible label, not just a footer footnote.

**Tier 2 — Inline fact attribution** (for specific claims that are edition-bound):

Use a small neutral badge next to key facts:

> **3 CUs** `2026-03`

> **First seen:** 2017-01 &nbsp; **Last seen:** 2026-03

> **Current programs:** 1 &nbsp; `as of 2026-03`

This is clean, unobtrusive, and lets a reader know the vintage of any specific fact without cluttering the page.

**Avoid:**
- Long inline citation strings like "(Source: WGU Official Catalog, March 2026)"
- Footnote-only attribution that isn't visible in the primary reading flow
- Attributing every bullet point separately — attribute the section, not each sentence

### For program descriptions and outcomes (once extracted):

> **About this program** · From the WGU catalog (2026-03) ·  [Official WGU page ↗]

The description is WGU-authored catalog text and should be presented as quoted/attributed catalog content, not paraphrased or presented as WGU Atlas's own analysis.

### For interpreted content (events, classification):

Keep the existing blue `Source: WGU public catalog archive` badge. Add `Interpretation: WGU Atlas` where interpretive summaries appear. This is already designed into the events system.

---

## 6. Monthly update workflow

The intended cadence is: new catalog → parse → rebuild → redeploy. Here is the minimal reproducible flow:

### Step 1 — Acquire new catalog (in `wgu-reddit`)

WGU publishes a new catalog edition approximately monthly. CDN blocks programmatic download; PDFs must be downloaded manually from the WGU institutional catalog page and converted to `.txt` with pdfplumber.

Add to: `data/raw_catalog_texts/catalog_YYYY_MM.txt`

### Step 2 — Parse (in `wgu-reddit`)

```bash
python3 WGU_catalog/parse_catalog_v11.py
```

Inspect the output for anomaly count. Compare to prior edition: course count should increase by 0–15, program count by 0–3. Large swings warrant manual inspection.

If V11 ERA_A support is used for historical runs, ERA detection is automatic. For new catalogs (ERA_B), no changes needed.

### Step 3 — Rebuild change tracking and diffs (in `wgu-reddit`)

```bash
python3 WGU_catalog/build_change_tracking.py
python3 WGU_catalog/build_edition_diffs.py
```

Review `edition_diffs_summary.csv` for the new transition. Flag anything with severity > 100 for potential manual curation as a named event.

### Step 4 — Rebuild site data (in `wgu-reddit`, output to `wgu-atlas`)

```bash
WGU_REDDIT_PATH=/path/to/wgu-reddit/WGU_catalog/outputs \
WGU_ATLAS_DATA=/path/to/wgu-atlas/data \
python3 wgu-atlas/scripts/build_site_data.py
```

This regenerates all `site_data/` artifacts. Verify counts match expectations (should be ≥ prior counts for active courses).

Copy the updated exports:
```bash
cp -r /path/to/wgu-reddit/WGU_catalog/outputs/site_data/exports/* wgu-atlas/public/data/
```

(Or adjust `build_site_data.py` output path so it writes directly to `wgu-atlas/public/data/`.)

### Step 5 — Update `wgu-atlas` and deploy

```bash
cd wgu-atlas
git add public/data/ data/
git commit -m "Data update: YYYY-MM catalog edition"
git push origin main
```

GitHub Actions picks up the push, runs `npm run build`, exports the site, deploys to GitHub Pages. No manual deploy step needed.

### Step 6 — Verify

Check the live site within a few minutes of the push completing. Confirm the homepage shows the correct `data_date`. Spot-check one or two newly added course codes.

### Important notes

- `build_site_data.py` takes 30–60 seconds due to loading `course_index_v10.json` (59 MB). This is expected.
- `homepage_summary.json` is pre-computed and will show stale "newest programs" data until regenerated. This is intentional — static builds are explicit about their data vintage.
- The `data_date` field in `homepage_summary.json` is the visible data version indicator on the site.
- The `wgu-reddit` parser and build scripts should always run on that repo's `main` branch before copying outputs to `wgu-atlas`.

---

## Priority order for next work

1. **Add CUs to course card and course detail page** — no new data, high user value
2. **Build program pages** using existing `program_history.csv` — fills the biggest navigation gap
3. **Build school/college pages** — provides real depth; needs only existing data + school tenets text
4. **Extract program descriptions** — new parsing, highest content value for program pages
5. **Extract program outcomes** — new parsing, strong user value for program pages
6. **Surface stability class more visibly** — minor UI polish, adds trust signals
7. **Certificate descriptions** — minor parser extension, good for cert users
8. **Course term-in-program** — useful but data model complexity, defer until program pages are stable
