from __future__ import annotations

"""
Atlas QA LLM Client.

Responsibility:
    - Hide provider-specific details (OpenAI vs Ollama).
    - Use the model registry for provider and pricing metadata.
    - Call the underlying LLM (Chat Completions for OpenAI, HTTP for Ollama).
    - Return a structured LlmCallResult object for downstream use.

This is the single entry point Atlas QA code should use:
    generate(model_name: str, prompt: str) -> LlmCallResult

Features:
    - Per-call timeout.
    - Simple retry with exponential backoff.
    - llm_failure / num_retries / error_message flags on LlmCallResult.

Decoding:
    - Atlas QA operations are expected to use deterministic decoding
      (e.g., temperature=0, top_p=1, single candidate) at the provider layer.
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import Any, Tuple

import requests

from atlas_qa.llm.registry import get_model_info
from atlas_qa.llm.types import LlmCallResult
from atlas_qa.utils.logging import get_logger

logger = get_logger("atlas_qa.llm.client")

DEFAULT_TIMEOUT_SEC = 90.0
MAX_RETRIES = 2


def _call_openai(model_name: str, prompt: str, api_key: str) -> str:
    """
    Call OpenAI via Chat Completions for models configured in MODEL_REGISTRY.

    This intentionally uses the simplest possible pattern, mirroring the
    previous working project:

      - chat.completions.create
      - messages=[{"role":"user","content":prompt}]
      - no temperature / token / reasoning params

    This avoids the Responses API and any reasoning-token quirks for GPT-5 models.
    """
    from openai import OpenAI

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing; cannot call OpenAI models.")

    client = OpenAI(api_key=api_key)

    resp = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        # Deliberately no temperature / max_* / reasoning options.
    )

    if not resp.choices:
        return ""

    msg = resp.choices[0].message
    content = getattr(msg, "content", None)

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts: list[str] = []
        for c in content:
            if isinstance(c, str) and c.strip():
                parts.append(c.strip())
            elif isinstance(c, dict):
                t = c.get("text") or c.get("content")
                if isinstance(t, str) and t.strip():
                    parts.append(t.strip())
        if parts:
            return "\n".join(parts).strip()

    return ""


_OLLAMA_TIMEOUT_SEC = 300
# qwen3 family uses extended thinking by default; disable it for deterministic eval.
_QWEN3_THINK_DISABLE = frozenset(["qwen3", "qwen3.5"])


def _call_ollama(model_name: str, prompt: str) -> str:
    """
    Call a local Ollama instance for the given model.
    """
    payload: dict = {"model": model_name, "prompt": prompt, "stream": False}
    family = model_name.split(":")[0].lower()
    if family in _QWEN3_THINK_DISABLE:
        payload["think"] = False

    r = requests.post(
        "http://localhost:11434/api/generate",
        json=payload,
        timeout=_OLLAMA_TIMEOUT_SEC,
    )
    r.raise_for_status()
    data = r.json()
    return (data.get("response") or "").strip()


def _call_model_once(
    model_name: str,
    prompt: str,
    provider: str,
    api_key: str,
) -> str:
    """
    Single underlying model call.

    Provider-specific helpers are responsible for configuring decoding
    (e.g., deterministic settings for benchmarking).
    """
    if provider == "openai":
        return _call_openai(model_name, prompt, api_key)
    if provider == "ollama":
        return _call_ollama(model_name, prompt)
    raise RuntimeError(f"Unsupported provider for model '{model_name}': {provider}")


def _call_model_with_retry(
    model_name: str,
    prompt: str,
    provider: str,
    api_key: str,
    timeout_sec: float = DEFAULT_TIMEOUT_SEC,
    max_retries: int = MAX_RETRIES,
) -> Tuple[str | None, bool, int, str | None]:
    """
    Run the underlying model call with a per-attempt timeout and simple retries.

    Returns:
        raw_text (str | None)
        llm_failure (bool)
        num_retries (int)  # how many retries were actually attempted
        error_message (str | None)
    """
    last_error: str | None = None

    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                backoff = 2**attempt
                logger.warning(
                    "Retrying model call model=%s provider=%s attempt=%d backoff=%ds",
                    model_name,
                    provider,
                    attempt,
                    backoff,
                )
                time.sleep(backoff)

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    _call_model_once,
                    model_name,
                    prompt,
                    provider,
                    api_key,
                )
                raw_text: str = future.result(timeout=timeout_sec)

            if attempt > 0:
                logger.info(
                    "Model call succeeded after %d retries model=%s provider=%s",
                    attempt,
                    model_name,
                    provider,
                )
            return raw_text, False, attempt, None

        except FuturesTimeoutError:
            last_error = f"Timeout after {timeout_sec}s"
            logger.error(
                "Model call timeout model=%s provider=%s attempt=%d timeout_sec=%.1f",
                model_name,
                provider,
                attempt,
                timeout_sec,
            )
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"
            logger.error(
                "Model call failed model=%s provider=%s attempt=%d error=%s",
                model_name,
                provider,
                attempt,
                e,
            )

    logger.error(
        "Model call giving up after %d retries model=%s provider=%s last_error=%s",
        max_retries,
        model_name,
        provider,
        last_error,
    )
    return None, True, max_retries, last_error


def generate(model_name: str, prompt: str) -> LlmCallResult:
    """
    Provider-agnostic LLM invocation.

    Parameters
    ----------
    model_name : str
        Registry key for the model.
    prompt : str
        Fully rendered prompt text.

    Returns
    -------
    LlmCallResult
        Structured result including raw text, cost, latency, and failure flags.
    """
    api_key = os.getenv("OPENAI_API_KEY", "")
    info = get_model_info(model_name)
    if info is None:
        raise RuntimeError(f"Model '{model_name}' not found in MODEL_REGISTRY.")

    started_at = time.time()

    raw_text, llm_failure, num_retries, error_message = _call_model_with_retry(
        model_name=model_name,
        prompt=prompt,
        provider=info.provider,
        api_key=api_key,
        timeout_sec=DEFAULT_TIMEOUT_SEC,
        max_retries=MAX_RETRIES,
    )

    if raw_text is None:
        raw_text = ""

    finished_at = time.time()
    elapsed_sec = finished_at - started_at

    logger.info(
        "LLM call finished model=%s provider=%s elapsed=%.3f llm_failure=%s retries=%d",
        model_name,
        info.provider,
        elapsed_sec,
        llm_failure,
        num_retries,
    )

    return LlmCallResult(
        model_name=model_name,
        provider=info.provider,
        raw_text=raw_text,
        input_tokens=0,
        output_tokens=0,
        total_cost_usd=0.0,
        elapsed_sec=elapsed_sec,
        llm_failure=llm_failure,
        num_retries=num_retries,
        error_message=error_message,
        timeout_sec=DEFAULT_TIMEOUT_SEC,
        started_at=started_at,
        finished_at=finished_at,
    )