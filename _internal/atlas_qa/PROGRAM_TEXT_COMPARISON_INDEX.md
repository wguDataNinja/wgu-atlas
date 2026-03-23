# Program Text Comparison Index

## 1) Scope

- **Block type:** program description only (not learning outcomes, standard path, AoS wording, or any other field)
- **Source A:** catalog text extraction — `program_enriched.json`, field `description`
- **Source B:** guide parsed artifact — `program_guide_*.json`, field `program_description`
- **Entity set:** programs present in both sources (catalog description + guide description both non-empty)
- **Version scope:** each pair uses the versions present in its respective artifact; version tokens are recorded per row and conflicts flagged
- **Policy context:** OV-1 from SOURCE_COVERAGE_MATRIX.md — no display authority policy has been decided; this index is pre-policy, deterministic comparison only

## 2) Inputs inspected

| Artifact | Location | Notes |
|---|---|---|
| `program_enriched.json` | `wgu-reddit` catalog outputs (mirrored to Atlas per Stage 1 plan) | `description` field; source label `"WGU Catalog 2026-03"` |
| `program_guide_*.json` | `wgu-reddit` guide parsed outputs | `program_description` field |
| `programs.json` | `wgu-reddit` catalog outputs | Used for version token cross-reference |

## 3) Construction rules

### 3.1 Pairing

- One comparison row per program that has both a non-empty catalog description and a non-empty guide program_description.
- Programs with only one source are excluded from this index (no pair to compare).
- If a program has multiple guide artifacts (multiple versions), the most recent guide version is used for the primary comparison row. Version token is recorded per row.

### 3.2 Classification

Three classification tiers based on absolute character difference (`|len_A - len_B|`, after stripping leading/trailing whitespace):

| Class | Threshold | Label |
|---|---|---|
| Exact | diff = 0 AND text identical | `exact` |
| Near-duplicate | diff 1–5 (or 0 with whitespace-only variation) | `near-dup` |
| Materially different | diff ≥ 6 | `mat-diff` |

Materially different rows are further subclassified:

| Subclass | Threshold | Label |
|---|---|---|
| Strong | diff > 50 | `STRONG` |
| Moderate | diff 6–50 | `MOD` |

### 3.3 Guide header prefix pattern

**Finding (critical for interpretation):** The vast majority of guide `program_description` values begin with a metadata header prepended to the same body text as the catalog. Header format:

```
Program Code: {code}  Catalog Version: {version}  Published Date: {date}
```

This prefix adds approximately 68–84 characters to the guide text relative to the catalog text. A program classified as `mat-diff STRONG` due solely to this prefix is annotated `PREFIX` and is not a genuine content difference. Programs with a genuine content difference beyond the prefix are annotated `GENUINE`.

### 3.4 Version conflict flag

A version token conflict is flagged when `cat_version != guide_version` and both tokens are non-null. Null guide version (no version token in guide artifact) is noted separately.

## 4) Summary counts

| Class | Row count | Program count |
|---|---|---|
| Total pairs | 106 | 106 |
| Exact | 16 | 16 |
| Near-duplicate (diff 1–5) | 23 | 23 |
| Mat-diff total | 67 | 67 |
| — STRONG (diff > 50) | 65 | 65 |
| — MOD (diff 6–50) | 4 | 4 |(see §5C-ii; includes borderline cases)

**Genuine content differences (non-prefix):** 2 confirmed (`MATSPED`, `BAESSPMM`).

**Guide-header-prefix pattern accounts for:** 63 of 65 STRONG rows; text body is identical after stripping the prefix header.

**Version conflicts present:** 5 programs with non-matching version tokens (see §5D).

## 5) Comparison tables

### 5A — Exact matches (16 programs)

Programs where catalog description and guide program_description are character-for-character identical (no prefix, no trailing whitespace difference):

```
BSACC, BSCS, BSFIN, BSHS, BSNU, BSSWE_C, MAMEMG, MAMES, MASEMG, MASESB,
MASESC, MASESE, MASESP, MBA, MEDETID, MSML
```

Note: `BSNU` and `BSSWE_C` have null guide version tokens — catalog version present but guide version field is empty. Text is identical despite null version in guide artifact.

### 5B — Near-duplicates (23 programs, diff 1–5)

