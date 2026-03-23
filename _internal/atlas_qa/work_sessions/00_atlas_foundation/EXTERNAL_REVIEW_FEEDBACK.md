# External Review Feedback

**RFI version reviewed:** v3 (2026-03-23)
**Active RFI version:** v4 — see `LOCAL_8B_RFI.md`
**Prior RFI snapshot:** `LOCAL_8B_RFI_v3_snapshot.md`

---

## Reviewer A

Below is the technical review of the RFI. It is based on the constraints, corpus shape, and v1 architecture in the document.

## 1. Top 3 changes I recommend immediately

### 1) Make **deterministic answer assembly** the default for a large share of v1

Your current design is directionally correct, but I would push it further: for exact-identifier and single-entity factual questions, the model should not be the primary answer composer. The system should:

* classify question type first
* resolve entity and version deterministically
* execute a typed retrieval or lookup plan
* assemble a structured evidence bundle
* use the model only for surface realization, or skip the model entirely for templated answers

For this corpus, many common student questions are likely to be:

* “What is D426?”
* “How many CUs is program X?”
* “What is in the capstone section for version Y?”
* “What changed between edition A and B?”

Those are not “reasoning-heavy” tasks. They are retrieval, selection, and formatting tasks. A 7B–8B model is most valuable at paraphrasing, answering mild natural-language variants, and composing concise summaries from already-curated evidence. It is least trustworthy when forced to decide what facts are relevant across multiple near-duplicate chunks.

**Practical rule:** if the query can be answered from one canonical row/object or one resolved section bundle, do not let the model decide the facts.

---

### 2) Introduce **canonical text views** as first-class retrieval objects

Your parser-derived boundaries are a major advantage. Use them to create deterministic synthetic views that are cleaner than raw text and more queryable than raw parse objects.

I would create these first:

* **Canonical course card**

  * canonical course code
  * title variants
  * linked catalog/guide occurrences
  * CU / units if stable
  * source versions
  * short normalized description
  * evidence pointers

* **Canonical program-version card**

  * program code
  * program title
  * edition/version
  * required courses
  * total CUs
  * section availability
  * linked guide sections
  * evidence pointers

* **Guide section card**

  * program
  * version
  * section type (`standard_path`, `areas_of_study`, `capstone`)
  * normalized section text
  * structured course mentions
  * evidence pointers

* **Version diff card**

  * entity
  * older version
  * newer version
  * deterministic added/removed/changed fields
  * evidence pointers

These views should become the main retrieval and generation inputs. Parsed artifacts alone are often too skeletal; raw spans alone are too noisy. Synthetic views give you the right abstraction boundary. This directly addresses your stated goal that facts should live in the corpus, not in model weights.  

---

### 3) Treat **version control** as a retrieval partition, not just metadata

Wrong-version contamination is not just a ranking problem. It is a dataset partitioning problem. I would enforce version selection upstream:

* resolve version intent before retrieval whenever possible
* retrieve only from one version by default
* widen to multiple versions only when the query explicitly asks for comparison, history, “latest vs prior,” or when version is unresolved and ambiguity must be surfaced
* prohibit answer generation from mixed-version contexts unless the system is in an explicit compare mode

This should be implemented as a hard retrieval contract, not merely a prompt instruction.

**Concrete rule set:**

* exact program + explicit version → only that version
* exact program + no version → latest supported version, but answer must say it
* comparison language → retrieve exactly the compared versions
* unresolved version ambiguity → abstain or ask the user to choose, depending on UX goals

This is the single highest-leverage control for reducing silent synthesis errors in your corpus. Your own risk list already points at this; I would elevate it from “risk” to “primary architectural invariant.” 

---

## 2. Top 3 things to defer from v1

### 1) Broad free-form multi-hop synthesis

Examples:

* “How do these three programs compare in difficulty and workload?”
* “Which path is best for a working parent?”
* “Summarize all meaningful curricular differences across several editions”

Even if retrieval is good, 7B–8B models tend to compress, omit, and merge nearby facts. That is especially dangerous in a versioned corpus with repeated titles and overlapping course sets.

Defer any feature where the system is expected to produce a broad synthesized narrative across many entities unless the comparison is built deterministically first.

---

### 2) Model-based answerability as the primary gate

