#!/usr/bin/env node
/**
 * generate_content_map.js
 *
 * Produces a single proofreading document of all visible text content
 * on WGU Atlas, organized by page/section with source file:line references.
 *
 * Usage:
 *   node scripts/generate_content_map.js
 *   node scripts/generate_content_map.js > content_map.txt
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");

// ──────────────────────────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────────────────────────

function readFile(relPath) {
  return fs.readFileSync(path.join(ROOT, relPath), "utf8");
}

function readJson(relPath) {
  return JSON.parse(readFile(relPath));
}

function src(relPath) {
  return `  [source: ${relPath}]`;
}

function line(relPath, lineNum) {
  return `  [source: ${relPath}:${lineNum}]`;
}

/** Find the 1-based line number of the first occurrence of a substring. */
function findLine(content, substring) {
  const idx = content.indexOf(substring);
  if (idx === -1) return "?";
  return content.slice(0, idx).split("\n").length;
}

/** Print a section header */
function header(title, level = 1) {
  const bar = "=".repeat(70);
  const dash = "-".repeat(70);
  if (level === 1) {
    console.log("\n" + bar);
    console.log(`  ${title.toUpperCase()}`);
    console.log(bar);
  } else if (level === 2) {
    console.log("\n" + dash);
    console.log(`  ${title}`);
    console.log(dash);
  } else {
    console.log(`\n  >> ${title}`);
  }
}

function item(label, value, sourceNote = "") {
  const val = value != null ? String(value).trim() : "(dynamic — from JSON data)";
  console.log(`  ${label}: ${val}`);
  if (sourceNote) console.log(`  ${sourceNote}`);
}

function blank() {
  console.log("");
}

// ──────────────────────────────────────────────────────────────────────────────
// Load data files
// ──────────────────────────────────────────────────────────────────────────────

const homepageSummary = readJson("public/data/homepage_summary.json");
const programs = readJson("public/data/programs.json");
const events = readJson("public/data/events.json");
const programEnriched = readJson("public/data/program_enriched.json");

const activePrograms = programs.filter((p) => p.status === "ACTIVE");
const retiredPrograms = programs.filter((p) => p.status === "RETIRED");
const curatedEvents = events.filter((e) => e.is_curated_major_event);
const otherEvents = events.filter((e) => !e.is_curated_major_event);

// ──────────────────────────────────────────────────────────────────────────────
// Read source files
// ──────────────────────────────────────────────────────────────────────────────

const navSrc           = readFile("src/components/layout/Nav.tsx");
const footerSrc        = readFile("src/components/layout/Footer.tsx");
const layoutSrc        = readFile("src/app/layout.tsx");
const homeSrc          = readFile("src/app/page.tsx");
const schoolCardsSrc   = readFile("src/components/home/SchoolCards.tsx");
const homeSearchSrc    = readFile("src/components/home/HomeSearch.tsx");
const coursesSrc       = readFile("src/app/courses/page.tsx");
const courseExplorerSrc = readFile("src/components/courses/CourseExplorer.tsx");
const courseDetailSrc  = readFile("src/app/courses/[code]/page.tsx");
const programsSrc      = readFile("src/app/programs/page.tsx");
const programExplorerSrc = readFile("src/components/programs/ProgramExplorer.tsx");
const programDetailSrc = readFile("src/app/programs/[code]/page.tsx");
const schoolsSrc       = readFile("src/app/schools/page.tsx");
const schoolDetailSrc  = readFile("src/app/schools/[slug]/page.tsx");
const compareSrc       = readFile("src/app/compare/page.tsx");
const compareSelectorSrc = readFile("src/components/compare/CompareSelector.tsx");
const compareViewSrc   = readFile("src/components/compare/CompareView.tsx");
const aboutSrc         = readFile("src/app/about/page.tsx");
const timelineSrc      = readFile("src/app/timeline/page.tsx");
const methodsSrc       = readFile("src/app/methods/page.tsx");
const dataSrc          = readFile("src/app/data/page.tsx");

// ──────────────────────────────────────────────────────────────────────────────
// OUTPUT
// ──────────────────────────────────────────────────────────────────────────────

console.log("WGU ATLAS — FULL SITE CONTENT MAP");
console.log("Generated: " + new Date().toISOString());
console.log("Purpose: Proofreading reference. Shows all visible text with source locations.");

// ══════════════════════════════════════════════════════════════════════════════
header("GLOBAL LAYOUT (every page)");
// ══════════════════════════════════════════════════════════════════════════════

header("Site Metadata (layout.tsx)", 2);
console.log(src("src/app/layout.tsx"));
item("Default title", "WGU Atlas");
item("Title template", "%s | WGU Atlas");
item("Meta description", "An independent guide to WGU degrees, courses, and schools, built from public WGU sources.");

