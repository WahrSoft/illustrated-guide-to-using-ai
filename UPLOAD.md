# Pushing the binary assets

The GitHub connector used to create this repo can write text files, but not multi-megabyte PDFs and JPEGs in one shot.

A complete local package is in the working copy: `images/`, `docs/images/`, `docs/index.html`, `src/build_pdf.py`, and `book/Illustrated_Guide_to_Using_AI.pdf`.

From a machine that has this folder:

```bash
git clone https://github.com/WahrSoft/illustrated-guide-to-using-ai.git
cd illustrated-guide-to-using-ai
cp -R /path/to/repo/* .
git add images docs book src scripts
git commit -m "Add illustrations, PDF, HTML book, and rebuild primitives"
git push
```

Then enable Pages: Settings → Pages → Deploy from branch `main` / `/docs`
(or allow the Actions workflow in `.github/workflows/pages.yml`).
