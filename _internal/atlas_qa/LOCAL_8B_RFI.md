# RFI (Updated v2): Local 8B Citation-Grounded QA for WGU Catalog + Program Guide Data

Status: Updated 2026-03-23 to reflect completed Atlas baseline (Stages 0–2 done)
Owner: WGU Atlas / data systems team
Prior version: 2026-03-23 (first external review round)

## 1) Purpose
We are requesting targeted feedback on remaining open decisions for a bounded, version-aware, citation-based QA system running on a local ~7B–8B model (Ollama).

This is a second-pass RFI. Core architecture direction is now set; we want critique on unresolved implementation choices and evaluation thresholds.

**What has changed since the last version:**
- Atlas-local LLM substrate is now implemented and live-verified (see §3.2).
- Source-authority and display policy for course and program descriptions is now settled (see §3.3). Questions in §5.4 that were open in the prior version are now resolved or narrowed.
- All catalog artifact families are mirrored into Atlas. No runtime dependency on upstream repo remains.
- §5.4 has been revised to reflect the settled decisions and identify the remaining genuine open questions.

## 2) Locked decisions (current plan)
The following are now treated as design commitments for v1:

1. Deterministic-first architecture
- deterministic routing and entity/version resolution
- deterministic lookup for exact/simple questions
- constrained generation only when needed

2. Canonical synthetic retrieval objects
- `course_card`
- `program_version_card`
- `guide_section_card`
- `version_diff_card` (deterministic where possible)

3. Hard version isolation
- single-version retrieval by default
- mixed-version context only in explicit compare mode

4. LLM role constraints
- allowed: structured intent/entity extraction (fuzzy queries), bounded phrasing
- disallowed: autonomous source selection, version arbitration, open synthesis

5. Abstention-first safety
- no answer without evidence bundle
- no negative claim without completeness checks

6. Source authority per block (newly locked — see §3.3 for detail)
- Course description default: CAT-TEXT (catalog). Guide descriptions are stored alternates, not default display.
- Guide-only enrichment blocks (competencies, cert signals, AoS, capstone): GUIDE sole source.
- Identity facts (CU, course code, title): CANON. Guide CU values are not authoritative.
- Program learning outcomes: CAT-TEXT sole source. Guides do not contain PLOs.
- LLM is not permitted to select source; source selection is deterministic and policy-driven.

## 3) New knowns (validated)
### 3.1 Corpus knowns
- Catalog editions: `108`
- Program guides: `115`
- Canonical course codes: `1594`
- Guide-enriched canonical courses: `751`
- Parser-derived units available:
  - catalog program blocks with line spans + versions
  - parsed guide sections (`standard_path`, `areas_of_study`, `capstone`)
  - guide→catalog linking
  - anomaly/reconciliation artifacts

### 3.2 Atlas-local LLM substrate (now live-verified)
The structured-output substrate is now ported, audited, and verified in Atlas at `src/atlas_qa/llm/` and `src/atlas_qa/utils/`:

- `client.py` — provider dispatch; `generate(model_name, prompt) -> LlmCallResult`
- `registry.py` — model registry with Ollama/OpenAI support
- `types.py` — `LlmCallResult` with `raw_text`, `llm_failure`, `parse_failure`, `schema_failure`, `num_retries`, `error_message`, `elapsed_sec`
- `structured.py` — `safe_parse_structured_response()`, `validate_and_fallback()`
- `artifacts.py` — per-call JSONL artifact capture with all failure flags
- `utils/logging.py` — stdlib logging wrapper

Real Ollama call (`llama3:latest`, 8B Q4) is live-verified end-to-end: `generate()` → HTTP → `safe_parse_structured_response()` → Pydantic validation → JSONL artifact on disk. OpenAI path fails clean when key is absent; live call pending key.

No Atlas QA module imports from the upstream repo. Import boundary is confirmed.

### 3.3 Source-authority knowns (newly settled)
A full annotation pass over 633 course description pairs (catalog vs guide) across all overlap zones has been completed. Key settled decisions:

**What is resolved:**
- Course description default = CAT-TEXT confirmed safe across all 571 overlapping courses. No row in the full 633-pair corpus produced a clear guide preference over catalog for default display.
- Guide prefix artifact explains 63 of 65 STRONG mat-diff program description pairs: guides prepend a metadata header (`Program Code / Catalog Version / Published Date`); after stripping, body text is identical to catalog. Only MATSPED (guide text abridged) and BAESSPMM (guide has additional sentence) have genuine content differences; catalog is the display default for both. Catalog is the display default for all program descriptions.
- GUIDE is the sole source for competency bullets, cert prep signals, AoS, and capstone. No authority question exists for these blocks.
- CANON is the sole authority for identity facts (CU, code, title). 41 courses have guide-internal CU conflicts across programs.
- PLOs exist only in CAT-TEXT; guides contain no program learning outcomes.

**What requires QA design care:**
- 5 programs have catalog/guide version token mismatches: MACCA, MACCF, MACCM, MACCT (catalog 3 months newer), MSHRM (guide 8 months newer — widest gap in corpus; body text currently identical after prefix strip but freshness gap is real). Mixed-version context for these programs requires explicit dual version citation.
- 74 courses have 2–4 guide description variants keyed to source programs. 185 courses have 2–6 competency variants. When program context is known, use the matching variant. When absent, use the most-common variant and disclose multi-variant status.
- Two hard anomaly flags must be in canonical objects before QA construction:
  - C179 (Advanced Networking Concepts): catalog text is 293 chars — unusually short; completeness unconfirmed. Guide adds detail not in catalog. Inspect catalog extract before treating catalog-default as complete for this course.
  - D554 (Advanced Financial Accounting I): guide description contains text from D560 (data anomaly in extraction pipeline). Do not use guide description for D554.

