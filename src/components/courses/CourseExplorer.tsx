"use client";

import { useState, useEffect, useMemo } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import type { CourseCard } from "@/lib/types";

const SCHOOLS = ["Business", "Health", "Technology", "Education"];

export default function CourseExplorer({
  courses,
  detailCodes,
}: {
  courses: CourseCard[];
  detailCodes: Set<string>;
}) {
  const searchParams = useSearchParams();

  const [query, setQuery] = useState(searchParams.get("q") ?? "");
  const [statusFilter, setStatusFilter] = useState<"all" | "active" | "retired">("active");
  const [scopeFilter, setScopeFilter] = useState<"all" | "AP" | "cert">("all");
  const [schoolFilter, setSchoolFilter] = useState(
    searchParams.get("school")
      ? SCHOOLS.find((s) => s.toLowerCase().includes(searchParams.get("school")!)) ?? ""
      : ""
  );
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 50;

  // Reset page when filters change
  useEffect(() => { setPage(1); }, [query, statusFilter, scopeFilter, schoolFilter]);

  const filtered = useMemo(() => {
    const q = query.toLowerCase();
    return courses.filter((c) => {
      if (statusFilter === "active" && !c.active) return false;
      if (statusFilter === "retired" && c.active) return false;
      if (scopeFilter === "AP" && c.scope !== "AP") return false;
      if (scopeFilter === "cert" && c.scope !== "cert") return false;
      if (schoolFilter && !c.current_college?.toLowerCase().includes(schoolFilter.toLowerCase())) return false;
      if (q && !c.code.toLowerCase().includes(q) && !c.title.toLowerCase().includes(q)) return false;
      return true;
    });
  }, [courses, query, statusFilter, scopeFilter, schoolFilter]);

  const paged = filtered.slice(0, page * PAGE_SIZE);
  const hasMore = paged.length < filtered.length;

  return (
    <div>
      {/* Filters */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 mb-5 flex flex-wrap gap-3 items-end">
        {/* Search */}
        <div className="flex-1 min-w-48">
          <label className="block text-xs text-slate-500 mb-1">Search</label>
          <input
            type="text"
            placeholder="Code or title…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full border border-slate-300 rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Status */}
        <div>
          <label className="block text-xs text-slate-500 mb-1">Status</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as typeof statusFilter)}
            className="border border-slate-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="active">Active only</option>
            <option value="retired">Retired only</option>
            <option value="all">All</option>
          </select>
        </div>

        {/* Scope */}
        <div>
          <label className="block text-xs text-slate-500 mb-1">Scope</label>
          <select
            value={scopeFilter}
            onChange={(e) => setScopeFilter(e.target.value as typeof scopeFilter)}
            className="border border-slate-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">AP + Cert</option>
            <option value="AP">AP only</option>
            <option value="cert">Cert only</option>
          </select>
        </div>

        {/* School */}
        <div>
          <label className="block text-xs text-slate-500 mb-1">School</label>
          <select
            value={schoolFilter}
            onChange={(e) => setSchoolFilter(e.target.value)}
            className="border border-slate-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All schools</option>
            {SCHOOLS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        {/* Reset */}
        <button
          onClick={() => { setQuery(""); setStatusFilter("active"); setScopeFilter("all"); setSchoolFilter(""); }}
          className="text-xs text-slate-500 hover:text-slate-800 underline"
        >
          Reset
        </button>
      </div>

      {/* Result count */}
      <p className="text-sm text-slate-500 mb-3">
        {filtered.length.toLocaleString()} course{filtered.length !== 1 ? "s" : ""}
        {filtered.length !== courses.length && ` of ${courses.length.toLocaleString()}`}
      </p>

      {/* Results */}
      <div className="flex flex-col gap-2">
        {paged.map((course) => (
          <CourseRow
            key={course.code}
            course={course}
            hasDetail={detailCodes.has(course.code)}
          />
        ))}
      </div>

      {/* Load more */}
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
    <div className={`border rounded-lg px-4 py-3 flex items-center gap-3 text-sm transition-colors ${
      hasDetail
        ? "border-slate-200 hover:border-blue-300 hover:bg-blue-50 cursor-pointer"
        : "border-slate-100 bg-slate-50/50"
    }`}>
      <span className={`font-mono text-xs px-2 py-0.5 rounded font-semibold shrink-0 ${
        course.scope === "cert"
          ? "bg-green-100 text-green-700"
          : course.active
          ? "bg-blue-100 text-blue-700"
          : "bg-slate-100 text-slate-500"
      }`}>
        {course.code}
      </span>

      <span className={`flex-1 font-medium ${course.active ? "text-slate-800" : "text-slate-500"}`}>
        {course.title}
      </span>

      <div className="hidden md:flex items-center gap-2 shrink-0">
        {!course.active && (
          <span className="text-xs text-slate-400">retired {course.last_seen}</span>
        )}
        <span className="text-xs text-slate-400">{course.current_college}</span>
        {hasDetail && <span className="text-blue-400">→</span>}
      </div>
    </div>
  );

  if (hasDetail) {
    return <Link href={`/courses/${course.code}`}>{row}</Link>;
  }
  return row;
}
