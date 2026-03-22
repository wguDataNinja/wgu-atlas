/**
 * coursePreviewData.ts
 *
 * Prototype-only data loader for the Session 2 course-page enrichment preview.
 * Reads from data/program_guides/ (INTERNAL_DATA) at build time.
 * Only serves the 10-course design cohort — not a production data pipeline.
 */

import fs from "fs";
import path from "path";

const INTERNAL_DATA = path.join(process.cwd(), "data");

// ---------------------------------------------------------------------------
// Cohort definition
// ---------------------------------------------------------------------------

export const COHORT_CODES = [
  "C178",
  "C480",
  "C169",
  "C165",
  "D426",
  "C170",
  "C176",
  "C824",
  "D118",
  "C216",
] as const;

export type CohortCode = (typeof COHORT_CODES)[number];

export const COHORT_META: Record<
  string,
  { shape: string; shapeNote: string; capstoneSignal: "explicit" | "title-only" | null }
> = {
  C178: {
    shape: "stable enriched + cert",
    shapeNote: "1 description, 1 competency set, CompTIA Security+",
    capstoneSignal: null,
  },
  C480: {
    shape: "stable enriched + cert + prereq",
    shapeNote: "1 description, 1 competency set, CompTIA Network+, requires D315",
    capstoneSignal: null,
  },
  C169: {
    shape: "meaningful multi-variant",
    shapeNote:
      "3 description variants (C++ in BSCS/MSCSUG, Python in BSDA), 3 competency sets — key variant-policy test",
    capstoneSignal: null,
  },
  C165: {
    shape: "cosmetic multi-variant",
    shapeNote: "2 near-identical description variants, 3 competency variants, 28+ programs",
    capstoneSignal: null,
  },
  D426: {
    shape: "reverse-prereq provider",
    shapeNote: "Is prerequisite for C170 (Data Management - Applications) and D191 (Advanced Data Management)",
    capstoneSignal: null,
  },
  C170: {
    shape: "prereq-bearing downstream",
    shapeNote: "1 stable description, 3 competency variants, requires D426",
    capstoneSignal: null,
  },
  C176: {
    shape: "cert-mapped + slight competency variance",
    shapeNote: "1 stable description, 2 competency variants, CompTIA Project+",
    capstoneSignal: null,
  },
  C824: {
    shape: "capstone + prereq",
    shapeNote: "Final course in MSN Leadership & Management program, requires C823",
    capstoneSignal: "explicit",
  },
  D118: {
    shape: "cumulative-sequence nursing",
    shapeNote:
      "Prereq is cumulative: all MSN Core + NP Core courses. Cannot be resolved to a single course code.",
    capstoneSignal: null,
  },
  C216: {
    shape: "sparse / no guide payload",
    shapeNote: "0 guide descriptions, 0 competency sets — tests sparse fallback layout",
    capstoneSignal: "title-only",
  },
};

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type EnrichmentDescription = {
  text: string;
  char_length: number;
  source_guides: string[];
  source_program_codes: string[];
};

export type CompetencySet = {
  bullets: string[];
  source_guides: string[];
  source_program_codes: string[];
};

export type CertSignal = {
  normalized_cert: string;
  matched_course_code: string;
  source_programs: string[];
  confidence: string;
  atlas_recommendation: string;
};

export type PrereqSignal = {
  prereq_value: string;
  prereq_type:
    | "explicit-course-prereq"
    | "code-anchored-prereq"
    | "cumulative-sequence-prereq"
    | "inverted-capture";
  normalized_prereq_title: string | null;
  normalized_prereq_code: string | null;
  confidence: string;
  review_status: string;
  notes: string | null;
  source_programs: string[];
};

export type ReversePrereqEntry = {
  target_code: string;
  target_title: string;
  source_programs: string[];
};

export type CoursePreviewEnrichment = {
  courseCode: string;
  descriptions: EnrichmentDescription[];
  competency_sets: CompetencySet[];
  cert: CertSignal | null;
  prereq: PrereqSignal | null;
  reverse_prereqs: ReversePrereqEntry[];
  shape: string;
  shapeNote: string;
  capstoneSignal: "explicit" | "title-only" | null;
};

// ---------------------------------------------------------------------------
// Internal JSON types (raw file shapes)
// ---------------------------------------------------------------------------

type RawCandidate = {
  course_code: string;
  descriptions: EnrichmentDescription[];
  competency_sets: CompetencySet[];
};

type RawCandidatesFile = {
  courses: RawCandidate[];
};

