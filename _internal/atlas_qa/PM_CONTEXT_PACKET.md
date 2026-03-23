# PM Context Packet — Atlas Local 8B QA System
**Role:** Project manager for v1 implementation after design is locked.
**Date:** 2026-03-23
**Status:** Design is complete (Stages 0–2 done). Stage 3 is the active next step.

---

## What this system is

Citation-grounded factual QA over WGU program catalog + program guide corpus. Runs on a local ~8B model (Ollama, `llama3:latest` Q4). **Deterministic-first architecture**: most answers come from deterministic lookup; LLM is only used for fuzzy intent extraction and constrained answer phrasing. No fine-tuning in v1.

**Scope:** program/course lookup, section-grounded factual answers, explicit version comparisons.
**Out of scope v1:** personal advising, schedules, tuition, open-ended career guidance.

---

## What is done

### Stages 0–2 complete (do not re-litigate)

**Substrate** (`src/atlas_qa/llm/` + `src/atlas_qa/utils/`):
- `client.py` — `generate(model_name, prompt) -> LlmCallResult`
- `registry.py` — Ollama/OpenAI dispatch (only `llama3` registered; others available)
- `types.py` — `LlmCallResult` with `raw_text`, `llm_failure`, `parse_failure`, `schema_failure`, `num_retries`, `error_message`, `elapsed_sec`
- `structured.py` — `safe_parse_structured_response()`, `validate_and_fallback()`
- `artifacts.py` — per-call JSONL artifact capture
- `utils/logging.py` — stdlib logging wrapper

Ollama end-to-end call is live-verified. OpenAI path fails clean when key absent. No Atlas QA file imports from `wgu-reddit`. Import boundary confirmed.

**Corpus artifacts** (all mirrored to Atlas — no runtime dependency on upstream repo):
- `data/catalog/trusted/2026_03/` — 8 files, ~1MB (committed)
- `data/catalog/change_tracking/` — 5 files (committed)
- `data/catalog/edition_diffs/` — 4 files (committed)
- `data/catalog/helpers/course_index_v10.json` — 58MB, **gitignored** (acquire from `wgu-reddit`)
- `data/program_guides/parsed/` — 115 parsed guide JSONs
- `data/canonical_courses.csv` / `.json` — 1594 course codes

**Source-authority analysis** (design artifact, not yet implemented):
- 633-pair annotation pass complete across all catalog/guide description overlap zones
- Policy document: `_internal/atlas_qa/BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md` v1.0
- Implementation plan: `_internal/atlas_qa/POLICY_IMPLEMENTATION_PLAN.md`

---

## Corpus facts (key numbers)

| Fact | Value |
|---|---|
| Catalog editions | 108 |
| Program guides | 115 |
| Canonical course codes | 1594 |
| Guide-enriched courses | 751 |
| Guide-only blocks (competency, AoS, capstone, cert) | no catalog overlap — no authority question |
| Courses with multi-variant guide descriptions | 74 (2–4 variants keyed by source program) |
| Courses with multi-variant competency sets | 185 (2–6 variants) |
| Programs with catalog/guide version mismatch | 5: MACCA, MACCF, MACCM, MACCT (cat 3mo newer), MSHRM (guide 8mo newer) |
| Hard anomaly courses | C179 (catalog text 293 chars, suspiciously short), D554 (guide text is from D560 — data error) |

---

## Source authority table (locked — do not reopen)

| Block | Default QA source | Notes |
|---|---|---|
| Course description | CAT-TEXT | Guide stored as alternate, never default |
| Guide description variants | ENRICH (program-scoped) | Use when program context known; fall back to CAT-TEXT |
| Competency bullets | ENRICH — sole source | Most-common variant default; disclose if multi-variant |
| Cert prep signal | ENRICH — sole source | Abstain on absence without completeness check |
| Prerequisites | CANON | |
| CU / title / course code | CANON | Guide CU not authoritative (41 courses with guide-internal CU conflicts) |
| Areas of Study | GUIDE — sole source | Program-scoped |
| Capstone (course + program) | GUIDE — sole source | Always name the program |
| Program description | CAT-TEXT | Guide prefix artifact explains 63/65 diffs; body identical after strip |
| Total CU | CAT | Guide SP sums unreliable (7 programs with >1 CU discrepancy) |
| Program learning outcomes | CAT-TEXT — sole source | Guides contain no PLOs |
| Licensure notes | CAT-TEXT | |
| Certification notes (program) | GUIDE | |

