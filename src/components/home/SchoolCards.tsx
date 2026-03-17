import Link from "next/link";

const SCHOOLS = [
  {
    name: "School of Business",
    slug: "business",
    color: "bg-blue-50 border-blue-200 hover:border-blue-400",
    description:
      "Bachelor's, master's, and MBA degrees in accounting, management, marketing, IT management, finance, and related fields.",
  },
  {
    name: "Leavitt School of Health",
    slug: "health",
    color: "bg-green-50 border-green-200 hover:border-green-400",
    description:
      "Degrees in nursing, healthcare administration, public health, health informatics, and allied health disciplines.",
  },
  {
    name: "School of Technology",
    slug: "technology",
    color: "bg-purple-50 border-purple-200 hover:border-purple-400",
    description:
      "Degrees in IT, cybersecurity, software engineering, data analytics, cloud computing, and computer science.",
  },
  {
    name: "School of Education",
    slug: "education",
    color: "bg-amber-50 border-amber-200 hover:border-amber-400",
    description:
      "Teacher preparation, educational leadership, and learning and technology degrees across all grade bands.",
  },
];

export default function SchoolCards() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
      {SCHOOLS.map((school) => (
        <Link
          key={school.slug}
          href={`/schools/${school.slug}`}
          className={`border rounded-lg p-4 flex flex-col gap-2 transition-colors ${school.color}`}
        >
          <span className="font-semibold text-slate-800 text-sm">
            {school.name}
          </span>
          <span className="text-xs text-slate-600 leading-snug">
            {school.description}
          </span>
          <span className="text-xs text-blue-600 font-medium mt-1">
            Explore {school.name} →
          </span>
        </Link>
      ))}
    </div>
  );
}
