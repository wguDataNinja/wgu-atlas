# Course Text Comparison — Batch 1 of 4

**Source artifact:** `_internal/atlas_qa/COURSE_TEXT_COMPARISON_INDEX.md`
**Batch scope:** §5A exact match reference (447 courses) + §5B near-duplicate pairs (59 rows, diff ≤ 5)
**Batching rule:** Rows appear in the same order as the source artifact. Batch 1 = all exact and near-duplicate rows. Batches 2–4 cover materially different rows only.
**Annotation status:** Complete — all `llm_*` fields annotated.

---

## §5A — Exact Match Reference (447 courses, no individual annotation required)

All 447 courses below have `cat_text == guide_text` for their first (or only) guide description variant. No display authority decision needed — either source produces the same text. A course appearing here may also appear in §5B or §5C for a different guide variant; those variants are annotated individually below.

<details>
<summary>Exact-match course codes (447 courses)</summary>

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

**Bulk annotation for all §5A courses:**
- `llm_difference_summary:` N/A — exact match; both sources identical
- `llm_preference_for_research_tool:` either
- `llm_preference_reason:` No authority decision required; texts are identical
- `llm_notable_observations:`
- `llm_review_flag:` no

---

## §5B — Near-Duplicate Pairs (59 rows, diff ≤ 5)

Note: rows with diff=0 within this section are second variants of multi-variant courses where the second variant happens to be exact. They are included here because the course has at least one non-exact variant elsewhere.

---

### 1. AUA2 — Auditing
- **type:** near-dup | **v:** 1/1 | **cat_len:** 377 | **guide_len:** 376 | **diff:** 1
- **source_programs:** MAMEK6
- **cat_text:** "Auditing covers the conduct of financial audits and the evaluation of internal controls…"
- **guide_text:** "Auditing covers the conduct of financial audits and the evaluation of internal controls…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the texts read the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither version is meaningfully better for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 2. C121 — Spreadsheets
- **type:** near-dup | **v:** 1/1 | **cat_len:** 239 | **guide_len:** 238 | **diff:** 1
- **source_programs:** BSBAHC, BSITM
- **cat_text:** "Spreadsheets is a project-based course that…"
- **guide_text:** "Spreadsheets is a project-based course that…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the texts are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions provide the same student-facing value.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 3. C165 — (variant 2/2)
- **type:** near-dup | **v:** 2/2 | **cat_len:** 339 | **guide_len:** 342 | **diff:** 3
- **source_programs:** MASEMG, MASESC, MASESP
- **cat_text:** "…focuses on scientific reasoning and practical, everyday applications…"
- **guide_text:** "…focuses on scientific reasoning and practical and everyday applications…"

> **Annotation**
> - `llm_difference_summary:` The catalog uses the clearer phrase "practical, everyday applications," while the guide adds an awkward extra "and."
> - `llm_preference_for_research_tool:` catalog
> - `llm_preference_reason:` The catalog wording is smoother and easier for students to read.
> - `llm_notable_observations:` Minor guide phrasing issue.
> - `llm_review_flag:` no

---

### 4. C200 — Managing in Social Context (variant 1/2)
- **type:** near-dup | **v:** 1/2 | **cat_len:** 338 | **guide_len:** 337 | **diff:** 1
- **source_programs:** MBA, MBAITM, MSMK
- **cat_text:** "Managing in Social Context examines the environment of business…"
- **guide_text:** "Managing in Social Context examines the environment of business…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the texts read the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful difference for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 5. C209 — Advanced Accounting Concepts and Applications
- **type:** near-dup | **v:** 1/1 | **cat_len:** 210 | **guide_len:** 208 | **diff:** 2
- **source_programs:** MACC, MSML
- **cat_text:** "Advanced Accounting Concepts and Applications examines complex accounting topics…"
- **guide_text:** "Advanced Accounting Concepts and Applications examines complex accounting topics…" *(minor spacing diff)*

> **Annotation**
> - `llm_difference_summary:` The only difference appears to be minor spacing, with no change in meaning.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally useful to students.
> - `llm_notable_observations:` Spacing only.
> - `llm_review_flag:` no

