# DEV LOG

Terse dated ledger. One entry per session.
Each entry records what changed, decisions locked, what's blocked, and the next starting task.

---

## 2026-03-20 (session 4 — regulatory placement pass)

**Done**
- Resolved 3 needs-review items: all 3 → keep (Teacher Licensure Programs, FNP Preceptor, PMHNP Preceptor)
- Added 15 placement entries to `public/data/official_resource_placements.json` (116 → 131)
- New `regulatory_licensure` resource_group introduced (priority 12, label "Licensure & Exams")
- Added GROUP_LABELS entry in `RelevantResources.tsx`
- Coverage: School of Education (3), School of Health (2), BSNPLTR (2), BSNU (1), BSPNTR (1), MSNUFNP (2), MSNUPMHNP (2), School of Business (1), School of Technology (1)

**Decisions locked**
- regulatory_licensure display_priority = 12 (above accreditation at 15, below outcomes at 10)
- All 14 candidates from the queue resolved; none deferred

**Blocked / open**
- NCLEX URL is nested under RN-to-BSN path; verify if BSNPLTR-specific NCLEX page exists
- BSPNTR clinicals: deferred; unclear which clinical pages apply to pre-nursing track
- Education Praxis/Student Teaching degree-level attachments: deferred; need program code enumeration
- ACEN/CCNE nursing accreditation: not found in sitemap pass

**Next starting task**
Outcomes + accreditation completeness audit (Tier 2): check `official_context_manifest_phase1.csv` for any outcomes/accreditation pages not yet in `official_resource_placements.json`.

---

## 2026-03-20 (session 3 — baseline commits + regulatory queue)

**Done**
- Made 3 local commits: data reorg, control-plane docs, src baseline changes
- Built `_internal/official_resource/regulatory_candidate_queue.md` — 14 candidates reviewed; 11 `keep`, 3 `needs-review`, 8 `skip`
- Updated official_resource SESSION_LOG.md and ARTIFACTS.md

**Decisions locked**
- None new this session beyond prior

**Blocked / open**
- 3 `needs-review` items in regulatory queue require page reads before finalizing: #3 Teacher Licensure Programs, #11 FNP Preceptor, #12 PMHNP Preceptor
- NCLEX page for BSNPLTR specifically — verify if degree-specific page exists or if school-level page is the right attachment
- Nursing disclosure/accreditation gaps flagged in queue

**Next starting task**
Curation review: read the 3 `needs-review` pages, confirm or decline, then update `public/data/official_resource_placements.json` with the first round of approved regulatory/licensure placements.

---

## 2026-03-20 (session 2 — housecleaning)

**Done**
- Renamed `data/lineage/program_ineage_events.json` → `program_lineage_events.json` (typo fixed)
- Removed typo fallback from `scripts/generate_program_history_enrichment.py` (line that referenced `program_ineage_events.json`)
- Deleted `scripts/__pycache__/` (junk, already gitignored)
- Deleted empty `docs/` directory (all canon docs live in `_internal/`; docs/ had no purpose)
- Fixed `_internal/ATLAS_REPO_MEMORY.md` repo map: removed stale `docs/` row, updated `data/` to reflect subdirectory structure, added `content_map.txt` entry
- Confirmed `public/screenshots/` does not exist; root-level `screenshots/` is the actual dir (already documented correctly)
- Confirmed `src/app/proto/` and `src/components/proto/` are intentional; already documented in ATLAS_REPO_MEMORY.md as experimental surfaces
- `compare_program_courses.py` typo fallback intentionally left (defensive; harmless now that file is renamed correctly)

**Decisions locked**
- `docs/` removed permanently; all canon lives in `_internal/`
- `content_map.txt` is an active tracked artifact; regenerate after major UI changes

**Blocked / open**
- Same as prior session; data reorg and src changes still uncommitted
- `compare_program_courses.py` typo fallback can be cleaned up in a future script maintenance pass

**Next starting task**
Commit all pending changes (data reorg, src, script fixes, DEV_LOG, ATLAS_CONTROL, ATLAS_REPO_MEMORY), then build `_internal/official_resource/regulatory_candidate_queue.md`.

---

## 2026-03-20 (session 1 — control doc consolidation)

**Done**
- Created `_internal/ATLAS_CONTROL.md` and `_internal/ATLAS_REPO_MEMORY.md` — completed 3-doc control system
- Ran repo readiness scan; identified stale docs, data reorg state, and prep steps
- Fixed authority map: all three control docs now live in `_internal/` (not `docs/`)
- Updated ATLAS_CONTROL.md: stale next-session order replaced, `docs/ATLAS_REPO_MEMORY.md` refs corrected to `_internal/`, lineage artifact paths updated to `data/lineage/`
- Marked K-01 and K-02 in WORKQUEUE.md as superseded (DECISIONS.md and ATLAS_SPEC.md are archived)
- Archived `scripts/bootstrap_source_enrichment_manifest.py` to `_internal/archive/2026-03-final-consolidation/`
- `docs/` directory is intentionally empty; all canon docs live in `_internal/`

**Decisions locked**
- 3-doc system: ATLAS_CONTROL + ATLAS_REPO_MEMORY + DEV_LOG, all in `_internal/`
- official-resource activation is first finish-track after baseline cleanup
- Compare is not the first implementation track; revisit after baseline cleanup
- Lineage export remains deferred; it is not automatic
- `homepage_summary.json` count mismatch: do not patch without confirming it is a true bug vs. semantic count difference

**Blocked / open**
- 15 data file deletions and new `data/site/`, `data/lineage/`, `data/enrichment/` dirs are uncommitted (working tree dirty)
- `LearningOutcomes.tsx`, `programs/[code]/page.tsx`, `CompareSelector.tsx` changes are uncommitted
- `data/lineage/program_ineage_events.json` has a filename typo — verify script references before renaming

**Next starting task**
Commit the pending data reorg + src changes, then build `_internal/official_resource/regulatory_candidate_queue.md`.
