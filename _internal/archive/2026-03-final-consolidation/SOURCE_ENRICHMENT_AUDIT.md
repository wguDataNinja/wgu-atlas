# Atlas Source Enrichment — Operating Model and Audit

**Last updated:** 2026-03-18

---

## 1. Purpose and operating model

The goal of source enrichment is narrow: decide which external sources should appear in the **Relevant Resources sidebar**, and on which Atlas pages they should appear.

### The canonical workflow

For every enrichment source, Atlas runs the same pipeline:

1. **Ingest** raw source inventory → raw universe artifact
2. **Normalize** to candidate manifest rows in `data/source_enrichment_manifest.json`
3. **Classify** candidate type (program_guide, outcomes, accreditation, specialization, youtube_video, etc.)
4. **Review** for student usefulness → set `review_status` + `decision_reason`
5. **Assign page targets** for worthwhile items → populate `program_targets`, `school_targets`, `course_targets`
6. **Regenerate** `public/data/official_resource_placements.json` from kept + targeted rows
7. **Log** the pass in the Pass Log below
8. **Monthly maintenance**: compare newest source snapshot to manifest → identify new/changed/disappeared rows → review only those

### Backfill vs maintenance

The workflow is identical. Only the review queue differs:

- **Backfill mode:** review all `unreviewed` items in the manifest
- **Maintenance mode:** review only rows where `last_seen_at` < current snapshot date, plus any rows marked `is_currently_present: false` that need retirement or re-check

---

## 2. Canonical manifest schema

The durable manifest lives at `data/source_enrichment_manifest.json`.

Every candidate row — across all source families — follows this schema:

```json
{
  "source_key": "https://www.wgu.edu/online-it-degrees/computer-science/program-guide.html",
  "source_family": "sitemap",
  "source_subtype": "program_guide_page",
  "url": "https://www.wgu.edu/online-it-degrees/computer-science/program-guide.html",
  "title": "B.S. Computer Science Program Guide",
  "candidate_type": "program_guide",
  "target_scope": "program",

  "review_status": "keep",
  "decision_reason": "core_program_context",
  "notes": "",

  "program_candidates": ["BSCS"],
  "school_candidates": ["technology"],
  "course_candidates": [],

  "program_targets": ["BSCS"],
  "school_targets": [],
  "course_targets": [],

  "is_currently_present": true,
  "first_seen_at": "2026-03-14",
  "last_seen_at": "2026-03-14",
  "last_reviewed_at": "2026-03-15"
}
```

### Field reference

**Identity / source:**
- `source_key` — stable row identifier; for sitemap rows equals `url`; for YouTube rows equals video ID
- `source_family` — `sitemap | youtube_official | youtube_cs | reddit`
- `source_subtype` — more specific type within the family (e.g. `program_guide_page`, `outcomes_page`, `youtube_video`)
- `url` — canonical URL or YouTube watch URL
- `title` — human-readable title

**Classification:**
- `candidate_type` — `program_guide | program_landing | specialization | accreditation | outcomes | school_context | youtube_video | other`
- `target_scope` — `program | school | course` (primary scope; not exclusive)

**Review decision:**
- `review_status` — `unreviewed | keep | skip | defer`
- `decision_reason` — compact reason code (see §3)
- `notes` — free-text for edge cases or useful context

**Candidate hints** (who this might be relevant to — informed by discovery, not binding):
- `program_candidates` — array of program codes (or name strings before code is known)
- `school_candidates` — array of school slugs (`technology`, `business`, `health`, `education`)
- `course_candidates` — array of course codes

**Placement targets** (where this actually appears — set at review time):
- `program_targets` — array of program codes that show this in their sidebar
- `school_targets` — array of school slugs that show this in their sidebar
- `course_targets` — array of course codes that show this in their sidebar

**Lifecycle:**
- `is_currently_present` — boolean; set to `false` if source disappeared from its inventory
- `first_seen_at` — ISO date string when first observed
- `last_seen_at` — ISO date string when last confirmed present
- `last_reviewed_at` — ISO date string of the last human review

Note: bootstrap rows have inferred/approximate dates based on session history (not precise scrape timestamps).

---

## 3. Review vocabulary

### Keep reasons
| Code | When to use |
|---|---|
| `core_program_context` | Official program guide or primary degree resource |
| `variant_explainer` | Specialization or track page that explains a program variant meaningfully |
| `official_outcomes_context` | Outcomes/assessment data page with structured competency information |
| `school_context` | School-level accreditation, learning results, or institutional context |
| `accreditation_context` | Specific accreditation or designation page (program-level or school-level) |

### Skip reasons
| Code | When to use |
|---|---|
| `marketing_only` | Primarily promotional; no substantive student-useful content |
| `duplicate_of_existing` | Redundant with another already-placed resource |
| `too_generic` | Not specific enough to any Atlas entity to be useful |
| `weak_student_value` | Exists but offers little to a student exploring a program |
| `not_surface_relevant` | Institutional/operational page not relevant to any Atlas surface |

---

## 4. Work surfaces by source family

| Source type | Raw universe | Active candidate manifest | Notes/log | Live placements |
|---|---|---|---|---|
| **WGU sitemap** | `data/official_context_manifest_phase1.csv|json` | `data/source_enrichment_manifest.json` | This doc (§5) | `public/data/official_resource_placements.json` |
| **Official WGU YouTube** | `_internal/youtube/raw/wgu_official_titles_raw.txt` | `data/source_enrichment_manifest.json` (future rows) | `_internal/youtube/YOUTUBE_WORKLOG.md` | — (not yet placed) |
| **WGU Career Services YouTube** | `_internal/youtube/raw/wgu_career_services_titles_raw.txt` | `data/source_enrichment_manifest.json` (future rows) | `_internal/youtube/YOUTUBE_WORKLOG.md` | — (not yet placed) |
| **Reddit/community** | — (external project) | `data/source_enrichment_manifest.json` (future rows) | §8 below | — (future) |

