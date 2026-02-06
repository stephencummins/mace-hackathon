# Mace Digital Compliance Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Claude](https://img.shields.io/badge/AI-Claude-purple.svg)](https://www.anthropic.com/claude)

**Hackathon Challenge**: Build a document compliance checker using Claude AI to validate ISO 19650 standards for Building Information Modeling (BIM).

> 📢 **New to the hackathon?** Check out [HACKATHON.md](HACKATHON.md) for complete registration details, setup instructions, and community links!

## 🎯 Challenge Overview

ISO 19650 is the international standard for information management using Building Information Modeling (BIM). This hackathon challenge is to build an intelligent document compliance checker that validates construction/BIM documents against ISO 19650 requirements.

## 🏗️ What is ISO 19650?

ISO 19650 defines how information should be managed throughout the lifecycle of a built asset using BIM. It covers:

- **ISO 19650-1**: Concepts and principles
- **ISO 19650-2**: Delivery phase of assets
- **ISO 19650-3**: Operational phase of assets
- **ISO 19650-5**: Security-minded approach

Key requirements include:
- Structured information exchange
- Clear naming conventions
- Metadata requirements
- Information delivery milestones
- Collaboration procedures

## 🚀 Challenge Tasks

### 🥉 Bronze Level: Basic Validation
Build a document validator that checks:
- [ ] File naming conventions (e.g., `PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-CLASSIFICATION-NUMBER_REVISION`)
- [ ] Required metadata fields
- [ ] Document structure compliance
- [ ] Basic format requirements

### 🥈 Silver Level: AI-Powered Analysis
Enhance with Claude AI to:
- [ ] Analyze document content for compliance
- [ ] Check for required sections and clauses
- [ ] Validate information exchange requirements
- [ ] Identify missing mandatory information

### 🥇 Gold Level: Full Compliance Suite
Create a comprehensive system with:
- [ ] Multi-document batch validation
- [ ] Compliance reporting dashboard
- [ ] Auto-correction suggestions
- [ ] Integration with SharePoint/Azure
- [ ] Real-time validation API

## 📋 Requirements Checklist

Documents must meet these ISO 19650 requirements:

### File Naming
- [ ] Project code present
- [ ] Originator code included
- [ ] Volume/system code specified
- [ ] Classification code correct
- [ ] Revision status indicated

### Metadata
- [ ] Author information
- [ ] Creation date
- [ ] Approval status
- [ ] Information container
- [ ] Security classification

### Content Structure
- [ ] Title block present
- [ ] Revision history included
- [ ] Required sections present
- [ ] Appropriate level of information need

## 🛠️ Getting Started

### Prerequisites
- Python 3.11+
- Anthropic API key
- Basic understanding of BIM/construction documents

### Installation

```bash
# Clone repository
git clone https://github.com/stephencummins/mace-digital-compliance-checker.git
cd mace-digital-compliance-checker

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
# Run validation on a single document
python check_compliance.py path/to/document.pdf

# Batch validate multiple documents
python batch_validate.py path/to/documents/

# Generate compliance report
python generate_report.py --format html
```

## 📚 Project Structure

```
mace-digital-compliance-checker/
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
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
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
- **Questions**: [Open an issue](https://github.com/stephencummins/mace-digital-compliance-checker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/stephencummins/mace-digital-compliance-checker/discussions)
- **Hackathon Info**: See [HACKATHON.md](HACKATHON.md) for registration and setup details

## 🎉 Good Luck!

Build something amazing and show us how AI can improve construction document compliance!

---

**Built for Mace Digital Hackathon** | **Powered by Claude AI**
