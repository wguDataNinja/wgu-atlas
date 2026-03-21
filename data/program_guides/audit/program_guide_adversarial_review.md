# Program Guide Adversarial Review

**Date:** 2026-03-21

## Verdict Summary

- Justified: 3
- Partially justified: 1
- Overstated: 3

## Claim-by-Claim

| Claim | Status | Evidence check | Safe wording |
|---|---|---|---|
| We scraped all the program guides. | justified | 115 parsed + 115 validation + 115 manifest_row artifacts exist on disk. | We have complete on-disk extraction artifacts for all 115 guides in the current corpus. |
| We know what is in them all. | partially_justified | AoS content is complete, but 4 guides are partial-use and 3 have unusable SP content. | We have full AoS coverage across all 115 guides, with known SP limitations in 3 guides and one dual-track SP partial. |
| We validated the corpus. | justified_with_scope | Family validation rollouts and per-guide validation files exist for all 115 guides. | All 115 guides have validation artifacts and family-level rollout records; validation caveats are documented per guide. |
| We can use the guides for Atlas enrichment. | justified_with_constraints | 111 full-use + 4 partial-use; no excluded guides. | The corpus is usable for Atlas enrichment planning now: 111 full-use guides and 4 partial-use guides with explicit exclusions. |
| We present the most useful guide-derived information where relevant. | overstated_currently | Phase D build and runtime wiring are not yet implemented. | We have identified and validated the most useful guide-derived fields; live product presentation is pending Phase D build and integration. |
| Standard Path is available for all guides. | overstated | SP unusable for BSITM, MATSPED, MSCSUG; BSPRN SP is partial by track design. | Standard Path is usable for 111 guides, partial for BSPRN, and unusable for 3 guides due to source extraction artifacts. |
| Guide metadata is complete everywhere. | overstated | BSNU, BSSWE_C, BSSWE_Java lack version/pub_date. | Most guides include version/pub_date metadata; known metadata gaps are documented and non-blocking for AoS use. |

## Non-Negotiable Caveats
- BSITM SP unusable
- MATSPED SP unusable
- MSCSUG SP unusable
- BSPRN SP partial (dual-track)
- MEDETID capstone partial

## Public Wording Boundary
Do not imply live site integration. Say parsed+validated corpus is complete and ready for Phase D schema/build work.
