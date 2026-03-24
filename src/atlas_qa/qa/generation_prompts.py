"""Strict prompt contract for Atlas QA Session 05 constrained generation.

The template is a plain string. All logic lives in generation.py — not here.

Contract rules (enforced at call site in generation.py):
- Supply only pre-assembled evidence artifacts — no raw corpus, no unvetted text.
- Instruct the model to cite the source_object_identity of each artifact it uses.
- Instruct the model to state the version used in the answer.
- Instruct the model to abstain (output ABSTAIN) rather than guess.
- Do not ask the model to search, infer beyond the artifacts, or resolve conflicts.
- Target: fits in ~2K tokens of context for an 8B model.

The output schema expected from the model:
{
  "answer_text": "<answer string or null>",
  "cited_evidence_ids": ["<source_object_identity>", ...],
  "version_disclosed": "<version string or null>",
  "abstain": false
}
If the model cannot answer, it should set abstain=true and leave answer_text null.
"""
from __future__ import annotations

import json

from atlas_qa.qa.types import EvidenceArtifact, EvidenceBundle

# ---------------------------------------------------------------------------
# Prompt template (logic-free string)
# ---------------------------------------------------------------------------

_SYSTEM_INSTRUCTIONS = """\
You are a precise academic catalog assistant. Answer the user's question using \
ONLY the evidence artifacts provided below. Do not use any outside knowledge.

Rules:
1. Cite every artifact you use by including its ID in "cited_evidence_ids".
2. Your answer_text MUST begin with the exact version string from the artifact (e.g., "As of version 2026-03, ..."). Populate "version_disclosed" with the same string.
3. If the evidence is insufficient, set "abstain": true and leave "answer_text" null.
4. Do not guess, infer beyond the artifacts, or resolve conflicting sources.
5. Respond with a single JSON object matching the schema below — nothing else.

Output schema:
{
  "answer_text": "As of version 2026-03, <your answer here>",
  "cited_evidence_ids": ["<artifact ID>", ...],
  "version_disclosed": "2026-03",
  "abstain": false
}
"""

_PROMPT_TEMPLATE = """\
{system_instructions}

--- EVIDENCE ARTIFACTS ---
{artifacts_block}
--- END EVIDENCE ---

USER QUESTION: {question}

IMPORTANT: answer_text must begin with "As of version {version_used}, ..."

Respond with JSON only."""


# ---------------------------------------------------------------------------
# Rendering function
# ---------------------------------------------------------------------------


def _render_artifact(artifact: EvidenceArtifact) -> str:
    """Render one artifact as a compact text block for the prompt."""
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


def render_generation_prompt(bundle: EvidenceBundle, question: str) -> str:
    """Render a fully populated generation prompt for the given bundle and question.

    The rendered prompt is self-contained and suitable for passing directly to
    the LLM via generate(). No logic should be embedded in the template string
    itself — all logic is here.
    """
    artifacts_block = "\n\n".join(
        _render_artifact(a) for a in bundle.artifacts
    )

    return _PROMPT_TEMPLATE.format(
        system_instructions=_SYSTEM_INSTRUCTIONS,
        artifacts_block=artifacts_block,
        question=question,
        version_used=bundle.version_used or "unknown",
    )
