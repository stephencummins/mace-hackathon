# Mace Digital Compliance Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Claude](https://img.shields.io/badge/AI-Claude-purple.svg)](https://www.anthropic.com/claude)

**Hackathon Challenge**: Build an AI‑powered document validator with Claude — for *any* document type your team works with. The repo ships a worked example for **ISO 19650 / BIM**; swap in your own domain.

> 📢 **New here?** Register on the **M+AI+CE site**: 👉 **[hackathon.stephen8n.com/p/mace](https://hackathon.stephen8n.com/p/mace)**. Then see [REGISTRATION.md](REGISTRATION.md) for setup and [HACKATHON.md](HACKATHON.md) for rules, levels, and judging.

## 🎯 Challenge Overview

Pick a document type your team works with — *anything* — and build an
AI‑powered validator with Claude. The **Bronze → Silver → Gold** structure
below applies regardless of domain: you bring the rules, Claude helps you
enforce them at scale.

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

## 🗂️ Example: HR document validator

Not a BIM team? Here's how the same approach works for HR — use this as a template for any department.

### Step 1 — define your naming pattern

HR documents at Mace might follow a pattern like:

```
HR-<TYPE>-<DEPARTMENT>-<NUMBER>_<REVISION>
```

For example:
- `HR-POL-ALL-001_v2.docx` — company-wide policy, revision 2 ✅
- `HR-JD-ENG-042_v1.pdf` — engineering job description ✅
- `Job Description Engineer Final FINAL.docx` — ❌ fails

Types: `POL` (policy), `JD` (job description), `PER` (performance review), `CON` (contract), `TRN` (training record)

### Step 2 — define your content rules (Silver)

What should an HR policy document always contain?
- A version number and effective date
- An owner / responsible person
- A review date
- A scope section
- Sign-off / approval

### Step 3 — prompt Claude

Paste this into the `claude` terminal:

> Implement Bronze-level naming validation for HR documents. The pattern is `HR-<TYPE>-<DEPARTMENT>-<NUMBER>_<REVISION>` where TYPE is one of POL, JD, PER, CON, TRN. Write `src/validators/naming_validator.py`, wire it into `check_compliance.py`, and add unit tests under `tests/`. Create a passing fixture `examples/HR-POL-ALL-001_v1.docx` and a failing fixture `examples/Job Description Final FINAL.docx`.

That's it. Claude will write the validator, wire it in, and write the tests. You just run them.

### The pattern for any domain

| Step | Question to answer | BIM example | HR example |
|------|-------------------|-------------|------------|
| 1 | What does a valid filename look like? | `PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-NUMBER_REVISION` | `HR-TYPE-DEPT-NUMBER_REVISION` |
| 2 | What metadata must always be present? | Author, revision, classification | Owner, effective date, review date |
| 3 | What must the content contain? | Exchange information requirements, delivery milestones | Scope, sign-off, version number |
| 4 | What does a passing fixture look like? | `MAC-LIBDM-XX-00-DR-A-001_P01.pdf` | `HR-POL-ALL-001_v1.docx` |
| 5 | What does a failing fixture look like? | `floor plan ground.pdf` | `Job Description Final FINAL.docx` |

Answer those five questions for your document type, swap them into the prompt, and Claude does the rest.

## 🚀 Challenge Tasks

Pick a domain (see above), then ladder through three tiers. Each tier is
described generically — substitute the specifics of *your* document type.

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
- Anthropic API key
- Basic understanding of BIM/construction documents

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
# Edit .env and add your ANTHROPIC_API_KEY
```

### Quick Start

```bash
# Verify the harness
python check_compliance.py --help

# Run the stub on a provided example (it returns placeholder output until
# you implement the real validators — that's the challenge).
python check_compliance.py examples/MAC-LIBDM-XX-00-DR-A-001_P01.pdf
```

Two filename‑demonstration PDFs ship in `examples/` (one ISO 19650 compliant,
one not). For Silver/Gold content validation, use your own BIM document.
Step‑by‑step walkthrough: see [REGISTRATION.md](REGISTRATION.md) Step 5
("First hour after cloning").

Batch validation and report generation (e.g. `batch_validate.py`,
`generate_report.py`) are examples of commands your Silver/Gold solution
might expose; they are not provided.

## 📚 Project Structure

> **Target layout.** Today the repo ships `check_compliance.py` (a stub),
> `requirements.txt`, `.env.example`, the markdown docs, `LICENSE`, `assets/`,
> and `examples/` (two filename‑demonstration PDFs — see
> [examples/README.md](examples/README.md)). The `src/`, `tests/`, and `docs/`
> trees below are what you build out as part of the challenge.

```
mace-hackathon/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── check_compliance.py            # Main validation script
├── src/
│   ├── validators/
│   │   ├── naming_validator.py    # File naming checker
│   │   ├── metadata_validator.py  # Metadata checker
│   │   └── content_validator.py   # AI-powered content analysis
│   ├── parsers/
│   │   ├── pdf_parser.py          # PDF document parser
│   │   └── docx_parser.py         # Word document parser
│   └── reports/
│       └── report_generator.py    # Compliance report generator
├── tests/                         # Unit tests
├── docs/
│   ├── ISO_19650_GUIDE.md        # ISO 19650 quick reference
│   └── API_REFERENCE.md          # API documentation
└── examples/
    ├── sample_compliant.pdf       # Example compliant document
    └── sample_non_compliant.pdf   # Example with issues
```

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
