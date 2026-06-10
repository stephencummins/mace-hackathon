# Runbook

Operational runbook for the Mace Digital Compliance Checker. Audience: the
**Operator** role from `GOVERNANCE.md` — whoever runs the CLI day-to-day or
keeps the HTTP service alive. Developer-level extension is in
`ONBOARDING.md`; service targets and what counts as "in spec" are in
`SLA.md`.

## What this tool is, in one paragraph

A Python CLI (`check_compliance.py`) and a FastAPI HTTP service
(`src.api.main:app`) that validate documents (PDF today) against a rubric.
The shipped rubric is ISO 19650; the same harness works for any document
type with a swappable rubric. Bronze checks the filename pattern locally;
Silver calls Claude (`claude-sonnet-4-6` by default) to read the document
and check content. Results land on stdout / a Rich console report / an HTML
or JSON file, with a per-validation audit line in `.audit/validations.jsonl`.

## Daily operation

### Start the CLI (interactive use)

```powershell
cd C:\path\to\mace-hackathon
.\venv\Scripts\activate
python check_compliance.py path\to\document.pdf
```

Common flags: `--format json|html|console`, `--no-cache`, `--model haiku|sonnet|opus`,
`--strict`. `python check_compliance.py --help` is the canonical reference.

### Start the HTTP service

```powershell
$env:API_TOKEN = "<generated-secret>"
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

The service **refuses to start** without `API_TOKEN`. `GET /healthz` is
unauthenticated (load-balancer probe). `POST /validate` requires
`Authorization: Bearer <API_TOKEN>` and accepts a single PDF as multipart
form-data. OpenAPI at `/docs` while running.

### Daily checks

| Check | How | Threshold |
|---|---|---|
| Audit log is being written | `python -m src.audit_report --last 20` | New entries since last run |
| Cost is on track | `python -m src.cost_report` | Within monthly target in SLA.md |
| Cache hit rate is healthy | Same `cost_report` output, "From cache" line | ≥ 50% on a repeat workload |
| API key is still valid | One sample CLI run on `examples/MAC-LIBDM-XX-00-DR-A-001_P01.pdf` | Exits 0 with a Silver report |

## Where things live

| Path | Purpose | Retention |
|---|---|---|
| `.cache/content-validator/` | Document-level result cache, keyed by PDF SHA-256 + rubric/model fingerprint | Keep until rubric or model changes; safe to delete to force fresh validation |
| `.audit/validations.jsonl` | Append-only audit trail (one JSON line per validation) | Keep — this is the audit record |
| `compliance-report.html` / `.json` | Default output of batch runs | Per-run artifact; overwrite or rename |
| `.env` | Local secrets (`ANTHROPIC_API_KEY`, `API_TOKEN`, `CLAUDE_MODEL`) | Never commit. Rotate on key compromise |
| `examples/` | Two demo PDFs (one compliant, one not) | Source-controlled fixtures, don't edit |

All three runtime directories (`.cache/`, `.audit/`, generated reports) are
gitignored.

## Common failures and fixes

### `httpx.ConnectError` / `SSL: CERTIFICATE_VERIFY_FAILED` on a Mace machine

**Cause:** Corporate TLS-intercepting proxy. Python's bundled cert store
doesn't trust the proxy's CA.

**Fix:** Already wired in — `truststore.inject_into_ssl()` runs at startup in
both `check_compliance.py` and `src/api/main.py`. If you still see this:
1. Confirm `truststore` is installed in the active venv: `pip show truststore`.
2. Confirm the machine actually trusts the proxy CA at the OS level (Settings → Manage user certificates → it should be in *Trusted Root Certification Authorities*).
3. Last resort: set `ANTHROPIC_BASE_URL` to the Mace API proxy
   (`https://api.stephen8n.com`) — see FAQ.md.

### `anthropic.AuthenticationError` / 401 from the Anthropic API

**Cause:** `ANTHROPIC_API_KEY` missing, expired, revoked, or has no quota.

**Fix:**
1. Check `.env` has the key (no quotes, no trailing whitespace).
2. Confirm the key still works:
   `python -c "import anthropic; print(anthropic.Anthropic().models.list().data[0].id)"`.
3. If it's an org key that's been rotated, generate a new one at
   console.anthropic.com (off the Mace network) and update `.env`.

### `400 Bad Request` from Claude with mention of `thinking` or `temperature`

**Cause:** The chosen model rejects a parameter the validator sent. Haiku
4.5 doesn't support adaptive thinking; Opus 4.7 rejects `temperature` /
`top_p` / `budget_tokens`.

**Fix:** Already handled in `src/validators/content_validator.py` —
`call_claude` omits `thinking` for models that don't support it. If you've
pinned an older model in `CLAUDE_MODEL`, switch back to `claude-sonnet-4-6`
or `claude-haiku-4-5`. If a future Anthropic change breaks the request
shape, see `shared/model-migration.md` in the Claude API skill and update
`content_validator.py`.

### Validation results look wrong on a document you trust is compliant

**Workflow:** False-positive escalation in `GOVERNANCE.md`. Briefly: capture
the audit entry (`doc_hash` is the key), file an issue with the reviewer's
justification, and either tweak the rubric (PR through the rubric-change
workflow) or add a documented exception. **Don't silently override.**

