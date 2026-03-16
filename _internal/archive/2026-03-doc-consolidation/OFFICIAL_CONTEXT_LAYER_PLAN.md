Append this as a new internal planning document, for example:

_internal/OFFICIAL_CONTEXT_LAYER_PLAN.md

⸻

WGU Atlas — Official Context Layer Plan

Drafted: 2026-03-14
Purpose: define the strategy for discovering, structuring, and surfacing relevant official WGU website content alongside Atlas catalog entities.

⸻

1. Why this layer matters

WGU Atlas already has a strong foundation built from the public catalog archive:
	•	courses
	•	programs
	•	schools/colleges
	•	historical changes
	•	version history
	•	deprecated/current entity pages

But the catalog is only one part of WGU’s public information footprint.

The official WGU website contains a large amount of useful supporting material that is:
	•	public
	•	institution-authored
	•	relevant to student decision-making
	•	often difficult to discover directly
	•	not well connected to the catalog structure

Examples include:
	•	newsroom announcements
	•	school rename announcements
	•	program launch pages
	•	comparison articles
	•	certification advice pages
	•	program guide pages
	•	program guide PDFs
	•	career explainers
	•	school/program promotional pages
	•	pathway/track comparison pages

Atlas can become significantly more useful by helping students and researchers find the right official WGU pages at the right time.

This should become a first-class product layer.

⸻

2. Product strategy

Core positioning

Atlas should not become “the Reddit site.”

Instead, Atlas should lead with:
	1.	Official catalog facts
	2.	Related official WGU resources
	3.	Student discussion (later, clearly secondary)

This is strategically important.

Why official context comes first

Leading with official WGU pages:
	•	makes Atlas more useful immediately
	•	makes the site feel more like a public utility
	•	increases trustworthiness
	•	helps users find buried institutional material
	•	positions Atlas as a guide to official information, not just a tracker of changes
	•	gives Atlas an institutionally friendlier posture before Reddit integration

Desired user experience

When a student lands on:
	•	a course page
	•	a program page
	•	a school/college page
	•	eventually a certificate page or event page

they should be able to see not only:
	•	what the catalog says

but also:
	•	which official WGU pages may help them understand that entity better

Examples:
	•	an IT certification advice article on an IT-cert-linked course
	•	a Java vs C# comparison page on software engineering track pages
	•	a program guide PDF on a program page
	•	a school rename press release on a school page
	•	a launch article on a newly added program page

⸻

3. The “Official Context Layer”

This new layer should be treated as distinct from both:
	•	catalog facts
	•	Atlas interpretation

Recommended visible labeling

Use labels like:
	•	Related official WGU resources
	•	Recommended WGU resources
	•	Official context
	•	Helpful official WGU pages

Avoid labeling these as:
	•	catalog facts
	•	Atlas conclusions
	•	required reading

They are supporting, contextual, official resources.

⸻

4. Layer hierarchy across Atlas

Atlas should evolve to have this content stack on entity pages:

Layer 1 — Official catalog facts

Examples:
	•	current/deprecated status
	•	first seen / last seen
	•	source catalog edition
	•	roster
	•	outcomes
	•	description
	•	school/program/course relationships

Layer 2 — Related official WGU resources

Examples:
	•	program guides
	•	official comparison articles
	•	launch pages
	•	school rename press releases
	•	WGU advice pages
	•	school/program explainers

Layer 3 — Student discussion (later)

Examples:
	•	Reddit links
	•	discussion landing pages
	•	discussion summaries
	•	discussion freshness/context warnings

This order is intentional.

⸻

5. Why this is a major opportunity

The WGU public website appears to contain a large number of potentially relevant pages discoverable from:
	•	https://www.wgu.edu/sitemap.html
	•	program pages
	•	newsroom pages
	•	guide PDFs
	•	school/program landing pages
	•	explainer/comparison articles

Many of these pages are hard for students to find through ordinary browsing.

