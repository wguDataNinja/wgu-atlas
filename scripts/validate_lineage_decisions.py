"""
validate_lineage_decisions.py
==============================
Integrity check for data/lineage/lineage_decisions.json.

Validates structure, enums, uniqueness, cross-references, and export safety
for the lineage curation overlay artifact before any export step.

Exit codes:
  0 — no ERRORs (warnings and info may be present)
  1 — one or more ERRORs found

Usage:
  python3 scripts/validate_lineage_decisions.py
  python3 scripts/validate_lineage_decisions.py \\
      --decisions data/lineage/lineage_decisions.json \\
      --enrichment data/lineage/program_history_enrichment.json \\
      --programs public/data/programs.json \\
      --candidates data/lineage/program_link_candidates.json
"""

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DECISION_VALUES = {"approve_history", "reject_history", "pending_hitl", "pending_gap_check"}
DISPLAY_STATE_VALUES = {"show", "suppress", "hide_pending"}
PROGRAM_STATE_VALUES = {
    "history_approved", "history_excluded", "new_from_scratch",
    "pathway_variant", "no_meaningful_history", "pending_hitl", "pending_gap_check",
}
HISTORY_UI_STATE_VALUES = {"show", "hide_new", "hide_no_history", "hide_excluded", "hide_pending"}

EVENT_REQUIRED_KEYS = {
    "event_id", "decision", "display_state", "decided_by", "decided_at",
    "wording_guard", "change_summary_template", "zero_overlap_rationale", "notes",
}
PROGRAM_REQUIRED_KEYS = {
    "program_code", "program_state", "history_ui_state",
    "linked_event_id", "decided_by", "decided_at", "notes",
}

DECISION_TO_DISPLAY = {
    "approve_history": "show",
    "reject_history": "suppress",
    "pending_hitl": "hide_pending",
    "pending_gap_check": "hide_pending",
}

# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

_errors: list[str] = []
_warnings: list[str] = []
_infos: list[str] = []


def error(msg: str) -> None:
    _errors.append(f"  ERROR   {msg}")


def warning(msg: str) -> None:
    _warnings.append(f"  WARNING {msg}")


def info(msg: str) -> None:
    _infos.append(f"  INFO    {msg}")


def print_report() -> None:
    for line in _errors:
        print(line)
    for line in _warnings:
        print(line)
    for line in _infos:
        print(line)


# ---------------------------------------------------------------------------
# Group A — Structure
# ---------------------------------------------------------------------------

def check_structure(data: dict) -> tuple[list, list]:
    """Returns (event_decisions, program_decisions) or ([], []) on fatal failure."""
    # A2
    for key in ("schema_version", "last_updated", "event_decisions", "program_decisions"):
        if key not in data:
            error(f"A2: missing top-level key '{key}'")

    event_decisions = data.get("event_decisions", [])
    program_decisions = data.get("program_decisions", [])

    # A3
    if not isinstance(event_decisions, list) or len(event_decisions) == 0:
        error("A3: 'event_decisions' must be a non-empty array")
    if not isinstance(program_decisions, list) or len(program_decisions) == 0:
        error("A3: 'program_decisions' must be a non-empty array")

    # A4 — event entries
    for i, ev in enumerate(event_decisions):
        if not isinstance(ev, dict):
            error(f"A4: event_decisions[{i}] is not an object")
            continue
        missing = EVENT_REQUIRED_KEYS - ev.keys()
        if missing:
            eid = ev.get("event_id", f"index {i}")
            error(f"A4: event '{eid}' missing required keys: {sorted(missing)}")
        # A6 — wording_guard boolean
        if "wording_guard" in ev and not isinstance(ev["wording_guard"], bool):
            eid = ev.get("event_id", f"index {i}")
            error(f"A6: event '{eid}' wording_guard must be boolean, got {type(ev['wording_guard']).__name__}")

    # A5 — program entries
    for i, prog in enumerate(program_decisions):
        if not isinstance(prog, dict):
            error(f"A5: program_decisions[{i}] is not an object")
            continue
        missing = PROGRAM_REQUIRED_KEYS - prog.keys()
        if missing:
            code = prog.get("program_code", f"index {i}")
            error(f"A5: program '{code}' missing required keys: {sorted(missing)}")

    return event_decisions, program_decisions


