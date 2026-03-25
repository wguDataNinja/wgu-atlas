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

**Project-overview grounding docs**
- `_internal/project_overview/01_SITE_DESIGN_SPEC.md`
- `_internal/project_overview/02_SCOPE_AND_ACCOMPLISHMENTS.md`
- `_internal/project_overview/03_DATA_QUALITY_AND_VALIDATION.md`
- `_internal/project_overview/04_SCRAPING_CHALLENGES.md`

These are not control-surface canon, but they are now the primary long-form reference set for:
- product identity
- current site scope
- accomplishment/coverage claims
- validation posture
- scraping/parsing difficulty record

If control-state questions arise, use ATLAS_CONTROL first. If factual product/scope grounding is needed, use the project-overview docs before older module writeups.

If local docs conflict on current progress or next-step sequencing, trust in this order:

1. on-disk execution artifacts (`data/program_guides/{parsed,validation,manifest_rows}`, `data/program_guides/family_validation/`, runtime artifacts in `public/data/`)
2. current control/memory canon (ATLAS_CONTROL, ATLAS_REPO_MEMORY, DEV_LOG)
3. project-overview grounding docs (`_internal/project_overview/`)
4. workstream execution log (`_internal/program_guides/DEV_NOTES.md`, module session logs)
5. module orientation/design docs (`_internal/program_guides/README.md`, `_internal/program_guides/TECHNICAL_READOUT.md`, `_internal/page_designs/*`)

---

## 5. Current workstream status

| Workstream | Status | Current objective | Primary blocker | Next bounded step |
|---|---|---|---|---|
| **Atlas QA** | **Active** — Sessions 07–11 complete + gold eval run 3 done (82/100); A at 93.3% (gate 95%), G at 90% (gate 100%) | Improve citation reliability (A-008, B-029, C-053, G-100 LLM non-determinism) and address G-100 definitively | Ollama must be running | Write session 12 spec |
| **Degree pages — review/improvement** | **CLOSED** — Sessions 1–2 complete (2026-03-22); all priority fixes implemented and live | No active objective | none | see `_internal/degree_pages/WORK_LOG.md` for deferred follow-ups |
| Program guides / degree pages (wiring) | **CLOSED OUT** — extraction complete, artifacts built, degree pages wired. Guide-derived content is live. | No active objective — narrow follow-ups exist (cert review queue, course-page prereqs, variant policy) but are not the active track | none | see `data/program_guides/README.md` for follow-up list |
| Courses (course-page enrichment) | **READY, NOT ACTIVE — design/prototype phase closed; implementation path is known** | No active objective until selected | not selected as current implementation track | when selected: build variant-toggle UI, wire enrichment into production courses/[code]/page.tsx, then add prereq/cert/reverse-prereq blocks |
| Homepage redesign | **ACTIVE — primary product/design track** | Define and design a research-first homepage that presents Atlas as a student research surface for curriculum inspection, degree comparison, and catalog history | proof-module copy and implementation plan not yet locked | convert homepage strategy into section-level messaging, module specs, and implementation-ready homepage plan |
| Official resource layer | active, bounded queueing established | continue conservative attachment expansion with provenance clarity | placement model expansion and completeness audits are still incomplete | reconcile regulatory queue vs current placements, then run outcomes/accreditation completeness pass |
| Continuity review | initialized, lightweight | validate compact review method | first tiny validation batch not created | create 4-card validation batch |
| Program lineage / degree history | ready, not selected | keep system stable for later export/UI if chosen | export/runtime wiring not implemented | no action unless selected |
| Catalog baseline / site runtime | stable | preserve current deterministic site behavior | none immediate | no action |

---

## 6. Current module snapshots

### 6.0 Program guide extraction / degree-enrichment layer

**Status**
- **CLOSED OUT**
- 115/115 program guides collected, parsed, validated, and converted into degree-enrichment artifacts
- guide-derived content is live on Atlas degree pages

**Durable facts**
- 751 canonical courses enriched with guide-derived descriptions and competency data
- 115 per-program degree artifacts built
- cert/prereq/family/anomaly extraction artifacts exist and remain the source for downstream course-page and review work
- parser is stable; no planned rewrite

