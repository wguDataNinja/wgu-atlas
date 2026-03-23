"""Strict prompt contract for Atlas QA Session 06 compare-mode generation.

The template is a plain string. All logic lives in compare.py — not here.

Contract rules:
- Supply two version-bucketed evidence sides — from_side and to_side.
- Instruct the model to summarize ONLY the deterministic differences visible
  in the supplied artifacts. No invented change categories.
- Require both version tokens to appear in the answer.
- Require citations from both sides.
- Instruct the model to abstain if the evidence does not support a difference claim.
- Target: fits in ~3K tokens for an 8B model.

Output schema expected from the model:
{
  "answer_text": "<comparison summary or null>",
  "cited_evidence_ids": ["<source_object_identity>", ...],
  "from_version_disclosed": "<from version string or null>",
  "to_version_disclosed": "<to version string or null>",
  "abstain": false
}
If the model cannot form a grounded comparison, it should set abstain=true.
"""
from __future__ import annotations

import json

from atlas_qa.qa.types import CompareEvidenceBundle, EvidenceArtifact

# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------

_COMPARE_SYSTEM_INSTRUCTIONS = """\
You are a precise academic catalog assistant. Compare the two versions of the
entity described below using ONLY the evidence artifacts provided. Do not use
any outside knowledge.

Rules:
1. Describe ONLY differences that are directly visible in the supplied evidence.
2. State BOTH version tokens explicitly — from_version_disclosed and to_version_disclosed.
3. Cite every artifact you use by including its ID in "cited_evidence_ids".
4. If the evidence shows no differences, state "No changes found between the two versions."
5. Do not invent change categories, infer beyond the artifacts, or reconcile sources.
6. If the evidence is insufficient to form a grounded comparison, set "abstain": true.
7. Respond with a single JSON object matching the schema below — nothing else.

Output schema:
{
  "answer_text": "<comparison summary as a plain string, or null>",
  "cited_evidence_ids": ["<artifact ID>", ...],
  "from_version_disclosed": "<from version string>",
  "to_version_disclosed": "<to version string>",
  "abstain": false
}
"""

_COMPARE_PROMPT_TEMPLATE = """\
{system_instructions}

--- FROM VERSION: {from_version} ---
{from_artifacts_block}
--- END FROM VERSION ---

--- TO VERSION: {to_version} ---
{to_artifacts_block}
--- END TO VERSION ---

USER QUESTION: {question}

Respond with JSON only."""


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _render_artifact(artifact: EvidenceArtifact) -> str:
    content_str: str
    if isinstance(artifact.content, dict):
        content_str = json.dumps(artifact.content, ensure_ascii=False, separators=(",", ":"))
    else:
        content_str = str(artifact.content)
    return (
        f"[{artifact.source_object_identity}]\n"
        f"type={artifact.artifact_type} entity={artifact.entity_code} "
        f"version={artifact.version} source={artifact.source_family.value}\n"
        f"{content_str}"
    )


def render_compare_prompt(bundle: CompareEvidenceBundle, question: str) -> str:
    """Render a compare generation prompt from a CompareEvidenceBundle.

    If a diff card is present, it is included in the from_side artifacts block
    as the authoritative difference summary. Both side artifacts are always
    rendered so the model can cite them.
    """
    from_artifacts = bundle.from_side.artifacts
    to_artifacts = bundle.to_side.artifacts

    # If a diff card is present, prepend it to the from_side block so the model
    # sees the deterministic diff summary first.
    diff_card_block = ""
    if bundle.diff_card is not None:
        dc = bundle.diff_card
        diff_summary = {
            "added": dc.added,
            "removed": dc.removed,
            "changed": dc.changed,
        }
        dc_ref = dc.evidence_refs[0].artifact_id if dc.evidence_refs else "version_diff_card"
        diff_card_block = (
            f"[{dc_ref}]\n"
            f"type=version_diff_card entity={dc.entity_id} "
            f"from={dc.from_version} to={dc.to_version}\n"
            f"{json.dumps(diff_summary, ensure_ascii=False, separators=(',', ':'))}\n\n"
        )

    from_block = diff_card_block + "\n\n".join(_render_artifact(a) for a in from_artifacts)
    to_block = "\n\n".join(_render_artifact(a) for a in to_artifacts)

    return _COMPARE_PROMPT_TEMPLATE.format(
        system_instructions=_COMPARE_SYSTEM_INSTRUCTIONS,
        from_version=bundle.from_version,
        to_version=bundle.to_version,
        from_artifacts_block=from_block,
        to_artifacts_block=to_block,
        question=question,
    )