# ---------------------------------------------------------------------------
# Group B — Enum values
# ---------------------------------------------------------------------------

def check_enums(event_decisions: list, program_decisions: list) -> None:
    for ev in event_decisions:
        if not isinstance(ev, dict):
            continue
        eid = ev.get("event_id", "?")
        if "decision" in ev and ev["decision"] not in DECISION_VALUES:
            error(f"B1: event '{eid}' invalid decision '{ev['decision']}'")
        if "display_state" in ev and ev["display_state"] not in DISPLAY_STATE_VALUES:
            error(f"B2: event '{eid}' invalid display_state '{ev['display_state']}'")

    for prog in program_decisions:
        if not isinstance(prog, dict):
            continue
        code = prog.get("program_code", "?")
        if "program_state" in prog and prog["program_state"] not in PROGRAM_STATE_VALUES:
            error(f"B3: program '{code}' invalid program_state '{prog['program_state']}'")
        if "history_ui_state" in prog and prog["history_ui_state"] not in HISTORY_UI_STATE_VALUES:
            error(f"B4: program '{code}' invalid history_ui_state '{prog['history_ui_state']}'")


# ---------------------------------------------------------------------------
# Group C — Uniqueness
# ---------------------------------------------------------------------------

def check_uniqueness(event_decisions: list, program_decisions: list) -> None:
    seen_eids: dict[str, int] = {}
    for i, ev in enumerate(event_decisions):
        if not isinstance(ev, dict):
            continue
        eid = ev.get("event_id")
        if eid is None:
            continue
        if eid in seen_eids:
            error(f"C1: duplicate event_id '{eid}' at indices {seen_eids[eid]} and {i}")
        else:
            seen_eids[eid] = i

    seen_codes: dict[str, int] = {}
    for i, prog in enumerate(program_decisions):
        if not isinstance(prog, dict):
            continue
        code = prog.get("program_code")
        if code is None:
            continue
        if code in seen_codes:
            error(f"C2: duplicate program_code '{code}' at indices {seen_codes[code]} and {i}")
        else:
            seen_codes[code] = i


# ---------------------------------------------------------------------------
# Group D — Internal cross-references
# ---------------------------------------------------------------------------

def check_cross_refs(event_decisions: list, program_decisions: list) -> None:
    known_event_ids = {ev.get("event_id") for ev in event_decisions if isinstance(ev, dict)}

    for prog in program_decisions:
        if not isinstance(prog, dict):
            continue
        code = prog.get("program_code", "?")
        linked = prog.get("linked_event_id")
        state = prog.get("program_state")

        # D1 — non-null linked_event_id must resolve
        if linked is not None and linked not in known_event_ids:
            error(f"D1: program '{code}' linked_event_id '{linked}' not found in event_decisions")

        # D2 — history_approved must have a linked event
        if state == "history_approved":
            if not linked:
                error(f"D2: program '{code}' has program_state 'history_approved' but linked_event_id is null")
            elif linked not in known_event_ids:
                error(f"D2: program '{code}' history_approved but linked event '{linked}' not found")


# ---------------------------------------------------------------------------
# Group E — Decision / display_state consistency
# ---------------------------------------------------------------------------

def check_decision_display_consistency(event_decisions: list) -> None:
    for ev in event_decisions:
        if not isinstance(ev, dict):
            continue
        eid = ev.get("event_id", "?")
        decision = ev.get("decision")
        display = ev.get("display_state")
        if decision not in DECISION_VALUES or display not in DISPLAY_STATE_VALUES:
            continue  # B-group errors already emitted
        expected = DECISION_TO_DISPLAY.get(decision)
        if expected and display != expected:
            error(
                f"E{list(DECISION_TO_DISPLAY.keys()).index(decision) + 1}: "
                f"event '{eid}' decision '{decision}' requires display_state '{expected}', got '{display}'"
            )


