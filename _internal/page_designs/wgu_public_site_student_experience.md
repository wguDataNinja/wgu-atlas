# WGU Public Site Student Experience — Degree Exploration Baseline

Reference capture date: 2026-03-20
Last updated: 2026-03-20
Status: **in progress — substantially expanded from initial baseline; further session work planned**

Related docs:
- `catalog_raw_analysis.md`
- `source_vs_atlas_program_entry.md`
- `compare_page.md`
- `homepage_design_session_2026-03.md`

---

## Important framing note

The raw WGU catalog is not the primary way most students first explore WGU degrees, courses, and options.

Students typically start on WGU's public website — the official marketing and navigation surface at wgu.edu — not with a PDF catalog.

This doc exists to capture the **official web exploration baseline** so Atlas can later be evaluated against both:

1. The raw WGU catalog (covered in `catalog_raw_analysis.md` and `source_vs_atlas_program_entry.md`)
2. The public WGU website student experience (this doc)

Until both baselines are documented, we only have half the picture of what Atlas improves on.

---

## 1. Purpose of this doc

This document preserves how students actually encounter and explore WGU on the public website, as distinct from the raw catalog experience.

Its goal is to capture:
- the official navigation and degree-discovery flow
- what a student sees before they ever open the catalog
- how WGU publicly presents program options, course information, and official supporting resources
- where that experience is strong or weak as a student research surface

This is a product-argument artifact and a planning baseline, not an implementation spec.

---

## 2. Why the public site baseline matters

Most Atlas comparison work to date has benchmarked against the raw catalog.

That benchmark is valid and important. But it understates Atlas's value if the public-site experience is also weak.

If wgu.edu's degree-exploration surface is:
- marketing-first rather than reference-first
- funnel-oriented rather than browse-oriented
- poor at supporting comparison, course exploration, or outcome visibility

...then Atlas's claim is not just "better than the catalog" but "better than the student's default research experience."

That is a stronger and more truthful claim.

Conversely, if the public site is actually a strong exploration surface, that changes what Atlas needs to offer to stand out.

This doc exists to answer which of those is true — and the answer turns out to be more nuanced than either extreme.

---

## 3. Scope of the official public-site exploration experience

The official WGU public-site exploration experience is broader than:
- the raw catalog
- the all-degrees grid
- individual degree pages

The public site currently exposes multiple overlapping exploration systems:
- degree discovery surfaces (taxonomy, browse, compare)
- long-form program-detail pages
- guided recommendation / quiz flow
- alternative-start entry pages (intro-term, single-course)
- certificate and standalone-course product pages
- licensure / compliance / teacher-preparation utility pages
- program guides — linked high-value official academic PDFs

This matters because the official site is not one coherent research surface. It is a set of overlapping discovery, enrollment, and compliance surfaces that students must navigate across.

---

## 4. Global navigation baseline

### Observed top navigation

Current wgu.edu top nav (observed):
- Online Degrees
- About WGU
- Tuition & Financial Aid
- Admissions & Transfers
- Student Login
- More

### What this tells us
- Degree exploration is the first nav item — it is clearly the primary entry for prospective students.
- The nav does not lead with a school index or an open degree list. It leads with a category-gated dropdown.
- Navigation paths are marketing/enrollment-first, not reference-first.

---

## 5. Online Degrees taxonomy

### The menu is a deeper taxonomy layer than it first appears

The Online Degrees nav is not just a simple seven-option menu. It is an official taxonomy layer organizing offerings simultaneously by school, degree level, credential type, pathway type, and support/utility page.

### Top-level degree-entry buckets
- Business
- Education
- Technology
- Health & Nursing
- Courses and Certificates
- All Degrees
- Explore Your Options

### Expanded submenu structures (observed)

**Business**
- Bachelor's
- Master's
- Certificates
- Advanced Accounting Courses

**Education**
- Bachelor's
- Master's
- Endorsements
- Licensure

**Technology**
- Bachelor's
- Master's
- Certificates
- 3rd Party Certifications
- Accelerated

