# Mace Digital Compliance Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Claude](https://img.shields.io/badge/AI-Claude-purple.svg)](https://www.anthropic.com/claude)

**Hackathon Challenge**: Build an AI‑powered document validator with Claude — for *any* document type your team works with. The repo ships a worked example for **ISO 19650 / BIM**; swap in your own domain.

> 📢 **New here?** Register on the **M+AI+CE site**: 👉 **[hackathon.stephen8n.com/p/mace](https://hackathon.stephen8n.com/p/mace)**. Then see [REGISTRATION.md](REGISTRATION.md) for setup and [HACKATHON.md](HACKATHON.md) for rules, levels, and judging.

## What you're doing

You're going to describe your document rules to an AI, and it'll write the code that enforces them.

Concretely: you open a terminal, run `claude`, and tell it what a valid document looks like for your team — the naming convention, the required fields, the sections that must be present. Claude writes a Python validator that checks any document against those rules and produces a pass/fail report.

No prior coding experience needed. The AI writes the code. You describe the rules.

The repo ships a working example for BIM documents (ISO 19650 naming conventions). If that's your domain, you can run it straight away. If not, the same approach works for any document type — contracts, RAMS, bid responses, HR policies, finance forms, planning submissions.

## 🎯 Challenge Overview

Pick a document type your team works with — *anything* — and build an
AI‑powered validator with Claude. The **Bronze → Silver → Gold → Platinum**
structure below applies regardless of domain: you bring the rules, Claude
helps you enforce them at scale.

## 🏗️ Worked example: ISO 19650 (BIM)

The starter content and fixtures (`examples/`) in this repo demo the
BIM / ISO 19650 case. ISO 19650 defines how information is managed across
the lifecycle of a built asset:

- **ISO 19650-1** — Concepts and principles
- **ISO 19650-2** — Delivery phase of assets
- **ISO 19650-3** — Operational phase of assets
- **ISO 19650-5** — Security-minded approach

Key requirements: structured information exchange, clear naming
conventions, metadata, delivery milestones, collaboration procedures.

### Other domains to consider

Swap BIM/ISO 19650 for any document type your team owns. A few starting
points:

- **Quality (ISO 9001)** — SOPs, procedure docs, audit reports
- **Health & Safety (ISO 45001)** — RAMS, method statements, safe systems of work
- **Bids & Tenders** — RFP responses, capability statements, PQQ submissions
- **Contracts & Legal** — NDAs, MSAs, change orders, variations
- **Finance** — invoices, expense reports, purchase orders, approval forms
- **HR** — policy documents, job descriptions, performance reviews
- **Project Management** — PIDs, project briefs, status reports, lessons learned
- **Planning Submissions** — planning applications, design & access statements

Use the worked example as a template — replace its filename/structure
rules with whatever pattern matters to *your* team.

## 🚀 Challenge Tasks

Pick a domain (see above), then ladder through four tiers. Each tier is
described generically — substitute the specifics of *your* document type.

> **The shipped worked example already implements all four tiers** for
> ISO 19650. Read the tier checklists below either as the task list for
> your own domain, *or* as a tour of what's already in the repo — every
> tier links to the file(s) that deliver it. The [CHANGELOG](CHANGELOG.md)
> has the full history of how it was built, commit by commit.

### 🥉 Bronze Level: Structural Validation
**No AI required. Pure pattern matching — everyone can ship this in the first hour.**
Build a validator that checks the *shape* of a document:
- [ ] File naming / reference pattern (your domain's convention — e.g. an ISO 19650 code, a contract id like `MSA-<client>-<rev>`, an SOP number like `QMS-001-A`)
- [ ] Required metadata fields (author, dates, version, classification — whatever your domain mandates)
- [ ] Required sections / structure
- [ ] Basic format requirements (file type, page size, etc. if relevant)

### 🥈 Silver Level: AI-Powered Content Analysis
**This is where Claude reads the document and checks whether the content actually complies.**
Enhance with Claude to check the *substance*:
- [ ] Read the document with Claude and verify it contains what your domain requires
- [ ] Check for missing mandatory clauses / sections / data
- [ ] Flag ambiguous, contradictory, or incomplete content
- [ ] Validate internal consistency (dates align, references resolve, totals add up)

### 🥇 Gold Level: Full Validation Suite
**A complete, deployable product your team could actually use.**
Create a production-grade tool:
- [ ] Multi-document batch validation
- [ ] Reporting dashboard
- [ ] Auto-correction / improvement suggestions
- [ ] Integration with where your team's docs live (SharePoint, document libraries, ticketing, etc.)
- [ ] Real-time validation API

### 💎 Platinum Level: Operational Readiness
**Beyond shipping — thinking about the full lifecycle.**
Document how this tool lives in a real organisation:
- [ ] **Operations & maintenance**: Deployment model, update/versioning process, dependency management, and clear ownership after the hackathon
- [ ] **Inference economics**: Model tiering (Haiku for structural checks, Sonnet for deep analysis), prompt length optimisation, output token minimisation, request batching; understand Anthropic's input/output and cache write/read pricing
- [ ] **Cost analysis**: Token usage per document type, cost projections at realistic monthly volumes, ROI versus manual review
- [ ] **Caching strategy**: Implement document fingerprinting (skip re-validation of unchanged docs), result caching, and Anthropic prompt caching headers — demonstrate measurable token savings
- [ ] **Governance**: Defined ownership model, access control policy, audit trail for validation decisions, approval workflow for rule changes, false-positive escalation path
- [ ] **Service management**: Support runbook, SLA (uptime, latency, accuracy targets), user onboarding guide, process for adding a new document type, changelog/release notes process

## 📋 Requirements Checklist

The same three‑bucket shape applies to any domain — fill in the specifics
for your document type.

### File Naming / Reference
- [ ] What pattern identifies a valid document of this type?
- [ ] Which codes / segments are mandatory?
- [ ] How is revision / version expressed?

### Metadata
- [ ] What fields must be present (author, dates, approval state, classification…)?
- [ ] What values are valid?

### Content Structure
- [ ] What sections / clauses must be present?
- [ ] What is the appropriate level of detail?
- [ ] What revision / audit trail is required?

> **BIM / ISO 19650 worked example:** filename codes
> `PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-NUMBER_REVISION`;
> metadata fields *author, creation date, approval status, information
> container, security classification*; structure expectations *title block,
> revision history, required sections, appropriate level of information
> need*. Substitute equivalents for your own domain.

## 🛠️ Getting Started

### Prerequisites
- Python 3.11+
- Anthropic API key (see [REGISTRATION.md](REGISTRATION.md) for the Mace-network specifics)
- For the worked example, a basic familiarity with BIM/construction documents helps — but the same harness works for any document type your team owns

### Installation

```bash
# Clone repository
git clone https://github.com/stephencummins/mace-hackathon.git
cd mace-hackathon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY (and API_TOKEN if running the HTTP service)
```

### Quick Start

```bash
# Verify the harness
python check_compliance.py --help

# Validate a BIM PDF (Bronze naming + Silver content analysis via Claude)
python check_compliance.py examples/MAC-LIBDM-XX-00-DR-A-001_P01.pdf

# Batch a directory, write an HTML report
python check_compliance.py path/to/folder/ --format html

# Run the HTTP service (requires API_TOKEN in .env)
uvicorn src.api.main:app --reload

# Inspect what's been validated and what it cost
python -m src.audit_report --last 20
python -m src.cost_report
```

Two filename-demonstration PDFs ship in `examples/` (one ISO 19650 compliant,
one not — see [examples/README.md](examples/README.md)). The Silver content
checks need a real document with sections, metadata, and revision history to
produce meaningful findings — bring your own BIM document, or build a fixture
set per the *new document types* path in [ONBOARDING.md](ONBOARDING.md).

For a full walkthrough of the first hour after cloning, see
[REGISTRATION.md](REGISTRATION.md) Step 5. For day-to-day operation once
you're running, see [RUNBOOK.md](RUNBOOK.md).

## 📚 Project Structure

This is what the repo actually ships as of the current Platinum tier. The
shape below covers the worked ISO 19650 example; the harness is generic and
the same layout works for other document types (see ONBOARDING.md Part 2).

```
mace-hackathon/
├── README.md                  # This file
├── HACKATHON.md               # Challenge brief, levels, judging
├── REGISTRATION.md            # Setup, accounts, first hour after cloning
├── CLAUDE.md                  # Guidance for Claude Code when working in this repo
├── FAQ.md                     # Short answers to common questions
├── GOVERNANCE.md              # Ownership, access, audit, rubric workflow (index for the operational docs)
├── RUNBOOK.md                 # Day-to-day operation, failures, escalation
├── SLA.md                     # Uptime / latency / accuracy / cost targets
├── ONBOARDING.md              # New users + new document types
├── CHANGELOG.md               # Tier-grouped history + maintenance process
├── LICENSE                    # MIT
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── check_compliance.py        # Main CLI entry point
├── src/
│   ├── runner.py              # Batch validation (Gold PR 1)
│   ├── cache.py               # Document-level result cache (Platinum PR 1)
│   ├── cost.py                # Pricing + cost computation (Platinum PR 2)
│   ├── cost_report.py         # python -m src.cost_report (Platinum PR 2)
│   ├── audit.py               # Validation audit trail (Platinum PR 3)
│   ├── audit_report.py        # python -m src.audit_report (Platinum PR 3)
│   ├── validators/
│   │   ├── naming_validator.py    # Bronze: filename pattern check
│   │   ├── content_validator.py   # Silver: Claude content analysis
│   │   └── iso_19650_rubric.md    # The shipped rubric (swap for a new domain)
│   ├── reports/                   # Console / HTML / JSON report renderers (Gold PR 1)
│   └── api/
│       └── main.py            # FastAPI HTTP service (Gold PR 3)
├── tests/                     # 72 pytest cases covering runner, validators, cache, cost, audit, API
├── examples/
│   ├── MAC-LIBDM-XX-00-DR-A-001_P01.pdf  # Bronze-compliant fixture
│   ├── floor plan ground.pdf             # Bronze-non-compliant fixture
│   └── api_curl.md            # HTTP API request examples
└── assets/                    # Hackathon banner image
```

Three runtime directories are gitignored and created on first use:
`.cache/` (document-level validation cache), `.audit/` (append-only audit
trail), and any `compliance-report.{html,json}` files batch runs produce.

## 🛠️ Operating the tool (post-hackathon)

If you're not here to *build* but to *run* the validator — your team
finished the hackathon and now wants to use it — these are the docs you
need, in reading order:

| Doc | What it gives you |
|---|---|
| [ONBOARDING.md](ONBOARDING.md) Part 1 | Step-by-step from clone to first validation. Start here. |
| [ONBOARDING.md](ONBOARDING.md) Part 2 | If you're validating something other than BIM — how to swap the rubric, parser, and fixtures for your domain. |
| [RUNBOOK.md](RUNBOOK.md) | Daily checks, where files live, every common failure with its fix, deployment shapes, rotation cadence, P0–P3 escalation. |
| [SLA.md](SLA.md) | Uptime, latency, accuracy, and cost targets — with realistic hackathon-stage numbers and a quarterly acceptance test. |
| [GOVERNANCE.md](GOVERNANCE.md) | Ownership roles, access control, audit trail spec, rubric-change workflow, false-positive escalation. The index that ties the rest together. |
| [CHANGELOG.md](CHANGELOG.md) | What changed, when, grouped by tier. Maintained per-PR. |

For one-off questions, [FAQ.md](FAQ.md) is the fastest route. For
hackathon judging criteria and the original brief,
[HACKATHON.md](HACKATHON.md).

## 🎓 Resources

### ISO 19650 Documentation
- [ISO 19650-1:2018 Overview](https://www.iso.org/standard/68078.html)
- [UK BIM Framework](https://www.ukbimframework.org/)
- [ISO 19650 Guidance](https://www.ukbimframework.org/standards-guidance/)

### Technical Resources
- [Claude AI Documentation](https://docs.anthropic.com/)
- [pypdf Documentation](https://pypdf.readthedocs.io/)
- [python-docx Documentation](https://python-docx.readthedocs.io/)

## 🏆 Judging Criteria

Projects will be evaluated on:

1. **Functionality** (40%)
   - Accuracy of compliance checking
   - Coverage of ISO 19650 requirements
   - Error handling

2. **Innovation** (30%)
   - Creative use of Claude AI
   - Unique features
   - User experience

3. **Code Quality** (20%)
   - Clean, maintainable code
   - Documentation
   - Testing

4. **Presentation** (10%)
   - Demo quality
   - Documentation clarity
   - Real-world applicability

## 💡 Tips for Success

1. **Start Simple**: Get basic file naming validation working first
2. **Use Claude Effectively**: Let AI handle complex content analysis
3. **Test with Real Documents**: Use actual BIM documents for validation
4. **Provide Clear Feedback**: Help users understand what needs fixing
5. **Think About Scale**: Design for batch processing from the start

## 🤝 Contributing

This is a hackathon challenge repository. Participants should:
1. Fork this repository
2. Build your solution
3. Submit via pull request or demo

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support

- **Slack Community**: [maice-workspace.slack.com](https://maice-workspace.slack.com)
- **Questions**: [Open an issue](https://github.com/stephencummins/mace-hackathon/issues)
- **Discussions**: [GitHub Discussions](https://github.com/stephencummins/mace-hackathon/discussions)
- **Hackathon Info**: See [HACKATHON.md](HACKATHON.md) for registration and setup details

## 🎉 Good Luck!

Build something amazing and show us how AI can improve construction document compliance!

---

**Built for Mace Digital Hackathon** | **Powered by Claude AI**
