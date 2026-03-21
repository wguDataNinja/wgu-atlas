# Program Guide Corpus Manifest

**Date:** 2026-03-21

## 1. Executive Summary
Phase C is closed at full artifact coverage (115/115). Data quality is not uniform: 111 guides are full-use, 4 are partial-use, and 0 are excluded. AoS content is complete and strongest; SP content is usable for 111 guides, partial for 1, and unusable for 3 due to source extraction artifacts.

This file is the canonical human-readable truth source for corpus state and claim boundaries.

## 2. Final Counts

| Metric | Value |
|---|---:|
| Total guides | 115 |
| Artifact coverage (parsed/validation/manifest) | 115/115 (100.0%) each |
| Family-validated coverage | 115/115 (100.0%) |
| Downstream-usable full | 111 |
| Downstream-usable partial | 4 |
| Excluded / not usable | 0 |
| Confidence distribution | 96 HIGH / 17 MEDIUM / 2 LOW |
| Parsed course descriptions (AoS courses) | 2593 |
| Competency sets | 2591 (99.9%) |
| Standard Path rows extracted | 2568 |
| Standard Path usability | 111 usable / 1 partial / 3 unusable |
| Family status | 14 complete, 5 complete-with-caveats, 0 partial, 0 deferred |

## 3. Family-By-Family Status

| Family | Guides | Status | Confidence (H/M/L) | Full | Partial | Excluded | Caveat Guides |
|---|---:|---|---:|---:|---:|---:|---|
| accounting_ma | 5 | complete | 5/0/0 | 5 | 0 | 0 | — |
| cs_grad | 5 | complete-with-caveats | 4/0/1 | 4 | 1 | 0 | MSCSUG |
| cs_ug | 8 | complete | 4/4/0 | 8 | 0 | 0 | — |
| data_analytics_grad | 3 | complete | 3/0/0 | 3 | 0 | 0 | — |
| education_ba | 11 | complete | 5/6/0 | 11 | 0 | 0 | — |
| education_bs | 4 | complete | 4/0/0 | 4 | 0 | 0 | — |
| education_grad | 2 | complete-with-caveats | 1/1/0 | 2 | 0 | 0 | MEDETID |
| education_ma | 9 | complete | 9/0/0 | 9 | 0 | 0 | — |
| endorsement | 8 | complete | 8/0/0 | 8 | 0 | 0 | — |
| graduate_standard | 9 | complete | 9/0/0 | 9 | 0 | 0 | — |
| healthcare_grad | 2 | complete | 2/0/0 | 2 | 0 | 0 | — |
| mba | 3 | complete | 3/0/0 | 3 | 0 | 0 | — |
| nursing_msn | 5 | complete | 5/0/0 | 5 | 0 | 0 | — |
| nursing_pmc | 4 | complete | 4/0/0 | 4 | 0 | 0 | — |
| nursing_rn_msn | 3 | complete | 3/0/0 | 3 | 0 | 0 | — |
| nursing_ug | 2 | complete-with-caveats | 0/2/0 | 1 | 1 | 0 | BSPRN |
| standard_bs | 19 | complete-with-caveats | 16/2/1 | 18 | 1 | 0 | BSITM |
| swe_grad | 4 | complete | 3/1/0 | 4 | 0 | 0 | — |
| teaching_mat | 9 | complete-with-caveats | 8/1/0 | 8 | 1 | 0 | MATSPED |

## 4. Guide-By-Guide Manifest

