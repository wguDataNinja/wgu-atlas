import type { Metadata } from "next";
import { getHomepageSummary } from "@/lib/data";
import { BASE_PATH } from "@/lib/basePath";

export const metadata: Metadata = {
  title: "Data",
  description: "Download WGU Atlas canonical datasets — course history, named events, title variant classification.",
};

// Files in public/data/downloads/ — served as static assets
const DATASETS = [
  {
    file: "canonical_courses.csv",
    label: "Canonical Course Table",
    description:
      "1,646-row table covering all course codes ever seen in the archive. Includes active/retired status, title variant classification, stability class, program counts, and confidence notes.",
    format: "CSV",
    rows: "1,646",
    path: "/data/downloads/canonical_courses.csv",
  },
  {
    file: "named_events.csv",
    label: "Named Catalog Events",
    description:
      "41 named events (all threshold-crossing transitions). Includes event type, severity score, affected schools/programs/courses, observed and interpreted summaries, confidence, and curated-event flag.",
    format: "CSV",
    rows: "41",
    path: "/data/downloads/named_events.csv",
  },
  {
    file: "title_variant_classification.csv",
    label: "Title Variant Classification",
    description:
      "167 course codes with title variation across editions, each classified by variant type: extraction noise, punctuation only, wording refinement, substantive change, or formatting only.",
    format: "CSV",
    rows: "167",
    path: "/data/downloads/title_variant_classification.csv",
  },
];

// Files in public/data/ — the same files used by the frontend
const JSON_EXPORTS = [
  {
    file: "courses.json",
    label: "Course Cards (full list)",
    description: "1,646 course cards with code, title, status, scope, school, edition count, stability class, and flags. Used by the course explorer.",
    size: "712 KB",
    path: "/data/courses.json",
  },
  {
    file: "events.json",
    label: "Events (full)",
    description: "41 events in full JSON form with all fields including course/program sample lists.",
    size: "48 KB",
    path: "/data/events.json",
  },
  {
    file: "search_index.json",
    label: "Search Index",
    description: "1,842-entry search index covering all courses and programs, with alt_titles for search matching.",
    size: "392 KB",
    path: "/data/search_index.json",
  },
];

export default function DataPage() {
  const summary = getHomepageSummary();

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold text-slate-800 mb-2">Data</h1>
      <p className="text-slate-500 mb-2">
        Download the canonical datasets behind WGU Atlas. All files reflect the{" "}
        <strong>{summary.data_date}</strong> catalog baseline.
      </p>
      <p className="text-sm text-slate-400 mb-10">
        Archive span: {summary.archive_span} · {summary.total_editions} editions ·{" "}
        {summary.total_course_codes_ever.toLocaleString()} total course codes ever seen
      </p>

      {/* Canonical CSV downloads */}
      <section className="mb-12">
        <h2 className="text-xl font-bold text-slate-800 mb-4">Canonical Datasets (CSV)</h2>
        <div className="flex flex-col gap-4">
          {DATASETS.map((ds) => (
            <div
              key={ds.file}
              className="border border-slate-200 rounded-lg p-5 flex flex-col md:flex-row md:items-start gap-4"
            >
              <div className="flex-1">
                <h3 className="font-semibold text-slate-800">{ds.label}</h3>
                <p className="text-sm text-slate-500 mt-1">{ds.description}</p>
                <div className="flex gap-3 mt-2 text-xs text-slate-400">
                  <span className="bg-slate-100 px-2 py-0.5 rounded">{ds.format}</span>
                  <span>{ds.rows} rows</span>
                </div>
              </div>
              <a
                href={`${BASE_PATH}${ds.path}`}
                download
                className="shrink-0 bg-blue-600 text-white text-sm px-4 py-2 rounded hover:bg-blue-700 transition-colors text-center"
              >
                Download
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* JSON exports */}
      <section className="mb-12">
        <h2 className="text-xl font-bold text-slate-800 mb-4">Site-Ready JSON Exports</h2>
        <p className="text-sm text-slate-500 mb-4">
          The same JSON files that power the WGU Atlas frontend. Provided for transparency
          and for developers who want to build on the data.
        </p>
        <div className="flex flex-col gap-3">
          {JSON_EXPORTS.map((ex) => (
            <div
              key={ex.file}
              className="border border-slate-200 rounded-lg px-5 py-4 flex flex-col md:flex-row md:items-start gap-3"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-slate-800 text-sm">{ex.label}</h3>
                  <span className="text-xs text-slate-400 font-mono bg-slate-100 px-1.5 py-0.5 rounded">
                    {ex.file}
                  </span>
                  <span className="text-xs text-slate-400">{ex.size}</span>
                </div>
                <p className="text-sm text-slate-500 mt-1">{ex.description}</p>
              </div>
              <a
                href={`${BASE_PATH}${ex.path}`}
                download
                className="shrink-0 border border-slate-300 text-slate-600 text-sm px-4 py-1.5 rounded hover:bg-slate-50 transition-colors text-center"
              >
                Download
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* Schema notes */}
      <section className="border-t border-slate-100 pt-8">
        <h2 className="text-xl font-bold text-slate-800 mb-4">Schema Notes</h2>
        <div className="text-sm text-slate-600 space-y-3">
          <p>
            <strong>stability_class</strong> — Classifies a course by its persistence across
            editions: <code className="bg-slate-100 px-1 rounded">perpetual</code> (all 108 editions),{" "}
            <code className="bg-slate-100 px-1 rounded">stable</code>,{" "}
            <code className="bg-slate-100 px-1 rounded">moderate</code>,{" "}
            <code className="bg-slate-100 px-1 rounded">ephemeral</code>,{" "}
            <code className="bg-slate-100 px-1 rounded">single</code> (1 edition),{" "}
            <code className="bg-slate-100 px-1 rounded">cert_only</code>.
          </p>
          <p>
            <strong>ghost_flag</strong> — True for retired AP courses with ≤2 catalog appearances.
            These may represent data anomalies or genuinely short-lived entries.
          </p>
          <p>
            <strong>title_variant_class</strong> — Classification of title variation across editions.
            <code className="bg-slate-100 px-1 rounded ml-1">extraction_noise</code> accounts for 87%
            of apparent title variation and does not represent intentional renames.
          </p>
          <p>
            <strong>programs_timeline</strong> (in individual course JSON files) — Lists programs
            by raw degree heading text, not by program code. Minor wording variations across editions
            may exist.
          </p>
          <p className="text-slate-400 text-xs mt-4">
            Full field definitions are in{" "}
            <code className="bg-slate-100 px-1 rounded">docs/README_INTERNAL.md</code>{" "}
            in the GitHub repository.
          </p>
        </div>
      </section>
    </div>
  );
}
