# Ambiguous Course Resolution: LLM Packet Schema

**Prepared:** 2026-03-21
**Scope:** Context packet and adjudication output schema for the ~171-row LLM residual

---

## Overview

Each packet corresponds to one ambiguous row that no deterministic signal resolved. It supplies all locally available context for LLM adjudication. The packet is designed to be self-contained: the LLM needs no external lookups.

Packets are grouped by program family in the input file. Within a group, resolved neighbors from the same guide appear as context, giving the LLM a reference frame for the typical code pattern in that guide.

---

## Input Packet Schema (per row)

```json
{
  "packet_id": "BAELED__Elementary_Social_Studies_Methods__aos",
  "program_context": {
    "program_code": "BAELED",
    "program_code_effective": "BAELED",
    "family": "education_ba",
    "degree_title": "Bachelor of Arts, Elementary Education",
    "degree_level": "undergraduate",
    "guide_version": "202603",
    "guide_pub_date": "12/11/2025"
  },
  "row_context": {
    "surface": "aos",
    "guide_title_raw": "Elementary Social Studies Methods",
    "guide_title_normalized": "elementary social studies methods",
    "aos_group": "Elementary Education",
    "sp_term": null,
    "sp_cus": null
  },
  "parsed_description": "Elementary Social Studies Methods prepares WGU candidates...",
  "aos_group_neighbors": [
    {
      "guide_title_raw": "Elementary Literacy Curriculum",
      "resolved_code": "D668",
      "anchor_class": "deterministic_resolved_degree_title_overlap"
    },
    {
      "guide_title_raw": "Early Literacy Methods",
      "resolved_code": "D669",
      "anchor_class": "deterministic_resolved_degree_title_overlap"
    }
  ],
  "candidates": [
    {
      "course_code": "C104",
      "canonical_title_current": "Elementary Social Studies Methods",
      "canonical_cus": "3",
      "current_college": "School of Education",
      "active_current": true,
      "current_programs": "",
      "historical_programs": "",
      "current_program_count": 0,
      "stability_class": "stable",
      "title_variant_class": "none",
      "first_seen_edition": "2017-01",
      "last_seen_edition": "2026-03"
    },
    {
      "course_code": "D674",
      "canonical_title_current": "Elementary Social Studies Methods",
      "canonical_cus": "3",
      "current_college": "School of Education",
      "active_current": true,
      "current_programs": "Bachelor of Arts, Educational Studies in Elementary Education; Bachelor of Arts, Educational Studies in Special Education",
      "historical_programs": "",
      "current_program_count": 2,
      "stability_class": "stable",
      "title_variant_class": "none",
      "first_seen_edition": "2022-01",
      "last_seen_edition": "2026-03"
    },
    {
      "course_code": "D681",
      "canonical_title_current": "Elementary Social Studies Methods",
      "canonical_cus": "2",
      "current_college": "School of Education",
      "active_current": true,
      "current_programs": "Master of Arts in Teaching, Elementary Education",
      "historical_programs": "",
      "current_program_count": 1,
      "stability_class": "stable",
      "title_variant_class": "none",
      "first_seen_edition": "2022-01",
      "last_seen_edition": "2026-03"
    }
  ],
  "previously_resolved_in_guide": [
    {
      "guide_title_raw": "The Professional Educator",
      "resolved_code": "D663",
      "anchor_class": "exact_current_unique"
    }
  ],
  "signals_checked_and_failed": [
    "cu_match",
    "one_active",
    "a_suffix_cert",
    "degree_level",
    "degree_title_overlap"
  ]
}
```

### Field Definitions

#### `packet_id`
Unique identifier: `{program_code}__{guide_title_normalized}__{surface}`. Use `__` as separator.

#### `program_context`
Everything known about the guide being processed. Include `guide_version` and `guide_pub_date` to allow the LLM to reason about temporal currency of course codes.

#### `row_context`
The specific row being adjudicated. Include `sp_cus` even when it doesn't uniquely resolve (it may narrow the field), and `sp_term` when present.

#### `parsed_description`
The description text from the parsed guide AoS entry (`areas_of_study[*].courses[*].description`). Include even if empty. If the guide description explicitly mentions CU count, credit requirements, or degree-level prerequisites, that is diagnostic. Omit for SP-only rows where the title does not appear in the AoS section.

#### `aos_group_neighbors`
The 3–5 surrounding courses in the same AoS group that have already been resolved (by any anchor class). Provides reference: if all neighboring resolved courses are D-prefix codes with similar edition ranges, the ambiguous course likely follows the same pattern.

#### `candidates`
All canonical candidate codes with full structured metadata. Include:
- `first_seen_edition` and `last_seen_edition` — key for legacy vs. current code inference
- `current_program_count` — explicit zero vs. nonzero is a useful signal
- `stability_class` — perpetual/stable/sparse gives recency signal

Do NOT include:
- Cert/prereq mentions (out of scope for this pass)
- Raw observed_titles field (redundant given title is same for all candidates)

#### `previously_resolved_in_guide`
Up to 10 already-resolved rows from anywhere in the same guide (not just same group). Prioritize rows where the resolved code is in a similar family (same D-prefix cohort, same CU range). This gives the LLM a "house style" for this guide.

