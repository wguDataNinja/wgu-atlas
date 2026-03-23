# Course Text Comparison Index

**Version:** 1.0
**Date:** 2026-03-23
**Status:** Staging artifact for later LLM review — no policy decisions here.
**Purpose:** Side-by-side index of all catalog-vs-guide course description pairs. Used to filter exact/near-duplicate pairs, identify materially different cases, and select an intelligent LLM sample for display/authority policy review.

---

## 1. Scope

**Block type covered:** Course overview/description text only.
- Source A: WGU catalog course description (extracted from catalog PDF text, 2026-03 edition)
- Source B: WGU program guide course description (extracted from AoS/SP sections of per-program guide PDFs, guide version varies by source program)

**Not covered in this pass:** competency bullets, cert signals, prereq text, capstone text. Those are guide-only and have no catalog overlap to index.

**Entity scope:** Active and recently retired course codes. Only pairs where BOTH sources have description text. Courses present in only one source are noted in §4 but not indexed here (they have no overlap pair to compare).

---

## 2. Inputs Inspected

| Artifact | Role |
|---|---|
| `public/data/course_descriptions.json` | Source A (catalog descriptions) — 838 entries |
| `data/program_guides/enrichment/course_enrichment_candidates.json` | Source B (guide descriptions) — 751 courses; 730 with at least 1 description |
| `data/canonical_courses.json` | Course identity reference (title, CU, status) |

---

## 3. Comparison Construction Rules

1. **Pairing:** Each catalog description is paired with each guide description variant for that course code. If a course has 3 guide description variants, it generates 3 rows (one per variant pairing).
2. **Version handling:** Source A version is `WGU Catalog 2026-03` (fixed). Source B version is not a single guide version — it reflects the source program(s) whose guide contained that description text. Source program codes are recorded per row.
3. **Exact match:** `cat_text.strip() == guide_text.strip()`
4. **Near-duplicate:** Not exact AND `abs(len_cat - len_guide) <= 5`. This catches 1–5 character differences (trailing punctuation, hyphen vs space, single-char whitespace differences).
5. **Materially different:** Not exact AND NOT near-dup. Subdivided into:
   - **STRONG** (diff > 50): likely different authoring event, rewrite, or version-drift
   - **MOD** (diff 6–50): possible minor edits, additions, or truncations
6. **Text included:** First 200 characters of each source for all non-exact rows. Truncated with `…`.
7. **Multi-variant guide cases:** All variants indexed as separate rows. `v_idx/v_total` field indicates which variant and total variant count.
8. **No text normalization** beyond `.strip()` — whitespace differences inside the string are not collapsed.

---

## 4. Summary Counts

| Category | Rows | Unique courses |
|---|---|---|
| **Total pairs indexed** | 633 | — |
| Exact match (cat == guide) | 465 | 447 |
| Near-duplicate (diff ≤ 5) | 59 | 57 |
| Materially different — STRONG (diff > 50) | 69 | ~65 |
| Materially different — MOD (diff 6–50) | 40 | ~38 |
| **Materially different total** | 109 | ~103 |
| Multi-variant guide rows (v > 1) | ~118 | ~74 |

**Non-paired courses (not indexed here):**
- Guide description only (no catalog desc): ~167 active courses
- Catalog description only (no guide enrichment): ~267 courses

**Interpretation:** 78% of pairs are exact matches — catalog and guide text are identical. 9% (59 rows) differ by ≤ 5 chars — almost certainly the same authoring event with minor formatting differences (trailing space, hyphen normalization). Only ~17% (109 rows) merit review. Of those, 69 are strongly different enough to constitute a genuine display authority question.

---

## 5A. Exact Match Pairs (465 rows, 447 unique courses)

All 447 courses below have `cat_text == guide_text` for their first (or only) guide description variant. These require no authority policy decision for display — either source produces the same text. Multi-variant courses not listed here may have exact matches on some variants but differences on others (see §5B/5C).

<details>
<summary>Exact-match course codes (447 courses — click to expand)</summary>

```
AFT2 AMT2 AOA2 ASA1 AVA2
C100 C165 C168 C180 C190 C200 C201 C202 C203 C204 C205 C206 C207 C208 C209 C211 C212 C213 C214 C215
C224 C225 C226 C227 C232 C233 C237 C273 C278 C360 C455 C456 C458 C464 C483 C659 C683 C715 C716 C717
C720 C721 C722 C723 C724 C784 C790 C792 C797 C798 C801 C802 C804 C805 C807 C810 C811 C812 C815 C816
C870 C871 C918 C919 C949 C950 C955 C957 C959 C960 C963 C968 C969 CUA1
D016 D017 D018 D019 D022 D023 D026 D027 D030 D031 D034 D035 D038
D072 D075 D076 D077 D080 D081 D098 D099 D100 D102 D105
D115 D116 D117 D123 D156 D174 D175 D176 D177 D179 D180 D184 D186 D187 D188
D196 D197 D198 D199 D202 D203 D220 D222 D223 D226 D235 D252 D253 D256 D257 D258 D259
D263 D265 D266 D267 D268 D269 D270 D277 D280 D286 D287 D288 D291 D292 D293 D294 D298 D299
D303 D308 D311 D313 D314 D315 D319 D322 D336 D343 D361 D363 D364 D365 D366 D367 D369
D373 D374 D375 D377 D378 D379 D380 D381 D382 D383 D385 D388 D390 D396 D399 D400 D402 D409
D412 D413 D414 D415 D416 D417 D420 D421 D422 D424 D425 D426 D428 D429 D430
D458 D464 D465 D466 D468 D469 D470 D471 D473 D481 D483 D484 D485 D486 D489 D491 D501 D522
D546 D547 D548 D549 D550 D552 D558 D564 D565 D571 D572 D573 D574 D575 D576 D579 D580 D582 D583 D584
D585 D586 D587 D589 D590 D591 D592 D593 D594 D595 D599 D605 D609 D610 D612 D613 D614 D617
D621 D623 D624 D625 D627 D628 D635 D640 D641 D642 D643 D644 D646 D647 D649 D650 D651 D652 D653 D654
D655 D656 D657 D659 D660 D661 D663 D664 D667 D668 D669 D670 D671 D672 D673 D674
D683 D684 D685 D686 D688 D689 D690 D691 D692 D695 D698 D705 D706 D707 D708 D709
D717 D718 D719 D720 D721 D722 D723 D737 D738 D739 D740 D741 D742 D743 D752 D755 D757
D771 D772 D774 D775 D776 D780 D782 D787 D790 D793 D794 D795 D796 D798 D799 D800 D802 D803
D805 D806 D807 D822 D827 D831 D835 D841 D844 D845 D846 D847 D848 D849 D850
D852 D853 D854 D855 D856 D857 D859 D860 D861 D862 D863 D866 D868 D869
D870 D871 D873 D874 D875 D876 D877 D878 D880 D881 D882 D887 D888 D889 D890 D891 D892 D893 D894
D896 D897 D898 D899 D900 D904 D908 D909 D910 D911 D913 D915
D922 D923 E004 E005 E006 E007 E008 E009 E010 E013 E015 E016 E017 E018 E019 E020 E021 E022 E023 E024
E025 E026 E027 E028 E029 E030 E031 E032 E033 E224 E225
ELO1 FEA1 LPA1 MFT2 MGT2 MMT2 NMA1 NNA1 QFT1 QHT1 RXT2 SLO1 VZT1
```
</details>

