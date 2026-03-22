import type { GuideArtifact } from "@/lib/types";

type Props = {
  capstone: GuideArtifact["capstone"];
};

export default function GuideCapstone({ capstone }: Props) {
  if (!capstone || !capstone.present) return null;

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1 h-5 bg-amber-500 rounded shrink-0" />
        <h2 className="text-lg font-bold text-slate-800">Capstone</h2>
      </div>
      <div className="border border-amber-200 bg-amber-50 rounded-lg px-4 py-3">
        <p className="text-sm font-semibold text-slate-800 mb-1">{capstone.title}</p>
        {capstone.partial && (
          <p className="text-xs text-amber-700 mb-2">
            Part of a multi-course capstone sequence.
          </p>
        )}
        {capstone.description && (
          <p className="text-sm text-slate-600 leading-relaxed">{capstone.description}</p>
        )}
        {capstone.competency_available && capstone.competency_bullets.length > 0 && (
          <ul className="mt-2 space-y-1">
            {capstone.competency_bullets.slice(0, 4).map((bullet, i) => (
              <li key={i} className="flex gap-2 text-xs text-slate-600">
                <span className="text-amber-400 shrink-0 mt-0.5">•</span>
                <span>{bullet}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
