import Link from "next/link";
import { getHomepageSummary } from "@/lib/data";
import HomeSearch from "@/components/home/HomeSearch";
import SchoolCards from "@/components/home/SchoolCards";
import EventPreview from "@/components/home/EventPreview";
import Footer from "@/components/layout/Footer";

export default function HomePage() {
  const summary = getHomepageSummary();

  return (
    <>
      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <section className="bg-gradient-to-b from-blue-950 to-blue-900 text-white py-14 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-3">
            WGU Atlas
          </h1>
          <p className="text-blue-200 text-lg mb-8">
            Explore courses, programs, catalog changes, and student discussion
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
            WGU Atlas is built from{" "}
            <strong>{summary.total_editions} public WGU catalog editions</strong> spanning{" "}
            <strong>{summary.archive_span}</strong>. It tracks{" "}
            <strong>{summary.total_course_codes_ever.toLocaleString()} course codes</strong>{" "}
            ({summary.active_ap_codes} currently active) and{" "}
            <strong>{summary.active_programs} current programs</strong> across WGU&apos;s four
            schools. Official catalog facts, student discussion, and any AI-generated
            summaries are always kept separate and clearly labeled.
          </p>

          <div className="mt-4 flex flex-wrap gap-4 text-sm">
            <Stat label="Active courses" value={summary.active_ap_codes} />
            <Stat label="Retired codes" value={summary.retired_ap_codes} />
            <Stat label="Catalog editions" value={summary.total_editions} />
            <Stat label="Named events" value={summary.curated_major_events_count} />
          </div>
        </div>
      </section>

      {/* ── Activity modules ─────────────────────────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

          {/* Newest programs */}
          <Module title="Newest Programs" href="/programs">
            <ul className="flex flex-col gap-2">
              {summary.newest_programs.slice(0, 5).map((p) => (
                <li key={p.program_code} className="text-sm">
                  <span className="font-mono text-xs text-slate-400 mr-1">{p.first_seen}</span>
                  <Link
                    href={`/programs/${p.program_code}`}
                    className="text-slate-700 hover:text-blue-600 hover:underline"
                  >
                    {p.degree_heading}
                  </Link>
                  <span className="text-xs text-slate-400 block">{p.school}</span>
                </li>
              ))}
            </ul>
          </Module>

          {/* Recent course additions */}
          <Module title="Recent Course Additions" href="/courses">
            <ul className="flex flex-col gap-2">
              {summary.recent_course_additions.slice(0, 6).map((c) => (
                <li key={c.code} className="flex items-center gap-2 text-sm">
                  <Link
                    href={`/courses/${c.code}`}
                    className="font-mono text-xs bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded hover:bg-blue-100 transition-colors"
                  >
                    {c.code}
                  </Link>
                  <span className="text-slate-700 truncate">{c.title}</span>
                  <span className="text-xs text-slate-400 shrink-0">{c.added_in}</span>
                </li>
              ))}
            </ul>
          </Module>

          {/* Recent version changes */}
          <Module title="Programs with Recent Updates" href="/programs">
            <ul className="flex flex-col gap-2">
              {summary.recent_version_changes.slice(0, 5).map((p) => (
                <li key={p.program_code} className="text-sm">
                  <Link
                    href={`/programs/${p.program_code}`}
                    className="text-slate-700 hover:text-blue-600 hover:underline line-clamp-1"
                  >
                    {p.degree_heading}
                  </Link>
                  <span className="text-xs text-slate-400">{p.school} · updated {p.last_version_date}</span>
                </li>
              ))}
            </ul>
          </Module>
        </div>
      </section>

      {/* ── Timeline preview ─────────────────────────────────────────────── */}
      <section className="border-t border-slate-100 bg-slate-50">
        <div className="max-w-4xl mx-auto px-4 py-12">
          <div className="flex items-baseline justify-between mb-5">
            <h2 className="text-xl font-bold text-slate-800">Major Catalog Events</h2>
            <Link href="/timeline" className="text-sm text-blue-600 hover:underline">
              Full timeline →
            </Link>
          </div>
          <EventPreview events={summary.curated_major_events_preview} />
        </div>
      </section>

      {/* ── Around the WGU web ───────────────────────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 py-12">
        <h2 className="text-xl font-bold text-slate-800 mb-6">Around the WGU Web</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <LinkGroup title="Official WGU Channels">
            <ExternalLink href="https://www.wgu.edu" label="WGU Website" />
            <ExternalLink href="https://www.youtube.com/@WGU" label="WGU YouTube" />
            <ExternalLink href="https://www.instagram.com/westerngovernors/" label="WGU Instagram" />
            <ExternalLink href="https://www.facebook.com/wgu.edu" label="WGU Facebook" />
          </LinkGroup>
          <LinkGroup title="Community Discussion">
            <ExternalLink href="https://www.reddit.com/r/WGU/" label="r/WGU" />
            <ExternalLink href="https://www.reddit.com/r/WGUIT/" label="r/WGUIT" />
            <ExternalLink href="https://www.reddit.com/r/WGUTeaching/" label="r/WGUTeaching" />
          </LinkGroup>
          <LinkGroup title="Resources">
            <ExternalLink href="https://www.wgu.edu/alumni/career-services.html" label="WGU Career Services" />
            <ExternalLink href="https://partners.wgu.edu" label="WGU Partners" />
          </LinkGroup>
        </div>
        <p className="text-xs text-slate-400 mt-4">
          WGU Atlas is not affiliated with WGU. External links are provided for reference only.
        </p>
      </section>

      <Footer dataDate={summary.data_date} />
    </>
  );
}

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
      <h3 className="font-semibold text-slate-700 mb-2 text-xs uppercase tracking-wide">{title}</h3>
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
