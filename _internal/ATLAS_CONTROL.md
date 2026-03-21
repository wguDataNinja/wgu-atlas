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
| Program guide extraction | initialized — analysis only | extract content from 115 program guide PDFs | 114 guide texts not yet extracted; no scripts yet | extract all PDFs to text; write `analyze_guide_manifest.py` |
| Official resource layer | initialized, likely next | move from planning to first queue artifact | first bounded queue artifact not built | create regulatory/licensure/disclosure candidate queue |
| Continuity review | initialized, lightweight | validate compact review method | first tiny validation batch not created | create 4-card validation batch |
| Program lineage / degree history | ready, not selected | keep system stable for later export/UI if chosen | export/runtime wiring not implemented | no action unless selected |
| Catalog baseline / site runtime | stable | preserve current deterministic site behavior | none immediate | no action |
| Homepage/product framing rethink | deferred | revisit after module priorities settle | depends on clearer emphasis across modules | defer |

---

## 6. Current module snapshots

### 6.0 Program guide extraction

**Status**
- initialized — analysis phase only
- technical readout complete
- no scripts written; no data artifacts yet
- 1 of 115 guide texts extracted (BSDA)

**Why it matters**
- Program guides contain the richest per-program content available from WGU: Standard Path tables with CUs and term, course descriptions, competency bullets, prereq mentions, cert-prep mentions.
- Extracting this content enables Atlas to show course-level detail that the main catalog does not provide in accessible form.
- 115 guides cover all active programs. Coverage is broader than the current enrichment layer.

**Locked direction**
- Manifest-first: characterize all 115 guides before writing a content parser
- BSDA is the thin-slice validation case
- Course title → Atlas code matching is a separate downstream step
- No implementation until Phase A (corpus manifest) is complete

**Key files**
- `_internal/program_guides/README.md`
- `_internal/program_guides/TECHNICAL_READOUT.md`
- `data/program_guides/` (planned — not yet created)
- `public/data/program_guides/` (planned — not yet created)

**Pipeline phases**
1. A: Extract 114 remaining PDFs to text; run `analyze_guide_manifest.py`; produce manifest + section presence matrix
2. B: Thin-slice BSDA parser; validate output
3. C: Full corpus parser with family branching
4. D: Site artifact build
5. E: Course code matching

**Next artifact**
- Extract all 115 PDFs to text; then write `analyze_guide_manifest.py`

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

1. Commit pending data reorg (`data/site/`, `data/lineage/`, `data/enrichment/`) and pending src changes
2. **Program guide Phase A:** Extract all 115 guide PDFs to text; commit to `raw_texts/`; write `analyze_guide_manifest.py`; produce `guide_manifest.json` and `section_presence_matrix.csv`
3. **Program guide Phase A continued:** Review manifest outputs; write `guide_family_classification.md` and `irregularities_report.md`
4. Build `_internal/official_resource/regulatory_candidate_queue.md`
5. Run first 4-card continuity-review batch (`_internal/continuity_review/validation_batch_01.md`)
6. Outcomes audit: identify which of the 40 empty-outcome programs can actually be populated
7. Resolve 6 programs missing guide placements in `public/data/official_resource_placements.json`

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
