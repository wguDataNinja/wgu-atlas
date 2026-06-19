import Link from "next/link";
import HomeSearch from "@/components/home/HomeSearch";
import { getHomepageSummary } from "@/lib/data";

export default function HomePage() {
  const summary = getHomepageSummary();
  const totalCodes = (summary?.active_ap_codes ?? 866) + (summary?.active_cert_codes ?? 52);
  const activePrograms = summary?.active_programs ?? 116;
  const totalEditions = summary?.total_editions ?? 111;

  return (
    <>
      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <section className="bg-gradient-to-b from-blue-950 to-blue-900 text-white py-16 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-3">
            WGU Atlas
          </h1>
          <p className="text-blue-200 text-lg mb-8 max-w-xl mx-auto">
            Research what a WGU degree actually contains: courses, comparisons, and catalog history.
          </p>
          <div className="flex justify-center mb-10">
            <HomeSearch />
          </div>
        </div>
      </section>

      {/* ── Scale band ───────────────────────────────────────────────────── */}
      <section className="bg-blue-900 border-t border-blue-800">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex flex-wrap justify-center gap-x-8 gap-y-2 text-sm text-blue-200">
            <span><strong className="text-white">{activePrograms}</strong> active degrees</span>
            <span><strong className="text-white">{totalCodes}</strong> courses tracked</span>
            <span><strong className="text-white">{totalEditions}</strong> catalog editions</span>
            <span><strong className="text-white">2017–2026</strong> archive span</span>
          </div>
        </div>
      </section>

      {/* ── What you can do ──────────────────────────────────────────────── */}
      <section className="max-w-5xl mx-auto px-4 py-14">
        <div className="grid md:grid-cols-3 gap-6">

          {/* Degree research */}
          <FeatureCard
            href="/programs/BSCS"
            label="Research a degree"
            description="See the full course roster, learning outcomes, embedded certifications, official resources, and catalog history. All in one place."
            cta="Browse degrees →"
            ctaHref="/programs"
            preview={
              <DegreePreview
                code="BSCS"
                name="Computer Science"
                school="School of Technology"
                cus={124}
                courses={37}
                firstSeen="2018-06"
              />
            }
          />

          {/* Compare */}
          <FeatureCard
            href="/compare"
            label="Compare by actual courses"
            description="See exactly which courses two degrees share, and which are unique to each. Not headline metrics. The actual curriculum."
            cta="Compare degrees →"
            ctaHref="/compare"
            preview={<ComparePreview />}
          />

          {/* Course connectedness */}
          <FeatureCard
            href="/courses/D268"
            label="Follow a course across programs"
            description="Every course links to the degrees that include it, active and retired. See how courses connect programs across the catalog."
            cta="Browse courses →"
            ctaHref="/courses"
            preview={
              <CoursePreview
                code="D268"
                title="Intro to Communication: Connecting"
                degreeCount={39}
                college="School of Technology"
              />
            }
          />

        </div>
      </section>

      {/* ── Timeline callout ─────────────────────────────────────────────── */}
      <section className="border-y border-slate-100 bg-slate-50">
        <div className="max-w-4xl mx-auto px-4 py-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-slate-800">9 years of catalog history</p>
            <p className="text-sm text-slate-500 mt-0.5">
              111 editions from 2017 to 2026. School reorganizations, program restructures, and mass course changes, named, dated, and annotated.
            </p>
          </div>
          <Link
            href="/timeline"
            className="shrink-0 text-sm font-semibold text-blue-600 hover:text-blue-800 hover:underline"
          >
            View catalog timeline →
          </Link>
        </div>
      </section>

      {/* ── School navigation ────────────────────────────────────────────── */}
      <section className="max-w-4xl mx-auto px-4 py-14">
        <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-6">
          Browse by college
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {SCHOOLS.map((school) => (
            <Link
              key={school.slug}
              href={`/schools/${school.slug}`}
              className={`border rounded-lg p-4 flex flex-col gap-1.5 transition-colors ${school.color}`}
            >
              <span className="font-semibold text-slate-800 text-sm">{school.name}</span>
              <span className="text-xs text-slate-600 leading-snug">{school.description}</span>
              <span className="text-xs text-blue-600 font-medium mt-1">Explore →</span>
            </Link>
          ))}
        </div>
      </section>

      {/* ── Trust line ───────────────────────────────────────────────────── */}
      <section className="border-t border-slate-100 bg-slate-50">
        <div className="max-w-4xl mx-auto px-4 py-5 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-400">
          <span>Independent community project · not affiliated with WGU · built from public WGU sources</span>
          <Link href="/about" className="hover:underline hover:text-slate-600">About Atlas</Link>
        </div>
      </section>
    </>
  );
}

// ---------------------------------------------------------------------------
// Feature card wrapper
// ---------------------------------------------------------------------------

