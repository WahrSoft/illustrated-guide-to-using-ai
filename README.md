# The Illustrated Guide to Using AI

A simple picture-book map of **how people use AI** — not how models are built or trained.

It is meant for the same job as *The Illustrated Guide to Kubernetes*: give professionals and leaders a shared language they can finish in one sitting.

**Story:** Luma, a small fox with a lantern, leaves a crowded chat booth and learns the harbor: prompts, models, agents, skills, harnesses, MCP, and loops.

- Live HTML: [GitHub Pages](https://wahrsoft.github.io/illustrated-guide-to-using-ai/)
- PDF: [book/Illustrated_Guide_to_Using_AI.pdf](book/Illustrated_Guide_to_Using_AI.pdf)

## What’s in the book

| Harbor figure | Concept |
|---|---|
| The folded note | Prompt / prompt engineering |
| Leo the library lion | LLM |
| Vee the serving kitchen | vLLM |
| Scout the pocket mouse | SLM |
| Dom the shopkeeper | SDM (specialized domain model) |
| The backpack | Agents |
| Recipe folders | Skills |
| Safety rigging | Harnesses |
| Universal docks | MCP |
| The garden path | Loops |
| Fog, fences, checklists | Hallucinations, grounding, evals, routing, workflows, cost |

Also covered: context window, memory, RAG, tools, guardrails, human-in-the-loop, multi-agent work, context engineering.

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

GitHub Pages is configured from the `docs/` folder on `main`.

1. Repo **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / folder: `/docs`

Or rely on `.github/workflows/pages.yml` (Actions must be allowed to write Pages).

Local preview:

```bash
python3 -m http.server -d docs 8000
```

## License

Text and original characters: [CC BY 4.0](LICENSE).

Illustrations were generated for this project and may be reused with the book.

Inspired by the spirit of CNCF’s *Illustrated Children’s Guide to Kubernetes* — a story people can actually finish.