Notable: the large blocks of D6xx–D9xx codes (Education college courses) and E0xx codes (BSIT/CNE/MSIT series) are almost entirely exact matches. Catalog and guide text was authored from the same source at the same time for these course families.

---

## 5B. Near-Duplicate Pairs (diff ≤ 5, 59 rows)

These pairs differ by 1–5 characters. The difference is almost always a trailing space, hyphen vs. space, "competency- based" vs. "competency-based", or whitespace normalization. No display policy decision needed for most of these — they are the same text.

**Exceptions to review:** D355 (diff=4) and C165 v2 (diff=3) show slightly different phrasing within the body. Flagged below.

| code | v_idx/v_total | cat_len | guide_len | diff | source_programs | cat_text (120 chars) | guide_text (120 chars) |
|---|---|---|---|---|---|---|---|
| AUA2 | 1/1 | 377 | 376 | 1 | MAMEK6 | `Auditing covers the conduct of financial audits and the evaluation of internal controls…` | `Auditing covers the conduct of financial audits and the evaluation of internal controls…` |
| C121 | 1/1 | 239 | 238 | 1 | BSBAHC,BSITM | `Spreadsheets is a project-based course that…` | `Spreadsheets is a project-based course that…` |
| C165 | 2/2 | 339 | 342 | 3 | MASEMG,MASESC,MASESP | `…focuses on scientific reasoning and practical, everyday applications…` | `…focuses on scientific reasoning and practical and everyday applications…` |
| C200 | 1/2 | 338 | 337 | 1 | MBA,MBAITM,MSMK | `Managing in Social Context examines the environment of business…` | `Managing in Social Context examines the environment of business…` |
| C209 | 1/1 | 210 | 208 | 2 | MACC,MSML | `Advanced Accounting Concepts and Applications examines complex accounting topics…` | `Advanced Accounting Concepts and Applications examines complex accounting topics…` |
| C278 | 2/2 | 355 | 354 | 1 | MAMEMG | `Earth Science: Earth's Composition…` | `Earth Science: Earth's Composition…` |
| C720 | 2/2 | 807 | 811 | 4 | BSBAHC,BSFIN | `Auditing I introduces students to the audit process…` | `Auditing I introduces students to the audit process…` |
| C971 | 1/1 | 769 | 768 | 1 | BSSWE_C | `Cloud Foundations introduces cloud computing…` | `Cloud Foundations introduces cloud computing…` |
| D028 | 1/2 | 828 | 827 | 1 | MSNUED,MSNULM,MSNUNI | `Organizational Systems and Quality Leadership…` | `Organizational Systems and Quality Leadership…` |
| D029 | 1/2 | 910 | 908 | 2 | MSNUED,MSNUFNP,MSNULM | `Foundations of Nursing Practice…` | `Foundations of Nursing Practice…` |
| D122 | 1/2 | 1198 | 1197 | 1 | MSNUFNP | `Advanced Pathophysiology…` | `Advanced Pathophysiology…` |
| D124 | 1/2 | 965 | 964 | 1 | MSNUFNP | `Advanced Health Assessment…` | `Advanced Health Assessment…` |
| D155 | 1/1 | 893 | 892 | 1 | MSNULM,MSRNNULM,PMCNULM | `Leadership and Management in Nursing…` | `Leadership and Management in Nursing…` |
| D175 | 2/3 | 663 | 662 | 1 | BSMKT | `Consumer Behavior and Ethics…` | `Consumer Behavior and Ethics…` |
| D178 | 1/1 | 801 | 800 | 1 | BSMKT | `Digital Marketing…` | `Digital Marketing…` |
| D181 | 1/1 | 832 | 831 | 1 | MSCIN | `Curriculum Design and Instruction…` | `Curriculum Design and Instruction…` |
| D296 | 1/1 | 1116 | 1115 | 1 | MEDETID | `Instructional Design Theory…` | `Instructional Design Theory…` |
| D297 | 1/1 | 788 | 787 | 1 | MEDETID | `Instructional Media…` | `Instructional Media…` |
| D312 | 1/2 | 688 | 687 | 1 | BSHS,BSNU,BSPRN | `Health, Fitness, and Wellness…` | `Health, Fitness, and Wellness…` |
| D312 | 2/2 | 688 | 688 | 0 | MSRNNUED,MSRNNULM,MSRNNUNI | (exact) | (exact) |
| D348 | 1/2 | 912 | 911 | 1 | MSNUPMHNP | `Psychopharmacology…` | `Psychopharmacology…` |
| D355 | 1/1 | 457 | 461 | 4 | BSHR | `Compensation and Benefits examines key aspects of building a total compensation…` | `Compensation and Benefits examines strategies for building total compensation systems…` |
| D372 | 1/1 | 888 | 887 | 1 | BSDA,BSSWE_C,BSSWE_Java | `Data Systems Administration…` | `Data Systems Administration…` |
| D376 | 1/1 | 643 | 642 | 1 | MSMK,MSMKA | `Marketing Research…` | `Marketing Research…` |
| D384 | 1/1 | 876 | 875 | 1 | MSMK,MSMKA | `Marketing Strategy…` | `Marketing Strategy…` |
| D386 | 1/1 | 409 | 408 | 1 | BSDA,BSSWE_C,BSSWE_Java | `Data Wrangling…` | `Data Wrangling…` |
| D387 | 1/2 | 405 | 404 | 1 | BSCS | `Algorithm Design and Analysis…` | `Algorithm Design and Analysis…` |
| D401 | 1/1 | 650 | 649 | 1 | BSHHS,BSHS,BSPH | `Healthcare Quality…` | `Healthcare Quality…` |
| D426 | 1/2 | 297 | 296 | 1 | BSCS,BSCSIA | `Data Management - Foundations offers an introduction in creating conceptual, logical and physical data models. Students gain skills in creating databases…` | `Data Management - Foundations offers an introduction in creating conceptual, logical and physical data models. Students gain skills in creating databases…` |
| D467 | 1/1 | 523 | 522 | 1 | BSSCOM | `Supply Chain Management…` | `Supply Chain Management…` |
| D480 | 1/1 | 759 | 758 | 1 | BSCS,BSSWE_C,BSSWE_Java | `Software Engineering…` | `Software Engineering…` |
| D492 | 1/1 | 305 | 303 | 2 | BSCSIA,BSDA | `Digital Forensics…` | `Digital Forensics…` |
| D545 | 1/1 | 490 | 489 | 1 | BSHA | `Healthcare Economics…` | `Healthcare Economics…` |
| D553 | 1/1 | 848 | 844 | 4 | MACCA,MACCF,MACCM | `Cost Accounting…` | `Cost Accounting…` |
| D557 | 1/1 | 595 | 594 | 1 | MACCT | `Taxation of Business Entities…` | `Taxation of Business Entities…` |
| D566 | 1/1 | 703 | 698 | 5 | BSPSY | `Psychotherapy and Counseling…` | `Psychotherapy and Counseling…` |
| D569 | 1/1 | 468 | 465 | 3 | BSPSY | `Child and Adolescent Psychology…` | `Child and Adolescent Psychology…` |
| D577 | 1/1 | 520 | 518 | 2 | BSHHS,BSPH,BSPSY | `Mental Health Concepts…` | `Mental Health Concepts…` |
| D578 | 1/1 | 619 | 617 | 2 | BSPSY | `Cognitive Psychology…` | `Cognitive Psychology…` |
| D583 | 2/2 | 632 | 632 | 0 | BSHS | (exact) | (exact) |
| D588 | 1/1 | 1069 | 1068 | 1 | BSPH | `Community and Population Health…` | `Community and Population Health…` |
| D597 | 1/1 | 589 | 591 | 2 | MSDADE,MSDADPE,MSDADS | `Data Analysis…` | `Data Analysis…` |
| D600 | 1/1 | 622 | 619 | 3 | MSDADE,MSDADPE,MSDADS | `Big Data…` | `Big Data…` |
| D626 | 1/1 | 544 | 543 | 1 | MPH | `Epidemiology…` | `Epidemiology…` |
| D635 | 2/2 | 993 | 989 | 4 | MATELED | `Secondary Clinical Experiences…` | `Secondary Clinical Experiences…` |
| D668 | 2/2 | 894 | 894 | 0 | MATSPED | (exact) | (exact) |
| D673 | 2/2 | 837 | 836 | 1 | MATELED | `Student Teaching: Elementary Education…` | `Student Teaching: Elementary Education…` |
| D757 | 2/2 | 499 | 498 | 1 | MATSPED | `Assessment in Special Education…` | `Assessment in Special Education…` |
| D769 | 1/1 | 657 | 656 | 1 | BAESMES,BAESSESB,BAESSESC | `Science Methods…` | `Science Methods…` |
| D785 | 1/1 | 756 | 756 | 0 | MSSWEDOE | (exact) | (exact) |
| D804 | 1/1 | 716 | 715 | 1 | MSCSAIML | `Foundations of AI…` | `Foundations of AI…` |
| D836 | 1/1 | 729 | 728 | 1 | MATSSES | `Social Studies Methods…` | `Social Studies Methods…` |
| D837 | 1/1 | 513 | 517 | 4 | MATSSES | `Classroom Management…` | `Classroom Management…` |
| D864 | 1/2 | 708 | 707 | 1 | BAESSESP,BSSESP,ENDSESP | `Physics…` | `Physics…` |
| D864 | 2/2 | 708 | 710 | 2 | MATSESP | `Physics…` | `Physics…` |
| D867 | 1/1 | 563 | 562 | 1 | BAESSESC,BSSESC | `Chemistry…` | `Chemistry…` |
| D879 | 1/1 | 420 | 419 | 1 | BAESSESB,BSSESB,ENDSESB | `Biology…` | `Biology…` |
| D901 | 1/1 | 902 | 901 | 1 | BAESMES,BSMES,MATMES | `Algebra…` | `Algebra…` |
| PFIT | 1/1 | 331 | 332 | 1 | BSITM | `Fitness and Health…` | `Fitness and Health…` |

