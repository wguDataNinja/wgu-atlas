"""
resolve_ambiguous_deterministic.py

Applies five deterministic signals to every ambiguous roster row across all
115 bridge guide files. Rows that resolve to a single canonical course are
marked with a new anchor_class; rows that do not resolve are forwarded as
'ambiguous_residual' for downstream LLM adjudication.

Signals applied (independently; no conflicts observed in data):
  1. cu_match          – SP row sp_cus matches exactly one candidate's canonical_cus
  2. one_active        – Exactly one candidate has active_current = True
  3. a_suffix_cert     – Cert-only A-suffix candidates excluded from degree guides;
                         exactly one non-cert candidate remains
  4. degree_level      – Candidates exclusively scoped to the opposite degree level
                         (UG guide: remove grad-only; grad guide: remove ug-only);
                         exactly one candidate remains
  5. degree_title      – Exactly one candidate has the guide's degree_title_guide
                         as a substring of its current_programs + historical_programs

Resolution anchor classes written to output rows:
  deterministic_resolved_<signal_id>        single signal fired
  deterministic_resolved_multi              multiple signals fired and agreed
  ambiguous_residual                        no signal resolved

Outputs:
  data/program_guides/bridge/guides_resolved/{program_code}.json
  data/program_guides/bridge/resolution_log_deterministic.json
"""

import csv
import json
import os
from collections import defaultdict
from datetime import date

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANONICAL_CSV      = os.path.join(REPO_ROOT, "data", "canonical_courses.csv")
BRIDGE_INDEX       = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "index.json")
BRIDGE_GUIDE_DIR   = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "guides")
RESOLVED_GUIDE_DIR = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "guides_resolved")
LOG_PATH           = os.path.join(REPO_ROOT, "data", "program_guides", "bridge", "resolution_log_deterministic.json")

# ---------------------------------------------------------------------------
# Degree-level classification helpers
# ---------------------------------------------------------------------------
GRAD_KEYWORDS = [
    "master", "mba", "m.s.", "m.a.", "mat ", "mat,", "graduate",
    "msed", "ms,", "ms ", "doctoral", "certificate of",
]
UG_KEYWORDS = ["bachelor", "b.s.", "b.a.", "bsn", "associate"]


def degree_level_of_guide(degree_title: str) -> str:
    """Return 'ug', 'grad', or 'unk' for a guide's degree title."""
    dt = degree_title.lower()
    if any(k in dt for k in ["bachelor", "b.a.", "b.s.", "bsn", "associate"]):
        return "ug"
    if any(k in dt for k in ["master", "mba", "m.s.", "m.a.", "mat", "graduate"]):
        return "grad"
    return "unk"


def programs_text(cc: dict) -> str:
    """Concatenate current + historical programs as a single lowercase string."""
    return (
        (cc.get("current_programs") or "") + " " +
        (cc.get("historical_programs") or "")
    ).lower()


def is_grad_only(cc: dict) -> bool:
    """True when candidate programs contain only graduate-level program titles."""
    pt = programs_text(cc)
    if not pt.strip():
        return False  # no programs → can't classify
    has_grad = any(k in pt for k in GRAD_KEYWORDS)
    has_ug   = any(k in pt for k in UG_KEYWORDS)
    return has_grad and not has_ug


def is_ug_only(cc: dict) -> bool:
    """True when candidate programs contain only undergraduate-level program titles."""
    pt = programs_text(cc)
    if not pt.strip():
        return False
    has_grad = any(k in pt for k in GRAD_KEYWORDS)
    has_ug   = any(k in pt for k in UG_KEYWORDS)
    return has_ug and not has_grad


# ---------------------------------------------------------------------------
# Signal functions
# Return the single winning course_code, or None if the signal does not resolve.
# ---------------------------------------------------------------------------

