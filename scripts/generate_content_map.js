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
// Load data files we'll sample
// ──────────────────────────────────────────────────────────────────────────────

const homepageSummary = readJson("public/data/homepage_summary.json");
const programs = readJson("public/data/programs.json");
const events = readJson("public/data/events.json");

const activePrograms = programs.filter((p) => p.status === "ACTIVE");
const retiredPrograms = programs.filter((p) => p.status === "RETIRED");
const curatedEvents = events.filter((e) => e.is_curated_major_event);
const otherEvents = events.filter((e) => !e.is_curated_major_event);

// ──────────────────────────────────────────────────────────────────────────────
// Read source files
// ──────────────────────────────────────────────────────────────────────────────

const navSrc = readFile("src/components/layout/Nav.tsx");
const footerSrc = readFile("src/components/layout/Footer.tsx");
const homeSrc = readFile("src/app/page.tsx");
const coursesSrc = readFile("src/app/courses/page.tsx");
const courseExplorerSrc = readFile("src/components/courses/CourseExplorer.tsx");
const programsSrc = readFile("src/app/programs/page.tsx");
const programExplorerSrc = readFile("src/components/programs/ProgramExplorer.tsx");
const programDetailSrc = readFile("src/app/programs/[code]/page.tsx");
const schoolsSrc = readFile("src/app/schools/page.tsx");
const schoolDetailSrc = readFile("src/app/schools/[slug]/page.tsx");
const timelineSrc = readFile("src/app/timeline/page.tsx");
const methodsSrc = readFile("src/app/methods/page.tsx");
const dataSrc = readFile("src/app/data/page.tsx");
const homeSearchSrc = readFile("src/components/home/HomeSearch.tsx");
const courseDetailSrc = readFile("src/app/courses/[code]/page.tsx");

// ──────────────────────────────────────────────────────────────────────────────
// OUTPUT
// ──────────────────────────────────────────────────────────────────────────────

console.log("WGU ATLAS — FULL SITE CONTENT MAP");
console.log("Generated: " + new Date().toISOString());
console.log("Purpose: Proofreading reference. Shows all visible text with source locations.");

// ══════════════════════════════════════════════════════════════════════════════
header("GLOBAL LAYOUT (every page)");
// ══════════════════════════════════════════════════════════════════════════════

header("Top Navigation Bar", 2);
console.log(`${src("src/components/layout/Nav.tsx")}`);
blank();
item("Brand / Logo", "WGU Atlas", line("src/components/layout/Nav.tsx", findLine(navSrc, "WGU Atlas")));
blank();
console.log("  Primary Links (student-facing):");
console.log("    Home  |  Courses  |  Programs  |  Schools  |  Compare");
console.log(`  ${line("src/components/layout/Nav.tsx", findLine(navSrc, "primaryLinks"))}`);
blank();
console.log("  Secondary Links (archive/meta):");
console.log("    Timeline  |  Methods  |  Data");
console.log(`  ${line("src/components/layout/Nav.tsx", findLine(navSrc, "secondaryLinks"))}`);

header("Footer", 2);
console.log(`${src("src/components/layout/Footer.tsx")}`);
blank();
console.log("  Column 1 — About:");
item("  Title", "WGU Atlas", line("src/components/layout/Footer.tsx", findLine(footerSrc, "WGU Atlas")));
item("  Byline", "Created by WGU-DataNinja");
item("  Note", "An independent community project. Not affiliated with WGU.");
blank();
console.log("  Column 2 — Data:");
item("  Label", "Data");
item("  Archive span", "Catalog archive: 2017-01 → 2026-03");
item("  Site data", `Site data: {dataDate}  (dynamic — from homepage_summary.json → data_date: "${homepageSummary.data_date}")`);
item("  Links", "Methods & caveats  ·  Download datasets");
blank();
console.log("  Column 3 — Disclaimer:");
item("  Text", "All data is derived from WGU's publicly available course catalog. Catalog dates reflect publication, not student rollout timing.");

// ══════════════════════════════════════════════════════════════════════════════
header("HOME PAGE  (/)", 1);
console.log(`${src("src/app/page.tsx")}`);
// ══════════════════════════════════════════════════════════════════════════════