For v1, answerability should be mostly hybrid but led by rules and scores, not by an LLM judgment. Small models are poor calibrated judges of whether evidence is sufficient, especially when evidence is partial-but-plausible.

Use model judgment only as one weak signal, not the top-level controller.

---

### 3) Heavy embedding dependence for exact-heavy retrieval

Do not overinvest early in dense retrieval as the core answer path. Your corpus is identifier-rich and structurally normalized. That favors:

* lexical retrieval
* entity dictionaries
* alias tables
* metadata filters
* deterministic joins

Embeddings should help recall on natural-language paraphrases and fuzzy section queries, but they should not be the backbone for code-heavy lookups.

---

## 3. Most likely failure mode in this plan

**Silent mixed-version synthesis after superficially correct retrieval.**

Not total hallucination. Not obvious retrieval miss. The most likely failure is this:

1. retrieval gets mostly relevant evidence
2. two chunks are from adjacent editions or linked guide/catalog artifacts
3. both mention similar courses/sections/titles
4. the model blends them into one coherent answer
5. citations look plausible, but the answer never makes the version boundary explicit

That is more dangerous than a blatant wrong answer because it will often pass casual review.

This is the characteristic failure mode for small-model RAG over repetitive institutional documents. Your current design already identifies version contamination and small-model context misuse as risks; I agree those are the top pair. I would add a third closely related risk: **citation-valid but claim-invalid answers**, where each cited chunk is real, but the combined claim is unsupported. 

---

## 4. Minimum viable evaluation suite I would require before launch

The evaluation needs to test the pipeline, not just final answer quality. At minimum, I would require gated checks for five layers.

### A) Query routing / entity resolution

Gold set categories:

* exact course code
* exact program code
* title aliases
* title collisions
* explicit version queries
* implicit latest-version queries
* comparison queries
* unsupported/out-of-scope queries

Metrics:

* routing accuracy
* entity resolution accuracy
* version resolution accuracy

Launch target:

* exact code/program routing: **≥99%**
* explicit version resolution: **≥99%**
* alias/title resolution: **≥95%**

If these are weak, downstream evaluation is misleading.

---

### B) Retrieval quality

Measure retrieval separately for each query class:

* exact identifier lookup
* single-entity NL factual lookup
* section retrieval
* comparison retrieval
* abstain-required queries

Metrics:

* Recall@k for gold evidence unit
* MRR / nDCG for ranked relevance
* version-filter precision
* contamination rate: fraction of retrieved context from wrong version/entity

Launch target:

* exact lookup gold evidence in top 1: **≥99%**
* single-entity NL evidence in top 3: **≥95%**
* section queries evidence in top 5: **≥90%**
* wrong-version contamination after filters: **<1%** on version-specific queries

For this corpus, contamination rate is more important than generic semantic relevance.

---

### C) Grounded answer generation

This must be claim-level, not answer-level only.

Score:

* citation presence
* citation correctness
* claim support
* unsupported claim rate
* omission of requested version qualifiers

I would explicitly separate:

* **citation attached**
* **citation points to relevant evidence**
* **claim is actually entailed by evidence**

Those are different.

Launch target:

* answers with all material claims supported: **≥95%** on in-scope answerable set
* unsupported material claim rate: **≤2%**
* citation attachment on non-abstained answers: **100%**

---

### D) Abstention correctness

Build a gold set of:

* out-of-scope questions
* underspecified version questions where ambiguity matters
* unsupported synthesis questions
* “looks answerable but corpus lacks evidence” questions
* partial evidence cases

Metrics:

* precision/recall/F1 for abstain
* false-answer rate on abstain-required queries
* over-refusal rate on answerable queries

Launch target:

* false-answer rate on abstain-required queries: **≤5%**
* abstain F1: **≥0.85**
* over-refusal on answerable in-scope queries: **≤10%**

In v1, it is better to over-refuse slightly than to fabricate.

---

### E) Version correctness

This deserves its own test suite, not just a tag in the general set.

Gold categories:

* latest-default queries
* explicit historical queries
* explicit compare queries
* ambiguous version questions
* guide/catalog disagreement cases
* changed course membership across editions

Metrics:

* correct version selected
* correct multi-version display when required
* no silent merge
* explicit version disclosure in answer text

Launch target:

* version correctness on version-sensitive answerable queries: **≥97%**
* silent merge rate: **0% tolerated in launch blocker set**

---