def sig_cu_match(row: dict, canonical: dict) -> str | None:
    """Signal 1: SP row sp_cus matches exactly one candidate's canonical_cus."""
    if row.get("surface") != "sp":
        return None
    sp_cus = row.get("sp_cus")
    if sp_cus is None:
        return None
    cands = row.get("canonical_candidate_codes", [])
    matching = [
        c for c in cands
        if canonical.get(c, {}).get("canonical_cus") == str(sp_cus)
    ]
    return matching[0] if len(matching) == 1 else None


def sig_one_active(row: dict, canonical: dict) -> str | None:
    """Signal 2: Exactly one candidate has active_current = True."""
    cands = row.get("canonical_candidate_codes", [])
    active = [c for c in cands if canonical.get(c, {}).get("active_current") == "True"]
    return active[0] if len(active) == 1 else None


def sig_a_suffix_cert(row: dict, canonical: dict, family: str) -> str | None:
    """Signal 3: Cert A-suffix candidates removed from degree guides; one non-cert remains."""
    if "cert" in family.lower():
        return None
    cands = row.get("canonical_candidate_codes", [])
    cert_only = [
        c for c in cands
        if c.endswith("A") and canonical.get(c, {}).get("contexts_seen") == "cert"
    ]
    if not cert_only:
        return None
    non_cert = [c for c in cands if c not in cert_only]
    return non_cert[0] if len(non_cert) == 1 else None


def sig_degree_level(row: dict, canonical: dict, guide_level: str) -> str | None:
    """Signal 4: Remove candidates exclusively scoped to the opposite degree level."""
    cands = row.get("canonical_candidate_codes", [])
    if guide_level == "ug":
        survivors = [c for c in cands if not is_grad_only(canonical.get(c, {}))]
    elif guide_level == "grad":
        survivors = [c for c in cands if not is_ug_only(canonical.get(c, {}))]
    else:
        return None
    return survivors[0] if len(survivors) == 1 else None


def sig_degree_title(row: dict, canonical: dict, degree_title: str) -> str | None:
    """Signal 5: Exactly one candidate has degree_title_guide in its current+historical programs."""
    if not degree_title:
        return None
    dt_lower = degree_title.lower()
    cands = row.get("canonical_candidate_codes", [])
    matching = [c for c in cands if dt_lower in programs_text(canonical.get(c, {}))]
    return matching[0] if len(matching) == 1 else None


# ---------------------------------------------------------------------------
# Resolution logic
# ---------------------------------------------------------------------------

SIGNAL_FUNCS = [
    ("cu_match",      lambda row, cc, gl, dt, fam: sig_cu_match(row, cc)),
    ("one_active",    lambda row, cc, gl, dt, fam: sig_one_active(row, cc)),
    ("a_suffix_cert", lambda row, cc, gl, dt, fam: sig_a_suffix_cert(row, cc, fam)),
    ("degree_level",  lambda row, cc, gl, dt, fam: sig_degree_level(row, cc, gl)),
    ("degree_title",  lambda row, cc, gl, dt, fam: sig_degree_title(row, cc, dt)),
]

# Priority order for conflict resolution (lower index = higher priority).
# When signals disagree, the highest-priority signal wins.
SIGNAL_PRIORITY = ["cu_match", "one_active", "a_suffix_cert", "degree_level", "degree_title"]


def resolve_row(row: dict, canonical: dict, guide_level: str,
                degree_title: str, family: str):
    """
    Apply all signals. Return (resolved_code, [fired_signals], conflict_detail).
    conflict_detail is None when all fired signals agree, or a string when they
    disagreed and priority resolution was applied.
    """
    fired = {}  # signal_id -> resolved_code

    for sig_id, fn in SIGNAL_FUNCS:
        code = fn(row, canonical, guide_level, degree_title, family)
        if code is not None:
            fired[sig_id] = code

    if not fired:
        return None, [], None

    codes = set(fired.values())
    if len(codes) == 1:
        # All signals agree
        resolved_code = next(iter(codes))
        return resolved_code, list(fired.keys()), None

    # Signals disagree — resolve by priority: take the result of the highest-priority signal
    conflict_detail = "conflict_resolved_by_priority: " + ", ".join(
        f"{s}={c}" for s, c in fired.items()
    )
    for sig_id in SIGNAL_PRIORITY:
        if sig_id in fired:
            return fired[sig_id], [sig_id], conflict_detail

    # Fallback: should never reach here
    return None, [], "conflict_unresolvable"


