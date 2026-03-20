# WGU Public Site Student Experience — Degree Exploration Baseline

Reference capture date: 2026-03-20
Status: **in progress — initial baseline only**
To be expanded in the next design/documentation session.

Related docs:
- `catalog_raw_analysis.md`
- `source_vs_atlas_program_entry.md`
- `compare_page.md`
- `homepage_design_session_2026-03.md`

---

## Important framing note

The raw WGU catalog is not the primary way most students first explore WGU degrees, courses, and options.

Students typically start on WGU's public website — the official marketing and navigation surface at wgu.edu — not with a PDF catalog.

This doc exists to capture the **official web exploration baseline** so Atlas can later be evaluated against both:

1. The raw WGU catalog (covered in `catalog_raw_analysis.md` and `source_vs_atlas_program_entry.md`)
2. The public WGU website student experience (this doc)

Until both baselines are documented, we only have half the picture of what Atlas improves on.

---

## 1. Purpose of this doc

This document preserves how students actually encounter and explore WGU on the public website, as distinct from the raw catalog experience.

Its goal is to capture:
- the official navigation and degree-discovery flow
- what a student sees before they ever open the catalog
- how WGU publicly presents program options, course information, and official supporting resources
- where that experience is strong or weak as a student research surface

This is a product-argument artifact and a planning baseline, not an implementation spec.

---

## 2. Why the public site baseline matters

Most Atlas comparison work to date has benchmarked against the raw catalog.

That benchmark is valid and important. But it understates Atlas's value if the public-site experience is also weak.

If wgu.edu's degree-exploration surface is:
- marketing-first rather than reference-first
- funnel-oriented rather than browse-oriented
- poor at supporting comparison, course exploration, or outcome visibility

...then Atlas's claim is not just "better than the catalog" but "better than the student's default research experience."

That is a stronger and more truthful claim.

Conversely, if the public site is actually a strong exploration surface, that changes what Atlas needs to offer to stand out.

This doc should answer which of those is true.

---

## 3. Global navigation baseline

### Observed top navigation

Current wgu.edu top nav (observed):
- Online Degrees
- About WGU
- Tuition & Financial Aid
- Admissions & Transfers
- Student Login
- More

### What this tells us now
- Degree exploration is the first nav item — it is clearly the primary entry for prospective students.
- The nav does not lead with schools or a degree index — it leads with a category-gated entry.

### To document next session
- Dropdown/hover/click behavior for each nav item
- Whether nav paths are marketing-first or reference-first
- What degree exploration paths are emphasized vs buried
- Whether "More" reveals additional degree-related navigation

---

## 4. Online Degrees entry flow

### Observed behavior (confirmed)

Clicking "Online Degrees" in the top nav forces a category selection before navigating to a degree surface.

Observed options presented:
- Business
- Education
- Technology
- Health & Nursing
- Courses and Certificates
- All Degrees
- Explore Your Options

### Initial analysis

- Degree exploration begins through high-level marketing/navigation buckets, not through a structured degree index.
- Students are being routed through a category choice before seeing any organized degree information.
- This is a funnel entry pattern, not a browse entry pattern.
- A student who does not know which bucket their program of interest belongs to must either guess or use "All Degrees" / "Explore Your Options."

This is an important baseline for Atlas comparison. Atlas allows open browsing and search without requiring prior category commitment.

### To document next session
- Where each option (Business, Education, etc.) actually leads
- Whether the destination is a school page, a program browse page, or a marketing page
- Whether the overall path from top nav to a specific program is smooth or friction-heavy
- Whether the experience is consistent across categories

---

## 5. All Degrees / Explore Your Options baseline

**Stub — to be documented next session.**

These two options appear to be the least-funnel-gated paths in the Online Degrees menu.

Next session should document:
- What "All Degrees" looks like — is it a true browse surface or a filtered landing page?
- What "Explore Your Options" leads to — is it a quiz/recommendation flow or a structured index?
- Whether either surface supports genuine scanning and comparison
- Whether filtering, sorting, or search is available
- Whether the student can understand degree options without clicking into each one individually
- How the surface compares to what a student could do in Atlas

---

## 6. School/college-level public pages

**Stub — to be documented next session.**

The Online Degrees menu presents degrees organized into these categories:
- Business
- Education
- Technology
- Health & Nursing
- Courses and Certificates

Next session should document how WGU presents each of these categories by visiting the corresponding pages and capturing:
- Are these true browse hubs or mostly promotional landing pages?
- Do they list actual programs clearly, or lead with testimonials, outcomes promises, and hero imagery?
- How easily can a student understand their options from these pages without clicking into each degree individually?
- Whether these map clearly to Atlas's school/college structure

