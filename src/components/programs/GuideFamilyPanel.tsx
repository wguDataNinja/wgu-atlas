import Link from "next/link";
import type { GuideArtifact } from "@/lib/types";

type Props = {
  family: GuideArtifact["family"];
  currentCode: string;
};

function formatSpRelationship(relationship: string): string {
  switch (relationship) {
    case "shared_core_diverging_track":
      return "Shares a common core sequence with sibling tracks";
    case "shared_core_diverging_vendor_track":
      return "Shares a common core sequence; vendor-specific courses diverge";
    case "structural_variant":
      return "Structural variant of a related program (advisor-sequenced)";
    default:
      return relationship.replace(/_/g, " ");
  }
}

export default function GuideFamilyPanel({ family, currentCode }: Props) {
  if (!family) return null;

  const siblings = family.siblings.filter((s) => s.program_code !== currentCode);
  if (siblings.length === 0 && !family.track_label) return null;

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1 h-5 bg-violet-500 rounded shrink-0" />
        <h2 className="text-lg font-bold text-slate-800">Related Programs</h2>
      </div>
      <div className="border border-violet-200 rounded-lg bg-violet-50 px-4 py-3">
        <p className="text-sm font-medium text-slate-700 mb-1">{family.family_label}</p>
        {family.track_label && (
          <p className="text-xs text-slate-500 mb-2">
            This track:{" "}
            <span className="font-medium text-slate-700">{family.track_label}</span>
          </p>
        )}
        <p className="text-xs text-slate-500 mb-3">{formatSpRelationship(family.sp_relationship)}</p>
        {siblings.length > 0 && (
          <div>
            <p className="text-xs text-slate-400 mb-1.5">Other tracks in this family:</p>
            <div className="flex flex-wrap gap-2">
              {siblings.map((sibling) => (
                <Link
                  key={sibling.program_code}
                  href={`/programs/${sibling.program_code}`}
                  className="inline-flex items-center gap-1.5 text-xs bg-white border border-violet-300 text-violet-700 hover:bg-violet-100 px-2.5 py-1 rounded transition-colors"
                >
                  <span className="font-mono">{sibling.program_code}</span>
                  {sibling.track_label && (
                    <span className="text-slate-500">— {sibling.track_label}</span>
                  )}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
