"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import type { ProgramRecord } from "@/lib/types";

const SCHOOLS = ["Business", "Health Professions", "Technology", "Education"];

export default function ProgramExplorer({ programs }: { programs: ProgramRecord[] }) {
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<"all" | "active" | "retired">("active");
  const [schoolFilter, setSchoolFilter] = useState("");
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 50;

  const filtered = useMemo(() => {
    const q = query.toLowerCase();
    return programs.filter((p) => {
      if (statusFilter === "active" && p.status !== "ACTIVE") return false;
      if (statusFilter === "retired" && p.status !== "RETIRED") return false;
      if (schoolFilter && !p.school.toLowerCase().includes(schoolFilter.toLowerCase())) return false;
      if (q && !p.canonical_name.toLowerCase().includes(q) && !p.program_code.toLowerCase().includes(q)) return false;
      return true;
    });
  }, [programs, query, statusFilter, schoolFilter]);

  const paged = filtered.slice(0, page * PAGE_SIZE);

  return (
    <div>
      {/* Filters */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 mb-5 flex flex-wrap gap-3 items-end">
        <div className="flex-1 min-w-48">
          <label className="block text-xs text-slate-500 mb-1">Search</label>
          <input
            type="text"
            placeholder="Program name or code…"
            value={query}
            onChange={(e) => { setQuery(e.target.value); setPage(1); }}
            className="w-full border border-slate-300 rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-xs text-slate-500 mb-1">Status</label>
          <select
            value={statusFilter}
            onChange={(e) => { setStatusFilter(e.target.value as typeof statusFilter); setPage(1); }}
            className="border border-slate-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="active">Active only</option>
            <option value="retired">Deprecated only</option>
            <option value="all">All</option>
          </select>
        </div>

        <div>
          <label className="block text-xs text-slate-500 mb-1">School</label>
          <select
            value={schoolFilter}
            onChange={(e) => { setSchoolFilter(e.target.value); setPage(1); }}
            className="border border-slate-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All schools</option>
            {SCHOOLS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        <button
          onClick={() => { setQuery(""); setStatusFilter("active"); setSchoolFilter(""); setPage(1); }}
          className="text-xs text-slate-500 hover:text-slate-800 underline"
        >
          Reset
        </button>
      </div>

      <p className="text-sm text-slate-500 mb-3">
        {filtered.length.toLocaleString()} program{filtered.length !== 1 ? "s" : ""}
        {filtered.length !== programs.length && ` of ${programs.length.toLocaleString()}`}
      </p>

      <div className="flex flex-col gap-2">
        {paged.map((program) => (
          <Link key={program.program_code} href={`/programs/${program.program_code}`}>
            <div className="border border-slate-200 rounded-lg px-4 py-3 flex items-center gap-3 text-sm hover:border-blue-300 hover:bg-blue-50 transition-colors cursor-pointer">
              <span className="font-mono text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded font-semibold shrink-0">
                {program.program_code}
              </span>
              <span className={`flex-1 font-medium ${program.status === "ACTIVE" ? "text-slate-800" : "text-slate-500"}`}>
                {program.canonical_name}
              </span>
              <div className="hidden md:flex items-center gap-3 shrink-0 text-xs text-slate-400">
                {program.status === "RETIRED" && (
                  <span>deprecated {program.last_seen}</span>
                )}
                <span>{program.school}</span>
                <span className="text-blue-400">→</span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {paged.length < filtered.length && (
        <button
          onClick={() => setPage((p) => p + 1)}
          className="mt-5 w-full border border-slate-300 rounded-lg py-2 text-sm text-slate-600 hover:bg-slate-50 transition-colors"
        >
          Show more ({filtered.length - paged.length} remaining)
        </button>
      )}

      {filtered.length === 0 && (
        <p className="text-center text-slate-400 py-12">No programs match these filters.</p>
      )}
    </div>
  );
}
