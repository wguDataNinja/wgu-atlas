## 4. Authority map

| Domain | Authority |
|---|---|
| Current execution control | `_internal/ATLAS_CONTROL.md` |
| Stable repo memory, architecture, runtime facts, durable decisions | `_internal/ATLAS_REPO_MEMORY.md` |
| Session history / handoff ledger | `_internal/DEV_LOG.md` |

This repo is being compressed to a 3-document system:

1. `_internal/ATLAS_CONTROL.md` — active control surface
2. `_internal/ATLAS_REPO_MEMORY.md` — stable repo memory, runtime facts, and wrapped decisions
3. `_internal/DEV_LOG.md` — terse dated ledger

No separate long-lived `ATLAS_SPEC.md` or `DECISIONS.md` should be treated as active canon. Both are archived in `_internal/archive/2026-03-final-consolidation/docs/`.

---

## 5. Current workstream status

| Workstream | Status | Current objective | Primary blocker | Next bounded step |
|---|---|---|---|---|
| Program guide extraction | Phase C — 89/115 artifact coverage (77.4%), 87/115 family-validated (75.7%) | assess Phase D readiness conservatively (numeric threshold crossed; risky families remain) | 26 unvalidated guides include high-risk families (nursing, endorsement, education_grad) | Phase D readiness assessment + accounting_ma specialization fix planning |
| Official resource layer | initialized, likely next | move from planning to first queue artifact | first bounded queue artifact not built | create regulatory/licensure/disclosure candidate queue |
| Continuity review | initialized, lightweight | validate compact review method | first tiny validation batch not created | create 4-card validation batch |
| Program lineage / degree history | ready, not selected | keep system stable for later export/UI if chosen | export/runtime wiring not implemented | no action unless selected |
| Catalog baseline / site runtime | stable | preserve current deterministic site behavior | none immediate | no action |
| Homepage/product framing rethink | deferred | revisit after module priorities settle | depends on clearer emphasis across modules | defer |

---

## 6. Current module snapshots

### 6.0 Program guide extraction

**Status**
- Phase C — 89/115 artifact coverage (77.4%). 12 complete families. 87 family-validated (75.7%).
- Phase D numeric threshold (≥70%) is crossed. Phase D readiness is NOT automatic — see coverage model below.
- Parser is stable and production-quality. Core state machine validated across 12+ families.

**Coverage model (three distinct numbers):**
- Artifact coverage: 89 guides have parsed + validation + manifest_row files. Includes deferred-LOW guides.
- Family-validated coverage: 87 guides in families that completed rollout review. Does not include deferred LOW guides.
- Downstream-usable full: ~84 guides (HIGH/MEDIUM, SP+AoS both intact). Does not include BSITM, MATSPED, MSCSUG SP.
- Downstream-usable partial: 3 guides (BSITM, MATSPED, MSCSUG — SP unusable, AoS intact).
- Not usable: MACCA, MACCF, MACCT (AoS broken, deferred).

**Complete families (12):**
standard_bs(19), cs_ug(8), education_ba(11), graduate_standard(9), mba(3), healthcare_grad(2), education_bs(4), teaching_mat(9), cs_grad(5), swe_grad(4), data_analytics_grad(3), education_ma(9)

**Partially validated:**
- accounting_ma: 5 guides parsed, 3 LOW (specialization guides have looks_like_prose parser limitation). MACC=HIGH, MACCM=MEDIUM usable. Specialization guides deferred.

**Why it matters**
- Program guides contain the richest per-program content: Standard Path with CUs and term, course descriptions, competency bullets, prereq mentions, cert-prep mentions.
- 0 empty course descriptions across all parsed guides. Strongest field in the pipeline.

**Current parser state**
- `scripts/program_guides/parse_guide.py` — stable, tested, no planned rewrites
- Session 18 fix: `_is_bullet_continuation` Title Case guard (≥80% capitalized words → not a continuation). Regression-verified.
- Session 19 fix: `parse_capstone` KeyError — added `prerequisite_mentions` and `certification_prep_mentions` to capstone dict. Regression-verified against 23 guides.
- Known limitation: `looks_like_prose` fails for short-wrapped description lines (40–50 chars, no terminal punctuation). Affects accounting_ma specialization guides. Fix deferred (verb-presence heuristic proposed but not implemented).
- Known source-artifact outliers (SP unusable, AoS intact): BSITM, MATSPED, MSCSUG

