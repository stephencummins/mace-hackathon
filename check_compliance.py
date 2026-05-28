#!/usr/bin/env python3
"""
Mace Digital Compliance Checker
ISO 19650 Document Validation Tool

Usage:
    python check_compliance.py document.pdf
    python check_compliance.py --help
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import click
from rich.console import Console
from rich.table import Table

import anthropic

from src.validators import validate_content, validate_naming

load_dotenv()

# Force UTF-8 output on Windows to avoid emoji/Rich encoding crashes
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

console = Console(force_terminal=True)


_STATUS_SYMBOLS = {"pass": "✓ Pass", "fail": "✗ Fail", "warning": "⚠ Warning"}


def _status_symbol(status: str) -> str:
    return _STATUS_SYMBOLS.get(status, status)


def _pretty_status(status: str) -> str:
    return status.upper()


@click.command()
@click.argument('document', type=click.Path(exists=True))
@click.option('--format', default='console', help='Output format: console, html, json')
@click.option('--strict', is_flag=True, help='Enable strict validation mode')
@click.option('--output', '-o', help='Output file path for report')
def check_compliance(document, format, strict, output):
    """
    Check document compliance with ISO 19650 standards.

    DOCUMENT: Path to the document to validate (PDF, DOCX, or XLSX)
    """
    console.print(f"\n[bold blue]Mace Digital Compliance Checker[/bold blue]")
    console.print(f"[dim]ISO 19650 Validation Tool[/dim]\n")

    doc_path = Path(document)
    console.print(f"📄 Analyzing: [cyan]{doc_path.name}[/cyan]")
    console.print(f"📏 Size: {doc_path.stat().st_size / 1024:.2f} KB\n")

    naming_result = validate_naming(doc_path)

    table = Table(title="Validation Results")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="white")

    if naming_result.passed:
        table.add_row("File Naming", "✓ Pass", naming_result.summary)
    else:
        details = "; ".join(naming_result.details) or naming_result.summary
        table.add_row("File Naming", "✗ Fail", details)

    try:
        content_result = validate_content(doc_path)
    except anthropic.APIError as exc:
        table.add_row("Content Review (AI)", "✗ Error", f"{type(exc).__name__}: {exc}")
        content_result = None
    else:
        if content_result is None:
            table.add_row(
                "Content Review (AI)",
                "… Skipped",
                "ANTHROPIC_API_KEY not set — set it in .env to enable Silver checks",
            )
        else:
            table.add_row(
                f"Content Review (AI) — {_pretty_status(content_result.overall_status)}",
                _status_symbol(content_result.overall_status),
                content_result.summary,
            )
            for finding in content_result.findings:
                table.add_row(
                    f"  └ {finding.check}",
                    _status_symbol(finding.status),
                    finding.detail,
                )

    console.print(table)
    console.print("\n[bold green]Validation Complete![/bold green]\n")

    # Show next steps
    console.print("[bold]Next Steps:[/bold]")
    console.print("1. Implement validators in src/validators/")
    console.print("2. Add document parsers in src/parsers/")
    console.print("3. Integrate Claude AI for content analysis")
    console.print("4. Generate detailed reports")


if __name__ == '__main__':
    check_compliance()
