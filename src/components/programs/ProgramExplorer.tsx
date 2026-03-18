"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import type { ProgramRecord } from "@/lib/types";
import { classifyDegreeLevel } from "@/lib/programs";
import { COLLEGES, LEVELS } from "@/lib/colleges";

export default function ProgramExplorer({ programs }: { programs: ProgramRecord[] }) {
  const [college, setCollegeState] = useState("");
  const [level, setLevelState] = useState("");
  const [search, setSearch] = useState("");
  const [includeRetired, setIncludeRetired] = useState(false);
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 50;

  function setCollege(val: string) {
    setCollegeState(val);
    setLevelState("");
    setPage(1);
  }
  function setLevel(val: string) {
    setLevelState(val === level ? "" : val);
    setPage(1);
  }

  const filtered = useMemo(() => {
    const q = search.toLowerCase().trim();
    return programs.filter((p) => {
      if (!includeRetired && p.status !== "ACTIVE") return false;

      if (college && p.school !== college) return false;

      if (level) {
        const dl = classifyDegreeLevel(p);
        if (level === "Bachelor's" && dl !== "Bachelor's") return false;
        if (level === "Master's" && dl !== "Master's") return false;
        if (level === "Certificate" && dl !== "Certificates & Endorsements") return false;
      }

      if (q && !p.canonical_name.toLowerCase().includes(q) && !p.program_code.toLowerCase().includes(q))
        return false;

      return true;
    });
  }, [programs, college, level, search, includeRetired]);

  const paged = filtered.slice(0, page * PAGE_SIZE);
  const hasMore = paged.length < filtered.length;
  const hasFilters = !!(college || level || search);

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
              checked={includeRetired}
              onChange={(e) => { setIncludeRetired(e.target.checked); setPage(1); }}
              className="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-xs text-slate-600">Include retired degrees</span>
          </label>
        </div>

        {/* Level + Search row */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide w-16 shrink-0">
            Level
          </span>
          {LEVELS.map((lv) => (
            <button
              key={lv}
              onClick={() => setLevel(lv)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                level === lv
                  ? "bg-slate-700 text-white"
                  : "bg-white border border-slate-300 text-slate-600 hover:border-slate-400"
              }`}
            >
              {lv}
            </button>
          ))}

          {hasFilters && (
            <button
              onClick={() => { setCollegeState(""); setLevelState(""); setSearch(""); setPage(1); }}
              className="text-xs text-slate-400 hover:text-slate-700 underline shrink-0"
            >
              Reset
            </button>
          )}

          <div className="flex-1 min-w-32">
            <input
              type="text"
              placeholder="Degree name or code…"
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Active filter summary */}
      {(hasFilters || includeRetired) && (
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
          {includeRetired && (
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
            {filtered.length.toLocaleString()} degree{filtered.length !== 1 ? "s" : ""}
          </span>
        </div>
      )}

      {!hasFilters && !includeRetired && (
        <p className="text-sm text-slate-500 mb-4">
          {filtered.length.toLocaleString()} current degrees
        </p>
      )}

      {/* Results */}
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
                  <span>retired {program.last_seen}</span>
                )}
                <span>{program.school}</span>
                <span className="text-blue-400">→</span>
              </div>
            </div>
          </Link>
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
        <p className="text-center text-slate-400 py-12">No degrees match these filters.</p>
      )}
    </div>
  );
}
