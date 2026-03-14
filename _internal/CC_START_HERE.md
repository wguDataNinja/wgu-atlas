Claude Code — Start Here

This file gives top-level context for work in the wgu-atlas repo.

Read this file first at the start of every fresh Claude Code session.

⸻

1. What this repo is

wgu-atlas is the new dedicated public repo for the WGU Atlas website.

Site identity
	•	Site name: WGU Atlas
	•	Subtitle: Explore courses, programs, catalog changes, and student discussion
	•	Creator attribution: Created by WGU-DataNinja

This repo will hold:
	•	the website source
	•	the site data layer
	•	minimal reproducible build scripts needed for website data
	•	public-facing documentation
	•	deployment configuration

This repo should remain clean, focused, and auditable.

It should not become a dump of everything from wgu-reddit.

⸻

2. What WGU Atlas is

WGU Atlas is a public-facing reference and explorer built from the validated public WGU catalog archive, with course/program history and later discussion context layered on top.

The product direction is:
	•	official catalog history first
	•	course/program lookup
	•	major historical change timeline
	•	student discussion as a real feature layer
	•	strict separation between:
	•	official catalog facts
	•	discussion signals
	•	LLM-generated summaries

The flagship feature is the course page.

⸻

3. Immediate mission in this repo

The near-term goal is to stand up the new repo cleanly and begin the first site build.

That means:
	1.	set up repo hygiene
	2.	migrate only the necessary code/data/docs from wgu-reddit
	3.	avoid unrelated legacy material
	4.	build the site shell for:
	•	homepage
	•	course explorer
	•	course page
	•	timeline
	•	methods
	•	data page

Do not start by moving everything over. This should be a selective extraction, not a transplant.

⸻

4. Source-of-truth files in the old repo

The current working truth still lives in wgu-reddit.

Use these files as your source-of-truth references:

Main references
	•	/Users/buddy/Desktop/WGU-Reddit/WGU_catalog/README_INTERNAL.md
	•	/Users/buddy/Desktop/WGU-Reddit/WGU_catalog/website_design_plan.md
	•	/Users/buddy/Desktop/WGU-Reddit/WGU_catalog/SCRAPE_LOG.md

These contain:
	•	scraper architecture
	•	validation basis
	•	archive coverage
	•	website design decisions
	•	current build state and milestones

Do not re-derive settled context if it is already documented there.

⸻

5. Current known project state

The following is already true in wgu-reddit and should be treated as established unless evidence says otherwise:

Archive and parser
	•	108 public catalog editions on disk
	•	coverage: 2017-01 through 2026-03
	•	missing: 2017-02, 2017-04, 2017-06
	•	active parser: parse_catalog_v11.py
	•	full archive run: 0 anomalies, 0 skipped editions
	•	14/14 structurally critical editions validated clean

Trusted current baseline
	•	trusted 2026-03 snapshot exists
	•	2026-03 counts:
	•	838 AP codes
	•	52 cert codes
	•	114 program body blocks

Historical data already built
	•	course history
	•	program history
	•	adjacent diffs
	•	enriched edition diffs
	•	event candidates
	•	validated structural era model

Website data layer already built

The first website data-layer milestone already exists in the old repo.

Built artifacts include:
	•	title variant classification
	•	canonical course intelligence table
	•	named event layer
	•	static site-ready exports

These are sufficient to begin building:
	•	homepage
	•	course explorer
	•	course page
	•	timeline
	•	methods
	•	data page

Still deferred
	•	cert cross-edition tracking beyond current snapshot model
	•	program roster-per-edition matrix
	•	predecessor/successor inference
	•	Reddit integration
	•	frontend implementation in the new repo

⸻

6. Site/product decisions already locked

Do not revisit these unless explicitly asked.

Branding
	•	Site name: WGU Atlas
	•	Subtitle: Explore courses, programs, catalog changes, and student discussion
	•	Creator attribution: Created by WGU-DataNinja

Repo
	•	Repo name: wgu-atlas

Stack

Preferred website stack:
	•	Next.js
	•	TypeScript
	•	Tailwind
	•	static site/data-driven architecture

Deployment direction
	•	public GitHub repo
	•	GitHub Pages
	•	build/deploy via GitHub Actions

Product framing

The site is:
	•	a public-facing reference and explorer
	•	catalog-history first
	•	discussion-aware
	•	not just a “student guide”
	•	not a raw data browser

Homepage jobs

The homepage should do four things:
	1.	Search
	2.	Orient
	3.	Surface what’s new
	4.	Connect to discussion

Homepage intended entry surfaces
	•	course search
	•	program search
	•	school/college drilldown
	•	newest programs
	•	recently updated programs
	•	recent catalog changes
	•	recently changed courses
	•	discussion-aware modules

Utility module

The site should include an Around the WGU web module with clearly separated groups:
	•	Official WGU channels
	•	Community discussion spaces
	•	Career / support channels

⸻

7. Website data in the old repo

The site data and related outputs currently live in the old repo.

You will need to inspect and selectively migrate from there.

Likely relevant areas include:
	•	outputs/site_data/
	•	canonical CSV/JSON artifacts
	•	site export files
	•	any scripts used to generate those outputs
	•	docs that explain provenance and schema

Use the documented outputs, not guesswork.

If file placement is ambiguous, inspect the old repo and confirm before migrating.

⸻

8. What belongs in this repo

This repo should include:
	•	website source
	•	canonical site data artifacts
	•	minimal reproducible scripts required to generate website data
	•	public docs
	•	deployment/workflow config

