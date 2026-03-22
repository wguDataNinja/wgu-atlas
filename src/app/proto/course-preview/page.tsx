import type { Metadata } from "next";
import Link from "next/link";
import { COHORT_CODES, COHORT_META } from "@/lib/coursePreviewData";
import { getCourseDetail } from "@/lib/data";

export const metadata: Metadata = {
  title: "Course-Page Enrichment — Prototype Cohort",
  description: "Session 2 prototype: enriched course-page preview for the 10-course design cohort.",
};

export default function CoursePreviewIndexPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      {/* Lab banner */}
      <div className="mb-8 pb-6 border-b border-slate-200">
        <div className="inline-block bg-amber-100 text-amber-800 text-xs font-mono px-2 py-1 rounded mb-3">
          PROTOTYPE LAB — NOT PRODUCTION UI
        </div>
        <h1 className="text-3xl font-bold text-slate-800">
          Course-Page Enrichment — Design Cohort Preview
        </h1>
        <p className="text-slate-500 mt-2 max-w-2xl">
          Session 2 prototype. Ten representative courses covering the full range of enrichment
          shapes: stable, multi-variant, cert-bearing, prereq-bearing, capstone, cumulative-sequence,
          and sparse/no-payload. Each page shows a best-guess first-pass enriched layout using
          guide-derived data. Nothing here is production.
        </p>
        <p className="text-xs text-slate-400 mt-2">
          Production course pages are at{" "}
          <Link href="/courses" className="text-blue-500 hover:underline">
            /courses
          </Link>
          . This surface is at <span className="font-mono">/proto/course-preview</span>.
        </p>
      </div>

      {/* Cohort table */}
      <div className="border border-slate-200 rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-4 py-2.5 font-semibold text-slate-600 w-20">Code</th>
              <th className="text-left px-4 py-2.5 font-semibold text-slate-600">Title</th>
              <th className="text-left px-4 py-2.5 font-semibold text-slate-600 hidden md:table-cell">Shape</th>
            </tr>
          </thead>
          <tbody>
            {COHORT_CODES.map((code) => {
              const meta = COHORT_META[code];
              const detail = getCourseDetail(code);
              return (
                <tr key={code} className="border-b border-slate-100 last:border-0 hover:bg-slate-50">
                  <td className="px-4 py-3">
                    <Link
                      href={`/proto/course-preview/${code}`}
                      className="font-mono text-blue-700 hover:underline font-semibold"
                    >
                      {code}
                    </Link>
                  </td>
                  <td className="px-4 py-3">
                    <Link
                      href={`/proto/course-preview/${code}`}
                      className="text-slate-800 hover:text-blue-700 hover:underline"
                    >
                      {detail?.canonical_title_current ?? code}
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

      {/* Shape legend */}
      <div className="mt-8">
        <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3">
          Shape Notes
        </h2>
        <div className="flex flex-col gap-2">
          {COHORT_CODES.map((code) => {
            const meta = COHORT_META[code];
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