The main unresolved QA design issues are no longer about default description authority — that is settled. The genuine open issues are: multi-variant handling when program context is absent (§5.4 Q1), dual-version-token disclosure UX for the 5 conflicted programs (§5.4 Q2–3), and anomaly-aware QA behavior for C179 and D554 (§5.4 Q4).

Full policy: `BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md`.

## 4) Core risk model
Highest-risk failure mode remains:

**Plausible, citation-bearing, wrong-version synthesis.**

Secondary risks:
- entity collision across near-duplicate titles/tracks
- negative claims made without completeness guarantees
- citation-present but claim-not-entailed answers
- source-authority violation: answering from guide when catalog is the policy default (or vice versa)

## 5) What we still need expert feedback on

### 5.1 Representation and canonical object design
1. Minimum required fields per canonical object to support robust retrieval + grounded answers.
2. Whether any additional first-class object is needed for v1 beyond the four current types (`course_card`, `program_version_card`, `guide_section_card`, `version_diff_card`).
3. Best practices for preserving source fidelity while normalizing text views.
4. How to carry source-authority fields (`display_source`, `anomaly_flags`, `description_guide_alternate_count`) in `course_card` so the QA control layer can apply the source policy deterministically at retrieval time without LLM involvement.

### 5.2 Retrieval and partitioning details
1. Practical hybrid weighting strategy by query class (exact vs NL).
2. Hard partition edge cases: when to allow controlled scope widening without introducing version/entity contamination.
3. Recommended reranking strategy for v1 before adding heavier components.

### 5.3 Completeness and abstention policy
1. Recommended operational definition of completeness for absence claims.
2. Best abstention thresholds/signals for deterministic-first pipelines.
3. Which ambiguous query classes should default to abstain vs clarify.

### 5.4 Source precedence and conflict handling (revised — prior open questions now mostly settled)

The prior version of this section asked whether catalog-first was the right default and how to handle guide-catalog conflicts. Those questions are now resolved (see §3.3 and §2 locked decision 6).

**Remaining genuine open questions:**

1. For courses with multi-variant competency rows (185 courses, 2–6 variants keyed to source programs): when program context is absent, is "most-common variant by source program count" a defensible default, or is there a better selection heuristic for a v1 QA system?

2. For the 5 version-conflicted programs (MACCA/MACCF/MACCM/MACCT/MSHRM): what is the least-confusing way to surface dual version tokens in a citation-grounded answer without appearing to undermine confidence in the answer itself?

3. For the MSHRM case specifically (guide 8 months newer, body text currently identical): should QA default to guide-version disclosure proactively, or only disclose the gap when the user's question is about content that could plausibly differ between versions?

4. Same-field substantive conflict within a single version — meaning both catalog and guide are present for the same field with genuinely different text, not explained by the known guide prefix artifact and not a named anomaly case (C179, D554): what is the right QA display contract — surface both with source labels, suppress the weaker source, or abstain until a per-field policy decision is made?

### 5.5 Evaluation and launch gates
1. Required minimum test set composition before v1 launch.
2. Critical thresholds for:
   - version contamination rate
   - claim entailment support
   - abstention precision/recall
3. Recommended manual-audit protocol for citation-entailment correctness.

## 6) Scope boundaries (unchanged)
In-scope v1:
- factual QA over catalog/guide data
- program/course lookup
- section-grounded answers
- explicit version-aware comparisons

Out-of-scope v1:
- personal advising
- schedule/instructor assignment
- tuition/admissions/aid unless explicitly represented
- open-ended career guidance

## 7) Requested response format
Please respond in this structure:

1. **Top 3 corrections to our current locked plan**
2. **Top 3 unresolved decisions we should settle before implementation freeze**
3. **Most likely high-impact failure still not fully mitigated**
4. **Minimum launch-gate metrics you would enforce**
5. **What to defer from v1 even if technically feasible**

## 8) Appendix: source family terminology

| Abbreviation | Meaning |
|---|---|
| CAT | Catalog PDF structured data (program/course metadata, CU totals, roster facts) |
| CAT-TEXT | Catalog extracted text fields (descriptions, PLOs, licensure language) |
| GUIDE | Parsed program guide content (standard path, AoS, capstone, competencies, cert signals) |
| CANON | Canonical course/program index — cross-source identity resolution (course codes, titles, CU) |
| ENRICH | Guide-derived enrichment fields surfaced at the course level (competency bullets, cert signals, guide description variants) |

---

## 9) Appendix: concise architecture snapshot
Pipeline (v1 target):
1. deterministic pre-router
2. structured LLM classifier for fuzzy queries
3. deterministic entity/version resolver
4. hard retrieval partitioning (entity/version/source/section)
5. deterministic fetch or hybrid retrieval over canonical objects
6. evidence bundle construction
7. pre-generation sufficiency/abstention gate
8. constrained generation (if needed)
9. post-check (citation + version disclosure + source-authority compliance)

Source family terminology: see §8 above.

Atlas-local substrate: `src/atlas_qa/llm/` (client, registry, types, structured, artifacts) + `src/atlas_qa/utils/logging`. All verified. See `LOCAL_8B_RAG_SYSTEM_DESIGN.md` §2.2–2.4 for current-state detail.

---

Contact: WGU Atlas data systems team
Intent: finalize implementation decisions and launch gates for v1.
