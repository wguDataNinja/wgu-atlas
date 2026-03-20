repoe xplain 1
Here's the deeper smart directory tree for the WGU Atlas repository with file counts for directories with many files:

```
wgu-atlas/
├── _internal/                    # Internal project management & documentation
│   ├── archive/                  # Historical documentation
│   │   └── 2026-03-doc-consolidation/
│   │       ├── CC_START_HERE.md
│   │       ├── DEV_LOG.md
│   │       ├── MIGRATION_HANDOFF.md
│   │       ├── OFFICIAL_CONTEXT_LAYER_PLAN.md
│   │       ├── PRODUCT_REVIEW_2026_03.md
│   │       ├── README.md
│   │       ├── docs_legacy/
│   │       └── official_context/
│   ├── continuity_review/        # Project continuity tracking
│   │   ├── ARTIFACTS.md
│   │   ├── README.md
│   │   ├── review_method_plan.md
│   │   └── SESSION_LOG.md
│   ├── official_resource/        # Resource management
│   │   ├── ARTIFACTS.md
│   │   ├── next_workstream_memo.md
│   │   ├── README.md
│   │   └── SESSION_LOG.md
│   ├── workqueue_inputs/         # Work queue data
│   │   └── official_context_phase2_remaining_batch.json
│   └── youtube/                  # YouTube content management
│       ├── YOUTUBE_WORKLOG.md
│       ├── raw/                  # Raw YouTube data
│       │   └── wgu_official_titles_raw.txt
│       └── working/              # Processed YouTube data
│           └── wgu_official_titles_filtered.txt
├── data/                         # Core data assets (16 JSON files)
│   ├── canonical_courses.csv
│   ├── canonical_courses.json
│   ├── program_history.csv
│   ├── data_club/                # Data club specific data
│   │   └── data_analytics_courses.json
│   ├── enrichment/               # Data enrichment artifacts
│   │   ├── official_context_manifest_phase1.csv
│   │   ├── official_context_manifest_phase1.json
│   │   ├── official_context_manifest_phase2_test.json
│   │   ├── README.txt
│   │   ├── source_enrichment_manifest.json
│   │   └── outcomes/             # Outcome mappings
│   │       ├── outcomes_links.json
│   │       ├── README.md
│   │       ├── bscs/
│   │       ├── bscsia/
│   │       └── caep/
│   ├── lineage/                  # Program lineage data
│   │   ├── lineage_decisions.json
│   │   ├── program_history_enrichment.json
│   │   ├── program_ineage_events.json
│   │   ├── program_lineage_enriched.json
│   │   ├── program_lineage_events_normalized.json
│   │   ├── program_link_candidates.json
│   │   └── program_transition_universe.csv
│   └── site/                     # Site-specific data
│       ├── curated_major_events.json
│       ├── named_events.csv
│       ├── named_events.json
│       └── title_variant_classification.csv
├── docs/                         # Project documentation
│   ├── ATLAS_SPEC.md
│   └── DECISIONS.md
├── public/                       # Static assets & data exports
│   ├── data/                     # Public data API
│   │   ├── course_descriptions.json
│   │   ├── courses.json
│   │   ├── events.json
│   │   ├── homepage_summary.json
│   │   ├── official_resource_placements.json
│   │   ├── program_enriched.json
│   │   ├── programs.json
│   │   ├── search_index.json
│   │   ├── courses/              # 838 course JSON files
│   │   │   ├── AFT2.json
│   │   │   ├── AIT2.json
│   │   │   ├── AMT2.json
│   │   │   ├── AOA2.json
│   │   │   ├── ASA1.json
│   │   │   ├── AUA2.json
│   │   │   ├── AVA2.json
│   │   │   ├── BVT2.json
│   │   │   ├── BWT2.json
│   │   │   ├── BYT2.json
│   │   │   ├── BZT2.json
│   │   │   ├── C100.json
│   │   │   ├── C121.json
│   │   │   ├── C165.json
│   │   │   ├── C168.json
│   │   │   ├── C172.json
│   │   │   ├── C175.json
│   │   │   ├── C179.json
│   │   │   ├── C180.json
│   │   │   ├── C190.json
│   │   │   ├── C200.json
│   │   │   ├── C201.json
│   │   │   ├── C202.json
│   │   │   ├── C203.json
│   │   │   ├── C204.json
│   │   │   ├── C205.json
│   │   │   ├── C206.json
│   │   │   ├── C207.json
│   │   │   ├── C208.json
│   │   │   ├── C209.json
│   │   │   ├── C210.json
│   │   │   ├── C211.json
│   │   │   ├── C212.json
│   │   │   ├── C213.json
│   │   │   ├── C214.json
│   │   │   ├── C215.json
│   │   │   ├── C216.json
│   │   │   ├── C218.json
│   │   │   ├── C219.json
│   │   │   ├── C224.json
│   │   │   ├── C225.json
│   │   │   ├── C226.json
│   │   │   ├── C227.json
│   │   │   ├── C232.json
│   │   │   └── ... (800+ more course files)
│   │   └── downloads/            # Downloadable resources
│   └── .nojekyll
├── screenshots/                  # Project screenshots (9 PNG files)
│   ├── courses.png
│   ├── data.png
│   ├── home.png
│   ├── methods.png
│   ├── programs.png
│   ├── schools.png
│   └── timeline.png
├── scripts/                      # Python processing scripts (10 Python files)
│   ├── add_program_history_enrichment.py
│   ├── bootstrap_source_enrichment_manifest.py
│   ├── build_program_lineage_artifacts.py
│   ├── build_site_data.py
│   ├── compare_program_courses.py
│   ├── extract_course_descriptions.py
│   ├── extract_program_enriched.py
│   ├── generate_content_map.js
│   ├── generate_program_history_artifacts.py
│   ├── generate_program_history_enrichment.py
│   └── validate_lineage_decisions.py
└── src/                          # Application source code
    ├── app/                      # Next.js app pages (15+ TSX files)
    │   ├── about/page.tsx
    │   ├── compare/page.tsx
    │   ├── courses/[code]/page.tsx
    │   ├── courses/page.tsx
    │   ├── data/page.tsx
    │   ├── layout.tsx
    │   ├── methods/page.tsx
    │   ├── not-found.tsx
    │   ├── page.tsx
    │   ├── programs/[code]/LearningOutcomes.tsx
    │   ├── programs/[code]/page.tsx
    │   ├── programs/page.tsx
    │   ├── proto/courses/page.tsx
    │   ├── proto/compare/page.tsx
    │   ├── schools/[slug]/page.tsx
    │   ├── schools/page.tsx
    │   └── timeline/page.tsx
    ├── components/               # React components (13+ TSX files)
    │   ├── compare/CompareSelector.tsx
    │   ├── compare/CompareView.tsx
    │   ├── courses/CourseExplorer.tsx
    │   ├── home/EventPreview.tsx
    │   ├── home/HomeSearch.tsx
    │   ├── home/SchoolCards.tsx
    │   ├── layout/Footer.tsx
    │   ├── layout/Nav.tsx
    │   ├── programs/ProgramExplorer.tsx
    │   ├── proto/CoursePrototypeLab.tsx
    │   ├── proto/ComparePrototypeLab.tsx
    │   ├── proto/compareProtoUtils.ts
    │   └── resources/RelevantResources.tsx
    └── lib/                      # Shared utilities
        ├── basePath.ts
        ├── colleges.ts
        ├── compareUtils.ts
        ├── data.ts
        ├── families.ts
        ├── programs.ts
        └── types.ts
```

**Key Insights:**
- **Massive course dataset**: 838 individual course JSON files in `public/data/courses/`
- **Data processing pipeline**: 10 Python scripts for data transformation and enrichment
- **Rich frontend**: 15+ Next.js pages with specialized components for different views
- **Lineage tracking**: Extensive program lineage and history data for tracking curriculum evolution
- **Modular architecture**: Clear separation between prototype features, production components, and data layers
# WGU Atlas Documentation Review Report

## 1. File-by-file summary

