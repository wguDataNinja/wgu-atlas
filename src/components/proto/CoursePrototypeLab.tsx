"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import type { CourseCard, ProgramRecord } from "@/lib/types";
import { classifyDegreeLevel } from "@/lib/programs";

// ---------------------------------------------------------------------------
// Types & constants
// ---------------------------------------------------------------------------

interface LabProps {
  courses: CourseCard[];
  detailCodes: Set<string>;
  programs: ProgramRecord[];
  programRosterMap: Record<string, string[]>;
  courseLevels: Record<string, string[]>;
}

interface FilterState {
  college: string;
  level: string;
  degree: string;
  search: string;
}

const EMPTY_FILTER: FilterState = { college: "", level: "", degree: "", search: "" };

const COLLEGES = [
  {
    key: "School of Business",
    short: "Business",
    description: "Accounting, management, marketing, finance, IT management",
    colorBg: "bg-blue-50",
    colorBorder: "border-blue-300",
    colorText: "text-blue-700",
    colorSelected: "bg-blue-600 text-white border-blue-600",
    colorHover: "hover:border-blue-400 hover:bg-blue-50",
    chipSelected: "bg-blue-600 text-white",
    chipUnselected: "bg-white text-blue-700 border border-blue-300 hover:bg-blue-50",
  },
  {
    key: "Leavitt School of Health",
    short: "Health",
    description: "Nursing, healthcare administration, public health, informatics",
    colorBg: "bg-rose-50",
    colorBorder: "border-rose-300",
    colorText: "text-rose-700",
    colorSelected: "bg-rose-600 text-white border-rose-600",
    colorHover: "hover:border-rose-400 hover:bg-rose-50",
    chipSelected: "bg-rose-600 text-white",
    chipUnselected: "bg-white text-rose-700 border border-rose-300 hover:bg-rose-50",
  },
  {
    key: "School of Technology",
    short: "Technology",
    description: "IT, cybersecurity, software engineering, data analytics, CS",
    colorBg: "bg-violet-50",
    colorBorder: "border-violet-300",
    colorText: "text-violet-700",
    colorSelected: "bg-violet-600 text-white border-violet-600",
    colorHover: "hover:border-violet-400 hover:bg-violet-50",
    chipSelected: "bg-violet-600 text-white",
    chipUnselected: "bg-white text-violet-700 border border-violet-300 hover:bg-violet-50",
  },
  {
    key: "School of Education",
    short: "Education",
    description: "Teacher preparation, educational leadership, learning technology",
    colorBg: "bg-amber-50",
    colorBorder: "border-amber-300",
    colorText: "text-amber-700",
    colorSelected: "bg-amber-500 text-white border-amber-500",
    colorHover: "hover:border-amber-400 hover:bg-amber-50",
    chipSelected: "bg-amber-500 text-white",
    chipUnselected: "bg-white text-amber-700 border border-amber-300 hover:bg-amber-50",
  },
];

const LEVELS = ["Bachelor's", "Master's", "Certificate"];

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

function courseMatchesCollege(course: CourseCard, collegeKey: string): boolean {
  const parts = course.current_college.split("; ").map((s) => s.trim());
  return parts.includes(collegeKey);
}

function courseMatchesLevel(
  course: CourseCard,
  level: string,
  courseLevels: Record<string, string[]>
): boolean {
  if (level === "Certificate") return course.scope === "cert";
  const levels = courseLevels[course.code] ?? [];
  return levels.includes(level) && course.scope !== "cert";
}

function getDegreeOptions(
  programs: ProgramRecord[],
  college: string,
  level: string
): ProgramRecord[] {
  if (!college || !level) return [];
  return programs.filter((p) => {
    if (p.school !== college) return false;
    const dl = classifyDegreeLevel(p);
    if (level === "Bachelor's") return dl === "Bachelor's";
    if (level === "Master's") return dl === "Master's";
    if (level === "Certificate") return dl === "Certificates & Endorsements";
    return false;
  });
}

