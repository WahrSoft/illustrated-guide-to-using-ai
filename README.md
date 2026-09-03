# The Illustrated Guide to Using AI

A simple picture-book map of **how people use AI** — not how models are built or trained.

**Story:** Luma, a small fox with a lantern, leaves a crowded chat booth and learns the harbor: prompts, models, agents, crews, skills, harnesses, MCP, and loops.

- Live HTML: [GitHub Pages](https://wahrsoft.github.io/illustrated-guide-to-using-ai/)
- PDF: [latest release download](https://github.com/WahrSoft/illustrated-guide-to-using-ai/releases/latest/download/Illustrated_Guide_to_Using_AI.pdf)
- Releases: [github.com/WahrSoft/illustrated-guide-to-using-ai/releases](https://github.com/WahrSoft/illustrated-guide-to-using-ai/releases)

A push or merge to `main` that touches `src/`, `images/`, or the PDF workflow rebuilds the book and replaces the **book** release asset.

## Repository layout

```
docs/index.html          Illustrated HTML book (Pages homepage)
docs/images/             Images used by the HTML
images/                  Canonical illustration primitives
src/build_pdf.py         Rebuild the PDF
src/story.md             Story and panel copy
requirements.txt         Python deps for the PDF builder
```

## Rebuild the PDF locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/build_pdf.py
```

Output: `book/Illustrated_Guide_to_Using_AI.pdf`

The builder looks for Libre Baskerville / Lora / Playfair, then Liberation or DejaVu, then macOS Times/Georgia, then ReportLab’s built-in Times.

## Publish the HTML

The book is `docs/index.html`. Set **Settings → Pages** to `main` / `/docs`.

## License

Text and original characters: [CC BY 4.0](LICENSE).
