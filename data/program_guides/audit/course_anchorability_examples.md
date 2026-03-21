# Course Anchorability Examples

Date: 2026-03-21

Supporting artifact for `course_anchorability_matrix` and `course_signal_quality_review`.

## Anchorability Class Examples

### exact_current_unique

- `MSCSIA` (aos): `Security Foundations` -> `D481`
- `MSCSIA` (aos): `Security Operations` -> `D483`
- `MSCSIA` (aos): `Cloud Security` -> `D485`
- `MSCSIA` (aos): `Penetration Testing` -> `D484`
- `MSCSIA` (aos): `Governance, Risk, and Compliance` -> `D486`
- `MSCSIA` (aos): `Cybersecurity Management` -> `D489`
- `MSCSIA` (sp): `Security Foundations` -> `D481`
- `MSCSIA` (sp): `Security Operations` -> `D483`

### exact_observed_variant_unique

- `BAESSPMM` (aos): `Introduction to Communication: Connecting with Others` -> `D268`
- `BAESSPMM` (sp): `Introduction to Communication: Connecting with Others` -> `D268`
- `MSNUFNP` (aos): `Quality Outcomes in a Culture of Value-Based Nursing Care` -> `D026`
- `MSNUFNP` (aos): `Leadership and Management in Complex Healthcare Systems` -> `D030`
- `MSNUFNP` (aos): `Advancing Evidence-Based Innovation in Nursing Practice` -> `D031`
- `MSNUFNP` (aos): `Advanced Pathophysiology for the Advanced Practice Nurse` -> `D115`
- `MSNUFNP` (aos): `Advanced Pharmacology for the Advanced Practice Nurse` -> `D116`
- `MSNUFNP` (aos): `Advanced Health Assessment for the Advanced Practice Nurse` -> `D117`

### normalization_unique

- None observed in this run.

### ambiguous_current_exact

- `MSCSIA` (aos): `Secure Network Design` -> `C700, D482`
- `MSCSIA` (aos): `Secure Software Design` -> `C706, D487`
- `MSCSIA` (aos): `Cybersecurity Architecture and Engineering` -> `C726, D488`
- `MSCSIA` (sp): `Secure Network Design` -> `C700, D482`
- `MSCSIA` (sp): `Secure Software Design` -> `C706, D487`
- `MSCSIA` (sp): `Cybersecurity Architecture and Engineering` -> `C726, D488`
- `MSCSIA` (sp): `Cybersecurity Graduate Capstone` -> `C796, D490`
- `BAESSPMM` (aos): `Integrated Physical Sciences` -> `C165, C908`

### ambiguous_observed_exact

- None observed in this run.

### ambiguous_normalized

- None observed in this run.

### unmapped

- `MSSWEDOE` (aos): `Software Product Design and Requirement Engineering` -> `none`
- `MSSWEDOE` (aos): `Continuous Integration and Continuous Delivery` -> `none`
- `MSSWEDOE` (sp): `Software Product Design and Requirement Engineering` -> `none`
- `MSSWEDOE` (sp): `Continuous Integration and Continuous Delivery` -> `none`
- `BAESSPMM` (aos): `Personalized Learning for Inclusive Classrooms` -> `none`
- `BAESSPMM` (aos): `Planning Instructional Strategies for Meaningful Learning` -> `none`
- `BAESSPMM` (aos): `Introduction to Systems Thinking and Applications` -> `none`
- `BAESSPMM` (aos): `Technology and Ethics: Emerging Trends and Society` -> `none`

### non_course_noise

- `BSPRN` (aos): `The following section includes the areas of study in the program, with their associated courses. Your specific` -> `none`

## High-Ambiguity Titles

