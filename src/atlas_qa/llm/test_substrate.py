"""
Test script for Atlas QA LLM substrate.

Tests the minimum viable structured-output functionality:
- successful structured parse path
- schema validation path
- fallback path
- parse/schema failure flag capture
- run artifact capture
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel

from src.atlas_qa.llm.client import generate
from src.atlas_qa.llm.structured import safe_parse_structured_response, validate_and_fallback
from src.atlas_qa.llm.artifacts import capture_call
from src.atlas_qa.utils.logging import get_logger

logger = get_logger("atlas_qa.test_substrate")


class TestResponse(BaseModel):
    """Test schema for structured responses."""
    question: str
    answer: str
    confidence: float


def test_successful_structured_parse():
    """Test successful structured parsing."""
    logger.info("=== Testing successful structured parse ===")
    
    # Test with a simple prompt that should return valid JSON
    prompt = """Answer the following question with a JSON object:
{
  "question": "What is 2 + 2?",
  "answer": "4",
  "confidence": 0.95
}"""
    
    try:
        result = generate("llama3", prompt)
        logger.info(f"Raw output: {result.raw_text}")
        
        # Test structured parsing
        parsed, parse_error, schema_error, used_fallback, error_message = safe_parse_structured_response(
            result.raw_text, TestResponse
        )
        
        logger.info(f"Parsed: {parsed}")
        logger.info(f"Parse error: {parse_error}")
        logger.info(f"Schema error: {schema_error}")
        logger.info(f"Used fallback: {used_fallback}")
        logger.info(f"Error message: {error_message}")
        
        # Capture artifact
        capture_call("llama3", prompt, result)
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False


def test_parse_failure():
    """Test parse failure handling."""
    logger.info("=== Testing parse failure ===")
    
    # Test with invalid JSON
    invalid_json = "This is not JSON at all"
    
    parsed, parse_error, schema_error, used_fallback, error_message = safe_parse_structured_response(
        invalid_json, TestResponse
    )
    
    logger.info(f"Parsed: {parsed}")
    logger.info(f"Parse error: {parse_error}")
    logger.info(f"Schema error: {schema_error}")
    logger.info(f"Used fallback: {used_fallback}")
    logger.info(f"Error message: {error_message}")
    
    # Should have parse error and fallback
    assert parse_error == True
    assert used_fallback == True
    assert parsed is None
    
    return True


def test_schema_failure():
    """Test schema validation failure."""
    logger.info("=== Testing schema failure ===")
    
    # Test with valid JSON but invalid schema
    invalid_schema = '{"question": "test", "answer": "test", "confidence": "not_a_float"}'
    
    parsed, parse_error, schema_error, used_fallback, error_message = safe_parse_structured_response(
        invalid_schema, TestResponse
    )
    
    logger.info(f"Parsed: {parsed}")
    logger.info(f"Parse error: {parse_error}")
    logger.info(f"Schema error: {schema_error}")
    logger.info(f"Used fallback: {used_fallback}")
    logger.info(f"Error message: {error_message}")
    
    # Should have schema error and fallback
    assert schema_error == True
    assert used_fallback == True
    assert parsed is None
    
    return True


def test_fallback_with_defaults():
    """Test fallback with default values."""
    logger.info("=== Testing fallback with defaults ===")
    
    # Test with invalid JSON but provide defaults
    invalid_json = "This is not JSON"
    defaults = {"question": "default", "answer": "default", "confidence": 0.5}
    
    result = validate_and_fallback(invalid_json, TestResponse, defaults)
    
    logger.info(f"Result: {result}")
    
    # Should have default values
    assert result.question == "default"
    assert result.answer == "default"
    assert result.confidence == 0.5
    
    return True


def main():
    """Run all tests."""
    logger.info("Starting Atlas QA LLM substrate tests")
    
    tests = [
        test_parse_failure,
        test_schema_failure,
        test_fallback_with_defaults,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result))
        except Exception as e:
            logger.error(f"Test {test.__name__} failed with exception: {e}")
            results.append((test.__name__, False))
    
    # Test successful parse only if llama3 is available
    try:
        result = test_successful_structured_parse()
        results.append(("test_successful_structured_parse", result))
    except Exception as e:
        logger.warning(f"Skipping successful parse test due to: {e}")
        results.append(("test_successful_structured_parse", None))
    
    # Summary
    logger.info("=== Test Results ===")
    for test_name, result in results:
        if result is None:
            status = "SKIPPED"
        elif result:
            status = "PASSED"
        else:
            status = "FAILED"
        logger.info(f"{test_name}: {status}")
    
    # Count results
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)
    
    logger.info(f"Summary: {passed} passed, {failed} failed, {skipped} skipped")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)