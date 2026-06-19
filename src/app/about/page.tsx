import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "About",
  description: "About WGU Atlas: a research surface for WGU degree structure, course relationships, program comparisons, and catalog history.",
};

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold text-slate-800 mb-2">About WGU Atlas</h1>
      <p className="text-slate-500 mb-10">
        A research surface for WGU degree structure, course comparisons, and catalog history.
      </p>

      <Section title="Catalog Timeline">
        <p>
          Atlas tracks 111 published WGU catalog editions from January 2017 through June 2026.
          Major events are named, dated, and annotated: school reorganizations, program restructures, mass course changes, and degree additions.
        </p>
        <p>
          <Link href="/timeline" className="text-blue-600 hover:underline font-medium">
            View the full catalog timeline →
          </Link>
        </p>
      </Section>

      <Section title="What Atlas is for">
        <p>
          Atlas helps students research what a WGU degree actually contains: course by course,
          across related programs, and over time.
        </p>
        <p>
          WGU publishes a lot of useful information. The problem is that it&apos;s spread across
          many page types and packaging styles. Atlas reorganizes the academic core of that
          information into a clearer research surface: inspect a degree, follow a course across
          programs, compare curricula side by side, understand how things changed.
        </p>
      </Section>

      <Section title="What you can do here">
        <ul className="list-none space-y-2 text-slate-600">
          {[
            ["Research a degree in one place", "roster, outcomes, certifications, history, and official resources together"],
            ["Compare programs by actual courses", "see exact shared and unique courses, not just headline metrics"],
            ["Follow a course across the catalog", "see every degree it appears in, active and retired"],
            ["Understand catalog history", "111 editions from 2017–2026; see when degrees and courses first appeared and how they changed"],
          ].map(([lead, detail]) => (
            <li key={lead} className="flex gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">→</span>
              <span>
                <span className="font-medium text-slate-700">{lead}</span>
                <span className="text-slate-400">: {detail}</span>
              </span>
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Independence and sources">
        <p>
          Atlas is an independent community project, not affiliated with or operated by WGU.
          All data is derived from WGU&apos;s publicly available course catalog (111 editions,
          January 2017 through June 2026), plus official WGU program guides and public
          outcomes pages.
        </p>
        <p>
          For advising, enrollment, or academic policy decisions, official WGU sources are
          authoritative. Atlas is a research aid, not a substitute.
        </p>
      </Section>

      <div className="border-t border-slate-100 pt-8 mt-4">
        <ul className="flex flex-col gap-3 text-sm">
          <li>
            <Link href="/methods" className="text-blue-600 hover:underline font-medium">
              How this data was collected
            </Link>
            <span className="text-slate-500 ml-2">
              archive coverage, validation, and trust caveats
            </span>
          </li>
          <li>
            <Link href="/timeline" className="text-blue-600 hover:underline font-medium">
              Catalog timeline
            </Link>
            <span className="text-slate-500 ml-2">
              major WGU catalog events from 2017 to 2026
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
