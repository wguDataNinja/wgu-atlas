# Program Guide Extraction — Phase D Readiness Gap Analysis

**Date:** 2026-03-21
**Session:** 20 (orientation and gap analysis — no parsing or rollout)
**Governing posture:** Descriptive before prescriptive. No Phase D artifact building. No broad parser changes.

---

## 1. What is validated as of Session 19

### Validated families (12 complete + 1 partial)

| Family | Guides | HIGH | MEDIUM | LOW | Notes |
|--------|--------|------|--------|-----|-------|
| standard_bs | 19 | 18 | 0 | 1 | BSITM SP: source-artifact extraction failure |
| cs_ug | 8 | 4 | 4 | 0 | High cert-prep density |
| education_ba | 11 | 5 | 6 | 0 | 4 Sped guides: 1 missing AoS course (PDF reordering) |
| graduate_standard | 9 | 8 | 1 | 0 | MSITM capstone description polluted |
| mba | 3 | 3 | 0 | 0 | — |
| healthcare_grad | 2 | 2 | 0 | 0 | — |
| education_bs | 4 | 4 | 0 | 0 | — |
| teaching_mat | 9 | 8 | 0 | 1 | MATSPED SP: source-artifact failure |
| cs_grad | 5 | 4 | 0 | 1 | MSCSUG SP: source-artifact failure |
| swe_grad | 4 | 3 | 1 | 0 | MSSWEUG: title hyphen in bridge guide |
| data_analytics_grad | 3 | 3 | 0 | 0 | Cleanest graduate family |
| education_ma | 9 | 9 | 0 | 0 | Cleanest family overall |
| **accounting_ma** | **5 (partial)** | **1** | **1** | **3** | MACCA, MACCF, MACCT deferred — looks_like_prose |
| **TOTAL validated** | **91 artifacts** | **71** | **13** | **7** | 87 family-validated; 3 deferred accounting_ma included in artifacts |

**Downstream-usable summary (from Session 19 counting model):**
- Full SP+AoS clean: ~84 guides (HIGH/MEDIUM, no SP failure)
- AoS-only usable: 3 (BSITM, MATSPED, MSCSUG — SP column extraction failure)
- Not usable: 3 (MACCA, MACCF, MACCT — AoS broken)

---

## 2. What remains — the 24 unvalidated guides

### 2.1 Summary table

| Family | Guides | Count | Assessment |
|--------|--------|-------|------------|
| endorsement | ENDECE, ENDELL, ENDMEMG, ENDSEMG, ENDSESB, ENDSESC, ENDSESE, ENDSESP | 8 | **CLEAN** — all HIGH in diagnostic parse |
| nursing_msn | MSNUED, MSNUFNP, MSNULM, MSNUNI, MSNUPMHNP | 5 | **CLEAN** — all HIGH in diagnostic parse |
| education_grad/MSEDL | MSEDL | 1 | **CLEAN** — HIGH in diagnostic parse |
| nursing_pmc | PMCNUED, PMCNUFNP, PMCNULM, PMCNUPMHNP | 4 | **ANOMALOUS** — SP=0 rows (layout defect), AoS intact |
| education_grad/MEDETID | MEDETID | 1 | **ANOMALOUS** — multi-path SP (3 sub-tables, 32 overcounted rows), AoS=9 intact |
| nursing_ug/BSNU | BSNU | 1 | **COMPLEX** — 4-column SP (Option A/B), SP=0 rows, AoS=22 intact |
| nursing_ug/BSPRN | BSPRN | 1 | **COMPLEX** — dual-track guide (1783 lines), MEDIUM, embedded catalog version refs |
| nursing_rn_msn | MSRNNUED, MSRNNULM, MSRNNUNI | 3 | **LOW** — running page headers interfere, non-course SP rows, 3+ missing bullets |
| accounting_ma (deferred) | MACCA, MACCF, MACCT | 3 | **LOW** — known looks_like_prose limitation (already documented) |

---

### 2.2 CLEAN families — diagnostic parse results (session 20)

These were parsed during gap analysis. All artifacts deleted post-diagnosis (no gate/rollout review completed). Results are diagnostic only.

**endorsement (8 guides) — all HIGH, 0 anomalies, 0 warnings**

| Code | SP Rows | AoS Groups | AoS Courses | SP format | Notes |
|------|---------|------------|-------------|-----------|-------|
| ENDECE | 6 | 3 | 6 | 2-column (no Term) | Clinical Experiences group handled as regular AoS group |
| ENDELL | 8 | 1 | 8 | 3-column | Field Experience for ELL is a regular AoS course |
| ENDMEMG | 2 | 1 | 2 | 2-column | Smallest guide in corpus (295 lines) |
| ENDSEMG | 2 | 1 | 2 | 2-column | — |
| ENDSESB | 9 | 2 | 9 | 2-column | — |
| ENDSESC | 7 | 3 | 7 | 2-column | — |
| ENDSESE | 9 | 4 | 9 | 2-column | — |
| ENDSESP | 7 | 3 | 7 | 2-column | — |

