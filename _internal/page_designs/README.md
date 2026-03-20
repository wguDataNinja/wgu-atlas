# Page Designs

This folder preserves page-state documentation, source-baseline analysis, screenshot-based design readings, and higher-level design-session synthesis for WGU Atlas.

It exists so that important UI and product understanding does not live only in chat or in temporary memory.

The files in this directory are not all the same kind of artifact. They fall into four groups:

---

## 1. Current page-state docs

These documents describe what a page currently is:
- route
- layout
- visible sections
- conditional rendering
- design characteristics
- planning observations

### Files
- `homepage.md`
  - current-state documentation for `/`
  - captures structure, hierarchy, and current homepage limitations

- `program_detail.md`
  - current-state documentation for `/programs/[code]`
  - BSCS is used as reference example because it activates all major layers

- `compare_page.md`
  - current-state visual and product reading of `/compare`
  - based on design-session screenshot analysis
  - preserves why Compare is a flagship feature

---

## 2. Source baseline / source-vs-product docs

These documents describe what the raw source system gives the student and how Atlas changes that experience.

### Files
- `catalog_raw_analysis.md`
  - practical analysis of the March 2026 WGU catalog as a student-facing source
  - explains how degree information is split across sections
  - captures usability limitations of the raw catalog

- `source_vs_atlas_program_entry.md`
  - direct comparison between a raw catalog degree entry and an Atlas program detail page
  - preserves the structural transformation argument
  - important for homepage positioning and product explanation

---

## 3. Screenshot-based design analysis

These files preserve observations that come from looking at real screens or screenshots, not just source files or machine-generated page docs.

### Files
- `screenshot_analysis_log.md`
  - running log of screenshot readings and visual conclusions
  - preserves what was visible, what stood out, and what each screenshot proved
  - useful because screenshot analysis otherwise disappears from memory

---

## 4. Design-session synthesis

These files preserve conclusions from broader design discussions that connect multiple pages and product arguments.

### Files
- `homepage_design_session_2026-03.md`
  - higher-level conclusions from the March 2026 homepage design session
  - preserves strongest product surfaces, source-baseline implications, and homepage direction

---

## Recommended reading order for homepage work

If returning later to homepage planning, read in this order:

1. `homepage.md`
2. `catalog_raw_analysis.md`
3. `program_detail.md`
4. `compare_page.md`
5. `source_vs_atlas_program_entry.md`
6. `homepage_design_session_2026-03.md`
7. `screenshot_analysis_log.md`

That order moves from:
- current homepage
to
- source limitations
to
- strongest inner surfaces
to
- homepage implications

---

## Maintenance notes

Update this folder when any of the following happens:

- a major page layout changes
- a new screenshot analysis produces useful conclusions
- a page becomes important enough for homepage or positioning decisions
- the source baseline understanding changes
- a major design session produces conclusions worth preserving

Do not treat this folder as:
- a task tracker
- a dev log
- an implementation checklist
- a final design spec system

Its purpose is preservation of product understanding and page-level design knowledge.

---

## File index

- `homepage.md`
- `program_detail.md`
- `catalog_raw_analysis.md`
- `compare_page.md`
- `source_vs_atlas_program_entry.md`
- `screenshot_analysis_log.md`
- `homepage_design_session_2026-03.md`