header("Top Navigation Bar", 2);
console.log(src("src/components/layout/Nav.tsx"));
blank();
item("Brand / Logo", "WGU Atlas");
blank();
console.log("  Primary Links:");
console.log("    Home  |  Courses  |  Degrees  |  Schools  |  Compare Degrees  |  About");
console.log(`  ${line("src/components/layout/Nav.tsx", findLine(navSrc, "primaryLinks"))}`);
blank();
console.log("  Note: Timeline, Methods, and Data are NOT in top nav.");
console.log("  They are accessible from the About page (/about).");

header("Footer", 2);
console.log(src("src/components/layout/Footer.tsx"));
blank();
console.log("  Column 1 — About:");
item("  Title", "WGU Atlas");
item("  Byline", "Created by WGU-DataNinja");
item("  Note", "An independent community project. Not affiliated with WGU.");
blank();
console.log("  Column 2 — Data:");
item("  Archive span", "Catalog archive: 2017-01 → 2026-03");
item("  Site data", `Site data: {dataDate}  (dynamic — data_date: "${homepageSummary.data_date}")`);
item("  Links", "Methods & caveats  ·  Download datasets");
blank();
console.log("  Column 3 — Disclaimer:");
item("  Text", "All data is derived from WGU's publicly available course catalog. Catalog dates reflect publication, not student rollout timing.");

// ══════════════════════════════════════════════════════════════════════════════
header("HOME PAGE  (/)", 1);
console.log(src("src/app/page.tsx"));
// ══════════════════════════════════════════════════════════════════════════════

header("Hero Section", 2);
item("H1 Title", "WGU Atlas", line("src/app/page.tsx", findLine(homeSrc, "WGU Atlas")));
item("Subtitle", "Explore WGU degrees, courses, and schools. Compare related degrees.", line("src/app/page.tsx", findLine(homeSrc, "Explore WGU degrees")));

header("Search Bar (HomeSearch component)", 2);
console.log(src("src/components/home/HomeSearch.tsx"));
item("Placeholder", "Search by course code or title…", line("src/components/home/HomeSearch.tsx", findLine(homeSearchSrc, "Search by course code")));
item("Inactive result label (course)", "retired");
item("Inactive result label (degree)", "retired");

header("School Cards (under search bar)", 2);
console.log(src("src/components/home/SchoolCards.tsx"));
blank();
console.log("  Four cards, each with: school name, description, 'Explore [School] →' CTA");
blank();
item("Business description", "Bachelor's, master's, and MBA degrees in accounting, management, marketing, IT management, finance, and related fields.");
item("Health description", "Degrees in nursing, healthcare administration, public health, health informatics, and allied health disciplines.");
item("Technology description", "Degrees in IT, cybersecurity, software engineering, data analytics, cloud computing, and computer science.");
item("Education description", "Teacher preparation, educational leadership, and learning and technology degrees across all grade bands.");
blank();
console.log("  CTA format: 'Explore [School Name] →'");
console.log(`  ${line("src/components/home/SchoolCards.tsx", findLine(schoolCardsSrc, "Explore"))}`);

header("Orientation Paragraph", 2);
console.log(src("src/app/page.tsx"));
blank();
const orientText = "WGU Atlas is an independent guide to WGU degrees, courses, and schools, built from public WGU sources. " +
  "It helps students explore degree options, compare related degrees, and understand changes over time when those changes matter to what they're viewing.";
console.log("  " + orientText);
console.log(`  ${line("src/app/page.tsx", findLine(homeSrc, "independent guide"))}`);

header("Compare Callout", 2);
console.log(src("src/app/page.tsx"));
blank();
item("Label", "Compare degrees");
item("Description", "See how related WGU degrees differ — course rosters, shared courses, and track-specific requirements.");
item("Link", "Compare degrees →  (→ /compare)");
console.log(`  ${line("src/app/page.tsx", findLine(homeSrc, "Compare degrees"))}`);

header("Attribution Line", 2);
item("Text", "Built from WGU's public catalog · Updated through March 2026 · About this site");
item("'About this site' link", "→ /about");
console.log(`  ${line("src/app/page.tsx", findLine(homeSrc, "public catalog"))}`);

// ══════════════════════════════════════════════════════════════════════════════
header("COURSES PAGE  (/courses)", 1);
console.log(src("src/app/courses/page.tsx"));
// ══════════════════════════════════════════════════════════════════════════════

