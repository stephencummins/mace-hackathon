# M+AI+CE Hackathon — Registration & Setup Guide

Registration and onboarding for M+AI+CE happen on the **hackathon site**, not in
this repository. This repo is the *challenge code* you build in once you're
registered.

## 🚪 Step 1: Register on the M+AI+CE site

👉 **https://hackathon.stephen8n.com/p/mace**

1. Open the site and click **"Sign In to Begin"**.
2. The site walks you through the getting-started flow: connecting your Claude,
   GitHub, and Google accounts, obtaining a Claude API key, and tracking your
   progress.
3. Completing sign-in *is* your registration — there is no separate form to
   email or post in Slack.

## 🪟 Prerequisites — install these first (Windows)

The challenge is a Python project you build with the Claude CLI. On a fresh
Windows machine, install these **before Step 4**:

1. **Python for Windows (3.11+)** — https://www.python.org/downloads/windows/
   Tick **"Add python.exe to PATH"** during install. Verify in a new terminal:
   `python --version`.
2. **Git for Windows** — https://git-scm.com/download/win
   Needed to clone the repo. Verify: `git --version`.
3. **GitHub account** — https://github.com/signup (also in Step 2; required
   for the challenge code and submissions).
4. **Claude CLI (Claude Code) for Windows** — the AI coding tool you build with:
   - Download and run the native Windows installer (no Node.js required):
     https://docs.anthropic.com/en/docs/claude-code
   - Verify: `claude --version`.

## 🧰 Step 2: Accounts you'll need

The site will prompt you for these; create them first if you don't have them:

- **Google account** — used to sign in to the others: https://accounts.google.com/
- **GitHub account** — for the challenge code and submissions: https://github.com/signup
- **Anthropic (Claude) account** — for the Claude API: https://console.anthropic.com/

### Claude API key

1. Go to https://console.anthropic.com/ → **API Keys**.
2. **Create Key**, name it `MAICE Hackathon`.
3. Copy it somewhere safe — you'll put it in your `.env` (Step 4).

### On Mace's network
`api.anthropic.com` is blocked on the Mace corporate network. Set these two variables so your code and the Claude CLI route via the hackathon proxy.

Add to your `.env` in Step 4:
```
ANTHROPIC_BASE_URL=https://api.stephen8n.com
ANTHROPIC_API_KEY=sk-ant-...   # your key from above
```

To cover the Claude CLI too, set them in PowerShell before running `claude`:
```powershell
$env:ANTHROPIC_BASE_URL = "https://api.stephen8n.com"
$env:ANTHROPIC_API_KEY = "sk-ant-..."   # paste your key from Step 2
```

Then run `claude` — you should be connected without needing to authenticate via a browser.

## 💬 Step 3: Join the community

- **Slack**: https://maice-workspace.slack.com — introductions, announcements,
  `#technical-help`, `#team-formation`.

## 💻 Step 4: Get the challenge code

```bash
git clone https://github.com/stephencummins/mace-hackathon.git
cd mace-hackathon

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env — on Mace's network set BOTH of these:
# ANTHROPIC_BASE_URL=https://api.stephen8n.com
# ANTHROPIC_API_KEY=sk-ant-...   (your key from Step 2)
```

Verify:

```bash
python check_compliance.py --help
```

## 🎯 Step 5: Start building — your first hour after cloning

> **New to Claude Code?** Optional crash-courses (free, with completion
> certificates) on [Anthropic Academy](https://anthropic.skilljar.com) —
> *Claude Code 101* (~1 hr) is the natural starting point. Full list in
> [HACKATHON.md → Train & Certify](HACKATHON.md).

```bash
# 1) Verify the harness runs
python check_compliance.py --help

# 2) Try it against a provided example (the stub returns placeholder output
#    until you implement the real validators — that's the challenge)
python check_compliance.py examples/MAC-LIBDM-XX-00-DR-A-001_P01.pdf

# 3) Drop into Claude inside the repo
claude
```

Then ask Claude to scaffold Bronze. A good starter prompt to paste:

> Implement Bronze-level validation for **my chosen domain**: <name the
> document type your team works with — BIM, quality manual, bid response,
> RAMS, contract, finance document, HR policy, planning submission, etc.>
> Define the naming / reference pattern that's valid for it, then write
> `src/validators/naming_validator.py` to check a filename against that
> pattern. Wire it into `check_compliance.py` so the result appears in the
> validation table. Add a unit test under `tests/`.
>
> *Worked example to copy if you want: BIM / ISO 19650 — pattern
> `PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-CLASSIFICATION-NUMBER_REVISION`,
> fixtures in `examples/`.*

Iterate until your own compliant/non‑compliant fixtures behave correctly
(or, for the BIM worked example, until
`examples/MAC-LIBDM-XX-00-DR-A-001_P01.pdf` passes and
`examples/floor plan ground.pdf` fails). Then:

1. Move on to **Silver** (AI content analysis) or **Gold** (full suite) — see
   the Challenge Tasks in [README.md](README.md).
2. Read [HACKATHON.md](HACKATHON.md) for rules + judging.
3. Fork the repo, work on a branch, push, and submit via pull request or demo.

## 🆘 Troubleshooting

**Can't sign in on the hackathon site** — use the same Google account across
Claude/GitHub; ask in Slack `#technical-help`.

**Claude API key not working** — confirm you copied the whole key with no
spaces and that it's active in the Anthropic console.

**Claude API calls failing on Mace network** —  is blocked. Ensure both  and  are set in your  and loaded in your shell ( then  on bash/zsh, or set them in PowerShell directly).

**Claude API calls failing on Mace network** — `api.anthropic.com` is blocked. Make sure both `ANTHROPIC_BASE_URL=https://api.stephen8n.com` and `ANTHROPIC_API_KEY=...` are set in your `.env` and active in your shell.

**Python dependencies won't install** — use Python 3.11+ and upgrade pip:
`pip install --upgrade pip`.

### Getting help

- **Slack**: `#technical-help` at https://maice-workspace.slack.com
- **GitHub**: open an issue with the `question` label

## 📅 Important dates

Registration open, kickoff, submission deadline, and winners are announced on
the hackathon site and in Slack `#announcements`.

---

**Questions?** Ask in Slack `#registration`, or see [HACKATHON.md](HACKATHON.md).

**Good luck and happy hacking!** 🚀