Atlas can create value by:
	•	indexing them
	•	classifying them
	•	matching them to relevant Atlas entities
	•	surfacing them in a clean, curated way

This makes Atlas more useful than either:
	•	the catalog alone
	•	the official site navigation alone

⸻

6. Example official WGU resource types

The master list should likely contain pages of these kinds.

A. School / institution context

Examples:
	•	school rename announcements
	•	school branding/positioning articles
	•	institutional strategy pages relevant to a school

Example:
	•	Leavitt School of Health rename article

B. Program guides

Examples:
	•	public program guide landing pages
	•	downloadable PDF program guides
	•	current standard path documents

These are likely high-value official current-state resources.

C. Program launch and update pages

Examples:
	•	new degree launch announcements
	•	new school/program rollout pages
	•	specialized program announcements

D. Comparison / decision-support articles

Examples:
	•	Java vs C# articles
	•	career path explainers
	•	program comparisons
	•	role-specific degree explainers

E. Certification-related resources

Examples:
	•	certification exam advice
	•	certification/value pages
	•	program/certification relationship articles
	•	certification preparation content

F. Career / pathway explainers

Examples:
	•	“what can you do with this degree”
	•	role-family articles
	•	school-specific career explainers

G. Program-specific public landing pages

Examples:
	•	current public program pages
	•	current admissions/program overview pages

⸻

7. Recommended product treatment

Do not treat these as primary facts

Atlas should not replace catalog facts with these pages.

Do treat them as useful contextual resources

They should be surfaced where they add student value.

Best page-level placements

Course pages
Potential official resource links:
	•	certification advice pages
	•	exam-related pages
	•	relevant school pages
	•	guide pages if tightly relevant

Program pages
Potential official resource links:
	•	program guide page
	•	program guide PDF
	•	launch page
	•	comparison article
	•	school-level program article
	•	career outcomes article

School/college pages
Potential official resource links:
	•	school rename press release
	•	school launch/brand article
	•	major school-specific articles

Event pages
Potential official resource links:
	•	launch/rename article explaining the event
	•	official announcement tied to the event

⸻

8. This layer should be curated, not dumped

Atlas should not mirror the WGU sitemap or show long lists of raw links.

Instead, Atlas should:
	•	gather a master list
	•	classify it
	•	score likely relevance
	•	surface only the most relevant items per entity

Good:
	•	1–3 strong links on a relevant page

Bad:
	•	14 mixed links with no explanation

⸻

9. The master list: required first artifact

Before any broad site integration, Atlas needs a central official-resource inventory.

Recommended file candidates
	•	data/official_context_links.csv
	•	data/official_context_links.json

Possibly later:
	•	data/official_context_links_curated.json

Recommended fields

Each record should ideally include:
	•	url
	•	title
	•	page_type
	•	official_context_type
	•	date
	•	source_section
	•	school_candidates
	•	program_candidates
	•	course_candidates
	•	keywords
	•	summary
	•	confidence
	•	notes

Example page_type values
	•	press_release
	•	program_guide_page
	•	program_guide_pdf
	•	comparison_article
	•	program_launch_page
	•	school_page
	•	career_article
	•	certification_article
	•	general_explainer

Example official_context_type values
	•	school_rename
	•	program_launch
	•	program_variant_comparison
	•	program_guide
	•	career_context
	•	certification_context
	•	school_context
	•	institutional_context

⸻

10. Discovery process

Phase 1 — Official-site discovery

Start with:
	•	https://www.wgu.edu/sitemap.html

Then gather candidate pages from:
	•	sitemap-linked HTML pages
	•	program guide pages
	•	guide PDFs
	•	WGU newsroom
	•	official school/program pages

Phase 2 — Normalize and classify

For each candidate:
	•	normalize title
	•	infer type
	•	extract date if available
	•	infer likely school/program/course relationships
	•	generate a short summary

