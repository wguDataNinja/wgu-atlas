# Program Guide Family Inventory

**Audit date:** 2026-03-21
**Total families:** 19
**Total guides:** 115
**Parsed guides:** 38 (standard_bs + cs_ug + education_ba)
**Corpus coverage:** 33%

---

## Family Status Summary

| Family | Count | Status | Rollout Confidence |
|--------|-------|--------|--------------------|
| standard_bs | 19 | **Fully rolled out** | 16 HIGH / 2 MEDIUM / 1 LOW |
| education_ba | 11 | **Fully rolled out** | 5 HIGH / 6 MEDIUM / 0 LOW |
| cs_ug | 8 | **Fully rolled out** | 4 HIGH / 4 MEDIUM / 0 LOW |
| graduate_standard | 9 | Untouched | manifest: 2H/7M |
| teaching_mat | 9 | Untouched | manifest: 0H/9M |
| education_ma | 9 | Untouched | manifest: 2H/7M |
| endorsement | 8 | Untouched | manifest: 0H/8M |
| cs_grad | 5 | Untouched | manifest: 1H/4M |
| accounting_ma | 5 | Untouched | manifest: 0H/5M |
| nursing_msn | 5 | Untouched | manifest: 0H/5M |
| education_bs | 4 | Untouched | manifest: 0H/4M |
| swe_grad | 4 | Untouched | manifest: 0H/4M |
| nursing_pmc | 4 | Untouched | manifest: 0H/4M |
| mba | 3 | Untouched | manifest: **3H/0M** |
| data_analytics_grad | 3 | Untouched | manifest: 0H/3M |
| nursing_rn_msn | 3 | Untouched | manifest: 0H/3M |
| nursing_ug | 2 | Untouched | manifest: 0H/2M |
| education_grad | 2 | Untouched | manifest: 1H/1M |
| healthcare_grad | 2 | Untouched | manifest: 1H/1M |

> **Note on manifest confidence:** The lightweight manifest probe uses simpler heuristics than the full content parser. "MEDIUM" in manifest means the probe flagged `no_sp_rows_found` (multi-line SP format not detected at probe level) — it does NOT predict content-parse failure. The manifest is a corpus characterization tool only; actual parse confidence must be earned by running the parser.

---

## Fully Rolled Out Families

### standard_bs (19 guides)

| Code | Degree | Confidence | SP Format | SP Rows | AoS Groups | AoS Courses | Capstone | Notes |
|------|--------|------------|-----------|---------|------------|-------------|---------|-------|
| BSACC | B.S. Accounting | HIGH | 3-col | 40 | 4 | 40 | — | |
| BSBAHC | B.S. Business Admin, Healthcare Mgmt | HIGH | 3-col | 40 | 7 | 39 | ✓ | |
| BSC | B.S. Communications | HIGH | 3-col | 38 | 6 | 38 | — | |
| BSDA | B.S. Data Analytics | HIGH | 3-col | 42 | 14 | 41 | ✓ | |
| BSFIN | B.S. Finance | HIGH | 3-col | 40 | 6 | 40 | — | has Prerequisites section |
| BSHA | B.S. Healthcare Administration | HIGH | 3-col | 34 | 7 | 34 | — | |
| BSHHS | B.S. Health and Human Services | HIGH | 3-col | 35 | 9 | 34 | ✓ | |
| BSHIM | B.S. Health Info Management | MEDIUM | 3-col | 36 | 8 | 36 | — | 1 PDF fragment as title |
| BSHR | B.S. Human Resource Management | HIGH | 3-col | 39 | 4 | 39 | — | |
| BSHS | B.S. Health Science | HIGH | 3-col | 28 | 6 | 28 | — | |
| BSIT | B.S. Information Technology | HIGH | 3-col | 35 | 12 | 35 | — | |
| BSITM | B.S. IT Management | **LOW** | 3-col | 35* | 9 | 40 | — | PDF layout artifact in SP |
| BSMES | B.S. Mathematics Education (Secondary) | HIGH | **2-col** | 39 | 8 | 39 | — | Clinical + Student Teaching AoS groups |
| BSMGT | B.S. Business Management | HIGH | 3-col | 36 | 5 | 35 | ✓ | |
| BSMKT | B.S. Marketing | HIGH | 3-col | 37 | 5 | 37 | — | |
| BSPH | B.S. Public Health | HIGH | 3-col | 33 | 6 | 33 | — | |
| BSPSY | B.S. in Psychology | HIGH | 3-col | 34 | 4 | 34 | — | |
| BSSCOM | B.S. Supply Chain & Operations Mgmt | MEDIUM | 3-col | 35 | 5 | 35 | — | Last SP row truncated |
| BSUXD | B.S. User Experience Design | HIGH | 3-col | 38 | 6 | 38 | — | |