header("Page Header", 2);
item("H1", "Courses", line("src/app/courses/page.tsx", findLine(coursesSrc, '"Courses"')));
item("Meta description", "Search and browse WGU courses — active and retired, with catalog history for each.");

header("CourseExplorer Filters", 2);
console.log(src("src/components/courses/CourseExplorer.tsx"));
blank();
item("Search placeholder", "Code or title…", line("src/components/courses/CourseExplorer.tsx", findLine(courseExplorerSrc, "Code or title")));
blank();
item("Status label", "Status");
console.log("  Status options:");
console.log("    Active only  (default)");
console.log("    Retired only");
console.log("    All");
blank();
item("Scope label", "Scope");
console.log("  Scope options:  AP + Cert (default)  |  AP only  |  Cert only");
blank();
item("School label", "School");
console.log("  School options:  All schools (default)  |  Business  |  Health  |  Technology  |  Education");
blank();
item("Reset button", "Reset");
item("Result count", "{n} courses  [of {total}]");
item("Empty state", "No courses match these filters.");
item("Load more", "Show more ({n} remaining)");

// ══════════════════════════════════════════════════════════════════════════════
header("COURSE DETAIL PAGE  (/courses/[code])", 1);
console.log(src("src/app/courses/[code]/page.tsx"));
// ══════════════════════════════════════════════════════════════════════════════

header("Breadcrumb", 2);
console.log("  Courses  ›  {code}");
blank();
header("Header Badges", 2);
console.log("  {code}  |  {N} CUs  |  Active -or- Retired");
item("  Active badge", "Active", line("src/app/courses/[code]/page.tsx", findLine(courseDetailSrc, '"Active"')));
item("  Retired badge", "Retired", line("src/app/courses/[code]/page.tsx", findLine(courseDetailSrc, '"Retired"')));

header("Section: Catalog History", 2);
item("H2", "Catalog History");
item("Source badge", "Source: WGU public catalog archive");
console.log("  Stat cards:  First in catalog  |  Last in catalog  |  Editions present  |  Catalog presence");

header("Back Link", 2);
item("Text", "← Back to Course Explorer");

// ══════════════════════════════════════════════════════════════════════════════
header("DEGREES PAGE  (/programs)", 1);
console.log(src("src/app/programs/page.tsx"));
// ══════════════════════════════════════════════════════════════════════════════

header("Page Header", 2);
item("H1", "Degrees", line("src/app/programs/page.tsx", findLine(programsSrc, '"Degrees"')));
item("Subtext", `{programs.length} degrees tracked across the WGU catalog — {activeCount} current, {retiredCount} retired.`);
item("Current count (live)", activePrograms.length);
item("Retired count (live)", retiredPrograms.length);
item("Meta description", "Browse all WGU degrees — current and retired — with changes over time and school history.");

header("ProgramExplorer Filters", 2);
console.log(src("src/components/programs/ProgramExplorer.tsx"));
blank();
item("Search placeholder", "Degree name or code…", line("src/components/programs/ProgramExplorer.tsx", findLine(programExplorerSrc, "Degree name or code")));
blank();
item("Status control", "Checkbox: Include retired degrees  (default: unchecked = current degrees only)");
console.log(`  ${line("src/components/programs/ProgramExplorer.tsx", findLine(programExplorerSrc, "Include retired"))}`);
blank();
item("School label", "School");
console.log("  School options:  All schools (default)  |  Business  |  Health  |  Technology  |  Education");
blank();
item("Reset button", "Reset");
item("Result count", "{n} degree(s)  [of {total}]");
item("Empty state", "No degrees match these filters.");
item("Load more", "Show more ({n} remaining)");
item("Row status badge (retired)", "retired {last_seen}");

// ══════════════════════════════════════════════════════════════════════════════
header("DEGREE DETAIL PAGE  (/programs/[code])", 1);
console.log(src("src/app/programs/[code]/page.tsx"));
// ══════════════════════════════════════════════════════════════════════════════

