"""FastAPI service wrapping the Bronze + Silver validators.

Run locally:
    $env:API_TOKEN = "your-secret"
    uvicorn src.api.main:app --reload
"""

from __future__ import annotations

import hmac
import os
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

# Use the OS cert store so the embedded Anthropic client trusts corporate
# TLS-intercepting proxies (e.g. Mace's network). Must run before any
# HTTPS client is constructed.
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, UploadFile, status

from src.runner import validate_documents

load_dotenv()

_TOKEN: Optional[str] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _TOKEN
    token = os.getenv("API_TOKEN")
    if not token:
        raise RuntimeError(
            "API_TOKEN environment variable is required. "
            "Set it before starting the server, e.g. "
            "$env:API_TOKEN = 'your-secret' (PowerShell) "
            "or export API_TOKEN=your-secret (bash)."
        )
    _TOKEN = token
    try:
        yield
    finally:
        _TOKEN = None


app = FastAPI(
    title="Mace Compliance API",
    version="0.1.0",
    description="ISO 19650 document validation: Bronze (naming) + Silver (AI content review).",
    lifespan=lifespan,
)


def require_token(authorization: Optional[str] = Header(default=None)) -> None:
    """Bearer-token auth dependency. Returns 401 on missing/wrong token."""
    if _TOKEN is None:
        # Should not happen: lifespan refuses to start without API_TOKEN.
        raise HTTPException(status_code=500, detail="Server not configured")
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header (expected 'Bearer <token>')",
            headers={"WWW-Authenticate": "Bearer"},
        )
    presented = authorization[len("Bearer ") :].strip()
    if not hmac.compare_digest(presented.encode("utf-8"), _TOKEN.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/healthz")
def healthz() -> dict:
    """Liveness probe. Intentionally unauthenticated."""
    return {"status": "ok"}


@app.post("/validate", dependencies=[Depends(require_token)])
def validate(file: UploadFile) -> dict:
    """Validate one PDF against ISO 19650.

    Accepts a single PDF via ``multipart/form-data``. Returns the same JSON
    structure the CLI emits with ``--format json`` for one document.
    """
    # Preserve the uploaded basename so the naming validator sees the real
    # filename, not the temp name. Path().name strips any path components.
    safe_name = Path(file.filename or "upload.pdf").name
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / safe_name
        target.write_bytes(file.file.read())
        [report] = validate_documents([target], progress=False)
        return report.to_json_dict()
