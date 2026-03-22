# Course-Page Enrichment — Session 1 Artifact

**Created:** 2026-03-21 (Session 1)
**Workstream:** `_internal/course_pages/`
**Purpose:** Preserve planning inputs and design cohort for the course-page enrichment work area. This is the authoritative starting-state document for course-page design sessions.
**Status:** Planning inputs captured. No implementation started.

---

## 1. Context Packet

### What Atlas is

A static Next.js reference/explainer site over the WGU course catalog. Stack: Next.js App Router, TypeScript, Tailwind, static export → GitHub Pages (`/wgu-atlas`). Runtime reads prebuilt JSON artifacts from `public/data/`. Simplicity and reproducibility are hard constraints.

### What course pages are now

Route: `/courses/[code]`
Source: `src/app/courses/[code]/page.tsx`

Current course pages are catalog/history-first. They show:
- Course code, CUs, active/retired status
- Catalog description (labeled with source date)
- Compact facts bar (first seen, status, degree appearances)
- Included in Current Degrees list (linked to program pages)
- Previously appeared in Retired Degrees list
- Title variants
- Notes/confidence caveats

What they do not yet show:
- Guide-derived description or competency bullets
- Cert signals / badges
- Prereq requirements
- Reverse-prereq relationships
- Capstone callout
- Program-contextual framing

### What the guide layer provides for course pages

The program-guides workstream is closed. Its outputs are the input for this workstream.

**`data/program_guides/enrichment/course_enrichment_candidates.json`**
- 751 canonical courses with guide-derived data (descriptions, competency bullets, program context)
- 730 have at least one description; 729 have at least one competency set
- 74 courses have 2–4 description variants (same course, different guide text across programs)
- 185 courses have 2–6 competency variant sets
- 656 courses have exactly 1 description (stable, single-variant)
- 544 courses have exactly 1 competency set (stable)
- 21 courses have 0 descriptions (sparse)

**`data/program_guides/cert_course_mapping.json`**
- 9 auto-accepted cert→course mappings (HIGH confidence, 3+ programs, ready to ship)
- 21 review-needed rows (editorial judgment required)
- Ready certs: CompTIA A+, CompTIA Network+, CompTIA Security+, CompTIA Project+, CompTIA Cloud+, AWS Certified, Praxis exam (2 courses, degree-only flag)

**`data/program_guides/prereq_relationships.json`**
- 50 auto-accepted prereq relationships (HIGH confidence, explicit course-to-course, ready to ship)
- 21 review-needed (includes 16 nursing cumulative-sequence rows, 1 inverted-capture)
- Type distribution: 51 explicit-course-prereq, 3 code-anchored, 16 cumulative-sequence, 1 inverted-capture

**`data/program_guides/degree_level_cert_signals.json`**
- NCLEX-RN (BSPRN), CPA Exam (MAcc family) — degree-level only; not primary course-page input

**Other guide artifacts available (for context):**
- `data/program_guides/sp_family_classification.json` — SP category per program
- `data/program_guides/sp_families.json` — 7 named program families
- `data/program_guides/guide_anomaly_registry.json` — 9 anomaly handling rules
- `data/program_guides/parsed/*_parsed.json` — full per-program parsed guide content

### Provenance clarity rules (carry forward from degree pages)

- Catalog description = official WGU text → labeled "WGU Catalog [date]"
- Guide description = from program guidebook → must be labeled with guide source
- Guide-derived content is richer but context-dependent; catalog description is authoritative and stable
- Never surface guide content without provenance attribution
- Flag when a field is context-dependent vs. stable/core

---

## 2. Current `/courses/[code]` Page Structure

### Layout

Max width container (`max-w-4xl`), top padding, single-column. No sidebar. No tabs.

### Breadcrumb

```
Courses  ›  {code}
```

### Header

```
[{code}]  [{N} CUs]  [Active | Retired]
{canonical_title_current}                  ← H1, text-3xl bold
{current_college}                          ← muted subtitle if present
Last in catalog: {last_seen_edition}       ← retired only
```

### Section 1: About This Course

Conditional — only shown if `catalogDesc.description` exists.

```
─ About This Course    [WGU Catalog 2026-03]

  "{catalogDesc.description}"   ← blockquote, border-left blue

  Official catalog text — WGU-authored.
```

Data source: `getCourseDescription(code)` → `public/data/course_descriptions.json`

