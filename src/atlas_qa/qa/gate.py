"""Deterministic answerability / sufficiency gate for Atlas QA Session 05.

All checks are structural — no model calls. If the gate fails, the answer path
returns an abstention state rather than attempting generation.
"""
from __future__ import annotations

from atlas_qa.qa.types import (
    AbstentionState,
    AnswerabilityResult,
    EvidenceBundle,
    SectionScope,
)

# Section types that require at least one guide_section_card artifact.
_GUIDE_SECTION_REQUIRED: frozenset[SectionScope] = frozenset({
    SectionScope.COMPETENCIES,
    SectionScope.CAPSTONE,
    SectionScope.AREAS_OF_STUDY,
})

# Anomaly types that are hard-blocking for guide-content requests.
_GUIDE_BLOCK_ANOMALY = "guide_misrouted_text"


def check_answerability(
    bundle: EvidenceBundle,
    section_scope: SectionScope | None = None,
) -> AnswerabilityResult:
    """Deterministic gate over an EvidenceBundle.

    Returns AnswerabilityResult(answerable=True) if all checks pass, or
    AnswerabilityResult(answerable=False, abstention_reason=...) on first
    failure.

    Checks (in order):
    1. Bundle is non-empty.
    2. At least one artifact matches the resolved entity code.
    3. Compare mode not present (multi-version = out_of_scope before wrong-version check).
    4. All artifacts are within the resolved version scope.
    5. If a guide-section scope is required, at least one guide_section_card is present.
    6. No unresolvable D554 guide block that blocks this query type.
    """
    notes: list[str] = []

    # 1. Non-empty bundle.
    if not bundle.artifacts:
        return AnswerabilityResult(
            answerable=False,
            abstention_reason=AbstentionState.INSUFFICIENT_EVIDENCE,
            gate_notes=["bundle is empty"],
        )

    # 2. At least one artifact matches the resolved entity code.
    matching = [a for a in bundle.artifacts if a.entity_code == bundle.entity_code]
    if not matching:
        return AnswerabilityResult(
            answerable=False,
            abstention_reason=AbstentionState.INSUFFICIENT_EVIDENCE,
            gate_notes=[
                f"no artifact matches entity_code={bundle.entity_code}"
            ],
        )

    # 3. Compare mode check — must precede wrong-version check.
    # Session 05 handles single-entity queries only. Multi-version bundles indicate
    # compare mode (Class D) and must be rejected with out_of_scope.
    distinct_versions = {a.version for a in bundle.artifacts}
    if len(distinct_versions) > 1:
        return AnswerabilityResult(
            answerable=False,
            abstention_reason=AbstentionState.OUT_OF_SCOPE,
            gate_notes=[
                f"compare mode detected: multiple versions in bundle: {distinct_versions}"
            ],
        )

    # 4. Version coverage — all artifacts within the resolved version.
    wrong_version = [
        a for a in bundle.artifacts
        if a.version != bundle.version_used
    ]
    if wrong_version:
        bad_versions = list({a.version for a in wrong_version})
        return AnswerabilityResult(
            answerable=False,
            abstention_reason=AbstentionState.INSUFFICIENT_EVIDENCE,
            gate_notes=[
                f"artifacts with wrong version: {bad_versions} (expected {bundle.version_used})"
            ],
        )

    # 5. Guide-section scope requirement.
    if section_scope in _GUIDE_SECTION_REQUIRED:
        guide_artifacts = [
            a for a in bundle.artifacts if a.artifact_type == "guide_section_card"
        ]
        if not guide_artifacts:
            return AnswerabilityResult(
                answerable=False,
                abstention_reason=AbstentionState.INSUFFICIENT_EVIDENCE,
                gate_notes=[
                    f"section_scope={section_scope.value} requires guide_section_card "
                    "but none present in bundle"
                ],
            )

    # 6. D554 guide block: if guide content was requested and a guide_misrouted_text
    #    disclosure is present, the guide content is blocked.
    if section_scope in _GUIDE_SECTION_REQUIRED:
        for disclosure in bundle.anomaly_disclosures:
            if disclosure.anomaly_type == _GUIDE_BLOCK_ANOMALY:
                return AnswerabilityResult(
                    answerable=False,
                    abstention_reason=AbstentionState.INSUFFICIENT_EVIDENCE,
                    gate_notes=[f"D554 guide block: {disclosure.message}"],
                )

    return AnswerabilityResult(
        answerable=True,
        abstention_reason=None,
        gate_notes=notes,
    )
