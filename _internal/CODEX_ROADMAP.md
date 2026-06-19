# WGU Atlas Next-Work Roadmap

Generated: 2026-06-18  
Purpose: forward-looking execution backlog for the next phase of WGU Atlas  
Audience: Buddy, strong Codex sessions, and weaker coding agents  

This roadmap reflects the repo state after the 2026-06 catalog mirror refresh.
It is not a replacement for `_internal/ATLAS_CONTROL.md`; it is an execution
planning artifact that turns current control-state into a phased backlog.

---

## 1. Current State Summary

### What is true now

- Atlas has a local catalog artifact mirror at `data/catalog/`.
- The mirror now spans 111 catalog editions, `2017-01` through `2026-06`.
- Missing catalog editions remain `2017-02`, `2017-04`, and `2017-06`.
- Mirrored catalog families now include:
  - `data/catalog/change_tracking/`
  - `data/catalog/edition_diffs/`
  - `data/catalog/helpers/`
  - `data/catalog/program_names/`
  - local gitignored `data/catalog/raw_catalog_texts/`
- Raw PDFs were intentionally not mirrored into Atlas.
- `public/data/` remains a 2026-03 site-current runtime layer.
- `data/catalog/trusted/` contains only `trusted/2026_03/`.
- `scripts/build_site_data.py` now prefers `WGU_CATALOG_OUTPUTS`, but it still reads current-course/current-cert inputs from `trusted/2026_03`.
- The upstream acquisition/parser/change-tracking pipeline still physically lives in `/Users/buddy/Desktop/WGU-Reddit/WGU_catalog`.
- Future intended boundary remains `wgu-catalog`, but the split has not been performed.

### What was completed in the last session

- Mirrored fresh change tracking and edition diff outputs into Atlas.
- Added `data/catalog/program_names/` to Atlas.
- Locally copied 111 raw text files into `data/catalog/raw_catalog_texts/`.
- Added `.gitignore` protection for raw catalog text files.
- Documented the 2026-06 mirror state and split-readiness posture.
- Updated `scripts/build_site_data.py` path configuration:
  - preferred: `WGU_CATALOG_OUTPUTS`
  - compatibility: `WGU_REDDIT_PATH`
  - default: `data/catalog/`
- Logged the parser footgun: `parse_catalog_v11.py` is authoritative only for full-corpus runs.

### Verified recent catalog changes

- `2026-03 -> 2026-04`: no course or program changes.
- `2026-04 -> 2026-05`: 28 course additions and 2 program additions: `BSAIE`, `BSPM`.
- `2026-05 -> 2026-06`: `E200` added, `D436` removed, no program additions/removals, 2 version changes.

### What is still frozen or deferred

- Public site-current data is still frozen at 2026-03.
- `homepage_summary.json` still reports:
  - `data_date: 2026-03`
  - `archive_span: 2017-01 to 2026-03`
  - `total_editions: 108`
- `public/data/courses.json` and `public/data/programs.json` still expose `last_seen: 2026-03` in current runtime records.
- No trusted 2026-06 current snapshot exists.
- No full repo split has been started.
- Atlas QA remains active but is not the main publishability blocker for the public site.
- Homepage redesign remains the primary product/design track, but catalog currency now needs an operational decision before publishing claims about latest coverage.

### Contradictions and ambiguities remaining

- Some docs and runtime artifacts correctly say 2026-03 because the public site-current snapshot is still 2026-03.
- Some mirror docs correctly say 2026-06 because history/diff artifacts now include 2026-04/05/06.
- This is not a bug by itself, but it is an easy source of user-facing overclaiming.
- `build_site_data.py` variable names still use `courses_2026` for 2026-03 inputs; this is misleading but not currently behavior-breaking.
- `summary_stats.json` reports `active_codes: 0` and `active_programs: 0`; treat those fields cautiously until the upstream change-tracking schema is reviewed.
- The prompt from the prior session said no program changes in the new editions, but verified artifacts show 2 program additions in `2026-04 -> 2026-05`.

---

## 2. Immediate Operational Priorities

### P0 — Preserve current truth and avoid accidental publish drift

Objective: keep the repo honest while the mirror and runtime layers disagree.

Do first:
- Keep `README.md`, `data/catalog/README.md`, and control docs explicit about the split state:
  - mirror latest: 2026-06
  - public site-current: 2026-03
