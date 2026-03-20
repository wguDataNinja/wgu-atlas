# Session Log

---

## 2026-03-20 — Lineage curation overlay: decisions, artifacts, doc patches

**Workstream:** Degree History / Program Lineage

**Decisions locked:**
- Curation overlay model finalized: `lineage_decisions.json` is display authority; `program_history_enrichment.json` is metrics source; `public/data/program_lineage.json` is future page-facing export
- State model finalized: 7 `program_state` values, 5 `history_ui_state` values, 4 `decision` values
- 11 event decisions drafted (7 approve, 1 reject, 1 pending_hitl ×2, 1 pending_gap_check)
- 23 program decisions drafted
- 5 `change_summary_template` strings drafted and wording-guard compliant
- Zero-overlap trigger: any pair with `jaccard_overlap == 0.0` (not min, not all)
- Wording guard: required for Jaccard < 0.15 or unconfirmed Jaccard
- Gap rule: > 6 editions between from/to programs → gap investigation
- Pathway variant rule: active predecessor → `pathway_variant`, not lineage
- §5.5 role split confirmed: enrichment = computed source; decisions = curation authority; future export = page-facing
- Validator severity: 3-tier (ERROR/WARNING/INFO); 20 test cases

**Artifacts created:**
- `data/lineage/draft_lineage_decisions.json`
- `_internal/draft_lineage_change_summaries.md`
- `_internal/draft_lineage_state_model.md`
- `_internal/draft_lineage_doc_patch_plan.md`
- `_internal/lineage_artifact_integration_plan.md`
- `_internal/lineage_validation_plan.md`
- `_internal/draft_DECISIONS_patch.md`
- `_internal/draft_ATLAS_SPEC_patch.md`
- `_internal/WORKFLOW_SESSION_PROTOCOL.md`
- `_internal/PROJECT_CONTINUITY_ATLAS.md`
- `_internal/SESSION_LOG.md` (this file)

**Next session:** Write `scripts/validate_lineage_decisions.py` per spec in `_internal/lineage_validation_plan.md`, then apply doc patches from `_internal/draft_DECISIONS_patch.md` and `_internal/draft_ATLAS_SPEC_patch.md`.

---

## 2026-03-20 — Lineage system: validator, docs, canonical artifact

**Workstream:** Degree History / Program Lineage

**Decisions locked:**
- PLE-025 added to event_decisions as reject_history (was missing; caused D1 errors for BSNPLTR/BSPNTR)
- `data/lineage/lineage_decisions.json` is now the canonical artifact (renamed from draft)
- Validator runs clean: 0 ERRORs, exit 0

**Artifacts created/updated:**
- `scripts/validate_lineage_decisions.py` — 24 checks (A1–A6, B1–B4, C1–C2, D1–D2, E1–E4, F1–F10, G1–G4, H1–H2)
- `data/lineage/lineage_decisions.json` — promoted from draft; now 12 event_decisions, 23 program_decisions
- `docs/DECISIONS.md` — patched: §5.5 replaced, §5.10/5.11 added, §6.1 updated, §6.2 updated, §6.5/6.6/6.7 added
- `docs/ATLAS_SPEC.md` — patched: §5.2 lineage_decisions entry added, §7.3 Stage 1.5 inserted, script registry updated

**Remaining warnings (expected, not blocking):**
- 44 × G4 warnings: active programs with candidates but no decisions entry — normal; second-pass curation needed

**Next session:** Export step — implement `export_program_lineage()` in `scripts/build_site_data.py` → `public/data/program_lineage.json`; or second-pass curation review of the 44 G4-warned active programs.

---

## 2026-03-20 — Operator context control doc established

**Workstream:** Documentation architecture / project operations

**Actions:**
- Created `_internal/ATLAS_OPERATOR_CONTEXT.md` as the new primary internal control surface for active GPT sessions.
- Updated `_internal/PROJECT_CONTINUITY_ATLAS.md` to explicitly point to the new operator doc as the richer operating reference.

**Next session:** Start from `_internal/ATLAS_OPERATOR_CONTEXT.md` and execute the top-ranked recommended session task.
