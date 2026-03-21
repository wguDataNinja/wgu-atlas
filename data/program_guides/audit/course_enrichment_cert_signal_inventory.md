# Course Enrichment Certification Signal Inventory

Date: 2026-03-21

Scope: sampled guides only (`course_enrichment_sample_inventory`).

## Signal classes used

- `explicit_prep_language`: text explicitly says course prepares for certification exam.
- `alignment_or_exam_token`: course carries cert brand/token but explicit prep wording may not be complete.
- `adjacent_professional_standard`: professional standard mention without direct exam-prep claim.
- `parser_noise_likely`: extracted token appears to be parser artifact (not reliable cert claim).

## BSCSIA — Bachelor of Science, Cybersecurity and Information Assurance

| Course | Canonical anchor | Mention(s) | Signal class |
|---|---|---|---|
| IT Applications | ambiguous | CompTIA A+ | alignment_or_exam_token |
| IT Foundations | ambiguous | CompTIA A+ | alignment_or_exam_token |
| Information Systems Security | C845 | aws and | parser_noise_likely |
| Network and Security - Applications | ambiguous | CompTIA Security+ | alignment_or_exam_token |
| Networks | ambiguous | CompTIA Network+ | alignment_or_exam_token |
| Business of IT - Project Management | ambiguous | CompTIA Project+; CompTIA Project+. | alignment_or_exam_token |
| Legal Issues in Information Security | ambiguous | aws and | parser_noise_likely |
| Cyber Defense and Countermeasures | ambiguous | aws and; CompTIA Cybersecurity | alignment_or_exam_token |

## BSCNEAWS — Bachelor of Science, Cloud and Network Engineering - Amazon Web

| Course | Canonical anchor | Mention(s) | Signal class |
|---|---|---|---|
| IT Applications | ambiguous | CompTIA A+ | alignment_or_exam_token |
| IT Foundations | ambiguous | CompTIA A+ | alignment_or_exam_token |
| Network and Security - Applications | ambiguous | CompTIA Security+ | alignment_or_exam_token |
| Networks | ambiguous | CompTIA Network+ | alignment_or_exam_token |
| Cloud Foundations | ambiguous | AWS Certified | alignment_or_exam_token |
| AWS Cloud Architecture | D319 | AWS Cloud | parser_noise_likely |
| Cloud Deployment and Operations | ambiguous | AWS Cloud | parser_noise_likely |
| BSCNE-AWS Capstone Project | E030 | AWS Capstone; AWS environment; AWS CLI; AWS platform | parser_noise_likely |

## MSCSIA — Master of Science, Cybersecurity and Information Assurance

| Course | Canonical anchor | Mention(s) | Signal class |
|---|---|---|---|
| Security Operations | D483 | aws and | parser_noise_likely |
| Cybersecurity Management | D489 | aws and | parser_noise_likely |

## BSACC — Bachelor of Science, Accounting

| Course | Canonical anchor | Mention(s) | Signal class |
|---|---|---|---|
| Managing in a Global Business Environment | D080 | aws in | parser_noise_likely |
| Auditing | ambiguous | CPA Code | adjacent_professional_standard |

## MATSPED — Master of Arts in Teaching, Special Education

| Course | Canonical anchor | Mention(s) | Signal class |
|---|---|---|---|
| Special Education Law, Policies and Procedures | unmapped | aws to | parser_noise_likely |

## Cross-sample observations

- Strong explicit prep language appears in several IT/network/security courses (e.g., CompTIA Security+, Network+, AWS Certified Practitioner exam references).
- A large subset of extracted cert mentions are parser-noise fragments around the token "aws" (e.g., "aws and", "aws in").
- Some non-cert professional references are present (e.g., AICPA code mention in accounting) but do not imply exam-prep mapping by themselves.