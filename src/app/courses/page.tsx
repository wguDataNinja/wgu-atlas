import type { Metadata } from "next";
import { Suspense } from "react";
import { getCourses, getAllCourseCodes } from "@/lib/data";
import CourseExplorer from "@/components/courses/CourseExplorer";

export const metadata: Metadata = {
  title: "Courses",
  description: "Search and browse WGU courses — active and retired, with catalog history for each.",
};

export default function CoursesPage() {
  const courses = getCourses();
  const allCodes = new Set(getAllCourseCodes());
  const activeCourses = courses.filter((c) => c.active && c.scope === "AP");

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-800">Courses</h1>
        <p className="text-slate-500 mt-1">
          {activeCourses.length.toLocaleString()} active courses across WGU&apos;s four schools.
          Search by code or title, or filter by school.
        </p>
      </div>
      <Suspense>
        <CourseExplorer courses={courses} detailCodes={allCodes} />
      </Suspense>
    </div>
  );
}
