// ---------------------------------------------------------------------------
// Compare prototype lab — shared data utilities.
// Server-safe (no "use client"). Safe to import in both server and client code.
//
// Provides:
//   - LAB_EXCLUSIONS: programs excluded from the lab compare universe
//   - labShortLabel(): compact differentiating label for column headers / chips
//   - labDisplayLabel(): longer label for identity bar
//   - buildLabPayload(): builds ComparePayload without requiring a ProgramFamily
//   - buildTermLanes(): groups courses by term into left/shared/right lanes
// ---------------------------------------------------------------------------

import type { ProgramRecord, ProgramEnriched, RosterCourse } from "@/lib/types";
import { classifyDegreeLevel } from "@/lib/programs";
import { compareRosters } from "@/lib/programs";
import { getIndexName } from "@/lib/families";

// Re-export for lab components so they only need to import from this file
export type { CompareResult } from "@/lib/programs";
export type {
  ComparePayload,
  CompareProgramMeta,
  CompareCourseEntry,
} from "@/lib/families";

// ---------------------------------------------------------------------------
// Lab universe exclusions
// ---------------------------------------------------------------------------

/**
 * Program codes excluded from the prototype lab compare universe.
 * These are programs that would produce misleading or unresolvable compare results.
 *
 * Excluded groups:
 *   - Pathway/bridge programs: classify as Bachelor's by name prefix but are
 *     upper-division accelerated paths, not standalone degrees.
 *   - Identical-canonical-name group (MEDETID family): all three programs share
 *     the same canonical_name with no curated track_labels — both sides of any
 *     compare would show the same header text.
 */
export const LAB_EXCLUSIONS = new Set([
  // Pathway programs (BSCS→MSCS, BSIT→MSIT, BSSWE→MSSWE bridge programs)
  "MSCSUG",
  "MSITUG",
  "MSSWEUG",
  // Identical-name group — disambiguation required before surfacing
  "MEDETID",
  "MEDETIDA",
  "MEDETIDK12",
]);

// ---------------------------------------------------------------------------
// Label helpers
// ---------------------------------------------------------------------------

/**
 * Short differentiating label for use in column headers and compact chips.
 * Extracts the most specific part of the degree name.
 *
 * Priority:
 *   1. Curated track_label from PILOT_FAMILIES (e.g. "Java Track", "C# Track")
 *   2. Specialization suffix after " - " (e.g. "Amazon Web Services")
 *   3. Trailing parenthetical qualifier (e.g. "Secondary Biology")
 *   4. Degree subject after the first comma (e.g. "Data Analytics")
 *   5. Truncated canonical name
 */
export function labShortLabel(code: string, canonicalName: string): string {
  // 1. Curated index name (pilot families only: BSSWE/BSSWE_C, MSDA tracks)
  const idx = getIndexName(code);
  if (idx) {
    const parenMatch = idx.match(/\(([^)]+)\)$/);
    return parenMatch ? parenMatch[1] : idx;
  }
  // 2. "Base Degree - Specialization" pattern
  const dashIdx = canonicalName.indexOf(" - ");
  if (dashIdx >= 0) return canonicalName.slice(dashIdx + 3);
  // 3. Trailing parenthetical: "Degree Name (qualifier)"
  const parenMatch = canonicalName.match(/\(([^)]+)\)$/);
  if (parenMatch) return parenMatch[1];
  // 4. Strip degree-type prefix to first comma: "Bachelor of Science, Finance" → "Finance"
  const commaIdx = canonicalName.indexOf(",");
  if (commaIdx > 0 && commaIdx < canonicalName.length - 5) {
    return canonicalName.slice(commaIdx + 2);
  }
  // 5. Truncate
  return canonicalName.length > 42 ? canonicalName.slice(0, 40) + "…" : canonicalName;
}

/**
 * Longer display label for the identity bar.
 * Prefers the curated index_name (which already includes track qualifier),
 * else returns the full canonical_name.
 */
export function labDisplayLabel(code: string, canonicalName: string): string {
  return getIndexName(code) ?? canonicalName;
}

