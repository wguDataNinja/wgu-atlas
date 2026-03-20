# Raw Catalog Analysis — Student-Use Perspective

Source: `~/Desktop/WGU-Reddit/WGU_catalog/data/raw_catalog_texts/catalog_2026_03.txt`
(pdfplumber extraction of `catalog-march-2026.pdf`)
Produced: 2026-03-20
Purpose: Homepage and product-design context — understanding what Atlas improves over the raw catalog

---

# Catalog structure relevant to students

The 2026-03 catalog is a 324-page PDF extracted to continuous text. It has five major sections relevant to students:

1. **Admissions / State Regulatory / Tuition / Academic Policies** (~pp. 15–62) — institutional boilerplate
2. **Academic Programs** (~pp. 62–232) — one entry per degree, organized by school
3. **Program Outcomes** (~pp. 233–258) — all outcomes for all degrees, in a single separate section
4. **Course Descriptions** (~pp. 259–323) — all course descriptions, in a single alphabetical list
5. **Instructor Directory** (~p. 324) — faculty listing

The critical structural fact: **the catalog splits degree information across three separate sections**. A student reading about a degree in Section 2 cannot see its outcomes or course descriptions without physically turning to Section 3 or Section 4. There is no cross-referencing, no linking, and no consolidation.

---

# What a degree entry actually gives the student

Using BSCS (B.S. Computer Science) as the reference example (catalog pp. 137–138, text lines ~4905–4954).

**What is present:**

- **Program name:** Plain heading — "Bachelor of Science, Computer Science"
- **Description:** 3–4 sentence paragraph. Example: *"The Bachelor of Science in Computer Science prepares students for a career in the high demand field of Computer Science. Upon program completion, students will apply their learned knowledge and skills in the designing, developing and optimizing of systems..."*
- **Course roster:** A flat table with four columns: `CCN` · `Course Number` · `Course Description` (title only, not description text) · `CUs` · `Term`
- **Term grouping:** Implicit only — each row has a Term number (1–9) but there are no explicit term-group headers separating the rows. It is one continuous table sorted by term.
- **CUs per course:** Yes, shown per row
- **Degree total CUs:** One line at the end: `BSCS 202412 Total CUs: 117` — this is the 2024-12 edition value; the current program is 123 CUs. No explanation of the discrepancy.
- **Program code:** Only embedded in the total CUs line (`BSCS 202412`) — not labeled or called out
- **School:** Only inferrable from the surrounding section header ("School of Technology Programs"). Not labeled within the entry itself.

**What is absent:**

- No outcomes (located ~95 pages later in a separate section)
- No course descriptions (located ~120 pages later in alphabetical order)
- No program code prominently labeled
- No first-offered date
- No CU history
- No college/school renaming history
- No retirement status or historical context of any kind
- No program guide link, no outcomes page link, no accreditation reference
- No sidebar, no "see also," no curated next-step material

**Extraction quality note:** The roster table extracts as continuous flat text. Course titles that span two lines in the PDF sometimes break mid-title in the extracted text (e.g., `D459 Introduction to Systems Thinking and` / `Applications` on the next line). Even in the original PDF the information is a static table — not interactive, not linked.

---

# What comparing two degrees is like from the raw catalog

To compare BSCS vs BSCSIA (Cybersecurity) a student would need to:

1. Find BSCS (p. 137). Read its roster. Manually note or copy all 37 course codes and titles.
2. Turn to BSCSIA (p. 141). Read its roster. Manually note all 38+ course codes and titles.
3. Manually cross-reference the two lists by course code to identify shared and unique courses.
4. Turn to Program Outcomes (p. 233) and find both degree names in the long bulleted section to compare outcomes — impossible to do simultaneously with the roster pages.

**Friction points:**

- Two rosters on different pages with no visual alignment
- No shared-course count or overlap signal anywhere in the document
- Course descriptions not inline — requires a separate lookup for every course
- Outcomes in a completely separate section with no cross-reference
- The CCN column (`ICSC 2211`) is present but not meaningful to most students; the usable code (`D684`) is the second column
- Total CU counts present but no breakdown of shared vs. unique

The comparison task is genuinely very hard using only the catalog. A motivated student needs significant manual effort or a second screen with the PDF open at two positions simultaneously.

---

# How outcomes are separated from degree pages

Program Outcomes is an entirely separate section beginning on page 233 — approximately 95 pages after the first program entry, and 95+ pages after the BSCS entry on p. 137.

The section is organized by school and degree name, in the same order as the Academic Programs section. Each degree gets a plain heading followed by a bulleted list of outcomes. For BSCS, the outcomes appear at text lines ~8167–8177 — roughly 3,200 lines after the program entry at lines 4905–4954.

**There is no reference within the program entry pointing to the outcomes section, and no reference within the outcomes section pointing back to the program entry.**

To read a degree's roster and its outcomes together, a student must navigate between p. 137 and p. 243 — over 100 pages apart — with no cross-reference in either direction.

---

# How course descriptions are separated from degree rosters

Course Descriptions occupy pages 259–323. They are sorted **alphabetically by course code** (C-codes first, then D-codes), not by program or by term.

For BSCS, the 37 course codes span the full range from `C458` to `D687`. To understand what any one course does, a student must:

1. Note the course code from the roster (e.g., `D684`)
2. Turn to the Course Descriptions section (~p. 259)
3. Find "D684" in the alphabetical list (well into the D-code block)
4. Read the description there

