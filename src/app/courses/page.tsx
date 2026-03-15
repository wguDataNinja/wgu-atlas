import type { Metadata } from "next";
import { Suspense } from "react";
import { getCourses, getAllCourseCodes } from "@/lib/data";
import CourseExplorer from "@/components/courses/CourseExplorer";

export const metadata: Metadata = {
  title: "Course Explorer",
  description: "Browse and search all 1,646 WGU course codes — active, retired, and certificate.",
};

export default function CoursesPage() {
  const courses = getCourses();
  const allCodes = new Set(getAllCourseCodes());

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-slate-800">Course Explorer</h1>
        <p className="text-slate-500 mt-1">
          {courses.length.toLocaleString()} course codes across the WGU catalog archive —
          active, deprecated, and certificate.
        </p>
      </div>
      <Suspense>
        <CourseExplorer courses={courses} detailCodes={allCodes} />
      </Suspense>
    </div>
  );
}