*BSITM: first 5 SP course titles garbled by PDF column extraction failure. AoS (40 courses) is correct.

**Reliable fields for standard_bs:** course descriptions, competency bullets, prereq mentions, cert-prep mentions. SP term/CU values reliable except BSITM.

---

### cs_ug (8 guides)

| Code | Degree | Confidence | SP Format | SP Rows | AoS Groups | AoS Courses | Capstone | Notes |
|------|--------|------------|-----------|---------|------------|-------------|---------|-------|
| BSCS | B.S. Computer Science | HIGH | 3-col multiline | 37 | 12 | 37 | — | |
| BSCNE | B.S. Cloud and Network Engineering | HIGH | 3-col multiline | 34 | 13 | 34 | — | |
| BSCNEAWS | B.S. Cloud/Network Eng (AWS) | HIGH | 3-col multiline | 35 | 13 | 35 | — | high cert-prep: 11 |
| BSCNEAZR | B.S. Cloud/Network Eng (Azure) | HIGH | 3-col multiline | 35 | 13 | 35 | — | high cert-prep: 13 |
| BSCNECIS | B.S. Cloud/Network Eng (CIS) | MEDIUM | 3-col multiline | 32 | 13 | 32 | — | source typo in SP |
| BSCSIA | B.S. Cybersecurity and Info Assurance | MEDIUM | 3-col multiline | 38 | 11 | 38 | ✓ | minor title variant |
| BSSWE_C | B.S. Software Engineering (C#) | MEDIUM | 3-col multiline | 35 | 10 | 35 | — | no footer metadata; 1 empty competency |
| BSSWE_Java | B.S. Software Engineering (Java) | MEDIUM | 3-col multiline | 38 | 10 | 38 | — | no footer metadata |

**Reliable fields for cs_ug:** course descriptions, competency bullets, prereq mentions, cert-prep mentions (especially high in cloud/network guides).

---

### education_ba (11 guides)

| Code | Degree | Confidence | SP Format | SP Rows | AoS Groups | AoS Courses | Capstone | Clinical/ST | Notes |
|------|--------|------------|-----------|---------|------------|-------------|---------|------------|-------|
| BAELED | B.A. Elementary Education | HIGH | 2-col | 37 | 5 | 37 | — | Clinical + ST | teacher licensure |
| BAESELED | B.A. Ed Studies in Elem Ed | HIGH | 3-col | 33 | 3 | 33 | — | — | |
| BAESMES | B.A. Ed Studies in Sec Math | HIGH | 3-col | 35 | 6 | 35 | — | — | |
| BAESSESB | B.A. Ed Studies in Sec Bio Sci | MEDIUM | 3-col | 36 | 9 | 37 | — | — | last SP row split at PDF page boundary |
| BAESSESC | B.A. Ed Studies in Sec Chem Sci | HIGH | 3-col | 36 | 8 | 36 | — | — | |
| BAESSESE | B.A. Ed Studies in Sec Earth Sci | MEDIUM | 3-col | 36 | 9 | 37 | — | — | same PDF boundary issue as BAESSESB |
| BAESSESP | B.A. Ed Studies in Sec Physics | HIGH | 3-col | 36 | 8 | 36 | — | — | |
| BAESSPEE | B.A. Ed Studies Sped + Elem | MEDIUM | 3-col | 41 | 5 | 40 | — | — | PDF reordering: 1 course missing from AoS |
| BAESSPMM | B.A. Ed Studies Mild-Mod Exceptionalities | MEDIUM | 3-col | 34 | 5 | 33 | — | — | same reordering artifact |
| BASPEE | B.A. Sped + Elem Ed (Dual Lic) | MEDIUM | 2-col | 45 | 7 | 44 | — | Clinical + ST | same reordering artifact |
| BASPMM | B.A. Sped Mild-Mod Exceptionalities | MEDIUM | 2-col | 38 | 6 | 37 | — | Clinical | same reordering artifact |

**Reliable fields for education_ba:** course descriptions, competency bullets. SP term/CU values reliable for educational_studies subtype only. Teacher licensure subtype has no Term column.
**Caution:** 4 Special Education guides have 1 missing AoS course — cross-reference SP row count to detect.

---

## Untouched Families (77 guides / 16 families)

| Family | Count | Codes | Key Unknowns | Risk Level |
|--------|-------|-------|-------------|-----------|
| graduate_standard | 9 | MSCIN, MSHRM, MSIT, MSITM, MSITPM, MSITUG, MSMK, MSMKA, MSML | SP format, grad CU/term expectations | **LOW** — structurally similar to standard_bs |
| teaching_mat | 9 | MATEES, MATELED, MATMES, MATSESB, MATSESC, MATSESE, MATSESP, MATSPED, MATSSES | SP format; clinical/ST section variants | **MEDIUM** — similar to education_ba; known patterns |
| education_ma | 9 | MAELLP12, MAMEK6, MAMEMG, MAMES, MASEMG, MASESB, MASESC, MASESE, MASESP | SP format; Field Experience in MAELLP12 | **MEDIUM** — Field Experience untested |
| endorsement | 8 | ENDECE, ENDELL, ENDMEMG, ENDSEMG, ENDSESB, ENDSESC, ENDSESE, ENDSESP | Structure may differ substantially | **HIGH** — may have abbreviated or non-standard structure |
| cs_grad | 5 | MSCSAIML, MSCSCS, MSCSHCI, MSCSIA, MSCSUG | SP format for graduate | **LOW-MEDIUM** |
| accounting_ma | 5 | MACC, MACCA, MACCF, MACCM, MACCT | SP format; track variant handling | **LOW-MEDIUM** |
| nursing_msn | 5 | MSNUED, MSNUFNP, MSNULM, MSNUNI, MSNUPMHNP | Clinical section handling | **HIGH** — unknown clinical section format |
| education_bs | 4 | BSSESB, BSSESC, BSSESE, BSSESP | SP format; Clinical/ST as in education_ba | **MEDIUM** |
| swe_grad | 4 | MSSWEAIE, MSSWEDDD, MSSWEDOE, MSSWEUG | SP format for graduate SWE | **LOW-MEDIUM** |
| nursing_pmc | 4 | PMCNUED, PMCNUFNP, PMCNULM, PMCNUPMHNP | Post-Master section unhandled | **HIGH** — Post-Master section silently skipped |
| mba | 3 | MBA, MBAHA, MBAITM | SP format | **LOW** — all manifest HIGH; simplest structure expected |
| data_analytics_grad | 3 | MSDADE, MSDADPE, MSDADS | SP format for track variants | **LOW-MEDIUM** |
| nursing_rn_msn | 3 | MSRNNUED, MSRNNULM, MSRNNUNI | Clinical section; RN pathway structure | **HIGH** |
| nursing_ug | 2 | BSNU, BSPRN | Prerequisites section; clinical sections | **HIGH** |
| education_grad | 2 | MEDETID, MSEDL | Practicum section in MSEDL unhandled | **MEDIUM** |
| healthcare_grad | 2 | MHA, MPH | SP format for grad healthcare | **LOW** |