| File | Summary | Unique info | Already in canon | Recommendation |
|------|---------|-------------|------------------|----------------|
| `_internal/archive/2026-03-doc-consolidation/DEV_LOG.md` | Detailed session log of migration from wgu-reddit to wgu-atlas, covering repo hygiene, data migration, Next.js scaffolding, entity pages, program enrichment, and cleanup passes | Migration decisions, build script path issues, Phase 1-8 session details, GitHub Pages deployment setup | Partially reflected in current operator context | **keep as archive reference** - contains migration-specific decisions not in current docs |
| `_internal/archive/2026-03-doc-consolidation/MIGRATION_HANDOFF.md` | Comprehensive migration guide with locked decisions, source-of-truth docs, inventory of what to transfer/leave behind, and specific risks/gotchas | Detailed migration inventory, path adaptation requirements, file-by-file transfer decisions | Core decisions reflected in current docs | **keep as archive reference** - migration-specific operational details |
| `_internal/archive/2026-03-doc-consolidation/PRODUCT_REVIEW_2026_03.md` | Product direction memo responding to shift toward catalog-backed information over change-history layer | Credit units extraction status, stability classification, program descriptions parsing needs, effort classification table | Some reflected in current docs | **later promote key points** - contains important product decisions |
| `_internal/archive/2026-03-doc-consolidation/OFFICIAL_CONTEXT_LAYER_PLAN.md` | Strategy for discovering, structuring, and surfacing official WGU website content alongside catalog entities | Official context layer strategy, YouTube channel analysis, outcomes page chart extraction plan | Not reflected in current docs | **later promote key points** - contains important architectural decisions |
| `_internal/archive/2026-03-doc-consolidation/CC_START_HERE.md` | Claude Code working context for wgu-atlas repo, including project state, decisions, and implementation plan | Current project state, ordered implementation plan, repo hygiene rules | Some reflected in current docs | **keep as archive reference** - working context for specific sessions |
| `_internal/archive/2026-03-doc-consolidation/official_context/README.md` | Workflow overview for Official Context Layer workstream with 5-phase process | Phase-based workflow, file structure | Not reflected in current docs | **later promote key points** - workflow methodology |
| `_internal/archive/2026-03-doc-consolidation/official_context/DEV_LOG.md` | Internal log for official-context workstream with Phase 1-2 progress | Sitemap extraction results (604 entries), Phase 2 test findings, batch processing approach | Not reflected in current docs | **keep as archive reference** - workstream-specific progress |
| `_internal/archive/2026-03-doc-consolidation/official_context/PHASE2_TEST_NOTES.md` | Findings from Phase 2 enrichment test on 15 entries | Test validation results, program guide vs outcomes page analysis, accreditation page scope differences | Not reflected in current docs | **keep as archive reference** - test-specific findings |
| `_internal/archive/2026-03-doc-consolidation/official_context/REVIEW_QUEUE.md` | Manual review tracking for Phase 1 to Phase 2 transition | Review criteria, pruning guidelines, keep/skip/maybe framework | Not reflected in current docs | **keep as archive reference** - review process documentation |
| `data/enrichment/outcomes/README.md` | Documentation of WGU accreditation & outcomes pages with data analysis | ABET outcomes data interpretation, CAEP accreditation details, CAHIIM time-to-degree metrics | Not reflected in current docs | **later promote key points** - accreditation data insights |

## 2. Questions answered

These files help answer the operator's open questions about:

**Official-resource artifact map:**
- `OFFICIAL_CONTEXT_LAYER_PLAN.md` provides comprehensive strategy for official WGU content discovery
- `official_context/README.md` and `DEV_LOG.md` show current progress (Phase 1 complete, 604 sitemap entries)
- `PHASE2_TEST_NOTES.md` validates the enrichment workflow

**Archive triage:**
- `MIGRATION_HANDOFF.md` provides detailed leave-behind list and transfer decisions
- `DEV_LOG.md` documents what was intentionally left behind during migration
- `CC_START_HERE.md` provides repo hygiene rules for what belongs in wgu-atlas

**Historical design rationale:**
- `DEV_LOG.md` contains session-by-session rationale for architectural decisions
- `PRODUCT_REVIEW_2026_03.md` documents the product direction shift toward catalog facts over change-history
- `OFFICIAL_CONTEXT_LAYER_PLAN.md` explains the strategic importance of leading with official context

**Source-enrichment process/state:**
- `DEV_LOG.md` documents the official context layer progress through Phases 1-2
- `PHASE2_TEST_NOTES.md` validates the enrichment workflow with 15 test entries
- `REVIEW_QUEUE.md` provides the manual review framework

**What should later be promoted:**
- Product decisions from `PRODUCT_REVIEW_2026_03.md` (credit units priority, program pages)
- Official context strategy from `OFFICIAL_CONTEXT_LAYER_PLAN.md`
- Accreditation insights from `data/enrichment/outcomes/README.md`

## 3. Most important unique takeaways

1. **Credit units are already extracted but not surfaced** - `canonical_cus` exists in all course detail files but isn't shown anywhere in the UI (highest-value zero-effort improvement)

2. **Official Context Layer is actively being built** - 604 sitemap entries extracted, Phase 2 test completed, workflow validated

3. **Build script path dependency is a critical migration risk** - `build_site_data.py` paths break when moved; requires env var adaptation

4. **Program descriptions and outcomes are parseable but not yet extracted** - well-bounded parsing opportunities identified

5. **YouTube channels contain 1,940+ official videos** - two official WGU YouTube channels identified as future official context sources

6. **Accreditation pages vary by scope** - school-level vs program-specific accreditation requires different attachment strategies

7. **ABET outcomes pages contain real pass-rate data** - course-level assessment results available for BSCS/BSCSIA programs

8. **Migration preserved 838 active AP course pages** - individual detail files exist, but retired/cert codes need routing guards

9. **GitHub Pages deployment requires basePath configuration** - already implemented with `/wgu-atlas` prefix

10. **Product direction shifted to lead with catalog facts** - change-history layer should be secondary to official catalog information

## 4. Promotion candidates

**To `_internal/ATLAS_OPERATOR_CONTEXT.md`:**
- Credit units extraction status and UI priority
- Official Context Layer progress and strategy
- Build script path adaptation requirements
- Product direction decisions about catalog facts vs change-history

**To `_internal/PROJECT_CONTINUITY_ATLAS.md`:**
- Migration decisions and what was left behind
- Session-by-session architectural rationale
- Official Context Layer workstream methodology

**To `docs/DECISIONS.md`:**
- Product direction shift toward catalog-backed information
- Official Context Layer as first-class strategy
- Credit units as highest-value immediate improvement
- Accreditation page scope classification

**To `docs/ATLAS_SPEC.md`:**
- Official Context Layer architecture and workflow
- YouTube channel integration strategy
- Accreditation data extraction approach

## 5. Next best batch

Recommend reading these 8-10 files to continue answering remaining unknowns:

1. `_internal/archive/2026-03-doc-consolidation/docs_legacy/README.md` - Legacy documentation structure
2. `_internal/archive/2026-03-doc-consolidation/docs_legacy/SCRAPE_LOG.md` - Scraper architecture and validation
3. `_internal/archive/2026-03-doc-consolidation/docs_legacy/README_INTERNAL.md` - Parser eras and field definitions
4. `_internal/archive/2026-03-doc-consolidation/docs_legacy/website_design_plan.md` - Locked site design and build phases
5. `data/enrichment/README.txt` - Source enrichment process overview
6. `data/enrichment/source_enrichment_manifest.json` - Source enrichment state
7. `_internal/continuity_review/ARTIFACTS.md` - Continuity review artifacts
8. `_internal/continuity_review/review_method_plan.md` - Review methodology
9. `data/enrichment/outcomes/outcomes_links.json` - Outcomes page structured index
10. `data/enrichment/outcomes/bscs/` (directory) - ABET outcomes data files

These files will provide deeper insight into the data pipeline, parser architecture, and enrichment processes that underpin the current system.


# WGU Atlas Documentation Review Report - Batch 2

## 1. File-by-file summary

| File | Summary | Role | Status |
|------|---------|------|--------|
| `README.md` | Public-facing project overview with data provenance, tech stack, and disclaimer | Public documentation | **core** - main public entry point |
| `docs/ATLAS_SPEC.md` | Comprehensive implementation specification covering stack, data domains, artifacts, scripts, and known gaps | Technical specification | **core** - authoritative implementation reference |
| `_internal/PROJECT_CONTINUITY_ATLAS.md` | Compact project continuity companion doc with mission, surfaces, workstreams, and state model | Internal continuity | **supporting** - session context and state tracking |
| `_internal/WORKFLOW_SESSION_PROTOCOL.md` | Reusable workflow protocol for GPT+Codex collaboration with session shape and artifact rules | Process documentation | **supporting** - operational methodology |
| `src/app/about/page.tsx` | Static About page explaining Atlas purpose, coverage, and independence | Public-facing page | **core** - essential user-facing content |
| `src/app/methods/page.tsx` | Methods page detailing archive coverage, parser eras, validation, and caveats | Public-facing page | **core** - transparency and trust |
| `src/app/data/page.tsx` | Data download page with CSV/JSON exports and schema notes | Public-facing page | **core** - data accessibility |
| `src/app/proto/courses/page.tsx` | Prototype lab for course browse UI variants | Experimental | **experimental** - not production UI |
| `src/app/proto/compare/page.tsx` | Prototype lab for degree compare layout variants | Experimental | **experimental** - not production UI |
| `src/app/programs/[code]/LearningOutcomes.tsx` | Client component for displaying program learning outcomes with show/hide functionality | Production UI | **core** - active production component |

## 2. Questions answered

**Route/module maturity map:**
- **Core production routes:** `/`, `/courses`, `/programs`, `/schools`, `/timeline`, `/data`, `/methods`, `/about`
- **Experimental routes:** `/proto/courses`, `/proto/compare` (labeled as prototype lab, not production)
- **Active production components:** LearningOutcomes is a client component in the main program detail flow

**Proto surface status:**
- Both prototype routes are explicitly marked as "NOT PRODUCTION UI" with amber badges
- They serve as comparison tools for UI variants, not final implementations
- Course prototype uses degree-level classification from program rosters
- Compare prototype has broader universe than production (lab vs pilot families)

