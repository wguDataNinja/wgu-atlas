# Ambiguous Course Resolution Strategy

**Prepared:** 2026-03-21
**Based on:** roster bridge (115 guides), course enrichment candidates extraction, canonical_courses.csv
**Scope:** Assessment of hybrid LLM-adjudication approach for the ambiguous mapping bucket

---

## Direct Answer

**The idea is fundamentally sound — but the proposed workflow is missing its most important first stage.**

The proposal as described would send all 1,599 ambiguous rows to LLM adjudication. That is the wrong boundary. After rigorous analysis of the ambiguous bucket, **1,231 rows (77%) already have at least one clean deterministic signal** that can resolve them without LLM reasoning. When multiple signals fire on the same row, they agree 100% of the time (378 multi-signal rows; 0 conflicts). These should never reach the LLM.

The correct workflow is:

1. **Stage A — Enhanced Deterministic Resolver** (new script, next session): resolve the 1,231 already-signaled rows plus ~197 more reachable via a 5th deterministic signal, yielding ~1,428 resolved rows from the ambiguous bucket by rule alone.
2. **Stage B — LLM Adjudication** (tightly bounded): apply LLM reasoning only to the true residual of approximately **171 rows** that no deterministic rule can touch.

This is not a minor optimization. Using LLM on signal-bearing rows wastes inference, introduces unnecessary randomness into rows where the answer is already clear, and makes the pipeline harder to audit. Save LLM work for what only LLM can do.

---

## Bucket Characterization

| Metric | Count |
|--------|-------|
| Total ambiguous rows | 1,599 |
| — AoS surface | 819 |
| — SP surface | 780 |
| Distinct ambiguous titles | 214 |
| Candidate set size 2 | 1,102 (69%) |
| Candidate set size 3 | 319 (20%) |
| Candidate set size 4–6 | 178 (11%) |

The 214 distinct titles driving 1,599 rows is structurally important: this is not 1,599 independent problems. Many are the same title appearing across 10–28 guides simultaneously. Once one instance of a title is resolved, the same logic applies to all other instances of that title in similar program contexts. **The effective decision space is much smaller than the raw row count.**

Top recurring ambiguous titles:

| Title | Guides | Candidates |
|-------|--------|------------|
| Integrated Physical Sciences | 28 | 2 |
| Secondary Literacy Methods and Interventions | 22 | 2 |
| General Secondary Methods | 17 | 2 |
| Secondary Disciplinary Literacy | 17 | 5 |
| Project Management | 16 | 3 |
| Data Management - Foundations | 14 | 3 |

---

## Deterministic Signal Inventory

Five clean deterministic signals are available. All five are mutually consistent on every row where more than one fires.

### Signal 1: CU Match (SP rows only)
**Definition:** SP row has an explicit CU value (`sp_cus`); exactly one candidate matches that CU value in `canonical_courses`.
**Yield:** 289 rows resolved
**Reliability:** Very high. SP CU values are authoritative; they come from the guide's own Standard Path table.

### Signal 2: One Active Candidate
**Definition:** Exactly one candidate has `active_current = True`.
**Yield:** 595 rows resolved (423 single-signal + overlap with others)
**Reliability:** High. An inactive course should not be the correct mapping for an active guide. The edge case (a guide citing a historical course intentionally) is rare and low-impact.

### Signal 3: A-Suffix Certificate Context
**Definition:** One or more candidates carry an `A` suffix AND have `contexts_seen = cert`. The guide is a degree program (not a certificate family). Therefore the non-cert candidate wins.
**Yield:** 88 rows resolved (mostly Business degree programs)
**Reliability:** Very high. `C715A` is the certificate variant of `C715`; they are structurally separate. A degree-program guide refers to the base course.