---

### 6. C278 — Earth Science: Earth's Composition (variant 2/2)
- **type:** near-dup | **v:** 2/2 | **cat_len:** 355 | **guide_len:** 354 | **diff:** 1
- **source_programs:** MAMEMG
- **cat_text:** "Earth Science: Earth's Composition…"
- **guide_text:** "Earth Science: Earth's Composition…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither source is meaningfully better.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 7. C720 — Auditing I (variant 2/2)
- **type:** near-dup | **v:** 2/2 | **cat_len:** 807 | **guide_len:** 811 | **diff:** 4
- **source_programs:** BSBAHC, BSFIN
- **cat_text:** "Auditing I introduces students to the audit process…"
- **guide_text:** "Auditing I introduces students to the audit process…" *(minor punctuation/spacing diff)*

> **Annotation**
> - `llm_difference_summary:` The texts differ only in minor punctuation or spacing and appear substantively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions should read the same to students.
> - `llm_notable_observations:` Formatting-level difference.
> - `llm_review_flag:` no

---

### 8. C971 — Cloud Foundations
- **type:** near-dup | **v:** 1/1 | **cat_len:** 769 | **guide_len:** 768 | **diff:** 1
- **source_programs:** BSSWE_C
- **cat_text:** "Cloud Foundations introduces cloud computing…"
- **guide_text:** "Cloud Foundations introduces cloud computing…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful student-facing difference.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 9. D028 — Organizational Systems and Quality Leadership (variant 1/2)
- **type:** near-dup | **v:** 1/2 | **cat_len:** 828 | **guide_len:** 827 | **diff:** 1
- **source_programs:** MSNUED, MSNULM, MSNUNI
- **cat_text:** "Organizational Systems and Quality Leadership…"
- **guide_text:** "Organizational Systems and Quality Leadership…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text is effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions offer the same information to students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 10. D029 — Foundations of Nursing Practice (variant 1/2)
- **type:** near-dup | **v:** 1/2 | **cat_len:** 910 | **guide_len:** 908 | **diff:** 2
- **source_programs:** MSNUED, MSNUFNP, MSNULM
- **cat_text:** "Foundations of Nursing Practice…"
- **guide_text:** "Foundations of Nursing Practice…" *(minor spacing diff)*

> **Annotation**
> - `llm_difference_summary:` The difference appears to be minor spacing, with no meaningful content change.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally useful for students.
> - `llm_notable_observations:` Spacing only.
> - `llm_review_flag:` no

---

