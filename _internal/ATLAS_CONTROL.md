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

If local docs conflict on current progress or next-step sequencing, trust in this order:

1. on-disk execution artifacts (`data/program_guides/{parsed,validation,manifest_rows}`, `data/program_guides/family_validation/`, runtime artifacts in `public/data/`)
2. workstream execution log (`_internal/program_guides/DEV_NOTES.md`, module session logs)
3. module orientation/design docs (`_internal/program_guides/README.md`, `_internal/program_guides/TECHNICAL_READOUT.md`, `_internal/page_designs/*`)

---

## 5. Current workstream status

| Workstream | Status | Current objective | Primary blocker | Next bounded step |
|---|---|---|---|---|
| Program guide extraction | **Guide data collection and extraction COMPLETE** — 115 guides parsed, 751 courses with enrichment data, degree-enrichment policy designed | Build Atlas degree-enrichment artifact generator | site wiring intentionally deferred | implement `build_guide_artifacts.py` — reads extracted data, applies policy, emits Atlas-ready degree-page artifacts (no page wiring yet) |
| Official resource layer | active, bounded queueing established | continue conservative attachment expansion with provenance clarity | placement model expansion and completeness audits are still incomplete | reconcile regulatory queue vs current placements, then run outcomes/accreditation completeness pass |
| Continuity review | initialized, lightweight | validate compact review method | first tiny validation batch not created | create 4-card validation batch |
| Program lineage / degree history | ready, not selected | keep system stable for later export/UI if chosen | export/runtime wiring not implemented | no action unless selected |
| Catalog baseline / site runtime | stable | preserve current deterministic site behavior | none immediate | no action |
| Homepage/product framing rethink | deferred | revisit after module priorities settle | depends on clearer emphasis across modules | defer |

---

## 6. Current module snapshots

### 6.0 Program guide extraction

**Status**
- **Guide data collection and extraction is COMPLETE.**
- 115/115 guidebooks parsed and validated. Parser stable, all 19 program families covered.
- **Guide-derived enrichment data is available for 751 canonical courses** (descriptions + competency bullets + program context).
- Course-matching audit complete: all ambiguous title matches resolved or explicitly recorded as unresolvable.
- **Human entry point:** `data/program_guides/README.md`
- Nothing from this data is yet published to the Atlas site.

**Coverage:**
- Parsed guides: 115/115
- Validated guides: 115/115
- Courses with guide-derived enrichment: 751 (of ~1,641 in the catalog)
- Courses unmatched (guide titles not in catalog): 542 — irreducible without catalog changes
- Publish-ready Atlas artifacts: none yet — the artifact generator has not been built

**Complete family coverage (19 total):**
standard_bs(19), cs_ug(8), education_ba(11), graduate_standard(9), mba(3), healthcare_grad(2), education_bs(4), teaching_mat(9), cs_grad(5), swe_grad(4), data_analytics_grad(3), education_ma(9), endorsement(8), nursing_msn(5), nursing_pmc(4), accounting_ma(5), nursing_ug(2), nursing_rn_msn(3)
education_grad: complete (MSEDL=HIGH + MEDETID=MEDIUM)

**No partial families remaining.**

**Why it matters**
- Program guides contain the richest per-program content: Standard Path with CUs and term, course descriptions, competency bullets, prereq mentions, cert-prep mentions.
- 0 empty course descriptions across all parsed guides. Strongest field in the pipeline.

**Current parser state**
- `scripts/program_guides/parse_guide.py` — stable, tested, no planned rewrites
- Session 18 fix: `_is_bullet_continuation` Title Case guard (≥80% capitalized words → not a continuation). Regression-verified.
- Session 19 fix: `parse_capstone` KeyError. Regression-verified.
- Session 22 fix (3 fixes): SP_CHANGES_RE conditional break, STANDARD_PATH_RE second-table break, Certificate Guidebook title skip.
- Session 23 fix (7 fixes): `looks_like_prose` 3-heuristic expansion, `_is_bullet_continuation` terminal-punctuation override, `ACCESSIBILITY_RE` typo tolerance, `no_footer_lines_found` combined-program suppression, `sp_row_invalid` "Advanced Standing" silent skip. See DEV_NOTES.md Session 23 for full detail.
- Known source-artifact outliers (SP unusable, AoS intact): BSITM, MATSPED, MSCSUG

**Known downstream exclusions**
- BSITM SP, MATSPED SP, MSCSUG SP: source-PDF column extraction failures — AoS usable
- BSPRN SP: Pre-Nursing track only — 15 Nursing-track courses AoS-only (dual-track structural)
- BSNU: version/pub_date/page_count not recoverable (no footer in source PDF) — content intact
- MSRNNUED/LM/NI: degree_title truncated (cosmetic — "Bachelor of Science and Post-Baccalaureate Certificate, Nursing +")
- MSCSAIML degree_title: truncated in parsed output (cosmetic)
- MACCM Corporate Financial Analysis: title/first-sentence quality issue (cosmetic)
- MEDETID: capstone field captures only first of 3 courses (multi-capstone structural limitation)
- MAELLP12: page_count=0 (cosmetic — older guide format, content intact)

