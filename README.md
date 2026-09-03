# The Illustrated Guide to Using AI

A simple picture-book map of **how people use AI** — not how models are built or trained.

It is meant for the same job as *The Illustrated Guide to Kubernetes*: give professionals and leaders a shared language they can finish in one sitting.

**Story:** Luma, a small fox with a lantern, leaves a crowded chat booth and learns the harbor: prompts, models, agents, crews, skills, harnesses, MCP, and loops.

- Live HTML: [GitHub Pages](https://wahrsoft.github.io/illustrated-guide-to-using-ai/)
- PDF: [book/Illustrated_Guide_to_Using_AI.pdf](book/Illustrated_Guide_to_Using_AI.pdf)

## What’s in the book

| Harbor figure | Concept |
|---|---|
| The folded note | Prompt / prompt engineering |
| Leo the library lion | LLM |
| Vee the serving kitchen | vLLM (self-hosted serving — not frontier) |
| Scout the pocket mouse | SLM |
| Dom the shopkeeper | SDM (specialized domain model) |
| The backpack | Agents |
| The supervisor crate | Crews / supervisors |
| Recipe folders | Skills |
| Safety rigging | Harnesses |
| Universal docks | MCP |
| The garden path | Loops |
| Fog, fences, checklists | Hallucinations, grounding, evals, routing, workflows, cost |

Also covered: context window, memory, vector stores, tools, guardrails, human-in-the-loop, crews, context engineering.

## Repository layout

```
docs/index.html          Publishable HTML book
docs/images/             Images used by the HTML
images/                  Canonical illustration primitives
book/*.pdf               Generated PDF
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

The builder looks for typefaces under common system paths (Libre Baskerville, Lora, Playfair Display) and falls back to Liberation / DejaVu Serif.

## Publish the HTML

The site is the `docs/` folder. The publishing pipeline **runs on `main`**:

1. Push changes under `docs/` to `main`
2. `.github/workflows/pages.yml` copies `docs/` onto the `gh-pages` branch
3. GitHub Pages serves `https://wahrsoft.github.io/illustrated-guide-to-using-ai/`

You can also trigger **Actions → Publish Pages from main → Run workflow**.

Repo **Settings → Pages** should stay:

- Source: **Deploy from a branch**
- Branch: `gh-pages` / folder: `/ (root)`

Do not use the `github-pages` environment + `actions/deploy-pages` path. That environment rejects deploys from `main`.

Local preview:

```bash
python3 -m http.server -d docs 8000
```

## License

Text and original characters: [CC BY 4.0](LICENSE).

Illustrations were generated for this project and may be reused with the book.

Inspired by the spirit of CNCF’s *Illustrated Children’s Guide to Kubernetes* — a story people can actually finish.
