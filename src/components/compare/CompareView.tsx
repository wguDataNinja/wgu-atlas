import Link from "next/link";
import type { ComparePayload, CompareCourseEntry, TermLane } from "@/lib/compareUtils";
import { buildTermLanes, labShortLabel } from "@/lib/compareUtils";

// ---------------------------------------------------------------------------
// Main component — Lane-Based Visual Compare
// ---------------------------------------------------------------------------
// Layout:
//   • Outer container has NO overflow-hidden so sticky lane headers work.
//   • Sticky lane headers (top-14) are the primary structural anchor.
//   • Change / Reset live in a utility bar above the 3-column headers,
//     part of the same sticky container.

export default function CompareView({
  payload,
  onChangeSelection,
  onReset,
}: {
  payload: ComparePayload;
  onChangeSelection?: () => void;
  onReset?: () => void;
}) {
  const { left, right, metrics } = payload;
  const leftLabel = labShortLabel(left.program_code, left.canonical_name);
  const rightLabel = labShortLabel(right.program_code, right.canonical_name);
  const leftOnly = metrics.left_count - metrics.shared_count;
  const rightOnly = metrics.right_count - metrics.shared_count;
  const termLanes = buildTermLanes(payload);

  return (
    <div className="mt-4">
      {/* Outer: NO overflow-hidden so sticky lane headers work */}
      <div className="rounded-xl border border-slate-300">

        {/* ── Sticky header: utility bar + 3-column lane headers ── */}
        <div className="sticky top-14 z-10">
          {/* Utility bar: Change / Reset (top-right) */}
          <div className="flex justify-end gap-4 px-3 py-1.5 bg-slate-800 rounded-t-xl border-b border-slate-700">
            {onChangeSelection && (
              <button
                onClick={onChangeSelection}
                className="text-xs text-slate-300 hover:text-white transition-colors"
              >
                Change
              </button>
            )}
            {onReset && (
              <button
                onClick={onReset}
                className="text-xs text-slate-400 hover:text-slate-200 transition-colors"
              >
                Reset
              </button>
            )}
          </div>

          {/* 3-column lane headers */}
          <div className="grid grid-cols-[1fr_2fr_1fr]">
            <div className="bg-blue-600 px-3 py-2.5 text-center border-r border-blue-700">
              <p className="text-xs font-bold text-white leading-tight">{leftLabel}</p>
              <p className="text-xs text-blue-200 mt-0.5">
                {leftOnly} unique · {left.program_code}
              </p>
            </div>
            <div className="bg-slate-700 px-3 py-2.5 text-center border-r border-slate-600">
              <p className="text-xs font-bold text-white leading-tight">Shared</p>
              <p className="text-xs text-slate-300 mt-0.5">
                {metrics.shared_count} in both
              </p>
            </div>
            <div className="bg-amber-500 px-3 py-2.5 text-center">
              <p className="text-xs font-bold text-white leading-tight">{rightLabel}</p>
              <p className="text-xs text-amber-100 mt-0.5">
                {rightOnly} unique · {right.program_code}
              </p>
            </div>
          </div>
        </div>

        {/* ── Term blocks ── */}
        <div>
          {termLanes.map(([term, lane]) => (
            <TermBlock
              key={term}
              term={term}
              lane={lane}
              rightCode={right.program_code}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Term block
// ---------------------------------------------------------------------------

function TermBlock({
  term,
  lane,
  rightCode,
}: {
  term: number;
  lane: TermLane;
  rightCode: string;
}) {
  const hasLeft = lane.leftOnly.length > 0;
  const hasShared = lane.shared.length > 0;
  const hasRight = lane.rightOnly.length > 0;
  const allShared = !hasLeft && !hasRight && hasShared;

  return (
    <div className="border-t border-slate-200">
      {/* Term divider */}
      <div className="bg-slate-600 px-4 py-1.5 flex items-center gap-3">
        <span className="text-xs font-bold text-white tracking-wide">
          {term === 0 ? "UNPLACED" : `TERM ${term}`}
        </span>
        {allShared && (
          <span className="text-xs text-slate-300 font-normal">
            all shared this term
          </span>
        )}
      </div>

      {/* Three-lane content */}
      <div className="grid grid-cols-[1fr_2fr_1fr]">
        <div
          className={`px-3 py-2 border-r border-slate-200 ${
            hasLeft ? "bg-blue-50" : "bg-blue-50/20"
          }`}
        >
          {lane.leftOnly.map((c) => (
            <CourseCard key={c.code} course={c} accent="blue" />
          ))}
        </div>

        <div className="px-3 py-2 border-r border-slate-200 bg-slate-50">
          {lane.shared.map((c) => (
            <SharedCourseCard key={c.code} course={c} rightCode={rightCode} />
          ))}
        </div>

        <div
          className={`px-3 py-2 ${hasRight ? "bg-amber-50" : "bg-amber-50/20"}`}
        >
          {lane.rightOnly.map((c) => (
            <CourseCard key={c.code} course={c} accent="amber" />
          ))}
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Course cards
// ---------------------------------------------------------------------------

function CourseCard({
  course,
  accent,
}: {
  course: CompareCourseEntry;
  accent: "blue" | "amber";
}) {
  const borderColor = accent === "blue" ? "border-blue-400" : "border-amber-400";
  const codeColor =
    accent === "blue"
      ? "text-blue-800 bg-blue-200 hover:underline"
      : "text-amber-800 bg-amber-200 hover:underline";

  return (
    <div
      className={`flex items-start gap-1.5 py-1.5 pl-2 border-l-2 ${borderColor} mb-1 last:mb-0`}
    >
      <Link
        href={`/courses/${course.code}`}
        className={`font-mono text-xs px-1 py-0.5 rounded shrink-0 ${codeColor}`}
      >
        {course.code}
      </Link>
      <div className="flex-1 min-w-0">
        <p className="text-xs text-slate-700 leading-snug">{course.title}</p>
      </div>
      <span className="text-xs text-slate-500 shrink-0 tabular-nums ml-1">
        {course.cus}
      </span>
    </div>
  );
}

function SharedCourseCard({
  course,
  rightCode,
}: {
  course: CompareCourseEntry;
  rightCode: string;
}) {
  const hasDrift =
    course.term_left != null &&
    course.term_right != null &&
    course.term_left !== course.term_right;

  return (
    <div className="flex items-start gap-1.5 py-1.5 pl-2 border-l-2 border-emerald-400 mb-1 last:mb-0">
      <Link
        href={`/courses/${course.code}`}
        className="font-mono text-xs text-emerald-800 bg-emerald-100 px-1 py-0.5 rounded shrink-0 hover:underline"
      >
        {course.code}
      </Link>
      <div className="flex-1 min-w-0">
        <p className="text-xs text-slate-700 leading-snug">{course.title}</p>
        {hasDrift && (
          <p className="text-xs text-amber-600 font-medium mt-0.5">
            ↕ term {course.term_right} in {rightCode}
          </p>
        )}
      </div>
      <span className="text-xs text-slate-500 shrink-0 tabular-nums ml-1">
        {course.cus}
      </span>
    </div>
  );
}
