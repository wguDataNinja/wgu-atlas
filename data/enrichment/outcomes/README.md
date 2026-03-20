# WGU Accreditation & Outcomes Pages

Tracked in `outcomes_links.json`. These are the pages WGU publishes that contain real data — not marketing copy. Coverage is sparse by design: WGU only publishes this kind of data when an accrediting body requires it.

| Page | Scope | Accreditor |
|---|---|---|
| B.S. Computer Science Outcomes | Program | ABET |
| B.S. Cybersecurity Outcomes | Program | ABET |
| B.S. Cybersecurity CAE-CDE Designation | Program | NSA/DHS |
| B.S. Health Information Management Accreditation | Program | CAHIIM |
| School of Business Accreditation | School | ACBSP |
| Teachers College Accreditation | School | CAEP |

---

## ABET Outcomes Pages (BSCS, BSCSIA)

WGU publishes `/outcomes.html` pages only for ABET-accredited programs. As of 2026-03, two programs have these: B.S. Computer Science and B.S. Cybersecurity and Information Assurance.

**What they contain** — two real data sections per page:

**Program Results** — enrollment and completion metrics:
- Total graduates
- Enrollments
- Retention rate
- On-time progress
- Very Satisfied students (VSAT)

**Program Assessment Results** — course pass rates by course across time periods (BSCS: July 2018–June 2022; BSCSIA: similar range).

**What this data tells us:**
- These degrees behave like multi-year programs. Enrollment, retention, and graduation figures reflect cohorts spread across years, not months.
- Many students are still in the pipeline after 1–3 years.
- Progress is mixed — not universally fast or slow.
- Some courses appear to be bottlenecks based on pass rate patterns.

**What this data does not tell us:**
- How many students finish in a few months (fast completers are invisible in aggregate charts).
- Median time to degree.
- Whether pass rate means first attempt or eventual pass after retries.

**Main takeaway:** These pages support "years is normal" much more than "months is normal."

---

## CAEP Accreditation — Teachers College

This is a school-level educator-preparation outcomes page, not a normal degree page.

WGU's Teachers College is CAEP-accredited for teacher-licensure programs. WGU says it was the first competency-based online university to receive CAEP accreditation for teacher-licensure degree programs. The page covers initial licensure and advanced licensure education programs, with data primarily for academic year 2023–2024.

Unlike the ABET outcomes pages, this one is not mainly about retention/graduation pipeline charts. It focuses on readiness, employer satisfaction, competency demonstration, and licensure outcomes.

**What the page measures — 4 CAEP measures:**

1. **Completer effectiveness** — surveys of graduates 2, 3, and 5 years after graduation, plus employer surveys, about how well the program prepared them for classroom work.
2. **Employer and stakeholder satisfaction** — employers report strong satisfaction with WGU graduates' skills and readiness.
3. **Candidate competency at completion** — edTPA pass rates for initial licensure programs; final demonstration / student teaching / capstone outcomes for advanced programs.
4. **Ability to be hired** — hiring outcomes plus licensing exam performance.

**Hard numbers explicitly in the text:**
- Praxis pass rate — Initial: 80.18% / Advanced: 90.33% / All programs: 85.25%
- Average licensure rates: 100%

**Substantial quantitative reporting around:** completer surveys, employer surveys, edTPA, Praxis pass rates, hiring/licensure outcomes.

---

## ACBSP Accreditation — School of Business

School-level page covering all ACBSP-accredited business programs. Contains downloadable PDFs of program results (enrollment, retention, graduation rates, student satisfaction) for FY2022–2024. School-level aggregate data not available elsewhere on the site.

No images captured yet.

---

## CAHIIM Accreditation — B.S. Health Information Management

Program-level accreditation page. Notable for containing one of the few explicit time-to-degree numbers WGU publishes anywhere:

- **61% of graduates complete the degree in 36 months or less**
- Program: 36 courses, $4,210/term
- Graduates eligible to sit for RHIA and RHIT certification exams
- CAHIIM requires annual program assessment reports (additional data may exist via CAHIIM directly)

No images captured yet.

---

## CAE-CDE Program Designation — B.S. Cybersecurity and Information Assurance

NSA/DHS Center of Academic Excellence in Cyber Defense Education designation page. Expected to cover which knowledge units (KUs) map to the designation and what the credential signals about curriculum rigor. Page content not yet reviewed — no summary in the manifest.

No images captured yet.

---

## Files

```
outcomes/
  README.md                                      ← this file
  outcomes_links.json                            ← structured index of all pages with why field
  bscs/
    cs-program-results.jpg                       ← ABET Program Results chart
    cs-program-assessment-results.webp           ← ABET Program Assessment Results chart
  bscsia/
    bscsia-program-results.webp                  ← ABET Program Results chart
    program-assessment-results-bscsia.webp       ← ABET Program Assessment Results chart
  caep/
    completer-caep.webp                          ← CAEP Measure 1: Completer effectiveness
    employers-survey.webp                        ← CAEP Measure 2: Employer/stakeholder satisfaction
    edtpa-caep.webp                              ← CAEP Measure 3: edTPA pass rates
    capstone-caep.webp                           ← CAEP Measure 3: Capstone outcomes
    dt-measure-caep.webp                         ← CAEP Measure 3: Demonstration teaching
    dt-final-caep.webp                           ← CAEP Measure 3: Final demonstration results
    hiring-rates-caep.webp                       ← CAEP Measure 4: Hiring outcomes
    praxis-pass-rates-caep.webp                  ← CAEP Measure 4: Praxis pass rates
    measure-caep.webp                            ← CAEP overall measures summary
```

Images captured 2026-03-19.
