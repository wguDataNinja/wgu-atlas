# Atlas Decisions

## 1. Contract
- `ATLAS_SPEC.md` = structure, artifacts, scripts, runtime.
- `DECISIONS.md` = policy, curation, product rules.
- Prefer one concept, one home. Merge duplicates into canon.

## 2. Provenance / trust
- Keep these separate:
  - official catalog facts
  - official WGU resources
  - student/community discussion
  - Atlas interpretation
- Do not present Atlas summaries as source-authored text.
- Preserve observed vs interpreted distinction in timeline/history views.
- Keep frozen trusted outputs distinguishable from regenerated working outputs.

## 3. Data / parser guardrails
- Debug parser issues from raw text context, not counts alone.
- Program identity is code/body anchored; TOC naming drift is secondary.
- AP and certificate scope stay separate unless intentionally combined.
- Downstream reconstruction uses extracted catalog text, not reparsed PDFs.
- Active parser canon: `parse_catalog_v11.py`.
- Base course identity is exact course code; fuzzy linkage is optional, never default.

## 4. Product posture
- Atlas is reference/explainer infrastructure, not a general discussion site.
- Lead with current student navigation across schools, programs, and courses.
- History is supporting context, not homepage identity.
- Timeline is a specialist surface, not the main product voice.
- Prefer restrained, provenance-legible enrichment over maximal density.

## 5. Program History policy
- Program History is page-level enrichment on program pages, not a separate product.
- Display policy is binary per event: include or exclude.
- `named_events` is not lineage recall base; lineage comes from transition/candidate artifacts.
- Stage split:
  - Stage 1 = semantic judgment (LLM/HITL)
  - later stages = deterministic overlap/diff/transform
- Artifacts:
  - `data/program_history_enrichment.json` = computed lineage events + metrics; `site_worthy` is triage only
  - `data/lineage/lineage_decisions.json` = human curation overlay; display authority
  - `public/data/program_lineage.json` (pending) = page-facing export
- Low overlap does not invalidate lineage if semantic continuity is strong.
- Page-facing lineage should stay compact: relation, dates, overlap/add-remove summary; no shared-code dumps.
- Human curation overrides heuristic `importance` / `site_worthy`.
- If `from.last_seen` to `to.first_seen` spans > 6 editions, treat as a gap; do not auto-link across it.
- If a proposed predecessor is still active, reject lineage and classify the new program as `pathway_variant`.

## 6. Program History curation
### 6.1 Include
`PLE-001`, `PLE-002`, `PLE-005`, `PLE-008`, `PLE-009`, `PLE-010`, `PLE-011`, `PLE-013`, `PLE-014`, `PLE-015`, `PLE-016`, `PLE-017`, `PLE-019`, `PLE-021`, `PLE-022`, `PLE-024`, `PLE-026`

### 6.2 Exclude
`PLE-003`, `PLE-006`, `PLE-007`, `PLE-018`, `PLE-020`, `PLE-025`, `PLE-027`

- `PLE-027` is suppressed as an intermediate namespace step inside the BSCC cloud-track restructure; `PLE-010` is the canonical event.

### 6.3 Unclassified
- Any `PLE-*` not in include/exclude is pending manual curation and must not be auto-displayed.

### 6.4 Interpretation scope
- Include/exclude governs page display only; excluded events still exist historically.

### 6.5 Wording guard
- Required when:
  - any individual pair `jaccard < 0.15`, or
  - approved event overlap is unconfirmed
- Allowed wording: `replaced`, `rebuilt`, `restructured`, `retitled`, `carried forward`, `redesigned`
- Avoid: `evolved from`, `descended from`, `builds on`, `updated version of`, `continuation of`, `expanded`, unqualified `successor to`
- Current wording-guard events: `PLE-010`, `PLE-011`, `PLE-013`, `PLE-014`, `PLE-015`, `PLE-022`, `PLE-026`

### 6.6 Zero-overlap export rule
- If any approved event has any pair with `jaccard_overlap == 0.0`, require `zero_overlap_rationale` in `lineage_decisions.json` before export.
- This rationale is internal only, not student-facing.
- Current in-scope case: `PLE-022`.

### 6.7 Curation overlay artifact
- `data/lineage/lineage_decisions.json` stores per-event and per-program curation decisions.
- Its `display_state` overrides heuristic `site_worthy` at export time.
- It must survive pipeline reruns and must not be regenerated.
- Events absent from this file are suppressed by default.
- Validate before export.

## 7. Official-context policy
- Official context is a first-class supporting layer.
- Intended order:
  1. catalog facts
  2. official WGU resources
  3. later, student/community discussion
- Atlas must not lead as a Reddit/discussion aggregator.
- Curated surfacing only; no sitemap dumps.
- Preferred density: 1–3 strong links per surface.
- Program guides, outcomes pages, specialization pages, and accreditation pages are valid enrichment.
- URL path alone is never enough for classification.

## 8. Official video policy
- Keep official WGU YouTube separate from Career Services YouTube.
- Do not broadly surface videos until import/classification/placement is stable.
- Videos are curated supporting resources, not feeds.
- Career Services content is only included when it helps explain domain/field/role context; generic job-search advice is excluded.

## 9. Outcomes / assessment policy
- Outcomes / pass-rate assets are official-context enrichment, not catalog fact layer.
- Keep source page URL, asset URL, and extraction status for every metric.
- Do not overstate program/time-window metrics as global pass rates.
- Lower pass rate is descriptive, not causal proof.

## 10. Timeline policy
- Timeline events and program-lineage events are separate systems.
- Timeline threshold logic is not lineage recall logic.
- Observed vs interpreted separation applies strongly here.

## 11. Student-facing positioning
- Homepage and core browse surfaces should prioritize current student navigation.
- Historical content appears when it explains the current entity.
- Official resources, videos, and future discussion links must be entity-scoped.
- Homepage should avoid archive-first framing and generic link dumps.

## 12. Provenance display
- Fact sections should carry compact source labels.
- Edition-bound facts may use compact `as-of` / edition labels.
- Interpretation must be clearly attributable to Atlas.

## 13. Compare feature
- Compare is student decision support, not a standalone analytics product.
- Show compare only for curated related-program families.
- Preserve source separation inside compare views.
- V1 constraints:
  - 2-way only
  - same school
  - same degree level
  - active programs only
  - curated families only
- Core compare object is exact course roster from `program_enriched.json`.
- Primary output is shared vs unique curriculum and overlap metrics.
- History on compare pages is supporting context only.
- V1 includes `first_seen` for programs; per-course added dates are deferred.

### 13.1 Comparable-family rules
A family must satisfy all:
1. same school
2. same degree level
3. pairwise Jaccard ≥ 0.25
4. each side contributes ≥ 2 unique courses
5. all active
6. human-curated as a real student choice

### 13.2 Compare display order
1. program headers
2. overlap summary
3. shared courses
4. left-only courses
5. right-only courses

### 13.3 Deferred compare work
- cross-school
- cross-level
- historical compare
- discussion/context compare
- auto family detection
- retired-program compare
- 3-way compare

### 13.4 Two-name model
- `canonical_name` = official body degree name; use everywhere by default
- `index_name` = TOC/disambiguation name; use only in compare UI where needed
- Never replace `canonical_name` globally with track labels

## 14. Maintenance
- Add to this file only when a rule is normative and likely to be rediscovered incorrectly.
- Do not put implementation inventories here.
- Update when provenance boundaries, curation sets, official-context policy, video policy, outcomes policy, or documentation governance materially change.