### 11. D122 — Advanced Pathophysiology (variant 1/2)
- **type:** near-dup | **v:** 1/2 | **cat_len:** 1198 | **guide_len:** 1197 | **diff:** 1
- **source_programs:** MSNUFNP
- **cat_text:** "Advanced Pathophysiology…"
- **guide_text:** "Advanced Pathophysiology…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither source is meaningfully better.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 12. D124 — Advanced Health Assessment (variant 1/2)
- **type:** near-dup | **v:** 1/2 | **cat_len:** 965 | **guide_len:** 964 | **diff:** 1
- **source_programs:** MSNUFNP
- **cat_text:** "Advanced Health Assessment…"
- **guide_text:** "Advanced Health Assessment…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text reads the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions provide the same value to students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 13. D155 — Leadership and Management in Nursing
- **type:** near-dup | **v:** 1/1 | **cat_len:** 893 | **guide_len:** 892 | **diff:** 1
- **source_programs:** MSNULM, MSRNNULM, PMCNULM
- **cat_text:** "Leadership and Management in Nursing…"
- **guide_text:** "Leadership and Management in Nursing…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful difference for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 14. D175 — Consumer Behavior and Ethics (variant 2/3)
- **type:** near-dup | **v:** 2/3 | **cat_len:** 663 | **guide_len:** 662 | **diff:** 1
- **source_programs:** BSMKT
- **cat_text:** "Consumer Behavior and Ethics…"
- **guide_text:** "Consumer Behavior and Ethics…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text is effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally suitable for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 15. D178 — Digital Marketing
- **type:** near-dup | **v:** 1/1 | **cat_len:** 801 | **guide_len:** 800 | **diff:** 1
- **source_programs:** BSMKT
- **cat_text:** "Digital Marketing…"
- **guide_text:** "Digital Marketing…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither source has a clear advantage for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 16. D181 — Curriculum Design and Instruction
- **type:** near-dup | **v:** 1/1 | **cat_len:** 832 | **guide_len:** 831 | **diff:** 1
- **source_programs:** MSCIN
- **cat_text:** "Curriculum Design and Instruction…"
- **guide_text:** "Curriculum Design and Instruction…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text reads the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally useful to students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 17. D296 — Instructional Design Theory
- **type:** near-dup | **v:** 1/1 | **cat_len:** 1116 | **guide_len:** 1115 | **diff:** 1
- **source_programs:** MEDETID
- **cat_text:** "Instructional Design Theory…"
- **guide_text:** "Instructional Design Theory…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful difference for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 18. D297 — Instructional Media
- **type:** near-dup | **v:** 1/1 | **cat_len:** 788 | **guide_len:** 787 | **diff:** 1
- **source_programs:** MEDETID
- **cat_text:** "Instructional Media…"
- **guide_text:** "Instructional Media…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text is effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions provide the same student-facing value.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 19. D312 — Health, Fitness, and Wellness (variant 1/2)
- **type:** near-dup | **v:** 1/2 | **cat_len:** 688 | **guide_len:** 687 | **diff:** 1
- **source_programs:** BSHS, BSNU, BSPRN
- **cat_text:** "Health, Fitness, and Wellness…"
- **guide_text:** "Health, Fitness, and Wellness…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither source is meaningfully better.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 20. D312 — Health, Fitness, and Wellness (variant 2/2)
- **type:** near-dup (diff=0, second variant exact) | **v:** 2/2 | **cat_len:** 688 | **guide_len:** 688 | **diff:** 0
- **source_programs:** MSRNNUED, MSRNNULM, MSRNNUNI
- **cat_text:** "Health, Fitness, and Wellness…"
- **guide_text:** "Health, Fitness, and Wellness…" *(exact match for this variant)*

