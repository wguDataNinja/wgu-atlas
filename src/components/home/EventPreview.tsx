import Link from "next/link";
import type { CuratedEventPreview } from "@/lib/types";

const TYPE_LABELS: Record<string, string> = {
  rename_cleanup: "Rename / Cleanup",
  composite: "Composite",
  school_rename: "School Rename",
  program_restructure: "Program Restructure",
  expansion: "Expansion",
  cert_formalization: "Cert Formalization",
};

export default function EventPreview({ events }: { events: CuratedEventPreview[] }) {
  return (
    <div className="flex flex-col gap-3">
      {events.slice(0, 4).map((ev) => (
        <Link
          key={ev.event_id}
          href={`/timeline#${ev.event_id}`}
          className="border border-slate-200 rounded-lg p-4 hover:border-blue-300 hover:bg-blue-50 transition-colors group"
        >
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs text-slate-400 font-mono">{ev.date_range}</span>
                <span className="text-xs bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded">
                  {TYPE_LABELS[ev.type] ?? ev.type}
                </span>
              </div>
              <p className="font-medium text-slate-800 text-sm group-hover:text-blue-700 transition-colors">
                {ev.title}
              </p>
              <p className="text-xs text-slate-500 mt-1 line-clamp-2">{ev.summary}</p>
            </div>
            <span className="text-slate-300 group-hover:text-blue-400 transition-colors">→</span>
          </div>
        </Link>
      ))}
      <Link href="/timeline" className="text-sm text-blue-600 hover:underline">
        View full timeline →
      </Link>
    </div>
  );
}
