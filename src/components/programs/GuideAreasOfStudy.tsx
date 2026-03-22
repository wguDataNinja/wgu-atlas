"use client";

import { useState } from "react";
import type { GuideArtifact } from "@/lib/types";

type Props = {
  areasOfStudy: GuideArtifact["areas_of_study"];
};

function AosGroup({ group, courses }: { group: string; courses: GuideArtifact["areas_of_study"][number]["courses"] }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="border border-slate-200 rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between px-4 py-3 bg-slate-50 hover:bg-slate-100 transition-colors text-left"
        aria-expanded={open}
      >
        <span className="text-sm font-semibold text-slate-700">{group}</span>
        <span className="flex items-center gap-2 shrink-0">
          <span className="text-xs text-slate-400">{courses.length} course{courses.length !== 1 ? "s" : ""}</span>
          <span className="text-slate-400 text-xs">{open ? "▴" : "▾"}</span>
        </span>
      </button>
      {open && (
        <div className="divide-y divide-slate-100">
          {courses.map((course, i) => (
            <div key={i} className="px-4 py-3">
              <p className="text-sm font-medium text-slate-800 mb-1">{course.title}</p>
              {course.description && (
                <p className="text-xs text-slate-500 leading-relaxed mb-2">{course.description}</p>
              )}
              {course.competency_available && course.competency_bullets.length > 0 && (
                <ul className="space-y-0.5">
                  {course.competency_bullets
                    .filter((b) => !b.startsWith("Begin your course by discussing"))
                    .map((bullet, j) => (
                      <li key={j} className="flex gap-2 text-xs text-slate-600">
                        <span className="text-slate-300 shrink-0 mt-0.5">–</span>
                        <span>{bullet}</span>
                      </li>
                    ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function GuideAreasOfStudy({ areasOfStudy }: Props) {
  if (!areasOfStudy || areasOfStudy.length === 0) return null;

  const totalCourses = areasOfStudy.reduce((sum, g) => sum + g.courses.length, 0);

  return (
    <section className="mb-8">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-1 h-5 bg-blue-600 rounded shrink-0" />
        <h2 className="text-lg font-bold text-slate-800">Areas of Study</h2>
        <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
          {areasOfStudy.length} groups · {totalCourses} courses
        </span>
      </div>
      <p className="text-xs text-slate-400 mb-3">
        Course groups from the WGU Program Guide. Expand each group to see course descriptions and competencies.
      </p>
      <div className="space-y-2">
        {areasOfStudy.map((group) => (
          <AosGroup key={group.group} group={group.group} courses={group.courses} />
        ))}
      </div>
    </section>
  );
}
