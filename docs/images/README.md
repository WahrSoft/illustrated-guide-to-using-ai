# Illustration primitives

Canonical drawings for *The Illustrated Guide to Using AI*.

The GitHub connector used to seed this repo truncates files around 2KB, so each JPEG is stored as numbered base64 parts:

```
images/cover-harbor-cast.jpg.b64.01
images/cover-harbor-cast.jpg.b64.02
...
```

Restore binaries (also copies into `docs/images/` for Pages):

```bash
python3 scripts/decode_images.py
```

Full-resolution originals and the print PDF live in the local working copy / release zip if you need them for `src/build_pdf.py`.

| File | Scene |
|---|---|
| `cover-harbor-cast.jpg` | Cover — Luma and the harbor cast |
| `chat-booth.jpg` | Opening — crowded chat booth |
| `prompts.jpg` | Prompt / prompt engineering |
| `llm-library-lion.jpg` | Leo the library lion (LLM) |
| `vllm-kitchen.jpg` | Vee the serving kitchen (vLLM) |
| `slm-pocket-mouse.jpg` | Scout the pocket mouse (SLM) |
| `sdm-shopkeeper.jpg` | Dom the shopkeeper (SDM) |
| `agents-backpack.jpg` | Agents |
| `skills-shelf.jpg` | Skills |
| `harness-rigging.jpg` | Harnesses |
| `mcp-docks.jpg` | MCP docks |
| `loops-garden.jpg` | Loops |
| `ending-picnic.jpg` | Closing picnic |
