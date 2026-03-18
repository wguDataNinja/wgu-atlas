// ---------------------------------------------------------------------------
// Compare prototype lab — shared data utilities.
// Server-safe (no "use client"). Safe to import in both server and client code.
// ---------------------------------------------------------------------------

import type { ProgramRecord, ProgramEnriched, RosterCourse } from "@/lib/types";
import type { ComparePayload, CompareProgramMeta, CompareCourseEntry } from "@/lib/families";
import type { CompareResult } from "@/lib/programs";
import { classifyDegreeLevel, compareRosters } from "@/lib/programs";
import { getIndexName } from "@/lib/families";

// Re-export types so lab components only need to import from this file
export type { ComparePayload, CompareProgramMeta, CompareCourseEntry, CompareResult };

// ---------------------------------------------------------------------------
// Lab universe exclusions
// ---------------------------------------------------------------------------

export const LAB_EXCLUSIONS = new Set([
  // Pathway/bridge programs: name starts with "Bachelor of Science" but are
  // upper-division accelerated paths into a master's, not standalone degrees.
  "MSCSUG",
  "MSITUG",
  "MSSWEUG",
  // Identical canonical name group — all three share the exact same
  // canonical_name with no curated track_labels to disambiguate them.
  "MEDETID",
  "MEDETIDA",
  "MEDETIDK12",
]);

// ---------------------------------------------------------------------------
// Label helpers
// ---------------------------------------------------------------------------

/**
 * Short differentiating label for column headers and compact chips.
 *
 * Priority:
 *   1. Curated track label from PILOT_FAMILIES (e.g. "Java Track", "C# Track")
 *   2. Specialization suffix after " - " (e.g. "Amazon Web Services")
 *   3. Trailing parenthetical qualifier (e.g. "Secondary Biology")
 *   4. Degree subject after the first comma (e.g. "Data Analytics")
 *   5. Truncated canonical name
 */
export function labShortLabel(code: string, canonicalName: string): string {
  const idx = getIndexName(code);
  if (idx) {
    const m = idx.match(/\(([^)]+)\)$/);
    return m ? m[1] : idx;
  }
  const dashIdx = canonicalName.indexOf(" - ");
  if (dashIdx >= 0) return canonicalName.slice(dashIdx + 3);
  const m = canonicalName.match(/\(([^)]+)\)$/);
  if (m) return m[1];
  const commaIdx = canonicalName.indexOf(",");
  if (commaIdx > 0 && commaIdx < canonicalName.length - 5) {
    return canonicalName.slice(commaIdx + 2);
  }
  return canonicalName.length > 42 ? canonicalName.slice(0, 40) + "…" : canonicalName;
}

/**
 * Longer display label for the identity bar.
 * Prefers the curated index_name (includes track qualifier) if available.
 */
export function labDisplayLabel(code: string, canonicalName: string): string {
  return getIndexName(code) ?? canonicalName;
}

// ---------------------------------------------------------------------------
// Term-lane data structure
// ---------------------------------------------------------------------------

export type TermLane = {
  shared: CompareCourseEntry[];
  leftOnly: CompareCourseEntry[];
  rightOnly: CompareCourseEntry[];
};

/**
 * Groups courses by term into three lanes: shared / left-only / right-only.
 * Shared courses bucketed by term_left; right-only by term_right.
 */
export function buildTermLanes(payload: ComparePayload): [number, TermLane][] {
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
 * family_id is set to "lab" as a sentinel value.
 */
export function buildLabPayload(
  leftProgram: ProgramRecord,
  rightProgram: ProgramRecord,
  leftEnriched: ProgramEnriched,
  rightEnriched: ProgramEnriched
): ComparePayload {
  const leftRoster: RosterCourse[] = leftEnriched.roster;
  const rightRoster: RosterCourse[] = rightEnriched.roster;

  const leftMap = new Map<string, RosterCourse>(leftRoster.map((c) => [c.code, c]));
  const rightMap = new Map<string, RosterCourse>(rightRoster.map((c) => [c.code, c]));

  const metrics = compareRosters(leftRoster, rightRoster);

  const shared_courses: CompareCourseEntry[] = metrics.shared_codes
    .map((code) => {
      const lc = leftMap.get(code)!;
      const rc = rightMap.get(code)!;
      return { code, title: lc.title, cus: lc.cus, term_left: lc.term, term_right: rc.term };
    })
    .sort((a, b) => (a.term_left ?? 0) - (b.term_left ?? 0));

  const left_only_courses: CompareCourseEntry[] = metrics.left_only_codes
    .map((code) => {
      const lc = leftMap.get(code)!;
      return { code, title: lc.title, cus: lc.cus, term_left: lc.term, term_right: null };
    })
    .sort((a, b) => (a.term_left ?? 0) - (b.term_left ?? 0));

  const right_only_courses: CompareCourseEntry[] = metrics.right_only_codes
    .map((code) => {
      const rc = rightMap.get(code)!;
      return { code, title: rc.title, cus: rc.cus, term_left: null, term_right: rc.term };
    })
    .sort((a, b) => (a.term_right ?? 0) - (b.term_right ?? 0));

  const toMeta = (p: ProgramRecord, count: number): CompareProgramMeta => ({
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