- Do not update public copy to claim 2026-06 current active course/program state until `public/data/` is regenerated from a trusted 2026-06 snapshot.
- Do not run `scripts/build_site_data.py` as a publish step until the trusted snapshot issue is resolved.

Why this matters:
- Atlas is a public reference product. A mismatch between mirrored history and runtime current state can easily become a trust problem if the UI claims the latest current edition but renders old active rosters.

Suitable for:
- Weaker agents can audit docs for wording consistency.
- Strong Codex should handle any runtime data regeneration decision.

### P1 — Create a trusted 2026-06 current snapshot

Objective: make 2026-06 publishable as the site-current edition.

The required missing artifact family is:
- `data/catalog/trusted/2026_06/`

Expected outputs, by analogy to `trusted/2026_03/`:
- `courses_2026_06.csv`
- `certs_2026_06.csv`
- `course_index_2026_06.json`
- `sections_index_2026_06.json`
- `degree_snapshots_2026_06.json`
- `program_blocks_2026_06.json`
- `program_index_2026_06.json`
- `manifest_2026_06.json`

Dependencies:
- Full-corpus parser output must be valid.
- 2026-06 raw text must be present and verified.
- A snapshot-freeze script or documented manual copy procedure must exist.
- Validation must compare 2026-06 current counts and high-risk changes.

Decision owner:
- Strong Codex plus operator approval if this requires long upstream pipeline runs.

Exit criteria:
- `trusted/2026_06/` exists.
- Its manifest states source files, counts, generated time, and validation status.
- The trusted snapshot can be consumed by Atlas without direct reads from `/Users/buddy/Desktop/WGU-Reddit/WGU_catalog`.

### P2 — Make `build_site_data.py` edition-configurable

Objective: allow Atlas to generate public runtime exports from either 2026-03 or 2026-06 without code edits.

Concrete tasks:
- Add a `WGU_CATALOG_CURRENT_EDITION` env var, defaulting to `2026_03` until explicitly switched.
- Replace hardcoded `trusted/2026_03` with `trusted/{edition}`.
- Resolve filenames dynamically:
  - `courses_{edition}.csv`
  - `certs_{edition}.csv`
  - `manifest_{edition}.json`
  - other trusted files as needed
- Rename local variables from `courses_2026` / `certs_2026` to `current_courses` / `current_certs`.
- Replace hardcoded homepage fields:
  - `data_date`
  - `archive_span`
  - `total_editions`
  - `total_course_codes_ever`
- Drive those fields from `summary_stats.json` and/or trusted manifest.
- Keep a clear failure if the requested trusted snapshot does not exist.

Dependencies:
- Can be done before `trusted/2026_06/`, but should not be used for publish until the snapshot exists.

Suitable for:
- Strong Codex for first implementation because the script writes many runtime artifacts.
- Weaker agents can later update docstrings/tests once the pattern is established.

Exit criteria:
- Running with default edition still reproduces the existing 2026-03 semantics.
- Running with `WGU_CATALOG_CURRENT_EDITION=2026_06` fails clearly until the trusted snapshot exists, then succeeds after it exists.

### P3 — Decide whether to publish 2026-06 runtime data before homepage redesign

Objective: avoid interleaving two major public changes without a plan.

Decision options:
- Option A: publish catalog currency first.
- Option B: keep site-current frozen at 2026-03 and proceed with homepage redesign.
- Option C: do both in a coordinated release branch.

Recommended default:
- Publish catalog currency first if the 2026-06 trusted snapshot can be produced in a bounded pass.
- Otherwise keep 2026-03 site-current explicit and proceed with homepage planning without changing currency claims.

Why:
- Homepage redesign will likely reuse headline stats. Those stats should not be redesigned around stale or ambiguous data.

---

## 3. Strategic Phases

### Phase 0 — Stabilize and Commit the Mirror State

Objective:
- Make the current mirror/docs state reviewable and recoverable before additional changes pile on.

Why it matters:
- The working tree is already dirty. The 2026-06 mirror pass touched real data and docs. This should not remain an ambiguous uncommitted blob.

Inputs/dependencies:
- Current modified files.
- Operator decision on whether to commit now or fold into a larger branch checkpoint.

