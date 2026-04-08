import type { Metadata } from "next";
import { getPrograms, getProgramEnriched } from "@/lib/data";
import { LAB_EXCLUSIONS } from "@/lib/compareUtils";
import Compare3PrototypeLab from "@/components/proto/Compare3PrototypeLab";
import type { ProgramEnriched } from "@/lib/types";

export const metadata: Metadata = {
  title: "Compare Degrees",
  description:
    "Compare 2 or 3 WGU degree course rosters. Two-degree mode uses the current lane compare view; third degree is optional.",
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
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-800">Compare Degrees</h1>
        <p className="text-slate-500 mt-1 text-sm">
          Pick two (or three) WGU degrees from the same college to see a side-by-side course breakdown.
        </p>
      </div>
      <Compare3PrototypeLab programs={comparePrograms} enriched={compareEnriched} />
    </div>
  );
}
