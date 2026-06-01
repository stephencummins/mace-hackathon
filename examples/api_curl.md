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
  "content_error": null,
  "from_cache": false,
  "usage": { "input_tokens": 1628, "output_tokens": 1649, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 4800 },
  "model": "claude-sonnet-4-6"
}
```

`content` is `null` when the server has no `ANTHROPIC_API_KEY` configured.
`content_error` is a string when the Anthropic call failed (rate limit,
network); the naming result is still returned. `from_cache` is `true` when
the result came from the document-level cache (`.cache/content-validator/`);
the `usage` field reflects the original call's token counts so cost
attribution works on cached responses too. Pass `?no_cache=true` on
`/validate` to skip the cache.

## OpenAPI

The interactive docs are at `http://127.0.0.1:8000/docs` (Swagger UI) and
`http://127.0.0.1:8000/redoc`.
