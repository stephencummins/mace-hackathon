# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mace Digital Compliance Checker is a hackathon project for validating construction/BIM documents against ISO 19650 standards using Claude AI.

**Challenge Levels:**
- **Bronze**: Basic file naming and metadata validation
- **Silver**: AI-powered content analysis with Claude
- **Gold**: Full compliance suite with batch processing, dashboard, and API

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

```
mace-digital-compliance-checker/
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
Pattern: `PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-CLASSIFICATION-NUMBER_REVISION`

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
- **pdfplumber/PyPDF2**: PDF parsing
- **python-docx**: Word document parsing

## Implementation Tips

1. Start with `src/validators/naming_validator.py` for Bronze level
2. Use Claude API in `src/validators/content_validator.py` for Silver level
3. Keep validation rules modular and testable
4. Return structured results (pass/fail/warning with details)
