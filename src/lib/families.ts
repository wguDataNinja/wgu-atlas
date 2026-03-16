// ---------------------------------------------------------------------------
// Degree Compare — pilot family definitions and compare payload builder.
// Session 2 foundation: curated family data + v1 content contract.
//
// Design notes:
//   - Families are curated explicitly; auto-detection is deferred (DECISIONS §15.3).
//   - V1 compare is always 2-way; buildComparePayload takes exactly one left + one right.
//   - A family may list >2 programs (e.g. MSDA has 3 tracks); the caller selects the pair.
//   - Comparable-family qualification rules: see DECISIONS §15.11.
//
// Two-name model (Session 4):
//   - canonical_name: the full body/degree name from programs.json. Preserved unchanged.
//     Same for all programs that share a degree title (e.g., both SWE tracks).
//   - index_name: the catalog index/TOC name from program_index_[date].json.
//     Includes track qualifiers the body name omits. Used in compare context only.
//     Source: WGU_catalog outputs — curated here in track_labels per family.
//     See DECISIONS §15.17 and ATLAS_SPEC §12C.
// ---------------------------------------------------------------------------

import type { ProgramRecord, ProgramEnriched, RosterCourse } from "./types";
import { classifyDegreeLevel, compareRosters } from "./programs";
import type { DegreeLevel, CompareResult } from "./programs";

// ---------------------------------------------------------------------------
// Family type
// ---------------------------------------------------------------------------

export interface ProgramFamily {
  /** Stable identifier. Used as foreign key in compare URLs / affordances. */
  id: string;
  /** Student-facing family label (e.g. "Software Engineering"). */
  label: string;
  /** Canonical school key — matches ProgramRecord.school. */
  school: string;
  degree_level: DegreeLevel;
  /** All program codes in this family. V1 UI renders 2-way pairs only. */
  program_codes: string[];
  /**
   * Student-facing framing for the family: why this comparison is useful
   * and what the main structural difference is.
   */
  compare_note: string;
  /**
   * Catalog index/TOC display names, keyed by program_code.
   * Source: program_index_[date].json from WGU_catalog trusted outputs.
   * These names include track qualifiers absent from canonical_name.
   * Example: "B.S. Software Engineering (Java Track)" vs canonical
   * "Bachelor of Science, Software Engineering".
   * Not all families need this — only families where canonical_name is identical
   * across members require disambiguation here.
   */
  track_labels?: Record<string, string>;
}

// ---------------------------------------------------------------------------
// Pilot families — Session 2 curated set (2026-03-15)
// ---------------------------------------------------------------------------

/**
 * Curated pilot families for Degree Compare v1.
 * Only families listed here get compare affordances.
 * Expand in future sessions after validating new pairs.
 */
export const PILOT_FAMILIES: ProgramFamily[] = [
  // ── Primary prototype ───────────────────────────────────────────────────
  // BSSWE vs BSSWE_C: same 119-CU program, different language track.
  // 33 of 38 courses shared (Jaccard 0.80). 5 Java-only, 3 C#-only.
  // The unique courses are exclusively language-stack courses; no other
  // curriculum differences. CU totals are equal despite different course
  // counts (C# courses carry more CUs each).
  {
    id: "bsswe-tracks",
    label: "Software Engineering",
    school: "School of Technology",
    degree_level: "Bachelor's",
    program_codes: ["BSSWE", "BSSWE_C"],
    compare_note:
      "Both tracks cover the same Software Engineering curriculum. " +
      "The difference is the programming language: Java (with Android mobile development) " +
      "or C# (.NET mobile development). 33 of the courses are identical.",
    // Source: WGU_catalog program_index_2026_03.json, School of Technology.
    // Both tracks share the body name "Bachelor of Science, Software Engineering";
    // the index is the only catalog location that distinguishes them by name.
    track_labels: {
      BSSWE: "B.S. Software Engineering (Java Track)",
      BSSWE_C: "B.S. Software Engineering (C# Track)",
    },
  },

  // ── Secondary validation family ─────────────────────────────────────────
  // MSDA 3-track family: 7-course shared core (Terms 1–3), then 4 unique
  // specialization courses per track (Terms 3–4 vary).
  // Jaccard between any two tracks: 0.47 (7 shared / 15 union).
  // All three tracks: 11 courses, 32 CUs, first seen 2024-06.
  // V1 renders 2-way pairs. MSDADPE (Decision Process Engineering) is the
  // third member; defer to later sessions for 3-way UI.
  {
    id: "msda-tracks",
    label: "MS Data Analytics",
    school: "School of Technology",
    degree_level: "Master's",
    program_codes: ["MSDADE", "MSDADS", "MSDADPE"],
    compare_note:
      "All three tracks share the same 7-course Data Analytics foundation " +
      "(analytics programming, data management, statistical mining, " +
      "data storytelling, and deployment). " +
      "The final 4 courses are the specialization: " +
      "Data Engineering (cloud and pipeline focus), " +
      "Data Science (ML and optimization focus), or " +
      "Decision Process Engineering (business process focus).",
    // Source: WGU_catalog program_index_2026_03.json, School of Technology.
    // Body names already contain track info via " - [Track]" suffix, but use
    // abbreviated "M.S." prefix in the index. Both forms preserved; index
    // form used in compare UI for consistency with BSSWE family.
    track_labels: {
      MSDADE: "M.S. Data Analytics (Data Engineering)",
      MSDADS: "M.S. Data Analytics (Data Science)",
      MSDADPE: "M.S. Data Analytics (Decision Process Engineering)",
    },
  },
];

// ---------------------------------------------------------------------------
// Family lookup helpers
// ---------------------------------------------------------------------------

