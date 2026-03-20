# Compare Page — `/compare`

Route: `/compare`
Reference capture date: 2026-03-20
Primary evidence:
- live compare screenshot reviewed in design session
- current compare page behavior as observed in UI
Related docs:
- `homepage.md`
- `program_detail.md`
- `catalog_raw_analysis.md`
- `source_vs_atlas_program_entry.md`
- `homepage_design_session_2026-03.md`

---

## Purpose of this doc

This document preserves the current-state visual and product reading of the Compare Degrees page as a homepage-relevant flagship feature.

It exists to answer:

- what the compare page currently looks like
- what information it makes legible
- why it is one of Atlas's strongest features
- what weaknesses exist in the current V1 presentation
- how suitable it is for homepage teasing or screenshot use

This is not an implementation spec and not a rebuild plan.
It is a design-analysis artifact.

---

## Why Compare matters

The raw WGU catalog has no meaningful comparison affordance.

A student who wants to compare two related degrees from the source materials must:

1. find both program entries in separate parts of the catalog
2. read both rosters manually
3. identify shared and unique courses by hand
4. separately find outcomes in a later section
5. mentally reconstruct the difference between tracks or specializations

Atlas Compare turns that manual task into a structured visual view.

Because of that, Compare is one of the clearest demonstrations that Atlas is not just presenting catalog data more attractively. It is providing a capability the source does not provide.

---

## Overall page identity

The Compare page is a clean desktop page with:

- standard top navigation
- simple heading and short explanatory text
- one dominant comparison module centered in the page

The page is visually sparse and focused. It does not include sidebars, promotional distractions, or secondary sections. Nearly all visual attention is directed to the comparison module.

This makes the page feel product-like and task-oriented.

---

## Top navigation state

The persistent site navigation appears at the top on a white background with a faint bottom border.

Visible nav items:
- WGU Atlas
- Home
- Courses
- Degrees
- Colleges
- Compare Degrees
- About

Current-page state:
- `Compare Degrees` is highlighted, making page identity clear

The nav is restrained and does not compete with the feature content.

---

## Page intro area

Below the nav is a page heading area.

Visible structure:
- large heading: `Compare Degrees`
- small explanatory paragraph beneath

The explanatory copy is functional, not dramatic. It explains that two degrees can be compared side by side and that shared/unique courses and overlap metrics are shown.

Design reading:
- the intro is serviceable
- the actual comparison module is more persuasive than the copy above it
- the page's strongest argument comes from the visualization, not the text

---

## Main compare module

The comparison experience lives inside one large centered card/module.

### Outer structure
The module has:
- a dark top strip
- rounded top corners
- a colored comparison summary row below
- stacked term sections below that

This module is the visual center of the page.

### Control area
In the upper-right of the dark top strip are small text controls:
- `Change`
- `Reset`

These are currently visually light and somewhat bolted-on.

Design reading:
- functional in V1
- not polished as a primary control system
- the controls work, but the page's strength is the compare visualization, not the control chrome

---

## Header comparison band

The strongest visual element in the module is the 3-part comparison summary header.

It is split into three horizontal blocks:

### Left block
Represents the first degree.
Observed example:
- `Data Science`
- `4 unique · MSDADS`

Visual treatment:
- blue background
- white text

### Center block
Represents shared courses.
Observed example:
- `Shared`
- `7 in both`

Visual treatment:
- dark slate/blue-gray background
- white text

### Right block
Represents the second degree.
Observed example:
- `Data Engineering`
- `4 unique · MSDADE`

Visual treatment:
- gold/orange background
- white text

---

## What the header band communicates well

At a glance, this band tells the user:

- which degree is on the left
- which degree is on the right
- how many courses are unique to each side
- how many are shared

This is extremely effective because it converts a complicated manual comparison task into an immediately understandable structure.

This is one of the strongest homepage-screenshot candidates in the product.

---

## Term-by-term structure

Below the comparison header, the compare module is organized into term sections.

Observed visible terms in the screenshot:
- TERM 1
- TERM 2
- TERM 3
- TERM 4

Each term begins with a dark bar label such as:
- `TERM 1`
- `TERM 2`

Additional text may appear next to the term label, such as:
- `all shared this term`

This term structure is one of the feature's biggest strengths because it preserves the degree-plan logic rather than flattening everything into one diff.

---

## Lane model

Within each term, the page uses a three-lane comparison model:

- left lane = unique to the left degree
- center lane = shared
- right lane = unique to the right degree

This lane model is the key visual logic of the page.

It allows a student to understand not only which courses differ, but where divergence begins and how it is distributed across the plan.

That is much more meaningful than simply listing "same" and "different" courses.

