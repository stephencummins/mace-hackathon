# Examples

Two minimal PDFs whose **filenames** demonstrate the ISO 19650 naming check —
the BIM **worked example** for the hackathon. Their *contents* are tiny
placeholders; these fixtures exercise **Bronze** (file-naming) validation
fully and **Silver** (AI content analysis) in name only — Silver will
surface lots of findings against placeholder content, which is informative
but not representative of a real BIM document.

For your own domain (quality manuals, bids, contracts, RAMS, finance docs,
HR policy, planning subs — anything your team owns), **create equivalent
fixtures** here: one filename that conforms to your team's pattern, one that
doesn't. The full "new document types" walkthrough is in
[ONBOARDING.md](../ONBOARDING.md) Part 2.

| File | Demonstrates |
| --- | --- |
| `MAC-LIBDM-XX-00-DR-A-001_P01.pdf` | A filename that **conforms** to the ISO 19650 pattern `PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-NUMBER_REVISION`. |
| `floor plan ground.pdf` | A filename that **does not conform** (spaces, no codes, no revision). |
| `api_curl.md` | Request examples for the Gold-tier HTTP API (`curl` and PowerShell snippets). |

Use them as fixtures while you build the naming validator:

```bash
python check_compliance.py examples/MAC-LIBDM-XX-00-DR-A-001_P01.pdf
python check_compliance.py "examples/floor plan ground.pdf"
```

For **meaningful Silver** runs and **Gold** demos (batch, reports, HTTP
API), bring your own BIM document — anything with real sections, metadata,
and revision history. For **Platinum** operational features (cache, cost
report, audit trail), the same real document run a few times is enough to
populate `.cache/` and `.audit/` so `python -m src.cost_report` and
`python -m src.audit_report` have something interesting to show.
