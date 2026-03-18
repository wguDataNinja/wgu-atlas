# Compare Degrees — Data Audit
**Date:** 2026-03-18
**Scope:** Active degree corpus (114 programs), compare data model, naming patterns, pair overlap analysis
**Status:** Audit/reporting pass only — no production changes made

---

## 1. Data Model Inventory

### Fields available for all active degrees (from `programs.json`)

| Field | Availability | Notes |
|---|---|---|
| `program_code` | Always present | Stable unique identifier |
| `canonical_name` | Always present | Full degree title from catalog body heading |
| `status` | Always present | ACTIVE / RETIRED |
| `school` | Always present | Current canonical school name |
| `degree_headings` | Always present | 1–2 headings per program; usually matches canonical_name |
| `first_seen` | Always present | Edition date of first catalog appearance |
| `last_seen` | Always present | Edition date of most recent appearance |
| `edition_count` | Always present | Count of catalog editions present in |
| `version_changes` | Always present | Number of curriculum version bumps observed |
| `cus_values` | Always present | Array of CU totals seen across editions; use latest |
| `colleges` | Always present | All historical school names for this program |

### Fields available from `program_enriched.json` (114 active programs)

| Field | Availability | Notes |
|---|---|---|
| `roster` | 113/114 (99%) | Ordered course list with term, code, title, CUs. ENDELL is the only program with an empty roster (0 courses). |
| `description` | Usually present | Official catalog description text |
| `outcomes` | Partial (~74/114) | Program Learning Outcomes; 40 programs have empty outcomes arrays |
| `roster_source` | Always present | Edition the roster was extracted from (all 2026-03) |

### Fields that are pilot-only or derived

| Field | Status | Notes |
|---|---|---|
| `index_name` (track label) | Pilot-only | Curated in `families.ts` for 5 programs only. Not in `programs.json`. Would need curation or pipeline change to expand. |
| `compare_note` | Pilot-only | Free-text compare framing; exists only on the 2 pilot `ProgramFamily` entries |
| `degree_level` (display label) | Derived | `classifyDegreeLevel()` in `programs.ts` — heuristic, name-prefix based |
| `family_id` | Pilot-only | Curated `PILOT_FAMILIES` in `families.ts`; 5 of 114 programs covered |
| `jaccard_overlap` | Computed on demand | Not stored; computed at render time from roster codes |

### Fields missing or unreliable

| Gap | Detail |
|---|---|
| Track disambiguation | Only the 5 pilot programs have `track_labels`. All other same-name programs (MEDETID group, BSSWE group) have no disambiguation signal in the data layer. |
| Degree level stored | Level is always derived from `canonical_name` prefix. This is reliable for standard degrees but breaks for pathway programs (see §5). |
| Course CUs in compare payload | Present in `roster` entries and passed through `ComparePayload`; reliable. |
| Term ordering | Present in `roster` as integer term numbers; reliable. |
| Course titles in compare | Sourced from `roster.title` fields; these match 2026-03 catalog extraction and are reliable. |

---

## 2. Active Degree Universe by College + Level

**Total active programs: 114**

### School of Technology

| Level | Count | Potential pairs |
|---|---|---|
| Bachelor's | 13 | 78 |
| Master's | 12 | 66 |

**Bachelor's (13):**
BSCNE, BSCNEAWS, BSCNEAZR, BSCNECIS, BSCS, BSCSIA, BSDA, BSIT, BSSWE, BSSWE_C,
MSCSUG\*, MSITUG\*, MSSWEUG\*
_\* Pathway programs — classified as Bachelor's by name prefix but semantically distinct (see §5)_

**Master's (12):**
MSCSAIML, MSCSCS, MSCSHCI, MSCSIA, MSDADE, MSDADPE, MSDADS, MSIT, MSITPM,
MSSWEAIE, MSSWEDDD, MSSWEDOE

---

### School of Education

| Level | Count | Potential pairs |
|---|---|---|
| Bachelor's | 16 | 120 |
| Master's | 23 | 253 |
| Cert/Endorsement | 7 | 21 |

**Bachelor's (16):**
BAELED, BAESELED, BAESMES, BAESSESB, BAESSESC, BAESSESE, BAESSESP, BAESSPEE, BAESSPMM,
BASPEE, BASPMM, BSMES, BSSESB, BSSESC, BSSESE, BSSESP

