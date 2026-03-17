import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "About",
  description: "About WGU Atlas — an independent guide to WGU degrees, courses, and schools, built from public WGU catalog sources.",
};

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold text-slate-800 mb-2">About WGU Atlas</h1>
      <p className="text-slate-500 mb-10">
        An independent guide to WGU degrees, courses, and schools.
      </p>

      <Section title="What is WGU Atlas?">
        <p>
          WGU Atlas is an independent reference built from WGU&apos;s public academic catalog. It
          is not affiliated with, endorsed by, or operated by Western Governors University.
        </p>
        <p>
          Atlas helps students explore WGU degree options, compare related degrees, and
          understand how degrees and courses have changed over time when those changes are
          relevant to what they&apos;re viewing.
        </p>
      </Section>

      <Section title="What it covers">
        <ul className="list-disc list-inside space-y-1 text-slate-600">
          <li>Current degrees across WGU&apos;s four schools</li>
          <li>Course catalog with history going back to 2017</li>
          <li>Degree comparisons for related programs (pilot set)</li>
          <li>Retired degrees still visible for reference</li>
          <li>School background and earlier names over time</li>
        </ul>
      </Section>

      <Section title="Source and independence">
        <p>
          All data is derived from WGU&apos;s publicly available course catalog, scraped and
          parsed from 108 catalog editions spanning January 2017 through March 2026. No
          internal WGU systems or private data were accessed.
        </p>
        <p>
          Atlas is a community project. It is not a substitute for official WGU advising,
          enrollment, or academic records.
        </p>
      </Section>

      <Section title="How history and resources are used">
        <p>
          Where a degree or school has changed names or structure over time, Atlas surfaces
          that history where it is relevant — for example, showing earlier names of a degree
          or a school on the relevant detail page. History is secondary context, not the
          primary lens.
        </p>
        <p>
          Official WGU resource links (program guides, outcome pages) are attached to degree
          and school pages where they have been identified and validated from public WGU web
          sources.
        </p>
      </Section>

      <div className="border-t border-slate-100 pt-8 mt-4">
        <h2 className="text-base font-semibold text-slate-700 mb-4">More detail</h2>
        <ul className="flex flex-col gap-3 text-sm">
          <li>
            <Link href="/methods" className="text-blue-600 hover:underline font-medium">
              Methods &amp; Caveats
            </Link>
            <span className="text-slate-500 ml-2">
              — how data was collected, validated, and how to interpret it correctly
            </span>
          </li>
          <li>
            <Link href="/data" className="text-blue-600 hover:underline font-medium">
              Data
            </Link>
            <span className="text-slate-500 ml-2">
              — download the canonical datasets behind Atlas
            </span>
          </li>
          <li>
            <Link href="/timeline" className="text-blue-600 hover:underline font-medium">
              Timeline
            </Link>
            <span className="text-slate-500 ml-2">
              — major WGU catalog events from 2017 to 2026
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mb-10">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1 h-5 bg-blue-600 rounded" />
        <h2 className="text-xl font-bold text-slate-800">{title}</h2>
      </div>
      <div className="space-y-3 text-slate-600 leading-relaxed text-sm">{children}</div>
    </section>
  );
}
