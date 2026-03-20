# Page Designs

This folder preserves:
- current page-state documentation
- source-baseline analysis (raw catalog and official WGU public site)
- screenshot-based visual readings
- source-vs-Atlas transformation analysis
- homepage design synthesis

It is the working hub for:
- homepage design work
- page-level design understanding
- source-baseline comparison work
- preserving conclusions from design sessions

**Why this matters:**
Important UI and product understanding should not live only in chat or temporary memory. Atlas needs to be evaluated against two distinct baselines — the raw catalog and WGU's public website — and homepage design depends on understanding both the strongest Atlas surfaces and the source systems they improve on.

---

## Design goals for this folder

The following goals emerged from the March 2026 design session and should inform all homepage and product-framing work that draws on these docs.

- The homepage should not be treated as only a launchpad or navigation surface. It should become a proof surface for what Atlas makes possible.
- Atlas should be positioned against two baselines: the raw WGU catalog, and the official WGU public-site exploration experience. The catalog-only comparison understates Atlas's value if the public site is also weak.
- The strongest Atlas story is that it restructures fragmented WGU information into something students can actually use — not that it is a nicer catalog or a community site.
- The homepage should demonstrate transformed student tasks, not just describe the site abstractly.
- The strongest product surfaces currently identified:
  - Degree pages — one-page consolidation of description, outcomes, roster, history, and official resources
  - Compare — a structured degree-comparison capability that does not exist in the source
  - Course connectedness — clickable roster links that replace repeated manual lookups
  - History/change context — first-offered dates, CU changes, school-name history absent from source
  - Relevant Resources — curated official materials not attached to degree entries in the source
- Ecosystem, community, and social research may matter later but should not displace the core academic-reference product story on the homepage.
- The work behind Atlas should be visible through useful product surfaces, not through methods-heavy framing or self-promotion.

---

## Documentation standard for files in this folder

Every file in `_internal/page_designs` should describe its contents, not merely point to them.

For page-state and design-analysis docs, preserve enough detail that a future reader can understand the page or argument without reopening the live site immediately. Where relevant, files should capture:
- what the page or artifact is
- why it matters
- what is visibly or structurally present
- what the student can do with it
- what it proves about Atlas
- what it implies for homepage or product design

For screenshot-based analysis, preserve the important visible facts in prose so the design reading is not lost if the screenshot is unavailable later.

For source-baseline docs, preserve both what the source contains and what friction or structural limitations the student experiences.

For synthesis docs, preserve the actual conclusions and reasoning — not just references to prior discussion.

The goal is not maximum verbosity, but durable descriptive usefulness.

---

## 1. Current page-state docs

These documents describe what a page currently is: route, layout, visible sections, design characteristics, and planning observations.

- **`homepage.md`**
  Current-state documentation for `/`. Captures structure, section hierarchy, and current homepage limitations relative to the site's strongest inner surfaces.

- **`program_detail.md`**
  Current-state documentation for `/programs/[code]`. BSCS is used as the reference example because it activates all major enrichment layers — description, outcomes, roster, history, and sidebar resources.

- **`compare_page.md`**
  Current-state visual and product reading of `/compare`, based on design-session screenshot analysis. Preserves why Compare is a flagship feature and its strongest homepage-proof characteristics.

---

## 2. Source baseline / source-vs-product docs

These documents describe what the raw source systems give the student — and how Atlas changes that experience.

- **`catalog_raw_analysis.md`**
  Practical analysis of the March 2026 WGU catalog as a student-facing source. Explains how degree information is split across sections, what the catalog does not provide, and why the raw format creates research friction.

- **`source_vs_atlas_program_entry.md`**
  Direct before/after comparison between a raw catalog degree entry and an Atlas program detail page (BSCS). Preserves the structural transformation argument. Important for homepage positioning and avoiding "just a nicer catalog" framing.