> **Annotation**
> - `llm_difference_summary:` N/A — exact match; both sources are identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` No choice is needed because the text is the same.
> - `llm_notable_observations:`
> - `llm_review_flag:` no

---

### 21. D348 — Psychopharmacology (variant 1/2)
- **type:** near-dup | **v:** 1/2 | **cat_len:** 912 | **guide_len:** 911 | **diff:** 1
- **source_programs:** MSNUPMHNP
- **cat_text:** "Psychopharmacology…"
- **guide_text:** "Psychopharmacology…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text reads the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally suitable for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 22. D355 — Compensation and Benefits ⚑ borderline
- **type:** near-dup | **v:** 1/1 | **cat_len:** 457 | **guide_len:** 461 | **diff:** 4
- **source_programs:** BSHR
- **cat_text:** "Compensation and Benefits examines key aspects of building a total compensation…"
- **guide_text:** "Compensation and Benefits examines strategies for building total compensation systems…"
- **note:** Different verb phrase — "key aspects of building" vs "strategies for building total compensation systems." May be a real minor rewrite despite small char diff.

> **Annotation**
> - `llm_difference_summary:` The guide frames the course around "strategies" and "systems," while the catalog uses broader wording about key aspects.
> - `llm_preference_for_research_tool:` needs_review
> - `llm_preference_reason:` Both are plausible, but the framing difference is substantive enough that the better student-facing choice is not obvious.
> - `llm_notable_observations:` Guide sounds slightly more specific.
> - `llm_review_flag:` yes

---

### 23. D372 — Data Systems Administration
- **type:** near-dup | **v:** 1/1 | **cat_len:** 888 | **guide_len:** 887 | **diff:** 1
- **source_programs:** BSDA, BSSWE_C, BSSWE_Java
- **cat_text:** "Data Systems Administration…"
- **guide_text:** "Data Systems Administration…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful difference for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 24. D376 — Marketing Research
- **type:** near-dup | **v:** 1/1 | **cat_len:** 643 | **guide_len:** 642 | **diff:** 1
- **source_programs:** MSMK, MSMKA
- **cat_text:** "Marketing Research…"
- **guide_text:** "Marketing Research…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text reads the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally useful.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 25. D384 — Marketing Strategy
- **type:** near-dup | **v:** 1/1 | **cat_len:** 876 | **guide_len:** 875 | **diff:** 1
- **source_programs:** MSMK, MSMKA
- **cat_text:** "Marketing Strategy…"
- **guide_text:** "Marketing Strategy…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither source has a meaningful advantage.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 26. D386 — Data Wrangling
- **type:** near-dup | **v:** 1/1 | **cat_len:** 409 | **guide_len:** 408 | **diff:** 1
- **source_programs:** BSDA, BSSWE_C, BSSWE_Java
- **cat_text:** "Data Wrangling…"
- **guide_text:** "Data Wrangling…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text is effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions offer the same student-facing value.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 27. D387 — Algorithm Design and Analysis (variant 1/2)
- **type:** near-dup | **v:** 1/2 | **cat_len:** 405 | **guide_len:** 404 | **diff:** 1
- **source_programs:** BSCS
- **cat_text:** "Algorithm Design and Analysis…"
- **guide_text:** "Algorithm Design and Analysis…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful difference for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 28. D401 — Healthcare Quality
- **type:** near-dup | **v:** 1/1 | **cat_len:** 650 | **guide_len:** 649 | **diff:** 1
- **source_programs:** BSHHS, BSHS, BSPH
- **cat_text:** "Healthcare Quality…"
- **guide_text:** "Healthcare Quality…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text reads the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally suitable for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 29. D426 — Data Management - Foundations (variant 1/2)
- **type:** near-dup | **v:** 1/2 | **cat_len:** 297 | **guide_len:** 296 | **diff:** 1
- **source_programs:** BSCS, BSCSIA
- **cat_text:** "Data Management - Foundations offers an introduction in creating conceptual, logical and physical data models. Students gain skills in creating databases…"
- **guide_text:** "Data Management - Foundations offers an introduction in creating conceptual, logical and physical data models. Students gain skills in creating databases…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither version is meaningfully better for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 30. D467 — Supply Chain Management
- **type:** near-dup | **v:** 1/1 | **cat_len:** 523 | **guide_len:** 522 | **diff:** 1
- **source_programs:** BSSCOM
- **cat_text:** "Supply Chain Management…"
- **guide_text:** "Supply Chain Management…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text is effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions provide the same information to students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 31. D480 — Software Engineering
- **type:** near-dup | **v:** 1/1 | **cat_len:** 759 | **guide_len:** 758 | **diff:** 1
- **source_programs:** BSCS, BSSWE_C, BSSWE_Java
- **cat_text:** "Software Engineering…"
- **guide_text:** "Software Engineering…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful student-facing difference.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 32. D492 — Digital Forensics
- **type:** near-dup | **v:** 1/1 | **cat_len:** 305 | **guide_len:** 303 | **diff:** 2
- **source_programs:** BSCSIA, BSDA
- **cat_text:** "Digital Forensics…"
- **guide_text:** "Digital Forensics…" *(minor spacing diff)*

> **Annotation**
> - `llm_difference_summary:` The only difference appears to be minor spacing, with no content change.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally useful for students.
> - `llm_notable_observations:` Spacing only.
> - `llm_review_flag:` no

---

### 33. D545 — Healthcare Economics
- **type:** near-dup | **v:** 1/1 | **cat_len:** 490 | **guide_len:** 489 | **diff:** 1
- **source_programs:** BSHA
- **cat_text:** "Healthcare Economics…"
- **guide_text:** "Healthcare Economics…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text reads the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither source is meaningfully better for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 34. D553 — Cost Accounting
- **type:** near-dup | **v:** 1/1 | **cat_len:** 848 | **guide_len:** 844 | **diff:** 4
- **source_programs:** MACCA, MACCF, MACCM
- **cat_text:** "Cost Accounting…"
- **guide_text:** "Cost Accounting…" *(minor punctuation or spacing variation)*

> **Annotation**
> - `llm_difference_summary:` The texts appear to differ only by punctuation or spacing, not by substance.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions should be equally clear to students.
> - `llm_notable_observations:` Formatting-level difference.
> - `llm_review_flag:` no

---

### 35. D557 — Taxation of Business Entities
- **type:** near-dup | **v:** 1/1 | **cat_len:** 595 | **guide_len:** 594 | **diff:** 1
- **source_programs:** MACCT
- **cat_text:** "Taxation of Business Entities…"
- **guide_text:** "Taxation of Business Entities…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful difference for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 36. D566 — Psychotherapy and Counseling
- **type:** near-dup | **v:** 1/1 | **cat_len:** 703 | **guide_len:** 698 | **diff:** 5
- **source_programs:** BSPSY
- **cat_text:** "Psychotherapy and Counseling…"
- **guide_text:** "Psychotherapy and Counseling…" *(minor variation)*

> **Annotation**
> - `llm_difference_summary:` The variation appears minor and does not suggest a meaningful difference in scope or usefulness.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither version appears clearly better for students.
> - `llm_notable_observations:` Small wording difference only.
> - `llm_review_flag:` no

---

### 37. D569 — Child and Adolescent Psychology
- **type:** near-dup | **v:** 1/1 | **cat_len:** 468 | **guide_len:** 465 | **diff:** 3
- **source_programs:** BSPSY
- **cat_text:** "Child and Adolescent Psychology…"
- **guide_text:** "Child and Adolescent Psychology…" *(minor variation)*

> **Annotation**
> - `llm_difference_summary:` The variation appears minor and does not change the course description in a meaningful way.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions seem equally useful for students.
> - `llm_notable_observations:` Small wording difference only.
> - `llm_review_flag:` no

---

### 38. D577 — Mental Health Concepts
- **type:** near-dup | **v:** 1/1 | **cat_len:** 520 | **guide_len:** 518 | **diff:** 2
- **source_programs:** BSHHS, BSPH, BSPSY
- **cat_text:** "Mental Health Concepts…"
- **guide_text:** "Mental Health Concepts…" *(minor spacing diff)*

> **Annotation**
> - `llm_difference_summary:` The only difference appears to be minor spacing, with no change in meaning.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally clear for students.
> - `llm_notable_observations:` Spacing only.
> - `llm_review_flag:` no

---

### 39. D578 — Cognitive Psychology
- **type:** near-dup | **v:** 1/1 | **cat_len:** 619 | **guide_len:** 617 | **diff:** 2
- **source_programs:** BSPSY
- **cat_text:** "Cognitive Psychology…"
- **guide_text:** "Cognitive Psychology…" *(minor spacing diff)*

> **Annotation**
> - `llm_difference_summary:` The only difference appears to be minor spacing, not content.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions provide the same student-facing information.
> - `llm_notable_observations:` Spacing only.
> - `llm_review_flag:` no

---

### 40. D583 — (variant 2/2, exact)
- **type:** near-dup (diff=0, second variant exact) | **v:** 2/2 | **cat_len:** 632 | **guide_len:** 632 | **diff:** 0
- **source_programs:** BSHS
- **cat_text:** *(exact match for this variant)*
- **guide_text:** *(exact match for this variant)*

> **Annotation**
> - `llm_difference_summary:` N/A — exact match; both sources are identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` No authority decision is needed because the text is the same.
> - `llm_notable_observations:`
> - `llm_review_flag:` no