**Methods/about/data page purpose and maturity:**
- **Methods:** Core transparency page explaining data collection, validation, and caveats
- **About:** Core informational page explaining Atlas purpose and independence
- **Data:** Core accessibility page with downloadable datasets and schema documentation
- All three are mature, production-ready public-facing pages

**LearningOutcomes component status:**
- **Active production UI** - client component used in program detail pages
- Implements show/hide functionality for outcomes lists
- Displays official WGU-authored outcomes with source attribution
- Uses preview count of 3 items with expandable view

**Operator/continuity docs coverage:**
- **Well covered:** Implementation specs (ATLAS_SPEC.md), project continuity, workflow protocols
- **Not well covered:** Runtime/export pipeline details, script active-set, course detail data contract

## 3. Runtime/export understanding

**Current site surface priorities:**
- **Primary:** Course and program exploration with historical context
- **Secondary:** Data transparency and download capabilities
- **Tertiary:** Timeline and school-based navigation
- **Experimental:** UI prototypes for future development

**Public-facing supporting pages:**
- **Essential:** About, Methods, Data pages provide transparency and trust
- **Functional:** Download pages with schema documentation
- **Contextual:** Methods page explains validation and caveats

**What remains unclear about export/runtime pipeline:**
- How course detail data contracts are structured and validated
- What scripts are actively used vs legacy
- How search/browse/navigation runtime components interact
- What assets/downloads are core vs experimental
- Build process dependencies and runtime data flow specifics

## 4. Most important unique takeaways

1. **Prototype routes are explicitly experimental** - `/proto/courses` and `/proto/compare` are labeled as not production UI, serving as comparison tools rather than final implementations

2. **LearningOutcomes is active production component** - The component is a client-side implementation with show/hide functionality, actively used in program detail pages

3. **Data transparency is core priority** - The Data page provides comprehensive downloads with schema notes, emphasizing accessibility and transparency

4. **Methods page establishes trust** - Detailed explanation of archive coverage, validation process, and key caveats (including the 696→838 correction story)

5. **About page emphasizes independence** - Clear statement of independence from WGU while using public sources

6. **ATLAS_SPEC.md is comprehensive** - Contains detailed implementation facts, artifact registry, and known gaps

7. **Project continuity is well-maintained** - Internal docs track state models, workstreams, and unresolved items systematically

8. **Workflow protocol is reusable** - Session protocol provides structured approach for GPT+Codex collaboration

9. **Prototype labs serve comparison purpose** - Both course and compare prototypes allow side-by-side inspection of UI variants

10. **Schema documentation is accessible** - Data page includes field definitions and classification explanations for users

## 5. Promotion candidates

**To `_internal/ATLAS_OPERATOR_CONTEXT.md`:**
- Runtime/export pipeline understanding gaps
- Script active-set clarification
- Course detail data contract specifications
- Search/browse/navigation runtime interactions

**To `_internal/PROJECT_CONTINUITY_ATLAS.md`:**
- Prototype lab status and purpose
- LearningOutcomes component implementation details
- Data page schema documentation approach

**To `docs/ATLAS_SPEC.md`:**
- Already comprehensive - no immediate additions needed
- Could include prototype lab methodology if they become production

## 6. Next best batch

Recommend reading these 8-10 files to answer remaining unknowns about:

1. `src/lib/data.ts` - Data loading functions and contracts
2. `src/lib/types.ts` - TypeScript type definitions for data structures
3. `src/lib/programs.ts` - Program helper functions and classification
4. `src/components/courses/CourseExplorer.tsx` - Course browsing implementation
5. `src/components/home/HomeSearch.tsx` - Search functionality
6. `src/app/courses/[code]/page.tsx` - Course detail page implementation
7. `scripts/build_site_data.py` - Build script and data generation
8. `public/data/downloads/` (directory) - Downloadable dataset structure
9. `src/lib/families.ts` - Program family definitions for compare feature
10. `src/components/layout/Nav.tsx` - Navigation structure

These files will provide deeper insight into the runtime data contracts, search/browse functionality, and the relationship between frontend components and data sources.




# WGU Atlas Documentation Review Report - Batch 3

## 1. File-by-file summary

| File | Summary | Role | Status |
|------|---------|------|--------|
| `scripts/build_site_data.py` | Comprehensive Python script that builds all site-ready data artifacts from upstream catalog data | Core regeneration tool | **active core** - main data pipeline |
| `scripts/extract_program_enriched.py` | Extracts program descriptions, course rosters, and learning outcomes from 2026-03 catalog text | Supporting utility | **active supporting** - program enrichment |
| `scripts/extract_course_descriptions.py` | Extracts course descriptions from catalog "Courses" section | Supporting utility | **active supporting** - course enrichment |
| `src/lib/data.ts` | Central data loading functions with fallback logic for course details | Core runtime | **active core** - data access layer |
| `src/lib/types.ts` | TypeScript type definitions for all data structures | Core types | **active core** - type system |
| `src/app/courses/[code]/page.tsx` | Course detail page with rich historical data and program relationships | Production UI | **core** - main course page |
| `src/app/programs/[code]/page.tsx` | Program detail page with descriptions, rosters, and outcomes | Production UI | **core** - main program page |
| `src/app/courses/page.tsx` | Course explorer listing page with filtering and search | Production UI | **core** - course index |
| `src/app/programs/page.tsx` | Program explorer listing page | Production UI | **core** - program index |
| `src/lib/programs.ts` | Program classification and comparison utilities | Supporting library | **supporting** - shared program logic |

## 2. Questions answered

**Current export/runtime map:**
- **Scripts → Artifacts:** `build_site_data.py` generates all core JSON files in `public/data/` and `data/`
- **Runtime → Inputs:** Pages consume specific artifacts via `src/lib/data.ts` data loaders
- **Fallback system:** Course details try individual files first, fall back to canonical data

**Script active-set:**
- **Active core:** `build_site_data.py` (main pipeline)
- **Active supporting:** `extract_program_enriched.py`, `extract_course_descriptions.py` (enrichment)
- **No occasional utilities** in this batch

**Course detail data contract:**
- **Rich detail files:** 838 active AP courses with `programs_timeline`, `title_variant_detail`
- **Fallback files:** Retired/cert courses use `canonical_courses.json` with string fields
- **Normalization:** String fields converted to arrays at runtime

**Program detail data contract:**
- **Core data:** `programs.json` (196 programs) with status, versions, colleges
- **Enriched data:** `program_enriched.json` (114 active) with descriptions, rosters, outcomes
- **Roster structure:** `{term, code, title, cus}` arrays grouped by term

**Page data consumption:**
- **Course pages:** Load detail files, descriptions, program mappings
- **Program pages:** Load program data, enriched data, outcomes
- **Explorer pages:** Load card lists, program mappings, level classification

## 3. Export/runtime map

### Script → Output artifacts
- `build_site_data.py` → `data/canonical_courses.csv/json`, `data/named_events.csv/json`, `public/data/courses.json`, `public/data/courses/{code}.json`, `public/data/events.json`, `public/data/search_index.json`, `public/data/homepage_summary.json`
- `extract_program_enriched.py` → `public/data/program_enriched.json`
- `extract_course_descriptions.py` → `public/data/course_descriptions.json`

### Runtime → Input artifacts
- **Course detail page** → `public/data/courses/{code}.json` (primary) or `data/canonical_courses.json` (fallback), `public/data/course_descriptions.json`, `public/data/programs.json`
- **Program detail page** → `public/data/programs.json`, `public/data/program_enriched.json`, `public/data/official_resource_placements.json`
- **Course explorer** → `public/data/courses.json`, `public/data/programs.json`, `public/data/program_enriched.json`
- **Program explorer** → `public/data/programs.json`

## 4. Script active-set assessment

| Script | Classification | Rationale |
|--------|---------------|-----------|
| `build_site_data.py` | **active core** | Main data pipeline, generates all core artifacts |
| `extract_program_enriched.py` | **active supporting** | Program enrichment, used for program detail pages |
| `extract_course_descriptions.py` | **active supporting** | Course description extraction, used for course detail pages |
| `src/lib/data.ts` | **active core** | Central data access layer with fallback logic |
| `src/lib/types.ts` | **active core** | Type system foundation for all data structures |
| `src/lib/programs.ts` | **supporting** | Shared program utilities, used by multiple components |

## 5. Most important unique takeaways

1. **Two-tier course detail system:** Active AP courses have rich individual files with historical timelines; retired/cert courses use canonical fallback with string normalization

2. **Program enrichment pipeline:** Separate extraction scripts pull descriptions, rosters, and outcomes from catalog text, creating a 3-layer data model (core + enriched + placements)

3. **Fallback data loading:** `src/lib/data.ts` implements sophisticated fallback logic for course details, ensuring all 1,641 codes are accessible

4. **School lineage constants:** Static school data in `src/lib/data.ts` provides historical context without requiring additional data files

5. **Exact code matching:** Program roster comparison uses exact course code matching (no aliasing), matching lineage pipeline semantics

6. **Jaccard overlap metric:** Consistent overlap calculation used across lineage pipeline and compare feature

7. **Three-layer program data:** Core program data, enriched descriptions/rosters/outcomes, and official resource placements

8. **School slug resolution:** `getSchoolSlugByName()` provides canonical slug lookup for any historical school name

