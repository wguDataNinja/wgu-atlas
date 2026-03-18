import type { Metadata } from "next";
import { Suspense } from "react";
import { getCourses, getAllCourseCodes, getPrograms, getProgramEnriched } from "@/lib/data";
import { classifyDegreeLevel } from "@/lib/programs";
import CourseExplorer from "@/components/courses/CourseExplorer";

export const metadata: Metadata = {
  title: "Courses",
  description: "Search and browse WGU courses — active and retired, with catalog history for each.",
};

function mapToDisplayLevel(level: string): string | null {
  if (level === "Bachelor's" || level === "Master's") return level;
  if (level === "Certificates & Endorsements") return "Certificate";
  return null;
}

export default function CoursesPage() {
  const courses = getCourses();
  const allCodes = new Set(getAllCourseCodes());
  const programs = getPrograms();
  const enriched = getProgramEnriched();

  // programRosterMap: programCode → courseCode[]
  const programRosterMap: Record<string, string[]> = {};
  for (const [code, data] of Object.entries(enriched)) {
    programRosterMap[code] = (data.roster ?? []).map((r) => r.code);
  }

  // courseLevels: courseCode → level[] (derived from active program rosters)
  const courseLevelsMap: Record<string, Set<string>> = {};
  for (const program of programs) {
    if (program.status !== "ACTIVE") continue;
    const dl = classifyDegreeLevel(program);
    const displayLevel = mapToDisplayLevel(dl);
    if (!displayLevel) continue;
    for (const code of programRosterMap[program.program_code] ?? []) {
      if (!courseLevelsMap[code]) courseLevelsMap[code] = new Set();
      courseLevelsMap[code].add(displayLevel);
    }
  }
  // Cert-scope courses are always Certificate level
  for (const c of courses) {
    if (c.scope === "cert") {
      if (!courseLevelsMap[c.code]) courseLevelsMap[c.code] = new Set();
      courseLevelsMap[c.code].add("Certificate");
    }
  }
  const courseLevels: Record<string, string[]> = Object.fromEntries(
    Object.entries(courseLevelsMap).map(([k, v]) => [k, [...v]])
  );

  const activeCount = courses.filter((c) => c.active).length;

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-800">Courses</h1>
        <p className="text-slate-500 mt-1">
          {activeCount.toLocaleString()} active courses across WGU&apos;s four colleges.
        </p>
      </div>
      <Suspense>
        <CourseExplorer
          courses={courses}
          detailCodes={allCodes}
          programs={programs.filter((p) => p.status === "ACTIVE")}
          programRosterMap={programRosterMap}
          courseLevels={courseLevels}
        />
      </Suspense>
    </div>
  );
}
