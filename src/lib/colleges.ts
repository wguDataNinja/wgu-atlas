// Shared college definitions used across filter UIs (Courses, Degrees).
// "key" matches program.school / course.current_college canonical values.

export interface CollegeDef {
  key: string;
  /** All historical names for this college, including the current one. */
  allNames: string[];
  short: string;
  description: string;
  chipSelected: string;
  chipUnselected: string;
}

export const COLLEGES: CollegeDef[] = [
  {
    key: "School of Business",
    allNames: ["College of Business", "School of Business"],
    short: "Business",
    description: "Accounting, management, marketing, finance, IT management",
    chipSelected: "bg-blue-600 text-white",
    chipUnselected: "bg-white text-blue-700 border border-blue-300 hover:bg-blue-50",
  },
  {
    key: "Leavitt School of Health",
    allNames: ["College of Health Professions", "Leavitt School of Health"],
    short: "Health",
    description: "Nursing, healthcare administration, public health, informatics",
    chipSelected: "bg-rose-600 text-white",
    chipUnselected: "bg-white text-rose-700 border border-rose-300 hover:bg-rose-50",
  },
  {
    key: "School of Technology",
    allNames: ["College of Information Technology", "School of Technology"],
    short: "Technology",
    description: "IT, cybersecurity, software engineering, data analytics, CS",
    chipSelected: "bg-violet-600 text-white",
    chipUnselected: "bg-white text-violet-700 border border-violet-300 hover:bg-violet-50",
  },
  {
    key: "School of Education",
    allNames: ["Teachers College", "School of Education"],
    short: "Education",
    description: "Teacher preparation, educational leadership, learning technology",
    chipSelected: "bg-amber-500 text-white",
    chipUnselected: "bg-white text-amber-700 border border-amber-300 hover:bg-amber-50",
  },
];

export const LEVELS = ["Bachelor's", "Master's", "Certificate"] as const;
export type LevelLabel = (typeof LEVELS)[number];
