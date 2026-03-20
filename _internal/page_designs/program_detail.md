# Program Detail Page — `/programs/[code]`

Route: `/programs/[code]`
Example: `/programs/BSCS` — Bachelor of Science, Computer Science
Last updated: 2026-03-20
Sources: `src/app/programs/[code]/page.tsx` · `src/app/programs/[code]/LearningOutcomes.tsx` · `src/components/resources/RelevantResources.tsx` · `public/data/program_enriched.json` · `public/data/official_resource_placements.json` · `public/data/programs.json`

BSCS was chosen as the reference example because it has all enrichment layers active:
- description ✓
- learning outcomes (6) ✓
- full course roster (37 courses, 9 terms) ✓
- official resource placements: program guide + outcomes link ✓
- college name history (CIT → School of Technology) ✓

---

```
══════════════════════════════════════════════════════════════
  PROGRAM DETAIL PAGE  (/programs/[code])
  Example: BSCS — B.S., Computer Science
  Current state · 2026-03
══════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────
  TOP NAVIGATION BAR
  [site-persistent — see homepage.md]
──────────────────────────────────────────────────────────────

  Brand:  WGU Atlas
  Links:  Home · Courses · Degrees · Colleges · Compare Degrees · About

──────────────────────────────────────────────────────────────
  PAGE LAYOUT — WITH RESOURCES (2-column)
  [src: src/app/programs/[code]/page.tsx:70-298]

  When a program has relevant resources:
    max-w-6xl · mx-auto · px-4 · py-10
    lg:grid lg:grid-cols-[1fr_19rem] lg:gap-10

  When no relevant resources:
    max-w-4xl · mx-auto · px-4 · py-10
    single column only

  The sidebar column is 19rem (304px) fixed-width.
  The main content column gets all remaining space (minmax 0, 1fr).
──────────────────────────────────────────────────────────────

  ┌──────────────────────────────────────┐  ┌───────────────┐
  │  MAIN CONTENT COLUMN                 │  │ SIDEBAR       │
  │                                      │  │ (19rem fixed) │
  │  [breadcrumb]                        │  │               │
  │  [header: code · status · CUs]       │  │ Relevant      │
  │  [H1: program name]                  │  │ Resources     │
  │  [school link]                       │  │               │
  │                                      │  │ ...           │
  │  About This Degree                   │  │               │
  │  Degree History                      │  │               │
  │  Learning Outcomes                   │  │               │
  │  Course Roster                       │  │               │
  │  ← Back to Degrees                   │  │               │
  └──────────────────────────────────────┘  └───────────────┘

  Sidebar is: lg:sticky lg:top-24 lg:mt-0
  (sticky on scroll; aligns to top of viewport + 24px offset)
  On mobile/tablet: sidebar renders below main content (mt-8)

──────────────────────────────────────────────────────────────
  BREADCRUMB
  [src: page.tsx:82-88]
──────────────────────────────────────────────────────────────

  Degrees › BSCS

  Style: text-sm text-slate-400
  "Degrees" → /programs  (hover:text-blue-600)
  "BSCS" = plain text (text-slate-600)

──────────────────────────────────────────────────────────────
  HEADER BLOCK
  [src: page.tsx:90-113]
──────────────────────────────────────────────────────────────

  BSCS · Current · 123 CUs
  (text-sm text-slate-500 · code · status · latest CU value)

  Bachelor of Science, Computer Science
  (text-3xl font-bold text-slate-800)

  School of Technology  [linked → /schools/technology]
  (text-blue-600 hover:underline text-sm)

  Note: CU value shows "(was 117)" if CUs changed over time.
  Note: If retired, shows "Retired — last seen: YYYY-MM" (text-sm text-slate-400)

──────────────────────────────────────────────────────────────
  SECTION: ABOUT THIS DEGREE
  [src: page.tsx:115-134]
  Renders only if enriched.description is present.
──────────────────────────────────────────────────────────────

  ┃ About This Degree          [WGU Catalog 2026-03]
    ╔══════════════════════════════════════════════════╗
    ║ "The Bachelor of Science in Computer Science     ║
    ║  prepares students for a career in the high      ║
    ║  demand field of Computer Science..."            ║
    ╚══════════════════════════════════════════════════╝
    Official catalog text — WGU-authored.

  Section header:
    - Blue accent bar:  w-1 h-5 bg-blue-600 rounded
    - H2:               text-lg font-bold text-slate-800
    - Source badge:     text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded
      (e.g. "WGU Catalog 2026-03")

  Description:
    - blockquote: border-l-4 border-blue-100 pl-4
    - Text:       text-slate-700 text-sm leading-relaxed italic

  Attribution:
    - "Official catalog text — WGU-authored."
    - text-xs text-slate-400 mt-2

──────────────────────────────────────────────────────────────
  SECTION: DEGREE HISTORY
  [src: page.tsx:136-198]
  Always renders (not conditional on enrichment).
──────────────────────────────────────────────────────────────

  ┃ Degree History    (text-base font-semibold text-slate-600)
    (slate accent bar: bg-slate-300)

  ┌──────────────────────────────────────────────────┐
  │  First offered  2018-05   Status  Current         │
  │  CUs (latest)   123 CUs   (was 117)               │
  └──────────────────────────────────────────────────┘
  Container: bg-slate-50 border border-slate-200 rounded-lg px-4 py-3
  Layout:    flex flex-wrap gap-x-6 gap-y-2
  Items:     text-sm text-slate-600
    label:   text-xs text-slate-400 mr-1
    value:   font-medium
    "Current" → text-green-700
    "Retired" → text-slate-500

  CU note: "CUs (latest)" label if CUs changed; "(was 117)" appended
  If retired: adds "Last seen" item

  College name history (only if colleges.length > 1):

    College name history   (text-xs text-slate-400)

    [ College of Information Technology ] →  [ School of Technology ]
      (bg-slate-100 text-slate-500)           (bg-blue-50 text-blue-700)

    Chips: text-xs px-2 py-0.5 rounded
    Arrows: text-slate-300 text-xs
    Last/current chip uses blue tint; earlier chips use slate

──────────────────────────────────────────────────────────────
  SECTION: LEARNING OUTCOMES
  [src: src/app/programs/[code]/LearningOutcomes.tsx]
  Renders only if enriched.outcomes.length > 0.
  Client component (collapsible).
──────────────────────────────────────────────────────────────

  ┃ Learning Outcomes          [WGU Catalog 2026-03]
    "Official WGU-authored outcomes from the catalog
     Program Outcomes section."
    (text-xs text-slate-400)

    • The graduate applies core information technology
      skills in IT systems, operating systems, networking...
    • The graduate will be able to solve computing problems
      using critical thinking and mathematical reasoning.
    • The graduate will be able to develop secure software
      systems to support organizational goals and needs.

    [Show 3 more ▾]        ← button, collapsed by default

  BSCS has 6 outcomes. First 3 shown, 3 hidden behind toggle.
  Toggle: text-xs text-blue-600 hover:text-blue-800
  Expanded label: "Show less ▴"
  Collapsed label: "Show {n} more ▾"

  Outcome list:
    ul: space-y-2
    li: flex gap-2 text-sm text-slate-700
    bullet: text-slate-300 mt-0.5 shrink-0 (plain "•")

  Section header same pattern as other sections:
    - Blue accent bar
    - H2: text-lg font-bold text-slate-800
    - Source badge: bg-slate-100

──────────────────────────────────────────────────────────────
  SECTION: COURSE ROSTER
  [src: page.tsx:211-282]
  Renders only if enriched.roster.length > 0.
──────────────────────────────────────────────────────────────

  ┃ Course Roster (37 courses)   [WGU Catalog 2026-03]

  Term 1
  ┌──────┬─────────────────────────────────────┬────┐
  │ Code │ Title                               │ CUs│
  ├──────┼─────────────────────────────────────┼────┤
  │ D684 │ Introduction to Computer Science    │  4 │
  │ C955 │ Applied Probability and Statistics  │  3 │
  │ D278 │ Scripting and Programming -         │  3 │
  │      │  Foundations                        │    │
  │ ...  │ (1 more)                            │    │
  └──────┴─────────────────────────────────────┴────┘

  [Terms 2 through 9 follow same pattern]

  BSCS roster structure: 9 terms · 37 total courses
    Term 1:  4 courses
    Term 2:  4 courses
    Term 3:  5 courses
    Term 4:  5 courses
    Term 5:  4 courses
    Term 6:  4 courses
    Term 7:  4 courses
    Term 8:  4 courses
    Term 9:  3 courses

  Section header:
    Blue accent bar + H2 "Course Roster ({n} courses)"
    source badge (same pattern as other sections)

  Term headers:
    h3: text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2
    e.g. "TERM 1"

  Table:
    border border-slate-200 rounded-lg overflow-hidden
    thead: bg-slate-50 border-b border-slate-200
    th:    text-left px-3 py-2 text-xs font-medium text-slate-500
    tr:    border-b border-slate-100 last:border-0 hover:bg-slate-50
           alternate rows: bg-slate-50/30 on odd
    td code: font-mono text-xs text-blue-700 hover:underline → /courses/{code}
    td title: text-slate-700
    td CUs:   text-slate-500 text-xs text-right

  Footer line:
    "Total: {sum} CUs across {n} courses.
     Degree total per catalog: {latestCus} CUs."
    text-xs text-slate-400 mt-3

──────────────────────────────────────────────────────────────
  BACK LINK
  [src: page.tsx:284-289]
──────────────────────────────────────────────────────────────

  ← Back to Degrees
  border-t border-slate-100 pt-6
  text-sm text-blue-600 hover:underline → /programs

──────────────────────────────────────────────────────────────
  SIDEBAR: RELEVANT RESOURCES
  [src: src/components/resources/RelevantResources.tsx]
  Renders only when placements exist for this surface_key.
  Sticky on desktop: lg:sticky lg:top-24
──────────────────────────────────────────────────────────────

  ┌─────────────────────────────────┐
  │  Relevant Resources             │
  │  Official WGU resources         │
  │  related to this degree.        │
  │                                 │
  │  OUTCOMES                       │
  │  B.S. Computer Science          │
  │  Outcomes at WGU ↗              │
  │  Official outcomes and          │
  │  assessment results for this    │
  │  program.                       │
  │                                 │
  │  PROGRAM GUIDES                 │
  │  B.S. Computer Science          │
  │  Program Guide ↗                │
  │  Official WGU program guide     │
  │  and current degree overview.   │
  └─────────────────────────────────┘

  Container:
    rounded-lg border border-slate-200 bg-slate-50/60 p-4

  Header:
    "Relevant Resources"
    text-sm font-semibold text-slate-800

  Subhead:
    "Official WGU resources related to this degree."
    mt-1 text-xs text-slate-500

  Group headers (only shown when multiple groups present):
    text-[11px] font-semibold uppercase tracking-wide text-slate-500 mb-2
    e.g. "OUTCOMES" / "PROGRAM GUIDES"

  Link items (per resource):
    Title + ↗  (text-sm text-blue-700 hover:underline)
    Benefit reason paragraph (text-xs text-slate-500 mt-0.5)

  BSCS resource groups and ordering:
    1. outcomes        (display_priority: lowest → shown first)
       "B.S. Computer Science Outcomes at WGU ↗"
       "Official outcomes and assessment results for this program."
    2. program_guide   (display_priority: higher → shown after)
       "B.S. Computer Science Program Guide ↗"
       "Official WGU program guide and current degree overview."

  Group label map:
    outcomes           → "Outcomes"
    accreditation      → "Accreditation"
    regulatory_licensure → "Licensure & Exams"
    program_variant    → "Specializations"
    program_guide      → "Program Guides"

══════════════════════════════════════════════════════════════
  PAGE STRUCTURE SUMMARY (top to bottom, with resources)
══════════════════════════════════════════════════════════════

  1. Nav bar               site-persistent
  2. Breadcrumb            Degrees › {code}
  3. Header block          code · status · CUs · name · school link
  4. About This Degree     catalog description (italic blockquote)
  5. Degree History        compact metadata row + college name chips
  6. Learning Outcomes     collapsible list (3 shown + toggle)
  7. Course Roster         term-grouped table · all courses · CU totals
  8. Back link             ← Back to Degrees
  [sidebar]                Relevant Resources (sticky, right column on lg+)

══════════════════════════════════════════════════════════════
  CONDITIONAL RENDERING SUMMARY
══════════════════════════════════════════════════════════════

  Always renders:
  ✓ Breadcrumb
  ✓ Header (code · name · status · school)
  ✓ Degree History section
  ✓ Back link

  Renders only with enrichment data:
  ✓ About This Degree       — requires enriched.description
  ✓ Learning Outcomes       — requires enriched.outcomes.length > 0
  ✓ Course Roster           — requires enriched.roster.length > 0

  Renders only with resource placements:
  ✓ Sidebar (Relevant Resources) — requires placements for surface_key
  ✓ 2-column layout              — triggered by hasRelevantResources flag
  ✓ Wider page (max-w-6xl)       — same trigger; otherwise max-w-4xl

  College name history row:
  ✓ Only when program.colleges.length > 1

  CU history note ("was {n}"):
  ✓ Only when program.cus_values.length > 1

══════════════════════════════════════════════════════════════
  DESIGN CHARACTERISTICS
══════════════════════════════════════════════════════════════

  Layout
    2-col (lg+):    main content + 19rem fixed sidebar
    1-col (mobile): stacked; sidebar below main
    Page max-w:     6xl (with sidebar) · 4xl (without)
    Sticky sidebar: top-24 on scroll

  Section header pattern (consistent across all sections)
    Blue accent bar:  w-1 h-5 bg-blue-600 rounded (or bg-slate-300 for Degree History)
    H2/heading:       text-lg font-bold text-slate-800
    Source badge:     text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded

  Color signals
    Active status:   text-green-700
    Retired status:  text-slate-500
    Current college: bg-blue-50 text-blue-700
    Past colleges:   bg-slate-100 text-slate-500
    Course codes:    font-mono text-xs text-blue-700
    Descriptions:    italic text-slate-700
    Resource links:  text-blue-700
    Attribution:     text-slate-400 (xs)

  Typography
    Page H1:         text-3xl font-bold text-slate-800
    Section H2:      text-lg font-bold text-slate-800
    Section H2 alt:  text-base font-semibold text-slate-600 (Degree History)
    Term headers:    text-xs font-semibold text-slate-500 uppercase tracking-wide
    Table headers:   text-xs font-medium text-slate-500
    Body:            text-sm text-slate-700
    Secondary:       text-xs text-slate-400/500
    Links:           text-blue-600/700 hover:underline

  Interactions
    Course code links:   hover:underline → /courses/{code}
    School name link:    hover:underline → /schools/{slug}
    Learning outcomes:   toggle "Show N more ▾" / "Show less ▴"
    Table rows:          hover:bg-slate-50
    Resource links:      open in new tab (target="_blank")

══════════════════════════════════════════════════════════════
  DESIGN OBSERVATIONS FOR PLANNING
══════════════════════════════════════════════════════════════

  - The 2-column layout only activates when a program has
    resource placements. Programs without resources get a
    narrower single-column layout. This means the page has
    two distinct visual states depending on enrichment depth.

  - Learning Outcomes is collapsed by default at 3 items.
    BSCS has 6 outcomes; a visitor sees 3 without interaction.
    No indication of how many are hidden until they read
    "Show 3 more ▾". The count in the toggle is the only signal.

  - The section header pattern (blue accent bar + H2 + source
    badge) is visually consistent across all content sections.
    The Degree History section breaks this slightly — it uses a
    slate-300 accent bar and a smaller/lighter H2, signaling
    it is metadata rather than enriched content.

  - Source badges ("WGU Catalog 2026-03") appear on every
    content section. Provenance is explicit throughout.

  - The sidebar "Relevant Resources" has no explicit section
    heading hierarchy tied to the main content — it is a
    standalone widget. Group headers only appear when there
    are 2+ groups. BSCS shows "OUTCOMES" and "PROGRAM GUIDES"
    as separate groups.

  - Course codes in the roster are clickable links to
    /courses/{code}. This is the primary cross-navigation
    path from degree pages to course pages.

  - The roster table shows CU counts per course and a totals
    line but does not currently show course descriptions
    inline. Description context requires navigating away.

  - "Degree History" section is always visible even for
    programs with minimal history (e.g. no CU changes, no
    college renaming). For those programs it shows only
    first_seen and status — useful but low information density.

  - The college name history chip flow (CIT → School of
    Technology) is the only place institutional naming changes
    surface on the degree page. Not labeled as a rename;
    requires context to interpret.

  - No explicit link to compare from a degree page. A user
    who wants to compare two degrees must navigate away to
    /compare and re-select. No "Compare this degree" shortcut
    exists on the degree detail page.
```
