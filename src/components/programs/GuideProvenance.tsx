import type { GuideArtifact } from "@/lib/types";

type Props = {
  provenance: GuideArtifact["guide_provenance"];
  quality: GuideArtifact["quality"];
  anomalyFlags: string[];
  suppressCaveatPill?: boolean;
};

export default function GuideProvenance({ provenance, quality, anomalyFlags, suppressCaveatPill }: Props) {
  const hasCaveats =
    quality.caveat_messages_ui.length > 0 || anomalyFlags.length > 0;

  const versionLabel = provenance.source_version
    ? `v${provenance.source_version}`
    : null;
  const dateLabel = provenance.source_pub_date ?? null;

  return (
    <div className="mt-1 flex flex-wrap items-center gap-2">
      <span className="inline-flex items-center gap-1.5 text-xs text-slate-400 bg-slate-50 border border-slate-200 px-2 py-0.5 rounded">
        <span>Source: WGU Program Guide</span>
        {versionLabel && (
          <span className="text-slate-300">·</span>
        )}
        {versionLabel && (
          <span>{versionLabel}</span>
        )}
        {dateLabel && (
          <>
            <span className="text-slate-300">·</span>
            <span>{dateLabel}</span>
          </>
        )}
        {provenance.confidence === "medium" && (
          <>
            <span className="text-slate-300">·</span>
            <span className="text-amber-600">medium confidence</span>
          </>
        )}
        {provenance.confidence === "low" && (
          <>
            <span className="text-slate-300">·</span>
            <span className="text-red-600">low confidence</span>
          </>
        )}
      </span>
      {hasCaveats && !suppressCaveatPill && (
        <span className="inline-flex items-center gap-1 text-xs text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">
          <span>⚠</span>
          <span>
            {quality.caveat_messages_ui.length > 0
              ? quality.caveat_messages_ui[0]
              : "Guide data has caveats — see source guide for accuracy."}
          </span>
        </span>
      )}
    </div>
  );
}