### Minimum test set composition

At absolute minimum, before launch:

* 75 exact identifier questions
* 75 single-entity NL questions
* 50 section-grounded questions
* 50 version-sensitive questions
* 40 comparison questions
* 40 abstain-required questions
* 20 parser-anomaly / conflict cases

Roughly **350 gold questions** is enough for a serious v1 gate if sampled well.

---

## 5. Any hard disagreement with your current architecture and why

### Disagreement 1: “Hybrid retrieval” is too generic as the v1 center of gravity

For this corpus, the backbone should be:

**router → entity/version resolver → deterministic object fetch or filtered lexical retrieval → optional rerank → bounded generation**

not a generic hybrid-RAG stack with additional safeguards.

Hybrid retrieval still belongs in the system, but mainly for:

* fuzzy natural-language questions
* title paraphrases
* section-content phrasing
* fallback recall when deterministic resolution is uncertain

If you design around generic hybrid RAG first, you will likely spend time compensating for failure modes you could have prevented with typed retrieval.

---

### Disagreement 2: “Post-answer validation” should not carry too much responsibility

Validation after generation is useful, but it should not be the main defense. Once a small model has synthesized across noisy context, many validators will only catch obvious failures.

Better pattern:

* validate evidence sufficiency **before** generation
* generate from a constrained structured evidence bundle
* do a lightweight post-check for unsupported spans, missing citations, and version disclosure

In other words, move the strongest controls earlier in the pipeline.

---

### Disagreement 3: parsed artifacts alone are not enough, but raw text should remain secondary

You asked what is materially lost if you rely mostly on parsed artifacts. The main losses are:

* local explanatory phrasing useful for NL matching
* qualifier language around requirements/exceptions
* section headers and adjacency cues
* subtle distinctions introduced by formatting or nearby prose

But the answer is not “index lots of raw text.” The answer is “generate canonical synthetic views and attach selective provenance spans.” Raw text should be evidence support, not the primary semantic substrate.

---

## Additional concrete recommendations by topic

### Feasibility on 7B–8B

High-confidence for v1:

* exact course/program lookup
* section-grounded factual QA
* explicit version lookup
* deterministic compare summaries when diffs are precomputed
* citation-bearing short answers from a small evidence bundle

Lower-confidence / unreliable:

* broad multi-program synthesis
* open-ended why/how advisement
* latent inference from absent evidence
* conflict resolution when catalog and guide disagree without deterministic precedence rules

Where small models will fail:

* choosing among several near-duplicate chunks
* preserving version boundaries across multiple citations
* negative claims (“not listed,” “no capstone mentioned”) unless explicitly supported by deterministic absence logic
* composing comparisons without dropping edge conditions

---

### Representation strategy

Primary retrieval units for v1:

1. canonical synthetic views
2. parsed artifact units
3. selective raw provenance spans

Not the reverse.

Most harmful raw-text noise patterns:

* repeated headers/footers
* OCR line breaks splitting codes/titles
* duplicate edition boilerplate
* table extraction corruption
* nearby but unrelated program text in the same page span
* section spillover caused by parser boundary drift

---

### Retrieval and routing

For exact-heavy corpora, use **hybrid**, but with clear dominance by exact/lexical mechanisms.

Recommended handling:

* `D426`, `BSDA`, exact titles, exact version strings
  → deterministic resolver + direct fetch or BM25-style exact retrieval only
* NL section queries
  → lexical + embedding recall, then strong metadata filters and rerank
* comparison queries
  → resolve both entities/versions first, retrieve both separately, then compose

Mandatory metadata filters in v1:

* entity type
* canonical entity id
* version/edition
* source family (catalog vs guide)
* section type
* answerability-relevant provenance quality flag
* parser confidence / anomaly flag

Chunk granularity:

* **catalog program blocks**: program-version block as primary, with sub-blocks for requirement subsections when large
* **guide sections**: section-level chunks, not page chunks
* **course index entries**: one entry per canonical course card, with aliases embedded

Reranking should be aggressive. For an 8B model, you want the smallest possible context that still fully supports the answer. I would typically pack:

* 1–3 chunks for exact/single-entity questions
* 2–4 chunks per side for comparisons
* do not exceed roughly 6–8 evidence units unless you have no alternative

---

### Context and prompting

Prefer **fewer, cleaner, labeled chunks** over more smaller ones.

