"""Generate the engineering-leadership deck for the M+AI+CE Hackathon.

10 slides, 16:9, for engineering leaders (CTO, Heads of Engineering,
Tech Leads) — how the hackathon teaches Mace developers to build with
Claude responsibly, and the governance model that comes with it. Run:

    python presentations/build_dev_governance_deck.py

Output:

    presentations/mace-dev-governance-deck.pptx

The deck is gitignored (regenerable); this script is checked in.
"""

from __future__ import annotations

from functools import partial
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches

from _deckkit import (
    ACCENT,
    CHARCOAL,
    GREEN,
    LIGHT_BG,
    MUTED,
    NAVY,
    SLIDE_H,
    SLIDE_W,
    WHITE,
    add_blank_slide,
    add_bullets,
    add_rect,
    add_text,
    header_band,
)
from _deckkit import footer_band as _footer_band

footer_band = partial(
    _footer_band, attribution="M+AI+CE Hackathon  ·  Building with AI at Mace"
)


# --- Slides -------------------------------------------------------------------

def slide_title(prs):
    s = add_blank_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, NAVY)
    add_rect(s, 0, Inches(3.4), SLIDE_W, Inches(0.08), ACCENT)
    add_text(
        s,
        Inches(0.8),
        Inches(2.0),
        SLIDE_W - Inches(1.6),
        Inches(1.4),
        "Building with AI at Mace",
        size=48,
        bold=True,
        color=WHITE,
    )
    add_text(
        s,
        Inches(0.8),
        Inches(3.6),
        SLIDE_W - Inches(1.6),
        Inches(0.6),
        "How the M+AI+CE Hackathon teaches the practices, and the governance that goes with them",
        size=20,
        color=WHITE,
    )
    add_text(
        s,
        Inches(0.8),
        Inches(4.5),
        SLIDE_W - Inches(1.6),
        Inches(0.5),
        "Engineering leadership briefing  ·  2026",
        size=16,
        color=ACCENT,
    )
    add_text(
        s,
        Inches(0.8),
        SLIDE_H - Inches(0.9),
        SLIDE_W - Inches(1.6),
        Inches(0.4),
        "For CTO, Heads of Engineering, Engineering Managers  ·  Confidential",
        size=12,
        color=WHITE,
    )


def slide_why(prs):
    s = add_blank_slide(prs)
    header_band(s, "Why this hackathon exists", "Three pressures, one response")
    add_bullets(
        s,
        Inches(0.9),
        Inches(1.7),
        Inches(11.5),
        Inches(5),
        [
            ("Claude is capable today",
             "AI-assisted development is no longer experimental. Engineers who learn to "
             "work with it well are 2–5× faster on the kind of code Mace writes most: "
             "domain logic, integrations, data validation, internal tools."),
            ("Mace developers need to learn *how*, not just *that*",
             "Telling people \"you can use AI\" is not training. The hackathon teaches "
             "the working patterns — describe intent, iterate, verify, instrument — that "
             "separate AI-as-pair-programmer from AI-as-copy-paste."),
            ("Governance has to come first, not last",
             "Tools that ship without ownership, audit, and a rule-change workflow end "
             "up as shadow IT. We build the governance scaffolding into the format so "
             "every team's output ships with it, not as an afterthought."),
        ],
        title_size=18,
        body_size=14,
    )
    footer_band(s, 2)


