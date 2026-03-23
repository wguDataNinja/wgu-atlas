# Stage 1 — Dependency Inventory and Target Map

## Document status
- Version: 1.0
- Produced as Stage 1 output per LOCAL_8B_RAG_SYSTEM_DESIGN.md §15.2
- Prerequisite: STAGE_0_OWNERSHIP_CONTRACT.md complete.
- Audience: Codex implementation. Every dependency has exactly one strategy. No ambiguity.

---

## 1) Inventory: Catalog data artifacts

| Dependency | Current source (wgu-reddit) | Used for | Atlas target | Strategy | Notes |
|---|---|---|---|---|---|
| Trusted catalog outputs — current edition | `WGU_catalog/outputs/trusted/2026_03/` | Program composition, CU totals, course roster facts | `data/catalog/trusted/2026_03/` | **mirror** | Mirror at build time. Not runtime-fetched. |
| Change tracking | `WGU_catalog/outputs/change_tracking/` | Edition-level change records for version diff | `data/catalog/change_tracking/` | **mirror** | Mirror at build time. |
| Edition diffs | `WGU_catalog/outputs/edition_diffs/` | Version diff cards | `data/catalog/edition_diffs/` | **mirror** | Mirror at build time. |
| Course index (`course_index_v10.json`, 59 MB) | `WGU_catalog/outputs/helpers/course_index_v10.json` | Full course lookup | `data/catalog/helpers/course_index_v10.json` | **mirror** | Large file. Mirror once; do not re-fetch at runtime. |
| Degree snapshots | `WGU_catalog/outputs/helpers/degree_snapshots_v10_seed.json` | Degree snapshot baseline | `data/catalog/helpers/degree_snapshots_v10_seed.json` | **mirror** | Mirror at build time. |
| Sections index | `WGU_catalog/outputs/helpers/sections_index_v10.json` | Section lookup support | `data/catalog/helpers/sections_index_v10.json` | **mirror** | Mirror at build time. |

**All catalog data**: `mirror` strategy. These are build-time inputs. Atlas copies them locally; no runtime reads from `wgu-reddit` paths.

---

## 2) Inventory: Program guide artifacts

| Dependency | Current source | Used for | Atlas target | Strategy | Notes |
|---|---|---|---|---|---|
| Parsed guide artifacts (115 `*_parsed.json`) | `wgu-reddit` → already in `wgu-atlas/data/program_guides/parsed/` | QA object generation, guide-grounded answers | `data/program_guides/parsed/` | **already in Atlas** | No action needed. |
| Guide manifest | Already in `wgu-atlas/data/program_guides/guide_manifest.json` | Guide discovery, version mapping | `data/program_guides/guide_manifest.json` | **already in Atlas** | No action needed. |
| Guide anomaly registry | Already in `wgu-atlas/data/program_guides/guide_anomaly_registry.json` | Completeness gating | `data/program_guides/guide_anomaly_registry.json` | **already in Atlas** | No action needed. |
| Section presence matrix | Already in `wgu-atlas/data/program_guides/section_presence_matrix.csv` | Negative claim completeness | `data/program_guides/section_presence_matrix.csv` | **already in Atlas** | No action needed. |
| Raw guide PDFs (115) | `WGU_catalog/program_guides/raw_pdfs/` | PDF text extraction only | none for runtime | **exclude** | Extraction is a build step. Not needed at QA runtime. |
| Raw guide texts (115) | `WGU_catalog/program_guides/raw_texts/` | Guide parsing input only | none for runtime | **exclude** | Parsing outputs already committed to Atlas. Not needed at QA runtime. |

---

## 3) Inventory: Canonical course data

| Dependency | Current source | Used for | Atlas target | Strategy | Notes |
|---|---|---|---|---|---|
| Canonical course index (CSV) | Already in `wgu-atlas/data/canonical_courses.csv` | Course lookup, CU facts | `data/canonical_courses.csv` | **already in Atlas** | No action needed. |
| Canonical course index (JSON) | Already in `wgu-atlas/data/canonical_courses.json` | Course lookup | `data/canonical_courses.json` | **already in Atlas** | No action needed. |

---

## 4) Inventory: LLM orchestration utilities

These are the patterns from `src/wgu_reddit_analyzer/benchmark/` that Atlas QA needs. They must be **ported** (rewritten clean into Atlas; not imported from `wgu-reddit` at runtime).

| Dependency | Current source | Used for | Atlas target | Strategy | Port scope |
|---|---|---|---|---|---|
| Provider dispatch (OpenAI / Ollama) | `benchmark/model_client.py` + `llm_connectivity_check.py` | Call local Ollama or OpenAI for classification/generation | `src/atlas_qa/llm/client.py` | **port** | Minimal: `generate(model, prompt) -> str`. Drop cost/latency estimation unless needed. |
| Model registry (provider + model metadata) | `benchmark/model_registry.py` | Provider lookup by model name | `src/atlas_qa/llm/registry.py` | **port** | Port only Atlas-relevant models (local 8B + optional OpenAI fallback). |
| Structured call result type | `benchmark/stage1_types.py` (`LlmCallResult`) | Typed output from model call | `src/atlas_qa/llm/types.py` | **port** | Port `LlmCallResult` or define Atlas-equivalent with same flags: `raw_text`, `llm_failure`, `parse_failure`, `schema_failure`, `num_retries`, `error_message`. |
| JSON extraction + schema validation | `benchmark/stage1_classifier.py` (structured output path) | Validated classifier output | `src/atlas_qa/llm/structured.py` | **port** | Extract the JSON parse + Pydantic validation + fallback pattern. Generalize for Atlas schemas. |
| Logging utilities | `utils/logging_utils.py` | Per-run observability | `src/atlas_qa/utils/logging.py` | **port** | Lightweight; port or replace with stdlib logging wrapper. |
| Run-level artifact capture | `benchmark/run_stage1_benchmark.py` (artifact write pattern) | Prompt + raw output + flags per call | `src/atlas_qa/llm/artifacts.py` | **port** | The pattern of writing `{prompt, raw_output, flags}` per call. Not the benchmark runner itself. |

