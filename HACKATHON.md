# M+AI+CE: The Hackathon

You describe your document rules. The AI writes the code that enforces them.

Open to every team across Mace — no coding experience required.

## What you're building

Pick a document type your team works with every day. It could be anything — BIM files, quality manuals, RAMS, bid responses, contracts, finance reports, HR policies, planning submissions. You're going to build a tool that checks whether those documents are correctly formatted and complete.

The repo ships a working example for BIM / ISO 19650 documents. If that's your domain, you can run it straight away.

## Register

👉 **[hackathon.stephen8n.com/p/mace](https://hackathon.stephen8n.com/p/mace)**

Sign in with your Google account. That's your registration — no form to fill in.

## What you need before the day

**Three things to install on your Windows laptop** (no admin rights needed):
1. **Python** — python.org/downloads/windows — tick "Add python.exe to PATH" during install
2. **Git for Windows** — git-scm.com/download/win
3. **Claude AI coding tool** — docs.anthropic.com/en/docs/claude-code

**One thing to do at home** (the Anthropic website is blocked on Mace's network):
- Create a free account at **console.anthropic.com** and generate an API key. Name it "MAICE Hackathon". Copy it somewhere safe.

Full setup walkthrough: [REGISTRATION.md](REGISTRATION.md)

## The four levels

### 🥉 Bronze — does the document *look* right?
**No AI involved. Pure pattern matching — everyone can get here in the first hour.**

Check whether a document's filename and structure follow the right format. For BIM: does the filename match `PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-NUMBER_REVISION`? For your domain: does it follow whatever naming convention your team uses?

### 🥈 Silver — does the document *say* the right things?
**This is where Claude reads the document and checks the content.**

Claude opens the document and checks whether it actually contains what it should — required clauses, complete data, consistent dates, no missing sections.

### 🥇 Gold — a tool your team could actually use
**A complete, deployable product.**

Batch checking across multiple documents, a results dashboard, suggested corrections, integration with SharePoint or your document library.

### 💎 Platinum — a solution your organisation can own
**Beyond shipping — thinking about the full lifecycle.**

You've built the tool. Now document how it lives in the real world:

- **Operations & maintenance**: Deployment model, update process, dependency management — and who owns it after the hackathon.
- **Inference economics**: Choose the right model for each task — Haiku for structural/deterministic checks, Sonnet where deep reasoning is needed. Optimise prompt length, minimise output tokens, and batch calls where possible. Understand Anthropic's cost model: input vs output pricing, cache write vs cache read rates.
- **Cost management**: Analyse token usage per document type and scenario. What does validation cost at realistic monthly volumes? What's the ROI versus manual review?
- **Caching strategy**: Reduce redundant API calls — document fingerprinting to skip re-validation, result caching, Anthropic prompt caching headers. Show measurable token savings.
- **Governance**: Who approves changes to the validation rules? Who has access to the tool and its outputs? How are false positives handled and escalated? What's the audit trail?
- **Service management**: A support runbook, a defined SLA (uptime, latency, accuracy targets), onboarding documentation for new users and new document types, and a changelog process.

## How judging works

| Criteria | Weight |
|----------|--------|
| Does it work? | 40% |
| Is it creative and well thought through? | 30% |
| Is the code clean and well documented? | 20% |
| How well do you present it? | 10% |

## Community

Join Slack: **[maice-workspace.slack.com](https://maice-workspace.slack.com)**
- `#technical-help` — if something isn't working
- `#team-formation` — find teammates
- `#announcements` — dates and updates

## Train & Certify

[Anthropic Academy](https://anthropic.skilljar.com) has free courses with completion certificates:
- **Claude Code 101** — about 1 hour, good starting point if you've never used Claude Code before
- **Claude Code in Action** — goes deeper into getting the best results

## Submitting

Bring a working demo on the day. Details posted in Slack `#announcements` closer to the time.

## Tips

- **You don't need to know how to code.** Describe what you want in plain English and Claude writes it.
- **Start with Bronze.** Everyone can get a working validator in the first hour.
- **Use test documents**, not sensitive real ones.
- **Ask for help early.** Slack `#technical-help` is there for a reason.

## Questions?

Ask in Slack `#registration` or raise your hand on the day.
