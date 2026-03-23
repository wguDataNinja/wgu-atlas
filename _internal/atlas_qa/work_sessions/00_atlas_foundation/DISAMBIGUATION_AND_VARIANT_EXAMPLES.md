# Disambiguation and Variant Handling Examples

**Purpose:** Make the remaining reviewer concerns concrete. Each example shows the exact situation, why it is difficult, and the intended deterministic behavior. These are the cases that most often produce entity-collision or silent-synthesis failures in practice.

**Version:** 2026-03-23 — created for RFI v4 external review round

**Cross-references:**
- Evidence bundle shapes: `EVIDENCE_BUNDLE_EXAMPLES.md`
- Canonical object fields: `CANONICAL_OBJECT_PROTOTYPE_PACK.md`
- Source authority policy: `BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md`

---

## Part 1: Disambiguation Examples

These are cases where entity resolution does not produce a unique answer and pre-retrieval disambiguation is required.

---

### Disambiguation Example 1 — Abbreviated program name, multiple matches

**User query:** "What courses are in the MBA program?"

**Competing entities:**
- MBAITM: Master of Business Administration, IT Management
- MBAHCM: Master of Business Administration, Healthcare Management
- (possibly additional MBA-prefixed programs if corpus grows)

**Why ambiguity exists:**
"MBA" is a title keyword, not a program code. Multiple programs share the title prefix. No version ambiguity yet — the problem is entity ambiguity upstream of version resolution.

**Expected deterministic behavior:**
1. Pre-router fails to match a program code; sends to entity resolver.
2. Entity resolver finds multiple program_codes matching "MBA" title keyword.
3. Disambiguation gate fires: `resolved_entity = null`, `disambiguation_required = true`.
4. System returns a structured disambiguation response listing candidates. Retrieval is not initiated.
5. Response (deterministic, not model-generated): "Multiple programs match 'MBA'. Which program are you asking about? Options: MBAITM (IT Management), MBAHCM (Healthcare Management)."

**What must NOT happen:**
- Retrieval must not begin while entity is unresolved.
- The system must not pick the "most common" or "most recent" MBA and answer silently.
- The model must not be asked to "pick the most likely one."

---

### Disambiguation Example 2 — Track or specialization collision

**User query:** "What is the capstone for the Accounting master's program?"

**Competing entities:**
- MACCA: Master of Accounting, CPA Track
- MACCF: Master of Accounting, Financial Management Track
- MACCM: Master of Accounting, Management Accounting Track
- MACCT: Master of Accounting, Tax Track

**Why ambiguity exists:**
All four are "Accounting master's programs." Each has its own capstone. Guide is the sole source for capstone data; the capstone may differ across tracks.

**Expected deterministic behavior:**
1. Entity resolver matches "Accounting master's" to 4 program codes in the MACC family.
2. Disambiguation gate fires.
3. Response: "There are 4 Accounting master's programs. Which track are you asking about?" — lists MACCA, MACCF, MACCM, MACCT with full degree titles.
4. After user selects (e.g., MACCA), entity is resolved → proceed to retrieval for capstone section.

**Additional complication:**
All 4 MACC programs have a catalog/guide version mismatch (catalog 3 months newer). After disambiguation, the version-conflict disclosure must also appear.

**What must NOT happen:**
- System must not synthesize a "general MACC capstone description" across all four tracks.
- The LLM must not attempt to pick the most likely track.

---

### Disambiguation Example 3 — Course title collision across programs

**User query:** "What are the competencies for the Advanced Accounting course?"

**Competing entities:**
- Multiple courses may have "Advanced" + "Accounting" in their titles (e.g., D554 Advanced Financial Accounting I, D555 Advanced Financial Accounting II, others in the MACC family)

**Why ambiguity exists:**
Title-keyword matching without a course code produces multiple candidates. Competencies are program-variant (ENRICH), so the right answer depends on both course and program.

**Expected deterministic behavior:**
1. Entity resolver identifies multiple course codes matching "Advanced Accounting."
2. Disambiguation gate fires: returns list of matching courses with full titles and program appearances.
3. Response: "Multiple courses match 'Advanced Accounting.' Which course are you asking about?" — lists candidates.
4. After user specifies (e.g., D554), entity resolved → retrieve competency variants for D554.
5. D554 has `anomaly_flags: ["guide_misrouted_text"]` → competency data is blocked → abstain on competency question for D554.

---

### Disambiguation Example 4 — Version ambiguity without explicit specification

**User query:** "What changed in BSCS?"

**Competing interpretations:**
- "Changed compared to what?" — no from_version specified.
- Could mean: latest vs previous, latest vs any historical version, or just "tell me about BSCS" (no compare intent).