**Master's (23):**
MAELLP12, MAMEK6, MAMEMG, MAMES, MASEMG, MASESB, MASESC, MASESE, MASESP,
MATEES, MATELED, MATMES, MATSESB, MATSESC, MATSESE, MATSESP, MATSPED, MATSSES,
MEDETID, MEDETIDA, MEDETIDK12, MSCIN, MSEDL

**Cert/Endorsement (7):**
ENDELL (0 courses), ENDMEMG, ENDSEMG, ENDSESB, ENDSESC, ENDSESE, ENDSESP

---

### School of Business

| Level | Count | Potential pairs |
|---|---|---|
| Bachelor's | 10 | 45 |
| Master's | 11 | 55 |

**Bachelor's (10):**
BSACC, BSC, BSFIN, BSHA, BSHR, BSITM, BSMGT, BSMKT, BSSCOM, BSUXD

**Master's (11):**
MACCA, MACCF, MACCM, MACCT, MBA, MBAHA, MBAITM, MSHRM, MSMK, MSMKA, MSML

---

### Leavitt School of Health

| Level | Count | Potential pairs |
|---|---|---|
| Bachelor's | 8 | 28 |
| Master's | 10 | 45 |
| Post-Master's Cert | 4 | 6 |

**Bachelor's (8):**
BSHHS, BSHIM, BSHS, BSNPLTR, BSNU, BSPH, BSPNTR, BSPSY

**Master's (10):**
MHA, MPH, MSNUED, MSNUFNP, MSNULM, MSNUNI, MSNUPMHNP, MSRNNUEDGR, MSRNNULMGR, MSRNNUNIFGR

**Post-Master's Cert (4):**
PMCNUED, PMCNUFNP, PMCNULM, PMCNUPMHNP

---

### Summary counts

| College | Bachelor's | Master's | Other | Total |
|---|---|---|---|---|
| Technology | 13 | 12 | — | 25 |
| Education | 16 | 23 | 7 | 46 |
| Business | 10 | 11 | — | 21 |
| Health | 8 | 10 | 4 | 22 |
| **Total** | **47** | **56** | **11** | **114** |

---

## 3. Naming Pattern Audit

### Pattern 1 — Specialization suffix (` - [Name]`): ~24 programs

The ` - ` separator is used to append a track or specialization name onto a base degree title. These are the cleanest cases for compare: the shared prefix is the family identifier and the suffix is the differentiator.

**Examples:**
- `Master of Science, Data Analytics - Data Engineering` (MSDADE)
- `Master of Science, Data Analytics - Data Science` (MSDADS)
- `Bachelor of Science, Cloud and Network Engineering - Amazon Web Services` (BSCNEAWS)
- `Master of Science, Software Engineering - AI Engineering` (MSSWEAIE)
- `Master of Science, Software Engineering - DevOps Engineering` (MSSWEDOE)
- `Master of Science in Accounting, Auditing Specialization` (MACCA)

**UI handling:** Currently fine for MSDA tracks because `index_name` is curated. For the rest (BSCNE, MSSWE, MSCS, MSACC, MSMK families), the ` - [suffix]` part distinguishes them but no `track_labels` are defined — the full canonical_name would appear in both the selector and header cards without abbreviation.

---

### Pattern 2 — "in X" subject specialization: ~26 programs

Almost entirely Education. The subject field after "in" carries all the differentiation.

**Examples:**
- `Bachelor of Arts, Educational Studies in Secondary Biological Science Education` (BAESSESB)
- `Master of Arts in Teaching, Science Education (Secondary Biology)` (MATSESB)
- `Master of Science in Accounting, Auditing Specialization` (MACCA)

**UI handling:** Long names (up to 92 characters). The differentiating word is often near the end of a very long string. In the compact CompareSelector bar and column headers, this causes truncation exactly where disambiguation is needed.

---

### Pattern 3 — Parenthetical qualifier `(...)`: ~20 programs

Three distinct uses of parentheses in canonical names:

