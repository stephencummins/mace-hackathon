"""Batch validation runner.

Wraps the Bronze + Silver validators with per-document error isolation so a
single bad PDF can't abort a batch. Consults the document-level cache
(src/cache.py) before each Claude call.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional

import anthropic
from pydantic import ValidationError
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from src import cache
from src.validators import (
    ContentValidationResult,
    ValidationResult,
    validate_naming,
)
from src.validators.content_validator import (
    _RUBRIC_TEXT,
    call_claude,
    resolve_model,
)


@dataclass
class DocReport:
    path: Path
    naming: ValidationResult
    content: Optional[ContentValidationResult] = None
    content_error: Optional[str] = None
    from_cache: bool = False
    cached_usage: Optional[dict] = None

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
            "from_cache": self.from_cache,
            "cached_usage": self.cached_usage,
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
    cache_dir: Optional[Path] = None,
    use_cache: bool = True,
) -> list[DocReport]:
    """Validate each path. anthropic.APIError is captured per-doc; the batch
    continues even if one document's Silver check fails.

    Caching: when ``use_cache`` is True (default), the document cache is
    consulted before each Claude call. ``cache_dir`` defaults to
    ``cache.DEFAULT_DIR`` (``.cache/content-validator/``).
    """
    paths_list = list(paths)
    reports: list[DocReport] = []
    effective_cache_dir = cache_dir if cache_dir is not None else cache.DEFAULT_DIR

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
                reports.append(_validate_one(path, client, effective_cache_dir, use_cache))
                bar.update(task, advance=1)
    else:
        for path in paths_list:
            reports.append(_validate_one(path, client, effective_cache_dir, use_cache))

    return reports


def _validate_one(
    path: Path,
    client: Optional[anthropic.Anthropic],
    cache_dir: Path,
    use_cache: bool,
) -> DocReport:
    naming = validate_naming(path)

    # Silver is reachable only if a client was injected or an API key is set.
    if client is None and not os.getenv("ANTHROPIC_API_KEY"):
        return DocReport(path=path, naming=naming)

    model = resolve_model()

    # Cache check (read).
    cache_key: Optional[str] = None
    if use_cache:
        try:
            pdf_bytes = Path(path).read_bytes()
            cache_key = cache.cache_key(pdf_bytes, _RUBRIC_TEXT, model)
            hit = cache.get(cache_key, cache_dir)
        except OSError:
            hit = None
        if hit is not None:
            try:
                cached_result = ContentValidationResult.model_validate(hit["result"])
                return DocReport(
                    path=path,
                    naming=naming,
                    content=cached_result,
                    from_cache=True,
                    cached_usage=hit.get("usage"),
                )
            except (ValidationError, KeyError, TypeError):
                pass  # corrupt entry — fall through to a fresh call

    # Fresh call.
    effective_client = client or anthropic.Anthropic()
    try:
        result, usage = call_claude(path, effective_client, model)
    except anthropic.APIError as exc:
        return DocReport(
            path=path,
            naming=naming,
            content_error=f"{type(exc).__name__}: {exc}",
        )

    # Cache write (best effort).
    if use_cache and cache_key is not None:
        try:
            cache.put(cache_key, result.model_dump(), usage, model, cache_dir)
        except OSError:
            pass

    return DocReport(path=path, naming=naming, content=result)
