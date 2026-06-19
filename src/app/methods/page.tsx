import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "How This Data Was Collected",
  description: "How WGU Atlas data was collected, validated, and what to keep in mind when interpreting it.",
};

export default function MethodsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold text-slate-800 mb-2">How This Data Was Collected</h1>
      <p className="text-slate-500 mb-10">
        What Atlas is built from, how it was validated, and what to keep in mind.
      </p>

      <Section title="The catalog archive">
        <p>
          Atlas is built from <strong>111 published editions</strong> of WGU&apos;s public course
          catalog, spanning January 2017 through June 2026. Each edition is a distinct published
          snapshot. Three editions are missing from the archive (2017-02, 2017-04, 2017-06) and
          were likely never published as separate snapshots.
        </p>
        <p>
          Each edition was parsed to extract course codes, titles, program memberships, and
          structural metadata. The 2026-06 edition serves as the current baseline, validated through automated consistency checks and as the most recently archived edition.
        </p>
      </Section>

      <Section title="Validation">
        <p>
          The current course count (866 active AP codes) was not taken at face value from the
          first pass. An initial scrape returned only 696 codes. The discrepancy was traced,
          corrected, and individually verified against the source.
        </p>
        <p>
          14 structurally critical editions (breakpoints where catalog structure changed) were
          individually validated. All 14 passed clean.
        </p>
      </Section>

      <Section title="What's observed vs. what's inferred">
        <p>
          Atlas keeps a clear line between what the catalog directly states and what is derived
          from patterns across editions:
        </p>
        <ul className="list-disc list-inside text-slate-600 space-y-1">
          <li>
            <strong>Observed:</strong> course code, title, program membership, edition dates.
            Directly present in the source.
          </li>
          <li>
            <strong>Inferred:</strong> event types, event interpretations, stability
            classifications. Derived from patterns and labeled with confidence levels.
          </li>
        </ul>
      </Section>

      <Section title="Program guides">
        <p>
          Degree pages on Atlas also draw from WGU&apos;s official program guides, which are
          published on WGU&apos;s main site. These guides contain course descriptions,
          competency sets, and learning outcomes for each degree.
        </p>
        <p>
          Program guides are degree-specific. An example:{" "}
          <a
            href="https://www.wgu.edu/online-nursing-health-degrees/health-human-services/program-guide.html"
            className="text-blue-600 hover:underline"
            target="_blank"
            rel="noopener noreferrer"
          >
            Health and Human Services program guide
          </a>
          . Each degree program has its own guide page on the WGU site.
        </p>
      </Section>

      <Section title="What to keep in mind">
        <ul className="space-y-3 text-slate-600">
          <CaveatItem title="Catalog dates aren't rollout dates">
            The catalog reflects when WGU published a change, not when students experienced it.
            A course appearing in a March catalog may have been available earlier or later.
          </CaveatItem>
          <CaveatItem title="Structure isn't experience">
            The official catalog captures the designed curriculum. It doesn&apos;t capture how
            courses are actually experienced by students, or variation in sequencing and pacing.
          </CaveatItem>
          <CaveatItem title="Code changes aren&apos;t always content changes">
            A course code change may reflect renumbering or administrative cleanup rather than
            a change to the actual course content.
          </CaveatItem>
          <CaveatItem title="Official WGU sources are authoritative">
            For enrollment, advising, or policy decisions, WGU&apos;s official sources are
            authoritative. Atlas is a research aid, not a substitute.
          </CaveatItem>
        </ul>
      </Section>
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

function CaveatItem({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <li className="flex flex-col gap-0.5">
      <span className="font-semibold text-slate-700">{title}</span>
      <span>{children}</span>
    </li>
  );
}
