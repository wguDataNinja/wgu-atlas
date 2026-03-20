# Continuity Review Module Artifacts

## Module-local files

### README.md
- **Purpose:** Module overview, current state, and next tasks
- **Content:** Purpose, scope, assumptions, open questions, next steps

### SESSION_LOG.md
- **Purpose:** Append-only log of module activities
- **Content:** Date, task, files created/updated, conclusions, next steps

### ARTIFACTS.md
- **Purpose:** Index of module-local artifacts and their purposes
- **Content:** File descriptions and relationships

### review_method_plan.md
- **Purpose:** Planning memo defining the review method approach
- **Content:** Review format options, validation approach, pattern types

## External files this module depends on

### data/lineage/lineage_decisions.json
- **Purpose:** Source of approved/pending/excluded continuity events
- **Usage:** Primary input for review card creation

### data/lineage/program_history_enrichment.json
- **Purpose:** Source of overlap metrics and course change data
- **Usage:** Provides quantitative data for review cards

### docs/DECISIONS.md
- **Purpose:** Policy framework for continuity decisions
- **Usage:** Reference for decision criteria and boundaries

### _internal/PROJECT_CONTINUITY_ATLAS.md
- **Purpose:** Project-level continuity context and state
- **Usage:** Understanding broader project constraints and goals

## Artifact relationships

- `review_method_plan.md` references external policy files
- `README.md` summarizes current state from all artifacts
- `SESSION_LOG.md` tracks creation and updates of all artifacts
- Review cards (future) will be generated from lineage data files