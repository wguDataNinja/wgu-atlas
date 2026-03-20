Atlas Source Enrichment — Operating Log and Next Work

Last updated: 2026-03-19
Status: Active backfill + maintenance planning
Primary goal: build a student-useful source layer for Atlas that can be backfilled now and maintained incrementally over time.

⸻

1. Purpose

Atlas source enrichment exists to decide:
	•	which external/supporting sources should appear in the Relevant Resources sidebar
	•	on which Atlas surfaces they should appear:
	•	school pages
	•	degree pages
	•	later, course pages
	•	what each source adds beyond the catalog itself

This is not a generic link-collection project.

The standard is:

Does this source add concrete value to a student exploring this entity?

Examples of value:
	•	accreditation / designation context
	•	outcomes / assessment reporting
	•	licensure / certification / exam eligibility
	•	specialization / track explanation
	•	school-level readiness / governance / results
	•	concrete program constraints or facts:
	•	state restrictions
	•	clinical/practicum requirements
	•	exam pathways
	•	completion framing
	•	course count
	•	cost/term framing

Generic marketing copy is low priority unless it contains concrete student-useful information.

⸻

2. Operating principle

Atlas should surface sources where they are most relevant to the reader.

The organizing rule is not:
	•	official vs non-official

The organizing rule is:
	•	what is useful and relevant at this page’s level?

That means sources should be judged by:
	•	relevance
	•	scope
	•	student usefulness
	•	whether they add something the catalog does not already provide

Source origin still matters for labeling/provenance, but it is not the main inclusion test.

⸻

3. Entity-level source model

School pages

School pages should show sources useful across:
	•	the school itself
	•	multiple degrees in that school
	•	major degree families in that school
	•	broad field areas aligned to that school

Good school-page examples:
	•	school accreditation
	•	school learning-results pages
	•	school governance / identity pages
	•	school-branded roadshows / fireside chats
	•	broad field/workforce discussions relevant across many degrees in the school

Avoid on school pages:
	•	single-degree guides
	•	single-degree outcomes pages
	•	narrow track pages
	•	generic resume/interview advice
	•	narrow employer recruiting sessions

Degree pages

Degree pages should show sources useful to someone considering that specific degree.

Good degree-page examples:
	•	program guide
	•	outcomes page
	•	accreditation / designation page
	•	licensure / certification / exam page
	•	track / specialization explainer
	•	official degree-adjacent resources that clarify what the degree leads to or requires

Course pages

Course pages should eventually show sources useful to someone taking, evaluating, or preparing for that course.

Likely future course-page sources:
	•	Reddit/community discussion
	•	practical advice
	•	pacing/assessment discussion
	•	experience-based threads
	•	troubleshooting/study context
	•	any rare official course-adjacent support material

Reddit/community is especially important here, but remains future work.

⸻

4. Current product state

Today, Atlas already has a Relevant Resources sidebar on degree pages.

This means:
	•	the attachment pattern already exists
	•	the current system is already entity-scoped
	•	source enrichment is an expansion of an existing pattern, not a new product surface

Current live source layer is still narrow and mostly official-only. The work now is to make it richer and more useful.

⸻

5. Current source families in scope

5.1 WGU sitemap / official WGU pages

Includes:
	•	program guides
	•	outcomes pages
	•	accreditation/designation pages
	•	specialization / track pages
	•	program landing pages
	•	school-level governance / context pages
	•	licensure / certification / exam / disclosure pages

5.2 Official WGU YouTube

Includes:
	•	school-branded videos
	•	roadshows
	•	fireside chats
	•	broad field/topic videos
	•	official panels and school-adjacent contextual material

5.3 WGU Career Services YouTube

Includes:
	•	some broad field/career-path content
	•	some degree-adjacent alumni/career materials

This source family requires aggressive filtering because much of it is too generic or too employer-session-heavy for Atlas.

5.4 Reddit / community (future)

Planned future source family, most likely for course pages.

⸻

6. Work surfaces

Sitemap / official WGU pages
	•	Raw universe: data/enrichment/official_context_manifest_phase1.csv
	•	Earlier reviewed subset: data/enrichment/official_context_manifest_phase2_test.json
	•	Outcomes/accreditation focused workspace:
	•	data/enrichment/outcomes/README.md
	•	data/enrichment/outcomes/outcomes_links.json