Best pattern:

* evidence objects with stable labels
* explicit entity/version labels on every chunk
* instructions to answer only from evidence
* structured output with answer + citations + abstain reason if unsupported

Prompt contract should require:

* explicit version named in the answer when version-sensitive
* every material claim tied to a citation
* abstain if evidence is missing, mixed, or conflicting without precedence rule
* no claim from memory
* no negative claim unless supported by deterministic completeness logic

---

### Answerability and abstention

Best v1 design: **hybrid, but mostly rule-based + score-based**

Reliable abstention signals:

* unresolved entity or version
* insufficient evidence coverage for required fields
* retrieval contamination across versions
* low margin between top candidate entities
* conflict between catalog and guide without precedence policy
* parser anomaly flag on the selected evidence
* compare question where one side is missing matched evidence

Hardest classes:

* underspecified version questions that still look answerable
* “What changed?” questions when changes are partially structural and partially textual
* negative queries
* questions requiring cross-source reconciliation rather than direct lookup

---

### Versioning policy

I agree with **default to latest** for v1, but only if the answer states that it is using the latest available version.

Return multiple versions by default only when:

* the user asks for comparison/history
* the entity name is stable but program structure materially differs across editions and ambiguity would change the answer
* resolver confidence is split across multiple close versions

To prevent silent merging:

* one-version retrieval contexts by default
* explicit compare mode with separate evidence buckets
* answer template that names source version before claims
* blocker validation if evidence bundle mixes versions without compare mode

---

### Highest-impact post-v1 improvements

1. deterministic diff generation for version comparisons
2. learned or cross-encoder reranking tuned on your query classes
3. better calibration for abstention using logged production failures
4. selective use of larger remote models for offline evaluation or adjudication, not primary serving
5. richer conflict-resolution policy between guide and catalog families

---

## Bottom line

Your proposed baseline is fundamentally sound, and the central design principle is correct. The main correction is to lean even harder into **typed deterministic retrieval and canonical synthetic views**, while reducing the share of work delegated to the 8B model. The highest risk is not generic hallucination; it is **plausible, citation-bearing, wrong-version synthesis**. v1 should be built to make that failure structurally difficult rather than trying to clean it up afterward.  

If useful, I can turn this into a reviewer-ready response memo in the exact five-part format from the RFI, tightened to executive-review length.






---

## Reviewer B

This RFI v2 reflects a significant and impressive leap in structural maturity. Moving the **Atlas-local substrate** to a live-verified state is a major win for data sovereignty and latency. Your "Locked Decisions" show a healthy respect for the "Stochastic Parrot" problem by tethering the 8B model to a deterministic leash.

The following critique focuses on ensuring that the "last mile" of implementation doesn't inadvertently introduce the version-bleeding or source-authority confusion you've worked so hard to prevent.

---

## 1) Top 3 corrections to your current locked plan

1.  **Reconsider the "Most-Common Variant" Heuristic (§5.4 Q1):**
    Using the "most-common variant" when program context is absent is a "soft" failure mode. If a student in a minority-variant program receives "most-common" data, the system has effectively hallucinated a requirement for them.
    * **Correction:** If program context is missing for a course with multiple variants, the system should **abstain from a definitive statement** and instead provide a summary: *"There are [N] variations of competencies for this course depending on your program. Please specify your program (e.g., BSIT) for the exact list."*

2.  **Proactive vs. Reactive Mismatch Disclosure (§5.4 Q3):**
    For the MSHRM case (8-month gap), waiting for a "content-plausible" conflict is too high a bar for an 8B model to adjudicate at runtime.
    * **Correction:** Make version-token mismatch disclosure a **standard UI component** for those 5 specific programs. If a user asks about MSHRM, a footer or callout should immediately state: *"Note: Data for this program is reconciled between Catalog [Date] and Program Guide [Date]."* Transparency builds more trust than a system that appears to ignore a nearly year-long discrepancy.

3.  **The "Abstention-First" Definition (§5.3):**
    Your plan is currently "Abstention-first," but "negative claim completeness" is difficult to guarantee.
    * **Correction:** Shift from a goal of "proving a negative" to "exhausting the index." Instead of saying "This course has no prerequisites," the system should say "No prerequisites are listed for this course in the [Version] Catalog." This protects the system if the source data itself is the point of failure.

---

