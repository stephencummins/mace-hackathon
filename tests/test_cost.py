"""Tests for the pricing/cost module and the cost_report CLI."""

from pathlib import Path
import json
import sys

import pytest
from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.cost import (
    MODEL_ALIASES,
    PRICING,
    compute_cost,
    format_usd,
    get_pricing,
    resolve_alias,
)
from src.cost_report import main as cost_report_main


# -- Pricing math ------------------------------------------------------------


def test_empty_usage_returns_zero():
    assert compute_cost({}, "claude-sonnet-4-6") == 0.0
    assert compute_cost(None, "claude-sonnet-4-6") == 0.0  # type: ignore[arg-type]


def test_input_only_cost():
    # 1M input tokens on Sonnet = $3.00
    cost = compute_cost({"input_tokens": 1_000_000}, "claude-sonnet-4-6")
    assert cost == pytest.approx(3.00)


def test_output_only_cost():
    # 1M output tokens on Sonnet = $15.00
    cost = compute_cost({"output_tokens": 1_000_000}, "claude-sonnet-4-6")
    assert cost == pytest.approx(15.00)


def test_cache_write_multiplier():
    # 1M cache_creation_input_tokens on Sonnet = $3 * 1.25 = $3.75
    cost = compute_cost({"cache_creation_input_tokens": 1_000_000}, "claude-sonnet-4-6")
    assert cost == pytest.approx(3.75)


def test_cache_read_multiplier():
    # 1M cache_read_input_tokens on Sonnet = $3 * 0.10 = $0.30
    cost = compute_cost({"cache_read_input_tokens": 1_000_000}, "claude-sonnet-4-6")
    assert cost == pytest.approx(0.30)


def test_all_four_components_sum():
    usage = {
        "input_tokens": 1_000_000,                    # $3.00
        "output_tokens": 1_000_000,                   # $15.00
        "cache_creation_input_tokens": 1_000_000,     # $3.75
        "cache_read_input_tokens": 1_000_000,         # $0.30
    }
    assert compute_cost(usage, "claude-sonnet-4-6") == pytest.approx(22.05)


def test_haiku_is_cheaper_than_sonnet_for_same_usage():
    usage = {"input_tokens": 100_000, "output_tokens": 50_000}
    sonnet = compute_cost(usage, "claude-sonnet-4-6")
    haiku = compute_cost(usage, "claude-haiku-4-5")
    assert haiku < sonnet
    # 100k input + 50k output: Sonnet $3*0.1 + $15*0.05 = $1.05, Haiku $1*0.1 + $5*0.05 = $0.35
    assert sonnet == pytest.approx(1.05)
    assert haiku == pytest.approx(0.35)


def test_unknown_model_falls_back_to_sonnet():
    usage = {"input_tokens": 1_000_000}
    assert compute_cost(usage, "claude-some-future-model") == pytest.approx(3.00)
    assert get_pricing("claude-some-future-model") is PRICING["claude-sonnet-4-6"]


# -- Aliases -----------------------------------------------------------------


def test_resolve_alias_known():
    assert resolve_alias("haiku") == "claude-haiku-4-5"
    assert resolve_alias("sonnet") == "claude-sonnet-4-6"
    assert resolve_alias("opus") == "claude-opus-4-7"


def test_resolve_alias_case_insensitive():
    assert resolve_alias("HAIKU") == "claude-haiku-4-5"
    assert resolve_alias("Sonnet") == "claude-sonnet-4-6"


def test_resolve_alias_passes_through_full_ids():
    assert resolve_alias("claude-opus-4-6") == "claude-opus-4-6"


def test_all_aliases_resolve_to_priced_models():
    for alias, model_id in MODEL_ALIASES.items():
        assert model_id in PRICING, f"alias {alias!r} -> unpriced model {model_id!r}"


# -- format_usd --------------------------------------------------------------


def test_format_usd_small_amounts_show_four_decimals():
    assert format_usd(0.0001) == "$0.0001"
    assert format_usd(0.5) == "$0.5000"


def test_format_usd_large_amounts_show_two_decimals_with_commas():
    assert format_usd(1.5) == "$1.50"
    assert format_usd(12_345.67) == "$12,345.67"


# -- cost_report CLI ---------------------------------------------------------


def _seed_cache(cache_dir: Path, model: str, usage: dict, count: int = 1) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    for i in range(count):
        path = cache_dir / f"key{i:04d}.json"
        path.write_text(
            json.dumps(
                {
                    "result": {"overall_status": "pass", "summary": "ok", "findings": []},
                    "usage": usage,
                    "model": model,
                    "cached_at": "2026-01-01T00:00:00",
                }
            ),
            encoding="utf-8",
        )


def test_cost_report_empty_directory(tmp_path):
    result = CliRunner().invoke(cost_report_main, ["--cache-dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "No cached entries" in result.output


def test_cost_report_populated(tmp_path):
    _seed_cache(
        tmp_path,
        model="claude-sonnet-4-6",
        usage={"input_tokens": 1000, "output_tokens": 500},
        count=4,
    )
    result = CliRunner().invoke(
        cost_report_main,
        ["--cache-dir", str(tmp_path), "--volume", "1000", "--manual-rate", "60", "--manual-mins", "15"],
    )
    assert result.exit_code == 0
    assert "Cost Report" in result.output
    assert "Documents in cache" in result.output
    assert "claude-sonnet-4-6" in result.output
    assert "Projection at 1,000 docs/month" in result.output
    assert "Manual" in result.output and "Automated" in result.output
    assert "Savings" in result.output


def test_cost_report_per_model_breakdown(tmp_path):
    _seed_cache(tmp_path, model="claude-haiku-4-5", usage={"input_tokens": 1000}, count=2)
    _seed_cache(tmp_path / "more", model="claude-sonnet-4-6", usage={"input_tokens": 1000}, count=3)
    # Move sonnet entries up
    for f in (tmp_path / "more").glob("*.json"):
        f.rename(tmp_path / f"s_{f.name}")
    result = CliRunner().invoke(cost_report_main, ["--cache-dir", str(tmp_path)])
    assert result.exit_code == 0
    # Both models should appear in the per-model table
    assert "claude-haiku-4-5" in result.output
    assert "claude-sonnet-4-6" in result.output