**What shipped**
- degree artifacts built and wired into production degree pages
- licensure, cert, family/track, provenance, caveat, AoS, and capstone handling are live
- NCLEX-RN and CPA Exam degree-level signals extracted and surfaced with correct framing
- anomaly-bearing programs handled with explicit caveat messaging

**Not-active follow-ups**
- cert review queue: 21 rows
- course-page prereq display: 50 auto-accepted rows ready
- multi-description / competency variant policy for course pages
- nursing cumulative-prereq display design

**Key files**
- `data/program_guides/README.md`
- `_internal/program_guides/PROGRAM_GUIDE_PROJECT_STATUS.md`
- `_internal/program_guides/DEV_NOTES.md`
- `data/program_guides/audit/PROGRAM_GUIDE_CORPUS_MANIFEST.{md,json}`
- `data/program_guides/bridge/merge_summary.json`
- `data/program_guides/enrichment/course_enrichment_summary.json`

---

### 6.0b Atlas QA

**Status:** Active — sessions 07–11 complete

**What exists:**
- Full deterministic pipeline: entity resolution → exact/fuzzy/compare/clarify routing → evidence bundle → gate → generation → post-check
- 265 unit + integration tests passing
- Model comparison complete: `llama3:latest` selected (9/10 on session07 sample, fastest)
- `qwen3.5:9b` viable (same accuracy, 2–3× slower); `llama3.1:latest` drops 2 queries

**Session outcomes:**
- Session 07: baseline run — 1/10 pass; two blockers identified
- Session 08: blocker fixes (version token, first-candidate bias) → 7/10
- Session 09: compare path routing fix → Class D entity codes now correct
- Session 10: clarify path — 7/8 targeted Class E queries fire clarify; E-066/E-073 invariants preserved
- Session 11: source_object_identity derivation guard (evidence.py); guide-presence gate check 6b (gate.py + answer.py) — G-092/G-099 now deterministically abstain

**Gold eval results — run 3 (2026-03-25T04-06, llama3:latest):**

| Class | Pass | Total | Rate | Gate | Status |
|-------|------|-------|------|------|--------|
| A | 14 | 15 | 93.3% | 95% | FAIL |
| B | 17 | 20 | 85.0% | 85% | PASS ✅ |
| C | 16 | 18 | 88.9% | 85% | PASS ✅ |
| D | 1 | 12 | 8.3% | 80% | FAIL (corpus gap) |
| E | 10 | 10 | 100% | 90% | PASS ✅ |
| F | 15 | 15 | 100% | 98% | PASS ✅ |
| G | 9 | 10 | 90.0% | 100% | FAIL |
| **Total** | **82** | **100** | **82%** | — | — |

Run 3 vs run 2 diff: +5 fixed (A-009, A-015, C-047, G-092, G-099), −4 regressed (A-008, B-018, B-029, C-053 — all LLM non-determinism)

**Known open issues:**
- Class D (11 failures): missing 2025-06 corpus cards — corpus gap, deferred
- Class A (1 failure): A-008 D554 citation — LLM non-determinism (model omits `course_cards/D554` from cited_evidence_ids)
- Class G (1 failure): G-100 MACCA/MACCF guide version — same citation non-determinism (`program_version_cards/MACCA`)
- B-029, C-053: same citation non-determinism pattern (MACCA, D554)
- B-018: BSACC total CU — model abstained (generation returned abstain=true)
- B-031, C-051: BSPRN not in corpus — will always fail; gold question set note
- E-066: gold question note is wrong (MBA is unambiguous; correct behavior is answer)

**Next bounded step:** address citation reliability — model fails to include `source_object_identity` in cited_evidence_ids ~20% of the time; root cause and fix options to be scoped in session 12

**Key files:**
- `scripts/run_gold_eval.py` — full 100-question eval runner
- `scripts/compare_models.py` — model comparison runner
- `src/atlas_qa/qa/` — pipeline source
- `tests/atlas_qa/` — 265 tests
- `data/atlas_qa/runtime_checks/` — all trace artifacts
- `_internal/atlas_qa/QA_GOLD_QUESTION_SET.md` — 100-question eval corpus
- `_internal/atlas_qa/work_sessions/` — session specs and dev logs

