# Page Design Reference

Purpose: text-based representations of each WGU Atlas page — structure, content, visual design, and function — for use in design and planning work.

These are working reference artifacts, not live documentation. Regenerate when a page changes significantly.

---

## What these files are

Each file covers one route. It captures:
- page section layout (top to bottom)
- all visible text and labels
- visual style signals (colors, typography, spacing tokens)
- interactive behavior
- functional inventory (what's on the page, what's notably absent)
- design observations relevant to planning

They are written in plain text with ASCII layout diagrams. The format is intentionally terse and machine-readable.

---

## How to generate one

### Inputs to gather

1. **Page component source** — `src/app/[route]/page.tsx`
2. **Major child component sources** — all components imported and rendered on the page
3. **content_map.txt section** — search for the route header (e.g. `HOME PAGE (/)`) in `content_map.txt`; this gives you the extracted visible text with source locations
4. **Live page text** (optional but useful) — paste the rendered text from the browser; confirms what's actually visible vs what the source implies

### Prompt to Claude

> Here is the page source, the content_map.txt section for this route, and the live rendered text.
> Output a text-based representation of this page covering: layout, content, visual design tokens, interactions, functional inventory, and design observations for planning.

Then save the output here as `{route_slug}.md`.

### Route → filename convention

| Route | Filename |
|---|---|
| `/` | `homepage.md` |
| `/courses` | `courses.md` |
| `/courses/[code]` | `course_detail.md` |
| `/programs` | `programs.md` |
| `/programs/[code]` | `program_detail.md` |
| `/schools` | `schools.md` |
| `/schools/[slug]` | `school_detail.md` |
| `/compare` | `compare.md` |
| `/timeline` | `timeline.md` |
| `/data` | `data.md` |
| `/methods` | `methods.md` |
| `/about` | `about.md` |

---

## Source locations for each input

| Input | Location |
|---|---|
| Page components | `src/app/` |
| Shared components | `src/components/` |
| Content map | `content_map.txt` (root) — regenerate with `node scripts/generate_content_map.js` |
| Runtime data shapes | `src/lib/types.ts`, `src/lib/data.ts` |

---

## Artifact index

| File | Route | Last updated | Notes |
|---|---|---|---|
| [homepage.md](./homepage.md) | `/` | 2026-03-20 | Initial capture |
