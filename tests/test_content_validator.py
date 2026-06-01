"""Tests for the Silver-level content validator. The Anthropic client is
mocked — no network calls and no API key required."""

from pathlib import Path
from unittest.mock import MagicMock
import sys

import anthropic
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.validators.content_validator import (
    ContentFinding,
    ContentValidationResult,
    validate_content,
)

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
PDF_FIXTURE = EXAMPLES / "MAC-LIBDM-XX-00-DR-A-001_P01.pdf"


def _fake_result(status: str = "warning") -> ContentValidationResult:
    return ContentValidationResult(
        overall_status=status,
        summary="A placeholder document with minimal content.",
        findings=[
            ContentFinding(
                check="Author / originator",
                status="fail",
                detail="No author block.",
                suggested_fix="Add an 'Author' field to the title block.",
            ),
            ContentFinding(
                check="Title block present",
                status="warning",
                detail="Inferred from filename only.",
            ),
        ],
    )


def _mock_client(parsed_output: ContentValidationResult) -> MagicMock:
    client = MagicMock()
    fake_response = MagicMock()
    fake_response.parsed_output = parsed_output
    client.messages.parse.return_value = fake_response
    return client


def test_returns_none_when_no_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = validate_content(PDF_FIXTURE)
    assert result is None


def test_uses_injected_client_even_without_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    fake = _fake_result()
    client = _mock_client(fake)
    result = validate_content(PDF_FIXTURE, client=client)
    assert result is fake
    client.messages.parse.assert_called_once()


def test_request_shape():
    client = _mock_client(_fake_result())
    validate_content(PDF_FIXTURE, client=client, model="claude-sonnet-4-6")

    kwargs = client.messages.parse.call_args.kwargs
    assert kwargs["model"] == "claude-sonnet-4-6"
    assert kwargs["thinking"] == {"type": "adaptive"}
    assert kwargs["output_format"] is ContentValidationResult

    system_blocks = kwargs["system"]
    assert isinstance(system_blocks, list) and len(system_blocks) == 1
    assert system_blocks[0]["cache_control"] == {"type": "ephemeral"}
    assert "ISO 19650" in system_blocks[0]["text"]

    user_content = kwargs["messages"][0]["content"]
    doc_blocks = [b for b in user_content if b["type"] == "document"]
    assert len(doc_blocks) == 1
    assert doc_blocks[0]["source"]["media_type"] == "application/pdf"
    assert doc_blocks[0]["source"]["type"] == "base64"
    assert isinstance(doc_blocks[0]["source"]["data"], str) and doc_blocks[0]["source"]["data"]


def test_model_env_var_overrides_default(monkeypatch):
    monkeypatch.setenv("CLAUDE_MODEL", "claude-haiku-4-5")
    client = _mock_client(_fake_result())
    validate_content(PDF_FIXTURE, client=client)
    assert client.messages.parse.call_args.kwargs["model"] == "claude-haiku-4-5"


def test_explicit_model_arg_overrides_env(monkeypatch):
    monkeypatch.setenv("CLAUDE_MODEL", "claude-haiku-4-5")
    client = _mock_client(_fake_result())
    validate_content(PDF_FIXTURE, client=client, model="claude-opus-4-7")
    assert client.messages.parse.call_args.kwargs["model"] == "claude-opus-4-7"


def test_propagates_api_error():
    client = MagicMock()
    client.messages.parse.side_effect = anthropic.APIError(
        "simulated upstream failure", request=MagicMock(), body=None
    )
    with pytest.raises(anthropic.APIError):
        validate_content(PDF_FIXTURE, client=client)


def test_suggested_fix_optional_and_round_trips():
    # default None for pass findings
    pass_finding = ContentFinding(check="Title block present", status="pass", detail="Present")
    assert pass_finding.suggested_fix is None

    # populated for fail/warning
    fix = "Add an 'Author' field to the title block."
    fail_finding = ContentFinding(
        check="Author / originator",
        status="fail",
        detail="No author block.",
        suggested_fix=fix,
    )
    assert fail_finding.suggested_fix == fix
    assert fail_finding.model_dump()["suggested_fix"] == fix


def test_thinking_omitted_for_models_that_dont_support_it():
    # Haiku 4.5 does not support adaptive thinking — the request must not include it.
    client = _mock_client(_fake_result())
    validate_content(PDF_FIXTURE, client=client, model="claude-haiku-4-5")
    kwargs = client.messages.parse.call_args.kwargs
    assert "thinking" not in kwargs, f"thinking should be omitted on Haiku, got {kwargs.get('thinking')}"


def test_rubric_instructs_claude_to_provide_fixes():
    # Regression: the rubric file must explain when/how to populate suggested_fix
    rubric = (Path(__file__).resolve().parents[1] / "src" / "validators" / "iso_19650_rubric.md").read_text(encoding="utf-8")
    assert "suggested_fix" in rubric
    assert "fail" in rubric.lower() and "warning" in rubric.lower()