---

## Course-row design

Courses appear as compact row-like items with:

- a colored course-code badge
- course title
- CU value aligned to the right

Observed color logic:
- shared courses in green-toned center region
- left-unique courses with blue-toned accents
- right-unique courses with gold-toned accents

This makes the page scannable even without reading every title.

---

## Observed example comparison

Reference screenshot compared:
- Data Science
- Data Engineering

Observed summary:
- left unique: 4
- shared: 7
- right unique: 4

### TERM 1
Marked as all shared this term.
Visible shared courses:
- D596 — The Data Analytics Journey
- D597 — Data Management
- D598 — Analytics Programming

### TERM 2
Also all shared this term.
Visible shared courses:
- D599 — Data Preparation and Exploration
- D600 — Statistical Data Mining
- D601 — Data Storytelling for Varied Audiences

### TERM 3
This is where divergence becomes visible.

Left unique:
- D603 — Machine Learning
- D604 — Advanced Analytics

Shared:
- D602 — Deployment

Right unique:
- D607 — Cloud Databases
- D608 — Data Processing

### TERM 4
No shared courses visible in the center.

Left unique:
- D605 — Optimization
- D606 — Data Science Capstone

Right unique:
- D609 — Data Analytics at Scale
- D610 — Data Engineering Capstone

---

## What Compare makes legible

The compare page makes several things easy to understand that are hard or impossible to see from the raw catalog:

### 1. Shared foundation
The student can immediately see where two degrees overlap.

### 2. Point of divergence
The student can see the term where specialization begins.

### 3. Nature of divergence
The user can understand whether the difference is:
- one or two swapped courses
- a whole late-stage specialization shift
- a capstone/path distinction
- a broader branch in direction

### 4. Credit-bearing structure
Because CU values remain visible, the student can see not just titles but the unit-bearing shape of the difference.

---

## Visual strengths

### Clean focus
The page is almost entirely devoted to the comparison task.

### Strong summary band
The three-part header is immediately understandable.

### Good structural logic
Term grouping plus lane comparison is an excellent model.

### Product-feeling UI
Even in V1, this feels like a specific tool, not a static data dump.

### Clear flagship potential
This is one of the easiest site features to explain visually to a first-time visitor.

---

## Current weaknesses / limitations visible in design

### 1. Control strip feels secondary
The `Change` and `Reset` controls are small and visually lightweight in a dark strip. They do not feel fully integrated into the rest of the module.

### 2. Heavy top chrome
The module has:
- dark strip
- colored summary band
- repeated dark term bars

This works, but creates a slightly heavy stacked visual hierarchy.

### 3. Intro copy is weaker than the module
The page's explanatory text is plain and undersells the feature. The visualization does the real persuasion.

### 4. Screenshot dependence for marketing/showcase
Because the module is so strong visually, homepage use will likely depend on well-chosen screenshots/crops. Fortunately, screenshot choice can be iterated later without changing the underlying product argument.

---

## Homepage suitability

Compare is strongly homepage-worthy.

### Why
Because it demonstrates:
- a capability absent from the catalog
- structured transformation of degree information
- practical student value
- the value of modeling, normalization, and product design

### Best homepage use
Likely forms:
- screenshot crop of the summary band plus visible divergence term
- screenshot crop showing TERM 3/TERM 4 divergence
- short accompanying message such as:
  - "See exactly what changes between related degrees"
  - "Compare shared and unique courses side by side"
  - "A task that is manual in the catalog becomes obvious in Atlas"

### Relative homepage priority
This feature should rank among the most prominent homepage teaser candidates.

---

## Product significance

Compare is one of the clearest examples of what Atlas is doing well.

It shows that Atlas is not merely:
- mirroring the source
- extracting text
- prettifying a PDF

It is:
- restructuring information
- creating a new student task flow
- making hidden relationships visible
- turning friction-heavy research into readable product interaction

---

## Planning conclusions

1. Compare should be treated as a flagship capability.
2. Homepage design should feature it more prominently than the current homepage does.
3. The visual comparison module is stronger than the current homepage compare callout.
4. Screenshot-based homepage promotion is valid and low-risk because the compare UI can evolve later without invalidating the feature claim.
5. Compare is one of the strongest proofs that Atlas justifies the underlying extraction/modeling work.

---

## Preservation summary

This doc preserves the following durable conclusions:

- Compare is one of the strongest surfaces on the site.
- Its visual logic is clear enough to serve as a homepage proof module.
- It materially solves a task the raw catalog does not support.
- Its current weaknesses are mostly presentation-polish issues, not concept issues.
- It should be promoted as a unique and useful product feature, not a buried utility page.
