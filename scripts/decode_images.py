#!/usr/bin/env python3
"""Rebuild JPEGs from whole or chunked base64 primitives.

Looks in images/ for:
  - name.jpg.b64            (single file, if complete JPEG base64)
  - name.jpg.b64.01, .02…  (concatenated in numeric order)
Writes images/name.jpg and docs/images/name.jpg.
"""
from pathlib import Path
import base64
import shutil
import re

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images"
DOC = ROOT / "docs" / "images"
DOC.mkdir(parents=True, exist_ok=True)

part_re = re.compile(r"^(.+\.jpg)\.b64\.(\d+)$")

def assemble():
    parts = {}
    for p in SRC.iterdir():
        m = part_re.match(p.name)
        if m:
            parts.setdefault(m.group(1), []).append((int(m.group(2)), p))
    count = 0
    names = set(parts) | {p.name[:-4] for p in SRC.glob("*.jpg.b64")}
    for name in sorted(names):
        chunks = []
        if name in parts:
            for _, fp in sorted(parts[name]):
                chunks.append(fp.read_text().strip())
        whole = SRC / f"{name}.b64"
        if not chunks and whole.exists():
            chunks.append(whole.read_text().strip())
        text = "".join(chunks)
        if not text.startswith("/9j/"):
            print("skip incomplete", name, "len", len(text))
            continue
        try:
            raw = base64.b64decode(text.encode("ascii"), validate=False)
        except Exception as e:
            print("skip bad b64", name, e)
            continue
        if raw[:2] != b"\xff\xd8":
            print("skip not jpeg", name, "len", len(raw))
            continue
        dest = SRC / name
        dest.write_bytes(raw)
        shutil.copy2(dest, DOC / dest.name)
        print("wrote", dest.relative_to(ROOT), len(raw))
        count += 1
    print(f"decoded {count} images")

if __name__ == "__main__":
    assemble()