**Hard anomaly rules (must be enforced in canonical objects):**
- C179: flag `cat_short_text`; disclose brief catalog text; offer guide alternate
- D554: flag `guide_misrouted_text`; block guide description entirely (set to `[]`); catalog only

**Version-conflicted programs:** MACCA, MACCF, MACCM, MACCT, MSHRM — cite both version tokens in any answer; do not silently blend.

---

## Architecture (locked)

**10-step pipeline:**
1. Deterministic pre-router (regex/rules for code/version/compare cues)
2. Structured LLM classifier for fuzzy queries (JSON schema only)
3. Deterministic entity + version resolution
4. Hard retrieval partitioning (entity/version/source/section)
5. Deterministic fetch for exact/simple queries
6. Hybrid retrieval (BM25 + embeddings + fusion) for NL queries
7. Evidence bundle construction (2–5 artifacts for single-entity; 4–8 for compare)
8. Pre-generation sufficiency/abstention gate
9. Constrained generation (if gates pass)
10. Post-check: citation presence + version disclosure + schema compliance

**Architecture invariants (hard rules):**
- Exact IDs never begin in semantic retrieval
- Default retrieval: single-version only
- Mixed-version context: forbidden unless explicit compare intent
- No answer without an evidence bundle
- No negative claim without completeness gate
- LLM is not the control plane; LLM is not permitted to select source or arbitrate versions

**Abstention states:** `not_in_corpus`, `insufficient_evidence`, `ambiguous_entity`, `ambiguous_version`, `out_of_scope`

---

## Canonical object types (4 — first-class)

| Type | Key fields |
|---|---|
| `course_card` | `course_code`, `canonical_title`, `canonical_cus`, `title_variants`, `instances_by_version`, `program_codes`, `guide_enrichment_summary`, `evidence_refs` + **source-authority fields** (see Stage 5 below) |
| `program_version_card` | `program_code`, `degree_title`, `college`, `version`, `is_latest`, `total_cus`, `course_list_summary`, `section_presence`, `guide_links`, `evidence_refs` |
| `guide_section_card` | `program_code`, `version`, `section_type`, normalized text + structured rows, `linked_course_codes`, `evidence_refs` |
| `version_diff_card` | `entity_type`, `entity_id`, `from_version`, `to_version`, deterministic `added/removed/changed`, `evidence_refs` |

---

## Query classes

| Class | Description | LLM use |
|---|---|---|
| A | Exact identifier lookup ("What is D426?") | Optional formatting only |
| B | Single-entity factual ("How many CUs for BSACC?") | Bounded synthesis over one evidence bundle |
| C | Section-grounded NL ("What competencies for...?") | Constrained answer from small bundle |
| D | Explicit version compare ("What changed between 2025_06 and 2026_03?") | Summarize deterministic diff only |
| E | Advising/opinion/out-of-scope | Abstain |

---

## Next: implementation stages (Stage 3 = current active)

Design is locked. The next work is execution. The build is structured as two parallel tracks:

### Track A — Policy implementation (authority artifact + course-page hardening)
From `POLICY_IMPLEMENTATION_PLAN.md`. Execute in order:

| Stage | Name | Script target | Output | Gate |
|---|---|---|---|---|
| **1** | Source-authority annotation artifact | `scripts/build_course_description_authority.py` | `data/atlas_qa/course_description_authority.json` | counts must match known values; no `display_source: "guide"` entries; D554 alternates empty |
| **2** | Artifact validation | `scripts/validate_course_description_authority.py` | Exit 0 | Blocks Stage 3 |
| **3** | Course-page display hardening | `src/app/courses/[code]/page.tsx` | Catalog-only confirmed in production path | Verify current state first — read before touching |
| **4** | Guide alternate storage | `scripts/build_course_guide_alternates.py` | `data/atlas_qa/course_guide_alternates.json` | Can run parallel to Stage 3 after Stage 1 |
| **5** | QA canonical object source-authority fields | `src/atlas_qa/qa/types.py` + `src/atlas_qa/qa/source_authority.py` | `course_card` extended with source-authority fields | Depends on Stage 1 |