---

### 41. D588 — Community and Population Health
- **type:** near-dup | **v:** 1/1 | **cat_len:** 1069 | **guide_len:** 1068 | **diff:** 1
- **source_programs:** BSPH
- **cat_text:** "Community and Population Health…"
- **guide_text:** "Community and Population Health…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text is effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful difference for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 42. D597 — Data Analysis
- **type:** near-dup | **v:** 1/1 | **cat_len:** 589 | **guide_len:** 591 | **diff:** 2
- **source_programs:** MSDADE, MSDADPE, MSDADS
- **cat_text:** "Data Analysis…"
- **guide_text:** "Data Analysis…" *(minor spacing diff)*

> **Annotation**
> - `llm_difference_summary:` The only difference appears to be minor spacing, with no meaningful content change.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally useful to students.
> - `llm_notable_observations:` Spacing only.
> - `llm_review_flag:` no

---

### 43. D600 — Big Data
- **type:** near-dup | **v:** 1/1 | **cat_len:** 622 | **guide_len:** 619 | **diff:** 3
- **source_programs:** MSDADE, MSDADPE, MSDADS
- **cat_text:** "Big Data…"
- **guide_text:** "Big Data…" *(minor variation)*

> **Annotation**
> - `llm_difference_summary:` The variation appears minor and does not clearly change the meaning or usefulness of the description.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither version appears clearly better for students.
> - `llm_notable_observations:` Small wording difference only.
> - `llm_review_flag:` no

