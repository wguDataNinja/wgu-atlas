/**
 * Degree-page review cohort — Session 1 (2026-03-22)
 * Sandboxed prototype surface at /proto/degree-preview
 * These 7 programs cover the distinct live page shapes.
 */

export const DEGREE_COHORT_CODES = [
  "BSCS",
  "BSSWE",
  "BSSESC",
  "MATSPED",
  "BSDA",
  "MEDETID",
  "BSITM",
] as const;

export type DegreeCohortCode = (typeof DEGREE_COHORT_CODES)[number];

export const DEGREE_COHORT_META: Record<
  DegreeCohortCode,
  { shape: string; shapeNote: string }
> = {
  BSCS: {
    shape: "plain baseline",
    shapeNote:
      "Full enrichment stack; zero guide extra blocks. High confidence. 37 courses, 9 terms. College rename history (CIT → School of Technology).",
  },
  BSSWE: {
    shape: "family + professional cert",
    shapeNote:
      "GuideFamilyPanel (Java Track / C# Track) + GuideCertBlock (AWS Certified, CompTIA Project+). Medium confidence — no source version/date. Loaded via BSSWE_Java artifact alias.",
  },
  BSSESC: {
    shape: "advisor-guided + licensure cert",
    shapeNote:
      "Advisor-guided roster banner + Licensure Preparation block (Praxis exam). No outcomes present — Learning Outcomes section absent. 40 courses, 9 terms.",
  },
  MATSPED: {
    shape: "suppressed SP + anomaly",
    shapeNote:
      "The only suppressed SP in the dataset. Roster section replaced by caveat message; Areas of Study is the primary content layer. Anomaly ANOM-001, medium confidence.",
  },
  BSDA: {
    shape: "capstone + professional cert",
    shapeNote:
      "GuideCapstone (Data Analytics Capstone, clean — no caveats) + GuideCertBlock (AWS Certified, CompTIA Project+). High confidence. 42 courses, 10 terms.",
  },
  MEDETID: {
    shape: "caveat capstone + anomaly",
    shapeNote:
      "Capstone partial=true (first of a multi-course sequence). Caveat appears in GuideProvenance header AND in GuideCapstone block. Anomaly ANOM-007, medium confidence. Small program: 12 courses, 4 terms.",
  },
  BSITM: {
    shape: "low confidence + anomaly",
    shapeNote:
      "Only low-confidence artifact in the dataset. Red 'low confidence' label in GuideProvenance badge. Roster gap caveat (ANOM-002). 'Capstone and Portfolio' AoS group present but capstone.present=false.",
  },
};
