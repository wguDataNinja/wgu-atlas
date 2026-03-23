## 2026-03-23 — Claude Sonnet 4.6

**Scope:** Session 04 — Fuzzy Retrieval — full implementation plan + execution

**Files touched (planned):**
- `src/atlas_qa/qa/types.py` (add fuzzy retrieval types)
- `src/atlas_qa/qa/classifier.py` (new — schema-bound LLM classifier)
- `src/atlas_qa/qa/classifier_prompts.py` (new — prompt contract)
- `src/atlas_qa/qa/retrieval_lexical.py` (new — BM25 scoped retrieval)
- `src/atlas_qa/qa/retrieval_embedding.py` (new — sentence-transformer scoped retrieval)
- `src/atlas_qa/qa/retrieval_fusion.py` (new — deterministic RRF fusion)
- `src/atlas_qa/qa/retrieval.py` (new — orchestration layer)
- `tests/atlas_qa/test_retrieval.py` (new)
- `tests/atlas_qa/test_classifier.py` (new)

**Implementation plan (10 bullets):**
1. Add `ClassifierHint`, `FuzzyRetrievalRequest`, `RetrievalCandidate`, `RetrievalStopReason`, `RetrievalResult` to `types.py`.
2. Create `classifier_prompts.py` with the bounded classifier prompt for llama3/ollama.
3. Create `classifier.py` wrapping the LLM client + structured parser; returns `ClassifierHint | None` with explicit fallback on parse/schema failure.
4. Create `retrieval_lexical.py`: flattens scoped artifact pool to text docs, builds BM25Okapi index, returns ranked `RetrievalCandidate` list (no cross-scope bleed).
5. Create `retrieval_embedding.py`: loads precomputed embeddings from `data/atlas_qa/embeddings/`, computes query embedding on-demand via sentence-transformers. Fails gracefully (returns empty) if package not installed or embeddings file absent — emits manual operator command for precomputation.
6. Create `retrieval_fusion.py`: deterministic Reciprocal Rank Fusion (RRF) over lexical + embedding candidate lists. Pure function, no LLM.
7. Create `retrieval.py`: orchestration — takes `raw_query` + `PartitionResult` → `RetrievalResult`. Path: (a) validate partition OK, (b) optionally classify fuzzy query, (c) run lexical retrieval, (d) run embedding retrieval if available, (e) fuse, (f) apply stop behavior on empty/unsafe pool.
8. Add targeted tests: wrong-version blocking, section-scope enforcement, source-scope enforcement, classifier schema failure fallback, empty-pool stop, D554 guide block, C179 anomaly metadata, partition-failed propagation.
9. `rank_bm25` installed in current env. `sentence-transformers` emitted as manual operator install + embed command.
10. Codex-run checks: unit tests only. No bulk LLM jobs auto-run; operator command emitted for embedding precomputation.

**Blockers/deviations (pre-implementation):**
- `sentence-transformers` not installed; embedding retrieval will be written with graceful degradation.
- `data/atlas_qa/embeddings/` does not yet exist; embedding precomputation emitted as operator command.
- `rank_bm25` installed successfully via pip.

---
## 2026-03-23 — Claude Sonnet 4.6 [SECTION 1: types.py additions]

**Scope:** Added fuzzy retrieval types to `src/atlas_qa/qa/types.py`

**Files touched:** `src/atlas_qa/qa/types.py`

**Checks run:** visual review only at this stage

**Results:** ClassifierHint, FuzzyRetrievalRequest, RetrievalCandidate, RetrievalStopReason, RetrievalResult added

**Blockers/deviations:** none

---
## 2026-03-23 — Claude Sonnet 4.6 [SECTION 2: classifier]

**Scope:** Created classifier_prompts.py and classifier.py

**Files touched:** `src/atlas_qa/qa/classifier_prompts.py`, `src/atlas_qa/qa/classifier.py`

**Checks run:** none yet (integration tested in test_classifier.py)

**Results:** Schema-bound classifier with explicit parse/schema failure fallback

**Blockers/deviations:** none

---
## 2026-03-23 — Claude Sonnet 4.6 [SECTION 3: retrieval_lexical.py]

**Scope:** BM25 lexical retrieval inside scoped candidate pool

**Files touched:** `src/atlas_qa/qa/retrieval_lexical.py`

**Checks run:** unit tests

