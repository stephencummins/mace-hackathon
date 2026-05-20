# M+AI+CE: The Hackathon

Welcome to **M+AI+CE: The Hackathon** — a web‑based hackathon for building intelligent document validation tools with Claude. Open to every team across Mace: pick a document type that matters to *your* department.

## 🎯 Hackathon Overview

**M+AI+CE** (Mace + AI + Compliance Excellence) challenges every team across the company to build innovative document‑validation tools with Claude — for *any* document type your department uses. The repo ships a worked example for **ISO 19650 (BIM)**, but the same Bronze → Silver → Gold structure applies to quality manuals, RAMS, bid responses, contracts, finance documents, HR policy, planning submissions — anything your team owns.

## 📅 Event Details

- **Register**: 👉 [hackathon.stephen8n.com/p/mace](https://hackathon.stephen8n.com/p/mace) — sign in to begin
- **Format**: Web-based hackathon
- **Focus**: Developer tools for construction document compliance
- **Technology Stack**: Claude AI, Python, GitHub
- **Challenge code**: [mace-hackathon](https://github.com/stephencummins/mace-hackathon)

## 🚀 Getting Started

### Prerequisites

Before participating in the hackathon, you'll need to set up the following accounts and tools:

#### Required Accounts

1. **Google Account**
   - Required for GitHub and Claude authentication
   - Used for Google Developer Console access

2. **GitHub Account**
   - Register using your Google account
   - Required for repository access and collaboration

3. **Claude Account**
   - Register using your Google account
   - Required for AI-powered document analysis

4. **Google Developer Account**
   - Needed for Google authentication integration
   - Access at: [Google Cloud Console](https://console.cloud.google.com/)

#### API Keys

- **Claude API Key**: Required for AI-powered compliance checking
  - Obtain from: [Anthropic Console](https://console.anthropic.com/)
  - Add to your `.env` file as `ANTHROPIC_API_KEY`

#### Required Tools (Windows)

Install before cloning the challenge code — full step-by-step in
[REGISTRATION.md](REGISTRATION.md):

- **Python for Windows 3.11+** — https://www.python.org/downloads/windows/ (tick "Add to PATH")
- **Git for Windows** — https://git-scm.com/download/win
- **Node.js 18+ LTS**, then the **Claude CLI**: `npm install -g @anthropic-ai/claude-code` — https://docs.anthropic.com/en/docs/claude-code

### Registration Process

Registration is handled entirely on the **M+AI+CE site** — there is no form to
email or post in Slack:

1. **Register**
   - Go to **[hackathon.stephen8n.com/p/mace](https://hackathon.stephen8n.com/p/mace)** and click **"Sign In to Begin"**
   - The site walks you through connecting your Claude, GitHub, and Google accounts and obtaining a Claude API key

2. **Get the Challenge Code**
   - Clone this repo: `git clone https://github.com/stephencummins/mace-hackathon.git`

3. **Join the Community**
   - Slack Workspace: [maice-workspace.slack.com](https://maice-workspace.slack.com)
   - Connect with other participants, mentors, and organizers; get real-time support and updates

Full step-by-step setup: see [REGISTRATION.md](REGISTRATION.md).

## 🌐 Hackathon Platform

The hackathon runs on the **M+AI+CE site**
([hackathon.stephen8n.com/p/mace](https://hackathon.stephen8n.com/p/mace)) for:

- Registration and sign-in
- The getting-started flow (accounts + Claude API key)
- Progress tracking and announcements

This **GitHub repository is the challenge code** you build in. Community and
support happen in [Slack](https://maice-workspace.slack.com).

## 🎓 Technical Setup

### 1. Clone the Repository

```bash
git clone https://github.com/stephencummins/mace-hackathon.git
cd mace-hackathon
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your credentials:
# - ANTHROPIC_API_KEY (from Claude Console)
# - GOOGLE_CLIENT_ID (from Google Developer Console)
# - GOOGLE_CLIENT_SECRET (from Google Developer Console)
```

### 4. Google Authentication Setup

For integrating Google authentication in your solution:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Configure the OAuth consent screen
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs
6. Copy Client ID and Client Secret to your `.env` file

## 💻 Challenge Levels

Each tier is generic — substitute the specifics of *your* chosen document type.

### 🥉 Bronze Level: Structural Validation
Validate the *shape* of a document for your domain:
- File naming / reference pattern (e.g. ISO 19650 codes, contract id, SOP number)
- Required metadata fields
- Required sections / structure
- Basic format requirements

### 🥈 Silver Level: AI-Powered Content Analysis
Use Claude to validate *substance*:
- Verify the document contains what your domain requires
- Flag missing mandatory clauses / sections / data
- Flag ambiguous or incomplete content
- Check internal consistency (dates align, references resolve, totals add up)

### 🥇 Gold Level: Full Validation Suite
Production-grade:
- Multi-document batch validation
- Reporting dashboard
- Auto-correction / improvement suggestions
- Integration with SharePoint/Azure
- Real-time validation API

## 🤝 Collaboration & Support

### Slack Workspace

Join our Slack community for:
- **#general**: General discussions and announcements
- **#technical-help**: Get help with technical issues
- **#resources**: Share useful resources and documentation
- **#random**: Off-topic discussions and team building

**Workspace URL**: [https://maice-workspace.slack.com](https://maice-workspace.slack.com)

### GitHub Collaboration

- **Issues**: Report bugs or request features
- **Discussions**: Ask questions and share ideas
- **Pull Requests**: Submit your solutions
- **Wiki**: Access additional documentation

## 📚 Resources

### Essential Documentation

- [ISO 19650 Standards](https://www.iso.org/standard/68078.html)
- [Claude AI Documentation](https://docs.anthropic.com/)
- [UK BIM Framework](https://www.ukbimframework.org/)
- [Google OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)

### 🎓 Train & Certify (optional)

[Anthropic Academy](https://anthropic.skilljar.com) hosts **free, self-paced
courses with completion certificates**. Most relevant for this hackathon:

- **Claude Code 101** — entry level, ~1 hr. The agentic loop, installation,
  the Explore → Plan → Code → Commit workflow.
- **Claude Code in Action** — core tools, context management (`CLAUDE.md`,
  `@`-mentions), Plan / Thinking Mode, custom commands, MCP servers, GitHub
  integration, hooks. Also offered on Coursera.
- **Skills in Claude Code** — building and sharing `SKILL.md`.
- **Sub-agents in Claude Code** — delegation patterns.
- **Building with the Claude API** — 84 lessons, 8+ hours, 10 quizzes if you
  want to go beyond the CLI.

**Suggested path for a structured cohort:** *Claude Code 101* → *Claude Code in
Action* → *Skills* / *Sub-agents*. Completion certificates give participants
something tangible.

**Supporting material:**

- [anthropics/courses](https://github.com/anthropics/courses) — Jupyter
  notebooks for code-along learning.
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) —
  reference implementations.

> **Note:** These are the same Academy materials that feed Anthropic's Claude
> Code certification track — so running through them doubles as cert prep if
> anyone wants to certify later.

### Sample Documents

The repo includes two **filename‑demonstration PDFs** in `examples/` for the
BIM / ISO 19650 worked example:

- `MAC-LIBDM-XX-00-DR-A-001_P01.pdf` — compliant filename
- `floor plan ground.pdf` — non-compliant filename

For your own domain, **create equivalent fixtures**: one filename that follows
your team's pattern, one that doesn't. For Silver/Gold content checks, use a
real document from your department.

## 🏆 Submission Guidelines

### What to Submit

1. **Working Code**
   - Fork the repository
   - Implement your solution
   - Ensure all tests pass

2. **Documentation**
   - README with setup instructions
   - API documentation (if applicable)
   - Architecture overview

3. **Demo**
   - Video demonstration (optional but recommended)
   - Live demo link (if deployed)
   - Screenshots of key features

### Evaluation Criteria

Projects will be evaluated on:

1. **Functionality** (40%)
   - Accuracy of compliance checking
   - Coverage of ISO 19650 requirements
   - Error handling and robustness

2. **Innovation** (30%)
   - Creative use of Claude AI
   - Unique features and approaches
   - User experience design

3. **Code Quality** (20%)
   - Clean, maintainable code
   - Comprehensive documentation
   - Test coverage

4. **Presentation** (10%)
   - Demo quality and clarity
   - Documentation completeness
   - Real-world applicability

## 🎉 Tips for Success

1. **Start Early**: Set up your environment and accounts before the hackathon starts
2. **Join Slack**: Connect with mentors and other participants
3. **Read the Docs**: Familiarize yourself with ISO 19650 requirements
4. **Test with Real Data**: Use actual BIM documents for validation
5. **Iterate Quickly**: Start with Bronze level and build up
6. **Document Everything**: Good documentation is part of the evaluation
7. **Ask Questions**: Use Slack and GitHub Discussions when stuck

## 🔒 Security & Privacy

- Never commit API keys or secrets to the repository
- Use environment variables for sensitive configuration
- Follow GitHub security best practices
- Respect data privacy when handling documents

## 📞 Contact & Support

- **Slack**: [maice-workspace.slack.com](https://maice-workspace.slack.com)
- **GitHub Issues**: [Report issues here](https://github.com/stephencummins/mace-hackathon/issues)
- **Email**: Contact organizers through Slack

## 🌟 Acknowledgments

This hackathon is powered by:
- **Claude AI** by Anthropic
- **GitHub** for collaboration and version control
- **Google Cloud** for authentication services
- **Mace Group** for construction industry expertise

---

**Ready to build something amazing?** Join us on Slack, clone the repository, and start coding!

**#MAICE #Hackathon #ClaudeAI #ISO19650 #BIM #Construction**
