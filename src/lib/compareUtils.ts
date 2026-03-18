// ---------------------------------------------------------------------------
// Compare feature — production utilities.
// Server-safe (no "use client"). Safe to import from both server and client code.
//
// Extracted from src/components/proto/compareProtoUtils.ts into lib/ as part
// of the prototype → production rollout.
// ---------------------------------------------------------------------------

import type { ProgramRecord, ProgramEnriched, RosterCourse } from "@/lib/types";
import type { ComparePayload, CompareProgramMeta, CompareCourseEntry } from "@/lib/families";
import type { CompareResult } from "@/lib/programs";
import { classifyDegreeLevel, compareRosters } from "@/lib/programs";
import { getIndexName } from "@/lib/families";

// Re-export types so consumers only need one import
export type { ComparePayload, CompareProgramMeta, CompareCourseEntry, CompareResult };

// ---------------------------------------------------------------------------
// Compare universe exclusions
// ---------------------------------------------------------------------------

/**
 * Program codes excluded from the compare universe.
 *
 * Pathway programs (MSCSUG / MSITUG / MSSWEUG): classify as Bachelor's by
 * name prefix but are upper-division accelerated bridge paths, not standalone
 * degrees. Including them would produce spurious "highly similar" results
 * against their corresponding BS programs.
 *
 * Identical-name group (MEDETID / MEDETIDA / MEDETIDK12): all three share the
 * exact same canonical_name. Without curated track_labels the compare UI
 * shows the same name on both sides and is unusable.
 */
export const LAB_EXCLUSIONS = new Set([
  "MSCSUG",
  "MSITUG",
  "MSSWEUG",
  "MEDETID",
  "MEDETIDA",
  "MEDETIDK12",
]);

// ---------------------------------------------------------------------------
// Short-label helpers
// ---------------------------------------------------------------------------

/**
 * Short differentiating label for column headers and compact chips.
 * Extracts the most specific/differentiating part of the degree name.
 *
 * Priority:
 *   1. Curated track label via getIndexName() — e.g. "Java Track", "C# Track"
 *   2. Specialization suffix after " - " — e.g. "Amazon Web Services"
 *   3. Trailing parenthetical "(qualifier)" — e.g. "Secondary Biology"
 *   4. Subject after the first comma — e.g. "Data Analytics"
 *   5. Strip common degree-type prefix for names without a comma
 *      — e.g. "Bachelor of Science Supply Chain..." → "Supply Chain..."
 *   6. Truncate at 42 chars
 */
export function labShortLabel(code: string, canonicalName: string): string {
  // 1. Curated track label from PILOT_FAMILIES (BSSWE/BSSWE_C, MSDA tracks)
  const idx = getIndexName(code);
  if (idx) {
    const m = idx.match(/\(([^)]+)\)$/);
    return m ? m[1] : idx;
  }
  // 2. "Base Degree - Specialization" pattern
  const dashIdx = canonicalName.indexOf(" - ");
  if (dashIdx >= 0) return canonicalName.slice(dashIdx + 3);
  // 3. Trailing parenthetical
  const pm = canonicalName.match(/\(([^)]+)\)$/);
  if (pm) return pm[1];
  // 4. Subject after first comma: "Bachelor of Science, Finance" → "Finance"
  const commaIdx = canonicalName.indexOf(",");
  if (commaIdx > 0 && commaIdx < canonicalName.length - 5) {
    return canonicalName.slice(commaIdx + 2);
  }
  // 5. Strip degree-type prefix for names with no comma
  //    Handles "Bachelor of Science Supply Chain..." → "Supply Chain..."
  //    and "Bachelor of Science in Psychology" → "Psychology"
  const stripped = canonicalName.replace(
    /^(?:bachelor of science(?:\s+in)?|bachelor of arts(?:\s+in)?)\s+/i,
    ""
  );
  if (stripped !== canonicalName) return stripped;
  // 6. Truncate
  return canonicalName.length > 42 ? canonicalName.slice(0, 40) + "…" : canonicalName;
}

/**
 * Longer display label for the identity bar.
 * Prefers the curated index_name (includes track qualifier) when available.
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
 * Shared courses are bucketed by term_left; right-only by term_right.
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
// Payload builder
// ---------------------------------------------------------------------------

/**
 * Build a ComparePayload for any two programs.
 * Does not require a ProgramFamily — works for any same-college + same-level pair.
 * Only uses roster data from enriched records; description/outcomes not needed.
 */
export function buildLabPayload(
  leftProgram: ProgramRecord,
  rightProgram: ProgramRecord,
  leftEnriched: Pick<ProgramEnriched, "roster">,
  rightEnriched: Pick<ProgramEnriched, "roster">
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
    family_id: "compare",
    left: toMeta(leftProgram, leftRoster.length),
    right: toMeta(rightProgram, rightRoster.length),
    shared_courses,
    left_only_courses,
    right_only_courses,
    metrics,
  };
}
