import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import {
  getProgramDetail,
  getAllProgramCodes,
  getProgramEnrichedByCode,
  getOfficialResourcePlacementsForSurface,
  getSchools,
} from "@/lib/data";
import type { RosterCourse } from "@/lib/types";
import RelevantResources from "@/components/resources/RelevantResources";

type Props = { params: Promise<{ code: string }> };

export async function generateStaticParams() {
  return getAllProgramCodes().map((code) => ({ code }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { code } = await params;
  const program = getProgramDetail(code);
  if (!program) return { title: "Degree Not Found" };
  const statusLabel = program.status === "ACTIVE" ? "" : " (Retired)";
  return {
    title: `${program.canonical_name}${statusLabel}`,
    description: `WGU degree: ${program.canonical_name}. First offered ${program.first_seen}.`,
  };
}

export default async function ProgramDetailPage({ params }: Props) {
  const { code } = await params;
  const program = getProgramDetail(code);
  if (!program) notFound();

  const enriched = getProgramEnrichedByCode(code);
  const schools = getSchools();
  const hasRelevantResources =
    getOfficialResourcePlacementsForSurface("program_detail", program.program_code)
      .length > 0;

  const isActive = program.status === "ACTIVE";
  const latestCus =
    program.cus_values.length > 0
      ? program.cus_values[program.cus_values.length - 1]
      : null;
  const cusChanged = program.cus_values.length > 1;

  // Find the school slug for the school link
  const schoolRecord = schools.find(
    (s) =>
      s.canonical_key === program.school ||
      s.historical_names.includes(program.school)
  );

  // Group roster by term
  const rosterByTerm: Record<number, RosterCourse[]> = {};
  if (enriched?.roster) {
    for (const course of enriched.roster) {
      if (!rosterByTerm[course.term]) rosterByTerm[course.term] = [];
      rosterByTerm[course.term].push(course);
    }
  }
  const terms = Object.keys(rosterByTerm)
    .map(Number)
    .sort((a, b) => a - b);

  return (
    <div
      className={`${hasRelevantResources ? "max-w-6xl" : "max-w-4xl"} mx-auto px-4 py-10`}
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
            <Link href="/programs" className="hover:text-blue-600">
              Degrees
            </Link>
            <span className="mx-2">›</span>
            <span className="text-slate-600">{code}</span>
          </nav>

          {/* Header */}
          <div className="mb-8">
            <p className="text-sm text-slate-500 mb-2">
              {code} · {isActive ? "Current" : "Retired"}{latestCus != null ? ` · ${latestCus} CUs` : ""}
            </p>
            <h1 className="text-3xl font-bold text-slate-800">{program.canonical_name}</h1>
            <div className="mt-1 flex flex-wrap items-center gap-x-2 gap-y-1">
              {schoolRecord ? (
                <Link
                  href={`/schools/${schoolRecord.slug}`}
                  className="text-blue-600 hover:underline text-sm"
                >
                  {program.school}
                </Link>
              ) : (
                <p className="text-slate-500 text-sm">{program.school}</p>
              )}
            </div>
            {!isActive && (
              <p className="text-sm text-slate-400 mt-1">
                Retired — last seen: {program.last_seen}
              </p>
            )}
          </div>

          {/* ============================================================
              ABOUT THIS DEGREE
              ============================================================ */}
          {enriched?.description && (
            <section className="mb-8">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-1 h-5 bg-blue-600 rounded" />
                <h2 className="text-lg font-bold text-slate-800">About This Degree</h2>
                <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
                  {enriched.description_source}
                </span>
              </div>
              <blockquote className="border-l-4 border-blue-100 pl-4 text-slate-700 text-sm leading-relaxed italic">
                {enriched.description}
              </blockquote>
              <p className="text-xs text-slate-400 mt-2">
                Official catalog text — WGU-authored.
              </p>
            </section>
          )}

          {/* ============================================================
              DEGREE HISTORY (compact — replaces Changes Over Time + Past Versions)
              ============================================================ */}
          <section className="mb-8">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-1 h-5 bg-slate-300 rounded" />
              <h2 className="text-base font-semibold text-slate-600">Degree History</h2>
            </div>
            <div className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600 bg-slate-50 border border-slate-200 rounded-lg px-4 py-3">
              <span>
                <span className="text-xs text-slate-400 mr-1">First offered</span>
                <span className="font-medium">{program.first_seen}</span>
              </span>
              <span>
                <span className="text-xs text-slate-400 mr-1">Status</span>
                <span className={`font-medium ${isActive ? "text-green-700" : "text-slate-500"}`}>
                  {isActive ? "Current" : "Retired"}
                </span>
              </span>
              {!isActive && (
                <span>
                  <span className="text-xs text-slate-400 mr-1">Last seen</span>
                  <span className="font-medium">{program.last_seen}</span>
                </span>
              )}
              {latestCus != null && (
                <span>
                  <span className="text-xs text-slate-400 mr-1">
                    {cusChanged ? "CUs (latest)" : "CUs"}
                  </span>
                  <span className="font-medium">{latestCus}</span>
                  {cusChanged && (
                    <span className="text-xs text-slate-400 ml-1">
                      (was {program.cus_values[0]})
                    </span>
                  )}
                </span>
              )}
            </div>
            {/* College name history — only show if there were actual name changes */}
            {program.colleges.length > 1 && (
              <div className="mt-3">
                <dt className="text-xs text-slate-400 mb-1.5">College name history</dt>
                <div className="flex flex-wrap items-center gap-1">
                  {program.colleges.map((college, i) => (
                    <span key={i} className="flex items-center gap-1">
                      <span
                        className={`text-xs px-2 py-0.5 rounded ${
                          i === program.colleges.length - 1
                            ? "bg-blue-50 text-blue-700"
                            : "bg-slate-100 text-slate-500"
                        }`}
                      >
                        {college}
                      </span>
                      {i < program.colleges.length - 1 && (
                        <span className="text-slate-300 text-xs">→</span>
                      )}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </section>

          {/* ============================================================
              LEARNING OUTCOMES (collapsible)
              ============================================================ */}
          {enriched?.outcomes && enriched.outcomes.length > 0 && (
            <section className="mb-8">
              <details className="group">
                <summary className="flex items-center gap-2 cursor-pointer list-none">
                  <div className="w-1 h-5 bg-blue-600 rounded shrink-0" />
                  <h2 className="text-lg font-bold text-slate-800">Learning Outcomes</h2>
                  <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
                    {enriched.outcomes_source}
                  </span>
                  <span className="text-xs text-slate-400 ml-auto group-open:hidden">
                    Show ▾
                  </span>
                  <span className="text-xs text-slate-400 ml-auto hidden group-open:inline">
                    Hide ▴
                  </span>
                </summary>
                <div className="mt-3 pl-3">
                  <p className="text-xs text-slate-400 mb-3">
                    Official WGU-authored outcomes from the catalog Program Outcomes section.
                  </p>
                  <ul className="space-y-2">
                    {enriched.outcomes.map((outcome, i) => (
                      <li key={i} className="flex gap-2 text-sm text-slate-700">
                        <span className="text-slate-300 mt-0.5 shrink-0">•</span>
                        <span>{outcome}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </details>
            </section>
          )}

          {/* ============================================================
              COURSE ROSTER
              ============================================================ */}
          {enriched?.roster && enriched.roster.length > 0 && (
            <section className="mb-8">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-1 h-5 bg-blue-600 rounded" />
                <h2 className="text-lg font-bold text-slate-800">
                  Course Roster ({enriched.roster.length} courses)
                </h2>
                <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
                  {enriched.roster_source}
                </span>
              </div>
              <div className="space-y-4">
                {terms.map((term) => (
                  <div key={term}>
                    <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">
                      Term {term}
                    </h3>
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
                          </tr>
                        </thead>
                        <tbody>
                          {rosterByTerm[term].map((course, i) => (
                            <tr
                              key={course.code}
                              className={`border-b border-slate-100 last:border-0 hover:bg-slate-50 ${
                                i % 2 === 0 ? "" : "bg-slate-50/30"
                              }`}
                            >
                              <td className="px-3 py-1.5">
                                <Link
                                  href={`/courses/${course.code}`}
                                  className="font-mono text-xs text-blue-700 hover:underline"
                                >
                                  {course.code}
                                </Link>
                              </td>
                              <td className="px-3 py-1.5 text-slate-700">
                                {course.title}
                              </td>
                              <td className="px-3 py-1.5 text-slate-500 text-xs text-right">
                                {course.cus}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ))}
              </div>
              <p className="text-xs text-slate-400 mt-3">
                Total: {enriched.roster.reduce((sum, c) => sum + c.cus, 0)} CUs across{" "}
                {enriched.roster.length} courses.
                {latestCus != null && ` Degree total per catalog: ${latestCus} CUs.`}
              </p>
            </section>
          )}

          {/* Back */}
          <div className="border-t border-slate-100 pt-6">
            <Link href="/programs" className="text-sm text-blue-600 hover:underline">
              ← Back to Degrees
            </Link>
          </div>
        </main>

        {hasRelevantResources && (
          <aside className="mt-8 self-start lg:sticky lg:top-24 lg:mt-0">
            <RelevantResources surface="program_detail" surfaceKey={program.program_code} />
          </aside>
        )}
      </div>
    </div>
  );
}
