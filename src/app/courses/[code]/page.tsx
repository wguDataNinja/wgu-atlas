import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { getCourseDetail, getAllCourseCodes, getHeadingToProgramCode } from "@/lib/data";

type Props = { params: Promise<{ code: string }> };

export async function generateStaticParams() {
  return getAllCourseCodes().map((code) => ({ code }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { code } = await params;
  const course = getCourseDetail(code);
  if (!course) return { title: "Course Not Found" };
  const statusLabel = course.active_current ? "" : " (Deprecated)";
  return {
    title: `${code}${statusLabel} — ${course.canonical_title_current}`,
    description: `WGU catalog history for ${code}: ${course.canonical_title_current}. First seen ${course.first_seen_edition}, ${course.historical_program_count} historical programs.`,
  };
}

export default async function CourseDetailPage({ params }: Props) {
  const { code } = await params;
  const course = getCourseDetail(code);

  if (!course) notFound();

  const headingToCode = getHeadingToProgramCode();

  const titleVariants = course.observed_titles.filter(
    (t) => t !== course.canonical_title_current
  );

  // For deprecated courses without programs_timeline, parse historical_programs
  const historicalProgramList: string[] =
    course.historical_programs && !course.programs_timeline
      ? course.historical_programs
          .split(";")
          .map((s) => s.trim())
          .filter(Boolean)
      : [];

  const isCurrent = course.active_current;
  const isRichDetail = Array.isArray(course.programs_timeline);

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      {/* Breadcrumb */}
      <nav className="text-sm text-slate-400 mb-6">
        <Link href="/courses" className="hover:text-blue-600">Courses</Link>
        <span className="mx-2">›</span>
        <span className="text-slate-600">{code}</span>
      </nav>

      {/* Header */}
      <div className="mb-8">
        <div className="flex items-start flex-wrap gap-2 mb-2">
          <span className="font-mono text-sm bg-blue-100 text-blue-700 px-2 py-1 rounded font-semibold mt-0.5">
            {code}
          </span>
          {course.canonical_cus != null && (
            <span className="text-sm bg-indigo-50 text-indigo-700 border border-indigo-200 px-2 py-1 rounded font-semibold">
              {course.canonical_cus} CU{course.canonical_cus !== 1 ? "s" : ""}
            </span>
          )}
          {isCurrent ? (
            <span className="text-sm bg-green-50 text-green-700 border border-green-200 px-2 py-1 rounded font-medium">
              Current
            </span>
          ) : (
            <span className="text-sm bg-slate-100 text-slate-500 px-2 py-1 rounded font-medium">
              Deprecated
            </span>
          )}
          {course.ghost_flag && (
            <span className="text-sm bg-orange-50 text-orange-600 border border-orange-200 px-2 py-1 rounded">
              Ghost (≤2 appearances)
            </span>
          )}
        </div>
        <h1 className="text-3xl font-bold text-slate-800">{course.canonical_title_current}</h1>
        {course.current_college && (
          <p className="text-slate-500 mt-1">{course.current_college}</p>
        )}
        {!isCurrent && (
          <p className="text-sm text-slate-400 mt-1">
            Last seen: {course.last_seen_edition} · Final source: WGU Catalog ({course.last_seen_edition})
          </p>
        )}
      </div>

      {/* Official catalog history section */}
      <section className="mb-8">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 bg-blue-600 rounded" />
          <h2 className="text-lg font-bold text-slate-800">Official Catalog History</h2>
          <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
            Source: WGU public catalog archive
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          <StatCard label="First seen" value={course.first_seen_edition} />
          <StatCard label="Last seen" value={course.last_seen_edition} />
          <StatCard label="Catalog editions" value={String(course.edition_count)} />
          <StatCard
            label="Stability"
            value={STABILITY_LABELS[course.stability_class] ?? course.stability_class}
          />
          {course.canonical_cus != null && (
            <StatCard label="Credit units (CUs)" value={String(course.canonical_cus)} />
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
          <StatCard label="Current programs" value={String(course.current_program_count)} />
          <StatCard label="Historical programs" value={String(course.historical_program_count)} />
        </div>

        {/* Contexts */}
        <div className="mb-4">
          <dt className="text-xs text-slate-500 mb-1">Appears in</dt>
          <dd className="text-sm text-slate-700">{CONTEXT_LABELS[course.contexts_seen] ?? course.contexts_seen}</dd>
        </div>

        {/* Title history */}
        {titleVariants.length > 0 && (
          <div className="mb-4">
            <dt className="text-xs text-slate-500 mb-1">
              Observed title variants
              {course.title_variant_class !== "none" && (
                <span className="ml-2 bg-slate-100 text-slate-500 px-1.5 rounded">
                  {VARIANT_LABELS[course.title_variant_class] ?? course.title_variant_class}
                </span>
              )}
            </dt>
            <ul className="flex flex-col gap-1">
              {titleVariants.map((t, i) => (
                <li key={i} className="text-sm text-slate-600 font-mono bg-slate-50 border border-slate-200 rounded px-2 py-1">
                  {t}
                </li>
              ))}
            </ul>
            {course.title_variant_detail && (
              <p className="text-xs text-slate-400 mt-1">{course.title_variant_detail}</p>
            )}
          </div>
        )}

        {/* Current programs */}
        {course.current_programs && course.current_programs.length > 0 && (
          <div className="mb-4">
            <dt className="text-xs text-slate-500 mb-2">Current programs ({course.current_program_count})</dt>
            <ul className="flex flex-col gap-1">
              {(typeof course.current_programs === "string"
                ? (course.current_programs as string).split(";").map((s) => s.trim()).filter(Boolean)
                : course.current_programs
              ).map((p, i) => {
                const code = headingToCode[p];
                return (
                  <li key={i} className="text-sm text-slate-700 flex items-start gap-1">
                    <span className="text-slate-300 mt-0.5">·</span>
                    {code ? (
                      <Link href={`/programs/${code}`} className="hover:text-blue-600 hover:underline">{p}</Link>
                    ) : p}
                  </li>
                );
              })}
            </ul>
          </div>
        )}

        {/* Colleges seen */}
        {course.colleges_seen && (
          <div className="mb-4">
            <dt className="text-xs text-slate-500 mb-1">Schools / colleges seen</dt>
            <div className="flex flex-wrap gap-1">
              {(Array.isArray(course.colleges_seen)
                ? course.colleges_seen
                : [course.colleges_seen]
              ).map((c, i) => (
                <span key={i} className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded">
                  {c}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Notes / confidence */}
        {(course.notes_confidence || course.notes) && (
          <div className="mt-4 bg-amber-50 border border-amber-200 rounded p-3 text-xs text-amber-800">
            <span className="font-semibold">Note: </span>
            {course.notes_confidence ?? course.notes}
          </div>
        )}
      </section>

      {/* Program history — rich timeline (active AP) */}
      {isRichDetail && course.programs_timeline && course.programs_timeline.length > 0 && (
        <section className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-1 h-5 bg-blue-600 rounded" />
            <h2 className="text-lg font-bold text-slate-800">Program History</h2>
          </div>
          <p className="text-sm text-slate-500 mb-3">
            All programs in which this course has appeared ({course.programs_timeline.length} total).
          </p>
          <div className="border border-slate-200 rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="text-left px-4 py-2 text-xs font-medium text-slate-500">Program</th>
                  <th className="text-left px-4 py-2 text-xs font-medium text-slate-500 shrink-0">First seen</th>
                </tr>
              </thead>
              <tbody>
                {course.programs_timeline.slice(0, 50).map((entry, i) => {
                  const progCode = headingToCode[entry.program];
                  return (
                    <tr key={i} className="border-b border-slate-100 last:border-0 hover:bg-slate-50">
                      <td className="px-4 py-2 text-slate-700">
                        {progCode ? (
                          <Link href={`/programs/${progCode}`} className="hover:text-blue-600 hover:underline">
                            {entry.program}
                          </Link>
                        ) : entry.program}
                      </td>
                      <td className="px-4 py-2 text-slate-400 font-mono text-xs">{entry.first_seen}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            {course.programs_timeline.length > 50 && (
              <div className="px-4 py-2 bg-slate-50 text-xs text-slate-400 border-t border-slate-200">
                Showing 50 of {course.programs_timeline.length} — full history in the downloadable dataset.
              </div>
            )}
          </div>
        </section>
      )}

      {/* Program history — simple list (deprecated/cert) */}
      {!isRichDetail && historicalProgramList.length > 0 && (
        <section className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-1 h-5 bg-blue-600 rounded" />
            <h2 className="text-lg font-bold text-slate-800">Historical Programs</h2>
          </div>
          <p className="text-sm text-slate-500 mb-3">
            Programs in which this course appeared ({historicalProgramList.length} total).
          </p>
          <ul className="flex flex-col gap-1">
            {historicalProgramList.map((p, i) => {
              const progCode = headingToCode[p];
              return (
                <li key={i} className="text-sm text-slate-700 flex items-start gap-1">
                  <span className="text-slate-300 mt-0.5">·</span>
                  {progCode ? (
                    <Link href={`/programs/${progCode}`} className="hover:text-blue-600 hover:underline">{p}</Link>
                  ) : p}
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {/* Discussion placeholder */}
      <section className="mb-8">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 bg-slate-300 rounded" />
          <h2 className="text-lg font-bold text-slate-500">Discussion Signals</h2>
          <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
            Coming in v1.1
          </span>
        </div>
        <p className="text-sm text-slate-400 italic">
          Student discussion data from Reddit and other community spaces will appear here in a future release.
          Official catalog facts and discussion signals will always remain clearly separated.
        </p>
      </section>

      {/* Back */}
      <div className="border-t border-slate-100 pt-6">
        <Link href="/courses" className="text-sm text-blue-600 hover:underline">
          ← Back to Course Explorer
        </Link>
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

const STABILITY_LABELS: Record<string, string> = {
  perpetual: "Perpetual (all editions)",
  stable: "Stable",
  moderate: "Moderate",
  ephemeral: "Ephemeral",
  single: "Single appearance",
  cert_only: "Cert only",
};

const CONTEXT_LABELS: Record<string, string> = {
  AP: "Academic programs (AP)",
  cert: "Certificate programs",
  both: "Academic programs + certificates",
};

const VARIANT_LABELS: Record<string, string> = {
  none: "No variants",
  extraction_noise: "Extraction noise (not a real rename)",
  punctuation_only: "Punctuation only",
  wording_refinement: "Minor wording refinement",
  substantive_change: "Substantive title change",
  formatting_only: "Formatting only",
};
