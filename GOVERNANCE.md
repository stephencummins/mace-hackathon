# Governance

This document covers the operational governance of the Mace Compliance
Checker: who owns it, who can use it, how decisions are recorded, how the
rubric changes, and what happens when the validator gets a known-good
document wrong.

The Platinum-tier rubric explicitly asks for each of these.

## Ownership

| Role | Responsibility | Default owner |
|---|---|---|
| Product owner | Sets the rubric, signs off on releases, owns the roadmap | Hackathon team lead |
| Maintainer | Reviews and merges PRs, manages secrets (`ANTHROPIC_API_KEY`, `API_TOKEN`) | Hackathon team lead |
| Operator | Runs the validator, monitors cost, archives audit trails | Whoever holds the CLI / runs the service |
| Domain reviewer | SME on ISO 19650; arbitrates false-positive escalations | A BIM specialist nominated for the engagement |

The hackathon submission lists named individuals against each role on the
team page. Outside hackathon mode, this table is filled in by whichever
department adopts the tool.

## Access control

- **API keys**: each operator has their own personal Anthropic API key (see
  the FAQ on shared vs personal keys). Keys are never committed; only set in
  `.env` or session env vars.
- **HTTP service token**: `API_TOKEN` is required for `POST /validate`; the
  server refuses to start without it. The token grants full access to the
  endpoint — rotate it by setting a new value and restarting the service.
  `GET /healthz` is intentionally unauthenticated so load balancers can
  probe it.
- **Rubric**: `src/validators/iso_19650_rubric.md` is plain markdown — anyone
  with PR rights can propose a change, but merge requires sign-off (see
  *Rubric change workflow* below).
- **Cache & audit**: the `.cache/` and `.audit/` directories contain
  validation outputs (potentially document content) and an attribution
  trail. They're gitignored. Treat the audit log like a finance log: keep
  it; don't share it casually.

## Audit trail

Every validation — CLI or API — appends one JSONL line to
`.audit/validations.jsonl` containing:

- ISO 8601 timestamp (UTC)
- `source`: `cli` or `api`
- `principal`: OS user for CLI; `tok_<8 hex>` (SHA-256 prefix of the bearer
  token) for API. The raw token is **never** logged.
- `doc_name` (basename only) + `doc_hash` (SHA-256 of PDF bytes). The hash
  lets you correlate an entry to the corresponding `.cache/<hash>.json`
  result file for forensic detail.
- `model`, `from_cache`
- `naming_passed`, `content_status`, `finding_counts`, `content_error`
- `cost_usd`

Inspect with the bundled tool:

```bash
python -m src.audit_report                        # last 20 entries + summary
python -m src.audit_report --source api           # filter by source
python -m src.audit_report --principal tok_a1b2   # filter by caller
python -m src.audit_report --last 0               # everything
```

The log is append-only — never edit it by hand. For data retention, copy or
archive `.audit/validations.jsonl` periodically; the file is safe to rotate
(e.g. monthly) because the validator opens it in append mode.

## Rubric change workflow

The rubric (`src/validators/iso_19650_rubric.md`) is the *single source of
truth* for what "compliant" means. Changes ship via PR:

1. Propose the change as a PR. Include a short rationale (which criterion,
   why it's tightening or loosening, an example of a document that should
   now grade differently).
2. **Required reviewers**: the Product owner and a Domain reviewer. One
   approval from each.
3. Run the example fixtures and at least one real BIM document before
   merging, to sanity-check the new grading. The cache automatically
   invalidates when the rubric text changes (the fingerprint is over the
   rubric content), so first runs after a rubric merge will hit Claude
   afresh.
4. Tag the merged commit with a `rubric/YYYY-MM-DD` git tag so historical
   audit entries can be linked to the rubric version that was active.

## False-positive escalation

When the validator flags a document the Domain reviewer considers
genuinely compliant:

1. **Capture evidence**: keep the audit entry, the document, and the
   reviewer's annotation explaining why it should pass.
2. **File an issue** with:
   - The `doc_hash` from the audit entry (so the cached finding can be
     pulled up)
   - The reviewer's justification
   - The proposed rubric tweak (e.g. *"clarify Criterion 4: an information
     container identifier in the body counts even without a title block"*)
3. **Decide**: rubric tweak vs known-exception list. Most cases are rubric
   tweaks. A documented exception is the right answer when the document
   genuinely doesn't fit the standard (e.g. a legacy asset transferred
   from a non-ISO-19650 source).
4. **Update**: rubric tweaks go through the *Rubric change workflow* above.
   Exception entries live in `docs/exceptions.md` (create when needed) with
   the document hash and reviewer's name.
5. **Communicate**: if a tool decision blocks a deliverable, the Operator
   notifies the Product owner via Slack `#technical-help`.

The goal: every false-positive either improves the rubric or is recorded
as a known exception — never silently overridden.