def slide_format(prs):
    s = add_blank_slide(prs)
    header_band(s, "What developers actually do", "Three-step loop, repeated until it works")

    # Three column cards: Describe / Build / Iterate
    box_w = Inches(3.95)
    box_h = Inches(4.6)
    box_top = Inches(1.7)
    box_left_1 = Inches(0.6)
    box_left_2 = Inches(0.6 + 3.95 + 0.2)
    box_left_3 = Inches(0.6 + 2 * (3.95 + 0.2))

    for left, header, sub, points, color in [
        (box_left_1, "1.  Describe", "Plain English", [
            "\"The valid filename pattern is PROJECT-ORIGINATOR-VOLUME…\"",
            "\"Documents must have an author, a date, and a suitability code.\"",
            "\"Write a unit test that asserts X is rejected.\"",
            "Engineers describe rules at the level a domain expert would write them.",
        ], NAVY),
        (box_left_2, "2.  Build", "Claude writes code", [
            "Claude proposes the implementation, the tests, and the wiring.",
            "Output lands in the working tree — engineer reads, runs, and commits.",
            "Tests are written first; engineer watches them fail, then pass.",
            "The engineer stays in control of every diff that lands.",
        ], ACCENT),
        (box_left_3, "3.  Iterate", "Treat it as pairing", [
            "Wrong abstraction? Push back. \"Refactor — this duplicates X.\"",
            "Missing case? Add a test, ask for the fix.",
            "Cost too high? Switch model, add caching.",
            "Iterate until the diff is right, not until it compiles.",
        ], GREEN),
    ]:
        add_rect(s, left, box_top, box_w, Inches(0.85), color)
        add_text(s, left + Inches(0.2), box_top + Inches(0.1), box_w - Inches(0.4), Inches(0.45),
                 header, size=22, bold=True, color=WHITE)
        add_text(s, left + Inches(0.2), box_top + Inches(0.5), box_w - Inches(0.4), Inches(0.3),
                 sub, size=13, color=WHITE)
        add_rect(s, left, box_top + Inches(0.85), box_w, box_h - Inches(0.85), LIGHT_BG)
        add_bullets(s,
                    left + Inches(0.25),
                    box_top + Inches(1.05),
                    box_w - Inches(0.5),
                    box_h - Inches(1.15),
                    points,
                    title_size=14,
                    body_size=12)

    footer_band(s, 3)


def slide_practice1(prs):
    s = add_blank_slide(prs)
    header_band(s, "Practice 1 — Claude is a senior pair, not an oracle", "Bronze tier")
    add_bullets(
        s,
        Inches(0.9),
        Inches(1.7),
        Inches(11.5),
        Inches(5),
        [
            ("Iterate. Don't expect one-shot perfection.",
             "The first response is a starting point. Read it. Run it. Argue with it. "
             "The engineer who commits the first thing Claude writes is the engineer who "
             "ships bugs they don't understand."),
            ("Tests before code — every time.",
             "Hackathon convention: write the failing test first, watch Claude make it "
             "pass, then add the next case. This is the simplest way to keep the AI "
             "honest about what \"working\" means."),
            ("Stay close to the diff.",
             "Engineers read every line that lands. AI-written code that's never been "
             "read by a human is the new version of copied-from-Stack-Overflow code — "
             "except faster to produce, so the problem scales faster."),
            ("Push back when the abstraction is wrong.",
             "Claude defaults to safety: extra error handling, defensive layers, helper "
             "functions for two-line patterns. Engineers learn to say \"simpler — just "
             "do the thing\" and to spot YAGNI in real time."),
        ],
        title_size=18,
        body_size=14,
    )
    footer_band(s, 4)


def slide_practice2(prs):
    s = add_blank_slide(prs)
    header_band(s, "Practice 2 — AI for reasoning, regex for structure", "Silver tier + model tiering")
    add_bullets(
        s,
        Inches(0.9),
        Inches(1.7),
        Inches(11.5),
        Inches(5),
        [
            ("Reach for AI where reasoning helps, not where determinism is fine.",
             "Bronze checks a filename pattern — a regex, zero AI cost, sub-second, "
             "free. Silver checks document content — that's where Claude adds value, "
             "because the question is \"does this paragraph say the right thing?\""),
            ("Pick the model deliberately.",
             "Haiku 4.5 for high volume and structural checks (~£0.001/doc). "
             "Sonnet 4.6 as default — good balance (~£0.003/doc). "
             "Opus 4.7 for hard reasoning and final-sign-off passes (~£0.005/doc). "
             "The hackathon ships a `--model` flag so the right tier is one keystroke away."),
            ("Treat rubrics as configuration, not code.",
             "The ISO 19650 rubric lives in src/validators/iso_19650_rubric.md — plain "
             "markdown, version controlled, swapped per domain. Engineers learn that "
             "AI \"prompts\" are a configuration surface that deserves PRs and review, "
             "not a hidden string buried in a function."),
            ("Measure before you optimise.",
             "Silver runs are logged with token counts and costs. Engineers see the "
             "real bill, not a vibe. \"Should we use Haiku here?\" is answered by data, "
             "not by argument."),
        ],
        title_size=18,
        body_size=14,
    )
    footer_band(s, 5)


