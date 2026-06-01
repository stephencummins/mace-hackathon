"""Tests for the document-level content validation cache."""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import cache


PDF = b"%PDF-1.4 example bytes"
RUBRIC = "You are an ISO 19650 reviewer. ..."
MODEL = "claude-sonnet-4-6"


def test_cache_key_is_deterministic():
    a = cache.cache_key(PDF, RUBRIC, MODEL)
    b = cache.cache_key(PDF, RUBRIC, MODEL)
    assert a == b
    assert len(a) == 64  # SHA-256 hex


def test_cache_key_changes_when_pdf_changes():
    a = cache.cache_key(PDF, RUBRIC, MODEL)
    b = cache.cache_key(PDF + b"X", RUBRIC, MODEL)
    assert a != b


def test_cache_key_changes_when_rubric_changes():
    a = cache.cache_key(PDF, RUBRIC, MODEL)
    b = cache.cache_key(PDF, RUBRIC + " edit", MODEL)
    assert a != b


def test_cache_key_changes_when_model_changes():
    a = cache.cache_key(PDF, RUBRIC, MODEL)
    b = cache.cache_key(PDF, RUBRIC, "claude-haiku-4-5")
    assert a != b


def test_get_missing_returns_none(tmp_path):
    assert cache.get("nonexistent-key", tmp_path) is None


def test_put_creates_directory_and_get_returns_payload(tmp_path):
    nested = tmp_path / "nested" / "cache"
    key = cache.cache_key(PDF, RUBRIC, MODEL)
    written = cache.put(
        key,
        result={"overall_status": "pass", "summary": "ok", "findings": []},
        usage={"input_tokens": 100, "output_tokens": 50},
        model=MODEL,
        cache_dir=nested,
    )
    assert written.exists()
    payload = cache.get(key, nested)
    assert payload is not None
    assert payload["result"]["overall_status"] == "pass"
    assert payload["usage"]["input_tokens"] == 100
    assert payload["model"] == MODEL
    assert "cached_at" in payload


def test_get_corrupt_file_returns_none(tmp_path):
    key = "abc123"
    (tmp_path / f"{key}.json").write_text("not valid json {", encoding="utf-8")
    assert cache.get(key, tmp_path) is None


def test_clear_removes_only_json_in_directory(tmp_path):
    (tmp_path / "a.json").write_text("{}", encoding="utf-8")
    (tmp_path / "b.json").write_text("{}", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("keep me", encoding="utf-8")
    removed = cache.clear(tmp_path)
    assert removed == 2
    assert (tmp_path / "notes.txt").exists()


def test_clear_missing_directory_returns_zero(tmp_path):
    assert cache.clear(tmp_path / "does-not-exist") == 0