**What to exclude from the port:**
- Cost/latency estimation (`cost_latency.py`) — not needed for Atlas QA runtime.
- Benchmark orchestration (`run_stage1_benchmark.py`, `build_stage1_panel.py`, etc.) — Reddit-specific benchmark tooling.
- Reddit-specific classifier logic (`stage1_classifier.py` prompt/label details) — replace with Atlas QA classifier schemas.
- Config loader that reads Reddit-specific env/secrets — replace with Atlas-local config.

---

## 5) Inventory: Build scripts

| Dependency | Current source | Used for | Atlas target | Strategy | Notes |
|---|---|---|---|---|---|
| `build_site_data.py` | `wgu-atlas/scripts/` | Site data build (not QA runtime) | stays in `scripts/` | **keep as-is** | Not a QA runtime dependency. Continues to read from `wgu-reddit` as build input. |
| `parse_guide.py` | `wgu-atlas/scripts/program_guides/` | Guide parsing (already done, outputs committed) | no change | **keep as-is** | One-time build tool. Outputs already committed to Atlas. Not a QA runtime dependency. |
| `extract_guide_texts.py` | `wgu-atlas/scripts/program_guides/` | PDF text extraction (already done) | no change | **keep as-is** | One-time build tool. Not a QA runtime dependency. |

---

## 6) Summary: all dependencies classified

Every dependency has exactly one strategy. No uncategorized entries.

| Strategy | Count | Items |
|---|---|---|
| already in Atlas | 6 | parsed guides, guide manifest, anomaly registry, section presence, canonical_courses CSV, canonical_courses JSON |
| mirror (build-time) | 6 | trusted outputs, change tracking, edition diffs, course index, degree snapshots, sections index |
| port (rewrite into Atlas) | 6 | provider dispatch, model registry, structured result type, JSON extraction/validation, logging utils, artifact capture pattern |
| keep as-is (build tool, not runtime) | 3 | build_site_data.py, parse_guide.py, extract_guide_texts.py |
| exclude (raw corpus, extraction inputs) | 2 | raw PDFs, raw guide texts |

**Total: 23 dependencies. 23 classified. 0 ambiguous.**

---

## 7) Atlas target directory layout (QA package)

```
wgu-atlas/
  data/
    catalog/
      trusted/
        2026_03/          ← mirror from wgu-reddit
      change_tracking/    ← mirror from wgu-reddit
      edition_diffs/      ← mirror from wgu-reddit
      helpers/
        course_index_v10.json         ← mirror from wgu-reddit
        degree_snapshots_v10_seed.json ← mirror from wgu-reddit
        sections_index_v10.json        ← mirror from wgu-reddit
    program_guides/       ← already present; no changes
    canonical_courses.csv ← already present; no changes
    canonical_courses.json ← already present; no changes
    qa/
      objects/            ← Stage 3: generated QA objects (course_card, program_version_card, etc.)
      fixtures/           ← Stage 6: eval fixtures
      reports/            ← eval reports
  src/
    atlas_qa/
      llm/
        client.py         ← ported from benchmark/model_client.py
        registry.py       ← ported from benchmark/model_registry.py
        types.py          ← ported from benchmark/stage1_types.py
        structured.py     ← ported JSON extraction + Pydantic validation
        artifacts.py      ← ported run artifact capture pattern
      utils/
        logging.py        ← ported from utils/logging_utils.py
      qa/                 ← Stage 3+: QA object generators, routing, retrieval, eval
```

---

## 8) Mirror procedure (catalog artifacts)

For each `mirror` dependency, the procedure is:

1. Copy from `wgu-reddit/WGU_catalog/outputs/<subpath>` to `wgu-atlas/data/catalog/<subpath>`.
2. Do not commit large runtime-only files to git (e.g., `course_index_v10.json` at 59 MB — add to `.gitignore` and document in a `data/catalog/README.md`).
3. Update `build_site_data.py` to accept an `ATLAS_CATALOG_DATA` env var pointing to `data/catalog/` as an alternative to `WGU_REDDIT_PATH`. This makes the build decoupled from the `wgu-reddit` path at the caller's option.

---

## 9) Definition of done

- [x] All current Atlas dependencies on `wgu-reddit` inventoried.
- [x] Every dependency classified with exactly one strategy.
- [x] No runtime-critical dependency lacks an Atlas target path.
- [x] Atlas target directory layout defined.
- [x] Mirror procedure documented.

Stage 2 is unblocked. Codex can proceed to port the Atlas-local foundation without guessing.
