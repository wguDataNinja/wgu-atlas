"use client";

import { useMemo, useState } from "react";
import type { ProgramRecord, ProgramEnriched } from "@/lib/types";
import { classifyDegreeLevel, DEGREE_LEVEL_ORDER } from "@/lib/programs";
import { buildLabPayload } from "@/lib/compareUtils";
import { getIndexName } from "@/lib/families";
import CompareView from "@/components/compare/CompareView";
import Compare3View from "./Compare3View";
import { buildCompare3Model } from "./compare3ProtoUtils";

type EnrichedRoster = Record<string, Pick<ProgramEnriched, "roster">>;

export default function Compare3PrototypeLab({
  programs,
  enriched,
}: {
  programs: ProgramRecord[];
  enriched: EnrichedRoster;
}) {
  const [selectedA, setSelectedA] = useState<string | null>(null);
  const [selectedB, setSelectedB] = useState<string | null>(null);
  const [selectedC, setSelectedC] = useState<string | null>(null);

  const [college, setCollege] = useState("");
  const [level, setLevel] = useState("");
  const [search, setSearch] = useState("");
  const [expandedSelectors, setExpandedSelectors] = useState(true);
  const [compareRequested, setCompareRequested] = useState(false);
  const searchTargetStep = !selectedA ? 1 : !selectedB ? 2 : 3;

  const programMap = useMemo(() => new Map(programs.map((p) => [p.program_code, p])), [programs]);

  const availableLevels = useMemo(() => {
    const base = college ? programs.filter((p) => p.school === college) : programs;
    const levels = new Set(base.map((p) => classifyDegreeLevel(p)));
    return DEGREE_LEVEL_ORDER.filter((l) => levels.has(l));
  }, [programs, college]);

  const programsForA = useMemo(() => {
    const q = searchTargetStep === 1 ? search.toLowerCase().trim() : "";
    return programs.filter((p) => {
      if (college && p.school !== college) return false;
      if (level && classifyDegreeLevel(p) !== levelToDegree(level)) return false;
      if (q && !p.canonical_name.toLowerCase().includes(q) && !p.program_code.toLowerCase().includes(q))
        return false;
      return true;
    });
  }, [programs, college, level, search, searchTargetStep]);

  const siblingsBase = useMemo(() => {
    if (!selectedA) return [];
    const a = programMap.get(selectedA);
    if (!a) return [];
    const aLevel = classifyDegreeLevel(a);
    return programs.filter(
      (p) => p.program_code !== a.program_code && p.school === a.school && classifyDegreeLevel(p) === aLevel
    );
  }, [selectedA, programMap, programs]);

  const siblingsForB = useMemo(() => {
    const q = searchTargetStep === 2 ? search.toLowerCase().trim() : "";
    if (!q) return siblingsBase;
    return siblingsBase.filter((p) => {
      const indexName = getIndexName(p.program_code) ?? "";
      return (
        p.program_code.toLowerCase().includes(q) ||
        p.canonical_name.toLowerCase().includes(q) ||
        indexName.toLowerCase().includes(q)
      );
    });
  }, [siblingsBase, search, searchTargetStep]);

  const siblingsForC = useMemo(() => {
    if (!selectedA || !selectedB) return [];
    const base = siblingsBase.filter((p) => p.program_code !== selectedB);
    const q = searchTargetStep === 3 ? search.toLowerCase().trim() : "";
    if (!q) return base;
    return base.filter((p) => {
      const indexName = getIndexName(p.program_code) ?? "";
      return (
        p.program_code.toLowerCase().includes(q) ||
        p.canonical_name.toLowerCase().includes(q) ||
        indexName.toLowerCase().includes(q)
      );
    });
  }, [siblingsBase, selectedA, selectedB, search, searchTargetStep]);

  const payload2 = useMemo(() => {
    if (!selectedA || !selectedB || selectedC) return null;
    const a = programMap.get(selectedA);
    const b = programMap.get(selectedB);
    const ea = enriched[selectedA];
    const eb = enriched[selectedB];
    if (!a || !b || !ea || !eb) return null;
    return buildLabPayload(a, b, ea, eb);
  }, [selectedA, selectedB, selectedC, programMap, enriched]);

  const model3 = useMemo(() => {
    if (!selectedA || !selectedB || !selectedC) return null;
    const a = programMap.get(selectedA);
    const b = programMap.get(selectedB);
    const c = programMap.get(selectedC);
    const ea = enriched[selectedA];
    const eb = enriched[selectedB];
    const ec = enriched[selectedC];
    if (!a || !b || !c || !ea || !eb || !ec) return null;
    return buildCompare3Model(
      { program: a, enriched: ea, selectedIdx: 0 },
      { program: b, enriched: eb, selectedIdx: 1 },
      { program: c, enriched: ec, selectedIdx: 2 }
    );
  }, [selectedA, selectedB, selectedC, programMap, enriched]);

  const canCompare = !!(selectedA && selectedB);
  const hasFilters = !!(college || level || search || selectedA || selectedB || selectedC);
  const showFullPanels = expandedSelectors || !compareRequested;
  const compareList = useMemo(() => {
    const codes = [selectedA, selectedB, selectedC].filter((x): x is string => !!x);
    return codes
      .map((code) => getIndexName(code) ?? shortDegName(programMap.get(code)?.canonical_name ?? code))
      .join(" vs ");
  }, [selectedA, selectedB, selectedC, programMap]);

  const handleReset = () => {
    setSelectedA(null);
    setSelectedB(null);
    setSelectedC(null);
    setCollege("");
    setLevel("");
    setSearch("");
    setExpandedSelectors(true);
    setCompareRequested(false);
  };

  return (
    <div>
      {showFullPanels && (
        <div>
          <div className="mb-4 border border-slate-200 rounded-xl overflow-hidden">
            <div className="bg-slate-50 border-b border-slate-200 px-4 py-3 flex items-center justify-between">
              <span className="text-sm font-semibold text-slate-700">
                Select 2 or 3 degrees
              </span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    if (!canCompare) return;
                    setCompareRequested(true);
                    setExpandedSelectors(false);
                  }}
                  disabled={!canCompare}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold border ${
                    canCompare
                      ? "bg-blue-600 text-white border-blue-600 hover:bg-blue-700"
                      : "bg-slate-100 text-slate-400 border-slate-200 cursor-not-allowed"
                  }`}
                >
                  Compare
                </button>
                <button
                  onClick={handleReset}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold border ${
                    hasFilters
                      ? "bg-white text-slate-700 border-slate-300 hover:border-slate-400"
                      : "bg-slate-100 text-slate-400 border-slate-200"
                  }`}
                >
                  Reset
                </button>
              </div>
            </div>

            <Filters
              college={college}
              level={level}
              search={search}
              searchTargetStep={searchTargetStep}
              availableLevels={availableLevels}
              onCollege={(c) => {
                setCollege(c);
                if (level && c) {
                  const levelKey = level === "Certificate" ? "Certificates & Endorsements" : level;
                  const colHasLevel = programs.some(
                    (p) => p.school === c && classifyDegreeLevel(p) === levelKey
                  );
                  if (!colHasLevel) setLevel("");
                }
              }}
              onLevel={setLevel}
              onSearch={setSearch}
              onHardReset={() => {
                setSelectedA(null);
                setSelectedB(null);
                setSelectedC(null);
                setCompareRequested(false);
              }}
            />

            <div className="grid lg:grid-cols-3 gap-5 p-4 pt-0">
              <SelectPanel
                step={1}
                title="Choose a degree"
                options={programsForA}
                selected={selectedA}
                onSelect={(code) => {
                  const next = selectedA === code ? null : code;
                  setSelectedA(next);
                  setSelectedB(null);
                  setSelectedC(null);
                  setSearch("");
                  setCompareRequested(false);
                  setExpandedSelectors(true);
                }}
              />

              <SelectPanel
                step={2}
                title="Compare with"
                options={siblingsForB}
                selected={selectedB}
                disabled={!selectedA}
                emptyText={!selectedA ? "Select degree A first." : "No comparable degrees."}
                onSelect={(code) => {
                  const next = selectedB === code ? null : code;
                  setSelectedB(next);
                  if (!next) setSelectedC(null);
                  setSearch("");
                  setCompareRequested(false);
                  setExpandedSelectors(true);
                }}
              />

              <SelectPanel
                step={3}
                optional
                title="Add third degree"
                options={siblingsForC}
                selected={selectedC}
                disabled={!selectedA || !selectedB}
                emptyText={!selectedA || !selectedB ? "Select degree A and B first." : "No third option."}
                onSelect={(code) => {
                  setSelectedC(selectedC === code ? null : code);
                  setSearch("");
                  setCompareRequested(false);
                  setExpandedSelectors(true);
                }}
              />
            </div>
          </div>

          {selectedA && !selectedB && (
            <div className="border border-dashed border-slate-200 rounded-xl p-8 text-center mb-6">
              <p className="text-slate-400 text-sm">Now select degree B to activate compare.</p>
            </div>
          )}
        </div>
      )}

      {compareRequested && (
        <div className="mb-3 px-1 flex items-center justify-between gap-4">
          <div className="flex items-center gap-2 min-w-0">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide shrink-0">Comparing</span>
            <span className="text-sm font-semibold text-slate-800 truncate">{compareList}</span>
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <button
              onClick={() => {
                setExpandedSelectors(true);
                setCompareRequested(false);
              }}
              className="text-xs font-semibold text-blue-600 hover:text-blue-700"
            >
              Change
            </button>
            <button
              onClick={handleReset}
              className="text-xs font-semibold text-slate-500 hover:text-slate-700"
            >
              Reset
            </button>
          </div>
        </div>
      )}

      {compareRequested && payload2 && (
        <CompareView
          payload={payload2}
          onChangeSelection={() => {
            setExpandedSelectors(true);
            setCompareRequested(false);
          }}
        />
      )}

      {compareRequested && model3 && (
        <Compare3View
          model={model3}
          onChangeSelection={() => {
            setExpandedSelectors(true);
            setCompareRequested(false);
          }}
        />
      )}
    </div>
  );
}