function filterCourses(
  courses: CourseCard[],
  state: FilterState,
  courseLevels: Record<string, string[]>,
  programRosterMap: Record<string, string[]>,
  activeOnly = true
): CourseCard[] {
  const q = state.search.toLowerCase().trim();

  // If a specific degree is selected, use roster membership as the primary filter
  if (state.degree) {
    const rosterSet = new Set(programRosterMap[state.degree] ?? []);
    return courses.filter((c) => {
      if (activeOnly && !c.active) return false;
      if (!rosterSet.has(c.code)) return false;
      if (q && !c.code.toLowerCase().includes(q) && !c.title.toLowerCase().includes(q)) return false;
      return true;
    });
  }

  return courses.filter((c) => {
    if (activeOnly && !c.active) return false;

    if (state.college) {
      if (state.level === "Certificate") {
        // Cert courses don't have a college match; show all when certificate level is selected
        if (c.scope !== "cert") return false;
      } else {
        if (!courseMatchesCollege(c, state.college)) return false;
      }
    }

    if (state.level) {
      if (!courseMatchesLevel(c, state.level, courseLevels)) return false;
    }

    if (q && !c.code.toLowerCase().includes(q) && !c.title.toLowerCase().includes(q)) return false;

    return true;
  });
}

// ---------------------------------------------------------------------------
// Shared CourseRow
// ---------------------------------------------------------------------------

function CourseRow({
  course,
  hasDetail,
  showCollege = false,
}: {
  course: CourseCard;
  hasDetail: boolean;
  showCollege?: boolean;
}) {
  const row = (
    <div
      className={`border rounded-lg px-4 py-3 flex items-center gap-3 text-sm transition-colors ${
        hasDetail
          ? "border-slate-200 hover:border-blue-300 hover:bg-blue-50 cursor-pointer"
          : "border-slate-100 bg-slate-50/50"
      }`}
    >
      <span
        className={`font-mono text-xs px-2 py-0.5 rounded font-semibold shrink-0 ${
          course.scope === "cert"
            ? "bg-green-100 text-green-700"
            : course.active
            ? "bg-blue-100 text-blue-700"
            : "bg-slate-100 text-slate-500"
        }`}
      >
        {course.code}
      </span>
      <span className="flex-1 font-medium text-slate-800">{course.title}</span>
      {showCollege && (
        <span className="hidden md:block text-xs text-slate-400 shrink-0 max-w-40 truncate">
          {course.current_college.split("; ")[0]}
        </span>
      )}
      {hasDetail && <span className="text-blue-400 shrink-0">→</span>}
    </div>
  );

  if (hasDetail) return <Link href={`/courses/${course.code}`}>{row}</Link>;
  return row;
}