**a) Pathway identifiers:**
- `Bachelor of Science, Computer Science (BSCS to MSCS)` (MSCSUG)
- `Bachelor of Science, Information Technology (BSIT to MSIT)` (MSITUG)

**b) Degree-pathway context:**
- `Bachelor of Science, Nursing - Prelicensure (Nursing)` (BSNPLTR)
- `Bachelor of Science, Nursing - Prelicensure (Pre-Nursing)` (BSPNTR)

**c) Grade-level / population qualifiers:**
- `Master of Arts in Teaching, Science Education (Secondary Biology)` (MATSESB)
- `Post-Master's Certificate, Nursing - ... (Post-MSN)` (PMCNUPMHNP)

**UI handling:** Pathway programs (MSCSUG, MSITUG, MSSWEUG) appear in the Bachelor's pool because their canonical name starts with "Bachelor of Science" — but they are not comparable to regular BS degrees. The parenthetical makes the intent clear to a reader but is invisible to the current `classifyDegreeLevel()` heuristic.

---

### Pattern 4 — Identical canonical names (disambiguation crisis): 2 groups

**Group A — Software Engineering tracks (BSSWE vs BSSWE_C):**
Both programs have `canonical_name: "Bachelor of Science, Software Engineering"`. The current compare UI handles this only because `track_labels` is manually curated in `families.ts`. Without those labels, both sides of the compare would show the same name.

**Group B — Ed Tech (MEDETID, MEDETIDA, MEDETIDK12):**
All three share `canonical_name: "Master of Education, Education Technology and Instructional Design"`. There are no `track_labels` for these. In the current UI they would appear identically in any selector and produce headers that read the same on both sides. The differentiator is only in the program code (`A` = accelerated, `K12` = K-12 focus presumably).

**This is a hard blocker for any expansion that includes the Ed Tech family without prior curation.**

---

### Pattern 5 — BA vs BS splits for same subject: ~10 pairs

Education has parallel BA ("Educational Studies in X") and BS ("Science Education (X)") programs for the same subjects.

**Examples:**
- `Bachelor of Arts, Educational Studies in Secondary Biological Science Education` (BAESSESB) — 37 courses
- `Bachelor of Science, Science Education (Secondary Biological Science)` (BSSESB) — 41 courses
- Jaccard: 90%, 37 shared courses

These are structurally very similar programs (90% overlap) but the naming exposes no obvious relationship. "Educational Studies" vs "Science Education" reads as different products to a student.

---

### Pattern 6 — RN-to-MSN bridge programs: 3 programs

`MSRNNUEDGR`, `MSRNNULMGR`, `MSRNNUNIFGR` have 32–33 courses each (vs 14–15 for the BSN-to-MSN equivalents) because they include undergraduate bridge content. They share the same base specialization names but are structurally double-size rosters.

**UI handling:** A compare between `MSNUED` (15 courses) and `MSRNNUEDGR` (33 courses) would render an asymmetric three-lane view with the majority of content on the right side. The Jaccard is 45% — meaningful but the visual imbalance would be striking.

---

### Pattern 7 — MBA family: 3 programs

`MBA` (11 courses), `MBAHA` (9 courses), `MBAITM` (9 courses). The base MBA and its specializations share 8 courses, leaving 1–3 unique courses per program. These are very high overlap (67%) but very low differentiation — only 1–2 unique courses per variant. The compare output would read as "these are almost identical."

---

## 4. Pair Shape Audit

### Bucket A — Near-identical track/specialization variants (≥75% Jaccard)

These are the strongest compare candidates. Students face a clear binary/n-way choice.

| Pair | Jaccard | College | Level | Note |
|---|---|---|---|---|
| BSSWE vs BSSWE_C | 80% | Technology | Bachelor's | **Pilot pair.** Java vs C# track. Handled by existing `track_labels`. |
| BSCNE vs BSCNEAWS | 82% | Technology | Bachelor's | Base vs AWS specialization. Clean ` - ` suffix differentiation. |
| BSCNE vs BSCNEAZR | 82% | Technology | Bachelor's | Base vs Azure. Same structure. |
| BSCNEAWS vs BSCNEAZR | 79% | Technology | Bachelor's | AWS vs Azure. Pure cloud-vendor choice. |
| MSSWEAIE vs MSSWEDOE | 54% | Technology | Master's | SWE specialization pair. Lower than expected. |
| MSDADE vs MSDADS | 47% | Technology | Master's | **Pilot pair.** Data Engineering vs Data Science. |
| MACCA vs MACCM | 67% | Business | Master's | Accounting specialization pair. |
| MBA vs MBAHA | 67% | Business | Master's | MBA with/without Healthcare focus. |

