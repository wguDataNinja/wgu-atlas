import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import {
  getProgramDetail,
  getAllProgramCodes,
  getProgramEnrichedByCode,
  getOfficialResourcePlacementsForSurface,
  getSchools,
  getDegreeGuideByCode,
} from "@/lib/data";
import type { RosterCourse } from "@/lib/types";
import RelevantResources from "@/components/resources/RelevantResources";
import LearningOutcomes from "./LearningOutcomes";
import GuideProvenance from "@/components/programs/GuideProvenance";
import GuideCertBlock from "@/components/programs/GuideCertBlock";
import GuideFamilyPanel from "@/components/programs/GuideFamilyPanel";
import GuideAreasOfStudy from "@/components/programs/GuideAreasOfStudy";
import GuideCapstone from "@/components/programs/GuideCapstone";

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
  const guideArtifact = getDegreeGuideByCode(code);
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

  // Guide artifact SP display mode — drives roster presentation
  const spDisplayMode = guideArtifact?.standard_path?.sp_display_mode ?? null;
  const spSuppressed = spDisplayMode === "suppressed";
  const spAdvisorGuided = spDisplayMode === "advisor-guided";

  // Quality signals
  const hasCaveats = (guideArtifact?.quality?.caveat_messages_ui?.length ?? 0) > 0;
  const isDegraded =
    guideArtifact &&
    (guideArtifact.guide_provenance.confidence === "low" || hasCaveats);

  // Capstone discoverability — when capstone only appears inside an AoS group
  const hasCapstoneInAos =
    guideArtifact?.areas_of_study?.some((g) =>
      g.group.toLowerCase().includes("capstone")
    ) ?? false;
  const showCapstoneAosHint =
    hasCapstoneInAos &&
    (!guideArtifact?.capstone || !guideArtifact?.capstone?.present);

  // Roster entries for AoS course linking
  const rosterForAos =
    enriched?.roster?.map((c) => ({ code: c.code, title: c.title })) ?? [];

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
          <div className="mb-6">
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
              DEGREE HISTORY
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
              PROGRAM LEARNING OUTCOMES
              Falls back to a placeholder when outcomes are absent but the
              program has enriched data (i.e., the gap is likely a data
              omission, not a missing enrichment).
              ============================================================ */}
          {enriched && (
            enriched.outcomes && enriched.outcomes.length > 0 ? (
              <LearningOutcomes
                outcomes={enriched.outcomes}
                source={enriched.outcomes_source}
              />
            ) : (
              <section className="mb-8">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-1 h-5 bg-blue-600 rounded shrink-0" />
                  <h2 className="text-lg font-bold text-slate-800">Program Learning Outcomes</h2>
                </div>
                <p className="text-sm text-slate-400 italic pl-3">
                  Program learning outcomes are not available in the current catalog edition.
                </p>
              </section>
            )
          )}

          {/* ============================================================
              COURSE ROSTER (normal) — shown early so students see the
              actual course list without scrolling through curriculum detail.
              ============================================================ */}
          {enriched?.roster && enriched.roster.length > 0 && !spSuppressed && (
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
              {spAdvisorGuided && (
                <p className="text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded px-3 py-2 mb-3">
                  This program uses an advisor-guided course sequence. The order and pacing of courses may vary by student — the roster below reflects the current catalog course set, not a fixed sequence guaranteed for every student.
                </p>
              )}
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

          {/* ============================================================
              GUIDE: AREAS OF STUDY
              For suppressed-roster programs this section IS the primary
              course map. For normal programs it's curriculum detail below
              the roster.
              ============================================================ */}
          {guideArtifact && guideArtifact.areas_of_study.length > 0 && (
            <GuideAreasOfStudy
              areasOfStudy={guideArtifact.areas_of_study}
              rosterCourses={rosterForAos}
            />
          )}

          {/* ============================================================
              GUIDE: CERT SIGNALS
              ============================================================ */}
          {guideArtifact && guideArtifact.cert_signals.length > 0 && (
            <GuideCertBlock certSignals={guideArtifact.cert_signals} />
          )}

          {/* ============================================================
              GUIDE: FAMILY / RELATED PROGRAMS
              ============================================================ */}
          {guideArtifact && guideArtifact.family && (
            <GuideFamilyPanel
              family={guideArtifact.family}
              currentCode={code}
            />
          )}

          {/* ============================================================
              COURSE ROSTER — SUPPRESSED
              Shown when the guide has no usable term sequence. AoS above
              is the primary course map for these programs.
              ============================================================ */}
          {spSuppressed && enriched?.roster && enriched.roster.length > 0 && (
            <section className="mb-8">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-1 h-5 bg-slate-300 rounded" />
                <h2 className="text-lg font-bold text-slate-800">
                  Course Roster ({enriched.roster.length} courses)
                </h2>
                <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
                  {enriched.roster_source}
                </span>
              </div>
              <div className="bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-sm text-slate-600">
                This program does not use a fixed-term course sequence. The Areas of Study section above is the primary program map for this degree — expand each group to see courses, descriptions, and competencies.
              </div>
              <p className="text-xs text-slate-400 mt-3">
                Total: {enriched.roster.reduce((sum, c) => sum + c.cus, 0)} CUs across{" "}
                {enriched.roster.length} courses (see Areas of Study above for the complete program map).
                {latestCus != null && ` Degree total per catalog: ${latestCus} CUs.`}
              </p>
            </section>
          )}

          {/* ============================================================
              GUIDE: CAPSTONE
              suppressPartialNote when page-level caveat block already
              covers the partial-sequence warning.
              ============================================================ */}
          {guideArtifact && guideArtifact.capstone && (
            <GuideCapstone
              capstone={guideArtifact.capstone}
              suppressPartialNote={hasCaveats}
            />
          )}

          {/* ============================================================
              CAPSTONE DISCOVERY HINT
              For programs where capstone content is only accessible inside
              an AoS group (capstone.present = false but AoS has a capstone
              group). Lets students know to look in Areas of Study above.
              ============================================================ */}
          {showCapstoneAosHint && (
            <p className="text-xs text-slate-400 mb-8">
              This program includes a capstone sequence — see the capstone group in Areas of Study above for details.
            </p>
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