**Note on D355:** This is the most notable near-dup. Catalog says "examines key aspects of building a total compensation" while guide says "examines strategies for building total compensation systems" — a 4-char length difference but different wording. This may be worth escalating to the LLM sample as a borderline meaningful case.

---

## 5C. Materially Different Pairs (diff > 5, 109 rows)

### 5C-i. STRONG differences (diff > 50) — 69 rows

These are the highest-priority cases for display authority policy. Sorted by diff descending.

| code | title | CU | v | cat_len | guide_len | diff | source_programs | cat_text (200 chars) | guide_text (200 chars) |
|---|---|---|---|---|---|---|---|---|---|
| D560 | Internal Auditing I | 3 | 1/1 | 998 | 506 | 492 | MACCA,MACCM | `Internal Auditing I provides learners with the basic knowledge and skills necessary to succeed as an entry-level internal audit professional. The course introduces the fundamentals of internal auditing…` | `Internal Auditing I provides learners with the basic knowledge and skills necessary to succeed as an entry-level internal audit professional. The Institute of Internal Auditors defines internal auditing…` |
| D358 | Global Human Resource Management | 3 | 1/1 | 414 | 897 | 483 | BSHR | `Organizations increasingly operate across borders, and HR professionals must be prepared to manage people in diverse cultural and legal environments. This course introduces you to international HR pra…` | `Global Human Resource Management explores the rapidly changing field of international human resource management (HRM) and examines a global perspective in relation to staffing, personnel management, s…` |
| D356 | HR Technology | 3 | 1/1 | 352 | 678 | 326 | BSHR | `Technology is transforming HR into a data-driven and strategic function. This course introduces you to human resource information systems, digital tools, and analytics that improve efficiency and guid…` | `HR Technology focuses on the usage of technology for strategic human resource management. The learner will develop competency in critical skills related to analyzing the value and application of the d…` |
| E011 | Technical Communication | 3 | 3/3 | 555 | 235 | 320 | MSITM | `Technical Communication teaches IT managers how to convey complex information clearly and effectively to diverse audiences, whether technical or nontechnical. The course covers skills in writing, pres…` | `This course covers basic elements of technical communication, including professional written communication proficiency; the ability to strategize approaches for communicating with technical and non-tec…` |
| D436 | Inclusive Workplace Culture Capstone | 3 | 1/1 | 387 | 706 | 319 | MSHRM | `Inclusive workplaces foster environments where people feel a sense of belonging and where diverse perspectives drive innovation. This capstone course helps you apply what you've learned throughout the…` | `The Inclusive Workplace Culture Capstone course is designed to be a comprehensive evaluation of the knowledge and skills accumulated throughout the Master of Science in Human Resource Management degr…` |
| AIT2 | Organic Chemistry | — | 1/2 | 260 | 562 | 302 | ENDSESC | `Organic Chemistry covers fundamental concepts of organic chemistry, including molecular structure, reactivity, and reaction mechanisms. Students explore topics such as nomenclature, stereochemistry, f…` | `Organic Chemistry covers fundamental and applied concepts of organic chemistry. The learner will develop competency in critical skills related to molecular structure, functional groups, and reaction me…` |
| C175 | Network and Security - Foundations | — | 2/3 | 594 | 296 | 298 | BSDA,BSSWE_C,BSSWE_Java | `Network and Security - Foundations introduces learners to the fundamentals of networking and security to…` | `Network and Security - Foundations introduces learners to the fundamentals of networking and security to prepare them for the CompTIA Network+ exam. This course covers…` |
| C175 | Network and Security - Foundations | — | 1/3 | 594 | 297 | 297 | BSCNE,BSCNEAWS,BSCNEAZR | `Network and Security - Foundations introduces learners to the fundamentals of networking and security to…` | `Network and Security - Foundations introduces learners to the fundamentals of networking and security to prepare them for the CompTIA Network+ exam. This course covers…` |
| C234 | Software Quality Assurance | — | 1/1 | 433 | 160 | 273 | BSITM | `Software Quality Assurance introduces you to the principles and practices essential for ensuring software reliability and functionality. The course covers testing methodologies, including unit, integra…` | `Software Quality Assurance introduces students to the principles and practices of software quality including software testing, debugging, and quality assurance methodologies.` |
| C172 | Network and Security - Design | — | 1/2 | 574 | 323 | 251 | BSCNE,BSCNEAWS,BSCNEAZR | `Network and Security - Design focuses on architecting and designing secure network solutions…` | `Network and Security - Design focuses on advanced network design, implementation and troubleshooting including routing and switching and network security.` |
| D435 | Inclusive Workplace Culture | 3 | 1/1 | 380 | 628 | 248 | MSHRM | `Inclusive organizations create workplaces where all employees can contribute their best work…` | `Inclusive Workplace Culture focuses on creating and sustaining inclusive work environments where all individuals can thrive. Students will develop competency in…` |
| D360 | Compensation and Benefits Design | 3 | 1/1 | 406 | 170 | 236 | BSHR | `Effective compensation and benefits strategies are essential for attracting, retaining, and motivating talent. This course explores how organizations design, implement, and evaluate pay structures, incen…` | `Compensation and Benefits Design introduces learners to concepts of designing and managing compensation and benefits packages.` |
| D235 | Care of Older Adults | 2 | 2/2 | 890 | 1110 | 220 | MSRNNUED,MSRNNULM,MSRNNUNI | `Care of Older Adults…` | `Care of Older Adults…` |
| C722 | Business of IT - Applications | 3 | 2/3 | 633 | 417 | 216 | MSDADPE,MSITM | `Business of IT - Applications focuses on applying IT management skills in professional settings…` | `Business of IT - Applications…` |
| E011 | Technical Communication | 3 | 1/3 | 555 | 357 | 198 | BSIT | `Technical Communication teaches IT managers how to convey complex information clearly…` | `Technical Communication introduces students to essential writing skills for the workplace, emphasizing…` |
| D082 | Intermediate Accounting II | — | 1/2 | 427 | 615 | 188 | BSACC,BSBAHC,BSC | `Intermediate Accounting II explores complex topics in financial accounting including equity, debt, leases, pensions…` | `Intermediate Accounting II examines complex topics in corporate financial reporting. Students will develop competency in analyzing stockholders' equity, earnings per share…` |
| D871 | Organic Chemistry: STEM Connections | 3 | 2/2 | 631 | 809 | 178 | MATSESC | `Organic Chemistry: STEM Connections…` | `Organic Chemistry: STEM Connections…` |
| D219 | Pathophysiology and Pharmacology for the RN-BSN | — | 1/1 | 610 | 444 | 166 | BSNU,BSPRN | `Pathophysiology and Pharmacology for the RN-BSN…` | `Pathophysiology and Pharmacology…` |
| C179 | Network and Security - Advanced Networking Concepts | — | 1/2 | 293 | 457 | 164 | BSCNE,BSCNEAWS,BSCNEAZR | `Network and Security - Advanced Networking Concepts…` | `Network and Security - Advanced Networking Concepts focuses on advanced networking including routing protocols, switching, and network automation…` |
| D352 | Corporate Finance | 3 | 1/1 | 367 | 525 | 158 | BSFIN,BSHR | `Corporate Finance examines financial management principles…` | `Corporate Finance provides students with a deep understanding of how firms make financial decisions…` |
| D441 | Women's Health | — | 1/1 | 307 | 455 | 148 | BSPRN | `Women's Health…` | `Women's Health covers the assessment, diagnosis, and management of common women's health conditions…` |
| D606 | Machine Learning | — | 1/1 | 754 | 606 | 148 | MSDADS | `Machine Learning…` | `Machine Learning…` |
| D432 | Strategic Human Resource Management | 3 | 1/1 | 411 | 552 | 141 | MSHRM | `Strategic HRM examines how HR strategy aligns with organizational goals…` | `Strategic Human Resource Management focuses on the strategic role of human resources in organizational success…` |
| D839 | Teaching and Learning in Secondary Schools | — | 2/2 | 874 | 738 | 136 | MATEES | `Teaching and Learning in Secondary Schools…` | `Teaching and Learning in Secondary Schools…` |
| D875 | Earth, Moon, and Space | — | 2/2 | 758 | 623 | 135 | MATSESB,MATSESC,MATSESE | `Earth, Moon, and Space…` | `Earth, Moon, and Space…` |
| D893 | Mathematics Methods | — | 2/2 | 743 | 874 | 131 | MAMES | `Mathematics Methods…` | `Mathematics Methods…` |
| C236 | Compensation and Benefits | 3 | 1/1 | 386 | 512 | 126 | BSBAHC,BSITM | `Compensation and benefits significantly influence how organizations attract, motivate, and retain talent. In this course, students will explore total rewards philosophy…` | `Compensation and Benefits develops competence in the design and implementation of compensation and benefits systems in a global work environment. Students will analyze…` |
| D440 | Prenatal and Newborn Health | — | 1/1 | 371 | 493 | 122 | BSPRN | `Prenatal and Newborn Health…` | `Prenatal and Newborn Health…` |
| C805 | Leadership Foundations | 3 | 3/3 | 414 | 527 | 113 | BSNU | `Leadership Foundations…` | `Leadership Foundations…` |
| D357 | Talent Acquisition | 3 | 1/1 | 436 | 325 | 111 | BSHR | `Talent Acquisition covers modern recruitment and hiring strategy…` | `Talent Acquisition focuses on strategies for attracting and selecting qualified candidates…` |
| C845 | Cybersecurity and Information Assurance Capstone | — | 1/1 | 1021 | 1131 | 110 | BSCSIA | `Cybersecurity Capstone…` | `Cybersecurity Capstone…` |
| D634 | Community Health | — | 1/1 | 783 | 674 | 109 | BSHS | `Community Health…` | `Community Health…` |
| D156 | Role of the Nurse Leader | 2 | 2/2 | 1202 | 1094 | 108 | MSRNNULM | `Role of the Nurse Leader…` | `Role of the Nurse Leader…` |
| D157 | Leadership and Management | — | 1/2 | 1133 | 1241 | 108 | MSNULM,PMCNULM | `Leadership and Management…` | `Leadership and Management…` |
| D224 | Concepts in Nursing Practice II | — | 1/1 | 679 | 571 | 108 | MSRNNUED,MSRNNULM,MSRNNUNI | `Concepts in Nursing Practice II…` | `Concepts in Nursing Practice II…` |
| D225 | Concepts in Nursing Practice III | — | 1/1 | 460 | 352 | 108 | MSRNNUED,MSRNNULM,MSRNNUNI | `Concepts in Nursing Practice III…` | `Concepts in Nursing Practice III…` |
| D218 | Health and Wellness Across the Lifespan | — | 1/1 | 393 | 496 | 103 | BSNU,BSPRN | `Health and Wellness…` | `Health and Wellness…` |
| D348 | Psychiatric Mental Health Care | — | 2/2 | 912 | 1014 | 102 | PMCNUPMHNP | `Psychiatric Mental Health Care…` | `Psychiatric Mental Health Care…` |
| C947 | Quality Improvement in Nursing Practice | — | 2/2 | 736 | 837 | 101 | MSRNNUED | `Quality Improvement…` | `Quality Improvement…` |
| D123 | Primary Care Nursing II | — | 2/2 | 1111 | 1014 | 97 | PMCNUFNP | `Primary Care Nursing II…` | `Primary Care Nursing II…` |
| D446 | Care of the Chronically Ill Adult | — | 1/1 | 801 | 896 | 95 | BSPRN | `Care of the Chronically Ill Adult…` | `Care of the Chronically Ill Adult…` |
| D269 | Health Assessment | 3 | 2/3 | 950 | 856 | 94 | BSNU | `Health Assessment…` | `Health Assessment…` |
| D425 | Human Growth and Development | 3 | 2/2 | 627 | 538 | 89 | BSPRN | `Human Growth and Development…` | `Human Growth and Development…` |
| D445 | Health Promotion and Disease Prevention | — | 1/1 | 686 | 774 | 88 | BSPRN | `Health Promotion and Disease Prevention…` | `Health Promotion and Disease Prevention…` |
| D857 | Earth Science | — | 2/2 | 1074 | 987 | 87 | MATSESE | `Earth Science…` | `Earth Science…` |
| D362 | Corporate Finance Analysis | 3 | 1/1 | 936 | 856 | 80 | BSFIN | `Corporate Finance Analysis…` | `Corporate Finance Analysis…` |
| D124 | Primary Care Nursing III | — | 2/2 | 965 | 1043 | 78 | PMCNUFNP | `Primary Care Nursing III…` | `Primary Care Nursing III…` |
| D354 | Human Resource Management | 3 | 1/2 | 476 | 553 | 77 | BSHR | `Human Resource Management covers core principles and practices of HRM…` | `Human Resource Management focuses on the competencies needed to manage human resources in the current global business environment…` |
| D269 | Health Assessment | 3 | 3/3 | 950 | 1026 | 76 | BSPRN,MSRNNUED,MSRNNULM | `Health Assessment…` | `Health Assessment…` |
| D118 | Adult Primary Care for the Advanced Practice Nurse | — | 1/1 | 805 | 880 | 75 | MSNUFNP,PMCNUFNP | `Adult Primary Care…` | `Adult Primary Care…` |
| D119 | Primary Care for the Advanced Practice Nurse II | — | 1/1 | 953 | 1028 | 75 | MSNUFNP,PMCNUFNP | `Primary Care NP II…` | `Primary Care NP II…` |
| D454 | Management of Health Conditions for RN-BSN | — | 1/1 | 882 | 956 | 74 | BSPRN | `Management of Health Conditions…` | `Management of Health Conditions…` |
| D255 | PPE I: Technical | — | 1/1 | 404 | 333 | 71 | BSHA,BSHIM | `The PPE I: Technical course allows you to use EHRGo, an electronic health record (EHR), to complete 42 structured activities that will help you gain experience with practical information management tas…` | `The PPE I: Technical course allows you to use EHRGo, an electronic health record (EHR), to complete 42 structured activities. The course's activities are tied to eight core competency areas of the hi…` |
| D554 | Advanced Financial Accounting I | 3 | 1/1 | 568 | 499 | 69 | MACCF,MACCT | `Internal Auditing I provides learners with the basic knowledge and skills necessary to succeed as an entry-level internal audit professional. The course introduces the fundamentals of internal auditin…` | `Internal Auditing I provides learners with the basic knowledge and skills necessary to succeed as an entry-level internal audit professional. The Institute of Internal Auditors defines internal auditing…` |
| D592 | Health Research Methods | 3 | 2/2 | 284 | 352 | 68 | MPH | `Health Research Methods…` | `Health Research Methods…` |
| C949 | Introduction to Programming in Python | 4 | 2/2 | 456 | 523 | 67 | BSDA | `Introduction to Programming in Python covers fundamental Python programming concepts including variables, data types, control structures, functions, and file handling. Students gain hands-on experience…` | `Introduction to Programming in Python introduces students to the fundamentals of programming using Python. Students develop competencies in Python syntax, data structures, and algorithms to solve probl…` |
| D089 | Advanced Accounting II | — | 1/2 | 926 | 861 | 65 | BSACC,BSBAHC,BSFIN | `Advanced Accounting II…` | `Advanced Accounting II…` |
| C805 | Leadership Foundations | 3 | 2/3 | 414 | 477 | 63 | BSHS | `Leadership Foundations…` | `Leadership Foundations…` |
| D122 | Advanced Pathophysiology | — | 2/2 | 1198 | 1135 | 63 | PMCNUFNP | `Advanced Pathophysiology…` | `Advanced Pathophysiology…` |
| D444 | Fundamentals of Nursing and Healthcare | — | 1/1 | 811 | 873 | 62 | BSPRN | `Fundamentals of Nursing and Healthcare…` | `Fundamentals of Nursing and Healthcare…` |
| D607 | Data Mining | — | 1/1 | 345 | 283 | 62 | MSDADE | `Data Mining…` | `Data Mining…` |
| D777 | Introduction to Software Engineering | 3 | 1/1 | 302 | 364 | 62 | MSSWEAIE,MSSWEDDD,MSSWEDOE | `Introduction to Software Engineering introduces key concepts…` | `Introduction to Software Engineering introduces students to the discipline of software engineering, covering…` |
| D433 | HR Analytics and Metrics | 3 | 1/1 | 448 | 389 | 59 | MSHRM | `HR Analytics and Metrics introduces data-driven approaches to human resource management…` | `HR Analytics and Metrics focuses on leveraging data to drive HR decision-making and strategy…` |
| C722 | Business of IT - Applications | 3 | 3/3 | 633 | 575 | 58 | MSITPM,MSITUG | `Business of IT - Applications…` | `Business of IT - Applications…` |
| D556 | Advanced Financial Accounting II | 3 | 1/1 | 489 | 431 | 58 | MACCF,MACCM | `Advanced Financial Accounting II…` | `Advanced Financial Accounting II…` |
| D594 | Environmental Health | 3 | 2/2 | 373 | 430 | 57 | MPH | `Environmental Health…` | `Environmental Health…` |
| D562 | Individual Taxation | 3 | 1/1 | 523 | 467 | 56 | MACCA | `Individual Taxation…` | `Individual Taxation…` |
| D907 | Healthcare Management | 3 | 1/1 | 484 | 428 | 56 | MHA | `Healthcare Management…` | `Healthcare Management…` |
| D912 | Health Informatics | — | 1/1 | 801 | 745 | 56 | MHA | `Health Informatics…` | `Health Informatics…` |
| D236 | Concepts in Nursing Practice | — | 1/1 | 527 | 477 | 50 | BSPRN,MSRNNUED,MSRNNULM | `Concepts in Nursing Practice…` | `Concepts in Nursing Practice…` |

