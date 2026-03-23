"""Schema-bound fuzzy-query classifier for Session 04.

Uses the LLM substrate (Ollama/llama3 by default) to extract advisory
retrieval signals from NL queries that do not resolve on the exact path.

The classifier is ADVISORY ONLY:
- Its output is schema-validated before use.
- Parse or schema failure falls back cleanly without broadening scope.
- The classifier never decides entity/version/source/section scope.
- It is not invoked on the exact path (Class A queries bypass it entirely).

Session 04 implementation.
"""
from __future__ import annotations

import logging

from atlas_qa.qa.classifier_prompts import build_classifier_prompt
from atlas_qa.qa.types import ClassifierHint

logger = logging.getLogger(__name__)

DEFAULT_CLASSIFIER_MODEL = "llama3"


def classify_fuzzy_query(
    query: str,
    model_name: str = DEFAULT_CLASSIFIER_MODEL,
) -> tuple[ClassifierHint | None, bool, bool, bool, str]:
    """Classify a fuzzy NL query using the schema-bound LLM classifier.

    Returns
    -------
    (hint, parse_error, schema_error, used_fallback, error_message)

    hint is None when classifier output cannot be safely parsed/validated.
    All error flags are explicit and testable.

    The caller must treat hint as advisory only and must never let it
    override upstream deterministic scope.
    """
    from src.atlas_qa.llm.client import generate
    from src.atlas_qa.llm.structured import safe_parse_structured_response

    prompt = build_classifier_prompt(query)

    try:
        result = generate(model_name, prompt)
    except Exception as exc:
        error_msg = f"LLM call failed: {exc}"
        logger.warning("Classifier LLM call failed: query=%r error=%s", query, exc)
        return None, False, False, True, error_msg

    if result.llm_failure or not result.raw_text:
        error_msg = result.error_message or "LLM returned empty response"
        logger.warning(
            "Classifier LLM failure: query=%r llm_failure=%s error=%s",
            query,
            result.llm_failure,
            error_msg,
        )
        return None, False, False, True, error_msg

    parsed, parse_error, schema_error, used_fallback, error_msg = (
        safe_parse_structured_response(result.raw_text, ClassifierHint)
    )

    if parsed is None:
        logger.warning(
            "Classifier parse/schema failure: query=%r parse_error=%s schema_error=%s error=%s",
            query,
            parse_error,
            schema_error,
            error_msg,
        )
        return None, parse_error, schema_error, used_fallback, error_msg

    logger.debug(
        "Classifier succeeded: query=%r hint=%s",
        query,
        parsed.model_dump(exclude_none=True),
    )
    return parsed, parse_error, schema_error, used_fallback, error_msg