header("Hero Section", 2);
item("H1 Title", "WGU Atlas", line("src/app/page.tsx", findLine(homeSrc, "WGU Atlas")));
item("Subtitle", "Search courses, programs, and WGU catalog history", line("src/app/page.tsx", findLine(homeSrc, "Search courses, programs")));

header("Search Bar (HomeSearch component)", 2);
console.log(`${src("src/components/home/HomeSearch.tsx")}`);
item("Placeholder", "Search by course code or title…", line("src/components/home/HomeSearch.tsx", findLine(homeSearchSrc, "Search by course code")));
item("Clear button", "✕");
item("'See all' link text", 'See all results for "{query}" →');
item("Inactive result label (course)", "retired");
item("Inactive result label (program)", "deprecated");

header("School Cards (under search bar)", 2);
console.log(`${src("src/components/home/SchoolCards.tsx")}`);
console.log("  (4 cards — school names are dynamic from data)");
console.log("  Card labels: [School current_name] + active course count");

header("Orientation Band", 2);
console.log(`${src("src/app/page.tsx")}  line ${findLine(homeSrc, "Orientation band")}`);
blank();
const orientText = `WGU Atlas is an unofficial reference built from WGU's public academic catalog. ` +
  `It covers {active_ap_codes} active courses and {active_programs} current programs across ` +
  `four schools, with history going back to {archive_span start year}. ` +
  `Use it to look up courses, browse programs, and understand how WGU's curriculum has changed over time.`;
console.log("  Paragraph:");
console.log("    " + orientText);
blank();
console.log("  Stat pills:");
item("  Pill 1", `Active courses: ${homepageSummary.active_ap_codes}  (dynamic)`);
item("  Pill 2", `Active programs: ${homepageSummary.active_programs}  (dynamic)`);
blank();
item("  Attribution line", `Data from WGU public catalog · {data_date} edition · About this data`);
item("  data_date value (current)", homepageSummary.data_date);

header("Activity Modules", 2);
console.log(`${src("src/app/page.tsx")}  line ${findLine(homeSrc, "Activity modules")}`);
blank();
console.log("  Module 1:");
item("  Title", "New Programs");
item("  Link", "See all →  (→ /programs)");
item("  Content", `Top 5 newest programs (dynamic from homepage_summary.json → newest_programs)`);
blank();
console.log("  Module 2:");
item("  Title", "New Courses");
item("  Link", "See all →  (→ /courses)");
item("  Content", `Top 6 recent course additions (dynamic from homepage_summary.json → recent_course_additions)`);
blank();
console.log("  Module 3:");
item("  Title", "Browse by School");
item("  Link", "See all →  (→ /schools)");
item("  Content", `All 4 schools by current_name + program count (dynamic)`);

header("Official WGU Resources Section", 2);
console.log(`${src("src/app/page.tsx")}  line ${findLine(homeSrc, "Official WGU Resources")}`);
blank();
item("Section H2", "Official WGU Resources");
blank();
console.log("  Link Group: Official Channels");
console.log("    WGU Website ↗  (https://www.wgu.edu)");
console.log("    WGU YouTube ↗  (https://www.youtube.com/@WGU)");
console.log("    WGU Instagram ↗  (https://www.instagram.com/westerngovernors/)");
console.log("    WGU Facebook ↗  (https://www.facebook.com/wgu.edu)");
blank();
console.log("  Link Group: Community");
console.log("    r/WGU ↗  (https://www.reddit.com/r/WGU/)");
console.log("    r/WGUIT ↗  (https://www.reddit.com/r/WGUIT/)");
console.log("    r/WGUTeaching ↗  (https://www.reddit.com/r/WGUTeaching/)");
blank();
console.log("  Link Group: Career & Support");
console.log("    WGU Career Services ↗  (https://www.wgu.edu/alumni/career-services.html)");
console.log("    WGU Partners ↗  (https://partners.wgu.edu)");
blank();
item("Disclaimer", "WGU Atlas is not affiliated with WGU. External links are provided for reference only.", line("src/app/page.tsx", findLine(homeSrc, "not affiliated with WGU. External")));

