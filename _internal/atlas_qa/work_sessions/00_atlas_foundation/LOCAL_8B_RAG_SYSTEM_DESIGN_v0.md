# Local 8B QA System Design (Revised v1.4)

## Document status
- **Updated 2026-03-23** to reflect completed Atlas-local baseline (Stages 0–2 done).
- `wgu-atlas` is the single implementation home for all Atlas QA runtime, artifacts, evals, and tests. Ownership boundary is now enforced, not only declared.
- `wgu-reddit` is a temporary upstream source only; all Stage 0–2 dependencies have been resolved. No runtime dependency on `wgu-reddit` remains in Atlas QA code.
- Scope: bounded, citation-based QA over WGU catalog + program-guide corpus.
- Runtime: local Ollama model (~7B–8B), no fine-tuning in v1.
- Current stage: Stage 3 (canonical object generation) is the active next step.

## 1) Executive summary
The architecture is now explicitly **deterministic-first**:
- deterministic routing and entity/version resolution
- deterministic lookup for exact/simple questions
- retrieval over canonical synthetic objects for NL questions
- small model used for constrained parsing and optional answer phrasing

Primary risk remains: **plausible, citation-bearing, wrong-version synthesis**.  
Primary control remains: **hard version/entity retrieval partitioning before generation**.

## 2) New knowns (validated)
These are now treated as confirmed implementation inputs.

### 2.1 Corpus knowns
- Catalog editions: `108`
- Program guides: `115`
- Canonical course index: `1594` course codes
- Guide-enriched courses: `751`
- Structured assets available:
  - catalog program blocks with line spans and version fields
  - parsed guide sections (`standard_path`, `areas_of_study`, `capstone`)
  - guide→catalog linking artifacts
  - anomalies/reconciliation outputs

### 2.2 Atlas-local LLM substrate (verified 2026-03-23)
The minimum viable structured-output substrate is now ported, audited, and live-verified in Atlas:

**Atlas-local modules (`src/atlas_qa/llm/` and `src/atlas_qa/utils/`):**
- `client.py` — provider dispatch; `generate(model_name, prompt) -> LlmCallResult`
- `registry.py` — model registry; `get_model_info(name)` with Ollama/OpenAI support
- `types.py` — `LlmCallResult` with all required flags: `raw_text`, `llm_failure`, `parse_failure`, `schema_failure`, `num_retries`, `error_message`, `elapsed_sec`
- `structured.py` — `safe_parse_structured_response()` (JSON extraction + Pydantic validation + fallback), `validate_and_fallback()`
- `artifacts.py` — `ArtifactCapture`; writes `{prompt, raw_output, flags}` per call to JSONL
- `utils/logging.py` — stdlib logging wrapper

**Verification status:**
- Structured parse (valid JSON, parse failure, schema failure), fallback, and artifact capture: all verified.
- Real Ollama call (`llama3:latest`, 8B Q4) end-to-end: **live-verified** — `generate()` → HTTP → `safe_parse_structured_response()` → Pydantic validation → JSONL artifact on disk. `elapsed_sec` ~13s, no failures.
- OpenAI path: clean failure when `OPENAI_API_KEY` absent; live call pending key. Note: retry loop retries on permanent key-missing failure (pre-existing behavior; not fixed in Stage 2).
- No Atlas QA source file imports from `wgu-reddit`. Import boundary confirmed.

Implication: Stage 3+ QA build work can import from `src.atlas_qa.*` directly. No substrate work needed before canonical object construction begins.

### 2.3 Atlas-local artifact inventory (as of 2026-03-23)

All Stage 1 artifact families are now present in Atlas. No QA runtime path needs to read from `wgu-reddit`.

**Catalog artifacts (mirrored to `data/catalog/`):**
- `trusted/2026_03/` — 8 files, ~1 MB; current edition program blocks, program/course indexes, manifest, degree snapshots, sections index, certs. Committed to git.
- `change_tracking/` — 5 files, ~644 KB; adjacent diffs, course/program history, summary stats. Committed.
- `edition_diffs/` — 4 files, ~244 KB; edition diff events, full diffs, rollups, summary. Committed.
- `helpers/course_index_v10.json` — 58 MB; **gitignored**. Acquire from `wgu-reddit/WGU_catalog/outputs/helpers/` after a fresh clone. See `data/catalog/README.md`.
- `helpers/degree_snapshots_v10_seed.json` — 524 KB; **gitignored**.
- `helpers/sections_index_v10.json` — 824 KB; **gitignored**.

