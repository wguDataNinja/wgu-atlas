import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import {
  COHORT_CODES,
  getCohortEnrichment,
  type CoursePreviewEnrichment,
} from "@/lib/coursePreviewData";
import {
  getCourseDetail,
  getCourseDescription,
  getHeadingToProgramCode,
  getPrograms,
} from "@/lib/data";
import CourseEnrichmentPreview from "@/components/proto/CourseEnrichmentPreview";

type Props = { params: Promise<{ code: string }> };

export function generateStaticParams() {
  return COHORT_CODES.map((code) => ({ code }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { code } = await params;
  const course = getCourseDetail(code);
  return {
    title: `${code} — Enriched Preview (Prototype)`,
    description: `Prototype enriched page for ${course?.canonical_title_current ?? code}. Session 2 design cohort.`,
  };
}

export default async function CoursePreviewDetailPage({ params }: Props) {
  const { code } = await params;

  // Only serve cohort codes
  if (!COHORT_CODES.includes(code as (typeof COHORT_CODES)[number])) {
    notFound();
  }

  const enrichmentMap = getCohortEnrichment();
  const enrichment: CoursePreviewEnrichment = enrichmentMap[code];

  // Catalog data (reuse existing production data pipeline)
  const course = getCourseDetail(code);
  if (!course) notFound();

  const catalogDesc = getCourseDescription(code);
  const headingToCode = getHeadingToProgramCode();
  const programs = getPrograms();

  const codeToStatus: Record<string, "ACTIVE" | "RETIRED"> = {};
  for (const p of programs) {
    codeToStatus[p.program_code] = p.status;
  }

  // Build current and retired degree appearances
  type TimelineEntry = { program: string; first_seen: string };
  let currentAppearances: TimelineEntry[] = [];
  const retiredAppearances: TimelineEntry[] = [];
  const isRichDetail = Array.isArray(course.programs_timeline);

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
    const allNames = course.historical_programs
      .split(";")
      .map((s: string) => s.trim())
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

  const isCurrent = course.active_current;
  const currentProgramNames: string[] =
    typeof course.current_programs === "string"
      ? (course.current_programs as string).split(";").map((s: string) => s.trim()).filter(Boolean)
      : (course.current_programs ?? []);

  if (isCurrent && currentProgramNames.length > 0) {
    currentAppearances = currentProgramNames.map((name) => ({ program: name, first_seen: "" }));
  }

  const titleVariants = course.observed_titles.filter(
    (t: string) => t !== course.canonical_title_current
  );

  const collegesSeen: string[] = Array.isArray(course.colleges_seen)
    ? course.colleges_seen
    : course.colleges_seen
    ? [course.colleges_seen]
    : [];

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      {/* Breadcrumb */}
      <nav className="text-sm text-slate-400 mb-6 flex items-center gap-1.5">
        <Link href="/proto/course-preview" className="hover:text-blue-600">
          Cohort Preview
        </Link>
        <span>›</span>
        <span className="text-slate-600">{code}</span>
        <span className="ml-2 bg-amber-100 text-amber-700 text-xs font-mono px-1.5 py-0.5 rounded">
          PROTOTYPE
        </span>
      </nav>

      <CourseEnrichmentPreview
        enrichment={enrichment}
        course={course}
        catalogDesc={catalogDesc ?? null}
        currentAppearances={currentAppearances}
        retiredAppearances={retiredAppearances}
        isCurrent={isCurrent}
        titleVariants={titleVariants}
        collegesSeen={collegesSeen}
        headingToCode={headingToCode}
      />

      <div className="border-t border-slate-100 pt-6 flex items-center gap-6">
        <Link
          href="/proto/course-preview"
          className="text-sm text-blue-600 hover:underline"
        >
          ← Back to Cohort Index
        </Link>
        <Link
          href={`/courses/${code}`}
          className="text-sm text-slate-400 hover:text-slate-600 hover:underline"
        >
          View production page →
        </Link>
      </div>
    </div>
  );
}
