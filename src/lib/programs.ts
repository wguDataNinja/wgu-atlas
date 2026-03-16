// ---------------------------------------------------------------------------
// Canonical program helpers — shared across routes and compare feature.
// Session 1 foundation: degree-level classification + roster comparison.
// No UI components. Safe to import in server and client contexts.
// ---------------------------------------------------------------------------

import type { ProgramRecord, RosterCourse } from "./types";

// ---------------------------------------------------------------------------
// Degree-level classification
// ---------------------------------------------------------------------------

export type DegreeLevel =
  | "Doctoral"
  | "Master's"
  | "Bachelor's"
  | "Associate"
  | "Certificates & Endorsements"
  | "Other";

/** Canonical display order for degree level groups. */
export const DEGREE_LEVEL_ORDER: DegreeLevel[] = [
  "Doctoral",
  "Master's",
  "Bachelor's",
  "Associate",
  "Certificates & Endorsements",
  "Other",
];

/**
 * Classify a program into a canonical degree level based on canonical_name.
 * Classification is name-prefix based and covers all WGU degree types observed
 * in the catalog through 2026-03. "Other" catches certificates, post-master's
 * specializations, and any novel degree types not yet enumerated here.
 */
export function classifyDegreeLevel(program: ProgramRecord): DegreeLevel {
  const name = program.canonical_name.toLowerCase();
  if (name.startsWith("doctor") || name.startsWith("ph.d")) return "Doctoral";
  if (
    name.startsWith("master") ||
    name.startsWith("m.b.a") ||
    name.startsWith("mba")
  )
    return "Master's";
  if (name.startsWith("bachelor")) return "Bachelor's";
  if (name.startsWith("associate")) return "Associate";
  if (
    name.startsWith("endorsement") ||
    name.startsWith("graduate certificate")
  )
    return "Certificates & Endorsements";
  return "Other";
}

/**
 * Group programs by degree level in canonical order.
 * Extracted from schools/[slug]/page.tsx; shared for school display and
 * compare-family scoping.
 */
export function groupProgramsByLevel(
  programs: ProgramRecord[]
): Record<string, ProgramRecord[]> {
  const groups: Partial<Record<DegreeLevel, ProgramRecord[]>> = {};

  for (const p of programs) {
    const level = classifyDegreeLevel(p);
    if (!groups[level]) groups[level] = [];
    groups[level]!.push(p);
  }

  for (const g of Object.values(groups)) {
    g!.sort((a, b) => a.canonical_name.localeCompare(b.canonical_name));
  }

  const ordered: Record<string, ProgramRecord[]> = {};
  for (const lv of DEGREE_LEVEL_ORDER) {
    if (groups[lv] && groups[lv]!.length > 0) ordered[lv] = groups[lv]!;
  }
  return ordered;
}

// ---------------------------------------------------------------------------
// Roster comparison contract
// ---------------------------------------------------------------------------

export interface CompareResult {
  /** Course codes present in both left and right rosters. */
  shared_codes: string[];
  /** Course codes present only in the left roster. */
  left_only_codes: string[];
  /** Course codes present only in the right roster. */
  right_only_codes: string[];
  /** Total courses in left roster (by unique code). */
  left_count: number;
  /** Total courses in right roster (by unique code). */
  right_count: number;
  /** Count of shared courses. */
  shared_count: number;
  /**
   * Jaccard overlap: shared / (left + right - shared).
   * Matches lineage pipeline metric semantics in program_lineage_enriched.json.
   */
  jaccard_overlap: number;
  /** Fraction of left courses that also appear in right (retention rate). */
  left_retained_pct: number;
  /** Fraction of right courses that also appear in left (inheritance rate). */
  right_inherited_pct: number;
}

/**
 * Compare two program rosters by course code.
 *
 * Identity is exact course code per DECISIONS §4.6; no aliasing, fuzzy
 * matching, or semantic linkage across codes is performed.
 *
 * This is the V1 compare contract for Degree Compare (DECISIONS §15).
 * Inputs are `ProgramEnriched.roster` arrays from program_enriched.json.
 */
export function compareRosters(
  left: RosterCourse[],
  right: RosterCourse[]
): CompareResult {
  const leftCodes = new Set(left.map((c) => c.code));
  const rightCodes = new Set(right.map((c) => c.code));

  const shared_codes = [...leftCodes].filter((c) => rightCodes.has(c));
  const left_only_codes = [...leftCodes].filter((c) => !rightCodes.has(c));
  const right_only_codes = [...rightCodes].filter((c) => !leftCodes.has(c));

  const shared_count = shared_codes.length;
  const union_count = leftCodes.size + rightCodes.size - shared_count;

  return {
    shared_codes,
    left_only_codes,
    right_only_codes,
    left_count: leftCodes.size,
    right_count: rightCodes.size,
    shared_count,
    jaccard_overlap: union_count > 0 ? shared_count / union_count : 0,
    left_retained_pct:
      leftCodes.size > 0 ? shared_count / leftCodes.size : 0,
    right_inherited_pct:
      rightCodes.size > 0 ? shared_count / rightCodes.size : 0,
  };
}
