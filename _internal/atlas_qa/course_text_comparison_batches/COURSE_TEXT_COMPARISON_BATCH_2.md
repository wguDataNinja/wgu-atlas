# Course Text Comparison — Batch 2 of 4

**Source artifact:** `_internal/atlas_qa/COURSE_TEXT_COMPARISON_INDEX.md`
**Batch scope:** §5C-i STRONG materially different pairs, rows 1–35 of 70 (diff > 50; sorted by diff descending, highest-priority cases first)
**Batching rule:** §5C-i was split in half by row number. Batch 2 = rows 1–35 (D560 through D224). Batch 3 = rows 36–70 (D225 through D236).
**Annotation status:** Re-annotated (original weak-model pass replaced).

Text excerpts are from the source artifact (200-char truncation). Where source showed abbreviated title only, the full text is available in the paired artifact files.

---

### 1. D560 — Internal Auditing I
- **type:** STRONG | **v:** 1/1 | **cat_len:** 998 | **guide_len:** 506 | **diff:** 492
- **source_programs:** MACCA, MACCM
- **cat_text:** "Internal Auditing I provides learners with the basic knowledge and skills necessary to succeed as an entry-level internal audit professional. The course introduces the fundamentals of internal auditing…"
- **guide_text:** "Internal Auditing I provides learners with the basic knowledge and skills necessary to succeed as an entry-level internal audit professional. The Institute of Internal Auditors defines internal auditing…"

> **Annotation**
> - `llm_difference_summary: Catalog continues well beyond the guide's stopping point; guide is truncated at roughly the halfway point of the full description.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Guide appears truncated; catalog provides a complete course overview nearly double the guide length.`
> - `llm_notable_observations: Both texts open identically; the divergence is entirely a length/completeness issue, not a framing difference.`
> - `llm_review_flag: no`

---

### 2. D358 — Global Human Resource Management
- **type:** STRONG | **v:** 1/1 | **cat_len:** 414 | **guide_len:** 897 | **diff:** 483
- **source_programs:** BSHR
- **cat_text:** "Organizations increasingly operate across borders, and HR professionals must be prepared to manage people in diverse cultural and legal environments. This course introduces you to international HR pra…"
- **guide_text:** "Global Human Resource Management explores the rapidly changing field of international human resource management (HRM) and examines a global perspective in relation to staffing, personnel management, s…"

> **Annotation**
> - `llm_difference_summary: Catalog is the shorter modern rewrite; guide is the older pre-rewrite BSHR text with more detailed coverage of specific IHRM topics including staffing, personnel management, and global perspective.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the current edition text; guide is locked to an older BSHR authoring event and should not be treated as the authoritative description.`
> - `llm_notable_observations: BSHR cluster course — guide is substantially richer in content but represents a pre-rewrite version. The guide's additional detail on global HRM topics is notable and may be worth reviewing against the catalog rewrite.`
> - `llm_review_flag: yes`

---

### 3. D356 — HR Technology
- **type:** STRONG | **v:** 1/1 | **cat_len:** 352 | **guide_len:** 678 | **diff:** 326
- **source_programs:** BSHR
- **cat_text:** "Technology is transforming HR into a data-driven and strategic function. This course introduces you to human resource information systems, digital tools, and analytics that improve efficiency and guid…"
- **guide_text:** "HR Technology focuses on the usage of technology for strategic human resource management. The learner will develop competency in critical skills related to analyzing the value and application of the d…"

> **Annotation**
> - `llm_difference_summary: Catalog is the shorter modern rewrite; guide is the older BSHR locked text with specific competency language around analyzing the value and application of digital HR tools.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the current edition text; guide is the pre-rewrite BSHR version locked to an older authoring event.`
> - `llm_notable_observations: BSHR cluster — guide's "develop competency in critical skills" framing and longer treatment of strategic HR applications is more detailed than the catalog rewrite. Content delta may be worth reviewing.`
> - `llm_review_flag: yes`

---

