# Course Signal Quality Review

Date: 2026-03-21

## Scope

- Included scope: all 115 parsed program guides.
- Signals reviewed: AoS parsed fields `certification_prep_mentions` and `prerequisite_mentions`.
- Classification: conservative, evidence-based classes only.

## Certification Signal Findings

- Total cert mention instances: `139` across `112` courses.
- Courses with non-noise cert signal: `58`.
| Class | Count | Percent |
|---|---:|---:|
| false_positive_parser_noise | 52 | 37.41% |
| explicit_prep_claim | 53 | 38.13% |
| explicit_alignment_or_associated_cert | 16 | 11.51% |
| unclear | 17 | 12.23% |
| adjacent_mention_only | 1 | 0.72% |

Examples:
- `explicit_prep_claim`: `Network and Security - Applications` (CompTIA Security+ prep wording in description).
- `explicit_alignment_or_associated_cert`: Praxis tokenized curriculum mentions in education guides.
- `adjacent_mention_only`: `Auditing` -> `CPA Code` (professional standard mention, not exam-prep mapping).
- `false_positive_parser_noise`: `aws and`, `aws in`, `aws to` fragments.

Certification conclusion: `promising but needs policy/extractor tightening`.
- Publish-safe now only under strict gating (explicit prep/alignment claims, noise filtered, anchor known).
- Do not auto-publish raw cert mention strings.

## Prerequisite Signal Findings

- Total prereq mention instances: `264` across `187` courses.
- Courses with explicit/internal dependency signal: `104`.
| Class | Count | Percent |
|---|---:|---:|
| parser_artifact_or_weak | 56 | 21.21% |
| internal_only_dependency_bundle | 19 | 7.2% |
| explicit_prerequisite_dependency | 162 | 61.36% |
| sequencing_or_context_clue | 27 | 10.23% |

Examples:
- `explicit_prerequisite_dependency`: `Network and Security - Foundations` -> prerequisite signal for `Networks`.
- `internal_only_dependency_bundle`: BSPRN/MSN bundle dependencies (`Courses: All ... previous terms`).
- `sequencing_or_context_clue`: references like `Data Management - Foundations` without stable dependency semantics.
- `parser_artifact_or_weak`: fragments such as `for this course` and no-prereq residual strings.

Prerequisite conclusion: `internal-only for now`.
- Signal has value for diagnostics and potential future extraction work.
- Not publish-safe as a student-facing dependency field in current parsed form.

## Overall signal safety decision

- Certification: `promising but needs policy/extractor tightening`.
- Prerequisites: `internal-only for now`.