# ---------------------------------------------------------------------------
# Group F — Export safety
# ---------------------------------------------------------------------------

def check_export_safety(
    event_decisions: list,
    program_decisions: list,
    zero_jaccard_event_ids: set[str],
) -> None:
    event_map = {ev["event_id"]: ev for ev in event_decisions if isinstance(ev, dict) and "event_id" in ev}

    # F1, F2 — approve_history events need change_summary_template
    for ev in event_decisions:
        if not isinstance(ev, dict):
            continue
        eid = ev.get("event_id", "?")
        decision = ev.get("decision")
        template = ev.get("change_summary_template")
        wg = ev.get("wording_guard")

        if decision == "approve_history":
            if not template:
                error(f"F1: event '{eid}' decision=approve_history but change_summary_template is null/empty")
            if wg is True and not template:
                error(f"F2: event '{eid}' wording_guard=true and approve_history but change_summary_template is null/empty")

    # F3 — approve_history with any zero-Jaccard pair needs zero_overlap_rationale
    for ev in event_decisions:
        if not isinstance(ev, dict):
            continue
        eid = ev.get("event_id", "?")
        if ev.get("decision") == "approve_history" and eid in zero_jaccard_event_ids:
            if not ev.get("zero_overlap_rationale"):
                error(
                    f"F3: event '{eid}' is approve_history and has a pair with jaccard_overlap=0.0 "
                    f"but zero_overlap_rationale is null/empty"
                )

    # F4–F10 — program-level consistency
    for prog in program_decisions:
        if not isinstance(prog, dict):
            continue
        code = prog.get("program_code", "?")
        state = prog.get("program_state")
        ui = prog.get("history_ui_state")
        linked = prog.get("linked_event_id")

        # F4 — only history_approved may have show
        if ui == "show" and state != "history_approved":
            error(f"F4: program '{code}' has history_ui_state='show' but program_state='{state}'")

        # F5 — history_approved linked event must be approve_history
        if state == "history_approved" and linked and linked in event_map:
            ev_decision = event_map[linked].get("decision")
            if ev_decision != "approve_history":
                error(
                    f"F5: program '{code}' is history_approved but linked event '{linked}' "
                    f"has decision='{ev_decision}'"
                )

        # F6 — history_excluded linked event must not be approve_history
        if state == "history_excluded" and linked and linked in event_map:
            ev_decision = event_map[linked].get("decision")
            if ev_decision == "approve_history":
                error(
                    f"F6: program '{code}' is history_excluded but linked event '{linked}' "
                    f"has decision='approve_history'"
                )

        # F7 — pathway_variant must have null linked_event_id
        if state == "pathway_variant" and linked is not None:
            error(f"F7: program '{code}' is pathway_variant but linked_event_id='{linked}' (must be null)")

        # F8 — pending programs must have hide_pending
        if state in ("pending_hitl", "pending_gap_check") and ui != "hide_pending":
            error(f"F8: program '{code}' has program_state='{state}' but history_ui_state='{ui}' (must be hide_pending)")

        # F9 — new_from_scratch / no_meaningful_history / pathway_variant must hide_new or hide_no_history
        if state in ("new_from_scratch", "no_meaningful_history", "pathway_variant"):
            if ui not in ("hide_new", "hide_no_history"):
                error(
                    f"F9: program '{code}' has program_state='{state}' "
                    f"but history_ui_state='{ui}' (must be hide_new or hide_no_history)"
                )

        # F10 — history_excluded must have hide_excluded
        if state == "history_excluded" and ui != "hide_excluded":
            error(f"F10: program '{code}' is history_excluded but history_ui_state='{ui}' (must be hide_excluded)")


