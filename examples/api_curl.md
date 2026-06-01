# Calling the validation API

The Gold-tier service exposes one POST endpoint plus a health check. Run it
locally with:

```powershell
$env:API_TOKEN = "your-secret"
$env:ANTHROPIC_API_KEY = "..."        # optional; enables Silver checks
uvicorn src.api.main:app --reload
```

The server refuses to start if `API_TOKEN` is unset.

## Health check

```bash
curl http://127.0.0.1:8000/healthz
# {"status":"ok"}
```

## Validate a document

### bash / curl

```bash
curl -X POST http://127.0.0.1:8000/validate \
  -H "Authorization: Bearer $API_TOKEN" \
  -F "file=@examples/MAC-LIBDM-XX-00-DR-A-001_P01.pdf"
```

### PowerShell

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/validate `
  -Headers @{ Authorization = "Bearer $env:API_TOKEN" } `
  -Form @{ file = Get-Item examples/MAC-LIBDM-XX-00-DR-A-001_P01.pdf }
```

## Response shape

```json
{
  "path": "...",
  "naming": {
    "passed": true,
    "status": "pass",
    "summary": "Filename follows ISO 19650 convention",
    "details": [],
    "fields": { "project": "MAC", "originator": "LIBDM", ... }
  },
  "content": {
    "overall_status": "fail",
    "summary": "...",
    "findings": [
      { "check": "...", "status": "fail", "detail": "...", "suggested_fix": "..." }
    ]
  },
  "content_error": null
}
```

`content` is `null` when the server has no `ANTHROPIC_API_KEY` configured.
`content_error` is a string when the Anthropic call failed (rate limit,
network); the naming result is still returned.

## OpenAPI

The interactive docs are at `http://127.0.0.1:8000/docs` (Swagger UI) and
`http://127.0.0.1:8000/redoc`.