### 4. E011 — Technical Communication (variant 3/3)
- **type:** STRONG | **v:** 3/3 | **cat_len:** 555 | **guide_len:** 235 | **diff:** 320
- **source_programs:** MSITM
- **cat_text:** "Technical Communication teaches IT managers how to convey complex information clearly and effectively to diverse audiences, whether technical or nontechnical. The course covers skills in writing, pres…"
- **guide_text:** "This course covers basic elements of technical communication, including professional written communication proficiency; the ability to strategize approaches for communicating with technical and non-tec…"

> **Annotation**
> - `llm_difference_summary: Catalog is a full course description framed for IT managers; the MSITM guide variant is a heavily condensed summary at less than half the catalog length.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Guide variant is severely truncated; catalog provides the complete course description.`
> - `llm_notable_observations: Most heavily truncated of the E011 guide variants (235 chars vs catalog 555). The MSITM guide condenses the IT manager framing to a brief list of communication skills.`
> - `llm_review_flag: no`

---

### 5. D436 — Inclusive Workplace Culture Capstone
- **type:** STRONG | **v:** 1/1 | **cat_len:** 387 | **guide_len:** 706 | **diff:** 319
- **source_programs:** MSHRM
- **cat_text:** "Inclusive workplaces foster environments where people feel a sense of belonging and where diverse perspectives drive innovation. This capstone course helps you apply what you've learned throughout the…"
- **guide_text:** "The Inclusive Workplace Culture Capstone course is designed to be a comprehensive evaluation of the knowledge and skills accumulated throughout the Master of Science in Human Resource Management degr…"

> **Annotation**
> - `llm_difference_summary: Catalog frames this broadly as a capstone applying prior learning; guide is explicitly scoped to the MSHRM degree with comprehensive evaluation and program-specific competency language.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Guide text is MSHRM-program-specific ("Master of Science in Human Resource Management degree"); catalog provides the general course description appropriate for default display.`
> - `llm_notable_observations: MSHRM cluster — guide's explicit program-degree framing is more informative for an MSHRM student but unsuitable as a general course description. Worth storing as a program-context alternate.`
> - `llm_review_flag: yes`

---

### 6. AIT2 — Organic Chemistry (variant 1/2)
- **type:** STRONG | **v:** 1/2 | **cat_len:** 260 | **guide_len:** 562 | **diff:** 302
- **source_programs:** ENDSESC
- **cat_text:** "Organic Chemistry covers fundamental concepts of organic chemistry, including molecular structure, reactivity, and reaction mechanisms. Students explore topics such as nomenclature, stereochemistry, f…"
- **guide_text:** "Organic Chemistry covers fundamental and applied concepts of organic chemistry. The learner will develop competency in critical skills related to molecular structure, functional groups, and reaction me…"

> **Annotation**
> - `llm_difference_summary: Catalog provides a brief topic survey; guide adds "applied concepts" framing and explicit competency development language, and is more than double the catalog length.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default display source; guide's competency framing is ENDSESC-program-specific.`
> - `llm_notable_observations: Guide is substantially longer with student-facing competency language that catalog lacks; the additional content may add value as a program-context alternate.`
> - `llm_review_flag: yes`

---

### 7. C175 — Network and Security - Foundations (variant 2/3)
- **type:** STRONG | **v:** 2/3 | **cat_len:** 594 | **guide_len:** 296 | **diff:** 298
- **source_programs:** BSDA, BSSWE_C, BSSWE_Java
- **cat_text:** "Network and Security - Foundations introduces learners to the fundamentals of networking and security to…"
- **guide_text:** "Network and Security - Foundations introduces learners to the fundamentals of networking and security to prepare them for the CompTIA Network+ exam. This course covers…"

> **Annotation**
> - `llm_difference_summary: Catalog provides the full course description; guide for BSDA/BSSWE programs is a condensed exam-focused version about half the catalog length.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Guide is truncated and leads with exam-prep framing; catalog is the complete general course description.`
> - `llm_notable_observations: Exam-lock pattern consistent with CNE/SWE cluster — guide opens with CompTIA Network+ reference and is ~50% of catalog length.`
> - `llm_review_flag: no`

