// ---------------------------------------------------------------------------
// Compare prototype lab utilities — thin re-export from production lib.
// Kept so prototype lab components (ComparePrototypeLab.tsx) don't need
// to change their import paths after the lib extraction.
// ---------------------------------------------------------------------------

export {
  LAB_EXCLUSIONS,
  labShortLabel,
  labDisplayLabel,
  buildTermLanes,
  buildLabPayload,
} from "@/lib/compareUtils";
export type {
  ComparePayload,
  CompareProgramMeta,
  CompareCourseEntry,
  CompareResult,
  TermLane,
} from "@/lib/compareUtils";