**Health & Nursing**
- Bachelor's
- Master's
- Licensure
- Certificates

**Courses and Certificates**
- Certificates
- Recently Added
- Courses

### What the nav is actually doing

The nav organizes offerings by school, degree level, credential type, pathway type, and support/utility pages at once. It is doing hidden recommendation work — steering users through school-first, level-first, certificate, licensure, accelerated-path, and single-course discovery simultaneously.

This should be read as an official exploration map — but one that is fragmented across multiple UI layers rather than presented as a unified index.

### Cross-listing as an official pattern

WGU cross-lists programs across school menus, which shows that its official exploration model partially recognizes student-interest adjacency beyond administrative school boundaries.

Examples observed:
- Health Information Management appears under Business and Technology but belongs to the Leavitt School of Health
- Information Technology Management appears in Technology but is from Business
- User Experience Design appears in Technology but is from Business
- Healthcare Administration appears in Health & Nursing but is from Business
- MBA Information Technology Management appears in Technology but is from Business
- Education Technology and Instructional Design appears under multiple school groupings

### Analysis

The official classification is more sophisticated than it looks at first. The problem is not lack of structure; the problem is that the structure is distributed across nav layers, browse pages, compare surfaces, long-form program pages, utility pages, and alternative product pages — not consolidated into a single legible index.

---

## 6. Explore Your Options — guided quiz/recommendation flow

### What it is

`/quiz/program.html` is a guided recommendation funnel framed as:
- "Discover your best path."
- "Take a minute to answer — this is just for you."
- Low-pressure disclaimer language
- GET STARTED CTA
- Question flow based on student motivations and interests

### How to characterize it

This is an official "help me choose" entry mode. It is not a browse or compare model. It is a recommendation funnel that routes users toward suggested degrees based on self-reported preferences.

### Atlas implication

Atlas should not imitate this as a core structure. This is an official external chooser for students who do not yet have a degree family in mind. At most, Atlas might later reference or link to it. Atlas's core value is structured reasoning, inspection, and comparison — not quiz-based recommendation.

---

## 7. All Degrees browse surface

### Default state

The default all-degrees page is visually noisy and weakly organized:
- mixed schools
- mixed credential levels
- mixed offer types
- no strong default grouping by school, level, or intent
- requires substantial scanning to identify relevant options

This makes the page weak for students who already have a degree family or college in mind. They must manually recover school context, degree level, offering type, and adjacency to related options.

### More Details expansion findings

Expanding a degree card from the default grid reveals genuinely useful facts:
- duration
- tuition
- number of courses
- skills list
- short summary
- sometimes a related compare link

This makes the surface more decision-relevant at the individual-card level.

### Still-limiting factor

Even with expanded cards, the page remains weak globally. The student must locate the right card, expand cards one by one, and manually synthesize across multiple expansions. The page is locally informative but not globally legible.

**Strong baseline phrasing:** WGU does provide useful facts in the browse layer, but those facts are trapped in per-card expansions inside a mixed grid rather than surfaced in a strong default organizational structure.

---

## 8. Official compare baseline

### What exists

WGU provides a real public compare flow:
- users select programs from the all-degrees grid
- a compare tray appears at the bottom of the screen
- users are routed to a dedicated compare page
- compare supports up to 3 degrees

### Comparison schema observed

The compare surface is built around a stable set of headline metrics:
- average time to completion
- tuition per 6 months
- average salary increase
- career opportunities
- View Degree CTA per column

### Sibling program comparison confirmed

The compare flow works not only for obviously different programs, but also for close sibling programs.

Observed sibling comparison example:
- Computer Science – B.S.
- Software Engineering – B.S.
- Cloud and Network Engineering – B.S.

WGU's compare should be treated as a real part of the official exploration baseline, not a decorative or trivial feature.

### Limits of the compare model

Even in close-sibling cases, the compare remains narrow:
- no course-by-course comparison
- no curricular overlap view
- no explicit structural differentiation
- no direct explanation of shared vs divergent program composition
- no relationship map between adjacent degrees