Phase 3 — Matching analysis

Run a separate pass to compare the master list against Atlas entities:
	•	schools
	•	programs
	•	courses
	•	major events

Important:
	•	do not hardcode known examples first
	•	let the process discover the obvious matches independently
	•	use known examples later as a test of the process

Phase 4 — Curated surfacing

Only after the inventory exists and matching is reviewed should Atlas begin surfacing these links on pages.

⸻

11. Why this should precede Reddit integration

Atlas is expected to eventually surface:
	•	Reddit links
	•	Reddit landing pages
	•	discussion summaries
	•	freshness/context warnings

But if Atlas leads with Reddit too early, it risks becoming perceived as:
	•	a Reddit aggregation layer
	•	a discussion site
	•	a student-opinion mirror

Leading with official WGU resources first avoids this.

Strategic sequence
	1.	Catalog archive facts
	2.	Official WGU resources
	3.	Student/community discussion

This helps:
	•	student trust
	•	institutional comfort
	•	long-term product credibility

⸻

12. The likely future page pattern

For a mature Atlas page:

Course page
	1.	Official catalog facts
	2.	Related official WGU resources
	3.	Student discussion (later)

Program page
	1.	Official catalog facts
	2.	Program guide / official WGU resources
	3.	Student discussion (later)

School page
	1.	Official catalog facts and lineage
	2.	Related official WGU resources
	3.	Student discussion (later, if relevant)

⸻

13. Relationship to future “Atlas intelligence” features

This official-context layer will later help support:
	•	better entity search
	•	better recommendation systems
	•	related-link suggestions
	•	more useful landing pages
	•	context-aware guide generation
	•	broader “WGU around the web” infrastructure

It may also help with downstream work involving:
	•	course-specific study materials
	•	certification-linked course interpretation
	•	alternate naming/shorthand discovery
	•	official vs student-used naming differences

⸻

14. Important trust rules

Preserve source separation

Never blur these three layers:
	•	catalog facts
	•	official context links
	•	student discussion

Do not overclaim relevance

Use calm, honest language like:
	•	Related official WGU resources
	•	Helpful official context
	•	You may also want to read

Avoid:
	•	“the correct explanation”
	•	“the definitive comparison”
	•	“this proves”

Keep official pages official

Atlas should not paraphrase away the origin of these pages.
They should remain obviously:
	•	external
	•	official
	•	WGU-authored

⸻

15. Good examples already discovered

Examples already surfaced manually include:
	•	Leavitt School of Health rename article
	•	program guide pages
	•	program guide PDFs
	•	Java vs C# comparison article
	•	IT certification advice article

These should not be manually hardcoded as the whole system.

Instead, they should be treated as:
	•	proof of concept
	•	seed examples
	•	validation targets for the official-context discovery process

⸻

16. Recommended next work phases

Phase A — Build the master official-resource inventory

Goal:
	•	collect and normalize relevant WGU pages

Phase B — Relationship discovery against Atlas entities

Goal:
	•	identify where official resources should likely attach

Phase C — Curated surfacing on pages

Goal:
	•	start showing official WGU resources on:
	•	school pages
	•	program pages
	•	selected course pages

Phase D — Later discussion layer

Goal:
	•	add Reddit/community discussion beneath the official layer

⸻

17. Success criteria

This layer is successful if:
	•	Atlas helps users find official WGU pages they would otherwise struggle to discover
	•	official context appears relevant and restrained
	•	Atlas feels more like a guide to WGU information, not just a historical tracker
	•	users can understand the difference between:
	•	official catalog facts
	•	related official resources
	•	later, community discussion

⸻

18. Bottom line

WGU’s public website appears to contain a large, underused body of relevant material discoverable from the sitemap and related official pages.

Atlas should build an Official Context Layer that:
	•	inventories those pages
	•	classifies them
	•	matches them to Atlas entities
	•	surfaces them as first-class supporting resources