function CourseList({
  courses,
  detailCodes,
  showCollege,
}: {
  courses: CourseCard[];
  detailCodes: Set<string>;
  showCollege?: boolean;
}) {
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 50;
  const paged = courses.slice(0, page * PAGE_SIZE);
  const hasMore = paged.length < courses.length;

  return (
    <div>
      <div className="flex flex-col gap-2">
        {paged.map((c) => (
          <CourseRow key={c.code} course={c} hasDetail={detailCodes.has(c.code)} showCollege={showCollege} />
        ))}
      </div>
      {hasMore && (
        <button
          onClick={() => setPage((p) => p + 1)}
          className="mt-4 w-full border border-slate-300 rounded-lg py-2 text-sm text-slate-600 hover:bg-slate-50 transition-colors"
        >
          Show more ({courses.length - paged.length} remaining)
        </button>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// PROTOTYPE 1 — Card-First Guided Browse
// ---------------------------------------------------------------------------

function Proto1({ courses, detailCodes, programs, programRosterMap, courseLevels }: LabProps) {
  const [state, setState] = useState<FilterState>(EMPTY_FILTER);

  const setCollege = (college: string) =>
    setState({ college, level: "", degree: "", search: "" });
  const setLevel = (level: string) =>
    setState((s) => ({ ...s, level, degree: "" }));
  const setDegree = (degree: string) =>
    setState((s) => ({ ...s, degree }));
  const setSearch = (search: string) =>
    setState((s) => ({ ...s, search }));

  const degreeOptions = useMemo(
    () => getDegreeOptions(programs, state.college, state.level),
    [programs, state.college, state.level]
  );

  const filtered = useMemo(
    () => filterCourses(courses, state, courseLevels, programRosterMap),
    [courses, state, courseLevels, programRosterMap]
  );

  const selectedCollege = COLLEGES.find((c) => c.key === state.college);

  return (
    <section className="py-10 border-b border-slate-200">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-1">
          <span className="bg-slate-800 text-white text-xs font-mono px-2 py-1 rounded">PROTO 1</span>
          <h2 className="text-xl font-bold text-slate-800">Card-First Guided Browse</h2>
        </div>
        <p className="text-slate-500 text-sm">
          College as the primary entry point. Choose a college to reveal level and degree options.
          Soft-gated start — results only appear after a college is selected.
        </p>
      </div>

      {/* College Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        {COLLEGES.map((col) => {
          const isSelected = state.college === col.key;
          return (
            <button
              key={col.key}
              onClick={() => setCollege(isSelected ? "" : col.key)}
              className={`text-left p-4 rounded-xl border-2 transition-all ${
                isSelected
                  ? col.colorSelected
                  : `bg-white ${col.colorBorder} ${col.colorHover}`
              }`}
            >
              <div className={`text-sm font-bold mb-1 ${isSelected ? "text-white" : col.colorText}`}>
                {col.short}
              </div>
              <div className={`text-xs leading-snug ${isSelected ? "text-white/80" : "text-slate-500"}`}>
                {col.description}
              </div>
              {isSelected && (
                <div className="mt-2 text-xs text-white/90 font-medium">✓ Selected</div>
              )}
            </button>
          );
        })}
      </div>

      {/* Level (visible after college selection) */}
      {state.college && (
        <div className="mb-5">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Level</div>
          <div className="flex gap-2 flex-wrap">
            {LEVELS.map((lv) => (
              <button
                key={lv}
                onClick={() => setLevel(state.level === lv ? "" : lv)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  state.level === lv
                    ? "bg-slate-800 text-white"
                    : "bg-white border border-slate-300 text-slate-700 hover:border-slate-400 hover:bg-slate-50"
                }`}
              >
                {lv}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Degree (optional, visible after college + level) */}
      {state.college && state.level && degreeOptions.length > 0 && (
        <div className="mb-5">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">
            Degree <span className="text-slate-400 font-normal normal-case">(optional)</span>
          </div>
          <select
            value={state.degree}
            onChange={(e) => setDegree(e.target.value)}
            className="w-full max-w-lg border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
          >
            <option value="">All {state.level} degrees in {selectedCollege?.short}</option>
            {degreeOptions.map((p) => (
              <option key={p.program_code} value={p.program_code}>
                {p.canonical_name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Search (visible after college selection) */}
      {state.college && (
        <div className="mb-5">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Search</div>
          <input
            type="text"
            placeholder="Filter by code or title…"
            value={state.search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full max-w-sm border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      )}

      {/* Results */}
      {!state.college ? (
        <div className="rounded-xl border-2 border-dashed border-slate-200 py-16 text-center">
          <div className="text-3xl mb-3">☝️</div>
          <p className="text-slate-500 font-medium">Select a college above to browse its courses.</p>
          <p className="text-slate-400 text-sm mt-1">Then narrow by level, degree, or search.</p>
        </div>
      ) : (
        <div>
          {/* Current slice breadcrumb */}
          <div className="flex items-center gap-2 text-sm mb-4">
            <span
              className={`px-2 py-1 rounded-md text-xs font-semibold ${selectedCollege?.colorSelected}`}
            >
              {selectedCollege?.short}
            </span>
            {state.level && (
              <>
                <span className="text-slate-400">›</span>
                <span className="px-2 py-1 rounded-md text-xs font-semibold bg-slate-800 text-white">
                  {state.level}
                </span>
              </>
            )}
            {state.degree && (
              <>
                <span className="text-slate-400">›</span>
                <span className="px-2 py-1 rounded-md text-xs font-semibold bg-slate-100 text-slate-700 max-w-xs truncate">
                  {programs.find((p) => p.program_code === state.degree)?.canonical_name ?? state.degree}
                </span>
              </>
            )}
            <span className="text-slate-400 text-xs ml-auto">{filtered.length} courses</span>
          </div>
          {filtered.length === 0 ? (
            <p className="text-center text-slate-400 py-12">No courses match these filters.</p>
          ) : (
            <CourseList courses={filtered} detailCodes={detailCodes} />
          )}
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// PROTOTYPE 2 — Compact Top-Bar Sibling System
// ---------------------------------------------------------------------------

function Proto2({ courses, detailCodes, programs, programRosterMap, courseLevels }: LabProps) {
  // Prefiltered default: Technology + Bachelor's
  const [state, setState] = useState<FilterState>({
    college: "School of Technology",
    level: "Bachelor's",
    degree: "",
    search: "",
  });
  const [activeOnly, setActiveOnly] = useState(true);

  const setCollege = (college: string) =>
    setState((s) => ({ ...s, college, level: s.college === college ? s.level : "", degree: "", search: "" }));
  const setLevel = (level: string) =>
    setState((s) => ({ ...s, level: s.level === level ? "" : level, degree: "" }));
  const setDegree = (degree: string) =>
    setState((s) => ({ ...s, degree }));
  const setSearch = (search: string) =>
    setState((s) => ({ ...s, search }));

  const degreeOptions = useMemo(
    () => getDegreeOptions(programs, state.college, state.level),
    [programs, state.college, state.level]
  );

  const filtered = useMemo(
    () => filterCourses(courses, state, courseLevels, programRosterMap, activeOnly),
    [courses, state, courseLevels, programRosterMap, activeOnly]
  );

  const selectedCollege = COLLEGES.find((c) => c.key === state.college);

  return (
    <section className="py-10 border-b border-slate-200">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-1">
          <span className="bg-slate-800 text-white text-xs font-mono px-2 py-1 rounded">PROTO 2</span>
          <h2 className="text-xl font-bold text-slate-800">Compact Top-Bar Sibling System</h2>
        </div>
        <p className="text-slate-500 text-sm">
          Dense, product-style filter bar. College chips stay visually dominant. Starts prefiltered to
          Technology / Bachelor&apos;s. Fast and repeatable — results always visible below.
        </p>
      </div>

      {/* Filter zone */}
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-5">
        {/* College chips — primary row */}
        <div className="flex items-center gap-2 flex-wrap mb-3">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide w-16 shrink-0">College</span>
          {COLLEGES.map((col) => {
            const isSelected = state.college === col.key;
            return (
              <button
                key={col.key}
                onClick={() => setCollege(isSelected ? "" : col.key)}
                className={`px-3 py-1.5 rounded-lg text-sm font-semibold transition-colors ${
                  isSelected ? col.chipSelected : col.chipUnselected
                }`}
              >
                {col.short}
              </button>
            );
          })}
          <div className="h-5 w-px bg-slate-300 mx-1" />
          <label className="flex items-center gap-1.5 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={activeOnly}
              onChange={(e) => setActiveOnly(e.target.checked)}
              className="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-xs text-slate-600">Active courses only</span>
          </label>
        </div>

        {/* Level + Degree + Search — secondary row */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide w-16 shrink-0">Level</span>
          {LEVELS.map((lv) => (
            <button
              key={lv}
              onClick={() => setLevel(lv)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                state.level === lv
                  ? "bg-slate-700 text-white"
                  : "bg-white border border-slate-300 text-slate-600 hover:border-slate-400"
              }`}
            >
              {lv}
            </button>
          ))}

          {/* Divider */}
          {(degreeOptions.length > 0 || state.degree) && (
            <div className="h-6 w-px bg-slate-300 mx-1" />
          )}

          {/* Degree */}
          {degreeOptions.length > 0 && (
            <select
              value={state.degree}
              onChange={(e) => setDegree(e.target.value)}
              className="border border-slate-300 rounded-lg px-3 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 max-w-56"
            >
              <option value="">All degrees</option>
              {degreeOptions.map((p) => (
                <option key={p.program_code} value={p.program_code}>
                  {p.canonical_name}
                </option>
              ))}
            </select>
          )}

          {/* Reset */}
          {(state.college || state.level || state.degree || state.search) && (
            <button
              onClick={() => setState(EMPTY_FILTER)}
              className="text-xs text-slate-400 hover:text-slate-700 underline shrink-0"
            >
              Reset
            </button>
          )}

          {/* Search */}
          <div className="flex-1 min-w-32">
            <input
              type="text"
              placeholder="Code or title…"
              value={state.search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Active filter indicator */}
      <div className="flex items-center gap-3 mb-4 min-h-6">
        {state.college || state.level || state.degree ? (
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-xs text-slate-500">Showing:</span>
            {state.college && (
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${selectedCollege?.chipSelected}`}>
                {selectedCollege?.short}
              </span>
            )}
            {state.level && (
              <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-700 text-white">
                {state.level}
              </span>
            )}
            {state.degree && (
              <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-100 text-slate-700 max-w-xs truncate">
                {programs.find((p) => p.program_code === state.degree)?.canonical_name}
              </span>
            )}
            {state.search && (
              <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-100 text-slate-700">
                &ldquo;{state.search}&rdquo;
              </span>
            )}
          </div>
        ) : (
          <span className="text-xs text-slate-400">No filters active — showing all active courses</span>
        )}
        <span className="text-xs text-slate-400 ml-auto">{filtered.length.toLocaleString()} courses</span>
      </div>

      {/* Results */}
      {filtered.length === 0 ? (
        <p className="text-center text-slate-400 py-12">No courses match these filters.</p>
      ) : (
        <CourseList courses={filtered} detailCodes={detailCodes} />
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// PROTOTYPE 3 — Split-Panel / Persistent Context
// ---------------------------------------------------------------------------

function Proto3({ courses, detailCodes, programs, programRosterMap, courseLevels }: LabProps) {
  // Default: Technology college selected
  const [state, setState] = useState<FilterState>({
    college: "School of Technology",
    level: "",
    degree: "",
    search: "",
  });
  const [panelOpen, setPanelOpen] = useState(true);

  const setCollege = (college: string) =>
    setState((s) => ({
      ...s,
      college: s.college === college ? "" : college,
      level: "",
      degree: "",
    }));
  const setLevel = (level: string) =>
    setState((s) => ({ ...s, level: s.level === level ? "" : level, degree: "" }));
  const setDegree = (degree: string) =>
    setState((s) => ({ ...s, degree }));
  const setSearch = (search: string) =>
    setState((s) => ({ ...s, search }));

  const degreeOptions = useMemo(
    () => getDegreeOptions(programs, state.college, state.level),
    [programs, state.college, state.level]
  );

  const filtered = useMemo(
    () => filterCourses(courses, state, courseLevels, programRosterMap),
    [courses, state, courseLevels, programRosterMap]
  );

  const selectedCollege = COLLEGES.find((c) => c.key === state.college);

  // Build a human-readable slice label
  const sliceLabel = useMemo(() => {
    const parts: string[] = [];
    if (state.college) parts.push(selectedCollege?.short ?? state.college);
    if (state.level) parts.push(state.level);
    if (state.degree) {
      const p = programs.find((p) => p.program_code === state.degree);
      if (p) parts.push(p.canonical_name);
    }
    return parts.join(" / ");
  }, [state, selectedCollege, programs]);

  return (
    <section className="py-10">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-1">
          <span className="bg-slate-800 text-white text-xs font-mono px-2 py-1 rounded">PROTO 3</span>
          <h2 className="text-xl font-bold text-slate-800">Split-Panel / Persistent Context</h2>
        </div>
        <p className="text-slate-500 text-sm">
          Persistent left-panel filter sidebar with contextual results on the right. College is the
          first filter; the current slice is always visible. Defaults to Technology — no results gate.
        </p>
      </div>

      {/* Mobile panel toggle */}
      <div className="md:hidden mb-3">
        <button
          onClick={() => setPanelOpen((o) => !o)}
          className="w-full flex items-center justify-between px-4 py-3 bg-slate-100 rounded-lg text-sm font-medium text-slate-700"
        >
          <span>Filters{sliceLabel ? ` — ${sliceLabel}` : ""}</span>
          <span>{panelOpen ? "▲ Hide" : "▼ Show"}</span>
        </button>
      </div>

      <div className="flex gap-6 items-start">
        {/* Left panel */}
        <div
          className={`w-60 shrink-0 ${panelOpen ? "block" : "hidden"} md:block`}
        >
          <div className="bg-white border border-slate-200 rounded-xl p-4 sticky top-4">
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
              College
            </div>
            <div className="flex flex-col gap-1 mb-5">
              {COLLEGES.map((col) => {
                const isSelected = state.college === col.key;
                return (
                  <button
                    key={col.key}
                    onClick={() => setCollege(col.key)}
                    className={`text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      isSelected
                        ? `${col.colorSelected}`
                        : `text-slate-600 hover:bg-slate-50`
                    }`}
                  >
                    <span className={isSelected ? "text-white" : col.colorText}>
                      {col.short}
                    </span>
                    {isSelected && <span className="ml-1 text-white/80 text-xs">✓</span>}
                  </button>
                );
              })}
            </div>

            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
              Level
            </div>
            <div className="flex flex-col gap-1 mb-5">
              {LEVELS.map((lv) => (
                <button
                  key={lv}
                  onClick={() => setLevel(lv)}
                  className={`text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    state.level === lv
                      ? "bg-slate-800 text-white"
                      : "text-slate-600 hover:bg-slate-50"
                  }`}
                >
                  {lv}
                  {state.level === lv && <span className="ml-1 text-white/80 text-xs">✓</span>}
                </button>
              ))}
            </div>

            {degreeOptions.length > 0 && (
              <>
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
                  Degree <span className="text-slate-400 font-normal normal-case">(optional)</span>
                </div>
                <div className="mb-5">
                  <select
                    value={state.degree}
                    onChange={(e) => setDegree(e.target.value)}
                    className="w-full border border-slate-300 rounded-lg px-2 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                  >
                    <option value="">All degrees</option>
                    {degreeOptions.map((p) => (
                      <option key={p.program_code} value={p.program_code}>
                        {p.canonical_name}
                      </option>
                    ))}
                  </select>
                </div>
              </>
            )}

            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">
              Search
            </div>
            <input
              type="text"
              placeholder="Code or title…"
              value={state.search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
            />

            {/* Current state summary */}
            <div className="bg-slate-50 rounded-lg p-3 text-xs text-slate-500 space-y-1">
              <div className="font-semibold text-slate-600 mb-1.5">Current filter</div>
              <div>
                College:{" "}
                <span className={`font-medium ${selectedCollege ? selectedCollege.colorText : "text-slate-400"}`}>
                  {selectedCollege?.short ?? "All"}
                </span>
              </div>
              <div>
                Level:{" "}
                <span className="font-medium text-slate-700">{state.level || "Any"}</span>
              </div>
              <div>
                Degree:{" "}
                <span className="font-medium text-slate-700">
                  {state.degree
                    ? programs.find((p) => p.program_code === state.degree)?.canonical_name ?? state.degree
                    : "All"}
                </span>
              </div>
              {(state.college || state.level || state.degree || state.search) && (
                <button
                  onClick={() => setState({ college: "", level: "", degree: "", search: "" })}
                  className="mt-2 text-slate-400 hover:text-slate-600 underline block"
                >
                  Clear all
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Right panel — results */}
        <div className="flex-1 min-w-0">
          {/* Slice header */}
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-semibold text-slate-800">
                {sliceLabel || "All active courses"}
              </h3>
              <p className="text-sm text-slate-500">{filtered.length.toLocaleString()} courses</p>
            </div>
          </div>

          {filtered.length === 0 ? (
            <div className="rounded-xl border-2 border-dashed border-slate-200 py-16 text-center">
              <p className="text-slate-400">No courses match these filters.</p>
            </div>
          ) : (
            <CourseList courses={filtered} detailCodes={detailCodes} showCollege={!state.college} />
          )}
        </div>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Main lab wrapper
// ---------------------------------------------------------------------------

export default function CoursePrototypeLab(props: LabProps) {
  return (
    <div>
      <Proto1 {...props} />
      <Proto2 {...props} />
      <Proto3 {...props} />
    </div>
  );
}