WGU compare supports high-level narrowing well — speed, cost, salary framing, role-family framing. It does not support deep academic reasoning.

### Page posture

The compare page is still embedded inside a broader persuasion shell:
- hero framing
- testimonial/reviews
- FAQ
- support messaging
- employer-preparedness claims
- start-date / apply nudges

It is a useful compare tool, but not a clean research workspace.

### Atlas implication

Do not frame Atlas as "the only way to compare." The more truthful contrast is:
- WGU helps students compare headline outcomes
- Atlas helps students compare program structure

---

## 9. Official program-detail pages: shared long-form template

### General characterization

Official WGU degree pages are not shallow. They contain substantial student-useful information. But that information is presented inside long-form, CTA-heavy, conversion-shaped pages.

### Shared scaffold observed across program pages

Across multiple programs, the official template repeatedly includes:
- global header and nav
- breadcrumb
- degree label / program identity
- hero CTA
- accreditation/certification logos
- in-page section nav
- overview narrative
- stat cards (time, cost, salary)
- repeated next-start-date / apply bands
- course section with program guide link
- special requirements callout
- WGU-vs-traditional comparison block
- Why WGU / value-prop tiles
- cost/time section
- flexible schedule section
- testimonial
- career outlook / ROI section
- admissions block
- transfer block
- repeated micro-CTAs
- footer / chat

### Shared product read

The program pages are:
- individually rich
- academically more useful than the all-degrees grid or compare page
- still operationally inefficient for research, because students must scroll through repeated persuasion modules and normalize facts across separate pages manually

**The limitation is not lack of information; it is packaging.** The official site embeds meaningful academic and policy details inside enrollment-oriented long-form pages.

---

### 9.1 Representative program page: B.S. Computer Science

#### What it exposes
- breadcrumb and program identity
- accreditation signals
- section anchor nav
- top-level time/cost/salary metrics
- grouped course roster
- program guide link
- included certifications
- cost/time model
- admissions requirements
- transfer guidance
- career-outlook content
- related accelerated path

#### What makes it important

This page shows that official program pages do expose real academic inspection material: course categories, program size, program guide, requirements, certifications, admissions rules. A student who works through the page can extract meaningful research information.

#### What remains limiting

The useful material is embedded inside a repeated persuasion shell: multiple CTAs, WGU-vs-traditional comparison, "Why WGU?" block, testimonial, employer logos, repeated start/apply bands.

---

### 9.2 Representative program page: Nursing Informatics RN-to-MSN

#### What it adds beyond simpler program pages

This page shows that bridge and licensure-heavy programs include additional structures not present in simpler degree pages:
- bridge-path explanation
- BSN + MSN progression logic
- split undergrad/grad tuition
- field experiences
- compliance / safety notice
- RN-license-based admissions
- California PHN options
- state-/licensure-sensitive program context
- post-baccalaureate certificate / credential-on-the-way logic

#### Why it matters

This confirms that official program pages are not one flat template. They share a scaffold but include program-family-specific additions. Nursing pages foreground licensure, compliance, and pathway complexity far more explicitly than IT pages. This matters for the official-resource-discovery baseline and for how Atlas should handle licensure-linked programs.

---

### 9.3 Representative program page: B.S. Data Analytics

#### Important findings
- Hero includes cert framing with logos
- Overview explicitly presents a "three-lever" framing: programming skills, math skills, business influence skills
- Stat cards include average transfer credits alongside standard time/tuition metrics
- Course section is detailed and grouped; capstone requirement is visible
- IT cert section includes third-party certifications, optional certificates, and WGU-issued certificates
- FAQ section gives explicit policy explanations
- Advisory board is publicly named

#### What makes this page especially useful

This page shows that some WGU program pages expose:
- transfer-heavy framing
- policy rationale via FAQ
- advisory-board context
- both third-party certs and WGU certificate layers

#### Important FAQ items (preserved)

