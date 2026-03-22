/**
 * CourseEnrichmentPreview.tsx
 *
 * Session 2 prototype component. Renders a best-guess enriched course page
 * for design cohort review. Not a production component.
 *
 * Section order (per Session 2 brief):
 *  1. Header
 *  2. Compact facts bar
 *  3. High-signal blocks near top: Capstone callout, Cert prep, Requires (prereq)
 *  4. Guide-derived overview (descriptions)
 *  5. Competencies (with variant treatment)
 *  6. Variant / context note (if multi-variant)
 *  7. Prerequisite-for block (reverse prereqs)
 *  8. Catalog description (existing WGU text)
 *  9. Degree appearance / history
 * 10. Also Known As / Notes
 */

"use client";

import Link from "next/link";
import type { CoursePreviewEnrichment, EnrichmentDescription, CompetencySet } from "@/lib/coursePreviewData";
import type { CourseDetail, CourseDescription } from "@/lib/types";

type TimelineEntry = { program: string; first_seen: string };

type Props = {
  enrichment: CoursePreviewEnrichment;
  course: CourseDetail;
  catalogDesc: CourseDescription | null;
  currentAppearances: TimelineEntry[];
  retiredAppearances: TimelineEntry[];
  isCurrent: boolean;
  titleVariants: string[];
  collegesSeen: string[];
  headingToCode: Record<string, string>;
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function SectionHeader({
  title,
  accentColor = "bg-blue-600",
  badge,
}: {
  title: string;
  accentColor?: string;
  badge?: string;
}) {
  return (
    <div className="flex items-center gap-2 mb-3">
      <div className={`w-1 h-5 ${accentColor} rounded`} />
      <h2 className="text-lg font-bold text-slate-800">{title}</h2>
      {badge && (
        <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">{badge}</span>
      )}
    </div>
  );
}

function SubSectionHeader({ title }: { title: string }) {
  return (
    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">{title}</h3>
  );
}

/** Format a list of program codes as a short readable string */
function programLabel(codes: string[]): string {
  if (codes.length === 0) return "";
  if (codes.length <= 3) return codes.join(", ");
  return `${codes.slice(0, 3).join(", ")} +${codes.length - 3} more`;
}

/** Detect if two description texts are cosmetically similar (>90% character overlap heuristic) */
function areDescriptionsCosmetic(a: string, b: string): boolean {
  const shorter = a.length < b.length ? a : b;
  const longer = a.length < b.length ? b : a;
  if (shorter.length === 0) return false;
  // Simple: if the shorter is almost entirely contained in the longer
  const overlap = shorter.split(" ").filter((w) => longer.includes(w)).length;
  const ratio = overlap / shorter.split(" ").length;
  return ratio > 0.85;
}

// ---------------------------------------------------------------------------
// Section: Capstone callout
// ---------------------------------------------------------------------------

function CapstoneCallout({
  signal,
  title,
}: {
  signal: "explicit" | "title-only";
  title: string;
}) {
  return (
    <section className="mb-6">
      <div className="bg-indigo-50 border border-indigo-200 rounded-lg px-4 py-3">
        <div className="flex items-start gap-2">
          <span className="text-indigo-600 font-bold text-sm mt-0.5">⬛</span>
          <div>
            <div className="font-semibold text-indigo-800 text-sm">Capstone Course</div>
            {signal === "explicit" ? (
              <p className="text-sm text-indigo-700 mt-0.5">
                This is a program capstone. Students integrate and synthesize competencies from
                across the degree program.
              </p>
            ) : (
              <p className="text-sm text-indigo-700 mt-0.5">
                Title suggests a capstone course (&ldquo;{title}&rdquo;), but no guide-derived
                capstone context was found.{" "}
                <span className="text-xs text-indigo-500 font-mono">[title-only inference]</span>
              </p>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Section: Certification prep
// ---------------------------------------------------------------------------

function CertPrepBlock({ cert }: { cert: NonNullable<CoursePreviewEnrichment["cert"]> }) {
  return (
    <section className="mb-6">
      <div className="bg-emerald-50 border border-emerald-200 rounded-lg px-4 py-3">
        <div className="flex items-start gap-2">
          <span className="text-emerald-600 font-bold text-sm mt-0.5">✓</span>
          <div>
            <div className="font-semibold text-emerald-800 text-sm">
              Certification Preparation — {cert.normalized_cert}
            </div>
            <p className="text-sm text-emerald-700 mt-0.5">
              This course includes preparation for the{" "}
              <strong>{cert.normalized_cert}</strong> certification exam.
            </p>
            <p className="text-xs text-emerald-600 mt-1">
              Confirmed across {cert.source_programs.length} degree program
              {cert.source_programs.length !== 1 ? "s" : ""} · Source:{" "}
              {programLabel(cert.source_programs)}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Section: Requires (prereq)
// ---------------------------------------------------------------------------

function RequiresBlock({ prereq }: { prereq: NonNullable<CoursePreviewEnrichment["prereq"]> }) {
  const isCumulative = prereq.prereq_type === "cumulative-sequence-prereq";

  if (isCumulative) {
    return (
      <section className="mb-6">
        <div className="bg-amber-50 border border-amber-200 rounded-lg px-4 py-3">
          <div className="flex items-start gap-2">
            <span className="text-amber-600 font-bold text-sm mt-0.5">→</span>
            <div>
              <div className="font-semibold text-amber-800 text-sm">
                Prerequisite Sequence Required
              </div>
              <p className="text-sm text-amber-700 mt-0.5">
                {prereq.notes ?? prereq.prereq_value}
              </p>
              <p className="text-xs text-amber-600 mt-1">
                This prerequisite is a cumulative sequence — it cannot be resolved to a single
                course code.{" "}
                <span className="font-mono text-amber-500">[cumulative-sequence — review-required]</span>
              </p>
              <p className="text-xs text-amber-600 mt-1">
                Raw value from guide:{" "}
                <span className="font-mono bg-amber-100 px-1 rounded">{prereq.prereq_value}</span>
              </p>
            </div>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="mb-6">
      <div className="border border-slate-200 rounded-lg px-4 py-3 bg-slate-50">
        <div className="flex items-start gap-2">
          <span className="text-slate-500 font-bold text-sm mt-0.5">→</span>
          <div>
            <div className="font-semibold text-slate-700 text-sm">Requires</div>
            <div className="mt-1">
              {prereq.normalized_prereq_code ? (
                <Link
                  href={`/courses/${prereq.normalized_prereq_code}`}
                  className="text-blue-700 hover:underline font-medium text-sm"
                >
                  {prereq.normalized_prereq_title ?? prereq.prereq_value}
                </Link>
              ) : (
                <span className="text-slate-700 text-sm font-medium">
                  {prereq.normalized_prereq_title ?? prereq.prereq_value}
                </span>
              )}{" "}
              {prereq.normalized_prereq_code && (
                <span className="text-slate-400 font-mono text-xs">
                  ({prereq.normalized_prereq_code})
                </span>
              )}
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Confirmed across {prereq.source_programs.length} program
              {prereq.source_programs.length !== 1 ? "s" : ""} ·{" "}
              {programLabel(prereq.source_programs)}
              {prereq.review_status !== "auto-accepted" && (
                <span className="ml-1 font-mono text-amber-500">[review-required]</span>
              )}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Section: Guide-derived overview
// ---------------------------------------------------------------------------

function GuideOverviewBlock({ descriptions }: { descriptions: EnrichmentDescription[] }) {
  if (descriptions.length === 0) return null;

  // Check if all descriptions are cosmetically similar
  const isSingleEffective =
    descriptions.length === 1 ||
    (descriptions.length === 2 &&
      areDescriptionsCosmetic(descriptions[0].text, descriptions[1].text));

  if (isSingleEffective) {
    return (
      <section className="mb-8">
        <SectionHeader
          title="Course Overview"
          badge="guide-derived"
        />
        <blockquote className="border-l-4 border-blue-200 pl-4 text-slate-700 text-sm leading-relaxed">
          {descriptions[0].text}
        </blockquote>
        <div className="mt-2 flex items-center gap-2">
          <p className="text-xs text-slate-400">
            Source:{" "}
            {programLabel(descriptions[0].source_program_codes)}
          </p>
          {descriptions.length === 2 && (
            <span className="text-xs text-slate-300 font-mono">
              [2 variants — collapsed as cosmetically identical]
            </span>
          )}
        </div>
      </section>
    );
  }

  // Multi-variant: show each with source attribution
  return (
    <section className="mb-8">
      <SectionHeader
        title="Course Overview"
        badge={`${descriptions.length} variants — guide-derived`}
      />
      <div className="space-y-4">
        {descriptions.map((desc, i) => (
          <div key={i} className="border border-blue-100 rounded-lg overflow-hidden">
            <div className="bg-blue-50 px-3 py-1.5 flex items-center gap-2">
              <span className="text-xs font-semibold text-blue-700">
                Variant {i + 1} of {descriptions.length}
              </span>
              <span className="text-xs text-blue-500">
                Programs: {programLabel(desc.source_program_codes)}
              </span>
            </div>
            <blockquote className="px-4 py-3 text-slate-700 text-sm leading-relaxed">
              {desc.text}
            </blockquote>
          </div>
        ))}
      </div>
      <p className="text-xs text-slate-400 mt-2">
        Multiple guide descriptions found. Over-showing all variants for design review.
        Collapse/merge policy not yet resolved.
      </p>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Section: Competencies
// ---------------------------------------------------------------------------

function CompetenciesBlock({ competency_sets }: { competency_sets: CompetencySet[] }) {
  if (competency_sets.length === 0) return null;

  const hasVariance = competency_sets.length > 1;

  // Check if all sets have identical bullets
  const firstBullets = JSON.stringify(competency_sets[0].bullets);
  const allIdentical = competency_sets.every(
    (s) => JSON.stringify(s.bullets) === firstBullets
  );

  if (!hasVariance || allIdentical) {
    return (
      <section className="mb-8">
        <SectionHeader
          title="What You'll Learn"
          badge={allIdentical && hasVariance ? `${competency_sets.length} sets — identical` : "guide-derived"}
        />
        <ul className="space-y-2">
          {competency_sets[0].bullets.map((bullet, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-slate-700">
              <span className="text-blue-400 mt-1 shrink-0">▸</span>
              <span>{bullet}</span>
            </li>
          ))}
        </ul>
        {allIdentical && hasVariance && (
          <p className="text-xs text-slate-400 mt-2">
            Consistent across {competency_sets.length} program contexts ·{" "}
            {programLabel([
              ...new Set(competency_sets.flatMap((s) => s.source_program_codes)),
            ])}
          </p>
        )}
        {!hasVariance && (
          <p className="text-xs text-slate-400 mt-2">
            Source: {programLabel(competency_sets[0].source_program_codes)}
          </p>
        )}
      </section>
    );
  }

  // Multi-variant competencies — show all with program attribution
  return (
    <section className="mb-8">
      <SectionHeader
        title="What You'll Learn"
        badge={`${competency_sets.length} competency variants — guide-derived`}
      />
      <div className="space-y-5">
        {competency_sets.map((cset, i) => (
          <div key={i} className="border border-slate-200 rounded-lg overflow-hidden">
            <div className="bg-slate-50 px-3 py-1.5 flex items-center gap-2 border-b border-slate-200">
              <span className="text-xs font-semibold text-slate-600">
                Variant {i + 1} of {competency_sets.length}
              </span>
              <span className="text-xs text-slate-400">
                Programs: {programLabel(cset.source_program_codes)}
              </span>
            </div>
            <ul className="px-4 py-3 space-y-2">
              {cset.bullets.map((bullet, j) => (
                <li key={j} className="flex items-start gap-2 text-sm text-slate-700">
                  <span className="text-blue-400 mt-1 shrink-0">▸</span>
                  <span>{bullet}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <p className="text-xs text-slate-400 mt-2">
        Multiple competency sets found. Over-showing all variants for design review.
        Program-specific collapse policy not yet resolved.
      </p>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Section: Variant / context note
// ---------------------------------------------------------------------------

function VariantContextNote({
  descriptions,
  competency_sets,
  shape,
}: {
  descriptions: EnrichmentDescription[];
  competency_sets: CompetencySet[];
  shape: string;
}) {
  const hasDescVariance = descriptions.length > 1;
  const hasCompVariance = competency_sets.length > 1;

  if (!hasDescVariance && !hasCompVariance) return null;

  // Only show when something meaningful is being flagged
  const allPrograms = new Set<string>([
    ...descriptions.flatMap((d) => d.source_program_codes),
    ...competency_sets.flatMap((c) => c.source_program_codes),
  ]);

  return (
    <section className="mb-8">
      <SubSectionHeader title="Program Context Notes" />
      <div className="bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-xs text-slate-600 space-y-1.5">
        <div>
          <span className="font-semibold">Shape:</span>{" "}
          <span className="font-mono text-slate-500">{shape}</span>
        </div>
        {hasDescVariance && (
          <div>
            <span className="font-semibold">Description variants:</span> {descriptions.length} —
            may reflect different program-specific framings of the same course material.
          </div>
        )}
        {hasCompVariance && (
          <div>
            <span className="font-semibold">Competency variants:</span> {competency_sets.length} —
            may reflect different emphasis or bullet-set versions across programs.
          </div>
        )}
        <div>
          <span className="font-semibold">Total programs covered:</span>{" "}
          {allPrograms.size} unique program contexts in guide data.
        </div>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Section: Prerequisite-for (reverse prereqs)
// ---------------------------------------------------------------------------

function PrerequisiteForBlock({
  reverse_prereqs,
}: {
  reverse_prereqs: CoursePreviewEnrichment["reverse_prereqs"];
}) {
  if (reverse_prereqs.length === 0) return null;

  return (
    <section className="mb-8">
      <SectionHeader title="Prerequisite For" accentColor="bg-violet-400" />
      <p className="text-xs text-slate-400 mb-3">
        Completing this course satisfies the prerequisite requirement for the following:
      </p>
      <div className="border border-slate-200 rounded-lg overflow-hidden">
        <ul>
          {reverse_prereqs.map((entry, i) => (
            <li
              key={i}
              className="border-b border-slate-100 last:border-0 px-4 py-2.5 text-sm flex items-start justify-between gap-4"
            >
              <div>
                <Link
                  href={`/courses/${entry.target_code}`}
                  className="text-blue-700 hover:underline font-medium"
                >
                  {entry.target_title}
                </Link>{" "}
                <span className="font-mono text-slate-400 text-xs">({entry.target_code})</span>
              </div>
              <span className="text-xs text-slate-400 shrink-0">
                {programLabel(entry.source_programs)}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Section: Catalog description (existing WGU text)
// ---------------------------------------------------------------------------

function CatalogDescriptionBlock({
  catalogDesc,
}: {
  catalogDesc: Props["catalogDesc"];
}) {
  if (!catalogDesc?.description) return null;

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1 h-5 bg-slate-300 rounded" />
        <h2 className="text-base font-semibold text-slate-600">About This Course</h2>
        <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
          WGU Catalog 2026-03
        </span>
      </div>
      <blockquote className="border-l-4 border-slate-100 pl-4 text-slate-600 text-sm leading-relaxed">
        {catalogDesc.description}
      </blockquote>
      <p className="text-xs text-slate-400 mt-2">Official catalog text — WGU-authored.</p>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Section: Degree appearances
// ---------------------------------------------------------------------------

function DegreeAppearancesBlock({
  currentAppearances,
  retiredAppearances,
  isCurrent,
  headingToCode,
}: {
  currentAppearances: TimelineEntry[];
  retiredAppearances: TimelineEntry[];
  isCurrent: boolean;
  headingToCode: Record<string, string>;
}) {
  return (
    <>
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

      {isCurrent && currentAppearances.length === 0 && (
        <section className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-1 h-5 bg-blue-600 rounded" />
            <h2 className="text-base font-semibold text-slate-800">Current Degrees</h2>
          </div>
          <p className="text-sm text-slate-400">No current degree appearances on record.</p>
        </section>
      )}

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
    </>
  );
}

// ---------------------------------------------------------------------------
// Main export
// ---------------------------------------------------------------------------

export default function CourseEnrichmentPreview({
  enrichment,
  course,
  catalogDesc,
  currentAppearances,
  retiredAppearances,
  isCurrent,
  titleVariants,
  collegesSeen,
  headingToCode,
}: Props) {
  const { cert, prereq, reverse_prereqs, descriptions, competency_sets, capstoneSignal, shape } =
    enrichment;

  const hasAnyEnrichment =
    descriptions.length > 0 || competency_sets.length > 0 || cert || prereq || reverse_prereqs.length > 0;

  return (
    <>
      {/* ── Header ──────────────────────────────────────────────────────── */}
      <div className="mb-6">
        <div className="flex items-start flex-wrap gap-2 mb-2">
          <span className="font-mono text-sm bg-blue-100 text-blue-700 px-2 py-1 rounded font-semibold">
            {course.course_code ?? enrichment.courseCode}
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
          <span className="text-xs bg-amber-100 text-amber-700 px-2 py-1 rounded font-mono">
            {shape}
          </span>
        </div>
        <h1 className="text-3xl font-bold text-slate-800">{course.canonical_title_current}</h1>
        {course.current_college && (
          <p className="text-slate-500 mt-1">{course.current_college}</p>
        )}
      </div>

      {/* ── Compact facts bar ─────────────────────────────────────────────── */}
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
          <span>
            <span className="text-xs text-slate-400 mr-1">Guide enrichment</span>
            <span className="font-medium">
              {descriptions.length}d / {competency_sets.length}c
            </span>
          </span>
        </div>
      </section>

      {/* ── HIGH SIGNAL near top ─────────────────────────────────────────── */}

      {capstoneSignal && (
        <CapstoneCallout
          signal={capstoneSignal}
          title={course.canonical_title_current}
        />
      )}

      {cert && <CertPrepBlock cert={cert} />}

      {prereq && <RequiresBlock prereq={prereq} />}

      {/* ── No-enrichment fallback notice (sparse courses) ───────────────── */}
      {!hasAnyEnrichment && (
        <div className="mb-8 bg-slate-50 border border-slate-200 rounded-lg px-4 py-4 text-sm text-slate-500">
          <div className="font-semibold text-slate-600 mb-1">No guide enrichment found</div>
          <p>
            This course has no guide-derived description or competency data. The page falls back
            to catalog facts and degree history only.
          </p>
          <p className="text-xs text-slate-400 mt-1 font-mono">[sparse fallback layout]</p>
        </div>
      )}

      {/* ── Guide-derived overview ───────────────────────────────────────── */}
      {descriptions.length > 0 && (
        <GuideOverviewBlock descriptions={descriptions} />
      )}

      {/* ── Competencies ────────────────────────────────────────────────── */}
      {competency_sets.length > 0 && (
        <CompetenciesBlock competency_sets={competency_sets} />
      )}

      {/* ── Variant / context note ──────────────────────────────────────── */}
      <VariantContextNote
        descriptions={descriptions}
        competency_sets={competency_sets}
        shape={shape}
      />

      {/* ── Prerequisite-for (reverse prereqs) ─────────────────────────── */}
      {reverse_prereqs.length > 0 && (
        <PrerequisiteForBlock reverse_prereqs={reverse_prereqs} />
      )}

      {/* ── Catalog description ─────────────────────────────────────────── */}
      <CatalogDescriptionBlock catalogDesc={catalogDesc} />

      {/* ── Degree appearances ──────────────────────────────────────────── */}
      <DegreeAppearancesBlock
        currentAppearances={currentAppearances}
        retiredAppearances={retiredAppearances}
        isCurrent={isCurrent}
        headingToCode={headingToCode}
      />

      {/* ── Also Known As ───────────────────────────────────────────────── */}
      {titleVariants.length > 0 && (
        <section className="mb-8">
          <SubSectionHeader title="Also known as in catalog" />
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

      {/* ── Notes ───────────────────────────────────────────────────────── */}
      {(course.notes_confidence || course.notes) && (
        <div className="mb-8 bg-amber-50 border border-amber-200 rounded p-3 text-xs text-amber-800">
          <span className="font-semibold">Note: </span>
          {course.notes_confidence ?? course.notes}
        </div>
      )}
    </>
  );
}