YouTube
	•	Official WGU raw: _internal/youtube/raw/wgu_official_titles_raw.txt
	•	Official WGU filtered: _internal/youtube/working/wgu_official_titles_filtered.txt
	•	Career Services raw: _internal/youtube/raw/wgu_career_services_titles_raw.txt
	•	Career Services filtered: _internal/youtube/working/wgu_career_services_titles_filtered.txt
	•	Worklog: _internal/youtube/YOUTUBE_WORKLOG.md

Audit / planning
	•	_internal/SOURCE_ENRICHMENT_AUDIT.md
	•	_internal/sources_document.txt

⸻

7. What has been learned so far

7.1 Outcomes / accreditation pages are high-value but sparse

This source class is worth surfacing, but it is not the main enrichment engine.

The outcomes/accreditation work showed that these pages are:
	•	rare
	•	unusually information-dense
	•	often the strongest official non-catalog signals on the site

Examples already identified:
	•	B.S. Computer Science outcomes
	•	B.S. Cybersecurity outcomes
	•	B.S. Cybersecurity CAE-CDE designation
	•	B.S. Health Information Management accreditation
	•	School of Business ACBSP
	•	Teachers College CAEP

What this means:
	•	this class is premium
	•	coverage will always be sparse
	•	it should be maintained, but not over-relied on as the main source-discovery path

7.2 The next best sitemap value is not “more outcomes”

The next strong sitemap classes appear to be:
	1.	regulatory / licensure / disclosure pages
	2.	specialization / track / variant pages
	3.	school governance / school context pages
	4.	select program landing pages, but only for concrete facts

This is the key directional update.

⸻

8. Coverage status by known sitemap class

Program guides

Status: mostly solved
	•	already harvested at scale
	•	already live on many degree pages
	•	should not remain in the main discovery queue
	•	only a small cleanup audit remains where missing coverage is suspected

Outcomes pages

Status: high-value, likely mostly sparse by nature
	•	strong set already identified
	•	should still be audited for completeness against the sitemap universe
	•	do not expect many additional pages

Accreditation / designation pages

Status: important, probably not fully closed
	•	several important ones identified already
	•	remaining accreditation/designation pages should be checked explicitly
	•	still worth a completeness audit

Regulatory / licensure / disclosure pages

Status: next priority
Examples identified as likely strong candidates:
	•	Teaching state licensure
	•	Nursing state licensure
	•	Nursing clinical information
	•	NCLEX page
	•	Praxis page
	•	AACN or similar certification/credential references

These are among the most student-important official pages because they contain constraints and obligations students need to know before enrolling.

Specialization / track / variant pages

Status: next major scalable enrichment class
Examples:
	•	MS Data Analytics tracks
	•	MS Accounting tracks
	•	MS Software Engineering tracks
	•	MS Marketing specialization pages

These are high student-value because they help explain real choices between closely related options.

School governance / school context pages

Status: promising school-page enrichment
Known likely candidates:
	•	Business governance
	•	Technology governance
	•	Education governance
	•	Health governance

These help complete school-page context, especially where sitemap school-level coverage is thin.

Program landing pages

Status: selective only
Useful only when they yield concrete facts:
	•	course count
	•	term cost framing
	•	completion framing
	•	practicum/clinical notes
	•	licensure/certification notes
	•	state restrictions
	•	exam relevance

Do not spend much effort on generic overview copy.

⸻

9. Current directional conclusion

Atlas is currently in backfill mode, but the work must be structured for monthly maintenance.

The important shift is:
	•	stop thinking in terms of “browse the sitemap for interesting pages”
	•	instead think in terms of source classes
	•	and for each source class ask:
	1.	why does it help students?
	2.	where does it belong?
	3.	how will we find only the new/changed ones next month?

That recurring workflow is part of the product value.

⸻

10. Backfill priorities — updated

Tier 1 — highest immediate value

Regulatory / licensure / disclosure pages
These are the next best sitemap pass.

Why:
	•	concrete student impact
	•	enrollment-critical constraints
	•	easy to justify in sidebar
	•	stronger than generic degree copy

Target examples:
	•	Teaching state licensure
	•	Nursing state licensure
	•	Clinicals page
	•	NCLEX page
	•	Praxis page
	•	explicit certification / state approval / exam eligibility pages

Tier 2 — highest scalable degree-enrichment class

Specialization / track / variant pages
These likely provide the best broad next yield after program guides.

Target examples:
	•	Data Analytics tracks
	•	Accounting tracks
	•	Software Engineering tracks
	•	Marketing track
	•	other track / endorsement / certificate pages that explain meaningful variants

Tier 3 — school-page completion

School governance / school context pages
Use these to strengthen school-level source blocks where official sitemap coverage is otherwise thin.

Tier 4 — selective mining only

