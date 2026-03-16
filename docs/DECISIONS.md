# Atlas Decisions

## 1) Contract
- Purpose: durable normative rules; prevents policy drift and repeated re-debate.
- Scope: provenance boundaries, curation rules, inclusion/exclusion policy, attachment policy, interpretation guardrails, documentation governance.
- Out of scope: implementation inventories, script contracts, schema catalogs (in `docs/ATLAS_SPEC.md`).

## 2) Documentation governance

### 2.1 Canon set
- Canonical docs are:
  - `docs/ATLAS_SPEC.md` (factual implementation spec)
  - `docs/DECISIONS.md` (normative policy)
- All other docs are source material until retired.

### 2.2 One-concept-one-home
- Each concept has one canonical home.
- Structural/procedural -> `ATLAS_SPEC`.
- Normative/policy -> `DECISIONS`.

### 2.3 Merge-not-proliferate rule
- If two docs explain the same process, merge into canon and deprecate duplicates.
- Session logs and narrative residue are not canonical.

## 3) Source/provenance boundaries (hard rules)

### 3.1 Three-layer separation
- Never blur:
  - official catalog facts
  - official WGU context/resources
  - student/community discussion

### 3.2 Interpretation separation
- Atlas interpretation (summaries, classifications, curation) is distinct from source facts.
- Do not present interpretation as if it were source-authored content.

### 3.3 Observed vs interpreted fields
- Event/history narratives must preserve observed/factual and interpreted/curated distinction.

### 3.4 Official-context role
- Official-context links are supporting resources, not catalog-fact replacements.

### 3.5 Trust baseline distinction
- Frozen trusted outputs and regenerated working outputs must remain distinguishable for regression/debugging.

## 4) Parser/data handling guardrails

### 4.1 Raw-context-first debugging
- Parser discrepancy triage must inspect representative raw text context.
- Counts/tables alone are insufficient.

### 4.2 Program identity precedence
- Program code/body identity overrides TOC naming drift.

### 4.3 Scope separation
- AP scope and certificate scope must remain explicit and separate unless a workflow intentionally combines them.

### 4.4 Downstream source of truth
- Downstream reconstruction operates on extracted catalog text layer.
- PDFs are archival source, not repeated downstream parse substrate.

### 4.5 Parser canon
- `parse_catalog_v11.py` is active parser canon.

### 4.6 Course identity base model
- Base historical course identity is exact course code.
- Alias/fuzzy/semantic linkage is optional higher layer, never implicit base behavior.

## 5) Program History policy

### 5.1 Product placement
- Program History is page-level enrichment on program pages, not a separate product.

### 5.2 Inclusion semantics
- Binary decision per event: included or excluded from page surfacing.
- No ranking tier for display policy.

### 5.3 Recall base rule
- `named_events` is not lineage recall base.
- Recall base is transition/candidate artifacts derived from program history + adjacent boundaries.

### 5.4 Stage boundary rule
- Stage 1 (LLM/HITL): semantic lineage judgment.
- Deterministic stages: overlap metrics, diffs, transforms.
- Do not collapse LLM judgment and deterministic computation responsibilities.

### 5.5 Final artifact rule
- Page-facing Program History artifact is `data/program_history_enrichment.json`.
- Intermediate artifacts remain review/analysis layers.

### 5.6 Overlap rule
- Course overlap is major evidence, not absolute gate.
- Low overlap can still be valid lineage if semantic continuity is strong.

### 5.7 Final shape rule
- Final page-facing lineage keeps compact fields:
  - overlap metrics
  - added/removed courses
- Shared course code lists are excluded from final page-facing schema.

### 5.8 Refresh cadence rule
- Historical backfill can be large.
- Monthly runs should be incremental by default.

### 5.9 Heuristic-vs-curation precedence
- Auto `importance`/`site_worthy` is heuristic triage.
- Human-reviewed curation decisions override heuristic flags for page display.

## 6) Program History curation set (current reviewed policy)

