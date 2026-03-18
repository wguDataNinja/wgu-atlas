"use client";

// ---------------------------------------------------------------------------
// Compare Degrees — Prototype Lab
// Three stacked layout prototypes for the compare experience.
// All three render the same selected pair simultaneously.
//
// Proto 1 — Compact Roster-First
//   Sticky compact identity bar + overlap summary → roster starts immediately.
//   3-lane layout, stronger tinting, sticky lane headers.
//
// Proto 2 — Differences First
//   Same bar → unique courses foregrounded → shared curriculum collapsed.
//   Challenger layout: "what's actually different" leads the page.
//
// Proto 3 — Lane-Based Visual Compare
//   Bolder visual language: solid lane fills, high-contrast term dividers,
//   course cards with colored accents. Tests whether stronger visual system
//   improves scannability on long rosters.
// ---------------------------------------------------------------------------

import { useState, useMemo } from "react";
import Link from "next/link";
import type { ProgramRecord, ProgramEnriched } from "@/lib/types";
import { classifyDegreeLevel, DEGREE_LEVEL_ORDER } from "@/lib/programs";
import {
  buildLabPayload,
  labShortLabel,
  labDisplayLabel,
  buildTermLanes,
} from "./compareProtoUtils";
import type { ComparePayload, CompareCourseEntry, TermLane, CompareResult } from "./compareProtoUtils";

// ---------------------------------------------------------------------------
// Preset pairs — representative stress cases for the prototype lab
// ---------------------------------------------------------------------------

const PRESET_PAIRS: {
  label: string;
  sub: string;
  left: string;
  right: string;
}[] = [
  {
    label: "S.E. Java vs C#",
    sub: "Tech · Bachelor's · 80% Jaccard · Identical canonical names",
    left: "BSSWE",
    right: "BSSWE_C",
  },
  {
    label: "Cloud Net. Eng.: Base vs AWS",
    sub: "Tech · Bachelor's · 82% · Vendor track choice",
    left: "BSCNE",
    right: "BSCNEAWS",
  },
  {
    label: "Accounting vs Finance",
    sub: "Business · Bachelor's · 54% · Distinct degrees",
    left: "BSACC",
    right: "BSFIN",
  },
  {
    label: "MAT Sci: Biology vs Chemistry",
    sub: "Education · Master's · 90% · Subject substitution",
    left: "MATSESB",
    right: "MATSESC",
  },
  {
    label: "MBA vs MBA-ITM",
    sub: "Business · Master's · High overlap · Near-zero diff",
    left: "MBA",
    right: "MBAITM",
  },
  {
    label: "Data Analytics vs Cybersecurity",
    sub: "Tech · Bachelor's · Low overlap · Stress test",
    left: "BSDA",
    right: "BSCSIA",
  },
  {
    label: "SWE: AI Eng vs DevOps",
    sub: "Tech · Master's · 54% · Specialization pair",
    left: "MSSWEAIE",
    right: "MSSWEDOE",
  },
];

// ---------------------------------------------------------------------------
// Main export — orchestrates selector + 3 stacked prototypes
// ---------------------------------------------------------------------------

