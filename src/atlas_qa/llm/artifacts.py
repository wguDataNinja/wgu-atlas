from __future__ import annotations

"""
Run-level artifact capture for Atlas QA LLM operations.

Provides the pattern of writing {prompt, raw_output, flags} per call
for auditability and debugging. Mirrors the artifact write pattern
from wgu-reddit benchmark runners.
"""

import json
import os
import time
from pathlib import Path
from typing import Any, Dict

from src.atlas_qa.llm.types import LlmCallResult


class ArtifactCapture:
    """Handles artifact capture for LLM calls."""
    
    def __init__(self, base_dir: str | Path = "artifacts"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped run directory
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.run_dir = self.base_dir / f"run_{timestamp}"
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
        self.artifact_log = self.run_dir / "artifacts.jsonl"
        
    def capture_call(
        self,
        model_name: str,
        prompt: str,
        call_result: LlmCallResult,
        parse_failure: bool = False,
        schema_failure: bool = False,
    ) -> None:
        """
        Capture a single LLM call artifact.

        Parameters
        ----------
        model_name : str
            Name of the model used.
        prompt : str
            Input prompt text.
        call_result : LlmCallResult
            Result from the LLM call.
        parse_failure : bool
            Whether JSON parsing failed (from safe_parse_structured_response).
        schema_failure : bool
            Whether Pydantic schema validation failed (from safe_parse_structured_response).
        """
        artifact = {
            "timestamp": time.time(),
            "model_name": model_name,
            "prompt": prompt,
            "raw_output": call_result.raw_text,
            "flags": {
                "llm_failure": call_result.llm_failure,
                "parse_failure": parse_failure,
                "schema_failure": schema_failure,
                "num_retries": call_result.num_retries,
                "error_message": call_result.error_message,
            },
            "metadata": {
                "input_tokens": call_result.input_tokens,
                "output_tokens": call_result.output_tokens,
                "total_cost_usd": call_result.total_cost_usd,
                "elapsed_sec": call_result.elapsed_sec,
                "timeout_sec": call_result.timeout_sec,
                "started_at": call_result.started_at,
                "finished_at": call_result.finished_at,
            }
        }
        
        # Write to JSONL file
        with open(self.artifact_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(artifact, ensure_ascii=False) + "\n")
            
    def get_run_dir(self) -> Path:
        """Get the current run directory path."""
        return self.run_dir
        
    def get_artifact_log(self) -> Path:
        """Get the artifact log file path."""
        return self.artifact_log


# Global artifact capture instance
_artifact_capture: ArtifactCapture | None = None


def get_artifact_capture() -> ArtifactCapture:
    """Get the global artifact capture instance."""
    global _artifact_capture
    if _artifact_capture is None:
        artifacts_dir = os.getenv("ATLAS_QA_ARTIFACTS_DIR", "artifacts")
        _artifact_capture = ArtifactCapture(artifacts_dir)
    return _artifact_capture


def capture_call(
    model_name: str,
    prompt: str,
    call_result: LlmCallResult,
    parse_failure: bool = False,
    schema_failure: bool = False,
) -> None:
    """
    Convenience function to capture a single LLM call artifact.

    Parameters
    ----------
    model_name : str
        Name of the model used.
    prompt : str
        Input prompt text.
    call_result : LlmCallResult
        Result from the LLM call.
    parse_failure : bool
        Whether JSON parsing failed (from safe_parse_structured_response).
    schema_failure : bool
        Whether Pydantic schema validation failed (from safe_parse_structured_response).
    """
    capture = get_artifact_capture()
    capture.capture_call(model_name, prompt, call_result, parse_failure, schema_failure)