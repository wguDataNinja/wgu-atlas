Yes — this absolutely deserves a single clear repo document. The goal is to explain what this pipeline does, why it exists, and how it runs monthly without forcing Codex (or humans) to rediscover it.

Below is a clean doc you can drop directly into the repo.

⸻

Program History from Catalogs

docs/program-history-from-catalogs.md

Purpose

This process reconstructs WGU program lineage and curriculum evolution from historical catalogs.

The output powers the Program History section on Atlas program pages, explaining how degree programs have evolved over time.

Example shown on Atlas:

2023 — Data Management / Data Analytics → Data Analytics

This allows students to understand:
	•	how a program changed
	•	what earlier programs existed
	•	how curriculum evolved

⸻

Overview of the Pipeline

The pipeline identifies program transitions and measures how curricula changed between programs.

The workflow combines:
	•	deterministic scripts
	•	one LLM step for semantic interpretation

catalog ingestion
      ↓
program timeline dataset
      ↓
transition universe detection
      ↓
LLM lineage proposals
      ↓
course comparison
      ↓
program history enrichment artifact
      ↓
Atlas program history display


⸻

Step 1 — Catalog Ingestion

Catalogs are scraped and parsed into structured artifacts.

Primary source:

WGU_catalog/

Key outputs:

outputs/program_names/*_program_blocks_v11.json
data/raw_catalog_texts/catalog_YYYY_MM.txt

These contain program descriptions and course rosters for each catalog edition.

⸻

Step 2 — Program Timeline Construction

Programs are tracked across catalog editions.

Generated artifact:

program_transition_universe.csv

This dataset identifies when programs:
	•	appear
	•	disappear
	•	coexist with similar programs

It provides candidate program transitions.

⸻

Step 3 — LLM Transition Identification

An LLM reviews the transition universe and identifies meaningful program lineage events.

Output:

data/program_lineage_events.json

Each event contains:
	•	transition type
	•	from_programs
	•	to_programs
	•	catalog boundary

Example:

Software Development → Software Engineering

The LLM is used only for semantic judgment, not computation.

⸻

Step 4 — Curriculum Comparison

A deterministic script compares course rosters between programs.

Script:

scripts/compare_program_courses.py

Output:

data/program_lineage_enriched.json

Metrics generated:
	•	shared_course_count
	•	courses_added
	•	courses_removed
	•	old_retained_pct
	•	new_inherited_pct
	•	jaccard_overlap

This quantifies how similar the programs are.

⸻

Step 5 — Final Program History Artifact

The enriched lineage data is transformed into a final artifact used for Atlas enrichment.

Script:

scripts/generate_program_history_enrichment.py

Output:

data/program_history_enrichment.json

This file contains:
	•	lineage events
	•	program relationships
	•	curriculum change metrics
	•	course differences

⸻

Step 6 — Atlas Enrichment Review

The artifact is reviewed to determine which events should appear on program pages.

Criteria:

Include events that explain:
	•	program renames
	•	program successors
	•	specialization splits
	•	family restructures
	•	major curriculum redesigns

Exclude events that are mostly:
	•	namespace changes
	•	minor catalog edits
	•	administrative restructuring

⸻

Example Program History Event

Example from the Data Analytics program:

Event:
BSDMDA → BSDA
Year: 2023
Transition: successor
Curriculum overlap: ~87%

Displayed on Atlas as:

2023 — Data Management / Data Analytics → Data Analytics


⸻

Result

Atlas now has historical program lineage explaining how WGU degrees evolved.

Typical examples include:
	•	Software Development → Software Engineering
	•	Cloud Computing → AWS/Azure specialization tracks
	•	MS Data Analytics → specialization tracks
	•	Business Administration restructuring
	•	Education programs → Educational Studies

⸻

Monthly Refresh Process

After the historical backfill, this pipeline runs during catalog updates.

Typical monthly workflow:

catalog scrape
→ update program timelines
→ detect new transitions
→ LLM lineage review
→ run curriculum comparison
→ update program history artifact

Most months produce:

0–2 new lineage events


⸻

Key Artifacts

Artifact	Purpose
program_transition_universe.csv	candidate program transitions
program_lineage_events.json	LLM-identified lineage events
program_lineage_enriched.json	curriculum comparisons
program_history_enrichment.json	final Atlas enrichment dataset


⸻

Design Philosophy

The system separates:

Semantic interpretation

Handled by LLM:
	•	identifying meaningful program lineage

Deterministic computation

Handled by scripts:
	•	curriculum comparisons
	•	artifact generation

This keeps the pipeline:
	•	reproducible
	•	inspectable
	•	stable across catalog updates.

⸻

If you’d like, I can also show you one small improvement that will make Atlas program pages much clearer: a tiny UI tweak for the Program History block that will make these events far easier to read.




changes to make :


Understood. Binary decision: include in Program History or do not include.

Below is the final inclusion list based on student value and clarity of lineage.

⸻

Add to Program History

These should appear on program pages.

Core Technology Programs

PLE-009
Cloud and Systems Administration → Cloud Computing

PLE-010
Cloud Computing → Cloud Computing specialization tracks (AWS / Azure)

PLE-011
Network Operations and Security → Network Engineering and Security (+ Cisco track)

PLE-013
Software Development → Software Engineering

PLE-014
Data Management / Data Analytics → Data Analytics

PLE-021
Cloud + Network programs → Cloud and Network Engineering

PLE-022
MS Information Technology Management → MS Information Technology (+ Product Management)

⸻

Graduate Program Specialization Splits

PLE-016
MS Data Analytics → Data Engineering / Decision Process Engineering / Data Science

PLE-017
MS Accounting → Auditing / Financial Reporting / Management Accounting / Taxation

⸻

Business Program Family Changes

PLE-008
Business degrees reorganized under Business Administration structure

PLE-019
Business Administration degrees moved back to discipline-specific degrees

⸻

Education Program Restructure

PLE-024
Education programs reorganized into Educational Studies pathways

⸻

Early Lineage Context (kept for continuity)

PLE-001
IT Security emphasis → Network Operations and Security

PLE-002
Networks Administration → Cloud and Systems Administration

PLE-005
Interdisciplinary Studies (K-8) → Elementary Education

⸻

Do NOT Add to Program History

These remain in the dataset but should not appear on the site.
	•	PLE-003 — Science education restructure (too granular)
	•	PLE-006 — Mathematics education restructure (same issue)
	•	PLE-007 — Special Education dual licensure
	•	PLE-018 — Marketing rename
	•	PLE-020 — Secondary science teaching split
	•	PLE-025 — Nursing pathway restructure
	•	PLE-026 — MBA Healthcare rename

⸻

Final Result

Program history will surface 15 lineage events across the catalog.

Each program page will show only the events relevant to that program code.

Example for the page you showed (BSDA):

Program History

2023
Data Management / Data Analytics → Data Analytics


⸻

Where We Are Now

You now have:
	•	catalog history metadata
	•	program lineage detection
	•	curriculum comparison
	•	enrichment decisions

Next step is straightforward:
	1.	Attach these events to the program pages
	2.	Then we document the monthly refresh workflow and compress repo docs.



    