Concrete tasks:
- Review `git status --short`.
- Decide whether `data/catalog/program_names/` should be committed. It is about 3.3 MB and useful for split readiness.
- Confirm `data/catalog/raw_catalog_texts/*.txt` stays local/ignored.
- Confirm helper JSONs stay ignored.
- Check line-ending warnings for mirrored CSVs; decide whether to normalize now or leave as source-format churn.
- Commit or explicitly checkpoint the mirror/docs changes.

Success condition:
- The mirror refresh has a clean commit or clear checkpoint.
- The repo can distinguish pre-existing unrelated changes from catalog mirror changes.

Agent fit:
- Weaker agents can list and summarize changed files.
- Strong Codex should decide commit grouping if unrelated dirty work overlaps.
- Operator owns actual commit/push policy if desired.

### Phase 1 — Trusted 2026-06 Snapshot and Validation

Objective:
- Freeze a current-edition snapshot for 2026-06 that can safely replace 2026-03 as the public site-current baseline.

Why it matters:
- The site cannot honestly claim current 2026-06 active courses/programs until the trusted current snapshot exists and is consumed.

Inputs/dependencies:
- `data/catalog/raw_catalog_texts/catalog_2026_06.txt`
- `data/catalog/program_names/2026_06_program_blocks_v11.json`
- `data/catalog/program_names/2026_06_program_index_v11.json`
- Current source trusted snapshot convention in `data/catalog/trusted/2026_03/`
- Upstream parser output conventions

Concrete tasks:
- Inventory how `trusted/2026_03/` was originally produced.
- Create a small snapshot-freeze script if none exists.
- Generate `trusted/2026_06/` from existing mirrored helpers/program blocks if possible.
- If not possible from Atlas mirror alone, run the smallest safe upstream command needed, but avoid single-edition parser runs.
- Build a validation manifest that checks:
  - expected edition ID
  - source text size and existence
  - AP course count
  - certificate course count
  - program block count
  - known changes: `E200` present, `D436` absent from current active AP set
  - `BSAIE` and `BSPM` present in current program set
  - no missing core trusted files
- Document the freeze procedure in `data/catalog/README.md`.

Success condition:
- `data/catalog/trusted/2026_06/` exists and passes a focused validation check.
- No single-edition parser run was used to generate global indexes.

Agent fit:
- Strong Codex.
- Weaker agents can inspect counts and compare JSON/CSV rows after the snapshot exists.
- Operator-only if a long full upstream pipeline must be rerun.

### Phase 2 — Edition-Configurable Site-Data Build

Objective:
- Make site export generation explicit about the current edition and source root.

Why it matters:
- Hardcoded `trusted/2026_03` is now the main blocker between mirrored history and publishable current data.

Inputs/dependencies:
- `scripts/build_site_data.py`
- `data/catalog/trusted/2026_03/`
- eventual `data/catalog/trusted/2026_06/`
- `public/data/` runtime schema

Concrete tasks:
- Add `WGU_CATALOG_CURRENT_EDITION`.
- Convert trusted paths and filenames to use that edition.
- Replace hardcoded homepage summary values with data-driven values.
- Add preflight checks:
  - trusted directory exists
  - required files exist
  - helper files exist
  - `summary_stats.editions` is compatible with generated archive span
- Add a dry-run or validation-only mode if practical.
- Run build against 2026-03 first and compare output shape.
- Run build against 2026-06 only after Phase 1.

Success condition:
- Build script can target current edition explicitly.
- The default path remains safe.
- A failed missing-snapshot case is obvious and non-destructive.

Agent fit:
- Strong Codex for implementation.
- Weaker agents can update README examples and run syntax checks.

### Phase 3 — Public Runtime Refresh to 2026-06

Objective:
- Regenerate and validate `public/data/` and downloadable `data/site` / canonical outputs for the 2026-06 site-current baseline.

Why it matters:
- This is the step that changes what users see as active/current.

Inputs/dependencies:
- Phase 1 trusted snapshot complete.
- Phase 2 build script edition-configurable.
- Local helper files present.

Concrete tasks:
- Run `scripts/build_site_data.py` with:
  - `WGU_CATALOG_OUTPUTS=data/catalog`
  - `WGU_CATALOG_CURRENT_EDITION=2026_06`
- Inspect generated diffs in:
  - `public/data/homepage_summary.json`
  - `public/data/courses.json`
  - `public/data/programs.json`
  - `public/data/search_index.json`
  - `public/data/events.json`
  - `data/canonical_courses.{csv,json}`
  - `data/site/`
