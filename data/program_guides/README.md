# Program Guides — Data Directory

**Human entry point for the WGU program-guide data area.**

---

## What this directory is

WGU publishes a Program Guidebook PDF for every active degree. This directory contains everything produced by extracting structured data from those PDFs — 115 guides covering every active program.

The extracted data includes:
- Course descriptions and competency bullets (per course, per program)
- Program schedule context (Standard Path: term, credit units)
- Course-to-program mappings (which courses appear in which programs)

**This is an internal data preparation directory.** Nothing here is currently published to the Atlas site. The next step is building the artifact generator that publishes approved guide content to Atlas degree pages.

**Post-program-guides direction:** The project is now centered on three tracks:
1. **Degrees** - immediate implementation target using completed guide data
2. **Courses** - major follow-on opportunity with 751 enriched courses
3. **Homepage** - sequenced after inner-surface strengthening

---

## Current state

| Area | Status |
|------|--------|
| Guide corpus collected and parsed | **Complete** — 115/115 guides |
| Per-course descriptions and competency bullets extracted | **Complete** — 2,593 courses covered |
| Guide courses matched to Atlas catalog codes | **Complete** — 751 courses matched; 542 unmatched (irreducible) |
| Cert → course mapping artifact | **Complete** — 9 auto-accepted, 21 review-needed |
| Prereq relationship artifact | **Complete** — 50 auto-accepted, 21 review-needed |
| SP family classification artifact | **Complete** — 115 programs, 7 named families |
| Anomaly registry | **Complete** — 9 records with handling rules |
| Policy and schema for Atlas degree-page enrichment | **Designed** — not yet built |
| Guide data published to Atlas site | **Not started** |

**Data collection and extraction is closed.** The next work is building the Atlas-facing output layer.

---

## Numbers that matter

### Guide corpus

- 115/115 guides parsed and validated
- 111 guides: fully usable | 4 guides: partially usable (caveats apply) | 0 excluded
- Parse confidence: 96 HIGH / 17 MEDIUM / 2 LOW
- 2,593 course descriptions extracted (100% of guide courses)
- 2,591 competency sets; 2,568 program schedule rows

### Course enrichment coverage

- **751 canonical courses** have guide-derived enrichment (descriptions + competency bullets + program context)
- 730 courses with descriptions; 729 with competency bullets
- 723 courses with program schedule context; 730 with program group context
- 542 course titles in guides could not be matched to the Atlas catalog — irreducible without catalog changes
- 6 course titles matched only to inactive catalog entries with no decisive signal — excluded

---

## Where to start reading

**To understand what this corpus covers:** [audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md](audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md)

**To build the Atlas degree-enrichment artifact layer:** [audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md](audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md)

**To see current enrichment numbers:** [enrichment/course_enrichment_summary.json](enrichment/course_enrichment_summary.json)

**To understand what claims are safe to make:** [audit/program_guide_claims_register.md](audit/program_guide_claims_register.md)

**To audit course-matching decisions (resolutions, deferred, unresolvable):** [bridge/merge_summary.json](bridge/merge_summary.json)

**To understand what cert→course mappings exist:** [cert_course_mapping.json](cert_course_mapping.json)

**To understand what prereq relationships exist:** [prereq_relationships.json](prereq_relationships.json)

**To understand how each program's SP is categorized:** [sp_family_classification.json](sp_family_classification.json)

**To understand the 7 named program families:** [sp_families.json](sp_families.json)

**To understand known extraction anomalies and handling rules:** [guide_anomaly_registry.json](guide_anomaly_registry.json)

**For the full product handoff (surface-by-surface payload, shape families, merge planning):** [_internal/program_guides/GUIDE_ARTIFACTS_PRODUCT_HANDOFF.md](../../_internal/program_guides/GUIDE_ARTIFACTS_PRODUCT_HANDOFF.md)

---

## Top-level guide target artifacts