### 6.1 Include on program pages
- Early lineage context:
  - `PLE-001` IT Security emphasis -> Network Operations and Security
  - `PLE-002` Networks Administration -> Cloud and Systems Administration
  - `PLE-005` Interdisciplinary Studies (K-8) -> Elementary Education
- Business family:
  - `PLE-008` Business degrees reorganized under Business Administration structure
  - `PLE-019` Business Administration degrees moved back to discipline-specific degrees
- Core technology:
  - `PLE-009` Cloud and Systems Administration -> Cloud Computing
  - `PLE-010` Cloud Computing -> Cloud Computing specialization tracks
  - `PLE-011` Network Operations and Security -> Network Engineering and Security (+ Cisco)
  - `PLE-013` Software Development -> Software Engineering
  - `PLE-014` Data Management / Data Analytics -> Data Analytics
  - `PLE-021` Cloud + Network programs -> Cloud and Network Engineering
  - `PLE-022` MS IT Management -> MS Information Technology (+ Product Management)
- Graduate specialization splits:
  - `PLE-016` MS Data Analytics -> DE / DPE / DS tracks
  - `PLE-017` MS Accounting -> Auditing / Financial Reporting / Management Accounting / Taxation
- Education restructure:
  - `PLE-024` Education programs -> Educational Studies pathways

### 6.2 Exclude from program pages
- `PLE-003`, `PLE-006`, `PLE-007`, `PLE-018`, `PLE-020`, `PLE-025`, `PLE-026`.

### 6.3 Unclassified IDs
- IDs outside include/exclude sets are pending manual curation and are not auto-promoted to page display.

### 6.4 Interpretation scope
- Include/exclude is page-display policy, not existence-denial in historical data.

## 7) Official Context Layer policy

### 7.1 Layer status
- Official context is first-class supporting layer.

### 7.2 Ordering
- Intended stack order:
  - catalog facts
  - official WGU resources
  - (later) student/community discussion

### 7.3 Product posture
- Atlas must not lead as a Reddit/discussion aggregator.

### 7.4 Attachment/surfacing policy
- Curated surfacing only; no sitemap dumps.
- Preferred density: 1-3 strong links per entity surface.
- Use distinct supporting block UI; keep resources visibly official/external.

### 7.5 Discovery policy
- Sitemap is valid bootstrap, not complete universe.
- Newsroom/press-release discovery is separate targeted pass.

### 7.6 Page-type handling rules
- Program guide HTML pages are valid canonical resources (even when PDF wrappers).
- Outcomes pages are high-value resources.
- Specialization/variant pages are high-value resources.
- Accreditation pages attach by scope:
  - school-level -> school pages
  - program-level -> program pages
- URL path alone is insufficient for type classification; content review required.

## 8) Official video policy

### 8.1 Source separation
- Keep sources distinct:
  - official WGU YouTube
  - WGU Career Services YouTube

### 8.2 Surfacing maturity gate
- Do not broadly surface videos until manifest import/classification/placement rules are stabilized.

### 8.3 Curation mode
- Videos are curated supporting resources, not feed streams.

### 8.4 Career Services inclusion rule
- Include only videos that explain domain/field/role context for degree/course understanding.
- Exclude generic job-search advice content (resume/interview/networking/LinkedIn) from Atlas enrichment surfaces.

## 9) Outcomes/assessment enrichment policy

### 9.1 Layer classification
- Outcomes/pass-rate assets are official-context enrichment, not catalog fact layer.

### 9.2 Provenance requirements
- Every extracted metric must retain source page URL + source asset URL + extraction note/status.

### 9.3 Interpretation guardrails
- Program assessment values are program/time-window specific; do not overstate as global course pass rate.
- Lower pass rate is descriptive signal, not causal proof.

### 9.4 Integration stance
- Outcomes/assessment data complements catalog + history (+ later discussion); it does not replace them.

## 10) Timeline/event policy
- Named-event timeline system and program-lineage system are distinct.
- Timeline threshold logic is not lineage recall logic.
- Observed vs interpreted separation applies strongly to timeline artifacts.

