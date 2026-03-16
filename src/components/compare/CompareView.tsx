import Link from "next/link";
import type { ComparePayload, CompareProgramMeta, CompareCourseEntry } from "@/lib/families";
import { extractTrackLabel } from "@/lib/families";
import type { CompareResult } from "@/lib/programs";
import type { ProgramRecord } from "@/lib/types";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type TermLane = {
  shared: CompareCourseEntry[];
  leftOnly: CompareCourseEntry[];
  rightOnly: CompareCourseEntry[];
};

// ---------------------------------------------------------------------------
// Term-lane builder
// ---------------------------------------------------------------------------

/**
 * Groups courses by term into three lanes: shared / left-only / right-only.
 * Shared courses are bucketed by term_left (their left-program term).
 * Right-only courses are bucketed by term_right.
 * Returns sorted list of [termNumber, TermLane] pairs.
 */
function buildTermLanes(payload: ComparePayload): [number, TermLane][] {
  const map = new Map<number, TermLane>();
  const ensure = (t: number): TermLane => {
    if (!map.has(t)) map.set(t, { shared: [], leftOnly: [], rightOnly: [] });
    return map.get(t)!;
  };
  for (const c of payload.shared_courses) {
    ensure(c.term_left ?? 0).shared.push(c);
  }
  for (const c of payload.left_only_courses) {
    ensure(c.term_left ?? 0).leftOnly.push(c);
  }
  for (const c of payload.right_only_courses) {
    ensure(c.term_right ?? 0).rightOnly.push(c);
  }
  return [...map.entries()].sort(([a], [b]) => a - b);
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export default function CompareView({
  payload,
}: {
  payload: ComparePayload;
  leftProgram: ProgramRecord;
  rightProgram: ProgramRecord;
}) {
  const { left, right, metrics } = payload;
  const jaccard = Math.round(metrics.jaccard_overlap * 100);
  const leftOnlyCount = metrics.left_count - metrics.shared_count;
  const rightOnlyCount = metrics.right_count - metrics.shared_count;
  const termLanes = buildTermLanes(payload);

  // Track labels for column headers (short form from index name)
  const leftTrackLabel = extractTrackLabel(left.index_name) ?? left.program_code;
  const rightTrackLabel = extractTrackLabel(right.index_name) ?? right.program_code;

  return (
    <div className="mt-2">
      {/* ── Program headers ────────────────────────────────────────────── */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <ProgramHeader meta={left} side="left" />
        <ProgramHeader meta={right} side="right" />
      </div>

      {/* ── Overlap summary ────────────────────────────────────────────── */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 mb-6">
        <h2 className="text-sm font-semibold text-slate-700 mb-3">Overlap Summary</h2>
        <div className="flex flex-wrap gap-4 mb-4 text-sm">
          <LegendChip color="emerald" label={`${metrics.shared_count} shared`} />
          <LegendChip
            color="blue"
            label={`${leftOnlyCount} only in ${leftTrackLabel}`}
          />
          <LegendChip
            color="amber"
            label={`${rightOnlyCount} only in ${rightTrackLabel}`}
          />
          <span className="text-slate-500 text-xs self-center">
            Jaccard overlap: <strong className="text-slate-700">{jaccard}%</strong>
          </span>
        </div>
        <OverlapBar metrics={metrics} />
        <p className="text-xs text-slate-400 mt-2">
          Overlap bar: shared (green) / {leftTrackLabel}-only (blue) /{" "}
          {rightTrackLabel}-only (amber). Jaccard = shared ÷ union.
        </p>
      </div>

      {/* ── Three-lane track timeline ───────────────────────────────────── */}
      <div className="mb-6">
        {/* Column headers */}
        <div className="grid grid-cols-[1fr_2fr_1fr] gap-3 mb-2 px-1">
          <TrackHeader
            code={left.program_code}
            label={leftTrackLabel}
            count={leftOnlyCount}
            side="left"
          />
          <TrackHeader
            code={null}
            label="Shared Courses"
            count={metrics.shared_count}
            side="shared"
          />
          <TrackHeader
            code={right.program_code}
            label={rightTrackLabel}
            count={rightOnlyCount}
            side="right"
          />
        </div>

        {/* Term blocks */}
        <div className="space-y-0 border border-slate-200 rounded-xl overflow-hidden divide-y divide-slate-100">
          {termLanes.map(([term, lane]) => (
            <TermBlock
              key={term}
              term={term}
              lane={lane}
              rightCode={right.program_code}
            />
          ))}
        </div>

        <p className="text-xs text-slate-400 mt-3 px-1">
          Courses are organized by term. Shared courses appear in the center column.
          Track-specific courses appear in the left or right column.{" "}
          {left.index_name
            ? `${leftTrackLabel} = ${left.program_code} · ${rightTrackLabel} = ${right.program_code}.`
            : ""}
        </p>
      </div>

      <p className="text-xs text-slate-400 border-t border-slate-100 pt-4 mt-2">
        Comparison source: 2026-03 WGU catalog roster. Exact course code identity
        only — no alias or fuzzy matching. Atlas-derived analysis.
      </p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Program header card
// ---------------------------------------------------------------------------

function ProgramHeader({
  meta,
  side,
}: {
  meta: CompareProgramMeta;
  side: "left" | "right";
}) {
  const isLeft = side === "left";
  // Use index_name as primary display if available, canonical_name as subtitle
  const primaryName = meta.index_name ?? meta.canonical_name;
  const showSubtitle = meta.index_name !== null;

  return (
    <div
      className={`border rounded-xl p-4 ${
        isLeft
          ? "border-blue-200 bg-blue-50/30"
          : "border-amber-200 bg-amber-50/30"
      }`}
    >
      <div className="flex items-center gap-2 mb-2 flex-wrap">
        <span className="font-mono text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded font-semibold">
          {meta.program_code}
        </span>
        <span
          className={`text-xs px-2 py-0.5 rounded font-medium ${
            isLeft
              ? "bg-blue-100 text-blue-700"
              : "bg-amber-100 text-amber-700"
          }`}
        >
          {isLeft ? "Track A" : "Track B"}
        </span>
      </div>
      <h3 className="text-sm font-semibold text-slate-800 leading-snug mb-1">
        <Link href={`/programs/${meta.program_code}`} className="hover:underline">
          {primaryName}
        </Link>
      </h3>
      {showSubtitle && (
        <p className="text-xs text-slate-500 mb-2 leading-snug">{meta.canonical_name}</p>
      )}
      <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs mt-2">
        <MetaRow label="School" value={meta.school} />
        <MetaRow label="Level" value={meta.degree_level} />
        {meta.total_cus != null && (
          <MetaRow label="Total CUs" value={`${meta.total_cus} CUs`} />
        )}
        <MetaRow label="Since" value={meta.first_seen} />
        <MetaRow label="Courses" value={`${meta.course_count}`} />
      </dl>
    </div>
  );
}

function MetaRow({ label, value }: { label: string; value: string }) {
  return (
    <>
      <dt className="text-slate-400">{label}</dt>
      <dd className="text-slate-700 font-medium truncate">{value}</dd>
    </>
  );
}

// ---------------------------------------------------------------------------
// Three-lane column header
// ---------------------------------------------------------------------------

function TrackHeader({
  code,
  label,
  count,
  side,
}: {
  code: string | null;
  label: string;
  count: number;
  side: "left" | "right" | "shared";
}) {
  const colorClass = {
    left: "bg-blue-50 border-blue-200 text-blue-800",
    shared: "bg-emerald-50 border-emerald-200 text-emerald-800",
    right: "bg-amber-50 border-amber-200 text-amber-800",
  }[side];

  const align = side === "right" ? "text-right" : side === "left" ? "text-left" : "text-center";

  return (
    <div className={`border rounded-lg px-3 py-2 ${colorClass} ${align}`}>
      <p className="text-xs font-semibold leading-tight">{label}</p>
      <p className="text-xs opacity-70 mt-0.5">
        {count} course{count !== 1 ? "s" : ""}
        {code ? ` · ${code}` : ""}
      </p>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Term block — one row of the timeline
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

  return (
    <div className="grid grid-cols-[1fr_2fr_1fr]">
      {/* Term label spans all three columns as a sub-header */}
      <div className="col-span-3 bg-slate-50 px-4 py-1.5 border-b border-slate-100 flex items-center gap-2">
        <span className="text-xs font-medium text-slate-500">
          {term === 0 ? "Unplaced" : `Term ${term}`}
        </span>
        {!hasLeft && !hasRight && hasShared && (
          <span className="text-xs text-slate-300 italic">all shared</span>
        )}
      </div>

      {/* Left-only column */}
      <div className={`px-3 py-2 border-r border-slate-100 ${hasLeft ? "" : "bg-slate-50/40"}`}>
        {lane.leftOnly.map((c) => (
          <CourseRow key={c.code} course={c} termKey="left" />
        ))}
      </div>

      {/* Shared column */}
      <div className="px-3 py-2 border-r border-slate-100">
        {lane.shared.map((c) => (
          <CourseRow
            key={c.code}
            course={c}
            termKey="shared"
            rightCode={rightCode}
          />
        ))}
      </div>

      {/* Right-only column */}
      <div className={`px-3 py-2 ${hasRight ? "" : "bg-slate-50/40"}`}>
        {lane.rightOnly.map((c) => (
          <CourseRow key={c.code} course={c} termKey="right" />
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Course row — compact course entry within a lane
// ---------------------------------------------------------------------------

function CourseRow({
  course,
  termKey,
  rightCode,
}: {
  course: CompareCourseEntry;
  termKey: "left" | "right" | "shared";
  rightCode?: string;
}) {
  const hasDrift =
    termKey === "shared" &&
    course.term_left != null &&
    course.term_right != null &&
    course.term_left !== course.term_right;

  return (
    <div className="flex items-start gap-1.5 py-1 min-w-0">
      <Link
        href={`/courses/${course.code}`}
        className="font-mono text-xs text-blue-700 hover:underline shrink-0 mt-0.5"
      >
        {course.code}
      </Link>
      <div className="flex-1 min-w-0">
        <span className="text-xs text-slate-700 leading-snug">{course.title}</span>
        {hasDrift && rightCode && (
          <span className="block text-xs text-amber-600 italic">
            term {course.term_right} in {rightCode}
          </span>
        )}
      </div>
      <span className="text-xs text-slate-400 shrink-0 tabular-nums ml-1">
        {course.cus}
      </span>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Overlap bar
// ---------------------------------------------------------------------------

function OverlapBar({ metrics }: { metrics: CompareResult }) {
  const union = metrics.left_count + metrics.right_count - metrics.shared_count;
  const sharedPct = union > 0 ? (metrics.shared_count / union) * 100 : 0;
  const leftOnlyPct =
    union > 0 ? ((metrics.left_count - metrics.shared_count) / union) * 100 : 0;
  const rightOnlyPct =
    union > 0 ? ((metrics.right_count - metrics.shared_count) / union) * 100 : 0;

  return (
    <div className="h-3 rounded-full overflow-hidden flex bg-slate-100">
      <div
        style={{ width: `${sharedPct}%` }}
        className="bg-emerald-400 transition-all"
        title={`Shared: ${Math.round(sharedPct)}%`}
      />
      <div
        style={{ width: `${leftOnlyPct}%` }}
        className="bg-blue-400 transition-all"
        title={`Left-only: ${Math.round(leftOnlyPct)}%`}
      />
      <div
        style={{ width: `${rightOnlyPct}%` }}
        className="bg-amber-400 transition-all"
        title={`Right-only: ${Math.round(rightOnlyPct)}%`}
      />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Legend chip
// ---------------------------------------------------------------------------

function LegendChip({
  color,
  label,
}: {
  color: "emerald" | "blue" | "amber";
  label: string;
}) {
  const dotClass = {
    emerald: "bg-emerald-400",
    blue: "bg-blue-400",
    amber: "bg-amber-400",
  }[color];

  return (
    <span className="flex items-center gap-1.5 text-xs text-slate-700">
      <span className={`inline-block w-3 h-3 rounded-sm ${dotClass}`} />
      <strong>{label}</strong>
    </span>
  );
}