**Known downstream exclusions**
- BSITM SP, MATSPED SP, MSCSUG SP: source-PDF column extraction failures
- MSCSAIML degree_title: truncated in parsed output (cosmetic)
- MACCM Corporate Financial Analysis: title/first-sentence quality issue
- MACCA, MACCF, MACCT AoS: courses mis-parsed as groups (parser limitation, not source artifact)
- MAELLP12: page_count=0 (cosmetic — older guide format, content intact)

**Key files**
- `_internal/program_guides/DEV_NOTES.md` — session history, parser change log, coverage accounting model
- `_internal/program_guides/TECHNICAL_READOUT.md` — parser design rationale
- `data/program_guides/parsed/` — 89 *_parsed.json files
- `data/program_guides/validation/` — 89 *_validation.json files
- `data/program_guides/manifest_rows/` — 89 *_manifest_row.json files
- `data/program_guides/family_validation/` — gate reports and rollout summaries
- `data/program_guides/audit/` — family inventory, section matrix, readiness assessment
- `public/data/program_guides/` — not yet created (Phase D)

**Pipeline phases**
1. A: Corpus manifest ✓
2. B: Thin-slice validation ✓
3. C: Full corpus parsing — **IN PROGRESS** (89 artifact / 87 family-validated)
4. D: Site artifact build — NOT STARTED (numeric threshold crossed but Phase D readiness requires separate conservative assessment)
5. E: Course code matching — NOT STARTED

**Next artifact**
- Conduct conservative Phase D readiness assessment (numeric threshold is met; must evaluate risky-family coverage and safe-field boundaries before starting)
- accounting_ma specialization fix: design and regression-test looks_like_prose verb-presence heuristic

---

### 6.1 Official resource layer

**Status**
- initialized
- planning direction is good enough
- likely next major workstream
- not yet converted into first real queue artifact

**Why it matters**
- This is the clearest next student-facing value layer after catalog facts.
- It fits the product posture better than a homepage redesign or Reddit/community expansion.
- It can improve program and school pages without changing the core site identity.

**Locked direction**
Priority order:

1. regulatory / licensure / disclosure
2. outcomes + accreditation completeness audit
3. specialization / track / variant resources
4. school governance / context
5. Official WGU YouTube
6. Career Services YouTube
7. selective program landing pages

**Key files**
- `_internal/official_resource/README.md`
- `_internal/official_resource/ARTIFACTS.md`
- `_internal/official_resource/SESSION_LOG.md`
- `_internal/official_resource/next_workstream_memo.md`
- `public/data/official_resource_placements.json`

**Next artifact**
- `_internal/official_resource/regulatory_candidate_queue.md`

---

### 6.2 Continuity review

**Status**
- initialized
- intentionally lightweight
- waiting on first validation batch
- not a major build track

**Why it matters**
- Keeps continuity work bounded
- Tests whether the review method is actually useful
- Avoids uncontrolled expansion of lineage/continuity work

**Locked method**
- first format: compact text cards
- first batch size: 4
- target pattern classes:
  - clean successor
  - rebuilt replacement
  - split family
  - ambiguous case

**Currently planned example IDs**
- `PLE-001`
- `PLE-011`
- `PLE-010`
- `PLE-012`

**Key files**
- `_internal/continuity_review/README.md`
- `_internal/continuity_review/ARTIFACTS.md`
- `_internal/continuity_review/SESSION_LOG.md`
- `_internal/continuity_review/review_method_plan.md`

**Next artifact**
- `_internal/continuity_review/validation_batch_01.md`

---

### 6.3 Program lineage / degree history

**Status**
- structurally sound
- ready but not selected
- safe to pause

**Why it matters**
- Strong supporting context layer
- Already has meaningful curation/validation work behind it
- Could become a worthwhile program-page enhancement later

**Current posture**
- Do not treat lineage as the automatic next implementation track.
- Resume only if lineage export/UI becomes the explicit next chosen module.
- Lineage export is a defer-or-promote decision; it is not automatic.

**Important artifacts**
- `data/lineage/lineage_decisions.json`
- `data/lineage/program_transition_universe.csv`
- `data/lineage/program_link_candidates.json`
- `data/lineage/program_lineage_enriched.json`
- `data/lineage/program_history_enrichment.json`
- `scripts/validate_lineage_decisions.py`

**Known unresolved items**
- pending HITL: `PLE-012`, `PLE-023`
- pending gap check: `PLE-028`

