import Link from "next/link";

export default function NotFound() {
  return (
    <div className="max-w-xl mx-auto px-4 py-24 text-center">
      <h1 className="text-4xl font-bold text-slate-800 mb-3">Not found</h1>
      <p className="text-slate-500 mb-2">
        This page doesn&apos;t exist — or this course code may be retired or a certificate
        code without a detail page in the current data version.
      </p>
      <p className="text-slate-400 text-sm mb-8">
        Retired and certificate codes appear in the Course Explorer listing but do not
        have individual detail pages in v1.
      </p>
      <div className="flex justify-center gap-4">
        <Link href="/courses" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors text-sm">
          Course Explorer
        </Link>
        <Link href="/" className="border border-slate-300 px-4 py-2 rounded hover:bg-slate-50 transition-colors text-sm text-slate-600">
          Home
        </Link>
      </div>
    </div>
  );
}