### Section 2: Compact Facts Bar

Inline row on grey background:

| Label | Value | Condition |
|---|---|---|
| First in catalog | `course.first_seen_edition` | always |
| Status | Active / Retired | always |
| Last seen | `course.last_seen_edition` | retired only |
| Current degrees | `course.current_program_count` | active only |
| Total degree appearances | `course.historical_program_count` | always |
| Colleges (historical) | count | only if `collegesSeen.length > 1` |

### Section 3: Included in Current Degrees

```
─ Included in Current Degrees ({N})

  [Degree Name]    ← linked to /programs/{code} when resolvable
  ...
```

### Section 4: Previously Appeared in Retired Degrees

```
─ Previously Appeared in Retired Degrees ({N})   ← muted

  [Degree Name]   from {first_seen}
  ...
  Showing 50 of {N} — full history in the downloadable dataset.
```

### Section 5: Also Known As

```
ALSO KNOWN AS IN CATALOG
  {variant_title}   ← monospace, one per line
  {title_variant_detail}  ← footnote if present
```

### Section 6: Notes

```
[amber warning box]
Note: {notes_confidence ?? notes}
```

### Back link

```
← Back to Courses
```

### Data pipeline

| Function | Source | What it provides |
|---|---|---|
| `getCourseDetail(code)` | `public/data/courses/{code}.json` | Catalog-derived facts |
| `getCourseDescription(code)` | `public/data/course_descriptions.json` | Catalog description text |
| `getPrograms()` | catalog programs data | Status lookup for appearance splitting |
| `getHeadingToProgramCode()` | internal map | Resolves program names to linkable codes |
| `getAllCourseCodes()` | `data/canonical_courses.json` | Static params generation |

---

## 3. Key Session Takeaway

**Course-page design should be driven by course-shape groups, not a generic single-page template.**

The guide layer adds multiple distinct block types (description, competencies, cert badge, prereq, reverse-prereq, capstone callout). These blocks do not apply uniformly. A course may have one, several, or none. The description and competency fields can have 0–4 variants per course, and the right display policy differs by variant type (cosmetic vs. meaningful vs. program-specific).

The correct design approach is:
1. Define the set of possible new block types
2. Define when each block appears (conditions)
3. Define variant-handling policy for description and competency fields
4. Design around representative course shapes, not the average course
5. Determine fallback behavior for sparse or zero-payload cases

The page system that emerges will have at least five distinct display modes:
- **Default enriched page** — stable guide description + competencies + (optionally) cert or prereq
- **Variant-aware page** — multi-variant description or competency sets, needs policy-driven display
- **Relationship-heavy page** — prereq, reverse-prereq, or both
- **Capstone page** — capstone callout block, often with prereq
- **Sparse fallback page** — no guide payload; current catalog-only layout holds

Plus one special case:
- **Nursing cumulative-sequence case** — not representable as a standard "Requires: X" block

---

## 4. Course-Shape Groups

The following shape groups are needed for course-page design. Each determines which new blocks appear and how they behave.

| Shape | Key characteristics | New blocks added |
|---|---|---|
| Stable enriched | 1 description, 1 competency set | guide description, competencies |
| Meaningful multi-variant | 2–4 descriptions with real content difference (e.g., C++ vs Python) | guide description with variant handling, competencies with variant handling |
| Near-identical/cosmetic multi-variant | 2–4 descriptions differing only by punctuation/capitalization | guide description (pick-one policy), competencies (variant note or merge) |
| Cert-mapped | auto-accepted cert→course mapping present | cert badge/block |
| Prereq-bearing | auto-accepted "requires X" relationship present | prereq block |
| Reverse-prereq | this course is listed as a prereq for downstream courses | "is prerequisite for" block |
| Capstone | capstone signal from guide | capstone callout block |
| Cumulative-sequence nursing | prereq = "all prior MSN Core + NP Core courses" — no code resolution | special sequence note (or deferred until design is ready) |
| Sparse / no-guide-payload fallback | 0 descriptions, 0 competency sets in enrichment file | no new sections; catalog-only layout |

---

## 5. Design Cohort (10 Courses)

Selected to cover all shape groups. Not a random sample.

---

### Course 1 — Stable enriched + cert (C178)

**C178 — Network and Security - Applications**
4 CUs · Active · College of IT