---

### 6.1 Official resource layer

**Status**
- initialized and active
- regulatory/licensure queue artifact exists
- some regulatory/licensure placements are already present in runtime artifact
- broader expansion and completeness auditing remain in progress

**Why it matters**
- This is the clearest next student-facing value layer after the current homepage/design track.
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

### 6.4 Degree pages — review/improvement

**Status:** CLOSED — Sessions 1–2 complete (2026-03-22)

**What shipped (Session 2):**
- AoS moved above Course Roster on all degree pages
- AoS course entries now link to `/courses/{code}` where a confident title match exists against the program's catalog roster
- Missing outcomes shows a fallback placeholder ("Program learning outcomes are not available in the current catalog edition.") instead of silent absence
- Advisor-guided banner copy improved to explain sequencing vs. fixed-term
- Suppressed roster block updated to reference AoS above as the primary program map
- Degraded-quality warning block (amber callout) added for low-confidence or caveat-bearing pages; replaces the less-visible inline chip
- Duplicate caveat messaging resolved: `GuideProvenance` pill suppressed when degraded block handles it; `GuideCapstone` partial note suppressed when caveats already covered
- Capstone discovery hint added for programs where `capstone.present=false` but AoS contains a capstone group
- Section label normalized to "Program Learning Outcomes"

**Key files:**
- `_internal/degree_pages/WORK_LOG.md` — session log including Session 2 cohort validation
- Production page: `src/app/programs/[code]/page.tsx`
- Guide components: `src/components/programs/Guide{Provenance,AreasOfStudy,Capstone}.tsx`
- Learning outcomes: `src/app/programs/[code]/LearningOutcomes.tsx`

---

### 6.5 Homepage redesign

**Status**
- **ACTIVE — primary product/design track**
- strategy updated on 2026-03-22
- homepage direction now grounded in both the raw catalog baseline and the official public-site student-experience baseline

**Current conclusion**
- homepage should present Atlas as a research surface
- core framing: Atlas helps students research what a WGU degree actually contains, how it connects to other programs, and how it changed over time
- Atlas should be framed not as the only source of WGU program information, but as the clearest surface for researching that information together
- homepage should be proof-first, not navigation-shell-first

**Locked direction**
- research-first positioning language should remain visible
- degree pages and Compare are the two co-anchor proof modules
- course-connectedness should be framed as following a course across programs
- history/continuity is a real research differentiator
- school navigation is secondary to the academic research story
- homepage should mirror the real student flow: degree → course → overlap → compare

**Current grounding docs**
- `_internal/page_designs/homepage_design_session_2026_03_22.md`
- `_internal/page_designs/wgu_public_site_student_experience.md`
- `_internal/project_overview/01_SITE_DESIGN_SPEC.md`
- `_internal/project_overview/02_SCOPE_AND_ACCOMPLISHMENTS.md`

**Next bounded step**
- turn strategy into implementation-ready homepage module/copy/spec artifact

---

## 7. Locked decisions

These should not be reopened by default.

- Atlas is a reference/explainer product, not a discussion/community product.
- Official resources come before Reddit/community enrichment.
- YouTube comes before Reddit/community, but after tighter official-resource attachment work.
- History/lineage is supporting context, not homepage identity.
- Program History is a program-page enrichment layer, not a separate product surface.
- Continuity review is a bounded validation track, not a large feature buildout.
- Homepage is now the primary active product/design workstream.
- Homepage framing is locked to a research-first, curriculum-inspection posture.
- Atlas should be presented as supporting student research, not as a generic browse shell or enrollment-style exploration surface.
- Degree pages and Compare are the two co-anchor homepage proof surfaces.
- School navigation and ecosystem material are secondary to the academic research story.
- Atlas should not be framed as the only place with WGU program information; the truthful contrast is structural clarity and research usability.
- The official-resource layer is the most likely next major module.
- No standalone Compare expansion track is active; Compare currently matters primarily as a homepage proof surface.
- Lineage export is not an automatic next move; it remains a defer-or-promote decision.
- If a predecessor program is still active, default to pathway-variant logic rather than lineage.
- Approved low-confidence lineage events require guardrails in wording.
- Approved zero-overlap lineage events require explicit rationale.
- Suppressed or unresolved lineage events should not surface by default.

