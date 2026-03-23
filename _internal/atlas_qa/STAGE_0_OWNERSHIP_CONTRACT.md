# Stage 0 — Atlas QA Ownership Boundary Contract

## Document status
- Version: 1.0
- Produced as Stage 0 output per LOCAL_8B_RAG_SYSTEM_DESIGN.md §15.2
- This is a binding boundary contract for all Atlas QA implementation work.

---

## 1) Ownership declaration

`wgu-atlas` is the single authoritative home for:

| Concern | Owner |
|---|---|
| Atlas QA runtime code | `wgu-atlas` |
| Atlas QA test suite | `wgu-atlas` |
| Atlas QA eval harness | `wgu-atlas` |
| Atlas QA generated artifacts (QA objects, fixtures, reports) | `wgu-atlas` |
| Atlas QA documentation, specs, internal runbooks | `wgu-atlas` |
| Query schemas and routing logic | `wgu-atlas` |
| Entity/version resolution logic | `wgu-atlas` |
| Retrieval index build code | `wgu-atlas` |
| Evidence bundle logic | `wgu-atlas` |
| Abstention/completeness gate logic | `wgu-atlas` |
| Answer formatting contracts | `wgu-atlas` |
| Evaluation datasets and fixtures | `wgu-atlas` |

`wgu-reddit` is the authoritative home for:

| Concern | Owner |
|---|---|
| Raw PDF corpus (catalog + program guides) | `wgu-reddit` |
| Catalog parser and parser outputs | `wgu-reddit` |
| Extraction intermediates | `wgu-reddit` |
| One-time migration scripts for bootstrapping | `wgu-reddit` |
| Reddit acquisition pipeline | `wgu-reddit` |

---

## 2) Hard rules (in effect immediately)

1. **No new QA runtime code in `wgu-reddit`.** Any new Atlas QA logic is written in `wgu-atlas`.
2. **No Atlas QA tests in `wgu-reddit`.** All QA tests and eval fixtures live in `wgu-atlas`.
3. **No hidden runtime dependency on upstream parser internals.** Atlas QA consumes normalized artifacts, not parser code.
4. **All production answer paths resolve from Atlas-local artifacts.** No runtime path reads from `wgu-reddit` paths.
5. **Any remaining `wgu-reddit` dependency is transitional and explicitly enumerated** in the Stage 1 inventory. Nothing uncategorized.
6. **Codex writes no new `wgu-reddit` import paths in Atlas QA code.**

---

## 3) What may remain external temporarily

These are tolerated as **build-time import sources only**, not runtime dependencies:

- Raw PDF corpus (`wgu-reddit/WGU_catalog/program_guides/raw_pdfs/`) — used during guide text extraction; not needed at QA runtime.
- Extracted guide texts (`wgu-reddit/WGU_catalog/program_guides/raw_texts/`) — used during parsing; outputs are already in `wgu-atlas/data/program_guides/parsed/`.
- Catalog parser outputs (`wgu-reddit/WGU_catalog/outputs/`) — used during site build and artifact bootstrapping; once mirrored/snapshotted into Atlas, no longer needed at runtime.
- Legacy parser code (`wgu-reddit/WGU_catalog/parse_catalog_v11.py`) — one-time build tool; excluded from Atlas entirely.

All transitional dependencies are enumerated and classified in the Stage 1 inventory.

---

## 4) Current repo boundary (as observed)

### What is already in `wgu-atlas`

| Artifact | Atlas path | Status |
|---|---|---|
| Parsed program guide artifacts (115 files) | `data/program_guides/parsed/` | Ready |
| Guide manifest | `data/program_guides/guide_manifest.json` | Ready |
| Guide anomaly registry | `data/program_guides/guide_anomaly_registry.json` | Ready |
| Section presence matrix | `data/program_guides/section_presence_matrix.csv` | Ready |
| Canonical course index (CSV + JSON) | `data/canonical_courses.csv`, `data/canonical_courses.json` | Ready |
| Program history artifacts | `data/` (various) | Ready |
| Site-ready JSON exports | `public/data/` | Ready |

### What currently lives only in `wgu-reddit`

| Artifact | wgu-reddit path | Notes |
|---|---|---|
| Catalog trusted outputs (current edition) | `WGU_catalog/outputs/trusted/2026_03/` | Program/course structured data |
| Change tracking | `WGU_catalog/outputs/change_tracking/` | Edition-level change records |
| Edition diffs | `WGU_catalog/outputs/edition_diffs/` | Per-edition diff artifacts |
| Course index (59 MB) | `WGU_catalog/outputs/helpers/course_index_v10.json` | Full course lookup index |
| Degree snapshots | `WGU_catalog/outputs/helpers/degree_snapshots_v10_seed.json` | Degree snapshot data |
| Sections index | `WGU_catalog/outputs/helpers/sections_index_v10.json` | Sections lookup |
| Raw program guide PDFs | `WGU_catalog/program_guides/raw_pdfs/` (115) | Extraction input only |
| Raw program guide texts | `WGU_catalog/program_guides/raw_texts/` (115) | Parsing input only |
| LLM orchestration patterns | `src/wgu_reddit_analyzer/benchmark/` | To port into Atlas |

---

## 5) Failure modes to prevent

| Failure mode | Prevention |
|---|---|
| "Temporary" dependencies become permanent | Stage 1 inventory reviewed at each stage; no uncategorized dependency allowed |
| Codex builds against upstream paths directly | Hard rule §2.4; grep check required in Stage 2 verification |
| Eval fixtures split across repos | Hard rule §2.2; all fixtures live in `wgu-atlas` |
| Runtime correctness depends on parser internals | Hard rule §2.3; Atlas QA consumes artifacts, not parser code |

---

## 6) Definition of done

- [x] Ownership declaration written (§1)
- [x] Hard rules defined (§2)
- [x] Transitional externals enumerated (§3)
- [x] Current boundary observed and documented (§4)
- [ ] Stage 1 inventory complete (see STAGE_1_DEPENDENCY_INVENTORY.md)

Stage 1 is unblocked. Proceed to dependency inventory.
