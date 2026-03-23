## 1. Top 3 corrections to your current locked plan

### 1) Make **source authority** a two-stage contract, not a single hard pre-retrieval filter

The current direction is mostly right, but I would not rely on only one boundary. A pure pre-retrieval hard filter can fail in two ways:

* it can hide useful evidence needed to detect conflict or anomaly state
* it can make debugging retrieval failures harder because the system never sees excluded alternatives

Recommended correction:

* **stage 1:** resolve the allowed source family for answering
* **stage 2:** retrieve only eligible answer evidence for packing
* **but also:** optionally fetch a tiny shadow set of disallowed-but-related evidence for validator/debug use, never for answer generation

That gives you strict answer-time compliance without blinding the control layer to conflict signals. This matters most for your named anomaly cases and any future same-field substantive conflict cases. 

---

### 2) Add a first-class **conflict/anomaly adjudication object**

The four current object types are good, but I would add one more first-class control object for v1:

* `adjudication_record` or `field_conflict_record`

Minimum purpose:

* entity id
* version
* field name
* source family pair involved
* conflict type (`authority_override`, `same_field_conflict`, `known_anomaly`, `variant_selection`, `dual_version_token`)
* winning policy
* fallback behavior
* disclosure requirement
* launch-blocking flag

Without this, conflict handling logic will be scattered across retrieval, canonical objects, and prompts. That increases the chance of inconsistent behavior. Given that source authority and anomaly handling are now core design commitments, they deserve their own explicit control object, not just flags embedded in `course_card`. 

---

### 3) Tighten the definition of **deterministic-first** so “structured LLM classifier” cannot silently widen scope

Right now, the locked plan still leaves one soft point: the fuzzy-query classifier. If that component can return broad or weakly calibrated candidates, it can still introduce the very contamination you are trying to eliminate.

I would add these constraints:

* classifier may propose candidates, not decide final entity/version scope
* deterministic resolver must either select one candidate above threshold or abstain
* no classifier-driven widening from single-version to multi-version scope
* no classifier-driven widening across source families
* every scope-widening event must be rule-triggered and auditable

This is especially important because silent mixed-version synthesis remains your stated top launch blocker. The classifier must not become an unbounded loophole around the partitioning rules. 

---

## 2. Top 3 unresolved decisions you should settle before implementation freeze

### 1) Multi-variant competency fallback: **most-common with disclosure** vs **abstain for program context**

This is the highest-value unresolved product decision in the document.

My recommendation for v1:

* for **display-oriented** answers, allow **most-common variant with explicit disclosure**
* for **comparison, requirement, or exact wording** questions, **abstain unless program context is resolved**

Reason:

* always abstaining will feel unnecessarily brittle
* always showing most-common risks presenting the wrong competency wording as canonical

So the freeze decision should not be binary. It should be **query-class dependent**. For v1, you need an explicit rule table that says which intents permit most-common fallback and which do not. 

---

### 2) The exact UX contract for the 5 dual-version-token programs

This needs to be fully specified before freeze. Not just “disclose dual version tokens,” but:

* where disclosure appears
* whether it appears inline or in a note
* whether it is always shown or only for affected fields
* whether answers are suppressed when source versions differ but body text is identical
* how citations label source/version pairs

Recommended v1 contract:

* answer normally
* attach source-labeled citations with version tokens
* add a short note only when multiple source versions contribute to the answer or when the question is version-sensitive

That avoids making ordinary answers look unstable while still surfacing the discrepancy when it matters. 

---

### 3) Same-field substantive conflict policy outside named anomalies

This is the most important unresolved control-layer decision. You already ask the right question in §5.4 Q4. My recommendation is to settle a strict hierarchy now:

* if one source is authoritative for that field, suppress the non-authoritative text from answer generation
* if both are same-field candidates and policy does not designate a winner, do **not** synthesize; surface both with labels or abstain
* if conflict affects a factual lookup path, treat as launch-blocking until policy exists

Do not leave this to runtime heuristics. This is exactly the kind of edge case that produces citation-bearing but unsupported answers. 

---

## 3. Most likely high-impact failure still not fully mitigated

**Entity-resolution error that appears as a version problem downstream.**

You are correctly focused on silent mixed-version synthesis, but the upstream precursor is often worse operationally: near-duplicate title or track collision causing the resolver to pick the wrong entity, after which the rest of the system behaves “correctly” within the wrong scope.

That failure is dangerous because:

