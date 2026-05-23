"""Tests for the ISO 19650 naming validator."""

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.validators.naming_validator import validate_naming

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
PASSING_FIXTURE = EXAMPLES / "MAC-LIBDM-XX-00-DR-A-001_P01.pdf"
FAILING_FIXTURE = EXAMPLES / "floor plan ground.pdf"


def test_passing_fixture():
    result = validate_naming(PASSING_FIXTURE)
    assert result.passed is True
    assert result.status == "pass"
    assert result.fields == {
        "project": "MAC",
        "originator": "LIBDM",
        "volume": "XX",
        "level": "00",
        "type": "DR",
        "role": "A",
        "number": "001",
        "revision": "P01",
    }


def test_failing_fixture():
    result = validate_naming(FAILING_FIXTURE)
    assert result.passed is False
    assert result.status == "fail"
    assert result.details, "expected at least one diagnostic detail"
    joined = " ".join(result.details)
    assert "whitespace" in joined.lower() or "revision" in joined.lower()


def test_extension_is_ignored():
    assert validate_naming("MAC-LIBDM-XX-00-DR-A-001_P01.docx").passed
    assert validate_naming("MAC-LIBDM-XX-00-DR-A-001_P01.xlsx").passed
    assert validate_naming("MAC-LIBDM-XX-00-DR-A-001_P01").passed


@pytest.mark.parametrize(
    "name,bad_field",
    [
        ("MAC-LIBDM-XX-00-DR-A-001_p01.pdf", "REVISION"),         # lowercase revision letter
        ("MAC-LIBDM-XX-00-DR-AB-001_P01.pdf", "ROLE"),            # role must be single letter
        ("MAC-LIBDM-XX-00-D-A-001_P01.pdf", "TYPE"),              # type must be 2 letters
        ("MAC-LIBDM-XX-00-DR-A-1_P01.pdf", "NUMBER"),             # number too short
    ],
)
def test_per_field_failures(name, bad_field):
    result = validate_naming(name)
    assert result.passed is False
    assert any(bad_field in d for d in result.details), (
        f"expected {bad_field} in details, got {result.details}"
    )


def test_missing_revision():
    result = validate_naming("MAC-LIBDM-XX-00-DR-A-001.pdf")
    assert result.passed is False
    assert any("revision" in d.lower() for d in result.details)


def test_wrong_field_count():
    result = validate_naming("MAC-LIBDM-XX-00-DR-A_P01.pdf")  # 6 fields, not 7
    assert result.passed is False
    assert any("7 hyphen-separated fields" in d for d in result.details)
