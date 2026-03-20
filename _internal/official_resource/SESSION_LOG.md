# Official Resource Module — Session Log

Append-only. Most recent entry first.

---

## 2026-03-20 — Placement curation: source review + 3 removals

**Task:** Full source review of all 15 placed regulatory_licensure URLs; remove entries that fail student-value test.

**Files changed:**
- `public/data/official_resource_placements.json` (−3 entries, 131 → 128)

**Source review findings and reason codes:**

| Surface | Resource | Decision | Reason code |
|---------|----------|----------|-------------|
| education (school) | Teaching License/Certification | keep | `high_student_value` |
| education (school) | State Licensure Information (Education) | keep | `compliance_signal` |
| education (school) | Teacher Licensure Programs | keep — pending density review | `overlap_trim_candidate` |
| education (school) | Praxis Exam | keep | `high_student_value` |
| education (school) | Student Teaching | keep | `high_student_value` |
| health (school) | State Licensure Information (Nursing) | keep | `compliance_signal` |
| health (school) | Health and Nursing Clinical Information | keep | `high_student_value` |
| BSNPLTR | Health and Nursing Clinical Information | keep | `high_student_value` |
| BSNU | NCLEX-RN Exam | **removed** | `generic_boilerplate` |
| BSPNTR | State Licensure Information (Nursing) | keep | `compliance_signal` |
| BSPNTR | Health and Nursing Clinical Information | keep | `high_student_value` |
| MSNUFNP | FNP Placement | keep | `high_student_value` |
| MSNUFNP | FNP Preceptor Requirements | **removed** | `wrong_audience` |
| MSNUPMHNP | PMHNP Placement | keep | `high_student_value` |
| MSNUPMHNP | PMHNP Preceptor Requirements | **removed** | `source_content_error` |
| business (school) | Business Licensure Information by State | keep | `compliance_signal` |
| technology (school) | IT Certifications Included in WGU Degrees | keep | `high_student_value` |

**Removal rationale:**
- BSNU / NCLEX-RN — `generic_boilerplate`: page is NCSBN boilerplate framed as RN-to-BSN marketing; no Atlas-grade student context
- MSNUFNP / FNP Preceptor — `wrong_audience`: page targets healthcare professionals being recruited as preceptors, not FNP students; all student-critical content already in FNP Placement
- MSNUPMHNP / PMHNP Preceptor — `source_content_error`: page appears misconfigured — contains FNP content (family medicine preceptors, CNMs, PAs) under a PMHNP heading; contact email is `CLPSFNP@wgu.edu`; unsafe to surface

**Education trim status:** 5 links on education school page — pending visual density review. All 5 kept for now; apply 1–3 density rule after UI review. `Teacher Licensure Programs` is the most likely trim candidate (`overlap_trim_candidate`).

**Net state after removals:**
- 128 total placements
- regulatory_licensure entries: 12 active

**Next step:** Outcomes + accreditation completeness audit (Tier 2).

---

## 2026-03-20 — Regulatory gap verification pass

**Task:** Verify concrete gaps from the regulatory placement pass; make high-confidence corrections only.

**Files changed:**
- `public/data/official_resource_placements.json` (net 0: removed 1, added 1)

**Gap findings:**

| Gap | Finding | Action |
|-----|---------|--------|
| NCLEX for BSNPLTR — correct URL? | Page is explicitly scoped to RN-to-BSN students (BSNU). Prelicensure gets only a tangential redirect. Wrong audience for BSNPLTR. No separate prelicensure NCLEX page exists in phase1 sitemap. | **Removed** NCLEX from BSNPLTR |
| BSPNTR clinicals — applicable? | Page explicitly covers prelicensure program structure including pre-nursing terms. Forward-looking language confirms it is relevant to students before nursing admission. | **Added** clinicals to BSPNTR |
| No BSNPLTR-specific NCLEX page | Confirmed: manifest contains only one NCLEX URL (RN-to-BSN path). No separate prelicensure NCLEX page found. | Noted; no WGU resource currently exists to attach |
| Education Praxis/Student Teaching at degree level | Too many programs (~15+) to enumerate safely without per-program verification. | Deferred cleanly |
| ACEN/CCNE nursing accreditation | Tier 2 accreditation scope — not regulatory. | Deferred to outcomes/accreditation audit |
| Education state-specific degree restrictions | Complex enumeration; out of scope for this pass. | Deferred cleanly |

**Net state after verification:**
- BSNPLTR: 1 placement (clinicals only)
- BSPNTR: 2 placements (nursing state licensure + clinicals)
- BSNU: 1 placement (NCLEX — correct; RN-to-BSN audience match)

**Remaining open item from regulatory pass:**
No BSNPLTR-specific NCLEX page exists on the WGU site (as of phase1 sitemap). If WGU adds one, attach it at BSNPLTR.

**Next step:** Outcomes + accreditation completeness audit (Tier 2).

---

## 2026-03-20 — Regulatory placement pass executed

**Task:** Resolve needs-review items; write approved placements to `official_resource_placements.json`.

**Files changed:**
- `public/data/official_resource_placements.json` (+15 entries, 116 → 131)
- `src/components/resources/RelevantResources.tsx` (added `regulatory_licensure: "Licensure & Exams"` to GROUP_LABELS)

