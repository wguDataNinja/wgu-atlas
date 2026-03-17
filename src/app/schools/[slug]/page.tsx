import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import {
  getSchools,
  getSchoolBySlug,
  getSchoolSlugByName,
  getProgramsBySchool,
  getCoursesBySchool,
  getOfficialResourcePlacementsForSurface,
  getHomepageSummary,
  getPrograms,
} from "@/lib/data";
import { groupProgramsByLevel } from "@/lib/programs";
import RelevantResources from "@/components/resources/RelevantResources";

type Props = { params: Promise<{ slug: string }> };

const SCHOOL_DESCRIPTIONS: Record<string, string> = {
  business:
    "Bachelor's, master's, and MBA degrees in accounting, management, marketing, IT management, finance, and related fields.",
  health:
    "Degrees in nursing, healthcare administration, public health, health informatics, and allied health disciplines.",
  technology:
    "Degrees in IT, cybersecurity, software engineering, data analytics, cloud computing, and computer science.",
  education:
    "Teacher preparation, educational leadership, and learning and technology degrees across all grade bands.",
};

export async function generateStaticParams() {
  return getSchools().map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const school = getSchoolBySlug(slug);
  if (!school) return { title: "School Not Found" };
  return {
    title: school.current_name,
    description: `WGU ${school.current_name} — degrees, courses, and catalog history.`,
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
  const hasRelevantResources =
    getOfficialResourcePlacementsForSurface("school_detail", school.slug).length > 0;

  const recentVersionChanges = summary.recent_version_changes
    .filter((v) => getSchoolSlugByName(v.school) === slug)
    .slice(0, 8);

  const newestPrograms = summary.newest_programs
    .filter((p) => getSchoolSlugByName(p.school) === slug)
    .slice(0, 8);

  const recentCourseAdditions = summary.recent_course_additions
    .filter((c) => getSchoolSlugByName(c.school) === slug)
    .slice(0, 10);

  const programsByLevel = groupProgramsByLevel(programs);
  const coursesSorted = [...courses].sort((a, b) => a.code.localeCompare(b.code));

  const retiredInSchool = allPrograms.filter(
    (p) =>
      p.status === "RETIRED" &&
      p.colleges.some((c) => school.historical_names.includes(c))
  );

  return (
    <div
      className={`${hasRelevantResources ? "max-w-7xl" : "max-w-5xl"} mx-auto px-4 py-10`}
    >
      <div
        className={
          hasRelevantResources
            ? "lg:grid lg:grid-cols-[minmax(0,1fr)_19rem] lg:gap-10"
            : ""
        }
      >
        <main className={hasRelevantResources ? "min-w-0" : ""}>
      {/* Breadcrumb */}
      <nav className="text-sm text-slate-400 mb-6">
        <Link href="/schools" className="hover:text-blue-600">
          Schools
        </Link>
        <span className="mx-2">›</span>
        <span className="text-slate-600">{school.current_name}</span>
      </nav>

      {/* ================================================================
          HEADER
          ================================================================ */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-800">{school.current_name}</h1>
        <p className="text-slate-500 mt-1">
          {programs.length} current degrees · {courses.length} active courses
        </p>
        <p className="text-xs text-slate-400 mt-2">
          Source: WGU public catalog · 2026-03 edition
        </p>
      </div>

      {/* ================================================================
          SHORT DESCRIPTION
          ================================================================ */}
      {SCHOOL_DESCRIPTIONS[slug] && (
        <p className="text-slate-600 text-sm leading-relaxed mb-8">
          {SCHOOL_DESCRIPTIONS[slug]}
        </p>
      )}

      {/* ================================================================
          CURRENT DEGREES
          ================================================================ */}
      <section className="mb-10">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 bg-blue-600 rounded" />
          <h2 className="text-lg font-bold text-slate-800">
            Current Degrees ({programs.length})
          </h2>
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
                  <th className="text-right px-3 py-2 text-xs font-medium text-slate-500 hidden md:table-cell">
                    First in catalog
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
          RECENT CHANGES
          ================================================================ */}
      {(newestPrograms.length > 0 ||
        recentVersionChanges.length > 0 ||
        recentCourseAdditions.length > 0) && (
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-1 h-5 bg-amber-500 rounded" />
            <h2 className="text-lg font-bold text-slate-800">Recent Changes</h2>
            <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
              Based on 2026-03 catalog
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {newestPrograms.length > 0 && (
              <div className="border border-slate-200 rounded-lg p-4">
                <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
                  New Degrees
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

            {recentVersionChanges.length > 0 && (
              <div className="border border-slate-200 rounded-lg p-4">
                <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
                  Recent Degree Updates
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
          RETIRED DEGREES
          ================================================================ */}
      {retiredInSchool.length > 0 && (
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-1 h-5 bg-slate-300 rounded" />
            <h2 className="text-base font-semibold text-slate-600">
              Retired Degrees ({retiredInSchool.length})
            </h2>
          </div>
          <details className="group">
            <summary className="cursor-pointer text-sm text-slate-500 hover:text-blue-600 mb-3 list-none flex items-center gap-1">
              <span className="group-open:hidden">▶ Show retired degrees</span>
              <span className="hidden group-open:inline">▼ Hide retired degrees</span>
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

      {/* ================================================================
          SCHOOL BACKGROUND / EARLIER NAMES
          ================================================================ */}
      <section className="mb-10">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 bg-slate-300 rounded" />
          <h2 className="text-base font-semibold text-slate-700">School Background</h2>
        </div>
        <SchoolLineage lineage={school.lineage} />
      </section>

      {/* Back */}
      <div className="border-t border-slate-100 pt-6">
        <Link href="/schools" className="text-sm text-blue-600 hover:underline">
          ← Back to Schools
        </Link>
      </div>
        </main>

        {hasRelevantResources && (
          <aside className="mt-8 self-start lg:sticky lg:top-24 lg:mt-0">
            <RelevantResources surface="school_detail" surfaceKey={school.slug} />
          </aside>
        )}
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

function cleanHeading(heading: string): string {
  const cleaned = heading.split("|")[0].trim();
  return cleaned.length > 65 ? cleaned.slice(0, 65) + "…" : cleaned;
}