## 2) Top 3 unresolved decisions to settle before freeze

1.  **The "Clarification Loop" UX:**
    Since you are using a deterministic-first architecture, you need a locked-in strategy for when the LLM identifies a "Fuzzy Query" that lacks a Version or Program identifier. Will the system **guess** based on the most recent version, or **prompt** the user? I recommend a "Latest Version by Default" policy with a clear "Change Version" toggle in the UI.

2.  **Canonical Object Minimum Fields (§5.1):**
    To support the policy in §3.3, `course_card` needs more than just text.
    * **Decision:** You must include a `source_provenance_map`. This field should explicitly map which keys (e.g., `description`, `competencies`) came from which source (`CAT-TEXT` vs `GUIDE`). This allows the "post-check" layer to verify source-authority compliance without re-running retrieval logic.

3.  **Reranking Strategy for v1 (§5.2):**
    For an 8B model, context window management is key.
    * **Decision:** Implement a simple **Cross-Encoder reranker** (like `bge-reranker-base`) after initial retrieval. This ensures that the few chunks the 8B model sees are the most relevant, reducing the risk of the model latching onto irrelevant "noise" in the tail of the retrieval set.

---

## 3) Most likely high-impact failure still not fully mitigated

**"The Near-Neighbor Version Trap"**

Because you are using local Ollama (Llama 3 8B), the model has extensive pre-existing knowledge about academic structures. If a user asks a question about a 2026 program version, but the RAG retrieval returns a highly relevant chunk from 2025 (due to a failure in the deterministic filter), the LLM may not have the "critical thinking" capacity to notice the 1-year digit difference. It will synthesize an answer that looks perfectly grounded but is factually obsolete.

**Mitigation:** The "Evidence Bundle" (§9, Step 6) must include a **hard version-tag** on every single line of text injected into the prompt. The System Prompt must strictly instruct: *"Reject any information that does not match Version [X]."*

---

## 4) Minimum launch-gate metrics

To ensure v1 doesn't degrade trust, I would enforce these three thresholds:

| Metric | Target | Definition |
| :--- | :--- | :--- |
| **Version Isolation Score** | **100%** | Zero instances of Program A / Year X data appearing in a Program A / Year Y response in a 500-query test set. |
| **Citation Entailment** | **>98%** | Every claim made by the LLM must be directly traceable to the provided text block (Manual Audit). |
| **Abstention Precision** | **>95%** | When the system says "I don't know" or "Data not found," it must actually be absent from the provided context. |

---

## 5) What to defer from v1

1.  **Cross-Source Synthesis:** Do not try to merge a Catalog description and a Guide description into a single "Super-Description." Stick to the **Source Authority Policy** (Catalog-first).
2.  **Multi-Hop Logic:** Defer queries that require calculating "Total CU to graduation" by summing individual course cards. Keep it to "Lookup" and "Compare" functions. Summation is a deterministic task for a database, not an 8B LLM.
3.  **Natural Language "Diffing":** If a user asks "What changed between 2024 and 2025?", use your `version_diff_card` (deterministic) rather than asking the LLM to summarize the differences between two raw text blocks.

**Would you like me to draft a sample `Evidence Bundle` structure that includes the source-authority tags for your `course_card` objects?**








---

## Reviewer C

This is an excellent, mature RFI. The level of detail, the clear separation of locked vs. open decisions, and the explicit acknowledgment of the risk model make it easy to provide focused feedback. The work on source authority (section 3.3) is particularly impressive and solves the most common failure mode in educational RAG systems.

Here is my expert feedback structured according to your requested format.

---

### 1. Top 3 corrections to our current locked plan

Your locked plan is fundamentally sound. My "corrections" are more about clarifying potential pitfalls in the implementation of these locked decisions.

