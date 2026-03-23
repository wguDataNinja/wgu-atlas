from __future__ import annotations

"""
Structured output handling for Atlas QA LLM operations.

Provides JSON extraction, schema validation, and fallback patterns
for structured LLM responses. Mirrors the safe_parse_stage1_response
pattern from wgu-reddit but generalized for Atlas QA needs.
"""

import json
import re
from typing import Any, Dict, Tuple

from pydantic import BaseModel, ValidationError


def _strip_code_fences(text: str) -> str:
    """Remove markdown code fences from text."""
    s = text.strip()
    if s.startswith("```"):
        lines = s.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    return s


def _extract_json_block(text: str) -> str:
    """
    Best-effort extraction of the main JSON object from the model output.

    Strips code fences and trims to the outermost {...} block. If no
    braces are found, returns the original text.
    """
    s = _strip_code_fences(text)

    start = s.find("{")
    end = s.rfind("}")
    if start != -1 and end != -1 and end > start:
        return s[start : end + 1]
    return s


def safe_parse_structured_response(
    raw_text: str,
    schema_class: type[BaseModel],
) -> Tuple[BaseModel | None, bool, bool, bool, str]:
    """
    Safe parsing for structured LLM responses.

    Parameters
    ----------
    raw_text : str
        Raw text from LLM response.
    schema_class : type[BaseModel]
        Pydantic model class to validate against.

    Returns
    -------
    (parsed_object, parse_error, schema_error, used_fallback, error_message)
    """
    parse_error = False
    schema_error = False
    used_fallback = False
    error_message = ""

    json_text = _extract_json_block(raw_text)

    # Strict JSON parse path
    try:
        data = json.loads(json_text)
        parsed = schema_class(**data)
        return parsed, parse_error, schema_error, used_fallback, error_message

    except json.JSONDecodeError as e:
        parse_error = True
        schema_error = True
        error_message = f"JSON decode error: {e}"
    except ValidationError as e:
        schema_error = True
        error_message = f"Schema validation error: {e}"
    except Exception as e:
        schema_error = True
        error_message = f"Unexpected error: {e}"

    # Fallback: return None with error flags
    used_fallback = True
    return None, parse_error, schema_error, used_fallback, error_message


def validate_and_fallback(
    raw_text: str,
    schema_class: type[BaseModel],
    default_values: Dict[str, Any] | None = None,
) -> BaseModel:
    """
    Validate structured response with fallback to default values.

    Parameters
    ----------
    raw_text : str
        Raw text from LLM response.
    schema_class : type[BaseModel]
        Pydantic model class to validate against.
    default_values : dict, optional
        Default values to use if validation fails.

    Returns
    -------
    BaseModel
        Validated object or object with default values.
    """
    parsed, parse_error, schema_error, used_fallback, error_message = safe_parse_structured_response(
        raw_text, schema_class
    )

    if parsed is not None:
        return parsed

    # Create object with default values
    if default_values is None:
        default_values = {}
    
    try:
        return schema_class(**default_values)
    except ValidationError as e:
        # If even defaults fail, create with empty dict
        return schema_class(**{})