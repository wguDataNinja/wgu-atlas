# YouTube Source Workstream — Log and Status

**Last updated:** 2026-03-18

---

## Work surfaces at a glance

| Purpose | File |
|---|---|
| Official WGU — raw universe | `_internal/youtube/raw/wgu_official_titles_raw.txt` |
| Official WGU — filtered working copy | `_internal/youtube/working/wgu_official_titles_filtered.txt` |
| Career Services — raw universe | `_internal/youtube/raw/wgu_career_services_titles_raw.txt` |
| Career Services — filtered working copy | `_internal/youtube/working/wgu_career_services_titles_filtered.txt` |

Source files outside repo (originals):
- `/Users/buddy/projects/yt-video-analysis/research/wgu/derived/title_inventory_llm_view.txt`
- `/Users/buddy/projects/yt-video-analysis/research/wgucareerservices/derived/title_inventory_llm_view.txt`

The repo copies are the working copies. Sync from the external files if those inventories are updated.

---

## File format

Each line:
```
VIDEO_ID | YYYY-MM-DD | Title of video
```

All files are plain text, one video per line.

---

## Official WGU channel

### Counts

| Stage | Count |
|---|---|
| Raw (imported 2026-03-18) | 1,535 |
| Excluded by first-pass filter | 717 |
| Filtered working copy | 818 |

### First-pass exclusion filter applied

Excluded any title containing (case-insensitive):
- `Commencement`, `Conferral`, `Ceremony`, `Graduation`
- `Graduate Speaker`, `Keynote`, `National Anthem`, `Honorary Degree`
- `Recap`, `Morning Ceremony`, `Afternoon Ceremony`, `Full Ceremony`

Also excluded regex pattern: `WGU 20\d\d .*(Commencement|Event|Ceremony)` (catches year+city commencement titles).

### Signal in filtered copy (~818 titles, overlapping)

| Signal type | Approx. count |
|---|---|
| Career path / degree-field content | ~147 |
| Student journey / alumni stories | ~122 |
| Education / teacher content | ~102 |
| Nursing / health content | ~62 |
| School/college named directly | ~12 |
| Thought leadership panels / summits | ~6 |
| School roadshows | ~6 |
| School fireside chats | ~4 |

Roadshows and fireside chats are the highest-confidence school-page candidates — small group, easy to review manually.

Degree-field and student journey videos are the largest group — these are primarily degree-page candidates, need further filtering by field/degree family.

### Remaining noise in filtered copy

The filtered copy still contains content that is not Atlas-relevant:
- Generic WGU brand/marketing ("WGU — Education for the People | College Built for Real Life")
- Very short-form reels with hashtag titles ("#CareerGuide", "#CareerGrowth")
- Podcast intros and unrelated interview content

These will be dropped during the candidate review pass (YT-1, YT-2). They do not need pre-filtering; reviewers should simply skip them.

### Next pass: YT-1 (school-level candidates)

Goal: produce a small list of high-confidence school-page candidates from the filtered working copy.

Approach:
1. Scan filtered copy for roadshows, fireside chats, thought-leadership panels, school-branded events
2. For each candidate: note video ID, title, and target school (Business / Technology / Health / Education)
3. Output: a short candidate list (target 5–15 per school) ready for placement consideration

Exclusions during review:
- Individual student stories without clear school-level framing
- Narrow degree/role-specific content (→ defer to YT-2 for degree page consideration)
- Very short-form reels (< 2–3 min implied by title style)

---

## WGU Career Services channel

### Counts

| Stage | Count |
|---|---|
| Raw (imported 2026-03-18) | 441 |
| Excluded by first-pass filter | 174 |
| Filtered working copy | 267 |

### First-pass exclusion filter applied

Excluded any title containing (case-insensitive):
- `Career Quest:` (colon = named employer recruiting session)
- `Resume`, `Cover Letter`, `LinkedIn Profile`
- `Job Search`, `Interview` (generic how-to)
- `Internship Expo`
- `Financial Series`, `Salary Negotiation`, `Federal Career`
- `AMA Career Workshop`, `Networking with WGU Connect`

### What remains and its quality

Career Services content after first-pass filtering is still mixed. The channel is primarily a job-hunting and employer-recruiting service, not a degree-context resource. What passes the first-pass filter includes:

High-potential (worth reviewing for Atlas):
- Degree/field-specific career content (e.g. "Launch Your Data Analytics Career with The Information Lab", "Cyber Week" series)
- Broad career journey narratives with degree context (e.g. "From MBA to Entrepreneur")
- Field-transition stories that map to specific colleges

Still noisy (likely to be excluded in candidate review):
- Employer recruiting sessions without a "Career Quest:" prefix
- Generic professional development sessions (networking, branding, AI job-search tools)
- Finance literacy sessions not caught by the first-pass filter

### Important note on Career Services

Career Services is a substantially weaker source for Atlas than Official WGU. After first-pass filtering, 267 titles remain — but most of those still need aggressive curation before any would be placement-worthy.

Recommended approach: treat Career Services as a **supplemental** source, reviewed after Official WGU passes are complete. Do not run a dedicated Career Services candidate pass until Official WGU school-level (YT-1) is done.

### Next pass: YT-3 (after YT-1 and YT-2)

Goal: identify the 10–20 Career Services videos genuinely useful on Atlas school or degree pages.

Approach:
1. Scan filtered copy for titles that map to specific degree fields (not generic job-hunting)
2. Flag: broad field career panels, degree-adjacent alumni journeys, "Cyber Week"-style field weeks
3. Output: small candidate list for placement consideration, with school/program tags

---

## Passes planned

| Pass | Source | Scope | Status |
|---|---|---|---|
| YT-1 | Official WGU | School-level candidates | Not started |
| YT-2 | Official WGU | Degree-level candidates | Not started |
| YT-3 | Career Services | School/degree candidates (selective) | Not started — do after YT-1 |

---

## Known open items

- The raw inventories were imported 2026-03-18. They will become stale over time as new videos are published. Sync from source when refreshing.
- Career Services filter is first-pass only. A second manual scan of the 267 remaining titles is needed before a candidate list can be produced.
- Neither channel has a `youtube_video` candidate artifact yet — that is the output of YT-1.
- No placement schema for YouTube resources has been finalized yet. The `official_resource_placements.json` schema supports it (any URL can be a resource), but `resource_group` values for videos need to be decided (e.g. `school_video`, `degree_video`).