Program landing pages
Review only for extractable concrete facts.

⸻

11. Current findings by school

Business

Current picture:
	•	strong school-level accreditation exists
	•	likely viable school-level official context
	•	likely strong specialization/track support
	•	likely some school-relevant official YouTube later

Education

Current picture:
	•	strong school-level CAEP context exists
	•	likely meaningful licensure / Praxis-related content
	•	likely some broad school-level official context
	•	likely mixed but usable YouTube support later

Technology

Current picture:
	•	strong degree-level outcomes/accreditation/designation signals exist
	•	weaker school-level sitemap coverage than YouTube
	•	specialization and cyber-adjacent context likely strong
	•	school-page strength may rely more on YouTube later

Health

Current picture:
	•	useful accreditation and program-specific pages exist
	•	likely strong licensure / clinical / NCLEX / credential relevance
	•	school-level sitemap coverage thinner than degree-level/regulatory content
	•	likely some strong broad school-aligned YouTube later

⸻

12. To-do list

Immediate
	•	Audit completeness of known outcomes pages against official_context_manifest_phase1.csv
	•	Audit completeness of known accreditation/designation pages against official_context_manifest_phase1.csv
	•	Confirm program-guide coverage is sufficiently complete and remove guides from active review work

Next sitemap pass
	•	Build and review a focused queue for regulatory / licensure / disclosure pages
	•	Review likely high-value pages such as:
	•	teaching state licensure
	•	nursing state licensure
	•	clinicals
	•	NCLEX
	•	Praxis
	•	certification/credential-specific pages
	•	Decide targets for each kept page:
	•	school
	•	degree
	•	later maybe course

After that
	•	Run specialization / track / variant review pass
	•	Start with:
	•	MS Data Analytics tracks
	•	MS Accounting tracks
	•	MS Software Engineering tracks
	•	MS Marketing track
	•	Record what each page adds beyond the catalog

Then
	•	Review the four school governance/context pages
	•	Decide whether they are strong enough for school-page sidebar use

Later
	•	Review main program landing pages, but only for concrete student-useful facts
	•	Resume Official WGU YouTube candidate work after sitemap passes are in a good state
	•	Defer Career Services deeper review until Official WGU YouTube has produced clear value
	•	Keep Reddit/community as future course-page work

⸻

13. Maintenance model

This project needs a monthly update workflow, not just one-off backfill.

For each source family, the recurring maintenance question is:

How do we find only the new or changed items next month?

Sitemap maintenance goal

For each monthly sitemap snapshot:
	•	ingest new sitemap
	•	diff against prior snapshot
	•	isolate new/changed URLs
	•	classify into source classes
	•	review only the high-value classes:
	•	outcomes
	•	accreditation/designation
	•	regulatory/licensure/disclosure
	•	specialization/variant
	•	meaningful school-context pages
	•	optionally changed program landing pages

YouTube maintenance goal

For each monthly inventory refresh:
	•	ingest updated title list
	•	diff against prior inventory
	•	exclude obvious junk first
	•	review only new titles in target classes

Reddit/community maintenance goal

Later:
	•	ingest recent matched posts
	•	filter by course/entity relevance
	•	review only recent/high-signal items

⸻

14. Working summary

Atlas should surface sources where they are most relevant to the reader.
	•	School pages should show sources relevant across the school, across multiple degrees, or across broad field areas in that school.
	•	Degree pages should show sources relevant to someone exploring that specific degree, including official pages that explain requirements, outcomes, accreditation, specialization, or concrete program constraints.
	•	Course pages should later show practical and community-sourced material where useful.

Current practical conclusion

The next best sitemap work is:
	1.	regulatory / licensure / disclosure pages
	2.	specialization / track / variant pages
	3.	school governance / school context pages
	4.	selective mining of program landing pages for concrete facts

This is the current operating direction.






addendum:

Reddit / community enrichment policy for course detail pages

Purpose

Reddit/community material is a future course-page enrichment layer intended to add student-experience context that the catalog cannot provide on its own.

This layer exists to help a future student answer practical questions such as:
	•	what students tend to worry about before starting
	•	how students describe the course experience
	•	what advice or cautions appear in discussion
	•	what resources, assessment patterns, or pacing concerns recur in practice

This layer is not part of the official catalog-fact layer and must never be presented as such.

Role in the page

For course detail pages, Reddit/community content is a supporting layer, not the primary page identity.

Course pages should continue to lead with:
	1.	official catalog facts
	2.	Atlas historical/catalog context
	3.	optional student/community discussion summary

Reddit/community enrichment is meant to complement official and historical data, not replace it.

