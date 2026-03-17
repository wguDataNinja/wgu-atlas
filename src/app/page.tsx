import Link from "next/link";
import { getHomepageSummary } from "@/lib/data";
import HomeSearch from "@/components/home/HomeSearch";
import SchoolCards from "@/components/home/SchoolCards";
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
            Explore WGU degrees, courses, and schools. Compare related degrees.
          </p>

          <div className="flex justify-center mb-10">
            <HomeSearch />
          </div>

          <SchoolCards />
        </div>
      </section>

      {/* ── Orientation ──────────────────────────────────────────────────── */}
      <section className="border-b border-slate-100 bg-slate-50">
        <div className="max-w-3xl mx-auto px-4 py-8">
          <p className="text-slate-600 text-sm leading-relaxed">
            WGU Atlas is an independent guide to WGU degrees, courses, and
            schools, built from public WGU sources. It helps students explore
            degree options, compare related degrees, and understand changes over
            time when those changes matter to what they&apos;re viewing.
          </p>
        </div>
      </section>

      {/* ── Compare callout ──────────────────────────────────────────────── */}
      <section className="max-w-3xl mx-auto px-4 py-8">
        <div className="border border-slate-200 rounded-lg px-5 py-4 flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-medium text-slate-800">Compare degrees</p>
            <p className="text-xs text-slate-500 mt-0.5">
              See how related WGU degrees differ — course rosters, shared
              courses, and track-specific requirements.
            </p>
          </div>
          <Link
            href="/compare"
            className="shrink-0 text-sm text-blue-600 hover:text-blue-800 font-medium hover:underline"
          >
            Compare degrees →
          </Link>
        </div>
      </section>

      {/* ── Attribution ──────────────────────────────────────────────────── */}
      <section className="max-w-3xl mx-auto px-4 pb-10">
        <p className="text-xs text-slate-400">
          Built from WGU&apos;s public catalog · Updated through March 2026 ·{" "}
          <Link href="/about" className="hover:underline">
            About this site
          </Link>
        </p>
      </section>

      <Footer dataDate={summary.data_date} />
    </>
  );
}
