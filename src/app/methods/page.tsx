import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Methods",
  description: "How WGU Atlas data was collected, validated, and interpreted — archive coverage, parser eras, and trust caveats.",
};

export default function MethodsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold text-slate-800 mb-2">Methods &amp; Caveats</h1>
      <p className="text-slate-500 mb-10">
        How this data was collected, validated, and how to interpret it correctly.
      </p>

      <Section title="Archive Coverage">
        <p>
          WGU Atlas is built from <strong>108 public WGU catalog editions</strong> spanning{" "}
          <strong>January 2017 through March 2026</strong>. Three editions are absent from
          the archive (2017-02, 2017-04, 2017-06), likely never published as separate
          snapshots on the WGU public catalog page.
        </p>
        <p>
          Each edition represents a distinct published snapshot of WGU&apos;s public course
          catalog. The parser extracts course codes, titles, program memberships, and
          structural metadata from each edition.
        </p>
      </Section>

      <Section title="Parser Eras">
        <p>
          The WGU catalog underwent a structural formatting change in mid-2024. Two
          parser eras are recognized:
        </p>
        <ul className="list-disc list-inside text-slate-600 space-y-1">
          <li><strong>ERA_A:</strong> 2017-01 through 2024-07 — original catalog structure</li>
          <li><strong>ERA_B:</strong> 2024-08 through 2026-03 — updated catalog structure</li>
        </ul>
        <p>
          The active parser (<code className="text-sm bg-slate-100 px-1 rounded">parse_catalog_v11.py</code>)
          handles both eras. A full archive run produces 0 skipped editions and 0 body-parse anomalies.

        </p>
      </Section>

      <Section title="Validation">
        <p>
          The 2026-03 edition serves as the trusted reference baseline. It was validated
          deeply after an initial scrape returned incomplete results (696 AP codes vs.
          the correct 838). The discrepancy was traced, corrected, and verified.
        </p>
        <p>
          14 structurally critical editions — breakpoints where the parser or catalog
          structure changed — were individually validated. All 14 passed clean.
        </p>
        <Callout>
          The 696 → 838 correction is an important part of this project&apos;s trust story.
          The current counts are hard-won and verified, not taken at face value from
          the first parser run.
        </Callout>
      </Section>

      <Section title="Observed vs. Inferred">
        <p>
          WGU Atlas distinguishes between observed facts and inferred relationships:
        </p>
        <ul className="list-disc list-inside text-slate-600 space-y-1">
          <li>
            <strong>Observed:</strong> directly present in the catalog archive — course code,
            title, program membership, edition dates
          </li>
          <li>
            <strong>Inferred:</strong> derived from patterns across editions — event types,
            event interpretations, stability classifications
          </li>
        </ul>
        <p>
          Interpretive content (event interpretations, title variant classifications) is
          labeled with confidence levels: <em>high</em>, <em>moderate</em>, or{" "}
          <em>tentative</em>.
        </p>
      </Section>

      <Section title="Title Variant Classification">
        <p>
          167 course codes show title variation across editions. These have been manually
          classified into categories:
        </p>
        <ul className="list-disc list-inside text-slate-600 space-y-1">
          <li><strong>Extraction noise</strong> (145 codes, 87%) — PDF line-wrap, Unicode variants, catalog oscillations. Not real renames.</li>
          <li><strong>Punctuation only</strong> (16) — hyphen, comma, em-dash changes.</li>
          <li><strong>Wording refinement</strong> (3) — typo fix or minor synonym swap.</li>
          <li><strong>Substantive change</strong> (2) — genuine semantic renames.</li>
          <li><strong>Formatting only</strong> (1) — space insertion.</li>
        </ul>
        <p>
          The overwhelming majority of apparent title variation is extraction artifact,
          not editorial intent.
        </p>
      </Section>

      <Section title="Key Caveats">
        <ul className="space-y-3 text-slate-600">
          <CaveatItem title="Catalog date ≠ implementation date">
            The catalog reflects publication timing, not guaranteed student rollout.
            A course appearing in a March catalog may have been deployed to students earlier or later.
          </CaveatItem>
          <CaveatItem title="Catalog presence ≠ lived experience">
            Official structure does not perfectly capture actual student pathways or
            the subjective experience of a course.
          </CaveatItem>
          <CaveatItem title="Code change ≠ substantive change">
            Course code changes may reflect renumbering, administrative reorganization,
            or cleanup — not necessarily changes to course content.
          </CaveatItem>
          <CaveatItem title="Reddit is supplementary context">
            Student discussion data (planned for v1.1) is useful context, not
            institutional truth. WGU Atlas keeps official catalog facts and discussion
            signals in clearly separate sections.
          </CaveatItem>
          <CaveatItem title="One-off courses require caution">
            Courses with only 1–2 catalog appearances are flagged (ghost_flag,
            single_appearance_flag). These may represent data anomalies or genuinely
            short-lived entries.
          </CaveatItem>
        </ul>
      </Section>

      <Section title="Data Separation Policy">
        <p>
          WGU Atlas enforces a strict separation between three information types:
        </p>
        <ul className="list-disc list-inside text-slate-600 space-y-1">
          <li><strong>Official catalog facts</strong> — from the WGU public catalog archive</li>
          <li><strong>Discussion signals</strong> — from Reddit and community spaces (v1.1)</li>
          <li><strong>LLM-generated summaries</strong> — clearly labeled with date, source count, and disclaimer (v1.1)</li>
        </ul>
        <p>
          These three types are never mixed in the same field or presented as equivalent.
        </p>
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

function Callout({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-blue-50 border border-blue-200 rounded p-3 text-sm text-blue-800">
      {children}
    </div>
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