Source separation

Atlas must preserve a hard boundary between:
	•	official catalog facts
	•	official WGU supporting resources
	•	student/community discussion
	•	Atlas-generated interpretation

Reddit/community material must appear in its own visibly separate block and must never be blended into official course-description, roster, or metadata fields.

Framing rule

Atlas will not frame Reddit enrichment primarily as a pain-point or complaint system.

Instead, the course-page community layer should be framed as a student discussion summary or equivalent student-facing label. The goal is to summarize the most useful student-discussion signals for a future student, not to maximize negative issue extraction.

Extraction scope

For course detail pages, Reddit/community enrichment should look for student-useful discussion signals, including:
	•	common questions
	•	what students repeatedly ask before or during the course
	•	reported experience
	•	perceived difficulty, pacing, workload, confidence, or ease
	•	assessment/course structure
	•	OA/PA/task/rubric patterns, alignment concerns, sequencing expectations
	•	advice/resources
	•	study strategies, useful materials, cohorts, docs, or preparation tips
	•	warnings/cautions
	•	recurring pitfalls, misleading assumptions, or areas of confusion

These categories may be extracted separately upstream even if they are later combined into one concise page summary.

What not to do

Atlas should not:
	•	treat Reddit discussion as official fact
	•	summarize only complaints or only advice
	•	infer broad consensus from a very small number of posts
	•	convert anecdotal discussion into strong factual claims
	•	classify a post as relevant merely because it names the course code

The standard is whether the discussion would help a prospective student understand what taking the course is like.

Relevance rule for post selection

A Reddit post is relevant for course-page enrichment only if it adds or seeks course-specific information useful to a future student, such as:
	•	difficulty
	•	pacing
	•	assessments
	•	study strategy
	•	resources
	•	practical concerns
	•	recurring confusion

Posts that only mention the course incidentally, list it in schedules/progress logs, or include it as part of a broad multi-course discussion without meaningful course-specific substance are not page-enrichment evidence.

Recommended internal labels:
	•	likely_relevant
	•	potentially_relevant
	•	not_relevant

Summary posture

Atlas should maintain a data analyst posture when presenting Reddit/community content.

That means the site should:
	•	be transparent about the dataset used
	•	identify the source family clearly
	•	state that the summary is Atlas-generated / AI-assisted if applicable
	•	indicate the amount of source evidence used
	•	link the underlying posts
	•	use fair, bounded language proportional to the evidence

Preferred summary language:
	•	“In N matched posts…”
	•	“Recent Reddit discussion often mentions…”
	•	“Posts in this set commonly discuss…”
	•	“Student discussion in this sample suggests…”

Avoid language that overstates certainty:
	•	“Students say…”
	•	“This course is…”
	•	“Reddit proves…”

Presentation format

The default public presentation for course pages should be a compact block such as:

What students on Reddit say about this course
[brief summary]

Source basis: N matched Reddit posts
Method: Atlas-generated summary of public student discussion. This is a community-discussion layer, not an official WGU source.
Posts: [links]

When evidence volume is higher or more substantive, Atlas may also show:
	•	a few representative quotes or excerpts
	•	linked source posts
	•	optional separation of questions, reported experiences, and advice

Volume-sensitive surfacing

The amount of Reddit content shown should depend on evidence quality and quantity.
	•	Low-volume / repetitive evidence: short summary only
	•	Moderate evidence: summary plus source links
	•	High-value / high-volume evidence: summary plus a few representative excerpts and links

The summary should remain restrained even when more raw material exists.

Comments policy

Comments may be fetched and incorporated when they materially improve the usefulness of the discussion summary.

Comments are especially valuable when they add:
	•	repeated advice
	•	practical answers to recurring questions
	•	study/resource recommendations
	•	clarification on assessments
	•	common pitfalls or disagreement

Comments are not required for every course. They should be used when their incremental value justifies the additional cost and complexity.

Output contract

Any Atlas-generated Reddit/community summary used on a course page should be:
	•	bounded to a known set of matched posts/comments
	•	clearly labeled as community discussion
	•	clearly labeled as Atlas-generated interpretation
	•	linked back to source posts
	•	written as student-useful context, not authoritative fact

Product stance

Reddit/community enrichment on course pages is intended to make Atlas more useful as a student decision-support and orientation tool.

Its role is to add:
	•	practical experience context
	•	common questions
	•	recurring advice/cautions

while preserving Atlas’s core commitments to:
	•	provenance clarity
	•	source separation
	•	interpretive transparency
	•	restrained enrichment over maximal content density