Current page: catalog description present · 6 current-degree appearances

Guide payload:
- Descriptions: **1** (stable)
- Competency sets: **1** (stable)
- Cert: **CompTIA Security+** (auto-accepted, 6 programs, HIGH)
- Prereq requirement: none
- Is prereq for: none
- Capstone: no

Description: "Network and Security - Applications prepares learners for the CompTIA Security+ certification exam. The course introduces learners to skills in identifying threats, attacks, and vulnerabilities to organizational security. The learner will also gain skills in designing security solutions for enterprise infrastructures and architectures, as well as in implementing security solutions across hardware, applications, and network services."

Competency sample: analyzes information security controls · designs security solutions · implements security solutions

SP context: term 5 in most programs; term 8 in BSIT/MSITUG

New blocks: guide description · competencies · cert badge
**Shape: stable enriched + cert**

---

### Course 2 — Stable enriched + cert + prereq (C480)

**C480 — Networks**
4 CUs · Active · College of IT

Current page: catalog description present · 6 current-degree appearances

Guide payload:
- Descriptions: **1** (stable)
- Competency sets: **1** (stable)
- Cert: **CompTIA Network+** (auto-accepted, 6 programs, HIGH)
- Prereq requirement: **requires D315 (Network and Security - Foundations)** (auto-accepted, HIGH, 6 programs)
- Is prereq for: none
- Capstone: no

Description: "Networks introduces skills in configuring networking components and a network infrastructure… The course prepares learners for the CompTIA Network+ certification exam. Network and Security - Foundations is a prerequisite for this course."

SP context: term 3 most programs; term 7 BSIT/MSITUG

New blocks: guide description · competencies · cert badge · prereq requirement
**Shape: stable enriched + cert + prereq — richest non-capstone case**

---

### Course 3 — Multi-variant meaningful (C169)

**C169 — Scripting and Programming - Applications**
4 CUs · Active · College of IT

Current page: catalog description present · 3 current-degree appearances (BSCS, BSDA, MSCSUG)

Guide payload:
- Descriptions: **3 variants — meaningfully different**
- Competency sets: **3 variants**
- Cert: none
- Prereq: 1 variant only mentions "Introduction to Programming in Python is a prerequisite" (BSDA framing)
- Capstone: no

Description variants:
1. BSCS/MSCSUG (C++ framing): "explores the various aspects of the C++ programming language by examining its syntax, the development environment, and tools and techniques to solve some real-world problems"
2. BSDA (Python framing): "explores the various aspects of the Python programming language… Introduction to Programming in Python is a prerequisite for this course"
3. MSCSUG (C++ again, different intro sentence): "In this undergraduate course students explore the various aspects of the C++ programming language…"

Design note: The course content genuinely differs by program — C++ in CS track, Python in DA track. A single "primary description" rule suppresses a real fact. This is the critical multi-variant policy case.

New blocks: guide description (variant-aware) · competencies (variant-aware)
**Shape: meaningful multi-variant — key policy case**

---

### Course 4 — Multi-variant cosmetic/wide-coverage (C165)

**C165 — Integrated Physical Sciences**
3 CUs · Active · General Education

Current page: catalog description present · 28+ current-degree appearances

Guide payload:
- Descriptions: **2 variants — near-identical** (difference: "earth sciences" vs "Earth sciences"; "practical, everyday" vs "practical and everyday")
- Competency sets: **3 variants**
- Cert: none
- Prereq: none
- Capstone: no

Description variants:
1. "…physics, chemistry, and earth sciences. Course materials focus on scientific reasoning and practical, everyday applications…"
2. "…physics, chemistry, and Earth sciences. Course materials focus on scientific reasoning and practical and everyday applications…"

Source programs: 28+ spanning Business, Health, Technology, Education colleges

Design note: A general-education course appearing across most WGU programs. Descriptions differ only cosmetically → pick-one policy resolves trivially. Three competency variants with wide program spread need attribution or merge rule.

New blocks: guide description · competencies (variant handling needed)
**Shape: cosmetic multi-variant + wide-coverage course**

---

### Course 5 — Reverse-prereq (D426)

**D426 — Data Management - Foundations**
3 CUs · Active · College of IT

Current page: catalog description present · 3 current-degree appearances (BSCS, BSCSIA, BSIT)

