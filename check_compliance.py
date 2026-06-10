#!/usr/bin/env python3
"""
Mace Digital Compliance Checker
ISO 19650 Document Validation Tool

Usage:
    python check_compliance.py document.pdf
    python check_compliance.py examples/ --format html
    python check_compliance.py --help
"""

import getpass
import sys

# Use the OS cert store so Python trusts corporate TLS-intercepting proxies
# (e.g. Mace's network). Must run before any HTTPS client is constructed.
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

from pathlib import Path
from dotenv import load_dotenv
import click
from rich.console import Console

from src import audit
from src.reports import render_console, render_html, render_json
from src.runner import DocReport, iter_pdfs, validate_documents

load_dotenv()

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

console = Console(force_terminal=True)

_DEFAULT_OUTPUT = {"html": "compliance-report.html", "json": "compliance-report.json"}


@click.command()
@click.argument(
    "document",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, path_type=Path),
)
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["console", "html", "json"], case_sensitive=False),
    default="console",
    help="Output format",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Write the report to a file. Defaults to compliance-report.<ext> for html/json.",
)
@click.option("--strict", is_flag=True, help="Enable strict validation mode (reserved)")
@click.option(
    "--no-cache",
    "no_cache",
    is_flag=True,
    help="Skip the document-level result cache (force a fresh Claude call).",
)
@click.option(
    "--model",
    "model",
    default=None,
    help="Model id or alias (haiku/sonnet/opus). Overrides CLAUDE_MODEL env var.",
)
def check_compliance(
    document: Path,
    fmt: str,
    output: Path | None,
    strict: bool,
    no_cache: bool,
    model: str | None,
) -> None:
    """Validate one document or a folder of documents against ISO 19650.

    DOCUMENT: Path to a PDF, or a directory to scan recursively for PDFs.
    """
    paths = list(iter_pdfs(document))
    if not paths:
        console.print(f"[red]No PDF files found under {document}[/red]")
        sys.exit(1)

    if fmt == "console":
        console.print("\n[bold blue]Mace Digital Compliance Checker[/bold blue]")
        console.print("[dim]ISO 19650 Validation Tool[/dim]")
        console.print(f"[dim]Scanning {len(paths)} document(s)...[/dim]")

    reports = validate_documents(
        paths,
        progress=(fmt == "console"),
        use_cache=not no_cache,
        model=model,
        audit_dir=audit.DEFAULT_DIR,
        audit_source="cli",
        audit_principal=getpass.getuser(),
    )

    if fmt == "console":
        render_console(reports, console)
        if output:
            output.write_text(_plain_text(reports), encoding="utf-8")
            console.print(f"\n[green]Wrote report to {output}[/green]")
        return

    if fmt == "html":
        content = render_html(reports)
        target = output or Path(_DEFAULT_OUTPUT["html"])
    else:  # json
        content = render_json(reports)
        target = output or Path(_DEFAULT_OUTPUT["json"])

    target.write_text(content, encoding="utf-8")
    console.print(f"[green]Wrote {fmt.upper()} report to {target}[/green]")


def _plain_text(reports: list[DocReport]) -> str:
    """Render console output as plain text for -o with --format console."""
    import io
    recording = Console(record=True, width=120, file=io.StringIO())
    render_console(reports, recording)
    return recording.export_text()


if __name__ == "__main__":
    check_compliance()