### 5C-ii. MOD differences (diff 6–50) — 40 rows

| code | title | v | cat_len | guide_len | diff | source_programs | cat_text (160 chars) | guide_text (160 chars) |
|---|---|---|---|---|---|---|---|---|
| D028 | Org. Systems & Quality Leadership | 2/2 | 828 | 783 | 45 | MSRNNUED,MSRNNULM,MSRNNUNI | `Organizational Systems and Quality Leadership…` | `Organizational Systems and Quality Leadership…` |
| D351 | Financial Planning | 1/2 | 403 | 448 | 45 | BSC,BSFIN,BSHR | `Financial Planning…` | `Financial Planning…` |
| D604 | Deep Learning | 1/1 | 469 | 424 | 45 | MSDADS | `Deep Learning…` | `Deep Learning…` |
| C683 | Introduction to IT | 2/2 | 421 | 377 | 44 | BSCS,BSCSIA,BSDA | `Introduction to IT covers fundamental concepts…` | `Introduction to IT covers fundamental concepts…` |
| D030 | Advanced Clinical Nursing | 2/2 | 748 | 704 | 44 | MSRNNUED,MSRNNULM,MSRNNUNI | `Advanced Clinical Nursing…` | `Advanced Clinical Nursing…` |
| D567 | Psychopathology | 1/1 | 511 | 467 | 44 | BSPSY | `Psychopathology…` | `Psychopathology…` |
| D598 | Statistical Programming | 1/1 | 479 | 436 | 43 | MSDADE,MSDADPE,MSDADS | `Statistical Programming…` | `Statistical Programming…` |
| D175 | Consumer Behavior and Ethics | 3/3 | 663 | 705 | 42 | BSPSY | `Consumer Behavior and Ethics…` | `Consumer Behavior and Ethics…` |
| D359 | Workforce Planning and Employment Law | 1/1 | 414 | 456 | 42 | BSHR | `Workforce Planning and Employment Law covers key aspects of strategic workforce management…` | `Workforce Planning and Employment Law examines organizational workforce planning, including labor relations, employment law…` |
| D601 | Natural Language Processing | 1/1 | 469 | 427 | 42 | MSDADE,MSDADPE,MSDADS | `Natural Language Processing…` | `Natural Language Processing…` |
| D555 | Taxation of Individuals | 3 | 1/1 | 555 | 518 | 37 | MACCF,MACCT | `Taxation of Individuals…` | `Taxation of Individuals…` |
| D752 | Clinical Experiences | 2 | 2/2 | 729 | 692 | 37 | MATELED | `Clinical Experiences…` | `Clinical Experiences…` |
| D782 | Software Engineering | 3 | 2/2 | 987 | 1020 | 33 | MSSWEAIE,MSSWEDDD,MSSWEDOE | `Software Engineering…` | `Software Engineering…` |
| D783 | DevOps Engineering | 1/1 | 501 | 533 | 32 | MSSWEDOE | `DevOps Engineering…` | `DevOps Engineering…` |
| D389 | Perspectives in Diversity | 1/2 | 773 | 742 | 31 | BSHHS,BSHS,BSPH | `Perspectives in Diversity…` | `Perspectives in Diversity…` |
| D778 | Introduction to AI | 1/2 | 507 | 535 | 28 | MSSWEAIE,MSSWEDDD,MSSWEDOE | `Introduction to AI…` | `Introduction to AI…` |
| D786 | Domain Driven Design | 1/1 | 467 | 495 | 28 | MSSWEDDD | `Domain Driven Design…` | `Domain Driven Design…` |
| D788 | Modern Software Architecture | 1/1 | 380 | 408 | 28 | MSSWEDDD | `Modern Software Architecture…` | `Modern Software Architecture…` |
| D608 | Visualization and Storytelling | 1/1 | 594 | 567 | 27 | MSDADE | `Visualization and Storytelling…` | `Visualization and Storytelling…` |
| C947 | Quality Improvement | 1/2 | 736 | 761 | 25 | MSNUED,PMCNUED | `Quality Improvement in Nursing…` | `Quality Improvement in Nursing…` |
| D337 | Cloud Networking | 1/1 | 423 | 398 | 25 | BSCNE,BSCNEAWS,BSCNEAZR | `Cloud Networking…` | `Cloud Networking…` |
| D781 | SE Foundations | 1/2 | 689 | 712 | 23 | MSSWEAIE,MSSWEDDD,MSSWEDOE | `SE Foundations…` | `SE Foundations…` |
| C483 | Intermediate Accounting I | 2/2 | 608 | 629 | 21 | BSBAHC | `Intermediate Accounting I…` | `Intermediate Accounting I…` |
| D434 | Employee Relations | 1/1 | 433 | 413 | 20 | MSHRM | `Employee Relations…` | `Employee Relations…` |
| D221 | Concepts in Nursing Practice I | 1/1 | 632 | 651 | 19 | BSNU,BSPRN | `Concepts in Nursing Practice I…` | `Concepts in Nursing Practice I…` |
| D353 | Accounting Applications | 1/2 | 355 | 340 | 15 | BSHA,BSHR | `Accounting Applications…` | `Accounting Applications…` |
| D453 | Pediatric Nursing | 1/1 | 651 | 666 | 15 | BSPRN | `Pediatric Nursing…` | `Pediatric Nursing…` |
| D447 | Medical Surgical Nursing | 1/1 | 925 | 939 | 14 | BSPRN | `Medical Surgical Nursing…` | `Medical Surgical Nursing…` |
| D914 | Healthcare Finance | 1/1 | 471 | 485 | 14 | MHA | `Healthcare Finance…` | `Healthcare Finance…` |
| D439 | Chronic Care Management | 1/1 | 629 | 616 | 13 | BSPRN | `Chronic Care Management…` | `Chronic Care Management…` |
| D602 | Applied Statistics | 1/1 | 483 | 471 | 12 | MSDADE,MSDADPE,MSDADS | `Applied Statistics…` | `Applied Statistics…` |
| D198 | Health Information Management | 2/2 | 665 | 654 | 11 | MSRNNUED,MSRNNULM,MSRNNUNI | `Health Information Management…` | `Health Information Management…` |
| D570 | Research Methods | 1/1 | 486 | 475 | 11 | BSHS,BSPSY | `Research Methods…` | `Research Methods…` |
| D801 | Machine Learning for AI | 1/1 | 903 | 892 | 11 | MSCSAIML | `Machine Learning for AI…` | `Machine Learning for AI…` |
| D495 | Data Analytics | 1/1 | 706 | 697 | 9 | BSDA | `Data Analytics…` | `Data Analytics…` |
| C190 | Introduction to Biology | 2/2 | 498 | 506 | 8 | MASEMG,MASESB | `Introduction to Biology…` | `Introduction to Biology…` |
| C952 | Operating Systems and Architecture | 1/1 | 265 | 273 | 8 | BSCS,MSCSUG | `Operating Systems and Architecture…` | `Operating Systems and Architecture…` |
| D581 | Biological Psychology | 1/2 | 661 | 653 | 8 | BSHS,BSPSY | `Biological Psychology…` | `Biological Psychology…` |
| D029 | Foundations of Nursing Practice | 2/2 | 910 | 904 | 6 | MSRNNUED,MSRNNULM,MSRNNUNI | `Foundations of Nursing Practice…` | `Foundations of Nursing Practice…` |