---

### 8. C175 — Network and Security - Foundations (variant 1/3)
- **type:** STRONG | **v:** 1/3 | **cat_len:** 594 | **guide_len:** 297 | **diff:** 297
- **source_programs:** BSCNE, BSCNEAWS, BSCNEAZR
- **cat_text:** "Network and Security - Foundations introduces learners to the fundamentals of networking and security to…"
- **guide_text:** "Network and Security - Foundations introduces learners to the fundamentals of networking and security to prepare them for the CompTIA Network+ exam. This course covers…"

> **Annotation**
> - `llm_difference_summary: Catalog provides the full course description; BSCNE cluster guide is the canonical exam-locked truncated version at roughly half the catalog length.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Guide is the CNE cluster locked version; catalog is more complete and not exam-scoped.`
> - `llm_notable_observations: Canonical CNE exam-lock pattern — guide leads with Network+ exam reference. Near-identical to variant 2/3; same text, different source programs.`
> - `llm_review_flag: no`

---

### 9. C234 — Software Quality Assurance
- **type:** STRONG | **v:** 1/1 | **cat_len:** 433 | **guide_len:** 160 | **diff:** 273
- **source_programs:** BSITM
- **cat_text:** "Software Quality Assurance introduces you to the principles and practices essential for ensuring software reliability and functionality. The course covers testing methodologies, including unit, integra…"
- **guide_text:** "Software Quality Assurance introduces students to the principles and practices of software quality including software testing, debugging, and quality assurance methodologies."

> **Annotation**
> - `llm_difference_summary: Guide is a single condensed sentence (160 chars); catalog provides nearly three times more content covering specific testing methodologies.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Guide is severely truncated to a single introductory sentence; catalog is the only meaningful course description available.`
> - `llm_notable_observations: At 160 chars the guide is among the shortest in the corpus — likely an incomplete or early extraction from the BSITM guide.`
> - `llm_review_flag: no`

---

### 10. C172 — Network and Security - Design (variant 1/2)
- **type:** STRONG | **v:** 1/2 | **cat_len:** 574 | **guide_len:** 323 | **diff:** 251
- **source_programs:** BSCNE, BSCNEAWS, BSCNEAZR
- **cat_text:** "Network and Security - Design focuses on architecting and designing secure network solutions…"
- **guide_text:** "Network and Security - Design focuses on advanced network design, implementation and troubleshooting including routing and switching and network security."

> **Annotation**
> - `llm_difference_summary: Catalog covers secure network architecture broadly; CNE cluster guide is narrower, focusing on routing, switching, and troubleshooting at roughly half the catalog length.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is more complete; CNE guide variant omits the security architecture framing and is substantially truncated.`
> - `llm_notable_observations: CNE cluster pattern — guide is shorter with a narrower technical scope; catalog is the appropriate default for general course display.`
> - `llm_review_flag: no`

---

### 11. D435 — Inclusive Workplace Culture
- **type:** STRONG | **v:** 1/1 | **cat_len:** 380 | **guide_len:** 628 | **diff:** 248
- **source_programs:** MSHRM
- **cat_text:** "Inclusive organizations create workplaces where all employees can contribute their best work…"
- **guide_text:** "Inclusive Workplace Culture focuses on creating and sustaining inclusive work environments where all individuals can thrive. Students will develop competency in…"

> **Annotation**
> - `llm_difference_summary: Catalog is a concise overview; MSHRM guide is 65% longer with competency-development framing specific to that program.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the general course description for default display; guide's competency framing is MSHRM-specific.`
> - `llm_notable_observations: MSHRM cluster pattern — guide consistently provides more specific competency language than catalog across this program's courses. Worth storing as a program-context alternate.`
> - `llm_review_flag: yes`

---