### Signal 4: Degree-Level Exclusion
**Definition:** The guide is undergraduate or graduate. Candidates whose `current_programs + historical_programs` contain only graduate-level keywords (master, MBA, MAT) but no undergraduate-level keywords are excluded. If after exclusion exactly one candidate remains, it wins.
**Yield:** 291 rows resolved
**Reliability:** Moderate-high. Keyword matching on program titles is imperfect but has clear face validity. Remaining uncertainty is whether a course appears in both levels.

### Signal 5: Degree-Title Overlap (NEW — not yet implemented)
**Definition:** Exactly one candidate has `current_programs + historical_programs` containing the guide's `degree_title_guide` as a substring.
**Yield:** 197 additional rows (beyond those already resolved by signals 1–4)
**Reliability:** High. A candidate explicitly listed under the exact degree title being processed is the direct match. This is a stronger claim than degree-level inference.

### Signal Summary

| Signal | Applicable to | Rows Resolved |
|--------|--------------|---------------|
| 1: CU match | SP only | 289 |
| 2: One active | AoS + SP | 595 |
| 3: A-suffix cert | AoS + SP | 88 |
| 4: Degree-level exclusion | AoS + SP | 291 |
| 5: Degree-title overlap (new) | AoS + SP | 197 |
| **Total (union, no double-count)** | | **~1,428** |
| Remaining true residual | | **~171** |

Multi-signal agreement check: **378 rows had 2+ signals fire. Signal conflicts: 0.** This is a strong quality indicator.

---

## True LLM Residual: 171 Rows

### Characteristics

- Candidate sets: 2 (30 rows), 3 (65), 4 (40), 5 (32), 6 (4)
- Program level: undergraduate (143), graduate (28)
- Surface: AoS (101), SP (70)
- Concentrated in: education programs (elementary/secondary variants), mathematics education, IT/technology cross-overs

### Why Deterministic Signals Fail Here

The defining characteristic of these 171 rows is the **empty-programs ghost problem**: one or more candidates have `current_programs = ""` and `historical_programs = ""` — meaning canonical_courses has no program attachment data for them. These are real course codes (not deleted), but their provenance in the canonical data is incomplete. Because they have no program-level signal, degree-level and degree-title signals cannot exclude them.

The correct candidate is typically visible in the form of one other candidate that clearly has appropriate program-level data — but it cannot be selected deterministically because the empty-programs code is same-CU and same-college, making it indistinguishable by rule.

**Representative examples:**

`Elementary Social Studies Methods` in BAELED (BA, Elementary Education):
- C104: 3CU, School of Education, no programs (legacy code)
- D674: 3CU, School of Education, in "Bachelor of Arts, Educational Studies in Elementary Education" programs
- D681: 2CU, School of Education, in MAT programs

Degree-level signal eliminates D681. C104 vs D674 remains: both 3CU, both same college, one empty. Correct answer is D674 — but only inferable from knowledge that D674 is the active replacement for C104 in similar BA elementary education programs, which is not present in the structured data.

`Calculus I` in BAESMES (BA, Educational Studies in Secondary Mathematics Education):
- C282: 4CU, School of Education, no programs
- C362: 4CU, School of Education, no programs
- C363: 2CU, School of Education, MAT Middle Grades (excluded by degree-level)
- C958: 4CU, School of Technology, CS programs (wrong college)
- D890: 3CU, School of Education, in BA Educational Studies Secondary Mathematics
- QJT2: 2CU, School of Education, MAT Middle Grades (excluded)

