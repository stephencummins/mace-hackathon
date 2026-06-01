"""Tests for the FastAPI validation service.

No real Anthropic API calls — Silver is skipped by removing ANTHROPIC_API_KEY
in fixtures, so the service responds with naming results only.
"""

from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
PASSING_FIXTURE = EXAMPLES / "MAC-LIBDM-XX-00-DR-A-001_P01.pdf"
FAILING_FIXTURE = EXAMPLES / "floor plan ground.pdf"


@pytest.fixture
def client(monkeypatch):
    """TestClient with API_TOKEN set and Silver disabled (no ANTHROPIC_API_KEY)."""
    monkeypatch.setenv("API_TOKEN", "test-token")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    from src.api.main import app
    with TestClient(app) as c:
        yield c


def test_healthz_unauthenticated(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_validate_requires_auth(client):
    files = {"file": ("test.pdf", b"%PDF-1.4 test", "application/pdf")}
    r = client.post("/validate", files=files)
    assert r.status_code == 401
    assert r.headers.get("www-authenticate") == "Bearer"


def test_validate_rejects_wrong_token(client):
    files = {"file": ("test.pdf", b"%PDF-1.4 test", "application/pdf")}
    r = client.post(
        "/validate",
        files=files,
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert r.status_code == 401


def test_validate_passing_fixture(client):
    pdf_bytes = PASSING_FIXTURE.read_bytes()
    files = {"file": (PASSING_FIXTURE.name, pdf_bytes, "application/pdf")}
    r = client.post(
        "/validate",
        files=files,
        headers={"Authorization": "Bearer test-token"},
    )
    assert r.status_code == 200
    body = r.json()
    # Uploaded filename was preserved through the temp dir, so naming should pass
    assert body["naming"]["passed"] is True
    assert body["naming"]["fields"]["project"] == "MAC"
    # Silver was skipped because ANTHROPIC_API_KEY is removed in this fixture
    assert body["content"] is None
    assert body["content_error"] is None


def test_validate_failing_fixture(client):
    pdf_bytes = FAILING_FIXTURE.read_bytes()
    files = {"file": (FAILING_FIXTURE.name, pdf_bytes, "application/pdf")}
    r = client.post(
        "/validate",
        files=files,
        headers={"Authorization": "Bearer test-token"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["naming"]["passed"] is False
    assert any("whitespace" in d.lower() for d in body["naming"]["details"])


def test_refuses_to_start_without_api_token(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)
    from src.api.main import app
    with pytest.raises(RuntimeError, match="API_TOKEN"):
        with TestClient(app):
            pass
