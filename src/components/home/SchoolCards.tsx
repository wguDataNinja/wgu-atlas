import Link from "next/link";

const SCHOOLS = [
  { name: "Business", slug: "business", icon: "📊", color: "bg-blue-50 border-blue-200 hover:border-blue-400" },
  { name: "Health Professions", slug: "health", icon: "🏥", color: "bg-green-50 border-green-200 hover:border-green-400" },
  { name: "Technology", slug: "technology", icon: "💻", color: "bg-purple-50 border-purple-200 hover:border-purple-400" },
  { name: "Education", slug: "education", icon: "📚", color: "bg-amber-50 border-amber-200 hover:border-amber-400" },
];

export default function SchoolCards({ counts }: { counts: Record<string, number> }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {SCHOOLS.map((school) => {
        // Match count key — source data uses short names
        const countKey = Object.keys(counts).find((k) =>
          k.toLowerCase().includes(school.slug)
        );
        const count = countKey ? counts[countKey] : null;

        return (
          <Link
            key={school.slug}
            href={`/courses?school=${encodeURIComponent(school.slug)}`}
            className={`border rounded-lg p-4 flex flex-col gap-1 transition-colors ${school.color}`}
          >
            <span className="text-2xl">{school.icon}</span>
            <span className="font-semibold text-slate-800 text-sm leading-snug">
              {school.name}
            </span>
            {count !== null && (
              <span className="text-xs text-slate-500">{count} active courses</span>
            )}
          </Link>
        );
      })}
    </div>
  );
}