### 12. D360 — Compensation and Benefits Design
- **type:** STRONG | **v:** 1/1 | **cat_len:** 406 | **guide_len:** 170 | **diff:** 236
- **source_programs:** BSHR
- **cat_text:** "Effective compensation and benefits strategies are essential for attracting, retaining, and motivating talent. This course explores how organizations design, implement, and evaluate pay structures, incen…"
- **guide_text:** "Compensation and Benefits Design introduces learners to concepts of designing and managing compensation and benefits packages."

> **Annotation**
> - `llm_difference_summary: Guide is a single introductory sentence (170 chars); catalog provides a full strategic overview more than double the guide length.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Guide is severely truncated; catalog is the only complete description.`
> - `llm_notable_observations: Unusual within BSHR cluster — while D358/D356 have longer guide text, D360's guide is drastically shorter (170 chars), suggesting different guide authoring events within the same program.`
> - `llm_review_flag: no`

---

### 13. D235 — Care of Older Adults (variant 2/2)
- **type:** STRONG | **v:** 2/2 | **cat_len:** 890 | **guide_len:** 1110 | **diff:** 220
- **source_programs:** MSRNNUED, MSRNNULM, MSRNNUNI
- **cat_text:** "Care of Older Adults…"
- **guide_text:** "Care of Older Adults…"

> **Annotation**
> - `llm_difference_summary: Guide version for MSRNN programs is 25% longer; likely includes program-specific clinical framing for RN-to-MSN populations.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default display source; full text is truncated in source so exact differences are not visible.`
> - `llm_notable_observations: MSRNN cluster — multiple older-adult and nursing practice courses in this batch show longer guide text; pattern suggests MSRNN guides carry additional clinical context.`
> - `llm_review_flag: yes`

---

### 14. C722 — Business of IT - Applications (variant 2/3)
- **type:** STRONG | **v:** 2/3 | **cat_len:** 633 | **guide_len:** 417 | **diff:** 216
- **source_programs:** MSDADPE, MSITM
- **cat_text:** "Business of IT - Applications focuses on applying IT management skills in professional settings…"
- **guide_text:** "Business of IT - Applications…"

> **Annotation**
> - `llm_difference_summary: Catalog is 50% longer; guide variant for MSDADPE/MSITM is a condensed version of the same description.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is more complete; guide is a truncated program-specific variant.`
> - `llm_notable_observations: C722 appears in three guide variants across batches; all guide variants are shorter than catalog (417, 575, 633 for variants 2/3, 3/3, and catalog respectively).`
> - `llm_review_flag: no`

---

### 15. E011 — Technical Communication (variant 1/3)
- **type:** STRONG | **v:** 1/3 | **cat_len:** 555 | **guide_len:** 357 | **diff:** 198
- **source_programs:** BSIT
- **cat_text:** "Technical Communication teaches IT managers how to convey complex information clearly…"
- **guide_text:** "Technical Communication introduces students to essential writing skills for the workplace, emphasizing…"

> **Annotation**
> - `llm_difference_summary: Catalog frames this as an IT manager communication course; BSIT guide variant frames it as general student workplace writing skills — a genuine framing philosophy difference.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog provides the authoritative course framing for default display; guide variant reflects a different intended audience (general IT students vs managers).`
> - `llm_notable_observations: The framing difference is substantive — "IT managers" vs "students... workplace writing" — suggesting the course serves different populations across programs. Could matter for students in non-management IT programs.`
> - `llm_review_flag: yes`

---

### 16. D082 — Intermediate Accounting II (variant 1/2)
- **type:** STRONG | **v:** 1/2 | **cat_len:** 427 | **guide_len:** 615 | **diff:** 188
- **source_programs:** BSACC, BSBAHC, BSC
- **cat_text:** "Intermediate Accounting II explores complex topics in financial accounting including equity, debt, leases, pensions…"
- **guide_text:** "Intermediate Accounting II examines complex topics in corporate financial reporting. Students will develop competency in analyzing stockholders' equity, earnings per share…"

