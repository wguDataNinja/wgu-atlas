// ---------------------------------------------------------------------------
// Course card — from public/data/courses.json (1,646 entries)
// ---------------------------------------------------------------------------
export interface CourseCard {
  code: string;
  title: string;
  active: boolean;
  scope: "AP" | "cert" | string;
  first_seen: string;
  last_seen: string;
  edition_count: number;
  current_college: string;
  current_program_count: number;
  stability_class: "perpetual" | "stable" | "moderate" | "ephemeral" | "single" | "cert_only" | string;
  ghost_flag: boolean;
  single_appearance_flag: boolean;
  title_variant_class: "none" | "extraction_noise" | "punctuation_only" | "wording_refinement" | "substantive_change" | "formatting_only" | string;
}

// ---------------------------------------------------------------------------
// Course detail — from public/data/courses/{code}.json (838 active AP files)
// or canonical_courses.json fallback for retired/cert-only codes
// ---------------------------------------------------------------------------
export interface ProgramTimelineEntry {
  program: string;
  first_seen: string;
}

export interface CourseDetail {
  course_code: string;
  canonical_title_current: string;
  observed_titles: string[];
  first_seen_edition: string;
  last_seen_edition: string;
  active_current: boolean;
  contexts_seen: string;
  current_college: string;
  current_programs: string[];
  current_program_count: number;
  historical_program_count: number;
  // Present in individual detail files (active AP only):
  programs_timeline?: ProgramTimelineEntry[];
  title_variant_detail?: string | null;
  notes?: string | null;
  // Present in canonical_courses.json (all courses):
  historical_programs?: string;  // semicolon-separated list for retired/cert
  notes_confidence?: string | null;
  edition_count: number;
  canonical_cus: number | null;
  stability_class: string;
  ghost_flag: boolean;
  single_appearance_flag: boolean;
  title_variant_class: string;
  current_title_confidence: string;
  colleges_seen: string[] | string;
}

// ---------------------------------------------------------------------------
// Program — from public/data/programs.json (196 entries)
// ---------------------------------------------------------------------------
export interface ProgramRecord {
  program_code: string;
  status: "ACTIVE" | "RETIRED";
  canonical_name: string;
  degree_headings: string[];
  first_seen: string;
  last_seen: string;
  edition_count: number;
  version_changes: number;
  version_progression: string;
  colleges: string[];
  cus_values: number[];
  school: string;
}

// ---------------------------------------------------------------------------
// Program enriched — from public/data/program_enriched.json
// Extracted from 2026-03 catalog text: descriptions, rosters, outcomes
// ---------------------------------------------------------------------------
export interface RosterCourse {
  term: number;
  code: string;
  title: string;
  cus: number;
}

export interface ProgramEnriched {
  program_code: string;
  description: string;
  description_source: string;
  roster: RosterCourse[];
  roster_source: string;
  outcomes: string[];
  outcomes_source: string | null;
}

// ---------------------------------------------------------------------------
// School — derived from programs.json + lineage constants
// ---------------------------------------------------------------------------
export interface SchoolLineageEntry {
  date: string;      // "YYYY-MM"
  name: string;      // School/college name at that date
  program_count?: number | null;
}

export interface SchoolRecord {
  slug: string;         // "business" | "health" | "technology" | "education"
  current_name: string;
  canonical_key: string; // matches programs.json school field
  lineage: SchoolLineageEntry[];
  historical_names: string[]; // all historical raw names (for matching courses.json)
}

// ---------------------------------------------------------------------------
// Event — from public/data/events.json (41 entries)
// ---------------------------------------------------------------------------
export interface CatalogEvent {
  event_id: string;
  start_edition: string;
  end_edition: string;
  event_title: string;
  event_type_primary: string;
  event_type_secondary: string;
  severity_score: number;
  course_churn: number;
  courses_added_count: number;
  courses_removed_count: number;
  program_churn: number;
  version_changes_count: number;
  title_changes_count: number;
  affected_schools: string;
  affected_programs_added: string;
  affected_programs_removed: string;
  affected_courses_added_sample: string;
  affected_courses_removed_sample: string;
  observed_summary: string;
  interpreted_summary: string;
  confidence: string;
  is_curated_major_event: boolean;
}

// ---------------------------------------------------------------------------
// Search index — from public/data/search_index.json (1,842 entries)
// ---------------------------------------------------------------------------
export interface SearchEntry {
  type: "course" | "program";
  code: string;
  title: string;
  active: boolean;
  scope: string;
  school: string;
  alt_titles: string[];
}

