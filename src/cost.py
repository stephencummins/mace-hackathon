"""Pricing constants and cost computation for Claude API calls.

Pricing is cached from the Anthropic platform docs (2026-04-29 snapshot).
The numbers move slowly but check https://platform.claude.com/docs/en/pricing
if you suspect drift.

Cache multipliers reflect the 5-minute TTL pricing we use on the rubric system
prompt: writes are billed at 1.25x the input rate, reads at ~0.10x.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

DEFAULT_FALLBACK_MODEL = "claude-sonnet-4-6"


@dataclass(frozen=True)
class ModelPricing:
    input_per_million: float       # USD per 1M input tokens
    output_per_million: float      # USD per 1M output tokens
    cache_write_multiplier: float = 1.25  # 5-min TTL writes vs base input
    cache_read_multiplier: float = 0.10   # cache reads vs base input


# Pricing snapshot — see module docstring for refresh guidance.
PRICING: dict[str, ModelPricing] = {
    "claude-opus-4-7":   ModelPricing(input_per_million=5.00, output_per_million=25.00),
    "claude-opus-4-6":   ModelPricing(input_per_million=5.00, output_per_million=25.00),
    "claude-sonnet-4-6": ModelPricing(input_per_million=3.00, output_per_million=15.00),
    "claude-haiku-4-5":  ModelPricing(input_per_million=1.00, output_per_million=5.00),
}


# Friendly tier names. Pass either an alias or a full model id; resolve_alias
# returns a model id you can hand to the SDK.
MODEL_ALIASES: dict[str, str] = {
    "opus":   "claude-opus-4-7",
    "sonnet": "claude-sonnet-4-6",
    "haiku":  "claude-haiku-4-5",
}


def resolve_alias(name_or_id: str) -> str:
    """Map an alias (haiku/sonnet/opus) to a model id, or pass through."""
    return MODEL_ALIASES.get(name_or_id.lower(), name_or_id)


def get_pricing(model: Optional[str]) -> ModelPricing:
    """Return pricing for the given model id, falling back to Sonnet on unknowns."""
    if model and model in PRICING:
        return PRICING[model]
    return PRICING[DEFAULT_FALLBACK_MODEL]


def compute_cost(usage: dict, model: str) -> float:
    """Compute the USD cost of a single API call from its usage block.

    Usage shape (Anthropic SDK):
        input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens

    Any missing field is treated as zero. Returns 0.0 for an empty usage dict.
    """
    if not usage:
        return 0.0
    p = get_pricing(model)
    input_rate = p.input_per_million / 1_000_000
    output_rate = p.output_per_million / 1_000_000
    return (
        int(usage.get("input_tokens") or 0) * input_rate
        + int(usage.get("cache_creation_input_tokens") or 0) * input_rate * p.cache_write_multiplier
        + int(usage.get("cache_read_input_tokens") or 0) * input_rate * p.cache_read_multiplier
        + int(usage.get("output_tokens") or 0) * output_rate
    )


def format_usd(amount: float) -> str:
    """Format a USD amount for display: $0.0123 / $1.23 / $12,345.67."""
    if amount < 1:
        return f"${amount:.4f}"
    return f"${amount:,.2f}"