Five JSON files live directly in this directory (not in a subdirectory). These are the Session 29 target extraction outputs.

| File | Contents | Status |
|------|----------|--------|
| `cert_course_mapping.json` | Cert→course mappings: 9 auto-accepted (high confidence, 3+ programs), 21 review-needed (medium, single-program or fragment) | Complete |
| `prereq_relationships.json` | Prereq relationships: 50 auto-accepted, 21 review-needed, 71 total. Types: explicit-course, code-anchored, cumulative-sequence, inverted-capture | Complete |
| `sp_family_classification.json` | Per-program SP classification (A/B/C/D) for all 115 programs | Complete |
| `sp_families.json` | 7 named family definitions: BSSWE, MACC, MSRNN, BSCNE, PMCNU, MSMK, BAELED | Complete |
| `guide_anomaly_registry.json` | 9 anomaly records with detection method, source-side vs extraction-side, and Atlas handling rules | Complete |

**Also present:** `guide_manifest.json` — earlier-phase guide structure manifest (pre-extraction-targets, covers guide presence flags and structural counts per guide).

For the full product-facing payload reference including merge planning, shape families, and known gaps, see `_internal/program_guides/GUIDE_ARTIFACTS_PRODUCT_HANDOFF.md`.

---

## Subdirectory guide

### `parsed/` — 115 `*_parsed.json` files

**What:** Structured output from `parse_guide.py` for each of the 115 guides.

**Contains per guide:** degree_title, version, pub_date, standard_path rows (title, CUs, term), areas_of_study groups (courses with descriptions and competency bullets), capstone, prereq mentions.

**Status:** Canonical. Do not regenerate unless a parser fix is applied.

**Role:** Primary source of truth for guide content. Everything downstream reads from here.

---

### `validation/` — 115 `*_validation.json` files

**What:** Per-guide quality scores — confidence (HIGH/MEDIUM/LOW), anomaly flags, warning counts, reconciliation of AoS vs SP course counts.

**Status:** Canonical. Produced by `parse_guide.py` alongside parsed output.

**Role:** Gate artifact. Downstream systems should respect confidence and anomaly signals.

---

### `manifest_rows/` — 115 `*_manifest_row.json` files

**What:** Compact per-guide summary row: program code, family, disposition, sp_status, confidence, counts. Aggregated into the corpus manifest.

**Status:** Canonical. Source of truth for corpus-level counts.

**Role:** Input to corpus manifest. Used by the Atlas degree-enrichment artifact generator for per-guide inclusion/exclusion decisions.

---

### `family_validation/` — gate reports and rollout summaries per family (19 families)

**What:** Per-family rollout summaries and gate reports tracking which guides were validated together and their aggregate confidence.

**Files:** `{family}_rollout_summary.{md,json}`, `{family}_gate_report.{md,json}`

**Status:** Canonical. Reflects final validated state of each family.

**Role:** Historical rollout record. Shows which families were complete at Phase C close.

---

### `bridge/` — course-to-program bridge and resolution pipeline

The bridge directory contains the multi-stage pipeline that maps guide course titles to canonical course codes.

**Key files:**

| File | Role |
|------|------|
| `program_guide_roster_bridge.json` | Original bridge (pre-resolution) — 115 guides, anchor class counts, alias crosswalk |
| `index.json` | Guide index used by downstream scripts |
| `guides/` | Per-guide bridge files (original, pre-resolution) |
| `resolution_log_deterministic.json` | Log of 1,428 deterministic resolutions with signals used |
| `guides_resolved/` | Per-guide files after deterministic resolution (has `ambiguous_residual` rows) |
| `llm_packets/packets.json` | 171 LLM adjudication context packets (residuals) |
| `llm_packets/adjudication_results.json` | LLM adjudication decisions (163 high + 2 medium + 6 unresolvable) |
| `guides_merged/` | **Final merged per-guide files** — no ambiguous rows remain |
| `merge_summary.json` | Post-merge coverage counts, medium cases, unresolvable cases |