**Program guide artifacts (pre-existing in Atlas):**
- `data/program_guides/parsed/` — 115 parsed guide JSON files
- `data/program_guides/guide_manifest.json`, `guide_anomaly_registry.json`, `section_presence_matrix.csv`

**Canonical course data (pre-existing in Atlas):**
- `data/canonical_courses.csv` and `data/canonical_courses.json` — 1594 course codes

Stage 3+ build work can assume all of the above are present locally.

---

### 2.4 Source-authority knowns (settled 2026-03-23)

The full block-authority and display policy is in `BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md`. The entries below are the QA-design-relevant decisions only.

**Course description:**
- Default answer source: `CAT-TEXT` (WGU Catalog 2026-03).
- Guide descriptions are stored as alternates keyed by source program code(s). Not displayed by default; available for program-context queries.
- 74 courses have 2–4 guide description variants. 185 courses have 2–6 competency variants.
- Confirmed safe across all 571 overlapping courses after full annotation pass: no row produced a clear guide preference over catalog for default display.

**Guide-only blocks (no catalog overlap, no authority question):**
- Competency bullets: GUIDE sole source.
- Cert prep signal: GUIDE sole source.
- Areas of Study: GUIDE sole source.
- Capstone (both program and course level): GUIDE sole source, always scoped to the program.

**Identity facts:**
- CU, course title, course code, canonical status: CANON authoritative. Guide CU values are not authoritative (41 courses have guide-internal CU conflicts across programs).
- Program identity (degree title, program code): CAT.
- Program total CU: CAT. Guide SP sums are not authoritative (7 programs have >1 CU discrepancy vs catalog total).

**Program learning outcomes:** CAT-TEXT sole source. Guides do not contain PLOs.

**Version conflicts requiring QA disclosure:**
- MACCA, MACCF, MACCM, MACCT: catalog 3 months newer than guide. Use CAT-TEXT; cite both version tokens.
- MSHRM: guide 8 months newer than catalog (body text currently identical after prefix strip, but freshness gap is the widest in corpus). Cite both version tokens. Do not assert catalog is current.

**Hard anomaly flags (must be in canonical objects before Stage 3 construction):**
- C179: catalog text is 293 chars — unusually short; completeness unconfirmed. Guide adds routing/switching/automation specifics. Inspect catalog extract before relying on catalog-default for this course.
- D554: guide description contains text from D560 (Internal Auditing I) — data anomaly in extraction pipeline. Do not use guide description for D554. Catalog text is unaffected.

---

### 2.5 Decision knowns
- v1 will not be agentic.
- v1 will not use model-based routing as primary controller.
- v1 will default to single-version retrieval unless explicit compare intent.
- exact IDs never begin with semantic retrieval.
- default version resolution is the most recent available version for the resolved entity (not "latest catalog" as a primary lookup object).

## 3) System objective and boundaries
### Objective
Answer student-style factual questions about programs/courses with:
- explicit evidence citations
- explicit version disclosure
- abstention when unsupported

### Non-objectives (v1)
- personal advising/recommendation
- broad multi-entity narrative synthesis
- free-form model-driven cross-version interpretation
- fine-tuning for factual correctness

## 4) Architecture invariants (hard rules)
1. Exact identifiers (`course_code`, `program_code`) never start in semantic retrieval.
2. Default retrieval is single-version only.
3. Mixed-version context is forbidden unless query intent is explicit comparison.
4. No answer without an evidence bundle.
5. No negative claim without completeness logic.
6. No comparison narrative unless diff is deterministic/precomputed.
7. LLM classifier output is untrusted input and must be schema-validated.

## 5) Revised v1.4 pipeline
1. Deterministic pre-router (regex/rules for obvious code/version/compare cues).
2. Structured LLM classifier for remaining fuzzy queries (JSON schema only).
3. Deterministic entity + version resolution.
4. Hard retrieval partitioning by entity/version/source/section.
5. Deterministic fetch for exact/simple classes.
6. Hybrid retrieval over canonical synthetic objects for NL classes.
7. Small evidence-bundle construction.
8. Pre-generation sufficiency/answerability check.
9. Constrained generation only when needed.
10. Post-check: citation presence + version disclosure + schema compliance.

