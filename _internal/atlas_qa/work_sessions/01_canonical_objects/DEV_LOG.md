# DEV_LOG — Session 01: Canonical Object Generation

Append-only. Each entry records what was actually done, not what was planned.

---

## 2026-03-23 — Claude (docs/setup pass)

**Scope:** Workspace scaffold — docs only, no runtime implementation
**Files touched:**
- `_internal/atlas_qa/WORK_SESSION_RULES.md` — created
- `_internal/atlas_qa/work_sessions/01_canonical_objects/SESSION_SPEC.md` — created (full execution spec)
- `_internal/atlas_qa/work_sessions/01_canonical_objects/DEV_LOG.md` — created (this file)
- `_internal/atlas_qa/work_sessions/02_exact_lookup_path/SESSION_SPEC.md` — created
- `_internal/atlas_qa/work_sessions/02_exact_lookup_path/DEV_LOG.md` — created

**Checks run:** none
**Results:** n/a
**Blockers/deviations:** No runtime implementation performed in this pass. Session spec written from locked design docs (`LOCAL_8B_RAG_SYSTEM_DESIGN.md` v1.4, `PM_CONTEXT_PACKET.md`). No design decisions made or reopened.

---

## 2026-03-23 — Claude (implementation pass)

**Scope:** Preflight → implementation plan → full Session 01 implementation

### Preflight results (Appendix A)

All required inputs present and readable:

| Input | Status | Notes |
|---|---|---|
| `data/catalog/trusted/2026_03/` | ✅ Present | 8 files |
| `data/catalog/change_tracking/` | ✅ Present | 5 files |
| `data/catalog/edition_diffs/` | ✅ Present | 4 files |
| `data/program_guides/parsed/` | ✅ Present | 115 files (matches expected corpus) |
| `data/program_guides/guide_manifest.json` | ✅ Present | 115 entries |
| `data/program_guides/guide_anomaly_registry.json` | ✅ Present | 9 anomalies |
| `data/canonical_courses.csv` | ✅ Present | |
| `data/canonical_courses.json` | ✅ Present | 1594 codes (matches expected) |
| `data/catalog/helpers/course_index_v10.json` | ✅ Present | 58MB (gitignored) |
| `data/catalog/helpers/degree_snapshots_v10_seed.json` | ✅ Present | 524KB (gitignored) |
| `data/catalog/helpers/sections_index_v10.json` | ✅ Present | 824KB (gitignored) |

Additional inputs discovered and used:
- `public/data/course_descriptions.json` — 838 catalog text descriptions (CAT-TEXT source)
- `data/program_guides/enrichment/course_enrichment_candidates.json` — 751 guide-enriched courses
- `data/program_guides/cert_course_mapping.json` — cert prep signal source
- `data/program_guides/prereq_relationships.json` — guide prereq mentions (unstructured; not used for `prerequisite_course_codes`)

**Preflight verdict: Session 01 can proceed. All required inputs present.**

### Implementation plan

1. `src/atlas_qa/qa/types.py` — Pydantic v2 models for all 4 object families (CourseCard, ProgramVersionCard, GuideSectionCard, VersionDiffCard) plus all sub-types
2. `src/atlas_qa/qa/source_authority.py` — anomaly registry (C179, D554), version conflict program registry (MACCA/MACCF/MACCM/MACCT/MSHRM), authority lookup helpers
3. `src/atlas_qa/qa/builders/course_card.py` — course_card builder; primary sources: canonical_courses.json, course_descriptions.json, enrichment_candidates.json, cert_course_mapping.json; outputs one card per course_code
4. `src/atlas_qa/qa/builders/program_version_card.py` — program_version_card builder; primary source: program_blocks_2026_03.json + parsed guides
5. `src/atlas_qa/qa/builders/guide_section_card.py` — guide_section_card builder; one card per program × section type
6. `src/atlas_qa/qa/builders/version_diff_card.py` — version_diff_card builder; source: edition_diffs_full.json
7. Build scripts in `scripts/` for each object family
8. `scripts/validate_canonical_objects.py` — schema, uniqueness, anomaly, and artifact checks
9. Golden fixtures for C715 (normal), C179 (short catalog text), D554 (misrouted guide), AIT2 (multi-variant competency), D550 (version-conflicted programs)
10. Validation target: 14/14 checks pass