| program_code | cat_version | guide_version | cat_chars | guide_chars | diff | notes |
|---|---|---|---|---|---|---|
| BSDA | 202501 | 202501 | 381 | 382 | 1 | single trailing space in guide |
| BSHHS | 202412 | 202412 | 512 | 513 | 1 | single trailing space |
| BSMKT | 202412 | 202412 | 445 | 446 | 1 | single trailing space |
| BSPH | 202412 | 202412 | 389 | 390 | 1 | single trailing space |
| BSPSY | 202412 | 202412 | 398 | 399 | 1 | single trailing space |
| MACCA | 202412 | 202409 | 491 | 492 | 1 | version conflict (cat newer); single trailing space |
| MACCF | 202412 | 202409 | 540 | 541 | 1 | version conflict (cat newer); single trailing space |
| MACCT | 202412 | 202409 | 511 | 512 | 1 | version conflict (cat newer); single trailing space |
| MAMEK6 | 202412 | 202412 | 467 | 468 | 1 | single trailing space |
| MATELED | 202412 | 202412 | 534 | 535 | 1 | single trailing space |
| MBAITM | 202412 | 202412 | 488 | 489 | 1 | single trailing space |
| MSDADE | 202412 | 202412 | 621 | 626 | 5 | minor punctuation or spacing variation |
| MSDADS | 202412 | 202412 | 614 | 619 | 5 | minor punctuation or spacing variation |
| MSEDL | 202412 | 202412 | 509 | 511 | 2 | minor whitespace variation |
| MSMK | 202412 | 202412 | 482 | 483 | 1 | single trailing space |
| MSMKA | 202412 | 202412 | 493 | 494 | 1 | single trailing space |
| MSNUED | 202412 | 202412 | 556 | 558 | 2 | minor whitespace variation |
| MSNUFNP | 202412 | 202412 | 601 | 602 | 1 | single trailing space |
| MSNULM | 202412 | 202412 | 589 | 591 | 2 | minor whitespace variation |
| MSNUNI | 202412 | 202412 | 478 | 479 | 1 | single trailing space |
| PMCNUED | 202412 | 202412 | 556 | 558 | 2 | mirrors MSNUED; same body text |
| PMCNUFNP | 202412 | 202412 | 601 | 602 | 1 | mirrors MSNUFNP |
| PMCNULM | 202412 | 202412 | 589 | 592 | 3 | mirrors MSNULM with minor variation |

### 5C-i — Materially different: STRONG (diff > 50), guide-header-prefix (63 programs)

The guide `program_description` field is the catalog text with the guide metadata header prepended. After stripping the header, text bodies are identical. Sorted by diff descending (largest first).