# ---------------------------------------------------------------------------
# Group G — Cross-checks against enrichment
# ---------------------------------------------------------------------------

def check_against_enrichment(
    event_decisions: list,
    program_decisions: list,
    enrichment: dict,
) -> set[str]:
    """Returns set of event_ids that have any pair with jaccard_overlap == 0.0."""
    enrichment_events = {ev["event_id"]: ev for ev in enrichment.get("events", []) if "event_id" in ev}
    decisions_event_ids = {ev.get("event_id") for ev in event_decisions if isinstance(ev, dict)}

    # Build zero-Jaccard set (F3 input)
    zero_jaccard_ids: set[str] = set()
    for eid, ev in enrichment_events.items():
        for pair in ev.get("pairs", []):
            if pair.get("jaccard_overlap") == 0.0:
                zero_jaccard_ids.add(eid)
                break

    # G1 — decision event IDs not in enrichment
    for eid in decisions_event_ids:
        if eid and eid not in enrichment_events:
            warning(f"G1: event '{eid}' in decisions but not found in program_history_enrichment.json")

    # G2 — enrichment events with site_worthy:true but no decisions entry
    for eid, ev in enrichment_events.items():
        if ev.get("site_worthy") is True and eid not in decisions_event_ids:
            info(f"G2: enrichment event '{eid}' has site_worthy=true but no entry in decisions (will be suppressed)")

    # G3 — approve_history overriding site_worthy:false
    for ev in event_decisions:
        if not isinstance(ev, dict):
            continue
        eid = ev.get("event_id")
        if ev.get("decision") == "approve_history" and eid in enrichment_events:
            if enrichment_events[eid].get("site_worthy") is False:
                warning(f"G3: event '{eid}' decision=approve_history overrides enrichment site_worthy=false")

    return zero_jaccard_ids


# ---------------------------------------------------------------------------
# Group G4 — Active programs with candidates but no decisions entry
# ---------------------------------------------------------------------------

def check_candidate_coverage(
    program_decisions: list,
    programs_data: dict,
    candidates_data: dict,
) -> None:
    decisions_codes = {p.get("program_code") for p in program_decisions if isinstance(p, dict)}

    # Build set of program codes mentioned in candidates
    candidate_codes: set[str] = set()
    for cand in candidates_data.get("candidates", []):
        for prog in cand.get("removed_programs", []):
            candidate_codes.add(prog.get("program_code", ""))
        for prog in cand.get("added_programs", []):
            candidate_codes.add(prog.get("program_code", ""))
    candidate_codes.discard("")

    # Build active/retired map from programs.json
    status_map: dict[str, str] = {}
    for prog in programs_data if isinstance(programs_data, list) else []:
        code = prog.get("program_code") or prog.get("code")
        status = prog.get("status", "").lower()
        if code:
            status_map[code] = status

    for code in sorted(candidate_codes):
        if code in decisions_codes:
            continue
        status = status_map.get(code, "unknown")
        if status == "active":
            warning(f"G4: active program '{code}' has lineage candidate but no program_decisions entry")
        else:
            info(f"G4: program '{code}' (status={status}) has lineage candidate but no program_decisions entry")


# ---------------------------------------------------------------------------
# Group H — Completeness reminders
# ---------------------------------------------------------------------------

