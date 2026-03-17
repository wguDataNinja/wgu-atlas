import type { Metadata } from "next";
import { Suspense } from "react";
import { getPrograms, getProgramEnriched } from "@/lib/data";
import { PILOT_FAMILIES } from "@/lib/families";
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

  // Only pass enriched data for pilot family programs — avoids serializing
  // the full 114-program map as a React prop.
  const pilotCodes = new Set(PILOT_FAMILIES.flatMap((f) => f.program_codes));
  const pilotEnriched: Record<string, ProgramEnriched> = {};
  for (const code of pilotCodes) {
    if (allEnriched[code]) pilotEnriched[code] = allEnriched[code];
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Compare Degrees</h1>
        <p className="text-slate-500 mt-2 max-w-2xl">
          Select two related degrees to compare their course rosters side by side.
          Shared courses, track-specific courses, and overlap metrics are shown for
          each comparison.
        </p>
      </div>
      <Suspense>
        <CompareSelector programs={programs} pilotEnriched={pilotEnriched} />
      </Suspense>
    </div>
  );
}