---

### 44. D626 — Epidemiology
- **type:** near-dup | **v:** 1/1 | **cat_len:** 544 | **guide_len:** 543 | **diff:** 1
- **source_programs:** MPH
- **cat_text:** "Epidemiology…"
- **guide_text:** "Epidemiology…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions provide the same value to students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 45. D635 — Secondary Clinical Experiences (variant 2/2)
- **type:** near-dup | **v:** 2/2 | **cat_len:** 993 | **guide_len:** 989 | **diff:** 4
- **source_programs:** MATELED
- **cat_text:** "Secondary Clinical Experiences…"
- **guide_text:** "Secondary Clinical Experiences…" *(minor punctuation or spacing variation)*

> **Annotation**
> - `llm_difference_summary:` The texts appear to differ only by punctuation or spacing and not by substance.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions should be equally clear to students.
> - `llm_notable_observations:` Formatting-level difference.
> - `llm_review_flag:` no

---

### 46. D668 — (variant 2/2, exact)
- **type:** near-dup (diff=0, second variant exact) | **v:** 2/2 | **cat_len:** 894 | **guide_len:** 894 | **diff:** 0
- **source_programs:** MATSPED
- **cat_text:** *(exact match for this variant)*
- **guide_text:** *(exact match for this variant)*

> **Annotation**
> - `llm_difference_summary:` N/A — exact match; both sources are identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` No choice is needed because the text is the same.
> - `llm_notable_observations:`
> - `llm_review_flag:` no

---

### 47. D673 — Student Teaching: Elementary Education (variant 2/2)
- **type:** near-dup | **v:** 2/2 | **cat_len:** 837 | **guide_len:** 836 | **diff:** 1
- **source_programs:** MATELED
- **cat_text:** "Student Teaching: Elementary Education…"
- **guide_text:** "Student Teaching: Elementary Education…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text reads the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally suitable for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 48. D757 — Assessment in Special Education (variant 2/2)
- **type:** near-dup | **v:** 2/2 | **cat_len:** 499 | **guide_len:** 498 | **diff:** 1
- **source_programs:** MATSPED
- **cat_text:** "Assessment in Special Education…"
- **guide_text:** "Assessment in Special Education…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful difference for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 49. D769 — Science Methods
- **type:** near-dup | **v:** 1/1 | **cat_len:** 657 | **guide_len:** 656 | **diff:** 1
- **source_programs:** BAESMES, BAESSESB, BAESSESC
- **cat_text:** "Science Methods…"
- **guide_text:** "Science Methods…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text is effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions provide the same student-facing value.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 50. D785 — (exact)
- **type:** near-dup (diff=0, exact) | **v:** 1/1 | **cat_len:** 756 | **guide_len:** 756 | **diff:** 0
- **source_programs:** MSSWEDOE
- **cat_text:** *(exact match)*
- **guide_text:** *(exact match)*

> **Annotation**
> - `llm_difference_summary:` N/A — exact match; both sources are identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` No authority decision is needed because the text is the same.
> - `llm_notable_observations:`
> - `llm_review_flag:` no

