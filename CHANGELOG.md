# Changelog

All notable changes to the Mace Digital Compliance Checker are recorded here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The project is
hackathon-stage and has not cut a numbered release yet — entries are grouped by tier
(Bronze → Silver → Gold → Platinum) rather than by semver. Dates are the date the
relevant work landed on `main`.

## How this file is maintained

- Every PR that lands on `main` adds (or updates) an entry under the right tier.
- The PR's own commit is the source of truth — write the changelog entry from the
  commit message, not the other way round.
- Group entries under **Added** / **Changed** / **Fixed** / **Removed** / **Security**.
- Cross-reference the commit hash so a reader can `git show <hash>` to see the diff.
- Once the tool leaves hackathon stage and adopts semver, tag `v0.1.0` against the
  current tip and split this file by version from that point on.

## Service-management — 2026-06-10

### Added

- Platinum PR 4: service management — runbook, SLA, onboarding, and this changelog
  process. Closes the last item on the Platinum rubric. (this commit)

## Platinum tier — 2026-05-29 → 2026-06-10

Operational readiness layer on top of the working Gold validator: caching, cost
analysis, audit trail, and the governance/service-management paperwork an
adopting team needs to actually run this.

### Added

- **Platinum PR 3** — validation audit trail and governance. `src/audit.py`
  appends one JSONL line per validation to `.audit/validations.jsonl` (CLI
  attributes via OS user; API attributes via SHA-256-hashed bearer token —
  raw token is never logged). `src/audit_report.py` reads it back with
  `--last / --source / --principal` filters. `GOVERNANCE.md` documents
  ownership, access control, the audit-trail spec, rubric-change workflow,
  and false-positive escalation. (`fa3ad7f`)
- **Platinum PR 2** — cost analysis and inference economics. `src/cost.py`
  applies Anthropic's 4-component pricing formula (input, output, cache
  write at 1.25×, cache read at 0.1×) across Opus 4.7/4.6, Sonnet 4.6, and
  Haiku 4.5. `src/cost_report.py` aggregates `.cache/` into a Markdown
  report with per-model totals, monthly projection at a configurable
  volume, and ROI vs manual review. `check_compliance.py` gains
  `--model haiku|sonnet|opus`. (`aa502ae`, `1efd583`)
- **Platinum PR 1** — document-level cache with measurable token savings.
  `src/cache.py` keys on SHA-256 of PDF bytes plus rubric/model fingerprint;
  cache hits are $0 (no API call). `DocReport` now carries `from_cache` and
  `usage` on both fresh and cache-hit paths. (`09c3eea`)
- Initial Platinum scaffolding — operations, cost, caching, governance,
  service-management section in `HACKATHON.md`. (`58f4309`)

### Fixed

- Haiku 4.5 no longer 400s on content validation: `call_claude` omits the
  `thinking` parameter for models that don't support adaptive thinking.
  (`aa502ae`)

## Gold tier — 2026-05-28 → 2026-06-01

A complete, deployable product: batch validation, multiple report formats,
auto-correction suggestions, and an HTTP API.

### Added

- **Gold PR 3** — real-time validation HTTP API. FastAPI service at
  `src.api.main:app`. `POST /validate` accepts multipart PDF upload and
  returns the same JSON as the CLI's `--format json`. Bearer-token auth via
  `API_TOKEN`; server refuses to start without it. `GET /healthz` is
  unauthenticated for load balancers. (`04ad736`)
- **Gold PR 2** — auto-correction suggestions for content findings. Claude
  proposes concrete edits, not just flags problems. (`1332cbe`)
- **Gold PR 1** — batch validation (`src/runner.py`) plus HTML and JSON
  report formats (`src/reports/`). `check_compliance.py` accepts directories
  and globs; reports are written to `compliance-report.{html,json}` by
  default. (`374ee30`)

## Silver tier — 2026-05-28

AI-powered content analysis: Claude reads the document and checks whether
the content actually complies, beyond filename/metadata structure.

### Added

- Silver content validator using Claude. Calls the Messages API with the
  ISO 19650 rubric and returns structured findings (pass / fail / warning
  with explanations). (`f618448`)

### Fixed

- Use OS cert store via `truststore` so Python works on the Mace network
  (corporate TLS-intercepting proxy). Without this, `httpx` rejects the
  proxy's cert chain and every API call fails. (`1073bb8`, merged `799b02d`)

## Bronze tier — 2026-05-23

Structural validation: pure pattern matching, no AI required. Everyone can
ship Bronze in the first hour.

### Added

- ISO 19650 naming validator wired into the CLI. Pattern:
  `PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-NUMBER_REVISION`. (`2ca5da2`)

### Fixed

- Naming pattern: 7 fields, not 8 — `CLASSIFICATION` removed to match the
  shipped fixtures. (`418fa45`, `3c88a95`)
- Windows Unicode crash: reconfigure stdout/stderr to UTF-8 so the rich
  console output's glyphs render without exploding under cp1252. (`ac0a913`)

## Pre-Bronze hackathon scaffolding — 2026-01-13 → 2026-05-23

Everything that makes the hackathon itself runnable: the challenge brief,
participant onboarding, network setup for the Mace corporate environment,
and the FAQ.

### Added

- Plain-English rewrites of `HACKATHON.md` and `REGISTRATION.md`. (`dad2bf3`,
  `af2a0ac`, `ad6ffac`, `a84143b`, `9852d49`)
- Participant welcome greeting in `CLAUDE.md` first-interaction guidance.
  (`a84143b`)
- FAQ covering general, technical, and security questions plus GitHub
  personal-vs-work account guidance. (`20f9093`, `d0ae00d`)
- Mace network proxy setup: `ANTHROPIC_BASE_URL` via `api.stephen8n.com`
  with exact PowerShell env-var lines. Warning that `console.anthropic.com`
  must be done off the Mace network. (`e78e179`, `39de0e2`, `7705f39`)
- Windows prerequisites (Python, Git, Claude CLI). Node.js prereq removed
  once the bundled-Node Claude CLI shipped. (`7c9aee6`, `31a570f`)
- "First hour after cloning" walkthrough plus runnable example PDFs (one
  ISO 19650 compliant, one not). (`a0c07b8`, `d375938`)
- Train & Certify section pointing at Anthropic Academy. (`574a82a`)
- Challenge broadened to any-team document validation, not BIM-only. The
  HR worked example was added then removed — staying with one canonical
  ISO 19650 example. (`071f775`, `8f5b8a9`, `bb3c627`)
- Repo renamed to `mace-hackathon`; self-references updated. (`0c87856`)
- Self-hosted registration platform (migrated off Manus). (`4406ce1`)
- Initial hackathon documentation: README, HACKATHON, CLAUDE, banner.
  (`9db366c`, `8a15cba`, `98b8442`, `267b38c`, `8b8a63a`)