* version isolation will not save you if the entity is wrong
* citations will still look valid
* deterministic lookup will confidently answer from the wrong program/version
* post-generation checks may all pass

You already mention entity collision as a secondary risk. I would elevate it. In practice, for this corpus, the riskiest chain is:

**fuzzy title match → wrong entity resolution → correctly partitioned retrieval → perfectly grounded wrong answer**

That is harder to detect than generic hallucination and should be treated as co-equal with mixed-version synthesis in launch gating. 

---

## 4. Minimum launch-gate metrics I would enforce

I would enforce separate gates for deterministic paths and non-deterministic retrieval paths.

### A) Deterministic lookup gate

Applies to exact-code lookup and single-entity factual lookups in your Class A/B style bucket.

Required:

* entity resolution accuracy: **≥99.5%**
* version resolution accuracy when explicit: **100%**
* answer field accuracy: **≥99.5%**
* unsupported-claim rate: **0% target, ≤0.5% maximum**
* source-authority violation rate: **0%**

These are the paths users will trust most. They need near-zero error tolerance. 

---

### B) Version-safety gate

This should be a distinct blocker suite.

Required:

* silent version merge rate: **0% acceptable in blocker set**
* wrong-version answer rate on version-sensitive queries: **≤1%**
* required version disclosure presence on multi-version evidence answers: **100%**
* mixed-version generation outside compare mode: **0%**

On this corpus, I would not allow a nonzero tolerated silent merge rate for launch. 

---

### C) Citation-entailment gate

Not just “citation present.”

Required:

* citation presence on non-abstained answers: **100%**
* material-claim entailment precision: **≥97%**
* citation-present but claim-not-entailed rate: **≤2%**
* source-authority compliance among cited evidence: **100%**

Manual audit should score at the **claim level**, not whole-answer level. 

---

### D) Abstention / ambiguity gate

Required:

* abstain precision on ambiguity-required set: **≥90%**
* abstain recall on ambiguity-required set: **≥85%**
* false-answer rate on abstain-required queries: **≤5%**
* over-refusal on clearly answerable in-scope queries: **≤10%**

For v1, slight over-refusal is preferable to confident wrong synthesis. 

---

### E) Recommended minimum test set before launch

I would require at least:

* 100 exact identifier queries
* 100 single-entity factual NL queries
* 75 section-grounded queries
* 75 version-sensitive queries
* 50 compare queries
* 50 ambiguity/abstain queries
* 25 anomaly/conflict queries

That is a **minimum 475-query launch suite**. Given the locked complexity around authority, variants, and version conflicts, anything much smaller will under-sample the real risk surface. 

---

## 5. What to defer from v1 even if technically feasible

### 1) Open-ended synthesis across multiple programs, sections, or versions

Even with your improved architecture, this is where a local 8B model will still compress distinctions, especially around track and version boundaries. Defer broad comparative narratives unless the comparison frame is built deterministically first. 

---

### 2) Automatic handling of unresolved same-field conflicts without a prewritten policy

Do not let the runtime system “decide” whether to merge, pick one, or show both. Until you have explicit per-field conflict policy, defer this to abstain-or-surface-both behavior only. 

---

### 3) Any feature that relies on negative claims beyond explicitly indexed completeness scopes

Your framing for absence claims is good, but operationally this remains fragile. Defer broad “not offered,” “not required,” “not mentioned anywhere,” or “does not exist” style answers unless the system can prove source-scope completeness for that exact field/entity/version combination. 

---

## Bottom line

The revised v3 is substantially stronger than the earlier version. The biggest remaining work is not in generic RAG quality; it is in tightening the control plane around:

* entity disambiguation
* source-authority enforcement with conflict visibility
* multi-variant fallback policy
* exact UX rules for dual-version-token disclosure

If those are settled cleanly, the architecture is credible for a v1 bounded factual QA system on a local 8B model. 









Here’s my feedback on v3, structured as requested.

---

### 1. Top 3 corrections to our current locked plan

