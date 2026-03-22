import type { Metadata } from "next";
import Link from "next/link";
import { DEGREE_COHORT_CODES, DEGREE_COHORT_META } from "@/lib/degreePreviewData";
import { getProgramDetail } from "@/lib/data";

export const metadata: Metadata = {
  title: "Degree-Page Review — Prototype Cohort",
  description: "Session 1 prototype: degree-page review surface for the 7-program design cohort.",
};

export default function DegreePreviewIndexPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      {/* Lab banner */}
      <div className="mb-8 pb-6 border-b border-slate-200">
        <div className="inline-block bg-amber-100 text-amber-800 text-xs font-mono px-2 py-1 rounded mb-3">
          PROTOTYPE LAB — NOT PRODUCTION UI
        </div>
        <h1 className="text-3xl font-bold text-slate-800">
          Degree-Page Review — Design Cohort
        </h1>
        <p className="text-slate-500 mt-2 max-w-2xl">
          Session 1 cohort review. Seven programs covering the full range of live degree-page
          shapes: plain baseline, family/track, cert-bearing, advisor-guided, suppressed roster,
          capstone, and caveat/confidence edge cases. Each page renders identically to production.
          Nothing here is a redesign.
        </p>
        <p className="text-xs text-slate-400 mt-2">
          Production degree pages are at{" "}
          <Link href="/programs" className="text-blue-500 hover:underline">
            /programs
          </Link>
          . This surface is at <span className="font-mono">/proto/degree-preview</span>.
        </p>
      </div>

      {/* Cohort table */}
      <div className="border border-slate-200 rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-4 py-2.5 font-semibold text-slate-600 w-24">Code</th>
              <th className="text-left px-4 py-2.5 font-semibold text-slate-600">Degree</th>
              <th className="text-left px-4 py-2.5 font-semibold text-slate-600 hidden md:table-cell">Shape</th>
            </tr>
          </thead>
          <tbody>
            {DEGREE_COHORT_CODES.map((code) => {
              const meta = DEGREE_COHORT_META[code];
              const program = getProgramDetail(code);
              return (
                <tr key={code} className="border-b border-slate-100 last:border-0 hover:bg-slate-50">
                  <td className="px-4 py-3">
                    <Link
                      href={`/proto/degree-preview/${code}`}
                      className="font-mono text-blue-700 hover:underline font-semibold"
                    >
                      {code}
                    </Link>
                  </td>
                  <td className="px-4 py-3">
                    <Link
                      href={`/proto/degree-preview/${code}`}
                      className="text-slate-800 hover:text-blue-700 hover:underline"
                    >
                      {program?.canonical_name ?? code}
                    </Link>
                    <div className="text-xs text-slate-400 mt-0.5 md:hidden">{meta.shape}</div>
                  </td>
                  <td className="px-4 py-3 hidden md:table-cell">
                    <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">
                      {meta.shape}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Shape notes */}
      <div className="mt-8">
        <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3">
          Shape Notes
        </h2>
        <div className="flex flex-col gap-2">
          {DEGREE_COHORT_CODES.map((code) => {
            const meta = DEGREE_COHORT_META[code];
            return (
              <div key={code} className="text-xs text-slate-500">
                <span className="font-mono font-semibold text-slate-600">{code}</span>
                {" — "}
                <span className="font-medium text-slate-700">{meta.shape}:</span>{" "}
                {meta.shapeNote}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