The FAQ explicitly answers:
- what to do if a student cannot meet eligibility requirements
- why certs/prereqs are required
- why certs older than five years are not accepted
- how self-pacing actually works
- what instructors do without lectures

These are official explanatory resources, not just marketing copy.

#### Advisory board

The page publicly names the Data Analytics Advisory Board. This is an official context layer that may matter later as attached evidence or institutional context.

---

## 10. Official-resource pages for education: licensure and student teaching

Education programs reveal that some official resources are major standalone pages linked from navigation — not just supplemental links buried within a single degree page.

### A. Student Teaching page

A standalone official resource page covering:
- required in-person clinical experiences and student teaching for education licensure programs
- minimum 65 hours of early/advanced clinicals
- full-time supervised student teaching lasting at least 60 days
- mentor teacher requirements
- culturally competent practitioner expectations
- program gateways and application checkpoints
- list of degree programs requiring student teaching
- links to related degree pages

**Why it matters:** This is a resource/support/compliance page embedded in the exploration experience. It links policy and compliance information directly to specific degree cards. It is not marketing — it is a real official preparation requirement surface.

### B. Teaching License/Certification page

A standalone explainer and routing page covering:
- what a teaching license/certification is
- difference between initial licensure and adding to an existing license
- who needs licensure
- grouped degree lists tied to initial licensure or adding to license
- FAQ covering reciprocity, duration, demand, alternative routes, etc.

**Why it matters:** This is a significant public explanation layer for students trying to understand licensure path types. It combines concept explanation with degree routing.

### C. State Licensure Information page

A state-by-state compliance and disclosure hub covering:
- state-specific teacher licensure information for all states and territories
- federal/NC-SARA compliance framing
- consumer complaint / refund / Title IV links
- licensure contact email
- a lighter promotional block linking to "How to Become a Teacher"

**Why it matters:** This is a high-value official-resource page. It is useful, but structurally separate from individual program pages — showing how important public official context may live off to the side rather than attached tightly to a degree entry.

### Product interpretation

Education exploration on the official site is deeply entangled with licensure, state compliance, student teaching, endorsements, and credential-path decisions. The site exposes these resources, but they live across multiple page types rather than in one integrated student research surface.

---

## 11. Official page-type taxonomy

The public site includes substantially more page types than the catalog or a simple degree index.

### Page types now observed
- top-nav taxonomy / exploration map
- all-degrees browse surface
- compare pages
- official program-detail pages (standard)
- official program-detail pages (bridge / licensure-heavy)
- official program-detail pages (accelerated path)
- guided recommendation quiz
- alternative-start / intro-term offer pages
- standalone course / advanced-course product pages
- licensure / compliance / teaching-preparation pages
- certification mapping pages
- program guides (linked academic artifact PDFs)

### Why this matters

The official public-site student experience is heterogeneous. It mixes discovery surfaces, product pages, support/compliance resources, enrollment funnels, and linked academic documents. That breadth helps coverage but contributes to fragmentation — students must move across multiple page types to complete a single research task.

---

## 12. Alternative-start page type: Personalized Start / Single Course Offerings

### What it is

This page is an alternative-start offer page, not a degree-detail page. It presents:
- intro-term / low-commitment on-ramp framing
- one or two courses
- $25 offer framing
- support features
- degree-credit carryover
- single-course catalog list
- enrollment process
- federal-aid caveat

### Product interpretation

This is an official lower-risk entry path. It is not a research surface.

### Atlas implication

Atlas probably does not want to emulate this page type directly, but may later want to note it, link to it, or contextualize it as an official on-ramp option. It should not be confused with Atlas's degree or course pages.

---

## 13. Standalone advanced-course product page type: Advanced Accounting Courses

### What it is

A standalone graduate-level non-degree course-product page, separate from the full-degree program pages.

### What it exposes
- target audience
- cost
- term length
- payment model
- requirements
- specific course list
- CPA-related value framing
- enrollment process

### Why it matters

This page shows that the public site includes course-marketplace-like offerings and standalone course products alongside full degree programs. This helps explain why the broader WGU public exploration environment can feel heterogeneous: it mixes full programs with alternate educational units and non-degree offerings.