header("WGU Catalog History Section", 2);
console.log(`${src("src/app/page.tsx")}  line ${findLine(homeSrc, "WGU Catalog History")}`);
blank();
item("H2", "WGU Catalog History");
item("Link", "Full timeline →  (→ /timeline)");
item("Subtext", `Notable curriculum and structural changes drawn from {total_editions} catalog editions.`);
item("total_editions value (current)", homepageSummary.total_editions);
console.log("  Content: EventPreview component — first 4 curated major events from homepage_summary.json");
blank();

// Show the curated events preview sample
console.log("  --- Sample: Curated Events Preview (first 4) ---");
const preview = homepageSummary.curated_major_events_preview || [];
preview.slice(0, 4).forEach((ev, i) => {
  console.log(`  Event ${i + 1}: ${ev.event_title || ev.event_id}`);
  if (ev.start_edition) console.log(`    Editions: ${ev.start_edition} → ${ev.end_edition}`);
  if (ev.observed_summary) console.log(`    Observed: ${ev.observed_summary}`);
});

// ══════════════════════════════════════════════════════════════════════════════
header("COURSES PAGE  (/courses)", 1);
console.log(`${src("src/app/courses/page.tsx")}`);
// ══════════════════════════════════════════════════════════════════════════════

header("Page Header", 2);
item("H1", "Courses", line("src/app/courses/page.tsx", findLine(coursesSrc, '"Courses"')));
item("Subtext", "{activeCourses.length} active courses across WGU's four schools. Search by code or title, or filter by school.");
item("Meta description", "Search and browse WGU courses — active and retired, with catalog history for each.");

header("CourseExplorer Filters", 2);
console.log(`${src("src/components/courses/CourseExplorer.tsx")}`);
blank();
item("Search label", "Search");
item("Search placeholder", "Code or title…", line("src/components/courses/CourseExplorer.tsx", findLine(courseExplorerSrc, "Code or title")));
blank();
item("Status label", "Status");
console.log("  Status options:");
console.log("    Active only  (default)");
console.log("    Retired only");
console.log("    All");
blank();
item("Scope label", "Scope");
console.log("  Scope options:");
console.log("    AP + Cert  (default)");
console.log("    AP only");
console.log("    Cert only");
blank();
item("School label", "School");
console.log("  School options:");
console.log("    All schools  (default)");
console.log("    Business  |  Health  |  Technology  |  Education");
blank();
item("Reset button", "Reset");
item("Result count", "{n} courses  [of {total}]");
item("Empty state", "No courses match these filters.");
item("Load more button", "Show more ({n} remaining)");

// ══════════════════════════════════════════════════════════════════════════════
header("COURSE DETAIL PAGE  (/courses/[code])", 1);
console.log(`${src("src/app/courses/[code]/page.tsx")}`);
// ══════════════════════════════════════════════════════════════════════════════

header("Breadcrumb", 2);
console.log("  Courses  ›  {code}");
blank();
header("Header Badges", 2);
console.log("  {code}  |  {N} CUs  |  Active -or- Retired");
blank();
console.log("  Status badge text:");
item("  Active", "Active", line("src/app/courses/[code]/page.tsx", findLine(courseDetailSrc, '"Active"')));
item("  Retired", "Retired", line("src/app/courses/[code]/page.tsx", findLine(courseDetailSrc, '"Retired"')));
blank();
header("Section: Official Catalog History", 2);
item("H2", "Official Catalog History");
item("Source badge", "Source: WGU public catalog archive");
blank();
console.log("  Stat cards (labels):");
console.log("    First seen  |  Last seen  |  Catalog editions  |  Versions seen");
blank();
header("Section: School & Program Membership (course detail)", 2);
console.log("  (Dynamic — from course JSON data)");
console.log("  Schools seen  |  Current programs  |  Program history");
blank();
header("Observed Titles (if variant)", 2);
item("Label", "Also seen as:");
blank();
header("Back Link", 2);
item("Text", "← Back to Courses");

// ══════════════════════════════════════════════════════════════════════════════
header("PROGRAMS PAGE  (/programs)", 1);
console.log(`${src("src/app/programs/page.tsx")}`);
// ══════════════════════════════════════════════════════════════════════════════