| Code | Family | Disp | Conf | SP Status | AoS | SP Rows | AoS Courses | Major Caveat |
|---|---|---|---|---|---|---:|---:|---|
| BAELED | education_ba | full-use | high | usable-no-term | usable | 37 | 37 | — |
| BAESELED | education_ba | full-use | high | usable-with-term | usable | 33 | 33 | — |
| BAESMES | education_ba | full-use | high | usable-with-term | usable | 35 | 35 | — |
| BAESSESB | education_ba | full-use | medium | usable-with-term | usable | 36 | 37 | 1 AoS titles not in SP: ['Secondary Disciplinary Literacy'] |
| BAESSESC | education_ba | full-use | high | usable-with-term | usable | 36 | 36 | — |
| BAESSESE | education_ba | full-use | medium | usable-with-term | usable | 36 | 37 | 1 AoS titles not in SP: ['Secondary Disciplinary Literacy'] |
| BAESSESP | education_ba | full-use | high | usable-with-term | usable | 36 | 36 | — |
| BAESSPEE | education_ba | full-use | medium | usable-with-term | usable | 41 | 40 | 1 SP titles not found in AoS: ['Considerations for Instructional Planning for Learners'] |
| BAESSPMM | education_ba | full-use | medium | usable-with-term | usable | 34 | 33 | 1 SP titles not found in AoS: ['Considerations for Instructional Planning for Learners'] |
| BASPEE | education_ba | full-use | medium | usable-no-term | usable | 45 | 44 | 1 SP titles not found in AoS: ['Considerations for Instructional Planning for Learners'] |
| BASPMM | education_ba | full-use | medium | usable-no-term | usable | 38 | 37 | 1 SP titles not found in AoS: ['Considerations for Instructional Planning for Learners'] |
| BSACC | standard_bs | full-use | high | usable-with-term | usable | 40 | 40 | — |
| BSBAHC | standard_bs | full-use | high | usable-with-term | usable | 40 | 39 | — |
| BSC | standard_bs | full-use | high | usable-with-term | usable | 38 | 38 | — |
| BSCNE | cs_ug | full-use | high | usable-with-term | usable | 34 | 34 | — |
| BSCNEAWS | cs_ug | full-use | high | usable-with-term | usable | 35 | 35 | — |
| BSCNEAZR | cs_ug | full-use | high | usable-with-term | usable | 35 | 35 | — |
| BSCNECIS | cs_ug | full-use | medium | usable-with-term | usable | 32 | 32 | 1 SP titles not found in AoS: ['Hybrid Cloud Infrastructure and and Orchestration'] |
| BSCS | cs_ug | full-use | high | usable-with-term | usable | 37 | 37 | — |
| BSCSIA | cs_ug | full-use | medium | usable-with-term | usable | 38 | 37 | 1 SP titles not found in AoS: ['Scripting and Programming Foundations'] |
| BSDA | standard_bs | full-use | high | usable-with-term | usable | 42 | 41 | — |
| BSFIN | standard_bs | full-use | high | usable-with-term | usable | 40 | 40 | — |
| BSHA | standard_bs | full-use | high | usable-with-term | usable | 34 | 34 | — |
| BSHHS | standard_bs | full-use | high | usable-with-term | usable | 35 | 34 | — |
| BSHIM | standard_bs | full-use | medium | usable-with-term | usable | 36 | 36 | 1 SP titles not found in AoS: ['Healthcare Information Systems Management'] |
| BSHR | standard_bs | full-use | high | usable-with-term | usable | 39 | 39 | — |
| BSHS | standard_bs | full-use | high | usable-with-term | usable | 28 | 28 | — |
| BSIT | standard_bs | full-use | high | usable-with-term | usable | 35 | 35 | — |
| BSITM | standard_bs | partial-use | low | unusable | usable | 35 | 40 | Standard Path unusable due to source PDF column extraction failure; AoS usable. |
| BSMES | standard_bs | full-use | high | usable-no-term | usable | 39 | 39 | — |
| BSMGT | standard_bs | full-use | high | usable-with-term | usable | 36 | 35 | — |
| BSMKT | standard_bs | full-use | high | usable-with-term | usable | 37 | 37 | — |
| BSNU | nursing_ug | full-use | medium | usable-with-term | usable | 22 | 22 | version/pub_date/page_count missing due to no footer lines in source text. |
| BSPH | standard_bs | full-use | high | usable-with-term | usable | 33 | 33 | — |
| BSPRN | nursing_ug | partial-use | medium | partial | usable | 19 | 34 | Standard Path covers Pre-Nursing track only; 15 Nursing-track courses are AoS-only. |
| BSPSY | standard_bs | full-use | high | usable-with-term | usable | 34 | 34 | — |
| BSSCOM | standard_bs | full-use | medium | usable-with-term | usable | 35 | 35 | 1 SP titles not found in AoS: ['21st Century Operations and Supply Chain'] |
| BSSESB | education_bs | full-use | high | usable-no-term | usable | 41 | 41 | — |
| BSSESC | education_bs | full-use | high | usable-no-term | usable | 40 | 40 | — |
| BSSESE | education_bs | full-use | high | usable-no-term | usable | 41 | 41 | — |
| BSSESP | education_bs | full-use | high | usable-no-term | usable | 40 | 40 | — |
| BSSWE_C | cs_ug | full-use | medium | usable-with-term | usable | 38 | 36 | One course has empty competency bullets (source-format artifact). |
| BSSWE_Java | cs_ug | full-use | medium | usable-with-term | usable | 40 | 38 | — |
| BSUXD | standard_bs | full-use | high | usable-with-term | usable | 38 | 38 | — |
| ENDECE | endorsement | full-use | high | usable-no-term | usable | 6 | 6 | — |
| ENDELL | endorsement | full-use | high | usable-with-term | usable | 8 | 8 | — |
| ENDMEMG | endorsement | full-use | high | usable-no-term | usable | 2 | 2 | — |
| ENDSEMG | endorsement | full-use | high | usable-no-term | usable | 2 | 2 | — |
| ENDSESB | endorsement | full-use | high | usable-no-term | usable | 9 | 9 | — |
| ENDSESC | endorsement | full-use | high | usable-no-term | usable | 7 | 7 | — |
| ENDSESE | endorsement | full-use | high | usable-no-term | usable | 9 | 9 | — |
| ENDSESP | endorsement | full-use | high | usable-no-term | usable | 7 | 7 | — |
| MACC | accounting_ma | full-use | high | usable-with-term | usable | 10 | 10 | — |
| MACCA | accounting_ma | full-use | high | usable-with-term | usable | 10 | 10 | — |
| MACCF | accounting_ma | full-use | high | usable-with-term | usable | 11 | 11 | — |
| MACCM | accounting_ma | full-use | high | usable-with-term | usable | 10 | 10 | Corporate Financial Analysis title/first-sentence quality issue (cosmetic). |
| MACCT | accounting_ma | full-use | high | usable-with-term | usable | 10 | 10 | — |
| MAELLP12 | education_ma | full-use | high | usable-with-term | usable | 11 | 11 | page_count=0 in metadata (cosmetic). |
| MAMEK6 | education_ma | full-use | high | usable-with-term | usable | 10 | 9 | — |
| MAMEMG | education_ma | full-use | high | usable-with-term | usable | 14 | 13 | — |
| MAMES | education_ma | full-use | high | usable-with-term | usable | 18 | 18 | — |
| MASEMG | education_ma | full-use | high | usable-with-term | usable | 14 | 14 | — |
| MASESB | education_ma | full-use | high | usable-with-term | usable | 13 | 13 | — |
| MASESC | education_ma | full-use | high | usable-with-term | usable | 14 | 14 | — |
| MASESE | education_ma | full-use | high | usable-with-term | usable | 12 | 12 | — |
| MASESP | education_ma | full-use | high | usable-with-term | usable | 13 | 13 | — |
| MATEES | teaching_mat | full-use | high | usable-no-term | usable | 20 | 20 | — |
| MATELED | teaching_mat | full-use | high | usable-with-term | usable | 28 | 28 | — |
| MATMES | teaching_mat | full-use | high | usable-no-term | usable | 21 | 21 | — |
| MATSESB | teaching_mat | full-use | high | usable-no-term | usable | 20 | 20 | — |
| MATSESC | teaching_mat | full-use | high | usable-no-term | usable | 20 | 20 | — |
| MATSESE | teaching_mat | full-use | high | usable-no-term | usable | 20 | 20 | — |
| MATSESP | teaching_mat | full-use | high | usable-no-term | usable | 20 | 20 | — |
| MATSPED | teaching_mat | partial-use | medium | unusable | usable | 9 | 30 | Standard Path unusable due to source PDF column extraction failure; AoS usable. |
| MATSSES | teaching_mat | full-use | high | usable-no-term | usable | 19 | 19 | — |
| MBA | mba | full-use | high | usable-with-term | usable | 11 | 10 | — |
| MBAHA | mba | full-use | high | usable-with-term | usable | 11 | 10 | — |
| MBAITM | mba | full-use | high | usable-with-term | usable | 11 | 10 | — |
| MEDETID | education_grad | full-use | medium | usable-with-term | usable | 12 | 9 | Capstone field captures first of three capstone-sequence courses (structural limitation). |
| MHA | healthcare_grad | full-use | high | usable-with-term | usable | 10 | 9 | — |
| MPH | healthcare_grad | full-use | high | usable-with-term | usable | 12 | 12 | — |
| MSCIN | graduate_standard | full-use | high | usable-no-term | usable | 10 | 10 | — |
| MSCSAIML | cs_grad | full-use | high | usable-with-term | usable | 10 | 10 | degree_title is truncated in parsed output (cosmetic; use catalog title). |
| MSCSCS | cs_grad | full-use | high | usable-with-term | usable | 10 | 10 | — |
| MSCSHCI | cs_grad | full-use | high | usable-with-term | usable | 10 | 10 | — |
| MSCSIA | cs_grad | full-use | high | usable-with-term | usable | 10 | 9 | — |
| MSCSUG | cs_grad | partial-use | low | unusable | usable | 30 | 37 | Standard Path unusable due to source PDF column extraction failure; AoS usable. |
| MSDADE | data_analytics_grad | full-use | high | usable-with-term | usable | 11 | 11 | — |
| MSDADPE | data_analytics_grad | full-use | high | usable-with-term | usable | 11 | 11 | — |
| MSDADS | data_analytics_grad | full-use | high | usable-with-term | usable | 11 | 11 | — |
| MSEDL | education_grad | full-use | high | usable-with-term | usable | 13 | 13 | — |
| MSHRM | graduate_standard | full-use | high | usable-with-term | usable | 10 | 10 | — |
| MSIT | graduate_standard | full-use | high | usable-with-term | usable | 11 | 11 | — |
| MSITM | graduate_standard | full-use | high | usable-with-term | usable | 10 | 9 | — |
| MSITPM | graduate_standard | full-use | high | usable-with-term | usable | 10 | 10 | — |
| MSITUG | graduate_standard | full-use | high | usable-with-term | usable | 35 | 35 | — |
| MSMK | graduate_standard | full-use | high | usable-with-term | usable | 11 | 11 | — |
| MSMKA | graduate_standard | full-use | high | usable-with-term | usable | 11 | 11 | — |
| MSML | graduate_standard | full-use | high | usable-with-term | usable | 10 | 9 | — |
| MSNUED | nursing_msn | full-use | high | usable-with-term | usable | 15 | 15 | — |
| MSNUFNP | nursing_msn | full-use | high | usable-with-term | usable | 16 | 16 | — |
| MSNULM | nursing_msn | full-use | high | usable-with-term | usable | 15 | 15 | — |
| MSNUNI | nursing_msn | full-use | high | usable-with-term | usable | 14 | 14 | — |
| MSNUPMHNP | nursing_msn | full-use | high | usable-with-term | usable | 17 | 17 | — |
| MSRNNUED | nursing_rn_msn | full-use | high | usable-with-term | usable | 32 | 32 | degree_title is truncated in parsed output (cosmetic; use catalog title). |
| MSRNNULM | nursing_rn_msn | full-use | high | usable-with-term | usable | 32 | 32 | degree_title is truncated in parsed output (cosmetic; use catalog title). |
| MSRNNUNI | nursing_rn_msn | full-use | high | usable-with-term | usable | 31 | 31 | degree_title is truncated in parsed output (cosmetic; use catalog title). |
| MSSWEAIE | swe_grad | full-use | high | usable-with-term | usable | 10 | 10 | — |
| MSSWEDDD | swe_grad | full-use | high | usable-with-term | usable | 10 | 10 | — |
| MSSWEDOE | swe_grad | full-use | high | usable-with-term | usable | 10 | 10 | — |
| MSSWEUG | swe_grad | full-use | medium | usable-with-term | usable | 38 | 38 | 1 SP titles not found in AoS: ['Scripting and Programming Foundations'] |
| PMCNUED | nursing_pmc | full-use | high | usable-with-term | usable | 8 | 8 | — |
| PMCNUFNP | nursing_pmc | full-use | high | usable-with-term | usable | 10 | 10 | — |
| PMCNULM | nursing_pmc | full-use | high | usable-with-term | usable | 8 | 8 | — |
| PMCNUPMHNP | nursing_pmc | full-use | high | usable-with-term | usable | 11 | 11 | — |

