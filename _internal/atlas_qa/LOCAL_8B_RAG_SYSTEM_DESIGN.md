# Local 8B QA System Design (Revised v1.3)

## Document status
- Updated to reflect repo ownership decision: `wgu-atlas` is the single implementation home for all Atlas QA runtime, artifacts, evals, and tests.
- `wgu-reddit` is a temporary upstream source only; cross-repo dependence will be reduced deliberately, in stages.
- Scope: bounded, citation-based QA over WGU catalog + program-guide corpus.
- Runtime: local Ollama model (~7B–8B), no fine-tuning in v1.

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

### 2.2 Existing local LLM orchestration knowns (already in `src`)
We already have working local-model patterns that match this project’s control philosophy:
- Ollama provider is registered and used via provider dispatch.
- Structured output parsing + validation is already implemented (JSON extraction + fallback + Pydantic schema validation).
- Parse/schema/fallback/LLM-failure flags are already tracked per call.
- End-to-end run artifacts already capture prompt, raw output, and error flags for auditability.

Implication: Atlas LLM does **not** need to invent local structured-output orchestration from scratch; it should reuse this pattern.

### 2.3 Decision knowns
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

## 5) Revised v1.3 pipeline
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
When source families disagree:
1. Catalog structured artifacts are authoritative for catalog-encoded fields (program composition, CU totals, edition roster facts).
2. Guide structured artifacts are authoritative for guide-only fields (standard path wording/rows, AoS wording, capstone wording).
3. Same-field conflict in same version: surface conflict explicitly; cite both; do not force-merge.

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
- provider abstraction is preserved (Ollama-first locally; OpenAI-compatible path remains available).
- model family remains swappable; Atlas QA must not hard-code to a single provider family.

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

#### Stage 0 — Atlas ownership boundary

**Purpose:** Declare ownership. Produce a written boundary contract.

**Outputs:**
- Statement that Atlas QA runtime, tests/evals, and generated artifacts live entirely in `wgu-atlas`.
- All remaining `wgu-reddit` dependencies are transitional and explicitly enumerated.

**Verification:**
- Dependency inventory listing every current Atlas dependency on `wgu-reddit`.
- Each dependency classified as: `keep temporarily` / `mirror into Atlas` / `replace in Atlas` / `delete`.
- No dependency remains uncategorized.

**Definition of done:** Single explicit ownership contract + dependency inventory for migration planning.

---

#### Stage 1 — Dependency inventory and target map

**Purpose:** Identify exactly what Atlas QA needs from `wgu-reddit` and define where each dependency will live in Atlas.

**Output table format:**

| Dependency | Current source | Used for | Atlas target | Strategy |
|---|---|---|---|---|
| parser output artifact X | wgu-reddit/... | build input | wgu-atlas/data/... | mirror |
| structured LLM utility Y | wgu-reddit/src/... | Ollama schema call | wgu-atlas/src/... | port |
| raw PDFs | wgu-reddit/... | extraction only | none for runtime | exclude |

**Deterministic rules:** Every dependency gets exactly one strategy: `mirror` / `port` / `replace` / `exclude`.

**Definition of done:** Codex can migrate foundations without guessing.

---

#### Stage 2 — Atlas-local foundation import/port

**Purpose:** Make Atlas self-sufficient enough to begin QA work without cross-repo runtime imports.

**Scope:**
- Port minimal structured-output utilities into Atlas (provider abstraction, JSON extraction + fallback, Pydantic schema validation, parse/schema/fallback/failure flags, run-level observability).
- Stage 2 entry requirement: Atlas-local structured-output substrate must be runnable in-repo with validation/fallback behavior preserved before broader QA build work.
- Mirror required build inputs/artifacts into Atlas-local locations.
- Create Atlas QA module skeleton.

**Stable interface contracts to define:**
- structured model call result
- validated classifier output
- evidence reference type
- version/entity identifiers

**Hard rule:** Atlas QA code imports Atlas modules only. No new code path imports runtime helpers from `wgu-reddit`.

**Verification:** Import smoke tests pass; grep/import check shows no forbidden upstream imports in QA package.

**Definition of done:** Atlas has its own minimal reusable QA foundation.

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

The staged plan in §15.2 defines the sequence. The immediate priorities map to Stages 0 and 1:

1. **Stage 0** — Produce the Atlas ownership boundary contract. Enumerate every current Atlas dependency on `wgu-reddit`. Classify each dependency (keep temporarily / mirror / port / replace / delete). No ambiguous dependency left uncategorized.
2. **Stage 1** — Produce the dependency inventory and target map table. Every dependency gets an Atlas target path and a single migration strategy. This is the Codex-ready input for Stage 2.
3. **Stage 2** — Port minimal structured-output utilities into Atlas-local modules. Mirror required artifacts. Stand up the Atlas QA package skeleton. Verify no forbidden upstream imports remain.
4. **Stage 3** — Build canonical object generators (`course_card`, `program_version_card`, `guide_section_card`, `version_diff_card`) entirely in Atlas.
5. **Stage 4** — Implement deterministic pre-router, strict query-class execution matrix, and hard version/entity/source/section partitioning.
6. **Stage 5+** — Add sufficiency/completeness gates, fuzzy retrieval path, evaluation harness, and compare mode.

## 18) Summary
v1.3 is a deterministic QA system with a constrained local LLM component, with `wgu-atlas` as the single implementation home. The architecture prevents the highest-risk error class (plausible mixed-version answers with valid-looking citations) and eliminates cross-repo runtime dependence through a deliberate staged migration. Stage 0 and Stage 1 artifacts are complete; see [STAGE_0_OWNERSHIP_CONTRACT.md](STAGE_0_OWNERSHIP_CONTRACT.md) and [STAGE_1_DEPENDENCY_INVENTORY.md](STAGE_1_DEPENDENCY_INVENTORY.md).