## 6) Query classes and execution paths
### Class A: exact identifier lookup
Examples: "What is D426?", "How many CUs for BSACC?"
- Path: deterministic lookup only.
- Model use: optional formatting only.

### Class B: single-entity factual lookup
Examples: "What is the capstone for BSDA?"
- Path: deterministic entity resolution + section-constrained retrieval.
- Model use: bounded synthesis over one typed evidence bundle.

### Class C: section-grounded NL lookup
Examples: "What competencies are listed for ..."
- Path: hybrid retrieval over canonical section objects + strict metadata filters.
- Model use: constrained answer from small bundle.

### Class D: explicit version comparison
Examples: "What changed between 2025_06 and 2026_03?"
- Path: deterministic `version_diff_card` where available; otherwise strict two-version bundle.
- Model use: summarize deterministic diff only.

### Class E: unsupported/advising/opinion
Examples: "Which path is best for me?"
- Path: abstain or bounded scope response.

## 7) Canonical synthetic retrieval objects (first-class)
Deterministic renderers from parsed artifacts.

### 7.1 `course_card`
- `course_code`, `canonical_title`, `canonical_cus`
- `title_variants`, `instances_by_version`, `program_codes`
- `guide_enrichment_summary`, `evidence_refs`

### 7.2 `program_version_card`
- `program_code`, `degree_title`, `college`, `version`, `is_latest`, `total_cus`
- `course_list_summary`, `section_presence`, `guide_links`, `evidence_refs`

### 7.3 `guide_section_card`
- `program_code`, `version`, `section_type`
- normalized section text + structured rows/entries
- linked `course_codes`, `evidence_refs`

### 7.4 `version_diff_card`
- `entity_type`, `entity_id`, `from_version`, `to_version`
- deterministic `added/removed/changed`
- `evidence_refs`

## 8) Retrieval design
### 8.1 Retrieval stack
- deterministic lookup first
- hybrid retrieval second (BM25 + embeddings + fusion)
- rerank third

### 8.2 Hard partitioning
Before retrieval, derive/enforce:
- `version_scope`
- `entity_scope` (`program_code` / `course_code`)
- `section_scope`
- `source_scope`

Any chunk outside hard scope is discarded before context packing.

### 8.3 Version policy
- No version specified: most recent available version for the resolved entity + explicit disclosure.
- Version specified: only that version.
- Compare intent: only explicitly compared versions.
- Unresolved version ambiguity: abstain (or clarifying UX later).

## 9) Source precedence policy
General rules:
1. Catalog structured artifacts are authoritative for catalog-encoded fields (program composition, CU totals, edition roster facts).
2. Guide structured artifacts are authoritative for guide-only fields (standard path wording/rows, AoS wording, capstone wording).
3. Same-field conflict in same version: surface conflict explicitly; cite both; do not force-merge.

Settled per-block authority (from `BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md`, 2026-03-23):

| Block | Default QA source | Notes |
|---|---|---|
| Course description / overview | CAT-TEXT | Guide description stored as alternate. 633-pair comparison corpus completed; no pair produced a clear guide preference over catalog for default display. |
| Guide description variants | ENRICH (program-scoped) | Use when program context is supplied; fall back to CAT-TEXT otherwise. |
| Competency bullets | ENRICH — sole source | Most-common variant by default; disclose multi-variant when count > 1. |
| Cert prep signal | ENRICH — sole source | Show when present; abstain on absence without completeness confirmation. |
| Prerequisites | CANON | Structured prereq relationships only; CAT-TEXT prereq mentions are informal. |
| Reverse prerequisites | CANON-derived | Do not assert absence without completeness confirmation. |
| Capstone callout | ENRICH — sole source | Always scoped to the program; do not assert "capstone" without naming the program. |
| CU / title / course code | CANON (fallback CAT) | Guide CU is not authoritative (41 courses with guide-internal CU conflicts). |
| Areas of Study | GUIDE — sole source | Program-scoped. |
| Capstone (program) | GUIDE — sole source | |
| Program description | CAT-TEXT | 63 of 65 STRONG mat-diff program pairs are explained by guide prepending a metadata header; body text is identical to catalog after stripping. Only MATSPED and BAESSPMM have genuine content differences; catalog is the display default for both. |
| Program identity (title, code) | CAT | |
| Total CU | CAT | Guide SP sums unreliable (7 programs with >1 CU discrepancy vs catalog total). |
| Program required courses (official policy) | CAT | Authoritative for accreditation-level requirements. Not machine-parseable from catalog PDF; abstain if structured data is unavailable. |
| Standard path sequencing / guide path presentation | GUIDE (standard_path) | Sole machine-parseable source. Qualify as "as listed in the program guide"; may reflect one path through an elective structure. |
| Program learning outcomes | CAT-TEXT — sole source | Guides do not contain PLOs. |
| Licensure notes | CAT-TEXT | Guide licensure mentions are supplemental context, not policy. |
| Certification notes (program) | GUIDE | Cite guide program + version. |
| Edition / version info | Per-source token | Never merge version tokens across source families. |