The Phase A manifest classified all endorsement guides as MEDIUM and noted "high uncertainty" about structure. The diagnostic parse shows the parser handles them correctly without any changes. Clinical Experiences and Field Experience sections are ordinary AoS groups, not structural anomalies.

**nursing_msn (5 guides) — all HIGH, 0 anomalies, 0 warnings**

| Code | SP Rows | AoS Groups | AoS Courses | Notes |
|------|---------|------------|-------------|-------|
| MSNUED | 15 | 2 | 15 | — |
| MSNUFNP | 16 | 3 | 16 | — |
| MSNULM | 15 | 2 | 15 | — |
| MSNUNI | 14 | 2 | 14 | — |
| MSNUPMHNP | 17 | 3 | 17 | — |

Nursing MSN guides are structurally standard. The "Field Experience" and "Capstone" entries in the SP are regular courses that appear in AoS without issue. The clinical/preceptor concern from Phase A was unfounded at the structural level — these sections are treated as ordinary AoS courses.

**education_grad/MSEDL — HIGH, 0 anomalies, 0 warnings**
- SP: 13 rows, AoS: 3 groups, 13 courses. Clean. No Practicum section anomaly.

---

### 2.3 ANOMALOUS families — AoS intact, specific parser gaps

**nursing_pmc (4 guides) — MEDIUM, SP=0 rows, AoS intact**

Root cause (consistent across all 4): Page layout puts "Changes to Curriculum" boilerplate between the "Standard Path" intro header (line ~223) and the actual "Standard Path for Post-Master's Certificate..." table (line ~242). The sequence is:
```
Standard Path [header]
  ... boilerplate text ...
[page footer: PMCNUED 202110 / © 2019 / page 5]
Changes to Curriculum [boilerplate block — normally after SP, here before the table]
Standard Path for Post-Master's Certificate... [actual table header]
  [3-column multiline SP data]
```
The parser detects "Standard Path" as the section start but the AoS section start is also detected, creating a range that includes the embedded "Changes to Curriculum" block. The SP parser fails to find the 3-column table within this range (the "Changes to Curriculum" boilerplate likely acts as a false terminator or the section start/end window excludes the actual table).

Secondary issue: degree_title extracted as "Certificate Guidebook" because the PMC guides start with "Certificate Guidebook" on line 1 (equivalent to "Program Guidebook" in regular guides), but the title extractor returns line 0 rather than line 1.

AoS: 8–11 courses, 0 anomalies across all 4. Full course descriptions and competency bullets intact.

**SP fix complexity:** Targeted. Likely requires either (a) detecting "Standard Path for..." as the true SP table start even when it follows "Changes to Curriculum", or (b) using the second occurrence of any "Standard Path..." heading as the table header in these guides. Low regression risk. Not attempted this session.

**degree_title fix complexity:** Trivial. Change title extraction to handle "Certificate Guidebook" as a document-type header and take line 2 as the title.

**education_grad/MEDETID — MEDIUM, multi-path SP**

Root cause: MEDETID has two degree specializations (K-12 and Adult Learner), each with its own full SP sub-table, plus a shared "combined" SP sub-table. The guide contains 3 embedded Standard Path tables:
1. `Standard Path for ...: K-12 and Adult Learner Specializations` (shared courses)
2. `Standard Path for ...: Adult Learner Specializations` (specialization-only)
3. `Standard Path for ...: K-12 Learner Specialization` (specialization-only)

The parser parses all 3 tables end-to-end, producing 32 rows containing duplicate course titles (shared courses appear multiple times) and the sub-table header lines themselves parsed as course rows. AoS has 9 unique courses in 4 groups (the core non-redundant content). The SP is overcounted.

AoS: clean. 4 groups, 9 courses, 0 anomalies.

**SP fix complexity:** Moderate. Would need to detect that MEDETID has multiple SP sub-tables and either (a) pick one canonical path (e.g., the "combined" or first sub-table), (b) deduplicate course titles, or (c) build a specialization-aware SP structure. Not trivial but contained to this one guide. Not attempted.

---

### 2.4 COMPLEX guides — non-standard structure, significant work required

**nursing_ug/BSNU — MEDIUM, 4-column SP format**