After exclusions: C282, C362, C958, D890 remain. D890 is the right answer (it's literally in the matching program). C958 is wrong (CS college). C282/C362 are empty. The LLM should see D890 as the clear winner by college alignment + program text — but the rule-based approach can't cleanly eliminate C282 and C362 while keeping D890.

### What LLM Can See That Rules Cannot

For these 171 rows, the correct resolution requires integrating:

1. **College alignment** — C958 (School of Technology) for a Mathematics Education guide is clearly wrong.
2. **Program-name fuzzy matching** — D674's "Educational Studies in Elementary Education" is close enough to BAELED's "Elementary Education" to prefer it over an empty-programs code.
3. **Historical code recognition** — C104, C282, C362, and similar low-letter-prefix codes tend to be legacy codes superseded by newer D-prefix codes for the same course. This pattern is inferable from the data distribution.
4. **Parsed guide description context** — the description in the guide's parsed AoS entry may reference specific program requirements, student teaching placement criteria, or CU counts that identify the version.
5. **Neighbor resolution context** — if the surrounding courses in the same AoS group all resolve to D-prefix codes in a certain program family, the ambiguous one probably does too.

---

## Why the Hybrid Approach is the Right Method for the Residual

**This is not a problem deterministic rules will solve incrementally.** The empty-programs ghost codes require knowledge that is not present in the structured fields: (1) the historical succession relationship between old-prefix and new-prefix course codes, (2) program-name fuzzy equivalence across similar but non-identical degree titles, (3) college-as-context signal. These are soft reasoning tasks, not structured field matching.

LLM adjudication is appropriate here because:
- The decision context is small (5–10 candidates, 3–5 paragraphs of context)
- The correct answer is often visible to an informed reader given the full packet
- The task is classification, not generation — risk of confabulation is bounded
- Wrong answers can be caught by human review of the medium-confidence tier
- 171 rows is a tractable review volume regardless of outcome

**Risk of NOT using LLM:** These 171 rows remain permanently unresolved, representing approximately 171 course occurrences missing from the enrichment candidates output. For the education programs especially (the dominant family in the residual), this is a meaningful gap in the eventual course page enrichment.

---

## Failure Modes and Risks

### Risk 1: LLM Overconfidence on Genuinely Indistinguishable Cases
Some candidates are structurally identical by all available signals: same CU, same college, both empty programs, same historical era. For example, two 4CU education codes from the same cohort with no program attachment. The LLM will produce an answer regardless of evidence quality. **Mitigation:** Require `confidence = high` for auto-accept; flag medium-confidence answers for human review; treat `unresolvable` as a valid and expected output.

### Risk 2: Ghost Code Ambiguity Not Resolvable From Context
Some empty-programs codes exist because the course was only ever in certificate programs or pilot programs not captured in program_history. The guide may genuinely intend either code. **Mitigation:** If the LLM outputs `unresolvable`, log it and leave as ambiguous rather than forcing a selection.

### Risk 3: AoS Rows Have Less Context Than SP Rows
SP rows carry an explicit CU value and a term placement, both of which are useful signals. AoS rows carry only a title and group name. For the 101 AoS residual rows, the context packet must supply the parsed guide description to compensate. If the description does not distinguish versions, confidence will be lower. **Mitigation:** Always include parsed description in AoS packets; accept lower yield from AoS rows.

### Risk 4: Same-Title Courses Genuinely Differ Only by Cohort Year
Some WGU courses are "version replacements" — D717 replaced D523 for the same course in the same program. A guide from a certain version year may intend the older code. Program guide version metadata (`guide_pub_date`) provides a partial signal. **Mitigation:** Include guide version and publication date in every context packet; instruct LLM to prefer the active current code unless version evidence points to the older one.

### Risk 5: Deterministic Resolutions Propagated to LLM Stage
If Stage A deterministic resolver has bugs, wrong resolutions cascade into the enrichment output. **Mitigation:** Validate Stage A resolutions by checking that resolved codes appear in the right program families; spot-check a sample before running enrichment.

---

## Recommended Workflow

### Stage A: Enhanced Deterministic Resolver (next session, top priority)

Build `scripts/program_guides/resolve_ambiguous_deterministic.py`.

Input: bridge guide files (115 × `{program_code}.json`)
Output: `data/program_guides/bridge/resolved/{program_code}.json` (or updated bridge guides in place) + `data/program_guides/bridge/resolution_log_deterministic.json`

Logic:
1. For each ambiguous row, apply signals 1–5 in order (they are independent and non-conflicting).
2. If any signal(s) resolve to exactly one candidate: mark `anchor_class = "deterministic_resolved_{signal_name}"`, record `resolved_code`, record `resolution_signals`.
3. If multiple signals fire and agree: record all signals; take the agreed-upon code.
4. If multiple signals fire and disagree: flag as `resolution_conflict` (this case does not currently occur but should be checked).
5. If no signal resolves: mark `anchor_class = "ambiguous_residual"`, forward to Stage B.

Expected output: ~1,428 rows newly resolved; ~171 rows forwarded as `ambiguous_residual`.

### Stage B: LLM Adjudication Packet Builder (same session as Stage A, or next)

Build `scripts/program_guides/build_ambiguous_resolution_packets.py`.

For each `ambiguous_residual` row: construct a context packet (see packet schema section below) and write to `data/program_guides/bridge/llm_packets/packets.json`.

### Stage C: LLM Adjudication Runner (can be a targeted Claude Code session)

For each packet: run LLM inference, collect structured adjudication output (see output schema below). Write to `data/program_guides/bridge/llm_packets/adjudication_results.json`.

This can be done interactively in a single Claude Code session, processing all 171 packets in one batch or in domain-grouped batches.

### Stage D: Merge and Validate

Build `scripts/program_guides/merge_resolved_ambiguous.py`.

Accept resolutions with `confidence = high` automatically (unless `alternative_possible = true`, which drops to manual review).
Flag `confidence = medium` for spot-check.
Keep `confidence = low` and `unresolvable` as permanently unresolved.
Update bridge guide files with new anchor_class values.

### Stage E: Rerun Enrichment Extraction

Rerun `build_course_enrichment_candidates.py` against the updated bridge.
Expected: course count grows from 501 to roughly 600–650. AoS mention count grows from 1,499 to roughly 1,800–1,900.

---

## Expected Yield

| Stage | Rows Resolved | Cumulative |
|-------|--------------|-----------|
| Current unique (baseline) | 2,735 | 54% of total rows |
| Stage A deterministic resolver | +1,428 | +28 ppt → ~82% |
| Stage C LLM (high confidence) | +85–105 | ~84–85% |
| Stage C LLM (medium, reviewed) | +30–50 | ~86–87% |
| Permanently unresolved | ~20–40 | — |

**Conservative total recovery from ambiguous bucket: ~85% (1,350/1,599 rows).** The 15% remainder (≈250 rows) will contain the structurally indistinguishable ghost-code cases where no evidence distinguishes candidates; these should stay unresolved.

---

## What Should Remain Deterministic

The following must never be delegated to LLM:

- **Any row with `anchor_class` not `ambiguous_*` or `unmapped`** — already correctly classified.
- **Unmapped rows** — these have no candidates at all; resolution requires adding new canonical-course entries, which is a different problem.
- **Signal 1 (CU match) rows** — exact numeric match; always deterministic.
- **Signal 2 (one active) rows** — binary active/inactive; always deterministic.
- **Signal 3 (A-suffix cert) rows** — structural code pattern + context; always deterministic.
- **Multi-signal rows where signals agree** — stronger evidence than any single LLM call.

Do not use LLM to "double-check" deterministic resolutions. Doing so would introduce noise into confident decisions.

---

## Recommended Next Session

**Session 26: Build the Enhanced Deterministic Resolver**

1. Implement `resolve_ambiguous_deterministic.py` with all 5 signals.
2. Output updated bridge guide files with resolved anchor classes and resolution_log.
3. Verify: ~1,428 rows resolved; ~171 forwarded as `ambiguous_residual`.
4. Build `build_ambiguous_resolution_packets.py` to package the 171 residual rows into structured LLM context packets.
5. Spot-check 10–20 resolved rows manually to validate signal accuracy.
6. Commit all artifacts.

If time permits in the same session:
- Run the 171 packets through LLM adjudication interactively.
- Write `merge_resolved_ambiguous.py` to fold accepted resolutions back into bridge.

Do not rerun enrichment extraction until both deterministic and LLM stages are complete.