- Validate public-data expectations:
  - homepage date is 2026-06
  - total editions is 111
  - `E200` is represented correctly
  - `D436` is no longer active
  - `BSAIE` and `BSPM` appear as active/current programs if upstream says they are current
  - no runtime routes break for removed/replaced courses
- Run `npm run build`.
- If feasible, run `npm run lint`.
- Manually inspect `/wgu-atlas/`, `/wgu-atlas/courses/D436`, `/wgu-atlas/courses/E200`, `/wgu-atlas/programs/BSAIE`, `/wgu-atlas/programs/BSPM`, `/wgu-atlas/timeline`, and `/wgu-atlas/data`.

Success condition:
- Static build passes.
- UI copy and runtime stats no longer contradict data currency.
- The site can be published as current through 2026-06.

Agent fit:
- Strong Codex for first full refresh.
- Weaker agents can run route smoke checks and document observations.
- Operator-only if deciding to deploy.

### Phase 4 — Catalog Pipeline Hardening Before Repo Split

Objective:
- Make the pipeline safer before moving it into `wgu-catalog`.

Why it matters:
- Splitting an unsafe pipeline into a new repo just moves the hazards. The single-edition parser default is the highest-priority hazard.

Inputs/dependencies:
- Upstream `/Users/buddy/Desktop/WGU-Reddit/WGU_catalog`
- `parse_catalog_v11.py`
- `acquire_catalog.py`
- `validate_editions.py`
- `build_change_tracking.py`
- `build_edition_diffs.py`

Concrete tasks:
- Change parser CLI behavior so authoritative downstream outputs require `--all` or an explicit `--single-edition-dev` mode.
- Make single-edition runs write to a scratch/dev output root by default, not the authoritative output tree.
- Add preflight warnings when the input edition count is less than the known corpus count.
- Add structural health checks for newly acquired editions:
  - file size anomaly
  - AP section anchor present
  - Total CUs terminators found
  - Program Outcomes anchor expected/optional by era
  - Certificates section expected from 2024-09 forward
  - course/program count sanity versus prior edition
  - footer/copyright pattern sanity
- Document canonical command sequence:
  - acquire/check
  - download/extract
  - full parse
  - validate
  - change tracking
  - edition diffs
  - mirror to Atlas
- Add a machine-readable manifest of current corpus editions and known gaps.

Success condition:
- A future weaker agent cannot accidentally corrupt global outputs with a single-edition run.
- There is a clear validation gate before mirror/publish.

Agent fit:
- Strong Codex for CLI changes and guardrails.
- Weaker agents can add documentation and simple file-existence checks once patterns are set.

### Phase 5 — wgu-catalog Split Readiness

Objective:
- Prepare a low-risk future split without doing it prematurely.

Why it matters:
- The catalog pipeline has outgrown `wgu-reddit`, but Atlas currently depends on its outputs. The split should improve boundaries, not break reproducibility.

Inputs/dependencies:
- Hardened pipeline command sequence from Phase 4.
- Stable mirror convention in Atlas.
- Decision on whether Atlas mirrors outputs or reads from a sibling checkout.

Concrete tasks:
- Create a split inventory:
  - acquisition scripts
  - parser scripts
  - validation scripts
  - change tracking scripts
  - edition diff scripts
  - shared libs/config
  - raw/source data policies
  - outputs that downstream repos consume
- Define public output contract for `wgu-catalog`:
  - directory layout
  - schema expectations
  - versioning/freeze convention
  - current-edition trusted snapshot convention
  - changelog or manifest
- Define downstream consumer roles:
  - Atlas consumes catalog mirror/output contract.
  - wgu-reddit consumes catalog outputs for Reddit analysis/site-data build.
  - wgu-catalog owns acquisition/parser/validation/diffs.
- Draft but do not execute a move order:
  - Phase A: copy scripts and docs into new repo
  - Phase B: verify outputs match existing source
  - Phase C: point Atlas to new output root
  - Phase D: remove old incidental ownership from wgu-reddit
- Document rollback plan.

Success condition:
- A future repo split can be executed as a controlled migration with known consumers and verification points.

