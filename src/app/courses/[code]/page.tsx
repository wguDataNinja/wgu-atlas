import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import {
  getCourseDetail,
  getAllCourseCodes,
  getHeadingToProgramCode,
  getPrograms,
  getCourseDescription,
} from "@/lib/data";

type Props = { params: Promise<{ code: string }> };

export async function generateStaticParams() {
  return getAllCourseCodes().map((code) => ({ code }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { code } = await params;
  const course = getCourseDetail(code);
  if (!course) return { title: "Course Not Found" };
  const statusLabel = course.active_current ? "" : " (Retired)";
  return {
    title: `${code}${statusLabel} — ${course.canonical_title_current}`,
    description: `${course.canonical_title_current} (${code}). ${course.active_current ? "Active" : "Retired"} WGU course — ${course.historical_program_count} degree appearances, first offered ${course.first_seen_edition}.`,
  };
}

export default async function CourseDetailPage({ params }: Props) {
  const { code } = await params;
  const course = getCourseDetail(code);
  if (!course) notFound();

  const headingToCode = getHeadingToProgramCode();
  const programs = getPrograms();

  // Build code → status map for splitting current vs retired appearances
  const codeToStatus: Record<string, "ACTIVE" | "RETIRED"> = {};
  for (const p of programs) {
    codeToStatus[p.program_code] = p.status;
  }

  const isCurrent = course.active_current;
  const isRichDetail = Array.isArray(course.programs_timeline);

  // Catalog description
  const catalogDesc = getCourseDescription(code);

  // Normalize current_programs to array
  const currentProgramNames: string[] =
    typeof course.current_programs === "string"
      ? (course.current_programs as string).split(";").map((s) => s.trim()).filter(Boolean)
      : (course.current_programs ?? []);

  // Normalize colleges_seen to array
  const collegesSeen: string[] = Array.isArray(course.colleges_seen)
    ? course.colleges_seen
    : course.colleges_seen
    ? [course.colleges_seen]
    : [];

  // Split programs_timeline into current and retired
  type TimelineEntry = { program: string; first_seen: string };
  let currentAppearances: TimelineEntry[] = [];
  const retiredAppearances: TimelineEntry[] = [];

  if (isRichDetail && course.programs_timeline) {
    for (const entry of course.programs_timeline) {
      const progCode = headingToCode[entry.program];
      const status = progCode ? codeToStatus[progCode] : undefined;
      if (status === "ACTIVE") {
        currentAppearances.push(entry);
      } else {
        retiredAppearances.push(entry);
      }
    }
  } else if (!isRichDetail && course.historical_programs) {
    // For retired/cert courses: parse historical_programs string and split by status
    const allNames = course.historical_programs
      .split(";")
      .map((s) => s.trim())
      .filter(Boolean);
    for (const name of allNames) {
      const progCode = headingToCode[name];
      const status = progCode ? codeToStatus[progCode] : undefined;
      const entry: TimelineEntry = { program: name, first_seen: "" };
      if (status === "ACTIVE") {
        currentAppearances.push(entry);
      } else {
        retiredAppearances.push(entry);
      }
    }
  }

  // For active courses, use current_programs for the current section (more authoritative)
  // and the timeline for retired
  if (isCurrent && currentProgramNames.length > 0) {
    currentAppearances = currentProgramNames.map((name) => ({ program: name, first_seen: "" }));
  }

  // Title variants
  const titleVariants = course.observed_titles.filter(
    (t) => t !== course.canonical_title_current
  );

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      {/* Breadcrumb */}
      <nav className="text-sm text-slate-400 mb-6">
        <Link href="/courses" className="hover:text-blue-600">Courses</Link>
        <span className="mx-2">›</span>
        <span className="text-slate-600">{code}</span>
      </nav>

      {/* ── Header ──────────────────────────────────────────────────────── */}
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
              Active
            </span>
          ) : (
            <span className="text-sm bg-slate-100 text-slate-500 px-2 py-1 rounded font-medium">
              Retired
            </span>
          )}
        </div>
        <h1 className="text-3xl font-bold text-slate-800">{course.canonical_title_current}</h1>
        {course.current_college && (
          <p className="text-slate-500 mt-1">{course.current_college}</p>
        )}
        {!isCurrent && course.last_seen_edition && (
          <p className="text-sm text-slate-400 mt-1">
            Last in catalog: {course.last_seen_edition}
          </p>
        )}
      </div>

      {/* ── About This Course ─────────────────────────────────────────────── */}
      {catalogDesc?.description && (
        <section className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-5 bg-blue-600 rounded" />
            <h2 className="text-lg font-bold text-slate-800">About This Course</h2>
            <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
              WGU Catalog 2026-03
            </span>
          </div>
          <blockquote className="border-l-4 border-blue-100 pl-4 text-slate-700 text-sm leading-relaxed">
            {catalogDesc.description}
          </blockquote>
          <p className="text-xs text-slate-400 mt-2">
            Official catalog text — WGU-authored.
          </p>
        </section>
      )}

      {/* ── Compact facts ─────────────────────────────────────────────────── */}
      <section className="mb-8">
        <div className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600 bg-slate-50 border border-slate-200 rounded-lg px-4 py-3">
          <span>
            <span className="text-xs text-slate-400 mr-1">First in catalog</span>
            <span className="font-medium">{course.first_seen_edition}</span>
          </span>
          <span>
            <span className="text-xs text-slate-400 mr-1">Status</span>
            <span className="font-medium">{isCurrent ? "Active" : "Retired"}</span>
          </span>
          {!isCurrent && course.last_seen_edition && (
            <span>
              <span className="text-xs text-slate-400 mr-1">Last seen</span>
              <span className="font-medium">{course.last_seen_edition}</span>
            </span>
          )}
          {isCurrent && (
            <span>
              <span className="text-xs text-slate-400 mr-1">Current degrees</span>
              <span className="font-medium">{course.current_program_count}</span>
            </span>
          )}
          <span>
            <span className="text-xs text-slate-400 mr-1">Total degree appearances</span>
            <span className="font-medium">{course.historical_program_count}</span>
          </span>
          {collegesSeen.length > 1 && (
            <span>
              <span className="text-xs text-slate-400 mr-1">Colleges (historical)</span>
              <span className="font-medium">{collegesSeen.length}</span>
            </span>
          )}
        </div>
      </section>

      {/* ── Included in Current Degrees ───────────────────────────────────── */}
      {currentAppearances.length > 0 && (
        <section className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-5 bg-blue-600 rounded" />
            <h2 className="text-base font-semibold text-slate-800">
              Included in Current Degrees ({currentAppearances.length})
            </h2>
          </div>
          <div className="border border-slate-200 rounded-lg overflow-hidden">
            <ul>
              {currentAppearances.map((entry, i) => {
                const progCode = headingToCode[entry.program];
                return (
                  <li
                    key={i}
                    className="border-b border-slate-100 last:border-0 px-4 py-2.5 text-sm"
                  >
                    {progCode ? (
                      <Link
                        href={`/programs/${progCode}`}
                        className="text-blue-700 hover:underline"
                      >
                        {entry.program}
                      </Link>
                    ) : (
                      <span className="text-slate-700">{entry.program}</span>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>
        </section>
      )}

      {/* ── Previously Appeared in Retired Degrees ────────────────────────── */}
      {retiredAppearances.length > 0 && (
        <section className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-5 bg-slate-300 rounded" />
            <h2 className="text-base font-semibold text-slate-500">
              Previously Appeared in Retired Degrees ({retiredAppearances.length})
            </h2>
          </div>
          <div className="border border-slate-200 rounded-lg overflow-hidden">
            <ul>
              {retiredAppearances.slice(0, 50).map((entry, i) => {
                const progCode = headingToCode[entry.program];
                return (
                  <li
                    key={i}
                    className="border-b border-slate-100 last:border-0 px-4 py-2 text-sm"
                  >
                    <span className="text-slate-400">
                      {progCode ? (
                        <Link
                          href={`/programs/${progCode}`}
                          className="hover:text-blue-600 hover:underline"
                        >
                          {entry.program}
                        </Link>
                      ) : (
                        entry.program
                      )}
                    </span>
                    {entry.first_seen && (
                      <span className="ml-2 text-xs text-slate-300 font-mono">
                        from {entry.first_seen}
                      </span>
                    )}
                  </li>
                );
              })}
            </ul>
            {retiredAppearances.length > 50 && (
              <div className="px-4 py-2 bg-slate-50 text-xs text-slate-400 border-t border-slate-200">
                Showing 50 of {retiredAppearances.length} — full history in the downloadable dataset.
              </div>
            )}
          </div>
        </section>
      )}

      {/* ── If no current appearances and course is active ─────────────────── */}
      {isCurrent && currentAppearances.length === 0 && (
        <section className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-5 bg-blue-600 rounded" />
            <h2 className="text-base font-semibold text-slate-800">Current Degrees</h2>
          </div>
          <p className="text-sm text-slate-400">No current degree appearances on record.</p>
        </section>
      )}

      {/* ── Also known as (title variants) ───────────────────────────────── */}
      {titleVariants.length > 0 && (
        <section className="mb-8">
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">
            Also known as in catalog
          </h3>
          <ul className="flex flex-col gap-1">
            {titleVariants.map((t, i) => (
              <li
                key={i}
                className="text-sm text-slate-500 font-mono bg-slate-50 border border-slate-200 rounded px-2 py-1"
              >
                {t}
              </li>
            ))}
          </ul>
          {course.title_variant_detail && (
            <p className="text-xs text-slate-400 mt-1">{course.title_variant_detail}</p>
          )}
        </section>
      )}

      {/* ── Notes ─────────────────────────────────────────────────────────── */}
      {(course.notes_confidence || course.notes) && (
        <div className="mb-8 bg-amber-50 border border-amber-200 rounded p-3 text-xs text-amber-800">
          <span className="font-semibold">Note: </span>
          {course.notes_confidence ?? course.notes}
        </div>
      )}

      {/* Back */}
      <div className="border-t border-slate-100 pt-6">
        <Link href="/courses" className="text-sm text-blue-600 hover:underline">
          ← Back to Courses
        </Link>
      </div>
    </div>
  );
}
