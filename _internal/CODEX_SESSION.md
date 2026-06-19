Codex Session — WGU Atlas Catalog Pipeline, Mirror Update, and Repo-Split Readiness

This file is the master context for a Codex work session.

The session has two priorities:

1. Bring the catalog pipeline state forward cleanly after the newly discovered 2026-04, 2026-05, and 2026-06 editions
2. Prepare the codebase and docs for a future split of the catalog pipeline into its own repo (wgu-catalog) without prematurely performing that split

This is an agentic work session. You may read files, inspect code, run safe commands, and edit files. You must work from the repo state that actually exists on disk.

Mandatory logging

Write all meaningful actions, decisions, discoveries, edits, blockers, and outcomes to:

* _internal/CODEX_SESSION_LOG.md

This log is the single source of truth for the session.

Logging rules

* Append only; do not rewrite prior session history unless explicitly fixing a factual error
* Include a timestamp for every substantive entry
* Log:
    * what you inspected
    * what you changed
    * what you decided not to change
    * what you discovered
    * what still needs operator action
* If you run a command with important output, summarize the result in the log
* Do not keep important state only in ephemeral context

⸻

1. Project overview

There are currently two local repos and a planned third.

Current repos

wgu-reddit

Originally a Reddit analyzer capstone, but it now contains a full WGU catalog pipeline:

* PDF discovery and acquisition
* PDF text extraction
* parsing
* change tracking
* edition diffs
* site-data build layer

wgu-atlas

Public-facing static site plus Atlas QA subsystem:

* Next.js static site
* mirrored catalog outputs under data/catalog/
* site-data build scripts
* Atlas QA / RAG experiment over catalog and guide artifacts

Planned repo

wgu-catalog (does not yet exist as a separate repo)

This should become the dedicated home for the catalog pipeline:

* acquisition
* parsing
* change tracking
* edition diffs
* validation

Strategic intent

The catalog pipeline has outgrown being a dependency hidden inside wgu-reddit. The long-term target is:

* wgu-catalog → pure catalog/data pipeline
* wgu-reddit → Reddit analyzer + site-data build layer consuming catalog outputs
* wgu-atlas → public site + Atlas-side derived data and QA experiments

This session is not the repo split itself unless the operator explicitly activates that work.
This session should improve readiness for the split while prioritizing current correctness and documentation.

⸻

2. What just happened

The following has already been completed before this session:

* A new acquisition script was built: acquire_catalog.py
* It supports:
    * discovery/check mode
    * download mode
    * extraction mode
* Three new WGU catalog editions were found since the prior local state:
    * 2026-04
    * 2026-05
    * 2026-06
* All three were downloaded and extracted
* The full parser pipeline was re-run successfully
* The resulting changes were verified:
    * 28 new Education courses
    * 1 replacement (D436 replaced by E200)
* No program changes were found in those editions
* A parser footgun was discovered:
    * running the parser for a single edition wipes/rebuilds the cross-edition global index and downstream outputs incorrectly
    * always use full reprocess / --all for authoritative pipeline refreshes

This session should assume that discovery, download, extraction, and the full reprocess already happened.

⸻

3. Session priorities

P0 — highest priority

Mirror the fresh catalog outputs into wgu-atlas cleanly

The site and Atlas-side scripts need the new outputs. This is the most concrete immediate task.

P1

Update internal documentation so the new acquisition workflow and current edition state are not lost

Important docs currently lag reality.

P2

Improve split readiness without actually doing a risky partial split

Prepare boundaries, path strategy, and documentation so the future wgu-catalog split is easier and less error-prone.

P3

Identify parser/pipeline hardening opportunities revealed by this update

Especially structural health checks and path consistency.

⸻

4. What this session should accomplish

The agent should aim to complete as much of the following as is justified by actual repo state:

A. Verify the newly updated pipeline state

Confirm the following from the repo, not from this prompt alone:

* new raw PDFs/texts exist for 2026_04, 2026_05, 2026_06
* fresh helper / change-tracking / diff outputs exist
* outputs are internally consistent enough to mirror forward
* the single-edition parser footgun is reflected somewhere durable

B. Mirror current catalog outputs to wgu-atlas

Update wgu-atlas/data/catalog/ from the fresh wgu-reddit/WGU_catalog outputs.

C. Update key docs

At minimum, inspect and update the docs that describe:

* edition counts
* latest edition
* acquisition workflow
* pipeline ownership boundaries
* current mirror conventions