/** Returns the family a program belongs to, or null if it is not in any family. */
export function getFamilyByCode(programCode: string): ProgramFamily | null {
  return PILOT_FAMILIES.find((f) => f.program_codes.includes(programCode)) ?? null;
}

/**
 * Returns true if both programs belong to the same family.
 * V1 gate: only call buildComparePayload when this is true.
 */
export function areProgramsComparable(codeA: string, codeB: string): boolean {
  const family = getFamilyByCode(codeA);
  return family !== null && family.program_codes.includes(codeB);
}

/**
 * Returns the sibling program codes in a family — i.e., the codes a student
 * would be offered as compare targets from a given program's page.
 */
export function getSiblingCodes(programCode: string): string[] {
  const family = getFamilyByCode(programCode);
  if (!family) return [];
  return family.program_codes.filter((c) => c !== programCode);
}

/**
 * Returns the catalog index/TOC display name for a program, or null if not
 * defined for its family. Index names include track qualifiers absent from
 * canonical_name. Use in compare UI context only.
 *
 * Example: getIndexName("BSSWE") → "B.S. Software Engineering (Java Track)"
 */
export function getIndexName(programCode: string): string | null {
  const family = getFamilyByCode(programCode);
  return family?.track_labels?.[programCode] ?? null;
}

/**
 * Extracts the short track qualifier from an index name.
 * Returns the parenthetical suffix, or null if no parenthetical.
 *
 * Examples:
 *   "B.S. Software Engineering (Java Track)"     → "Java Track"
 *   "M.S. Data Analytics (Data Engineering)"     → "Data Engineering"
 *   "Bachelor of Science, Software Engineering"  → null
 */
export function extractTrackLabel(indexName: string | null): string | null {
  if (!indexName) return null;
  const m = indexName.match(/\(([^)]+)\)$/);
  return m ? m[1] : null;
}

// ---------------------------------------------------------------------------
// V1 compare payload types
// ---------------------------------------------------------------------------

export interface CompareProgramMeta {
  program_code: string;
  /** Full body/degree name from programs.json. Preserved unchanged; same for all tracks. */
  canonical_name: string;
  /**
   * Catalog index/TOC display name (from family.track_labels). Includes track
   * qualifier absent from canonical_name. Null when not defined for this family.
   * Use in compare UI to disambiguate programs with identical canonical names.
   *
   * Example: "B.S. Software Engineering (Java Track)"
   */
  index_name: string | null;
  school: string;
  degree_level: DegreeLevel;
  /** Latest total CUs from catalog. */
  total_cus: number | null;
  /**
   * When the program first appeared in the catalog ("YYYY-MM").
   * Included in v1 per DECISIONS §15.12.
   */
  first_seen: string;
  /** Total courses in this program's current roster. */
  course_count: number;
}

/**
 * A single course entry in the compare output.
 * term_left: term in left program (null if not in left).
 * term_right: term in right program (null if not in right).
 * For shared courses: both are non-null (may differ — minor placement drift).
 * For left-only: term_left is set, term_right is null.
 * For right-only: term_left is null, term_right is set.
 */
export interface CompareCourseEntry {
  code: string;
  title: string;
  cus: number;
  term_left: number | null;
  term_right: number | null;
}

/**
 * The complete v1 compare output produced by buildComparePayload.
 * This is the data contract for the compare view (DECISIONS §15.13).
 *
 * Display ordering guidance:
 *   1. Program header (left vs right) with degree_level, school, CUs, first_seen.
 *   2. Overlap summary bar: shared_count, left_only_count, right_only_count, jaccard %.
 *   3. Shared courses list (sorted by term_left).
 *   4. Left-only courses (sorted by term_left).
 *   5. Right-only courses (sorted by term_right).
 *
 * Fields deferred from v1:
 *   - Course first_seen_in_program (when a course joined this specific roster).
 *   - Outcome differences per program.
 *   - Term placement differences beyond what term_left / term_right already captures.
 *   - Official-context resource links per program.
 */
export interface ComparePayload {
  /** The family this comparison belongs to. */
  family_id: string;
  left: CompareProgramMeta;
  right: CompareProgramMeta;
  /** Courses present in both programs, sorted by term_left. */
  shared_courses: CompareCourseEntry[];
  /** Courses present only in the left program, sorted by term_left. */
  left_only_courses: CompareCourseEntry[];
  /** Courses present only in the right program, sorted by term_right. */
  right_only_courses: CompareCourseEntry[];
  /** Raw comparison metrics from compareRosters(). */
  metrics: CompareResult;
}

// ---------------------------------------------------------------------------
// Payload builder
// ---------------------------------------------------------------------------

/**
 * Assemble the full v1 ComparePayload from two programs and their enriched rosters.
 *
 * Precondition: areProgramsComparable(left.program_code, right.program_code) === true.
 * Caller is responsible for validating this before invoking.
 *
 * Course identity: exact code match only, per DECISIONS §4.6.
 * Source: ProgramEnriched.roster from public/data/program_enriched.json.
 */
export function buildComparePayload(
  family: ProgramFamily,
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
    index_name: family.track_labels?.[p.program_code] ?? null,
    school: p.school,
    degree_level: classifyDegreeLevel(p),
    total_cus: p.cus_values.length > 0 ? p.cus_values[p.cus_values.length - 1] : null,
    first_seen: p.first_seen,
    course_count: count,
  });

  return {
    family_id: family.id,
    left: toMeta(leftProgram, leftRoster.length),
    right: toMeta(rightProgram, rightRoster.length),
    shared_courses,
    left_only_courses,
    right_only_courses,
    metrics,
  };
}
