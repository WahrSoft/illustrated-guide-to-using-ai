#!/usr/bin/env python3
"""Decode images/*.jpg.b64 into images/ and docs/images/."""
from pathlib import Path
import base64
import shutil

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images"
DOC = ROOT / "docs" / "images"
DOC.mkdir(parents=True, exist_ok=True)

count = 0
for b64 in sorted(SRC.glob("*.jpg.b64")):
    raw = base64.b64decode(b64.read_text().encode("ascii"))
    dest = SRC / b64.name.replace(".b64", "")
    dest.write_bytes(raw)
    shutil.copy2(dest, DOC / dest.name)
    print("wrote", dest.relative_to(ROOT), len(raw))
    count += 1
print(f"decoded {count} images")