**Blockers discovered during planning:**
- `prerequisite_course_codes` from CANON: no structured per-course prereq data exists in the Atlas-local catalog artifacts. `prereq_relationships.json` captures guide text mentions but not which course is the *subject* (the course requiring the prereq). Set to `[]` pending future structured source. Logged here; not a blocker for Session 02 (exact lookup path does not depend on prereq lookup in current spec).

### Implementation

**Files created:**
- `src/atlas_qa/qa/__init__.py`
- `src/atlas_qa/qa/types.py`
- `src/atlas_qa/qa/source_authority.py`
- `src/atlas_qa/qa/builders/__init__.py`
- `src/atlas_qa/qa/builders/course_card.py`
- `src/atlas_qa/qa/builders/program_version_card.py`
- `src/atlas_qa/qa/builders/guide_section_card.py`
- `src/atlas_qa/qa/builders/version_diff_card.py`
- `src/atlas_qa/qa/tests/__init__.py`
- `src/atlas_qa/qa/tests/fixtures/fixture_c715.json`
- `src/atlas_qa/qa/tests/fixtures/fixture_c179.json`
- `src/atlas_qa/qa/tests/fixtures/fixture_d554.json`
- `src/atlas_qa/qa/tests/fixtures/fixture_multi_variant.json`
- `src/atlas_qa/qa/tests/fixtures/fixture_version_conflict.json`
- `scripts/build_course_cards.py`
- `scripts/build_program_version_cards.py`
- `scripts/build_guide_section_cards.py`
- `scripts/build_version_diff_cards.py`
- `scripts/validate_canonical_objects.py`

**Files generated (data/atlas_qa/):**
- `course_cards.json` — 1641 cards (1594 canonical codes + inactive courses present in canonical_courses.json)
- `program_version_cards.json` — 114 cards
- `guide_section_cards.json` — 245 cards
- `version_diff_cards.json` — 2214 cards

### Checks run

- `python scripts/validate_canonical_objects.py` — **14/14 passed**
  - File existence: ✅ all 4 output files present
  - Schema: ✅ all 1641 course_cards, 114 program_version_cards, 245 guide_section_cards, 2214 version_diff_cards parse cleanly
  - Uniqueness: ✅ no duplicate course_codes
  - C179 anomaly: ✅ `cat_short_text_flag=True`, description=293 chars
  - D554 anomaly: ✅ `guide_misrouted_text_flag=True`, `guide_description_alternates=[]`

### Fixture spot-checks

| Fixture | course_code | cat_short_text_flag | guide_misrouted_text_flag | competency_variant_count | version_conflict_programs |
|---|---|---|---|---|---|
| fixture_c715 | C715 | True (272 chars) | False | 2 | 0 |
| fixture_c179 | C179 | True (293 chars) | False | 2 | 0 |
| fixture_d554 | D554 | False | True | 1 | 2 (MACCF, MACCT) |
| fixture_multi_variant | AIT2 | True | False | 2 | 0 |
| fixture_version_conflict | D550 | False | False | 1 | 4 (MACCA, MACCF, MACCM, MACCT) |

### Deviations and open items

1. **`prerequisite_course_codes` is `[]` for all courses.** No structured per-course prereq source exists in Atlas-local catalog artifacts. The `prereq_relationships.json` file captures guide text mentions but its structure tracks the mention, not the subject course. This field requires a dedicated structured extraction step. Not blocking Session 02 (which does not require prereq lookup per its spec).

2. **`is_prereq_for` is `[]` for all courses.** Same root cause. Spec notes "do not assert absence without completeness confirmation" — leaving empty is the conservative/correct choice here.

3. **`canonical_courses.json` has 1641 codes including inactive entries** (1594 is the "current canonical" count from the manifest; some inactive codes are also present). All 1641 are included in course_cards.json. The active/inactive distinction is captured via `active_current` in the source data.

**Session 01 status: COMPLETE**
