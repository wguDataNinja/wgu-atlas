# Session 06 — Compare Mode, Eval Harness, Launch Gates

**Status:** Stub / not yet active
**Intent:** Implementation
**Dependency:** Session 05 (`05_evidence_and_generation`) must be complete before this starts

---

## Naming note

This folder was previously named `05_compare_and_eval` and held a stale stub spec
describing Session 01 (canonical object generation) work. That spec has been discarded.
The folder was renumbered to `06_compare_and_eval` to reflect correct session ordering.

Session 05 (`05_evidence_and_generation`) covers: evidence bundle construction,
answerability gate, constrained generation, and post-check — the complete single-entity
answer path.

Session 06 (this session) will cover: compare mode, version_diff_card, Atlas-local eval
harness, and v1 launch gates.

---

## Primary eval input

The gold question set for Session 06 eval harness work is:

- `_internal/atlas_qa/QA_GOLD_QUESTION_SET.md` — 100 questions across all query classes,
  with expected behavior, entity type, source scope, version-sensitivity, and notes.
- Recommended launch-gate subset: 20 questions from that document (§5).
- Launch-gate pass criteria are declared in §5 of the question set as targets;
  final thresholds must be confirmed and encoded in the eval harness implementation.

This document must be read before writing the full Session 06 spec.

---

## Scope (high level — to be detailed before implementation starts)

Per `LOCAL_8B_RAG_SYSTEM_DESIGN.md` Stage 6:

- **Compare path (Class D queries):** deterministic `version_diff_card` where available;
  otherwise strict two-version evidence bundle. Model use: summarize deterministic diff only.
- **`version_diff_card` completion:** `version_diff_card` objects are scaffolded in Session 01
  but the compare retrieval path is deferred here.
- **Atlas-local eval harness:** fixtures, gates, contamination tests, abstention tests.
- **Launch metrics and gates:**
  - exact code/program resolution: near-deterministic reliability
  - version-specific contamination: near-zero tolerance
  - citation coverage on non-abstained answers: mandatory
  - claim-level support audit: high pass threshold
  - abstention precision/recall: validated on dedicated set

---

## Write the full spec before starting

This is a stub. Per `WORK_SESSION_RULES.md`, the full `SESSION_SPEC.md` must be written
immediately before implementation starts — not ahead of need. Do not start implementation
against this stub.

Required spec sections (match Session 04/05 format):
- Status, dependency note
- LLM use policy
- Locked implementation decisions
- Objective, Why this session exists, Dependencies
- Codex execution instructions (read-first list, required execution order)
- In scope / Out of scope
- Architecture invariants
- Expected implementation locations
- Required typed outputs
- Compare path requirements
- Eval harness requirements
- Launch gate criteria
- Definition of done
- Edge cases
- Recommended implementation order
- Escalation rules