type RawCertEntry = {
  normalized_cert: string;
  matched_course_code: string;
  source_programs: string[];
  confidence: string;
  atlas_recommendation: string;
};

type RawCertFile = {
  auto_accepted: RawCertEntry[];
};

type RawPrereqEntry = {
  prereq_value: string;
  prereq_type: string;
  normalized_prereq_title: string | null;
  normalized_prereq_code: string | null;
  confidence: string;
  review_status: string;
  notes: string | null;
  target_course_title: string;
  target_course_code: string;
  source_programs: string[];
};

type RawPrereqFile = {
  auto_accepted: RawPrereqEntry[];
  review_needed: RawPrereqEntry[];
};

// ---------------------------------------------------------------------------
// Loading
// ---------------------------------------------------------------------------

function readJson<T>(relPath: string): T {
  const full = path.join(INTERNAL_DATA, relPath);
  return JSON.parse(fs.readFileSync(full, "utf-8")) as T;
}

let _cache: Record<string, CoursePreviewEnrichment> | null = null;

export function getCohortEnrichment(): Record<string, CoursePreviewEnrichment> {
  if (_cache) return _cache;

  const cohortSet = new Set<string>(COHORT_CODES);

  // Load candidates (extract only cohort courses to avoid parsing 88k lines into memory repeatedly)
  const candidates = readJson<RawCandidatesFile>(
    "program_guides/enrichment/course_enrichment_candidates.json"
  );
  const candidateMap: Record<string, RawCandidate> = {};
  for (const c of candidates.courses) {
    if (cohortSet.has(c.course_code)) {
      candidateMap[c.course_code] = c;
    }
  }

  // Load cert mapping (auto_accepted only — these are the 9 high-confidence certs)
  const certFile = readJson<RawCertFile>("program_guides/cert_course_mapping.json");
  const certMap: Record<string, CertSignal> = {};
  for (const entry of certFile.auto_accepted) {
    if (cohortSet.has(entry.matched_course_code)) {
      certMap[entry.matched_course_code] = {
        normalized_cert: entry.normalized_cert,
        matched_course_code: entry.matched_course_code,
        source_programs: entry.source_programs,
        confidence: entry.confidence,
        atlas_recommendation: entry.atlas_recommendation,
      };
    }
  }

  // Load prereq relationships (both auto_accepted and review_needed for the cohort)
  const prereqFile = readJson<RawPrereqFile>("program_guides/prereq_relationships.json");
  const allPrereqRows: RawPrereqEntry[] = [
    ...prereqFile.auto_accepted,
    ...prereqFile.review_needed,
  ];

  // Forward prereqs: what does a cohort course require?
  const prereqForward: Record<string, PrereqSignal> = {};
  // Reverse prereqs: what courses does a cohort course unlock?
  const prereqReverse: Record<string, ReversePrereqEntry[]> = {};

  for (const row of allPrereqRows) {
    // Forward: cohort course is the target
    if (cohortSet.has(row.target_course_code) && !prereqForward[row.target_course_code]) {
      prereqForward[row.target_course_code] = {
        prereq_value: row.prereq_value,
        prereq_type: row.prereq_type as PrereqSignal["prereq_type"],
        normalized_prereq_title: row.normalized_prereq_title,
        normalized_prereq_code: row.normalized_prereq_code,
        confidence: row.confidence,
        review_status: row.review_status,
        notes: row.notes,
        source_programs: row.source_programs,
      };
    }
    // Reverse: cohort course is the prerequisite
    if (row.normalized_prereq_code && cohortSet.has(row.normalized_prereq_code)) {
      if (!prereqReverse[row.normalized_prereq_code]) {
        prereqReverse[row.normalized_prereq_code] = [];
      }
      prereqReverse[row.normalized_prereq_code].push({
        target_code: row.target_course_code,
        target_title: row.target_course_title,
        source_programs: row.source_programs,
      });
    }
  }

  // Build enrichment record for each cohort course
  _cache = {};
  for (const code of COHORT_CODES) {
    const candidate = candidateMap[code];
    const meta = COHORT_META[code];
    _cache[code] = {
      courseCode: code,
      descriptions: candidate?.descriptions ?? [],
      competency_sets: candidate?.competency_sets ?? [],
      cert: certMap[code] ?? null,
      prereq: prereqForward[code] ?? null,
      reverse_prereqs: prereqReverse[code] ?? [],
      shape: meta.shape,
      shapeNote: meta.shapeNote,
      capstoneSignal: meta.capstoneSignal,
    };
  }

  return _cache;
}
