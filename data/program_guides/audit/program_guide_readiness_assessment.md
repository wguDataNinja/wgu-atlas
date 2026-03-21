# Program Guide Readiness Assessment

**Audit date:** 2026-03-21
**Type:** Conservative decision-ready audit

---

## Corpus Coverage

| Metric | Value |
|--------|-------|
| Total guides | 115 |
| Parsed guides | 38 |
| Corpus coverage | **33%** |
| Fully validated families | standard_bs, cs_ug, education_ba |
| Untouched families | 16 families, 77 guides |

---

## What Is Already Trustworthy

Scope: 38 parsed guides across 3 completed families.

- **Course descriptions:** 0 empty descriptions across all 38 guides (532+ courses). The cleanest, most reliable field in the entire pipeline.
- **Competency bullets:** Near-zero empty (2 known PDF artifact cases, both documented). Robust across all structure variants.
- **Cert-prep inline mentions:** Reliable inline extraction. Highly valuable in cs_ug; present in 27/38 parsed guides.
- **AoS state machine:** Validated across 3 structurally different families. Handles 4–14 groups, 28–45 courses per guide.
- **Standard Path 3-col parsing:** Validated for 24 guides.
- **Standard Path 2-col parsing:** Validated for 4 guides (education_ba teacher licensure + BSMES).
- **Footer metadata extraction:** Validated across guides with footer format.
- **Header-line metadata extraction:** Validated across education_ba and relevant standard_bs guides.
- **Clinical Experiences / Student Teaching as AoS group labels:** Validated in education_ba and BSMES.
- **Section anchor detection:** Robust. False-Capstone-detection fix deployed and validated.
- **Artifact schema:** parsed.json / validation.json / manifest_row.json / rollout_summary.json all have stable, production-quality schemas.

---

## What Is Trustworthy Only for Completed Families

Do not extrapolate these to untouched families.

- SP course count and title list (per program in 3 completed families)
- SP term sequence and CU values (where 3-col format confirmed)
- AoS group count and structure (per program in 3 completed families)
- Prereq mention flags (as binary flags only; false-positive rate documented)
- Capstone identification (present/absent reliable for parsed guides)
- Guide metadata (version, pub_date) for 36 of 38 parsed guides

---

## What Is Promising But Not Yet Trustworthy

These families are expected to parse cleanly but have 0 content parses done.

| Family | Guides | Why promising | Why not yet trustworthy |
|--------|--------|--------------|------------------------|
| graduate_standard | 9 | Structurally similar to standard_bs; DEV_NOTES recommended | No content parse; graduate SP format unconfirmed |
| mba | 3 | All manifest HIGH; simplest expected structure | No content parse |
| healthcare_grad | 2 | MHA mentioned in DEV_NOTES; manifest 1H/1M | No content parse |
| cs_grad | 5 | Analogous to cs_ug structure | No content parse; graduate differences unknown |
| teaching_mat | 9 | Shares Clinical/ST patterns validated in education_ba | No content parse; all manifest MEDIUM |
| education_bs | 4 | Same Clinical/ST patterns as education_ba teacher licensure | No content parse |
| data_analytics_grad | 3 | Track variant structure expected | No content parse |
| accounting_ma | 5 | Track variant structure expected | No content parse |
| swe_grad | 4 | Analogous to cs_ug/cs_grad structure | No content parse |
| education_ma | 9 | Similar to education_ba | MAELLP12 has Field Experience (untested) |

---

## What Is Too Risky to Use Yet

| Item | Risk | Status |
|------|------|--------|
| **BSITM Standard Path data** | LOW confidence — PDF column extraction failure garbled SP titles | Do not use SP data; AoS correct and usable |
| **4 Sped education_ba AoS outputs** | 1 missing course per guide; known PDF reordering artifact | Flag for downstream users; cross-check SP count |
| **Any data from 77 untouched guides** | No content parse done | Off-limits for integration |
| **Endorsement family** | Structure unknown; may differ substantially | Requires gate test before any assumption |
| **Nursing families (msn/pmc/rn_msn/ug)** | Clinical section handling untested; Post-Master sections skipped | Requires gate test + Post-Master handler |
| **Field Experience content** | Section format unknown; parser not run | Deferred |
| **Practicum content** | Section format unknown; parser not run | Deferred |
| **Prereq text (raw)** | Known false-positive regex pattern | Use as flag only; never display raw extracted text |
| **Course-code matching** | Phase E not started | Titles cannot be linked to Atlas codes yet |
| **Site artifacts** | Phase D not started | No runtime artifacts produced |

---

## Validations Earned vs. Still Missing

### Earned

- SP format detection (2-col, 3-col, multiline): cross-validated
- AoS state machine robustness: 3 families, diverse structures
- Bullet continuation logic: validated with edge case documented
- Metadata extraction (footer + header-line): validated
- Section anchor detection: robust
- Artifact schemas: production-quality
- False-Capstone-detection fix: no regressions found

### Still Missing

- Graduate SP format behavior (7 grad families)
- Endorsement structure
- Nursing clinical/PMC/RN-MSN section handling
- Field Experience and Practicum section handling
- education_ma, teaching_mat, education_bs full rollout
- Bullet-continuation heuristic fix for Sped course title edge case (deferred)
- Course-code matching (Phase E)
- Site artifact build script and output schema (Phase D)

---

## Overall Posture

**NOT ready for broad rollout or site integration.**

**Ready for: continued targeted family rollouts with gate testing.**

The 38 parsed guides represent production-quality internal artifacts for their families. The course description and competency bullet data is genuinely trustworthy. But 67% of the corpus is unparsed, and 4 of the 5 highest-risk section patterns (nursing clinical, Field Experience, Practicum, Post-Master, endorsement structure) are completely unvalidated.

Site integration at this stage would cover only 33% of programs — producing a patchy result that is difficult to explain to users and hard to fill in later without disruption.

---

## Recommended Next 3 Concrete Steps

**Step 1 — Run graduate_standard gate test**
Parse MBA (all manifest HIGH, simplest graduate structure expected). If HIGH confidence and no new section patterns, proceed immediately to full graduate_standard rollout (9 guides).

**Step 2 — Run mba rollout**
3 guides, all manifest HIGH. If gate test confirms clean structure, full rollout is appropriate in a single pass. This brings parsed guide count to ~50 (43%).

**Step 3 — Run healthcare_grad gate test (MHA or MPH)**
2 guides; MHA mentioned in DEV_NOTES as a candidate. Confirms whether graduate healthcare guides differ from standard graduate structure. Small batch, high information value.

After these three steps: reassess at ~50 parsed guides (43%). Likely next targets: `teaching_mat` and `education_bs` (share validated education_ba patterns). Defer endorsement and nursing until structure is confirmed via independent gate tests.

**Phase D (site artifact build) target:** Begin design when ≥70 guides are parsed (60-70% coverage). Do not wire to site until coverage warrants it.
