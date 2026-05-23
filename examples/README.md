# Examples

Two minimal PDFs whose **filenames** demonstrate the ISO 19650 naming check —
the BIM **worked example** for the hackathon. Their *contents* are tiny
placeholders; these fixtures exercise **Bronze** (file-naming) validation only.

For your own domain (quality manuals, bids, contracts, RAMS, finance docs,
HR policy, planning subs — anything your team owns), **create equivalent
fixtures** here: one filename that conforms to your team's pattern, one that
doesn't.

| File | Demonstrates |
| --- | --- |
| `MAC-LIBDM-XX-00-DR-A-001_P01.pdf` | A filename that **conforms** to the ISO 19650 pattern `PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-NUMBER_REVISION`. |
| `floor plan ground.pdf` | A filename that **does not conform** (spaces, no codes, no revision). |

Use them as fixtures while you build the naming validator:

```bash
python check_compliance.py examples/MAC-LIBDM-XX-00-DR-A-001_P01.pdf
python check_compliance.py "examples/floor plan ground.pdf"
```

For **Silver** (AI content analysis) and **Gold** (full suite), bring your own
BIM document — anything with real sections, metadata, and revision history.
