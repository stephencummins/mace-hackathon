# Presentations

Reproducible decks for the Mace Digital Compliance Checker. The Python
scripts are checked in; the rendered `.pptx` outputs are gitignored
because they regenerate deterministically from the scripts.

## Decks

| Script | Output | Audience | Length |
|---|---|---|---|
| `build_cxo_deck.py` | `mace-cxo-deck.pptx` | Mace CXOs — pitch to adopt the validator post-hackathon | 10 slides, 16:9 |

## Build

```powershell
.\venv\Scripts\activate
pip install python-pptx       # one-time; not in requirements.txt
python presentations\build_cxo_deck.py
```

The output `.pptx` lands next to the script. Open in PowerPoint /
Keynote / LibreOffice Impress.

## Editing

Edit content in the Python script, not in PowerPoint — the script is the
source of truth so the deck stays in sync with what the repo actually
says. If a stat needs updating (cost numbers, test counts, etc.), grep
the script for the current value and update it there, then re-render.