**Ecosystem index note:** A broader WGU online ecosystem index now exists at `_internal/WGU_ONLINE_ECOSYSTEM_INDEX.md` for future homepage/community/social exploration. It does not change the current product posture or the deferred status of Reddit/community integration.

- Multi-source overlap resolution (catalog vs guide description text) uses an artifact-first, bounded-LLM workflow: deterministic comparison index → batched LLM annotation files → explicit block authority and display policy. Do not let LLMs improvise policy directly on raw source corpora. The resolution artifacts live in `_internal/atlas_qa/`.

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

1. **Atlas QA — session 11:** fix Class A postcheck (MACCA/MACCM `source_object_identity` is null in corpus) + Class G guide-presence gate for D554; re-run full eval. Spec: `_internal/atlas_qa/work_sessions/11_postcheck_and_guide_presence_gate/SESSION_SPEC.md`.
2. **Homepage redesign — implementation planning pass:** convert the 2026-03-22 homepage strategy into implementation-ready section/module specs, copy hierarchy, and build order.
3. **Official resource — bounded next pass:** reconcile regulatory queue against current placements, then run outcomes/accreditation completeness audit. Working area: `_internal/official_resource/`.
4. **Course-page enrichment — production implementation planning:** only after homepage planning is stabilized; start from prototype conclusions and define production wiring sequence.
5. **Continuity review first batch:** run first 4-card batch (`_internal/continuity_review/validation_batch_01.md`). Low priority relative to items 1–3.

**Guide-adjacent items that can be picked up any time without blocking other work:**
- Cert review queue (21 rows) — editorial judgment against source text
- Prereq display component for course pages — 50 auto-accepted rows ready

---

## 10. Key artifact map

| Need | Go to |
|---|---|
| What matters now | `_internal/ATLAS_CONTROL.md` |
| How the repo works | `_internal/ATLAS_REPO_MEMORY.md` |
| What changed recently | `_internal/DEV_LOG.md` |
| Current product/site state | `_internal/project_overview/01_SITE_DESIGN_SPEC.md` |
| What Atlas has built / accomplishment claims | `_internal/project_overview/02_SCOPE_AND_ACCOMPLISHMENTS.md` |
| Validation / trust posture | `_internal/project_overview/03_DATA_QUALITY_AND_VALIDATION.md` |
| Scraping/parsing difficulty record | `_internal/project_overview/04_SCRAPING_CHALLENGES.md` |
| Homepage strategy | `_internal/page_designs/homepage_design_session_2026_03_22.md` |
| Official public-site student baseline | `_internal/page_designs/wgu_public_site_student_experience.md` |
| **Degree pages — review/improvement** | **`_internal/degree_pages/`** — artifact, work log, content maps |
| Page-design and source-baseline docs | `_internal/page_designs/` — see `README.md` for reading order |
| **Program guide extraction — human entry point** | **`data/program_guides/README.md`** |
| Program guide extraction — operator status | `_internal/program_guides/PROGRAM_GUIDE_PROJECT_STATUS.md` |
| Program guide extraction — design and pipeline | `_internal/program_guides/TECHNICAL_READOUT.md` |
| Program guide extraction — session history | `_internal/program_guides/DEV_NOTES.md` |
| Program guide extraction — degree-enrichment design pack | `data/program_guides/audit/PHASE_D_POLICY_AND_SCHEMA_MASTER_PLAN.md` |
| Program guide extraction — enrichment coverage | `data/program_guides/enrichment/course_enrichment_summary.json` |
| Program guide extraction — course-matching audit | `data/program_guides/bridge/merge_summary.json` |
| Course/program text overlap policy + annotation artifacts | `_internal/atlas_qa/BLOCK_AUTHORITY_AND_DISPLAY_POLICY.md` and `_internal/atlas_qa/` |
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
