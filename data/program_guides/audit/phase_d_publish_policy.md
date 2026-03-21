# Phase D Publish Policy

**Version:** phase_d_policy_v1  
**Date:** 2026-03-21

## Inclusion States
- `publish_full`: full-use guides, all v1-safe fields
- `publish_partial`: partial-use guides with explicit suppression and caveat flags
- `internal_only`: non-safe fields regardless of guide confidence

## Field-Level Policy (v1)
| Field | Decision | Surface | Notes |
|---|---|---|---|
| Standard Path list | Publish | Degree | Exclude for SP-unusable guides |
| Standard Path CUs | Publish | Degree | Same gate as SP list |
| Standard Path term | Publish when present | Degree | Render as no-term ordered list when absent |
| AoS groups | Publish | Degree | Core structure context |
| Course descriptions | Publish | Degree | Strongest guide field |
| Competency bullets | Publish conditional | Degree | Suppress known empty exceptions |
| Capstone | Publish conditional | Degree | Add partial marker for MEDETID |
| Guide version/pub metadata | Publish optional | Degree/internal | Omit silently when absent |
| Prerequisite mentions | Internal only | None | False-positive risk |
| Cert-prep (structured) | Internal only (v1) | None | Not yet normalized field |
| Family-specific sections | Internal only (v1) | None | Defer until explicit requirement |

## Caveat Guides
See JSON policy for exact allow/disallow and caveat messaging:
- BSITM, MATSPED, MSCSUG: AoS-only publication
- BSPRN: SP partial with explicit Pre-Nursing labeling
- MEDETID: capstone partial marker
- BSNU: metadata optional/missing allowed

## Claim Boundary
- Safe public: complete extraction artifacts exist, caveats documented, live integration pending.
- Unsafe public: any statement implying all fields are equally reliable or already live on Atlas.