---

### Bucket B — Related degrees with moderate overlap (25–74%)

Meaningful compare output; the shared core is real but not dominant. The "what's different" framing works well.

| Pair | Jaccard | College | Level | Note |
|---|---|---|---|---|
| BAESSESB vs BSSESB | 90% | Education | Bachelor's | BA "Educational Studies" vs BS "Science Ed" — same subject, parallel paths |
| MATSESB vs MATSESC | 90% | Education | Master's | MAT Science — Biology vs Chemistry. Clear sibling choice. |
| BAELED vs BAESELED | 89% | Education | Bachelor's | Elementary Ed vs Ed Studies in Elementary Ed |
| MEDETID vs MEDETIDA | 83% | Education | Master's | **Identical names** — disambiguation required before surfacing |
| MSRNNUEDGR vs MSRNNULMGR | 65% | Health | Master's | RN-to-MSN specialization pair |
| BSACC vs BSFIN | 54% | Business | Bachelor's | Accounting vs Finance — classic student choice |
| MSMK vs MSMKA | 57% | Business | Master's | Marketing Digital vs Analytics specializations |
| MSSWEAIE vs MSSWEDDD | 54% | Technology | Master's | SWE AI Engineering vs Domain Driven Design |
| MSCSCS vs MSCSHCI | 67% | Technology | Master's | CS Computing Systems vs Human-Computer Interaction |

---

### Bucket C — Low overlap (<25%) — likely not useful compare pairs

| Pair | Jaccard | College | Level | Note |
|---|---|---|---|---|
| BSDA vs BSCSIA | ~15% | Technology | Bachelor's | Data Analytics vs Cybersecurity — unrelated |
| BSPH vs BSPSY | <10% | Health | Bachelor's | Public Health vs Psychology — different domains |
| MSEDL vs MEDETID | <20% | Education | Master's | Educational Leadership vs Ed Tech — unrelated |
| MBA vs MSML | ~20% | Business | Master's | MBA vs Management & Leadership — adjacent but not track-related |
| MHA vs MPH | ~20% | Health | Master's | Healthcare Admin vs Public Health — different missions |

---

### Bucket D — Naming makes relation unclear (without context)

These are high-overlap pairs where the name gives a student no signal that they're choosing between variants of the same program.

| Pair | Jaccard | Issue |
|---|---|---|
| BAESSESB vs BSSESB | 90% | "Educational Studies in Secondary Biological Science" vs "Science Education (Secondary Biological)" — same thing, no apparent connection |
| BSSWE vs BSSWE_C | 80% | Both named "Bachelor of Science, Software Engineering" — only the code differentiates them |
| MEDETID vs MEDETIDA vs MEDETIDK12 | 83% | All three have the exact same canonical_name |
| BAELED vs BAESELED | 89% | "Elementary Education" vs "Educational Studies in Elementary Education" — near-synonymous to a student |

---

### Bucket E — Long names that will stress the UI

| Degree | Chars | Risk |
|---|---|---|
| BAESSPMM — "Bachelor of Arts, Educational Studies in Mild to Moderate Exceptionalities Special Education" | 92 | Will truncate in CompareSelector compact bar; column headers in three-lane view will overflow |
| PMCNUPMHNP — "Post-Master's Certificate, Nursing - Psychiatric Mental Health Nurse Practitioner (Post-MSN)" | 92 | Same |
| MSCSAIML — "Master of Science, Computer Science, Artificial Intelligence and Machine Learning" | 81 | Stressful in program headers |
| BAESSESB/BAESSESC/BAESSESE/BAESSESP — 78–79 chars each | 78–79 | Education BA family — all long |

**38 of 114 active programs have canonical names longer than 60 characters.** This is 33% of the corpus.

---

### Bucket F — Structural mismatch: UG-to-Graduate pathway programs

Three programs that classify as "Bachelor's" but are not standalone degrees:

