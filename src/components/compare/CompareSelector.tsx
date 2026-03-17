"use client";

import { useState, useMemo } from "react";
import type { ProgramRecord, ProgramEnriched } from "@/lib/types";
import {
  PILOT_FAMILIES,
  getFamilyByCode,
  getSiblingCodes,
  areProgramsComparable,
  buildComparePayload,
  getIndexName,
} from "@/lib/families";
import { classifyDegreeLevel, DEGREE_LEVEL_ORDER } from "@/lib/programs";
import CompareView from "./CompareView";

const PILOT_CODES = new Set(PILOT_FAMILIES.flatMap((f) => f.program_codes));

export default function CompareSelector({
  programs,
  pilotEnriched,
}: {
  programs: ProgramRecord[];
  pilotEnriched: Record<string, ProgramEnriched>;
}) {
  const [selectedA, setSelectedA] = useState<string | null>(null);
  const [selectedB, setSelectedB] = useState<string | null>(null);
  const [schoolFilter, setSchoolFilter] = useState("");
  const [levelFilter, setLevelFilter] = useState("");
  // When both programs are selected, selectors collapse to a compact bar.
  const [expandedSelectors, setExpandedSelectors] = useState(true);

  // Programs eligible for compare (in pilot families, ACTIVE)
  const eligiblePrograms = useMemo(
    () =>
      programs.filter(
        (p) => p.status === "ACTIVE" && PILOT_CODES.has(p.program_code)
      ),
    [programs]
  );

  // Schools available from eligible programs
  const schools = useMemo(
    () => [...new Set(eligiblePrograms.map((p) => p.school))].sort(),
    [eligiblePrograms]
  );

  // Degree levels available, restricted to the selected school
  const availableLevels = useMemo(() => {
    const base = schoolFilter
      ? eligiblePrograms.filter((p) => p.school === schoolFilter)
      : eligiblePrograms;
    const levels = new Set(base.map((p) => classifyDegreeLevel(p)));
    return DEGREE_LEVEL_ORDER.filter((l) => levels.has(l));
  }, [eligiblePrograms, schoolFilter]);

  // Programs shown in selector A (filtered by school + level)
  const programsForA = useMemo(() => {
    return eligiblePrograms.filter((p) => {
      if (schoolFilter && p.school !== schoolFilter) return false;
      if (levelFilter && classifyDegreeLevel(p) !== levelFilter) return false;
      return true;
    });
  }, [eligiblePrograms, schoolFilter, levelFilter]);

  // Sibling options for selector B (based on selected A)
  const siblingsForB = useMemo(() => {
    if (!selectedA) return [];
    return getSiblingCodes(selectedA)
      .map((code) => programs.find((p) => p.program_code === code))
      .filter((p): p is ProgramRecord => p != null && p.status === "ACTIVE");
  }, [selectedA, programs]);

  // Build compare payload when both are selected
  const comparePayload = useMemo(() => {
    if (!selectedA || !selectedB) return null;
    if (!areProgramsComparable(selectedA, selectedB)) return null;
    const leftProgram = programs.find((p) => p.program_code === selectedA);
    const rightProgram = programs.find((p) => p.program_code === selectedB);
    const leftEnriched = pilotEnriched[selectedA];
    const rightEnriched = pilotEnriched[selectedB];
    const family = getFamilyByCode(selectedA);
    if (!leftProgram || !rightProgram || !leftEnriched || !rightEnriched || !family)
      return null;
    return buildComparePayload(
      family,
      leftProgram,
      rightProgram,
      leftEnriched,
      rightEnriched
    );
  }, [selectedA, selectedB, programs, pilotEnriched]);

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

  // Compact bar: shown when both selected and selectors are collapsed
  const showCompactBar = bothSelected && !expandedSelectors;
  // Show full selector panels when expanded (or when only one selected)
  const showFullPanels = expandedSelectors || !bothSelected;

  return (
    <div>
      {/* ── Compact selection bar (both selected, collapsed state) ─────── */}
      {showCompactBar && selectedAProgram && selectedBProgram && (
        <div className="flex items-center gap-3 mb-5 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl">
          <div className="flex items-center gap-2 flex-1 min-w-0 flex-wrap">
            <span className="font-mono text-xs bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded shrink-0">
              {selectedA}
            </span>
            <span className="text-sm text-slate-700 truncate">
              {getIndexName(selectedA!) ?? selectedAProgram.canonical_name}
            </span>
            <span className="text-slate-400 text-xs shrink-0">vs</span>
            <span className="font-mono text-xs bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded shrink-0">
              {selectedB}
            </span>
            <span className="text-sm text-slate-700 truncate">
              {getIndexName(selectedB!) ?? selectedBProgram.canonical_name}
            </span>
          </div>
          <button
            onClick={() => setExpandedSelectors(true)}
            className="text-xs text-blue-600 hover:text-blue-800 underline shrink-0 transition-colors"
          >
            Change
          </button>
          <button
            onClick={handleReset}
            className="text-xs text-slate-400 hover:text-slate-600 underline shrink-0 transition-colors"
          >
            Reset
          </button>
        </div>
      )}

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
                    onClick={() => { setSelectedA(null); setSelectedB(null); }}
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
                    <option key={s} value={s}>{s}</option>
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
                    <option key={l} value={l}>{l}</option>
                  ))}
                </select>
              </div>

              {/* Program list for A */}
              <div className="divide-y divide-slate-100">
                {programsForA.length === 0 ? (
                  <p className="px-4 py-8 text-center text-sm text-slate-400">
                    No degrees match these filters.
                  </p>
                ) : (
                  programsForA.map((p) => {
                    const family = getFamilyByCode(p.program_code);
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
                          {indexName && (
                            <p className="text-xs text-slate-400 mt-0.5 truncate">
                              {p.canonical_name}
                            </p>
                          )}
                          {family && !indexName && (
                            <p className="text-xs text-slate-400 mt-0.5">
                              {family.label} · {classifyDegreeLevel(p)}
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
                  Only degrees with comparable track variants are shown.
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

              <div className="divide-y divide-slate-100">
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
                      This program has no track variants in the comparison set.
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
                            {indexName && (
                              <p className="text-xs text-slate-400 mt-0.5 truncate">
                                {p.canonical_name}
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
                    Showing only degrees in the same family as your selection.
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
      {comparePayload && selectedAProgram && selectedBProgram && (
        <CompareView
          payload={comparePayload}
          leftProgram={selectedAProgram}
          rightProgram={selectedBProgram}
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