---

## 6. Suggested Sample Set for Later LLM Review

The following groups are proposed for the LLM comparison pass. Goal: cover the main patterns in the 109 mat-diff rows with a manageable set of 15–20 pairs.

### A. Clear rewrites (catalog is a new short-form; guide is older long-form)
These represent a whole-course catalog text rewrite where the guide version is still the old text. Highest policy priority — the two sources describe the same course but at different points in authoring history.

| Code | Diff | Pattern |
|---|---|---|
| D358 | 483 | Guide is ~2× longer; catalog is newer, shorter summary |
| D356 | 326 | Same pattern; BSHR course family |
| D360 | 236 | Same — catalog is shorter new version |
| D357 | 111 | Same |
| D354 | 77 | Same |
| D359 | 42 | Borderline — different phrase framing |

### B. Course-level meaningful variant (same course, different programs use different guide text)
These have multiple guide variants; one variant matches catalog while another doesn't.

| Code | Diff | Pattern |
|---|---|---|
| C175 | 297/298 | 3 guide variants; catalog is longer version; variants v1/v2 are shorter |
| C172 | 251 | 2 variants; significant framing difference between variants |
| C179 | 164 | 2 variants; one more detailed than catalog |
| E011 | 198/320 | 3 variants; v1 (BSIT) and v3 (MSITM) are both meaningfully different from catalog |

