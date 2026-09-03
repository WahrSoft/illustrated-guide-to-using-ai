# The Illustrated Guide to Using AI

A simple picture-book map of **how people use AI** — not how models are built or trained.

**Story:** Luma, a small fox with a lantern, leaves a crowded chat booth and learns the harbor: prompts, models, agents, crews, skills, harnesses, MCP, and loops.

- Live HTML: [GitHub Pages](https://wahrsoft.github.io/illustrated-guide-to-using-ai/)
- Book page: [docs/index.html](docs/index.html)

## Repository layout

```
docs/index.html          Illustrated HTML book (Pages homepage)
docs/images/             Images used by the HTML
images/                  Canonical illustration primitives
src/build_pdf.py         Rebuild the PDF
src/story.md             Story and panel copy
requirements.txt         Python deps for the PDF builder
```

## Rebuild the PDF

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/build_pdf.py
```

Output: `book/Illustrated_Guide_to_Using_AI.pdf`

## Publish the HTML

The book is `docs/index.html`. A root `index.html` only redirects there so Pages never falls back to this README.

Set **Settings → Pages** to:

- Source: **Deploy from a branch**
- Branch: `main` / folder: `/docs`

That serves the illustrated book at the site root. `docs/.nojekyll` stops Jekyll from promoting a README.

## License

Text and original characters: [CC BY 4.0](LICENSE).
