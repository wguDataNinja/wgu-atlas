import Link from "next/link";
import { getHomepageSummary, getSchools, getProgramsBySchool } from "@/lib/data";
import HomeSearch from "@/components/home/HomeSearch";
import SchoolCards from "@/components/home/SchoolCards";
import EventPreview from "@/components/home/EventPreview";
import Footer from "@/components/layout/Footer";

export default function HomePage() {
  const summary = getHomepageSummary();
  const schools = getSchools();

  return (
    <>
      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <section className="bg-gradient-to-b from-blue-950 to-blue-900 text-white py-14 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-3">
            WGU Atlas
          </h1>
          <p className="text-blue-200 text-lg mb-8">
            Search courses, programs, and WGU catalog history
          </p>

          <div className="flex justify-center mb-8">
            <HomeSearch />
          </div>

          <SchoolCards counts={summary.active_by_school} />
        </div>
      </section>

      {/* ── Orientation band ─────────────────────────────────────────────── */}
      <section className="border-b border-slate-100 bg-slate-50">
        <div className="max-w-4xl mx-auto px-4 py-8">
          <p className="text-slate-600 text-sm leading-relaxed max-w-2xl">
            WGU Atlas is an unofficial reference built from WGU&apos;s public academic
            catalog. It covers{" "}
            <strong>{summary.active_ap_codes} active courses</strong> and{" "}
            <strong>{summary.active_programs} current programs</strong> across
            four schools, with history going back to {summary.archive_span.split("–")[0]}.
            Use it to look up courses, browse programs, and understand how WGU&apos;s
            curriculum has changed over time.
          </p>

          <div className="mt-4 flex flex-wrap gap-3 text-sm">
            <Stat label="Active courses" value={summary.active_ap_codes} />
            <Stat label="Active programs" value={summary.active_programs} />
          </div>

          <p className="text-xs text-slate-400 mt-4">
            Data from WGU public catalog · {summary.data_date} edition ·{" "}
            <Link href="/methods" className="hover:underline">About this data</Link>
          </p>
        </div>
      </section>

      {/* ── Activity modules ─────────────────────────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

          {/* Newest programs */}
          <Module title="New Programs" href="/programs">
            <ul className="flex flex-col gap-2">
              {summary.newest_programs.slice(0, 5).map((p) => (
                <li key={p.program_code} className="text-sm">
                  <Link
                    href={`/programs/${p.program_code}`}
                    className="text-slate-700 hover:text-blue-600 hover:underline"
                  >
                    {cleanHeading(p.degree_heading)}
                  </Link>
                  <span className="text-xs text-slate-400 block">
                    {shortSchool(p.school)} · {p.first_seen}
                  </span>
                </li>
              ))}
            </ul>
          </Module>

          {/* Recent course additions */}
          <Module title="New Courses" href="/courses">
            <ul className="flex flex-col gap-2">
              {summary.recent_course_additions.slice(0, 6).map((c) => (
                <li key={c.code} className="flex items-start gap-2 text-sm">
                  <Link
                    href={`/courses/${c.code}`}
                    className="font-mono text-xs bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded hover:bg-blue-100 transition-colors shrink-0 mt-0.5"
                  >
                    {c.code}
                  </Link>
                  <span className="text-slate-700 leading-snug">{c.title}</span>
                </li>
              ))}
            </ul>
          </Module>

          {/* Browse by school */}
          <Module title="Browse by School" href="/schools">
            <ul className="flex flex-col gap-2">
              {schools.map((school) => {
                const programs = getProgramsBySchool(school.canonical_key);
                return (
                  <li key={school.slug}>
                    <Link
                      href={`/schools/${school.slug}`}
                      className="text-sm text-slate-700 hover:text-blue-600 hover:underline"
                    >
                      {school.current_name}
                    </Link>
                    <span className="text-xs text-slate-400 ml-2">
                      {programs.length} programs
                    </span>
                  </li>
                );
              })}
            </ul>
          </Module>
        </div>
      </section>

      {/* ── Around the WGU web ───────────────────────────────────────────── */}
      <section className="border-t border-slate-100 bg-slate-50">
        <div className="max-w-6xl mx-auto px-4 py-12">
          <h2 className="text-lg font-bold text-slate-800 mb-6">
            Official WGU Resources
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
            <LinkGroup title="Official Channels">
              <ExternalLink href="https://www.wgu.edu" label="WGU Website" />
              <ExternalLink href="https://www.youtube.com/@WGU" label="WGU YouTube" />
              <ExternalLink href="https://www.instagram.com/westerngovernors/" label="WGU Instagram" />
              <ExternalLink href="https://www.facebook.com/wgu.edu" label="WGU Facebook" />
            </LinkGroup>
            <LinkGroup title="Community">
              <ExternalLink href="https://www.reddit.com/r/WGU/" label="r/WGU" />
              <ExternalLink href="https://www.reddit.com/r/WGUIT/" label="r/WGUIT" />
              <ExternalLink href="https://www.reddit.com/r/WGUTeaching/" label="r/WGUTeaching" />
            </LinkGroup>
            <LinkGroup title="Career & Support">
              <ExternalLink href="https://www.wgu.edu/alumni/career-services.html" label="WGU Career Services" />
              <ExternalLink href="https://partners.wgu.edu" label="WGU Partners" />
            </LinkGroup>
          </div>
          <p className="text-xs text-slate-400 mt-4">
            WGU Atlas is not affiliated with WGU. External links are provided for reference only.
          </p>
        </div>
      </section>

      {/* ── WGU History (catalog timeline) ───────────────────────────────── */}
      <section className="max-w-4xl mx-auto px-4 py-10">
        <div className="flex items-baseline justify-between mb-4">
          <h2 className="text-base font-semibold text-slate-700">
            WGU Catalog History
          </h2>
          <Link href="/timeline" className="text-sm text-blue-600 hover:underline">
            Full timeline →
          </Link>
        </div>
        <p className="text-xs text-slate-400 mb-4">
          Notable curriculum and structural changes drawn from {summary.total_editions} catalog editions.
        </p>
        <EventPreview events={summary.curated_major_events_preview} />
      </section>

      <Footer dataDate={summary.data_date} />
    </>
  );
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function cleanHeading(heading: string): string {
  const s = heading.split("|")[0].trim();
  return s.length > 60 ? s.slice(0, 60) + "…" : s;
}

function shortSchool(school: string): string {
  return school
    .replace("School of ", "")
    .replace("Leavitt School of ", "")
    .replace("College of ", "")
    .replace("Teachers College", "Education");
}

// ---------------------------------------------------------------------------
// UI components
// ---------------------------------------------------------------------------

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="bg-white border border-slate-200 rounded px-3 py-2">
      <div className="text-lg font-bold text-blue-700">{value.toLocaleString()}</div>
      <div className="text-xs text-slate-500">{label}</div>
    </div>
  );
}

function Module({
  title,
  href,
  children,
}: {
  title: string;
  href: string;
  children: React.ReactNode;
}) {
  return (
    <div className="border border-slate-200 rounded-lg p-5">
      <div className="flex items-baseline justify-between mb-4">
        <h3 className="font-semibold text-slate-800">{title}</h3>
        <Link href={href} className="text-xs text-blue-600 hover:underline">
          See all →
        </Link>
      </div>
      {children}
    </div>
  );
}

function LinkGroup({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h3 className="font-semibold text-slate-700 mb-2 text-xs uppercase tracking-wide">
        {title}
      </h3>
      <ul className="flex flex-col gap-1.5">{children}</ul>
    </div>
  );
}

function ExternalLink({ href, label }: { href: string; label: string }) {
  return (
    <li>
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-slate-600 hover:text-blue-700 hover:underline"
      >
        {label} ↗
      </a>
    </li>
  );
}