9. **Program heading to code mapping:** `getHeadingToProgramCode()` resolves degree headings to program codes with status-based precedence

10. **Type-driven contracts:** All data contracts are explicitly typed, ensuring consistency between scripts and runtime

## 6. Promotion candidates

**To `_internal/ATLAS_OPERATOR_CONTEXT.md`:**
- Course detail two-tier system explanation
- Program enrichment pipeline architecture
- Fallback data loading strategy
- School lineage constant management

**To `_internal/PROJECT_CONTINUITY_ATLAS.md`:**
- Program roster comparison contract
- Jaccard overlap metric consistency
- School slug resolution methodology

**To `docs/ATLAS_SPEC.md`:**
- Already comprehensive - no immediate additions needed
- Could include fallback data loading patterns if expanded

## 7. Remaining unknowns

After this batch, key unknowns remain around:

- **Search/browse/navigation runtime:** How search indexing works, pagination, filtering performance
- **Component architecture:** UI component structure, state management, client vs server components
- **Build process dependencies:** Next.js build configuration, static generation patterns
- **Asset management:** Image handling, download file structure, static asset organization
- **Error handling:** Data loading error states, fallback UI patterns
- **Performance optimization:** Large dataset handling, lazy loading strategies
- **Testing infrastructure:** Test coverage, data validation patterns

## 8. Next best batch

Recommend reading these 8-10 files to answer remaining unknowns:

1. `src/components/courses/CourseExplorer.tsx` - Course browsing implementation
2. `src/components/home/HomeSearch.tsx` - Search functionality
3. `src/components/programs/ProgramExplorer.tsx` - Program browsing
4. `src/lib/families.ts` - Program family definitions for compare feature
5. `src/app/compare/page.tsx` - Compare feature implementation
6. `next.config.ts` - Build configuration
7. `package.json` - Dependencies and scripts
8. `public/data/downloads/` (directory) - Downloadable dataset structure
9. `src/components/layout/Nav.tsx` - Navigation structure
10. `src/components/resources/RelevantResources.tsx` - Resource placement component

These files will provide insight into the frontend architecture, search/browse patterns, and build/runtime dependencies.



## Compact Structured Report

### 1. File-by-file summary

**src/lib/data.ts**
- Core data access layer that reads from public/data/ and data/ directories
- Provides unified APIs for courses, programs, schools, events, and official resources
- Core - central to all data consumption in the live app

**src/lib/types.ts**
- Defines all TypeScript interfaces for data contracts (CourseCard, CourseDetail, ProgramRecord, etc.)
- Establishes the runtime type system that components consume
- Core - defines the contracts everything else depends on

**src/lib/families.ts**
- Implements the compare-family feature with curated pilot families (BSSWE tracks, MSDA tracks)
- Contains v1 compare payload builder and two-name model (canonical_name vs index_name)
- Supporting - enables compare functionality but not central to core browsing

**src/components/courses/CourseExplorer.tsx**
- Interactive course filtering UI with college/level/degree filters and search
- Client-side filtering of 1,646 courses with pagination
- Core - primary course discovery interface

**src/components/home/HomeSearch.tsx**
- Global search component using public/data/search_index.json (1,842 entries)
- Client-side fuzzy search with instant results and "see all" link
- Core - main search entry point

**src/components/layout/Nav.tsx**
- Main navigation with primary links (Home, Courses, Degrees, Colleges, Compare, About)
- Uses Next.js usePathname for active state highlighting
- Core - navigation backbone

**src/app/courses/[code]/page.tsx**
- Server-side rendered course detail page with rich data from individual JSON files
- Handles both active AP courses (838 files) and fallback to canonical_courses.json
- Core - primary course detail experience

**src/components/resources/RelevantResources.tsx**
- Sidebar component that displays official WGU resources grouped by type
- Consumes public/data/official_resource_placements.json
- Supporting - enhances detail pages but not essential to core browsing

**public/data/homepage_summary.json**
- Pre-computed summary statistics and recent changes for homepage display
- Contains 108 editions, 1,594 total course codes, 114 active programs
- Core - powers homepage data visualization

