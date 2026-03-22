import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import {
  getProgramDetail,
  getProgramEnrichedByCode,
  getOfficialResourcePlacementsForSurface,
  getSchools,
  getDegreeGuideByCode,
} from "@/lib/data";
import type { RosterCourse } from "@/lib/types";
import RelevantResources from "@/components/resources/RelevantResources";
import LearningOutcomes from "@/app/programs/[code]/LearningOutcomes";
import GuideProvenance from "@/components/programs/GuideProvenance";
import GuideCertBlock from "@/components/programs/GuideCertBlock";
import GuideFamilyPanel from "@/components/programs/GuideFamilyPanel";
import GuideAreasOfStudy from "@/components/programs/GuideAreasOfStudy";
import GuideCapstone from "@/components/programs/GuideCapstone";
import {
  DEGREE_COHORT_CODES,
  DEGREE_COHORT_META,
  type DegreeCohortCode,
} from "@/lib/degreePreviewData";

type Props = { params: Promise<{ code: string }> };

export function generateStaticParams() {
  return DEGREE_COHORT_CODES.map((code) => ({ code }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { code } = await params;
  const program = getProgramDetail(code);
  return {
    title: `${code} — Degree Preview (Prototype)`,
    description: `Prototype review page for ${program?.canonical_name ?? code}. Session 2 design cohort.`,
  };
}

export default async function DegreePreviewDetailPage({ params }: Props) {
  const { code } = await params;

  // Only serve cohort codes
  if (!DEGREE_COHORT_CODES.includes(code as DegreeCohortCode)) {
    notFound();
  }

  const program = getProgramDetail(code);
  if (!program) notFound();

  const enriched = getProgramEnrichedByCode(code);
  const guideArtifact = getDegreeGuideByCode(code);
  const schools = getSchools();
  const hasRelevantResources =
    getOfficialResourcePlacementsForSurface("program_detail", program.program_code).length > 0;

  const isActive = program.status === "ACTIVE";
  const latestCus =
    program.cus_values.length > 0
      ? program.cus_values[program.cus_values.length - 1]
      : null;
  const cusChanged = program.cus_values.length > 1;

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

  const cohortMeta = DEGREE_COHORT_META[code as DegreeCohortCode];

  return (
    <div
      className={`${hasRelevantResources ? "max-w-6xl" : "max-w-4xl"} mx-auto px-4 py-10`}
    >
      {/* Prototype breadcrumb */}
      <nav className="text-sm text-slate-400 mb-6 flex items-center gap-1.5">
        <Link href="/proto/degree-preview" className="hover:text-blue-600">
          Cohort Preview
        </Link>
        <span>›</span>
        <span className="text-slate-600">{code}</span>
        <span className="ml-2 bg-amber-100 text-amber-700 text-xs font-mono px-1.5 py-0.5 rounded">
          PROTOTYPE
        </span>
        <span className="ml-1 text-xs bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded">
          {cohortMeta.shape}
        </span>
      </nav>

      <div
        className={
          hasRelevantResources
            ? "lg:grid lg:grid-cols-[minmax(0,1fr)_19rem] lg:gap-10"
            : ""
        }
      >
        <main className={hasRelevantResources ? "min-w-0" : ""}>
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
            {guideArtifact && (
              <GuideProvenance
                provenance={guideArtifact.guide_provenance}
                quality={guideArtifact.quality}
                anomalyFlags={guideArtifact.anomaly_flags}
                suppressCaveatPill={hasCaveats}
              />
            )}
          </div>

          {/* Degraded quality warning */}
          {isDegraded && (
            <div className="mb-8 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3">
              <div className="flex items-start gap-2">
                <span className="shrink-0 text-amber-600 mt-0.5">⚠</span>
                <div className="space-y-1 text-sm">
                  {guideArtifact.guide_provenance.confidence === "low" && (
                    <p className="font-medium text-amber-800">
                      Guide data for this program has low confidence — information below reflects what could be extracted from the source guide.
                    </p>
                  )}
                  {guideArtifact.quality.caveat_messages_ui.map((msg, i) => (
                    <p key={i} className="text-amber-700">{msg}</p>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* About This Degree */}
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

          {/* Degree History */}
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

          {/* Program Learning Outcomes */}
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

          {/* Guide: Cert Signals */}
          {guideArtifact && guideArtifact.cert_signals.length > 0 && (
            <GuideCertBlock certSignals={guideArtifact.cert_signals} />
          )}

          {/* Guide: Family */}
          {guideArtifact && guideArtifact.family && (
            <GuideFamilyPanel
              family={guideArtifact.family}
              currentCode={code}
            />
          )}

          {/* Guide: Areas of Study (moved above Course Roster) */}
          {guideArtifact && guideArtifact.areas_of_study.length > 0 && (
            <GuideAreasOfStudy
              areasOfStudy={guideArtifact.areas_of_study}
              rosterCourses={rosterForAos}
            />
          )}

          {/* Course Roster (normal) */}
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
                            <th className="text-left px-3 py-2 text-xs font-medium text-slate-500">Code</th>
                            <th className="text-left px-3 py-2 text-xs font-medium text-slate-500">Title</th>
                            <th className="text-right px-3 py-2 text-xs font-medium text-slate-500">CUs</th>
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
                              <td className="px-3 py-1.5 text-slate-700">{course.title}</td>
                              <td className="px-3 py-1.5 text-slate-500 text-xs text-right">{course.cus}</td>
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

          {/* Course Roster (suppressed) */}
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

          {/* Guide: Capstone */}
          {guideArtifact && guideArtifact.capstone && (
            <GuideCapstone
              capstone={guideArtifact.capstone}
              suppressPartialNote={hasCaveats}
            />
          )}

          {/* Capstone discovery hint for AoS-only capstone programs */}
          {showCapstoneAosHint && (
            <p className="text-xs text-slate-400 mb-8">
              This program includes a capstone sequence — see the capstone group in Areas of Study above for details.
            </p>
          )}

          {/* Footer nav */}
          <div className="border-t border-slate-100 pt-6 flex items-center gap-6">
            <Link href="/proto/degree-preview" className="text-sm text-blue-600 hover:underline">
              ← Back to Cohort Index
            </Link>
            <Link
              href={`/programs/${code}`}
              className="text-sm text-slate-400 hover:text-slate-600 hover:underline"
            >
              View production page →
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
