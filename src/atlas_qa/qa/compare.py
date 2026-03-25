"""Explicit compare mode for Atlas QA Session 06.

Handles Class D queries — explicit version comparison only.
No implicit compare behavior. Two versions max for v1 compare path.

Architecture invariants enforced here:
- Compare mode only activates on explicit compare intent (detected below).
- Version resolution is version-scoped before retrieval begins.
- Two versions max.
- CompareEvidenceBundle is always version-bucketed by side.
- If version resolution is ambiguous, compare abstains or clarifies.
- If diff card support is absent, falls back to strict two-version bundles.
- All compare answers require both version tokens and citations.
- Known conflict/anomaly programs carry required disclosures.

Pipeline:
1. detect_compare_intent(raw_query) → bool
2. extract_compare_versions(raw_query) → (from_version, to_version) or None pair
3. resolve_compare_request(raw_query, entity_code, entity_type) → CompareRequest | None
4. build_compare_bundle(request) → CompareEvidenceBundle | CompareAnswer(abstention)
5. generate_compare_answer(bundle, question) → CompareGenerationOutput
6. compare_post_check(gen_output, bundle) → ComparePostCheckResult
7. answer_compare(raw_query, entity_code, entity_type) → CompareAnswer
"""
from __future__ import annotations

import json
import re
from typing import Callable

from pydantic import BaseModel, ValidationError

from atlas_qa.qa.compare_prompts import render_compare_prompt
from atlas_qa.qa.loaders import get_program_version_cards, get_version_diff_cards
from atlas_qa.qa.source_authority import VERSION_CONFLICT_PROGRAMS
from atlas_qa.qa.types import (
    AbstentionState,
    AnomalyDisclosure,
    CompareAnswer,
    CompareEvidenceBundle,
    CompareGenerationOutput,
    ComparePostCheckResult,
    CompareRequest,
    CompareSide,
    EntityType,
    EvidenceArtifact,
    EvidenceRef,
    SourceFamily,
    VersionDiffCard,
)

# ---------------------------------------------------------------------------
# Compare intent detection
# ---------------------------------------------------------------------------

# Keywords that signal explicit compare intent.
_COMPARE_KEYWORDS = re.compile(
    r"\b(changed?|changes?|compared?|comparison|difference[s]?|differ[s]?|"
    r"added|removed?|deleted?|vs\.?|versus|between\b.*\band\b|from\b.*\bto\b|"
    r"what was different|what is different|how has|how did)\b",
    re.IGNORECASE,
)

# Version string patterns (both YYYY-MM catalog and YYYYMM guide formats).
_VERSION_RE = re.compile(r"\b(\d{4}-\d{2}|\d{6})\b")


def detect_compare_intent(raw_query: str) -> bool:
    """Return True if the query contains explicit compare intent keywords
    AND references at least two version strings.

    Compare mode is explicit-only per architecture invariant 1.
    """
    has_keyword = bool(_COMPARE_KEYWORDS.search(raw_query))
    versions = _VERSION_RE.findall(raw_query)
    return has_keyword and len(versions) >= 2


def extract_compare_versions(raw_query: str) -> tuple[str | None, str | None]:
    """Extract the two version strings from an explicit compare query.

    Returns (from_version, to_version) in the order they appear in the query.
    Returns (None, None) if fewer than two version strings are found.
    Returns (first, None) if exactly one version is found.
    """
    versions = _VERSION_RE.findall(raw_query)
    if len(versions) == 0:
        return None, None
    if len(versions) == 1:
        return versions[0], None
    return versions[0], versions[1]


def resolve_compare_request(
    raw_query: str,
    entity_code: str,
    entity_type: EntityType,
) -> CompareRequest | None:
    """Build a CompareRequest from a raw compare query and a resolved entity.

    Returns None if the version pair cannot be determined (abstain at call site).
    """
    from_version, to_version = extract_compare_versions(raw_query)
    if from_version is None or to_version is None:
        return None

    return CompareRequest(
        raw_query=raw_query,
        entity_code=entity_code,
        entity_type=entity_type,
        from_version=from_version,
        to_version=to_version,
    )


