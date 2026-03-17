import type { Metadata } from "next";
import Link from "next/link";
import { getSchools, getProgramsBySchool, getCoursesBySchool } from "@/lib/data";

export const metadata: Metadata = {
  title: "Schools",
  description: "Browse WGU's four schools — Business, Health, Technology, and Education — with degree and course listings.",
};

const SCHOOL_DESCRIPTIONS: Record<string, string> = {
  business: "Bachelor's, master's, and MBA programs in accounting, management, marketing, IT management, finance, and related fields.",
  health: "Programs in nursing, healthcare administration, public health, health informatics, and allied health disciplines.",
  technology: "Programs in IT, cybersecurity, software engineering, data analytics, cloud computing, and computer science.",
  education: "Teacher preparation, educational leadership, and learning and technology programs across all grade bands.",
};

export default function SchoolsPage() {
  const schools = getSchools();

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Schools</h1>
        <p className="text-slate-500 mt-1">
          WGU is organized into four schools. Each school page shows its current
          degrees and courses, school background, and recent changes.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {schools.map((school) => {
          const programs = getProgramsBySchool(school.canonical_key);
          const courses = getCoursesBySchool(school.historical_names);
          const historicalNames = school.lineage
            .map((l) => l.name)
            .filter((n) => n !== school.current_name);

          return (
            <Link
              key={school.slug}
              href={`/schools/${school.slug}`}
              className="block border border-slate-200 rounded-lg p-5 hover:border-blue-300 hover:bg-blue-50/30 transition-colors"
            >
              <h2 className="text-lg font-bold text-slate-800 mb-1">
                {school.current_name}
              </h2>
              {historicalNames.length > 0 && (
                <p className="text-xs text-slate-400 mb-2">
                  Formerly: {historicalNames.join(" · ")}
                </p>
              )}
              <p className="text-sm text-slate-600 mb-3">
                {SCHOOL_DESCRIPTIONS[school.slug]}
              </p>
              <div className="flex gap-4 text-xs text-slate-500">
                <span>
                  <span className="font-semibold text-slate-700">{programs.length}</span>{" "}
                  current degrees
                </span>
                <span>
                  <span className="font-semibold text-slate-700">{courses.length}</span>{" "}
                  active courses
                </span>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
