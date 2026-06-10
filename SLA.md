# Service Level Agreement

Operational targets for the Mace Digital Compliance Checker. **Hackathon-stage
numbers** — set with the realistic deployment shape (CLI on an operator's
laptop, or a small HTTP service inside one department) in mind. When a
department promotes this tool to production they should rewrite this file
against the SLA their users actually need.

## Scope

Covered by this SLA:

- The **CLI** (`check_compliance.py`).
- The **HTTP API** (`src.api.main:app`) when run by an operator who has
  agreed to these targets.
- The shipped **ISO 19650 rubric** (`src/validators/iso_19650_rubric.md`).
  Custom rubrics inherit the harness's SLA but not its accuracy targets —
  accuracy needs re-measurement when the rubric changes.

Out of scope:

- Anthropic API uptime (depends on platform.claude.com — separate SLA).
- The Mace network proxy (`api.stephen8n.com`) — separate SLA from the
  network team.
- Anything participants build on top during the hackathon.

## Uptime targets

| Surface | Target | Measured how | Honest note |
|---|---|---|---|
| CLI | Best-effort | Operator's machine on, venv intact | A laptop tool; "uptime" really means "you have the code" |
| HTTP API — hackathon deployment | Best-effort during demo + judging window | `GET /healthz` returns 200 | Single Uvicorn process on a developer machine; restart cost ≈ 2s |
| HTTP API — department deployment | **99.5%** monthly (≈ 3h 40min downtime/month) | Reverse-proxy access log + healthz uptime check (e.g. UptimeRobot) | Achievable shape: containerised + systemd / Kubernetes restart-on-failure, dependency on Anthropic |
| Audit log writes | 100% of successful validations produce an audit line | `validations.jsonl` line count == validations run | OS write failures are swallowed, but in practice never happen on local disk |