1.  **Clarify "Deterministic-First Architecture" (Locked Decision #1 & #4):** The plan to use a structured LLM classifier for fuzzy queries is correct, but the line between "deterministic routing" and "constrained generation" needs a hard boundary *before* the LLM is invoked.
    - **Correction:** For the "structured LLM classifier for fuzzy queries," do not treat this as a single intent-classification step. Implement it as a two-step gate:
        - **Step 1 (Schema Validation):** The *only* acceptable output from the LLM for this step is a Pydantic-validated object like `{ "intent": "program_details", "entities": [{"name": "MACCA", "type": "program_code"}] }`. If the LLM fails to output this exact structure, the system should abstain immediately, *not* attempt to use the LLM's raw text output for retrieval.
        - **Step 2 (Deterministic Execution):** The output of Step 1 is then used *only* to call deterministic functions (e.g., `get_program_version_card("MACCA")`). Under no circumstances should the output of the classifier be passed to a separate "generation" LLM for retrieval. This prevents the LLM from autonomously selecting sources or versions, which you correctly forbid. Your `safe_parse_structured_response()` in `structured.py` is perfectly suited to enforce this gate.

2.  **Rethink "Single-Version Retrieval by Default" (Locked Decision #3) in context of §5.4 Q2:** While correct for 99% of queries, the 5 conflicted programs (MACCA, MACCF, MACCM, MACCT, MSHRM) represent a legitimate edge case where the *default* single-version retrieval could be wrong. The lock is good, but the implementation must have an escape hatch.
    - **Correction:** Implement an **"authoritative-version-first"** resolver, not just a "single-version" resolver. For these 5 programs, the system should have a pre-defined mapping that says `"MACCA": {"authoritative_version": "2025-03", "fallback_version": "2024-12"}`. The default retrieval should be for the authoritative version, but the `version_diff_card` and the citation should always disclose the existence of the other token. This provides a deterministic, policy-driven answer to your question in §5.4 Q2 without relying on the LLM to make a judgment call.

3.  **Source Authority as a Retrieval Constraint, Not Just a Display Policy (Locked Decision #6):** You've correctly locked display and authority. However, for maximum safety, this authority policy must be enforced at *retrieval time*, not just at generation/display time.
    - **Correction:** Your retrieval pipeline should implement a **source-policy filter**. If the user asks a question about "course competencies," the system should *never* retrieve from `CAT-TEXT` or `CANON` for that query. It should only query the index containing `GUIDE` objects. Conversely, for a question about "course description," it should *only* retrieve from `CAT-TEXT`. This hard retrieval partition based on the field's defined authority prevents the LLM from ever being presented with conflicting source material, eliminating the possibility of a source-authority violation at the generation stage.

### 2. Top 3 unresolved decisions we should settle before implementation freeze

1.  **§5.4 Q1: Multi-variant Competency Selection Heuristic:** The "most-common variant by source program count" is defensible, but it's a heuristic that can create a subtle failure mode: giving a student from a niche program the competency list for a more common but different program.
    - **Settlement:** Implement a **fallback chain**:
        1.  **Program Context:** If the user query contains a specific program identifier (e.g., "in the MACCT program"), use the variant tied to that program.
        2.  **No Context, but Single Canonical Guide:** If the course has a single canonical guide across all programs (the majority case), use that.
        3.  **No Context & Multiple Variants:** Use the most-common variant, but **append a deterministic, non-LLM-generated disclaimer** to the evidence bundle. For example: `[Note: This course has X different competency sets across programs. This is the version from the most common program, Y. The variant for your specific program may differ.]` This makes the system's behavior transparent and avoids a "confidently wrong" answer.

2.  **§5.4 Q3: MSHRM Proactive Disclosure:** The 8-month gap is a real risk. If a student asks about a policy change that might have occurred in that window, the system would have no way to know. Waiting for the user to ask about a "difference" is too late.
    - **Settlement:** **Yes, be proactive.** Implement a **version-gap flag** for any retrieval over a conflicted program. If the user asks *any* factual question about the program, the citation block should include a standard line: `[Note: This information is based on the [current_date] catalog version. A newer program guide dated [newer_date] is available but shows no textual differences in the retrieved content.]` This proactively manages user expectations without undermining confidence. For your question in §5.4 Q2, this same logic applies to the 5 conflicted programs.

3.  **§5.4 Q4: Same-Field Substantive Conflict:** This is the trickiest remaining edge case. Using the two anomaly examples (C179, D554) as a guide, you need a policy for the general case.
    - **Settlement:** Adopt a **"both-surfaces-with-source-authority"** contract, but with a strict triage rule:
        1.  **Pre-identified Anomaly (C179, D554):** Follow the anomaly-specific handling (e.g., for C179, surface the guide description as an "enrichment note" but do not replace the catalog default). This is a manual policy override.
        2.  **General Conflict (not pre-identified):** Surface both, with source labels. The LLM is forbidden from choosing. The response should be structured: `Catalog Description: [text]` and `Guide Description (Enrichment): [text]`. Include a note: `[Note: The catalog and guide differ for this course. Both are shown.]` This is the safest path, as it doesn't require a per-field policy and makes the conflict transparent to the user, who is the ultimate arbiter.

### 3. Most likely high-impact failure still not fully mitigated

**The "Entity Collision + Version Ambiguity" Cascade.**

Your risk model correctly identifies "plausible, citation-bearing, wrong-version synthesis." The highest-impact version of this will happen when there's an entity collision (e.g., a course code that exists in multiple programs or a program name like "MBA" with different tracks) *and* the user's query is vague.

**Example:** A user asks, "Tell me about the capstone for the MBA."
- The deterministic router might resolve to the generic "MBA" program, which might be a placeholder.
- The hybrid retrieval, seeing no exact match, widens scope (as per §5.2 Q2) and retrieves `guide_section_card`s for "MBA in IT Management" and "MBA in Healthcare Management."
- The LLM, given two sources, may synthesize a generic description that doesn't match either, or worse, cite the wrong one.

**Mitigation:** Your `version_diff_card` is designed for this, but it's currently framed for version comparisons. **You need an `entity_disambiguation_card`** that is triggered *before* retrieval. This card would be used when multiple entities match a fuzzy query. Instead of retrieving and synthesizing, the system would abstain and present the user with a deterministic, structured choice: "We found multiple MBA programs (MBAITM, MBAHCM). Which one are you asking about?" This forces the user to resolve the ambiguity, preventing the system from making a potentially wrong, but plausible, synthesis.

### 4. Minimum launch-gate metrics you would enforce

1.  **Version Contamination Rate:** 0% on a holdout set of 100 queries that specifically target the 5 version-conflicted programs and the 74 multi-variant courses.
    - *How to measure:* Manually audit the `version_diff_card` in the evidence bundle for every single response. The citation must always list the correct version token(s) used. Any response where the citation is for the wrong version, or fails to disclose a known gap, fails the gate.

2.  **Claim Entailment Support:** 99% precision on a holdout set of 100 queries.
    - *How to measure:* For every factual claim made in the LLM's final answer, a human auditor must be able to point to the exact sentence in the evidence bundle that supports it. This is a stricter measure than just "citation present." For the deterministic lookup cases (e.g., "What is the CU for C179?"), this must be 100%. For the generative summarization cases, it must be >95%.

3.  **Abstention Precision/Recall:** As a system, it's better to abstain incorrectly than to answer incorrectly. For a set of 50 queries that are explicitly out-of-scope (e.g., "What's Professor Smith's email?") or maliciously ambiguous, the system must abstain with 100% recall (i.e., it never attempts an answer). For 50 queries that are in-scope but ambiguous, the system should have a recall of >90% for identifying the ambiguity and presenting the `entity_disambiguation_card` (or abstaining) rather than attempting a guess.

### 5. What to defer from v1 even if technically feasible

1.  **Natural Language Comparison (beyond explicit version compare):** Defer queries like "How does the capstone for MACCT compare to the one for MBAITM?" The complexity of entity resolution, retrieval partitioning, and structured output for a *pairwise* comparison is a v2 feature. Stick to the explicit `version_diff_card` for the known conflicted versions.

2.  **Semantic Reranking (as a core component, §5.2 Q3):** You asked about a reranking strategy. For v1, **do not use a semantic reranker**. Your deterministic-first approach and hybrid keyword/vector search (with a simple, tuned `k` value) will be more predictable and debuggable. Adding a reranker introduces a new black box that can subtly change relevance in ways that are hard to audit. Save this for v2 when you have a robust test set to measure its actual impact.

3.  **Completeness Checks for Absence Claims (§5.3 Q1):** Defer the automated "completeness check" for claims of absence. The operational definition for v1 should be **"absence in the retrieved evidence bundle."** Do not attempt to verify that the evidence bundle *itself* is complete (i.e., that there isn't some other catalog section not retrieved that contains the answer). For v1, if the deterministic retrieval for "entity X" + "field Y" returns no result, the system can safely state: "No information on Y was found in the [source] for X." This is a factual statement. The risk of claiming something doesn't exist when it does (e.g., in a different section) is too high for v1 without a complex completeness model.