### API service won't start: `RuntimeError: API_TOKEN environment variable is required`

**Cause:** Working as designed — refusing to expose `/validate` without auth.

**Fix:** Generate a token (`python -c "import secrets; print(secrets.token_urlsafe(32))"`),
set it in the shell, restart. Distribute the token to authorised clients
out-of-band — never commit it.

### Cache directory looks corrupted (JSON decode errors on validation)

**Cause:** Truncated write, manually edited cache file, or a partial sync
from another machine.

**Fix:** Cache is fully regeneratable.
```powershell
Remove-Item -Recurse -Force .cache
python check_compliance.py path\to\doc.pdf  # repopulates as needed
```

### Audit log writes silently dropped

**Behaviour:** `src/runner.py` swallows `OSError` on audit-write —
validation must never break because of an audit failure.

**Diagnose:** If `python -m src.audit_report` shows fewer entries than runs:
1. Check `.audit/` directory permissions.
2. Check disk space.
3. Check the audit dir hasn't been gitignored *and* removed (`.audit/` is
   gitignored, that's expected).
4. Try a manual write: `New-Item .audit\test.txt -ItemType File`. If that
   fails, the OS is the problem.

### Windows: emoji / box-drawing characters render as `?` or crash with `UnicodeEncodeError`

**Cause:** Console codepage isn't UTF-8.

**Fix:** Already wired in — `check_compliance.py` reconfigures stdout/stderr
to UTF-8 with `errors="replace"`. If it still happens, you're probably in
an environment where `sys.stdout.reconfigure` doesn't exist (rare). Set
`PYTHONIOENCODING=utf-8` in the environment before launching.

## Deployment model

Hackathon stage: this is **not a 24/7 service**. There is no production
hosting. Realistic deployment shapes:

1. **CLI on operator's laptop.** Default. `.env` is local, results are
   local, audit is local. Best for ad-hoc validation.
2. **HTTP service on operator's laptop, exposed to a small team.** Bind
   `0.0.0.0`, port-forward or share over Tailscale, distribute the
   `API_TOKEN` to the team. Best for "validate before checking in".
3. **HTTP service on a small VM / container in a department-owned
   environment.** Same Uvicorn command behind a reverse proxy. This is the
   target shape if a department adopts the tool — see *Promotion path*
   below.

### Promotion path (hackathon → department-owned)

When a department wants to keep using this past the hackathon:
1. Fork into the department's GitHub org. Update `GOVERNANCE.md` ownership
   table.
2. Move secrets out of `.env` into the department's secret manager
   (Azure Key Vault, AWS Secrets Manager, 1Password Connect — whatever the
   team already uses).
3. Pin a Python version and lock dependencies (`pip-compile` or `uv pip
   compile` against `requirements.txt`).
4. Containerise: `python:3.11-slim` base, `pip install -r requirements.txt`,
   `CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]`.
5. Set up the rubric-change workflow per `GOVERNANCE.md` (PRs, sign-off,
   `rubric/YYYY-MM-DD` git tags).
6. Define real SLA targets in `SLA.md` (hackathon defaults are placeholders
   for a one-developer-on-a-laptop deployment).

## Rotation and patching

| What | Cadence | Procedure |
|---|---|---|
| `ANTHROPIC_API_KEY` | On compromise, on team change, otherwise annually | Generate new key → update `.env` → smoke test → revoke old key in console |
| `API_TOKEN` | On compromise, on team change, otherwise quarterly | Generate (`secrets.token_urlsafe(32)`) → restart service → distribute to authorised clients |
| `requirements.txt` | Monthly or on advisory | `pip list --outdated`, bump, run full pytest, commit |
| `CLAUDE_MODEL` | When Anthropic deprecates the current default | Follow `shared/model-migration.md` from the Claude API skill |
| The rubric (`iso_19650_rubric.md`) | Per `GOVERNANCE.md` change workflow | PR with reviewer sign-off, `rubric/YYYY-MM-DD` tag |

## Escalation

| Severity | Example | Who | How |
|---|---|---|---|
| P0 — tool produces wrong answers in production | False pass on a known non-compliant document | Operator → Domain reviewer → Maintainer | Slack `#technical-help`; capture `doc_hash` from audit |
| P1 — service down for users | API 5xx, can't validate at all | Operator → Maintainer | Slack `#technical-help`; check `/healthz`, restart |
| P2 — degraded but workable | One model variant 400ing, others fine | Operator → Maintainer | Slack `#technical-help`; switch `--model` until fixed |
| P3 — known false positive | Reviewer disagrees with a flag | Operator → Domain reviewer | False-positive workflow in `GOVERNANCE.md` |

Hackathon support hours are best-effort. Post-hackathon hours are set by
the adopting department — see `SLA.md`.

## Smoke test (after any change)

```powershell
.\venv\Scripts\activate
python -m pytest -x --tb=short
python check_compliance.py examples\MAC-LIBDM-XX-00-DR-A-001_P01.pdf
python -m src.audit_report --last 1
python -m src.cost_report
```

All four must succeed before declaring the change safe to use.
