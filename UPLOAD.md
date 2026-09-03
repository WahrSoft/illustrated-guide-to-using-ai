# Pushing the binary assets

The GitHub connector that seeds this repo truncates file bodies around 2KB. Whole JPEGs and the print PDF cannot go up in one API call.

In-repo workaround: store each web JPEG as numbered base64 parts (`images/name.jpg.b64.01`, `.02`, ...) and reassemble with:

```bash
python3 scripts/decode_images.py
```

That writes `images/*.jpg` and copies them to `docs/images/` before the Pages workflow publishes `docs/`.

## Status

- `agents-backpack` is fully chunked (parts 01-07) and decodes to a 320x214 web JPEG.
- The other 12 drawings still need the same treatment or a normal git push of the local binaries.

## Fast path from a machine that has the working copy

```bash
git clone https://github.com/WahrSoft/illustrated-guide-to-using-ai.git
cd illustrated-guide-to-using-ai
cp /path/to/local/repo/images/*.jpg images/
mkdir -p docs/images book
cp /path/to/local/repo/docs/images/*.jpg docs/images/
cp /path/to/local/repo/src/build_pdf.py src/
cp /path/to/local/repo/book/*.pdf book/
git add images docs book src scripts
git commit -m "Add illustrations, PDF, and rebuild primitives"
git push
```