> **Annotation**
> - `llm_difference_summary: Catalog uses a generic "complex topics in financial accounting" framing; guide adds "corporate financial reporting" emphasis and explicit competency language around stockholders' equity and earnings per share.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default display source; guide's competency framing is program-specific to BSACC/BSBAHC/BSC.`
> - `llm_notable_observations: Guide's "develops competency in analyzing stockholders' equity, earnings per share" is more specific and student-facing than catalog; the corporate reporting framing is a genuine content emphasis difference worth preserving as an alternate.`
> - `llm_review_flag: yes`

---

### 17. D871 — Organic Chemistry: STEM Connections (variant 2/2)
- **type:** STRONG | **v:** 2/2 | **cat_len:** 631 | **guide_len:** 809 | **diff:** 178
- **source_programs:** MATSESC
- **cat_text:** "Organic Chemistry: STEM Connections…"
- **guide_text:** "Organic Chemistry: STEM Connections…"

> **Annotation**
> - `llm_difference_summary: Guide variant for MATSESC is 28% longer; likely adds teacher-education-specific STEM connections and pedagogical framing absent from catalog.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default; guide is a program-specific variant for a teacher education program (MATSESC = MA Teaching, Earth/Space Science with Chemistry).`
> - `llm_notable_observations: MATSESC context suggests guide adds teacher-educator framing for chemistry content — potentially meaningful for students in that credential program.`
> - `llm_review_flag: yes`

---

### 18. D219 — Pathophysiology and Pharmacology for the RN-BSN
- **type:** STRONG | **v:** 1/1 | **cat_len:** 610 | **guide_len:** 444 | **diff:** 166
- **source_programs:** BSNU, BSPRN
- **cat_text:** "Pathophysiology and Pharmacology for the RN-BSN…"
- **guide_text:** "Pathophysiology and Pharmacology…"

> **Annotation**
> - `llm_difference_summary: Catalog is 37% longer; guide is a condensed version that omits the additional clinical context present in catalog.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is more complete; guide appears truncated relative to the full description.`
> - `llm_notable_observations: Nursing course with significant length difference; guide for BSNU/BSPRN is notably shorter, which is atypical for BSPRN cluster courses that usually have longer guide text.`
> - `llm_review_flag: no`

---

### 19. C179 — Network and Security - Advanced Networking Concepts (variant 1/2)
- **type:** STRONG | **v:** 1/2 | **cat_len:** 293 | **guide_len:** 457 | **diff:** 164
- **source_programs:** BSCNE, BSCNEAWS, BSCNEAZR
- **cat_text:** "Network and Security - Advanced Networking Concepts…"
- **guide_text:** "Network and Security - Advanced Networking Concepts focuses on advanced networking including routing protocols, switching, and network automation…"

> **Annotation**
> - `llm_difference_summary: Unlike other CNE cluster courses, the guide here is 56% longer than the catalog, adding specific content on routing protocols, switching, and network automation absent from the brief catalog description.`
> - `llm_preference_for_research_tool: needs_review`
> - `llm_preference_reason: Reversed pattern from C175/C172 — catalog is unusually short and guide adds substantive technical content; cannot default to catalog without reviewing whether catalog is the truncated version here.`
> - `llm_notable_observations: This is the only CNE cluster course in this batch where guide is substantially longer than catalog. Catalog at 293 chars is among the shorter descriptions in the corpus. Warrants data-level inspection to determine if catalog is the truncated source.`
> - `llm_review_flag: yes`

---

### 20. D352 — Corporate Finance
- **type:** STRONG | **v:** 1/1 | **cat_len:** 367 | **guide_len:** 525 | **diff:** 158
- **source_programs:** BSFIN, BSHR
- **cat_text:** "Corporate Finance examines financial management principles…"
- **guide_text:** "Corporate Finance provides students with a deep understanding of how firms make financial decisions…"