header("Page Header", 2);
item("H1", "Programs", line("src/app/programs/page.tsx", findLine(programsSrc, '"Programs"')));
item("Subtext", `{programs.length} programs tracked across the WGU catalog archive — {activeCount} current, {retiredCount} deprecated.`);
item("Current active count (live)", activePrograms.length);
item("Current retired count (live)", retiredPrograms.length);
item("Meta description", "Browse all 196 WGU degree programs — active and deprecated — with version history and school lineage.");

header("ProgramExplorer Filters", 2);
console.log(`${src("src/components/programs/ProgramExplorer.tsx")}`);
blank();
item("Search label", "Search");
item("Search placeholder", "Program name or code…", line("src/components/programs/ProgramExplorer.tsx", findLine(programExplorerSrc, "Program name or code")));
blank();
item("Status label", "Status");
console.log("  Status options:");
console.log("    Active only  (default)");
console.log("    Deprecated only");      // Note: uses "Deprecated" not "Retired"
console.log("    All");
blank();
item("School label", "School");
console.log("  School options:");
console.log("    All schools  (default)");
console.log("    Business  |  Health Professions  |  Technology  |  Education");
blank();
item("Reset button", "Reset");
item("Result count", "{n} programs  [of {total}]");
item("Empty state", "No programs match these filters.");
item("Load more button", "Show more ({n} remaining)");
item("Row status badge (retired)", "deprecated {last_seen}");

// ══════════════════════════════════════════════════════════════════════════════
header("PROGRAM DETAIL PAGE  (/programs/[code])", 1);
console.log(`${src("src/app/programs/[code]/page.tsx")}`);
// ══════════════════════════════════════════════════════════════════════════════

header("Breadcrumb", 2);
console.log("  Programs  ›  {code}");
blank();
header("Header Badges", 2);
console.log("  {code}  |  {status badge}  |  {N} CUs");
item("  Active badge", "Current");
item("  Retired badge", "Deprecated");
blank();
header("Section: About This Program", 2);
item("H2", "About This Program");
item("Source badge", "{enriched.description_source}  (dynamic from program_enriched.json)");
item("Content", "{enriched.description}  (official catalog text, italicized blockquote)");
item("Attribution", "Official catalog text — WGU-authored. Sourced from {description_source}.");
blank();
header("Section: Official Catalog History", 2);
item("H2", "Official Catalog History");
item("Source badge", "Source: WGU public catalog archive");
blank();
console.log("  Stat cards (labels):");
console.log("    First seen  |  Last seen  |  Catalog editions  |  Version changes  |  Total CUs (latest)");
blank();
item("Sub-label: School lineage", "School lineage");
item("Sub-label: Known names", "Known names");
item("Canonical marker", "(canonical)");
blank();
header("Section: Program Learning Outcomes", 2);
item("H2", "Program Learning Outcomes");
item("Source badge", "{enriched.outcomes_source}");
item("Note", "Official WGU-authored outcomes from the catalog Program Outcomes section. Present in ERA_B catalogs (2024-08+).");
blank();
header("Section: Version History", 2);
item("H2", "Version History");
item("No changes text", "No curriculum version changes observed across catalog editions.");
item("Changes text", "{N} version change(s) observed.");
console.log("  Table headers:  Catalog date  |  Version stamp");
item("CU change note", "Total CUs changed across versions: {cus_values joined by →}");
blank();
header("Section: Course Roster", 2);
item("H2", "Course Roster ({N} courses)");
item("Source badge", "{enriched.roster_source}");
item("Note", "Term sequence and course list from the 2026-03 catalog. Click any course code to view its full catalog history.");
console.log("  Table headers:  Code  |  Title  |  CUs");
item("Term sub-header", "Term {N}");
item("Footer", "Total: {sum} CUs across {N} courses. Program total per catalog: {latestCus} CUs.");
blank();
header("Back link", 2);
item("Text", "← Back to Programs");

// ══════════════════════════════════════════════════════════════════════════════
header("SCHOOLS PAGE  (/schools)", 1);
console.log(`${src("src/app/schools/page.tsx")}`);
// ══════════════════════════════════════════════════════════════════════════════

header("Page Header", 2);
item("H1", "Schools", line("src/app/schools/page.tsx", findLine(schoolsSrc, '"Schools"')));
item("Subtext", "WGU is organized into four schools. Each school page shows its program and course catalog, lineage history, and recent activity.", line("src/app/schools/page.tsx", findLine(schoolsSrc, "WGU is organized")));
item("Attribution", `Source: WGU public catalog archive · {current year}`);