**Why ambiguity exists:**
"Changed" implies comparison, but the from_version is not specified. The system cannot safely select a version pair without user input.

**Expected deterministic behavior:**
1. Pre-router detects comparison language ("changed") → routes toward Class D.
2. Version resolver: `to_version` = 2026_03 (latest, resolvable). `from_version` = unresolved.
3. Disambiguation gate fires on version: system cannot select `from_version` silently.
4. Response: "Which version would you like to compare to 2026-03? Available prior versions: 2025-06, 2025-03, 2024-09 (and others)." — or: "Comparing to the immediately prior version (2025-06). Would you like a different comparison?"
5. If system uses "latest vs immediately prior" as default with disclosure, this is acceptable if the disclosure is explicit.

**Open question (for reviewers):** Is "compare to immediately prior version" a reasonable default with disclosure, or should the system always ask? This is a UX design question that affects the version resolver contract.

---

### Disambiguation Example 5 — Inactive/retired course still in system

**User query:** "Tell me about C392."

**Competing interpretations:**
- C392 may be a retired/inactive course. The canonical_courses.json may still contain it, but it is no longer in the current catalog.

**Why ambiguity exists:**
Not entity ambiguity — C392 is a unique code — but status ambiguity. The course exists in the corpus but may not be "current."

**Expected deterministic behavior:**
1. Entity resolves to C392 (unique code match).
2. `course_card` for C392 has `is_active: false`, `last_catalog_version: "2024_06"`.
3. No disambiguation required, but the answer must disclose the course's retired status.
4. Response: "C392 was last included in the WGU catalog in the 2024-06 edition. It is not present in the current 2026-03 catalog. [Description from last available version follows.]"

**What must NOT happen:**
- System must not answer as if C392 is a current course.
- System must not silently omit the retired status.

---

## Part 2: Multi-Variant Handling Examples

These are cases where the answer depends on which variant of a multi-variant field is selected. The fallback chain is:
1. Program context known → use matching variant
2. No context, single canonical variant → use it
3. No context, multiple variants → (a) most-common variant with explicit deterministic disclosure, or (b) abstain and ask for context

---

### Variant Example 1 — Competency question, program context known

**User query:** "What competencies does D358 cover in the MSHRM program?"

**Program context:** MSHRM (explicit in query)
**Multi-variant status:** D358 has 2 competency variants (BSHR, MSHRM)

**Matching variant behavior:**
- Resolver identifies program context = MSHRM.
- Retrieves MSHRM variant from `course_card.competency_variants`.
- No disclosure needed: exact match.

**Expected answer contract:**
> "In the MSHRM program, D358 (Learning and Development) covers:
> - Evaluates talent development strategy against organizational objectives.
> - Applies adult learning theory to design of executive development programs.
> Source: MSHRM program guide, 2026-01."

**No disclosure or abstention needed.** Program context resolved the variant.

---

### Variant Example 2 — Competency question, no program context, single variant

**User query:** "What are the competencies for C168?"

**Program context:** absent
**Multi-variant status:** C168 has 1 competency variant (single source program)

**Fallback behavior (single variant):**
- No program context, but only 1 variant exists.
- Use the single variant directly.
- No multi-variant disclosure needed.

**Expected answer contract:**
> "C168 (Discrete Mathematics I) covers:
> - Applies set theory and logic operations to computational problems.
> - Constructs formal proofs using propositional and predicate logic.
> Source: program guide, 2026-03."

**Simple case.** No ambiguity.

---

### Variant Example 3 — Competency question, no program context, multiple variants (most-common variant path)

**User query:** "What are the competencies for D358?"

**Program context:** absent
**Multi-variant status:** D358 has 2 competency variants (BSHR: most common by source program count, MSHRM)

**Fallback behavior (multiple variants, option A: most-common with disclosure):**
- No program context.
- BSHR variant selected as most-common (BSHR is a larger program family).
- Disclosure string is deterministic, pre-composed, required in answer.

**Expected answer contract:**
> "D358 (Learning and Development) competencies [from most common source program, BSHR]:
> - Analyzes training needs using established assessment frameworks.
> - Designs instructional content aligned to organizational competency models.
>
> Note: This course appears in 2 programs (BSHR, MSHRM). Competency wording may differ. Specify your program (e.g., 'in the MSHRM program') for program-specific competencies."
> Source: BSHR program guide, 2025-09.

**Open question:** Is this the right default behavior? See RFI §5.4 Q1. The risk is that a student in MSHRM reads BSHR competencies and believes them to be authoritative.

---

### Variant Example 4 — Competency question, no program context, multiple variants (abstain path)

