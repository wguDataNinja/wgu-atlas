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
  if (!program) return { title: "Program Not Found" };
  const statusLabel = program.status === "ACTIVE" ? "" : " (Deprecated)";
  return {
    title: `${program.canonical_name}${statusLabel}`,
    description: `WGU program history for ${program.canonical_name}. First seen ${program.first_seen}, ${program.version_changes} version changes tracked.`,
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
  const versionSteps = parseVersionProgression(program.version_progression);
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
          Programs
        </Link>
        <span className="mx-2">›</span>
        <span className="text-slate-600">{code}</span>
      </nav>

      {/* Header */}
      <div className="mb-8">
        <div className="flex items-start flex-wrap gap-2 mb-2">
          <span className="font-mono text-sm bg-purple-100 text-purple-700 px-2 py-1 rounded font-semibold mt-0.5">
            {code}
          </span>
          {isActive ? (
            <span className="text-sm bg-green-50 text-green-700 border border-green-200 px-2 py-1 rounded font-medium">
              Current
            </span>
          ) : (
            <span className="text-sm bg-slate-100 text-slate-500 px-2 py-1 rounded font-medium">
              Deprecated
            </span>
          )}
          {latestCus != null && (
            <span className="text-sm bg-indigo-50 text-indigo-700 border border-indigo-200 px-2 py-1 rounded font-semibold">
              {latestCus} CUs{cusChanged ? " (changed)" : ""}
            </span>
          )}
        </div>
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
            Last seen: {program.last_seen} · Final source: WGU Catalog (
            {program.last_seen})
          </p>
        )}
      </div>

      {/* ================================================================
          PROGRAM DESCRIPTION (from catalog text)
          ================================================================ */}
      {enriched?.description && (
        <section className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-5 bg-blue-600 rounded" />
            <h2 className="text-lg font-bold text-slate-800">About This Program</h2>
            <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
              {enriched.description_source}
            </span>
          </div>
          <blockquote className="border-l-4 border-blue-100 pl-4 text-slate-700 text-sm leading-relaxed italic">
            {enriched.description}
          </blockquote>
          <p className="text-xs text-slate-400 mt-2">
            Official catalog text — WGU-authored. Sourced from {enriched.description_source}.
          </p>
        </section>
      )}

      {/* ================================================================
          OFFICIAL CATALOG HISTORY
          ================================================================ */}
      <section className="mb-8">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 bg-slate-300 rounded" />
          <h2 className="text-base font-semibold text-slate-700">Catalog History</h2>
          <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
            Source: WGU public catalog archive
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          <StatCard label="First seen" value={program.first_seen} />
          <StatCard label="Last seen" value={program.last_seen} />
          <StatCard label="Catalog editions" value={String(program.edition_count)} />
          <StatCard label="Version changes" value={String(program.version_changes)} />
          {latestCus != null && (
            <StatCard
              label={cusChanged ? "Total CUs (latest)" : "Total CUs"}
              value={String(latestCus)}
            />
          )}
        </div>

        {/* School lineage */}
        {program.colleges.length > 0 && (
          <div className="mb-5">
            <dt className="text-xs text-slate-500 mb-2">School lineage</dt>
            <div className="flex flex-wrap items-center gap-1">
              {program.colleges.map((college, i) => (
                <span key={i} className="flex items-center gap-1">
                  <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded">
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

        {/* Known names */}
        {program.degree_headings.length > 1 && (
          <div className="mb-5">
            <dt className="text-xs text-slate-500 mb-1">Known names</dt>
            <ul className="flex flex-col gap-1">
              {program.degree_headings.map((h, i) => (
                <li
                  key={i}
                  className={`text-sm ${
                    h === program.canonical_name
                      ? "font-medium text-slate-800"
                      : "text-slate-500"
                  }`}
                >
                  {h === program.canonical_name ? "· " : "  "}
                  {h}
                  {h === program.canonical_name && (
                    <span className="ml-2 text-xs text-slate-400">(canonical)</span>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>

      {/* ================================================================
          PROGRAM LEARNING OUTCOMES
          ================================================================ */}
      {enriched?.outcomes && enriched.outcomes.length > 0 && (
        <section className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-5 bg-blue-600 rounded" />
            <h2 className="text-lg font-bold text-slate-800">Program Learning Outcomes</h2>
            <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
              {enriched.outcomes_source}
            </span>
          </div>
          <p className="text-xs text-slate-400 mb-3">
            Official WGU-authored outcomes from the catalog Program Outcomes section.
            Present in ERA_B catalogs (2024-08+).
          </p>
          <ul className="space-y-2">
            {enriched.outcomes.map((outcome, i) => (
              <li key={i} className="flex gap-2 text-sm text-slate-700">
                <span className="text-slate-300 mt-0.5 shrink-0">•</span>
                <span>{outcome}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* ================================================================
          VERSION HISTORY
          ================================================================ */}
      {versionSteps.length > 0 && (
        <section className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-1 h-5 bg-blue-600 rounded" />
            <h2 className="text-lg font-bold text-slate-800">Version History</h2>
          </div>
          <p className="text-sm text-slate-500 mb-3">
            {program.version_changes === 0
              ? "No curriculum version changes observed across catalog editions."
              : `${program.version_changes} version change${
                  program.version_changes !== 1 ? "s" : ""
                } observed.`}
          </p>
          <div className="border border-slate-200 rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="text-left px-4 py-2 text-xs font-medium text-slate-500">
                    Catalog date
                  </th>
                  <th className="text-left px-4 py-2 text-xs font-medium text-slate-500">
                    Version stamp
                  </th>
                </tr>
              </thead>
              <tbody>
                {versionSteps.map((step, i) => (
                  <tr
                    key={i}
                    className="border-b border-slate-100 last:border-0 hover:bg-slate-50"
                  >
                    <td className="px-4 py-2 text-slate-700 font-mono text-xs">
                      {step.date}
                    </td>
                    <td className="px-4 py-2 text-slate-500 font-mono text-xs">
                      {step.version}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {cusChanged && (
            <p className="text-xs text-slate-400 mt-2">
              Total CUs changed across versions: {program.cus_values.join(" → ")}
            </p>
          )}
        </section>
      )}

      {/* ================================================================
          COURSE ROSTER
          ================================================================ */}
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
          <p className="text-xs text-slate-400 mb-3">
            Term sequence and course list from the 2026-03 catalog. Click any
            course code to view its full catalog history.
          </p>
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
            {latestCus != null &&
              ` Program total per catalog: ${latestCus} CUs.`}
          </p>
        </section>
      )}

      {/* Back */}
      <div className="border-t border-slate-100 pt-6">
        <Link href="/programs" className="text-sm text-blue-600 hover:underline">
          ← Back to Programs
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

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-slate-50 border border-slate-200 rounded px-3 py-2">
      <dt className="text-xs text-slate-400 mb-0.5">{label}</dt>
      <dd className="text-sm font-semibold text-slate-700">{value}</dd>
    </div>
  );
}

function parseVersionProgression(
  raw: string
): Array<{ date: string; version: string }> {
  if (!raw.trim()) return [];
  return raw.split("→").map((step) => {
    const trimmed = step.trim();
    const colonIdx = trimmed.indexOf(":");
    if (colonIdx === -1) return { date: trimmed, version: "" };
    return {
      date: trimmed.slice(0, colonIdx).trim(),
      version: trimmed.slice(colonIdx + 1).trim(),
    };
  });
}
