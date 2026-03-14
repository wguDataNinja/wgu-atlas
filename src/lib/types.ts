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
  programs_timeline: ProgramTimelineEntry[];
  edition_count: number;
  stability_class: string;
  ghost_flag: boolean;
  single_appearance_flag: boolean;
  title_variant_class: string;
  title_variant_detail: string | null;
  current_title_confidence: string;
  notes_confidence: string | null;
  colleges_seen: string[] | string;
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
