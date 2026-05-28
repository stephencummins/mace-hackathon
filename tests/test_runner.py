"""Tests for the batch validation runner."""

from pathlib import Path
from unittest.mock import MagicMock
import sys

import anthropic
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.runner import DocReport, iter_pdfs, validate_documents
from src.validators.content_validator import (
    ContentFinding,
    ContentValidationResult,
)

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
PASSING_FIXTURE = EXAMPLES / "MAC-LIBDM-XX-00-DR-A-001_P01.pdf"
FAILING_FIXTURE = EXAMPLES / "floor plan ground.pdf"


def _fake_content_result() -> ContentValidationResult:
    return ContentValidationResult(
        overall_status="warning",
        summary="Placeholder document.",
        findings=[
            ContentFinding(check="Author / originator", status="fail", detail="No author."),
        ],
    )


def _mock_client(*, side_effect=None) -> MagicMock:
    client = MagicMock()
    if side_effect is not None:
        client.messages.parse.side_effect = side_effect
    else:
        fake_response = MagicMock()
        fake_response.parsed_output = _fake_content_result()
        client.messages.parse.return_value = fake_response
    return client


def test_iter_pdfs_directory():
    paths = list(iter_pdfs(EXAMPLES))
    names = sorted(p.name for p in paths)
    assert names == ["MAC-LIBDM-XX-00-DR-A-001_P01.pdf", "floor plan ground.pdf"]


def test_iter_pdfs_single_file():
    paths = list(iter_pdfs(PASSING_FIXTURE))
    assert paths == [PASSING_FIXTURE]


def test_iter_pdfs_yields_file_even_for_non_pdf_extension(tmp_path):
    f = tmp_path / "weird.docx"
    f.write_bytes(b"placeholder")
    paths = list(iter_pdfs(f))
    assert paths == [f]


def test_validate_documents_no_api_key_skips_content(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    reports = validate_documents([PASSING_FIXTURE, FAILING_FIXTURE], progress=False)
    assert len(reports) == 2
    assert reports[0].naming.passed is True
    assert reports[1].naming.passed is False
    for report in reports:
        assert report.content is None
        assert report.content_error is None


def test_validate_documents_with_mocked_client():
    client = _mock_client()
    reports = validate_documents(
        [PASSING_FIXTURE, FAILING_FIXTURE], progress=False, client=client
    )
    assert client.messages.parse.call_count == 2
    for report in reports:
        assert report.content is not None
        assert report.content.overall_status == "warning"
        assert report.content_error is None


def test_validate_documents_isolates_api_errors():
    api_error = anthropic.APIError("simulated", request=MagicMock(), body=None)
    client = _mock_client(side_effect=[api_error, MagicMock(parsed_output=_fake_content_result())])
    reports = validate_documents(
        [PASSING_FIXTURE, FAILING_FIXTURE], progress=False, client=client
    )
    assert len(reports) == 2
    assert reports[0].content_error is not None
    assert "APIError" in reports[0].content_error
    assert reports[0].content is None
    assert reports[1].content is not None
    assert reports[1].content_error is None


def test_doc_report_to_json_dict_roundtrip():
    report = DocReport(
        path=PASSING_FIXTURE,
        naming=__import__("src.validators.naming_validator", fromlist=["validate_naming"]).validate_naming(PASSING_FIXTURE),
        content=_fake_content_result(),
    )
    blob = report.to_json_dict()
    assert blob["path"].endswith("MAC-LIBDM-XX-00-DR-A-001_P01.pdf")
    assert blob["naming"]["passed"] is True
    assert blob["content"]["overall_status"] == "warning"
    assert blob["content_error"] is None
    import json
    assert json.dumps(blob)  # serializable
