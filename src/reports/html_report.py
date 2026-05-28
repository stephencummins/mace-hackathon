"""HTML rendering via Rich's recording Console + export_html."""

from __future__ import annotations

import io

from rich.console import Console

from src.reports.console_report import render_console
from src.runner import DocReport

_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Mace Compliance Report</title>
<style>
body {{ background: #fafafa; color: #222; font-family: -apple-system, Segoe UI, sans-serif; padding: 24px; }}
pre {{ background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 6px; overflow-x: auto; }}
{stylesheet}
</style>
</head>
<body>
<h1>Mace Digital Compliance Report</h1>
<p><em>ISO 19650 validation</em></p>
<pre><code>{code}</code></pre>
</body>
</html>
"""


def render_html(reports: list[DocReport]) -> str:
    # file=StringIO suppresses terminal output; record=True still captures into the buffer
    recording = Console(
        record=True,
        width=140,
        color_system="truecolor",
        force_terminal=True,
        file=io.StringIO(),
    )
    render_console(reports, recording)
    return recording.export_html(inline_styles=True, code_format=_HTML_TEMPLATE)
