# nursing_pmc — Gate Report
**Date:** 2026-03-21
**Family size:** 4 guides
**Gate guide:** PMCNUED
**Gate result:** PASS — all 4 guides HIGH confidence, 0 anomalies, 0 warnings

---

## Gate summary

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Anomalies |
|------|--------|------------|---------|------------|-------------|-----------|
| PMCNUED | Post-Master's Certificate, Nursing - Nursing Education (Post-MSN) | HIGH | 8 | 2 | 8 | 0 |
| PMCNUFNP | Post-Master's Certificate, Nursing - Family Nurse Practitioner (PostMSN) | HIGH | 10 | 2 | 10 | 0 |
| PMCNULM | Post-Master's Certificate, Nursing - Leadership and Management (PostMSN) | HIGH | 8 | 2 | 8 | 0 |
| PMCNUPMHNP | Post-Master's Certificate, Nursing - Psychiatric Mental Health Nurse | HIGH | 11 | 2 | 11 | 0 |

---

## PMCNUED (HIGH) — gate passed

Clean parse after SP layout fix. 8/8 reconciliation. 0 anomalies. 2 AoS groups: Nursing Core (1 course) and Nursing Education Specialty (7 courses). No capstone.

---

## Root cause and fix

**Root cause:** "Changes to Curriculum" boilerplate appears between the bare "Standard Path" intro header and the actual "Standard Path for Post-Master's Certificate..." table. In `parse_standard_path_multiline()`, the existing code broke immediately when "Changes to Curriculum" was encountered, regardless of whether the SP table had been entered. Since the table hadn't started yet (state = `BEFORE_TABLE`), the break was premature — the actual table was never reached.

**Fix:** Changed the SP_CHANGES_RE handler in `parse_standard_path_multiline()` from an unconditional `break` to a conditional:
- `break` if `state != 'BEFORE_TABLE'` (table is active — normal end-of-table signal)
- `continue` if `state == 'BEFORE_TABLE'` (table not yet started — skip and keep scanning)

Applied the equivalent fix (`in_table` condition) to `parse_standard_path()` for completeness.

**Scope:** General — applies to all guides. For all previously validated guides, "Changes to Curriculum" appears after the table starts, so `state != 'BEFORE_TABLE'` evaluates to True and the break fires as before. No behavior change for any validated guide.

---

## Secondary fix: degree_title

**Root cause:** PMC guides start with "Certificate Guidebook" on line 0 (equivalent to "Program Guidebook" in regular guides). The title extractor only skipped "Program Guidebook", so "Certificate Guidebook" was set as the degree_title.

**Fix:** Added "Certificate Guidebook" to the document-type header skip list in `extract_title_and_description()`.

**Scope:** General. Only affects guides where line 0 is "Certificate Guidebook" — which is the 4 PMC guides in this corpus.

---

## Structural notes

**SP format:** All 4 guides use multi-line 3-column format (Course / CUs / Term). Consistent with nursing_msn family.

**AoS structure:** All 4 guides have 2 AoS groups (core + specialty). Nursing Education and Leadership/Management tracks share 1 core course; FNP and PMHNP share 3 nurse practitioner core courses.

**"Post-Master" section:** Phase A manifest noted a "Post-Master" section variant in all 4 guides. In the parsed output, this content is correctly handled as part of the AoS — no separate section was detected or required.

**Metadata:** Page counts valid (10–13 pages). Version strings valid.

---

## Regression verification

3 parser fixes applied this session. Regression-verified against 19 guides from completed families:
- All HIGH guides maintained HIGH
- BSCSIA maintained MEDIUM with same 2 warnings
- MACCM maintained MEDIUM with same 2 warnings
- Zero confidence or anomaly regressions

---

## Rollout decision

**Full rollout — all 4 guides usable downstream.**

---

## Coverage impact

After nursing_pmc rollout:
- Artifact coverage: 110 / 115 guides (95.7%)
- Family-validated coverage: 106 / 115 guides (92.2%) — 15 complete families
- Downstream-usable full (SP+AoS): approximately 103 guides