This should happen before broad Reddit integration.

That order gives Atlas the strongest product identity:
	•	official facts first
	•	official WGU context second
	•	student discussion later

That is both:
	•	more useful to students
	•	and more institutionally legible.

⸻

If you want, I can also write the next _internal document for the master official-links inventory workflow so Codex has a concrete spec for building the list.


Append this update section to _internal/OFFICIAL_CONTEXT_LAYER_PLAN.md:

⸻

19. Current status update (as of 2026-03-14)

This plan is no longer hypothetical. The Official Context Layer work is now underway.

Website context manifest — current state

Phase 1 completed
A raw sitemap manifest has already been created from:
	•	https://www.wgu.edu/sitemap.html

Outputs created:
	•	data/official_context_manifest_phase1.csv
	•	data/official_context_manifest_phase1.json

Internal support files created:
	•	_internal/official_context/README.md
	•	_internal/official_context/DEV_LOG.md
	•	_internal/official_context/REVIEW_QUEUE.md

Phase 1 result summary:
	•	raw links extracted from sitemap: 806
	•	after filtering obvious non-content links: 797
	•	after deduplication by URL: 604 unique entries

The Phase 1 manifest preserves the raw structure of each entry with:
	•	title
	•	url
	•	source = sitemap

and blank enrichment fields for later completion.

Phase 2 test completed successfully
A small enrichment test has already been run against a selected high-value subset of sitemap entries.

Test output:
	•	data/official_context_manifest_phase2_test.json

What the test validated:
	•	program guide pages are consistently discoverable and useful
	•	outcomes pages are especially rich and high-value
	•	specialization / track / variant pages are substantive and worth keeping
	•	accreditation / designation pages are meaningful and should be attached to either school or program entities
	•	generic sitemap titles such as “Program Guide” can be disambiguated successfully using page content and URL structure

The test confirmed that the enrichment workflow is viable and worth scaling.

Phase 2 scale-up — currently in progress

A larger high-value batch is now being enriched by Claude Code.

This in-progress batch covers the most Atlas-relevant portion of the sitemap inventory, including:
	•	outcomes pages
	•	accreditation / designation pages
	•	specialization / track / variant pages
	•	stackable certificate pages
	•	main program landing pages

This work is intentionally being done before any broad matching-to-entity pass.

Current Phase 2 enrichment strategy

The current strategy is:
	1.	Do not enrich the entire sitemap first
	2.	Prioritize the highest-value official content categories
	3.	Build a meaningful official-resource layer before worrying about lower-value institutional long-tail pages

High-priority categories now being enriched:
	•	outcomes_page
	•	program_guide_page
	•	program_subpage
	•	accreditation_page
	•	program_page
	•	certificate_page

Important current findings

The enrichment work has already surfaced several useful patterns:

Outcomes pages are more valuable than expected
These are not simple marketing pages. They often contain:
	•	structured learning outcomes
	•	competency framing
	•	assessment tables
	•	pass-rate charts
	•	student or graduate outcome data
	•	accreditation-aligned structure

These should become a high-priority official resource type for Atlas.

Program guide pages are worth keeping even though the HTML is thin
The HTML guide page is often just a wrapper around the real downloadable PDF, but it is still useful because:
	•	it is the canonical official landing point
	•	it exposes the downloadable guide
	•	it is easier and safer to link than a raw PDF URL alone

Specialization / track pages are highly useful
These pages often explain:
	•	how one specialization differs from another
	•	curriculum emphasis
	•	career outcomes
	•	track-specific positioning

This makes them especially valuable for:
	•	program pages
	•	future comparison/family pages
	•	“Atlas vs catalog structure” interpretation

Accreditation / designation pages split into two useful classes
Some apply to:
	•	a whole school (e.g. business or education)

Others apply to:
	•	one program only

Atlas should later attach them accordingly.