The 99.5% department target carves out planned maintenance windows
(announced ≥ 24h ahead in Slack `#announcements`) and Anthropic API
outages (we relay; we don't own them).

## Latency targets

Measured end-to-end, single-PDF request.

| Operation | Target | Typical (observed) | What drives it |
|---|---|---|---|
| Bronze (naming validator only) | **< 1s** P95 | ~50 ms | Regex on the filename; no I/O beyond reading the path |
| Silver, cache hit | **< 2s** P95 | ~200 ms | SHA-256 of PDF bytes + JSON read from `.cache/` |
| Silver, cache miss (Haiku) | **< 8s** P95 | 2–4s | One Anthropic API call; depends on Anthropic's response time |
| Silver, cache miss (Sonnet) | **< 15s** P95 | 4–8s | One Anthropic API call; Sonnet is slower than Haiku |
| Silver, cache miss (Opus) | **< 30s** P95 | 8–15s | One Anthropic API call; Opus is the deepest reasoner |
| Batch validation | Sum of per-doc latencies | Runs sequentially today | `src/runner.py` is single-threaded — parallelisation is a future PR |
| `python -m src.audit_report` | **< 2s** for ≤ 10k entries | sub-second | One pass over a JSONL file |
| `python -m src.cost_report` | **< 5s** for ≤ 10k cache entries | sub-second | One pass over `.cache/` |

Latency degrades when:
- The Mace network proxy is slow → add 1–3s.
- Anthropic is degraded → add whatever Anthropic adds; status at
  `status.anthropic.com`.
- Validating very large PDFs (> 50 pages) — the PDF parser dominates.

## Accuracy targets

Accuracy is measured against a labelled fixture set: each document has a
ground-truth pass/fail/warning per criterion, set by the Domain reviewer.

| Tier | Target | Measured against |
|---|---|---|
| Bronze (filename naming) | **100% precision and recall** on the shipped fixtures | `examples/MAC-LIBDM-XX-00-DR-A-001_P01.pdf` (compliant) and the non-compliant counterpart |
| Silver (content) — recall | **≥ 90%** of true findings flagged | Domain-reviewer-labelled fixture set (built up post-hackathon) |
| Silver (content) — precision | **≥ 80%** of flags accepted by the Domain reviewer | Same fixture set; false-positive rate ≤ 20% |
| End-to-end (Bronze + Silver) | **No false passes** on a known non-compliant document | Acceptance gate; treated as P0 if violated (see `RUNBOOK.md` Escalation) |

Honest caveats:

- The fixture set is small at hackathon stage. The targets above are
  reachable but not yet *demonstrated at scale* — adopting the tool means
  agreeing to build the fixture set as part of onboarding (see
  `ONBOARDING.md`).
- Recall and precision drift when the rubric is changed. Re-measure after
  every `rubric/YYYY-MM-DD` tag.
- False positives flow through the workflow in `GOVERNANCE.md` and either
  improve the rubric or become documented exceptions — they're not
  silently overridden.

## Cost targets

Per Platinum PR 2 (`src/cost_report.py`):

| Workload | Target | What it assumes |
|---|---|---|
| Per-document Silver run (Sonnet 4.6) | **≤ $0.01** | Typical BIM PDF, no cache hit |
| Per-document Silver run (Haiku 4.5) | **≤ $0.003** | Typical BIM PDF, no cache hit |
| Cache hit | **$0** | No API call |
| Monthly cap at 1,000 docs / month, Sonnet | **≤ $25** | Assuming ≥ 50% cache hit rate after warm-up |

If `python -m src.cost_report` shows a projection ≥ 2× the target, that's
a P2: the operator should investigate (rubric ballooning, model changed,
cache disabled). Procedure in `RUNBOOK.md`.

## Support hours

| Phase | Hours | Channel | Response target |
|---|---|---|---|
| Hackathon week | Best-effort, demo days especially | Slack `#technical-help` | Acknowledgement during the working day |
| Post-hackathon, no adopter yet | Best-effort, no commitment | Open a GitHub issue | None — community-supported |
| Post-hackathon, adopted by a department | Set by the adopting department | Set by the adopting department | Set by the adopting department |

The hackathon team does not own a 24/7 on-call rota. P0/P1 escalation in
`RUNBOOK.md` reflects best-effort routing during working hours.

## Change management

| Change | Notice | Approval |
|---|---|---|
| Rubric change | Per `GOVERNANCE.md` rubric-change workflow | Product owner sign-off |
| Default model (`CLAUDE_MODEL`) | Note in `CHANGELOG.md` | Maintainer |
| Breaking API change (request/response shape) | Major-bump entry in `CHANGELOG.md` before merging | Maintainer + at least one operator-affected confirmation |
| Dependency upgrade | Entry in `CHANGELOG.md` post-merge | Maintainer (tests must still pass) |

## What this SLA does not cover

- **Document content quality.** The tool finds rubric mismatches; it does
  not author documents. A compliant filename and structure does not make a
  document *good*.
- **Document provenance / integrity.** The tool reads the bytes you give
  it. Validating signatures, watermarks, or chain-of-custody is out of
  scope.
- **PII / classification handling.** Documents sent through Silver are
  processed by Anthropic per their data usage terms — see
  platform.claude.com. Treat the cache and audit directories as the same
  classification as the source documents.
- **Multi-tenancy.** One operator, one `API_TOKEN`. If multiple teams need
  isolated audit/cost trails, deploy multiple instances.

## Acceptance test (does the running deployment meet the SLA?)

A quarterly check the operator should run:

```powershell
# Bronze + Silver acceptance — both must exit 0
python check_compliance.py examples\MAC-LIBDM-XX-00-DR-A-001_P01.pdf --format json
python check_compliance.py examples\non-compliant-fixture.pdf --format json

# Latency sample — record p50/p95 over 20 runs against the fixture
1..20 | ForEach-Object {
  Measure-Command { python check_compliance.py examples\MAC-LIBDM-XX-00-DR-A-001_P01.pdf --format json | Out-Null }
} | Select-Object -ExpandProperty TotalSeconds | Sort-Object

# Cost projection — must be within target
python -m src.cost_report --volume 1000

# Audit trail still being written
python -m src.audit_report --last 5
```

Record results in the team's quarterly review. Anything outside target is
a change-management item, not a silent drift.