Guide payload:
- Descriptions: **2 variants — near-identical** (punctuation only)
- Competency sets: **2 variants**
- Cert: none
- Prereq requirement: none (guide text: "No prerequisites are required for this course")
- **Is prereq for: C170 (Data Management - Applications) AND D191 (Advanced Data Management)** — HIGH confidence, 8 and 4 programs respectively
- Capstone: no

SP context: term 1 in BSCS; term 7–8 in BSIT/BSCSIA

Description: "Data Management Foundations offers an introduction in creating conceptual, logical and physical data models. Students gain skills in creating databases and tables in SQL-enabled database management systems, as well as skills in normalizing databases. No prerequisites are required for this course."

New blocks: guide description · competencies · reverse-prereq block ("Prerequisite for: Data Management - Applications · Advanced Data Management")
**Shape: reverse-prereq provider**

---

### Course 6 — Prereq-bearing downstream (C170)

**C170 — Data Management - Applications**
4 CUs · Active · College of IT

Current page: catalog description present · 8 current-degree appearances

Guide payload:
- Descriptions: **1** (stable; prereq mentioned in description text)
- Competency sets: **3 variants** (8 source programs → 3 distinct bullet sets)
- Cert: none
- **Prereq requirement: requires D426 (Data Management - Foundations)** (HIGH confidence, 8 programs)
- Is prereq for: none
- Capstone: no

SP context: term 1 BSCS; term 3–7 others

Description: "Data Management - Applications covers conceptual data modeling and introduces MySQL… The following course is a prerequisite: Data Management - Foundations."

Design note: Prereq is already embedded in the guide description text. The prereq block and the description will both surface the same relationship — coordinate display to avoid redundancy.

New blocks: guide description · competencies (3 variants) · prereq requirement
**Shape: prereq-bearing + multiple comp variants**

---

### Course 7 — Cert-mapped project management (C176)

**C176 — Business of IT - Project Management**
4 CUs · Active · College of IT

Current page: catalog description present · 6 current-degree appearances

Guide payload:
- Descriptions: **1** (stable)
- Competency sets: **2 variants**
- **Cert: CompTIA Project+** (auto-accepted, 6 programs, HIGH)
- Prereq: none
- Capstone: no

SP context: term 3 (BSIT); term 6–7 (others)

Description: "In this course, students will build on industry standard concepts, techniques, and processes to develop a comprehensive foundation for project management activities… This course prepares students for the following certification exam: CompTIA Project+."

New blocks: guide description · competencies (2 variants) · cert badge
**Shape: cert-mapped + slight comp variant**

---

### Course 8 — Capstone + prereq (C824)

**C824 — Nursing Leadership and Management Capstone**
2 CUs · Active · College of Health Professions

Current page: catalog description present · 3 current-degree appearances (MSNULM, MSRNNULM, PMCNULM)

Guide payload:
- Descriptions: **2 variants — near-identical** (one adds "This course is eligible for an In Progress grade")
- Competency sets: **1** (stable; single synthesis statement)
- Cert: none
- **Prereq requirement: requires C823 (Nursing Leadership and Management Field Experience)** (HIGH confidence, 3 programs)
- Is prereq for: none
- **Capstone: yes** — explicitly "final course in the MSN Leadership and Management program"; healthcare improvement project (HIP) evaluation

SP context: term 4 (MSNULM); term 8 (MSRNNULM); term 2 (PMCNULM)

Single competency: "The learner integrates and synthesizes competencies from across the degree program and thereby demonstrates the ability to participate in and contribute value to the chosen professional field."

New blocks: guide description · competencies · prereq requirement · capstone callout
**Shape: capstone + prereq**

---

### Course 9 — Cumulative-sequence nursing case (D118)

**D118 — Adult Primary Care for the Advanced Practice Nurse**
Source programs: MSNUFNP, PMCNUFNP

Guide payload:
- Description: likely present (NP clinical courses have guide content)
- Competency sets: likely present
- Cert: none
- **Prereq type: cumulative-sequence** — "All MSN Core courses and NP Core courses are required prior to taking this course"
  - normalized_prereq_code: null (unresolvable to single course code)
  - review_status: review-required
  - recovery_method: template_parse
- Capstone: no

16 nursing rows in the prereq file follow this exact pattern. None can be represented as "Requires: [Course X]." A standard prereq block cannot handle this.

