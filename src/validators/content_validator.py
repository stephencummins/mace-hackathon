"""Silver-level ISO 19650 content validator using Claude.

Sends the document to Claude with a cached rubric and returns structured findings.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Literal, Optional

import anthropic
from pydantic import BaseModel, Field

DEFAULT_MODEL = "claude-sonnet-4-6"

_RUBRIC_PATH = Path(__file__).parent / "iso_19650_rubric.md"
_RUBRIC_TEXT = _RUBRIC_PATH.read_text(encoding="utf-8")


class ContentFinding(BaseModel):
    check: str = Field(description="The criterion being assessed (use the rubric heading text)")
    status: Literal["pass", "fail", "warning"]
    detail: str = Field(description="One- to two-sentence justification citing document evidence")
    suggested_fix: Optional[str] = Field(
        default=None,
        description=(
            "Concrete remediation when status is 'fail' or 'warning'. "
            "Omit (null) for 'pass' findings."
        ),
    )


class ContentValidationResult(BaseModel):
    overall_status: Literal["pass", "fail", "warning"]
    summary: str = Field(description="Single sentence summary suitable for a CLI table row (<= 25 words)")
    findings: list[ContentFinding]


def resolve_model(explicit: Optional[str] = None) -> str:
    """Resolve the model id from (in order) explicit arg, CLAUDE_MODEL env, default."""
    return explicit or os.getenv("CLAUDE_MODEL") or DEFAULT_MODEL


def call_claude(
    path: str | Path,
    client: anthropic.Anthropic,
    model: str,
) -> tuple[ContentValidationResult, dict]:
    """Make the Anthropic call and return (parsed_result, usage_dict).

    Public so the runner can call it directly when it wants the usage block
    for cache accounting; ``validate_content`` is the simpler facade.
    """
    pdf_bytes = Path(path).read_bytes()
    pdf_b64 = base64.standard_b64encode(pdf_bytes).decode("ascii")

    response = client.messages.parse(
        model=model,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": _RUBRIC_TEXT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "Assess this document against the rubric and return a "
                            "structured ContentValidationResult."
                        ),
                    },
                ],
            }
        ],
        output_format=ContentValidationResult,
    )

    usage = response.usage.model_dump() if hasattr(response.usage, "model_dump") else dict(response.usage)
    return response.parsed_output, usage


def validate_content(
    path: str | Path,
    *,
    client: Optional[anthropic.Anthropic] = None,
    model: Optional[str] = None,
) -> Optional[ContentValidationResult]:
    """Validate document content against the ISO 19650 rubric using Claude.

    Returns:
        ContentValidationResult on success.
        None when no API key is set and no client is supplied — callers
        should render this as a 'skipped' row in their report.

    Raises:
        anthropic.APIError (and subclasses) on API failure. Callers wrap in
        try/except to render API errors as a row in their report.
    """
    if client is None:
        if not os.getenv("ANTHROPIC_API_KEY"):
            return None
        client = anthropic.Anthropic()

    result, _usage = call_claude(path, client, resolve_model(model))
    return result