**Needs-review resolutions:**
- #3 Teacher Licensure Programs → **keep** — page is a distinct program catalog with timelines and tuition, ~15% overlap with Teaching License/Certification; both warranted at school level
- #11 FNP Preceptor → **keep** — distinct from FNP Placement; covers supervision progression and PA preceptor state constraints; ~40% overlap but different operational focus
- #12 PMHNP Preceptor → **keep** — same logic as FNP Preceptor; covers two-site minimum and preceptor qualifications distinct from the placement checklist

**Placements added (15 total):**
- School of Education: 3 (state licensure, teaching license overview, teacher licensure programs)
- School of Health: 2 (nursing state licensure, clinical requirements)
- BSNPLTR: 2 (clinicals, NCLEX-RN)
- BSNU: 1 (NCLEX-RN)
- BSPNTR: 1 (nursing state licensure — select-state enrollment signal)
- MSNUFNP: 2 (FNP placement, FNP preceptor)
- MSNUPMHNP: 2 (PMHNP placement, PMHNP preceptor)
- School of Business: 1 (business state licensure)
- School of Technology: 1 (IT certifications overview)

**New resource_group introduced:** `regulatory_licensure` (display priority 12; renders as "Licensure & Exams" in sidebar)

**Gaps flagged for follow-up:**
- NCLEX URL is nested under RN-to-BSN program path; verify if a BSNPLTR-specific NCLEX page exists
- BSPNTR clinical requirements: only state licensure added; clinicals attachment deferred pending confirmation of which clinical pages apply to pre-nursing
- Education degree-level Praxis/Student Teaching attachments: deferred; need to enumerate which program codes have student teaching and Praxis requirements before attaching
- ACEN/CCNE nursing accreditation pages: not found in phase1 sitemap pass; check if they exist

**Next step:** Outcomes + accreditation completeness audit (Tier 2) against `official_context_manifest_phase1.csv`.

---

## 2026-03-20 — Regulatory candidate queue built

**Task:** Build `_internal/official_resource/regulatory_candidate_queue.md`.

**Files created:**
- `_internal/official_resource/regulatory_candidate_queue.md`

**Source reads:**
- `data/enrichment/official_context_manifest_phase1.csv` (605 rows)
- `data/enrichment/README.txt`
- `data/enrichment/official_context_manifest_phase2_test.json` (122 reviewed entries)
- `data/enrichment/outcomes/outcomes_links.json` (cross-reference for already-captured accreditation)
- `_internal/official_resource/next_workstream_memo.md`
- `public/data/programs.json` (program codes and school assignments)

**Candidates identified:** 14 entries reviewed; 11 marked `keep`, 3 marked `needs-review`, 8 skipped

**Key findings:**
- Strong school-level regulatory pairs exist for all four schools (Education: state licensure + teaching license; Health: state licensure + clinicals; Business: state licensure by state; Technology: IT certifications overview)
- Nursing has degree-specific clinical placement pages for FNP and PMHNP — enrollment-critical; select-state programs
- NCLEX-RN page found but is nested under RN-to-BSN program URL; should verify degree-level attachment target (BSNPLTR or BSNU)
- Individual IT vendor cert pages (Cisco, AWS, etc.) deferred to specialization/track pass — not in regulatory queue scope
- 3 needs-review items require reading the page before confirming: Teacher Licensure Programs (#3), FNP Preceptor (#11), PMHNP Preceptor (#12)

**Gaps flagged for follow-up:**
- NCLEX page specifically for BSNPLTR may not exist yet; verify
- Nursing state approval/disclosure page (beyond state licensure overview) — check if required by federal regulation
- ACEN or CCNE nursing accreditation pages — not found in this sitemap pass
- Education state-specific restrictions at degree level may warrant additional annotations

**Next step:** Curation review of `regulatory_candidate_queue.md` — confirm `keep` decisions, resolve 3 `needs-review` items, then update `public/data/official_resource_placements.json` with approved placements.

---

## 2026-03-20 — Module initialization

**Task:** Initialize module workspace and produce planning memo.

**Files created:**
- `_internal/official_resource/README.md`
- `_internal/official_resource/SESSION_LOG.md`
- `_internal/official_resource/ARTIFACTS.md`
- `_internal/official_resource/next_workstream_memo.md`

**Source reads:**
- `_internal/PROJECT_CONTINUITY_ATLAS.md`
- `docs/DECISIONS.md` (§7, §8, §9)
- `data/enrichment/README.txt`

**Major conclusions:**
- Program guides are live and not in the active queue.
- Outcomes/accreditation are high-value and sparse; completeness audit remains but is probably cheap.
- Regulatory/licensure/disclosure pages are the highest-value unfinished sitemap class — enrollment-critical, narrowly scoped, no code dependencies.
- Specialization/track/variant pages are the most scalable next degree-enrichment class after regulatory.
- YouTube stays explicitly downstream of sitemap/page-class work; attachment model not yet clear.
- Career Services YouTube is deferred.
- Density rule locked: 1–3 strong links per surface.
- Outcomes/accreditation completeness audit should stay adjacent (Tier 1/2 boundary) — high value, likely cheap to close.

**Priority order confirmed:**
1. Regulatory / licensure / disclosure pass
2. Outcomes + accreditation completeness audit
3. Specialization / track / variant pass
4. School governance / context pages
5. Official WGU YouTube classification
6. Career Services YouTube
7. Selective mining of program landing pages

**Next step:** Build regulatory/licensure/disclosure candidate queue as a curation-ready artifact (title, URL, source class, target surface, student value rationale, recommendation).
