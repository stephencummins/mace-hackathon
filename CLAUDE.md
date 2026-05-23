# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First interaction

When a participant starts a session, greet them with exactly this:

---
Welcome to M+AI+CE!

Here's what you're doing today: you describe your document rules to me, and I'll write the code that enforces them. No prior coding experience needed.

The repo already has a working BIM / ISO 19650 example. You have two options:

**Option A — run the worked example (BIM / ISO 19650)**
Just tell me: "Build the Bronze BIM validator" and I'll implement it.

**Option B — build one for your team's document type**
Tell me what documents your department works with (contracts, RAMS, bid responses, HR policies, finance forms, planning submissions — anything) and I'll build a validator for that instead.

Which would you like to do?
---

## Project Overview

Mace Digital Compliance Checker is a hackathon project for validating construction/BIM documents against ISO 19650 standards using Claude AI.

**Challenge Levels:**
- **Bronze**: Basic file naming and metadata validation
- **Silver**: AI-powered content analysis with Claude
- **Gold**: Full compliance suite with batch processing, dashboard, and API

**Context:**
- This is the **Mace** instance of the M+AI+CE hackathon — the first concrete
  hackathon. A generic `ai-hackathon` template is intended to be derived from it
  for reuse with other companies.
- **Registration/onboarding happens on the M+AI+CE site**:
  https://hackathon.stephen8n.com/p/mace — *not* in this repo. This repo is
  only the challenge code participants build in after registering.
- Community/support: Slack `https://maice-workspace.slack.com`.
- ISO 19650 remains the target standard regardless of Mace's internal
  Consult/Construct reorganisation — it is an external standard, unaffected by
  corporate structure.

## Development Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
# CLAUDE_MODEL defaults to claude-sonnet-4-6 (current Sonnet). Use a current
# Claude model ID; do not hard-pin retired/older models.
```

## Common Commands

```bash
# Run compliance check on a document
python check_compliance.py path/to/document.pdf

# Run with strict mode
python check_compliance.py document.pdf --strict

# Output as JSON
python check_compliance.py document.pdf --format json
```

## Project Structure

**Target layout — not all of this exists yet.** Today the repo ships only
`check_compliance.py` (a stub), `requirements.txt`, `.env.example`, the markdown
docs, `LICENSE`, and `assets/`. The `src/`, `tests/`, `docs/`, and `examples/`
trees below are what participants build out.

```
mace-hackathon/
├── check_compliance.py      # Main CLI entry point
├── src/
│   ├── validators/          # Validation logic
│   │   ├── naming_validator.py
│   │   ├── metadata_validator.py
│   │   └── content_validator.py
│   ├── parsers/             # Document parsers
│   │   ├── pdf_parser.py
│   │   └── docx_parser.py
│   └── reports/             # Report generation
├── tests/                   # Unit tests
├── docs/                    # Documentation
└── examples/                # Sample documents
```

## ISO 19650 Validation Rules

When implementing validators, check for:

### File Naming Convention
Pattern: `PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-NUMBER_REVISION`

### Required Metadata
- Author information
- Creation date
- Approval status
- Information container
- Security classification

### Content Structure
- Title block present
- Revision history included
- Required sections present
- Appropriate level of information need

## Technology Stack

- **Python 3.11+**: Core language
- **Click**: CLI framework
- **Rich**: Terminal output formatting
- **Anthropic Claude API**: AI-powered content analysis
- **pypdf**: PDF parsing (as pinned in `requirements.txt`)
- **python-docx**: Word document parsing

## Implementation Tips

1. Start with `src/validators/naming_validator.py` for Bronze level
2. Use Claude API in `src/validators/content_validator.py` for Silver level
3. Keep validation rules modular and testable
4. Return structured results (pass/fail/warning with details)