**Pipeline stages:**
1. `build_roster_bridge.py` → `guides/` (original bridge)
2. `resolve_ambiguous_deterministic.py` → `guides_resolved/` (deterministic applied)
3. `build_ambiguous_resolution_packets.py` + `write_adjudication_results.py` → LLM adjudication
4. `merge_resolved_ambiguous.py` → `guides_merged/` (final merged state)

**`guides_merged/` is the canonical bridge output.** Downstream enrichment reads from here.

#### The 2 medium-confidence cases (audit record)

Both accepted with status `llm_resolved_medium_reviewed`. See [bridge/merge_summary.json](bridge/merge_summary.json) for rationale.

- `BSIT__introduction_to_it__aos` → E004
- `BSPRN__community_health_and_population_focused_nursing__aos` → C826

#### The 6 unresolvable cases (audit record)

All 6 are "Health Equity and Social Determinants of Health" for BSHS, BSPH, BSPSY (AoS + SP). Both candidates (D057, D302) are inactive with zero current programs. Status: `unresolvable`. Excluded from enrichment. Original candidates preserved in bridge files and `merge_summary.json`.

---

### `enrichment/` — course enrichment candidates

**What:** The primary deliverable of the data extraction phase. For each course that could be confidently matched to a guide row, this contains all guide-derived content: descriptions, competency sets, program context, program group context.

**Key files:**

| File | Role |
|------|------|
| `course_enrichment_candidates.json` | Full enrichment data — 751 courses |
| `course_enrichment_summary.json` | Coverage counts and match-tier distribution |

**Status:** Current. Generated by `build_course_enrichment_candidates.py` against the final merged course-matching files.

**Coverage:** 751 courses, 730 with descriptions, 729 with competency bullets.

**Role:** Input to Atlas degree-page enrichment (the artifact generator, not yet built). Candidate data for future Atlas course-page enrichment. College-level uses also possible later.

---

### `audit/` — planning, policy, schema, and reference docs (52 files)

The audit directory contains the policy decisions, schemas, assessments, and planning artifacts produced during the workstream. It is the authoritative reference for **why things are the way they are**.

#### Read these first (most important)

| File | Role |
|------|------|
| [PROGRAM_GUIDE_CORPUS_MANIFEST.md](audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md) | Canonical corpus facts — 115 guides, counts, coverage, confidence |
| [program_guide_claims_register.md](audit/program_guide_claims_register.md) | Approved vs disallowed claims about the corpus |
| [program_guide_adversarial_review.md](audit/program_guide_adversarial_review.md) | Claim stress test — what wording is safe |
| [PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md](audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md) | Single entry point for building the Atlas degree-enrichment artifact layer — policy, schema, and implementation plan |

#### Course-matching methodology and enrichment design

| File | Role |
|------|------|
| [program_guide_roster_bridge_assessment.md](audit/program_guide_roster_bridge_assessment.md) | How guide course titles are matched to catalog codes; coverage model; match-tier definitions |
| [program_guide_roster_bridge_schema.md](audit/program_guide_roster_bridge_schema.md) | Schema for the course-matching artifact files |
| [course_anchorability_matrix.md](audit/course_anchorability_matrix.md) | Which courses can be matched and at what confidence |
| [course_signal_quality_review.md](audit/course_signal_quality_review.md) | Quality assessment of each matching signal |
| [course_enrichment_candidate_schema.md](audit/course_enrichment_candidate_schema.md) | Schema for the enrichment candidate output files |
| [ambiguous_course_resolution_strategy.md](audit/ambiguous_course_resolution_strategy.md) | Design of the two-stage (deterministic + LLM) ambiguous title resolution approach |

#### Degree-enrichment artifact layer design

These docs define how extracted guide data will be published to Atlas degree pages. The artifact generator itself has not been built yet.