| Code | Name | Actual purpose |
|---|---|---|
| MSCSUG | Bachelor of Science, Computer Science (BSCS to MSCS) | Pathway program — upper-division BSCS courses leading into MSCS |
| MSITUG | Bachelor of Science, Information Technology (BSIT to MSIT) | Same structure for BSIT → MSIT |
| MSSWEUG | Bachelor of Science, Software Engineering (BSSWE to MSSWE) | Same for BSSWE → MSSWE |

These have 81–85% overlap with their corresponding BS programs because they're the upper-division layer. They appear in the Technology Bachelor's pool and would generate spurious "highly similar" compare results if surfaced in a general comparison browser. They are not comparable in the student-decision sense.

**They should be explicitly excluded from the compare universe**, or placed in a separate category.

---

## 5. Feasibility and Friction Assessment

### Same-college same-level compare is feasible for a meaningful subset — but not universally

The 717 potential pairs break down as:
- **≥75% overlap (28 pairs):** Strong compare value; students face a real choice between structurally similar options
- **50–74% (77 pairs):** Viable compare; meaningful shared core with clear differentiation
- **25–49% (135 pairs):** Borderline; compare works but shared core is weaker
- **<25% (477 pairs):** Low value; these programs don't share enough to make comparison useful

The most useful compare universe is roughly **the top 100 pairs** — mostly within-family specialization choices or parallel-path degree variants (BA vs BS, BSN direct vs RN-to-MSN, etc.).

---

### The current family-gated model is too narrow but the instinct is right

Five programs and two families is clearly a prototype. However, **the curation gate is load-bearing:** without it, the compare browser would surface confusing pairs (pathway programs vs regular degrees, unrelated programs with accidental gen-ed overlap, programs with identical names). A fully open arbitrary-compare UI would mislead more than it helps.

The right expansion path is **more curated families, not open arbitrary compare.** Families to add next, in priority order:

1. **BSCNE tracks** (BSCNE, BSCNEAWS, BSCNEAZR, BSCNECIS) — 68–82% overlap; clean ` - ` suffix names; obvious student choice
2. **MSSWE tracks** (MSSWEAIE, MSSWEDDD, MSSWEDOE) — 54% overlap; same specialization pattern as MSDA
3. **MSCS tracks** (MSCSAIML, MSCSCS, MSCSHCI) — 67% overlap; same pattern
4. **MS Accounting specializations** (MACCA, MACCF, MACCM, MACCT) — 50–67% overlap; 4-way family
5. **MBA family** (MBA, MBAHA, MBAITM) — 64–67% overlap; very low differentiation (1–2 unique courses); edge case to evaluate
6. **Education MAT science subjects** (MATSESB, MATSESC, MATSESE, MATSESP) — 90% overlap; clear sibling choice

---

### The "Track A / Track B" label is wrong for most cases

The current CompareView uses `extractTrackLabel()` to show column headers like "Java Track" and "C# Track." This language is correct for the BSSWE pair, marginally acceptable for MSDA specializations, and **wrong for nearly everything else.** "Biology Track" is not how WGU describes MATSESB. "AWS Track" is not how BSCNEAWS is named.

For most pairs, the right column label is just the degree-specific differentiator: the subject, the vendor, the specialization name — not the word "Track." The current logic falls back to `canonical_name` when no `track_labels` are defined, which means very long names appear in column headers as-is.

---

### Name normalization is needed before broad rollout

At minimum, these issues must be resolved before expanding compare:

1. **Identical canonical names** — MEDETID/MEDETIDA/MEDETIDK12 are unshowable without disambiguation labels. BSSWE/BSSWE_C works only because of manually curated `track_labels`.

2. **Pathway program exclusion** — MSCSUG, MSITUG, MSSWEUG must be filtered out of the compare universe. They currently appear alongside regular BS programs.

3. **Long-name layout** — Column headers and program header cards need a truncation or abbreviation strategy for names >60 characters. This affects 38 programs (33% of corpus).

4. **Column header labels** — The "Track A / Track B" pattern needs generalization. A family-specific `short_label` per program (analogous to `track_labels`) is needed for clean column headers.

---

### Compare qualification rules (DECISIONS §15.12) hold up — with one gap