## 5. Known Issue Register

| Code(s) | Severity | Impact | Handling |
|---|---|---|---|
| BSITM | major | SP unusable; AoS usable | Use AoS only; exclude SP. |
| MATSPED | major | SP unusable; AoS usable | Use AoS only; exclude SP. |
| MSCSUG | major | SP unusable; AoS usable | Use AoS only; exclude SP. |
| BSPRN | major | SP is Pre-Nursing-only; Nursing track AoS-only | Label SP as Pre-Nursing-only or suppress SP. |
| MEDETID | moderate | capstone field captures first of 3 sequence courses | Use AoS/SP normally; treat capstone as partial. |
| BSNU | moderate | version/pub_date/page_count unavailable | Do not require metadata fields for inclusion. |
| MSRNNUED,MSRNNULM,MSRNNUNI,MSCSAIML | low | degree_title truncated in parsed output | Use catalog degree title as display title. |
| BSSWE_C | low | one course has empty competency bullets | Suppress bullets for that single course. |
| MACCM | low | cosmetic description/title quality issue | Allow with note or minor editorial cleanup at render time. |
| MAELLP12 | low | page_count=0 cosmetic metadata gap | Omit page count display for this guide. |

## 6. Safe-Field Inventory

- Safe for all 115 guides (AoS): `areas_of_study[].group`, `areas_of_study[].courses[].title`, `areas_of_study[].courses[].description`
- Safe for 113/115 with two known empty-course exceptions: `areas_of_study[].courses[].competency_bullets`
- Safe for 112/115 guides: `standard_path[].title`, `standard_path[].cus`
- Safe for 89/115 guides: `standard_path[].term` (23 guides are no-term SP formats)
- Not safe as public structured fields without more work: prereq mentions; parsed degree_title for known truncated guides