function shortDegName(canonical: string): string {
  return canonical
    .replace(/^Bachelor of Science[, ]+/i, "")
    .replace(/^Bachelor of Arts[, ]+/i, "")
    .replace(/^Master of Science[, ]+/i, "M.S. ")
    .replace(/^Master of Business Administration[, ]*/i, "MBA ")
    .replace(/^Master of Arts[, ]+/i, "M.A. ")
    .trim();
}

function levelToDegree(level: string) {
  if (level === "Certificate") return "Certificates & Endorsements";
  return level;
}

function Filters({
  college,
  level,
  search,
  searchTargetStep,
  availableLevels,
  onCollege,
  onLevel,
  onSearch,
  onHardReset,
}: {
  college: string;
  level: string;
  search: string;
  searchTargetStep: number;
  availableLevels: string[];
  onCollege: (x: string) => void;
  onLevel: (x: string) => void;
  onSearch: (x: string) => void;
  onHardReset: () => void;
}) {
  const colleges = [
    "School of Business",
    "Leavitt School of Health",
    "School of Technology",
    "School of Education",
  ];
  const levels = ["Bachelor's", "Master's", "Certificate"];

  return (
    <div className="p-4 bg-slate-50 border-y border-slate-100 mb-4">
      <div className="flex items-center gap-2 flex-wrap mb-3">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide w-16 shrink-0">College</span>
        {colleges.map((c) => {
          const selected = college === c;
          return (
            <button
              key={c}
              onClick={() => {
                onCollege(selected ? "" : c);
                onHardReset();
              }}
              className={`px-3 py-1.5 rounded-lg text-sm border ${
                selected ? "bg-slate-700 border-slate-700 text-white" : "bg-white border-slate-300 text-slate-600"
              }`}
            >
              {c.replace("School of ", "").replace("Leavitt School of ", "")}
            </button>
          );
        })}
      </div>
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide w-16 shrink-0">Level</span>
        {levels.map((lv) => {
          const key = lv === "Certificate" ? "Certificates & Endorsements" : lv;
          if (college && !availableLevels.includes(key)) return null;
          return (
            <button
              key={lv}
              onClick={() => {
                onLevel(level === lv ? "" : lv);
                onHardReset();
              }}
              className={`px-3 py-1.5 rounded-lg text-sm border ${
                level === lv ? "bg-slate-700 border-slate-700 text-white" : "bg-white border-slate-300 text-slate-600"
              }`}
            >
              {lv}
            </button>
          );
        })}
        <div className="flex-1 min-w-40">
          <input
            type="text"
            placeholder={`Search step ${searchTargetStep} options…`}
            value={search}
            onChange={(e) => {
              onSearch(e.target.value);
            }}
            className="w-full border border-slate-300 rounded-lg px-3 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
    </div>
  );
}

