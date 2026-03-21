# Program Guides — Data Directory

**Human entry point for the WGU program-guide extraction workstream.**

---

## What this directory is

This directory contains all artifacts from extracting structured data out of WGU Program Guidebook PDFs — 115 guides covering every active program. The extracted data includes course descriptions, competency bullets, Standard Path schedules, and course-to-program mappings.

This is a **data preparation and internal enrichment** directory. Nothing here is directly served to the site yet. The next step (Phase D) is to build the site artifact generator that publishes approved content to `public/data/program_guides/`.

---

## Phase status

| Phase | Description | Status |
|-------|-------------|--------|
| A | Corpus manifest | Complete |
| B | Thin-slice validation | Complete |
| C | Full corpus parsing (115/115) | **Complete** |
| D | Site artifact build (degree-page payloads) | Not started |
| E — Roster bridge | 115/115 guides bridged to canonical courses | **Complete** |
| E — Deterministic resolution | 1,428/1,599 ambiguous rows resolved deterministically | **Complete** |
| E — LLM adjudication | 163 high + 2 medium of 171 residuals adjudicated | **Complete** |
| E — Merge | All resolutions merged into bridge; enrichment rerun | **Complete** |

**Scraping/extraction phase is closed.** The guide corpus is fully parsed, validated, bridged, and enriched.

---

## Current state — numbers that matter

### Corpus

- 115/115 guides parsed, validated, and manifest-rowed
- 111 guides: full-use | 4 guides: partial-use | 0 excluded
- Confidence: 96 HIGH / 17 MEDIUM / 2 LOW
- 2,593 AoS course descriptions (100% coverage)
- 2,591 competency sets
- 2,568 Standard Path rows

### Course enrichment (post-merge)

- **751 courses** have enrichment data (descriptions + competencies + program context)
- 730 courses with descriptions, 729 with competencies
- 723 courses with SP context, 730 with AoS context
- 542 rows still unmapped (titles not in canonical course database — irreducible)
- 6 rows unresolvable (both candidates inactive, no decisive signal)

### Resolution breakdown (1,599 originally ambiguous rows)

| Tier | Count | Status |
|------|-------|--------|
| Exact/unique from bridge | ~2,952 | Never ambiguous |
| Deterministic (multi-signal) | 1,428 | Resolved |
| LLM adjudication — high | 163 | Auto-accepted |
| LLM adjudication — medium | 2 | Human-reviewed, accepted |
| Unresolvable | 6 | Excluded (inactive candidates) |
| Unmapped | 542 | Not findable in canonical DB |

---

## Where to start reading

**If you want to understand the corpus:** [audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md](audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md)

**If you want to build Phase D:** [audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md](audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md)

**If you want the current enrichment numbers:** [enrichment/course_enrichment_summary.json](enrichment/course_enrichment_summary.json)

**If you want to understand what claims are safe to make:** [audit/program_guide_claims_register.md](audit/program_guide_claims_register.md)

**If you want the post-merge bridge state:** [bridge/merge_summary.json](bridge/merge_summary.json)

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

**Role:** Input to corpus manifest. Used by Phase D build script for inclusion/exclusion policy.

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

**What:** The main downstream deliverable of Phase E. For each course that could be unambiguously linked to a guide row, this contains all the guide-derived enrichment: descriptions, competency sets, program context, AoS group context.

**Key files:**

| File | Role |
|------|------|
| `course_enrichment_candidates.json` | Full enrichment data — 751 courses |
| `course_enrichment_summary.json` | Coverage counts and anchor class distribution |

**Status:** Current. Generated by `build_course_enrichment_candidates.py` against `bridge/guides_merged/`.

**Coverage:** 751 courses, 730 with descriptions, 729 with competencies.

**Role:** Input to Phase D (degree pages) and eventually Phase E (course pages).

---

### `audit/` — planning, policy, schema, and reference docs (52 files)

The audit directory contains the policy decisions, schemas, assessments, and planning artifacts produced during the workstream. It is the authoritative reference for **why things are the way they are**.

#### Read these first (most important)

| File | Role |
|------|------|
| [PROGRAM_GUIDE_CORPUS_MANIFEST.md](audit/PROGRAM_GUIDE_CORPUS_MANIFEST.md) | Canonical corpus facts — 115 guides, counts, coverage, confidence |
| [program_guide_claims_register.md](audit/program_guide_claims_register.md) | Approved vs disallowed claims about the corpus |
| [program_guide_adversarial_review.md](audit/program_guide_adversarial_review.md) | Claim stress test — what wording is safe |
| [PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md](audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md) | Phase D build guide — single entry point for site artifact generation |

#### Bridge and enrichment design

| File | Role |
|------|------|
| [program_guide_roster_bridge_assessment.md](audit/program_guide_roster_bridge_assessment.md) | Bridge methodology, coverage model, anchor class definitions |
| [program_guide_roster_bridge_schema.md](audit/program_guide_roster_bridge_schema.md) | Bridge artifact schema |
| [course_anchorability_matrix.md](audit/course_anchorability_matrix.md) | Which courses can be anchored and at what confidence |
| [course_signal_quality_review.md](audit/course_signal_quality_review.md) | Quality of each resolution signal |
| [course_enrichment_candidate_schema.md](audit/course_enrichment_candidate_schema.md) | Schema for enrichment candidate artifacts |
| [ambiguous_course_resolution_strategy.md](audit/ambiguous_course_resolution_strategy.md) | Hybrid deterministic + LLM resolution design |

#### Phase D planning pack

| File | Role |
|------|------|
| [phase_d_publish_policy.md](audit/phase_d_publish_policy.md) | What gets published, what stays internal |
| [phase_d_artifact_schema.md](audit/phase_d_artifact_schema.md) | Schema for Phase D site artifacts |
| [phase_d_degree_course_ownership_matrix.md](audit/phase_d_degree_course_ownership_matrix.md) | Degree/course ownership for publish decisions |
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
| **Canonical — current state** | `bridge/guides_merged/`, `enrichment/`, `bridge/merge_summary.json` | Post-merge final state |
| **Canonical — audit/policy** | `audit/PROGRAM_GUIDE_CORPUS_MANIFEST.*`, `audit/program_guide_claims_register.*`, `audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` | Decision record |
| **Intermediate pipeline stages** | `bridge/guides/`, `bridge/guides_resolved/`, `bridge/resolution_log_deterministic.json`, `bridge/llm_packets/` | Preserved for auditability; not the final state |
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

**Phase D** — build the site artifact generator (`build_guide_artifacts.py`) that:
- reads `parsed/`, `validation/`, `manifest_rows/` + Phase D policy/schema JSON
- applies include/exclude policy per guide
- emits schema-valid draft index and per-guide artifacts under `public/data/program_guides/`
- no runtime wiring yet

Start from [audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md](audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md).

Course-page enrichment shipping (Phase E continuation) requires Phase D to be complete first.
