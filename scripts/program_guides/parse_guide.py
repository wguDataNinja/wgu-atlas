#!/usr/bin/env python3
"""
parse_guide.py
==============
Content parser for WGU program guide text files.

Phase B thin slice: fully supports BSDA. Other guides may parse partially;
anomalies are recorded rather than causing failures.

Usage:
    # Parse a specific program by code
    python3 scripts/program_guides/parse_guide.py --program BSDA

    # Parse a specific text file
    python3 scripts/program_guides/parse_guide.py --input /path/to/BSDA.txt

    # Parse all available text files
    python3 scripts/program_guides/parse_guide.py --all

Environment:
    WGU_GUIDES_TEXT_DIR   directory containing raw text files
    WGU_GUIDES_DATA_DIR   output root (data/program_guides/ in repo)

Outputs per program:
    data/program_guides/parsed/{CODE}_parsed.json
    data/program_guides/validation/{CODE}_validation.json
    data/program_guides/manifest_rows/{CODE}_manifest_row.json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).parent
_REPO_ROOT  = _SCRIPT_DIR.parent.parent
_HOME = Path.home()

_DEFAULT_TEXT_DIR = _HOME / "Desktop" / "WGU-Reddit" / "WGU_catalog" / "program_guides" / "raw_texts"
_DEFAULT_DATA_DIR = _REPO_ROOT / "data" / "program_guides"

TEXT_DIR = Path(os.environ.get("WGU_GUIDES_TEXT_DIR", str(_DEFAULT_TEXT_DIR)))
DATA_DIR = Path(os.environ.get("WGU_GUIDES_DATA_DIR", str(_DEFAULT_DATA_DIR)))

PARSED_DIR       = DATA_DIR / "parsed"
VALIDATION_DIR   = DATA_DIR / "validation"
MANIFEST_ROW_DIR = DATA_DIR / "manifest_rows"

for d in [PARSED_DIR, VALIDATION_DIR, MANIFEST_ROW_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Patterns (guide-specific)
# ---------------------------------------------------------------------------

FOOTER_RE = re.compile(
    r'^([A-Z][A-Z0-9_\-]+)\s+(\d{6})\s+©\s+\d{4}\s+Western Governors University\s+'
    r'(\d{1,2}/\d{1,2}/\d{2,4})\s+(\d+)\s*$'
)
FOOTER_LOOSE_RE    = re.compile(r'^([A-Z][A-Z0-9_\-]+)\s+(\d{6})\s+©')
# Multi-line footer format: "BSCS 202412" on its own line (code + version only)
FOOTER_CODE_ONLY_RE = re.compile(r'^([A-Z][A-Z0-9_\-]+)\s+(\d{6})\s*$')
# Standalone page number (1–3 digits) emitted on its own line in multi-line footers
PAGE_NUM_RE = re.compile(r'^\d{1,3}$')

STANDARD_PATH_RE    = re.compile(r'^Standard Path(\s+for\s+.+)?$')
AREAS_OF_STUDY_RE   = re.compile(r'^Areas of Study\b')
CAPSTONE_RE         = re.compile(r'^Capstone$', re.IGNORECASE)
ACCESSIBILITY_RE    = re.compile(r'^Accessibility and Accommodations')

# SP_HEADER_RE matches both "Course Description" (older) and "Course Title" (newer) column headers
SP_HEADER_RE       = re.compile(r'^Course\s+(?:Description|Title)\s+CUs?\s+Term', re.IGNORECASE)
# Multi-line SP header: "CUs" or "CU" alone on a line signals multi-line table format
SP_CU_ONLY_RE      = re.compile(r'^CUs?\s*$', re.IGNORECASE)
SP_ROW_RE     = re.compile(r'^(.+?)\s+(\d{1,2})\s+(\d{1,2})\s*$')
SP_CHANGES_RE = re.compile(r'^Changes to Curriculum')

COMPETENCY_TRIGGER = 'This course covers the following competencies:'
BULLET_RE = re.compile(r'^([●•])\s*(.*)')

CERT_PREP_RE = re.compile(
    r'(?:prepares students for the following certification exam[:\s]+([^.]+))|'
    r'(?:certification exam[:\s]+([^.]+))',
    re.IGNORECASE,
)
PREREQ_RE = re.compile(
    r'(?:The following (?:course(?:s)? (?:are|is) a prerequisite|'
    r'(?:course(?:s)? must be completed))[:\s]+([^.]+))|'
    r'(?:([^.]+?) is a prerequisite for this course)',
    re.IGNORECASE,
)

# Lines that are definitely not course titles or group headings
SKIP_CONTENT_RE = re.compile(
    r'^(©|www\.|https?://|Click here|Student Handbook|Mobile Compatibility)',
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_footer(line: str) -> bool:
    """True for any line that is a footer/page-header component and should be skipped."""
    # Old single-line format: "BSDA 202309 © 2019 Western Governors University 5/1/23 7"
    if FOOTER_LOOSE_RE.match(line) and '©' in line:
        return True
    # New split format component 1: "BSCS 202412" (code + version only, no ©)
    if FOOTER_CODE_ONLY_RE.match(line):
        return True
    # New split format component 3: "© 2019 Western Governors University 8/2/24"
    if line.startswith('©'):
        return True
    return False


def is_bullet(line: str) -> bool:
    return bool(BULLET_RE.match(line))


def clean_bullet(line: str) -> str:
    m = BULLET_RE.match(line)
    return m.group(2).strip() if m else line.strip()


def looks_like_prose(line: str) -> bool:
    """True if line reads like mid-paragraph prose rather than a standalone heading."""
    if len(line) > 80:
        return True
    words = line.split()
    if not words:
        return False
    # Prose indicators: ends with sentence-like punctuation or is notably long
    if line.endswith(('.', ',', ';', ':', '?')):
        return True
    return False


# ---------------------------------------------------------------------------
# Pass 0: metadata extraction from footer lines
# ---------------------------------------------------------------------------

def extract_metadata(stripped: list) -> dict:
    """
    Scan footer lines to extract program code, version, pub_date, page_count.
    Returns dict with extracted metadata and a list of anomalies.
    """
    from collections import Counter
    codes, versions, dates, pages = [], [], [], []
    anomalies = []

    # New guide format: "Program Code: BSIT Catalog Version: 202604 Published Date: 11/20/2025"
    HEADER_META_RE = re.compile(
        r'Program Code:\s*([A-Z][A-Z0-9_\-]+)\s+Catalog Version:\s*(\d{6})'
        r'(?:\s+Published Date:\s*(\S+))?',
        re.IGNORECASE,
    )

    prev_code_seen = False
    for line in stripped:
        # Check new header-line metadata format (typically line 3 of modern guides)
        hm = HEADER_META_RE.search(line)
        if hm:
            codes.append(hm.group(1))
            versions.append(hm.group(2))
            if hm.group(3):
                dates.append(hm.group(3))
            prev_code_seen = False
            continue

        if not line:
            continue  # blank lines do not reset prev_code_seen

        m = FOOTER_RE.match(line)
        if m:
            codes.append(m.group(1))
            versions.append(m.group(2))
            dates.append(m.group(3))
            pages.append(int(m.group(4)))
            prev_code_seen = False
        elif FOOTER_LOOSE_RE.match(line):
            parts = line.split()
            if len(parts) >= 2:
                codes.append(parts[0])
                versions.append(parts[1])
            prev_code_seen = False
        elif FOOTER_CODE_ONLY_RE.match(line):
            # Multi-line footer: "BSCS 202412" on its own line
            m2 = FOOTER_CODE_ONLY_RE.match(line)
            codes.append(m2.group(1))
            versions.append(m2.group(2))
            prev_code_seen = True
        elif line.startswith('©') and prev_code_seen:
            # Extract pub date from the © line: "© 2019 Western Governors University 8/2/24"
            parts = line.rstrip().split()
            if parts and '/' in parts[-1]:
                dates.append(parts[-1])
            # Don't reset — page number line follows
        elif PAGE_NUM_RE.match(line) and prev_code_seen:
            # Standalone page number in multi-line footer
            try:
                pages.append(int(line.strip()))
            except ValueError:
                pass
            prev_code_seen = False
        else:
            prev_code_seen = False

    if not codes:
        anomalies.append({'type': 'no_footer_lines_found', 'note': 'metadata not recoverable'})
        return {'program_code': None, 'version': None, 'pub_date': None,
                'page_count': 0, 'anomalies': anomalies}

    code_counts = Counter(codes)
    ver_counts  = Counter(versions)
    program_code = code_counts.most_common(1)[0][0]
    version      = ver_counts.most_common(1)[0][0]
    pub_date     = dates[-1] if dates else None  # last occurrence is usually most up to date
    page_count   = max(pages) if pages else 0

    if len(set(versions)) > 1:
        anomalies.append({'type': 'multiple_versions', 'versions': sorted(set(versions))})

    return {
        'program_code': program_code,
        'version': version,
        'pub_date': pub_date,
        'page_count': page_count,
        'anomalies': anomalies,
    }


# ---------------------------------------------------------------------------
# Pass 1: section location
# ---------------------------------------------------------------------------

def locate_sections(stripped: list) -> dict:
    """
    Scan the full file for section anchors.
    Returns dict of section_name → line_index (first occurrence unless noted).
    """
    found = {}
    for i, line in enumerate(stripped):
        if STANDARD_PATH_RE.match(line) and 'Standard Path' not in found:
            found['Standard Path'] = i
        if AREAS_OF_STUDY_RE.match(line) and 'Areas of Study' not in found:
            found['Areas of Study'] = i
        if CAPSTONE_RE.match(line) and 'Capstone' not in found:
            found['Capstone'] = i
        if ACCESSIBILITY_RE.match(line) and 'Accessibility' not in found:
            found['Accessibility'] = i
    return found


# ---------------------------------------------------------------------------
# Pass 2: Standard Path table parsing
# ---------------------------------------------------------------------------

def parse_standard_path(stripped: list, sp_start: int, aos_start: int) -> tuple:
    """
    Parse Standard Path table rows between sp_start and aos_start.
    Returns: (rows, anomalies)
    Each row: {title, cus, term}
    """
    rows = []
    anomalies = []
    in_table = False

    for i in range(sp_start, aos_start):
        line = stripped[i]
        if not line:
            continue
        if is_footer(line):
            continue
        if SP_HEADER_RE.match(line):
            in_table = True
            continue
        if SP_CHANGES_RE.match(line):
            break  # "Changes to Curriculum" marks end of SP table

        if not in_table:
            continue

        m = SP_ROW_RE.match(line)
        if m:
            title, cus_str, term_str = m.group(1).strip(), m.group(2), m.group(3)
            # Sanity check: CUs 1–20, Term 1–15
            cus  = int(cus_str)
            term = int(term_str)
            if cus < 1 or cus > 20:
                anomalies.append({'type': 'sp_row_unusual_cus', 'line': i, 'cus': cus, 'title': title})
            if term < 1 or term > 15:
                anomalies.append({'type': 'sp_row_unusual_term', 'line': i, 'term': term, 'title': title})
            rows.append({'title': title, 'cus': cus, 'term': term})
        else:
            # Might be a title continuation line or noise
            if line and not STANDARD_PATH_RE.match(line):
                # Title wrap: if previous row exists, append to its title
                if rows and not SP_ROW_RE.match(line) and len(line.split()) <= 8:
                    rows[-1]['title'] = rows[-1]['title'] + ' ' + line
                    anomalies.append({'type': 'sp_title_continuation', 'line': i, 'text': line})

    if not rows:
        anomalies.append({'type': 'sp_no_rows_extracted', 'sp_start': sp_start})

    return rows, anomalies


def detect_sp_multiline(stripped: list, sp_start: int, aos_start: int) -> bool:
    """
    Return True if the SP table uses multi-line format (title, CUs, term on separate lines).
    Detected by presence of 'CUs' alone on a line within the SP section.
    """
    for i in range(sp_start, min(sp_start + 80, aos_start)):
        line = stripped[i]
        if SP_CU_ONLY_RE.match(line):
            return True
    return False


def parse_standard_path_multiline(stripped: list, sp_start: int, aos_start: int) -> tuple:
    """
    Parse multi-line SP table where title, CUs, and term each appear on their own line.

    Format example:
        Course Description     ← column header (one line)
        CUs                    ← column header (one line)
        Term                   ← column header (one line)
        Introduction to IT     ← title line
        3                      ← CU value
        1                      ← term value
        Next Course Title      ← next title
        ...

    Long titles may wrap across 2 lines before the CU value appears.
    Returns: (rows, anomalies)
    """
    rows = []
    anomalies = []

    HEADER_LINE_RE  = re.compile(r'^Course\s+(?:Description|Title)\s*$', re.IGNORECASE)
    COLUMN_WORD_RE  = re.compile(r'^(?:CUs?|Term)\s*$', re.IGNORECASE)
    SP_TOTAL_RE     = re.compile(r'^Total\s+CUs?\b', re.IGNORECASE)
    INT_RE          = re.compile(r'^\d{1,2}$')

    # States: BEFORE_TABLE, EXPECTING_TITLE, EXPECTING_TERM
    state = 'BEFORE_TABLE'
    title_buf = []
    cu_val = None
    prev_was_footer = False  # track footer proximity to distinguish page nums from CU/term values

    for i in range(sp_start, aos_start):
        line = stripped[i]
        if not line:
            continue  # blanks don't reset prev_was_footer
        if is_footer(line):
            prev_was_footer = True
            continue
        if SP_CHANGES_RE.match(line):
            break
        if AREAS_OF_STUDY_RE.match(line):
            break

        # "Total CUs N" line marks end of SP table
        if SP_TOTAL_RE.match(line):
            break

        # Skip standalone page numbers that follow footer lines (blanks between are ok)
        if prev_was_footer and PAGE_NUM_RE.match(line):
            prev_was_footer = False
            continue

        prev_was_footer = False

        if state == 'BEFORE_TABLE':
            if HEADER_LINE_RE.match(line):
                state = 'EXPECTING_TITLE'
            continue

        # Skip column-header words and header labels wherever they appear (repeated at page tops)
        if COLUMN_WORD_RE.match(line) or HEADER_LINE_RE.match(line):
            continue

        if state == 'EXPECTING_TITLE':
            m = INT_RE.match(line)
            if m:
                # This integer is the CU value — title accumulation is done
                cu_val = int(line)
                state = 'EXPECTING_TERM'
            else:
                # Another title line (or wrap)
                title_buf.append(line)

        elif state == 'EXPECTING_TERM':
            m = INT_RE.match(line)
            if m:
                term_val = int(line)
                title = ' '.join(title_buf).strip()
                if title and 1 <= cu_val <= 20 and 1 <= term_val <= 15:
                    rows.append({'title': title, 'cus': cu_val, 'term': term_val})
                else:
                    anomalies.append({'type': 'sp_row_invalid',
                                      'title': title, 'cus': cu_val, 'term': term_val})
                title_buf = []
                cu_val = None
                state = 'EXPECTING_TITLE'
            else:
                # Expected term number but got text — title of next course?
                anomalies.append({'type': 'sp_expected_term_got_text', 'line': i, 'text': line})
                # Treat as start of next title; flush current incomplete row
                if title_buf:
                    anomalies.append({'type': 'sp_incomplete_row',
                                      'title': ' '.join(title_buf), 'cu': cu_val})
                title_buf = [line]
                cu_val = None
                state = 'EXPECTING_TITLE'

    if title_buf:
        anomalies.append({'type': 'sp_incomplete_row_at_eof', 'title': ' '.join(title_buf)})

    if not rows:
        anomalies.append({'type': 'sp_no_rows_extracted', 'sp_start': sp_start})

    return rows, anomalies


# ---------------------------------------------------------------------------
# Pass 3: Areas of Study parsing
# ---------------------------------------------------------------------------

def _flush_bullet(pending: str, bullets: list):
    if pending.strip():
        bullets.append(pending.strip())


def _flush_course(current: dict, courses: list):
    if current.get('title'):
        courses.append(current)


def _flush_group(current_group: str, courses: list, groups: list):
    if current_group is not None and courses:
        groups.append({'group': current_group, 'courses': courses})


def parse_areas_of_study(stripped: list, aos_start: int, cap_start: int,
                          acc_start: int) -> tuple:
    """
    Parse the Areas of Study section into group > course > {description, competencies}.

    State machine:
        INTRO         — skip AoS header and intro boilerplate
        SEEKING       — looking for group heading or course title
        IN_DESCRIPTION — accumulating description lines for current course
        IN_COMPETENCIES — accumulating bullet list for current course

    Returns: (groups_list, anomalies)
    groups_list: [{group, courses: [{title, description, competency_bullets,
                                      prerequisite_mentions, certification_prep_mentions}]}]
    """
    # Determine upper bound
    end_idx = cap_start if cap_start else acc_start if acc_start else len(stripped)

    groups   = []
    anomalies = []

    current_group   = None
    group_courses   = []
    current_course  = None    # dict being built
    pending_titles  = []      # buffer: collects title candidates before we know group vs course
    description_buf = []
    bullet_buf      = []
    pending_bullet  = ""
    in_bullet       = False

    state = 'INTRO'
    intro_lines_seen = 0
    intro_prose_seen = False

    def emit_bullet():
        nonlocal pending_bullet, in_bullet
        if pending_bullet.strip():
            bullet_buf.append(pending_bullet.strip())
        pending_bullet = ""
        in_bullet = False

    def emit_course():
        nonlocal current_course, description_buf, bullet_buf, in_bullet, pending_bullet
        emit_bullet()
        if current_course:
            # Only write description from buf if not already set by the trigger handler
            if description_buf:
                current_course['description'] = ' '.join(description_buf).strip()
            current_course['competency_bullets'] = list(bullet_buf)
            group_courses.append(current_course)
        current_course = None
        description_buf = []
        bullet_buf = []
        in_bullet = False
        pending_bullet = ""

    def emit_group():
        nonlocal current_group, group_courses
        if current_group is not None and group_courses:
            groups.append({'group': current_group, 'courses': list(group_courses)})
        current_group = None
        group_courses = []

    def start_course(title: str) -> dict:
        return {
            'title': title,
            'description': '',
            'competency_bullets': [],
            'prerequisite_mentions': [],
            'certification_prep_mentions': [],
        }

    def process_pending_titles():
        """
        Resolve 0–2 buffered title candidates into group heading and/or course title.
        Called when we're about to start a course description.
        """
        nonlocal current_group, group_courses, current_course, pending_titles
        if not pending_titles:
            anomalies.append({'type': 'course_description_with_no_title', 'state': state})
            return

        if len(pending_titles) == 1:
            # One buffered line → course title, group unchanged
            current_course = start_course(pending_titles[0])
        elif len(pending_titles) == 2:
            # Two buffered lines → first is group heading, second is course title
            emit_course()
            emit_group()
            current_group = pending_titles[0]
            group_courses = []
            current_course = start_course(pending_titles[1])
        else:
            # More than 2 — unusual; treat last as course title
            anomalies.append({'type': 'too_many_pending_titles',
                              'titles': list(pending_titles)})
            current_course = start_course(pending_titles[-1])
            if len(pending_titles) >= 2:
                emit_course()
                emit_group()
                current_group = pending_titles[0]
                group_courses = []

        pending_titles.clear()

    # ── Main loop ────────────────────────────────────────────────────────────
    for i in range(aos_start, end_idx):
        line = stripped[i]

        # Skip empty lines everywhere
        if not line:
            continue

        # Skip footer lines everywhere (includes split-format "CODE YYYYMM" and "©..." lines)
        if is_footer(line):
            continue

        # Skip standalone page numbers emitted by the multi-line footer format
        if PAGE_NUM_RE.match(line):
            continue

        # The "for" line after the AoS header
        if line == 'for' and state == 'INTRO':
            continue

        # ── INTRO: skip until first group heading ─────────────────────────
        if state == 'INTRO':
            intro_lines_seen += 1
            # AoS header line itself
            if AREAS_OF_STUDY_RE.match(line):
                continue
            # Skip repeated SP-header line (shouldn't appear here but guard anyway)
            if SP_HEADER_RE.match(line):
                continue
            # Mark that we've seen the intro boilerplate (long prose block)
            if looks_like_prose(line):
                intro_prose_seen = True
                continue
            # After seeing prose, the first non-prose line is the first group heading
            if intro_prose_seen and not looks_like_prose(line):
                state = 'SEEKING'
                emit_course()
                emit_group()
                current_group = line
                group_courses = []
            # else: short line before any prose (e.g. sub-header) — keep skipping
            continue

        # ── All states: handle competency trigger ─────────────────────────
        if line == COMPETENCY_TRIGGER:
            if state in ('IN_DESCRIPTION', 'SEEKING'):
                # If we were still SEEKING (no description), process titles now
                if state == 'SEEKING':
                    process_pending_titles()
                # Flush any pending description to current course
                if current_course:
                    current_course['description'] = ' '.join(description_buf).strip()
                    description_buf = []
                    # Scan description for prereq/cert mentions
                    _scan_description_mentions(current_course)
                state = 'IN_COMPETENCIES'
            else:
                anomalies.append({'type': 'competency_trigger_unexpected_state',
                                  'line': i, 'state': state})
            continue

        # ── IN_COMPETENCIES ───────────────────────────────────────────────
        if state == 'IN_COMPETENCIES':
            if is_bullet(line):
                emit_bullet()
                m = BULLET_RE.match(line)
                pending_bullet = m.group(2).strip() if m else line
                in_bullet = True
                continue
            elif in_bullet and not is_footer(line):
                # Check if this is a bullet continuation (indented / lowercase start)
                # or a new standalone line (course title / group heading)
                # Heuristic: if short and title-case → new content; else continuation
                if _is_bullet_continuation(line, pending_bullet):
                    pending_bullet += ' ' + line
                    continue
                else:
                    # End of bullet; this line starts new content → end course too
                    emit_bullet()
                    in_bullet = False
                    emit_course()
                    state = 'SEEKING'
                    # Fall through to SEEKING block below
            elif not is_bullet(line) and not in_bullet:
                # Non-bullet line after competencies → end of this course
                emit_bullet()
                emit_course()
                state = 'SEEKING'
                # Fall through to handle this line in SEEKING
            else:
                # Was in_bullet, now non-continuation, non-bullet line
                emit_bullet()
                emit_course()
                state = 'SEEKING'
                # Fall through to handle this line in SEEKING

        # ── SEEKING: looking for group heading or course title ────────────
        if state == 'SEEKING':
            if SKIP_CONTENT_RE.match(line):
                continue
            # Terminal sections
            if CAPSTONE_RE.match(line):
                break
            if ACCESSIBILITY_RE.match(line):
                break

            # If we have at least one buffered title and this line looks like prose,
            # the titles are resolved and the description begins now.
            if pending_titles and looks_like_prose(line):
                process_pending_titles()
                description_buf.append(line)
                state = 'IN_DESCRIPTION'
                continue

            # Standalone short line — buffer as potential group heading or course title.
            if len(pending_titles) < 3:
                pending_titles.append(line)
            else:
                anomalies.append({'type': 'pending_titles_overflow', 'line': i, 'text': line,
                                  'buffer': list(pending_titles)})
            continue

        # ── IN_DESCRIPTION: accumulating description ──────────────────────
        if state == 'IN_DESCRIPTION':
            if SKIP_CONTENT_RE.match(line):
                continue
            # Terminal check
            if CAPSTONE_RE.match(line) or ACCESSIBILITY_RE.match(line):
                emit_bullet()
                emit_course()
                state = 'SEEKING'
                break

            description_buf.append(line)
            # If this description-like line is actually short and the PREVIOUS
            # state was misidentified, we'll catch it via anomaly later.
            continue

    # ── Final flush ───────────────────────────────────────────────────────────
    emit_bullet()
    emit_course()
    emit_group()

    return groups, anomalies


def _is_bullet_continuation(line: str, pending: str) -> bool:
    """
    True if 'line' looks like a continuation of the current bullet text,
    rather than a new standalone heading or course title.
    """
    if not line:
        return False
    # If the pending bullet is very short (< 30 chars) and the line adds to it
    # with lowercase start or a conjunction, it's continuation
    first_word = line.split()[0] if line.split() else ''
    if first_word.islower():
        return True
    # If the pending bullet ends mid-sentence (no terminal punctuation) and
    # line continues, treat as continuation — but only if line is not very short
    if len(pending) > 20 and not pending[-1] in '.?!':
        if len(line) > 30:
            return True
    return False


def _scan_description_mentions(course: dict):
    """
    Scan course description for prerequisite and cert-prep mentions.
    Populates course['prerequisite_mentions'] and course['certification_prep_mentions'].
    """
    desc = course.get('description', '')
    if not desc:
        return

    # Prereq mentions
    prereq_patterns = [
        re.compile(r'([^.]+?) (?:is|are) (?:a )?prerequisite(?:s)? for this course', re.IGNORECASE),
        re.compile(r'The following course(?:s)? (?:is|are) (?:a )?prerequisite[:\s]+([^.]+)', re.IGNORECASE),
        re.compile(r'prerequisite[:\s]+([^.]+)', re.IGNORECASE),
    ]
    for pat in prereq_patterns:
        for m in pat.finditer(desc):
            mention = m.group(1).strip() if m.lastindex and m.group(1) else m.group(0).strip()
            if mention and mention not in course['prerequisite_mentions']:
                course['prerequisite_mentions'].append(mention)

    # Cert prep mentions
    cert_pat = re.compile(
        r'prepares students for the following certification exam[:\s]+([^.]+)',
        re.IGNORECASE,
    )
    for m in cert_pat.finditer(desc):
        mention = m.group(1).strip()
        if mention not in course['certification_prep_mentions']:
            course['certification_prep_mentions'].append(mention)

    cert_pat2 = re.compile(
        r'(?:CompTIA|Praxis|NCLEX|CPA|AWS|Azure|Cisco)\s+\S+',
        re.IGNORECASE,
    )
    for m in cert_pat2.finditer(desc):
        mention = m.group(0).strip()
        if mention not in course['certification_prep_mentions']:
            course['certification_prep_mentions'].append(mention)


# ---------------------------------------------------------------------------
# Pass 4: Capstone parsing
# ---------------------------------------------------------------------------

def parse_capstone(stripped: list, cap_start: int, acc_start: int) -> tuple:
    """
    Parse the Capstone section. Usually contains one course entry.
    Returns: (capstone_dict, anomalies)
    """
    if cap_start is None:
        return None, []

    end_idx = acc_start if acc_start else len(stripped)
    anomalies = []

    title = None
    description_buf = []
    bullets = []
    pending_bullet = ""
    in_bullet = False
    in_competencies = False

    for i in range(cap_start + 1, end_idx):  # +1 to skip "Capstone" heading line
        line = stripped[i]
        if not line:
            continue
        if is_footer(line):
            continue
        if ACCESSIBILITY_RE.match(line):
            break

        if title is None:
            title = line
            continue

        if line == COMPETENCY_TRIGGER:
            in_competencies = True
            continue

        if in_competencies:
            if is_bullet(line):
                if pending_bullet.strip():
                    bullets.append(pending_bullet.strip())
                m = BULLET_RE.match(line)
                pending_bullet = m.group(2).strip() if m else line
                in_bullet = True
            elif in_bullet:
                if _is_bullet_continuation(line, pending_bullet):
                    pending_bullet += ' ' + line
                else:
                    if pending_bullet.strip():
                        bullets.append(pending_bullet.strip())
                    pending_bullet = ""
                    in_bullet = False
        else:
            description_buf.append(line)

    if pending_bullet.strip():
        bullets.append(pending_bullet.strip())

    if title is None:
        anomalies.append({'type': 'capstone_no_title'})
        return None, anomalies

    capstone = {
        'title': title,
        'description': ' '.join(description_buf).strip(),
        'competency_bullets': bullets,
    }
    _scan_description_mentions(capstone)
    return capstone, anomalies


# ---------------------------------------------------------------------------
# Pass 5: Title block and program description
# ---------------------------------------------------------------------------

def extract_title_and_description(stripped: list, sp_start: int) -> tuple:
    """
    Extract degree title and program description from the top of the document.
    Degree title is line 1 (index 1, after "Program Guidebook").
    Program description is the freeform paragraphs before the boilerplate.
    Returns: (degree_title, program_description)
    """
    BOILERPLATE_START = re.compile(
        r'^(Understanding the Competency|Accreditation|The Degree Plan|'
        r'How You Will Interact|Connecting with Other|Orientation|'
        r'Transferability|Continuous Enrollment)',
        re.IGNORECASE,
    )

    degree_title = None
    desc_lines   = []
    in_desc      = False

    for i, line in enumerate(stripped):
        if not line:
            continue
        if is_footer(line):
            continue
        if i == 0 and line == 'Program Guidebook':
            continue
        if degree_title is None:
            degree_title = line
            in_desc = True
            continue
        if in_desc:
            if BOILERPLATE_START.match(line):
                break
            desc_lines.append(line)

    return degree_title, ' '.join(desc_lines).strip()


# ---------------------------------------------------------------------------
# Validation report builder
# ---------------------------------------------------------------------------

def build_validation(
    code: str,
    metadata: dict,
    sections: dict,
    sp_rows: list,
    groups: list,
    capstone: dict,
    sp_anomalies: list,
    aos_anomalies: list,
    cap_anomalies: list,
    degree_title: str,
) -> dict:
    """
    Build a structured validation report for the parsed guide.
    """
    sp_titles  = {r['title'] for r in sp_rows}
    aos_titles = set()
    for g in groups:
        for c in g['courses']:
            aos_titles.add(c['title'])
    cap_title = capstone['title'] if capstone else None
    if cap_title:
        aos_titles.add(cap_title)

    sp_only  = sorted(sp_titles - aos_titles)
    aos_only = sorted(aos_titles - sp_titles)
    both     = sorted(sp_titles & aos_titles)

    warnings = []
    if sp_only:
        warnings.append(f"{len(sp_only)} SP titles not found in AoS: {sp_only[:5]}")
    if aos_only:
        warnings.append(f"{len(aos_only)} AoS titles not in SP: {aos_only[:5]}")

    aos_course_count = sum(len(g['courses']) for g in groups)
    empty_desc = [c['title'] for g in groups for c in g['courses']
                  if not c.get('description')]
    empty_comp = [c['title'] for g in groups for c in g['courses']
                  if not c.get('competency_bullets')]

    all_anomalies = (
        metadata.get('anomalies', [])
        + sp_anomalies
        + aos_anomalies
        + cap_anomalies
    )

    if empty_desc:
        warnings.append(f"{len(empty_desc)} courses with no description")
    if empty_comp:
        warnings.append(f"{len(empty_comp)} courses with no competency bullets")

    # Confidence
    if not warnings and not all_anomalies and len(both) == len(sp_titles):
        confidence = "high"
    elif len(all_anomalies) <= 3 and len(warnings) <= 2:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "program_code":             code,
        "degree_title":             degree_title,
        "version":                  metadata.get('version'),
        "pub_date":                 metadata.get('pub_date'),
        "page_count":               metadata.get('page_count'),
        "detected_sections":        list(sections.keys()),
        "section_line_indices":     sections,
        "standard_path_row_count":  len(sp_rows),
        "aos_group_count":          len(groups),
        "aos_course_count":         aos_course_count,
        "capstone_present":         capstone is not None,
        "title_reconciliation": {
            "in_both":   len(both),
            "sp_only":   sp_only,
            "aos_only":  aos_only,
        },
        "empty_descriptions":       empty_desc,
        "empty_competency_lists":   empty_comp,
        "anomaly_count":            len(all_anomalies),
        "anomalies":                all_anomalies,
        "warnings":                 warnings,
        "parseability_confidence":  confidence,
    }


# ---------------------------------------------------------------------------
# Manifest row builder
# ---------------------------------------------------------------------------

def build_manifest_row(code: str, txt_path: Path, validation: dict, groups: list,
                        sp_rows: list) -> dict:
    """Build a manifest row from parsed results (for manifest_rows/ output)."""
    cert_count  = sum(
        len(c.get('certification_prep_mentions', []))
        for g in groups for c in g['courses']
    )
    prereq_count = sum(
        len(c.get('prerequisite_mentions', []))
        for g in groups for c in g['courses']
    )
    inferred_groups = [g['group'] for g in groups]

    from scripts.program_guides.analyze_guide_manifest import classify_family
    family = classify_family(code)

    return {
        "source_pdf_filename":       code + ".pdf",
        "source_text_filename":      txt_path.name,
        "inferred_program_code":     code,
        "page_count":                validation['page_count'],
        "version_strings":           [validation['version']] if validation['version'] else [],
        "publication_dates":         [validation['pub_date']] if validation['pub_date'] else [],
        "has_standard_path":         validation['standard_path_row_count'] > 0,
        "has_areas_of_study":        validation['aos_course_count'] > 0,
        "has_capstone_section":      validation['capstone_present'],
        "has_course_descriptions":   len(validation['empty_descriptions']) < validation['aos_course_count'],
        "has_competency_bullets":    len(validation['empty_competency_lists']) < validation['aos_course_count'],
        "has_term_structure":        validation['standard_path_row_count'] > 0,
        "has_cu_values":             validation['standard_path_row_count'] > 0,
        "has_cert_prep_mentions":    cert_count > 0,
        "has_prereq_mentions":       prereq_count > 0,
        "standard_path_row_count":   validation['standard_path_row_count'],
        "competency_trigger_count":  validation['aos_course_count'],
        "competency_bullet_count":   sum(len(c.get('competency_bullets', []))
                                        for g in groups for c in g['courses']),
        "cert_prep_mention_count":   cert_count,
        "prereq_mention_count":      prereq_count,
        "detected_section_headings": validation['detected_sections'],
        "inferred_course_groups":    inferred_groups,
        "likely_guide_family":       family,
        "template_type":             "full" if validation['capstone_present'] else "partial",
        "parseability_confidence":   validation['parseability_confidence'],
        "warnings":                  validation['warnings'],
        "irregularities":            [a['type'] for a in validation['anomalies']],
    }


# ---------------------------------------------------------------------------
# Main parse function
# ---------------------------------------------------------------------------

def parse_guide(txt_path: Path, verbose: bool = True) -> dict:
    """
    Full parse pipeline for one guide file.
    Returns dict with parsed output, validation, and manifest row.
    """
    with open(txt_path, encoding='utf-8', errors='replace') as f:
        raw = f.readlines()

    stripped = [l.rstrip('\n').strip() for l in raw]
    code = txt_path.stem

    if verbose:
        print(f"\n{'='*60}")
        print(f"Parsing: {txt_path.name}  (lines={len(stripped)})")

    # Pass 0: metadata
    meta = extract_metadata(stripped)
    program_code = meta.get('program_code') or code
    if verbose:
        print(f"  Metadata: code={program_code}  version={meta.get('version')}  "
              f"pub_date={meta.get('pub_date')}  pages={meta.get('page_count')}")

    # Pass 1: section locations
    sections = locate_sections(stripped)
    sp_start  = sections.get('Standard Path')
    aos_start = sections.get('Areas of Study')
    cap_start = sections.get('Capstone')
    acc_start = sections.get('Accessibility')

    if verbose:
        print(f"  Sections: {list(sections.keys())}")
        for name, idx in sections.items():
            print(f"    {name}: line {idx}  '{stripped[idx]}'")

    if sp_start is None:
        print("  [WARN] Standard Path not found")
    if aos_start is None:
        print("  [WARN] Areas of Study not found")

    # Pass 2: Standard Path — detect format and route to appropriate parser
    sp_rows, sp_anomalies = [], []
    if sp_start is not None and aos_start is not None:
        if detect_sp_multiline(stripped, sp_start, aos_start):
            sp_rows, sp_anomalies = parse_standard_path_multiline(stripped, sp_start, aos_start)
        else:
            sp_rows, sp_anomalies = parse_standard_path(stripped, sp_start, aos_start)
    if verbose:
        print(f"  Standard Path: {len(sp_rows)} rows  anomalies={len(sp_anomalies)}")

    # Pass 3: Areas of Study
    groups, aos_anomalies = [], []
    if aos_start is not None:
        groups, aos_anomalies = parse_areas_of_study(
            stripped, aos_start,
            cap_start if cap_start else (acc_start if acc_start else len(stripped)),
            acc_start if acc_start else len(stripped),
        )
    if verbose:
        total_courses = sum(len(g['courses']) for g in groups)
        print(f"  Areas of Study: {len(groups)} groups, {total_courses} courses  "
              f"anomalies={len(aos_anomalies)}")
        for g in groups:
            print(f"    [{g['group']}] {len(g['courses'])} courses")

    # Pass 4: Capstone
    capstone, cap_anomalies = None, []
    if cap_start is not None:
        capstone, cap_anomalies = parse_capstone(
            stripped, cap_start, acc_start if acc_start else len(stripped)
        )
    if verbose and capstone:
        print(f"  Capstone: '{capstone['title']}'  bullets={len(capstone['competency_bullets'])}")

    # Pass 5: Title and description
    degree_title, prog_desc = extract_title_and_description(
        stripped, sp_start if sp_start else 0
    )
    if verbose:
        print(f"  Degree title: '{degree_title}'")

    # Validation report
    validation = build_validation(
        program_code, meta, sections, sp_rows, groups, capstone,
        sp_anomalies, aos_anomalies, cap_anomalies, degree_title,
    )
    if verbose:
        print(f"  Validation: confidence={validation['parseability_confidence']}  "
              f"anomalies={validation['anomaly_count']}  warnings={len(validation['warnings'])}")
        if validation['warnings']:
            for w in validation['warnings']:
                print(f"    WARN: {w}")

    # Parsed output
    all_anomalies = (
        meta.get('anomalies', []) + sp_anomalies + aos_anomalies + cap_anomalies
    )
    parsed = {
        "program_code":       program_code,
        "version":            meta.get('version'),
        "pub_date":           meta.get('pub_date'),
        "page_count":         meta.get('page_count'),
        "degree_title":       degree_title,
        "program_description": prog_desc,
        "standard_path":      sp_rows,
        "areas_of_study":     groups,
        "capstone":           capstone,
        "anomalies":          all_anomalies,
    }

    # Manifest row
    manifest_row = build_manifest_row(code, txt_path, validation, groups, sp_rows)

    return {
        "code":          code,
        "parsed":        parsed,
        "validation":    validation,
        "manifest_row":  manifest_row,
    }


def write_outputs(result: dict, verbose: bool = True):
    code = result['code']
    parsed_path   = PARSED_DIR       / f"{code}_parsed.json"
    val_path      = VALIDATION_DIR   / f"{code}_validation.json"
    mrow_path     = MANIFEST_ROW_DIR / f"{code}_manifest_row.json"

    for path, obj in [(parsed_path, result['parsed']),
                      (val_path,    result['validation']),
                      (mrow_path,   result['manifest_row'])]:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)

    if verbose:
        print(f"  Wrote: {parsed_path.name}")
        print(f"  Wrote: {val_path.name}")
        print(f"  Wrote: {mrow_path.name}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Parse WGU program guide text files.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--program', metavar='CODE',
                       help='Program code to parse (e.g. BSDA)')
    group.add_argument('--input', metavar='PATH',
                       help='Path to specific .txt file')
    group.add_argument('--all', action='store_true',
                       help='Parse all available text files')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress per-pass verbose output')
    args = parser.parse_args()

    verbose = not args.quiet
    txt_files = []

    if args.program:
        p = TEXT_DIR / f"{args.program}.txt"
        if not p.exists():
            print(f"ERROR: {p} not found")
            sys.exit(1)
        txt_files = [p]
    elif args.input:
        p = Path(args.input)
        if not p.exists():
            print(f"ERROR: {p} not found")
            sys.exit(1)
        txt_files = [p]
    elif args.all:
        txt_files = sorted(TEXT_DIR.glob("*.txt"))
        if not txt_files:
            print(f"No .txt files found in {TEXT_DIR}")
            sys.exit(1)

    success, failed = 0, []

    for txt_path in txt_files:
        try:
            result = parse_guide(txt_path, verbose=verbose)
            write_outputs(result, verbose=verbose)
            success += 1
        except Exception as e:
            failed.append((txt_path.name, str(e)))
            print(f"  ERROR parsing {txt_path.name}: {e}")
            import traceback; traceback.print_exc()

    if len(txt_files) > 1:
        print(f"\n=== Parse summary ===")
        print(f"  Success: {success}")
        print(f"  Failed:  {len(failed)}")
        if failed:
            for name, err in failed:
                print(f"    {name}: {err}")


if __name__ == "__main__":
    # Patch import path so manifest classify_family is accessible
    sys.path.insert(0, str(_REPO_ROOT))
    main()
