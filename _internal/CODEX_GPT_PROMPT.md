# Chat GPT Prompt — Codex Prep + Roadmap

*Copy-paste this to your Chat GPT assistant (conversational, not agentic).*

---

I run a project called **WGU Atlas** — a public-facing reference site
that lets students explore WGU courses, programs, and catalog history.
There are three repos involved:

1. **wgu-reddit** — started as a Reddit analyzer capstone, but it
   grew a full catalog pipeline: acquire PDFs, parse them, track
   changes across editions, build site-data exports.
2. **wgu-catalog** — doesn't exist as a separate repo yet. It should.
   The catalog pipeline has outgrown being a dependency of a Reddit
   analyzer. We want to extract it into its own repo.
3. **wgu-atlas** — the Next.js static site + a Python QA subsystem
   (RAG over catalog data). This is the public face.

**What we just did:** We discovered 3 new WGU catalog editions had
been published since our last update (Apr, May, June 2026). We built
an `acquire_catalog.py` script with check/download modes, downloaded
and extracted all 3, ran the full parser pipeline, and verified the
changes (28 new education courses, one replacement). We also found
that the parser wipes its cross-edition index when run for single
editions — a footgun we now know about.

**The crossroads:** We have all this documented in a file called
`_internal/CODEX_SESSION.md` — a comprehensive session prompt for
Codex CLI. The idea is to give Codex (which can read files, run
commands, and edit code) a strong, structured pass at the repo to
do real work.

What I need from you in two phases:

**Phase 1 — Before Codex runs:** Read
`_internal/CODEX_SESSION.md`. Edit it for maximum usefulness to an
agent that can act. Tighten ambiguity, fill gaps, sharpen the
priority list, and flag anything a literal-minded agent would get
wrong. Send the edited version back as a clean file.

**Phase 2 — After Codex runs:** After v7 gives us its output
(written to `_internal/CODEX_SESSION_LOG.md`), read that log +
the repo state and build a **work roadmap**. Not a todo list — a
strategic roadmap with phases, dependencies, and decision points.
What should we do first, second, third, and what would we decide
at each fork?

The repos are both on this machine, both local. I can share their
contents or paths as needed.
