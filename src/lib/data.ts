import fs from "fs";
import path from "path";
import type {
  CourseCard,
  CourseDetail,
  CatalogEvent,
  HomepageSummary,
} from "./types";

const PUBLIC_DATA = path.join(process.cwd(), "public", "data");

export function getCourses(): CourseCard[] {
  const raw = fs.readFileSync(path.join(PUBLIC_DATA, "courses.json"), "utf-8");
  return JSON.parse(raw);
}

export function getEvents(): CatalogEvent[] {
  const raw = fs.readFileSync(path.join(PUBLIC_DATA, "events.json"), "utf-8");
  return JSON.parse(raw);
}

export function getHomepageSummary(): HomepageSummary {
  const raw = fs.readFileSync(
    path.join(PUBLIC_DATA, "homepage_summary.json"),
    "utf-8"
  );
  return JSON.parse(raw);
}

export function getCourseDetail(code: string): CourseDetail | null {
  const filePath = path.join(PUBLIC_DATA, "courses", `${code}.json`);
  if (!fs.existsSync(filePath)) return null;
  const raw = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(raw);
}

/** Returns all course codes that have a detail file (active AP only). */
export function getDetailableCodes(): string[] {
  const dir = path.join(PUBLIC_DATA, "courses");
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .map((f) => f.replace(".json", ""));
}