The sitemap under-represents newsroom content
The main sitemap does not appear to expose the full WGU newsroom / press-release universe.
This means newsroom discovery will require a separate targeted pass later.

⸻

20. Official video layer — expanded scope

The Official Context Layer should now be understood more broadly than official website pages alone.

Atlas now has evidence of at least two official WGU YouTube channel inventories that should become part of the long-term official-resource architecture.

Channel 1 — official WGU YouTube

Source file available outside this repo:
	•	/Users/buddy/projects/yt-video-analysis/research/wgu/derived/title_inventory_condensed.tsv

Approximate size:
	•	1,500+ videos

This corpus includes:
	•	school-related videos
	•	academic / career explainers
	•	official announcements
	•	certification / AI / healthcare / education / business topic videos
	•	commencement and event videos
	•	school-specific content
	•	“what is X?” style explainer videos

Channel 2 — WGU Career Services YouTube

Source file available outside this repo:
	•	/Users/buddy/projects/yt-video-analysis/research/wgucareerservices/derived/title_inventory_condensed.tsv

Approximate size:
	•	440 videos

This corpus includes:
	•	Career Quest sessions
	•	resume / interviewing / networking / LinkedIn videos
	•	AI-for-job-search content
	•	employer information sessions
	•	cyber / business / healthcare / education career content
	•	internships / fairs / career development workshops

Why these channels matter

These two corpora should eventually become a parallel official video layer for Atlas.

This means Atlas is likely evolving toward four content layers:
	1.	Official catalog facts
	2.	Related official WGU web resources
	3.	Related official WGU videos
	4.	Student/community discussion (later, secondary)

This is a stronger and more institutionally legible structure than moving directly from catalog facts to Reddit.

Important distinction between the two video channels

These two sources should be modeled separately at ingestion time.

Official WGU YouTube
Likely best for:
	•	school/program context
	•	institutional announcements
	•	explainers
	•	public-facing academic/career content
	•	school-level enrichment

WGU Career Services YouTube
Likely best for:
	•	job-search support
	•	employer sessions
	•	career development
	•	networking / resume / LinkedIn content
	•	future career resource hubs
	•	selective school/program enrichment where strongly relevant

Current recommendation for the video layer

Do not surface videos yet.

First:
	1.	import both channel inventories into Atlas as raw manifests
	2.	keep the two channels distinct
	3.	define a common schema
	4.	later run a small enrichment/classification test on selected samples
	5.	only then decide where and how videos should appear in Atlas

Recommended future video-manifest schema

Each video record should eventually support fields like:
	•	published_date
	•	video_id
	•	title
	•	url
	•	keep
	•	status
	•	video_type
	•	official_context_type
	•	summary
	•	school_candidates
	•	program_candidates
	•	course_candidates
	•	notes
	•	source

Suggested source values:
	•	official_wgu_youtube
	•	official_wgu_careerservices_youtube

Important product note

Official videos should be treated like official-resource links:
	•	useful
	•	curated
	•	secondary to catalog facts
	•	not dumped into pages as a feed

A likely future page pattern is:
	•	Official catalog facts
	•	Related official WGU resources
	•	Related official WGU videos
	•	Student discussion (later)

⸻

21. Refined near-term roadmap for the Official Context Layer

Immediate next step

Finish the current high-value Phase 2 enrichment batch for official WGU website pages.

Next after that

Review the enriched manifest and decide which official web resources belong on:
	•	program pages
	•	school pages
	•	selected course pages

Parallel planning track

Prepare the raw import and planning structure for the two official YouTube channel inventories.

Later

Run separate, targeted discovery/enrichment passes for:
	•	WGU newsroom / press-release pages
	•	official video manifests
	•	entity-to-resource matching
	•	future standalone resource hubs (if justified)

⸻

22. Updated bottom line

The Official Context Layer is now an active workstream, not just a concept.

