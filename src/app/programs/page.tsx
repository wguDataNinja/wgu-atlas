import type { Metadata } from "next";
import { Suspense } from "react";
import { getPrograms } from "@/lib/data";
import ProgramExplorer from "@/components/programs/ProgramExplorer";

export const metadata: Metadata = {
  title: "Degrees",
  description: "Browse WGU degrees — view course rosters, compare related degrees, and see current or retired status for each.",
};

export default function ProgramsPage() {
  const programs = getPrograms();
  const activeCount = programs.filter((p) => p.status === "ACTIVE").length;
  const retiredCount = programs.filter((p) => p.status === "RETIRED").length;

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-800">Degrees</h1>
        <p className="text-slate-500 mt-1">
          {programs.length} WGU degrees — {activeCount} current, {retiredCount} retired.
        </p>
      </div>
      <Suspense>
        <ProgramExplorer programs={programs} />
      </Suspense>
    </div>
  );
}