### Historical transitional artifacts (no longer active)
- `data/official_context_manifest_phase2_test.json` — 122 reviewed rows from the original enrichment pass. Data migrated into `source_enrichment_manifest.json`. Retained as a historical reference.
- `_internal/workqueue_inputs/official_context_phase2_remaining_batch.json` — original input queue (262 entries). Migrated into `source_enrichment_manifest.json` as unreviewed rows. Retained for reference.

---

## 5. Sitemap source — current state

### What is done
- **Phase 1:** 604 entries extracted from WGU sitemap (2026-03-14). Raw URLs and titles.
- **Phase 2 (partial):** 122 entries enriched, all `review_status: keep`. Live as 116 placements.
  - 115 program guide pages → 109 programs have live placements
  - 3 accreditation pages (ACBSP/Business, CAEP/Education, CAHIIM/Health Info Mgmt)
  - 2 outcomes pages (B.S. CS, B.S. CSIA)
  - 2 specialization subpages (M.S. Data Analytics, M.S. SE)

### Program guides: solved
109 of 114 active programs have a live program guide placement. Do not re-include program guide pages in new review queues.

Six programs missing placements (worth a targeted check):
`BSNPLTR`, `BSPNTR`, `MASEMG`, `MEDETID`, `MEDETIDA`, `MEDETIDK12`

### Active unreviewed queue (262 rows in manifest)
| Category | Count | What they are |
|---|---|---|
| `school_page` | 138 | Individual degree program landing pages on wgu.edu (not Atlas school pages) |
| `specialization` | 123 | Stackable cert pages (~20) + track/variant/endorsement subpages (~103) |
| `accreditation` | 1 | CAE-CDE Program Designation (B.S. Cybersecurity) — quick win |

### Permanent exclusions from sitemap
- Financial aid / scholarship pages (~145 in Phase 1)
- Admissions utility pages
- Generic about/legal/contact pages
- Program guide pages — already done

### Next sitemap passes (priority order)
1. The 1 remaining accreditation entry (CAE-CDE, 5 min)
2. Outcomes pages — filter Phase 1 for `outcomes.html` URLs; high-value content
3. Specialization subpages — 123 entries; do in sub-batches of 20–30
4. Program landing pages — 138 entries; lowest urgency

---

## 6. YouTube source — current state

Both inventories imported 2026-03-18. First-pass filters applied. See `_internal/youtube/YOUTUBE_WORKLOG.md` for full detail.

| Channel | Raw | After first-pass filter | Excluded |
|---|---|---|---|
| Official WGU | 1,535 | 818 | 717 (commencement/graduation) |
| Career Services | 441 | 267 | 174 (employer sessions, job-hunting how-tos) |

### Next YouTube passes
- **YT-1:** Official WGU school-level candidates (roadshows, fireside chats, field panels) → target 5–15 per school
- **YT-2:** Official WGU degree-level candidates (field explainers, program journey videos)
- **YT-3:** Career Services selective pass (after YT-1 done) → target 10–20 total

YouTube rows will be added to `data/source_enrichment_manifest.json` as candidates are reviewed.

---

## 7. Active review queues

| Queue | Source | Count | Status |
|---|---|---|---|
| Unreviewed sitemap rows | `data/source_enrichment_manifest.json` | 262 | Ready to review |
| YouTube filtered working copies | `_internal/youtube/working/` | 818 + 267 | Needs candidate review pass |

---

## 8. Reddit / community — future placeholder

A separate project maintains a large database of WGU-related Reddit posts with course-code filtering. When Atlas course pages are richer and the external project provides an integration path, Reddit posts will be added to `data/source_enrichment_manifest.json` as `source_family: "reddit"` rows targeting `course_targets`.

Dependencies: richer course pages (WORKQUEUE C-01/C-02), Reddit project API/export, UI pattern decision for community content.

---

## 9. Pass log

| Pass | Date | Source | Output | Placements added | Notes |
|---|---|---|---|---|---|
| sitemap-p1 | 2026-03-14 | WGU sitemap | `official_context_manifest_phase1.json` (604 entries) | 0 | Raw extraction |
| sitemap-p2-test | 2026-03-14 | Phase 1 manifest | `official_context_manifest_phase2_test.json` (15 fetched) | 0 | Workflow validation |
| sitemap-p2-guides | 2026-03-15 | Phase 1 manifest | phase2_test.json (122 total) | 116 live placements | Session cut short at quota |
| yt-import-01 | 2026-03-18 | External yt-video-analysis repo | `_internal/youtube/raw/*.txt` + `working/*.txt` | 0 | Import + first-pass filter |
| manifest-bootstrap | 2026-03-18 | phase2_test.json + remaining_batch.json | `data/source_enrichment_manifest.json` | 0 | Migration to durable manifest |



Outcomes pages — what they contain

The discovered outcomes.html pages are high-value because they include two substantive data sections:
	•	Program Results: enrollment, retention, on-time progress, graduation, satisfaction
	•	Program Assessment Results: course pass rates over time

These pages support a stronger official_outcomes_context classification than ordinary program pages because they provide structured program-level outcomes and assessment data, not just descriptive copy.

What we learned from them

So far, the outcomes pages suggest:
	•	these programs are tracked on a multi-year timeline
	•	the normal student picture looks more like years than months
	•	they do not tell us exact fast-acceleration prevalence
	•	course pass-rate tables are useful but methodologically ambiguous


  we 