Design choices:
1. Show a "Sequence note" block with descriptive text ("Requires completion of all MSN Core and NP Core courses")
2. Suppress until a dedicated sequence display model is designed
3. Link to the program page where the sequence is visible

**Shape: cumulative-sequence prereq — must be explicitly deferred or given distinct handling**

---

### Course 10 — Sparse / no-guide-payload fallback (C216)

**C216 — MBA Capstone**
4 CUs · Active · College of Business

Current page: standard layout (catalog desc if present, facts bar, 1 current-degree appearance: MBA)

Guide payload:
- Descriptions: **0** — empty array
- Competency sets: **0** — empty array
- Cert: none
- Prereq: none
- Capstone: yes by title only — but no guide payload to populate a callout block
- SP context: MBA, term 4

21 courses in the enrichment file are in this state. The course code was matched to a guide, but no description or competency content was extracted.

Design: page falls back entirely to current layout. No new sections are added. If capstone is inferred from title only, decide whether to surface a minimal callout or suppress entirely.

**Shape: sparse — tests the "no new sections" fallback**

---

## 6. Cohort Summary Table

| # | Code | Title | Desc | Comp variants | Cert | Prereq req | Is prereq for | Capstone | Sequence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | C178 | Network and Security - Applications | 1 | 1 | CompTIA Security+ | — | — | — | — |
| 2 | C480 | Networks | 1 | 1 | CompTIA Network+ | D315 | — | — | — |
| 3 | C169 | Scripting and Programming - Applications | **3 (meaningful)** | 3 | — | (1 variant) | — | — | — |
| 4 | C165 | Integrated Physical Sciences | 2 (cosmetic) | 3 | — | — | — | — | — |
| 5 | D426 | Data Management - Foundations | 2 (cosmetic) | 2 | — | — | C170, D191 | — | — |
| 6 | C170 | Data Management - Applications | 1 | **3** | — | D426 | — | — | — |
| 7 | C176 | Business of IT - Project Management | 1 | 2 | CompTIA Project+ | — | — | — | — |
| 8 | C824 | Nursing Leadership and Management Capstone | 2 (cosmetic) | 1 | — | C823 | — | **yes** | — |
| 9 | D118 | Adult Primary Care for Adv Practice Nurse | likely | likely | — | all-prior-sequence | — | — | **yes** |
| 10 | C216 | MBA Capstone | **0** | **0** | — | — | — | title only | — |

---

## 7. What the Cohort Covers for Design

| Design question | Course(s) |
|---|---|
| Default enriched page layout | C178 |
| Cert badge placement and wording | C178, C480, C176 |
| Prereq block ("Requires: X") | C480, C170, C824 |
| Prereq embedded in guide description text | C170, C480 |
| Reverse-prereq block ("Prerequisite for: Y") | D426 |
| Capstone callout with guide payload | C824 |
| Capstone callout without guide payload (title-only signal) | C216 |
| Variant policy — meaningful content difference | C169 |
| Variant policy — cosmetic/near-identical | C165, D426 |
| Competency variants across wide program spread | C165, C170 |
| Cumulative-sequence prereq handling or deferral | D118 |
| Sparse/no-payload fallback | C216 |

---

## 8. Open Design Questions (Unresolved)

These must be answered before implementation planning.

1. **Multi-variant description policy** — When a course has 2–4 description variants, what goes on the page?
   - Pick primary (first, most common, highest-confidence anchor program)?
   - Show all with program attribution labels?
   - Pick-one for cosmetic variants; show multiple for meaningful variants?

2. **Multi-variant competency policy** — Same question for competency bullet sets.
   - Same policy as description, or different?
   - How to label "In [Program]: …" if showing multiple?

3. **Capstone publication rule** — What qualifies a course for a capstone callout?
   - Guide capstone field only (programmatic)?
   - Title-only inference (e.g., C216 "MBA Capstone")?
   - Both, or only the explicit signal?

4. **Cumulative-sequence nursing handling** — Defer entirely, or surface a descriptive sequence note?

5. **Prereq/description redundancy** — Some guide descriptions already contain the prereq text ("X is a prerequisite for this course"). Coordinate display so the prereq block and description don't duplicate.

---

## 9. Next Step

Produce a **shape-disposition / display-policy artifact** that answers the open questions above and defines exact display rules per shape group. That artifact is the gate before implementation planning begins.

Working area for that artifact: `_internal/course_pages/`