**Blocking unresolved programs**
- `BSHHS`
- `MHA`
- `MATSPED`
- `MEDETID`
- `MEDETIDA`
- `MEDETIDK12`

---

## 7. Locked decisions

These should not be reopened by default.

- Atlas is a reference/explainer product, not a discussion/community product.
- Official resources come before Reddit/community enrichment.
- YouTube comes before Reddit/community, but after tighter official-resource attachment work.
- History/lineage is supporting context, not homepage identity.
- Program History is a program-page enrichment layer, not a separate product surface.
- Continuity review is a bounded validation track, not a large feature buildout.
- Homepage rethink is not the first move.
- The official-resource layer is the most likely next major module.
- Compare is not the first active implementation track; revisit after baseline cleanup settles.
- Lineage export is not an automatic next move; it remains a defer-or-promote decision.
- If a predecessor program is still active, default to pathway-variant logic rather than lineage.
- Approved low-confidence lineage events require guardrails in wording.
- Approved zero-overlap lineage events require explicit rationale.
- Suppressed or unresolved lineage events should not surface by default.

**Ecosystem index note:** A broader WGU online ecosystem index now exists at `_internal/WGU_ONLINE_ECOSYSTEM_INDEX.md` for future homepage/community/social exploration. It does not change the current product posture or the deferred status of Reddit/community integration.

---

## 8. Open questions / blockers

| ID | Question | Default if unresolved |
|---|---|---|
| Q-OFF-QUEUE | What is the first clean candidate queue for official-resource work? | start with regulatory/licensure/disclosure |
| Q-OFF-ATTACH | What is the minimum robust attachment model before YouTube expansion? | defer broader YouTube rollout |
| Q-LIN-012 | Should `PLE-012` be accepted as lineage? | reject history |
| Q-LIN-023 | Should `PLE-023` be accepted as lineage? | reject history |
| Q-LIN-028 | Is `PLE-028` true continuity or a gap-linked new launch? | split / retire+new |
| Q-LIN-MATSPED | Is MSSP an acceptable predecessor for MATSPED (M.A.T. Special Education)? Degree-level mismatch concern. | new_from_scratch |
| Q-CONT-001 | Does the 4-card continuity review format produce useful validation signal? | keep continuity work small |

---

## 9. Exact next-session order

1. **Program guide — Phase D readiness assessment:** education_ma is complete. Numeric threshold (≥70%) is crossed (87/115 family-validated). Assess conservatively: what is the realistic downstream coverage, what families remain untouched and how risky are they, and is it safe to begin Phase D artifact build? Do not start Phase D on numeric threshold alone. Write a short Phase D readiness memo.
2. **Program guide — accounting_ma specialization fix:** Design and regression-test looks_like_prose verb-presence heuristic (see DEV_NOTES Session 19 for proposed approach). Test against MACCA, MACCF, MACCT. Verify no regressions across all 89 validated guides before deciding whether to implement.
3. Build `_internal/official_resource/regulatory_candidate_queue.md`
4. Run first 4-card continuity-review batch (`_internal/continuity_review/validation_batch_01.md`)

---

## 10. Key artifact map

| Need | Go to |
|---|---|
| What matters now | `_internal/ATLAS_CONTROL.md` |
| How the repo works | `_internal/ATLAS_REPO_MEMORY.md` |
| What changed recently | `_internal/DEV_LOG.md` |
| Page-state docs, source baseline, homepage design conclusions | `_internal/page_designs/` — see `README.md` for reading order |
| Program guide extraction — design and pipeline | `_internal/program_guides/TECHNICAL_READOUT.md` |
| Program guide extraction — workstream control | `_internal/program_guides/README.md` |
| Official-resource module materials | `_internal/official_resource/` |
| Continuity-review materials | `_internal/continuity_review/` |
| Lineage data + decisions | `data/lineage/` |
| Runtime/public artifacts | `public/data/` |
| Build/data scripts | `scripts/` |
| App/runtime code | `src/` |

---

## 11. Session-close requirements

At the end of a working session, record:

- what changed
- what decisions were locked
- what remains blocked
- what is pause-ready
- exact next starting task

If a change affects current priorities, workstream state, or the next-session order, update this file.

Stable repo facts, architecture, runtime behavior, and durable decisions belong in `_internal/ATLAS_REPO_MEMORY.md`.
Session-by-session history belongs in `_internal/DEV_LOG.md`.
