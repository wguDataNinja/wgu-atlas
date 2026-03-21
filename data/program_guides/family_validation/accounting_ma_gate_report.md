# accounting_ma — Gate Report
**Date:** 2026-03-21
**Family size:** 5 guides
**Gate guide:** MACC
**Gate result:** PARTIAL PASS — MACC gates HIGH; specialization guides deferred

---

## Gate summary

| Code | Degree | Confidence | SP Rows | AoS Groups | AoS Courses | Anomalies | Issue |
|------|--------|------------|---------|------------|-------------|-----------|-------|
| MACC | M.S., Accounting | HIGH | 10 | 4 | 10 | 0 | — |
| MACCM | M.S. in Accounting, Management Accounting | MEDIUM | 10 | 3 | 10 | 0 | Title quality (1 course) |
| MACCA | M.S. in Accounting, Auditing Specialization | **LOW** | 10 | 3 | 10 | 7 | Course parsed as group |
| MACCF | M.S. in Accounting, Financial Reporting | **LOW** | 11 | 4 | 11 | 9 | 2 courses as groups |
| MACCT | M.S. in Accounting, Taxation Specialization | **LOW** | 10 | 4 | 10 | 22 | 2 courses as groups |

---

## MACC (HIGH) — gate passed

Clean parse. 10/10 courses. 0 anomalies. 4 AoS groups (Accounting, Finance, Strategy, Management). Older guide version (202202); footer metadata. SP is clean.

---

## MACCM (MEDIUM) — parseable with caveats

"Corporate Financial Analysis" course has a title quality issue: the first sentence of the description ("Corporate Financial Analysis teaches the...") was partially incorporated into the course title. The description starts mid-sentence. 6 competency bullets are intact. The course IS present (10/10 AoS count matches SP). No AoS anomalies. SP is clean.

---

## MACCA, MACCF, MACCT (LOW) — systematic parser failure

### Root cause

`looks_like_prose()` requires lines to be >80 chars OR end with terminal punctuation (`.,:;?`). The 202409 specialization guides use a narrower PDF column layout, producing description lines of 40–50 chars with no terminal punctuation. These lines are not recognized as prose.

When the parser is in SEEKING state with one buffered title (the course title), and the next line looks non-prose, it gets buffered as a second pending_titles candidate. This cascades: description text is treated as pending_titles, the course title becomes a GROUP NAME, and subsequent description lines become spurious course titles with empty descriptions and bullets.

### Pattern (MACCA example)

In source: `Internal Auditing II` followed by `Internal Auditing II is a continuation of\nInternal Auditing I and covers the\n...`

Parser sees:
1. "Internal Auditing II" → pending_titles[0]
2. "Internal Auditing II is a continuation of" → 42 chars, no punctuation → `looks_like_prose` returns False → pending_titles[1]
3. "Internal Auditing I and covers the" → pending_titles overflow → `process_pending_titles` resolves [0]=group, [1]=course title (wrong!)
4. "competencies expected of an internal audit..." → pending_titles[2]... cascade continues

Result: "Internal Auditing II" becomes a GROUP NAME; "Internal Auditing I and covers the" becomes a course TITLE; the course has empty description and 0 bullets.

### SP is clean for all 5 guides

SP data (10–11 rows, 0 SP anomalies for all 5 guides) is correct and usable. The failure is confined entirely to AoS section parsing.

---

## What fix is needed

`looks_like_prose()` must be extended to recognize short description lines that are clearly mid-sentence but ≤80 chars and don't end with terminal punctuation. A verb-presence heuristic ("is a", "teaches", "provides", "examines") might work but needs careful evaluation — short group headings (e.g., "Accounting", "Software") must not be misidentified. This requires dedicated investigation with regression testing against all validated families before implementation.

---

## Rollout decision

- **MACC**: validated, usable downstream
- **MACCM**: parseable with title/description quality note for Corporate Financial Analysis course
- **MACCA, MACCF, MACCT**: deferred — parser fix required first

No rollout summary produced. Family is not complete this session.
