# Homepage — `/`

Route: `/`
Last updated: 2026-03-20
Sources: `src/app/page.tsx` · `src/components/home/HomeSearch.tsx` · `src/components/home/SchoolCards.tsx` · `src/components/layout/Nav.tsx` · `src/components/layout/Footer.tsx` · `content_map.txt`

---

```
══════════════════════════════════════════════════════════════
  WGU ATLAS — HOMEPAGE  (/)
  Current state · 2026-03
══════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────
  TOP NAVIGATION BAR
  [src: src/components/layout/Nav.tsx]
  Full-width · site-persistent
──────────────────────────────────────────────────────────────

  Brand:   WGU Atlas
  Links:   Home · Courses · Degrees · Colleges · Compare Degrees · About

  Not in top nav (accessible via /about only):
    Timeline · Methods · Data

──────────────────────────────────────────────────────────────
  SECTION 1 — HERO
  [src: src/app/page.tsx:10-25]
  [src: src/components/home/HomeSearch.tsx]
  [src: src/components/home/SchoolCards.tsx]

  Full-width section · dark blue gradient background
  (bg-gradient-to-b from-blue-950 to-blue-900)
  White text · centered · max-width 3xl · py-14
──────────────────────────────────────────────────────────────

  H1:       WGU Atlas
            (text-4xl/5xl · bold · tracking-tight)

  Subtitle: Explore WGU degrees and courses. See what's
            included. Compare related degrees.
            (text-blue-200 · text-lg · mb-8)

  ┌─────────────────────────────────────────────┐
  │  🔍  Search degrees or courses…          [✕] │
  └─────────────────────────────────────────────┘
  White rounded-lg · shadow-sm · max-w-xl · centered
  Focus ring: ring-2 ring-blue-500
  Clear (✕) button appears when query present

  Search behavior:
  - Loads search_index.json once on mount (client-side fetch)
  - Queries fire at ≥2 characters
  - Matches on: code · title · alt_titles
  - Returns up to 8 results as dropdown
  - Result row: [CODE badge] · title · "retired" (if inactive)
    Course badge:  bg-blue-100 text-blue-700 · font-mono
    Degree badge:  bg-purple-100 text-purple-700 · font-mono
  - Last row: "See all results for '{query}' →" → /courses?q=...
  - Closes on outside click

  ┌─────────────────────┐  ┌─────────────────────┐
  │  School of Business │  │ Leavitt School of   │
  │  (bg-blue-50 /      │  │ Health              │
  │   border-blue-200)  │  │ (bg-green-50 /      │
  │                     │  │  border-green-200)  │
  │  Bach's, master's,  │  │  Degrees in nursing,│
  │  MBA in accounting, │  │  healthcare admin,  │
  │  management,        │  │  public health,     │
  │  marketing, etc.    │  │  health informatics.│
  │                     │  │                     │
  │  Explore School of  │  │  Explore Leavitt    │
  │  Business →         │  │  School of Health → │
  └─────────────────────┘  └─────────────────────┘
  ┌─────────────────────┐  ┌─────────────────────┐
  │  School of          │  │  School of           │
  │  Technology         │  │  Education           │
  │  (bg-purple-50 /    │  │  (bg-amber-50 /      │
  │   border-purple-200)│  │   border-amber-200)  │
  │                     │  │                      │
  │  Degrees in IT,     │  │  Teacher prep,       │
  │  cybersecurity,     │  │  ed leadership,      │
  │  software eng,      │  │  learning & tech     │
  │  data analytics.    │  │  across all grade    │
  │                     │  │  bands.              │
  │  Explore School of  │  │  Explore School of   │
  │  Technology →       │  │  Education →         │
  └─────────────────────┘  └─────────────────────┘

  Grid: grid-cols-1 mobile · sm:grid-cols-2 sm+
  Card: border rounded-lg p-4 · flex-col gap-2
        border color shifts on hover (e.g. hover:border-blue-400)
  Each card links to: /schools/{slug}
  Card content:
    - College name   (font-semibold text-slate-800 text-sm)
    - Description    (text-xs text-slate-600 leading-snug)
    - CTA            (text-xs text-blue-600 font-medium mt-1)
      "Explore {Name} →"

──────────────────────────────────────────────────────────────
  SECTION 2 — ORIENTATION PARAGRAPH
  [src: src/app/page.tsx:28-37]

  bg-slate-50 · border-b border-slate-100
  max-w-3xl · mx-auto · px-4 · py-8
──────────────────────────────────────────────────────────────

  "WGU Atlas is an independent guide to WGU degrees and
  courses, built from public WGU sources. Use it to explore
  available degrees, see the courses included in each,
  compare related degrees side by side, and look up any
  course's details or degree appearances."

  Style: text-slate-600 · text-sm · leading-relaxed
  No heading. No links. Plain paragraph only.

──────────────────────────────────────────────────────────────
  SECTION 3 — COMPARE CALLOUT
  [src: src/app/page.tsx:39-56]

  max-w-3xl · mx-auto · px-4 · py-8
  (no background change from body white)
──────────────────────────────────────────────────────────────

  ┌────────────────────────────────────────────────────────┐
  │  Compare Degrees                    Compare Degrees →  │
  │  See how related WGU degrees differ —                  │
  │  course rosters, shared courses, and                   │
  │  degree-specific requirements.                         │
  └────────────────────────────────────────────────────────┘

  Container:  border border-slate-200 · rounded-lg
              px-5 py-4 · flex row · items-center
              justify-between · gap-4
  Left col:   label (text-sm font-medium text-slate-800)
              + description (text-xs text-slate-500 mt-0.5)
  Right col:  "Compare Degrees →"
              (text-sm text-blue-600 shrink-0 · hover:underline)
              → /compare

──────────────────────────────────────────────────────────────
  SECTION 4 — ATTRIBUTION LINE
  [src: src/app/page.tsx:58-66]

  max-w-3xl · mx-auto · px-4 · pb-10
──────────────────────────────────────────────────────────────

  "Built from WGU's public catalog · Updated through
  March 2026 · About this site"

  Style:         text-xs text-slate-400
  "About this site" → /about  (hover:underline)

──────────────────────────────────────────────────────────────
  FOOTER
  [src: src/components/layout/Footer.tsx]

  border-t border-slate-200 · bg-slate-50 · mt-16
  max-w-6xl · mx-auto · px-4 · py-8
  grid-cols-1 mobile · md:grid-cols-3 md+
──────────────────────────────────────────────────────────────

  Col 1 — WGU Atlas
    "WGU Atlas"  (font-semibold text-slate-700)
    "Created by WGU-DataNinja"
    "An independent community project. Not affiliated with WGU."

  Col 2 — Data
    "Data"  (font-semibold text-slate-700)
    "Catalog coverage: 2017-01 → 2026-03"
    "Data through: 2026-03"
    Links: Methods · Download datasets  (underline · hover:text-slate-700)

  Col 3 — Disclaimer
    "Disclaimer"  (font-semibold text-slate-700)
    "All data is derived from WGU's publicly available course
    catalog. Catalog dates reflect publication, not student
    rollout timing."

══════════════════════════════════════════════════════════════
  PAGE STRUCTURE SUMMARY (top to bottom)
══════════════════════════════════════════════════════════════

  1. Nav bar           full-width · site-persistent
  2. Hero              dark blue gradient · full-width
                       H1 + subtitle + search bar + 4 school cards
  3. Orientation       slate-50 bg · plain 1-paragraph explainer
  4. Compare callout   white bg · single bordered box with CTA
  5. Attribution       1-line provenance/date note
  6. Footer            3-col · project / data / disclaimer

══════════════════════════════════════════════════════════════
  FUNCTIONAL INVENTORY
══════════════════════════════════════════════════════════════

  Active on homepage:
  ✓ Cross-entity search (courses + degrees · up to 8 results)
  ✓ School/college navigation (4 cards → /schools/{slug})
  ✓ Compare degrees callout (1 link → /compare)

  Not on homepage (accessible elsewhere):
  ✗ Program/degree browsing (no browse list, only search)
  ✗ Course browsing (no browse list, only search)
  ✗ Timeline
  ✗ Methods / methodology
  ✗ Data / download
  ✗ Historical change context
  ✗ Outcomes / accreditation / official resources
  ✗ Community / external links
  ✗ Any counts or scale signals (degrees, courses, editions)

══════════════════════════════════════════════════════════════
  DESIGN CHARACTERISTICS
══════════════════════════════════════════════════════════════

  Color system
    Hero bg:         blue-950 → blue-900 gradient
    Hero text:       white / blue-200 (subtitle)
    School cards:    tinted bg + border per school:
                       Business  → blue-50  / blue-200  / hover:blue-400
                       Health    → green-50 / green-200 / hover:green-400
                       Technology→ purple-50/ purple-200/ hover:purple-400
                       Education → amber-50 / amber-200 / hover:amber-400
    Body bg:         white (sections 3–5) · slate-50 (orientation + footer)
    Body text:       slate-800 (primary) · slate-600 · slate-500 · slate-400
    CTA / links:     blue-600

  Layout
    Page max-width:  3xl for content sections · 6xl for footer
    Alignment:       centered mx-auto throughout
    Mobile:          single column throughout
    Breakpoints:     sm (cards 2-up) · md (footer 3-up)

  Typographic scale (homepage only)
    H1:              text-4xl → text-5xl (responsive) · font-bold · tracking-tight
    Hero subtitle:   text-lg · text-blue-200
    Card name:       text-sm · font-semibold · text-slate-800
    Card desc:       text-xs · text-slate-600 · leading-snug
    Card CTA:        text-xs · text-blue-600 · font-medium
    Callout label:   text-sm · font-medium · text-slate-800
    Callout desc:    text-xs · text-slate-500
    Callout link:    text-sm · text-blue-600
    Orientation:     text-sm · text-slate-600 · leading-relaxed
    Attribution:     text-xs · text-slate-400
    Footer col heads:text-sm · font-semibold · text-slate-700
    Footer body:     text-sm · text-slate-500

  Interactions
    Search:          focus ring (ring-2 ring-blue-500 border-blue-500)
                     dropdown appears at ≥2 chars · outside-click close
                     clear button on non-empty input
    School cards:    border color shift on hover
    Compare link:    hover:underline
    Attribution:     hover:underline on "About this site"
    Footer links:    underline default · hover:text-slate-700

  Visual weight hierarchy (strongest → weakest)
    1. Hero + search   dominant — full-width dark section, above fold
    2. School cards    primary navigation — 4 colored cards, above fold
    3. Orientation     low weight — small text, below fold on most screens
    4. Compare callout secondary CTA — bordered box, low visual prominence
    5. Attribution     minimal — xs text, easily skipped
    6. Footer          utility — 3-col, standard reference

══════════════════════════════════════════════════════════════
  DESIGN OBSERVATIONS FOR PLANNING
══════════════════════════════════════════════════════════════

  - Homepage is almost entirely a navigation surface, not a
    content surface. The only real user actions are: search,
    or pick a school. Everything else is explanatory text.

  - No scale or coverage signals anywhere above the fold.
    The site has 107+ active degrees and 1,600+ courses but
    nothing communicates that to a first-time visitor.

  - School cards are the primary browse path but they go to
    /schools/{slug}, not /programs or /courses. A visitor
    picking "School of Technology" gets school context, not
    a direct degree list.

  - Compare callout is significantly underweighted. It is the
    most differentiated feature on the site — buried below
    the fold in a small bordered box after the orientation
    paragraph. Easy to miss.

  - The orientation paragraph is below the fold on most
    screens. It functions as a secondary clarifier, not an
    above-fold value statement.

  - Search covers both courses and degrees but gives no
    indication of scope before a query. Placeholder
    "Search degrees or courses…" is the only hint.

  - Timeline, Methods, and Data are hidden from the top nav
    entirely. They exist only via /about (Methods, Data,
    Timeline) or the footer (Methods, Data). Power-user
    features, effectively invisible to casual visitors.

  - Nav says "Colleges" but routes use /schools/ and the
    app internally refers to "schools." Mild terminology
    inconsistency between nav label and route/codebase.

  - The footer repeats "WGU Atlas" as a column header.
    Paired with "Created by WGU-DataNinja" and the
    independence statement, it functions as the product's
    identity statement — but it's at the very bottom.
```
