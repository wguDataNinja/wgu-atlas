# Compare 3 Prototype Design Proposal

Date: 2026-03-26  
Scope: Prototype-only route `/proto/compare-3`  
Status: Proposal (no production behavior changes)

## 1) Goal

Keep the current compare experience mostly intact, but allow selecting **2 or 3 degrees**.

Hard requirements from product direction:
- Prototype route only: `/proto/compare-3`
- Compare activates after the **second** degree is selected
- Third degree is **optional** and selected from viable remaining options
- **No shared column**
- Layout is **column-per-degree** (2 columns for 2-way, 3 columns for 3-way)
- Shared courses are indicated by **connected background treatment**, not a separate bucket
- Desktop-first/desktop-only rendering for compare canvas

---

## 2) Current Baseline (What Exists)

### Route/data-loading baseline
- `/proto/compare` currently loads active + roster-bearing programs, excludes known compare blockers, and passes filtered enriched data to a lab component.
- Reference: [src/app/proto/compare/page.tsx](/Users/buddy/projects/wgu-atlas/src/app/proto/compare/page.tsx)

Relevant current code:
```tsx
// src/app/proto/compare/page.tsx
const labPrograms = programs.filter(
  (p) =>
    p.status === "ACTIVE" &&
    !LAB_EXCLUSIONS.has(p.program_code) &&
    (allEnriched[p.program_code]?.roster?.length ?? 0) > 0
);
```

### Selector baseline
- Current production selector is 2-program only (`selectedA`, `selectedB`).
- Compare payload builds only when both are selected.
- Reference: [src/components/compare/CompareSelector.tsx](/Users/buddy/projects/wgu-atlas/src/components/compare/CompareSelector.tsx)

Relevant current code:
```tsx
const [selectedA, setSelectedA] = useState<string | null>(null);
const [selectedB, setSelectedB] = useState<string | null>(null);

const comparePayload = useMemo(() => {
  if (!selectedA || !selectedB) return null;
  ...
  return buildLabPayload(leftProgram, rightProgram, leftEnriched, rightEnriched);
}, [selectedA, selectedB, programs, enriched]);
```

### View baseline
- Current compare view has a 3-lane structure for 2-way compare: left unique / shared / right unique.
- Reference: [src/components/compare/CompareView.tsx](/Users/buddy/projects/wgu-atlas/src/components/compare/CompareView.tsx)

Relevant current code:
```tsx
<div className="grid grid-cols-[1fr_2fr_1fr]">
  <div>left unique</div>
  <div>shared</div>
  <div>right unique</div>
</div>
```

---

## 3) Proposed UX: 2-or-3 Selection

## 3.1 Selector flow
1. User picks Degree A.
2. UI shows viable Degree B options (same school + same level, excluding A).
3. After B is selected, compare canvas activates immediately.
4. UI exposes optional “Add third degree” panel.
5. Degree C options are viable set minus A/B.
6. Selecting C upgrades view to 3-way layout.
7. Clearing C falls back to 2-way layout with no mode reset.

## 3.2 Viability rules
Keep current compare viability constraints:
- active programs
- non-empty roster
- excluded code list honored
- same school + same degree level within the selected set

## 3.3 Activation states
- `0 selected`: empty state
- `1 selected`: prompt for second degree
- `2 selected`: compare active (2-column mode)
- `3 selected`: compare active (3-column mode)

---

## 4) Proposed Compare Canvas

## 4.1 Structural rule (core change)
Replace unique/shared/unique lanes with **degree columns only**.

- 2-way: `grid-cols-2` (Degree A, Degree B)
- 3-way: `grid-cols-3` (Degree A, Degree B, Degree C)
- No dedicated “Shared” column in any mode

## 4.2 Course placement rule
For each term block:
- Build union of course codes present in any selected degree for that term context.
- Render one logical row per union course.
- In each degree column cell:
  - show course card if that degree contains that course
  - show empty placeholder cell if not

Result:
- Every displayed course is represented in degree columns only.
- Shared courses naturally appear in multiple columns on the same row.

## 4.3 Shared visibility rule
Apply a **connected row background** based on membership mask:
- only A
- only B
- only C
- A+B
- A+C
- B+C
- A+B+C

The row background spans across participating column cells so shared membership is obvious without a shared lane.

## 4.4 Header treatment
Keep sticky utility/header concept from existing view:
- top utility bar with `Change` / `Reset`
- per-degree column header with short label + code + course count
- equal-width headers for 2 or 3 selected degrees

---

## 5) Color System Proposal (Desktop Prototype)

Current compare palette is blue/shared-slate/amber, with green accents for shared course cards.
In the new model, shared state moves from a column to row connections, so palette must carry more semantic load.

## 5.1 Column identity colors
- Degree A: blue family
- Degree B: amber family
- Degree C: violet family

## 5.2 Shared-row connector colors (membership masks)
- A only: `blue-50`
- B only: `amber-50`
- C only: `violet-50`
- A+B: `cyan-50`
- A+C: `indigo-50`
- B+C: `orange-50`
- A+B+C: `emerald-50`

## 5.3 Card accents
- Keep code-badge + left-border accents per owning degree color.
- For shared rows, cards keep degree identity colors; row background carries cross-degree relationship.

Note: these exact classes should be tuned in-browser for contrast/readability before finalizing.

