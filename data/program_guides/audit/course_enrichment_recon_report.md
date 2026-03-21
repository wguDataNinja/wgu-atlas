# Course Enrichment Reconnaissance Report

Date: 2026-03-21

Scope: preliminary evidence-backed inventory of guide-derived course enrichment value. This is not a final implementation design.

## Chosen sample and sufficiency

- Sample size: 11 guides (`BSCSIA`, `BSCNEAWS`, `MSCSIA`, `MSIT`, `BSACC`, `MBA`, `BSNU`, `BSPRN`, `MHA`, `BAELED`, `MATSPED`).
- Breadth: Business, Technology, Health, Education; UG + graduate; 9 families; includes two partial-use guides.
- Cert focus included via cert-heavy IT guides and non-cert contrast guides.
- This supports a preliminary read, not corpus-uniform claims.

## What course-level information exists in guides

| Information type | Present in sample? | Typical surface | Usability read |
|---|---|---|---|
| Course title | Yes | Standard Path, AoS course lists | Strong for degree context; limited for code-level anchoring |
| CU values | Yes | Standard Path rows | Strong for degree planning context |
| Term sequencing | Mostly (except no-term or unusable SP) | Standard Path rows | Strong where SP usable; degree-context-only |
| AoS grouping/role context | Yes | AoS group headers | Strong for role-in-degree enrichment |
| Course descriptions | Yes | AoS course cards | Strong; high-value narrative |
| Competency bullets | Yes (near-complete) | AoS course cards | Strong; materially richer than canonical catalog table |
| Capstone designation/details | Present in subset | Capstone section | Strong at degree level |
| Prerequisite mentions (parsed) | Present but uneven | AoS parsed fields | Weak/mixed; internal-only unless tightened |
| Certification mentions (parsed) | Present but noisy | AoS parsed fields | Mixed: some strong explicit prep + many false positives |

## Where the information lives in guides

- Recurrent section surfaces in sample validation artifacts: `Standard Path`, `Areas of Study`, `Accessibility`, and optional `Capstone`.
- Operationally useful course enrichment surfaces are concentrated in AoS course objects (`description`, `competency_bullets`, role group).
- SP contributes sequencing/CU context but is not a standalone course-identity source.
- In this repo snapshot, `data/program_guides/raw_texts/` is not present; recon is based on parsed/validation/manifest artifacts.

## Direct usability and anchorability

- Corpus-wide check: course-code-like tokens in parsed guide course/SP titles = `0` guides in SP, `0` guides in AoS (effectively none).
- Sample exact-title canonical anchoring (no fuzzy): `133` unique, `96` ambiguous, `45` unmapped across `274` AoS course occurrences.
- Implication: guides hold strong course content, but code-level anchoring usually requires canonical title mapping logic because explicit codes are generally absent in parsed guide course titles.

## Certification relationship findings (priority focus)

- Positive evidence shape exists in cert-heavy IT guides:
  - `Network and Security - Applications`: explicit Security+ exam-prep wording.
  - `Networks`: explicit Network+ exam-prep wording.
  - `Cloud Foundations`: explicit AWS Certified Practitioner exam-prep wording.
- But cert parsed field quality is currently mixed:
  - frequent parser-noise tokens (`aws and`, `aws in`, `aws to`, etc.) appear as cert mentions.
  - some adjacent professional references (`CPA Code`) are not direct cert-prep claims.
- Conclusion: cert relationships are promising but require extraction/policy hardening before any publish-safe mapping.

## Strongest course enrichment opportunities now

| Opportunity | Evidence in sample | Opportunity class |
|---|---|---|
| AoS course descriptions | Present across all sampled guides | Strong opportunity |
| Competency bullet enrichment | Present across all sampled guides (with known minor corpus exceptions) | Strong opportunity |
| AoS role context (group labels) | Repeated clusters by school/discipline | Strong opportunity |
| SP CU + term degree context | Available in most sampled guides (with caveats) | Strong opportunity |
| Capstone narratives | Present in several grad/professional guides | Strong opportunity |
| Cert course relationships | Explicit in subset, noisy overall | Plausible, needs policy/extractor work |
| Parsed prerequisite dependencies | Many fragments/generic phrases | Weak/risky for public fielding now |

## College-level derived enrichment potential

- Preliminary evidence is positive: repeated AoS structural patterns appear by school/family.
- Education sample (`BAELED`, `MATSPED`): recurring `Professional Core`, `Clinical Experiences`, `Student Teaching`.
- Technology sample (`BSCSIA`, `BSCNEAWS`, `MSCSIA`, `MSIT`): recurring network/security/cloud/IT management clusters.
- Health sample (`BSNU`, `BSPRN`, `MHA`): recurring nursing/healthcare core structures with program-specific caveats.
- This looks suitable for later college-level aggregation work, but not enough to claim corpus-wide normalization yet.

## Caveat guides in sample

- `BSPRN`: partial-use; SP is Pre-Nursing-only while Nursing-track courses are AoS-only.
- `MATSPED`: partial-use; SP unusable due to source extraction artifact; AoS remains usable.
- These caveats materially affect SP-driven course-context assumptions.

## Answers to required recon questions

1. Course-level info present: titles, CU/term context, AoS group role, descriptions, competencies, optional capstones, noisy prereq/cert parsed snippets.
2. Surfaces: Standard Path, Areas of Study, Capstone, and degree-level program description context.
3. Strongest opportunities: AoS descriptions + competencies + role grouping; SP CU/term as degree context.
4. Weak/risky: parsed cert/prereq fields in current form; direct code claims from guide text.
5. Course-code anchors: direct codes largely absent in parsed course/SP titles; title-based canonical anchoring is possible but often ambiguous.
6. Cert/course relationships: explicit prep language exists in cert-heavy IT programs, but mixed with substantial parser noise.
7. Future course-page enrichment likelihood: yes for conservative fields (description/competencies/role), contingent on anchor and policy gating.
8. College-level derived enrichment likelihood: promising, given repeated AoS structures across sampled school lanes.
9. Best next session: run strict anchorability matrix + cert/prereq quality hardening pass before any course-page policy or shipping decisions.

## Recommended next session

1. Build a strict exact-title canonical anchorability matrix for course occurrences (unique vs ambiguous vs unmapped), expanding beyond this sample.
2. Split cert/prereq extracted strings into publishable vs internal-only classes using explicit linguistic rules and token-level noise suppression.
3. Draft a conservative course-enrichment candidate schema limited to high-confidence fields (description, competencies, AoS role context) and explicit exclusions.