## 10) Negative claim completeness policy
For negative claims (absence assertions), require all:
1. High-confidence entity/version resolution.
2. Required sections present and complete for that entity/version.
3. Retrieval coverage threshold met for required sections.
4. No anomalies that invalidate completeness for the queried field.

Else output: insufficient evidence / cannot confirm absence.

## 11) LLM role and control-plane policy
The local model is **not** the control plane.

LLM allowed roles:
- structured intent/entity extraction for fuzzy queries
- bounded surface realization from vetted evidence

Provider/model policy:
- Provider abstraction is preserved (Ollama-first locally; OpenAI-compatible path remains available).
- Model family remains swappable; Atlas QA must not hard-code to a single provider family.
- **Current verified state:** Ollama path live-verified with `llama3:latest` (8B Q4). OpenAI path confirmed clean failure when key is absent; live call pending `OPENAI_API_KEY`. Only `llama3` is registered in `registry.py`; additional models can be added when needed.
- Available Ollama models on this machine (not yet registered): `llama3.1:latest`, `qwen3.5:9b`, `mistral:7b-instruct`, `qwen2.5-coder:7b`, `codestral:latest`.

LLM disallowed roles:
- autonomous source selection
- version arbitration
- conflict resolution without deterministic policy
- deciding absence claims without completeness gate

## 12) Context construction for 8B models
- Evidence bundle size targets:
  - single-entity: 2–5 typed artifacts
  - explicit compare: 4–8 typed artifacts
- Prefer canonical objects over raw spans.
- Raw spans are secondary support only.

Prompt contract:
1. Use only provided evidence.
2. State version used.
3. Cite evidence IDs for each factual claim.
4. Do not merge versions unless compare mode is explicit.
5. If evidence insufficient, abstain.

## 13) Answerability and abstention
Hybrid deterministic-first gate:
1. rule gates (missing entity/version/class out-of-scope)
2. retrieval sufficiency gates (score + coverage + section match)
3. completeness gate for negative claims
4. generation only if gates pass

Abstention states:
- `not_in_corpus`
- `insufficient_evidence`
- `ambiguous_entity`
- `ambiguous_version`
- `out_of_scope`

## 14) Evaluation and launch gates
Evaluate layers independently:
1. routing/entity/version resolution
2. retrieval quality
3. grounded answer quality
4. abstention correctness
5. version correctness

### 14.1 Required failure-mode tests
- wrong-version contamination
- citation-bearing but unsupported claims
- section leakage
- entity collision (tracks/specializations)
- false positive/false negative abstentions

### 14.2 Minimum v1 launch gates
- exact code/program resolution: near-deterministic reliability
- version-specific contamination: near-zero tolerance
- citation coverage on non-abstained answers: mandatory
- claim-level support audit: high pass threshold
- abstention precision/recall: validated on dedicated set

## 15) Repo ownership and staged migration plan

### 15.0 Ownership boundary contract

`wgu-atlas` is the single authoritative home for:
- Atlas QA runtime
- Atlas QA tests and evals
- Atlas QA generated artifacts
- any Atlas-specific preparation steps