---

## 6) Desktop-Only Handling

For `/proto/compare-3` compare canvas:
- Render full compare view only at `xl` and above.
- Below `xl`, show selector UI plus a non-error notice:
  - “Compare 3 prototype is desktop-only. Expand window to view the comparison canvas.”

This preserves flow while preventing cramped unreadable 3-column rendering.

---

## 7) Data/Model Additions (Prototype-Only)

Add a proto utility module (new file) for 3-way shaping:
- input: selected degree records + rosters (2 or 3)
- output:
  - normalized program meta list in selected order
  - term-indexed union rows
  - per-row membership bitmask and per-degree course slots
  - top-level counts (per-degree total, pairwise overlaps, all-shared count)

No production compare contracts need to change for this prototype.

---

## 8) Implementation Plan

1. Add new route page: `src/app/proto/compare-3/page.tsx`
2. Reuse current lab universe filtering from existing proto compare route
3. Add new component: `src/components/proto/Compare3PrototypeLab.tsx`
4. Add new utility: `src/components/proto/compare3ProtoUtils.ts`
5. Implement selector with `A + B required`, `C optional`
6. Implement compare canvas with 2/3 equal columns and connected shared-row backgrounds
7. Add desktop-only guard for canvas
8. Add a few preset examples for quick review (2-way and 3-way)

---

## 9) Architecture Plan (Updated)

This section defines the implementation architecture to keep 2-way behavior stable while adding 3-way prototype behavior.

## 9.1 File structure
- New route: `src/app/proto/compare-3/page.tsx`
- New orchestrator: `src/components/proto/Compare3PrototypeLab.tsx`
- New 3-way view: `src/components/proto/Compare3View.tsx`
- New 3-way utility/data shaping: `src/components/proto/compare3ProtoUtils.ts`
- Reuse existing 2-way view unchanged: `src/components/compare/CompareView.tsx`
- Reuse existing universe + label helpers from `src/lib/compareUtils.ts`

## 9.2 Reuse boundaries
- Keep current 2-way visual and behavior path by rendering existing `CompareView` when only A+B are selected.
- Do not fork or modify production `/compare` components for this prototype route.
- Keep universe/viability rules identical to current compare:
  - ACTIVE only
  - non-empty roster
  - `LAB_EXCLUSIONS`
  - B/C options constrained to same school + same degree level as A

## 9.3 Parent orchestration model
- Use one parent/orchestrator component with mode branching:
  - 2 selected (`A+B`) -> 2-way mode with current compare UI
  - 3 selected (`A+B+C`) -> 3-way mode with new columnar UI
- Selection behavior:
  - compare activates immediately after B is selected
  - adding/removing C never resets A/B
  - clearing A resets B/C; clearing B resets C

## 9.4 3-way data model
Use a row-matrix model (not shared-lane buckets).

Per selection set (A,B,C), build:
- `programsOrdered`: final render order of selected programs
- `pairwiseMetrics`: AB/AC/BC overlap metrics
- `rowsByTerm`: grouped row objects where each row has:
  - `code`, `title`, `cus`
  - `presentByProgram: boolean[3]`
  - `termByProgram: (number | null)[3]`
  - `membershipMask` (`A`, `B`, `C`, `AB`, `AC`, `BC`, `ABC`)
  - `anchorTerm` for grouping/sorting (recommended: minimum non-null term)

This keeps all courses inside degree columns and supports presence/absence rendering directly.

## 9.5 2-of-3 similarity visualization
Do not depend on visual connectors for non-adjacent pairs (A+C).

Preferred treatment:
- emphasize matching cells/cards themselves (stronger tint/border for participating cells)
- apply row-level membership badge/chip (e.g., `A+C shared`)
- keep non-participating cells muted/empty

This works for adjacent and non-adjacent pairs without fragile connector logic.

## 9.6 Optional auto-ordering for readability
Recommended for 3-way mode:
- compute pairwise overlap across selected triple
- place most connected program in middle
- place least-similar pair on the outside

Guardrails:
- apply only in 3-way mode
- keep it deterministic
- show a small “auto-arranged by overlap” note
- preserve original selection chips so users can see what was picked

---

## 10) Acceptance Criteria

- Route `/proto/compare-3` loads and is isolated from production `/compare`
- User can select A, then B, and compare view activates
- User can optionally add/remove C without resetting A/B
- Compare canvas has no shared column
- All courses are displayed only in degree columns
- Shared membership is visually legible through connected row backgrounds
- 2-way mode renders as 2 equal columns; 3-way as 3 equal columns
- Below `xl`, canvas is replaced by a clear desktop-only notice

---

## 11) Risks / Tradeoffs

- Row-alignment complexity is higher than current lane bucket model
- Color combinatorics can become noisy if not tuned carefully
- 3-way density may still feel tight on smaller laptop widths; desktop-only guard mitigates this
- Pairwise/shared metrics can distract; keep top metrics minimal in first prototype pass

---

## 12) Recommended First Pass

Implement a conservative v1 for `/proto/compare-3`:
- keep selector language and controls familiar
- keep sticky header behavior
- ship only the new column model + shared-row connectors
- avoid extra analytics widgets in v1

This gives a direct apples-to-apples visual review against current compare behavior with minimal concept drift.
