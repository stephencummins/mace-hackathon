# M+AI+CE Hackathon — FAQ

## General

**What is M+AI+CE?**
M+AI+CE is a Mace hackathon where teams build AI-powered document validators using Anthropic's Claude API. Participants pick a document type their department works with — quality manuals, RAMS, bid responses, contracts, BIM files, HR policy, finance reports — and build a tool that checks documents automatically against the rules that matter for that document type.

**Who can participate?**
Anyone at Mace. No prior AI or coding experience is required — the Claude CLI means you can build a working tool by describing what you want in plain English.

**What do I actually build?**
A Python command-line tool that takes a document as input and produces a structured validation report. Three tiers of increasing complexity:
- **Bronze** — structural checks: naming conventions, required fields, file metadata (no AI involved)
- **Silver** — AI content analysis: Claude reads the document and checks whether the content meets defined rules
- **Gold** — a full validation suite: batch processing, a dashboard, auto-correction suggestions

**Do I need to be a developer?**
No. The Claude CLI lets you describe what you want and it writes the code. Bronze to Silver is achievable in a day with no prior coding experience.

**Can I work in a team?**
Yes. Form a team on the hackathon dashboard at hackathon.stephen8n.com/p/mace. One person per team sets up the Anthropic account and shares the API key with teammates.

**How are submissions judged?**
- Functionality — 40%
- Innovation — 30%
- Code quality — 20%
- Presentation — 10%

**Where do I go if something isn't working?**
Slack `#technical-help` at maice-workspace.slack.com.

---

## Technical

**What do I need to install?**
Three things, none of which require admin rights:
1. Python 3.11+ — python.org/downloads/windows
2. Git for Windows — git-scm.com/download/win
3. Claude CLI — docs.anthropic.com/en/docs/claude-code (native installer, no Node.js needed)

**What is the Claude CLI?**
Claude Code is Anthropic's AI coding assistant. You run it in a terminal inside your project folder and describe what you want to build. It reads your code, writes new code, runs tests, and iterates — like pair programming with an AI.

**What is an Anthropic API key?**
A personal credential that lets your code call Claude. Each participant creates their own free account at console.anthropic.com and generates a key. New accounts include free credits sufficient for the hackathon.

**Why do I need my own Anthropic account rather than a shared one?**
Anthropic's terms require each key to correspond to an individual account. Using separate accounts also means each participant's usage is isolated — one person's activity can't affect another's.

**Why do I set `ANTHROPIC_BASE_URL` to `api.stephen8n.com`?**
Mace's network filters block `api.anthropic.com` directly. The hackathon provides a pass-through proxy at `api.stephen8n.com` that routes API calls to Anthropic on your behalf. See the Security section below for what this does and doesn't do.

**Do I need to create my API key on the Mace network?**
No — and you can't. The Anthropic console (`console.anthropic.com`) is also blocked. Create your account and API key before the hackathon day, on home Wi-Fi or a phone hotspot. It takes two minutes and you only do it once.

**I'm getting `SSL: CERTIFICATE_VERIFY_FAILED` errors when running the validator on the Mace network. What's going on?**
Mace's network intercepts HTTPS traffic with a self-signed corporate certificate. Windows tools (PowerShell, browsers, the Claude CLI) trust this certificate via the system cert store, but Python's bundled `certifi` does not. The `truststore` package in `requirements.txt` patches Python's SSL module to use the OS cert store, which resolves the error. `check_compliance.py` calls `truststore.inject_into_ssl()` at startup automatically — if you write standalone scripts that talk to the API, do the same near the top of the file (before any HTTPS client is constructed).

**Which Claude model should I use?**
The validator defaults to **`claude-sonnet-4-6`** — good balance of quality and cost for a ~12-criterion compliance rubric. Switch with `--model` (CLI alias `haiku` / `sonnet` / `opus`, or a full model id) or via the `CLAUDE_MODEL` env var. Rule of thumb: **Haiku 4.5** when iterating on the rubric or grading high volumes where you can tolerate occasional miss-grading (~$0.001 per doc). **Sonnet 4.6** as the default — what you'll demo and ship with (~$0.003 per doc on our placeholder fixture). **Opus 4.7** when you want the highest quality run, e.g. before signing off on a release (~$0.005 per doc). The document cache makes the model choice a one-time cost per (document, rubric, model) tuple, so switching to Opus for a final pass is cheap if most docs are unchanged.

**How much will this cost?**
Most of the cost is output tokens (the findings + suggested fixes). At Sonnet 4.6 rates ($3 / $15 per million input/output), a typical Bronze+Silver run on a real BIM document is around **$0.003–$0.01 per doc**. Run `python -m src.cost_report` against your populated `.cache/content-validator/` to get a real corpus-driven breakdown: per-model totals, monthly projection at your expected volume, and ROI versus a manual reviewer at a configurable hourly rate. Cache hits cost $0 (no API call), so re-validation of unchanged documents is free.

