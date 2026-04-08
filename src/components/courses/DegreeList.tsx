"use client";

import { useState } from "react";
import Link from "next/link";

const INITIAL_SHOW = 8;

type Entry = { program: string; first_seen: string };

export default function DegreeList({
  appearances,
  headingToCode,
  courseActive = true,
}: {
  appearances: Entry[];
  headingToCode: Record<string, string>;
  courseActive?: boolean;
}) {
  const [expanded, setExpanded] = useState(false);
  const visible = expanded ? appearances : appearances.slice(0, INITIAL_SHOW);
  const hidden = appearances.length - INITIAL_SHOW;

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1 h-5 bg-blue-600 rounded" />
        <h2 className="text-base font-semibold text-slate-800">
          {courseActive
            ? `Included in Current Degrees (${appearances.length})`
            : `Found in Active Programs (${appearances.length})`}
        </h2>
      </div>
      <div className="border border-slate-200 rounded-lg overflow-hidden">
        <ul>
          {visible.map((entry, i) => {
            const progCode = headingToCode[entry.program];
            return (
              <li
                key={i}
                className="border-b border-slate-100 last:border-0 px-4 py-2.5 text-sm"
              >
                {progCode ? (
                  <Link href={`/programs/${progCode}`} className="text-blue-700 hover:underline">
                    {entry.program}
                  </Link>
                ) : (
                  <span className="text-slate-700">{entry.program}</span>
                )}
              </li>
            );
          })}
        </ul>
        {appearances.length > INITIAL_SHOW && (
          <button
            onClick={() => setExpanded((v) => !v)}
            className="w-full px-4 py-2.5 text-sm text-blue-600 hover:text-blue-700 bg-slate-50 border-t border-slate-200 text-left font-medium"
          >
            {expanded ? "Show fewer" : `Show all ${appearances.length} degrees (+${hidden} more)`}
          </button>
        )}
      </div>
    </section>
  );
}
