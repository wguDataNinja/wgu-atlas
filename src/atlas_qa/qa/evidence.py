"""Evidence bundle construction for Atlas QA Session 05.

Assembles a typed EvidenceBundle from:
- RetrievalResult.selected_candidates  (fuzzy path)
- ExactLookupAnswer                    (exact path)

The bundle is deterministic — no model calls, no reranking, no scope changes.
Compare-mode inputs are rejected at construction time.
"""
from __future__ import annotations

from atlas_qa.qa.types import (
    AbstentionState,
    AnomalyDisclosure,
    EntityType,
    EvidenceArtifact,
    EvidenceBundle,
    EvidenceRef,
    ExactLookupAnswer,
    QAResponse,
    RetrievalResult,
    SourceFamily,
)

# Maximum artifacts per single-entity bundle (spec: 1–5).
_MAX_ARTIFACTS = 5


def _artifact_from_candidate(
    candidate,
    version_used: str,
    entity_code: str,
) -> EvidenceArtifact:
    """Convert a RetrievalCandidate to an EvidenceArtifact."""
    ref = EvidenceRef(
        source_type=candidate.source_family.value,
        artifact_id=candidate.source_object_identity,
        version=candidate.version or version_used,
    )
    return EvidenceArtifact(
        artifact_type=candidate.artifact_type,
        entity_code=candidate.entity_code,
        version=candidate.version or version_used,
        source_family=candidate.source_family,
        content=candidate.content_text,
        source_object_identity=candidate.source_object_identity,
        evidence_ref=ref,
    )


def bundle_from_retrieval(result: RetrievalResult) -> EvidenceBundle | QAResponse:
    """Build an EvidenceBundle from a RetrievalResult.

    Returns an EvidenceBundle on success or a QAResponse abstention on failure.
    """
    raw_query = result.raw_query

    # Propagate upstream stop reason.
    if result.stop_reason is not None:
        return _abstain(raw_query, AbstentionState.INSUFFICIENT_EVIDENCE,
                        diag={"stop_reason": result.stop_reason.value})

    candidates = result.selected_candidates
    if not candidates:
        return _abstain(raw_query, AbstentionState.INSUFFICIENT_EVIDENCE,
                        diag={"reason": "selected_candidates is empty"})

    # Reject compare mode — no mixed-version bundles in Session 05.
    partition = result.request.partition if result.request else None
    if partition and partition.compare_mode:
        return _abstain(raw_query, AbstentionState.OUT_OF_SCOPE,
                        diag={"reason": "compare_mode not supported in Session 05"})

    # Derive entity_code and entity_type from partition or first candidate.
    if partition and partition.entity_codes:
        entity_code = partition.entity_codes[0]
        entity_type = partition.entity_type
    else:
        entity_code = candidates[0].entity_code
        entity_type = None

    # Resolve entity type from candidates if partition didn't provide it.
    if entity_type is None:
        for c in candidates:
            if c.artifact_type in ("course_card",):
                entity_type = EntityType.COURSE
                break
            elif c.artifact_type in ("program_version_card", "guide_section_card"):
                entity_type = EntityType.PROGRAM
                break

    if entity_type is None:
        return _abstain(raw_query, AbstentionState.INSUFFICIENT_EVIDENCE,
                        diag={"reason": "could not determine entity_type from candidates"})

    # Determine version_used from partition scope or first candidate.
    version_scope = partition.version_scope if partition else []
    version_used = version_scope[0] if version_scope else (candidates[0].version or "unknown")

    # Verify all candidates are within the resolved version — reject mismatches.
    versioned_candidates = [
        c for c in candidates
        if c.version is None or c.version == version_used
    ]
    if not versioned_candidates:
        return _abstain(raw_query, AbstentionState.INSUFFICIENT_EVIDENCE,
                        diag={"reason": "all candidates are from wrong version"})

    # Cap at max artifacts.
    selected = versioned_candidates[:_MAX_ARTIFACTS]

    source_scope = list({c.source_family for c in selected})

    artifacts = [_artifact_from_candidate(c, version_used, entity_code) for c in selected]

    # Carry upstream scope notes as anomaly disclosures where relevant.
    notes = list(partition.notes) if partition else []
    anomaly_disclosures = _notes_to_disclosures(notes)

    return EvidenceBundle(
        entity_code=entity_code,
        entity_type=entity_type,
        version_used=version_used,
        source_scope=source_scope,
        artifacts=artifacts,
        anomaly_disclosures=anomaly_disclosures,
        notes=notes,
        from_exact_path=False,
    )


def bundle_from_exact(answer: ExactLookupAnswer) -> EvidenceBundle | QAResponse:
    """Build an EvidenceBundle from an ExactLookupAnswer.

    Returns an EvidenceBundle on success or a QAResponse abstention on failure.
    """
    # Propagate upstream abstention if answer carries none.
    if answer is None:
        return _abstain("", AbstentionState.INSUFFICIENT_EVIDENCE,
                        diag={"reason": "null ExactLookupAnswer"})

    source_object_identity = answer.source_object_identity
    version_used = answer.resolved_version

    # Determine source family from the artifact identity prefix.
    if "course_card" in source_object_identity or answer.entity_type == EntityType.COURSE:
        artifact_type = "course_card"
        source_family = SourceFamily.CATALOG
    else:
        artifact_type = "program_version_card"
        source_family = SourceFamily.CATALOG

    ref = EvidenceRef(
        source_type=source_family.value,
        artifact_id=source_object_identity,
        version=version_used,
    )

    content: dict | str
    if isinstance(answer.field_value, dict):
        content = answer.field_value
    else:
        content = str(answer.field_value) if answer.field_value is not None else ""

    artifact = EvidenceArtifact(
        artifact_type=artifact_type,
        entity_code=answer.entity_code,
        version=version_used,
        source_family=source_family,
        content=content,
        source_object_identity=source_object_identity,
        evidence_ref=ref,
    )

    return EvidenceBundle(
        entity_code=answer.entity_code,
        entity_type=answer.entity_type,
        version_used=version_used,
        source_scope=[source_family],
        artifacts=[artifact],
        anomaly_disclosures=list(answer.anomaly_disclosures),
        notes=[],
        from_exact_path=True,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _notes_to_disclosures(notes: list[str]) -> list[AnomalyDisclosure]:
    """Convert partition scope notes to AnomalyDisclosure objects where they
    match known anomaly patterns (C179 short-text, D554 guide block,
    version-conflict). Unrecognised notes are ignored at this layer."""
    disclosures: list[AnomalyDisclosure] = []
    for note in notes:
        note_lower = note.lower()
        if "cat_short_text" in note_lower or "c179" in note_lower or "short text" in note_lower:
            disclosures.append(AnomalyDisclosure(
                anomaly_type="cat_short_text",
                message=note,
            ))
        elif "guide_misrouted" in note_lower or "d554" in note_lower or "guide block" in note_lower:
            disclosures.append(AnomalyDisclosure(
                anomaly_type="guide_misrouted_text",
                message=note,
            ))
        elif "version_conflict" in note_lower or "version mismatch" in note_lower:
            disclosures.append(AnomalyDisclosure(
                anomaly_type="version_conflict",
                message=note,
            ))
    return disclosures


def _abstain(raw_query: str, state: AbstentionState, diag: dict | None = None) -> QAResponse:
    return QAResponse(
        raw_query=raw_query,
        abstention=state,
        diagnostics=diag or {},
    )
