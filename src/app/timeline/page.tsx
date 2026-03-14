import type { Metadata } from "next";
import { getEvents } from "@/lib/data";
import type { CatalogEvent } from "@/lib/types";

export const metadata: Metadata = {
  title: "Timeline",
  description: "Major WGU catalog events from 2017 to 2026 — school reorganizations, mass course changes, program additions, and more.",
};

const TYPE_LABELS: Record<string, string> = {
  rename_cleanup: "Rename / Cleanup",
  composite: "Composite",
  school_rename: "School Rename",
  program_restructure: "Program Restructure",
  expansion: "Expansion",
  cert_formalization: "Cert Formalization",
  version_review: "Version Review",
  mixed: "Mixed",
};

const TYPE_COLORS: Record<string, string> = {
  rename_cleanup: "bg-blue-100 text-blue-700",
  composite: "bg-purple-100 text-purple-700",
  school_rename: "bg-orange-100 text-orange-700",
  program_restructure: "bg-pink-100 text-pink-700",
  expansion: "bg-green-100 text-green-700",
  cert_formalization: "bg-teal-100 text-teal-700",
  version_review: "bg-slate-100 text-slate-600",
  mixed: "bg-yellow-100 text-yellow-700",
};

function severityLabel(score: number) {
  if (score >= 300) return { label: "Very High", color: "bg-red-100 text-red-700" };
  if (score >= 150) return { label: "High", color: "bg-orange-100 text-orange-700" };
  if (score >= 75) return { label: "Moderate", color: "bg-yellow-100 text-yellow-700" };
  return { label: "Low", color: "bg-slate-100 text-slate-500" };
}

export default function TimelinePage() {
  const events = getEvents();
  const curated = events.filter((e) => e.is_curated_major_event);
  const other = events.filter((e) => !e.is_curated_major_event);

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Catalog Timeline</h1>
        <p className="text-slate-500 mt-2">
          {events.length} named catalog events across 107 edition transitions (2017–2026).
          Curated major events include hand-written interpretations; remaining events have
          machine-generated observed summaries.
        </p>
        <div className="mt-3 flex items-center gap-2 text-xs text-slate-400 bg-slate-50 border border-slate-200 rounded px-3 py-2 w-fit">
          <span className="w-2 h-2 bg-blue-500 rounded-full shrink-0" />
          All entries sourced from WGU public catalog archive. Observed summaries describe
          what changed; interpreted summaries explain why. Confidence noted where applicable.
        </div>
      </div>

      {/* Curated major events */}
      <section className="mb-12">
        <h2 className="text-xl font-bold text-slate-800 mb-1">Major Events</h2>
        <p className="text-sm text-slate-500 mb-5">
          {curated.length} curated events with hand-written titles and interpretations.
        </p>
        <div className="relative">
          <div className="absolute left-4 top-0 bottom-0 w-px bg-slate-200" />
          <div className="flex flex-col gap-6">
            {curated.map((ev) => (
              <EventCard key={ev.event_id} event={ev} curated />
            ))}
          </div>
        </div>
      </section>

      {/* All events */}
      <section>
        <h2 className="text-xl font-bold text-slate-800 mb-1">All Catalog Events</h2>
        <p className="text-sm text-slate-500 mb-5">
          {other.length} additional threshold-crossing transitions with observed summaries.
        </p>
        <div className="flex flex-col gap-3">
          {other.map((ev) => (
            <EventCard key={ev.event_id} event={ev} curated={false} />
          ))}
        </div>
      </section>
    </div>
  );
}

function EventCard({ event, curated }: { event: CatalogEvent; curated: boolean }) {
  const sev = severityLabel(event.severity_score);
  const typeColor = TYPE_COLORS[event.event_type_primary] ?? "bg-slate-100 text-slate-600";
  const typeLabel = TYPE_LABELS[event.event_type_primary] ?? event.event_type_primary;

  if (curated) {
    return (
      <div
        id={event.event_id}
        className="ml-8 relative border border-slate-200 rounded-lg p-5 bg-white hover:border-blue-200 transition-colors"
      >
        {/* Timeline dot */}
        <div className="absolute -left-10 top-5 w-3 h-3 rounded-full border-2 border-blue-500 bg-white" />

        <div className="flex flex-wrap items-center gap-2 mb-2">
          <span className="font-mono text-xs text-slate-400">{event.start_edition} → {event.end_edition}</span>
          <span className={`text-xs px-2 py-0.5 rounded font-medium ${typeColor}`}>{typeLabel}</span>
          <span className={`text-xs px-2 py-0.5 rounded ${sev.color}`}>
            Severity {sev.label}
          </span>
          <span className="text-xs text-slate-400 font-medium">
            {event.confidence} confidence
          </span>
        </div>

        <h3 className="font-bold text-slate-800 text-base mb-2">{event.event_title}</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
          <div>
            <dt className="text-xs text-slate-400 mb-1">Observed</dt>
            <dd className="text-sm text-slate-700">{event.observed_summary}</dd>
          </div>
          <div>
            <dt className="text-xs text-slate-400 mb-1">Interpretation</dt>
            <dd className="text-sm text-slate-600 italic">{event.interpreted_summary}</dd>
          </div>
        </div>

        <div className="flex flex-wrap gap-3 text-xs text-slate-500">
          {event.affected_schools && (
            <span>Schools: {event.affected_schools.replace(/;/g, ", ")}</span>
          )}
          <span>+{event.courses_added_count} / −{event.courses_removed_count} courses</span>
          {event.version_changes_count > 0 && (
            <span>{event.version_changes_count} version changes</span>
          )}
          {event.title_changes_count > 0 && (
            <span>{event.title_changes_count} title changes</span>
          )}
        </div>
      </div>
    );
  }

  // Compact row for non-curated events
  return (
    <div
      id={event.event_id}
      className="border border-slate-200 rounded-lg px-4 py-3 hover:border-slate-300 transition-colors"
    >
      <div className="flex flex-wrap items-center gap-2 mb-1">
        <span className="font-mono text-xs text-slate-400">{event.start_edition} → {event.end_edition}</span>
        <span className={`text-xs px-1.5 py-0.5 rounded ${typeColor}`}>{typeLabel}</span>
        <span className={`text-xs px-1.5 py-0.5 rounded ${sev.color}`}>{sev.label}</span>
      </div>
      <p className="text-sm text-slate-700">{event.observed_summary}</p>
      <div className="flex flex-wrap gap-3 text-xs text-slate-400 mt-1">
        {event.affected_schools && (
          <span>{event.affected_schools.replace(/;/g, ", ")}</span>
        )}
        <span>+{event.courses_added_count} / −{event.courses_removed_count} courses</span>
      </div>
    </div>
  );
}
