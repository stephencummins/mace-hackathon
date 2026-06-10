"""Tests for the audit trail module and the audit_report CLI."""

from pathlib import Path
import json
import sys

import pytest
from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import audit
from src.audit_report import main as audit_report_main
from src.runner import DocReport
from src.validators.content_validator import ContentFinding, ContentValidationResult
from src.validators.naming_validator import validate_naming


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
PASSING_FIXTURE = EXAMPLES / "MAC-LIBDM-XX-00-DR-A-001_P01.pdf"
FAILING_FIXTURE = EXAMPLES / "floor plan ground.pdf"


def _make_report(path: Path, *, model="claude-sonnet-4-6", from_cache=False) -> DocReport:
    content = ContentValidationResult(
        overall_status="fail",
        summary="Stub fail.",
        findings=[
            ContentFinding(check="Author / originator", status="fail", detail="Missing."),
            ContentFinding(check="Revision history", status="warning", detail="Sparse."),
        ],
    )
    return DocReport(
        path=path,
        naming=validate_naming(path),
        content=content,
        from_cache=from_cache,
        usage={"input_tokens": 1000, "output_tokens": 500, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0},
        model=model,
    )


# -- hash_pdf / principal_for_token -----------------------------------------


def test_hash_pdf_is_deterministic():
    a = audit.hash_pdf(b"some pdf bytes")
    b = audit.hash_pdf(b"some pdf bytes")
    assert a == b
    assert len(a) == 64


def test_hash_pdf_changes_with_content():
    assert audit.hash_pdf(b"abc") != audit.hash_pdf(b"abd")


def test_principal_for_token_format():
    p = audit.principal_for_token("my-secret-token")
    assert p.startswith("tok_")
    assert len(p) == len("tok_") + 8


def test_principal_for_token_does_not_leak_token():
    raw = "very-secret-bearer"
    p = audit.principal_for_token(raw)
    assert raw not in p
    # Second hash of the same token returns the same principal
    assert p == audit.principal_for_token(raw)
    # Different token → different principal
    assert p != audit.principal_for_token("other-token")


# -- log_validation / iter_entries / summary ---------------------------------


def test_log_validation_appends_and_roundtrips(tmp_path):
    report = _make_report(PASSING_FIXTURE)
    entry = audit.log_validation(report, source="cli", principal="alice", audit_dir=tmp_path)
    assert entry.source == "cli"
    assert entry.principal == "alice"
    assert entry.doc_name == PASSING_FIXTURE.name
    assert entry.doc_hash == audit.hash_pdf(PASSING_FIXTURE.read_bytes())
    assert entry.content_status == "fail"
    assert entry.finding_counts == {"fail": 1, "warning": 1}
    assert entry.cost_usd > 0

    entries = list(audit.iter_entries(tmp_path))
    assert len(entries) == 1
    assert entries[0]["principal"] == "alice"
    assert entries[0]["doc_hash"] == entry.doc_hash


def test_log_validation_appends_multiple(tmp_path):
    audit.log_validation(_make_report(PASSING_FIXTURE), source="cli", principal="a", audit_dir=tmp_path)
    audit.log_validation(_make_report(FAILING_FIXTURE), source="api", principal="tok_aaaa", audit_dir=tmp_path)
    audit.log_validation(_make_report(PASSING_FIXTURE, from_cache=True), source="cli", principal="b", audit_dir=tmp_path)

    entries = list(audit.iter_entries(tmp_path))
    assert [e["source"] for e in entries] == ["cli", "api", "cli"]
    assert [e["from_cache"] for e in entries] == [False, False, True]


def test_iter_entries_tolerates_corrupt_lines(tmp_path):
    log = tmp_path / "validations.jsonl"
    log.write_text(
        '{"ts": "2026-01-01T00:00:00", "source": "cli"}\n'
        "this is not json\n"
        '{"ts": "2026-01-02T00:00:00", "source": "api"}\n',
        encoding="utf-8",
    )
    entries = list(audit.iter_entries(tmp_path))
    assert [e["source"] for e in entries] == ["cli", "api"]


def test_iter_entries_missing_directory(tmp_path):
    assert list(audit.iter_entries(tmp_path / "does-not-exist")) == []


def test_summary_aggregates(tmp_path):
    audit.log_validation(_make_report(PASSING_FIXTURE), source="cli", principal="a", audit_dir=tmp_path)
    audit.log_validation(_make_report(FAILING_FIXTURE), source="api", principal="tok_aaaa", audit_dir=tmp_path)
    audit.log_validation(_make_report(PASSING_FIXTURE, from_cache=True), source="cli", principal="a", audit_dir=tmp_path)

    s = audit.summary(audit.iter_entries(tmp_path))
    assert s["total"] == 3
    assert s["by_source"] == {"cli": 2, "api": 1}
    assert s["cache_hits"] == 1
    assert s["by_principal"]["a"] == 2
    assert s["by_principal"]["tok_aaaa"] == 1
    assert s["total_cost_usd"] > 0


# -- audit_report CLI -------------------------------------------------------


def test_audit_report_empty(tmp_path):
    result = CliRunner().invoke(audit_report_main, ["--audit-dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "No audit entries" in result.output


def test_audit_report_populated(tmp_path):
    audit.log_validation(_make_report(PASSING_FIXTURE), source="cli", principal="alice", audit_dir=tmp_path)
    audit.log_validation(_make_report(FAILING_FIXTURE), source="api", principal="tok_aaaa", audit_dir=tmp_path)
    result = CliRunner().invoke(audit_report_main, ["--audit-dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "Audit trail" in result.output
    assert "alice" in result.output
    assert "tok_aaaa" in result.output
    assert "Total validations" in result.output


def test_audit_report_filters_by_source(tmp_path):
    audit.log_validation(_make_report(PASSING_FIXTURE), source="cli", principal="alice", audit_dir=tmp_path)
    audit.log_validation(_make_report(FAILING_FIXTURE), source="api", principal="tok_aaaa", audit_dir=tmp_path)
    result = CliRunner().invoke(audit_report_main, ["--audit-dir", str(tmp_path), "--source", "api"])
    assert result.exit_code == 0
    assert "tok_aaaa" in result.output
    assert "alice" not in result.output


def test_audit_report_filters_by_principal(tmp_path):
    audit.log_validation(_make_report(PASSING_FIXTURE), source="cli", principal="alice", audit_dir=tmp_path)
    audit.log_validation(_make_report(FAILING_FIXTURE), source="cli", principal="bob", audit_dir=tmp_path)
    result = CliRunner().invoke(audit_report_main, ["--audit-dir", str(tmp_path), "--principal", "alice"])
    assert result.exit_code == 0
    assert "alice" in result.output
    assert "bob" not in result.output