> **Annotation**
> - `llm_difference_summary: Catalog uses a brief "financial management principles" framing; guide is 43% longer with a more detailed treatment of how firms make financial decisions.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default display source; guide's extended treatment is program-specific to BSFIN/BSHR.`
> - `llm_notable_observations: Guide's "deep understanding of how firms make financial decisions" framing is more substantive and student-facing than catalog's brief framing; appears in two programs.`
> - `llm_review_flag: yes`

---

### 21. D441 — Women's Health
- **type:** STRONG | **v:** 1/1 | **cat_len:** 307 | **guide_len:** 455 | **diff:** 148
- **source_programs:** BSPRN
- **cat_text:** "Women's Health…"
- **guide_text:** "Women's Health covers the assessment, diagnosis, and management of common women's health conditions…"

> **Annotation**
> - `llm_difference_summary: Catalog is brief; guide adds clinical structure with "assessment, diagnosis, and management" framing specific to the BSPRN program.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default; guide's clinical framing is program-specific to BSPRN.`
> - `llm_notable_observations: For a nursing research query, guide's clinical structure (assessment/diagnosis/management) may be more informative than the brief catalog description. Consistent with BSPRN pattern of longer guide text for clinical courses.`
> - `llm_review_flag: yes`

---

### 22. D606 — Machine Learning
- **type:** STRONG | **v:** 1/1 | **cat_len:** 754 | **guide_len:** 606 | **diff:** 148
- **source_programs:** MSDADS
- **cat_text:** "Machine Learning…"
- **guide_text:** "Machine Learning…"

> **Annotation**
> - `llm_difference_summary: Catalog is 24% longer; guide for MSDADS is a condensed variant of the same description.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is more complete; guide appears to be a program-specific abridgment.`
> - `llm_notable_observations: Both texts are truncated in source; both are substantial. The truncation suggests a program-specific abridgment rather than a fundamentally different description.`
> - `llm_review_flag: no`

---

### 23. D432 — Strategic Human Resource Management
- **type:** STRONG | **v:** 1/1 | **cat_len:** 411 | **guide_len:** 552 | **diff:** 141
- **source_programs:** MSHRM
- **cat_text:** "Strategic HRM examines how HR strategy aligns with organizational goals…"
- **guide_text:** "Strategic Human Resource Management focuses on the strategic role of human resources in organizational success…"

> **Annotation**
> - `llm_difference_summary: Catalog uses a concise "HR strategy aligns with organizational goals" framing; MSHRM guide is 34% longer with a more detailed treatment of HR's strategic role in organizational success.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default; guide's extended strategic framing is MSHRM-specific.`
> - `llm_notable_observations: MSHRM cluster — guide consistently adds more detail on strategic and organizational dimensions across this program's courses. The pattern suggests the MSHRM guide was authored at a higher level of specificity than the catalog descriptions for these courses.`
> - `llm_review_flag: yes`

---

### 24. D839 — Teaching and Learning in Secondary Schools (variant 2/2)
- **type:** STRONG | **v:** 2/2 | **cat_len:** 874 | **guide_len:** 738 | **diff:** 136
- **source_programs:** MATEES
- **cat_text:** "Teaching and Learning in Secondary Schools…"
- **guide_text:** "Teaching and Learning in Secondary Schools…"

> **Annotation**
> - `llm_difference_summary: Catalog is 18% longer; MATEES guide variant is condensed and likely omits some catalog content.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the more complete version; guide is a shorter program-specific variant.`
> - `llm_notable_observations: MATEES (MA Teaching) variant; both texts are truncated in source so exact differences are not visible.`
> - `llm_review_flag: no`

---

### 25. D875 — Earth, Moon, and Space (variant 2/2)
- **type:** STRONG | **v:** 2/2 | **cat_len:** 758 | **guide_len:** 623 | **diff:** 135
- **source_programs:** MATSESB, MATSESC, MATSESE
- **cat_text:** "Earth, Moon, and Space…"
- **guide_text:** "Earth, Moon, and Space…"

> **Annotation**
> - `llm_difference_summary: Catalog is 22% longer; guide variant for teacher education STEM programs (MATSESB/C/E) is condensed.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the more complete version.`
> - `llm_notable_observations: Teacher education STEM course; both texts are truncated in source.`
> - `llm_review_flag: no`