**Where's the audit trail for validations?**
Every CLI and API validation appends one JSONL line to `.audit/validations.jsonl` (gitignored). Each line records a timestamp, the source (`cli` / `api`), the principal (OS user for CLI, a SHA-256 prefix of the bearer token for API — never the raw token), the document name + content hash, the model, whether the result came from cache, the finding counts, and the dollar cost. Inspect with `python -m src.audit_report` (filters available: `--last N`, `--source`, `--principal`). The full process — ownership, access policy, rubric-change workflow, false-positive escalation — is documented in `GOVERNANCE.md` at the repo root.

**How do I run the validator as an HTTP service?**
Gold tier ships a small FastAPI service that wraps the same Bronze + Silver checks the CLI runs. Set `API_TOKEN` in your `.env` (the server refuses to start without it), then run `uvicorn src.api.main:app --reload`. Send a PDF to `POST /validate` as `multipart/form-data` with `Authorization: Bearer <API_TOKEN>`; the response is the same JSON the CLI emits with `--format json`. Full curl + PowerShell snippets are in `examples/api_curl.md`, and the OpenAPI docs are at `http://127.0.0.1:8000/docs` while the server is running.

**Should I use a personal or Mace GitHub account?**
For the hackathon, use a personal GitHub account. The challenge repo is public and no sensitive Mace code or data is being committed, so there's no need to involve IT. If you don't have one, create a free account at github.com — you can register with your personal or Mace email address.

**What if Mace adopts GitHub more formally after the hackathon?**
If the hackathon generates appetite for AI-assisted development at Mace, the natural next step is a GitHub Enterprise organisation tied to Mace's Azure Active Directory / Entra ID. That gives IT central control — staff sign in with their `@macegroup.com` credentials, access is managed automatically when people join or leave, and private repos stay within the organisation. For now though, personal accounts get you through the day without any IT dependency.

---

## Security

**What data leaves the Mace network during the hackathon?**
When you run the validator against a document, the document content is sent to Anthropic's API over HTTPS. No document content is stored on the hackathon platform (hackathon.stephen8n.com) — it only records your name, progress through the setup steps, and team membership.

**Who can see our API calls?**
Anthropic receives the content of each API request under their standard API terms. The hackathon proxy (`api.stephen8n.com`) is a pass-through — it forwards requests without logging or storing request bodies. Stephen Cummins operates the proxy and can see request metadata (timestamp, size, response code) in Cloudflare logs, but not the content of documents.

**Does Anthropic use our documents to train its models?**
No. Anthropic's API terms explicitly state that inputs and outputs via the API are not used to train models. This is a key difference from consumer products (claude.ai) where usage may inform training. The API is designed for business use and carries stronger data handling commitments. See: anthropic.com/legal/privacy

**Should we use sensitive or confidential documents?**
For the hackathon, use test documents or publicly available examples wherever possible. The worked example in the repo uses BIM document naming conventions with no project-sensitive content. If your team's chosen document type involves confidential data, build the validator using anonymised or synthetic examples — the validator logic is what's being judged, not the real documents.

**Is the hackathon platform itself secure?**
Yes. hackathon.stephen8n.com is:
- Served over HTTPS via Cloudflare
- Authentication via Google SSO — no passwords stored
- Hosted on infrastructure already used for other Mace-adjacent tools

**Who is responsible for API costs?**
Each participant's API key is billed to their own Anthropic account. New accounts include free credits that comfortably cover a day's hackathon use. There is no shared billing that could expose Mace to unexpected costs.

**Is this compliant with Mace's data policies?**
The hackathon is designed to avoid handling production or sensitive data. Participants are advised to use test documents only. If your team has questions about a specific document type, raise them in Slack `#technical-help` before the event.

**Does this comply with Anthropic's Terms of Service?**
Yes. Each participant operates their own account under Anthropic's standard API (Commercial) Terms of Service. The proxy is a transparent pass-through and does not circumvent billing, resell access, or share credentials — all of which are prohibited. Using a reverse proxy for network routing is standard practice and explicitly supported by Anthropic (the `ANTHROPIC_BASE_URL` environment variable exists for exactly this purpose).

---

## On the day

**What's the rough schedule?**
Timings will be posted in Slack `#announcements`. Budget: ~30 min setup, then building all day, presentations in the afternoon.

**What if my API key stops working?**
Check it's active in the Anthropic console (on your phone or home network). Free-tier credits should be more than sufficient for a day's use — if you're hitting limits, raise it in `#technical-help`.

**What if I can't clone the repo?**
Check `github.com` is reachable on the Mace network (`curl -I https://github.com` in PowerShell). If it's blocked, ask in `#technical-help` — we have a fallback.

**Questions not covered here?**
Ask in Slack `#technical-help` or `#registration`.
