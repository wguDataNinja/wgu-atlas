import type { Metadata } from "next";
import { Suspense } from "react";
import { getPrograms, getProgramEnriched } from "@/lib/data";
import { LAB_EXCLUSIONS } from "@/lib/compareUtils";
import CompareSelector from "@/components/compare/CompareSelector";
import type { ProgramEnriched } from "@/lib/types";

export const metadata: Metadata = {
  title: "Compare Degrees",
  description:
    "Compare WGU degree course rosters side by side. See shared courses, track-specific courses, and overlap metrics.",
};

export default function ComparePage() {
  const programs = getPrograms();
  const allEnriched = getProgramEnriched();

  // Broadened universe: active programs with non-empty rosters, minus exclusions.
  // No longer gated to pilot families — any same-college + same-level pair is valid.
  const comparePrograms = programs.filter(
    (p) =>
      p.status === "ACTIVE" &&
      !LAB_EXCLUSIONS.has(p.program_code) &&
      (allEnriched[p.program_code]?.roster?.length ?? 0) > 0
  );

  // Lean enriched: only roster data (avoids serializing the full enriched map).
  const compareEnriched: Record<string, Pick<ProgramEnriched, "roster">> = {};
  for (const p of comparePrograms) {
    const e = allEnriched[p.program_code];
    if (e) compareEnriched[p.program_code] = { roster: e.roster };
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Compare Degrees</h1>
        <p className="text-slate-500 mt-2 max-w-2xl">
          Select two degrees to compare their course rosters side by side.
          Shared courses, unique courses, and overlap metrics are shown for each
          comparison.
        </p>
      </div>
      <Suspense>
        <CompareSelector programs={comparePrograms} enriched={compareEnriched} />
      </Suspense>
    </div>
  );
}
