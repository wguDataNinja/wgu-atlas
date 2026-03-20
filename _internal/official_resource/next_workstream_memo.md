# Official Resource — Next Workstream Memo

_Date: 2026-03-20_

---

## 1. What the official-resource layer is for

Atlas's job is to make canonical WGU information easier for students to use than long catalog PDFs. The official-resource layer is how Atlas surfaces supporting official WGU pages and media alongside catalog facts.

For a student exploring a school or degree, this layer answers the questions the catalog doesn't easily answer:
- What accreditation or designation does this program carry?
- Does this degree lead to a licensure exam, and are there state restrictions?
- What specializations or tracks exist, and how do they differ?
- What do outcomes or assessment results look like?

The layer is not a link collection. It is curated, entity-scoped context that adds something the catalog itself does not already provide.

---

## 2. Candidate source classes

| Source class | Student value | Likely page level | Priority |
|---|---|---|---|
| Program guides | High — curriculum and structure detail | Degree | **Done** — not in active queue |
| Outcomes / assessment pages | High — rare, unusually information-dense | Degree | **Now** — completeness audit |
| Accreditation / designation pages | High — enrollment-relevant credential signal | Degree, School | **Now** — completeness audit |
| Regulatory / licensure / disclosure pages | Very high — enrollment-critical constraints; state restrictions, exam requirements | Degree (mostly), School (broad cases) | **Next — Tier 1** |
| Specialization / track / variant pages | High — explains real degree-choice differences | Degree | **Next — Tier 2** |
| School governance / context pages | Medium — school identity, governance, mission | School | Next — Tier 3 |
| Program landing pages | Variable — only when concrete facts are present | Degree | Selective mining only |
| Official WGU YouTube | Medium-high — field/workforce context, school-branded | School first, then degree | After sitemap passes stable |
| Career Services YouTube | Low-medium — only domain/role context qualifies | School (narrow cases) | Defer until Official YT producing value |

---

## 3. Best next bounded official-resource workstream

**Regulatory / licensure / disclosure pages pass.**

Scope: identify, classify, and make attachment decisions for official WGU pages covering:
- Teaching state licensure
- Nursing state licensure
- Clinical/practicum requirements
- NCLEX (nursing board exam)
- Praxis (teaching certification exam)
- Explicit certification, state-approval, exam-eligibility, or disclosure pages

Input: `data/enrichment/official_context_manifest_phase1.csv`

Output: `_internal/official_resource/regulatory_candidate_queue.md` — a curation-ready artifact, not just a URL list.

Why this is first:
- Highest concrete student impact of any remaining source class
- Enrollment-critical (state restrictions, exam eligibility are must-know before choosing a program)
- Easy to justify in sidebar — very low risk of misclassification
- Narrowly scoped — does not require code changes or new attachment surfaces
- Expected candidate pool is small (~10–20 pages)

---

## 4. Attachment / surfacing model

**School pages should show:**
- School-level accreditation (ACBSP for Business, CAEP for Education)
- School governance / context pages
- Official WGU YouTube content that is school-branded or covers the broad field (e.g., CS field, health field)
- Broad regulatory context that spans many degrees in the school (e.g., WGU teacher licensure overview on the Education school page)

**Degree pages should show:**
- Program-specific outcomes/assessment pages
- Degree-specific accreditation or designation
- Regulatory/licensure/disclosure pages specific to that degree (e.g., NCLEX on BSN, Praxis on MAT)
- Specialization/track/variant pages for that degree
- Program guides (already live)
- Degree-adjacent Official WGU YouTube when classification and attachment model are ready

**Not attaching yet:**
- Career Services YouTube — too generic; most content is employer-session or job-search advice
- Reddit/community — course-page layer only; out of scope for this module
- Program landing pages broadly — selective extraction only where concrete facts are present
- Course pages — not yet in scope for official enrichment

**Density rule:** 1–3 strong links per surface. Never dump sitemap subsets.

**YouTube note:** YouTube attachment belongs explicitly after the sitemap/page-class passes have clarified what the attachment model looks like in practice. Do not try to resolve this before then.

---

## 5. What phase 1 should exclude

These are tempting but intentionally out of scope for now:

- **Reddit/community enrichment** — course-page layer only; not part of this module
- **Career Services YouTube** — defer until Official WGU YouTube is producing clear value; most Career Services content fails the student-usefulness test for Atlas
- **Program landing pages as a systematic pass** — only mine selectively when a page is already in scope for another reason
- **Course pages** — not yet in scope for official enrichment; future work
- **New UI surfaces** — the degree-page sidebar already exists; no new product surfaces are needed to execute this workstream
- **Broad YouTube classification** — wait for attachment model clarity; do not front-run it

---

## 6. Recommended ranking inside the official-resource layer

1. **Regulatory / licensure / disclosure pass** — enrollment-critical, bounded, no dependencies
2. **Outcomes + accreditation completeness audit** — high-value, likely cheap to close; keep adjacent to Tier 1, not deferred
3. **Specialization / track / variant pass** — most scalable next degree-enrichment class
4. **School governance / context pages** — school-page completion; small number of pages to review
5. **Official WGU YouTube classification** — after attachment model is clear from sitemap/page-class work
6. **Career Services YouTube** — after Official WGU YouTube is producing value
7. **Selective mining of program landing pages** — ongoing, low-urgency, only for concrete facts

---

## 7. Single best next bounded task

**Build the regulatory/licensure/disclosure candidate queue.**

This is a curation-ready artifact, not just a URL discovery exercise. For each candidate, record:

| Field | Notes |
|---|---|
| Title | Page title or inferred label |
| URL | Full URL from sitemap manifest |
| Source class | e.g., `regulatory/licensure`, `disclosure`, `exam-eligibility` |
| Target surface | `school` or `degree` (and which degree if specific) |
| Student value | One-sentence rationale: what does this add that the catalog doesn't? |
| Recommendation | `keep` / `skip` / `needs-review` |

Input: `data/enrichment/official_context_manifest_phase1.csv`
Output: `_internal/official_resource/regulatory_candidate_queue.md`
Target size: ~10–20 candidates

This artifact is immediately usable for curation decisions when complete.
