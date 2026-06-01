"""Aggregate the document cache into a cost report.

Usage:
    python -m src.cost_report
    python -m src.cost_report --volume 1000 --manual-rate 60 --manual-mins 15

Reads every JSON file under ``--cache-dir`` (default
``.cache/content-validator/``), sums the recorded usage per model, applies
the pricing in ``src.cost``, and prints a Markdown report to stdout
covering corpus spend, per-model breakdown, monthly projection, and ROI
vs manual review.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import click

from src.cache import DEFAULT_DIR
from src.cost import compute_cost, format_usd


def _scan_cache(cache_dir: Path) -> list[dict]:
    """Return cached payloads as a list of dicts. Skips corrupt files."""
    if not cache_dir.exists():
        return []
    entries: list[dict] = []
    for path in sorted(cache_dir.glob("*.json")):
        try:
            entries.append(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError):
            continue
    return entries


def _render_markdown(
    entries: list[dict],
    volume: int,
    manual_rate: float,
    manual_mins: int,
) -> str:
    if not entries:
        return "# Cost Report\n\nNo cached entries found. Run the validator first to populate `.cache/content-validator/`.\n"

    by_model: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_model[e.get("model") or "unknown"].append(e)

    total_cost = sum(compute_cost(e.get("usage") or {}, e.get("model") or "") for e in entries)
    avg_per_doc = total_cost / len(entries) if entries else 0.0
    projected = avg_per_doc * volume

    manual_per_doc = (manual_rate / 60.0) * manual_mins
    manual_monthly = manual_per_doc * volume
    savings = manual_monthly - projected
    savings_pct = (savings / manual_monthly * 100.0) if manual_monthly else 0.0

    lines: list[str] = []
    lines.append("# Cost Report")
    lines.append("")
    lines.append(f"_Source: `{len(entries)}` cached entries_")
    lines.append("")
    lines.append("## Corpus")
    lines.append("")
    lines.append(f"- Documents in cache: **{len(entries)}**")
    lines.append(f"- Total spend (across all cached calls): **{format_usd(total_cost)}**")
    lines.append(f"- Average per document: **{format_usd(avg_per_doc)}**")
    lines.append("")
    lines.append("## Per model")
    lines.append("")
    lines.append("| Model | Docs | Total | Avg / doc |")
    lines.append("|---|---:|---:|---:|")
    for model, lst in sorted(by_model.items()):
        m_total = sum(compute_cost(e.get("usage") or {}, model) for e in lst)
        m_avg = m_total / len(lst) if lst else 0.0
        lines.append(f"| `{model}` | {len(lst)} | {format_usd(m_total)} | {format_usd(m_avg)} |")
    lines.append("")
    lines.append(f"## Projection at {volume:,} docs/month")
    lines.append("")
    lines.append(f"- Expected monthly spend: **{format_usd(projected)}**")
    lines.append("")
    lines.append("## ROI vs manual review")
    lines.append("")
    lines.append(
        f"_Assumptions: ${manual_rate:.2f}/hour × {manual_mins} min/doc = "
        f"{format_usd(manual_per_doc)}/doc for manual review._"
    )
    lines.append("")
    lines.append(f"| | Cost / doc | Monthly @ {volume:,} docs |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Manual | {format_usd(manual_per_doc)} | {format_usd(manual_monthly)} |")
    lines.append(f"| Automated | {format_usd(avg_per_doc)} | {format_usd(projected)} |")
    lines.append(
        f"| **Savings** | **{format_usd(manual_per_doc - avg_per_doc)}** | "
        f"**{format_usd(savings)} ({savings_pct:.1f}%)** |"
    )
    lines.append("")
    return "\n".join(lines)


@click.command()
@click.option(
    "--cache-dir",
    "cache_dir",
    type=click.Path(path_type=Path),
    default=str(DEFAULT_DIR),
    show_default=True,
    help="Cache directory to scan.",
)
@click.option("--volume", default=500, show_default=True, type=int, help="Projected monthly document volume.")
@click.option(
    "--manual-rate",
    "manual_rate",
    default=60.0,
    show_default=True,
    type=float,
    help="Manual reviewer hourly rate (USD).",
)
@click.option(
    "--manual-mins",
    "manual_mins",
    default=15,
    show_default=True,
    type=int,
    help="Minutes of manual review per document.",
)
def main(cache_dir: Path, volume: int, manual_rate: float, manual_mins: int) -> None:
    """Aggregate cache history into a cost report (Markdown to stdout)."""
    entries = _scan_cache(Path(cache_dir))
    click.echo(_render_markdown(entries, volume, manual_rate, manual_mins))


if __name__ == "__main__":
    main()