D. Improve transition readiness for wgu-catalog

Do not perform a full split unless explicitly activated.
Instead:

* clarify current ownership boundaries
* identify scripts/files that should migrate first
* reduce ambiguity in docs
* make path expectations explicit

E. Leave a strong next-step record

If work remains, log it clearly enough that a later Codex pass or weaker coding model can continue safely.

⸻

5. Explicit non-goals for this session

Do not do these unless explicitly activated by the operator:

* create the new wgu-catalog repo
* perform the full repo split
* broadly refactor Atlas QA
* re-architect the site
* build new user-facing features
* rerun long full-pipeline jobs unless necessary and operator-approved
* run long multi-query Atlas QA evals
* opportunistically clean unrelated code

Keep the session disciplined.

⸻

6. Current pipeline structure

Layer 0 — Acquire

Step	Script	Repo	Input	Output
Discover	acquire_catalog.py check	catalog pipeline	WGU catalog HTML page	edition list + URLs
Download	acquire_catalog.py download	catalog pipeline	edition IDs	data/raw_catalog_pdfs/catalog_YYYY_MM.pdf
Extract	built-in extract flow / pdfplumber	catalog pipeline	PDFs	data/raw_catalog_texts/catalog_YYYY_MM.txt

Layer 1 — Parse

Step	Script	Repo	Input	Output
Parse	parse_catalog_v11.py	catalog pipeline	raw text files	helpers + program outputs

Layer 2 — Change track

Step	Script	Repo	Input	Output
Track	build_change_tracking.py	catalog pipeline	helpers + program blocks	outputs/change_tracking/

Layer 3 — Edition diffs

Step	Script	Repo	Input	Output
Diff	build_edition_diffs.py	catalog pipeline	change tracking + helpers	outputs/edition_diffs/

Layer 4 — Validate

Step	Script	Repo	Input	Output
Validate	validate_editions.py	catalog pipeline	raw text + parser internals	validation artifact

Layer 4a — Site data build (wgu-reddit)

Step	Script	Repo	Input	Output
Site data	build_site_data.py	wgu-reddit	helpers + diffs + trusted outputs	outputs/site_data/

Layer 5 — Mirror to Atlas

Selected pipeline outputs are copied into:

* wgu-atlas/data/catalog/

Layer 6 — Site build (wgu-atlas)

Step	Script	Repo	Input	Output
Build site data	scripts/build_site_data.py	wgu-atlas	data/catalog/ + path config	public/data/
Build site	npm run build	wgu-atlas	site source + public data	static export

Layer 7 — Atlas QA / experimental knowledgebase (wgu-atlas)

This is a separate internal track, not the main public Atlas product. Do not treat it as the primary objective of this session.

⸻

7. Current known state

Catalog corpus

Expected local pipeline state:

* 111 editions on disk
* latest local edition: 2026-06
* three unrecoverable older gaps remain:
    * 2017-02
    * 2017-04
    * 2017-06

Newly observed edition changes

Transition	Courses added	Courses removed	Programs changed
2026-03 → 2026-04	0	0	0
2026-04 → 2026-05	28	0	0
2026-05 → 2026-06	1	1	0

Important specific changes:

* E054–E101 introduced in Education
* E200 introduced
* D436 removed/replaced

Known parser footgun

This must be preserved in docs/logs:

* parse_catalog_v11.py is authoritative only when run as a full corpus process
* running it for a single edition rebuilds global indexes from an incomplete set and invalidates downstream outputs

⸻

8. Priority task list

P0 — mirror fresh outputs into Atlas

Inspect actual paths and copy/update the relevant artifacts from the catalog pipeline into wgu-atlas/data/catalog/.

Expected families:

* outputs/change_tracking/
* outputs/edition_diffs/
* outputs/helpers/
* outputs/program_names/
* data/raw_catalog_texts/

Be careful with large/gitignored files.

Expected mirror targets

From pipeline repo into Atlas:

* change_tracking/
* edition_diffs/
* helpers/
* program_names/
* raw_catalog_texts/

Log exactly what was copied and what was intentionally skipped.

P1 — update core docs

Likely targets include, depending on actual repo state:

* WGU_catalog/README_INTERNAL.md
* wgu-atlas/data/catalog/README.md
* wgu-atlas/README.md
* wgu-atlas/AGENTS.md
* wgu-atlas/_internal/ATLAS_CONTROL.md
* any boundary/ownership docs that are now stale

Minimum doc themes to correct:

* latest edition
* edition count
* acquisition workflow
* new acquire_catalog.py
* current repo-boundary intent
* footgun / safe full-reprocess rule

P2 — make split-readiness more concrete

Without splitting the repo:

* identify the scripts/modules that clearly belong in future wgu-catalog
* identify current path assumptions that will break the split
* document the minimal move order
* make sure docs stop treating the catalog pipeline as an incidental part of wgu-reddit

P3 — parser hardening ideas

Inspect whether there is a clean place to add or at least document lightweight structural health checks for newly acquired editions:

* Total CUs anchor found
* AP header found
* course/program count sanity
* file size anomaly
* copyright/footer regression risk

Prefer documenting and preparing this over broad implementation unless there is a very small obvious win.

P3 — path unification readiness

Inventory the current path conventions:

* script-relative pathing
* env-var pathing
* hardcoded pathing

Document the real current state and likely unification target:

* WGU_CATALOG_ROOT
    or
* WGU_REDDIT_PATH / future catalog root

⸻

9. Operator/runtime rules

Safe to run

Codex may run:

* inspection commands
* short validation commands
* small build steps if clearly needed and unlikely to be long-running
* local file comparisons
* targeted copy/mirror operations

Do not run without operator approval

Codex must not independently run:

* large full-pipeline rebuilds if they may take a while
* long multi-query Atlas QA evals
* broad repo-wide migrations
* anything destructive without a clear rollback path

If a long run would be useful, hand back:

* the exact command
* what it tests
* what output to inspect

⸻

10. Important path references

Catalog pipeline side

Likely root:

* wgu-reddit/WGU_catalog/

Important subpaths:

* scripts/acquire_catalog.py
* parse_catalog_v11.py
* build_change_tracking.py
* build_edition_diffs.py
* validate_editions.py
* data/raw_catalog_pdfs/
* data/raw_catalog_texts/
* outputs/helpers/
* outputs/change_tracking/
* outputs/edition_diffs/
* outputs/program_names/
* outputs/trusted/2026_03/

Atlas side

Likely root:

* wgu-atlas/

Important subpaths:

* data/catalog/
* public/data/
* scripts/build_site_data.py
* _internal/ATLAS_CONTROL.md
* _internal/ATLAS_REPO_MEMORY.md
* _internal/DEV_LOG.md

⸻

11. Agent guidance — what a literal-minded agent may get wrong

Do not make these mistakes:

1. Do not start the repo split just because the target architecture is described
    * split-readiness is in scope
    * executing the split is not unless explicitly activated
2. Do not treat Atlas QA as the main product surface
    * it is an internal experimental track
    * the Atlas site is the main product
3. Do not rerun the whole parser pipeline just to “be safe”
    * it was already run
    * verify repo state first
4. Do not lose the parser footgun
    * this is a critical operational finding
    * it must land in durable docs/logs
5. Do not mirror blindly
    * inspect target directories first
    * log what changes
6. Do not normalize docs by hand-waving counts
    * verify counts from actual repo state when possible
7. Do not leave future split boundaries implicit
    * if you clarify them, write them down

⸻

12. Recommended execution order

1. Open _internal/CODEX_SESSION_LOG.md; append preflight entry
2. Inspect actual repo state in both repos
3. Confirm the new editions and outputs are present
4. Mirror fresh outputs into wgu-atlas/data/catalog/
5. Update the most important stale docs
6. Clarify split-readiness boundaries in docs/logs
7. Inventory path conventions and note unification target
8. Record remaining work and operator-only follow-ups

⸻

13. Preferred output of this session

By the end of the session, the ideal result is:

* Atlas mirror updated to current catalog outputs
* key docs updated to current reality
* the parser footgun documented durably
* split-readiness clarified
* no premature repo split attempted
* _internal/CODEX_SESSION_LOG.md contains a trustworthy session history
* any longer or riskier next steps are handed back as explicit commands / backlog items

⸻

14. Future split plan (reference only, not active implementation)

Likely Phase 1

Create wgu-catalog and move:

* acquisition
* parsing
* validation
* change tracking
* edition diffs
* supporting libs/config

Likely Phase 2

Shrink wgu-reddit to:

* Reddit analyzer
* site-data build layer that consumes catalog outputs

Likely Phase 3

Update wgu-atlas to:

* reference the new catalog boundary clearly
* continue mirroring or eventually read from a more stable catalog-owned source

This is planning context only. Do not execute the split unless explicitly activated.