**Same query as Example 3**, but under a stricter abstention policy:

**Fallback behavior (multiple variants, option B: abstain):**
- No program context.
- Multiple variants exist with potentially substantive differences.
- System abstains rather than silently presenting one variant as default.

**Expected answer contract:**
> "D358 (Learning and Development) has competency listings that vary by program (2 variants found: BSHR, MSHRM). To show the correct competency list, please specify your program. Example: 'What are the competencies for D358 in the BSHR program?'"

**No competency data is surfaced until program context is provided.**

**Tradeoff:** This is the safer behavior but more friction for users in common programs. The right answer depends on how substantively different the variants are — something the human review of flagged courses should inform.

---

### Variant Example 5 — Guide description variant, program context known

**User query:** "How does MSHRM describe D358?"

**Program context:** MSHRM (explicit)
**Multi-variant status:** D358 has 2 guide description variants

**Note:** This is a guide-description question, not a catalog-description question. Catalog is still the default display source for course descriptions, but this user is explicitly asking about the MSHRM guide's description.

**Matching variant behavior:**
- Query intent is guide-description, program-scoped.
- Source scope: ENRICH (guide description alternates).
- Resolver selects MSHRM guide description variant.

**Expected answer contract:**
> "In the MSHRM program guide (2026-01), D358 (Learning and Development) is described as:
> 'Learning and Development examines strategic human capital development practices...'
>
> Note: This is the program guide description, scoped to MSHRM. The WGU catalog (2026-03) uses different wording as the default course description."

**Key behavior:** The QA system does not merge the catalog description and guide description. Both are cited with their sources. The guide description is surfaced only because the user explicitly asked for the MSHRM guide's version.

---

## Part 3: Interaction between disambiguation and variant handling

Some queries require both steps in sequence.

### Combined Example — ambiguous entity + multi-variant

**User query:** "What competencies does the Advanced Accounting course teach?"

**Step 1 — Disambiguation:**
- Multiple course codes match "Advanced Accounting."
- Disambiguation fires: list candidates, ask user to specify.
- Retrieval not initiated.

**Step 2 — After user specifies D554:**
- Entity resolved: D554.
- D554 has `anomaly_flags: ["guide_misrouted_text"]`.
- Competency data is blocked for D554.
- Result: abstain on competency question.

**Step 3 — After user specifies a different course (e.g., D555):**
- Entity resolved: D555.
- D555 has 1 competency variant (single source program).
- Use variant directly. No program context needed.

**Lesson for implementation:** Disambiguation and variant selection are sequential gates, not parallel. The variant selection logic only runs after entity is uniquely resolved.

---

## Summary table

| Example | Context present | Variant count | Expected behavior |
|---|---|---|---|
| V1 — D358, MSHRM context | Yes | 2 | Use matching variant; no disclosure |
| V2 — C168, no context | No | 1 | Use single variant; no disclosure |
| V3 — D358, no context, option A | No | 2 | Most-common variant + deterministic disclosure |
| V4 — D358, no context, option B | No | 2 | Abstain; ask for program context |
| V5 — D358 guide description, MSHRM | Yes (guide-desc query) | 2 | MSHRM guide variant; cite both sources |

| Disambiguation | Why | Expected behavior |
|---|---|---|
| D1 — "MBA" | Title keyword, multiple codes | List candidates, require selection |
| D2 — "Accounting master's" | Track family collision | List 4 MACC tracks, require selection |
| D3 — "Advanced Accounting" course | Title keyword, multiple codes | List candidates; may also hit anomaly after selection |
| D4 — "What changed in BSCS" | No from_version | Clarify version pair before retrieval |
| D5 — C392 retired | Status ambiguity | Resolve uniquely; disclose retired status |

---

## Open questions for reviewers

1. **V3 vs V4 (most-common vs abstain):** Which is the right v1 default for multi-variant competency questions when program context is absent? The design is currently undecided on this. See RFI §5.4 Q1 and `EVIDENCE_BUNDLE_EXAMPLES.md` Example 4.

2. **D1/D2 (disambiguation card):** Should the system maintain a first-class `disambiguation_card` object type as part of the canonical object set, or is this an output structure handled purely by the control layer? Reviewer opinion welcome on whether this warrants a named object type.

3. **D4 (version ambiguity):** "Compare to immediately prior version" as a default with explicit disclosure — is this safe for v1, or should the system always require an explicit from_version?

4. **V5 (guide description, explicit program context):** Is the answer contract shown correct — surfacing the guide variant with explicit source labels, while noting catalog uses different wording? Or should the system abstain on guide-description questions unless the user explicitly asks for "the guide's description"?