This process must be repeated for every course of interest. For a 37-course program, it is up to 37 separate lookups across 65 pages of alphabetically sorted descriptions.

Course descriptions in the extracted text are dense single-paragraph continuous sentences, not formatted with headers. They extract cleanly but are visually undifferentiated from each other.

---

# What history/change context is and is not present

**Present:**
- The edition code embedded in the total CUs line (e.g., `BSCS 202412`) — tells a careful reader which edition the entry reflects, but is not labeled or explained
- A single CU total snapshot (e.g., `Total CUs: 117` for BSCS) — but the current program is 123 CUs; no explanation given

**Not present:**
- No first-offered date
- No retirement status or retired-program markers
- No history of prior CU totals
- No college/school naming history (e.g., no mention that BSCS moved from "College of Information Technology" to "School of Technology")
- No continuity or predecessor/successor program information
- No change-over-time section or changelog

A student reading the catalog has essentially zero historical context. Everything is presented as a current static snapshot.

---

# What official-resource context is and is not present

**Not present in program entries:**
- No program guide links
- No outcomes page links
- No accreditation references
- No licensure or regulatory links
- No "learn more" or "see also" references of any kind

**Elsewhere in the document:**
- The Admissions section (pp. 15–23) contains some URLs for state-specific licensure and regulatory information — but these are at the school level in an admissions context, not attached to individual degree entries

The catalog is a pure static disclosure document. It contains no resource curation layer of any kind.

---

# Main usability limitations of the raw catalog

1. **Tripartite split:** Every degree's complete picture — roster + outcomes + course descriptions — requires navigating three separate sections spread across ~90 pages. No way to see all three together.

2. **No comparison affordance:** Nothing in the catalog is designed for comparison. A student comparing two degrees must do so manually, with no overlap signals, no shared-course indicators, and no side-by-side view.

3. **Alphabetical course descriptions:** Descriptions sorted by code, not by degree. Up to 37 separate lookups required to understand the courses in a single program.

4. **Outcomes buried and disconnected:** Outcomes are 90+ catalog pages away from the program entry with no cross-reference in either direction.

5. **No program codes as navigation targets:** Program codes appear only embedded in the edition/CU line at the bottom of each entry — not labeled, not indexed, not usable for navigation.

6. **Static snapshot with no history:** No way to understand when a program was introduced, whether it changed, or what happened to a related prior program.

7. **No links, no sidebar, no curated context:** Even in PDF form, internal links are absent from program entries. No sidebar, no "see also," no next-step guidance.

8. **Extraction fragility:** Multi-line table cells in pdfplumber output sometimes split course titles across lines with no delimiter — affects automated parsing at those boundaries.

---

# What Atlas is clearly improving

1. **Consolidated program page:** Description + roster + outcomes on one page. What requires three-section navigation in the catalog is one scroll in Atlas.

2. **Term-grouped roster with inline links:** Catalog has a flat sorted table with no visual term separation. Atlas groups by explicit term headers and makes every course code a clickable link to the course detail page. The 37-lookup problem is eliminated.

3. **Inline outcomes:** Outcomes on the same page as the roster and description. In the catalog: 90+ pages away. In Atlas: zero distance.

4. **Compare tool:** The catalog provides no comparison affordance. Atlas provides side-by-side roster comparison with shared/unique course identification for curated pairs. This capability simply does not exist in the catalog format.

5. **History and change context:** Catalog shows only the current edition snapshot. Atlas shows first-offered date, CU history (with "was {n}" notation), school/college name changes, and retirement status — none derivable from a single catalog edition.

6. **Curated official resources:** Catalog embeds no resource links within program entries. Atlas's sidebar surfaces program guides, outcomes pages, accreditation, and licensure links — official context that students would otherwise have to find independently.

7. **Program code as navigation target:** In the catalog, the program code is an incidental string. In Atlas it is the URL slug and primary identifier — programs are directly addressable by code.

8. **Course descriptions inline:** Catalog requires up to 37 separate alphabetical lookups. Atlas links every roster course to a course detail page with the full description, history, and degree appearances.

---

# Recommended homepage implications

Understanding the raw catalog makes several Atlas capabilities meaningfully more impressive to communicate:

**Degree pages:** The catalog gives a flat table, a paragraph, and nothing else on the same page. Atlas consolidates description + term-grouped roster + outcomes + official resources in one view. The homepage should convey that Atlas is a structured, navigable version of something that is otherwise flat and fragmented.

**Compare:** The catalog has no comparison concept. A student comparing two degrees faces a manual, multi-page, error-prone task. Atlas does it in two clicks. This is the most under-sold capability on the current homepage — the catalog context makes the value obvious.

**Course pages:** Up to 37 separate lookups per degree in an alphabetical section in a different part of the document. Atlas makes every course directly accessible from the roster. This eliminates a structural limitation of the source format.

**History/change context:** The catalog is a single static snapshot. It cannot tell a student when a program was introduced, whether CUs changed, or what happened to a prior degree. Atlas's history context is entirely additive — information with no equivalent in the source document.

**Relevant resources:** The catalog contains no curated resource links near program entries. Atlas's sidebar surfaces official WGU materials that are otherwise discoverable only by navigating wgu.edu independently. For a student doing research, the sidebar may be the fastest path to official supporting materials that the catalog itself doesn't provide.