The 6 qualification rules (same school, same level, Jaccard ≥0.25, ≥2 unique courses, active only, curated affirmation) are sound. The gap is:

- **Rule 2 (same degree level)** doesn't catch pathway programs. `classifyDegreeLevel()` classifies MSCSUG as "Bachelor's" and it is technically an active Bachelor's program — but it isn't a standalone degree that a student would compare against BSCS.

A simple fix: add a `pathway_program` flag or an explicit exclusion list.

---

## 6. Information We Should Include in the External Review Request

### Facts to state upfront

1. **Scope of current compare:** Two hand-curated families, 5 programs total (Java vs C# Software Engineering; 3 Data Analytics specializations). This is an intentional pilot; the data exists for many more.

2. **Data completeness:** 113 of 114 active programs have full course rosters from the 2026-03 catalog. Roster data is the primary input to the comparison. It is reliable but represents one point in time.

3. **Scale of the real compare universe:** 114 active degrees across 4 colleges, with ~100 high-value same-college same-level pairs. Not all are useful comparisons — curation is required to distinguish meaningful student choices from spurious overlaps.

4. **Course identity is exact-code only:** Comparison is by course code. Two courses with different codes but equivalent content are not matched. This is intentional and correct per the data model, but reviewers should understand that "0 shared" can mean "redesigned curriculum" or "same content, renamed codes."

### Representative compare examples to share

Show reviewers these three pair types to illustrate the range:

| Example | Jaccard | Why it's illustrative |
|---|---|---|
| BSSWE (Java) vs BSSWE_C (C#) | 80% | Ideal case: high overlap, clean differentiator, obvious student question |
| BSCNE vs BSCNEAWS | 82% | Vendor track choice — slightly different structure, less disambiguating naming |
| MATSESB vs MATSESC | 90% | Subject specialization: 19/20 courses shared, 1 unique per side — extreme case |
| BSACC vs BSFIN | 54% | Distinct degrees with meaningful but moderate shared core — classic decision pair |
| MEDETID vs MEDETIDA | 83% | Identical names, must rely on code/description — disambiguation crisis example |

### Naming complexity to explain

Tell reviewers:
- Many WGU degree names are long (up to 92 characters). The compare UI must accommodate these without breaking.
- Some programs in the same family have identical canonical names. The UI relies on curated short labels that don't exist for most programs yet.
- The differentiating word is often buried at the end of a long shared prefix (e.g., "...Science Education (Secondary **Biology**)" vs "...Science Education (Secondary **Chemistry**)").
- "Track" is the right word for BSSWE vs BSSWE_C but wrong for most other high-overlap pairs. Reviewers should evaluate whether the UI's column-header language feels appropriate as the feature expands.

### Roster structures to explain

Three structures reviewers will encounter:
1. **Shared core + specialization tail** (MSDA model): Terms 1–2 identical, terms 3–4 diverge completely. Clean, easy to read.
2. **Mostly shared with a few swaps** (BSSWE model): ~33 shared courses, 5 unique to each side, scattered across terms 5–9.
3. **Mostly shared with subject substitution** (Education MAT model): 19/20 courses identical; 1 course per side is the subject-specific content. The comparison is nearly trivial but students do need to see it.

### UI stress cases reviewers should keep in mind

1. **Identical program names on both sides** — if disambiguation labels are absent, both header cards show the same text.
2. **Extreme asymmetry** — RN-to-MSN programs have 32–33 courses vs 14–15 for the BSN-to-MSN equivalents. One side of the three-lane view would be visually dominant.
3. **Near-zero differentiation** — MBA vs MBAHA differ by 1–2 courses. Is a three-lane compare view the right UI for a pair that's 95% identical?
4. **Long names in column headers** — "Master of Arts in Teaching, Science Education (Secondary Biological Science)" as a column header is too long at any reasonable column width.
5. **"Track" language applied to non-tracks** — The column headers say "X Track" where X is derived from the degree name. For subject-area education degrees, this reads awkwardly ("Biology Track" is not a WGU concept).

---

*Generated from active data as of 2026-03 catalog. Overlap metrics are computed from `program_enriched.json` rosters using exact course code identity per DECISIONS §4.6.*
