"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import type { SearchEntry } from "@/lib/types";
import { BASE_PATH } from "@/lib/basePath";

export default function HomeSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchEntry[]>([]);
  const [index, setIndex] = useState<SearchEntry[]>([]);
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  // Load search index once on mount
  useEffect(() => {
    fetch(`${BASE_PATH}/data/search_index.json`)
      .then((r) => r.json())
      .then(setIndex)
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!query.trim() || query.length < 2) {
      setResults([]);
      setOpen(false);
      return;
    }
    const q = query.toLowerCase();
    const hits = index
      .filter(
        (e) =>
          e.code.toLowerCase().includes(q) ||
          e.title.toLowerCase().includes(q) ||
          e.alt_titles?.some((t) => t.toLowerCase().includes(q))
      )
      .slice(0, 8);
    setResults(hits);
    setOpen(hits.length > 0);
  }, [query, index]);

  // Close on outside click
  useEffect(() => {
    function handler(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  function href(entry: SearchEntry) {
    if (entry.type === "course") return `/courses/${entry.code}`;
    return `/courses?q=${encodeURIComponent(entry.title)}`;
  }

  return (
    <div ref={ref} className="relative w-full max-w-xl">
      <div className="flex items-center gap-2 bg-white border border-slate-300 rounded-lg shadow-sm px-4 py-3 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500 transition">
        <svg className="w-4 h-4 text-slate-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
        </svg>
        <input
          type="text"
          placeholder="Search by course code or title…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => results.length > 0 && setOpen(true)}
          className="flex-1 bg-transparent outline-none text-sm placeholder-slate-400"
          autoComplete="off"
        />
        {query && (
          <button onClick={() => { setQuery(""); setOpen(false); }} className="text-slate-400 hover:text-slate-600 text-xs">✕</button>
        )}
      </div>

      {open && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-200 rounded-lg shadow-lg z-50 overflow-hidden">
          {results.map((entry) => (
            <Link
              key={`${entry.type}-${entry.code}`}
              href={href(entry)}
              onClick={() => setOpen(false)}
              className="flex items-center gap-3 px-4 py-2.5 hover:bg-slate-50 transition-colors border-b border-slate-100 last:border-0"
            >
              <span className={`text-xs font-mono px-1.5 py-0.5 rounded font-semibold ${
                entry.type === "course"
                  ? "bg-blue-100 text-blue-700"
                  : "bg-purple-100 text-purple-700"
              }`}>
                {entry.code}
              </span>
              <span className="text-sm text-slate-800 truncate">{entry.title}</span>
              {!entry.active && (
                <span className="ml-auto text-xs text-slate-400 shrink-0">retired</span>
              )}
            </Link>
          ))}
          <Link
            href={`/courses?q=${encodeURIComponent(query)}`}
            onClick={() => setOpen(false)}
            className="flex items-center gap-2 px-4 py-2 text-xs text-blue-600 hover:bg-blue-50 transition-colors"
          >
            See all results for &ldquo;{query}&rdquo; →
          </Link>
        </div>
      )}
    </div>
  );
}
