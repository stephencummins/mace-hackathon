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
            ContentFinding(
                check="Author / originator",
                status="fail",
                detail="No author.",
                suggested_fix="Add an 'Author' field to the title block.",
            ),
        ],
    )


_FAKE_USAGE = {
    "input_tokens": 1200,
    "output_tokens": 350,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 4800,
}


def _make_response(parsed) -> MagicMock:
    resp = MagicMock()
    resp.parsed_output = parsed
    resp.usage.model_dump.return_value = dict(_FAKE_USAGE)
    return resp


def _mock_client(*, side_effect=None) -> MagicMock:
    client = MagicMock()
    if side_effect is not None:
        # Wrap any non-exception entries so .usage.model_dump() works
        client.messages.parse.side_effect = [
            entry if isinstance(entry, BaseException) else _make_response(entry.parsed_output)
            for entry in side_effect
        ]
    else:
        client.messages.parse.return_value = _make_response(_fake_content_result())
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


def test_validate_documents_with_mocked_client(tmp_path):
    client = _mock_client()
    reports = validate_documents(
        [PASSING_FIXTURE, FAILING_FIXTURE],
        progress=False,
        client=client,
        cache_dir=tmp_path,
    )
    assert client.messages.parse.call_count == 2
    for report in reports:
        assert report.content is not None
        assert report.content.overall_status == "warning"
        assert report.content_error is None


def test_validate_documents_isolates_api_errors(tmp_path):
    api_error = anthropic.APIError("simulated", request=MagicMock(), body=None)
    client = _mock_client(side_effect=[api_error, MagicMock(parsed_output=_fake_content_result())])
    reports = validate_documents(
        [PASSING_FIXTURE, FAILING_FIXTURE],
        progress=False,
        client=client,
        cache_dir=tmp_path,
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
    # suggested_fix flows through serialization
    assert blob["content"]["findings"][0]["suggested_fix"] == "Add an 'Author' field to the title block."
    # cache fields default to inactive
    assert blob["from_cache"] is False
    assert blob["cached_usage"] is None
    import json
    assert json.dumps(blob)  # serializable


# --- Cache behaviour --------------------------------------------------------


def test_cache_miss_then_hit(tmp_path):
    from src import cache
    from src.validators.content_validator import _RUBRIC_TEXT, resolve_model

    client = _mock_client()
    # First call: cache miss → API called once, cache written
    reports1 = validate_documents([PASSING_FIXTURE], progress=False, client=client, cache_dir=tmp_path)
    assert client.messages.parse.call_count == 1
    assert reports1[0].from_cache is False
    assert reports1[0].content is not None

    key = cache.cache_key(PASSING_FIXTURE.read_bytes(), _RUBRIC_TEXT, resolve_model())
    assert (tmp_path / f"{key}.json").exists()

    # Second call with the SAME client: cache hit → API NOT called again
    reports2 = validate_documents([PASSING_FIXTURE], progress=False, client=client, cache_dir=tmp_path)
    assert client.messages.parse.call_count == 1  # unchanged
    assert reports2[0].from_cache is True
    assert reports2[0].content is not None
    assert reports2[0].content.overall_status == reports1[0].content.overall_status
    assert reports2[0].cached_usage is not None
    assert reports2[0].cached_usage["input_tokens"] == _FAKE_USAGE["input_tokens"]


def test_use_cache_false_bypasses_both_read_and_write(tmp_path):
    client = _mock_client()
    # Pre-seed the cache with a known result
    validate_documents([PASSING_FIXTURE], progress=False, client=client, cache_dir=tmp_path)
    cache_files_before = list(tmp_path.glob("*.json"))
    assert len(cache_files_before) == 1
    mtime_before = cache_files_before[0].stat().st_mtime

    # Now run with use_cache=False — should hit the API again and NOT touch the cache file
    import time as _time
    _time.sleep(0.01)
    reports = validate_documents(
        [PASSING_FIXTURE],
        progress=False,
        client=client,
        cache_dir=tmp_path,
        use_cache=False,
    )
    assert client.messages.parse.call_count == 2
    assert reports[0].from_cache is False
    assert cache_files_before[0].stat().st_mtime == mtime_before
