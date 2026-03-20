"use client";

import { useState } from "react";

const PREVIEW_COUNT = 3;

export default function LearningOutcomes({
  outcomes,
  source,
}: {
  outcomes: string[];
  source: string | null;
}) {
  const [showAll, setShowAll] = useState(false);

  const visible = showAll ? outcomes : outcomes.slice(0, PREVIEW_COUNT);
  const remaining = outcomes.length - PREVIEW_COUNT;

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1 h-5 bg-blue-600 rounded shrink-0" />
        <h2 className="text-lg font-bold text-slate-800">Learning Outcomes</h2>
        <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
          {source}
        </span>
      </div>
      <div className="pl-3">
        <p className="text-xs text-slate-400 mb-3">
          Official WGU-authored outcomes from the catalog Program Outcomes section.
        </p>
        <ul className="space-y-2">
          {visible.map((outcome, i) => (
            <li key={i} className="flex gap-2 text-sm text-slate-700">
              <span className="text-slate-300 mt-0.5 shrink-0">•</span>
              <span>{outcome}</span>
            </li>
          ))}
        </ul>
        {outcomes.length > PREVIEW_COUNT && (
          <button
            onClick={() => setShowAll((v) => !v)}
            className="mt-3 text-xs text-blue-600 hover:text-blue-800 transition-colors"
          >
            {showAll
              ? "Show less ▴"
              : `Show ${remaining} more ▾`}
          </button>
        )}
      </div>
    </section>
  );
}