def check_completeness(event_decisions: list, program_decisions: list) -> None:
    # H1 — pending wording_guard events without template
    for ev in event_decisions:
        if not isinstance(ev, dict):
            continue
        eid = ev.get("event_id", "?")
        if ev.get("wording_guard") is True and ev.get("decision") in ("pending_hitl", "pending_gap_check"):
            info(f"H1: event '{eid}' is pending with wording_guard=true — change_summary_template will be required before approval")

    # H2 — summary
    total_ev = len([e for e in event_decisions if isinstance(e, dict)])
    approve = len([e for e in event_decisions if isinstance(e, dict) and e.get("decision") == "approve_history"])
    reject = len([e for e in event_decisions if isinstance(e, dict) and e.get("decision") == "reject_history"])
    pending = total_ev - approve - reject

    total_prog = len([p for p in program_decisions if isinstance(p, dict)])
    show = len([p for p in program_decisions if isinstance(p, dict) and p.get("history_ui_state") == "show"])
    hide_pend = len([p for p in program_decisions if isinstance(p, dict) and p.get("history_ui_state") == "hide_pending"])
    other = total_prog - show - hide_pend

    info(
        f"H2: {total_ev} event_decisions ({approve} approve / {reject} reject / {pending} pending); "
        f"{total_prog} program_decisions ({show} show / {hide_pend} hide_pending / {other} other)"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate lineage_decisions.json")
    parser.add_argument(
        "--decisions",
        default="data/lineage/lineage_decisions.json",
        help="Path to lineage_decisions.json (required)",
    )
    parser.add_argument(
        "--enrichment",
        default="data/lineage/program_history_enrichment.json",
        help="Path to program_history_enrichment.json (optional, enables G1–G3, F3)",
    )
    parser.add_argument(
        "--programs",
        default="public/data/programs.json",
        help="Path to programs.json (optional, enables G4 active-program check)",
    )
    parser.add_argument(
        "--candidates",
        default="data/lineage/program_link_candidates.json",
        help="Path to program_link_candidates.json (optional, enables G4)",
    )
    args = parser.parse_args()

    decisions_path = Path(args.decisions)
    enrichment_path = Path(args.enrichment)
    programs_path = Path(args.programs)
    candidates_path = Path(args.candidates)

    # A1 — parse decisions file
    if not decisions_path.exists():
        print(f"  ERROR   A1: decisions file not found: {decisions_path}")
        return 1

    try:
        with decisions_path.open() as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  ERROR   A1: decisions file is not valid JSON: {e}")
        return 1

    # Run structural checks
    event_decisions, program_decisions = check_structure(data)
    if _errors:
        # Structure errors make further checks unreliable — still run enums/uniqueness
        pass

    check_enums(event_decisions, program_decisions)
    check_uniqueness(event_decisions, program_decisions)
    check_cross_refs(event_decisions, program_decisions)
    check_decision_display_consistency(event_decisions)

    # Load optional enrichment file
    zero_jaccard_ids: set[str] = set()
    if enrichment_path.exists():
        try:
            with enrichment_path.open() as f:
                enrichment = json.load(f)
            zero_jaccard_ids = check_against_enrichment(event_decisions, program_decisions, enrichment)
        except json.JSONDecodeError as e:
            warning(f"G-skip: enrichment file could not be parsed ({e}); G1–G3 and F3 skipped")
    else:
        warning(f"G-skip: enrichment file not found at {enrichment_path}; G1–G3 skipped; F3 cannot run")

    # F checks (F3 needs zero_jaccard_ids from enrichment)
    check_export_safety(event_decisions, program_decisions, zero_jaccard_ids)

    # G4 — active programs with candidates
    if programs_path.exists() and candidates_path.exists():
        try:
            with programs_path.open() as f:
                programs_data = json.load(f)
            with candidates_path.open() as f:
                candidates_data = json.load(f)
            check_candidate_coverage(program_decisions, programs_data, candidates_data)
        except json.JSONDecodeError as e:
            info(f"G4-skip: could not parse programs or candidates file ({e}); G4 skipped")
    else:
        info(f"G4-skip: programs or candidates file not found; G4 skipped")

    check_completeness(event_decisions, program_decisions)

    print_report()

    if _errors:
        print(f"\n  {len(_errors)} ERROR(s), {len(_warnings)} WARNING(s), {len(_infos)} INFO(s) — exit 1")
        return 1
    else:
        status = "clean" if not _warnings else f"{len(_warnings)} WARNING(s)"
        print(f"\n  0 ERRORs, {status}, {len(_infos)} INFO(s) — exit 0")
        return 0


if __name__ == "__main__":
    sys.exit(main())
