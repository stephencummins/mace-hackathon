"""ISO 19650 file-naming validator (Bronze level).

Pattern: PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-NUMBER_REVISION
Example: MAC-LIBDM-XX-00-DR-A-001_P01.pdf
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union

FIELD_PATTERNS: dict[str, str] = {
    "project":    r"[A-Z0-9]{2,6}",
    "originator": r"[A-Z0-9]{2,6}",
    "volume":     r"[A-Z0-9]{2,4}",
    "level":      r"[A-Z0-9]{2,4}",
    "type":       r"[A-Z]{2}",
    "role":       r"[A-Z]",
    "number":     r"[0-9]{3,6}",
    "revision":   r"[A-Z][0-9]{2}",
}

_PREFIX_FIELDS = ["project", "originator", "volume", "level", "type", "role", "number"]

_FULL_PATTERN = re.compile(
    "^"
    + "-".join(f"(?P<{name}>{FIELD_PATTERNS[name]})" for name in _PREFIX_FIELDS)
    + f"_(?P<revision>{FIELD_PATTERNS['revision']})"
    + "$"
)


@dataclass
class ValidationResult:
    passed: bool
    status: str   # "pass" | "fail"
    summary: str
    details: list[str] = field(default_factory=list)
    fields: dict[str, str] = field(default_factory=dict)


def validate_naming(path: Union[str, Path]) -> ValidationResult:
    """Validate a filename against the ISO 19650 Bronze naming convention.

    Only the filename stem (without extension) is checked. Returns a
    ValidationResult; on failure, ``details`` lists the specific deviations.
    """
    stem = Path(path).stem

    match = _FULL_PATTERN.match(stem)
    if match:
        return ValidationResult(
            passed=True,
            status="pass",
            summary="Filename follows ISO 19650 convention",
            fields=match.groupdict(),
        )

    return ValidationResult(
        passed=False,
        status="fail",
        summary="Filename does not follow ISO 19650 convention",
        details=_diagnose(stem),
    )


def _diagnose(stem: str) -> list[str]:
    issues: list[str] = []

    if re.search(r"\s", stem):
        issues.append("Contains whitespace; ISO 19650 names use only A-Z, 0-9, '-' and '_'")

    if "_" not in stem:
        issues.append("Missing revision suffix (expected '_REVISION', e.g. '_P01')")
        return issues

    prefix, _, revision = stem.rpartition("_")
    parts = prefix.split("-")

    if len(parts) != len(_PREFIX_FIELDS):
        issues.append(
            f"Expected {len(_PREFIX_FIELDS)} hyphen-separated fields before '_REVISION', "
            f"found {len(parts)}"
        )
    else:
        for name, value in zip(_PREFIX_FIELDS, parts):
            if not re.fullmatch(FIELD_PATTERNS[name], value):
                issues.append(
                    f"{name.upper()} '{value}' does not match expected pattern "
                    f"/{FIELD_PATTERNS[name]}/"
                )

    if not re.fullmatch(FIELD_PATTERNS["revision"], revision):
        issues.append(
            f"REVISION '{revision}' does not match expected pattern "
            f"/{FIELD_PATTERNS['revision']}/ (e.g. P01)"
        )

    return issues
