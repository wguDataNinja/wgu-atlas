import fs from "fs";
import path from "path";
import type {
  CourseCard,
  CourseDetail,
  CatalogEvent,
  HomepageSummary,
  ProgramRecord,
  ProgramEnriched,
  SchoolRecord,
} from "./types";

const PUBLIC_DATA = path.join(process.cwd(), "public", "data");
const INTERNAL_DATA = path.join(process.cwd(), "data");

// ---------------------------------------------------------------------------
// Courses
// ---------------------------------------------------------------------------

export function getCourses(): CourseCard[] {
  const raw = fs.readFileSync(path.join(PUBLIC_DATA, "courses.json"), "utf-8");
  return JSON.parse(raw);
}

/**
 * Load course detail. Tries the individual detail file first (active AP, has
 * programs_timeline). Falls back to canonical_courses.json for retired and
 * cert-only codes, normalizing string fields to arrays.
 */
export function getCourseDetail(code: string): CourseDetail | null {
  const filePath = path.join(PUBLIC_DATA, "courses", `${code}.json`);
  if (fs.existsSync(filePath)) {
    const raw = fs.readFileSync(filePath, "utf-8");
    return JSON.parse(raw);
  }
  // Fallback: canonical_courses.json (all 1,641 codes)
  const canon = getCanonicalCourses();
  const raw = canon[code];
  if (!raw) return null;
  // Normalize string fields that individual detail files store as arrays
  return {
    ...raw,
    observed_titles: splitCanonicalList(raw.observed_titles as unknown as string, " | "),
    current_programs: splitCanonicalList(raw.current_programs as unknown as string, "; "),
    colleges_seen: Array.isArray(raw.colleges_seen)
      ? raw.colleges_seen
      : splitCanonicalList(raw.colleges_seen as unknown as string, " | "),
  };
}

/** Split a canonical delimited string into an array, filtering empty entries. */
function splitCanonicalList(value: unknown, sep: string): string[] {
  if (!value || typeof value !== "string") return [];
  return value.split(sep).map((s) => s.trim()).filter(Boolean);
}

/** Returns all course codes that have any detail (active AP + retired + cert). */
export function getAllCourseCodes(): string[] {
  return Object.keys(getCanonicalCourses());
}

/** Returns codes that have a rich individual detail file (active AP only). */
export function getDetailableCodes(): string[] {
  const dir = path.join(PUBLIC_DATA, "courses");
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .map((f) => f.replace(".json", ""));
}

// Lazy-loaded canonical courses map (code → detail)
let _canonicalCourses: Record<string, CourseDetail> | null = null;
function getCanonicalCourses(): Record<string, CourseDetail> {
  if (!_canonicalCourses) {
    const raw = fs.readFileSync(
      path.join(INTERNAL_DATA, "canonical_courses.json"),
      "utf-8"
    );
    _canonicalCourses = JSON.parse(raw);
  }
  return _canonicalCourses!;
}

// ---------------------------------------------------------------------------
// Programs
// ---------------------------------------------------------------------------

let _programs: ProgramRecord[] | null = null;

export function getPrograms(): ProgramRecord[] {
  if (!_programs) {
    const raw = fs.readFileSync(
      path.join(PUBLIC_DATA, "programs.json"),
      "utf-8"
    );
    _programs = JSON.parse(raw);
  }
  return _programs!;
}

export function getProgramDetail(code: string): ProgramRecord | null {
  return getPrograms().find((p) => p.program_code === code) ?? null;
}

export function getAllProgramCodes(): string[] {
  return getPrograms().map((p) => p.program_code);
}

/**
 * Build a map from degree heading string → program_code.
 * When multiple programs share a heading (e.g. retired + active successor),
 * prefer ACTIVE; among same status, prefer the latest last_seen.
 */