Agent fit:
- Strong Codex for architecture and move plan.
- Weaker agents can build file inventories and doc tables.
- Operator-only for actual repo creation, remotes, and destructive removals.

### Phase 6 — Product Roadmap After Data Currency

Objective:
- Resume product value work after the data currency question is settled.

Why it matters:
- The site’s value comes from usable research surfaces, not just data freshness.

Priority order after catalog publishability:
- Homepage redesign implementation plan.
- Official resource layer completeness pass.
- Course-page enrichment follow-ups.
- Atlas QA F-089 regression fix.
- Non-BSDA degree-homepage reconciliation pilot.
- Continuity review first batch.
- Program lineage export/UI only if explicitly selected.

Agent fit:
- Homepage planning and UI implementation need strong Codex plus visual QA.
- Official resource audits can be split between weaker agents and strong review.
- Small Atlas QA bug fixes need strong Codex if eval behavior is involved.

---

## 4. Decision Points / Forks

### Decision 1 — Freeze trusted 2026-06 now or later

Recommended: freeze now if the upstream snapshot generation is bounded.

Choose now if:
- The operator wants Atlas to reflect latest catalog state soon.
- The trusted snapshot can be generated without a long risky rebuild.
- You want homepage stats to be current before redesign.

Choose later if:
- The trusted snapshot procedure is unclear.
- The public site does not need immediate latest-current claims.
- The next priority is product design, not data currency.

Default if unresolved:
- Keep site-current frozen at 2026-03 and keep docs explicit.

### Decision 2 — Regenerate `public/data/` now or keep frozen

Recommended: do not regenerate until `trusted/2026_06/` exists.

Regenerate only when:
- trusted 2026-06 snapshot exists
- build script can target editions explicitly
- validation route list is ready

Default if unresolved:
- Do not regenerate.

### Decision 3 — Start `wgu-catalog` repo split now or defer

Recommended: defer actual split until after parser guardrails and output contract are documented.

Start now only if:
- Operator explicitly activates the split.
- There is time to verify output parity.
- Consumer path strategy is decided.

Default if unresolved:
- Keep preparing split readiness in docs and guardrails.

### Decision 4 — Atlas mirror strategy vs direct-read strategy

Recommended: keep Atlas mirror strategy.

Why:
- Atlas remains buildable without live reads from upstream repo paths.
- It preserves public repo reproducibility for committed runtime artifacts.
- It reduces coupling while `wgu-catalog` does not yet exist.

Alternative:
- Direct-read from sibling `wgu-catalog` checkout for local builds.

Default if unresolved:
- Mirror stable outputs into `data/catalog/`; use `WGU_CATALOG_OUTPUTS` as the explicit escape hatch.

### Decision 5 — Commit raw program-name artifacts or ignore them

Recommended: commit `data/catalog/program_names/`.

Why:
- It is small enough at about 3.3 MB.
- It is useful for QA, future current snapshot freeze, and split-readiness.
- It avoids requiring raw text/helper regeneration for every inspection.

Default if unresolved:
- Commit `program_names/`; keep `raw_catalog_texts/` and helpers ignored.

### Decision 6 — Homepage before or after catalog currency

Recommended: catalog currency gate first, unless snapshot generation becomes a time sink.

Why:
- Homepage proof modules and stats will depend on current data claims.
- Redesigning around stale stats creates avoidable rework.

Default if unresolved:
- Write homepage plan in data-neutral language, then implement after currency decision.

---

## 5. Cleanup and Polish Backlog

### Documentation cleanup

- Add a short "data currency matrix" to `README.md`:
  - mirror latest
  - site-current latest
  - guide data vintage
  - official resource layer status
- Update `README_INTERNAL.md` generated timestamp or mark it as manually amended.
- Add `CODEX_ROADMAP.md` to the artifact map in `ATLAS_CONTROL.md` if it becomes the active next-work guide.
- Reduce duplicate 2026-03/2026-06 explanations once a trusted 2026-06 snapshot exists.
- Audit project-overview docs for outdated 108-edition claims, but do not rewrite broad long-form docs until site-current decision is made.

### Path unification

- Prefer `WGU_CATALOG_OUTPUTS` in Atlas docs and scripts.
- Keep `WGU_REDDIT_PATH` only as compatibility.
- Introduce `WGU_CATALOG_CURRENT_EDITION`.
- Avoid hardcoded `/Users/buddy/Desktop/WGU-Reddit/WGU_catalog` outside internal docs/logs.
- Build a small path preflight helper if multiple scripts begin using the same env vars.