def slide_practice3(prs):
    s = add_blank_slide(prs)
    header_band(s, "Practice 3 — Production-grade thinking from day one", "Platinum tier — cache, cost, ops")

    # Stat tiles across the top
    tile_w = Inches(2.9)
    tile_h = Inches(1.5)
    tile_top = Inches(1.7)
    tile_left_start = Inches(0.6)
    gap = Inches(0.25)
    stats = [
        ("£0", "Re-validating an unchanged doc (cache hit)", ACCENT),
        ("99.8%", "Cost saving vs manual review at 1k docs/month", GREEN),
        ("100%", "Validations recorded in the audit trail", NAVY),
        ("4", "Operational docs shipped: runbook, SLA, onboarding, changelog", NAVY),
    ]
    for i, (big, sub, color) in enumerate(stats):
        left = tile_left_start + i * (tile_w + gap)
        add_rect(s, left, tile_top, tile_w, tile_h, LIGHT_BG)
        add_text(s, left + Inches(0.2), tile_top + Inches(0.15), tile_w - Inches(0.4), Inches(0.8),
                 big, size=32, bold=True, color=color)
        add_text(s, left + Inches(0.2), tile_top + Inches(0.95), tile_w - Inches(0.4), Inches(0.5),
                 sub, size=11, color=CHARCOAL)

    # Narrative below
    body_top = Inches(3.5)
    add_text(s, Inches(0.6), body_top, Inches(12), Inches(0.4),
             "What we teach by building it in", size=18, bold=True, color=NAVY)
    add_bullets(s, Inches(0.9), body_top + Inches(0.5), Inches(11.5), Inches(3),
                [
                    "Content-hash caching: don't re-pay for an unchanged document. The cache key is SHA-256(PDF) + rubric + model — change any one and you re-run, otherwise it's free.",
                    "Cost reporting at the source: python -m src.cost_report produces a real corpus-driven breakdown, monthly projection at a chosen volume, and ROI vs manual review. Engineers learn that AI cost is a tracked operational metric, not a mystery.",
                    "Model tiering is a deployment choice, not a personal preference: the cost report shows what each tier costs on real workloads, and the --model flag flips between them per-run.",
                    "Operational docs (RUNBOOK / SLA / ONBOARDING / CHANGELOG) ship with the tool, not after it. The Platinum tier of the hackathon explicitly requires them — so every output is adoptable, not just demoable.",
                ],
                title_size=14, body_size=12)
    footer_band(s, 6)


def slide_practice4(prs):
    s = add_blank_slide(prs)
    header_band(s, "Practice 4 — Every AI decision is auditable", "Platinum PR 3 — audit + governance")
    add_bullets(
        s,
        Inches(0.9),
        Inches(1.7),
        Inches(11.5),
        Inches(5),
        [
            ("One append-only line per validation",
             "Every CLI run and every API request writes one JSON line to "
             ".audit/validations.jsonl. Timestamp, source (cli/api), principal, "
             "document name + SHA-256, model, cache hit, finding counts, cost. "
             "Finance-log grade."),
            ("Principals are attributed safely",
             "CLI runs are attributed to the OS user — automatic, no extra config. "
             "API calls are attributed to a SHA-256 hash of the bearer token (\"tok_a1b2c3d4\"). "
             "The raw token is never logged. Solves attribution without creating a "
             "secret-leak risk."),
            ("Tied to the rubric version",
             "Rubric changes get a rubric/YYYY-MM-DD git tag. Audit entries reference "
             "the rubric and model in force at the time. \"Why did this doc pass in March "
             "and fail in May?\" is a one-line answer."),
            ("Reviewable on demand",
             "python -m src.audit_report --last 50 --source api --principal tok_a1b2 "
             "renders a Rich table with summary footer. The governance scaffolding "
             "answers \"who ran what\" without a special tool."),
        ],
        title_size=18,
        body_size=14,
    )
    footer_band(s, 7)