`wgu-reddit` is a **temporary upstream source** only. Any remaining dependency on it is transitional and must be explicitly enumerated. No dependency remains uncategorized.

**Hard rules in effect from this point forward:**
- No new QA runtime code in `wgu-reddit`.
- No Atlas QA tests in `wgu-reddit`.
- No hidden runtime dependency on upstream parser internals.
- All production answer paths resolve from Atlas-local artifacts.

**What may remain external temporarily:**
- Raw PDF corpus
- Extraction intermediates
- Legacy parser code
- One-time migration scripts used only to bootstrap Atlas-local artifacts

These are treated as **build-time import sources**, not long-term runtime dependencies.

---

### 15.1 Four Atlas-local layers (architecture under this ownership model)

The architecture from §5 maps to four Atlas-local layers:

1. **Artifact layer** — normalized QA-ready artifacts stored in Atlas
2. **Deterministic control layer** — routing, entity/version resolution, retrieval scoping, abstention gates
3. **Constrained model layer** — structured classification and bounded answer phrasing
4. **Evaluation layer** — Atlas-local fixtures, gates, contamination tests, abstention tests

The control philosophy is unchanged. The only change is repo ownership.

---

### 15.2 Staged migration plan

#### Stage 0 — Atlas ownership boundary ✅ COMPLETE

**Purpose:** Declare ownership. Produce a written boundary contract.

**Completed 2026-03-23.** Outputs:
- `STAGE_0_OWNERSHIP_CONTRACT.md` — ownership declaration, hard rules, transitional externals enumerated, current boundary observed.
- 23 dependencies classified; 0 uncategorized.

See [STAGE_0_OWNERSHIP_CONTRACT.md](STAGE_0_OWNERSHIP_CONTRACT.md).

---

#### Stage 1 — Dependency inventory and target map ✅ COMPLETE

**Purpose:** Identify exactly what Atlas QA needs from `wgu-reddit` and define where each dependency will live in Atlas.

**Completed 2026-03-23.** 23 dependencies classified; every dependency has exactly one strategy (mirror / port / keep / exclude); no guessing required.

See [STAGE_1_DEPENDENCY_INVENTORY.md](STAGE_1_DEPENDENCY_INVENTORY.md).

---

#### Stage 2 — Atlas-local foundation import/port ✅ COMPLETE

**Purpose:** Make Atlas self-sufficient enough to begin QA work without cross-repo runtime imports.

**Completed 2026-03-23.** What was done:
- Minimum viable LLM substrate ported, audited, and verified in `src/atlas_qa/llm/` and `src/atlas_qa/utils/`. See §2.2 for module inventory and verification status.
- All 6 catalog artifact families mirrored to `data/catalog/`. See §2.3 for inventory and large-file policy.
- Import boundary confirmed: no Atlas QA module imports from `wgu-reddit`.
- Real Ollama success path live-verified end-to-end.

**Open items (not blocking Stage 3):**
- Evidence reference ID format: explicitly TBD/RFI. Evidence-backed answers are a v1 hard requirement (Architecture invariant §4.4); the internal schema for evidence reference IDs is not yet frozen. Not blocking Stage 3 canonical object construction — objects can be built with a placeholder `evidence_refs` shape that is finalized before Stage 4.
- OpenAI live call: pending `OPENAI_API_KEY`. Clean failure confirmed when key absent.
- Version token conflict precedence (provenance vs manifest fields): open for Stage 3 canonical object construction details only. This does not reopen the settled high-level source-authority policy (§9); it concerns how to resolve conflicting version tokens within a single artifact during object generation.
- The three v10 helper files are gitignored; must be re-acquired from upstream after a fresh clone (see `data/catalog/README.md`).

See [INITIAL_ATLAS_QA_FOUNDATION_STATE.md](INITIAL_ATLAS_QA_FOUNDATION_STATE.md) for full detail.

---

#### Stage 3 — Canonical object generation in Atlas

**Purpose:** Build deterministic QA-ready synthetic objects entirely in Atlas (no model use).

**Objects:** `course_card`, `program_version_card`, `guide_section_card`

**Verification:** Schema validation, golden fixtures for representative entities, uniqueness checks, version-isolation checks, evidence-ref integrity checks.

**Definition of done:** Atlas can answer exact/simple questions from canonical objects without semantic retrieval.

