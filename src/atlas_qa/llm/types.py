from __future__ import annotations
"""
Typed data structures for Atlas QA LLM substrate.

Defines the structured call result type and other core types needed for
LLM operations. These types provide a stable interface for all Atlas QA code.
"""

from typing import Literal
from pydantic import BaseModel


class LlmCallResult(BaseModel):
    """
    Metadata for a single LLM call.

    Captures low-level details needed for cost, latency, and failure
    analysis. Everything inside here should be provider-agnostic.
    """
    model_name: str
    provider: str
    raw_text: str
    input_tokens: int
    output_tokens: int
    total_cost_usd: float
    elapsed_sec: float

    # Failure / retry metadata
    llm_failure: bool = False
    num_retries: int = 0
    error_message: str | None = None
    timeout_sec: float | None = None

    # Timing metadata
    started_at: float | None = None
    finished_at: float | None = None