SP format: 4-column (Course + CUs + Option A Term + Option B Term). The parser only supports 2-column (no Term) and 3-column (with Term). Since BSNU has two Term columns, the column detection fails and SP=0 rows are extracted.

AoS: 2 groups, 22 courses, 0 anomalies. Full content intact.

Would require adding a 4-column SP format parser variant. Not high value for Phase D — the AoS is available without SP data. SP fix complexity is non-trivial and BSNU-specific.

**nursing_ug/BSPRN — MEDIUM, dual-track guide with embedded catalog refs**

BSPRN is 1783 lines (largest guide in corpus). Contains:
- Two distinct SP tables (Pre-Nursing track + Nursing track)
- Two AoS sections (Pre-Nursing/Nursing combined structure)
- Embedded "BSPNTR/BSNPLTR 202303" catalog version references as page headers and embedded group names
- The parser produced 34 SP rows and 34 AoS courses at MEDIUM confidence, but with significant title mismatches (9 SP-only, 2 AoS-only titles) and version-reference strings appearing as group names

This guide is structurally atypical: it's a consolidated guide for what is effectively two programs. The "BSPNTR/BSNPLTR 202303" headers are from an embedded older catalog section. The parser tries to handle this as a single guide and partially succeeds, but the result is unreliable.

---

### 2.5 LOW confidence guides — substantial structural issues

**nursing_rn_msn (3 guides) — LOW, running header interference + non-course SP rows**

These are combined RN-to-MSN pathway guides (~1200 lines each). Key issues:

1. **No footer metadata**: "MSRNNUUG + MSNUED 202202" appears as a running page header every ~50 lines, not as a footer in the expected format. The metadata extractor finds no valid footer lines, so version/pub_date/page_count are unrecoverable.

2. **Non-course SP rows**: "Advanced Standing for RN License" is listed in the SP with cus=50 (a credit block, not a discrete course). This triggers `sp_row_invalid` anomaly.

3. **AoS group contamination**: "MSRNNUUG + MSNUED 202202" (the running page header) is parsed as an AoS group name in one location where it appears between AoS content blocks.

4. **Reconciliation failures**: 7 SP titles not found in AoS, 2 AoS titles not in SP. "Accessibility and Accomodations" (typo in source) parsed as an AoS title.

5. **Content gaps**: 3 courses with no description or competency bullets.

**Overall assessment**: These guides combine undergraduate RN content (MSRNNUUG) with specialty MSN content into a single very long document. The structural complexity is fundamental, not incidental. A robust parse would require dedicated handling for: (a) running header suppression, (b) non-course credit blocks, (c) multi-component guide structure. This is a non-trivial parser investment for 3 guides.

**accounting_ma specializations (3 guides) — LOW (already documented)**

MACCA, MACCF, MACCT: looks_like_prose failure on 40–50 char lines. Fix designed in Session 19 (verb-presence heuristic) but not implemented. AoS is structurally correct but specific courses are mis-parsed as group names.

---

## 3. Coverage projection under different rollout scenarios

### Baseline (current, post Session 19)
- Artifact coverage: 91 / 115 (79.1%)
- Family-validated: 87 / 115 (75.7%)
- Downstream-usable full SP+AoS: ~84 / 115

### Scenario A: Roll out the 14 clean candidates (endorsement 8 + nursing_msn 5 + MSEDL 1)
- Artifact coverage: 105 / 115 (91.3%)
- Family-validated: 101 / 115 (87.8%)
- Downstream-usable full SP+AoS: ~98 / 115
- **Work required:** Gate tests (3 gate guides + 14 rollout reviews). No parser changes needed. Conservative estimate: 1 session.

### Scenario B: Scenario A + fix accounting_ma specializations
- Family-validated: 104 / 115 (90.4%)
- **Work required:** Scenario A + looks_like_prose fix + regression testing across 91 guides. Medium session.

### Scenario C: Scenario A + add nursing_pmc and MEDETID with targeted fixes
- Family-validated: 110 / 115 (95.7%) [with PMC as AoS-only or with SP fix]
- **Work required:** Scenario A + nursing_pmc SP layout fix + MEDETID multi-path handling. Moderate to complex.

### Hard ceiling without major parser investment
- nursing_rn_msn (3): LOW, structural complexity. Would require running header suppression + non-course row handling + multi-component guide support. Probably not worth the investment for 3 guides.
- nursing_ug BSNU (1): 4-column SP. AoS usable without SP; adding SP support requires format detection work.
- nursing_ug BSPRN (1): Dual-track embedded-catalog guide. Partial usability at MEDIUM, SP title clutter.
- Even with all reasonable fixes, ~6 guides (nursing_rn_msn 3 + nursing_ug 2 + possibly BSPRN) will remain at MEDIUM/LOW.

