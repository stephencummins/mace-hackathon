"""Generate the CXO-level deck for the Mace Digital Compliance Checker.

10 slides, 16:9, Mace-CXO audience. Run:

    python presentations/build_cxo_deck.py

Output:

    presentations/mace-cxo-deck.pptx

The deck is gitignored (regenerable artifact); this script is checked in
so anyone can rebuild it after editing.
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

# Deck-specific footer attribution
footer_band = partial(_footer_band, attribution="M+AI+CE Hackathon  ·  Mace Digital Compliance Checker")


# --- Slides -------------------------------------------------------------------

def slide_title(prs):
    s = add_blank_slide(prs)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, NAVY)
    add_rect(s, 0, Inches(3.4), SLIDE_W, Inches(0.08), ACCENT)
    add_text(
        s,
        Inches(0.8),
        Inches(2.2),
        SLIDE_W - Inches(1.6),
        Inches(1.2),
        "Mace Digital Compliance Checker",
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
        "AI-powered ISO 19650 validation",
        size=24,
        color=WHITE,
    )
    add_text(
        s,
        Inches(0.8),
        Inches(4.3),
        SLIDE_W - Inches(1.6),
        Inches(0.5),
        "Built in the M+AI+CE Hackathon  ·  2026",
        size=16,
        color=ACCENT,
    )
    add_text(
        s,
        Inches(0.8),
        SLIDE_H - Inches(0.9),
        SLIDE_W - Inches(1.6),
        Inches(0.4),
        "CXO briefing  ·  Confidential",
        size=12,
        color=WHITE,
    )


def slide_agenda(prs):
    s = add_blank_slide(prs)
    header_band(s, "Agenda", "What we'll cover in 20 minutes")
    items = [
        ("The problem", "BIM compliance review today: slow, expensive, inconsistent"),
        ("What we built", "A working validator for ISO 19650, end to end"),
        ("Results — measured", "Cost per document, ROI versus manual review, audit traceability"),
        ("Governance and risk", "Ownership, access, audit trail, rubric change control"),
        ("Adoption path", "From hackathon to department-owned tool"),
        ("The ask", "Pilot sponsor, named owner, fixture set"),
    ]
    add_bullets(s, Inches(0.9), Inches(1.7), Inches(11.5), Inches(5), items)
    footer_band(s, 2)


def slide_problem(prs):
    s = add_blank_slide(prs)
    header_band(s, "The problem", "ISO 19650 compliance is mandatory — and manual")
    add_bullets(
        s,
        Inches(0.9),
        Inches(1.7),
        Inches(11.5),
        Inches(5),
        [
            ("Mandatory on most public-sector and Tier 1 projects",
             "ISO 19650 is the international BIM information-management standard. "
             "Non-compliance is a contractual risk and a delivery-gate failure."),
            ("Manual review is slow and inconsistent",
             "A senior reviewer takes 10–20 minutes per document. Different reviewers "
             "flag different issues. Backlogs build up before delivery milestones."),
            ("Expensive — at scale, structural cost",
             "1,000 documents per month at 15 min each is ~250 reviewer-hours. "
             "At a fully loaded £60/hour that's £15,000/month of skilled time on "
             "checking, not designing."),
            ("Risk surfaces late",
             "Issues are found in batch reviews near delivery rather than at "
             "drafting time, when fixes are 10× more expensive."),
        ],
        title_size=18,
        body_size=14,
    )
    footer_band(s, 3)


def slide_solution(prs):
    s = add_blank_slide(prs)
    header_band(s, "What we built", "Four tiers, all live in the repo")
    items = [
        ("Bronze — filename / structure check",
         "Pure pattern match against PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-NUMBER_REVISION. "
         "Sub-second. No AI cost. Catches the bulk of routine errors."),
        ("Silver — Claude reads the content",
         "Claude Sonnet 4.6 (or Haiku for cost, Opus for depth) checks the document body "
         "against an ISO 19650 rubric: metadata, structure, suitability codes, revision history."),
        ("Gold — batch + reports + HTTP API",
         "Validate a folder; produce HTML / JSON reports; auto-suggested fixes; "
         "FastAPI service so it can plug into SharePoint or any document store."),
        ("Platinum — production-grade operations",
         "Document-level cache (free re-runs), cost reporting and ROI projection, "
         "audit trail with attributable principal, governance and service-management docs."),
    ]
    add_bullets(s, Inches(0.9), Inches(1.7), Inches(11.5), Inches(5), items, title_size=18, body_size=14)
    footer_band(s, 4)


def slide_architecture(prs):
    s = add_blank_slide(prs)
    header_band(s, "How it works", "One harness, swappable rubric")

    # Three column boxes
    box_w = Inches(3.8)
    box_h = Inches(4.2)
    box_top = Inches(1.7)
    gap = Inches(0.25)
    box_left_1 = Inches(0.6)
    box_left_2 = Inches(0.6 + 3.8 + 0.25)
    box_left_3 = Inches(0.6 + 2 * (3.8 + 0.25))

    for left, title, points, color in [
        (box_left_1, "Input", [
            "PDF on disk or uploaded over HTTP",
            "Anyone who can run a CLI or hit an authenticated endpoint",
            "Same harness validates BIM, contracts, RAMS, HR, finance — swap the rubric",
        ], NAVY),
        (box_left_2, "Validation", [
            "Bronze: regex on the filename — local, instant",
            "Silver: Claude reads the PDF, scores it against the rubric",
            "Cache: re-run on same doc + rubric + model is free (no API call)",
        ], ACCENT),
        (box_left_3, "Output", [
            "Console, HTML, or JSON report — pass / fail / warning per criterion",
            "One audit line per validation (who, what, when, cost)",
            "Cost report — per-model totals, monthly projection, ROI vs manual review",
        ], GREEN),
    ]:
        add_rect(s, left, box_top, box_w, Inches(0.5), color)
        add_text(s, left + Inches(0.2), box_top + Inches(0.08), box_w - Inches(0.4), Inches(0.4),
                 title, size=18, bold=True, color=WHITE)
        add_rect(s, left, box_top + Inches(0.5), box_w, box_h - Inches(0.5), LIGHT_BG)
        add_bullets(s,
                    left + Inches(0.25),
                    box_top + Inches(0.7),
                    box_w - Inches(0.5),
                    box_h - Inches(0.8),
                    points,
                    title_size=14,
                    body_size=12)

    footer_band(s, 5)


def slide_results(prs):
    s = add_blank_slide(prs)
    header_band(s, "Results — measured", "Numbers from real runs, not estimates")

    # Stat tiles
    tile_w = Inches(2.9)
    tile_h = Inches(1.8)
    tile_top = Inches(1.7)
    tile_left_start = Inches(0.6)
    gap = Inches(0.25)
    stats = [
        ("£0.003–£0.01", "Cost per document, Sonnet 4.6", NAVY),
        ("99.8%", "Cost saving vs. manual review at 1,000 docs/month", GREEN),
        ("0", "Cost of re-validating an unchanged document (cache hit)", ACCENT),
        ("72 / 72", "Test cases passing across the full validator", NAVY),
    ]
    for i, (big, sub, color) in enumerate(stats):
        left = tile_left_start + i * (tile_w + gap)
        add_rect(s, left, tile_top, tile_w, tile_h, LIGHT_BG)
        add_text(s, left + Inches(0.2), tile_top + Inches(0.25), tile_w - Inches(0.4), Inches(0.9),
                 big, size=36, bold=True, color=color)
        add_text(s, left + Inches(0.2), tile_top + Inches(1.1), tile_w - Inches(0.4), Inches(0.6),
                 sub, size=12, color=CHARCOAL)

    # Bottom narrative
    body_top = Inches(3.8)
    add_text(s, Inches(0.6), body_top, Inches(12), Inches(0.4),
             "What this means in practice", size=18, bold=True, color=NAVY)
    add_bullets(s, Inches(0.9), body_top + Inches(0.5), Inches(11.5), Inches(3),
                [
                    "At 1,000 BIM documents per month, today's manual cost is around £15,000/month of senior reviewer time. The validator delivers the same first-pass review for ~£25/month in Anthropic API charges.",
                    "Reviewers stop being the gate — they arbitrate flagged cases (false-positive escalation in GOVERNANCE.md). That's a few hours a week, not a few hundred.",
                    "Audit trail (.audit/validations.jsonl) attributes every decision to a principal — OS user for CLI, hashed bearer token for API. Finance-log grade.",
                    "Cache means the second run of an unchanged document costs nothing — important for the quarterly re-review cadence on long-lived projects.",
                ],
                title_size=14, body_size=12)
    footer_band(s, 6)


def slide_governance(prs):
    s = add_blank_slide(prs)
    header_band(s, "Governance and risk", "How this is safe to adopt")
    add_bullets(
        s,
        Inches(0.9),
        Inches(1.7),
        Inches(11.5),
        Inches(5),
        [
            ("Defined ownership",
             "Product owner, Maintainer, Operator, Domain reviewer — roles named in GOVERNANCE.md. "
             "The adopting department fills in named individuals."),
            ("Access control",
             "Personal Anthropic API keys; HTTP service refuses to start without API_TOKEN; "
             "raw tokens are never logged (audit stores a SHA-256 prefix instead)."),
            ("Rubric change workflow",
             "The rubric is plain markdown in source control. Changes are PRs with sign-off; "
             "merged commits get a rubric/YYYY-MM-DD git tag so the audit trail ties findings "
             "to the rubric version that produced them."),
            ("False-positive escalation",
             "Every disagreement becomes either a rubric improvement or a documented exception. "
             "Never silently overridden."),
            ("Data handling",
             "Documents pass through Anthropic per their data-usage terms. The cache and audit "
             "carry the same classification as the source documents. No third parties involved."),
        ],
        title_size=16,
        body_size=13,
    )
    footer_band(s, 7)


def slide_adoption(prs):
    s = add_blank_slide(prs)
    header_band(s, "Adoption path", "From hackathon to department-owned")

    # Three phase boxes horizontally
    box_w = Inches(3.95)
    box_h = Inches(4.4)
    box_top = Inches(1.7)
    box_left_1 = Inches(0.6)
    box_left_2 = Inches(0.6 + 3.95 + 0.2)
    box_left_3 = Inches(0.6 + 2 * (3.95 + 0.2))

    for left, phase, when, points, color in [
        (box_left_1, "Today", "Hackathon stage", [
            "Code lives in github.com/stephencummins/mace-hackathon",
            "Bronze + Silver + Gold + Platinum all working",
            "Operator runs the CLI on their laptop",
            "No SLA commitments — best-effort",
        ], MUTED),
        (box_left_2, "Phase 1", "Department pilot (1–3 months)", [
            "Fork into the department's GitHub org",
            "Fill in GOVERNANCE.md ownership table with names",
            "Build a labelled fixture set in the department's domain",
            "Run alongside manual review; compare results",
            "Re-baseline SLA.md targets against the new fixture set",
        ], ACCENT),
        (box_left_3, "Phase 2", "Production (6+ months)", [
            "Secrets in the department's secret manager (Key Vault / 1Password)",
            "Containerised HTTP service behind a reverse proxy",
            "99.5% uptime SLA, defined support hours",
            "Replaces first-pass manual review; reviewers arbitrate",
            "Onboard a second document type using the same harness",
        ], GREEN),
    ]:
        add_rect(s, left, box_top, box_w, Inches(0.7), color)
        add_text(s, left + Inches(0.2), box_top + Inches(0.08), box_w - Inches(0.4), Inches(0.35),
                 phase, size=18, bold=True, color=WHITE)
        add_text(s, left + Inches(0.2), box_top + Inches(0.4), box_w - Inches(0.4), Inches(0.3),
                 when, size=12, color=WHITE)
        add_rect(s, left, box_top + Inches(0.7), box_w, box_h - Inches(0.7), LIGHT_BG)
        add_bullets(s,
                    left + Inches(0.25),
                    box_top + Inches(0.9),
                    box_w - Inches(0.5),
                    box_h - Inches(1.0),
                    points,
                    title_size=14,
                    body_size=12)

    footer_band(s, 8)


def slide_ask(prs):
    s = add_blank_slide(prs)
    header_band(s, "What we're asking for", "To move from hackathon to pilot")
    add_bullets(
        s,
        Inches(0.9),
        Inches(1.7),
        Inches(11.5),
        Inches(5),
        [
            ("A pilot sponsor",
             "A named Mace executive who wants the first-pass review of ISO 19650 documents "
             "automated for one project or department."),
            ("A named operator",
             "Someone on the project team who runs the tool day-to-day and owns rotation, "
             "audit review, and escalation routing (see RUNBOOK.md)."),
            ("A labelled fixture set",
             "20–50 real documents with ground-truth pass/fail labels per criterion, "
             "from a Domain reviewer. This is what proves accuracy at department scale "
             "rather than just on the shipped examples."),
            ("Three months",
             "A pilot horizon long enough to measure cache hit rate (warm-up matters) and "
             "compare validator output to the manual review it's running alongside."),
            ("Then we decide",
             "Adopt and promote to production (Phase 2), iterate the rubric, or stop. "
             "Either way you have a clean audit trail of what was checked and what it cost."),
        ],
        title_size=18,
        body_size=14,
    )
    footer_band(s, 9)


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
        "Slack: maice-workspace.slack.com  ·  #technical-help",
        size=16,
        color=WHITE,
    )
    add_text(
        s,
        Inches(0.8),
        Inches(5.2),
        SLIDE_W - Inches(1.6),
        Inches(0.5),
        "Full operational docs:  README · GOVERNANCE · RUNBOOK · SLA · ONBOARDING · CHANGELOG",
        size=14,
        color=ACCENT,
    )


# --- Build --------------------------------------------------------------------

def build() -> Path:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide_title(prs)
    slide_agenda(prs)
    slide_problem(prs)
    slide_solution(prs)
    slide_architecture(prs)
    slide_results(prs)
    slide_governance(prs)
    slide_adoption(prs)
    slide_ask(prs)
    slide_thanks(prs)

    out = Path(__file__).parent / "mace-cxo-deck.pptx"
    prs.save(out)
    return out


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path} ({path.stat().st_size:,} bytes)")
