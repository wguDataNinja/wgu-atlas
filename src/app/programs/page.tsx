import type { Metadata } from "next";
import { Suspense } from "react";
import { getPrograms } from "@/lib/data";
import ProgramExplorer from "@/components/programs/ProgramExplorer";

export const metadata: Metadata = {
  title: "Programs",
  description: "Browse all 196 WGU degree programs — active and deprecated — with version history and school lineage.",
};

export default function ProgramsPage() {
  const programs = getPrograms();
  const activeCount = programs.filter((p) => p.status === "ACTIVE").length;
  const retiredCount = programs.filter((p) => p.status === "RETIRED").length;

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-800">Programs</h1>
        <p className="text-slate-500 mt-1">
          {programs.length} programs tracked across the WGU catalog archive —{" "}
          {activeCount} current, {retiredCount} deprecated.
        </p>
      </div>
      <Suspense>
        <ProgramExplorer programs={programs} />
      </Suspense>
    </div>
  );
}