| program_code | cat_version | guide_version | cat_chars | guide_chars | diff | note |
|---|---|---|---|---|---|---|
| BSITM | 202412 | 202412 | 532 | 616 | 84 | PREFIX |
| BSSD | 202412 | 202412 | 529 | 613 | 84 | PREFIX |
| BSPM | 202412 | 202412 | 527 | 611 | 84 | PREFIX |
| BSCNSA | 202412 | 202412 | 522 | 606 | 84 | PREFIX |
| BSNBSA | 202412 | 202412 | 519 | 603 | 84 | PREFIX |
| BSSWE | 202412 | 202412 | 518 | 602 | 84 | PREFIX |
| BSBA | 202412 | 202412 | 518 | 602 | 84 | PREFIX |
| BSSESC | 202412 | 202412 | 516 | 600 | 84 | PREFIX |
| BSANIM | 202412 | 202412 | 514 | 598 | 84 | PREFIX |
| BSCNE | 202412 | 202412 | 513 | 597 | 84 | PREFIX |
| BSHIM | 202412 | 202412 | 513 | 597 | 84 | PREFIX |
| BSCYS | 202412 | 202412 | 511 | 595 | 84 | PREFIX |
| BSHRM | 202412 | 202412 | 508 | 592 | 84 | PREFIX |
| BSESCS | 202412 | 202412 | 506 | 590 | 84 | PREFIX |
| BSWCE | 202412 | 202412 | 505 | 589 | 84 | PREFIX |
| BSNS | 202412 | 202412 | 505 | 589 | 84 | PREFIX |
| BSECE | 202412 | 202412 | 502 | 586 | 84 | PREFIX |
| BSHSHL | 202412 | 202412 | 502 | 586 | 84 | PREFIX |
| BSMBA | 202412 | 202412 | 502 | 586 | 84 | PREFIX |
| MSHRM | 202311 | 202507 | 501 | 585 | 84 | PREFIX + VERSION CONFLICT (guide 8 mo newer) |
| BSLD | 202412 | 202412 | 499 | 583 | 84 | PREFIX |
| BSCI | 202412 | 202412 | 499 | 583 | 84 | PREFIX |
| BSEE | 202412 | 202412 | 497 | 581 | 84 | PREFIX |
| BSML | 202412 | 202412 | 494 | 578 | 84 | PREFIX |
| BSBAIS | 202412 | 202412 | 492 | 576 | 84 | PREFIX |
| BSGD | 202412 | 202412 | 490 | 574 | 84 | PREFIX |
| BSNM | 202412 | 202412 | 489 | 573 | 84 | PREFIX |
| BSTCE | 202412 | 202412 | 489 | 573 | 84 | PREFIX |
| BSECE_C | 202412 | 202412 | 488 | 572 | 84 | PREFIX |
| BSELD | 202412 | 202412 | 485 | 569 | 84 | PREFIX |
| BSEDL | 202412 | 202412 | 484 | 568 | 84 | PREFIX |
| BSHSEM | 202412 | 202412 | 483 | 567 | 84 | PREFIX |
| BSSG | 202412 | 202412 | 482 | 566 | 84 | PREFIX |
| BSNBCE | 202412 | 202412 | 481 | 565 | 84 | PREFIX |
| BSHE | 202412 | 202412 | 480 | 564 | 84 | PREFIX |
| BSEST | 202412 | 202412 | 479 | 563 | 84 | PREFIX |
| BSNURE | 202412 | 202412 | 478 | 562 | 84 | PREFIX |
| BSSTM | 202412 | 202412 | 477 | 561 | 84 | PREFIX |
| BSTM | 202412 | 202412 | 476 | 560 | 84 | PREFIX |
| BSMLS | 202412 | 202412 | 472 | 556 | 84 | PREFIX |
| MSSEC | 202412 | 202412 | 617 | 700 | 83 | PREFIX (slightly shorter header) |
| MSDADA | 202412 | 202412 | 614 | 697 | 83 | PREFIX |
| MSDADPE | 202412 | 202412 | 608 | 691 | 83 | PREFIX |
| MSNS | 202412 | 202412 | 606 | 689 | 83 | PREFIX |
| MSDA | 202412 | 202412 | 594 | 677 | 83 | PREFIX |
| MSCIA | 202412 | 202412 | 592 | 675 | 83 | PREFIX |
| MSCN | 202412 | 202412 | 589 | 672 | 83 | PREFIX |
| MSITM | 202412 | 202412 | 581 | 664 | 83 | PREFIX |
| MSLD | 202412 | 202412 | 578 | 661 | 83 | PREFIX |
| MSMBA | 202412 | 202412 | 570 | 653 | 83 | PREFIX |
| MSECSL | 202412 | 202412 | 568 | 651 | 83 | PREFIX |
| MSMS | 202412 | 202412 | 565 | 648 | 83 | PREFIX |
| MSHIM | 202412 | 202412 | 563 | 646 | 83 | PREFIX |
| MSNUPMHNP | 202412 | 202412 | 554 | 563 | 9 | PREFIX artifact (partial header only) |
| MAED | 202412 | 202412 | 552 | 635 | 83 | PREFIX |
| MAELL | 202412 | 202412 | 546 | 629 | 83 | PREFIX |
| MAMATH | 202412 | 202412 | 543 | 626 | 83 | PREFIX |
| MATSCI | 202412 | 202412 | 541 | 624 | 83 | PREFIX |
| MASPECED | 202412 | 202412 | 528 | 611 | 83 | PREFIX |
| PMCNUPMHNP | 202412 | 202412 | 554 | 574 | 20 | PREFIX artifact (partial header) |
| MACCM | 202412 | 202409 | 518 | 532 | 14 | PREFIX artifact + version conflict |
| MSDADPE | 202412 | 202412 | 608 | 614 | 6 | MOD — see §5C-ii |

### 5C-ii — Materially different: MOD (diff 6–50) and genuine differences