| File | Role |
|------|------|
| [phase_d_publish_policy.md](audit/phase_d_publish_policy.md) | What guide data gets published to degree pages; what stays internal |
| [phase_d_artifact_schema.md](audit/phase_d_artifact_schema.md) | Schema for the Atlas degree-page artifact files |
| [phase_d_degree_course_ownership_matrix.md](audit/phase_d_degree_course_ownership_matrix.md) | Degree/course ownership mapping for publish decisions |
| [phase_d_build_plan.md](audit/phase_d_build_plan.md) | Implementation plan for `build_guide_artifacts.py` |

#### Historical / background

Everything else in `audit/` is background planning, intermediate assessments, and inventory docs produced during the workstream. They are useful for understanding decisions but not required for ongoing work.

---

## Scripts that matter

All scripts live under `scripts/program_guides/`.

| Script | Purpose | When to run |
|--------|---------|-------------|
| `parse_guide.py` | Parse a guide PDF text file into structured JSON | Only if parser fix needed |
| `build_roster_bridge.py` | Build original bridge from parsed + canonical courses | Only if bridge needs rebuild |
| `resolve_ambiguous_deterministic.py` | Apply deterministic signals to ambiguous rows | Only if bridge rebuilt |
| `build_ambiguous_resolution_packets.py` | Build LLM context packets for residual ambiguous rows | Only if resolver re-run |
| `write_adjudication_results.py` | Write LLM adjudication results to JSON | Only if adjudication redone |
| `merge_resolved_ambiguous.py` | Merge all resolutions into `guides_merged/` | Run after any resolution update |
| `build_course_enrichment_candidates.py` | Extract enrichment from merged bridge | Run after merge to update enrichment |

**Normal update path:** if new guides are added, re-run the full pipeline from `parse_guide.py` → `build_roster_bridge.py` → deterministic → LLM → merge → enrichment.

---

## What is canonical vs intermediate vs historical

| Category | Examples | Notes |
|----------|----------|-------|
| **Canonical — do not modify** | `parsed/`, `validation/`, `manifest_rows/` | Source of truth for guide content |
| **Canonical — current state** | `bridge/guides_merged/`, `enrichment/`, `bridge/merge_summary.json` | Final course-matching and enrichment state |
| **Canonical — decisions** | `audit/PROGRAM_GUIDE_CORPUS_MANIFEST.*`, `audit/program_guide_claims_register.*`, `audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` | What was decided and why |
| **Intermediate — pipeline stages** | `bridge/guides/`, `bridge/guides_resolved/`, `bridge/resolution_log_deterministic.json`, `bridge/llm_packets/` | Preserved for auditability; not the final state |
| **Historical / background** | Most other `audit/` files | Useful reference; not required for ongoing work |
| **Family validation** | `family_validation/` | Historical rollout record |

---

## Partial-use and excluded guides

| Guide | Issue | Downstream handling |
|-------|-------|---------------------|
| BSITM | SP unusable (PDF column extraction failure) | AoS content only |
| MATSPED | SP broken (all courses concatenated in one title) | AoS content only |
| MSCSUG | SP unusable (PDF column extraction failure) | AoS content only |
| BSPRN | SP covers Pre-Nursing track only (15 Nursing-track courses AoS-only) | SP labeled Pre-Nursing-only if shown |
| BSNU | No footer (version/pub_date/page_count missing) | Content intact; metadata gap acknowledged |

---

## What is next

**Build the Atlas degree-enrichment artifact generator** (`build_guide_artifacts.py`):
- reads the extracted guide data (`parsed/`, `validation/`, `manifest_rows/`) plus the approved policy and schema
- applies per-guide inclusion/exclusion policy
- emits Atlas-ready draft artifacts under `public/data/program_guides/`
- no site wiring yet — this step produces files for verification, not live pages

Start from [audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md](audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md).

**Later decisions:**
- How and when course-level enrichment surfaces on Atlas course pages
- Whether college-level enrichment can be derived from the same guide data