## 11) Product-scope constraints
- Atlas is reference/explainer infrastructure, not general discussion site.
- Atlas is not a job-search advice product.
- Prefer restrained, provenance-legible enrichment over maximal content density.

## 12) Student-facing positioning rules

### 12.1 Product lead rule
- Atlas should lead with student-useful navigation for current courses/programs/schools.
- Archive/history capability is supporting context, not homepage identity.

### 12.2 History-as-supporting-context rule
- Historical content is surfaced when it explains the current entity the user is viewing.
- Avoid broad archive narration on core browse/detail surfaces.

### 12.3 Relevance-first attachment rule
- For official web resources, official videos, and future discussion links, attachment must be entity-scoped.
- The question is always `where is this specifically useful?`, not `how do we surface more links globally?`

### 12.4 Homepage restraint rule
- Homepage modules should prioritize student navigation/orientation.
- Generic link dumps and archive-first framing are lower priority than entity-directed paths.

### 12.5 Timeline positioning rule
- `/timeline` is a specialist historical surface.
- It remains available, but should not define overall product tone on primary entry points.

## 13) Provenance display rules

### 13.1 Section-level source labeling
- Fact sections should carry compact source labels with edition context where applicable.

### 13.2 Inline fact vintage labels
- Edition-bound facts may use compact `as-of`/edition labels near key values.
- Avoid verbose inline citation strings and avoid hiding provenance only in footnotes.

### 13.3 Interpretation labeling
- Interpreted summaries should be visibly attributable to Atlas, distinct from official source text.

## 14) Related-program comparison policy

### 14.1 Comparison intent
- Related-program/track comparison is a student decision-support feature (shared vs unique curriculum and overlap context), not a standalone analytics product.

### 14.2 Conditional surfacing
- Show comparison affordances where a meaningful related family exists; do not force on unrelated programs.

### 14.3 Source separation in compare views
- Comparison views must preserve source boundaries:
  - catalog-derived structural differences
  - optional official-context attachments
  - later discussion context (if added) as separate layer

## 15) Degree Compare feature policy

### 15.1 Product intent
- Degree Compare is a student decision-support feature.
- Primary student question: "How different are two programs — and which specific courses differ between them?"
- Compare is a distinct mode from normal program browsing; it must not dilute the browse experience for students who do not need it.
- Compare is not a standalone analytics product; it is enrichment on existing program surfaces.

### 15.2 Compare vs browse separation
- Compare affordances are shown conditionally — only where a meaningful related-program family exists.
- Program pages for programs not in any recognized family show no compare UI.
- Spurious or low-information diffs (cross-level, cross-school, unrelated programs) are not surfaced.

### 15.3 V1 scope constraints
- V1 compare is always 2-way: exactly one left program vs one right program.
- 3-way or n-way compare is deferred; family definitions may list >2 programs but the v1 UI always renders a single pair.
- V1 constraint: same school AND same degree level (e.g., two bachelor's programs in Technology; two master's programs in Business).
- Rationale: cross-school and cross-level comparisons produce low-value diffs (mostly unique courses on both sides) that do not help student decisions.
- V1 focuses on current (ACTIVE) programs only; retired-program compare is deferred.
- V1 families are curated explicitly; auto-detection from data alone is deferred.

### 15.4 Core comparison object
- The core comparison object is the course roster: the ordered list of course codes per term extracted from `program_enriched.json`.
- Identity uses exact course code per §4.6; no aliasing, fuzzy matching, or semantic linkage across codes.
- Compare is executed by `compareRosters()` in `src/lib/programs.ts`.

### 15.5 Primary comparison value
- Shared vs unique curriculum is the primary student-useful comparison output.
- Key output fields: shared course codes, left-unique codes, right-unique codes, shared count, Jaccard overlap, left-retained-pct, right-inherited-pct.
- Jaccard overlap semantics match those of `program_lineage_enriched.json` (reuse existing metric definition).
- Provenance and history metadata (when courses were added, version timestamps) are secondary to decision usefulness and deferred to a later phase.

