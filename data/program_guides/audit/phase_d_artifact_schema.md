# Phase D Artifact Schema

**Version:** phase_d_schema_v1  
**Date:** 2026-03-21

## Output Strategy
- `public/data/program_guides/index.json`
- `public/data/program_guides/guides/{program_code}.json`

## Required Top-Level Fields (Per Guide)
- Identity: `program_code`, `family`, `degree_title_display`, `source_degree_title`
- Quality: `confidence`, `disposition`, `sp_status`, `aos_status`, `caveat_flags[]`
- Provenance: `schema_version`, `generated_at`, `source_paths`, `source_version`, `source_pub_date`, `source_page_count`
- Payload: `standard_path`, `areas_of_study`, `capstone`

## Partial-Use Encoding
Partial guides are included, not dropped.
- SP-unusable guides: `standard_path.available=false`, rows empty, caveat flag set
- SP-partial guides: `standard_path.available=true`, `standard_path.partial=true`, explicit label

## Example Types
1. Full-use normal guide (`BSCS`)
2. Partial-use dual-track guide (`BSPRN`)
3. Capstone-caveat guide (`MEDETID`)
4. SP-unusable but AoS-usable guide (`MSCSUG`)

Refer to JSON schema artifact for detailed example objects.
