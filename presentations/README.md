# Presentations

Reproducible decks for the Mace Digital Compliance Checker. The Python
scripts are checked in; the rendered `.pptx` outputs are gitignored
because they regenerate deterministically from the scripts.

## Decks

| Script | Output | Audience | Length |
|---|---|---|---|
| `build_cxo_deck.py` | `mace-cxo-deck.pptx` | Mace CXOs — pitch to adopt the validator post-hackathon | 10 slides, 16:9 |
| `build_dev_governance_deck.py` | `mace-dev-governance-deck.pptx` | Mace engineering leadership — how the hackathon teaches AI-assisted dev practices + the governance model that ships with them | 10 slides, 16:9 |

Both decks share visual primitives (colours, fonts, header/footer bands,
bullet helpers) via `_deckkit.py`. Edit that file to change the look of
every deck at once.

## Build

```powershell
.\venv\Scripts\activate
pip install python-pptx       # one-time; not in requirements.txt
python presentations\build_cxo_deck.py
python presentations\build_dev_governance_deck.py
```

The output `.pptx` lands next to each script. Open in PowerPoint /
Keynote / LibreOffice Impress.

## Editing

Edit content in the Python script, not in PowerPoint — the script is the
source of truth so the deck stays in sync with what the repo actually
says. If a stat needs updating (cost numbers, test counts, etc.), grep
the script for the current value and update it there, then re-render.

Style changes (palette, fonts, header bands) go in `_deckkit.py` — both
decks pick up the change on next render.