---

## 4. Phase D readiness assessment

### What Phase D requires
Phase D = build `public/data/program_guides/{code}.json` for site integration. This means:
- Deciding which guides are safe to publish
- Defining the exact schema for the published artifact
- Building the `build_guide_site_data.py` script
- Testing that the runtime (Next.js) can consume the artifacts correctly

### Favorable signals
- 84+ downstream-usable guides with complete SP+AoS data (0 empty descriptions across all)
- Scenario A would push this to ~98 guides (85.2%) with no parser work
- Parser is stable and production-quality for validated families
- AoS data quality is uniformly excellent: 0 empty descriptions, near-zero empty bullet lists

### Honest gaps for Phase D
1. **No runtime integration exists yet.** `public/data/program_guides/` is empty. The schema for site-facing artifacts hasn't been confirmed against component needs. Phase D requires designing the output schema first.
2. **Inclusion/exclusion policy not formalized.** Which guides get published? All 84+ downstream-usable? Only HIGH confidence? What's the fallback for MEDIUM guides? This needs to be explicit before building.
3. **Course-code matching not done (Phase E).** Published guides will have course titles but no Atlas code links. This is acceptable for Phase D (titles only) but limits downstream utility.
4. **The 6–8 remaining problematic guides need explicit disposition.** Either: (a) exclude from Phase D output, (b) publish AoS-only where SP fails, or (c) fix parser. This choice needs to be made before the build script is written.

### Conservative Phase D readiness verdict
**Phase D is justified but not urgent.** The numeric and quality thresholds are clearly met for Scenario A. However, proceeding to Phase D before rolling out the 14 clean candidates (Scenario A) would waste the near-term coverage opportunity. The correct sequence is:

1. Gate and roll out endorsement + nursing_msn + MSEDL (Scenario A) — 1 session, no parser changes
2. Decide on nursing_pmc SP fix and accounting_ma fix (Scenario B/C scope)
3. Define Phase D inclusion/exclusion policy and output schema
4. Build Phase D artifacts

Do not start Phase D this session or the next rollout session. Do not use numeric threshold alone as a go signal.

---

## 5. Remaining risks by family

| Family | Guides | Risk | Root cause | Fix complexity |
|--------|--------|------|-----------|----------------|
| endorsement | 8 | **None** — parser handles correctly | Phase A uncertainty was unfounded | No fix needed |
| nursing_msn | 5 | **None** — parser handles correctly | Phase A uncertainty was unfounded | No fix needed |
| education_grad/MSEDL | 1 | **None** | Standard structure | No fix needed |
| nursing_pmc | 4 | **SP data missing** | "Changes to Curriculum" before SP table (page layout) | Targeted/low-regression SP anchor fix |
| education_grad/MEDETID | 1 | **SP overcounted** | 3 embedded SP sub-tables for 2 specializations | Moderate — specialization-path selection logic |
| nursing_ug/BSNU | 1 | **SP format unsupported** | 4-column SP (Option A/B dual path) | Non-trivial — 4-column format detection |
| nursing_ug/BSPRN | 1 | **Multi-track clutter** | Dual-track guide + embedded catalog refs | Complex — guide is unusual by design |
| nursing_rn_msn | 3 | **LOW quality** | Running headers, non-course SP rows, multi-component guide | Major investment for 3 guides |
| accounting_ma (deferred) | 3 | **AoS broken** | looks_like_prose too narrow | Medium — verb heuristic + full regression test |

---

## 6. Summary for decision-making

| Question | Answer |
|----------|--------|
| Are the "risky" families actually risky? | Endorsement and nursing_msn: NO. Parser handles them correctly. nursing_rn_msn and nursing_ug: YES — genuine structural complexity. |
| What is the fastest path to meaningful Phase D coverage? | Gate + roll out endorsement (8), nursing_msn (5), MSEDL (1). 14 guides, ~1 session, zero parser changes. Pushes family-validated to 101/115. |
| Is Phase D justified now? | Numeric threshold is met. Quality is sufficient. Runtime integration doesn't exist yet. Roll out the 14 clean guides first, then design Phase D schema and inclusion policy. |
| What are the stopping points? | nursing_rn_msn (3) and nursing_ug BSNU (1) are genuine hard cases. BSPRN (1) is usable at MEDIUM but noisy. These 5 guides might warrant explicit exclusion from Phase D rather than further parser investment. |
| What does "complete corpus" realistically mean? | A realistic ceiling is ~110/115 family-validated (if PMC fix + MEDETID fix + accounting_ma fix are done). The final 5–6 (nursing_rn_msn 3, BSNU 1, BSPRN 1) will remain at MEDIUM/LOW without major structural work. |