---

## 14. Technology-specific certification mapping page

### What it provides

A degree-to-certification bundle mapping for IT programs, showing:
- which certs are included in each IT degree
- which degrees do not include certs
- accelerated-program cert bundle

### Why it is important

This is a valuable official mapping artifact. Degree pages and compare pages do not always show certifications in a normalized cross-program view.

### Important limitation

The page provides a degree → cert mapping, but does not provide:
- course → cert mapping
- sequencing or when the cert is earned
- whether each cert is tied to a specific course
- whether certs are required vs optional in a clean structured form

### Atlas implication

This is useful official context, but still incomplete for the cert/course structure Atlas would ideally want to expose.

---

## 15. Accelerated degree pages as a distinct official subtype

Accelerated degree pages are not ordinary single-degree pages. They are structured as:
- B.S. → M.S. pathways
- bridge programs
- fewer courses than separate completion
- split undergrad/grad tuition
- staged progression
- cert bundles spanning the combined path

Accelerated programs are a distinct official page type and program subtype. They should not be flattened into ordinary bachelor's or master's exploration when Atlas references or links them.

---

## 16. Program guides as a major official artifact layer

### Why this matters

Program guides appear to be one of the highest-value official WGU artifacts for Atlas. They may be more structurally useful than public degree pages for academic content.

### What a program guide contains

**A. Program metadata / versioning**
- version ID
- document date / effective date
- stable footer/version anchors

**B. Standard Path table**

This is a high-value structured layer containing:
- term-by-term sequence
- course title
- CUs per course
- term placement
- total courses
- implied total CUs
- total number of terms

This is the cleanest official source for default sequencing, pacing, program size, and term structure.

**C. Areas of Study section**

This is a second high-value layer containing:
- area of study / subject grouping
- course descriptions
- competency bullets
- capstone
- occasional prerequisite mentions
- occasional certification-prep mentions

This is the cleanest official source for course meaning, conceptual grouping, program-specific competencies, and implicit academic relationships between courses.

**D. Boilerplate sections (low value for parsing)**
- WGU model explanation
- transfer policy boilerplate
- accessibility/services/contact pages
- generic curriculum-change notices

These can generally be ignored for data extraction.

### Worked example: BSDA program guide

**Guide metadata:**
- Version ID: BSDA 202309
- Date: 5/1/23
- 21 pages
- clean text extraction
- Standard Path table extracted well
- full course descriptions extracted well
- competency bullets extracted well

**Standard Path findings:**
- 43 courses
- 8 terms
- course/CU/term table is clean and parseable
- term-by-term sequencing is explicit

**Areas of Study groups observed (BSDA):**
- Data Analytics
- Business of IT
- Scripting and Programming
- Business Core
- Data Management
- Business Management
- General Education
- Network and Security
- Full Stack Engineering
- Web Development
- Information Technology Management
- Software
- Data Science
- Computer Science
- Capstone

**Parseable signals:**
- area-of-study headers are strong anchors
- competency bullets follow recognizable patterns
- certification-prep mentions can appear inline in course prose
- prerequisites are sometimes embedded in prose
- page footers/version strings are easy to strip

### Product interpretation

Program guides should be treated as a major official artifact layer for Atlas, not just a linked supplement.

They are:
- more structured than public degree pages
- more academic than compare pages
- likely the best official source for sequence, curriculum, and course meaning at scale

---

## 17. Updated public-site design posture

### More accurate characterization

The official public site is not simply "marketing-first and shallow." It is better described as:
- broad
- heavily templated
- multi-surface
- conversion-aware
- partly structured
- academically richer at the program-guide and program-page layer
- still fragmented as a student research environment

### Revised synthesis

The site provides many of the pieces a serious student needs, but distributes them across:
- nav taxonomy
- mixed browse surfaces
- narrow compare pages
- long-form program pages
- utility/compliance pages
- linked program guides
- alternative-entry and non-degree product pages