**Key count expectations for Stage 1:**
- `total_courses` ≥ 838
- `both_present` = 571 (±2)
- `multi_variant_guide` = 74
- `anomaly_flagged` = 2 (C179, D554)
- `review_flagged` ~25

**Hard-coded review_flag courses (module-level constant in build script):**
- BSHR cluster: D358, D356, D354, D360
- MSHRM cluster: D432, D433, D435, D436
- BSPRN/nursing: D218, D348, C947 + others from Batch 2/3 annotation
- Other: C236, E011, D255, D118, D119, D124, C845

### Track B — QA pipeline build
From `LOCAL_8B_RAG_SYSTEM_DESIGN.md`. Work sessions planned:

| Session | Name | Focus |
|---|---|---|
| `01_canonical_objects` | Canonical object generation | Build `course_card`, `program_version_card`, `guide_section_card`, `version_diff_card` from existing corpus artifacts |
| `02_exact_lookup_path` | Exact lookup path | Class A deterministic lookup; entity/version resolution |
| `03_scope_partitioning` | Hard partitioning | Entity/version/source/section scope gates |
| `04_fuzzy_retrieval` | Hybrid retrieval | BM25 + embedding + fusion for NL queries |
| `05_compare_and_eval` | Compare mode + evaluation | Version diff, abstention testing, launch gates |

Session spec files are at `_internal/atlas_qa/work_sessions/0N_*/SESSION_SPEC.md`. Most are stubs — write specs before starting each session.

---

## Open design questions (from RFI — awaiting external feedback)

These are **not blockers for Track A (Stage 1–5)**. They may affect Track B canonical object design. Do not resolve them without owner input.

1. Multi-variant competency default: is "most-common variant by source program count" defensible, or is there a better heuristic?
2. Version-conflicted programs (MACCA/MACCF/MACCM/MACCT/MSHRM): UX for dual version tokens in answers
3. MSHRM specifically: proactive guide-version disclosure vs. query-triggered disclosure
4. Same-field substantive conflict not explained by known artifacts: surface both with labels, suppress weaker, or abstain?
5. §5.1–5.3 from RFI: canonical object minimum fields, retrieval partition edge cases, abstention thresholds — await external reviewer recommendations

---

## File locations

| Concern | Path |
|---|---|
| Design doc (v1.4) | `_internal/atlas_qa/LOCAL_8B_RAG_SYSTEM_DESIGN.md` |
| Source authority policy | `_internal/atlas_qa/BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md` |
| Implementation plan (Stages 1–5) | `_internal/atlas_qa/POLICY_IMPLEMENTATION_PLAN.md` |
| External RFI (v2) | `_internal/atlas_qa/LOCAL_8B_RFI.md` |
| LLM substrate | `src/atlas_qa/llm/` + `src/atlas_qa/utils/` |
| Catalog artifacts | `data/catalog/` |
| Guide artifacts | `data/program_guides/` |
| Canonical courses | `data/canonical_courses.{csv,json}` |
| Output artifacts (to build) | `data/atlas_qa/` |
| Build scripts (to write) | `scripts/build_*.py`, `scripts/validate_*.py` |
| Work session specs | `_internal/atlas_qa/work_sessions/0N_*/` |
| Course text comparison batches | `_internal/atlas_qa/course_text_comparison_batches/` |

---

## PM operating rules

- **Design is locked.** Do not reopen locked decisions. If an external reviewer suggests changes, flag to owner before acting.
- **Track A (Stages 1–5) can start immediately.** No unresolved blockers.
- **Stage 1 has no app code changes** — pure data artifact build. Low risk, start here.
- **Stage 3 requires reading the production page before touching it.** Do not assume current state.
- **LLM is never allowed to select source or resolve version conflicts.** Any code that allows this violates the architecture.
- **D554 guide alternates must be blocked at Stage 1.** This is a hard requirement, not optional.
- **C179 requires disclosure in QA answers, not suppression.** Catalog text is still served; the anomaly is flagged in the canonical object.
- **Commit and push after each completed stage.** Check git status before starting any stage.
