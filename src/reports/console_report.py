"""Rich-console rendering of DocReports. Shared by the console output path
and the HTML renderer (which prints through a recording Console)."""

from __future__ import annotations

from collections import Counter

from rich.console import Console
from rich.table import Table

from src.runner import DocReport

_STATUS_SYMBOLS = {
    "pass": "✓ Pass",
    "fail": "✗ Fail",
    "warning": "⚠ Warning",
    "skipped": "… Skipped",
    "error": "✗ Error",
}


def _symbol(status: str) -> str:
    return _STATUS_SYMBOLS.get(status, status)


def render_console(reports: list[DocReport], console: Console) -> None:
    """Print one section per doc, plus a batch summary if there's more than one."""
    for report in reports:
        _render_one(report, console)
    if len(reports) > 1:
        _render_summary(reports, console)


def _render_one(report: DocReport, console: Console) -> None:
    console.print(f"\n[bold cyan]📄 {report.path.name}[/bold cyan]")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Check", style="cyan")
    table.add_column("Status")
    table.add_column("Details")

    if report.naming.passed:
        table.add_row("File Naming", _symbol("pass"), report.naming.summary)
    else:
        details = "; ".join(report.naming.details) or report.naming.summary
        table.add_row("File Naming", _symbol("fail"), details)

    if report.content_error:
        table.add_row("Content Review (AI)", _symbol("error"), report.content_error)
    elif report.content is None:
        table.add_row(
            "Content Review (AI)",
            _symbol("skipped"),
            "ANTHROPIC_API_KEY not set — set it in .env to enable Silver checks",
        )
    else:
        cache_suffix = " [magenta](cached)[/magenta]" if report.from_cache else ""
        table.add_row(
            f"Content Review (AI) — {report.content.overall_status.upper()}{cache_suffix}",
            _symbol(report.content.overall_status),
            report.content.summary,
        )
        for finding in report.content.findings:
            table.add_row(
                f"  └ {finding.check}",
                _symbol(finding.status),
                finding.detail,
            )
            if finding.suggested_fix:
                table.add_row(
                    "      [green]↳ Fix[/green]",
                    "",
                    f"[green]{finding.suggested_fix}[/green]",
                )

    console.print(table)


def _render_summary(reports: list[DocReport], console: Console) -> None:
    counts: Counter[str] = Counter()
    naming_fails = 0
    cache_hits = 0
    saved_input = 0
    saved_output = 0
    for report in reports:
        if report.content_error:
            counts["error"] += 1
        elif report.content is None:
            counts["skipped"] += 1
        else:
            counts[report.content.overall_status] += 1
        if not report.naming.passed:
            naming_fails += 1
        if report.from_cache:
            cache_hits += 1
            usage = report.cached_usage or {}
            saved_input += int(usage.get("input_tokens") or 0)
            saved_output += int(usage.get("output_tokens") or 0)

    table = Table(title="Batch Summary", show_header=True, header_style="bold")
    table.add_column("Count", justify="right")
    table.add_column("Outcome")
    table.add_row(str(len(reports)), "Documents validated")
    for key in ("pass", "warning", "fail", "skipped", "error"):
        if counts[key]:
            table.add_row(str(counts[key]), f"Content review: {key}")
    if naming_fails:
        table.add_row(str(naming_fails), "Naming non-conformant")
    if cache_hits:
        saved = f"{saved_input:,} input + {saved_output:,} output tokens saved"
        table.add_row(str(cache_hits), f"From cache ({saved})")
    console.print()
    console.print(table)