---

### 51. D804 — Foundations of AI
- **type:** near-dup | **v:** 1/1 | **cat_len:** 716 | **guide_len:** 715 | **diff:** 1
- **source_programs:** MSCSAIML
- **cat_text:** "Foundations of AI…"
- **guide_text:** "Foundations of AI…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither version is meaningfully better for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 52. D836 — Social Studies Methods
- **type:** near-dup | **v:** 1/1 | **cat_len:** 729 | **guide_len:** 728 | **diff:** 1
- **source_programs:** MATSSES
- **cat_text:** "Social Studies Methods…"
- **guide_text:** "Social Studies Methods…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text reads the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally useful to students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 53. D837 — Classroom Management
- **type:** near-dup | **v:** 1/1 | **cat_len:** 513 | **guide_len:** 517 | **diff:** 4
- **source_programs:** MATSSES
- **cat_text:** "Classroom Management…"
- **guide_text:** "Classroom Management…" *(minor variation)*

> **Annotation**
> - `llm_difference_summary:` The variation appears minor and does not clearly change the meaning or usefulness of the description.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither version appears clearly better for students.
> - `llm_notable_observations:` Small wording difference only.
> - `llm_review_flag:` no

---

### 54. D864 — Physics (variant 1/2)
- **type:** near-dup | **v:** 1/2 | **cat_len:** 708 | **guide_len:** 707 | **diff:** 1
- **source_programs:** BAESSESP, BSSESP, ENDSESP
- **cat_text:** "Physics…"
- **guide_text:** "Physics…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful difference for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 55. D864 — Physics (variant 2/2)
- **type:** near-dup | **v:** 2/2 | **cat_len:** 708 | **guide_len:** 710 | **diff:** 2
- **source_programs:** MATSESP
- **cat_text:** "Physics…"
- **guide_text:** "Physics…" *(minor spacing diff)*

> **Annotation**
> - `llm_difference_summary:` The only difference appears to be minor spacing, with no change in meaning.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally suitable for students.
> - `llm_notable_observations:` Spacing only.
> - `llm_review_flag:` no

---

### 56. D867 — Chemistry
- **type:** near-dup | **v:** 1/1 | **cat_len:** 563 | **guide_len:** 562 | **diff:** 1
- **source_programs:** BAESSESC, BSSESC
- **cat_text:** "Chemistry…"
- **guide_text:** "Chemistry…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text is effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions provide the same value to students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 57. D879 — Biology
- **type:** near-dup | **v:** 1/1 | **cat_len:** 420 | **guide_len:** 419 | **diff:** 1
- **source_programs:** BAESSESB, BSSESB, ENDSESB
- **cat_text:** "Biology…"
- **guide_text:** "Biology…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively identical.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Neither source has a meaningful advantage for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 58. D901 — Algebra
- **type:** near-dup | **v:** 1/1 | **cat_len:** 902 | **guide_len:** 901 | **diff:** 1
- **source_programs:** BAESMES, BSMES, MATMES
- **cat_text:** "Algebra…"
- **guide_text:** "Algebra…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the text reads the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` Both versions are equally useful to students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no

---

### 59. PFIT — Fitness and Health
- **type:** near-dup | **v:** 1/1 | **cat_len:** 331 | **guide_len:** 332 | **diff:** 1
- **source_programs:** BSITM
- **cat_text:** "Fitness and Health…"
- **guide_text:** "Fitness and Health…" *(trailing char diff only)*

> **Annotation**
> - `llm_difference_summary:` Only a trivial trailing-character difference; the descriptions are effectively the same.
> - `llm_preference_for_research_tool:` either
> - `llm_preference_reason:` There is no meaningful difference for students.
> - `llm_notable_observations:` Trailing character only.
> - `llm_review_flag:` no