---

### 26. D893 — Mathematics Methods (variant 2/2)
- **type:** STRONG | **v:** 2/2 | **cat_len:** 743 | **guide_len:** 874 | **diff:** 131
- **source_programs:** MAMES
- **cat_text:** "Mathematics Methods…"
- **guide_text:** "Mathematics Methods…"

> **Annotation**
> - `llm_difference_summary: Guide variant for MAMES is 18% longer; likely adds mathematics education pedagogy framing for teacher educators.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default; guide adds education-specific framing for the MAMES (MA Mathematics Education Secondary) program.`
> - `llm_notable_observations: MAMES is a teacher education program; the longer guide text likely reflects pedagogical framing around mathematics instruction that is relevant to that specific audience.`
> - `llm_review_flag: yes`

---

### 27. C236 — Compensation and Benefits
- **type:** STRONG | **v:** 1/1 | **cat_len:** 386 | **guide_len:** 512 | **diff:** 126
- **source_programs:** BSBAHC, BSITM
- **cat_text:** "Compensation and benefits significantly influence how organizations attract, motivate, and retain talent. In this course, students will explore total rewards philosophy…"
- **guide_text:** "Compensation and Benefits develops competence in the design and implementation of compensation and benefits systems in a global work environment. Students will analyze…"

> **Annotation**
> - `llm_difference_summary: Catalog emphasizes "total rewards philosophy"; guide emphasizes "design and implementation in a global work environment" with competency framing — a genuine content emphasis difference, not just length.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default display source; the framing difference is real but catalog remains the authoritative display version.`
> - `llm_notable_observations: "Total rewards" vs "global design/implementation" represents genuinely different emphasis between the two descriptions of the same course. Worth human review to assess which better serves students browsing the course.`
> - `llm_review_flag: yes`

---

### 28. D440 — Prenatal and Newborn Health
- **type:** STRONG | **v:** 1/1 | **cat_len:** 371 | **guide_len:** 493 | **diff:** 122
- **source_programs:** BSPRN
- **cat_text:** "Prenatal and Newborn Health…"
- **guide_text:** "Prenatal and Newborn Health…"

> **Annotation**
> - `llm_difference_summary: Guide is 33% longer; likely adds clinical prenatal/newborn care framing specific to BSPRN students.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default; guide adds BSPRN-specific clinical framing.`
> - `llm_notable_observations: BSPRN cluster — multiple nursing clinical courses in this batch show longer guide text; consistent with the BSPRN guide carrying additional clinical context for RN-BSN students.`
> - `llm_review_flag: yes`

---

### 29. C805 — Leadership Foundations (variant 3/3)
- **type:** STRONG | **v:** 3/3 | **cat_len:** 414 | **guide_len:** 527 | **diff:** 113
- **source_programs:** BSNU
- **cat_text:** "Leadership Foundations…"
- **guide_text:** "Leadership Foundations…"

> **Annotation**
> - `llm_difference_summary: BSNU guide variant is 27% longer; likely adds nursing-specific leadership context for undergraduate nursing students.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default; guide variant is program-specific to BSNU.`
> - `llm_notable_observations: C805 appears in three guide variants spanning nursing (BSNU) and human services (BSHS) programs; each program family likely frames leadership through its own lens.`
> - `llm_review_flag: yes`

---

### 30. D357 — Talent Acquisition
- **type:** STRONG | **v:** 1/1 | **cat_len:** 436 | **guide_len:** 325 | **diff:** 111
- **source_programs:** BSHR
- **cat_text:** "Talent Acquisition covers modern recruitment and hiring strategy…"
- **guide_text:** "Talent Acquisition focuses on strategies for attracting and selecting qualified candidates…"

