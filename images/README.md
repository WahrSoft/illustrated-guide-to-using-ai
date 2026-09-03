# Illustration primitives

Canonical drawings for *The Illustrated Guide to Using AI*.

GitHub's connector cannot store raw JPEGs in one shot, so each drawing is also stored as a sibling `.jpg.b64` file (standard base64 of the JPEG).

Restore the binaries:

```bash
python3 scripts/decode_images.py
```

That writes `images/*.jpg` and copies them to `docs/images/` for the HTML book.

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
