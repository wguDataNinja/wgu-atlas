import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import {
  getSchools,
  getSchoolBySlug,
  getProgramsBySchool,
  getCoursesBySchool,
  getHomepageSummary,
  getPrograms,
} from "@/lib/data";
import type { ProgramRecord, CourseCard } from "@/lib/types";

type Props = { params: Promise<{ slug: string }> };

export async function generateStaticParams() {
  return getSchools().map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const school = getSchoolBySlug(slug);
  if (!school) return { title: "School Not Found" };
  return {
    title: school.current_name,
    description: `WGU ${school.current_name} — programs, courses, and catalog history.`,
  };
}

export default async function SchoolPage({ params }: Props) {
  const { slug } = await params;
  const school = getSchoolBySlug(slug);
  if (!school) notFound();

  const programs = getProgramsBySchool(school.canonical_key);
  const courses = getCoursesBySchool(school.historical_names);
  const summary = getHomepageSummary();
  const allPrograms = getPrograms();

  // School-filtered activity modules
  // Normalize school names: some homepage_summary entries use historical school names
  const schoolNormMap: Record<string, string> = {
    "Teachers College": "education",
    "School of Education": "education",
    "College of Business": "business",
    "School of Business": "business",
    "College of Health Professions": "health",
    "Leavitt School of Health": "health",
    "College of Information Technology": "technology",
    "School of Technology": "technology",
  };

  const recentVersionChanges = summary.recent_version_changes
    .filter((v) => schoolNormMap[v.school] === slug)
    .slice(0, 8);

  const newestPrograms = summary.newest_programs
    .filter((p) => schoolNormMap[p.school] === slug)
    .slice(0, 8);

  const recentCourseAdditions = summary.recent_course_additions
    .filter((c) => schoolNormMap[c.school] === slug)
    .slice(0, 10);

  // Programs sorted by first_seen descending
  const programsSortedByRecent = [...programs].sort((a, b) =>
    b.first_seen.localeCompare(a.first_seen)
  );

  // Group programs by degree level for organized display
  const programsByLevel = groupProgramsByLevel(programs);

  // Courses grouped by term (sort by code)
  const coursesSorted = [...courses].sort((a, b) => a.code.localeCompare(b.code));

  // Retired programs that were in this school
  const retiredInSchool = allPrograms.filter(
    (p) =>
      p.status === "RETIRED" &&
      p.colleges.some((c) => school.historical_names.includes(c))
  );

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      {/* Breadcrumb */}
      <nav className="text-sm text-slate-400 mb-6">
        <Link href="/schools" className="hover:text-blue-600">
          Schools
        </Link>
        <span className="mx-2">›</span>
        <span className="text-slate-600">{school.current_name}</span>
      </nav>

      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-sm bg-green-50 text-green-700 border border-green-200 px-2 py-0.5 rounded font-medium">
            Active
          </span>
          <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
            Source: WGU Catalog 2026-03
          </span>
        </div>
        <h1 className="text-3xl font-bold text-slate-800">{school.current_name}</h1>
        <p className="text-slate-500 mt-1">
          {programs.length} active programs · {courses.length} active courses
        </p>
      </div>

      {/* ================================================================
          SCHOOL LINEAGE
          ================================================================ */}
      <section className="mb-10">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 bg-blue-600 rounded" />
          <h2 className="text-lg font-bold text-slate-800">School History</h2>
          <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
            Source: WGU public catalog archive
          </span>
        </div>
        <SchoolLineage lineage={school.lineage} />
      </section>

      {/* ================================================================
          RECENT ACTIVITY
          ================================================================ */}
      {(newestPrograms.length > 0 ||
        recentVersionChanges.length > 0 ||
        recentCourseAdditions.length > 0) && (
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-1 h-5 bg-amber-500 rounded" />
            <h2 className="text-lg font-bold text-slate-800">Recent Activity</h2>
            <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
              Based on 2026-03 catalog
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Newest programs */}
            {newestPrograms.length > 0 && (
              <div className="border border-slate-200 rounded-lg p-4">
                <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
                  Newest Programs
                </h3>
                <ul className="space-y-2">
                  {newestPrograms.map((p) => (
                    <li key={p.program_code}>
                      <Link
                        href={`/programs/${p.program_code}`}
                        className="text-sm text-blue-700 hover:underline"
                      >
                        {p.degree_heading.length > 60
                          ? p.degree_heading.slice(0, 60) + "…"
                          : p.degree_heading}
                      </Link>
                      <span className="text-xs text-slate-400 ml-1">
                        {p.first_seen}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recent version changes */}
            {recentVersionChanges.length > 0 && (
              <div className="border border-slate-200 rounded-lg p-4">
                <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
                  Recent Version Updates
                </h3>
                <ul className="space-y-2">
                  {recentVersionChanges.map((v) => (
                    <li key={v.program_code}>
                      <Link
                        href={`/programs/${v.program_code}`}
                        className="text-sm text-blue-700 hover:underline"
                      >
                        {cleanHeading(v.degree_heading)}
                      </Link>
                      <span className="text-xs text-slate-400 ml-1">
                        v{v.version_stamp}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recent course additions */}
            {recentCourseAdditions.length > 0 && (
              <div className="border border-slate-200 rounded-lg p-4">
                <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
                  Recent Course Additions
                </h3>
                <ul className="space-y-2">
                  {recentCourseAdditions.map((c) => (
                    <li key={c.code}>
                      <Link
                        href={`/courses/${c.code}`}
                        className="text-sm text-blue-700 hover:underline"
                      >
                        {c.code} — {c.title.length > 40 ? c.title.slice(0, 40) + "…" : c.title}
                      </Link>
                      <span className="text-xs text-slate-400 ml-1">
                        {c.added_in}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </section>
      )}

      {/* ================================================================
          ACTIVE PROGRAMS
          ================================================================ */}
      <section className="mb-10">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 bg-blue-600 rounded" />
          <h2 className="text-lg font-bold text-slate-800">
            Active Programs ({programs.length})
          </h2>
          <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
            Source: WGU Catalog 2026-03
          </span>
        </div>

        {Object.entries(programsByLevel).map(([level, progs]) => (
          <div key={level} className="mb-5">
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-2">
              {level}
            </h3>
            <div className="border border-slate-200 rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <tbody>
                  {progs.map((p, i) => {
                    const latestCus =
                      p.cus_values.length > 0
                        ? p.cus_values[p.cus_values.length - 1]
                        : null;
                    return (
                      <tr
                        key={p.program_code}
                        className={`border-b border-slate-100 last:border-0 hover:bg-slate-50 ${
                          i % 2 === 0 ? "" : "bg-slate-50/50"
                        }`}
                      >
                        <td className="px-3 py-2">
                          <span className="font-mono text-xs bg-purple-50 text-purple-700 px-1.5 py-0.5 rounded">
                            {p.program_code}
                          </span>
                        </td>
                        <td className="px-3 py-2">
                          <Link
                            href={`/programs/${p.program_code}`}
                            className="text-blue-700 hover:underline"
                          >
                            {p.canonical_name}
                          </Link>
                        </td>
                        <td className="px-3 py-2 text-slate-400 text-xs text-right whitespace-nowrap">
                          {latestCus != null ? `${latestCus} CUs` : ""}
                        </td>
                        <td className="px-3 py-2 text-slate-400 text-xs text-right whitespace-nowrap">
                          since {p.first_seen}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </section>

      {/* ================================================================
          ACTIVE COURSES
          ================================================================ */}
      <section className="mb-10">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 bg-blue-600 rounded" />
          <h2 className="text-lg font-bold text-slate-800">
            Active Courses ({courses.length})
          </h2>
          <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
            Source: WGU Catalog 2026-03
          </span>
        </div>

        <details className="group">
          <summary className="cursor-pointer text-sm text-blue-600 hover:underline mb-3 list-none flex items-center gap-1">
            <span className="group-open:hidden">▶ Show all {courses.length} active courses</span>
            <span className="hidden group-open:inline">▼ Hide course list</span>
          </summary>
          <div className="border border-slate-200 rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="text-left px-3 py-2 text-xs font-medium text-slate-500">
                    Code
                  </th>
                  <th className="text-left px-3 py-2 text-xs font-medium text-slate-500">
                    Title
                  </th>
                  <th className="text-right px-3 py-2 text-xs font-medium text-slate-500">
                    CUs
                  </th>
                  <th className="text-right px-3 py-2 text-xs font-medium text-slate-500 hidden md:table-cell">
                    First seen
                  </th>
                </tr>
              </thead>
              <tbody>
                {coursesSorted.map((c, i) => (
                  <tr
                    key={c.code}
                    className={`border-b border-slate-100 last:border-0 hover:bg-slate-50 ${
                      i % 2 === 0 ? "" : "bg-slate-50/30"
                    }`}
                  >
                    <td className="px-3 py-1.5">
                      <Link
                        href={`/courses/${c.code}`}
                        className="font-mono text-xs text-blue-700 hover:underline"
                      >
                        {c.code}
                      </Link>
                    </td>
                    <td className="px-3 py-1.5 text-slate-700 text-sm">
                      {c.title}
                    </td>
                    <td className="px-3 py-1.5 text-slate-400 text-xs text-right">
                      {/* CUs not on CourseCard — would need detail lookup */}
                      —
                    </td>
                    <td className="px-3 py-1.5 text-slate-400 text-xs text-right hidden md:table-cell">
                      {c.first_seen}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </details>
      </section>

      {/* ================================================================
          DEPRECATED PROGRAMS
          ================================================================ */}
      {retiredInSchool.length > 0 && (
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-1 h-5 bg-slate-400 rounded" />
            <h2 className="text-lg font-bold text-slate-800">
              Deprecated Programs ({retiredInSchool.length})
            </h2>
          </div>
          <details className="group">
            <summary className="cursor-pointer text-sm text-slate-500 hover:text-blue-600 mb-3 list-none flex items-center gap-1">
              <span className="group-open:hidden">▶ Show deprecated programs</span>
              <span className="hidden group-open:inline">▼ Hide deprecated programs</span>
            </summary>
            <div className="border border-slate-200 rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="text-left px-3 py-2 text-xs font-medium text-slate-500">Code</th>
                    <th className="text-left px-3 py-2 text-xs font-medium text-slate-500">Name</th>
                    <th className="text-right px-3 py-2 text-xs font-medium text-slate-500 hidden md:table-cell">Last seen</th>
                  </tr>
                </thead>
                <tbody>
                  {retiredInSchool
                    .sort((a, b) => b.last_seen.localeCompare(a.last_seen))
                    .map((p, i) => (
                      <tr
                        key={p.program_code}
                        className={`border-b border-slate-100 last:border-0 hover:bg-slate-50 ${
                          i % 2 === 0 ? "" : "bg-slate-50/30"
                        }`}
                      >
                        <td className="px-3 py-1.5">
                          <Link
                            href={`/programs/${p.program_code}`}
                            className="font-mono text-xs text-slate-500 hover:text-blue-600 hover:underline"
                          >
                            {p.program_code}
                          </Link>
                        </td>
                        <td className="px-3 py-1.5 text-slate-500 text-sm">
                          <Link
                            href={`/programs/${p.program_code}`}
                            className="hover:text-blue-600 hover:underline"
                          >
                            {p.canonical_name}
                          </Link>
                        </td>
                        <td className="px-3 py-1.5 text-slate-400 text-xs text-right hidden md:table-cell">
                          {p.last_seen}
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </details>
        </section>
      )}

      {/* Back */}
      <div className="border-t border-slate-100 pt-6">
        <Link href="/schools" className="text-sm text-blue-600 hover:underline">
          ← Back to Schools
        </Link>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function SchoolLineage({
  lineage,
}: {
  lineage: Array<{ date: string; name: string }>;
}) {
  return (
    <div className="border border-slate-200 rounded-lg overflow-hidden">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 border-b border-slate-200">
          <tr>
            <th className="text-left px-4 py-2 text-xs font-medium text-slate-500">
              Effective
            </th>
            <th className="text-left px-4 py-2 text-xs font-medium text-slate-500">
              Name
            </th>
          </tr>
        </thead>
        <tbody>
          {lineage.map((entry, i) => {
            const isCurrent = i === lineage.length - 1;
            return (
              <tr
                key={entry.date}
                className={`border-b border-slate-100 last:border-0 ${
                  isCurrent ? "bg-blue-50/40" : ""
                }`}
              >
                <td className="px-4 py-2 font-mono text-xs text-slate-500">
                  {entry.date}
                </td>
                <td className="px-4 py-2 text-slate-800">
                  {entry.name}
                  {isCurrent && (
                    <span className="ml-2 text-xs text-green-600 font-medium">
                      current
                    </span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Strip truncated degree headings (artifact from catalog extraction). */
function cleanHeading(heading: string): string {
  const cleaned = heading.split("|")[0].trim();
  return cleaned.length > 65 ? cleaned.slice(0, 65) + "…" : cleaned;
}

/** Group programs by degree level prefix. */
function groupProgramsByLevel(
  programs: ProgramRecord[]
): Record<string, ProgramRecord[]> {
  const order = [
    "Doctor",
    "Master",
    "Bachelor",
    "Associate",
    "Endorsement",
    "Other",
  ];
  const groups: Record<string, ProgramRecord[]> = {};

  for (const p of programs) {
    const name = p.canonical_name.toLowerCase();
    let level = "Other";
    if (name.startsWith("doctor") || name.startsWith("ph.d")) level = "Doctoral";
    else if (name.startsWith("master") || name.startsWith("m.b.a") || name.startsWith("mba"))
      level = "Master's";
    else if (name.startsWith("bachelor")) level = "Bachelor's";
    else if (name.startsWith("associate")) level = "Associate";
    else if (name.startsWith("endorsement") || name.startsWith("graduate certificate"))
      level = "Certificates & Endorsements";
    else level = "Other";

    if (!groups[level]) groups[level] = [];
    groups[level].push(p);
  }

  // Sort within groups by name
  for (const g of Object.values(groups)) {
    g.sort((a, b) => a.canonical_name.localeCompare(b.canonical_name));
  }

  // Return in logical order
  const levelOrder = [
    "Doctoral",
    "Master's",
    "Bachelor's",
    "Associate",
    "Certificates & Endorsements",
    "Other",
  ];
  const ordered: Record<string, ProgramRecord[]> = {};
  for (const lv of levelOrder) {
    if (groups[lv] && groups[lv].length > 0) {
      ordered[lv] = groups[lv];
    }
  }
  return ordered;
}