### Naming consistency

- Replace misleading `courses_2026` / `certs_2026` variable names in `build_site_data.py`.
- Rename comments that say "2026" when they mean "current trusted edition".
- Use edition IDs consistently:
  - filesystem: `2026_06`
  - display: `2026-06`
- Keep `trusted/2026_03` language clear: frozen current-site snapshot, not "latest".

### Mirror hygiene

- Keep helper JSONs ignored.
- Keep raw text files ignored unless a future explicit storage policy changes.
- Commit or intentionally ignore `program_names/`.
- Add a mirror manifest in `data/catalog/` with:
  - source path
  - mirror timestamp
  - file counts
  - latest edition
  - ignored local-only families
- Consider a future `scripts/mirror_catalog_outputs.py` to replace manual `cp` commands.

### Trust/freeze conventions

- Define what makes a trusted current snapshot trusted:
  - generated from full-corpus parser output
  - count checks pass
  - known transition assertions pass
  - manifest written
  - no direct manual row edits
- Use a separate `trusted/YYYY_MM/manifest_YYYY_MM.json`.
- Never overwrite an older trusted snapshot in place.

### Parser safety

- Remove or reverse the default behavior where `parse_catalog_v11.py` processes only 2026-03 and then writes global outputs.
- Require explicit dev mode for single-edition runs.
- Add output-root isolation for dev runs.
- Add a validation command that must pass before mirror.

### UI polish folded into later phases

- When runtime data moves to 2026-06, inspect course and program pages for replaced/removed entities:
  - `D436`
  - `E200`
  - `BSAIE`
  - `BSPM`
- Update user-facing "current catalog" labels only after runtime refresh.
- Re-check `/data` and `/methods` pages for data currency language.
- Keep public UI free of internal extraction confidence labels.

---

## 6. Delegation Guidance

### Good for weaker coding agents

- Audit docs for stale `108 editions`, `2026-03 latest`, and `WGU_REDDIT_PATH` wording.
- Create tables of current artifact counts.
- Compare `public/data/` dates against `data/catalog/` dates.
- Add or update README examples after strong Codex defines the pattern.
- Build a file inventory for future `wgu-catalog` split.
- Create draft mirror manifests from existing command outputs.
- Run non-destructive smoke checks:
  - `python3 -m py_compile scripts/build_site_data.py`
  - JSON parse checks
  - route/content grep checks
- Build first-pass docs for operational command sequences.

### Should stay with stronger Codex

- Trusted 2026-06 snapshot generation strategy.
- Changes to `parse_catalog_v11.py` CLI behavior.
- Changes to `scripts/build_site_data.py` that affect generated public runtime data.
- First 2026-06 public data regeneration.
- Evaluation of artifact discrepancies, especially program additions/removals.
- Homepage redesign implementation and visual QA.
- Atlas QA eval/generation fixes.
- Actual split architecture for `wgu-catalog`.

### Operator/manual only

- Approving long full-pipeline reruns.
- Creating a new `wgu-catalog` repo or remote.
- Publishing/deploying updated site data.
- Deciding whether `BSAIE`/`BSPM` should be announced as active programs in public copy before full site refresh.
- Manual source review when WGU catalog artifacts are ambiguous.
- Any destructive cleanup in the dirty working tree.

---

## 7. Risk Register

| Risk | Impact | Likelihood | Mitigation |
|---|---:|---:|---|
| Single-edition parser footgun | Corrupts global indexes and downstream diffs | High until fixed | Require `--all` for authoritative runs; isolate dev outputs |
| Missing trusted 2026-06 snapshot | Blocks honest public current refresh | High | Phase 1 snapshot freeze before public regeneration |
| Stale `public/data/` with fresh mirror | User-facing claims can drift from rendered data | High | Keep docs/UI explicit; no 2026-06 public claims until refresh |
| Path/env-var inconsistency | Builds read wrong source tree | Medium | Standardize on `WGU_CATALOG_OUTPUTS`; add preflight checks |
| Repo split coordination | Breaks Atlas/wgu-reddit consumers | Medium | Define output contract before moving code |
| Parser structural fragility | New catalog layout breaks extraction silently | Medium | Add structural health checks and count assertions |
| Large-file handling | Accidental commit of 92 MB raw texts or 58 MB helpers | Medium | Keep `.gitignore`; verify `git status` before commit |
| Line-ending churn in mirrored CSVs | Noisy diffs obscure semantic changes | Medium | Decide normalization policy before committing mirror updates |
| Prompt/document contradiction | Agents follow stale prompt instead of artifacts | Medium | Treat on-disk artifacts as authority; keep session log explicit |
| Homepage redesign over stale stats | Rework and trust issues | Medium | Decide catalog currency before locking homepage stats |
| Dirty working tree | Accidental overwrite of unrelated user work | High | Touch only scoped files; review status by path |

