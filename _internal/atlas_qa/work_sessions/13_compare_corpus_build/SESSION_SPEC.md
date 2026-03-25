# Session 13 — Compare Corpus Build

**Status:** STUB — not ready to activate
**Intent:** Data / corpus build
**Dependency:** Session 12 complete; explicit operator activation required before this
session begins

> This is a planning stub. The full implementation spec must be written immediately
> before activation. Do not begin implementation from this document.

---

## Purpose

Unlock Class D (explicit version comparison) query coverage by building the missing
historical corpus cards required for compare-path answers. This session is primarily a
data build, not a code change. The pipeline compare path already exists and routes
correctly (Session 09); the gap is that historical program version cards for the 2025-06
catalog edition do not exist in the corpus.

---

## Why this session exists

After session 12, the remaining non-addressable failure class is Class D: 11 of 12
queries fail because the compare path cannot find `2025-06` program version cards to
diff against the current `2026-03` cards. These are not pipeline bugs — the routing,
evidence, gate, generation, and postcheck logic all work correctly for compare queries
when both version cards are present. The data simply isn't there.

Class D questions look like:
- "What courses were added to BSDA between the last two catalog versions?"
- "How did BSACC change between catalog editions?"

Without 2025-06 cards, the compare path finds no `from_version` artifact and the gate
blocks the query as insufficient evidence. The fix is to build the missing cards, not to
change the pipeline.

Building this corpus is a non-trivial data extraction task. It requires re-running or
adapting the card-building pipeline against the 2025-06 catalog edition artifacts, which
may already exist in `data/catalog/change_tracking/` or `data/catalog/edition_diffs/`,
or may need to be rebuilt from upstream catalog sources.

This session is deferred because:
1. Session 12 addresses all remaining code-fixable failures first.
2. The corpus build scope is larger and requires a separate investigation pass to
   confirm what 2025-06 source data is available and in what form.
3. Class D gate (80%) is the lowest of any active class — it was always expected to
   require a separate data pass.

---

## High-level scope

When activated, this session would:

1. Audit what 2025-06 catalog edition data already exists in the repo
   (`data/catalog/change_tracking/`, `data/catalog/edition_diffs/`, upstream sources).
2. Determine the exact set of program codes that appear in D-class gold questions and
   confirm which have 2025-06 records available.
3. Build `program_version_cards` entries for the 2025-06 edition — following the same
   schema as the existing 2026-03 cards.
4. Extend the loaders in `src/atlas_qa/qa/loaders.py` to load multi-version cards if
   not already supported.
5. Run the Class D affected subset (D-054 through D-065) to validate routing and
   generation.
6. Run the full gold eval and confirm Class D reaches its 80% gate.

Expected outcome: overall gold eval improves from ~87% (post-session-12 estimate) to
~93%+, with Class D passing its gate.

---

## Out of scope (for this session, when it activates)

- Changes to the compare pipeline logic or routing — compare path is not the problem
- Model swap or prompt changes — session 12 handles those
- Any Class A / G failures that remain after session 12 (LLM non-determinism, not corpus)
- New query classes beyond D
- Historical cards for editions older than 2025-06

---

## Inputs likely required

- `data/catalog/change_tracking/` — may contain 2025-06 program data
- `data/catalog/edition_diffs/` — edition diff events between 2025-06 and 2026-03
- `data/catalog/trusted/` — may have 2025-06 edition blocks if collected
- `_internal/atlas_qa/QA_GOLD_QUESTION_SET.md` §Class D — exact queries and entity
  codes to target
- `src/atlas_qa/qa/loaders.py` — multi-version card loading behavior
- `src/atlas_qa/qa/compare.py` — how compare bundles are assembled from version cards

---

## Activation note

This session must not begin until:
1. Session 12 is complete and the full gold eval run is reviewed.
2. The operator explicitly confirms Class D is the next target.
3. A pre-session data audit confirms which 2025-06 source artifacts exist on disk.

Do not assume the 2025-06 data is available without checking first. The audit is the
first step, not a precondition to skip.

---

## Codex note

Before writing any code or building any data artifacts: the full implementation spec for
this session must be written first. This stub is not sufficient to begin work. At
activation time, read the current corpus structure, the Class D gold question entity
codes, and the available catalog edition data — then write a full spec in the style of
Sessions 08–12 before proceeding.