## 7. Atlas-Usable Summary

- Parsed/validated corpus is complete for Phase C and is suitable for Phase D schema/policy design.
- Program-page enrichment is supportable at artifact level, but runtime publication under `public/data/program_guides/` is not built yet.
- Course-page guide enrichment still depends on Phase E course-code matching (not started).

## 8. Artifact Map

- Source artifacts: `data/program_guides/{parsed,validation,manifest_rows}/`
- Family validation: `data/program_guides/family_validation/`
- Planning/audit: `data/program_guides/audit/`
- Runtime target (not built): `public/data/program_guides/`

## 9. Concise Chronology

- **2026-03-20**: Phase A/B groundwork and early family rollouts established manifest-first workflow and gate-test discipline.
- **2026-03-21**: Families were completed through staged gate + rollout sessions, including parser fixes for multiline/SP/bullet-edge cases.
- **2026-03-21**: Session 23 closed corpus artifact coverage to 115/115 and family-validated coverage to 115/115.
- **2026-03-21**: Enrichment planning artifacts were created (degree/course matrices, no-use list, final memo).
- **2026-03-21**: Post-close verification reconciled counts, corrected overclaims, and produced a durable claims register + corpus manifest.

## 10. Corrections and Overclaim Tightening

- Standard Path usable-guide count reconciled to 112 (not 113) because MATSPED SP is unusable.
- Term-available guide count reconciled to 89 of 112 SP-usable guides (not 95 of 113).
- teaching_mat rollout confidence corrected to 8 HIGH / 1 MEDIUM / 0 LOW.
- graduate_standard rollout confidence corrected to 9 HIGH / 0 MEDIUM / 0 LOW.
- Stale audit docs that still claim 38/115 are now superseded by this manifest.
