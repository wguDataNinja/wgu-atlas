Here is an updated, denser operator doc draft with the key session learnings folded in.

# ATLAS Operator Context

```yaml
operator_context_version: 1.1
last_updated: 2026-03-20
owner_role: active_gpt_operator
scope: project_control_surface
primary_read_order:
  - _internal/ATLAS_OPERATOR_CONTEXT.md
  - docs/DECISIONS.md
  - docs/ATLAS_SPEC.md
  - _internal/PROJECT_CONTINUITY_ATLAS.md
  - _internal/SESSION_LOG.md
supersedes_as_primary_control_doc:
  - _internal/PROJECT_CONTINUITY_ATLAS.md
canon_authority:
  policy: docs/DECISIONS.md
  implementation: docs/ATLAS_SPEC.md
  workflow: _internal/WORKFLOW_SESSION_PROTOCOL.md
  continuity: _internal/SESSION_LOG.md
agent_registry:
  AI-1:
    role: official_resource
    class: module_agent
    power: high_or_low_ok
    primary_dir: _internal/official_resource/
    current_state: initialized_pause_ready
  AI-2:
    role: documentation_control_plane
    class: low_power_default
    power: low
    primary_dir: _internal/
    current_state: active_operator_doc_support
  continuity_review:
    role: continuity_review
    class: module_agent
    power: high_or_low_ok
    primary_dir: _internal/continuity_review/
    current_state: initialized_waiting_validation_batch
  high_power_codex:
    role: hard_planning_spec_code_deep_analysis
    class: selective_escalation
    power: high
    primary_dir: none
    current_state: use_only_when_needed
session_defaults:
  low_power_agent_for:
    - doc maintenance
    - session close-out
    - backlog snapshots
    - module continuity updates
    - bounded planning memos
  high_power_for:
    - hard planning
    - spec design
    - coding
    - validator/export/runtime work
    - deep artifact analysis

1) Purpose and Contract

This is the primary operating control surface for active GPT sessions in wgu-atlas.

Use it to:
	•	start fast without re-reading many files
	•	see current module state, priorities, blockers, and next options
	•	direct agents with minimal orientation cost
	•	keep policy, implementation, and execution control synchronized

Authority split:
	•	docs/DECISIONS.md = normative policy
	•	docs/ATLAS_SPEC.md = factual implementation/runtime/spec
	•	this file = execution control, current state, module routing, backlog options

2) Mission / Product Posture / Success Criteria

Mission:
	•	make canonical WGU program/course information easier to use than catalog PDFs
	•	help students learn schools, degrees, and courses through ordinary browsing
	•	preserve provenance clarity and trust boundaries
	•	use history when it clarifies the current entity

Product posture:
	•	Atlas is a reference/explainer product, not a discussion feed
	•	current student navigation is primary
	•	official WGU resources are the next layer after catalog facts
	•	history/lineage is supporting context, not homepage identity
	•	simplicity, reproducibility, and low-maintenance updating are hard constraints

Success criteria:
	•	official information is easier to navigate and understand than source PDFs
	•	useful context emerges through normal browsing of degrees/courses/schools
	•	Atlas interpretation stays visibly separate from source material
	•	project remains explainable and reproducible for portfolio/interview use
	•	updates can be repeated with modest operator effort

3) Operator Priorities

Ranked current priorities:
	1.	preserve coherent control across canon docs, operator docs, and active module state
	2.	choose the highest-leverage next module/workstream rather than defaulting to the most recent one
	3.	advance official-resource planning/review as the likely next major module
	4.	keep lineage/continuity systems stable and pause-ready unless re-selected as the next implementation track
	5.	avoid low-leverage churn, broad cleanup, repeated summaries, and unnecessary agent spend

4) Site / Module Map

4.1 Product surfaces
	•	/ homepage / entry experience
	•	/courses, /courses/[code] course browse + detail
	•	/programs, /programs/[code] program browse + detail
	•	/schools, /schools/[slug] school browse + detail
	•	/timeline historical timeline
	•	/compare program comparison
	•	/data data downloads
	•	/methods methods/provenance/documentation
	•	search / browse / navigation surfaces

4.2 Core modules
	•	Catalog baseline
	•	Program detail page value
	•	Course detail page value
	•	School page value
	•	Official resource layer
	•	Program lineage / degree history
	•	Continuity review
	•	Compare
	•	Search / browse / navigation
	•	Methods / data / downloads

5) Workstream Status Matrix

Workstream	Status	Current objective	Why it matters	Primary blockers	Next executable step
Project / module planning	active	choose next major module and sequence	prevents recency bias and wasted implementation	priorities still being pressure-tested	run/finish high-level planning discussion
Official Resource module	initialized_in_progress	move from planning memo to first curation-ready queue	likely next major student-facing value layer	queue artifact not built yet; attachment model still tightening	build regulatory/licensure/disclosure candidate queue
Continuity Review module	initialized_lightweight	validate compact review method	keeps continuity work bounded while preserving momentum	first validation batch not created	create 4-card validation batch
Program Lineage / Degree History	structurally_ready_pauseable	keep ready for export/UI if chosen	strong supporting differentiator; system now documented/validated	export step + runtime wiring not implemented	implement export/UI only if selected after planning
Core Catalog baseline	stable	preserve deterministic refresh/update path	foundation of all site surfaces	only matters during refresh cycles	no immediate action
Homepage / entry experience	deferred_next	revisit product framing later	important first impression but downstream of module choices	depends on clearer product emphasis	defer until official-resource + module priorities are clearer
Reddit / community	deferred	none now	future course-page context layer only	intentionally deferred by posture	no current action

6) Current Module Snapshots

6.1 Official Resource

Status:
	•	module initialized
	•	planning memo complete
	•	pause-ready
	•	next task locked

Key files:
	•	_internal/official_resource/README.md
	•	_internal/official_resource/SESSION_LOG.md
	•	_internal/official_resource/ARTIFACTS.md
	•	_internal/official_resource/next_workstream_memo.md

Locked direction:
	•	next bounded workstream = regulatory / licensure / disclosure pass
	•	outcomes + accreditation completeness audit stays immediately adjacent behind it
	•	current priority order:
	1.	regulatory/licensure/disclosure
	2.	outcomes + accreditation completeness audit
	3.	specialization / track / variant
	4.	school governance / context
	5.	Official WGU YouTube
	6.	Career Services YouTube
	7.	selective program landing pages

Next artifact:
	•	_internal/official_resource/regulatory_candidate_queue.md

6.2 Continuity Review

Status:
	•	module initialized
	•	method decided
	•	waiting for first tiny validation batch

Key files:
	•	_internal/continuity_review/README.md
	•	_internal/continuity_review/SESSION_LOG.md
	•	_internal/continuity_review/ARTIFACTS.md
	•	_internal/continuity_review/review_method_plan.md

Locked method:
	•	first review format = compact text cards
	•	first validation batch size = 4
	•	first pattern classes:
	•	clean successor
	•	rebuilt replacement
	•	split family
	•	ambiguous case
	•	example IDs currently planned:
	•	PLE-001
	•	PLE-011
	•	PLE-010
	•	PLE-012

Guardrail:
	•	this module is for bounded validation, not a full continuity feature or large review batch

Next artifact:
	•	_internal/continuity_review/validation_batch_01.md

6.3 Program Lineage / Degree History

Status:
	•	structurally ready
	•	can be paused
	•	no longer automatic top priority

Canonical artifacts:
	•	data/lineage/lineage_decisions.json = curation/display authority
	•	data/program_history_enrichment.json = computed metrics source
	•	scripts/validate_lineage_decisions.py = validation gate
	•	public/data/program_lineage.json = pending page-facing export target

Locked curation totals:
	•	approved events: 17
	•	excluded events: 7
	•	pending HITL: 2 (PLE-012, PLE-023)
	•	pending gap check: 1 (PLE-028)

Blocking unresolved entities:
	•	pending HITL programs: BSHHS, MHA, MATSPED
	•	pending gap-check programs: MEDETID, MEDETIDA, MEDETIDK12

Current posture:
	•	safe to pause
	•	resume only if lineage export/UI becomes the chosen next implementation track

7) Locked Decisions Snapshot (Do Not Re-litigate by Default)
	•	lineage_decisions.json is durable curation overlay and display authority
	•	events absent from lineage_decisions.json are suppressed by default
	•	display_state overrides heuristic site_worthy
	•	approved zero-overlap pairs require zero_overlap_rationale
	•	low/unconfirmed overlap approved events require wording guard
	•	if predecessor is still active, classify new program as pathway_variant, not lineage
	•	Program History is program-page enrichment, not a separate product
	•	official resources come before Reddit/community
	•	YouTube comes before Reddit/community
	•	homepage rethink is not first move
	•	official-resource layer is likely the next major module
	•	continuity review is a small parallel validation track, not a main buildout

8) Canon Docs and Operator Docs

Doc	Role	When to update
docs/DECISIONS.md	policy / curation rules	when rules change
docs/ATLAS_SPEC.md	implementation/spec/runtime truth	when artifacts/scripts/contracts change
_internal/ATLAS_OPERATOR_CONTEXT.md	primary operator control plane	when module state, priorities, agent map, or backlog options change
_internal/PROJECT_CONTINUITY_ATLAS.md	compact continuity companion	light refreshes / portable context
_internal/WORKFLOW_SESSION_PROTOCOL.md	reusable execution protocol	when workflow changes
_internal/SESSION_LOG.md	session ledger	at session close / major lock

9) Important Artifacts and Locations

9.1 Operator docs
	•	_internal/ATLAS_OPERATOR_CONTEXT.md
	•	_internal/PROJECT_CONTINUITY_ATLAS.md
	•	_internal/WORKFLOW_SESSION_PROTOCOL.md
	•	_internal/SESSION_LOG.md

9.2 Program lineage
	•	data/lineage/lineage_decisions.json
	•	data/program_transition_universe.csv
	•	data/program_link_candidates.json
	•	data/program_lineage_enriched.json
	•	data/program_history_enrichment.json
	•	scripts/validate_lineage_decisions.py
	•	scripts/build_site_data.py

9.3 Official-resource module
	•	_internal/official_resource/README.md
	•	_internal/official_resource/SESSION_LOG.md
	•	_internal/official_resource/ARTIFACTS.md
	•	_internal/official_resource/next_workstream_memo.md
	•	data/enrichment/README.txt
	•	data/source_enrichment_manifest.json
	•	public/data/official_resource_placements.json

9.4 Continuity-review module
	•	_internal/continuity_review/README.md
	•	_internal/continuity_review/SESSION_LOG.md
	•	_internal/continuity_review/ARTIFACTS.md
	•	_internal/continuity_review/review_method_plan.md

10) Workflow Model

Execution policy:
	•	GPT briefly reflects on agent output
	•	GPT then writes the next agent work session
	•	reflections should stay compact
	•	prefer low-power agents by default
	•	escalate to high-power only when reasoning/spec/code demands it
	•	full outputs go to files; chat gets compact review summaries only
	•	avoid broad repo roaming during focused sessions

Per-session minimum:
	1.	read this doc + relevant module README
	2.	identify the single highest-leverage task or decision point
	3.	assign the cheapest capable agent
	4.	save full artifacts
	5.	append concise session log
	6.	update this doc if state/priorities/options changed

11) High-Priority Unresolved Questions

ID	Question	Type	Default if unresolved
Q-LIN-012	Should PLE-012 (BSHSC -> BSHHS) be approved lineage?	HITL	reject_history
Q-LIN-023	Should PLE-023 (MHL -> MHA) be approved lineage?	HITL	reject_history
Q-LIN-028	Is PLE-028 legitimate continuity or gap-linked new launch?	gap investigation	split/retire+new
Q-LIN-MATSPED	Is MSSP predecessor for MATSPED acceptable?	HITL	new_from_scratch
Q-OFF-ATTACH	What minimal robust YouTube attachment model should follow sitemap passes?	placement model	defer rollout

12) Current Backlog Options

Option	Type	Value	Why now	Why not now
Project/module planning	planning	choose next major module rationally	project is at prioritization moment	none
Official Resource candidate queue	review/planning artifact	converts module planning into curation-ready work	likely next module	may wait until close-out docs fully synced
Continuity Review validation batch	review	tests whether continuity method is actually useful	small, bounded, parallel	lower leverage than module planning
Lineage export/UI	implementation	turns ready lineage system into live feature	technically ready foundation exists	may not be the highest-value next implementation
Session close-out + operator doc refinement	control-plane	makes future sessions cheap and coherent	natural stopping point now	none

13) Recommended Next Sessions (Ordered)
	1.	complete project/module planning and choose the next major workstream
	2.	if Official Resource is confirmed: build _internal/official_resource/regulatory_candidate_queue.md
	3.	run continuity-review 4-card validation batch
	4.	only then choose whether lineage export/UI is the next implementation track
	5.	if needed, perform formal session close-out / operator-doc sync pass

14) Deferred / Not-Now Scope
	•	Reddit/community enrichment
	•	broad homepage redesign before module priorities settle
	•	broad YouTube surfacing before attachment model stabilizes
	•	complex continuity/lineage visualization systems
	•	course-level continuity buildout
	•	compare expansion beyond current bounded V1 scope
	•	speculative cleanup that does not improve an active module or operator workflow

15) Session Handoff / Close-Out

At session end, record:
	•	what changed
	•	what decisions were locked
	•	what modules are pause-ready
	•	what remains blocked
	•	realistic next work options
	•	exact next starting task if one is chosen

Quality bar:
	•	next operator resumes in under 5 minutes
	•	unresolved questions appear once in tables/IDs, not repeated in prose
	•	module state is visible without reading large artifacts

16) Active GPT Responsibility Standard

The active GPT must:
	•	challenge low-leverage work
	•	prefer actions that improve both delivery speed and correctness
	•	keep policy, implementation, and operator docs synchronized
	•	protect provenance boundaries and deterministic workflows
	•	avoid unnecessary verbosity in reflections
	•	maximize project progression rate and final quality
	•	regularly step back and ask whether the current work is the highest-leverage work

Practical rule:
	•	if a task does not reduce a blocker, lock a decision, improve a live module, or lower future orientation cost, deprioritize it.

Big changes I made:
- added richer YAML metadata and agent registry
- folded in module pause-ready states
- updated priorities so lineage is no longer default-top
- added explicit backlog/options
- made workflow model match your desired “brief reflection -> next agent session” behavior
- embedded the low-power vs high-power division directly in the doc

I agree with you: this is the density target future docs should move toward.