def anchor_class_for(signals: list[str]) -> str:
    if not signals:
        return "ambiguous_residual"
    if len(signals) == 1:
        return f"deterministic_resolved_{signals[0]}"
    return "deterministic_resolved_multi"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(RESOLVED_GUIDE_DIR, exist_ok=True)

    # Load canonical courses
    canonical = {}
    with open(CANONICAL_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            canonical[row["course_code"]] = row
    print(f"Loaded {len(canonical)} canonical courses.")

    # Load bridge index
    with open(BRIDGE_INDEX, encoding="utf-8") as f:
        bridge_index = json.load(f)
    guide_entries = bridge_index["guide_index"]
    print(f"Bridge index: {len(guide_entries)} guides.")

    # ---------------------------------------------------------------------------
    # Accumulators
    # ---------------------------------------------------------------------------
    # Per-signal yield
    signal_yield         = defaultdict(int)   # signal_id -> rows resolved by that signal (possibly among others)
    signal_solo_yield    = defaultdict(int)   # signal_id -> rows where it was the ONLY signal
    multi_signal_count   = 0                  # rows resolved by 2+ agreeing signals
    conflict_resolved    = 0                  # rows resolved via priority after signal conflict
    residual_count       = 0
    total_ambiguous      = 0
    total_rows           = 0

    # Full resolution log entries
    log_entries = []

    processed_guides = 0
    warn_missing = []

    for entry in guide_entries:
        program_code = entry["program_code"]
        family       = entry.get("family", "")

        guide_path  = os.path.join(BRIDGE_GUIDE_DIR, f"{program_code}.json")
        if not os.path.exists(guide_path):
            warn_missing.append(program_code)
            continue

        with open(guide_path, encoding="utf-8") as f:
            guide = json.load(f)

        degree_title = guide.get("degree_title_guide", "")
        guide_level  = degree_level_of_guide(degree_title)

        new_rows = []
        for row in guide.get("roster_rows", []):
            total_rows += 1
            anchor_class = row.get("anchor_class", "")

            if not anchor_class.startswith("ambiguous"):
                # Pass through unchanged
                new_rows.append(row)
                continue

            total_ambiguous += 1
            resolved_code, fired_signals, conflict_detail = resolve_row(
                row, canonical, guide_level, degree_title, family
            )

            new_row = dict(row)

            if False:  # placeholder — conflict branch now handled via priority
                # Conflict case
                new_row["anchor_class"]             = "ambiguous_residual"
                new_row["resolution_signals"]        = fired_signals
                new_row["resolved_code"]             = None
                conflict_count += 1
                residual_count += 1
            elif resolved_code:
                new_anchor = anchor_class_for(fired_signals)
                new_row["anchor_class"]          = new_anchor
                new_row["resolved_code"]          = resolved_code
                new_row["resolution_signals"]     = fired_signals
                if conflict_detail:
                    new_row["resolution_conflict_note"] = conflict_detail

                for sig in fired_signals:
                    signal_yield[sig] += 1
                if conflict_detail:
                    conflict_resolved += 1
                elif len(fired_signals) == 1:
                    signal_solo_yield[fired_signals[0]] += 1
                else:
                    multi_signal_count += 1

                log_entries.append({
                    "program_code":       program_code,
                    "family":             family,
                    "surface":            row.get("surface"),
                    "guide_title_raw":    row.get("guide_title_raw"),
                    "original_cands":     row.get("canonical_candidate_codes", []),
                    "resolved_code":      resolved_code,
                    "anchor_class":       new_anchor,
                    "signals":            fired_signals,
                    "conflict_note":      conflict_detail,
                    "guide_level":        guide_level,
                    "sp_cus":             row.get("sp_cus"),
                })
            else:
                new_row["anchor_class"]             = "ambiguous_residual"
                new_row["resolved_code"]             = None
                new_row["resolution_signals"]        = []
                residual_count += 1

                log_entries.append({
                    "program_code":    program_code,
                    "family":          family,
                    "surface":         row.get("surface"),
                    "guide_title_raw": row.get("guide_title_raw"),
                    "original_cands":  row.get("canonical_candidate_codes", []),
                    "resolved_code":   None,
                    "anchor_class":    "ambiguous_residual",
                    "signals":         [],
                    "guide_level":     guide_level,
                    "sp_cus":          row.get("sp_cus"),
                })

            new_rows.append(new_row)

        # Write resolved guide
        new_guide = dict(guide)
        new_guide["roster_rows"] = new_rows
        out_path = os.path.join(RESOLVED_GUIDE_DIR, f"{program_code}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(new_guide, f, indent=2, ensure_ascii=False)

        processed_guides += 1

    # ---------------------------------------------------------------------------
    # Write resolution log
    # ---------------------------------------------------------------------------
    resolved_count = total_ambiguous - residual_count

    resolution_log = {
        "generated_on":              str(date.today()),
        "total_guides_processed":    processed_guides,
        "total_rows":                total_rows,
        "total_ambiguous_rows":      total_ambiguous,
        "total_resolved":            resolved_count,
        "total_ambiguous_residual":  residual_count,
        "total_conflict_resolved":   conflict_resolved,
        "resolution_rate":           round(resolved_count / total_ambiguous, 4) if total_ambiguous else 0,
        "signal_yield": {
            sig: {
                "rows_contributed_to":  signal_yield[sig],
                "rows_sole_signal":     signal_solo_yield[sig],
            }
            for sig in ["cu_match", "one_active", "a_suffix_cert", "degree_level", "degree_title"]
        },
        "multi_signal_clean_agree":  multi_signal_count,
        "conflict_priority_resolved": conflict_resolved,
        "warnings_missing_guides":   warn_missing,
        "entries": log_entries,
    }

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(resolution_log, f, indent=2, ensure_ascii=False)

    # ---------------------------------------------------------------------------
    # Stdout report
    # ---------------------------------------------------------------------------
    print()
    print("=" * 60)
    print("DETERMINISTIC AMBIGUITY RESOLVER — COMPLETE")
    print("=" * 60)
    print(f"  Guides processed:             {processed_guides}")
    print(f"  Total roster rows:            {total_rows}")
    print(f"  Total ambiguous rows:         {total_ambiguous}")
    print()
    print(f"  Resolved (deterministic):     {resolved_count}  ({resolved_count/total_ambiguous:.1%})")
    print(f"  — clean multi-signal agree:   {multi_signal_count}")
    print(f"  — conflict priority resolved: {conflict_resolved}")
    print(f"  Forwarded as residual:        {residual_count}  ({residual_count/total_ambiguous:.1%})")
    print()
    print("  Per-signal yield:")
    for sig in ["cu_match", "one_active", "a_suffix_cert", "degree_level", "degree_title"]:
        contrib = signal_yield[sig]
        solo    = signal_solo_yield[sig]
        print(f"    {sig:<20} contributed={contrib:>4}  sole={solo:>4}")
    print(f"    {'multi_signal':<20} rows={multi_signal_count:>4}")
    print()
    if warn_missing:
        print(f"  Missing guide files: {warn_missing}")
    print(f"  Resolved guide files: {RESOLVED_GUIDE_DIR}")
    print(f"  Resolution log:       {LOG_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