- `Calculus I` -> 6 candidates (C282, C362, C363, C958, D890, QJT2)
- `Secondary Disciplinary Literacy` -> 5 candidates (C728, C729, D162, D805, D806)
- `Elementary Disciplinary Literacy` -> 5 candidates (C732, C733, D164, D690, D698)
- `Technical Communication` -> 4 candidates (C768, C948, D339, E011)
- `Student Teaching I in Secondary Education` -> 4 candidates (D533, D534, D721, D741)
- `Student Teaching II in Secondary Education` -> 4 candidates (D535, D536, D722, D742)
- `Algebra for Secondary Mathematics Teaching` -> 4 candidates (C879, C880, D898, D904)
- `Enterprise Risk Management` -> 4 candidates (C418, C986, D368, D515)
- `Data Visualization` -> 4 candidates (C752, C939, D500, DCDV)
- `Student Teaching I in Special Education` -> 4 candidates (D529, D530, D719, D739)
- `Student Teaching II in Special Education` -> 4 candidates (D531, D532, D720, D740)
- `Student Teaching I in Elementary Education` -> 4 candidates (D523, D524, D717, D737)
- `Student Teaching II in Elementary Education` -> 4 candidates (D525, D526, D718, D738)
- `Middle School Science: Content Knowledge` -> 4 candidates (C293, C616, C902, DBV2)
- `Biology: Content Knowledge` -> 4 candidates (C294, C614, C900, CZV2)

## Certification Course-Level Examples

### false_positive_parser_noise

- `MSCSIA` `Security Operations` | mentions: aws and
- `MSCSIA` `Cybersecurity Management` | mentions: aws and
- `BAESSPMM` `Special Education Law, Policies and Procedures` | mentions: aws to
- `BSSESB` `General Earth Science I` | mentions: aws that
- `BSHIM` `Pathophysiology` | mentions: aws on
- `BSCSIA` `Information Systems Security` | mentions: aws and
- `BSCSIA` `Legal Issues in Information Security` | mentions: aws and
- `BSFIN` `Managing in a Global Business Environment` | mentions: aws in

### explicit_prep_claim

- `BSSWE_Java` `Business of IT - Project Management` | mentions: CompTIA Project+, CompTIA Project+.
- `BSSWE_Java` `Cloud Foundations` | mentions: AWS Certified
- `MSSWEUG` `Business of IT - Project Management` | mentions: CompTIA Project+, CompTIA Project+.
- `BSCNE` `IT Applications` | mentions: CompTIA A+
- `BSCNE` `IT Foundations` | mentions: CompTIA A+
- `BSCNE` `Network and Security - Applications` | mentions: CompTIA Security+
- `BSCNE` `Cloud Applications` | mentions: CompTIA Cloud+
- `BSCNE` `Networks` | mentions: CompTIA Network+

### explicit_alignment_or_associated_cert

- `MSCSAIML` `Machine Learning for Computer Scientists` | mentions: AWS Certified
- `ENDSESP` `Secondary Physics Curriculum` | mentions: Praxis exam., aws of, Praxis prep,
- `MATSESP` `Secondary Physics Curriculum` | mentions: Praxis exam., aws of, Praxis prep,
- `MATEES` `Secondary English Language Arts Curriculum` | mentions: Praxis 5039
- `ENDSESC` `Secondary Chemistry Curriculum` | mentions: Praxis exam,
- `MATSESC` `Secondary Chemistry Curriculum` | mentions: Praxis exam,
- `BSSESC` `Secondary Chemistry Curriculum` | mentions: Praxis exam,
- `MATSSES` `Secondary Social Studies Curriculum` | mentions: Praxis Social

### unclear

- `BSCNECIS` `DevNet Fundamentals` | mentions: Cisco Environment., Cisco DevNet
- `BSCNECIS` `Cyber Operations Fundamentals` | mentions: Cisco practices, Cisco Cybersecurity
- `BSCNECIS` `BSCNE-Cisco Capstone Project` | mentions: Cisco Capstone, Cisco tools
- `BSCNEAZR` `Azure Solutions Architecture` | mentions: Azure Solution, Azure platform.
- `BSCNEAZR` `BSCNE-Azure Capstone Project` | mentions: Azure Capstone, Azure environment, Azure CLI, Azure platform
- `BSCNEAWS` `AWS Cloud Architecture` | mentions: AWS Cloud
- `BSCNEAWS` `Cloud Deployment and Operations` | mentions: AWS Cloud
- `BSCNEAWS` `BSCNE-AWS Capstone Project` | mentions: AWS Capstone, AWS environment, AWS CLI, AWS platform

