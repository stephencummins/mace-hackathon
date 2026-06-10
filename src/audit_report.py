"""Inspect the validation audit trail.

Usage:
    python -m src.audit_report
    python -m src.audit_report --last 50 --source api
    python -m src.audit_report --principal tok_a1b2
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from src import audit
from src.cost import format_usd

# Force UTF-8 on Windows to match the main CLI's behaviour.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def _status_glyph(status: Optional[str]) -> str:
    return {
        "pass": "✓",
        "fail": "✗",
        "warning": "⚠",
        "skipped": "…",
        None: "…",
    }.get(status, "?")


@click.command()
@click.option(
    "--audit-dir",
    "audit_dir",
    type=click.Path(path_type=Path),
    default=str(audit.DEFAULT_DIR),
    show_default=True,
    help="Directory containing validations.jsonl.",
)
@click.option("--last", default=20, show_default=True, type=int, help="Show the most recent N entries.")
@click.option("--source", default=None, help="Filter by source (cli, api, ...).")
@click.option("--principal", default=None, help="Filter by principal (substring match).")
def main(audit_dir: Path, last: int, source: Optional[str], principal: Optional[str]) -> None:
    """Tail the audit log and print a Rich table plus a summary footer."""
    console = Console(force_terminal=True)
    entries = list(audit.iter_entries(Path(audit_dir)))

    if source:
        entries = [e for e in entries if e.get("source") == source]
    if principal:
        entries = [e for e in entries if principal in (e.get("principal") or "")]

    if not entries:
        console.print(f"[yellow]No audit entries in {audit_dir}/[/yellow]")
        return

    recent = entries[-last:] if last > 0 else entries

    table = Table(title=f"Audit trail (showing {len(recent)} of {len(entries)})", show_header=True, header_style="bold")
    table.add_column("Timestamp", style="dim")
    table.add_column("Source")
    table.add_column("Principal")
    table.add_column("Document")
    table.add_column("Status")
    table.add_column("Model", style="dim")
    table.add_column("Cache")
    table.add_column("Cost", justify="right")

    for e in recent:
        status_text = f"{_status_glyph(e.get('content_status'))} {e.get('content_status') or 'skipped'}"
        cache_text = "✓ hit" if e.get("from_cache") else "— miss"
        table.add_row(
            e.get("ts", "?")[:19],
            e.get("source", "?"),
            e.get("principal", ""),
            (e.get("doc_name") or "")[:40],
            status_text,
            (e.get("model") or "")[len("claude-") :] or "?",
            cache_text,
            format_usd(float(e.get("cost_usd") or 0.0)),
        )

    console.print(table)

    summary = audit.summary(entries)
    footer = Table(title="Summary (all matching entries)", show_header=True, header_style="bold")
    footer.add_column("Count", justify="right")
    footer.add_column("Group")
    footer.add_row(str(summary["total"]), "Total validations")
    for src, n in sorted(summary["by_source"].items()):
        footer.add_row(str(n), f"Source: {src}")
    for status, n in sorted(summary["by_status"].items()):
        footer.add_row(str(n), f"Status: {status}")
    for prin, n in sorted(summary["by_principal"].items()):
        footer.add_row(str(n), f"Principal: {prin}")
    footer.add_row(str(summary["cache_hits"]), "Cache hits")
    footer.add_row(format_usd(summary["spent_usd"]), "Actual spend (fresh runs)")
    footer.add_row(format_usd(summary["saved_usd"]), "Saved by cache")
    console.print()
    console.print(footer)


if __name__ == "__main__":
    main()
