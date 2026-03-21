# Course Anchorability Matrix

Date: 2026-03-21

## Scope

- Included scope: all 115 parsed program guides in `data/program_guides/parsed/`.
- Surfaces analyzed: AoS course titles (primary) and SP row titles for usable/partial SP guides (secondary).
- Method: strict matching to `data/canonical_courses.csv` using exact current-title, exact observed-variant, normalization-only exact, ambiguous, unmapped, and non-course/noise classes. No fuzzy matching.

## AoS Anchorability Results

| Class | Count | Percent |
|---|---:|---:|
| exact_current_unique | 1307 | 50.4% |
| exact_observed_variant_unique | 192 | 7.4% |
| normalization_unique | 0 | 0.0% |
| ambiguous_current_exact | 819 | 31.59% |
| ambiguous_observed_exact | 0 | 0.0% |
| ambiguous_normalized | 0 | 0.0% |
| unmapped | 274 | 10.57% |
| non_course_noise | 1 | 0.04% |

- AoS unique-attachable now (strict): `1499/2592` = `57.83%` (excluding non-course noise).
- AoS ambiguity volume: `819` (`31.59%`).
- AoS unmapped volume: `274` (`10.57%`).

## SP Anchorability Results

| Class | Count | Percent |
|---|---:|---:|
| exact_current_unique | 1263 | 50.64% |
| exact_observed_variant_unique | 190 | 7.62% |
| normalization_unique | 0 | 0.0% |
| ambiguous_current_exact | 778 | 31.19% |
| ambiguous_observed_exact | 0 | 0.0% |
| ambiguous_normalized | 0 | 0.0% |
| unmapped | 263 | 10.55% |
| non_course_noise | 0 | 0.0% |

- SP unique-attachable now (strict): `1453/2494` = `58.26%`.
- SP ambiguity volume: `778` (`31.19%`).
- SP unmapped volume: `263` (`10.55%`).

## Interpretation

- Attachment strength: `moderate`.
- Why: strict unique matching safely attaches about 58% of course occurrences now; the larger residual is mostly ambiguity (same title across multiple canonical codes), not pure failure to map.
- Practical meaning: high-confidence attachment can start with unique matches; ambiguity and unmapped cases need policy controls before course-page use.

## Family pattern notes

Lowest attachability families in this run:
- `teaching_mat`: attachable `16.67%`, AoS total `198`, ambiguous `100`, unmapped `65`.
- `education_ma`: attachable `26.5%`, AoS total `117`, ambiguous `85`, unmapped `1`.
- `education_ba`: attachable `43.95%`, AoS total `405`, ambiguous `149`, unmapped `78`.
- `cs_ug`: attachable `47.54%`, AoS total `284`, ambiguous `138`, unmapped `11`.
- `education_bs`: attachable `56.79%`, AoS total `162`, ambiguous `54`, unmapped `16`.
Highest attachability families in this run:
- `mba`: attachable `100.0%`, AoS total `30`, ambiguous `0`, unmapped `0`.
- `education_grad`: attachable `86.36%`, AoS total `22`, ambiguous `0`, unmapped `3`.
- `nursing_ug`: attachable `83.64%`, AoS total `56`, ambiguous `9`, unmapped `0`.
- `healthcare_grad`: attachable `80.95%`, AoS total `21`, ambiguous `3`, unmapped `1`.
- `nursing_rn_msn`: attachable `75.79%`, AoS total `95`, ambiguous `15`, unmapped `8`.

## Class examples

- `exact_current_unique`: `Security Foundations` -> `D481` (MSCSIA).
- `exact_observed_variant_unique`: `Introduction to Communication: Connecting with Others` -> `D268` (BAESSPMM).
- `ambiguous_current_exact`: `Calculus I` -> multiple canonical codes (`C282`, `C362`, `C363`, `C958`, `D890`, `QJT2`).
- `unmapped`: `Software Product Design and Requirement Engineering` (MSSWEDOE).
- `non_course_noise`: BSPRN extracted sentence line captured as course title.