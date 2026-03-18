import Link from "next/link";
import type { ComparePayload, CompareCourseEntry, TermLane } from "@/lib/compareUtils";
import { buildTermLanes, labShortLabel } from "@/lib/compareUtils";

// ---------------------------------------------------------------------------
// Main component — Proto3 Lane-Based Visual Compare
// ---------------------------------------------------------------------------
// Layout notes:
//   • Outer container has NO overflow-hidden so sticky lane headers work.
//   • Top section (identity bar + overlap strip) gets its own rounded-t-xl
//     overflow-hidden wrapper to clip backgrounds at the top corners.
//   • Lane headers use sticky top-14 (below the 56px nav).

export default function CompareView({ payload }: { payload: ComparePayload }) {
  const { left, right, metrics } = payload;
  const leftLabel = labShortLabel(left.program_code, left.canonical_name);
  const rightLabel = labShortLabel(right.program_code, right.canonical_name);
  const leftOnly = metrics.left_count - metrics.shared_count;
  const rightOnly = metrics.right_count - metrics.shared_count;
  const overlapPct = Math.round(metrics.jaccard_overlap * 100);
  const termLanes = buildTermLanes(payload);

  return (
    <div className="mt-2">
      {/* Outer: NO overflow-hidden so sticky lane headers work */}
      <div className="rounded-xl border border-slate-300">

        {/* ── Top section: rounded-t-xl overflow-hidden clips backgrounds ── */}
        <div className="rounded-t-xl overflow-hidden">
          {/* Identity bar */}
          <div className="grid grid-cols-[1fr_auto_1fr] items-stretch divide-x divide-slate-200">
            {/* Left program */}
            <div className="flex items-center gap-2 px-4 py-3 bg-blue-50/60">
              <span className="font-mono text-xs bg-blue-200 text-blue-800 px-1.5 py-0.5 rounded font-semibold shrink-0">
                {left.program_code}
              </span>
              <div className="min-w-0">
                <p
                  className="text-sm font-medium text-slate-800 leading-tight truncate"
                  title={left.canonical_name}
                >
                  <Link
                    href={`/programs/${left.program_code}`}
                    className="hover:underline"
                  >
                    {leftLabel}
                  </Link>
                </p>
                <p className="text-xs text-slate-400 mt-0.5">
                  {left.school} · {left.degree_level}
                  {left.total_cus != null ? ` · ${left.total_cus} CU` : ""}
                </p>
              </div>
            </div>

            {/* VS divider */}
            <div className="flex items-center px-4 bg-slate-50">
              <span className="text-xs font-semibold text-slate-400">vs</span>
            </div>

            {/* Right program */}
            <div className="flex items-center gap-2 px-4 py-3 bg-amber-50/60">
              <span className="font-mono text-xs bg-amber-200 text-amber-800 px-1.5 py-0.5 rounded font-semibold shrink-0">
                {right.program_code}
              </span>
              <div className="min-w-0">
                <p
                  className="text-sm font-medium text-slate-800 leading-tight truncate"
                  title={right.canonical_name}
                >
                  <Link
                    href={`/programs/${right.program_code}`}
                    className="hover:underline"
                  >
                    {rightLabel}
                  </Link>
                </p>
                <p className="text-xs text-slate-400 mt-0.5">
                  {right.school} · {right.degree_level}
                  {right.total_cus != null ? ` · ${right.total_cus} CU` : ""}
                </p>
              </div>
            </div>
          </div>

          {/* Overlap strip: 3 columns with counts above color segments */}
          <div className="border-t border-slate-200 grid grid-cols-[1fr_2fr_1fr]">
            {/* Left-only column (blue) */}
            <div className="px-3 pt-2 pb-0 bg-blue-50 border-r border-blue-100">
              <p className="text-xs font-bold text-blue-800">{leftOnly}</p>
              <p className="text-xs text-blue-600 leading-tight">
                unique to {leftLabel}
              </p>
              <div className="mt-2 h-2 bg-blue-400 rounded-bl-xl" />
            </div>
            {/* Shared column (green) */}
            <div className="px-3 pt-2 pb-0 bg-emerald-50 border-r border-emerald-100 text-center">
              <p className="text-xs font-bold text-emerald-800">{metrics.shared_count}</p>
              <p className="text-xs text-emerald-600 leading-tight">
                shared · {overlapPct}% overlap
              </p>
              <div className="mt-2 h-2 bg-emerald-400" />
            </div>
            {/* Right-only column (amber) */}
            <div className="px-3 pt-2 pb-0 bg-amber-50 text-right">
              <p className="text-xs font-bold text-amber-800">{rightOnly}</p>
              <p className="text-xs text-amber-600 leading-tight">
                unique to {rightLabel}
              </p>
              <div className="mt-2 h-2 bg-amber-400 rounded-br-xl" />
            </div>
          </div>
        </div>

        {/* ── Sticky lane column headers ── */}
        <div className="grid grid-cols-[1fr_2fr_1fr] sticky top-14 z-10">
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

        {/* ── Footer ── */}
        <p className="text-xs text-slate-400 px-4 py-3 border-t border-slate-200 bg-slate-50 rounded-b-xl">
          Comparison source: 2026-03 WGU catalog roster. Exact course code
          identity only — no alias or fuzzy matching. Atlas-derived analysis.
        </p>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Term block — one row in the lane layout
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
      {/* Term divider — dark, high-contrast */}
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
        {/* Left-only */}
        <div
          className={`px-3 py-2 border-r border-slate-200 ${
            hasLeft ? "bg-blue-50" : "bg-blue-50/20"
          }`}
        >
          {lane.leftOnly.map((c) => (
            <CourseCard key={c.code} course={c} accent="blue" />
          ))}
        </div>

        {/* Shared */}
        <div className="px-3 py-2 border-r border-slate-200 bg-slate-50">
          {lane.shared.map((c) => (
            <SharedCourseCard key={c.code} course={c} rightCode={rightCode} />
          ))}
        </div>

        {/* Right-only */}
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