def slide_practice5(prs):
    s = add_blank_slide(prs)
    header_band(s, "Practice 5 — AI tools deserve runbooks too", "Platinum PR 4 — service management")
    add_bullets(
        s,
        Inches(0.9),
        Inches(1.7),
        Inches(11.5),
        Inches(5),
        [
            ("RUNBOOK.md",
             "Day-to-day operation: how to start the CLI and the HTTP service, where "
             "the cache and audit live, every common failure mode with its fix "
             "(cert chain on corporate networks, 401s, 400s, cache corruption), "
             "P0–P3 escalation, smoke test for any change."),
            ("SLA.md",
             "Uptime, latency (per tier and per model), accuracy (recall ≥90%, precision "
             "≥80% on the labelled fixture set), and cost targets. Honest about "
             "hackathon-stage maturity. Quarterly acceptance test included."),
            ("ONBOARDING.md",
             "Part 1: how a new operator gets running, end to end. Part 2: how an "
             "adopter swaps the rubric, parser, and fixtures for a new domain. The "
             "same harness validates BIM today and HR policy tomorrow."),
            ("CHANGELOG.md",
             "Tier-grouped history backfilled from git, with a documented per-PR "
             "maintenance process. Engineers learn that \"what changed\" is a "
             "user-facing artifact, not just a log."),
            ("Why this matters for AI tooling specifically",
             "Tools that ship without these docs become orphans when the original "
             "author moves on. AI-assisted dev makes it cheap to ship tools — and "
             "therefore cheap to create orphans. The Platinum tier makes the "
             "paperwork the default, not an afterthought."),
        ],
        title_size=16,
        body_size=13,
    )
    footer_band(s, 8)


def slide_governance(prs):
    s = add_blank_slide(prs)
    header_band(s, "The governance model", "Four roles · Four workflows")

    # Two-column layout: roles on the left, workflows on the right
    col_w = Inches(6.0)
    col_top = Inches(1.7)
    col_h = Inches(5.0)
    col_left_1 = Inches(0.6)
    col_left_2 = Inches(0.6 + 6.0 + 0.4)

    # Left column — roles
    add_rect(s, col_left_1, col_top, col_w, Inches(0.6), NAVY)
    add_text(s, col_left_1 + Inches(0.2), col_top + Inches(0.1), col_w - Inches(0.4), Inches(0.4),
             "Roles (GOVERNANCE.md)", size=18, bold=True, color=WHITE)
    add_rect(s, col_left_1, col_top + Inches(0.6), col_w, col_h - Inches(0.6), LIGHT_BG)
    add_bullets(s,
                col_left_1 + Inches(0.25),
                col_top + Inches(0.8),
                col_w - Inches(0.5),
                col_h - Inches(0.9),
                [
                    ("Product owner",
                     "Owns the rubric and the roadmap. Signs off releases."),
                    ("Maintainer",
                     "Reviews + merges PRs. Holds the API key and the service token."),
                    ("Operator",
                     "Runs the tool day-to-day. Monitors cost. Archives audit trails."),
                    ("Domain reviewer",
                     "Subject-matter expert (e.g. BIM specialist). Arbitrates false-positive escalations."),
                ],
                title_size=14, body_size=11)

    # Right column — workflows
    add_rect(s, col_left_2, col_top, col_w, Inches(0.6), ACCENT)
    add_text(s, col_left_2 + Inches(0.2), col_top + Inches(0.1), col_w - Inches(0.4), Inches(0.4),
             "Workflows", size=18, bold=True, color=WHITE)
    add_rect(s, col_left_2, col_top + Inches(0.6), col_w, col_h - Inches(0.6), LIGHT_BG)
    add_bullets(s,
                col_left_2 + Inches(0.25),
                col_top + Inches(0.8),
                col_w - Inches(0.5),
                col_h - Inches(0.9),
                [
                    ("Access control",
                     "Personal API keys; HTTP service requires API_TOKEN; raw secrets never logged."),
                    ("Rubric change workflow",
                     "PR → Domain reviewer sign-off → Maintainer merge → rubric/YYYY-MM-DD git tag."),
                    ("False-positive escalation",
                     "Capture audit entry → file issue → decide rubric tweak vs documented exception → close."),
                    ("Service management",
                     "RUNBOOK / SLA / ONBOARDING / CHANGELOG. Quarterly acceptance test confirms the deployment still meets targets."),
                ],
                title_size=14, body_size=11)

    footer_band(s, 9)