### adjacent_mention_only

- `BSACC` `Auditing` | mentions: CPA Code

## Prerequisite Course-Level Examples

### parser_artifact_or_weak

- `BAESSPMM` `Composition: Successful Self-Expression` | mentions: for this course and there is no specific technical knowledge needed
- `BSSWE_Java` `Composition: Successful Self-Expression` | mentions: for this course and there is no specific technical knowledge needed
- `MSSWEUG` `Composition: Successful Self-Expression` | mentions: for this course and there is no specific technical knowledge needed
- `BSCNE` `Composition: Successful Self-Expression` | mentions: for this course and there is no specific technical knowledge needed
- `BSSESB` `Composition: Successful Self-Expression` | mentions: for this course and there is no specific technical knowledge needed
- `BSHIM` `Composition: Successful Self-Expression` | mentions: for this course and there is no specific technical knowledge needed
- `BSMES` `Composition: Successful Self-Expression` | mentions: for this course and there is no specific technical knowledge needed
- `MSITM` `Project Management` | mentions: for this course

### internal_only_dependency_bundle

- `MSNUFNP` `Adult Primary Care for the Advanced Practice Nurse` | mentions: courses are required prior to taking this course: All MSN Core courses and NP Core courses
- `MSNUFNP` `Pediatric Primary Care for the Advanced Practice Nurse` | mentions: courses are required prior to taking this course: All MSN Core courses and NP Core courses
- `MSNUFNP` `Special Populations Primary Care for the Advanced Practice Nurse` | mentions: courses are required prior to taking this course: All MSN Core courses and NP Core courses
- `PMCNUFNP` `Adult Primary Care for the Advanced Practice Nurse` | mentions: courses are required prior to taking this course: All MSN Core courses and NP Core courses
- `PMCNUFNP` `Pediatric Primary Care for the Advanced Practice Nurse` | mentions: courses are required prior to taking this course: All MSN Core courses and NP Core courses
- `PMCNUFNP` `Special Populations Primary Care for the Advanced Practice Nurse` | mentions: courses are required prior to taking this course: All MSN Core courses and NP Core courses
- `PMCNUFNP` `Health Promotion of Patients and Populations Across the Lifespan` | mentions: courses are required prior to taking this course: All MSN Core courses and NP Core courses
- `BSPRN` `Health and Wellness Through Nutritional Sciences` | mentions: Courses: All prelicensure nursing curriculum courses from previous terms

### explicit_prerequisite_dependency

- `MACCM` `Data Analytics for Accountants II` | mentions: Data Analytics for Accountants I, for this course
- `BSSWE_Java` `Front-End Web Development` | mentions: Web Development Foundations, for this course
- `BSSWE_Java` `Advanced Data Management` | mentions: Data Management - Foundations, for this course
- `MSSWEUG` `Front-End Web Development` | mentions: Web Development Foundations, for this course
- `MSSWEUG` `Advanced Data Management` | mentions: Data Management - Foundations, for this course
- `BSCNE` `Networks` | mentions: Network and Security - Foundations, for this course
- `BSMES` `Precalculus` | mentions: Successful completion of a college level algebra course, for this course
- `BSMES` `Multivariable Calculus` | mentions: Calculus II, for this course

### sequencing_or_context_clue

- `BSSWE_Java` `Data Management - Applications` | mentions: Data Management - Foundations
- `MSSWEUG` `Data Management - Applications` | mentions: Data Management - Foundations
- `BSFIN` `Financial Management I` | mentions: for Financial Management I is Corporate Finance
- `BSDA` `Data Management - Applications` | mentions: Data Management - Foundations
- `BSUXD` `Introduction to Business Finance` | mentions: for this course is Introduction to Business Accounting
- `BSIT` `Data Management - Applications` | mentions: Data Management - Foundations
- `BSMGT` `Introduction to Business Finance` | mentions: for this course is Introduction to Business Accounting
- `MASEMG` `Astronomy` | mentions: for this course is General Physics