header("School Cards (SCHOOL_DESCRIPTIONS)", 2);
console.log(`${src("src/app/schools/page.tsx")}  lines 10-15`);
blank();
item("business", "Bachelor's, master's, and MBA programs in accounting, management, marketing, IT management, finance, and related fields.");
item("health", "Programs in nursing, healthcare administration, public health, health informatics, and allied health disciplines.");
item("technology", "Programs in IT, cybersecurity, software engineering, data analytics, cloud computing, and computer science.");
item("education", "Teacher preparation, educational leadership, and learning and technology programs across all grade bands.");
blank();
console.log("  Card subtext: Formerly: {historical names}  (if any)");
item("Stats", "{N} active programs  ·  {N} active courses");
item("Meta description", "Browse WGU's four schools — Business, Health, Technology, and Education — with program and course listings.");

// ══════════════════════════════════════════════════════════════════════════════
header("SCHOOL DETAIL PAGE  (/schools/[slug])", 1);
console.log(`${src("src/app/schools/[slug]/page.tsx")}`);
// ══════════════════════════════════════════════════════════════════════════════

// Read the rest of the school detail page
const schoolDetailFull = readFile("src/app/schools/[slug]/page.tsx");
header("Breadcrumb", 2);
console.log("  Schools  ›  {school.current_name}");
blank();
header("Page Header", 2);
item("H1", "{school.current_name}  (dynamic)");
item("Historical names", "Formerly known as: {historical names}  (if any)");
blank();

