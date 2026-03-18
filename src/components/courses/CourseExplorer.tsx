"use client";

import { useState, useMemo } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import type { CourseCard, ProgramRecord } from "@/lib/types";
import { classifyDegreeLevel } from "@/lib/programs";
import { COLLEGES, LEVELS } from "@/lib/colleges";

export default function CourseExplorer({
  courses,
  detailCodes,
  programs,
  programRosterMap,
  courseLevels,
}: {
  courses: CourseCard[];
  detailCodes: Set<string>;
  programs: ProgramRecord[];
  programRosterMap: Record<string, string[]>;
  courseLevels: Record<string, string[]>;
}) {
  const searchParams = useSearchParams();

  const initialCollege =
    COLLEGES.find((c) =>
      c.key.toLowerCase().includes(searchParams.get("school") ?? "")
    )?.key ?? "";

  const [college, setCollegeState] = useState(initialCollege);
  const [level, setLevelState] = useState("");
  const [degree, setDegree] = useState("");
  const [search, setSearch] = useState(searchParams.get("q") ?? "");
  const [activeOnly, setActiveOnly] = useState(true);
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 50;

  function setCollege(val: string) {
    setCollegeState(val);
    setLevelState("");
    setDegree("");
    setPage(1);
  }
  function setLevel(val: string) {
    setLevelState(val);
    setDegree("");
    setPage(1);
  }

  // Degree options: active programs in selected college + level
  const degreeOptions = useMemo(() => {
    if (!college || !level) return [];
    return programs.filter((p) => {
      if (p.status !== "ACTIVE") return false;
      if (p.school !== college) return false;
      const dl = classifyDegreeLevel(p);
      if (level === "Bachelor's") return dl === "Bachelor's";
      if (level === "Master's") return dl === "Master's";
      if (level === "Certificate") return dl === "Certificates & Endorsements";
      return false;
    });
  }, [programs, college, level]);

  const filtered = useMemo(() => {
    const q = search.toLowerCase().trim();

    // Degree selected — use roster membership as primary gate
    if (degree) {
      const rosterSet = new Set(programRosterMap[degree] ?? []);
      return courses.filter((c) => {
        if (activeOnly && !c.active) return false;
        if (!rosterSet.has(c.code)) return false;
        if (q && !c.code.toLowerCase().includes(q) && !c.title.toLowerCase().includes(q)) return false;
        return true;
      });
    }

    return courses.filter((c) => {
      if (activeOnly && !c.active) return false;

      if (college) {
        if (level === "Certificate") {
          if (c.scope !== "cert") return false;
        } else {
          const collegeDef = COLLEGES.find((col) => col.key === college);
          const parts = c.current_college.split("; ").map((s) => s.trim());
          if (!parts.some((p) => collegeDef?.allNames.includes(p))) return false;
        }
      }

      if (level) {
        if (level === "Certificate") {
          if (c.scope !== "cert") return false;
        } else {
          const levels = courseLevels[c.code] ?? [];
          if (!levels.includes(level) || c.scope === "cert") return false;
        }
      }

      if (q && !c.code.toLowerCase().includes(q) && !c.title.toLowerCase().includes(q)) return false;
      return true;
    });
  }, [courses, college, level, degree, search, activeOnly, courseLevels, programRosterMap]);

  const paged = filtered.slice(0, page * PAGE_SIZE);
  const hasMore = paged.length < filtered.length;
  const hasFilters = !!(college || level || degree || search);

  const selectedCollege = COLLEGES.find((c) => c.key === college);

  return (
    <div>
      {/* Filter zone */}
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-5">
        {/* College row */}
        <div className="flex items-center gap-2 flex-wrap mb-3">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide w-16 shrink-0">
            College
          </span>
          {COLLEGES.map((col) => {
            const isSelected = college === col.key;
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
              onChange={(e) => { setActiveOnly(e.target.checked); setPage(1); }}
              className="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-xs text-slate-600">Active courses only</span>
          </label>
        </div>

        {/* Level + Degree + Search row */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide w-16 shrink-0">
            Level
          </span>
          {LEVELS.map((lv) => (
            <button
              key={lv}
              onClick={() => setLevel(level === lv ? "" : lv)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                level === lv
                  ? "bg-slate-700 text-white"
                  : "bg-white border border-slate-300 text-slate-600 hover:border-slate-400"
              }`}
            >
              {lv}
            </button>
          ))}

          {degreeOptions.length > 0 && (
            <>
              <div className="h-5 w-px bg-slate-300 mx-1" />
              <select
                value={degree}
                onChange={(e) => { setDegree(e.target.value); setPage(1); }}
                className="border border-slate-300 rounded-lg px-3 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 max-w-64"
              >
                <option value="">All degrees</option>
                {degreeOptions.map((p) => (
                  <option key={p.program_code} value={p.program_code}>
                    {p.canonical_name}
                  </option>
                ))}
              </select>
            </>
          )}

          {hasFilters && (
            <button
              onClick={() => {
                setCollegeState("");
                setLevelState("");
                setDegree("");
                setSearch("");
                setPage(1);
              }}
              className="text-xs text-slate-400 hover:text-slate-700 underline shrink-0"
            >
              Reset
            </button>
          )}

          <div className="flex-1 min-w-32">
            <input
              type="text"
              placeholder="Code or title…"
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Active filter summary */}
      {(hasFilters || !activeOnly) && (
        <div className="flex items-center gap-1.5 flex-wrap mb-4">
          <span className="text-xs text-slate-500">Showing:</span>
          {college && (
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${selectedCollege?.chipSelected}`}>
              {selectedCollege?.short}
            </span>
          )}
          {level && (
            <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-700 text-white">
              {level}
            </span>
          )}
          {degree && (
            <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-100 text-slate-700 max-w-xs truncate">
              {programs.find((p) => p.program_code === degree)?.canonical_name}
            </span>
          )}
          {!activeOnly && (
            <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-100 text-slate-600">
              incl. retired
            </span>
          )}
          {search && (
            <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-100 text-slate-700">
              &ldquo;{search}&rdquo;
            </span>
          )}
          <span className="text-xs text-slate-400 ml-auto">
            {filtered.length.toLocaleString()} course{filtered.length !== 1 ? "s" : ""}
          </span>
        </div>
      )}

      {!hasFilters && activeOnly && (
        <p className="text-sm text-slate-500 mb-4">
          {filtered.length.toLocaleString()} active courses
        </p>
      )}

      {/* Results */}
      <div className="flex flex-col gap-2">
        {paged.map((course) => (
          <CourseRow key={course.code} course={course} hasDetail={detailCodes.has(course.code)} />
        ))}
      </div>

      {hasMore && (
        <button
          onClick={() => setPage((p) => p + 1)}
          className="mt-5 w-full border border-slate-300 rounded-lg py-2 text-sm text-slate-600 hover:bg-slate-50 transition-colors"
        >
          Show more ({filtered.length - paged.length} remaining)
        </button>
      )}

      {filtered.length === 0 && (
        <p className="text-center text-slate-400 py-12">No courses match these filters.</p>
      )}
    </div>
  );
}

function CourseRow({ course, hasDetail }: { course: CourseCard; hasDetail: boolean }) {
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
      <span className={`flex-1 font-medium ${course.active ? "text-slate-800" : "text-slate-500"}`}>
        {course.title}
      </span>
      <div className="hidden md:flex items-center gap-2 shrink-0">
        {!course.active && (
          <span className="text-xs text-slate-400">retired {course.last_seen}</span>
        )}
        <span className="text-xs text-slate-400">{course.current_college.split("; ")[0]}</span>
        {hasDetail && <span className="text-blue-400">→</span>}
      </div>
    </div>
  );

  if (hasDetail) return <Link href={`/courses/${course.code}`}>{row}</Link>;
  return row;
}
