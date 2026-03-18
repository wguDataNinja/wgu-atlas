"use client";

import { useState, useMemo } from "react";
import type { ProgramRecord, ProgramEnriched } from "@/lib/types";
import { getIndexName } from "@/lib/families";
import { classifyDegreeLevel, DEGREE_LEVEL_ORDER } from "@/lib/programs";
import { buildLabPayload } from "@/lib/compareUtils";
import CompareView from "./CompareView";

export default function CompareSelector({
  programs,
  enriched,
}: {
  programs: ProgramRecord[];
  enriched: Record<string, Pick<ProgramEnriched, "roster">>;
}) {
  const [selectedA, setSelectedA] = useState<string | null>(null);
  const [selectedB, setSelectedB] = useState<string | null>(null);
  const [schoolFilter, setSchoolFilter] = useState("");
  const [levelFilter, setLevelFilter] = useState("");
  // When both programs are selected, selectors collapse to a compact bar.
  const [expandedSelectors, setExpandedSelectors] = useState(true);

  // Schools available from the programs list
  const schools = useMemo(
    () => [...new Set(programs.map((p) => p.school))].sort(),
    [programs]
  );

  // Degree levels available, restricted to the selected school
  const availableLevels = useMemo(() => {
    const base = schoolFilter
      ? programs.filter((p) => p.school === schoolFilter)
      : programs;
    const levels = new Set(base.map((p) => classifyDegreeLevel(p)));
    return DEGREE_LEVEL_ORDER.filter((l) => levels.has(l));
  }, [programs, schoolFilter]);

  // Programs shown in selector A (filtered by school + level)
  const programsForA = useMemo(() => {
    return programs.filter((p) => {
      if (schoolFilter && p.school !== schoolFilter) return false;
      if (levelFilter && classifyDegreeLevel(p) !== levelFilter) return false;
      return true;
    });
  }, [programs, schoolFilter, levelFilter]);

  // Sibling options for selector B: same school + degree level as selected A
  const siblingsForB = useMemo(() => {
    if (!selectedA) return [];
    const leftProgram = programs.find((p) => p.program_code === selectedA);
    if (!leftProgram) return [];
    const leftSchool = leftProgram.school;
    const leftLevel = classifyDegreeLevel(leftProgram);
    return programs.filter(
      (p) =>
        p.program_code !== selectedA &&
        p.school === leftSchool &&
        classifyDegreeLevel(p) === leftLevel
    );
  }, [selectedA, programs]);

  // Build compare payload when both are selected
  const comparePayload = useMemo(() => {
    if (!selectedA || !selectedB) return null;
    const leftProgram = programs.find((p) => p.program_code === selectedA);
    const rightProgram = programs.find((p) => p.program_code === selectedB);
    const leftEnriched = enriched[selectedA];
    const rightEnriched = enriched[selectedB];
    if (!leftProgram || !rightProgram || !leftEnriched || !rightEnriched)
      return null;
    return buildLabPayload(leftProgram, rightProgram, leftEnriched, rightEnriched);
  }, [selectedA, selectedB, programs, enriched]);

  const handleSelectA = (code: string) => {
    if (code === selectedA) {
      setSelectedA(null);
      setSelectedB(null);
      setExpandedSelectors(true);
    } else {
      setSelectedA(code);
      setSelectedB(null);
      setExpandedSelectors(true);
    }
  };

  const handleSelectB = (code: string) => {
    const newB = code === selectedB ? null : code;
    setSelectedB(newB);
    // Collapse selectors when both programs are confirmed
    if (newB !== null) setExpandedSelectors(false);
  };

  const handleReset = () => {
    setSelectedA(null);
    setSelectedB(null);
    setSchoolFilter("");
    setLevelFilter("");
    setExpandedSelectors(true);
  };

  const selectedAProgram = programs.find((p) => p.program_code === selectedA);
  const selectedBProgram = programs.find((p) => p.program_code === selectedB);
  const bothSelected = !!(selectedA && selectedB);

  // Show full selector panels when expanded (or when only one selected)
  const showFullPanels = expandedSelectors || !bothSelected;

  return (
    <div>
      {/* ── Full selector panels ────────────────────────────────────────── */}
      {showFullPanels && (
        <>
          <div className="grid md:grid-cols-2 gap-5 mb-4">
            {/* ── Selector A ────────────────────────────────────────── */}
            <div className="border border-slate-200 rounded-xl overflow-hidden">
              <div className="bg-slate-50 border-b border-slate-200 px-4 py-3 flex items-center justify-between">
                <h2 className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                  <StepBadge n={1} active />
                  Choose a degree
                </h2>
                {selectedA && (
                  <button
                    onClick={() => {
                      setSelectedA(null);
                      setSelectedB(null);
                    }}
                    className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
                  >
                    Clear
                  </button>
                )}
              </div>

              {/* Filters */}
              <div className="px-4 py-3 border-b border-slate-100 flex gap-2 flex-wrap bg-white">
                <select
                  value={schoolFilter}
                  onChange={(e) => {
                    setSchoolFilter(e.target.value);
                    setLevelFilter("");
                    setSelectedA(null);
                    setSelectedB(null);
                  }}
                  className="border border-slate-300 rounded px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All schools</option>
                  {schools.map((s) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
                <select
                  value={levelFilter}
                  onChange={(e) => {
                    setLevelFilter(e.target.value);
                    setSelectedA(null);
                    setSelectedB(null);
                  }}
                  className="border border-slate-300 rounded px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All levels</option>
                  {availableLevels.map((l) => (
                    <option key={l} value={l}>
                      {l}
                    </option>
                  ))}
                </select>
              </div>

              {/* Program list for A */}
              <div className="divide-y divide-slate-100 max-h-80 overflow-y-auto">
                {programsForA.length === 0 ? (
                  <p className="px-4 py-8 text-center text-sm text-slate-400">
                    No degrees match these filters.
                  </p>
                ) : (
                  programsForA.map((p) => {
                    const isSelected = selectedA === p.program_code;
                    const indexName = getIndexName(p.program_code);
                    const displayName = indexName ?? p.canonical_name;
                    return (
                      <button
                        key={p.program_code}
                        onClick={() => handleSelectA(p.program_code)}
                        className={`w-full text-left px-4 py-3 flex items-start gap-3 transition-colors ${
                          isSelected
                            ? "bg-blue-50 border-l-2 border-blue-500"
                            : "hover:bg-slate-50 border-l-2 border-transparent"
                        }`}
                      >
                        <span
                          className={`font-mono text-xs px-1.5 py-0.5 rounded mt-0.5 shrink-0 ${
                            isSelected
                              ? "bg-blue-200 text-blue-800"
                              : "bg-purple-100 text-purple-700"
                          }`}
                        >
                          {p.program_code}
                        </span>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm text-slate-700 leading-snug">
                            {displayName}
                          </p>
                          {indexName ? (
                            <p className="text-xs text-slate-400 mt-0.5 truncate">
                              {p.canonical_name}
                            </p>
                          ) : (
                            <p className="text-xs text-slate-400 mt-0.5">
                              {p.school} · {classifyDegreeLevel(p)}
                            </p>
                          )}
                        </div>
                      </button>
                    );
                  })
                )}
              </div>

              <div className="px-4 py-3 border-t border-slate-100 bg-slate-50/60">
                <p className="text-xs text-slate-400">
                  {programsForA.length} degree{programsForA.length !== 1 ? "s" : ""} shown.
                  Select one to see comparable degrees in step 2.
                </p>
              </div>
            </div>

            {/* ── Selector B ────────────────────────────────────────── */}
            <div
              className={`border rounded-xl overflow-hidden transition-opacity ${
                selectedA ? "border-slate-200 opacity-100" : "border-slate-100 opacity-50"
              }`}
            >
              <div className="bg-slate-50 border-b border-slate-200 px-4 py-3 flex items-center justify-between">
                <h2 className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                  <StepBadge n={2} active={!!selectedA} />
                  Compare with
                </h2>
                {selectedB && (
                  <button
                    onClick={() => setSelectedB(null)}
                    className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
                  >
                    Clear
                  </button>
                )}
              </div>

              <div className="divide-y divide-slate-100 max-h-80 overflow-y-auto">
                {!selectedA ? (
                  <div className="px-4 py-12 text-center">
                    <p className="text-sm text-slate-400">
                      Select a degree in step 1 first.
                    </p>
                  </div>
                ) : siblingsForB.length === 0 ? (
                  <div className="px-4 py-8 text-center">
                    <p className="text-sm text-slate-500">No comparable degrees.</p>
                    <p className="text-xs text-slate-400 mt-1">
                      No other degrees share the same school and level as this program.
                    </p>
                  </div>
                ) : (
                  <>
                    {selectedAProgram && (
                      <div className="px-4 py-2.5 bg-blue-50/50 border-b border-blue-100">
                        <p className="text-xs text-slate-500">
                          Comparing with:{" "}
                          <span className="font-medium text-blue-700">
                            {getIndexName(selectedAProgram.program_code) ??
                              selectedAProgram.canonical_name}
                          </span>
                        </p>
                      </div>
                    )}
                    {siblingsForB.map((p) => {
                      const isSelected = selectedB === p.program_code;
                      const indexName = getIndexName(p.program_code);
                      const displayName = indexName ?? p.canonical_name;
                      return (
                        <button
                          key={p.program_code}
                          onClick={() => handleSelectB(p.program_code)}
                          className={`w-full text-left px-4 py-3 flex items-start gap-3 transition-colors ${
                            isSelected
                              ? "bg-amber-50 border-l-2 border-amber-500"
                              : "hover:bg-slate-50 border-l-2 border-transparent"
                          }`}
                        >
                          <span
                            className={`font-mono text-xs px-1.5 py-0.5 rounded mt-0.5 shrink-0 ${
                              isSelected
                                ? "bg-amber-200 text-amber-800"
                                : "bg-purple-100 text-purple-700"
                            }`}
                          >
                            {p.program_code}
                          </span>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm text-slate-700 leading-snug">
                              {displayName}
                            </p>
                            {indexName ? (
                              <p className="text-xs text-slate-400 mt-0.5 truncate">
                                {p.canonical_name}
                              </p>
                            ) : (
                              <p className="text-xs text-slate-400 mt-0.5">
                                {p.school} · {classifyDegreeLevel(p)}
                              </p>
                            )}
                          </div>
                        </button>
                      );
                    })}
                  </>
                )}
              </div>

              {selectedA && siblingsForB.length > 0 && (
                <div className="px-4 py-3 border-t border-slate-100 bg-slate-50/60">
                  <p className="text-xs text-slate-400">
                    Showing degrees in the same school and level as your selection.
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Reset link */}
          {(selectedA || selectedB || schoolFilter || levelFilter) && (
            <div className="flex justify-end mb-6">
              <button
                onClick={handleReset}
                className="text-xs text-slate-400 hover:text-slate-700 underline transition-colors"
              >
                Reset all
              </button>
            </div>
          )}

          {/* Prompt: A selected, waiting for B */}
          {selectedA && !selectedB && siblingsForB.length > 0 && (
            <div className="border border-dashed border-slate-200 rounded-xl p-8 text-center mb-6">
              <p className="text-slate-400 text-sm">
                Now select a degree in step 2 to see the comparison.
              </p>
            </div>
          )}
        </>
      )}

      {/* ── Compare result ─────────────────────────────────────────────── */}
      {comparePayload && (
        <CompareView
          payload={comparePayload}
          onChangeSelection={() => setExpandedSelectors(true)}
          onReset={handleReset}
        />
      )}
    </div>
  );
}

function StepBadge({ n, active }: { n: number; active: boolean }) {
  return (
    <span
      className={`inline-flex items-center justify-center w-5 h-5 rounded-full text-xs font-bold ${
        active ? "bg-blue-600 text-white" : "bg-slate-300 text-slate-500"
      }`}
    >
      {n}
    </span>
  );
}
