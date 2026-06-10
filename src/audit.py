"""Append-only audit trail of validation decisions.

One JSONL line per DocReport, written to ``.audit/validations.jsonl`` under
CWD. Entries are summary-only — forensic detail lives in ``.cache/`` keyed
by the same SHA-256 hash of the document bytes.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Iterator, Optional

from src.cost import compute_cost

if TYPE_CHECKING:
    from src.runner import DocReport

DEFAULT_DIR = Path(".audit")
_LOG_NAME = "validations.jsonl"


@dataclass
class AuditEntry:
    ts: str
    source: str                          # "cli" | "api" | future
    principal: str                       # OS user / "tok_<hash>" / etc.
    doc_name: str                        # basename only
    doc_hash: str                        # SHA-256 hex of raw PDF bytes
    model: Optional[str]
    from_cache: bool
    naming_passed: bool
    content_status: Optional[str]        # pass / fail / warning / None when skipped
    content_error: Optional[str]
    finding_counts: dict[str, int] = field(default_factory=dict)
    cost_usd: float = 0.0


def hash_pdf(pdf_bytes: bytes) -> str:
    return hashlib.sha256(pdf_bytes).hexdigest()


def principal_for_token(bearer: str) -> str:
    """Hashed token identifier safe to log. Never include the raw token."""
    return "tok_" + hashlib.sha256(bearer.encode("utf-8")).hexdigest()[:8]


def _log_path(audit_dir: Path) -> Path:
    return audit_dir / _LOG_NAME


def _entry_from(report: "DocReport", *, source: str, principal: str) -> AuditEntry:
    counts: Counter[str] = Counter()
    content_status: Optional[str] = None
    if report.content is not None:
        content_status = report.content.overall_status
        for f in report.content.findings:
            counts[f.status] += 1

    cost = compute_cost(report.usage or {}, report.model or "") if report.usage and report.model else 0.0

    try:
        pdf_hash = hash_pdf(Path(report.path).read_bytes())
    except OSError:
        pdf_hash = ""

    return AuditEntry(
        ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        source=source,
        principal=principal or "",
        doc_name=Path(report.path).name,
        doc_hash=pdf_hash,
        model=report.model,
        from_cache=report.from_cache,
        naming_passed=report.naming.passed,
        content_status=content_status,
        content_error=report.content_error,
        finding_counts=dict(counts),
        cost_usd=round(cost, 6),
    )


def log_validation(
    report: "DocReport",
    *,
    source: str,
    principal: str,
    audit_dir: Path = DEFAULT_DIR,
) -> AuditEntry:
    """Append one summary line for the given report. Returns the entry."""
    audit_dir.mkdir(parents=True, exist_ok=True)
    entry = _entry_from(report, source=source, principal=principal)
    line = json.dumps(asdict(entry), separators=(",", ":"))
    with _log_path(audit_dir).open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return entry


def iter_entries(audit_dir: Path = DEFAULT_DIR) -> Iterator[dict]:
    """Yield parsed entries in file order (oldest first). Skips corrupt lines."""
    path = _log_path(audit_dir)
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            try:
                yield json.loads(raw)
            except json.JSONDecodeError:
                continue


def summary(entries: Iterable[dict]) -> dict:
    """Aggregate counts and costs from an iterable of entries.

    ``spent_usd`` sums entries where ``from_cache`` is False (real spend).
    ``saved_usd`` sums entries where ``from_cache`` is True (cost the cache
    avoided). ``total_cost_usd`` keeps the old field for backwards
    compatibility but equals ``spent + saved``.
    """
    entries_list = list(entries)
    by_source: Counter[str] = Counter()
    by_status: Counter[str] = Counter()
    by_principal: Counter[str] = Counter()
    cache_hits = 0
    spent = 0.0
    saved = 0.0
    for e in entries_list:
        by_source[e.get("source") or "unknown"] += 1
        status = e.get("content_status") or "skipped"
        by_status[status] += 1
        by_principal[e.get("principal") or "unknown"] += 1
        cost = float(e.get("cost_usd") or 0.0)
        if e.get("from_cache"):
            cache_hits += 1
            saved += cost
        else:
            spent += cost
    return {
        "total": len(entries_list),
        "by_source": dict(by_source),
        "by_status": dict(by_status),
        "by_principal": dict(by_principal),
        "cache_hits": cache_hits,
        "spent_usd": round(spent, 6),
        "saved_usd": round(saved, 6),
        "total_cost_usd": round(spent + saved, 6),
    }