def slide_recommendations(prs):
    s = add_blank_slide(prs)
    header_band(s, "What we're recommending", "Standardise the practices, scale the governance")
    add_bullets(
        s,
        Inches(0.9),
        Inches(1.7),
        Inches(11.5),
        Inches(5),
        [
            ("Run the hackathon format quarterly",
             "Every developer, every business, every domain. The format teaches the "
             "practices in two days that ad-hoc \"just use Claude\" learning takes a year "
             "to surface — and often surfaces by going wrong first."),
            ("Require Platinum-tier governance for any AI-built tool that ships",
             "If a tool produced via AI-assisted development is going to be used by anyone "
             "outside its author's team, it ships with RUNBOOK + SLA + ONBOARDING + "
             "CHANGELOG + GOVERNANCE. Non-negotiable."),
            ("Named owner per tool",
             "Every AI-built tool has a named Product owner, Maintainer, Operator, and "
             "Domain reviewer before it leaves hackathon stage. The roles are in "
             "GOVERNANCE.md — fill them in or don't ship."),
            ("Standardise on the rubric-as-config pattern",
             "Domain rules belong in plain-text config files (markdown, YAML), version "
             "controlled, reviewable as PRs. Not buried in prompt strings. This is the "
             "single highest-leverage pattern the hackathon teaches."),
            ("Track cost the same way we track other operational metrics",
             "Every tool reports its own cost via a cost_report module. Surface the "
             "totals in the same dashboards as compute, storage, and licences. AI is an "
             "operational cost, not a magic line item."),
        ],
        title_size=16,
        body_size=13,
    )
    footer_band(s, 10)


def slide_thanks(prs):
    s = add_blank_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, NAVY)
    add_rect(s, 0, Inches(3.6), SLIDE_W, Inches(0.08), ACCENT)
    add_text(
        s,
        Inches(0.8),
        Inches(2.4),
        SLIDE_W - Inches(1.6),
        Inches(1.2),
        "Thank you  ·  Questions?",
        size=48,
        bold=True,
        color=WHITE,
    )
    add_text(
        s,
        Inches(0.8),
        Inches(3.8),
        SLIDE_W - Inches(1.6),
        Inches(0.6),
        "github.com/stephencummins/mace-hackathon",
        size=20,
        color=WHITE,
    )
    add_text(
        s,
        Inches(0.8),
        Inches(4.4),
        SLIDE_W - Inches(1.6),
        Inches(0.6),
        "Slack: maice-workspace.slack.com",
        size=16,
        color=WHITE,
    )
    add_text(
        s,
        Inches(0.8),
        Inches(5.2),
        SLIDE_W - Inches(1.6),
        Inches(0.5),
        "Governance reference: GOVERNANCE · RUNBOOK · SLA · ONBOARDING · CHANGELOG",
        size=14,
        color=ACCENT,
    )


# --- Build --------------------------------------------------------------------

def build() -> Path:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide_title(prs)
    slide_why(prs)
    slide_format(prs)
    slide_practice1(prs)
    slide_practice2(prs)
    slide_practice3(prs)
    slide_practice4(prs)
    slide_practice5(prs)
    slide_governance(prs)
    slide_recommendations(prs)
    # No separate thanks slide — recommendations is the natural close;
    # but we render a closing slide because the deck spec is 10 slides
    # body + 1 closing, matching the CXO deck shape.
    slide_thanks(prs)

    out = Path(__file__).parent / "mace-dev-governance-deck.pptx"
    prs.save(out)
    return out


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path} ({path.stat().st_size:,} bytes)")