> **Annotation**
> - `llm_difference_summary: Catalog is 34% longer with a modern recruitment strategy framing; BSHR guide is condensed around attracting and selecting candidates.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the more complete version; guide is a truncated BSHR variant.`
> - `llm_notable_observations: Within the BSHR cluster, D357 has shorter guide text (unlike D358/D356 where guide is longer). BSHR courses were not all locked at the same authoring event.`
> - `llm_review_flag: no`

---

### 31. C845 — Cybersecurity and Information Assurance Capstone
- **type:** STRONG | **v:** 1/1 | **cat_len:** 1021 | **guide_len:** 1131 | **diff:** 110
- **source_programs:** BSCSIA
- **cat_text:** "Cybersecurity Capstone…"
- **guide_text:** "Cybersecurity Capstone…"

> **Annotation**
> - `llm_difference_summary: Both texts are substantial; guide is 11% longer and likely adds BSCSIA-specific capstone context beyond what catalog provides.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default; guide's additional content is program-scoped to BSCSIA.`
> - `llm_notable_observations: Both are long, substantive descriptions; text is truncated in source so full comparison is not available. The modest percentage difference at this text length could represent meaningful additional capstone-specific content.`
> - `llm_review_flag: yes`

---

### 32. D634 — Community Health
- **type:** STRONG | **v:** 1/1 | **cat_len:** 783 | **guide_len:** 674 | **diff:** 109
- **source_programs:** BSHS
- **cat_text:** "Community Health…"
- **guide_text:** "Community Health…"

> **Annotation**
> - `llm_difference_summary: Catalog is 16% longer; guide for BSHS is a condensed version of the community health description.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is more complete; guide is a truncated variant.`
> - `llm_notable_observations: Both texts are truncated in source; straightforward catalog-longer case.`
> - `llm_review_flag: no`

---

### 33. D156 — Role of the Nurse Leader (variant 2/2)
- **type:** STRONG | **v:** 2/2 | **cat_len:** 1202 | **guide_len:** 1094 | **diff:** 108
- **source_programs:** MSRNNULM
- **cat_text:** "Role of the Nurse Leader…"
- **guide_text:** "Role of the Nurse Leader…"

> **Annotation**
> - `llm_difference_summary: Catalog is 10% longer; MSRNNULM guide variant is slightly condensed relative to catalog.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the more complete version.`
> - `llm_notable_observations: Both are substantial nurse leader course descriptions (>1000 chars); the difference is modest at this text length.`
> - `llm_review_flag: no`

---

### 34. D157 — Leadership and Management (variant 1/2)
- **type:** STRONG | **v:** 1/2 | **cat_len:** 1133 | **guide_len:** 1241 | **diff:** 108
- **source_programs:** MSNULM, PMCNULM
- **cat_text:** "Leadership and Management…"
- **guide_text:** "Leadership and Management…"

> **Annotation**
> - `llm_difference_summary: Guide variant for MSNULM/PMCNULM is 10% longer; likely adds advanced nursing leadership management context specific to those programs.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the default; guide's additional content is program-specific to MSNULM/PMCNULM.`
> - `llm_notable_observations: MSNULM = MSN Nursing Leadership and Management; the guide for this advanced credential program being longer suggests program-depth additions relevant to that specialization.`
> - `llm_review_flag: yes`

---

### 35. D224 — Concepts in Nursing Practice II
- **type:** STRONG | **v:** 1/1 | **cat_len:** 679 | **guide_len:** 571 | **diff:** 108
- **source_programs:** MSRNNUED, MSRNNULM, MSRNNUNI
- **cat_text:** "Concepts in Nursing Practice II…"
- **guide_text:** "Concepts in Nursing Practice II…"

> **Annotation**
> - `llm_difference_summary: Catalog is 19% longer; guide for MSRNN programs is a condensed variant.`
> - `llm_preference_for_research_tool: catalog`
> - `llm_preference_reason: Catalog is the more complete version.`
> - `llm_notable_observations: Part of the Concepts in Nursing Practice series (also D221, D225, D236 in other batches); catalog is consistently the longer version for this course series across the MSRNN cluster.`
> - `llm_review_flag: no`