# ---------------------------------------------------------------------------
# Compare evidence bundle construction
# ---------------------------------------------------------------------------


def _find_diff_card(
    entity_code: str,
    from_version: str,
    to_version: str,
) -> VersionDiffCard | None:
    """Look up a VersionDiffCard for the entity/version pair from the corpus."""
    try:
        diff_cards = get_version_diff_cards()
    except Exception:
        return None
    for card in diff_cards:
        if (
            card.entity_id == entity_code
            and card.from_version == from_version
            and card.to_version == to_version
        ):
            return card
    return None


def _artifact_from_diff_card(card: VersionDiffCard) -> EvidenceArtifact:
    ref_id = card.evidence_refs[0].artifact_id if card.evidence_refs else "version_diff_card"
    ref = EvidenceRef(
        source_type="catalog_diff",
        artifact_id=ref_id,
        version=f"{card.from_version}\u2192{card.to_version}",
    )
    content = {
        "added": card.added,
        "removed": card.removed,
        "changed": card.changed,
    }
    return EvidenceArtifact(
        artifact_type="version_diff_card",
        entity_code=card.entity_id,
        version=card.to_version,
        source_family=SourceFamily.CATALOG,
        content=content,
        source_object_identity=ref_id,
        evidence_ref=ref,
    )


def _artifact_from_program_card(card, version_label: str) -> EvidenceArtifact:
    identity = f"program_version_card:{card.program_code}:{card.catalog_version}"
    ref = EvidenceRef(
        source_type="catalog",
        artifact_id=identity,
        version=card.catalog_version,
    )
    content = {
        "program_code": card.program_code,
        "degree_title": card.degree_title,
        "college": card.college,
        "total_cus": card.total_cus,
        "catalog_version": card.catalog_version,
        "course_codes": card.course_codes,
    }
    return EvidenceArtifact(
        artifact_type="program_version_card",
        entity_code=card.program_code,
        version=card.catalog_version,
        source_family=SourceFamily.CATALOG,
        content=content,
        source_object_identity=identity,
        evidence_ref=ref,
    )


def _anomaly_disclosures_for_entity(entity_code: str) -> list[AnomalyDisclosure]:
    """Return required anomaly disclosures for known conflict entities."""
    disclosures: list[AnomalyDisclosure] = []
    if entity_code in VERSION_CONFLICT_PROGRAMS:
        conflict = VERSION_CONFLICT_PROGRAMS[entity_code]
        cat_v = conflict.get("catalog_version", "unknown")
        guide_v = conflict.get("guide_version", "unknown")
        disclosures.append(AnomalyDisclosure(
            anomaly_type="version_conflict",
            message=(
                f"{entity_code} has a version conflict: "
                f"catalog={cat_v}, guide={guide_v}. "
                "Both version tokens must appear in any answer about this entity."
            ),
        ))
    return disclosures