- **`wgu_public_site_student_experience.md`** *(in progress)*
  In-progress baseline for how students actually explore WGU on the public website. Important because the catalog is not the primary first-touch exploration surface — most students begin at wgu.edu. Documents the confirmed top-nav structure, Online Degrees category-gated entry flow, and the public degree hub. Stubs for sections covering school-level pages, official program page structure, compare baseline, course-discovery baseline, and official-resource discovery are queued for the next session.

---

## 3. Screenshot-based design analysis

These files preserve observations derived from looking at real screens or screenshots, not just source files or structured page docs.

- **`screenshot_analysis_log.md`**
  Running log of screenshot readings and visual conclusions. Preserves what was visible, what stood out, and what each screenshot proved about the product. Useful because screenshot analysis otherwise disappears from memory between sessions.

---

## 4. Design-session synthesis

These files preserve conclusions from broader design discussions that connect multiple pages and product arguments.

- **`homepage_design_session_2026-03.md`**
  Preserves higher-level conclusions from the March 2026 homepage design session, including homepage direction, product surface hierarchy, source-baseline implications, and recommended teaser priorities. Establishes that the homepage should become proof-of-value-first rather than navigation-first.

---

## 5. Comparative framing / future synthesis

This category is expected to hold future docs that directly compare:
- the raw catalog baseline
- the official WGU public-site exploration baseline
- Atlas improvement surfaces across both

Such docs are useful for homepage positioning, product explanation, and avoiding claims that depend only on the catalog comparison. No dedicated file exists yet in this category; `source_vs_atlas_program_entry.md` is the closest current artifact.

---

## Homepage design workflow

Homepage work should proceed in this order:

1. Understand the current homepage — what it does well and what it underplays
2. Understand the raw catalog baseline — what the source contains and where it fails the student
3. Understand the official WGU public-site exploration baseline — how students actually discover and research degrees
4. Study the strongest Atlas inner surfaces — degree pages, compare, course pages, history, resources
5. Preserve screenshot-based visual readings to ground product claims in visible evidence
6. Synthesize homepage implications only after source and product baselines are both clear

### Current homepage direction, based on preserved analysis

- The homepage should become more proof-of-value-first and less purely navigation-first.
- Degree pages and Compare are the strongest homepage-proof surfaces identified so far.
- Course connectedness is more important than it first appeared — it removes a major source-format limitation.
- History/change context is a meaningful differentiator because it is largely absent from both the catalog and the public site.
- Relevant Resources matter because neither the catalog nor the public site cleanly attaches supporting official materials near the degree entry.
- Public-site baseline work is still in progress and should be completed before final homepage design decisions are locked.

---

## Recommended reading order for homepage work

1. `homepage.md`
2. `catalog_raw_analysis.md`
3. `wgu_public_site_student_experience.md`
4. `program_detail.md`
5. `compare_page.md`
6. `source_vs_atlas_program_entry.md`
7. `homepage_design_session_2026-03.md`
8. `screenshot_analysis_log.md`

This order moves from the current homepage → source baselines → strongest Atlas surfaces → homepage strategy and visual evidence.

---

## Maintenance notes

Update this folder when:
- a major page layout changes
- a new source baseline is documented (catalog, public site, or other)
- screenshot review changes product understanding
- a page becomes homepage-relevant
- design-session conclusions shift homepage strategy

When updating or adding a file, prefer preserving key content and observations inside the file rather than relying on filenames or external memory. File-specific detail should live in the dedicated docs; this README should stay as the hub and orientation point for the folder.

Do not treat this folder as a task tracker, dev log, implementation checklist, or final design spec. Its purpose is preservation of product understanding and page-level design knowledge.

---

## File index

- `homepage.md`
- `program_detail.md`
- `compare_page.md`
- `catalog_raw_analysis.md`
- `source_vs_atlas_program_entry.md`
- `wgu_public_site_student_experience.md` *(in progress)*
- `screenshot_analysis_log.md`
- `homepage_design_session_2026-03.md`