#### `signals_checked_and_failed`
Complete list of deterministic signals that were checked and did not resolve this row. Prevents the LLM from re-discovering a signal that was already checked and failed. For example, if `degree_level` is listed here, the LLM knows that degree-level inference could not distinguish the candidates.

---

## Output Schema (per adjudication)

```json
{
  "packet_id": "BAELED__Elementary_Social_Studies_Methods__aos",
  "selected_code": "D674",
  "confidence": "high",
  "alternative_possible": false,
  "rationale": "D674 is the active 3CU variant of this course currently used in BA-level Educational Studies programs — the closest family to BAELED. C104 has no current_programs entries and a 2017 first_seen_edition, indicating a legacy code superseded by D674 in the same cohort transition. The neighboring resolved courses in the Elementary Education AoS group all resolve to D-prefix codes from the same 2022+ era. D681 (2CU, MAT) is for graduate programs and does not apply here.",
  "signal_used": "legacy_vs_active_code_pattern + aos_group_neighbor_cohort",
  "unresolvable_reason": null,
  "review_flag": false
}
```

### Field Definitions

#### `selected_code`
The canonical course code selected. `null` if unresolvable.

#### `confidence`
Must be one of: `"high"`, `"medium"`, `"low"`, `"unresolvable"`.

- `"high"`: Clear single answer; confident a reader with full WGU context would agree.
- `"medium"`: Likely correct, but one or more candidates cannot be fully ruled out.
- `"low"`: Weak evidence; real risk of being wrong; should not be auto-accepted.
- `"unresolvable"`: Candidates are genuinely indistinguishable from available evidence. Do not select.

Do not use `"high"` unless at least one piece of named, specific evidence points to the selected code — not just "this seems more likely."

#### `alternative_possible`
`true` if, with different interpretation of the same evidence, the alternative candidate(s) could plausibly be correct. Use with `"high"` when the evidence is strong but not airtight (e.g., the program name match is close but not exact). Triggers spot-check review even for high-confidence decisions.

#### `rationale`
Concise English explanation: which specific evidence drove the decision, why alternatives were excluded. Should be 2–5 sentences. Must name the specific candidates considered and cite specific fields (e.g., `current_programs`, `first_seen_edition`, `aos_group_neighbors`).

#### `signal_used`
Short label(s) of the evidence type used:
- `"legacy_vs_active_code_pattern"` — old prefix code (C1xx) vs newer code
- `"program_name_fuzzy_match"` — candidate programs text closely matches guide program name
- `"college_mismatch"` — candidate's college doesn't match guide's typical college
- `"aos_group_neighbor_cohort"` — neighbors all resolve to same code generation
- `"cu_context_from_description"` — description implies a CU count matching one candidate
- `"edition_range_alignment"` — candidate's edition range matches guide pub date
- `"unresolvable_empty_programs_tie"` — multiple empty-programs candidates, same CU, no differentiator

#### `unresolvable_reason`
If `confidence = "unresolvable"`: brief description of why no selection is possible. For example: `"Two candidates (C282, C362) are structurally identical — same CU, same college, same empty programs, overlapping edition ranges. No available evidence distinguishes them."`

#### `review_flag`
`true` if this adjudication should be manually reviewed regardless of confidence level. Set when the context reveals something unexpected (e.g., a candidate's programs contradict expected family, a description mentions a different degree level than the guide).

---

## Acceptance Policy

| Confidence | `alternative_possible` | Action |
|------------|------------------------|--------|
| `high` | `false` | **Auto-accept** |
| `high` | `true` | **Spot-check** (review 1 in 3) |
| `medium` | any | **Human review** before accept |
| `low` | any | **Reject** — leave as `ambiguous_residual` |
| `unresolvable` | n/a | **Leave unresolved** — log the reason |

Auto-accepted rows are updated in bridge files with `anchor_class = "llm_resolved_high"`.
Spot-checked rows that pass review: `anchor_class = "llm_resolved_high_verified"`.
Medium-accepted rows that pass review: `anchor_class = "llm_resolved_medium_reviewed"`.

---

## Packet Batching Strategy

Group the 171 packets by `family` before processing. Suggested order:

1. `education_ba` — largest group; resolving a few titles unlocks the pattern for many rows
2. `education_mat` / `education_grad` — share many titles with education_ba
3. `cs_ug` / `cs_grad` — IT/technology group
4. `standard_bs` / `business_*` — business programs
5. Remaining small families

Within each group, process AoS rows before SP rows (AoS rows have more context via parsed description). Process 2-candidate rows before 3+ candidate rows.

**Within a single LLM session, the first few adjudications in a family set the pattern.** Once the LLM correctly resolves `D890` for Calculus I in BAESMES, it should apply the same D-prefix cohort logic to Calculus II, Linear Algebra, etc. in the same guide.

---

## Expected Yield from LLM Stage

Based on the nature of the 171 residual rows:

| Outcome | Estimated count |
|---------|-----------------|
| `high` confidence, `alternative_possible = false` | 70–90 |
| `high` confidence, `alternative_possible = true` | 15–25 |
| `medium` confidence | 25–40 |
| `low` confidence | 10–20 |
| `unresolvable` | 15–30 |
| **Net auto-accepted** | **70–90** |
| **Net accepted after review** | **95–130** |