It currently includes:
	•	a raw sitemap-derived manifest
	•	a successful enrichment test
	•	a larger enrichment pass in progress
	•	a broader scope that now includes two official WGU YouTube channels

Atlas should continue treating this as a first-class strategy:
	•	catalog facts first
	•	official WGU resources second
	•	official WGU videos next
	•	student discussion later

That remains the strongest long-term product posture for usefulness, trust, and institutional legibility.

⸻
# WGU Atlas — Outcomes/Assessment Chart Enrichment Plan

Drafted: 2026-03-15  
Purpose: document the official WGU outcomes-page chart assets we have identified and define how Atlas should extract and use them to enrich course-level information.

---

## 1. Why this matters

WGU student discussion repeatedly surfaces the same question:

- which courses are hardest?
- which courses are bottlenecks?
- which courses have lower pass rates?
- where do students struggle most in a program?

Until now, Atlas has mainly had:

- catalog facts
- program/course history
- structural change information
- student discussion signals

But WGU’s own outcomes pages appear to expose an additional high-value official signal:

- program-level assessment/pass-rate tables by course
- program results tables covering retention, enrollment, OTP, satisfaction, and graduation metrics

This is important because it gives Atlas something rare:

- **official, program-linked outcome data**
- **course-level pass-rate evidence**
- **objective context that can sit alongside student discussion**

That makes this a first-class enrichment opportunity.

---

## 2. What we found

On at least some official WGU outcomes pages, WGU links to static chart images hosted in their DAM.

Example page:
- BSCSIA outcomes page

The page appears to include ordinary anchor links to image assets, not special widgets or embedded chart components.

Examples identified from the page:

- Mapping image
- Program Results chart image
- Program Assessment Results chart image

Important implementation implication:

These assets can likely be discovered by scanning ordinary page links for:

- image extensions (`.png`, `.jpg`, `.jpeg`, etc.)
- WGU DAM paths
- outcome/result-related naming patterns

This makes them much easier to collect than if they were rendered through a JS chart library.

---

## 3. The two chart types we care about

### A. Program Results

This chart appears to contain program-level metrics over time, such as:

- total enrollment
- on-time progress
- retention windows
- graduation rates
- drop rate
- VSAT / student satisfaction

This is valuable for Atlas as **program-level context**.

Use case:
- enrich program detail pages
- support school/program official-context sections
- provide factual context for how a program has performed over time

### B. Program Assessment Results

This chart appears to contain **course-level pass rates** across a program.

This is the highest-value target for Atlas because it can directly enrich course pages and course difficulty context.

Use case:
- attach official pass-rate evidence to course detail pages
- compare discussion-based “hard course” reputation with official pass-rate data
- identify recurring low-pass-rate courses inside a program
- support future “hardest courses in this program” views

---

## 4. Why Program Assessment Results are especially important

This is where Atlas can create a uniquely useful synthesis.

We already have student discussion research around:

- hard courses
- bottleneck courses
- pain points
- repeated complaints about certain technical/math-heavy classes

Now we may also be able to collect official WGU evidence showing:

- pass-rate levels by course
- pass-rate trend across periods
- relative difficulty signals within a program

That lets Atlas do something much better than either source alone:

### Student discussion alone
Useful, but subjective and noisy.

### Official pass-rate tables alone
Useful, but buried and hard to discover.

### Atlas combining both
Potentially very strong:
- official pass-rate context
- catalog context
- student discussion context
- all attached to the same course/program entities

This is one of the clearest examples of Atlas enriching the public catalog with adjacent official data that WGU itself does not organize well.

---

## 5. What Atlas should try to collect

For every outcomes page that exposes these assets, Atlas should try to gather:

### Page-level metadata
- source outcomes page URL
- source page title
- linked image URL
- image type
- related program
- related school
- discovery method

### Program Results fields
Where legible, extract:
- reporting periods / term columns
- enrollment totals
- OTP
- retention metrics
- graduation-rate metrics
- drop rate
- VSAT / satisfaction