**Key files**
- `data/program_guides/README.md` — **human entry point** for the full program-guides area
- `_internal/program_guides/PROGRAM_GUIDE_PROJECT_STATUS.md` — concise operator entry point
- `_internal/program_guides/DEV_NOTES.md` — session history and technical change log
- `data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.{md,json}` — canonical corpus facts
- `data/program_guides/audit/program_guide_claims_register.{md,json}` — approved/disallowed claims
- `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` — design doc for building the Atlas degree-enrichment artifact layer
- `data/program_guides/enrichment/course_enrichment_summary.json` — enrichment coverage counts
- `data/program_guides/bridge/merge_summary.json` — course-matching audit: resolutions, deferred cases, unresolvable records
- `public/data/program_guides/` — not yet created; requires the artifact generator to be built first

**What is complete**
- All 115 guidebooks collected, parsed, and validated
- Per-course descriptions and competency bullets extracted
- Guide courses matched to canonical catalog codes for 751 courses
- Policy and schema for the Atlas degree-enrichment artifact layer fully designed
- Course-matching audit with explicit records for all ambiguous or unresolvable cases

**What is next**
- Build the Atlas **degree-enrichment artifact generator** (`build_guide_artifacts.py`):
  reads extracted guide data, applies the approved policy, and produces Atlas-ready JSON for degree pages.
  Start from `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md`.
- Course-page enrichment and college-level enrichment are later decisions, not part of this next step.

---

### 6.1 Official resource layer

**Status**
- initialized and active
- regulatory/licensure queue artifact exists
- some regulatory/licensure placements are already present in runtime artifact
- broader expansion and completeness auditing remain in progress

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
- outcomes + accreditation completeness audit against sitemap-derived candidates

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
| Q-OFF-QUEUE | After regulatory queueing, what is the next bounded official-resource batch to execute? | run outcomes/accreditation completeness audit |
| Q-OFF-ATTACH | What is the minimum robust attachment model before YouTube expansion? | defer broader YouTube rollout |
| Q-LIN-012 | Should `PLE-012` be accepted as lineage? | reject history |
| Q-LIN-023 | Should `PLE-023` be accepted as lineage? | reject history |
| Q-LIN-028 | Is `PLE-028` true continuity or a gap-linked new launch? | split / retire+new |
| Q-LIN-MATSPED | Is MSSP an acceptable predecessor for MATSPED (M.A.T. Special Education)? Degree-level mismatch concern. | new_from_scratch |
| Q-CONT-001 | Does the 4-card continuity review format produce useful validation signal? | keep continuity work small |

---

## 9. Exact next-session order

Guide data collection and extraction is complete. 115 guidebooks parsed, 751 courses with enrichment data, all course-matching resolved or explicitly recorded. The degree-enrichment artifact layer design (policy, schema, build plan) is also complete.

The design artifacts for the Atlas degree-enrichment layer live in `data/program_guides/audit/` — specifically:
- `PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` (start here)
- `phase_d_publish_policy.{md,json}`, `phase_d_artifact_schema.{md,json}`, `phase_d_build_plan.{md,json}`

1. **Program guide — degree-enrichment artifact generator:** Implement `build_guide_artifacts.py` — reads extracted guide data, applies the approved publish policy, emits Atlas-ready degree-page artifacts for verification. Do not wire runtime pages yet.
2. **Official resource — bounded next pass:** reconcile regulatory queue against current placements, then run outcomes/accreditation completeness audit.
3. Run first 4-card continuity-review batch (`_internal/continuity_review/validation_batch_01.md`)

---

## 10. Key artifact map

| Need | Go to |
|---|---|
| What matters now | `_internal/ATLAS_CONTROL.md` |
| How the repo works | `_internal/ATLAS_REPO_MEMORY.md` |
| What changed recently | `_internal/DEV_LOG.md` |
| Page-state docs, source baseline, homepage design conclusions | `_internal/page_designs/` — see `README.md` for reading order |
| **Program guide extraction — human entry point** | **`data/program_guides/README.md`** |
| Program guide extraction — operator status | `_internal/program_guides/PROGRAM_GUIDE_PROJECT_STATUS.md` |
| Program guide extraction — design and pipeline | `_internal/program_guides/TECHNICAL_READOUT.md` |
| Program guide extraction — session history | `_internal/program_guides/DEV_NOTES.md` |
| Program guide extraction — degree-enrichment design pack | `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` |
| Program guide extraction — enrichment coverage | `data/program_guides/enrichment/course_enrichment_summary.json` |
| Program guide extraction — course-matching audit | `data/program_guides/bridge/merge_summary.json` |
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