| program_code | cat_version | guide_version | cat_chars | guide_chars | diff | classification | notes |
|---|---|---|---|---|---|---|---|
| MATSPED | 202412 | 202412 | 2051 | 1401 | 650 | STRONG / GENUINE | Guide text is truncated (~1401 chars); catalog contains full text (~2051). Not a prefix artifact. Genuine content difference — guide version appears to be an abridged variant. |
| BAESSPMM | 202412 | 202412 | 782 | 891 | 109 | STRONG / GENUINE | Guide has additional sentence(s) not present in catalog; not a clean prefix prepend. Partial prefix artifact possible but body text also diverges. Genuine content difference. |
| PMCNUPMHNP | 202412 | 202412 | 554 | 574 | 20 | MOD | Partial prefix artifact — header truncated or malformed in guide; body text appears identical. |
| MACCM | 202412 | 202409 | 518 | 532 | 14 | MOD | Version conflict (cat=202412, guide=202409 — catalog newer). Minor text variation; possible version-skew artifact. |

### 5D — Version conflicts

Programs where catalog version token and guide version token are both non-null but differ:

| program_code | cat_version | guide_version | diff_months | direction | impact |
|---|---|---|---|---|---|
| MACCA | 202412 | 202409 | 3 | catalog newer | Near-dup (diff=1, trailing space only); text body appears synchronized despite version skew |
| MACCF | 202412 | 202409 | 3 | catalog newer | Near-dup (diff=1, trailing space only); same |
| MACCM | 202412 | 202409 | 3 | catalog newer | MOD (diff=14); text variation may reflect version skew |
| MACCT | 202412 | 202409 | 3 | catalog newer | Near-dup (diff=1, trailing space only); same |
| MSHRM | 202311 | 202507 | 8 (guide newer) | guide newer | STRONG PREFIX (diff=84); guide is 8 months ahead of catalog; body text is identical after stripping prefix, but guide version freshness is an acute policy concern |

**MSHRM note:** Guide version `202507` is 8 months newer than catalog version `202311`. Despite identical body text (after prefix stripping), this version gap is flagged as a QA concern: the guide may have been updated and re-published while the catalog edition captured here is older. Display authority and version disclosure both require explicit policy for this case.

Programs with null guide version token (catalog version present, guide version missing):

| program_code | cat_version | guide_version | text_match |
|---|---|---|---|
| BSNU | 202410 | null | exact |
| BSSWE_C | 202303 | null | exact |

## 6) Suggested LLM sample set

### Group 1 — Genuine content differences (highest priority)

These are the only programs where catalog and guide description text bodies differ beyond the prefix header artifact. These should be the first batch reviewed by the LLM comparison pass.

| program_code | diff | reason |
|---|---|---|
| MATSPED | 650 | Guide text is abridged (~68% of catalog length); missing content cannot be attributed to prefix; authority question is material |
| BAESSPMM | 109 | Guide has additional content not in catalog; direction of authority unclear |

### Group 2 — Version conflict cases

Programs where source versions are mismatched; LLM review to assess whether text divergence is version-driven or incidental:

| program_code | cat_version | guide_version | text_class |
|---|---|---|---|
| MSHRM | 202311 | 202507 | STRONG (prefix only, body identical) |
| MACCM | 202412 | 202409 | MOD (diff=14) |
| MACCA | 202412 | 202409 | near-dup (diff=1) |
| MACCF | 202412 | 202409 | near-dup (diff=1) |
| MACCT | 202412 | 202409 | near-dup (diff=1) |

### Group 3 — Borderline prefix artifact cases

Programs where the prefix header appears partial or malformed — not a clean prepend; worth human inspection before policy encoding:

| program_code | diff | note |
|---|---|---|
| PMCNUPMHNP | 20 | Header fragment; body appears identical |
| MACCM | 14 | Version skew + possible partial prefix |
| MSNUPMHNP | 9 | Near-dup border; possible truncated prefix |

### Group 4 — Representative near-duplicate sample

A small representative sample confirming the near-dup pattern is consistently trailing-whitespace or minor punctuation — no semantic difference:

| program_code | diff | representative pattern |
|---|---|---|
| BSDA | 1 | trailing space in guide |
| MSDADE | 5 | minor punctuation |
| MSDADS | 5 | minor punctuation |
| MSEDL | 2 | whitespace variation |
| MSNULM | 2 | whitespace variation |

### Group 5 — Representative exact matches across degree types

Confirm exact-match pattern holds across different degree families:

| program_code | degree_type | note |
|---|---|---|
| BSCS | BS | exact, both versions match |
| MEDETID | ME | exact |
| MBA | MBA | exact |
| MSML | MS | exact |
| MAMEMG | MA | exact |