**Strong summary:** The public site is broad and information-rich in places, but the student still has to do too much manual synthesis. The limitation is not lack of information — it is packaging and fragmentation.

---

## 18. Updated Atlas implications

### What not to claim

Do not frame Atlas as:
- the first place students can compare degrees (WGU has a real compare surface)
- the only place students can see courses (official program pages do include rosters)
- the only place with official context (program guides and utility pages exist)
- the only place with program information

Those claims are too broad given the official site.

### Stronger and more truthful contrast

Atlas improves on the official public-site experience by making official information:
- more legible
- more structurally organized
- easier to compare at the curriculum level (vs WGU's headline-metrics-only compare)
- easier to inspect across programs
- easier to connect across schools and adjacent paths
- easier to use without scrolling through repeated persuasion shells

### Most important homepage implication

The homepage should not try to imitate WGU's public site by becoming:
- a giant menu
- a huge card wall
- a general-purpose enrollment funnel
- a heterogeneous marketplace of all offer types

Instead it should prove that Atlas makes official WGU information more usable by:
- exposing structure
- clarifying relationships
- surfacing useful curriculum-level comparisons
- foregrounding academic composition and official context without enrollment-funnel wrapping

### Strong final framing

WGU's public site already proves that there is a lot of official material. Atlas's opportunity is not to add noise — it is to restructure that material into a clearer student-use guide.

---

## Appendix: official page families and high-value artifacts

### Official page families now observed
- taxonomy/menu pages
- browse pages
- compare pages
- standard program pages
- accelerated program pages
- bridge/licensure-heavy program pages
- quiz/recommendation pages
- intro-term offer pages
- standalone course/certificate pages
- licensure/compliance pages
- cert-mapping pages
- program-guide PDFs

### High-value official artifacts for future harvesting
- program guides
- IT cert mapping pages
- licensure/state-info pages
- teacher-preparation pages
- advisory-board sections (on applicable program pages)
- FAQ/policy explanation sections on program pages

---

## Open questions for future sessions

Questions now answered in this doc:
- ~~Where does "All Degrees" lead?~~
- ~~What does "Explore Your Options" lead to?~~
- ~~Is there any official compare flow on wgu.edu?~~
- ~~What do official program pages contain?~~
- ~~Are program guides accessible and parseable?~~

Remaining open questions:
- Are all school-level pages now documented? (Business, Education, Technology, Health & Nursing each need a dedicated landing-page read)
- Are learning outcomes / graduate competency statements visible on official program pages, or only in program guides?
- Are there official program pages for all active programs, or do some lack pages?
- What does a student see if they navigate from the official site to Atlas for the same program? Is the difference immediately legible?
- Are course-level pages publicly accessible on wgu.edu?
- How does the licensure/state-compliance surface differ for IT programs vs Education programs?
- Are advisory boards listed for programs other than Data Analytics?
- What is the current scope of programs with accessible program guides?

---

## Session handoff note

This doc has been substantially expanded from its initial baseline.

The following surfaces are now documented with real findings:
- global nav and Online Degrees taxonomy (§4, §5)
- Explore Your Options quiz flow (§6)
- All Degrees browse surface (§7)
- Official compare flow (§8)
- Official program-detail page template and three representative examples (§9)
- Education official-resource pages: student teaching, licensure, state compliance (§10)
- Official page-type taxonomy (§11)
- Alternative-start, advanced-course, cert-mapping, and accelerated page types (§12–§15)
- Program guides as a major official artifact layer with worked BSDA example (§16)
- Updated product posture and Atlas implications (§17, §18)

The following remain as future work:
- School-level landing page reads (Business, Education, Technology, Health & Nursing)
- Course-level discovery baseline on the public site
- Confirmed outcomes/competency-statement visibility on program pages
- Atlas-vs-official-site side-by-side comparison for at least one representative program

Homepage design can now proceed from a substantially more complete dual baseline (catalog + public site). The synthesis section in `homepage_design_session_2026-03.md` should be revisited once the remaining school-level and course-discovery gaps are filled.