// ---------------------------------------------------------------------------
// Homepage summary — from public/data/homepage_summary.json
// ---------------------------------------------------------------------------
export interface RecentVersionChange {
  program_code: string;
  last_version_date: string;
  version_stamp: string;
  degree_heading: string;
  school: string;
}

export interface NewestProgram {
  program_code: string;
  first_seen: string;
  degree_heading: string;
  school: string;
}

export interface RecentCourseAddition {
  code: string;
  title: string;
  added_in: string;
  school: string;
}

export interface CuratedEventPreview {
  event_id: string;
  date_range: string;
  title: string;
  type: string;
  schools: string;
  summary: string;
}

export interface HomepageSummary {
  data_date: string;
  archive_span: string;
  total_editions: number;
  total_course_codes_ever: number;
  active_ap_codes: number;
  active_cert_codes: number;
  retired_ap_codes: number;
  active_programs: number;
  retired_programs: number;
  active_by_school: Record<string, number>;
  active_by_school_note: string;
  curated_major_events_count: number;
  most_recent_curated_event: string;
  recent_version_changes: RecentVersionChange[];
  newest_programs: NewestProgram[];
  recent_course_additions: RecentCourseAddition[];
  curated_major_events_preview: CuratedEventPreview[];
}

// ---------------------------------------------------------------------------
// Course description — from public/data/course_descriptions.json
// Extracted from the "Courses" section of the WGU catalog text.
// ---------------------------------------------------------------------------
export interface CourseDescription {
  title: string;        // title as it appears in the catalog (may differ slightly from canonical_title_current)
  description: string;  // official catalog prose
}

// ---------------------------------------------------------------------------
// Guide artifact — from data/program_guides/degree_artifacts/{CODE}_degree_artifact.json
// One file per program, loaded on demand at build time.
// ---------------------------------------------------------------------------

export interface GuideProvenance {
  schema_version: string;
  generated_at: string;
  source_version: string | null;
  source_pub_date: string | null;
  source_page_count: number;
  confidence: string;
}

export interface GuideQuality {
  sp_status: string;
  sp_category: string;
  aos_status: string;
  aos_course_count: number;
  caveat_flags: string[];
  caveat_messages_ui: string[];
}

export interface GuideStandardPathRow {
  title: string;
  cus: number;
  term: number | null;
}

export interface GuideStandardPath {
  available: boolean;
  partial: boolean;
  label: string | null;
  sp_display_mode?: string;
  sp_suppression_reason?: string | null;
  rows: GuideStandardPathRow[];
}

export interface GuideCourse {
  title: string;
  description: string | null;
  competency_bullets: string[];
  competency_available: boolean;
}

export interface GuideAreaOfStudy {
  group: string;
  courses: GuideCourse[];
}

export interface GuideCapstone {
  present: boolean;
  partial: boolean;
  title: string;
  description: string | null;
  competency_bullets: string[];
  competency_available: boolean;
}

export interface GuideCertSignal {
  normalized_cert: string;
  via_course_title: string;
  via_course_code: string | null;
  confidence: string;
  atlas_recommendation: string;
}

export interface GuideFamilySibling {
  program_code: string;
  track_label: string | null;
}

export interface GuideFamily {
  family_code: string;
  family_label: string;
  family_type: string;
  sp_relationship: string;
  track_label: string | null;
  display_recommendation: string;
  siblings: GuideFamilySibling[];
}

export interface GuideArtifact {
  program_code: string;
  source_degree_title: string;
  disposition: string;
  guide_provenance: GuideProvenance;
  quality: GuideQuality;
  standard_path: GuideStandardPath;
  areas_of_study: GuideAreaOfStudy[];
  capstone: GuideCapstone | null;
  cert_signals: GuideCertSignal[];
  family: GuideFamily | null;
  anomaly_flags: string[];
}

// ---------------------------------------------------------------------------
// Official resource placements — from public/data/official_resource_placements.json
// ---------------------------------------------------------------------------
export type ResourceSurface = "program_detail" | "school_detail";

export interface OfficialResourcePlacement {
  resource_url: string;
  resource_title: string;
  show_on_surface: ResourceSurface;
  surface_key: string;
  surface_label: string;
  site_area: "programs" | "schools" | string;
  placement_mode: "sidebar" | string;
  display_priority: number;
  resource_group: string;
  benefit_reason: string;
  status: "show" | "hide" | string;
}