header("Breadcrumb", 2);
console.log("  Degrees  ›  {code}");
blank();
header("Header Badges", 2);
console.log("  {code}  |  {status badge}  |  {N} CUs");
item("  Current badge", "Current");
item("  Retired badge", "Retired", line("src/app/programs/[code]/page.tsx", findLine(programDetailSrc, '"Retired"')));
blank();
header("Section: About This Degree", 2);
item("H2", "About This Program");
item("Source badge", "{enriched.description_source}  (dynamic from program_enriched.json)");
item("Content", "{enriched.description}  (official catalog text, italicized blockquote)");
item("Attribution", "Official catalog text — WGU-authored. Sourced from {description_source}.");
blank();
header("Section: Changes Over Time", 2);
item("H2", "Changes Over Time", line("src/app/programs/[code]/page.tsx", findLine(programDetailSrc, "Changes Over Time")));
item("Source badge", "Source: WGU public catalog archive");
blank();
console.log("  Stat cards:  First seen  |  Last seen  |  Catalog editions  |  Version changes  |  Total CUs (latest)");
blank();
item("Sub-label: School name history", "Earlier names", line("src/app/programs/[code]/page.tsx", findLine(programDetailSrc, "Earlier names")));
item("Sub-label: Known names", "Known names");
item("Canonical marker", "(canonical)");
blank();
header("Section: Program Learning Outcomes", 2);
item("H2", "Program Learning Outcomes");
item("Note", "Official WGU-authored outcomes from the catalog Program Outcomes section. Present in ERA_B catalogs (2024-08+).");
blank();
header("Section: Past Versions", 2);
item("H2", "Past Versions", line("src/app/programs/[code]/page.tsx", findLine(programDetailSrc, "Past Versions")));
item("No changes text", "No curriculum version changes observed across catalog editions.");
item("Changes text", "{N} version change(s) observed.");
console.log("  Table headers:  Catalog date  |  Version stamp");
item("CU change note", "Total CUs changed across versions: {cus_values joined by →}");
blank();
header("Section: Course Roster", 2);
item("H2", "Course Roster ({N} courses)");
item("Note", "Term sequence and course list from the 2026-03 catalog. Click any course code to view its full catalog history.");
console.log("  Table headers:  Code  |  Title  |  CUs");
item("Footer", "Total: {sum} CUs across {N} courses. Program total per catalog: {latestCus} CUs.");
blank();
header("Back Link", 2);
item("Text", "← Back to Degrees", line("src/app/programs/[code]/page.tsx", findLine(programDetailSrc, "Back to Degrees")));

// ══════════════════════════════════════════════════════════════════════════════
header("SCHOOLS PAGE  (/schools)", 1);
console.log(src("src/app/schools/page.tsx"));
// ══════════════════════════════════════════════════════════════════════════════

header("Page Header", 2);
item("H1", "Schools", line("src/app/schools/page.tsx", findLine(schoolsSrc, '"Schools"')));
item("Subtext", "WGU is organized into four schools. Each school page shows its current degrees and courses, school background, and recent changes.", line("src/app/schools/page.tsx", findLine(schoolsSrc, "WGU is organized")));
item("Attribution", `Source: WGU public catalog archive · {current year}`);

header("School Cards (SCHOOL_DESCRIPTIONS)", 2);
console.log(src("src/app/schools/page.tsx"));
blank();
item("business", "Bachelor's, master's, and MBA degrees in accounting, management, marketing, IT management, finance, and related fields.");
item("health", "Degrees in nursing, healthcare administration, public health, health informatics, and allied health disciplines.");
item("technology", "Degrees in IT, cybersecurity, software engineering, data analytics, cloud computing, and computer science.");
item("education", "Teacher preparation, educational leadership, and learning and technology degrees across all grade bands.");
blank();
console.log("  Card subtext: Formerly: {historical names}  (if any)");
item("Stats", "{N} current degrees  ·  {N} active courses");
item("Meta description", "Browse WGU's four schools — Business, Health, Technology, and Education — with degree and course listings.");

// ══════════════════════════════════════════════════════════════════════════════
header("SCHOOL DETAIL PAGE  (/schools/[slug])", 1);
console.log(src("src/app/schools/[slug]/page.tsx"));
// ══════════════════════════════════════════════════════════════════════════════

header("Breadcrumb", 2);
console.log("  Schools  ›  {school.current_name}");
blank();
header("Page Sections (in order)", 2);
blank();