function FeatureCard({
  label,
  description,
  cta,
  ctaHref,
  preview,
}: {
  href: string;
  label: string;
  description: string;
  cta: string;
  ctaHref: string;
  preview: React.ReactNode;
}) {
  return (
    <div className="border border-slate-200 rounded-xl overflow-hidden flex flex-col">
      <div className="bg-slate-50 border-b border-slate-100 p-4 flex-1">
        {preview}
      </div>
      <div className="p-4">
        <p className="text-sm font-semibold text-slate-800 mb-1">{label}</p>
        <p className="text-xs text-slate-500 leading-relaxed mb-3">{description}</p>
        <Link href={ctaHref} className="text-xs font-semibold text-blue-600 hover:underline">
          {cta}
        </Link>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Mini previews — rendered from real data, no screenshots needed
// ---------------------------------------------------------------------------

function DegreePreview({
  code, name, school, cus, courses, firstSeen,
}: {
  code: string; name: string; school: string; cus: number; courses: number; firstSeen: string;
}) {
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <span className="font-mono text-xs bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded">{code}</span>
        <span className="text-xs text-slate-500">{cus} CUs</span>
      </div>
      <p className="text-sm font-semibold text-slate-800 leading-snug">{name}</p>
      <p className="text-xs text-slate-400">{school}</p>
      <div className="flex gap-3 text-xs text-slate-500 pt-1">
        <span className="bg-white border border-slate-200 rounded px-2 py-0.5">{courses} courses</span>
        <span className="bg-white border border-slate-200 rounded px-2 py-0.5">since {firstSeen}</span>
      </div>
    </div>
  );
}

function ComparePreview() {
  const shared = ["C955", "D268", "C393"];
  const left = ["D684", "C867", "C952"];
  const right = ["D491", "D370", "D388"];
  return (
    <div className="space-y-2">
      <div className="grid grid-cols-[1fr_1fr_1fr] gap-1 text-xs">
        <div className="bg-blue-600 text-white rounded px-2 py-1 text-center font-semibold truncate">CS</div>
        <div className="bg-slate-600 text-white rounded px-2 py-1 text-center font-semibold">Shared</div>
        <div className="bg-amber-500 text-white rounded px-2 py-1 text-center font-semibold truncate">BSDA</div>
      </div>
      <div className="grid grid-cols-[1fr_1fr_1fr] gap-1">
        <div className="space-y-1">
          {left.map(c => (
            <div key={c} className="text-xs font-mono bg-blue-50 text-blue-700 rounded px-1.5 py-0.5 truncate">{c}</div>
          ))}
        </div>
        <div className="space-y-1">
          {shared.map(c => (
            <div key={c} className="text-xs font-mono bg-slate-100 text-slate-600 rounded px-1.5 py-0.5 truncate">{c}</div>
          ))}
        </div>
        <div className="space-y-1">
          {right.map(c => (
            <div key={c} className="text-xs font-mono bg-amber-50 text-amber-700 rounded px-1.5 py-0.5 truncate">{c}</div>
          ))}
        </div>
      </div>
      <p className="text-xs text-slate-400 pt-0.5">13 shared · 24 unique to CS · 29 unique to BSDA</p>
    </div>
  );
}

function CoursePreview({
  code, title, degreeCount, college,
}: {
  code: string; title: string; degreeCount: number; college: string;
}) {
  const sampleDegrees = [
    "B.S. Computer Science",
    "B.S. Data Analytics",
    "B.S. Business Administration",
    "B.S. Cybersecurity",
  ];
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <span className="font-mono text-xs bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">{code}</span>
        <span className="text-xs text-slate-400">{college}</span>
      </div>
      <p className="text-sm font-semibold text-slate-800 leading-snug">{title}</p>
      <p className="text-xs text-slate-500">Appears in <strong className="text-slate-700">{degreeCount} degrees</strong></p>
      <div className="space-y-0.5 pt-0.5">
        {sampleDegrees.map(d => (
          <div key={d} className="text-xs text-slate-500 flex items-center gap-1.5">
            <span className="w-1 h-1 rounded-full bg-blue-400 shrink-0" />
            {d}
          </div>
        ))}
        <div className="text-xs text-slate-400 pl-2.5">+{degreeCount - sampleDegrees.length} more</div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// School data
// ---------------------------------------------------------------------------

const SCHOOLS = [
  {
    name: "School of Business",
    slug: "business",
    color: "bg-blue-50 border-blue-200 hover:border-blue-400",
    description: "Bachelor's, master's, and MBA degrees in accounting, management, marketing, IT management, finance, and related fields.",
  },
  {
    name: "Leavitt School of Health",
    slug: "health",
    color: "bg-green-50 border-green-200 hover:border-green-400",
    description: "Degrees in nursing, healthcare administration, public health, health informatics, and allied health disciplines.",
  },
  {
    name: "School of Technology",
    slug: "technology",
    color: "bg-purple-50 border-purple-200 hover:border-purple-400",
    description: "Degrees in IT, cybersecurity, software engineering, data analytics, cloud computing, and computer science.",
  },
  {
    name: "School of Education",
    slug: "education",
    color: "bg-amber-50 border-amber-200 hover:border-amber-400",
    description: "Teacher preparation, educational leadership, and learning and technology degrees across all grade bands.",
  },
];