### Program Assessment Results fields
Where legible, extract:
- course code
- course title
- pass-rate values by period
- trend direction if obvious
- first/last period shown
- source program
- source image URL

---

## 6. Proposed data model

Atlas should treat these as a new official data layer, separate from both catalog facts and discussion.

### A. Program-level table
Suggested file:
- `data/official_program_results.json`

Suggested record shape:
- program_key
- source_page_url
- source_image_url
- metric_name
- period
- value
- notes

### B. Course-level assessment table
Suggested file:
- `data/official_course_assessment_results.json`

Suggested record shape:
- source_program_key
- course_code
- course_title
- period
- pass_rate
- source_page_url
- source_image_url
- notes

### C. Optional asset inventory
Suggested file:
- `data/official_outcomes_chart_assets.json`

Suggested record shape:
- source_page_url
- source_page_title
- asset_url
- asset_type
- program_key
- school_key
- keep
- extraction_status
- notes

---

## 7. Discovery strategy

### Phase 1 — Find outcomes pages
Use the official resource inventory and sitemap-derived manifest to identify:

- `outcomes_page` entries
- other program pages that may link to outcomes/result charts

### Phase 2 — Scan those pages for linked chart assets
Look for ordinary anchor links that point to WGU DAM image assets.

Detection heuristics:
- href ends with `.png`, `.jpg`, `.jpeg`
- URL contains WGU DAM path
- filename or nearby text suggests:
  - mapping
  - outcomes
  - program results
  - program assessment results
  - chart

### Phase 3 — Download or record the chart assets
Store:
- asset URL
- source page URL
- linked text / nearby heading
- matched program

### Phase 4 — Extract chart/tabular content
Because these appear to be image files, Atlas will need a separate extraction step.

That extraction workflow should be treated cautiously:
- preserve original source image URL
- preserve image archive copy if stored
- clearly mark extracted values as derived from official chart image
- log uncertainty when rows/columns are difficult to parse

### Phase 5 — Normalize into Atlas entities
Map extracted values to:
- program keys
- school keys
- course codes where present

---

## 8. How Atlas should use this data

## Program pages
Use Program Results as official context, not as the main story.

Possible uses:
- compact “Official outcomes data available” panel
- selected program metrics
- link to source outcomes page/chart
- future “program performance context” section

## Course pages
This is the bigger opportunity.

Possible uses:
- “Official pass-rate data seen in X program(s)”
- pass-rate trend snippet where reliable
- program-specific warning that pass rates vary by program/context
- pairing with discussion layer later:
  - official pass-rate signal
  - student-reported difficulty signal

## Program-level “hard course” summaries later
If coverage is broad enough, Atlas could later support:
- hardest courses in a program
- lowest-pass-rate courses in a program
- pass-rate trend watchlists

This should only happen once extraction quality is good enough.

---

## 9. Important trust rules

### Preserve source separation
Do not mix these into catalog facts.

These are:
- official WGU outcomes/assessment resources
- not catalog fields

### Preserve provenance
Every extracted metric should retain:
- source page URL
- source asset URL
- extraction note

### Preserve caution on interpretation
A lower pass rate does not automatically mean:
- bad course
- bad design
- worse student experience

It means:
- lower observed pass rate in the source assessment table

Atlas should present this calmly and factually.

### Preserve program context
Program Assessment Results appear program-specific.

That means course pass-rate values may reflect:
- that program
- that time window
- that outcomes-page source

Atlas should avoid overclaiming that a course has one global pass rate everywhere.

---

## 10. Relationship to the discussion layer

This dataset is highly complementary to the future discussion layer.

Student discussion can tell us:
- what students complain about
- what they fear
- what they consider hard or unfair

Official assessment tables may tell us:
- whether pass-rate data supports that pattern
- whether difficulty appears persistent
- which courses stand out objectively within a program

