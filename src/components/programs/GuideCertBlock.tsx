import Link from "next/link";
import type { GuideArtifact } from "@/lib/types";

type Props = {
  certSignals: GuideArtifact["cert_signals"];
};

export default function GuideCertBlock({ certSignals }: Props) {
  const usable = certSignals.filter(
    (s) => s.atlas_recommendation === "use" || s.atlas_recommendation === "degree-only"
  );
  if (usable.length === 0) return null;

  // Group by cert name, collecting all course links per cert.
  const byCert = new Map<string, { code: string | null; title: string | null; degreeOnly: boolean }[]>();
  for (const signal of usable) {
    if (!byCert.has(signal.normalized_cert)) byCert.set(signal.normalized_cert, []);
    byCert.get(signal.normalized_cert)!.push({
      code: signal.via_course_code,
      title: signal.via_course_title,
      degreeOnly: signal.atlas_recommendation === "degree-only",
    });
  }

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1 h-5 bg-emerald-500 rounded shrink-0" />
        <h2 className="text-lg font-bold text-slate-800">Industry Certifications</h2>
      </div>
      <div className="bg-emerald-50 border border-emerald-200 rounded-lg px-4 py-3">
        <p className="text-sm font-medium text-slate-700 mb-2">
          This program includes coursework aligned with:
        </p>
        <ul className="space-y-1.5">
          {Array.from(byCert.entries()).map(([cert, courses]) => (
            <li key={cert} className="flex items-baseline gap-2 flex-wrap">
              <span className="inline-block bg-white border border-emerald-300 text-emerald-800 text-xs font-semibold px-2 py-0.5 rounded shrink-0">
                {cert}
              </span>
              {courses.every((c) => c.degreeOnly) ? (
                <span className="text-xs text-slate-500">Degree-level preparation</span>
              ) : (
                <span className="text-xs text-slate-500">
                  via{" "}
                  {courses
                    .filter((c) => !c.degreeOnly)
                    .map((c, i, arr) => (
                      <span key={c.title ?? i}>
                        {c.code ? (
                          <Link
                            href={`/courses/${c.code}`}
                            className="text-blue-600 hover:underline"
                          >
                            {c.title}
                          </Link>
                        ) : (
                          c.title
                        )}
                        {i < arr.length - 1 && ", "}
                      </span>
                    ))}
                </span>
              )}
            </li>
          ))}
        </ul>
        <p className="text-xs text-slate-400 mt-2">
          Cert alignment is informational — preparation depends on individual coursework and study.
        </p>
      </div>
    </section>
  );
}