### C. Genuine content difference (not a rewrite, but different emphasis or detail)
Both sources have comparable length but different content framing.

| Code | Diff | Pattern |
|---|---|---|
| D560 | 492 | Catalog adds significantly more body content after same opening sentence |
| D436 | 319 | Capstone: catalog is outcome-framing; guide is competency-framing |
| D435 | 248 | Non-capstone companion to D436; same pattern |
| D432 | 141 | MSHRM course — different framing across all D43x courses |
| C236 | 126 | Compensation and Benefits — different structure despite same topic |

### D. Multi-variant: meaningful within-guide difference
Courses where guide variants v1 and v2 are themselves different (not just catalog vs guide).

| Code | Diff | Pattern |
|---|---|---|
| C169 | (not in cat overlap but known 3-variant case) | C++/Python meaningful split — in guide-only category |
| C722 | 216 (v2) + 58 (v3) | Three-way split; two variants differ from catalog by 58 and 216 chars |
| D269 | 94 (v2) + 76 (v3) | Health Assessment: three different source program groups |

### E. Near-identical review (borderline cases)
| Code | Diff | Pattern |
|---|---|---|
| D355 | 4 (near-dup) | "key aspects of building" vs "strategies for building" — may be a real rewrite |
| C949 | 67 (STRONG) | Python intro: catalog vs BSDA guide — two different paragraphs, same topic |
| D255 | 71 | PPE I: both describe the same EHRGo course but emphasize different aspects |
