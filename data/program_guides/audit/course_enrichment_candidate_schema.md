# Course Enrichment Candidate Schema (Conservative)

Date: 2026-03-21

Status: candidate-only policy/schema draft. Not a shipping schema.

## What now looks realistically supportable

Given anchorability and signal review, a conservative course-level payload should include only uniquely anchored course occurrences and high-confidence fields:
1. Canonical anchor (`course_code`) with explicit anchor provenance.
2. Guide-derived description candidates.
3. Guide-derived competency bullets.
4. AoS role/group context per program appearance.
5. Program appearance context (program code, family, source surface).

## Candidate payload shape

```json
{
  "course_code": "D481",
  "anchor_provenance": {
    "anchor_class": "exact_current_unique",
    "source_program_code": "MSCSIA",
    "source_surface": "aos",
    "source_title": "Security Foundations"
  },
  "guide_description_candidates": ["..."],
  "guide_competency_bullets": ["..."],
  "aos_role_context": [
    {"program_code": "MSCSIA", "group": "Security"}
  ],
  "program_appearance_context": [
    {"program_code": "MSCSIA", "family": "cs_grad"}
  ]
}
```

## Field decisions

| Field | Recommendation | Why |
|---|---|---|
| Canonical course anchor | Publish candidate | Required for safe attachment |
| Guide descriptions | Publish candidate | High-value, high-coverage |
| Competency bullets | Publish candidate | High-value, high-coverage |
| AoS role/group context | Publish candidate | Strong degree-role context |
| Program appearance context | Publish candidate | Useful attribution and provenance |
| SP sequence context | Publish later/optional | Degree-context-heavy, not canonical course identity |
| Certification relationships | Internal or gated publish-later | Valuable but noisy without tightening |
| Prerequisite relationships | Internal-only now | Fragmentary and not publish-safe |

## Gating rules

1. Emit course payload only for unique strict anchor classes.
2. Exclude ambiguous/unmapped/non-course records from public payload.
3. Respect guide caveat policy (partial-use, SP limitations).
4. Do not emit raw cert/prereq strings publicly.

## What must happen before implementation

1. Deterministic disambiguation policy for ambiguous titles.
2. Unmapped-title triage and alias curation.
3. Cert signal hardening + claim policy.
4. Prereq extractor redesign if public dependency modeling is desired.