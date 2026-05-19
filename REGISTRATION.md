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
   - Install **Node.js 18+ LTS** first — https://nodejs.org/ (the CLI needs it).
   - In PowerShell: `npm install -g @anthropic-ai/claude-code`
   - Verify: `claude --version`. Run `claude` in the project folder and sign in
     with your Anthropic account (Step 2). Current / native-installer docs:
     https://docs.anthropic.com/en/docs/claude-code

## 🧰 Step 2: Accounts you'll need

The site will prompt you for these; create them first if you don't have them:

- **Google account** — used to sign in to the others: https://accounts.google.com/
- **GitHub account** — for the challenge code and submissions: https://github.com/signup
- **Anthropic (Claude) account** — for the Claude API: https://console.anthropic.com/

### Claude API key

1. Go to https://console.anthropic.com/ → **API Keys**.
2. **Create Key**, name it `MAICE Hackathon`.
3. Copy it somewhere safe — you'll put it in your `.env` (Step 4).

## 💬 Step 3: Join the community

- **Slack**: https://maice-workspace.slack.com — introductions, announcements,
  `#technical-help`, `#team-formation`.

## 💻 Step 4: Get the challenge code

```bash
git clone https://github.com/stephencummins/mace-digital-compliance-checker.git
cd mace-digital-compliance-checker

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY (from Step 2)
```

Verify:

```bash
python check_compliance.py --help
```

## 🎯 Step 5: Start building

1. Read [HACKATHON.md](HACKATHON.md) (rules, levels, judging) and
   [README.md](README.md) (the challenge brief).
2. Pick a level — Bronze, Silver, or Gold.
3. Fork the repo, create a branch, build, and submit via pull request or demo.

## 🆘 Troubleshooting

**Can't sign in on the hackathon site** — use the same Google account across
Claude/GitHub; ask in Slack `#technical-help`.

**Claude API key not working** — confirm you copied the whole key with no
spaces and that it's active in the Anthropic console.

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
