"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const primaryLinks = [
  { href: "/", label: "Home" },
  { href: "/courses", label: "Courses" },
  { href: "/programs", label: "Programs" },
  { href: "/schools", label: "Schools" },
];

const secondaryLinks = [
  { href: "/timeline", label: "Timeline" },
  { href: "/methods", label: "Methods" },
  { href: "/data", label: "Data" },
];

export default function Nav() {
  const pathname = usePathname();

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname === href || pathname.startsWith(href + "/");

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4 flex items-center h-14 gap-1">
        <Link href="/" className="font-bold text-blue-700 text-lg tracking-tight shrink-0 mr-4">
          WGU Atlas
        </Link>

        {/* Primary nav — student-facing destinations */}
        <div className="flex gap-1">
          {primaryLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                isActive(href)
                  ? "bg-blue-50 text-blue-700"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
              }`}
            >
              {label}
            </Link>
          ))}
        </div>

        {/* Divider */}
        <div className="h-4 w-px bg-slate-200 mx-2" />

        {/* Secondary nav — archive/meta destinations */}
        <div className="flex gap-1">
          {secondaryLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={`px-3 py-1.5 rounded text-sm transition-colors ${
                isActive(href)
                  ? "bg-slate-100 text-slate-700 font-medium"
                  : "text-slate-400 hover:text-slate-600 hover:bg-slate-50"
              }`}
            >
              {label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