This repo should not initially include:
	•	raw PDF archive
	•	raw extracted text archive
	•	obsolete parser versions
	•	archive_legacy clutter
	•	unrelated wgu-reddit internals
	•	broad Reddit pipeline internals
	•	one-off debugging files
	•	scratch notebooks unless explicitly needed

Auditable does not mean dumping every historical file into this repo.

⸻

9. Repo hygiene rules

Keep this repo public-clean and legible.

General rules
	•	prefer explicit structure
	•	prefer small, durable docs
	•	prefer current code over copied legacy clutter
	•	preserve provenance
	•	do not create unnecessary duplicate docs

Internal docs

Use _internal/ for working instructions and session memory.

Current internal docs:
	•	_internal/CC_START_HERE.md
	•	_internal/DEV_LOG.md

Public docs

Public-facing docs should live in normal repo locations later, likely:
	•	README.md
	•	docs/

Logging rule

Update _internal/DEV_LOG.md with:
	•	durable decisions
	•	migration status
	•	blockers
	•	next steps

Do not turn it into a transcript.

⸻

10. Working method for Claude Code

When starting major work in this repo:
	1.	read this file
	2.	read _internal/DEV_LOG.md
	3.	inspect the source-of-truth files in wgu-reddit
	4.	propose the minimal clean migration or build plan
	5.	execute in scoped steps
	6.	update _internal/DEV_LOG.md with durable results

Before moving code or data, explicitly identify:
	•	what will be copied
	•	what will be rewritten
	•	what will be left behind

If a source file in wgu-reddit looks obsolete or duplicated, do not assume. Confirm against the documented truth.

⸻

11. Immediate next steps for the first working session

The next Claude Code session in this repo should focus on:

Phase 1
	•	create repo hygiene files
	•	create public README
	•	create basic public docs scaffold
	•	propose the target repo structure

Phase 2
	•	identify the exact files/artifacts to migrate from wgu-reddit
	•	migrate only the necessary website data and supporting scripts
	•	normalize paths and references

Phase 3
	•	scaffold the site app
	•	wire in the current site-ready data
	•	begin the first pages:
	•	homepage
	•	course explorer
	•	course page
	•	timeline
	•	methods
	•	data page

Do not work on Reddit integration yet unless it is needed for page layout placeholders.

⸻

12. What success looks like in this repo

A successful near-term outcome is:
	•	wgu-atlas becomes the clean public home of the project
	•	the website can build from committed/public data artifacts
	•	the repo is understandable to outsiders
	•	the site shell can be developed without depending on the old repo
	•	the project remains credible, auditable, and easy to maintain

⸻

13. If unsure

If something seems unclear:
	•	check the three source-of-truth files in wgu-reddit
	•	prefer documented conclusions over re-analysis
	•	show representative evidence before making structural decisions

When in doubt, optimize for:
	•	clarity
	•	minimalism
	•	provenance
	•	trustworthiness


14. Ordered implementation plan

Follow this order unless a real blocker requires adjustment.

Phase 1 — Repo hygiene and internal setup
	1.	Read:
	•	_internal/CC_START_HERE.md
	•	_internal/MIGRATION_HANDOFF.md
	2.	Create or replace the basic repo hygiene files:
	•	README.md
	•	.gitignore
	•	.editorconfig
	•	LICENSE
	•	_internal/DEV_LOG.md
	3.	Propose the initial public repo structure before migrating any code or data.
	4.	Keep the repo minimal, public-clean, and auditable.

Phase 2 — Migration from wgu-reddit
	5.	Use _internal/MIGRATION_HANDOFF.md as the authoritative migration map.
	6.	Migrate only the files/artifacts needed for the first WGU Atlas build.
	7.	Do not migrate:
	•	raw catalog PDFs/text
	•	obsolete parser versions
	•	archive/legacy clutter
	•	unrelated Reddit Analyzer internals
	8.	Normalize file paths and references so the new repo no longer depends structurally on the old repo.
	9.	Update _internal/DEV_LOG.md with what was migrated, what was left behind, and any path or build issues discovered.

Phase 3 — Pause for clean migration review
	10.	Stop after migration and report the resulting repo structure, migrated artifacts, and any remaining cleanup needs.
	11.	Do not start frontend work until the migration state is clean and understandable.

Phase 4 — Site scaffold
	12.	Scaffold the site using the preferred stack:

	•	Next.js
	•	TypeScript
	•	Tailwind

	13.	Build the first site shell for:

	•	homepage
	•	course explorer
	•	course page
	•	timeline
	•	methods
	•	data page

	14.	Use the committed static data artifacts as the source of truth for the first build.

Phase 5 — GitHub Pages and deployment
	15.	Do not configure GitHub Pages before the site shell exists.
	16.	Once the site can build locally, add the deployment workflow for GitHub Pages via GitHub Actions.
	17.	Then enable GitHub Pages and deploy the first live version.
	18.	After the first live deploy, future iterations can proceed against the live site.

Phase 6 — Public hardening pass
	19.	After migration and before major feature expansion, do a public hardening pass focused on:

	•	code cleanup
	•	build reproducibility
	•	provenance clarity
	•	trust/auditability documentation

	20.	Make the repo easy for a skeptical technical reader to inspect and understand.

Phase 7 — Later work (not first-session priorities)
	21.	After the initial site is live, later phases may include:

	•	program pages
	•	program roster-per-edition matrix
	•	Reddit integration
	•	LLM-generated course guides
	•	successor/predecessor inference
	•	richer timeline/event coverage

Working rule

At each phase boundary:
	•	summarize what changed
	•	update _internal/DEV_LOG.md
	•	keep durable conclusions, not transcript-style notes