// Extract section headings dynamically
const h2Matches = [...schoolDetailSrc.matchAll(/h2[^>]*>([^<{]+)</g)];
const h3Matches = [...schoolDetailSrc.matchAll(/h3[^>]*>([^<{]+)</g)];
const schoolSections = [...h2Matches, ...h3Matches]
  .map((m) => m[1].trim())
  .filter((t) => t.length > 2 && !t.includes("{"));

if (schoolSections.length > 0) {
  console.log("  Section headings (from source):");
  schoolSections.forEach((s) => console.log(`    • ${s}`));
} else {
  console.log("  1. Header: {school.current_name} — N current degrees · N active courses");
  console.log("  2. Short description (from SCHOOL_DESCRIPTIONS)");
  console.log("  3. Current Degrees (N)  — grouped by degree level");
  console.log("  4. Active Courses (N)  — collapsible");
  console.log("  5. Recent Changes  — New Degrees / Recent Degree Updates / Recent Course Additions");
  console.log("  6. Retired Degrees (N)  — collapsible");
  console.log("  7. School Background  — name lineage table");
}

blank();
item("Header subtext", "{N} current degrees · {N} active courses");
item("Retired degrees toggle", "▶ Show retired degrees / ▼ Hide retired degrees");
item("Courses toggle", "▶ Show all {N} active courses / ▼ Hide course list");
item("Meta description", "WGU {school.current_name} — degrees, courses, and catalog history.");

// ══════════════════════════════════════════════════════════════════════════════
header("COMPARE DEGREES PAGE  (/compare)", 1);
console.log(src("src/app/compare/page.tsx"));
// ══════════════════════════════════════════════════════════════════════════════

header("Page Header", 2);
item("H1", "Compare Degrees", line("src/app/compare/page.tsx", findLine(compareSrc, "Compare Degrees")));
item("Description", "Select two degrees to compare their course rosters side by side. Shared courses, unique courses, and overlap metrics are shown for each comparison.");
item("Meta title", "Compare Degrees");
item("Meta description", "Compare WGU degree course rosters side by side. See shared courses, track-specific courses, and overlap metrics.");

header("CompareSelector UI", 2);
console.log(src("src/components/compare/CompareSelector.tsx"));
blank();
console.log("  Universe: active programs with non-empty rosters, excluding LAB_EXCLUSIONS (6 programs).");
console.log("  Sibling logic: same school + same degree level as the selected program (not pilot-family gated).");
blank();
console.log("  Step 1 panel:");
item("  Header", "Choose a degree", line("src/components/compare/CompareSelector.tsx", findLine(compareSelectorSrc, "Choose a degree")));
item("  Filters", "All schools (default) + All levels (default)");
item("  Empty state", "No degrees match these filters.");
item("  Footer note", "{N} degrees shown. Select one to see comparable degrees in step 2.");
blank();
console.log("  Step 2 panel:");
item("  Header", "Compare with");
item("  Prompt (before step 1)", "Select a degree in step 1 first.");
item("  No siblings text", "No comparable degrees.");
item("  No siblings sub-text", "No other degrees share the same school and level as this program.");
item("  Comparing-with label", "Comparing with: {index_name ?? canonical_name}");
item("  Footer note", "Showing degrees in the same school and level as your selection.");
blank();
console.log("  Prompt (A selected, waiting for B):");
item("  Text", "Now select a degree in step 2 to see the comparison.");
blank();
console.log("  Note: Change and Reset live in the CompareView sticky header — no compact bar.");

header("CompareView — Sticky header + lane roster", 2);
console.log(src("src/components/compare/CompareView.tsx"));
blank();
console.log("  Sticky header (sticky top-14 z-10) — spans the full compare view while scrolling:");
blank();
console.log("    Utility bar (top row, dark slate-800, top-right):");
item("    Change button", "Change  (text link, slate-300)");
item("    Reset button", "Reset  (text link, slate-400)");
blank();
console.log("    3-column lane headers (grid-cols-[1fr_2fr_1fr]):");
item("    Left column (bg-blue-600)", "{leftLabel}  /  {leftOnly} unique · {left.program_code}");
item("    Center column (bg-slate-700)", "Shared  /  {metrics.shared_count} in both");
item("    Right column (bg-amber-500)", "{rightLabel}  /  {rightOnly} unique · {right.program_code}");
blank();
console.log("  Term dividers (bg-slate-600, white bold text):");
item("  Label format", "TERM {N}  (or UNPLACED for term=0)");
item("  All-shared annotation", "all shared this term  (slate-300, when no unique courses in term)");
blank();
console.log("  Course cards (within lanes):");
item("  Left-only card", "border-l-2 border-blue-400  ·  blue-200 code badge  ·  title  ·  CU count");
item("  Shared card", "border-l-2 border-emerald-400  ·  emerald-100 code badge  ·  title  ·  drift annotation if term differs");
item("  Right-only card", "border-l-2 border-amber-400  ·  amber-200 code badge  ·  title  ·  CU count");
item("  Term-drift annotation", "↕ term {term_right} in {rightCode}  (amber-600, shown on shared cards when left/right term differs)");
blank();
console.log("  Removed vs previous version:");
console.log("    — Identity bar (left code / vs / right code section)");
console.log("    — Overlap / count strip (unique + shared counts with colored segments)");
console.log("    — Comparison source disclaimer footer");

header("Compare Universe", 2);
console.log("  (Defined in src/lib/compareUtils.ts — LAB_EXCLUSIONS)");
blank();
console.log("  Universe: active programs with non-empty rosters, same school + degree level pairing.");
console.log("  Previous: gated to 5 pilot-family codes only.");
console.log("  Current:  ~107 active programs across all 4 colleges.");
blank();
console.log("  Exclusions (6 programs hardcoded in LAB_EXCLUSIONS):");
console.log("    MSCSUG, MSITUG, MSSWEUG");
console.log("      → Pathway / bridge programs. Name starts with 'Bachelor of Science' but are");
console.log("        upper-division accelerated paths into a master's — not standalone degrees.");
console.log("    MEDETID, MEDETIDA, MEDETIDK12");
console.log("      → Identical canonical name group. All three share the exact same canonical_name.");
console.log("        No curated track_labels to disambiguate them; compare UI is unusable.");

// ══════════════════════════════════════════════════════════════════════════════
header("COMPARE SIMULATION — BSSWE vs BSSWE_C (actual data)", 1);
// ══════════════════════════════════════════════════════════════════════════════

console.log("\n  Live comparison computed from public/data/program_enriched.json");
console.log("  This mirrors what the Compare Degrees UI renders at /compare");
blank();

try {
  const bsswe = programEnriched["BSSWE"];
  const bsswe_c = programEnriched["BSSWE_C"];

  if (!bsswe || !bsswe_c) {
    console.log("  [WARNING] BSSWE or BSSWE_C not found in program_enriched.json — skipping simulation.");
  } else {
    const rosterA = bsswe.roster || [];
    const rosterB = bsswe_c.roster || [];

    const codesA = new Set(rosterA.map((c) => c.code));
    const codesB = new Set(rosterB.map((c) => c.code));

    const sharedCodes = [...codesA].filter((c) => codesB.has(c));
    const leftOnlyCodes = [...codesA].filter((c) => !codesB.has(c));
    const rightOnlyCodes = [...codesB].filter((c) => !codesA.has(c));

    const union = new Set([...codesA, ...codesB]);
    const jaccard = Math.round((sharedCodes.length / union.size) * 100);

    const totalCusA = rosterA.reduce((s, c) => s + (c.cus || 0), 0);
    const totalCusB = rosterB.reduce((s, c) => s + (c.cus || 0), 0);

    // Build lookup maps
    const mapA = Object.fromEntries(rosterA.map((c) => [c.code, c]));
    const mapB = Object.fromEntries(rosterB.map((c) => [c.code, c]));

    const leftProgram = programs.find((p) => p.program_code === "BSSWE");
    const rightProgram = programs.find((p) => p.program_code === "BSSWE_C");

    console.log("  ┌─────────────────────────────────────────────────────────────────┐");
    console.log("  │  COMPARE DEGREES: B.S. Software Engineering                     │");
    console.log("  │  B.S. Software Engineering (Java Track)  vs  (C# Track)         │");
    console.log("  └─────────────────────────────────────────────────────────────────┘");
    blank();
    console.log(`  Left:   BSSWE — ${leftProgram?.canonical_name ?? "B.S. Software Engineering"}`);
    console.log(`  Right:  BSSWE_C — ${rightProgram?.canonical_name ?? "B.S. Software Engineering"}`);
    blank();
    console.log("  Overlap Summary");
    console.log("  " + "─".repeat(50));
    console.log(`  Shared courses:      ${sharedCodes.length}`);
    console.log(`  Java-only courses:   ${leftOnlyCodes.length}`);
    console.log(`  C#-only courses:     ${rightOnlyCodes.length}`);
    console.log(`  Total courses (A):   ${rosterA.length}  (${totalCusA} CUs)`);
    console.log(`  Total courses (B):   ${rosterB.length}  (${totalCusB} CUs)`);
    console.log(`  Jaccard overlap:     ${jaccard}%  (${sharedCodes.length} shared / ${union.size} union)`);
    blank();

    // Shared courses column
    console.log("  Shared Courses (" + sharedCodes.length + ")");
    console.log("  " + "─".repeat(50));
    sharedCodes.forEach((code) => {
      const c = mapA[code];
      const termA = c.term ?? "?";
      const termB = mapB[code]?.term ?? "?";
      const driftNote = termA !== termB ? `  ← term ${termA} / term ${termB}` : `  (term ${termA})`;
      console.log(`    ${code.padEnd(10)} ${(c.title || "").slice(0, 45).padEnd(46)} ${c.cus ?? "?"}cu${driftNote}`);
    });
    blank();

    // Left-only courses
    console.log(`  Java Track Only (${leftOnlyCodes.length})`);
    console.log("  " + "─".repeat(50));
    leftOnlyCodes.forEach((code) => {
      const c = mapA[code];
      console.log(`    ${code.padEnd(10)} ${(c.title || "").slice(0, 45).padEnd(46)} ${c.cus ?? "?"}cu  (term ${c.term ?? "?"})`);
    });
    blank();

    // Right-only courses
    console.log(`  C# Track Only (${rightOnlyCodes.length})`);
    console.log("  " + "─".repeat(50));
    rightOnlyCodes.forEach((code) => {
      const c = mapB[code];
      console.log(`    ${code.padEnd(10)} ${(c.title || "").slice(0, 45).padEnd(46)} ${c.cus ?? "?"}cu  (term ${c.term ?? "?"})`);
    });
    blank();

    console.log("  Family note: Both tracks cover the same Software Engineering curriculum.");
    console.log("  The difference is the programming language: Java (with Android mobile");
    console.log("  development) or C# (.NET mobile development). 33 of the courses are identical.");
  }
} catch (e) {
  console.log("  [ERROR computing comparison]: " + e.message);
}

// ══════════════════════════════════════════════════════════════════════════════
header("ABOUT PAGE  (/about)", 1);
console.log(src("src/app/about/page.tsx"));
// ══════════════════════════════════════════════════════════════════════════════

header("Page Header", 2);
item("H1", "About WGU Atlas", line("src/app/about/page.tsx", findLine(aboutSrc, "About WGU Atlas")));
item("Subtitle", "An independent guide to WGU degrees, courses, and schools.");
item("Meta description", "About WGU Atlas — an independent guide to WGU degrees, courses, and schools, built from public WGU catalog sources.");

header("Sections", 2);
blank();
console.log("  Section 1: What is WGU Atlas?");
console.log("    WGU Atlas is an independent reference built from WGU's public academic catalog.");
console.log("    It is not affiliated with, endorsed by, or operated by Western Governors University.");
console.log("    Atlas helps students explore WGU degree options, compare related degrees, and");
console.log("    understand how degrees and courses have changed over time when those changes");
console.log("    are relevant to what they're viewing.");
blank();
console.log("  Section 2: What it covers");
console.log("    • Current degrees across WGU's four schools");
console.log("    • Course catalog with history going back to 2017");
console.log("    • Degree comparisons for related programs (pilot set)");
console.log("    • Retired degrees still visible for reference");
console.log("    • School background and earlier names over time");
blank();
console.log("  Section 3: Source and independence");
console.log("    All data is derived from WGU's publicly available course catalog, scraped and");
console.log("    parsed from 108 catalog editions spanning January 2017 through March 2026.");
console.log("    No internal WGU systems or private data were accessed.");
console.log("    Atlas is a community project. Not a substitute for official WGU advising.");
blank();
console.log("  Section 4: How history and resources are used");
console.log("    Where a degree or school has changed names or structure over time, Atlas surfaces");
console.log("    that history where relevant — earlier names on detail pages. History is secondary");
console.log("    context, not the primary lens.");
blank();
console.log("  More detail links:");
item("  Methods & Caveats", "→ /methods  — how data was collected, validated, and how to interpret it");
item("  Data", "→ /data  — download the canonical datasets behind Atlas");
item("  Timeline", "→ /timeline  — major WGU catalog events from 2017 to 2026");

// ══════════════════════════════════════════════════════════════════════════════
header("TIMELINE PAGE  (/timeline)", 1);
console.log(src("src/app/timeline/page.tsx"));
console.log("  Note: Timeline is accessible from About page and footer — NOT in top nav.");
// ══════════════════════════════════════════════════════════════════════════════

header("Page Header", 2);
item("H1", "Catalog Timeline", line("src/app/timeline/page.tsx", findLine(timelineSrc, "Catalog Timeline")));
item("events.length (current)", events.length);
item("curated events (current)", curatedEvents.length);
item("other events (current)", otherEvents.length);

header("Event Type Labels", 2);
const typeLabels = {
  rename_cleanup: "Rename / Cleanup",
  composite: "Composite",
  school_rename: "School Rename",
  program_restructure: "Program Restructure",
  expansion: "Expansion",
  cert_formalization: "Cert Formalization",
  version_review: "Version Review",
  mixed: "Mixed",
};
Object.entries(typeLabels).forEach(([k, v]) => console.log(`  ${k}  →  "${v}"`));

header("Sample: Curated Events (all)", 2);
curatedEvents.forEach((ev, i) => {
  console.log(`\n  [${i + 1}] ${ev.event_id}`);
  console.log(`      Title: ${ev.event_title || "(none)"}`);
  console.log(`      Editions: ${ev.start_edition} → ${ev.end_edition}`);
  console.log(`      Type: ${ev.event_type_primary}  |  Severity: ${ev.severity_score}`);
  if (ev.observed_summary) console.log(`      Observed: ${ev.observed_summary}`);
  if (ev.interpreted_summary) console.log(`      Interpreted: ${ev.interpreted_summary}`);
  if (ev.affected_schools) console.log(`      Schools: ${ev.affected_schools}`);
});

header("Sample: Non-Curated Events (all)", 2);
otherEvents.forEach((ev, i) => {
  console.log(`\n  [${i + 1}] ${ev.event_id}`);
  console.log(`      Editions: ${ev.start_edition} → ${ev.end_edition}`);
  console.log(`      Type: ${ev.event_type_primary}  |  Severity: ${ev.severity_score}`);
  if (ev.observed_summary) console.log(`      Observed: ${ev.observed_summary}`);
});

// ══════════════════════════════════════════════════════════════════════════════
header("METHODS PAGE  (/methods)", 1);
console.log(src("src/app/methods/page.tsx"));
console.log("  Note: Methods is accessible from About page and footer — NOT in top nav.");
// ══════════════════════════════════════════════════════════════════════════════

item("H1", "Methods & Caveats");
item("Meta description", "How WGU Atlas data was collected, validated, and interpreted — archive coverage, parser eras, and trust caveats.");
blank();
console.log("  Sections: Archive Coverage · Parser Eras · Validation · Observed vs. Inferred");
console.log("            Title Variant Classification · Key Caveats · Data Separation Policy");

// ══════════════════════════════════════════════════════════════════════════════
header("DATA PAGE  (/data)", 1);
console.log(src("src/app/data/page.tsx"));
console.log("  Note: Data is accessible from About page and footer — NOT in top nav.");
// ══════════════════════════════════════════════════════════════════════════════

item("H1", "Data", line("src/app/data/page.tsx", findLine(dataSrc, '"Data"')));
item("data_date (current)", homepageSummary.data_date);
item("archive_span (current)", homepageSummary.archive_span);
item("total_editions (current)", homepageSummary.total_editions);
item("Meta description", "Download WGU Atlas canonical datasets — course history, named events, title variant classification.");
blank();
console.log("  Downloads: canonical_courses.csv  |  named_events.csv  |  title_variant_classification.csv");
console.log("  JSON:      courses.json  |  events.json  |  search_index.json");

// ══════════════════════════════════════════════════════════════════════════════
header("SEO / PAGE METADATA SUMMARY", 1);
// ══════════════════════════════════════════════════════════════════════════════

console.log("\n  Route               Title                          Meta Description");
console.log("  " + "-".repeat(100));
console.log("  /                   WGU Atlas                      An independent guide to WGU degrees, courses, and schools, built from public WGU sources.");
console.log("  /courses            Courses                        Search and browse WGU courses — active and retired, with catalog history for each.");
console.log("  /programs           Degrees                        Browse all WGU degrees — current and retired — with changes over time and school history.");
console.log("  /schools            Schools                        Browse WGU's four schools — Business, Health, Technology, and Education — with degree and course listings.");
console.log("  /compare            Compare Degrees                Compare WGU degree course rosters side by side. See shared courses, track-specific courses, and overlap metrics.");
console.log("  /about              About                          About WGU Atlas — an independent guide to WGU degrees, courses, and schools, built from public WGU catalog sources.");
console.log("  /timeline           Timeline                       (on page — major WGU catalog events from 2017 to 2026)");
console.log("  /methods            Methods                        How WGU Atlas data was collected, validated, and interpreted — archive coverage, parser eras, and trust caveats.");
console.log("  /data               Data                           Download WGU Atlas canonical datasets — course history, named events, title variant classification.");
console.log("  /courses/[code]     {code} — {title}               WGU course {code}: {title}. Active/Retired.");
console.log("  /programs/[code]    {program name}                 WGU degree detail for {name}. First seen {date}, {N} version changes tracked.");
console.log("  /schools/[slug]     {school name}                  WGU {school name} — degrees, courses, and catalog history.");

// ══════════════════════════════════════════════════════════════════════════════
header("END OF CONTENT MAP", 1);
// ══════════════════════════════════════════════════════════════════════════════

console.log("\n  To edit content, find the [source: path:line] reference above each item.");
console.log("  Static text → edit the .tsx file directly.");
console.log("  Dynamic data (labeled 'dynamic') → sourced from public/data/*.json files.");
console.log("  School descriptions → src/app/schools/page.tsx  and  src/components/home/SchoolCards.tsx");
console.log("  Nav links → src/components/layout/Nav.tsx");
console.log("  Footer text → src/components/layout/Footer.tsx");
console.log("  Compare universe + exclusions (compare) → src/lib/compareUtils.ts");
console.log("");
