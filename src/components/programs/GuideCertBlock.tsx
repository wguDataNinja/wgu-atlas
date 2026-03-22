import type { GuideArtifact } from "@/lib/types";

type Props = {
  certSignals: GuideArtifact["cert_signals"];
};

export default function GuideCertBlock({ certSignals }: Props) {
  // Filter to only recommended signals
  const usable = certSignals.filter((s) => s.atlas_recommendation === "use");
  if (usable.length === 0) return null;

  // Deduplicate by cert name, preserving insertion order
  const seen = new Set<string>();
  const uniqueCerts: string[] = [];
  for (const signal of usable) {
    if (!seen.has(signal.normalized_cert)) {
      seen.add(signal.normalized_cert);
      uniqueCerts.push(signal.normalized_cert);
    }
  }

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1 h-5 bg-emerald-500 rounded shrink-0" />
        <h2 className="text-lg font-bold text-slate-800">Industry Certifications</h2>
      </div>
      <div className="bg-emerald-50 border border-emerald-200 rounded-lg px-4 py-3">
        <p className="text-sm text-slate-700">
          <span className="font-medium">This program includes coursework aligned with:</span>{" "}
          {uniqueCerts.map((cert, i) => (
            <span key={cert}>
              <span className="inline-block bg-white border border-emerald-300 text-emerald-800 text-xs font-medium px-2 py-0.5 rounded mx-0.5">
                {cert}
              </span>
              {i < uniqueCerts.length - 1 && " "}
            </span>
          ))}
        </p>
        <p className="text-xs text-slate-400 mt-2">
          Cert alignment is informational — preparation depends on individual coursework and study.
        </p>
      </div>
    </section>
  );
}