def build_compare_bundle(
    request: CompareRequest,
) -> CompareEvidenceBundle | CompareAnswer:
    """Build a CompareEvidenceBundle from a CompareRequest.

    Strategy (per spec locked decision 3):
    1. Try to find a VersionDiffCard for the entity/version pair.
       If found, use it as the primary compare substrate.
    2. If no diff card exists, fall back to strict two-version evidence bundles:
       look up entity cards for each version separately.
    3. If either version's evidence cannot be found, return a CompareAnswer abstention.
    """
    entity_code = request.entity_code
    from_version = request.from_version
    to_version = request.to_version
    entity_type = request.entity_type

    anomaly_disclosures = _anomaly_disclosures_for_entity(entity_code)

    # --- Path 1: version_diff_card ---
    diff_card = _find_diff_card(entity_code, from_version, to_version)

    if diff_card is not None:
        diff_artifact = _artifact_from_diff_card(diff_card)
        from_side = CompareSide(version=from_version, artifacts=[diff_artifact])
        to_side = CompareSide(version=to_version, artifacts=[])
        return CompareEvidenceBundle(
            entity_code=entity_code,
            entity_type=entity_type,
            from_version=from_version,
            to_version=to_version,
            source_scope=[SourceFamily.CATALOG],
            from_side=from_side,
            to_side=to_side,
            diff_card=diff_card,
            anomaly_disclosures=anomaly_disclosures,
            notes=["version_diff_card used as compare substrate"],
        )

    # --- Path 2: strict two-version fallback ---
    # Load program cards and find matching versions.
    try:
        program_cards = get_program_version_cards()
    except Exception as exc:
        return _compare_abstain(
            request.raw_query,
            entity_code,
            entity_type,
            from_version,
            to_version,
            AbstentionState.INSUFFICIENT_EVIDENCE,
            diag={"reason": f"corpus unavailable: {exc}"},
        )

    # Collect cards for from_version and to_version.
    from_cards = [
        c for c in program_cards.values()
        if c.program_code == entity_code and c.catalog_version == from_version
    ]
    to_cards = [
        c for c in program_cards.values()
        if c.program_code == entity_code and c.catalog_version == to_version
    ]

    if not from_cards and not to_cards:
        return _compare_abstain(
            request.raw_query,
            entity_code,
            entity_type,
            from_version,
            to_version,
            AbstentionState.INSUFFICIENT_EVIDENCE,
            diag={"reason": f"no corpus cards found for {entity_code} at {from_version} or {to_version}"},
        )

    from_artifacts = [_artifact_from_program_card(c, from_version) for c in from_cards[:2]]
    to_artifacts = [_artifact_from_program_card(c, to_version) for c in to_cards[:2]]

    # If one side is empty, record the gap but do not hard-block — the model
    # must state the missing side explicitly.
    notes: list[str] = ["two-version fallback used (no version_diff_card found)"]
    if not from_artifacts:
        notes.append(f"no corpus card found for {entity_code} at from_version={from_version}")
    if not to_artifacts:
        notes.append(f"no corpus card found for {entity_code} at to_version={to_version}")

    # Require at least one artifact on at least one side to proceed.
    if not from_artifacts and not to_artifacts:
        return _compare_abstain(
            request.raw_query,
            entity_code,
            entity_type,
            from_version,
            to_version,
            AbstentionState.INSUFFICIENT_EVIDENCE,
            diag={"reason": "both sides empty in two-version fallback"},
        )

    source_scope = list({a.source_family for a in from_artifacts + to_artifacts})

    return CompareEvidenceBundle(
        entity_code=entity_code,
        entity_type=entity_type,
        from_version=from_version,
        to_version=to_version,
        source_scope=source_scope,
        from_side=CompareSide(version=from_version, artifacts=from_artifacts),
        to_side=CompareSide(version=to_version, artifacts=to_artifacts),
        diff_card=None,
        anomaly_disclosures=anomaly_disclosures,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Compare generation
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "llama3"


class _CompareModelOutput(BaseModel):
    answer_text: str | None = None
    cited_evidence_ids: list[str] = []
    from_version_disclosed: str | None = None
    to_version_disclosed: str | None = None
    abstain: bool = False


def generate_compare_answer(
    bundle: CompareEvidenceBundle,
    question: str,
    model_name: str = DEFAULT_MODEL,
) -> CompareGenerationOutput:
    """Call the LLM with the compare prompt and return a typed CompareGenerationOutput."""
    from atlas_qa.llm.client import generate

    prompt = render_compare_prompt(bundle, question)
    llm_result = generate(model_name, prompt)
    raw_text = llm_result.raw_text or ""

    if llm_result.llm_failure or not raw_text.strip():
        return CompareGenerationOutput(
            raw_text=raw_text,
            answer_text=None,
            llm_failure=True,
        )

    json_text = _extract_json(raw_text)

    try:
        data = json.loads(json_text)
    except (json.JSONDecodeError, ValueError):
        return CompareGenerationOutput(
            raw_text=raw_text,
            answer_text=None,
            parse_error=True,
            schema_error=True,
        )

    try:
        parsed = _CompareModelOutput(**data)
    except (ValidationError, TypeError):
        return CompareGenerationOutput(
            raw_text=raw_text,
            answer_text=None,
            schema_error=True,
        )

    if parsed.abstain or not parsed.answer_text:
        return CompareGenerationOutput(
            raw_text=raw_text,
            answer_text=None,
            cited_evidence_ids=parsed.cited_evidence_ids,
            from_version_disclosed=parsed.from_version_disclosed,
            to_version_disclosed=parsed.to_version_disclosed,
        )

    return CompareGenerationOutput(
        raw_text=raw_text,
        answer_text=parsed.answer_text,
        cited_evidence_ids=parsed.cited_evidence_ids,
        from_version_disclosed=parsed.from_version_disclosed,
        to_version_disclosed=parsed.to_version_disclosed,
    )


def _extract_json(text: str) -> str:
    s = text.strip()
    if s.startswith("```"):
        lines = s.splitlines()[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    start = s.find("{")
    end = s.rfind("}")
    if start != -1 and end != -1 and end > start:
        return s[start : end + 1]
    return s


# ---------------------------------------------------------------------------
# Compare post-check
# ---------------------------------------------------------------------------


def compare_post_check(
    gen_output: CompareGenerationOutput,
    bundle: CompareEvidenceBundle,
) -> ComparePostCheckResult:
    """Deterministic post-check for a compare answer.

    Checks:
    1. Schema valid: no parse_error, schema_error, or llm_failure.
    2. Both version tokens named in answer_text.
    3. At least one citation from each non-empty side is present
       (or diff card citation if diff card path was used).
    """
    failure_reasons: list[str] = []

    # 1. Schema validity.
    schema_valid = (
        not gen_output.parse_error
        and not gen_output.schema_error
        and not gen_output.llm_failure
    )
    if not schema_valid:
        failure_reasons.append("compare generation output failed schema/LLM check")

    answer_text = gen_output.answer_text or ""

    # 2. Both version tokens named.
    from_version_named = bool(bundle.from_version and bundle.from_version in answer_text)
    to_version_named = bool(bundle.to_version and bundle.to_version in answer_text)
    if not from_version_named:
        failure_reasons.append(
            f"from_version '{bundle.from_version}' not named in answer_text"
        )
    if not to_version_named:
        failure_reasons.append(
            f"to_version '{bundle.to_version}' not named in answer_text"
        )

    # 3. Citation presence.
    all_artifacts: list[EvidenceArtifact] = (
        bundle.from_side.artifacts + bundle.to_side.artifacts
    )
    # Diff card artifact identity if present.
    if bundle.diff_card and bundle.diff_card.evidence_refs:
        diff_id = bundle.diff_card.evidence_refs[0].artifact_id
    else:
        diff_id = None

    bundle_ids: set[str] = {a.source_object_identity for a in all_artifacts}
    if diff_id:
        bundle_ids.add(diff_id)

    cited = set(gen_output.cited_evidence_ids)
    citation_ids_present = bool(
        (cited & bundle_ids)
        or any(bid in answer_text for bid in bundle_ids)
        or (diff_id and diff_id in answer_text)
    )
    if not citation_ids_present:
        failure_reasons.append(
            f"no bundle artifact IDs found in cited_evidence_ids or answer_text "
            f"(bundle IDs: {sorted(bundle_ids)})"
        )

    passed = schema_valid and from_version_named and to_version_named and citation_ids_present

    return ComparePostCheckResult(
        passed=passed,
        from_version_named=from_version_named,
        to_version_named=to_version_named,
        citation_ids_present=citation_ids_present,
        schema_valid=schema_valid,
        failure_reasons=failure_reasons,
    )


# ---------------------------------------------------------------------------
# Top-level compare orchestrator
# ---------------------------------------------------------------------------


def answer_compare(
    raw_query: str,
    entity_code: str,
    entity_type: EntityType,
    model_name: str = DEFAULT_MODEL,
    _generate_fn: Callable | None = None,
) -> CompareAnswer:
    """Full compare pipeline: resolve → bundle → generate → post-check.

    _generate_fn is injectable for testing (replaces the real LLM call).
    If _generate_fn is None, generate_compare_answer() is called directly.
    """
    # Step 1 — Resolve compare request.
    request = resolve_compare_request(raw_query, entity_code, entity_type)
    if request is None:
        return _compare_abstain(
            raw_query, entity_code, entity_type, None, None,
            AbstentionState.AMBIGUOUS_VERSION,
            diag={"reason": "could not extract two version strings from query"},
        )

    # Step 2 — Build compare evidence bundle.
    bundle_or_abstain = build_compare_bundle(request)
    if isinstance(bundle_or_abstain, CompareAnswer):
        return bundle_or_abstain
    bundle: CompareEvidenceBundle = bundle_or_abstain

    # Step 3 — Constrained compare generation.
    if _generate_fn is not None:
        gen_output: CompareGenerationOutput = _generate_fn(bundle, raw_query)
    else:
        try:
            gen_output = generate_compare_answer(bundle, raw_query, model_name=model_name)
        except Exception as exc:
            return CompareAnswer(
                raw_query=raw_query,
                entity_code=entity_code,
                entity_type=entity_type,
                from_version=request.from_version,
                to_version=request.to_version,
                abstention=AbstentionState.INSUFFICIENT_EVIDENCE,
                compare_bundle=bundle,
                diagnostics={"generation_error": str(exc)},
            )

    if gen_output.llm_failure or gen_output.answer_text is None:
        return CompareAnswer(
            raw_query=raw_query,
            entity_code=entity_code,
            entity_type=entity_type,
            from_version=request.from_version,
            to_version=request.to_version,
            abstention=AbstentionState.INSUFFICIENT_EVIDENCE,
            compare_bundle=bundle,
            generation_output=gen_output,
            diagnostics={"reason": "compare generation abstained or failed"},
        )

    # Step 4 — Compare post-check.
    postcheck_result = compare_post_check(gen_output, bundle)
    if not postcheck_result.passed:
        return CompareAnswer(
            raw_query=raw_query,
            entity_code=entity_code,
            entity_type=entity_type,
            from_version=request.from_version,
            to_version=request.to_version,
            abstention=AbstentionState.INSUFFICIENT_EVIDENCE,
            compare_bundle=bundle,
            generation_output=gen_output,
            postcheck=postcheck_result,
            diagnostics={"postcheck_failures": postcheck_result.failure_reasons},
        )

    return CompareAnswer(
        raw_query=raw_query,
        entity_code=entity_code,
        entity_type=entity_type,
        from_version=request.from_version,
        to_version=request.to_version,
        abstention=None,
        answer_text=gen_output.answer_text,
        compare_bundle=bundle,
        generation_output=gen_output,
        postcheck=postcheck_result,
        diagnostics={},
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _compare_abstain(
    raw_query: str,
    entity_code: str | None,
    entity_type: EntityType | None,
    from_version: str | None,
    to_version: str | None,
    state: AbstentionState,
    diag: dict | None = None,
) -> CompareAnswer:
    return CompareAnswer(
        raw_query=raw_query,
        entity_code=entity_code,
        entity_type=entity_type,
        from_version=from_version,
        to_version=to_version,
        abstention=state,
        diagnostics=diag or {},
    )