### 15.6 History metadata is secondary
- Program history context (lineage, prior name) may appear on compare surfaces only as supporting context.
- Do not lead compare UI with historical narration; lead with the current course diff.

### 15.7 Source separation in compare views
- Compare views must preserve Atlas source boundaries (per §3):
  - catalog-derived structural differences (courses, term structure): primary layer.
  - official-context attachments (program guides, outcomes pages): optional enrichment, deferred phase.
  - discussion context: deferred phase.
- Do not blend official-context commentary or discussion with course diff output.

### 15.8 Page and route model
- V1 compare is surfaced as an affordance on program detail pages (`/programs/[code]`) where the program belongs to a recognized family.
- A standalone `/compare` route is deferred until the feature proves utility in V1.
- V1 does not require a new top-level nav entry.

### 15.9 V1 display ordering
- Compare output is displayed in this order:
  1. Program headers (left vs right): name, school, degree level, CUs, first-seen date.
  2. Overlap summary: shared count, left-only count, right-only count, Jaccard overlap %.
  3. Shared courses — sorted by term in left program.
  4. Left-only courses — sorted by term in left program.
  5. Right-only courses — sorted by term in right program.
- Rationale: establishing shared ground first (what you take regardless of choice) frames the diffs as marginal additions, which is how students think about track decisions.

### 15.10 V1 program-added-date decision
- Program `first_seen` date is included in v1 compare output.
- Rationale: first-seen communicates program maturity; a new track (2024+) vs an established track (2019+) is relevant student context.
- Source: `ProgramRecord.first_seen` from `programs.json`.

### 15.11 V1 course-added-date decision (deferred)
- Per-course first-seen-in-program dates are deferred from v1.
- Rationale: requires joining `courses/{code}.json` `programs_timeline` per course, which adds fetch complexity for low decision value in v1. Students comparing tracks care about what they'll take, not when each course was added to the roster.
- Deferred to: post-v1, after v1 usage validates the feature direction.

### 15.12 V1 comparable-family qualification rules
Six rules; a family must satisfy all six to receive compare affordances.
1. **Same school**: all member programs share the same `canonical_key` (matches `ProgramRecord.school`).
2. **Same degree level**: all member programs share the same `DegreeLevel` per `classifyDegreeLevel()`.
3. **Meaningful overlap**: Jaccard ≥ 0.25 for each pair in the family. Establishes a recognizable shared core; below this threshold programs are not structurally related enough for compare to be useful.
4. **Meaningful differences**: each program in the pair contributes ≥ 2 unique courses. Pairs where one side has only 1 unique course (e.g., MBA vs MBAITM/MBAHA, which differ only by a capstone swap) are too trivially different to warrant a compare feature.
5. **Active programs only**: all member programs have `status === "ACTIVE"`. Retired programs are excluded in v1.
6. **Curated affirmation**: rules 1–5 are necessary but not sufficient. A human curation step confirms that the comparison represents a genuine student choice (e.g., "which language track should I pick?" is a real decision; two unrelated programs that happen to share gen-ed courses are not).

### 15.13 V1 content contract (per compare payload)
Complete field inventory for `ComparePayload` from `src/lib/families.ts`.
- `family_id`: string — identifies the curated family.
- `left` / `right` (`CompareProgramMeta`): `program_code`, `canonical_name`, `school`, `degree_level`, `total_cus`, `first_seen`, `course_count`.
- `shared_courses` (`CompareCourseEntry[]`): each entry has `code`, `title`, `cus`, `term_left`, `term_right`. Sorted by `term_left`. For shared courses where term placement differs between programs, both terms are present.
- `left_only_courses` (`CompareCourseEntry[]`): same entry shape; `term_right` is null. Sorted by `term_left`.
- `right_only_courses` (`CompareCourseEntry[]`): same entry shape; `term_left` is null. Sorted by `term_right`.
- `metrics` (`CompareResult`): `shared_count`, `left_count`, `right_count`, `left_only_codes`, `right_only_codes`, `jaccard_overlap`, `left_retained_pct`, `right_inherited_pct`.
- Fields absent from v1 payload: course first_seen_in_program, official-context links, outcome diffs, discussion context.

