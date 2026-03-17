import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "About",
  description: "About WGU Atlas — an independent guide to WGU degree programs and courses, built from public WGU sources.",
};

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold text-slate-800 mb-2">About WGU Atlas</h1>
      <p className="text-slate-500 mb-10">
        An independent guide to WGU degree programs and courses.
      </p>

      <Section title="What is WGU Atlas?">
        <p>
          WGU Atlas is an independent guide built from WGU&apos;s public catalog and other
          public WGU sources. It is not affiliated with or operated by WGU.
        </p>
        <p>
          The site is meant to help students understand WGU degree options, explore
          courses, compare related degrees, and find useful context in one place.
        </p>
      </Section>

      <Section title="What it covers">
        <ul className="list-disc list-inside space-y-1 text-slate-600">
          <li>Current WGU degrees across all four schools</li>
          <li>A course catalog with historical coverage back to 2017</li>
          <li>Degree comparisons for related degrees</li>
          <li>Retired degrees that are still useful for reference</li>
          <li>School background and earlier names where relevant</li>
        </ul>
      </Section>

      <Section title="Source and independence">
        <p>
          Atlas is built from WGU&apos;s publicly available catalog data, covering 108
          editions from January 2017 through March 2026. It does not use internal WGU
          systems or private data.
        </p>
        <p>
          It is a community project, and official WGU sources should still be the final
          word for advising, enrollment, and academic policy.
        </p>
      </Section>

      <Section title="How history and resources are used">
        <p>
          When a degree or school has changed over time, Atlas shows that context where
          it helps explain what you&apos;re viewing. That might include earlier names,
          past versions, or other relevant background.
        </p>
        <p>
          Official WGU resources, such as program guides and outcomes pages, are attached
          to degree and school pages when they have been identified and verified from
          public WGU sources.
        </p>
      </Section>

      <div className="border-t border-slate-100 pt-8 mt-4">
        <h2 className="text-base font-semibold text-slate-700 mb-4">More detail</h2>
        <ul className="flex flex-col gap-3 text-sm">
          <li>
            <Link href="/methods" className="text-blue-600 hover:underline font-medium">
              Methods
            </Link>
            <span className="text-slate-500 ml-2">
              — how the data was collected and how to interpret it
            </span>
          </li>
          <li>
            <Link href="/data" className="text-blue-600 hover:underline font-medium">
              Data
            </Link>
            <span className="text-slate-500 ml-2">
              — download the Atlas datasets
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
