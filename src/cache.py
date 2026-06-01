"""Document-level cache for content validation.

Skips the Claude API call when the same (pdf bytes, rubric, model) triplet
was validated before. Cache is filesystem-based, one JSON file per fingerprint.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DEFAULT_DIR = Path(".cache/content-validator")


def cache_key(pdf_bytes: bytes, rubric_text: str, model: str) -> str:
    """SHA-256 over pdf bytes + rubric + model. Any of those changing
    produces a new key, so cache invalidates automatically."""
    h = hashlib.sha256()
    h.update(pdf_bytes)
    h.update(b"|")
    h.update(rubric_text.encode("utf-8"))
    h.update(b"|")
    h.update(model.encode("utf-8"))
    return h.hexdigest()


def get(key: str, cache_dir: Path = DEFAULT_DIR) -> Optional[dict]:
    """Return cached payload or None on miss. Corrupt files count as a miss."""
    path = cache_dir / f"{key}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def put(
    key: str,
    result: dict,
    usage: dict,
    model: str,
    cache_dir: Path = DEFAULT_DIR,
) -> Path:
    """Write a cache entry. Creates the directory if needed."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "result": result,
        "usage": usage,
        "cached_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": model,
    }
    path = cache_dir / f"{key}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def clear(cache_dir: Path = DEFAULT_DIR) -> int:
    """Remove all cache files in the directory. Returns count removed."""
    if not cache_dir.exists():
        return 0
    count = 0
    for entry in cache_dir.glob("*.json"):
        try:
            entry.unlink()
            count += 1
        except OSError:
            pass
    return count