That combination could become one of Atlas’s most valuable course-enrichment features.

---

## 11. Recommended immediate next steps

### Step A
Inventory all official outcomes pages already present in the official-context manifest.

### Step B
Build a small scanner for linked DAM image assets on those pages.

### Step C
Create an internal inventory of:
- source page
- source program
- chart asset URL
- chart type

### Step D
Run a pilot extraction on a small sample:
- one technology program
- one business program
- one health or education program if available

### Step E
Evaluate extraction quality before committing to broad site integration.

---

## 12. Bottom line

WGU outcomes pages may expose one of the most valuable official enrichment layers Atlas has found so far:

- official program results
- official course-level pass-rate tables
- discoverable through ordinary linked image assets
- highly relevant to student decision-making

This is especially important because Atlas already has student discussion research around hard courses.

If Atlas can combine:
- catalog structure
- course history
- official pass-rate evidence
- later, student discussion

then course pages become substantially more useful than either the catalog alone or WGU’s own public site structure.


Below is a clean, repo-ready document that only lists videos and where they go, as requested.

⸻

WGU Career Services YouTube Videos for Atlas Enrichment

This document lists WGU Career Services YouTube videos selected to enrich Atlas pages.

Videos are embedded only when they help students understand:
	•	the field of a degree
	•	the types of roles associated with that degree
	•	the real-world application of course topics

Atlas does not include job-search advice videos (resume, interviewing, networking, etc.).

⸻

Degree Page Enrichment

Accounting

Career Quest: Careers in Accounting

Explains accounting roles and career paths.

Career Quest: Accounting Careers with CBIZ

Employer perspective on accounting work and responsibilities.

⸻

Healthcare Administration

Career Quest: Exploring the Business Side of Healthcare with Parallon (HCA Healthcare)

Explains operational and administrative healthcare roles.

Career Quest: Careers in Long-term Care ft. WGU Alumna Jenny Parker

Explains management and operations in long-term care organizations.

Love Your Career: Healthcare Clinical & Operational ft. Shanell Murphy

Explains the relationship between clinical and administrative healthcare roles.

⸻

Information Technology

Career Quest: Tech Careers in the Insurance Industry

Shows how IT roles operate inside a large industry.

⸻

IT Management

Career Quest: The Power of IT Management – The Bridge between Business Strategy and Tech

Explains the domain and responsibilities of IT management roles.

⸻

Data Analytics

Launch Your Data Analytics Career with The Information Lab

Explains real-world analytics work and how organizations use data.

I’m in a Data Analytics Program… What Career Should I Go For?

Explains typical analytics roles and career directions.

⸻

Education

Explore Education Careers with ESC of Central Ohio

Explains roles within school systems and education organizations.

Career Options with BAES & MAES Degrees

Explains career paths associated with education degrees.

How to Leverage My Teaching Degree? | Charlotte-Mecklenburg Schools

Shows how teaching credentials translate to professional roles.

⸻

Nursing

Navigating the Core of Emergency Room Nursing

Explains responsibilities and workflow in a clinical nursing specialty.

⸻

Course Page Enrichment

Cybersecurity

Cyber Week: Risk to Resilience

Relevant for courses covering:
	•	cybersecurity risk
	•	security governance
	•	enterprise security strategy

⸻

Cyber Week: Securing Our Future – Defending Critical Infrastructure

Relevant for courses covering:
	•	infrastructure security
	•	cyber defense
	•	national security systems

⸻

Cyber Week: AI Security – The Next Frontier for Cybersecurity Professionals

Relevant for courses covering:
	•	AI security
	•	emerging cybersecurity threats
	•	machine learning security risks

⸻

Maintenance

This list may expand if additional Career Services videos clearly:
	•	explain a technical domain
	•	explain a professional field
	•	demonstrate real-world application of course topics

Videos focused primarily on job search advice are not added to Atlas.