export default function ComparePrototypeLab({
  programs,
  enriched,
}: {
  programs: ProgramRecord[];
  enriched: Record<string, ProgramEnriched>;
}) {
  // Build a lookup for quick code → record access
  const programMap = useMemo(
    () => new Map(programs.map((p) => [p.program_code, p])),
    [programs]
  );

  // Find the first valid preset (both codes present in lab universe)
  const defaultPreset = useMemo(() => {
    return PRESET_PAIRS.find(
      (pp) => programMap.has(pp.left) && programMap.has(pp.right) && enriched[pp.left] && enriched[pp.right]
    ) ?? null;
  }, [programMap, enriched]);

  const [selectedLeft, setSelectedLeft] = useState<string>(defaultPreset?.left ?? "");
  const [selectedRight, setSelectedRight] = useState<string>(defaultPreset?.right ?? "");

  // Which preset button is active (for highlight)
  const activePresetIdx = useMemo(() => {
    return PRESET_PAIRS.findIndex((pp) => pp.left === selectedLeft && pp.right === selectedRight);
  }, [selectedLeft, selectedRight]);

  // Build the compare payload
  const payload = useMemo<ComparePayload | null>(() => {
    if (!selectedLeft || !selectedRight) return null;
    const lp = programMap.get(selectedLeft);
    const rp = programMap.get(selectedRight);
    const le = enriched[selectedLeft];
    const re = enriched[selectedRight];
    if (!lp || !rp || !le || !re) return null;
    return buildLabPayload(lp, rp, le, re);
  }, [selectedLeft, selectedRight, programMap, enriched]);

  const handlePreset = (pp: (typeof PRESET_PAIRS)[0]) => {
    setSelectedLeft(pp.left);
    setSelectedRight(pp.right);
  };

  return (
    <div>
      {/* ── Lab pair selector ─────────────────────────────────────── */}
      <LabSelector
        programs={programs}
        enriched={enriched}
        selectedLeft={selectedLeft}
        selectedRight={selectedRight}
        activePresetIdx={activePresetIdx}
        onPreset={handlePreset}
        onSetLeft={setSelectedLeft}
        onSetRight={setSelectedRight}
      />

      {/* ── No pair selected ──────────────────────────────────────── */}
      {!payload && (
        <div className="border border-dashed border-slate-200 rounded-xl p-12 text-center text-slate-400">
          Select a comparison pair above to see all three prototypes.
        </div>
      )}

      {/* ── Stacked prototypes ────────────────────────────────────── */}
      {payload && (
        <div className="space-y-12">
          {/* ── Proto 1 ─────────────────────────────────────────── */}
          <section>
            <ProtoSectionHeader
              n={1}
              label="Compact Roster-First"
              desc="Sticky identity bar + overlap summary → roster immediately. 3-lane layout with stronger tinting."
            />
            <Proto1CompactRosterFirst payload={payload} />
          </section>

          {/* ── Proto 2 ─────────────────────────────────────────── */}
          <section>
            <ProtoSectionHeader
              n={2}
              label="Differences First"
              desc="Unique courses foregrounded. Shared curriculum collapsed by default. Challenger layout."
            />
            <Proto2DifferencesFirst payload={payload} />
          </section>

          {/* ── Proto 3 ─────────────────────────────────────────── */}
          <section>
            <ProtoSectionHeader
              n={3}
              label="Lane-Based Visual Compare"
              desc="Bold lane fills, high-contrast term dividers. Tests whether stronger visual system improves scannability."
            />
            <Proto3LaneVisual payload={payload} />
          </section>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Lab pair selector
// ---------------------------------------------------------------------------

function LabSelector({
  programs,
  enriched,
  selectedLeft,
  selectedRight,
  activePresetIdx,
  onPreset,
  onSetLeft,
  onSetRight,
}: {
  programs: ProgramRecord[];
  enriched: Record<string, ProgramEnriched>;
  selectedLeft: string;
  selectedRight: string;
  activePresetIdx: number;
  onPreset: (pp: (typeof PRESET_PAIRS)[0]) => void;
  onSetLeft: (code: string) => void;
  onSetRight: (code: string) => void;
}) {
  const [schoolFilter, setSchoolFilter] = useState("");
  const [levelFilter, setLevelFilter] = useState("");
  const [showFreeform, setShowFreeform] = useState(false);

  const programMap = useMemo(
    () => new Map(programs.map((p) => [p.program_code, p])),
    [programs]
  );

  const schools = useMemo(
    () => [...new Set(programs.map((p) => p.school))].sort(),
    [programs]
  );

  const availableLevels = useMemo(() => {
    const base = schoolFilter ? programs.filter((p) => p.school === schoolFilter) : programs;
    const levels = new Set(base.map((p) => classifyDegreeLevel(p)));
    return DEGREE_LEVEL_ORDER.filter((l) => levels.has(l));
  }, [programs, schoolFilter]);

  const filteredForA = useMemo(() => {
    return programs.filter((p) => {
      if (schoolFilter && p.school !== schoolFilter) return false;
      if (levelFilter && classifyDegreeLevel(p) !== levelFilter) return false;
      return true;
    });
  }, [programs, schoolFilter, levelFilter]);

  const siblingsForB = useMemo(() => {
    if (!selectedLeft) return [];
    const left = programMap.get(selectedLeft);
    if (!left) return [];
    const leftSchool = left.school;
    const leftLevel = classifyDegreeLevel(left);
    return programs.filter(
      (p) =>
        p.program_code !== selectedLeft &&
        p.school === leftSchool &&
        classifyDegreeLevel(p) === leftLevel &&
        enriched[p.program_code]
    );
  }, [selectedLeft, programs, programMap, enriched]);

  const selectedLeftName = programMap.get(selectedLeft)?.canonical_name ?? "";
  const selectedRightName = programMap.get(selectedRight)?.canonical_name ?? "";

  return (
    <div className="mb-8 border border-slate-200 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="bg-slate-50 border-b border-slate-200 px-4 py-3 flex items-center justify-between">
        <span className="text-sm font-semibold text-slate-700">Select a compare pair</span>
        <button
          onClick={() => setShowFreeform(!showFreeform)}
          className="text-xs text-blue-600 hover:text-blue-800 underline"
        >
          {showFreeform ? "Hide freeform selector" : "Freeform selector"}
        </button>
      </div>

      {/* Preset buttons */}
      <div className="px-4 py-3 flex flex-wrap gap-2 bg-white border-b border-slate-100">
        {PRESET_PAIRS.map((pp, i) => {
          const valid =
            programMap.has(pp.left) &&
            programMap.has(pp.right) &&
            !!enriched[pp.left] &&
            !!enriched[pp.right];
          return (
            <button
              key={i}
              onClick={() => valid && onPreset(pp)}
              disabled={!valid}
              title={valid ? pp.sub : `${pp.left} or ${pp.right} not in lab universe`}
              className={`px-3 py-1.5 rounded-lg border text-xs font-medium transition-colors ${
                i === activePresetIdx
                  ? "bg-blue-600 text-white border-blue-600"
                  : valid
                  ? "bg-white text-slate-700 border-slate-300 hover:border-blue-400 hover:text-blue-700"
                  : "bg-slate-50 text-slate-300 border-slate-200 cursor-not-allowed"
              }`}
            >
              {pp.label}
            </button>
          );
        })}
      </div>

      {/* Current selection summary */}
      {selectedLeft && selectedRight && (
        <div className="px-4 py-2 bg-blue-50/50 border-b border-blue-100 flex items-center gap-3 flex-wrap">
          <span className="text-xs text-slate-500">Comparing:</span>
          <span className="font-mono text-xs bg-blue-100 text-blue-800 px-1.5 py-0.5 rounded">
            {selectedLeft}
          </span>
          <span className="text-xs text-slate-600 max-w-xs truncate">{selectedLeftName}</span>
          <span className="text-slate-400 text-xs">vs</span>
          <span className="font-mono text-xs bg-amber-100 text-amber-800 px-1.5 py-0.5 rounded">
            {selectedRight}
          </span>
          <span className="text-xs text-slate-600 max-w-xs truncate">{selectedRightName}</span>
        </div>
      )}

      {/* Freeform selector (collapsible) */}
      {showFreeform && (
        <div className="px-4 py-4 bg-white">
          <div className="flex flex-wrap gap-3 mb-3">
            <select
              value={schoolFilter}
              onChange={(e) => { setSchoolFilter(e.target.value); setLevelFilter(""); }}
              className="border border-slate-300 rounded px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="">All schools</option>
              {schools.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
            <select
              value={levelFilter}
              onChange={(e) => setLevelFilter(e.target.value)}
              className="border border-slate-300 rounded px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="">All levels</option>
              {availableLevels.map((l) => <option key={l} value={l}>{l}</option>)}
            </select>
          </div>
          <div className="grid sm:grid-cols-2 gap-3">
            <div>
              <p className="text-xs font-medium text-slate-500 mb-1">
                Program A ({filteredForA.length} options)
              </p>
              <select
                value={selectedLeft}
                onChange={(e) => onSetLeft(e.target.value)}
                className="w-full border border-slate-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500"
                size={6}
              >
                {filteredForA.map((p) => (
                  <option key={p.program_code} value={p.program_code}>
                    [{p.program_code}] {p.canonical_name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <p className="text-xs font-medium text-slate-500 mb-1">
                Program B — same school + level as A ({siblingsForB.length} options)
              </p>
              <select
                value={selectedRight}
                onChange={(e) => onSetRight(e.target.value)}
                className="w-full border border-slate-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500"
                size={6}
                disabled={!selectedLeft}
              >
                {siblingsForB.map((p) => (
                  <option key={p.program_code} value={p.program_code}>
                    [{p.program_code}] {p.canonical_name}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-2">
            Program B list auto-filters to same school + degree level as A.{" "}
            {programs.length} programs in lab universe.
          </p>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Prototype section header
// ---------------------------------------------------------------------------

function ProtoSectionHeader({
  n,
  label,
  desc,
}: {
  n: number;
  label: string;
  desc: string;
}) {
  return (
    <div className="flex items-start gap-3 mb-4 pb-3 border-b border-slate-200">
      <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-slate-700 text-white text-sm font-bold shrink-0 mt-0.5">
        {n}
      </span>
      <div>
        <h2 className="text-base font-semibold text-slate-800">{label}</h2>
        <p className="text-xs text-slate-400 mt-0.5">{desc}</p>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Shared: Compact Identity Bar (used by all 3 prototypes)
// ---------------------------------------------------------------------------

function CompactIdentityBar({
  payload,
  sticky,
}: {
  payload: ComparePayload;
  sticky?: boolean;
}) {
  const { left, right, metrics } = payload;
  const jaccard = Math.round(metrics.jaccard_overlap * 100);
  const leftLabel = labShortLabel(left.program_code, left.canonical_name);
  const rightLabel = labShortLabel(right.program_code, right.canonical_name);
  const leftOnly = metrics.left_count - metrics.shared_count;
  const rightOnly = metrics.right_count - metrics.shared_count;

  return (
    <div
      className={`bg-white border border-slate-200 rounded-xl overflow-hidden ${
        sticky ? "sticky top-14 z-20 shadow-sm" : ""
      }`}
    >
      {/* Top row: program identities */}
      <div className="grid grid-cols-[1fr_auto_1fr] items-stretch divide-x divide-slate-100">
        {/* Left program */}
        <div className="flex items-center gap-2 px-4 py-2.5 bg-blue-50/40">
          <span className="font-mono text-xs bg-blue-200 text-blue-800 px-1.5 py-0.5 rounded font-semibold shrink-0">
            {left.program_code}
          </span>
          <div className="min-w-0">
            <p className="text-sm font-medium text-slate-800 leading-tight truncate" title={labDisplayLabel(left.program_code, left.canonical_name)}>
              {leftLabel}
            </p>
            {left.total_cus != null && (
              <p className="text-xs text-slate-400">{left.total_cus} CU · since {left.first_seen}</p>
            )}
          </div>
        </div>

        {/* VS divider */}
        <div className="flex items-center px-3 bg-slate-50">
          <span className="text-xs font-semibold text-slate-400">vs</span>
        </div>

        {/* Right program */}
        <div className="flex items-center gap-2 px-4 py-2.5 bg-amber-50/40">
          <span className="font-mono text-xs bg-amber-200 text-amber-800 px-1.5 py-0.5 rounded font-semibold shrink-0">
            {right.program_code}
          </span>
          <div className="min-w-0">
            <p className="text-sm font-medium text-slate-800 leading-tight truncate" title={labDisplayLabel(right.program_code, right.canonical_name)}>
              {rightLabel}
            </p>
            {right.total_cus != null && (
              <p className="text-xs text-slate-400">{right.total_cus} CU · since {right.first_seen}</p>
            )}
          </div>
        </div>
      </div>

      {/* Bottom row: overlap stats + bar */}
      <div className="border-t border-slate-100 px-4 py-2 flex items-center gap-4 flex-wrap bg-slate-50/50">
        <span className="text-xs text-slate-600">
          <strong className="text-emerald-700">{metrics.shared_count}</strong> shared
        </span>
        <span className="text-xs text-slate-600">
          <strong className="text-blue-600">{leftOnly}</strong> {leftLabel}-only
        </span>
        <span className="text-xs text-slate-600">
          <strong className="text-amber-600">{rightOnly}</strong> {rightLabel}-only
        </span>
        <span className="text-xs text-slate-500 border-l border-slate-200 pl-3 ml-1">
          Jaccard <strong className="text-slate-700">{jaccard}%</strong>
        </span>
        <div className="flex-1 min-w-24">
          <OverlapBar metrics={metrics} />
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Shared: Overlap Bar
// ---------------------------------------------------------------------------

function OverlapBar({ metrics }: { metrics: CompareResult }) {
  const union = metrics.left_count + metrics.right_count - metrics.shared_count;
  const sharedPct = union > 0 ? (metrics.shared_count / union) * 100 : 0;
  const leftPct = union > 0 ? ((metrics.left_count - metrics.shared_count) / union) * 100 : 0;
  const rightPct = union > 0 ? ((metrics.right_count - metrics.shared_count) / union) * 100 : 0;
  return (
    <div className="h-2 rounded-full overflow-hidden flex bg-slate-200">
      <div style={{ width: `${sharedPct}%` }} className="bg-emerald-400" title={`Shared ${Math.round(sharedPct)}%`} />
      <div style={{ width: `${leftPct}%` }} className="bg-blue-400" title={`Left-only ${Math.round(leftPct)}%`} />
      <div style={{ width: `${rightPct}%` }} className="bg-amber-400" title={`Right-only ${Math.round(rightPct)}%`} />
    </div>
  );
}

// ---------------------------------------------------------------------------
// PROTOTYPE 1 — Compact Roster-First
// ---------------------------------------------------------------------------
// Intent: sticky compact identity bar → roster begins immediately.
// Stronger lane tinting than production. Moved-term annotations more visible.
// Tests whether compressing the top section + strengthening the roster
// solves most UX pain without changing the fundamental layout.

function Proto1CompactRosterFirst({ payload }: { payload: ComparePayload }) {
  const { left, right } = payload;
  const leftLabel = labShortLabel(left.program_code, left.canonical_name);
  const rightLabel = labShortLabel(right.program_code, right.canonical_name);
  const termLanes = buildTermLanes(payload);

  return (
    <div className="rounded-xl border border-slate-200 overflow-hidden">
      {/* Sticky identity bar */}
      <CompactIdentityBar payload={payload} sticky />

      {/* Lane headers — sticky below the identity bar */}
      <div
        className="grid grid-cols-[1fr_2fr_1fr] gap-0 sticky top-[calc(3.5rem+5rem)] z-10 border-b border-slate-200"
        style={{ top: "calc(3.5rem + 5.5rem)" }}
      >
        <div className="bg-blue-100 border-r border-blue-200 px-3 py-2 text-xs font-semibold text-blue-800">
          {leftLabel} only
          <span className="ml-1.5 font-normal text-blue-600">
            ({metrics1Count(payload, "left")} courses)
          </span>
        </div>
        <div className="bg-emerald-50 border-r border-emerald-200 px-3 py-2 text-xs font-semibold text-emerald-800 text-center">
          Shared
          <span className="ml-1.5 font-normal text-emerald-600">
            ({payload.metrics.shared_count} courses)
          </span>
        </div>
        <div className="bg-amber-100 px-3 py-2 text-xs font-semibold text-amber-800 text-right">
          {rightLabel} only
          <span className="ml-1.5 font-normal text-amber-600">
            ({metrics1Count(payload, "right")} courses)
          </span>
        </div>
      </div>

      {/* Term rows */}
      <div className="divide-y divide-slate-150">
        {termLanes.map(([term, lane]) => (
          <Proto1TermRow
            key={term}
            term={term}
            lane={lane}
            rightCode={right.program_code}
          />
        ))}
      </div>

      <p className="text-xs text-slate-400 px-4 py-3 border-t border-slate-100 bg-slate-50">
        Source: 2026-03 WGU catalog rosters. Exact course code identity only.
      </p>
    </div>
  );
}

function metrics1Count(payload: ComparePayload, side: "left" | "right") {
  return side === "left"
    ? payload.metrics.left_count - payload.metrics.shared_count
    : payload.metrics.right_count - payload.metrics.shared_count;
}

function Proto1TermRow({
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
    <div>
      {/* Term label */}
      <div className="bg-slate-100 px-4 py-1 text-xs font-medium text-slate-500 border-b border-slate-200 flex items-center gap-2">
        {term === 0 ? "Unplaced" : `Term ${term}`}
        {allShared && <span className="text-slate-300 italic">all shared</span>}
      </div>
      {/* Three-lane content row */}
      <div className="grid grid-cols-[1fr_2fr_1fr] min-h-8">
        {/* Left-only */}
        <div className={`px-3 py-2 border-r border-slate-200 ${hasLeft ? "bg-blue-50" : "bg-blue-50/20"}`}>
          {lane.leftOnly.map((c) => (
            <CourseRowCompact key={c.code} course={c} />
          ))}
        </div>
        {/* Shared */}
        <div className="px-3 py-2 border-r border-slate-200 bg-white">
          {lane.shared.map((c) => (
            <CourseRowShared key={c.code} course={c} rightCode={rightCode} />
          ))}
        </div>
        {/* Right-only */}
        <div className={`px-3 py-2 ${hasRight ? "bg-amber-50" : "bg-amber-50/20"}`}>
          {lane.rightOnly.map((c) => (
            <CourseRowCompact key={c.code} course={c} />
          ))}
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// PROTOTYPE 2 — Differences First
// ---------------------------------------------------------------------------
// Intent: Foreground unique courses. Shared curriculum is collapsed by default.
// Tests whether "what's different?" as the primary question improves usability,
// especially for high-overlap pairs where the unique courses are the decision point.

function Proto2DifferencesFirst({ payload }: { payload: ComparePayload }) {
  const { left, right, metrics } = payload;
  const leftLabel = labShortLabel(left.program_code, left.canonical_name);
  const rightLabel = labShortLabel(right.program_code, right.canonical_name);
  const leftOnly = metrics.left_count - metrics.shared_count;
  const rightOnly = metrics.right_count - metrics.shared_count;

  // Default: shared collapsed when it dominates (Jaccard >= 0.4), expanded when it's a minority
  const [sharedExpanded, setSharedExpanded] = useState(metrics.jaccard_overlap < 0.4);

  // Group left-only and right-only by term for context
  const leftByTerm = groupByTerm(payload.left_only_courses, "left");
  const rightByTerm = groupByTerm(payload.right_only_courses, "right");
  const sharedByTerm = groupByTerm(payload.shared_courses, "left");

  return (
    <div className="rounded-xl border border-slate-200 overflow-hidden">
      <CompactIdentityBar payload={payload} />

      <div className="p-5 space-y-5">
        {/* ── What's Different section ─────────────────────── */}
        <div>
          <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">
            What&rsquo;s Different
          </h3>

          {leftOnly === 0 && rightOnly === 0 ? (
            <p className="text-sm text-slate-400 italic">
              No differences — both rosters are identical.
            </p>
          ) : (
            <div className="grid sm:grid-cols-2 gap-4">
              {/* Left-only block */}
              <div className="border border-blue-200 rounded-xl overflow-hidden">
                <div className="bg-blue-600 px-4 py-2.5 flex items-center justify-between">
                  <span className="text-sm font-semibold text-white">
                    Only in {leftLabel}
                  </span>
                  <span className="text-xs bg-blue-500 text-blue-100 px-2 py-0.5 rounded-full font-medium">
                    {leftOnly} course{leftOnly !== 1 ? "s" : ""}
                  </span>
                </div>
                {leftOnly === 0 ? (
                  <p className="px-4 py-4 text-sm text-slate-400 italic">
                    No courses unique to this track.
                  </p>
                ) : (
                  <div className="divide-y divide-blue-50">
                    {leftByTerm.map(([term, courses]) => (
                      <DiffTermBlock key={term} term={term} courses={courses} side="left" />
                    ))}
                  </div>
                )}
              </div>

              {/* Right-only block */}
              <div className="border border-amber-200 rounded-xl overflow-hidden">
                <div className="bg-amber-500 px-4 py-2.5 flex items-center justify-between">
                  <span className="text-sm font-semibold text-white">
                    Only in {rightLabel}
                  </span>
                  <span className="text-xs bg-amber-400 text-amber-100 px-2 py-0.5 rounded-full font-medium">
                    {rightOnly} course{rightOnly !== 1 ? "s" : ""}
                  </span>
                </div>
                {rightOnly === 0 ? (
                  <p className="px-4 py-4 text-sm text-slate-400 italic">
                    No courses unique to this track.
                  </p>
                ) : (
                  <div className="divide-y divide-amber-50">
                    {rightByTerm.map(([term, courses]) => (
                      <DiffTermBlock key={term} term={term} courses={courses} side="right" />
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* ── Shared Curriculum section (collapsible) ─────── */}
        <div className="border border-slate-200 rounded-xl overflow-hidden">
          <button
            onClick={() => setSharedExpanded(!sharedExpanded)}
            className="w-full flex items-center justify-between px-4 py-3 bg-slate-50 hover:bg-slate-100 transition-colors text-left"
          >
            <div className="flex items-center gap-3">
              <span className="text-sm font-semibold text-slate-700">
                Shared Curriculum
              </span>
              <span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full font-medium">
                {metrics.shared_count} courses
              </span>
              <span className="text-xs text-slate-400">
                Jaccard {Math.round(metrics.jaccard_overlap * 100)}% · taken regardless of which track you choose
              </span>
            </div>
            <span className="text-slate-400 text-sm ml-2 shrink-0">
              {sharedExpanded ? "▲ collapse" : "▼ expand"}
            </span>
          </button>

          {sharedExpanded && (
            <div className="divide-y divide-slate-100">
              {sharedByTerm.map(([term, courses]) => (
                <SharedTermBlock key={term} term={term} courses={courses} rightCode={right.program_code} />
              ))}
            </div>
          )}
        </div>
      </div>

      <p className="text-xs text-slate-400 px-5 py-3 border-t border-slate-100 bg-slate-50">
        Source: 2026-03 WGU catalog rosters. Exact course code identity only.
      </p>
    </div>
  );
}

function groupByTerm(
  courses: CompareCourseEntry[],
  termKey: "left" | "right"
): [number, CompareCourseEntry[]][] {
  const map = new Map<number, CompareCourseEntry[]>();
  for (const c of courses) {
    const t = (termKey === "left" ? c.term_left : c.term_right) ?? 0;
    if (!map.has(t)) map.set(t, []);
    map.get(t)!.push(c);
  }
  return [...map.entries()].sort(([a], [b]) => a - b);
}

function DiffTermBlock({
  term,
  courses,
  side,
}: {
  term: number;
  courses: CompareCourseEntry[];
  side: "left" | "right";
}) {
  const bgRow = side === "left" ? "bg-blue-50/60" : "bg-amber-50/60";
  return (
    <div className={bgRow}>
      <div className="px-4 py-1.5 border-b border-slate-100">
        <span className="text-xs font-medium text-slate-400">
          {term === 0 ? "Unplaced" : `Term ${term}`}
        </span>
      </div>
      {courses.map((c) => (
        <div key={c.code} className="flex items-baseline gap-2 px-4 py-1.5 border-b border-white/70 last:border-0">
          <Link
            href={`/courses/${c.code}`}
            className="font-mono text-xs text-blue-700 hover:underline shrink-0"
          >
            {c.code}
          </Link>
          <span className="text-sm text-slate-700 flex-1">{c.title}</span>
          <span className="text-xs text-slate-400 shrink-0 tabular-nums">{c.cus} CU</span>
        </div>
      ))}
    </div>
  );
}

function SharedTermBlock({
  term,
  courses,
  rightCode,
}: {
  term: number;
  courses: CompareCourseEntry[];
  rightCode: string;
}) {
  return (
    <div>
      <div className="px-4 py-1 bg-slate-50 border-b border-slate-100">
        <span className="text-xs font-medium text-slate-400">
          {term === 0 ? "Unplaced" : `Term ${term}`}
        </span>
      </div>
      {courses.map((c) => {
        const hasDrift = c.term_left != null && c.term_right != null && c.term_left !== c.term_right;
        return (
          <div key={c.code} className="flex items-start gap-2 px-4 py-1.5 border-b border-slate-50 last:border-0">
            <Link
              href={`/courses/${c.code}`}
              className="font-mono text-xs text-blue-700 hover:underline shrink-0 mt-0.5"
            >
              {c.code}
            </Link>
            <div className="flex-1 min-w-0">
              <span className="text-sm text-slate-600">{c.title}</span>
              {hasDrift && (
                <span className="block text-xs text-amber-600 font-medium">
                  ↕ term {c.term_right} in {rightCode}
                </span>
              )}
            </div>
            <span className="text-xs text-slate-400 shrink-0 tabular-nums mt-0.5">{c.cus} CU</span>
          </div>
        );
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------
// PROTOTYPE 3 — Lane-Based Visual Compare
// ---------------------------------------------------------------------------
// Intent: Bolder visual language. Solid lane fills. High-contrast term dividers.
// Course entries feel more like a comparison graphic, less like a sparse table.
// Tests whether stronger visual system improves scannability on long rosters.

function Proto3LaneVisual({ payload }: { payload: ComparePayload }) {
  const { left, right } = payload;
  const leftLabel = labShortLabel(left.program_code, left.canonical_name);
  const rightLabel = labShortLabel(right.program_code, right.canonical_name);
  const leftOnly = payload.metrics.left_count - payload.metrics.shared_count;
  const rightOnly = payload.metrics.right_count - payload.metrics.shared_count;
  const termLanes = buildTermLanes(payload);

  return (
    <div className="rounded-xl border border-slate-300 overflow-hidden">
      <CompactIdentityBar payload={payload} />

      {/* Column headers — bold, color-filled */}
      <div className="grid grid-cols-[1fr_2fr_1fr]">
        <div className="bg-blue-600 px-3 py-2.5 text-center">
          <p className="text-xs font-bold text-white leading-tight">{leftLabel}</p>
          <p className="text-xs text-blue-200 mt-0.5">{leftOnly} unique · {left.program_code}</p>
        </div>
        <div className="bg-slate-700 px-3 py-2.5 text-center border-x border-slate-600">
          <p className="text-xs font-bold text-white leading-tight">Shared</p>
          <p className="text-xs text-slate-300 mt-0.5">{payload.metrics.shared_count} courses in both</p>
        </div>
        <div className="bg-amber-500 px-3 py-2.5 text-center">
          <p className="text-xs font-bold text-white leading-tight">{rightLabel}</p>
          <p className="text-xs text-amber-100 mt-0.5">{rightOnly} unique · {right.program_code}</p>
        </div>
      </div>

      {/* Term rows */}
      <div>
        {termLanes.map(([term, lane]) => (
          <Proto3TermRow
            key={term}
            term={term}
            lane={lane}
            rightCode={right.program_code}
          />
        ))}
      </div>

      <p className="text-xs text-slate-400 px-4 py-3 border-t border-slate-200 bg-slate-50">
        Source: 2026-03 WGU catalog rosters. Exact course code identity only.
      </p>
    </div>
  );
}

function Proto3TermRow({
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
          <span className="text-xs text-slate-300 font-normal">all shared this term</span>
        )}
      </div>

      {/* Three-lane content */}
      <div className="grid grid-cols-[1fr_2fr_1fr]">
        {/* Left-only */}
        <div className={`px-3 py-2 border-r border-slate-200 ${hasLeft ? "bg-blue-100" : "bg-blue-50/30"}`}>
          {lane.leftOnly.map((c) => (
            <Proto3CourseCard key={c.code} course={c} accent="blue" />
          ))}
        </div>
        {/* Shared */}
        <div className="px-3 py-2 border-r border-slate-200 bg-slate-50">
          {lane.shared.map((c) => (
            <Proto3SharedCard key={c.code} course={c} rightCode={rightCode} />
          ))}
        </div>
        {/* Right-only */}
        <div className={`px-3 py-2 ${hasRight ? "bg-amber-100" : "bg-amber-50/30"}`}>
          {lane.rightOnly.map((c) => (
            <Proto3CourseCard key={c.code} course={c} accent="amber" />
          ))}
        </div>
      </div>
    </div>
  );
}

function Proto3CourseCard({
  course,
  accent,
}: {
  course: CompareCourseEntry;
  accent: "blue" | "amber";
}) {
  const borderColor = accent === "blue" ? "border-blue-400" : "border-amber-400";
  const codeColor = accent === "blue" ? "text-blue-800 bg-blue-200" : "text-amber-800 bg-amber-200";
  return (
    <div className={`flex items-start gap-1.5 py-1.5 pl-2 border-l-2 ${borderColor} mb-1 last:mb-0`}>
      <Link
        href={`/courses/${course.code}`}
        className={`font-mono text-xs px-1 py-0.5 rounded shrink-0 hover:underline ${codeColor}`}
      >
        {course.code}
      </Link>
      <div className="flex-1 min-w-0">
        <p className="text-xs text-slate-700 leading-snug">{course.title}</p>
      </div>
      <span className="text-xs text-slate-500 shrink-0 tabular-nums ml-1">{course.cus}</span>
    </div>
  );
}

function Proto3SharedCard({
  course,
  rightCode,
}: {
  course: CompareCourseEntry;
  rightCode: string;
}) {
  const hasDrift = course.term_left != null && course.term_right != null && course.term_left !== course.term_right;
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
      <span className="text-xs text-slate-500 shrink-0 tabular-nums ml-1">{course.cus}</span>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Shared course row helpers (used by Proto1)
// ---------------------------------------------------------------------------

function CourseRowCompact({ course }: { course: CompareCourseEntry }) {
  return (
    <div className="flex items-baseline gap-1.5 py-1 min-w-0">
      <Link
        href={`/courses/${course.code}`}
        className="font-mono text-xs text-blue-700 hover:underline shrink-0"
      >
        {course.code}
      </Link>
      <span className="text-xs text-slate-700 flex-1 leading-snug min-w-0 truncate" title={course.title}>
        {course.title}
      </span>
      <span className="text-xs text-slate-400 shrink-0 tabular-nums ml-1">{course.cus}</span>
    </div>
  );
}

function CourseRowShared({
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
    <div className="flex items-baseline gap-1.5 py-1 min-w-0">
      <Link
        href={`/courses/${course.code}`}
        className="font-mono text-xs text-blue-700 hover:underline shrink-0"
      >
        {course.code}
      </Link>
      <div className="flex-1 min-w-0">
        <span className="text-xs text-slate-700 leading-snug">{course.title}</span>
        {hasDrift && (
          <span className="block text-xs text-amber-600 font-semibold">
            ↕ term {course.term_right} in {rightCode}
          </span>
        )}
      </div>
      <span className="text-xs text-slate-400 shrink-0 tabular-nums ml-1">{course.cus}</span>
    </div>
  );
}
