"""Batch validation runner.

Wraps the Bronze + Silver validators with per-document error isolation so a
single bad PDF can't abort a batch.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional

import anthropic
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from src.validators import (
    ContentValidationResult,
    ValidationResult,
    validate_content,
    validate_naming,
)


@dataclass
class DocReport:
    path: Path
    naming: ValidationResult
    content: Optional[ContentValidationResult] = None
    content_error: Optional[str] = None

    def to_json_dict(self) -> dict:
        return {
            "path": str(self.path),
            "naming": {
                "passed": self.naming.passed,
                "status": self.naming.status,
                "summary": self.naming.summary,
                "details": list(self.naming.details),
                "fields": dict(self.naming.fields),
            },
            "content": self.content.model_dump() if self.content else None,
            "content_error": self.content_error,
        }


def iter_pdfs(target: Path, *, recursive: bool = True) -> Iterator[Path]:
    """Yield documents to validate.

    - If ``target`` is a file, yield it (regardless of extension).
    - If ``target`` is a directory, yield ``*.pdf`` matches, sorted.
    """
    if target.is_file():
        yield target
        return
    pattern = "**/*.pdf" if recursive else "*.pdf"
    yield from sorted(target.glob(pattern))


def validate_documents(
    paths: Iterable[Path],
    *,
    progress: bool = True,
    client: Optional[anthropic.Anthropic] = None,
) -> list[DocReport]:
    """Validate each path. anthropic.APIError is captured per-doc; the batch
    continues even if one document's Silver check fails."""
    paths_list = list(paths)
    reports: list[DocReport] = []

    if progress and paths_list:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            transient=True,
        ) as bar:
            task = bar.add_task("Validating...", total=len(paths_list))
            for path in paths_list:
                bar.update(task, description=f"Validating {path.name}")
                reports.append(_validate_one(path, client))
                bar.update(task, advance=1)
    else:
        for path in paths_list:
            reports.append(_validate_one(path, client))

    return reports


def _validate_one(path: Path, client: Optional[anthropic.Anthropic]) -> DocReport:
    naming = validate_naming(path)
    try:
        content = validate_content(path, client=client) if client else validate_content(path)
        return DocReport(path=path, naming=naming, content=content)
    except anthropic.APIError as exc:
        return DocReport(
            path=path,
            naming=naming,
            content_error=f"{type(exc).__name__}: {exc}",
        )