export function getHeadingToProgramCode(): Record<string, string> {
  const programs = getPrograms();
  const map: Record<string, string> = {};

  // Process RETIRED first, then ACTIVE — so ACTIVE wins on conflict
  const sorted = [...programs].sort((a, b) => {
    if (a.status !== b.status) return a.status === "ACTIVE" ? 1 : -1;
    return a.last_seen < b.last_seen ? -1 : 1;
  });

  for (const p of sorted) {
    for (const heading of p.degree_headings) {
      map[heading] = p.program_code;
    }
  }
  return map;
}

// ---------------------------------------------------------------------------
// Program enriched (descriptions, rosters, outcomes)
// ---------------------------------------------------------------------------

let _programEnriched: Record<string, ProgramEnriched> | null = null;

export function getProgramEnriched(): Record<string, ProgramEnriched> {
  if (!_programEnriched) {
    const raw = fs.readFileSync(
      path.join(PUBLIC_DATA, "program_enriched.json"),
      "utf-8"
    );
    _programEnriched = JSON.parse(raw);
  }
  return _programEnriched!;
}

export function getProgramEnrichedByCode(code: string): ProgramEnriched | null {
  return getProgramEnriched()[code] ?? null;
}

// ---------------------------------------------------------------------------
// Schools — static data derived from README_INTERNAL.md §12 (College name history)
// ---------------------------------------------------------------------------

// School lineage extracted from README_INTERNAL.md §12
// program_count at lineage entry = approximate active programs at that era
const SCHOOL_RECORDS: SchoolRecord[] = [
  {
    slug: "business",
    current_name: "School of Business",
    canonical_key: "School of Business",
    historical_names: ["College of Business", "School of Business"],
    lineage: [
      { date: "2017-01", name: "College of Business" },
      { date: "2024-02", name: "School of Business" },
    ],
  },
  {
    slug: "health",
    current_name: "Leavitt School of Health",
    canonical_key: "Leavitt School of Health",
    historical_names: ["College of Health Professions", "Leavitt School of Health"],
    lineage: [
      { date: "2017-01", name: "College of Health Professions" },
      { date: "2023-01", name: "Leavitt School of Health" },
    ],
  },
  {
    slug: "technology",
    current_name: "School of Technology",
    canonical_key: "School of Technology",
    historical_names: ["College of Information Technology", "School of Technology"],
    lineage: [
      { date: "2017-01", name: "College of Information Technology" },
      { date: "2024-04", name: "School of Technology" },
    ],
  },
  {
    slug: "education",
    current_name: "School of Education",
    canonical_key: "School of Education",
    historical_names: ["Teachers College", "School of Education"],
    lineage: [
      { date: "2017-01", name: "Teachers College" },
      { date: "2023-03", name: "School of Education" },
    ],
  },
];

export function getSchools(): SchoolRecord[] {
  return SCHOOL_RECORDS;
}

export function getSchoolBySlug(slug: string): SchoolRecord | null {
  return SCHOOL_RECORDS.find((s) => s.slug === slug) ?? null;
}

/** Programs belonging to a given school (by canonical_key, current school field). */
export function getProgramsBySchool(canonicalKey: string): ProgramRecord[] {
  return getPrograms().filter(
    (p) => p.status === "ACTIVE" && p.school === canonicalKey
  );
}

/** Course cards belonging to a given school (by current_college, any historical name). */
export function getCoursesBySchool(historicalNames: string[]): CourseCard[] {
  return getCourses().filter(
    (c) => c.active && historicalNames.includes(c.current_college)
  );
}

// ---------------------------------------------------------------------------
// Events + homepage
// ---------------------------------------------------------------------------

export function getEvents(): CatalogEvent[] {
  const raw = fs.readFileSync(path.join(PUBLIC_DATA, "events.json"), "utf-8");
  return JSON.parse(raw);
}

export function getHomepageSummary(): HomepageSummary {
  const raw = fs.readFileSync(
    path.join(PUBLIC_DATA, "homepage_summary.json"),
    "utf-8"
  );
  return JSON.parse(raw);
}
