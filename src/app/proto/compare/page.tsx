import type { Metadata } from "next";
import { getPrograms, getProgramEnriched } from "@/lib/data";
import { LAB_EXCLUSIONS } from "@/components/proto/compareProtoUtils";
import ComparePrototypeLab from "@/components/proto/ComparePrototypeLab";

export const metadata: Metadata = {
  title: "Compare Degrees — Prototype Lab",
  description:
    "Prototype lab: three compare layout variants stacked for side-by-side inspection. Broadened universe beyond pilot families.",
};

export default function CompareProtoPage() {
  const programs = getPrograms();
  const allEnriched = getProgramEnriched();

  // Lab universe: active programs, has a non-empty roster, not in exclusion list.
  // Broader than production PILOT_FAMILIES gate — any same-college+level pair is valid here.
  const labPrograms = programs.filter(
    (p) =>
      p.status === "ACTIVE" &&
      !LAB_EXCLUSIONS.has(p.program_code) &&
      (allEnriched[p.program_code]?.roster?.length ?? 0) > 0
  );

  // Only serialize enriched data for lab universe programs (not the full 114-program map).
  const labEnriched: Record<string, ReturnType<typeof getProgramEnriched>[string]> = {};
  for (const p of labPrograms) {
    if (allEnriched[p.program_code]) labEnriched[p.program_code] = allEnriched[p.program_code];
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="mb-8 pb-6 border-b border-slate-200">
        <div className="inline-block bg-amber-100 text-amber-800 text-xs font-mono px-2 py-1 rounded mb-3">
          PROTOTYPE LAB — NOT PRODUCTION UI
        </div>
        <h1 className="text-3xl font-bold text-slate-800">
          Compare Degrees — Prototype Variants
        </h1>
        <p className="text-slate-500 mt-2 max-w-2xl">
          Three compare layout approaches stacked vertically. Select a pair once — all three
          prototypes update. Lab universe:{" "}
          <strong className="text-slate-700">{labPrograms.length} active degrees</strong> across 4
          colleges (same-college + same-level pairs). Excludes 6 programs with known
          disambiguation blockers.
        </p>
      </div>
      <ComparePrototypeLab programs={labPrograms} enriched={labEnriched} />
    </div>
  );
}