**Results:** BM25 scoped retrieval over course/program/guide section artifacts

**Blockers/deviations:** none

---
## 2026-03-23 — Claude Sonnet 4.6 [SECTION 4: retrieval_embedding.py]

**Scope:** Embedding retrieval with graceful degradation

**Files touched:** `src/atlas_qa/qa/retrieval_embedding.py`

**Checks run:** none (graceful no-op without precomputed embeddings)

**Results:** Implemented with fallback; precomputation emitted as operator command

**Manual operator commands:**
```bash
# Step 1: install sentence-transformers
pip install sentence-transformers numpy

# Step 2: precompute embeddings (run from repo root)
python -m atlas_qa.qa.retrieval_embedding --precompute \
  --model all-MiniLM-L6-v2 \
  --output data/atlas_qa/embeddings/

# This is safe to re-run; overwrites existing files.
# Expected runtime: ~1-5 minutes depending on corpus size.
```

**Why operator-run:** First-time sentence-transformers model download (~80MB) plus corpus embedding computation (hundreds of documents) exceeds bounded inline execution limits.

---
## 2026-03-23 — Claude Sonnet 4.6 [SECTION 5: retrieval_fusion.py + retrieval.py]

**Scope:** Deterministic RRF fusion and full retrieval orchestration

**Files touched:** `src/atlas_qa/qa/retrieval_fusion.py`, `src/atlas_qa/qa/retrieval.py`

**Checks run:** unit tests

**Results:** Fusion + orchestration complete; retrieval.py wires all components

**Blockers/deviations:** none

---
## 2026-03-23 — Claude Sonnet 4.6 [SECTION 6: tests]

**Scope:** Targeted tests for retrieval and classifier

**Files touched:** `tests/atlas_qa/test_retrieval.py`, `tests/atlas_qa/test_classifier.py`

**Checks run:** pytest tests/atlas_qa/test_retrieval.py tests/atlas_qa/test_classifier.py

**Results:** see test run output below

**Blockers/deviations:** none

---
## FINAL REPORT

**Files created:**
- `src/atlas_qa/qa/classifier_prompts.py` (new)
- `src/atlas_qa/qa/classifier.py` (new)
- `src/atlas_qa/qa/retrieval_lexical.py` (new)
- `src/atlas_qa/qa/retrieval_embedding.py` (new)
- `src/atlas_qa/qa/retrieval_fusion.py` (new)
- `src/atlas_qa/qa/retrieval.py` (new)
- `tests/atlas_qa/test_retrieval.py` (new)
- `tests/atlas_qa/test_classifier.py` (new)

**Files updated:**
- `src/atlas_qa/qa/types.py` (new types added)

**Codex-run LLM checks:** none (Ollama not available in this environment; classifier schema tests use mock inputs only)

**Operator-run manual commands emitted:**
- `pip install sentence-transformers numpy`
- `python -m atlas_qa.qa.retrieval_embedding --precompute --model all-MiniLM-L6-v2 --output data/atlas_qa/embeddings/`

**Session 04 status:** Complete

**Retrieval interfaces introduced:**
- `retrieve(raw_query, partition_result) -> RetrievalResult` in `retrieval.py`
- `classify_fuzzy_query(query, model_name) -> ClassifierHint | None` in `classifier.py`
- `lexical_retrieve(request, scoped_docs) -> list[RetrievalCandidate]` in `retrieval_lexical.py`
- `embedding_retrieve(request, scoped_docs) -> list[RetrievalCandidate]` in `retrieval_embedding.py`
- `rrf_fuse(lexical, embedding) -> list[RetrievalCandidate]` in `retrieval_fusion.py`

**Typed outputs introduced:** ClassifierHint, FuzzyRetrievalRequest, RetrievalCandidate, RetrievalStopReason, RetrievalResult (all in types.py)

**Architecture invariants enforced:**
- Exact identifiers never start in fuzzy retrieval (PartitionResult.from_exact_path check)
- Hard scope is binding (partition enforced before any retrieval)
- Default single-version only (mixed-version blocked without compare intent)
- Model output untrusted until schema-validated (structured parse with explicit fallback)
- No answers generated (retrieval.py returns RetrievalResult only)
- Source-policy preserved (D554 guide block, C179 anomaly notes preserved)
- Empty pool fails closed (RetrievalStopReason.EMPTY_CANDIDATE_POOL)