function SelectPanel({
  step,
  title,
  options,
  selected,
  disabled,
  optional,
  emptyText,
  onSelect,
}: {
  step: number;
  title: string;
  options: ProgramRecord[];
  selected: string | null;
  disabled?: boolean;
  optional?: boolean;
  emptyText?: string;
  onSelect: (code: string) => void;
}) {
  return (
    <div className={`border rounded-xl overflow-hidden ${disabled ? "opacity-60 border-slate-100" : "border-slate-200"}`}>
      <div className="bg-slate-50 border-b border-slate-200 px-4 py-3">
        <h2 className="text-sm font-semibold text-slate-700 flex items-center gap-2">
          <StepBadge n={step} active={!disabled} />
          {title}
          {optional && <span className="text-xs text-slate-400 font-normal">(optional)</span>}
        </h2>
      </div>
      <div className="divide-y divide-slate-100 max-h-[420px] overflow-y-auto">
        {disabled ? (
          <p className="px-4 py-8 text-center text-sm text-slate-400">{emptyText ?? "Unavailable"}</p>
        ) : options.length === 0 ? (
          <p className="px-4 py-8 text-center text-sm text-slate-400">{emptyText ?? "No options."}</p>
        ) : (
          options.map((p) => {
            const isSelected = selected === p.program_code;
            const indexName = getIndexName(p.program_code);
            const displayName = indexName ?? p.canonical_name;
            return (
              <button
                key={p.program_code}
                onClick={() => onSelect(p.program_code)}
                className={`w-full text-left px-4 py-3 flex items-start gap-3 transition-colors ${
                  isSelected ? "bg-blue-50 border-l-2 border-blue-500" : "hover:bg-slate-50 border-l-2 border-transparent"
                }`}
              >
                <span className={`font-mono text-xs px-1.5 py-0.5 rounded mt-0.5 shrink-0 ${isSelected ? "bg-blue-200 text-blue-800" : "bg-purple-100 text-purple-700"}`}>
                  {p.program_code}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-slate-700 leading-snug">{displayName}</p>
                  <p className="text-xs text-slate-400 mt-0.5 truncate">
                    {indexName ? p.canonical_name : `${p.school} · ${classifyDegreeLevel(p)}`}
                  </p>
                </div>
              </button>
            );
          })
        )}
      </div>
    </div>
  );
}

function StepBadge({ n, active }: { n: number; active?: boolean }) {
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