---

## 7. Official program page structure

**Stub — to be documented next session.**

The official WGU website includes individual program pages for each degree.

The public degree hub is confirmed at:

> https://www.wgu.edu/online-degree-programs.html

The official site presents online degrees and programs as a browse/filter surface, based on current web confirmation.

Next session should document one or more representative official WGU degree pages (e.g., the BSCS or a comparable program) and capture:
- Hero structure and top-of-page identity
- Whether the full course roster is visible
- Whether program outcomes are visible on the page
- Whether program guides or related resources are surfaced near the program description
- Whether official-resource context (outcomes, accreditation, licensure) is attached near the degree
- How much of the page is marketing-oriented vs academic-detail-oriented
- How this compares to the same program's Atlas page

---

## 8. Official compare baseline

**Stub — to be documented next session.**

Atlas offers a purpose-built degree comparison tool (`/compare`) that has no equivalent in the raw catalog.

Next session should answer:
- Whether WGU's public site offers any direct degree comparison tool
- What a student must do on wgu.edu if they want to compare two related degrees
- Whether the official site supports any kind of side-by-side or overlap view
- How Atlas Compare differs from that baseline experience

If the public site has no comparison surface, that further strengthens the case for Atlas Compare as a unique capability — not just relative to the catalog, but relative to the student's full official research experience.

---

## 9. Official course-discovery baseline

**Stub — to be documented next session.**

A key Atlas feature is that every course code in a program roster is a link to a course detail page.

Next session should document how a student discovers course-level information on the official WGU site:
- Whether courses are publicly visible from program pages
- Whether individual course-level pages exist on wgu.edu
- How a student learns what a course in a degree actually covers
- Whether the course list on an official program page is scannable and complete or abbreviated

---

## 10. Official-resource discovery baseline

**Stub — to be documented next session.**

Atlas surfaces official WGU resources (program guides, outcomes, accreditation, etc.) directly on program pages via the Relevant Resources sidebar.

Next session should document how a student finds these materials on the official site:
- Program guides — are they easy to locate from degree pages?
- Learning outcomes — are they visible on or near degree pages?
- Accreditation — is accreditation status and detail easy to find?
- Licensure and disclosure — are licensure disclosures visible and accessible?
- Admissions and program-specific requirements — how easy to find from the degree page?
- Other official supporting materials — how are they organized?

---

## 11. WGU public-site design posture

**Stub — to be documented next session.**

Once the public-site experience has been observed across several surfaces, this section should characterize the official site in product terms:

- Marketing-first vs reference-first
- Exploration-friendly vs funnel-heavy
- Comparison-friendly vs comparison-poor
- Structured vs scattered
- Student-research-oriented vs prospective-student-conversion-oriented

That characterization will be the clearest statement of what Atlas improves on relative to the student's actual starting point.

---

## 12. Atlas implications

**Stub — to be completed after baseline is documented.**

Once the public-site baseline is fully captured, this section should explain how Atlas improves on the official public exploration experience — not just the raw catalog.

The key questions this section will answer:
- What can a student do in Atlas that they cannot easily do on wgu.edu?
- What does Atlas make faster or clearer?
- Where does Atlas provide reference depth that the public site does not offer?
- How does the Atlas homepage claim need to change once both baselines are understood?

---

## 13. Open questions for next session

- Where do "Business," "Education," "Technology," "Health & Nursing," and "Courses and Certificates" lead from the Online Degrees menu?
- What does "All Degrees" look like as a surface?
- What does "Explore Your Options" lead to?
- How many clicks does it take to reach a specific degree page from the top nav?
- What does an official WGU degree page contain near the top of the page?
- Is the full course roster visible on official program pages?
- Are learning outcomes visible on official program pages?
- Are program guides easy to find from within a program page?
- Is there any official compare flow or side-by-side degree comparison on wgu.edu?
- What is the course-level exploration baseline on the public site?
- Are official-resource links (guides, accreditation, licensure) surfaced near degree information or buried elsewhere?

---

## 14. Session handoff note

This doc is intentionally partial.

It captures confirmed observations from the current session (global nav structure, Online Degrees dropdown options, and the existence of the public degree hub at wgu.edu/online-degree-programs.html) and stubs the remaining analysis for the next session.

Next session should continue documenting the official WGU public-site student journey by following the key entry flows and capturing what a student actually encounters.

Homepage design work should proceed with this baseline in mind. Atlas should ultimately be positioned not only against the raw catalog, but against the full official student research experience — because that is the experience Atlas is actually replacing.