// ---------------------------------------------------------------------------
// Term-lane data structure
// ---------------------------------------------------------------------------

export type TermLane = {
  shared: import("@/lib/families").CompareCourseEntry[];
  leftOnly: import("@/lib/families").CompareCourseEntry[];
  rightOnly: import("@/lib/families").CompareCourseEntry[];
};

/**
 * Groups courses by term into three lanes: shared / left-only / right-only.
 * Shared courses are bucketed by term_left; right-only by term_right.
 * Returns sorted [termNumber, TermLane] pairs.
 */
export function buildTermLanes(
  payload: import("@/lib/families").ComparePayload
): [number, TermLane][] {
  const map = new Map<number, TermLane>();
  const ensure = (t: number): TermLane => {
    if (!map.has(t)) map.set(t, { shared: [], leftOnly: [], rightOnly: [] });
    return map.get(t)!;
  };
  for (const c of payload.shared_courses) ensure(c.term_left ?? 0).shared.push(c);
  for (const c of payload.left_only_courses) ensure(c.term_left ?? 0).leftOnly.push(c);
  for (const c of payload.right_only_courses) ensure(c.term_right ?? 0).rightOnly.push(c);
  return [...map.entries()].sort(([a], [b]) => a - b);
}

// ---------------------------------------------------------------------------
// Payload builder — lab variant (no ProgramFamily required)
// ---------------------------------------------------------------------------

/**
 * Build a ComparePayload for any two programs without requiring a ProgramFamily.
 * Used in the prototype lab for the broadened compare universe.
 *
 * Precondition: both programs have non-empty rosters.
 * family_id is set to "lab" as a sentinel value.
 */
export function buildLabPayload(
  leftProgram: ProgramRecord,
  rightProgram: ProgramRecord,
  leftEnriched: ProgramEnriched,
  rightEnriched: ProgramEnriched
): import("@/lib/families").ComparePayload {
  const leftRoster: RosterCourse[] = leftEnriched.roster;
  const rightRoster: RosterCourse[] = rightEnriched.roster;

  const leftMap = new Map<string, RosterCourse>(leftRoster.map((c) => [c.code, c]));
  const rightMap = new Map<string, RosterCourse>(rightRoster.map((c) => [c.code, c]));

  const metrics = compareRosters(leftRoster, rightRoster);

  const shared_courses = metrics.shared_codes
    .map((code) => {
      const lc = leftMap.get(code)!;
      const rc = rightMap.get(code)!;
      return {
        code,
        title: lc.title,
        cus: lc.cus,
        term_left: lc.term,
        term_right: rc.term,
      };
    })
    .sort((a, b) => (a.term_left ?? 0) - (b.term_left ?? 0));

  const left_only_courses = metrics.left_only_codes
    .map((code) => {
      const lc = leftMap.get(code)!;
      return { code, title: lc.title, cus: lc.cus, term_left: lc.term, term_right: null };
    })
    .sort((a, b) => (a.term_left ?? 0) - (b.term_left ?? 0));

  const right_only_courses = metrics.right_only_codes
    .map((code) => {
      const rc = rightMap.get(code)!;
      return { code, title: rc.title, cus: rc.cus, term_left: null, term_right: rc.term };
    })
    .sort((a, b) => (a.term_right ?? 0) - (b.term_right ?? 0));

  const toMeta = (
    p: ProgramRecord,
    count: number
  ): import("@/lib/families").CompareProgramMeta => ({
    program_code: p.program_code,
    canonical_name: p.canonical_name,
    index_name: getIndexName(p.program_code),
    school: p.school,
    degree_level: classifyDegreeLevel(p),
    total_cus: p.cus_values.length > 0 ? p.cus_values[p.cus_values.length - 1] : null,
    first_seen: p.first_seen,
    course_count: count,
  });

  return {
    family_id: "lab",
    left: toMeta(leftProgram, leftRoster.length),
    right: toMeta(rightProgram, rightRoster.length),
    shared_courses,
    left_only_courses,
    right_only_courses,
    metrics,
  };
}