// Extract some of the section headings from the school detail page
const schoolSections = [];
const h2Matches = [...schoolDetailFull.matchAll(/h2[^>]*>([^<{]+)</g)];
const h3Matches = [...schoolDetailFull.matchAll(/h3[^>]*>([^<{]+)</g)];
[...h2Matches, ...h3Matches].forEach(m => {
  const text = m[1].trim();
  if (text && text.length > 2 && !text.includes("{")) schoolSections.push(text);
});

if (schoolSections.length > 0) {
  header("Detected Section Headings", 2);
  schoolSections.forEach(s => console.log(`  • ${s}`));
} else {
  // Manually list known sections from reading the file
  header("Sections", 2);
  console.log("  (Sections are dynamic — school name, programs, courses from data)");
}

item("Meta description", "WGU {school.current_name} — programs, courses, and catalog history.");

// ══════════════════════════════════════════════════════════════════════════════
header("TIMELINE PAGE  (/timeline)", 1);
console.log(`${src("src/app/timeline/page.tsx")}`);
// ══════════════════════════════════════════════════════════════════════════════

header("Page Header", 2);
item("H1", "Catalog Timeline", line("src/app/timeline/page.tsx", findLine(timelineSrc, "Catalog Timeline")));
item("Subtext", `{events.length} named catalog events across 107 edition transitions (2017–2026). Curated major events include hand-written interpretations; remaining events have machine-generated observed summaries.`);
item("events.length (current)", events.length);
item("Info note", "All entries sourced from WGU public catalog archive. Observed summaries describe what changed; interpreted summaries explain why. Confidence noted where applicable.");

header("Type Label Definitions", 2);
console.log(`${src("src/app/timeline/page.tsx")}  lines 10-19`);
blank();
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

header("Severity Labels", 2);
console.log("  score >= 300  →  Very High");
console.log("  score >= 150  →  High");
console.log("  score >= 75   →  Moderate");
console.log("  score < 75    →  Low");

header("Major Events Section", 2);
item("H2", "Major Events");
item("Subtext", `{curated.length} curated events with hand-written titles and interpretations.`);
item("curated count (current)", curatedEvents.length);
blank();
console.log("  Event card fields:");
console.log("    {start_edition} → {end_edition}  |  [type label]  |  Severity {label}  |  {confidence} confidence");
console.log("    H3: {event.event_title}");
console.log("    Observed: (label)  {event.observed_summary}");
console.log("    Interpretation: (label)  {event.interpreted_summary}");
console.log("    Schools: {affected_schools}");
console.log("    +{courses_added_count} / −{courses_removed_count} courses");
console.log("    {version_changes_count} version changes  (if > 0)");
console.log("    {title_changes_count} title changes  (if > 0)");

header("All Catalog Events Section", 2);
item("H2", "All Catalog Events");
item("Subtext", `{other.length} additional threshold-crossing transitions with observed summaries.`);
item("other count (current)", otherEvents.length);

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
console.log(`${src("src/app/methods/page.tsx")}`);
// ══════════════════════════════════════════════════════════════════════════════

item("H1", "Methods & Caveats", line("src/app/methods/page.tsx", findLine(methodsSrc, "Methods")));
item("Subtext", "How this data was collected, validated, and how to interpret it correctly.");
item("Meta description", "How WGU Atlas data was collected, validated, and interpreted — archive coverage, parser eras, and trust caveats.");
blank();

header("Section: Archive Coverage", 2);
item("H2", "Archive Coverage");
console.log(`\n  WGU Atlas is built from 108 public WGU catalog editions spanning`);
console.log(`  January 2017 through March 2026. Three editions are absent from`);
console.log(`  the archive (2017-02, 2017-04, 2017-06), likely never published as separate`);
console.log(`  snapshots on the WGU public catalog page.`);
console.log(`\n  Each edition represents a distinct published snapshot of WGU's public course`);
console.log(`  catalog. The parser extracts course codes, titles, program memberships, and`);
console.log(`  structural metadata from each edition.`);
console.log(`\n  ${line("src/app/methods/page.tsx", findLine(methodsSrc, "Archive Coverage"))}`);

header("Section: Parser Eras", 2);
item("H2", "Parser Eras");
console.log(`\n  The WGU catalog underwent a structural formatting change in mid-2024. Two`);
console.log(`  parser eras are recognized:`);
console.log(`\n  • ERA_A: 2017-01 through 2024-07 — original catalog structure`);
console.log(`  • ERA_B: 2024-08 through 2026-03 — updated catalog structure`);
console.log(`\n  The active parser (parse_catalog_v11.py) handles both eras. A full archive`);
console.log(`  run produces 0 skipped editions and 0 body-parse anomalies.`);
console.log(`\n  ${line("src/app/methods/page.tsx", findLine(methodsSrc, "Parser Eras"))}`);

header("Section: Validation", 2);
item("H2", "Validation");
console.log(`\n  The 2026-03 edition serves as the trusted reference baseline. It was validated`);
console.log(`  deeply after an initial scrape returned incomplete results (696 AP codes vs.`);
console.log(`  the correct 838). The discrepancy was traced, corrected, and verified.`);
console.log(`\n  14 structurally critical editions — breakpoints where the parser or catalog`);
console.log(`  structure changed — were individually validated. All 14 passed clean.`);
console.log(`\n  [Callout box] The 696 → 838 correction is an important part of this project's trust story.`);
console.log(`  The current counts are hard-won and verified, not taken at face value from`);
console.log(`  the first parser run.`);
console.log(`\n  ${line("src/app/methods/page.tsx", findLine(methodsSrc, "Validation"))}`);

header("Section: Observed vs. Inferred", 2);
item("H2", "Observed vs. Inferred");
console.log(`\n  WGU Atlas distinguishes between observed facts and inferred relationships:`);
console.log(`\n  • Observed: directly present in the catalog archive — course code,`);
console.log(`    title, program membership, edition dates`);
console.log(`  • Inferred: derived from patterns across editions — event types,`);
console.log(`    event interpretations, stability classifications`);
console.log(`\n  Interpretive content (event interpretations, title variant classifications) is`);
console.log(`  labeled with confidence levels: high, moderate, or tentative.`);
console.log(`\n  ${line("src/app/methods/page.tsx", findLine(methodsSrc, "Observed vs. Inferred"))}`);

header("Section: Title Variant Classification", 2);
item("H2", "Title Variant Classification");
console.log(`\n  167 course codes show title variation across editions. These have been manually`);
console.log(`  classified into categories:`);
console.log(`\n  • Extraction noise (145 codes, 87%) — PDF line-wrap, Unicode variants, catalog oscillations. Not real renames.`);
console.log(`  • Punctuation only (16) — hyphen, comma, em-dash changes.`);
console.log(`  • Wording refinement (3) — typo fix or minor synonym swap.`);
console.log(`  • Substantive change (2) — genuine semantic renames.`);
console.log(`  • Formatting only (1) — space insertion.`);
console.log(`\n  The overwhelming majority of apparent title variation is extraction artifact,`);
console.log(`  not editorial intent.`);
console.log(`\n  ${line("src/app/methods/page.tsx", findLine(methodsSrc, "Title Variant Classification"))}`);

header("Section: Key Caveats", 2);
item("H2", "Key Caveats");
console.log(`\n  Caveat 1: Catalog date ≠ implementation date`);
console.log(`    The catalog reflects publication timing, not guaranteed student rollout.`);
console.log(`    A course appearing in a March catalog may have been deployed to students earlier or later.`);
console.log(`\n  Caveat 2: Catalog presence ≠ lived experience`);
console.log(`    Official structure does not perfectly capture actual student pathways or`);
console.log(`    the subjective experience of a course.`);
console.log(`\n  Caveat 3: Code change ≠ substantive change`);
console.log(`    Course code changes may reflect renumbering, administrative reorganization,`);
console.log(`    or cleanup — not necessarily changes to course content.`);
console.log(`\n  Caveat 4: Reddit is supplementary context`);
console.log(`    Student discussion data (planned for v1.1) is useful context, not`);
console.log(`    institutional truth. WGU Atlas keeps official catalog facts and discussion`);
console.log(`    signals in clearly separate sections.`);
console.log(`\n  Caveat 5: One-off courses require caution`);
console.log(`    Courses with only 1–2 catalog appearances are flagged (ghost_flag,`);
console.log(`    single_appearance_flag). These may represent data anomalies or genuinely`);
console.log(`    short-lived entries.`);
console.log(`\n  ${line("src/app/methods/page.tsx", findLine(methodsSrc, "Key Caveats"))}`);

header("Section: Data Separation Policy", 2);
item("H2", "Data Separation Policy");
console.log(`\n  WGU Atlas enforces a strict separation between three information types:`);
console.log(`\n  • Official catalog facts — from the WGU public catalog archive`);
console.log(`  • Discussion signals — from Reddit and community spaces (v1.1)`);
console.log(`  • LLM-generated summaries — clearly labeled with date, source count, and disclaimer (v1.1)`);
console.log(`\n  These three types are never mixed in the same field or presented as equivalent.`);
console.log(`\n  ${line("src/app/methods/page.tsx", findLine(methodsSrc, "Data Separation Policy"))}`);

// ══════════════════════════════════════════════════════════════════════════════
header("DATA PAGE  (/data)", 1);
console.log(`${src("src/app/data/page.tsx")}`);
// ══════════════════════════════════════════════════════════════════════════════

item("H1", "Data", line("src/app/data/page.tsx", findLine(dataSrc, '"Data"')));
item("Subtext", `Download the canonical datasets behind WGU Atlas. All files reflect the {data_date} catalog baseline.`);
item("data_date (current)", homepageSummary.data_date);
item("Archive line", `Archive span: {archive_span} · {total_editions} editions · {total_course_codes_ever} total course codes ever seen`);
item("archive_span (current)", homepageSummary.archive_span);
item("total_editions (current)", homepageSummary.total_editions);
item("total_course_codes_ever (current)", homepageSummary.total_course_codes_ever);
item("Meta description", "Download WGU Atlas canonical datasets — course history, named events, title variant classification.");

header("Section: Canonical Datasets (CSV)", 2);
item("H2", "Canonical Datasets (CSV)");
blank();
console.log("  Dataset 1:");
item("  Label", "Canonical Course Table");
item("  Description", "1,646-row table covering all course codes ever seen in the archive. Includes active/retired status, title variant classification, stability class, program counts, and confidence notes.");
item("  Format", "CSV  |  1,646 rows");
item("  File", "canonical_courses.csv");
blank();
console.log("  Dataset 2:");
item("  Label", "Named Catalog Events");
item("  Description", "41 named events (all threshold-crossing transitions). Includes event type, severity score, affected schools/programs/courses, observed and interpreted summaries, confidence, and curated-event flag.");
item("  Format", "CSV  |  41 rows");
item("  File", "named_events.csv");
blank();
console.log("  Dataset 3:");
item("  Label", "Title Variant Classification");
item("  Description", "167 course codes with title variation across editions, each classified by variant type: extraction noise, punctuation only, wording refinement, substantive change, or formatting only.");
item("  Format", "CSV  |  167 rows");
item("  File", "title_variant_classification.csv");

header("Section: Site-Ready JSON Exports", 2);
item("H2", "Site-Ready JSON Exports");
item("Intro text", "The same JSON files that power the WGU Atlas frontend. Provided for transparency and for developers who want to build on the data.");
blank();
console.log("  Export 1:");
item("  Label", "Course Cards (full list)");
item("  Description", "1,646 course cards with code, title, status, scope, school, edition count, stability class, and flags. Used by the course explorer.");
item("  File", "courses.json  |  712 KB");
blank();
console.log("  Export 2:");
item("  Label", "Events (full)");
item("  Description", "41 events in full JSON form with all fields including course/program sample lists.");
item("  File", "events.json  |  48 KB");
blank();
console.log("  Export 3:");
item("  Label", "Search Index");
item("  Description", "1,842-entry search index covering all courses and programs, with alt_titles for search matching.");
item("  File", "search_index.json  |  392 KB");

header("Section: Schema Notes", 2);
item("H2", "Schema Notes");
console.log(`
  stability_class — Classifies a course by its persistence across editions:
    perpetual (all 108 editions), stable, moderate, ephemeral, single (1 edition), cert_only.

  ghost_flag — True for retired AP courses with ≤2 catalog appearances.
    These may represent data anomalies or genuinely short-lived entries.

  title_variant_class — Classification of title variation across editions.
    extraction_noise accounts for 87% of apparent title variation and does
    not represent intentional renames.

  programs_timeline (in individual course JSON files) — Lists programs by raw
    degree heading text, not by program code. Minor wording variations across
    editions may exist.

  Full field definitions are in docs/ATLAS_SPEC.md in the GitHub repository.`);
console.log(`\n  ${line("src/app/data/page.tsx", findLine(dataSrc, "Schema Notes"))}`);

// ══════════════════════════════════════════════════════════════════════════════
header("SEO / PAGE METADATA SUMMARY", 1);
// ══════════════════════════════════════════════════════════════════════════════

console.log("\n  Route               Title                          Meta Description");
console.log("  " + "-".repeat(90));
console.log("  /                   WGU Atlas                      (from layout.tsx)");
console.log("  /courses            Courses                        Search and browse WGU courses — active and retired, with catalog history for each.");
console.log("  /programs           Programs                       Browse all 196 WGU degree programs — active and deprecated — with version history and school lineage.");
console.log("  /schools            Schools                        Browse WGU's four schools — Business, Health, Technology, and Education — with program and course listings.");
console.log("  /compare            Compare Programs               Compare WGU degree program course rosters side by side. See shared courses, track-specific courses, and overlap metrics.");
console.log("  /timeline           Timeline                       Major WGU catalog events from 2017 to 2026 — school reorganizations, mass course changes, program additions, and more.");
console.log("  /methods            Methods                        How WGU Atlas data was collected, validated, and interpreted — archive coverage, parser eras, and trust caveats.");
console.log("  /data               Data                           Download WGU Atlas canonical datasets — course history, named events, title variant classification.");
console.log("  /courses/[code]     {code} — {title}               {title} ({code}). Active/Retired WGU course — {N} programs, first offered {date}.");
console.log("  /programs/[code]    {program name}                 WGU program history for {name}. First seen {date}, {N} version changes tracked.");
console.log("  /schools/[slug]     {school name}                  WGU {school name} — programs, courses, and catalog history.");

// ══════════════════════════════════════════════════════════════════════════════
header("END OF CONTENT MAP", 1);
// ══════════════════════════════════════════════════════════════════════════════

console.log("\n  To edit content, find the [source: path:line] reference above each item.");
console.log("  Static text → edit the .tsx file directly.");
console.log("  Dynamic data (labeled 'dynamic') → sourced from public/data/*.json files.");
console.log("  School descriptions → src/app/schools/page.tsx  lines 10-15");
console.log("  Nav links → src/components/layout/Nav.tsx  lines 6-17");
console.log("  Footer text → src/components/layout/Footer.tsx");
console.log("");
