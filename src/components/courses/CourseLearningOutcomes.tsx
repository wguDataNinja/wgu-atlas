import type {
  CourseGuideEnrichmentCompetencySet,
  CourseGuideEnrichmentDescription,
} from "@/lib/types";

type Props = {
  descriptions: CourseGuideEnrichmentDescription[];
  competencySets: CourseGuideEnrichmentCompetencySet[];
};

export default function CourseLearningOutcomes({
  descriptions,
  competencySets,
}: Props) {
  if (descriptions.length === 0 && competencySets.length === 0) return null;

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1 h-5 bg-blue-600 rounded" />
        <h2 className="text-lg font-bold text-slate-800">Course Learning Outcomes</h2>
      </div>

      <div className="border border-slate-200 rounded-lg bg-white p-4 space-y-4">
        {descriptions.map((desc, idx) => (
          <p key={`desc-${idx}`} className="text-sm text-slate-700 leading-relaxed">
            {desc.text}
          </p>
        ))}

        {competencySets.length > 0 && (
          <div className="space-y-3">
            {competencySets.map((set, idx) => (
              <ul key={`comp-${idx}`} className="list-disc list-inside space-y-1 text-sm text-slate-700">
                {set.bullets.map((bullet, bulletIdx) => (
                  <li key={bulletIdx}>{bullet}</li>
                ))}
              </ul>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
