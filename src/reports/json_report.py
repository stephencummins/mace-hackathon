"""JSON rendering of DocReports."""

from __future__ import annotations

import json

from src.runner import DocReport


def render_json(reports: list[DocReport]) -> str:
    return json.dumps([report.to_json_dict() for report in reports], indent=2)