---

## 8. Recommended Execution Order: Next 2-6 Weeks

### Week 1 — Stabilize catalog currency path

1. Review and checkpoint/commit the 2026-06 mirror + docs changes.
2. Decide whether `data/catalog/program_names/` is committed.
3. Inventory how to create `trusted/2026_06/`.
4. Draft or implement a trusted snapshot freeze script.
5. Add parser safety plan to upstream catalog docs.

Exit condition:
- The mirror state is preserved and the exact trusted snapshot path is known.

### Week 2 — Build and validate trusted 2026-06

1. Create `data/catalog/trusted/2026_06/`.
2. Write `manifest_2026_06.json`.
3. Validate known 2026-06 assertions:
   - `E200` present
   - `D436` no longer active/current
   - `BSAIE` present
   - `BSPM` present
   - 111-edition history layer intact
4. Document snapshot freeze convention.
5. Do not regenerate public runtime until validation is clean.

Exit condition:
- 2026-06 is a trustworthy current snapshot.

### Week 3 — Edition-configurable site build

1. Add `WGU_CATALOG_CURRENT_EDITION`.
2. Remove hardcoded `trusted/2026_03` behavior.
3. Run build against 2026-03 to preserve baseline behavior.
4. Run build against 2026-06 in a controlled pass.
5. Inspect generated diffs before accepting.

Exit condition:
- Public-data regeneration is explicit, repeatable, and edition-targeted.

### Week 4 — Publishability validation

1. Run `npm run build`.
2. Run `npm run lint` if dependency state allows.
3. Smoke-test high-risk routes:
   - `/wgu-atlas/`
   - `/wgu-atlas/courses/D436`
   - `/wgu-atlas/courses/E200`
   - `/wgu-atlas/programs/BSAIE`
   - `/wgu-atlas/programs/BSPM`
   - `/wgu-atlas/timeline`
   - `/wgu-atlas/data`
   - `/wgu-atlas/methods`
4. Update public copy for 2026-06 only after runtime data is confirmed.
5. Operator decides deploy timing.

Exit condition:
- Atlas can be honestly published as current through 2026-06.

### Weeks 5-6 — Resume product work with cleaner foundations

1. Convert homepage strategy into implementation-ready module specs.
2. Continue official-resource completeness pass.
3. Pick one small course-page enrichment slice:
   - prereq display from 50 auto-accepted rows, or
   - cert badge display after review queue triage.
4. Fix Atlas QA F-089 regression if QA is needed for the next public or internal demo.
5. Prepare `wgu-catalog` split inventory, but do not execute split unless explicitly activated.

Exit condition:
- Product work resumes on top of a clear data foundation.

---

## 9. Top Recommended Next Actions

1. Checkpoint/commit the catalog mirror and documentation changes separately from unrelated dirty work.
2. Create and validate `data/catalog/trusted/2026_06/`.
3. Make `scripts/build_site_data.py` target the current trusted edition via `WGU_CATALOG_CURRENT_EDITION`.
4. Regenerate `public/data/` only after 2026-06 trusted snapshot validation passes.
5. Harden `parse_catalog_v11.py` so single-edition runs cannot overwrite authoritative global outputs.

---

## 10. Explicit Non-Goals for the Next Pass

- Do not create the `wgu-catalog` repo unless the operator explicitly activates it.
- Do not run long full-pipeline jobs without operator approval.
- Do not regenerate public runtime data from 2026-06 until `trusted/2026_06/` exists.
- Do not perform broad UI redesign while data currency claims are unresolved.
- Do not clean unrelated dirty files opportunistically.
- Do not commit raw PDFs or raw catalog text files to Atlas.