---

#### Stage 4 — Deterministic exact/simple QA path

**Purpose:** Ship the highest-confidence answer path first.

**Scope:** exact identifier routing, deterministic entity/version resolution, simple factual fetch, abstention states, citation-formatted responses.

**Verification:** exact course/program code lookup tests, latest-version default tests, explicit-version enforcement tests, unsupported-query abstention tests.

**Definition of done:** A bounded, production-credible subset of QA works with near-deterministic reliability.

---

#### Stage 5 — Hard-scoped fuzzy retrieval

**Purpose:** Add natural-language lookup without sacrificing version/entity correctness.

**Scope:** pre-router, structured classifier, hard partitioning, retrieval over canonical objects, sufficiency gate.

**Hard rules:** classifier output is untrusted until validated; hard scopes enforced before retrieval; out-of-scope objects discarded before packing; generation blocked if sufficiency gate fails.

**Verification:** wrong-version contamination tests, section leakage tests, entity collision tests, abstention precision tests, retrieval scope enforcement tests.

**Definition of done:** Atlas supports bounded NL QA while preserving hard control guarantees.

---

#### Stage 6 — Compare mode and hardening

**Purpose:** Add explicit version comparison and launch gates.

**Scope:** deterministic `version_diff_card`, compare query path, Atlas-local eval harness, launch metrics.

**Hard rules:** compare only explicit versions; diff derived deterministically where possible; no freeform compare narrative without deterministic support.

**Verification:** compare contamination tests, diff accuracy tests, citation support audits, negative-claim completeness tests, abstention correctness tests.

**Definition of done:** Atlas QA reaches a v1 launchable standard.

## 16) Deferred from v1
1. open-ended multi-program synthesis
2. model-based primary routing
3. agentic tool loop as default interaction mode
4. heavy reranker stack as mandatory baseline
5. fine-tuning for factual correctness

## 17) Immediate implementation priorities

Stages 0, 1, and 2 are complete. The current active stage is **Stage 3**.

1. ~~**Stage 0**~~ — ✅ Complete. Ownership boundary contract produced.
2. ~~**Stage 1**~~ — ✅ Complete. Dependency inventory produced; 23 dependencies classified.
3. ~~**Stage 2**~~ — ✅ Complete. Substrate ported and live-verified; catalog artifacts mirrored; import boundary confirmed.
4. **Stage 3 (active)** — Build canonical object generators (`course_card`, `program_version_card`, `guide_section_card`, `version_diff_card`) entirely in Atlas. Inputs are now all Atlas-local. Source-authority fields from §2.4 and §9 must be reflected in `course_card` (see `POLICY_IMPLEMENTATION_PLAN.md` §5 for the field list).
5. **Stage 4** — Implement deterministic pre-router, exact identifier routing, entity/version resolution, and simple factual fetch. Abstention states must be wired before generation path is opened.
6. **Stage 5** — Add sufficiency/completeness gates, fuzzy retrieval path, structured classifier, and hard scope partitioning.
7. **Stage 6** — Compare mode, eval harness, and v1 launch gates.

## 18) Summary
v1.4 is a deterministic QA system with a constrained local LLM component, with `wgu-atlas` as the single implementation home. The architecture prevents the highest-risk error class (plausible mixed-version answers with valid-looking citations) and eliminates cross-repo runtime dependence through a deliberate staged migration.

**Current baseline (as of 2026-03-23):** Stages 0–2 are complete. Atlas has a verified local LLM substrate (`src/atlas_qa/`), all catalog and program-guide artifact families mirrored to `data/catalog/` and `data/program_guides/`, no runtime dependency on `wgu-reddit`, a real Ollama success path verified end-to-end, and a settled block-authority display policy grounding the canonical object design. Stage 3 (canonical object generation) is the active next step.

See [STAGE_0_OWNERSHIP_CONTRACT.md](STAGE_0_OWNERSHIP_CONTRACT.md), [STAGE_1_DEPENDENCY_INVENTORY.md](STAGE_1_DEPENDENCY_INVENTORY.md), [INITIAL_ATLAS_QA_FOUNDATION_STATE.md](INITIAL_ATLAS_QA_FOUNDATION_STATE.md), and [BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md](BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md).
