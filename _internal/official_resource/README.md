# Official Resource Module — Continuity Doc

_Last updated: 2026-03-20. Bring to any new session for this module._

---

## Module purpose

This module owns the official-resource enrichment layer for WGU Atlas.

Its job: identify, classify, and attach official WGU pages and media to Atlas school and degree surfaces, so a student exploring Atlas can find concrete official context — accreditation, licensure, specializations, outcomes — without navigating the full WGU sitemap themselves.

The standard for inclusion: **does this source add concrete value to a student exploring this entity?**

This module does not own catalog facts, course data, or Reddit/community enrichment.

---

## In-scope source families

| Source family | Status | Notes |
|---|---|---|
| Program guides | Done — not in active queue | Already harvested at scale and live on most degree pages. Small cleanup audit remaining where coverage suspected missing. |
| Outcomes / assessment pages | Identified; completeness audit remaining | High-value, rare. Strong set already found. Worth checking for remaining gaps against sitemap universe. |
| Accreditation / designation pages | Identified; completeness audit remaining | Several important ones found. Completeness check against sitemap still warranted. |
| Regulatory / licensure / disclosure | **Next — Tier 1** | Highest unfinished priority. Teaching licensure, nursing licensure, NCLEX, Praxis, clinicals, state-approval/disclosure pages. Enrollment-critical constraints students need before choosing a program. |
| Specialization / track / variant pages | **Next — Tier 2** | Most scalable next degree-enrichment pass. Explains real choices between related degree options. |
| School governance / context pages | Next — Tier 3 | School-page completion. Four school governance/context pages (Business, Technology, Education, Health). Likely useful where sitemap school-level coverage is thin. |
| Program landing pages | Selective mining only | Useful only when they contain extractable concrete facts (course count, cost framing, clinicals, state restrictions). Not a systematic pass. |
| Official WGU YouTube | Deferred — after sitemap passes stable | School-branded, field/workforce material. Keep separate from Career Services. Do not broadly surface until attachment model is clear from sitemap/page-class work. |
| Career Services YouTube | Deferred | Only domain/field/role context qualifies. Aggressive filtering required. Hold until Official WGU YouTube is producing value. |
| Reddit / community | Out of scope for this module | Course-page layer only. Handled separately. |

---

## Current state

- Program guides: live on most degree pages. Not in active queue.
- Outcomes / accreditation: strong set identified (CS, cybersecurity, HIM, ACBSP, CAEP). Completeness audit against `official_context_manifest_phase1.csv` not yet done.
- Regulatory / licensure: candidates known conceptually (NCLEX, Praxis, state licensure, clinicals). Candidate queue artifact not yet built.
- Specialization / track: known examples (MS Data Analytics, MS Accounting, MS Software Engineering, MS Marketing). Candidate queue not yet built.
- School governance: not yet reviewed.
- YouTube: raw title lists exist. Classification and attachment model not yet resolved.

---

## Locked assumptions

- Density rule: **1–3 strong links per surface.** No sitemap dumps.
- Source provenance separation: official resources must be clearly distinguished from Atlas interpretation (DECISIONS §7).
- Page-level targeting: school pages show sources relevant across the school or school-wide field areas; degree pages show sources relevant to that specific degree. Do not attach degree-specific content at the school level.
- Program guides are not in the active review queue.
- Reddit/community is out of scope for this module.
- YouTube stays downstream of sitemap/page-class work — do not broaden YouTube attachment until page-class work has stabilized the attachment model.
- Career Services YouTube requires aggressive filtering; defer until Official WGU YouTube is producing clear value.

---

## Current open questions

1. **Regulatory/licensure attachment level**: Some licensure pages (e.g., teaching state licensure overview) may be broad enough for a school-level attachment rather than degree-level. Rule of thumb: if it spans many degrees in a school, it goes on the school page; if it is degree-specific (e.g., NCLEX for BSN), it goes on the degree page.

2. **Outcomes/accreditation completeness**: After the candidate queue for regulatory/licensure is built, we need a structured check of the outcomes/accreditation set against the sitemap universe. Unknown how many gaps remain.

3. **YouTube attachment model**: Will become clearer after the sitemap/page-class passes. Do not try to resolve this before then.

---

## Next planned tasks

1. **Regulatory / licensure / disclosure candidate queue** — build a curation-ready artifact (~10–20 candidates) with: title, URL, source class, target surface, student value rationale, recommendation (keep / skip / needs review). Pull from `data/enrichment/official_context_manifest_phase1.csv`.
2. **Outcomes + accreditation completeness audit** — check identified set against sitemap universe; close gaps while cheap.
3. **Specialization / track / variant candidate queue** — same curation-ready format as above.
4. **School governance / context pages review** — four pages; decide school-page attachment suitability.
5. **Official WGU YouTube classification** — when attachment model is clearer from above work.
