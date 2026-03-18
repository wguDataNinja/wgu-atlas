import type { Metadata } from "next";
import { getCourses, getAllCourseCodes, getPrograms, getProgramEnriched } from "@/lib/data";
import { classifyDegreeLevel, type DegreeLevel } from "@/lib/programs";
import CoursePrototypeLab from "@/components/proto/CoursePrototypeLab";

export const metadata: Metadata = {
  title: "Course Browse — Prototype Lab",
  description: "Prototype lab: three interactive UI variants for the Courses browse/filter experience.",
};

function mapToDisplayLevel(level: DegreeLevel): string | null {
  if (level === "Bachelor's" || level === "Master's") return level;
  if (level === "Certificates & Endorsements") return "Certificate";
  // Doctoral, Associate, Other — skip for prototype
  return null;
}

export default function CoursePrototypePage() {
  const courses = getCourses();
  const allCodesArr = getAllCourseCodes();
  const programs = getPrograms();
  const enriched = getProgramEnriched();

  // programRosterMap: programCode → courseCode[]
  const programRosterMap: Record<string, string[]> = {};
  for (const [code, data] of Object.entries(enriched)) {
    programRosterMap[code] = (data.roster ?? []).map((r) => r.code);
  }

  // courseLevels: courseCode → level[] (from program roster membership)
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

  // Also tag cert-scope courses as Certificate
  for (const c of courses) {
    if (c.scope === "cert") {
      if (!courseLevelsMap[c.code]) courseLevelsMap[c.code] = new Set();
      courseLevelsMap[c.code].add("Certificate");
    }
  }

  const courseLevels: Record<string, string[]> = Object.fromEntries(
    Object.entries(courseLevelsMap).map(([k, v]) => [k, [...v]])
  );

  return (
    <div className="max-w-7xl mx-auto px-4 py-10">
      <div className="mb-8 pb-6 border-b border-slate-200">
        <div className="inline-block bg-amber-100 text-amber-800 text-xs font-mono px-2 py-1 rounded mb-3">
          PROTOTYPE LAB — NOT PRODUCTION UI
        </div>
        <h1 className="text-3xl font-bold text-slate-800">Course Browse — Prototype Variants</h1>
        <p className="text-slate-500 mt-2 max-w-2xl">
          Three UI approaches for the Courses browse/filter experience, stacked vertically for comparison.
          Same data, same filter logic — different presentation models. College is the primary filter in all three.
        </p>
      </div>
      <CoursePrototypeLab
        courses={courses}
        detailCodes={new Set(allCodesArr)}
        programs={programs.filter((p) => p.status === "ACTIVE")}
        programRosterMap={programRosterMap}
        courseLevels={courseLevels}
      />
    </div>
  );
}