### 15.14 Session 2 pilot compare reviews

#### Pilot 1: BSSWE vs BSSWE_C — Bachelor of Science, Software Engineering (Java vs C#)
- School: School of Technology · Level: Bachelor's · CUs: 119 vs 119 · First seen: 2023-01 vs 2023-01
- Roster: 38 courses (Java) vs 36 courses (C#) · **33 shared · 5 Java-only · 3 C#-only**
- Jaccard: 0.805 · Left retained: 86.8% · Right inherited: 91.7%
- Unique to Java track: Java Fundamentals (D286), Java Frameworks (D287), Back-End Programming (D288), Advanced Java (D387), Mobile Application Development – Android (D308). All in Terms 5–9.
- Unique to C# track: Software I – C# (C968, 6 CUs), Software II – Advanced C# (C969, 6 CUs), Mobile Application Development Using C# (C971, 3 CUs). All in Terms 6–9.
- Notable: C# track has 3 fewer courses but the same 119 CUs because C968 and C969 carry 6 CUs each vs 3 CUs for their Java equivalents. The capstone (D424 Software Engineering Capstone) is shared — both tracks end with the same final project.
- Two shared courses (D270 Composition, C458 Health/Fitness/Wellness) appear in different terms between tracks (minor scheduling placement, not curriculum difference).
- Student-meaningfulness: high. The comparison directly answers "which language track should I take?" with a concrete list of what changes. The shared core is large and reassuring; the unique courses are immediately recognizable as language-specific.

#### Pilot 2: MSDADE vs MSDADS — MS Data Analytics (Data Engineering vs Data Science)
- School: School of Technology · Level: Master's · CUs: 32 vs 32 · First seen: 2024-06 vs 2024-06
- Roster: 11 courses each · **7 shared · 4 Data Engineering-only · 4 Data Science-only**
- Jaccard: 0.467 · Left retained: 63.6% · Right inherited: 63.6%
- Shared core (all 7 shared courses are in Terms 1–3): Analytics Programming (D598), Data Management (D597), The Data Analytics Journey (D596), Data Preparation and Exploration (D599), Statistical Data Mining (D600), Data Storytelling for Varied Audiences (D601), Deployment (D602).
- Unique to Data Engineering (Terms 3–4): Cloud Databases (D607), Data Processing (D608), Data Analytics at Scale (D609), Data Engineering Capstone (D610).
- Unique to Data Science (Terms 3–4): Machine Learning (D603), Advanced Analytics (D604), Optimization (D605), Data Science Capstone (D606).
- Structure: Terms 1–2 are entirely shared (6 courses). Term 3 splits: 1 shared (Deployment) + 2 specialization. Term 4: entirely specialization (2 courses + capstone).
- Student-meaningfulness: high. The compare reveals a clean shared core → diverge structure. Students understand they're choosing a specialization direction, not a different program. The unique courses map clearly onto "pipeline/cloud engineering" vs "machine learning/statistical modeling" careers.
- Validates "shared core + specialization" pattern: confirmed. This pattern is the same across all three MSDA tracks and across MSSWE tracks; the v1 compare contract handles it cleanly.

### 15.15 Advanced compare capabilities (deferred)
- Cross-school compare: deferred.
- Cross-level compare (bachelor's vs master's): deferred.
- Historical roster compare (old edition vs current edition): deferred.
- Discussion-contextualized compare: deferred.
- Auto-generated family detection from overlap data alone: deferred.
- Compare for retired programs: deferred.
- 3-way (n-way) compare UI: deferred.

### 15.16 Phased rollout

#### Phase 1 (Session 1 — 2026-03-15): Canonical helpers and taxonomy foundation — COMPLETE
- [x] Define Degree Compare policy in `docs/DECISIONS.md` (this section).
- [x] Implement `getSchoolSlugByName()` in `src/lib/data.ts`.
- [x] Implement `classifyDegreeLevel()`, `groupProgramsByLevel()`, `compareRosters()` / `CompareResult` in `src/lib/programs.ts`.
- [x] Fix school filter drift in `ProgramExplorer` (Health Professions → Health).
- [x] Replace ad-hoc `schoolNormMap` in school page; replace local `groupProgramsByLevel`.
- [x] Document in `docs/ATLAS_SPEC.md` §12. Update `_internal/WORKQUEUE.md`.

#### Phase 2 (Session 2 — 2026-03-15): Pilot families, compare payload, v1 content contract — COMPLETE
- [x] Run pilot compare reviews: BSSWE vs BSSWE_C and MSDADE vs MSDADS (§15.14).
- [x] Confirm v1 is 2-way only (§15.3).
- [x] Confirm same-school + same-degree-level constraint (§15.3).
- [x] Confirm current ACTIVE programs only (§15.3).
- [x] Confirm compare output display ordering: shared → left-only → right-only (§15.9).
- [x] Decide program first_seen included in v1 (§15.10).
- [x] Decide course added-date deferred from v1 (§15.11).
- [x] Define comparable-family qualification rules (§15.12).
- [x] Define v1 content contract / `ComparePayload` schema (§15.13).
- [x] Create `src/lib/families.ts`: `ProgramFamily`, `PILOT_FAMILIES`, `ComparePayload`, `buildComparePayload()`, `getFamilyByCode()`, `getSiblingCodes()`, `areProgramsComparable()`.
- [x] Document in `docs/ATLAS_SPEC.md` §12. Update `_internal/WORKQUEUE.md` J-01 → complete.

#### Phase 3 (Session 3 — 2026-03-16): Standalone compare page MVP — COMPLETE
- [x] Created `/compare` route (`src/app/compare/page.tsx`) — static export, primary nav entry.
- [x] Created `CompareSelector` client component — school/level filters, 2-step program selection (A then B from family siblings only), reset state.
- [x] Created `CompareView` component — §15.9 display ordering: program headers → overlap bar → shared courses → left-only → right-only.
- [x] Source-separation confirmed: catalog diff only; no official-context blending in v1.
- [x] Pilot comparisons working: BSSWE vs BSSWE_C, MSDADE vs MSDADS, MSDADE vs MSDADPE, MSDADS vs MSDADPE.
- [x] Desktop-first; mobile is functional but not optimized.
- [x] Nav: "Compare" added to primary nav for MVP discoverability (see §15.8 note below).
- Note on §15.8 override: §15.8 deferred top-level nav; this MVP adds it for testability. Revisit in Phase 4 after usage validation.
- Note on §15.8 route: opted for standalone `/compare` over `/programs/[code]` inline because the user flow "sit down and choose two programs" is better served by a dedicated entry point. Phase 4 can add inline affordances on program pages.

#### Phase 4 (Session 4 — 2026-03-16): Two-name model, index plumbing, layout redesign — COMPLETE
- [x] Investigated catalog index/TOC naming: `program_index_2026_03.json` in WGU_catalog outputs distinguishes SWE tracks ("Java Track" / "C# Track") and MSDA tracks ("Data Engineering", "Data Science", "Decision Process Engineering").
- [x] Confirmed body/canonical_name is intentionally identical for both SWE tracks; index is the only catalog location with distinguishing names.
- [x] Defined two-name model: `canonical_name` (unchanged, from programs.json body) + `index_name` (from catalog TOC via curated `track_labels` in families.ts). See §15.17.
- [x] Plumbed index names into compare context: `track_labels` field on `ProgramFamily`, `index_name` field on `CompareProgramMeta`, `getIndexName()` and `extractTrackLabel()` helpers.
- [x] Updated `CompareSelector`: uses index names in program list items and "Comparing with" banner; collapses to compact summary bar when both programs selected.
- [x] Redesigned `CompareView`: term-aware three-lane layout (left-only | shared | right-only per term), replacing stacked set-diff tables. Preserves term sequence and shows where tracks share vs diverge.
- [x] Program header cards: index_name as primary headline, canonical_name as subtitle. "Program A/B" replaced with "Track A/Track B".
- [x] Overlap bar and overlap summary: unchanged.
- [x] Compare now shows distinguishing track labels throughout — no ambiguous identical names.
- Desktop-first; mobile is functional but three-lane layout is not optimized for small screens.

#### Phase 5 (TBD): Advanced capabilities and program-page affordances
- [ ] Add inline compare affordances on `/programs/[code]` for family-member programs.
- [ ] Evaluate cross-school or cross-level expansions.
- [ ] Evaluate historical roster compare.
- [ ] Evaluate official-context enrichment layer in compare views.
- [ ] Evaluate 3-way compare UI for families with >2 members.

### 15.17 Two-name model for program display
Two parallel name concepts are maintained for programs. Neither replaces the other; they serve different contexts.

**Name 1 — canonical_name (body degree name)**
- Source: `ProgramRecord.canonical_name` from `public/data/programs.json`.
- Derivation: extracted from the body heading of the WGU catalog program block.
- Stability: very high — this is the official degree name as WGU titles it.
- Usage: all general display contexts (program browse, program detail pages, lineage artifacts, search index).
- Example: `Bachelor of Science, Software Engineering` (same for both SWE tracks).
- Rule: never modify `canonical_name` to include track qualifiers; the degree name does not change between tracks.

**Name 2 — index_name (catalog TOC / disambiguation name)**
- Source: `ProgramFamily.track_labels` in `src/lib/families.ts`, curated from `program_index_[date].json` in WGU_catalog trusted outputs.
- Derivation: extracted from the catalog index/TOC section which lists programs under schools. This section includes track qualifiers absent from body headings.
- Stability: high — catalog index naming has been stable since 2023-01 for these programs; however, it is curated in families.ts and must be manually updated when catalog index changes.
- Usage: compare selector program lists, compact selection bar, compare program header cards, column headers in three-lane layout.
- Example: `B.S. Software Engineering (Java Track)` (BSSWE) and `B.S. Software Engineering (C# Track)` (BSSWE_C).
- Rule: use index_name only in compare UI context where disambiguation is essential. Do not propagate index_name to general program browse or program detail pages.

**Short track label (derived from index_name)**
- Derived by `extractTrackLabel(indexName)` — extracts the parenthetical qualifier.
- Example: `"B.S. Software Engineering (Java Track)"` → `"Java Track"`.
- Usage: compact column headers and overlap legend chips within compare views.

**When each is used:**
| Context | Name |
|---|---|
| Program browse list | `canonical_name` |
| Program detail page title | `canonical_name` |
| Search index / search results | `canonical_name` |
| Lineage/history context | `canonical_name` |
| Compare selector — program list items | `index_name` (primary), `canonical_name` (subtitle) |
| Compare selector — compact bar | `index_name` |
| Compare program header cards | `index_name` (primary), `canonical_name` (subtitle) |
| Compare column headers / legend | short track label (derived from `index_name`) |

**Known caveats:**
- `index_name` uses abbreviated degree prefix (`B.S.`, `M.S.`) vs the full form in `canonical_name` (`Bachelor of Science,`, `Master of Science,`). These are not interchangeable.
- Index names for MSDA programs contain the same track distinction as `canonical_name` (which already has ` - [Track]` suffix); the index form just abbreviates the degree prefix. The track labels still clarify for consistency.
- `BSSWE_C` has zero outcomes in `program_enriched.json` (outcomes extraction matched the catalog section to BSSWE only, as the outcomes heading does not distinguish tracks). This is a known pipeline gap; the compare view is unaffected since outcomes are not in v1 compare payload.

## 16) Maintenance rules for this file
- Add here when rule is normative and likely to be rediscovered incorrectly.
- Do not add here for pure structure/inventory/workflow mechanics (goes to `ATLAS_SPEC`).
- Keep dense, explicit, and non-narrative.
- Trigger updates when any of these materially change:
  - provenance boundaries
  - Program History curation set
  - official-context ordering/attachment policy
  - video policy
  - outcomes interpretation policy
  - documentation governance