**public/data/downloads/**
- Static CSV/JSON exports for canonical_courses, events, and title variants
- Public dataset artifacts for external consumption
- Existing but not central - downloadable artifacts

### 2. Questions answered

**Current runtime data contract for course detail pages:**
- Primary: public/data/courses/{code}.json (838 active AP files) with programs_timeline, title variants
- Fallback: data/canonical_courses.json (all 1,641 codes) for retired/cert-only
- Normalizes string fields to arrays (observed_titles, current_programs, colleges_seen)

**Current search/browse/navigation structure:**
- Search: HomeSearch.tsx → public/data/search_index.json (1,842 entries)
- Browse: CourseExplorer.tsx filters courses by college/level/degree with pagination
- Navigation: Nav.tsx provides 6 primary routes, uses Next.js routing

**Role of RelevantResources in the live app:**
- Sidebar component on program/course detail pages
- Displays official WGU resources grouped by outcomes, accreditation, specializations, guides
- Consumes public/data/official_resource_placements.json with placement_mode "sidebar"

**Compare-family/runtime assumptions from families.ts:**
- V1 compare is 2-way only, pilot families: BSSWE tracks and MSDA tracks
- Two-name model: canonical_name (body name) vs index_name (catalog index name with track qualifiers)
- Uses ProgramEnriched.roster from public/data/program_enriched.json for course comparison

**Role of homepage_summary.json:**
- Pre-computed statistics for homepage display (edition counts, course/program totals, recent changes)
- Powers "Recent Version Changes", "Newest Programs", "Recent Course Additions" sections
- Contains curated major events preview (10 events)

**Role and maturity of downloadable datasets:**
- public/data/downloads/ contains static CSV/JSON exports
- canonical_courses.csv/json, curated_major_events.json, named_events.csv/json, title_variant_classification.csv
- Mature artifacts for external consumption, not used by live app

### 3. Runtime contract map

**runtime file/component → input artifact(s) / type(s)**

- CourseExplorer → public/data/courses.json (CourseCard[]), public/data/programs.json (ProgramRecord[]), data/canonical_courses.json (fallback)
- HomeSearch → public/data/search_index.json (SearchEntry[])
- Nav → (no external artifacts, static routes)
- Course detail page → public/data/courses/{code}.json (CourseDetail) OR data/canonical_courses.json (fallback)
- RelevantResources → public/data/official_resource_placements.json (OfficialResourcePlacement[])
- Homepage → public/data/homepage_summary.json (HomepageSummary)
- Compare view → public/data/program_enriched.json (ProgramEnriched), public/data/programs.json (ProgramRecord)

**helper/type file → what contract it defines or mediates**

- src/lib/types.ts → All runtime data contracts (CourseCard, CourseDetail, ProgramRecord, etc.)
- src/lib/data.ts → Data access contracts and normalization logic
- src/lib/families.ts → Compare payload contracts and family definitions
- src/lib/programs.ts → Program classification and roster comparison contracts

### 4. Live app vs supporting/existing artifact distinction

**Definitely live and important:**
- CourseExplorer, HomeSearch, Nav, Course detail pages
- public/data/courses.json, search_index.json, programs.json, homepage_summary.json
- src/lib/data.ts, src/lib/types.ts

**Supporting but secondary:**
- RelevantResources (enhances detail pages)
- official_resource_placements.json (resource sidebar data)
- families.ts (compare feature)

**Existing but not clearly central:**
- public/data/downloads/ (static exports, not consumed by app)
- canonical_courses.json in data/ (fallback only)

**Unclear:**
- Some internal data/ files may be build artifacts not directly consumed

### 5. Most important unique takeaways

1. **Dual data source pattern**: Active AP courses use individual JSON files (838 files), retired/cert use canonical fallback
2. **Client-side filtering**: CourseExplorer does all filtering in-browser, no API calls
3. **Two-name model in compare**: canonical_name (body) vs index_name (catalog index with track qualifiers)
4. **Pre-computed homepage data**: homepage_summary.json contains all stats, no runtime computation
5. **Static resource placements**: Official WGU resources are curated in official_resource_placements.json
6. **Search index is separate**: search_index.json (1,842 entries) distinct from courses.json (1,646 entries)
7. **Program families are curated**: Only 2 pilot families (BSSWE, MSDA) with explicit track definitions
8. **School lineage is static**: SchoolRecord definitions in families.ts, not derived from data
9. **Downloadable datasets are exports**: public/data/downloads/ not consumed by live app
10. **Version 1 compare constraints**: 2-way only, exact code matching, no historical course data

### 6. Promotion candidates

**_internal/ATLAS_OPERATOR_CONTEXT.md:**
- Dual data source pattern for courses (individual vs canonical fallback)
- Client-side filtering architecture in CourseExplorer
- Two-name model details for compare feature

**_internal/PROJECT_CONTINUITY_ATLAS.md:**
- Runtime data contract map showing component → artifact relationships
- Live vs supporting artifact distinction
- Homepage pre-computation strategy

**docs/ATLAS_SPEC.md:**
- Search index structure and separation from courses.json
- Official resource placement system
- Program family curation approach

### 7. Remaining unknowns

1. **Program detail pages**: How they consume program_enriched.json and display rosters/outcomes
2. **Compare view implementation**: Actual UI components and how they use buildComparePayload
3. **School pages**: How they aggregate courses and programs by school
4. **Timeline page**: What data it consumes and how it visualizes events
5. **Methods page**: What content it displays and data sources
6. **Build process**: How public/data/ files are generated from data/ sources
7. **Search index generation**: How search_index.json is created and maintained
8. **Official resource curation**: How official_resource_placements.json is maintained

### 8. Need for another batch

**Yes, one more batch is needed.**

**Recommended next 8–10 files:**
1. src/app/programs/[code]/page.tsx (program detail page)
2. src/app/compare/page.tsx (compare landing/selection)
3. src/app/compare/[family]/page.tsx (compare view implementation)
4. src/app/schools/[slug]/page.tsx (school detail page)
5. src/app/timeline/page.tsx (timeline page)
6. src/app/methods/page.tsx (methods page)
7. src/components/programs/ProgramExplorer.tsx (if exists)
8. src/lib/programs.ts (program utilities and classification)
9. scripts/ directory files (build process)
10. public/data/program_enriched.json (sample structure)

This batch would complete the picture of how the live app consumes data across all major views and clarify the build process.


# Repo-Explainer Report: Runtime Contracts & Live Surface Maturity

## 1. File-by-file summary

### `src/app/programs/[code]/page.tsx`
- **Summary**: Full program detail page with static generation for all program codes. Renders degree metadata, description, learning outcomes, and course roster with term grouping.
- **Role**: Core live surface for program exploration. Generates static pages at build time via `generateStaticParams`.
- **Classification**: **core live surface**

### `src/app/compare/page.tsx`
- **Summary**: Comparison tool for two active programs. Loads all programs and enriched data, filters to active programs with rosters, passes lean enriched data to client component.
- **Role**: Supporting live surface for degree comparison. Uses client-side `Suspense` for dynamic comparison logic.
- **Classification**: **supporting live surface**

### `src/app/schools/[slug]/page.tsx`
- **Summary**: School detail page with static generation for all school slugs. Shows current/retired programs, active courses, college history, and recent changes.
- **Role**: Core live surface for school exploration. Generates static pages at build time.
- **Classification**: **core live surface**

### `src/app/timeline/page.tsx`
- **Summary**: Timeline view of catalog events with curated major events and all threshold-crossing transitions. Renders severity scores, event types, and summaries.
- **Role**: Supporting live surface for catalog history exploration. No static generation - renders all events dynamically.
- **Classification**: **supporting live surface**

### `src/app/methods/page.tsx`
- **Summary**: Static informational page about data collection methodology, parser eras, validation, and caveats. No dynamic data loading.
- **Role**: Documentation/supporting content. Purely informational with no runtime data dependencies.
- **Classification**: **supporting content**

### `src/components/programs/ProgramExplorer.tsx`
- **Summary**: Client-side program explorer with filtering by college, level, and search. Uses pagination and supports retired program inclusion.
- **Role**: Utility component for program discovery. Client-side filtering with no server-side data fetching.
- **Classification**: **utility component**

### `src/lib/programs.ts`
- **Summary**: Shared program classification and comparison utilities. Provides degree level classification and roster comparison logic.
- **Role**: Core library for program data processing. Used by both server and client contexts.
- **Classification**: **core utility library**

### `src/lib/data.ts`
- **Summary**: Data access layer loading JSON files from `public/data/`. Provides functions for courses, programs, events, and enriched data.
- **Role**: Central data access abstraction. Handles fallbacks and normalization for different data sources.
- **Classification**: **core data layer**

### `scripts/build_site_data.py`
- **Summary**: Python script that builds all site-ready data artifacts: title variant classification, canonical courses, named events, and static exports.
- **Role**: Build process generator. Creates the JSON files consumed by the live application.
- **Classification**: **build process script**

## 2. Questions answered

### Program detail page runtime contract
- **Input**: Program code from URL parameter
- **Data sources**: `programs.json` (metadata), `program_enriched.json` (description, roster, outcomes)
- **Static generation**: All program codes via `generateStaticParams()`
- **Runtime**: Server-side rendering with client-side interactivity for outcomes

### School detail page runtime contract
- **Input**: School slug from URL parameter
- **Data sources**: `programs.json` (filtered by school), `courses.json` (filtered by college), `homepage_summary.json` (recent changes)
- **Static generation**: All school slugs via `generateStaticParams()`
- **Runtime**: Server-side rendering with client-side expandable sections

### Timeline page runtime contract
- **Input**: None (static page)
- **Data sources**: `events.json` (all catalog events), `curated_major_events.json` (curated subset)
- **Static generation**: None - renders all events dynamically
- **Runtime**: Client-side rendering with severity-based styling

### Compare page runtime role
- **Input**: Two program codes selected via client-side UI
- **Data sources**: `programs.json` (filtered to active programs), lean enriched data (roster only)
- **Static generation**: None - fully client-side comparison
- **Runtime**: Server-side data loading with client-side comparison logic

### What `build_site_data.py` generates
- **Title variant classification**: CSV/JSON with course title change analysis
- **Canonical courses**: Complete course intelligence table (CSV/JSON)
- **Named events**: Catalog event layer with curated major events
- **Static exports**: `courses.json`, `events.json`, `search_index.json`, `homepage_summary.json`
- **Individual course files**: 838 course detail JSON files in `public/data/courses/`

### Methods page role
- **Role**: Supporting informational content
- **Classification**: **supporting content** (not a core live surface)
- **Purpose**: Documents data collection methodology, parser eras, validation, and caveats

## 3. Runtime contract map

### Runtime files/pages/components → input artifacts
- `programs/[code]/page.tsx` → `programs.json`, `program_enriched.json`
- `schools/[slug]/page.tsx` → `programs.json`, `courses.json`, `homepage_summary.json`
- `compare/page.tsx` → `programs.json`, `program_enriched.json` (roster subset)
- `timeline/page.tsx` → `events.json`, `curated_major_events.json`
- `methods/page.tsx` → none (static content)
- `ProgramExplorer.tsx` → `programs.json` (via props)
- `src/lib/data.ts` → all `public/data/*.json` files

### Scripts → output artifacts
- `scripts/build_site_data.py` → `canonical_courses.csv/json`, `title_variant_classification.csv/json`, `named_events.csv/json`, `curated_major_events.json`, `courses.json`, `events.json`, `search_index.json`, `homepage_summary.json`, individual course files

## 4. Live surface maturity snapshot

- **Program detail**: **core live surface** - fully static generation, complete data integration
- **School detail**: **core live surface** - fully static generation, comprehensive school view
- **Timeline**: **supporting live surface** - dynamic rendering, focused on event exploration
- **Compare**: **supporting live surface** - client-side comparison tool with filtered data
- **Methods**: **supporting content** - informational page with no data dependencies

## 5. Most important unique takeaways

1. **Static generation strategy**: Program and school pages use `generateStaticParams()` for all possible routes, creating fully pre-rendered pages at build time
2. **Data layer abstraction**: `src/lib/data.ts` provides a clean abstraction over `public/data/` JSON files with fallbacks and normalization
3. **Build process centrality**: `build_site_data.py` is the single source of truth for generating all runtime data artifacts
4. **Enriched data separation**: `program_enriched.json` contains additional metadata (descriptions, rosters, outcomes) beyond basic program metadata
5. **Client-side filtering**: Program explorer and compare functionality use client-side filtering rather than server-side data fetching
6. **Event-driven architecture**: Timeline and homepage use curated event data for catalog change visualization
7. **Individual course files**: 838 active AP courses have individual JSON files in `public/data/courses/` for detailed views
8. **Fallback strategy**: Course detail uses individual files first, falls back to canonical courses for retired/cert codes
9. **Lean data for comparison**: Compare page uses minimal enriched data (roster only) to reduce bundle size
10. **Static content separation**: Methods page is purely informational with no runtime data dependencies

## 6. Promotion candidates

### `_internal/ATLAS_OPERATOR_CONTEXT.md`
- Add sections on static generation strategy for program/school pages
- Document the data layer abstraction pattern in `src/lib/data.ts`
- Include build process flow showing `build_site_data.py` → `public/data/` → runtime

### `_internal/PROJECT_CONTINUITY_ATLAS.md`
- Document the separation between core live surfaces (program/school detail) and supporting surfaces (timeline/compare)
- Add runtime contract specifications for each major page
- Include data artifact generation pipeline documentation

### `docs/ATLAS_SPEC.md`
- Add runtime architecture section describing the static generation + client-side filtering pattern
- Document the data layer contracts and fallback strategies
- Include build process specifications for `build_site_data.py`

## 7. Final remaining unknowns

1. **Program lineage integration**: How program lineage data from `data/lineage/` connects to the live application
2. **Official resource placements**: Runtime usage of `official_resource_placements.json` beyond sidebar rendering
3. **Course descriptions**: How `course_descriptions.json` is utilized in the live application
4. **Search functionality**: Implementation details of search using `search_index.json`
5. **Learning outcomes rendering**: How outcomes data from `program_enriched.json` is processed and displayed
6. **Event severity calculation**: Algorithm used to compute severity scores for catalog events
7. **Title variant classification**: Runtime usage of title variant data beyond the classification CSV
8. **Build process triggers**: When and how `build_site_data.py` is executed in the development workflow

## 8. Is repo-explainer complete enough?

**Yes, enough to proceed to consolidation later**

The current batch has successfully identified the core runtime contracts, data flow, and live surface architecture. The remaining unknowns are implementation details that can be addressed during consolidation rather than requiring additional exploration batches.

## 9. Large-file note

- `public/data/program_enriched.json` was skipped as too large
- `public/data/events.json` was skipped by instruction
- Conclusions were inferred from runtime code that loads/consumes these files instead of reading the files directly




# WGU Atlas Standalone-Readiness Audit

## 1. What was migrated into wgu-atlas

**Core website data artifacts:**
- `public/data/courses.json` (1,646 course cards)
- `public/data/courses/{code}.json` (838 individual course detail files)
- `public/data/events.json` (41 catalog events)
- `public/data/search_index.json` (1,842 search entries)
- `public/data/homepage_summary.json` (homepage module data)
- `public/data/program_enriched.json` (114 program descriptions/rosters/outcomes)
- `public/data/programs.json` (196 program records)
- `public/data/official_resource_placements.json` (116 curated resource placements)

**Canonical data artifacts:**
- `data/canonical_courses.csv` and `.json` (1,646 course intelligence table)
- `data/named_events.csv` and `.json` (41 events)
- `data/title_variant_classification.csv` and `.json` (167 classified title variants)
- `data/curated_major_events.json` (10 curated events)
- `data/program_history.csv` (196 program lifecycle records)

**Build infrastructure:**
- `scripts/build_site_data.py` (Python script to regenerate all site data)
- `scripts/extract_program_enriched.py` (extract program descriptions/rosters)
- `scripts/bootstrap_source_enrichment_manifest.py` (enrichment manifest builder)

**Documentation:**
- `docs/README_INTERNAL.md` (scraper architecture and validation)
- `docs/SCRAPE_LOG.md` (archive coverage and build milestones)
- `docs/website_design_plan.md` (site design and build phases)

## 2. What was intentionally left behind

**Raw data sources (external dependency):**
- `data/raw_catalog_pdfs/` (source PDFs - many GB)
- `data/raw_catalog_texts/` (extracted text files)
- `outputs/raw_course_rows/` (per-edition raw extractions)
- `outputs/program_names/` (per-edition parser blocks)
- `outputs/anomalies/` (parser anomaly logs)

**Parser and pipeline code:**
- `src/wgu_reddit_analyzer/` (entire Reddit Analyzer Python package)
- `WGU_catalog/parse_catalog_v11.py` (catalog parser)
- `WGU_catalog/build_change_tracking.py` (change tracking generator)
- `WGU_catalog/build_edition_diffs.py` (edition diffs generator)
- All other parser scripts and utilities

**Database and infrastructure:**
- `wgu_reddit.db` (SQLite database)
- `db/` (database migrations and schema)
- `scripts/` (Reddit acquisition scripts)
- `notebooks/` (research notebooks)
- `monitoring/` (application health monitoring)

**Legacy and unrelated content:**
- `site/` (old Hugo site build)
- `site.BACKUP_*` (old site backups)
- `llm-sql/` (unrelated research tooling)
- `monthly_report/` (Reddit Analyzer reporting)
- `WGU_catalog/instructor_directory/` (separate pipeline)
- `WGU_catalog/geomapping/` (instructor geomapping)
- `_demo/`, `archive_legacy/` (legacy/archived material)

## 3. Current external dependencies / non-standalone points

**Critical external dependency:**
- **Upstream catalog data**: `build_site_data.py` requires access to `wgu-reddit/WGU_catalog/outputs/` directory containing:
  - `course_history.csv` (496 KB)
  - `program_history.csv` (40 KB) 
  - `courses_2026_03.csv` (200 KB)
  - `certs_2026_03.csv` (4 KB)
  - `edition_diffs_full.json` (184 KB)
  - `edition_diffs_events.json` (24 KB)
  - `course_index_v10.json` (59 MB - largest file)

**Path configuration:**
- `build_site_data.py` uses environment variables `WGU_REDDIT_PATH` and `WGU_ATLAS_DATA` to locate upstream data
- Script paths are hardcoded relative to `wgu-reddit` structure

**Large file management:**
- `course_index_v10.json` (59 MB) is intentionally excluded from git but required for regeneration
- Must be accessed via external path or git-LFS

**Parser version dependency:**
- Data generation depends on `parse_catalog_v11.py` from upstream repo
- No parser code migrated to `wgu-atlas`

## 4. Standalone-readiness gaps

### Must-have to stand alone:
1. **Parser code migration**: Need to migrate `parse_catalog_v11.py` and supporting scripts
2. **Raw catalog archive**: Need to include PDF/text archives for self-contained regeneration
3. **Build script adaptation**: `build_site_data.py` needs to work without external path dependencies
4. **Large file strategy**: Need solution for `course_index_v10.json` (59 MB) - either git-LFS or external service

### Nice-to-have:
1. **Automated testing**: Validation scripts for data integrity
2. **Documentation updates**: Keep `README_INTERNAL.md` synchronized with current state
3. **CI/CD pipeline**: Automated build and deployment workflow
4. **Data validation tools**: Scripts to verify data consistency

### Should remain external:
1. **Reddit Analyzer pipeline**: Separate research project, not core to catalog site
2. **Instructor directory**: Separate data pipeline
3. **Geomapping**: Separate research project
4. **Monthly reporting**: Separate operational concern

## 5. Likely bring-over candidates

### For canon docs:
- **Parser documentation**: Move parser architecture docs from `wgu-reddit` to `docs/` in `wgu-atlas`
- **Validation methodology**: Document how catalog data is validated and trusted
- **Archive coverage notes**: Document which editions are missing and why

### For scripts:
- **Parser code**: `parse_catalog_v11.py` and supporting utilities
- **Validation scripts**: Scripts that verify data integrity
- **Archive management**: Scripts for downloading/processing new catalog editions

### For data artifacts:
- **Raw catalog archive**: PDFs and extracted text for self-contained regeneration
- **Parser outputs**: Raw parser outputs for debugging and validation
- **Historical snapshots**: Previous versions of data artifacts for rollback

### For internal archive/support docs:
- **Parser development history**: Important decisions about parser evolution
- **Archive processing notes**: Notes about catalog format changes over time
- **Validation test cases**: Examples of edge cases and how they're handled

## 6. Risks of over-bringing things in

**Repository bloat:**
- Raw PDF archive (many GB) would make cloning slow
- Large parser outputs could bloat git history
- Research notebooks and experimental code add noise

**Maintenance burden:**
- Parser code requires ongoing maintenance and testing
- Raw data processing adds complexity to CI/CD
- Multiple data formats increase chance of inconsistency

**Scope creep:**
- Reddit Analyzer pipeline is a separate project
- Instructor directory and geomapping are unrelated features
- Monthly reporting and monitoring are operational concerns

**Security concerns:**
- Credentials and API keys from upstream repo
- Database files with potentially sensitive data
- Configuration files with environment-specific settings

## 7. Standalone judgment

**Standalone enough for maintenance: YES**
- All current site functionality works with committed data artifacts
- No immediate dependencies on external repos for basic operation
- Build process is documented and reproducible

**Standalone enough for rebuild/regeneration: NO**
- Cannot regenerate data without access to upstream `wgu-reddit` outputs
- Parser code and raw archives not included
- Large file dependencies not resolved

**Standalone enough for future extension: MOSTLY**
- Can extend frontend functionality without external dependencies
- Adding new data sources would require careful integration
- Parser modifications require upstream repo access

## 8. Best next bounded task

**Priority 1: Create self-contained data regeneration capability**
- Migrate essential parser code (`parse_catalog_v11.py`)
- Add raw catalog archive (selective - only recent editions)
- Adapt `build_site_data.py` to work without external path dependencies
- Implement large file strategy for `course_index_v10.json`

**Priority 2: Documentation and validation**
- Update `README.md` with clear regeneration instructions
- Add data validation scripts
- Document external dependencies and how to resolve them

**Priority 3: Infrastructure improvements**
- Set up automated testing for data integrity
- Create CI/CD pipeline for automated regeneration
- Implement proper versioning for data artifacts

The most critical gap is the inability to regenerate data without external dependencies. This should be addressed before considering the repo truly standalone.


Based on my analysis of the specified files, here's the comprehensive operational report:

## 1. File-by-file summary

### Script Files

**scripts/add_program_history_enrichment.py**
- 1–3 sentence summary: Adds importance and site_worthy fields from program_history_enrichment.json to corresponding entries in program_history.json. Uses start_edition/end_edition keys to match enrichment data to history entries.
- Current role: Active supporting - enriches lineage artifacts with importance scoring
- Classification: active supporting

**scripts/build_program_lineage_artifacts.py**
- 1–3 sentence summary: Builds lineage review artifacts (program_transition_universe.csv and program_link_candidates.json) with full historical backfill by default. Computes course overlap using removed program roster at boundary start_edition and added program roster at boundary end_edition.
- Current role: Active core - generates the primary lineage artifacts that feed downstream processing
- Classification: active core

**scripts/compare_program_courses.py**
- 1–3 sentence summary: Stage 2 lineage enrichment that loads Stage 1 lineage events, normalizes JSON formatting drift, compares from_program/to_program course rosters, and emits pair-level overlap and diffs. Handles missing catalog sources gracefully.
- Current role: Active core - performs the critical course roster comparison for lineage analysis
- Classification: active core

**scripts/generate_program_history_artifacts.py**
- 1–3 sentence summary: Stage 3 deterministic transform that converts data/program_lineage_enriched.json into data/program_history.json. Builds program-centric history by aggregating lineage events.
- Current role: Active core - final transformation to program history format
- Classification: active core

**scripts/generate_program_history_enrichment.py**
- 1–3 sentence summary: Builds the final Atlas-ready event-level program history enrichment artifact. Infers importance and site_worthy fields based on transition type and overlap metrics. Attempts to load Stage 1 metadata for title information.
- Current role: Active core - generates the final enrichment artifact used by the site
- Classification: active core

**scripts/generate_content_map.js**
- 1–3 sentence summary: Produces a single proofreading document of all visible text content on WGU Atlas, organized by page/section with source file:line references. Used for content review and documentation.
- Current role: Occasional utility - content auditing and documentation generation
- Classification: occasional utility

### App Shell Files

**src/app/layout.tsx**
- 1–3 sentence summary: Root layout component that provides global metadata (title template "%s | WGU Atlas", description) and wraps children with Nav and Footer components. Loads homepage summary data for Footer.
- Current role: Active core - defines the global app shell structure
- Classification: active core

**src/components/layout/Footer.tsx**
- 1–3 sentence summary: Footer component with three-column layout showing WGU Atlas branding, data information (catalog coverage, data date), and disclaimer. Links to methods and data pages.
- Current role: Active core - provides consistent site-wide footer with data attribution
- Classification: active core

**src/lib/basePath.ts**
- 1–3 sentence summary: Exports BASE_PATH constant for client-side asset fetches and plain <a> download links. Reads from NEXT_PUBLIC_BASE_PATH environment variable, defaults to empty string for local dev.
- Current role: Active supporting - handles deployment path configuration
- Classification: active supporting

## 2. Script active-set summary

| file | classification | produces/supports | upstream/site-runtime/uncertain |
|------|---------------|-------------------|--------------------------------|
| add_program_history_enrichment.py | active supporting | Adds importance/site_worthy to program_history.json | upstream-only |
| build_program_lineage_artifacts.py | active core | program_transition_universe.csv, program_link_candidates.json | upstream-only |
| compare_program_courses.py | active core | program_lineage_enriched.json | upstream-only |
| generate_program_history_artifacts.py | active core | program_history.json | upstream-only |
| generate_program_history_enrichment.py | active core | program_history_enrichment.json | upstream-only |
| generate_content_map.js | occasional utility | content_map.txt | site-runtime-related |

## 3. App shell / deployment notes

**Global shell assumptions:**
- Uses Next.js App Router with RootLayout pattern
- Global metadata defined in layout.tsx with title template "%s | WGU Atlas"
- Three-tier layout: Nav (top) → Main (flex-1) → Footer (bottom)
- Tailwind CSS for styling with slate color scheme
- Data flows from getHomepageSummary() to Footer component

**Deployment/path assumptions:**
- BASE_PATH configured via NEXT_PUBLIC_BASE_PATH environment variable
- GitHub Actions workflow sets BASE_PATH=/wgu-atlas for deployment
- Local development uses empty BASE_PATH
- Client-side fetches and plain <a> links must use BASE_PATH constant
- Next.js Link components automatically prepend basePath

**Static export / GitHub Pages / route behavior:**
- BASE_PATH support enables subdirectory deployment (GitHub Pages)
- Routes: /, /courses, /programs, /schools, /compare, /about, /timeline, /methods, /data
- Dynamic routes: /courses/[code], /programs/[code], /schools/[slug]
- Footer links to /methods and /data are relative (no BASE_PATH needed for Next.js Links)

## 4. Most important operator takeaways

1. **Lineage pipeline is 3-stage**: build_program_lineage_artifacts.py → compare_program_courses.py → generate_program_history_artifacts.py → generate_program_history_enrichment.py
2. **Course overlap is first-class**: Uses last-removed and first-added rosters at boundary editions for accurate overlap calculation
3. **BASE_PATH is critical for deployment**: Must be set to /wgu-atlas for GitHub Pages, empty for local dev
4. **Data separation**: Scripts are upstream-only, site components are runtime-only
5. **Content map is key documentation**: generate_content_map.js provides complete content audit with source references
6. **Footer data attribution**: Shows catalog coverage (2017-01 → 2026-03) and data date
7. **Importance scoring**: generate_program_history_enrichment.py infers importance based on transition type and overlap metrics
8. **Error handling**: Scripts handle missing catalog sources gracefully with notes
9. **JSON normalization**: compare_program_courses.py handles LLM formatting drift in lineage events
10. **GitHub Pages ready**: BASE_PATH configuration supports subdirectory deployment

## 5. What still remains unclear after this batch

1. **Data source dependencies**: Need to understand the catalog archive structure and how scripts access WGU_catalog data
2. **Build pipeline orchestration**: How these scripts are chained together in CI/CD
3. **Data validation**: What validation occurs between pipeline stages
4. **Error handling in production**: How script failures are handled in the build process
5. **Performance characteristics**: How long the lineage pipeline takes to run
6. **Data freshness**: How often the catalog archive is updated and how that triggers rebuilds

## 6. Need for another explainer batch

**Yes** - recommend the next exact files:

1. **scripts/build_site_data.py** - to understand how site data is generated from lineage artifacts
2. **src/lib/data.ts** - to understand data loading and API layer
3. **next.config.ts** - to understand Next.js configuration and build settings
4. **package.json** - to understand dependencies, scripts, and build commands
5. **.github/workflows/** files - to understand CI/CD pipeline and deployment process

This batch would complete the picture of how lineage data flows from scripts to the live site.


Based on my analysis of the specified files, here's the comprehensive operational report:

## 1. File-by-file summary

### Script Files

**scripts/generate_content_map.js**
- 1–3 sentence summary: Produces a single proofreading document of all visible text content on WGU Atlas, organized by page/section with source file:line references. Used for content review and documentation.
- Current role: Occasional utility - content auditing and documentation generation
- Classification: occasional utility

**content_map.txt**
- 1–3 sentence summary: Generated content map showing all visible text with source locations, used for proofreading and content audit purposes
- Current role: Reference artifact - comprehensive content documentation
- Classification: occasional utility

### App Shell Files

**src/app/page.tsx**
- 1–3 sentence summary: Homepage component with hero section, search bar, school cards, orientation paragraph, compare callout, and attribution. Uses HomeSearch and SchoolCards components.
- Current role: Active core - defines the main landing page structure and navigation
- Classification: active core

**src/components/home/EventPreview.tsx**
- 1–3 sentence summary: Displays curated timeline events with type labels, date ranges, and links to full timeline. Shows up to 4 events with hover effects.
- Current role: Active supporting - provides timeline preview functionality
- Classification: active supporting

**src/components/home/SchoolCards.tsx**
- 1–3 sentence summary: Renders four college cards with descriptions, colors, and explore links. Static component with hardcoded school data.
- Current role: Active core - provides primary navigation to college pages
- Classification: active core

**src/app/schools/page.tsx**
- 1–3 sentence summary: Schools index page showing four college cards with descriptions, historical names, and degree/course counts. Links to individual school detail pages.
- Current role: Active core - serves as the main college browsing interface
- Classification: active core

**src/components/compare/CompareSelector.tsx**
- 1–3 sentence summary: Interactive degree comparison selector with filters (college, level, search), two-step selection process, and sibling logic for degree pairing.
- Current role: Active core - enables the degree comparison functionality
- Classification: active core

**src/components/compare/CompareView.tsx**
- 1–3 sentence summary: Lane-based visual comparison view with sticky headers, term dividers, and course cards showing shared/unique courses between selected degrees.
- Current role: Active core - renders the actual degree comparison visualization
- Classification: active core

### Configuration Files

**next.config.ts**
- 1–3 sentence summary: Next.js configuration with static export output, basePath set to "/wgu-atlas", and unoptimized images for GitHub Pages deployment.
- Current role: Active core - defines build and deployment configuration
- Classification: active core

**package.json**
- 1–3 sentence summary: Project dependencies and scripts for Next.js 15.2.3, React 19, TypeScript, ESLint, and build commands (dev, build, start, lint).
- Current role: Active core - defines project dependencies and build commands
- Classification: active core

**.github/workflows/deploy.yml**
- 1–3 sentence summary: GitHub Actions workflow for deploying to GitHub Pages with Node.js 20, npm build with NEXT_PUBLIC_BASE_PATH=/wgu-atlas, and Pages deployment.
- Current role: Active core - automates deployment to GitHub Pages
- Classification: active core

## 2. Content map assessment

**What generate_content_map.js does:**
- Generates a comprehensive content audit document (content_map.txt) showing all visible text across the site
- Includes source file:line references for every piece of content
- Organized by page/section with hierarchical structure
- Used for proofreading and content review purposes

**What content_map.txt is useful for:**
- Content auditing and proofreading reference
- Finding source locations for any visible text
- Documentation of site content structure
- Quality assurance for content changes

**Should it be treated as a standing operator/reference artifact:**
Yes - it serves as a critical reference for content management and should be regenerated when content changes

**Large-file/token-budget note needed:**
Yes - the content map is substantial (65K+ tokens) and should be noted as a large generated artifact that may impact token budgets in future documentation workflows

## 3. Homepage / school-browse / compare summary

**Homepage (/):**
- **Structure:** Hero section with search, school cards, orientation paragraph, compare callout, attribution
- **Role:** Primary landing page and content discovery hub
- **Stability:** Core - stable structure, unlikely to change significantly

**School index (/schools):**
- **Structure:** Four college cards with descriptions, historical names, degree/course counts
- **Role:** Main college browsing interface and navigation hub
- **Stability:** Core - fundamental navigation component, stable

**Compare selector/view (/compare):**
- **Structure:** Two-step selector with filters, followed by lane-based visual comparison
- **Role:** Advanced degree comparison functionality with detailed course overlap analysis
- **Stability:** Core - sophisticated feature that's central to site value proposition

## 4. Build / deploy orchestration notes

**Build command assumptions:**
- `npm run build` with `NEXT_PUBLIC_BASE_PATH=/wgu-atlas` environment variable
- Static export output mode for GitHub Pages compatibility
- TypeScript compilation and ESLint validation

**Export/deploy assumptions:**
- Static site generation (output: "export")
- GitHub Pages deployment with subdirectory structure
- Unoptimized images for simplicity and compatibility

**GitHub Pages / basePath assumptions:**
- basePath set to "/wgu-atlas" for subdirectory deployment
- All client-side fetches and plain <a> links must use BASE_PATH constant
- Next.js Link components automatically prepend basePath

**Operator awareness:**
- Deployment triggered by push to main branch
- Single concurrent deployment allowed
- Node.js 20 runtime required
- npm cache used for faster builds

## 5. Most important operator takeaways

1. **GitHub Pages deployment is core** - basePath configuration and static export are critical for proper subdirectory hosting
2. **Content map is a large generated artifact** - should be treated as reference documentation with token-budget considerations
3. **Compare functionality is sophisticated** - two-step selector with lane-based visualization is a key differentiator
4. **School cards are central navigation** - both homepage and schools page rely on consistent college card components
5. **Build process is automated** - GitHub Actions handles deployment with proper environment variables
6. **Static export enables simplicity** - no server requirements, pure client-side functionality
7. **Content auditing is systematic** - generate_content_map.js provides comprehensive content reference
8. **College descriptions are duplicated** - exists in both SchoolCards and schools page components
9. **BASE_PATH is critical for links** - client-side fetches must use the constant, not hardcoded paths
10. **Deployment is atomic** - single concurrent deployment prevents conflicts

## 6. Main-doc vs secondary-doc recommendations

**Main operator doc should include:**
- Build/deploy process (next.config.ts, package.json, deploy.yml)
- Content map generation and usage
- BASE_PATH configuration importance
- GitHub Pages deployment requirements
- Core component roles (homepage, schools, compare)

**Secondary continuity/reference doc should include:**
- Detailed component breakdowns (EventPreview, CompareSelector, CompareView)
- Content map structure and interpretation
- School card data and descriptions
- Timeline preview functionality
- Component-specific implementation details

**ATLAS_SPEC only:**
- Content map generation process
- Component architecture decisions
- Build configuration rationale

**Archive/reference only:**
- Historical content map versions
- Component evolution notes
- Deployment history and changes

## 7. Remaining unknowns

1. **Data pipeline integration** - How the lineage scripts integrate with the build process
2. **Content map regeneration triggers** - When and how often the content map should be updated
3. **Performance characteristics** - Build times and deployment performance considerations
4. **Error handling** - How build failures are handled and communicated
5. **Content update workflow** - Process for updating college descriptions and other static content
6. **Testing strategy** - How the site and components are tested
7. **Monitoring/alerting** - How deployment success/failure is monitored

## 8. Need for any more repo-explainer work

**Yes, one final small batch** - recommend analyzing:

1. **src/lib/data.ts** - to understand data loading and API layer
2. **src/lib/compareUtils.ts** - to understand compare functionality implementation
3. **src/lib/colleges.ts** - to understand college data structure
4. **src/lib/programs.ts** - to understand program data handling

This would complete the picture of how data flows from the lineage scripts through the site components.



Based on my analysis of the final batch of files, here's the comprehensive report:

## 1. File-by-file summary

**src/lib/compareUtils.ts**
- 1–3 sentence summary: Production utilities for the compare feature, extracted from prototype code. Provides course roster comparison, term-lane grouping, and payload building for degree comparisons.
- Current role: Active core - enables the sophisticated degree comparison functionality
- Classification: active core

**src/lib/colleges.ts**
- 1–3 sentence summary: Shared college definitions used across filter UIs, mapping canonical school names to display labels, descriptions, and styling classes.
- Current role: Active supporting - provides consistent college data and styling across the site
- Classification: active supporting

**_internal/youtube/YOUTUBE_WORKLOG.md**
- 1–3 sentence summary: Documentation of YouTube source workstream status, including filtering results and planned review passes for Official WGU and Career Services channels.
- Current role: Active supporting - tracks YouTube content curation workflow
- Classification: active supporting

**_internal/workqueue_inputs/official_context_phase2_remaining_batch.json**
- 1–3 sentence summary: Large JSON queue file containing 586 remaining items for official context phase 2 processing, organized by category (specialization, school_page, accreditation).
- Current role: Active support artifact - tracks pending official context enrichment work
- Classification: active supporting

## 2. Questions answered

**What compareUtils adds beyond the already-understood compare components:**
- Server-safe utilities that can be imported from both server and client code
- Sophisticated course roster comparison algorithms with metrics calculation
- Term-lane data structure for organizing courses by shared/unique status
- Program exclusions logic (LAB_EXCLUSIONS) to prevent spurious comparisons
- Short-label generation for differentiating similar degree names
- Payload building that works for any same-college + same-level program pair

**What colleges.ts contributes to runtime/data normalization:**
- Canonical mapping between program.school values and display properties
- Historical name tracking for colleges that have been renamed
- Consistent styling classes for college filter chips across the site
- Short descriptions and chip styling for consistent UI presentation

**Current status of the YouTube workstream:**
- Official WGU channel: 818 filtered titles remaining, ready for YT-1 school-level candidate review
- Career Services channel: 267 filtered titles remaining, to be reviewed after Official WGU passes
- Three planned passes: YT-1 (school-level), YT-2 (degree-level), YT-3 (Career Services)
- Currently paused at pre-candidate review stage

**Current status of the official-context remaining-batch queue:**
- Active support artifact with 586 items remaining for phase 2 processing
- Organized by category: specialization (400+ items), school_page (180+ items), accreditation (1 item)
- Represents pending official context enrichment work for degree and school pages

## 3. Operator-level takeaways

1. **compareUtils is the engine behind degree comparison** - provides sophisticated roster analysis and term-based course organization
2. **colleges.ts ensures consistency** - centralizes college data and styling for filters across the entire site
3. **YouTube workstream is structured but paused** - has clear methodology but hasn't progressed to candidate review
4. **Official context queue is substantial** - 586 items remain for phase 2, representing significant pending work
5. **LAB_EXCLUSIONS prevent comparison noise** - sophisticated filtering to exclude pathway programs and identical-name groups
6. **Term-lane architecture enables rich visualization** - organizes courses by term for the sticky-header compare view
7. **Server-safe utilities enable flexibility** - compareUtils can be used in both server and client contexts
8. **College data normalization is centralized** - colleges.ts prevents inconsistencies in college display and filtering

## 4. Main-doc vs secondary-doc recommendation

**Main operator doc should include:**
- compareUtils role in degree comparison functionality
- colleges.ts for college data consistency and filtering
- LAB_EXCLUSIONS and comparison logic
- Term-lane data structure for course organization

**Secondary continuity/reference doc should include:**
- YouTube workstream methodology and current status
- Official context phase 2 queue structure and pending work
- Detailed compareUtils API and payload structure
- College historical name mappings and styling classes

**Archive/reference only:**
- YouTube raw title inventories
- Official context phase 1 artifacts
- Historical college name change documentation

## 5. Final repo-explainer judgment

**Enough to begin compression into the minimal doc set: YES**

The repo-explainer work is now complete. I have analyzed all critical components:

- **Core scripts** (lineage pipeline, content generation)
- **App shell** (layout, navigation, deployment)
- **Key components** (homepage, schools, compare functionality)
- **Configuration** (build, deployment, GitHub Pages)
- **Support utilities** (college data, comparison logic)
- **Workstreams** (YouTube, official context)

The operator now has comprehensive understanding of:
- What each component does and its role in the system
- How data flows from lineage scripts through the site
- Deployment and build process requirements
- Current workstream status and pending tasks
- Key operational considerations for maintenance

This provides sufficient foundation to begin compressing the knowledge into the minimal operator documentation set.


























