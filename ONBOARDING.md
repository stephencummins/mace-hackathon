# Onboarding

Two audiences:

1. **New users / operators** — you want to *use* the tool to validate documents.
   Start at [Part 1](#part-1--new-users).
2. **New domains / adopters** — you want to *swap or extend* the tool to
   validate a different document type (HR policies, contracts, RAMS, bid
   responses…). Start at [Part 2](#part-2--new-document-types).

If you're running the tool for the first time, both parts apply: do Part 1
first, then Part 2 when you outgrow the shipped ISO 19650 rubric.

---

## Part 1 — New users

### Prerequisites

| Tool | Version | Why |
|---|---|---|
| Python | 3.11+ | Async generics, modern type hints |
| Git | Any modern | Clone the repo, work on a branch |
| Anthropic API key | Active | Silver-level content checks call Claude |
| (Optional) Claude Code CLI | Any | If you want the AI-assisted dev workflow described in `CLAUDE.md` |

Mace-network specifics: see `FAQ.md` ("How do I get this running on the
Mace network?"). The proxy and corporate cert chain are already wired in
via `truststore` — you shouldn't need to do anything beyond the standard
setup.

### Step 1 — Get the code

```powershell
git clone https://github.com/stephencummins/mace-hackathon.git
cd mace-hackathon
```

### Step 2 — Create a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate       # Windows
# source venv/bin/activate    # macOS / Linux
pip install -r requirements.txt
```

### Step 3 — Configure secrets

```powershell
Copy-Item .env.example .env
notepad .env
```

In `.env`, set:

- `ANTHROPIC_API_KEY` — your key from console.anthropic.com (off the Mace
  network — see FAQ).
- `CLAUDE_MODEL` — leave as `claude-sonnet-4-6` unless you have a reason
  to change.
- `API_TOKEN` — only needed if you'll run the HTTP service. Generate with
  `python -c "import secrets; print(secrets.token_urlsafe(32))"`.

`.env` is gitignored. **Never commit it.**

### Step 4 — Run your first validation

```powershell
python check_compliance.py examples\MAC-LIBDM-XX-00-DR-A-001_P01.pdf
```

What you should see:

- A Rich console report.
- A green tick on the filename check (Bronze).
- A Silver section with pass/fail/warning findings against the rubric.
- A "Estimated cost this run" footer (Platinum PR 2).

If you don't, jump to `RUNBOOK.md` § *Common failures and fixes*.

### Step 5 — Try the other modes

```powershell
# JSON output (for scripts)
python check_compliance.py examples\<pdf> --format json

# HTML report (for sharing)
python check_compliance.py examples\<pdf> --format html
start compliance-report.html

# Skip the cache (force fresh validation)
python check_compliance.py examples\<pdf> --no-cache

# Use a different model
python check_compliance.py examples\<pdf> --model haiku

# Batch a directory
python check_compliance.py path\to\folder\ --format html
```

### Step 6 — Inspect the audit and cost trails

```powershell
python -m src.audit_report --last 10
python -m src.cost_report
```

These read from `.audit/` and `.cache/` respectively and show what's been
run, by whom, and what it cost.

### Step 7 — (Optional) Run the HTTP service

```powershell
$env:API_TOKEN = "<the token you set in .env, or a fresh one>"
uvicorn src.api.main:app --reload
```

Smoke test it:

```powershell
curl.exe -H "Authorization: Bearer $env:API_TOKEN" `
  -F "file=@examples\MAC-LIBDM-XX-00-DR-A-001_P01.pdf" `
  http://127.0.0.1:8000/validate
```

OpenAPI docs at `http://127.0.0.1:8000/docs`. Full curl + PowerShell
snippets are in `examples/api_curl.md`.

### You're done

At this point you can validate documents, share reports, and inspect
costs and the audit trail. If you only care about ISO 19650 / BIM, stop
here. If your team works with a different document type, continue to
Part 2.

---

## Part 2 — New document types

The harness is generic. The shipped rubric is ISO 19650. To validate a
different document type (HR policies, contracts, RAMS, bid responses,
planning submissions, finance forms…), you swap or extend three things:

1. The **filename pattern** (Bronze).
2. The **content rubric** (Silver).
3. The **fixture set** (acceptance tests).

Parser changes are only needed if your documents aren't PDFs.

### Step 1 — Describe the rules in plain English

Before touching code, write down — in plain English — what makes a valid
document of your type. The shape:

| Layer | Question to answer |
|---|---|
| Filename | What pattern identifies a valid document? Which segments are mandatory? How is revision expressed? |
| Metadata | What fields must be present (author, date, version, classification)? What values are valid? |
| Content | What sections must be present? What level of detail? What internal consistency rules (dates align, totals add up, references resolve)? |

For example, for an HR policy you might say: *"Filename must be
`HR-POLICY-<2-letter-team>-<3-digit-num>-V<major>_<minor>.pdf`. Must have a
named policy owner, an effective date, and a review date no more than 2
years after effective. Must contain sections: Purpose, Scope, Policy,
Procedure, Responsibilities, Review."*

### Step 2 — Update the filename validator (Bronze)

`src/validators/naming_validator.py` holds the regex and the field
breakdown. Two changes:

1. Update the pattern to match your domain.
2. Update the field names returned in `ValidationResult` so the report
   labels are accurate (e.g. *Originator* → *Team code*).

Update the tests too: `tests/test_naming_validator.py` has the
canonical compliant and non-compliant cases. Pattern: write the
non-compliant case first, watch it fail, then write the regex.

### Step 3 — Swap the rubric (Silver)

The content rubric lives in `src/validators/iso_19650_rubric.md`. It's
plain markdown, sent verbatim to Claude with the document as the user
message.

Two options:

- **Replace it.** Rename to e.g. `src/validators/hr_policy_rubric.md`,
  rewrite the criteria, and update the import in
  `src/validators/content_validator.py` (search for `iso_19650_rubric.md`).
- **Multi-rubric.** Add the new rubric alongside; have
  `content_validator.py` pick the rubric file based on a CLI flag or env
  var. This is the right shape if one team validates multiple document
  types in one tool.

Rubric authoring tips:

- Be specific. "Has a date" is too loose — say "Has a date in ISO 8601
  (YYYY-MM-DD) format in the title block or document properties."
- Each criterion should be `pass` / `fail` / `warning` — three states is
  the cap. More states make the model less consistent.
- Give the model permission to flag `warning` rather than force a
  binary. Genuine ambiguity is information.
- Cite sections or page numbers in the criterion so the model knows
  where to look — "in the Purpose section" beats "somewhere in the
  document".

### Step 4 — (Only if not PDF) Add a parser

`src/parsers/` is where document parsing lives. PDFs use `pypdf`. To add
DOCX:

1. Add `python-docx` to `requirements.txt`.
2. Create `src/parsers/docx_parser.py` exposing the same interface as
   `pdf_parser.py` (`extract_text(path: Path) -> str`).
3. Update `content_validator.py` (or `runner.py`, depending on where
   parsing is dispatched) to pick the parser based on file extension.

Same shape for PPTX (`python-pptx`), email (`mailparser`), etc.

### Step 5 — Build a fixture set

Before changing anything, save 2–10 documents that represent the range
of cases you care about:

```
examples/
├── compliant-policy-2024.pdf
├── missing-review-date.pdf
├── ambiguous-scope.pdf
└── legacy-pre-2018-format.pdf
```

For each, write down (in a markdown file or a CSV) the ground-truth
result per criterion. This is the corpus that drives the accuracy
targets in `SLA.md`.

### Step 6 — Run the new validator

```powershell
python check_compliance.py examples\compliant-policy-2024.pdf
python check_compliance.py examples\missing-review-date.pdf
```

Compare results to the ground truth. Tune the rubric until both:

- All known-compliant documents pass.
- All known-non-compliant documents fail on the right criteria (not the
  wrong ones — a false-positive on a different criterion is still wrong).

### Step 7 — Run the tests

```powershell
python -m pytest -x --tb=short
```

Add tests for the new naming pattern in `tests/test_naming_validator.py`.
Content-validator behaviour is integration-level (it calls Claude), so
those tests usually mock the API — see `tests/test_content_validator.py`
for the pattern.

### Step 8 — Document and commit

- Update `README.md` if the domain change is permanent (rename "BIM /
  ISO 19650" to your domain).
- Update `CLAUDE.md` § *Project Overview* and § *Validation Rules* to
  reflect the new rubric.
- Add a `CHANGELOG.md` entry under [Unreleased] or the next tier:
  `Changed: rubric swapped from ISO 19650 to HR policy v1.`
- Commit with a clear message; per `GOVERNANCE.md`'s rubric-change
  workflow, tag the merged commit `rubric/YYYY-MM-DD` so the audit
  trail can be tied back to the rubric version.

### Step 9 — Adopt the SLA, or rewrite it

The targets in `SLA.md` were measured against the shipped ISO 19650
rubric and Sonnet 4.6. If you've changed either:

- Re-measure the latency (Sonnet vs Haiku vs Opus give different P95s).
- Re-measure the cost (longer rubrics cost more; bigger documents cost
  more).
- Rebuild the accuracy numbers from your new fixture set.

A rubric swap is a *new validator*. Treat the SLA values as a starting
template, not a guarantee.

---

## Where to go next

- `RUNBOOK.md` — once you're running, this is your day-to-day reference.
- `GOVERNANCE.md` — who owns this, how rule changes go through, how
  false positives are handled.
- `SLA.md` — what "working as intended" actually means.
- `FAQ.md` — short answers to common questions.
- `HACKATHON.md` — the original challenge brief, if you want the
  Bronze/Silver/Gold/Platinum context.

Welcome — and good luck.