1. **Enforce source authority at *indexing* time, not just retrieval-time filter (Locked Decision #6).**  
   Your plan to filter by source at retrieval is correct, but a hard filter still leaves the risk of a mis-query retrieving the wrong source family (e.g., a competency query that accidentally uses a CAT‑TEXT field because of embedding similarity). A safer boundary is to **store each semantic field in a separate vector index** (or with a strict metadata tag that the retriever must match). This makes it impossible for a competency question to ever see CAT‑TEXT content, even in a hybrid search.  
   *Correction:* Move source authority enforcement to the index schema and query construction layer. The retrieval call should explicitly target the index(es) that correspond to the resolved source scope, not retrieve from a unified pool and filter after.

2. **Clarify the role of “deterministic assembly” for exact queries (Locked Decision #1).**  
   The current wording says “model is **not** the primary answer composer; the intended path is deterministic lookup → typed retrieval → structured evidence bundle → templated or surface‑realization‑only answer.” This is excellent, but it risks conflating “no LLM” with “no generative step.” For exact-code factual queries (e.g., “What are the CUs for C179?”), the path should be **fully deterministic**—no LLM even for surface realization. Use a templated response populated from the canonical object. This eliminates the failure mode where an 8B model hallucinates a minor wording change that could be misinterpreted.  
   *Correction:* Explicitly carve out a zero‑LLM path for exact‑identifier, single‑fact queries. Reserve “constrained generation” for queries that require natural language composition (e.g., summarization, comparisons). The classifier in step 2 should route to the zero‑LLM path when possible.

3. **Pre‑retrieval disambiguation (5.2.5) is not just optional—it’s mandatory for v1.**  
   You’ve correctly identified entity collision as a secondary risk, and you ask whether a deterministic disambiguation step should be defined. I would argue that without it, the “entity/version resolver” (step 3) cannot function safely. Your corpus already contains near‑duplicate program titles (e.g., different MBA tracks). If the resolver returns multiple candidate entities for a fuzzy query, the current pipeline would likely proceed with an ambiguous evidence bundle, leading to the cascade failure you’ve flagged.  
   *Correction:* Elevate 5.2.5 from an open question to a locked design commitment. The disambiguation step must produce either a single resolved entity/version or an abstention with a clarification prompt. Do not allow the pipeline to continue with ambiguity.

---

### 2. Top 3 unresolved decisions we should settle before implementation freeze

1. **§5.4 Q1: Multi‑variant competency fallback chain.**  
   Your proposed chain is sensible, but option (a) (“use most‑common variant with disclosure”) is risky for v1. The disclosure text is long and may confuse users; moreover, the “most‑common” variant may still be wrong for many users. The failure mode is giving a student a competency list that doesn’t match their program, which could affect their academic planning.  
   **Settle on (b): abstain and ask for program context** when multiple variants exist and no program is specified. This aligns with your “abstention‑first safety” principle. For v1, it’s better to be humble than to risk giving plausible‑but‑wrong information. You can later add a more sophisticated heuristic when you have user‑context signals.

2. **§5.4 Q3: Proactive disclosure for MSHRM version gap.**  
   The 8‑month gap is substantial. I recommend **proactive disclosure** for *any* query about MSHRM (and the other 4 conflicted programs) when the answer is based on the older version. The disclosure should be a deterministic, templated line in the citation block, e.g.,  
   > *Note: The information above uses the [catalog/guide] version dated [date]. A newer version exists ([date]), but no content differences were found for this question.*  
   This manages expectations without requiring the LLM to decide when it’s relevant. Settle on this as a policy, not a per‑query judgment.

3. **§5.3.1: Completeness framing for negative claims.**  
   Your framing—“not found in the relevant indexed source scope”—is defensible and matches the typical RAG system’s honesty. However, you must also define what constitutes “relevant indexed source scope” for each query class. For example, if a user asks “Does course X have a cert prep signal?” and the cert‑signal block is present in GUIDE but the query was routed to CAT‑TEXT (because of mis‑classification), you must ensure the completeness check is tied to the *correct* source scope.  
   **Settle on a rule:** The completeness check is performed on the evidence bundle after source authority filtering. If the bundle contains no documents from the authoritative source for the requested field, the system must abstain, not make a negative claim. This prevents false negatives caused by retrieval errors.

---

### 3. Most likely high‑impact failure still not fully mitigated

**Silent entity‑scope contamination through mis‑routed NL queries.**  

Despite your hard version isolation and source filters, the classifier for fuzzy queries (step 2) is a single point of failure. If the structured LLM mis‑classifies an NL question (e.g., “Tell me about the networking course”) and outputs a wrong entity (e.g., C179 instead of C172), the rest of the deterministic pipeline will faithfully retrieve and generate an answer for the wrong entity. The user will receive a plausible, well‑cited answer that is completely wrong for their intended course.

**Why it’s still a high‑impact risk:**  
- The classifier is an 8B model, which can be brittle.  
- You have many near‑duplicate course titles (e.g., “Advanced Networking Concepts” vs “Networking Fundamentals”).  
- The failure would pass all your launch gates because the answer is correctly grounded to the retrieved entity—it’s just the wrong entity.

**Mitigation already partially addressed:**  
Your disambiguation step (5.2.5) would catch many cases if the classifier returns multiple candidates. But if the classifier returns a single but wrong candidate, disambiguation won’t fire.  

**Recommendation:**  
Add a **consistency check** after retrieval: compute a similarity score between the user’s original query and the retrieved entity’s canonical name/title. If the score is below a threshold (or if the entity’s name is not a substring match of the query for exact‑identifier cases), route to a confirmation prompt before generating. This creates a lightweight guard against entity‑mismatch failures.

---

### 4. Minimum launch‑gate metrics you would enforce

1. **Silent version merge rate: 0%**  
   This is your top risk. On a test set of 100 queries that explicitly involve the 5 conflicted programs (and a separate set for multi‑variant courses), a human auditor must verify that no answer synthesizes content from two versions without disclosure. Any violation blocks launch.

2. **Claim entailment precision (for generative answers): 98%**  
   For a test set of 200 queries requiring summarization (e.g., NL section‑grounded, explicit compare), a human must trace every factual claim in the answer back to the cited evidence. Claims not entailed are recorded. Threshold: ≤4 failures.

3. **Exact‑lookup zero‑LLM path accuracy: 100%**  
   For 100 exact‑code queries (e.g., “CU for C179”, “title for D554”), the system must return the correct value without invoking any LLM. Errors here are unacceptable and indicate a bug in deterministic routing or canonical objects.

4. **Abstention recall on ambiguous queries: 95%**  
   For a test set of 50 ambiguous queries (e.g., “tell me about the MBA program” when multiple tracks exist, or “competencies for course X” when multiple variants exist and no program context), the system must either (a) abstain with a clarification prompt or (b) present a disambiguation choice. If it attempts to answer, that’s a failure. (Recall = correctly abstained / total ambiguous queries.)

5. **Manual audit protocol:**  
   Use a double‑blind review: two independent auditors evaluate each generated answer against the evidence bundle. Disagreements are resolved by a third senior reviewer. Audit at least 10% of all answers produced during the final validation phase, stratified by query class.

---

### 5. What to defer from v1 even if technically feasible

1. **Semantic reranking (5.2.3).**  
   Your current hybrid weighting (keyword + vector) will be sufficient for v1. Adding a reranker introduces complexity, new failure modes (e.g., reranker biasing toward one source), and makes debugging harder. Defer until you have a production dataset to evaluate its real benefit.

2. **Automated completeness checks for absence claims (beyond “not in evidence bundle”).**  
   You already have a pragmatic framing. Do not attempt to verify that the evidence bundle itself is complete (e.g., by checking if a field might exist in a different section of the catalog). That would require a full catalog schema model and is overkill for v1. Stick to “not found in retrieved evidence” and defer advanced completeness to v2.

3. **General natural language comparison across different programs (e.g., “compare the capstone of MACCT with the capstone of MBAITM”).**  
   This requires complex entity resolution, retrieval across multiple versions/sources, and structured output. Your v1 scope wisely limits explicit comparisons to known version pairs. Keep it that way.

4. **LLM‑based “surface realization” for exact‑lookup answers.**  
   As noted earlier, use templates. Even a simple LLM to rephrase “3 CUs” as “This course carries 3 competency units” is an unnecessary risk. Save generative polish for v2 when you have better safety controls.

---

Overall, v3 is significantly tighter than v2. The remaining open questions are well‑bounded, and your risk model is focused on the right failures. If you lock in the corrections above and settle the three unresolved decisions, you’ll have a solid foundation for implementation.










This v3 update is a significant hardening of the Atlas architecture. Moving to a **deterministic-first** approach with hard retrieval-time partitioning is precisely the right move for an 8B model. At that scale, you can't trust the LLM to act as a librarian; you have to hand it the specific books, already opened to the right page, and tell it not to look at anything else.

The "live-verified" substrate is a major milestone—congrats on getting the local Ollama/Pydantic loop operational. Here is the requested feedback on the remaining friction points.

---

## 1) Top 3 corrections to your current locked plan

1.  **The "Most-Common" Competency Fallback (§5.4 Q1):**
    * **The Risk:** In an academic context, "wording may differ" is often an understatement. If a student is studying for a specific assessment, a "most-common" variant might miss a critical competency required for their version.
    * **Correction:** Do not default to the "most-common" variant. Instead, implement a **"Discovery View."** If program context is missing, return a count and summary: *"There are 3 variations of competencies for C179 across programs. Please specify your program (e.g., BSIT) to see the definitive list, or [Click here] to see all variants side-by-side."*

2.  **Hard Source Filter vs. "Enrichment Failover" (§2.6 & §5.4 Q4):**
    * **The Risk:** Your plan to enforce source filters *before* retrieval is great for version safety but risky for content completeness (the C179 case). If you strictly filter for `CAT-TEXT` and the catalog entry is anemic (293 chars), the LLM will provide a technically "authoritative" but functionally useless answer.
    * **Correction:** Allow a **"Heuristic Enrichment Flag."** If the primary authority (`CAT-TEXT`) falls below a certain character threshold or fails a basic "completeness" check, the retriever should be allowed to pull the `GUIDE` alternate *only* as a labeled "Supplemental Detail" block, rather than a hidden replacement.

3.  **Deterministic Surface Realization for Class A/B:**
    * **The Risk:** If the model is completely bypassed for Class A (exact lookups), the UX can feel jarringly robotic compared to the NL responses of Class C.
    * **Correction:** Use the 8B model as a **"Polite Wrapper."** Feed the deterministic data into a very "cold" (Temperature 0.0) LLM call with a strict template: *"Translate this JSON identity data into a natural single sentence. Do not add facts."* This maintains the "personality" of the assistant without risking the facts.

---

## 2) Top 3 unresolved decisions to settle before freeze

1.  **The Disambiguation UI/UX (§5.2 Q5):**
    * **Decision:** You need a "Clarification Intercept." If the entity resolver returns multiple high-confidence matches (e.g., "Network+ Course" matching three different versions), the system must **pause the pipeline** and present a "Which one did you mean?" selection to the user before generating any citations.

2.  **Dual Version Token Disclosure (§5.4 Q2–3):**
    * **Decision:** For the 5 conflicted programs (like MSHRM), use a **"Data Freshness Header."** > **Note:** This response combines the Program Guide (March 2026) and the Catalog (Nov 2025). Where they differ, the Catalog (Official) is shown first.

3.  **The "Negative Claim" Standard (§5.3 Q1):**
    * **Decision:** Adopt a **"Scope-Bound Negative"** framing. The model should never say "This course has no prerequisites." It must say "I found no prerequisites listed for this course in the [Version] Program Guide." This protects the system from upstream data gaps.

---

## 3) Most likely high-impact failure still not fully mitigated

**"The Citation Ghost" (Hallucinated Entailment)**

An 8B model is excellent at following patterns, but it can still "hallucinate logic." The model might provide a correct citation (`[Source A]`) but then draw an inference that isn't actually in the text (e.g., "Because this is a capstone, you must finish it last," when the text only says it's a capstone).

**Mitigation:** Your post-check (§9, Step 9) needs a specific **Entailment Prompt** that asks a second "cold" instance of the model: *"Does the provided evidence explicitly state [Fact X]? Answer only YES or NO."*

---

## 4) Minimum launch-gate metrics

| Metric | Threshold | Rationale |
| :--- | :--- | :--- |
| **Silent Version Merge Rate** | **0%** | Any mixing of versions without disclosure is a failure of the core "version-aware" promise. |
| **Entity Collision Error** | **<2%** | If the user asks about Course A and gets Course B, trust is instantly lost. |
| **Citation Entailment Precision** | **>98%** | Every claim must be supported by the cited block; citations must not be "decorations." |
| **Abstention Recall** | **>95%** | The system must correctly identify when it *should* stay silent on out-of-scope/ambiguous queries. |

---

## 5) What to defer from v1

* **Multi-Hop Credit Analysis:** Do not try to answer "How many CUs do I have left if I finished X and Y?" This requires cross-object math that 8B models struggle with.
* **Semantic Version Diffing:** If a user asks "What's the difference between the 2025 and 2026 versions?", provide the two `version_diff_card` summaries side-by-side rather than asking the LLM to generate a narrative comparison.
* **Historical Archive Support:** Limit v1 to "Current" and "Immediate Prior" versions. Supporting the full `108` catalog editions will create an unmanageable disambiguation overhead.

**Would you like me to help refine the "Entailment Prompt" for your Step 9 post-check layer to ensure the 8B model isn't over-inferring from the evidence?**