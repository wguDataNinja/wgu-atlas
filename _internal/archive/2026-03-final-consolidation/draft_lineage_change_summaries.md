# Draft `change_summary_template` Strings

_Wording-guard events only. Reviewed 2026-03-20._

---

## PLE-015 — BSBAHC → BSHA

```
This program replaced the B.S. Business Administration — Healthcare Management (BSBAHC)
in July 2023. The degree was restructured as a standalone Healthcare Administration
program; the Business Administration framework was retired.
```

**Framing rationale:** "Restructured as" and "retired" are defensible without claiming curriculum continuity. Avoids "evolved from" or "expanded."

**wording_guard:** true

---

## PLE-026 — MBAHM → MBAHA

```
This M.B.A. specialization replaced the Healthcare Management concentration (MBAHM)
in May 2025. The program was retitled as Healthcare Administration within the M.B.A.
program family.
```

**Framing rationale:** "Retitled as … within the M.B.A. program family" anchors the change to the MBA family without implying curriculum continuity. Avoids "continuing within," which implies ongoing content inheritance.

**wording_guard:** true

---

## PLE-022 — MSITM → MSIT / MSITPM / MSITUG

```
This program launched in February 2026 as part of a restructuring of the M.S.
Information Technology Management (MSITM). The curriculum was entirely rebuilt;
no courses were directly carried over from the prior program.
```

**Framing rationale:** "Entirely rebuilt" and "no courses carried over" are accurate and provenance-safe. Required language for any Jaccard = 0.0 event.

**wording_guard:** true

### PLE-022 `zero_overlap_rationale` (internal, not student-facing)

```
MSITM used a legacy course series. The successor programs (MSIT, MSITPM) were built on
an entirely new course series at program launch. The zero course overlap reflects a
complete curriculum refresh rather than a break in organizational lineage — IT Management
to Information Technology is a confirmed institutional succession per the 2026-01→02
boundary event.
```

---

## PLE-013 — BSITSW/BSITSWC → BSSWE/BSSWE_C

```
This program replaced the B.S. Software Development in January 2023. The curriculum
was substantially rebuilt — approximately 6–11% of prior courses were carried forward,
with new content developed for the Software Engineering designation.
```

**Framing rationale:** Percent range is accurate to the two pairs. "Substantially rebuilt" is the correct characterization at this Jaccard level (0.059–0.111).

**wording_guard:** true

---

## PLE-014 — BSDMDA → BSDA

```
This program replaced the B.S. Data Management/Data Analytics (BSDMDA) in July 2023.
The curriculum was substantially rebuilt: 33 new courses were introduced, 30 prior
courses were retired, and 9 courses were carried forward. The data management component
was removed in favor of a dedicated analytics focus.
```

**Framing rationale:** Exact course counts sourced directly from `program_lineage_enriched.json`; safe to publish. "Removed in favor of" characterizes intent without editorializing.

**wording_guard:** true

---

## Wording Guard Policy

Applies to all events with any individual pair Jaccard < 0.15, and to all approved events where Jaccard is unconfirmed.

**Permitted terms:** replaced, rebuilt, restructured, retitled, carried forward, redesigned

**Forbidden terms:** evolved from, descended from, builds on, updated version of, successor to (unqualified), continuation of, expanded, continuing within

**Zero-overlap requirement:** Events with Jaccard = 0.0 must use "entirely rebuilt" or "no courses carried over" language AND must have `zero_overlap_rationale` populated before export.
