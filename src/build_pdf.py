#!/usr/bin/env python3
"""Build The Illustrated Guide to Using AI — landscape picture-book explainer PDF."""

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pathlib import Path

PAGE_W, PAGE_H = landscape(letter)

CREAM = HexColor("#FBF6EE")
INK = HexColor("#2C2A26")
TEAL = HexColor("#2A6F7A")
CORAL = HexColor("#D96B5B")
MUSTARD = HexColor("#D4A84B")
NAVY = HexColor("#1E3A5F")
SOFT_TEAL = HexColor("#E8F2F3")
SOFT_CORAL = HexColor("#FCEDEA")
SOFT_MUSTARD = HexColor("#F8F0DC")
PANEL_BG = HexColor("#F0E9DC")
RULE = HexColor("#C9BDA8")


def _register_fonts():
    candidates = {
        "LB": [
            "/usr/share/fonts/SlidesCarnival/google/Libre Baskerville/static/LibreBaskerville-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ],
        "LB-Bold": [
            "/usr/share/fonts/SlidesCarnival/google/Libre Baskerville/static/LibreBaskerville-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        ],
        "LB-Italic": [
            "/usr/share/fonts/SlidesCarnival/google/Libre Baskerville/static/LibreBaskerville-Italic.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
        ],
        "Lora": [
            "/usr/share/fonts/SlidesCarnival/google/Lora/static/Lora-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ],
        "Lora-Bold": [
            "/usr/share/fonts/SlidesCarnival/google/Lora/static/Lora-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        ],
        "Lora-Italic": [
            "/usr/share/fonts/SlidesCarnival/google/Lora/static/Lora-Italic.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
        ],
        "Playfair": [
            "/usr/share/fonts/SlidesCarnival/google/Playfair Display/static/PlayfairDisplay-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ],
        "Playfair-Bold": [
            "/usr/share/fonts/SlidesCarnival/google/Playfair Display/static/PlayfairDisplay-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        ],
    }
    for name, paths in candidates.items():
        for p in paths:
            if Path(p).exists():
                pdfmetrics.registerFont(TTFont(name, p))
                break
        else:
            raise FileNotFoundError(f"No font available for {name}")


_register_fonts()

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "images"
OUT = ROOT / "book" / "Illustrated_Guide_to_Using_AI.pdf"


def draw_bg(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def draw_footer(c, page_num, total=19):
    c.setFillColor(RULE)
    c.setFont("LB", 8)
    c.drawCentredString(PAGE_W / 2, 0.28 * inch, f"— {page_num} —")


def wrap_text(c, text, font, size, max_width):
    c.setFont(font, size)
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if c.stringWidth(test, font, size) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(c, text, x, y, font, size, max_width, leading=None, color=INK):
    if leading is None:
        leading = size * 1.35
    c.setFillColor(color)
    lines = wrap_text(c, text, font, size, max_width)
    for i, line in enumerate(lines):
        c.setFont(font, size)
        c.drawString(x, y - i * leading, line)
    return len(lines) * leading


def draw_panel(c, x, y, w, h, title, body, accent=TEAL):
    c.setFillColor(PANEL_BG)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
    c.setStrokeColor(accent)
    c.setLineWidth(2.5)
    c.line(x + 10, y + h - 2, x + w - 10, y + h - 2)
    c.setFillColor(accent)
    c.setFont("LB-Bold", 9)
    c.drawString(x + 14, y + h - 18, title)
    max_w = w - 28
    leading = 11
    c.setFillColor(INK)
    lines = wrap_text(c, body, "LB", 8.5, max_w)
    yy = y + h - 34
    for line in lines:
        if yy < y + 10:
            break
        c.setFont("LB", 8.5)
        c.drawString(x + 14, yy, line)
        yy -= leading


def image_fit(path, max_w, max_h):
    ir = ImageReader(str(path))
    iw, ih = ir.getSize()
    scale = min(max_w / iw, max_h / ih)
    return iw * scale, ih * scale


def _spread(c, image_name, title, story, panel_title, panel_body, page_num, accent=TEAL):
    draw_bg(c)
    img = IMG / image_name
    margin = 0.4 * inch
    max_w = PAGE_W - 2 * margin
    max_h = PAGE_H - 3.3 * inch
    w, h = image_fit(img, max_w, max_h)
    c.drawImage(str(img), (PAGE_W - w) / 2, PAGE_H - margin - h, width=w, height=h, preserveAspectRatio=True, mask="auto")
    c.setFillColor(NAVY)
    c.setFont("Playfair-Bold", 13)
    c.drawCentredString(PAGE_W / 2, PAGE_H - margin - h - 0.28 * inch, title)
    draw_wrapped(c, story, 0.7 * inch, PAGE_H - margin - h - 0.55 * inch, "LB", 9.5, PAGE_W - 1.4 * inch, leading=13)
    draw_panel(c, 0.45 * inch, 0.4 * inch, PAGE_W - 0.9 * inch, 1.2 * inch, panel_title, panel_body, accent=accent)
    draw_footer(c, page_num)


def page_cover(c):
    draw_bg(c)
    img = IMG / "cover-harbor-cast.jpg"
    margin = 0.4 * inch
    max_w = PAGE_W - 2 * margin
    max_h = PAGE_H - 2.1 * inch
    w, h = image_fit(img, max_w, max_h)
    x = (PAGE_W - w) / 2
    y = PAGE_H - margin - h - 0.15 * inch
    c.drawImage(str(img), x, y, width=w, height=h, preserveAspectRatio=True, mask="auto")
    c.setFillColor(NAVY)
    c.setFont("Playfair-Bold", 22)
    c.drawCentredString(PAGE_W / 2, 1.15 * inch, "The Illustrated Guide to Using AI")
    c.setFont("Lora-Italic", 12)
    c.setFillColor(TEAL)
    c.drawCentredString(PAGE_W / 2, 0.85 * inch, "How Luma Learned to Get Things Done")
    c.setFont("LB", 8)
    c.setFillColor(RULE)
    c.drawCentredString(PAGE_W / 2, 0.45 * inch, "A shared language for professionals and leaders")


def page_dedication(c):
    draw_bg(c)
    c.setFillColor(NAVY)
    c.setFont("Playfair-Bold", 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 1.5 * inch, "A simple map for a noisy field")
    c.setStrokeColor(MUSTARD)
    c.setLineWidth(1.5)
    c.line(PAGE_W / 2 - 1.2 * inch, PAGE_H - 1.75 * inch, PAGE_W / 2 + 1.2 * inch, PAGE_H - 1.75 * inch)
    body = "For the professionals and leaders who have to explain AI in a room where half the people are certain and the other half are lost — and for anyone who needs a shared language without a research paper."
    draw_wrapped(c, body, 1.7 * inch, PAGE_H - 2.35 * inch, "Lora-Italic", 12, PAGE_W - 3.4 * inch, leading=18, color=INK)
    note = "This book is about using AI, not building or training models. The story is a vehicle. The panels are the brief. Read it in ten minutes, then use the same pictures when you brief a team, a board, or a customer."
    draw_wrapped(c, note, 1.7 * inch, PAGE_H - 3.85 * inch, "LB", 10, PAGE_W - 3.4 * inch, leading=15, color=TEAL)
    note2 = "The harbor is the working system around a model: how you ask, which helper you send, what the helper is allowed to touch, how it checks its work, and when a person steps in."
    draw_wrapped(c, note2, 1.7 * inch, PAGE_H - 5.15 * inch, "LB", 10, PAGE_W - 3.4 * inch, leading=15, color=INK)
    c.setFont("LB", 9)
    c.setFillColor(RULE)
    c.drawCentredString(PAGE_W / 2, 1.2 * inch, "In the spirit of The Illustrated Guide to Kubernetes — a story people can actually finish")
    draw_footer(c, 2)


def page_opening(c):
    draw_bg(c)
    img = IMG / "chat-booth.jpg"
    margin = 0.45 * inch
    max_w = PAGE_W * 0.52
    max_h = PAGE_H - 2.6 * inch
    w, h = image_fit(img, max_w, max_h)
    c.drawImage(str(img), margin, PAGE_H - margin - h - 0.1 * inch, width=w, height=h, preserveAspectRatio=True, mask="auto")
    tx = margin + w + 0.35 * inch
    ty = PAGE_H - 0.7 * inch
    max_text = PAGE_W - tx - margin
    c.setFillColor(NAVY)
    c.setFont("Playfair-Bold", 14)
    c.drawString(tx, ty, "Once upon a time…")
    h1 = draw_wrapped(c, "Once upon a time there was a little question named Luma. She was a simple question. She had one wish and a tiny lantern of curiosity.", tx, ty - 0.35 * inch, "LB", 10, max_text, leading=14)
    h2 = draw_wrapped(c, "She lived in a crowded chat booth, where answers arrived like paper airplanes… and then blew away. Every time Luma came back, nobody remembered her. The booth could talk. It could not do.", tx, ty - 0.35 * inch - h1 - 0.2 * inch, "LB", 10, max_text, leading=14)
    draw_wrapped(c, "Luma wished for a place where questions could grow into work.", tx, ty - 0.35 * inch - h1 - h2 - 0.4 * inch, "LB-Italic", 10, max_text, leading=14, color=TEAL)
    draw_panel(c, margin, 0.45 * inch, PAGE_W - 2 * margin, 1.15 * inch, "IN PRACTICE", "A chat box answers once and forgets. A working AI system keeps context, uses tools, and turns a request into finished work — a plan, a file, a booked event, a checked list.", accent=CORAL)
    draw_footer(c, 3)


def page_prompt(c):
    _spread(c, "prompts.jpg", "The Folded Note — Prompts", "Before Luma met the lion, Captain Context sat her down at a desk of paper airplanes. “The ask is the first tool,” said the captain. “A crumpled note gets a crumpled day. A well-folded note names the job, the audience, the constraints, and what done looks like.” Luma folded one glowing airplane: picnic for four, no nuts, ready by sunset, include a shopping list.", "PROMPT / PROMPT ENGINEERING", "A prompt is the instruction you give a model. Prompt engineering is the craft of writing that instruction so the job, constraints, format, and definition of done are unmistakable. It is still the cheapest lever in the harbor — and it is not the last one.", 4, MUSTARD)


def page_llm(c):
    _spread(c, "llm-library-lion.jpg", "The Great Library Lion — LLM", "A vast, gentle lion padded out of a library the size of a mountain. His mane was made of pages. “I am Leo,” he said. “I am a Large Language Model. I have read so many stories that I can help you start almost any one.” Luma asked for a picnic plan. Leo wrote a beautiful plan. Then he sat very still. The plan was words. The picnic was not packed.", "LLM — LARGE LANGUAGE MODEL", "A general-purpose thinking engine that reads your words and writes useful words back. Wonderful at explaining, drafting, summarizing, and planning. By itself it does not fetch your calendar, open your files, or pack the sandwiches.", 5, TEAL)


def page_vllm(c):
    _spread(c, "vllm-kitchen.jpg", "The Busy Serving Kitchen — vLLM", "Behind Leo’s library was a kitchen that never slept. An octopus named Vee danced between stoves. “I feed the lions who live in this harbor,” said Vee. “The mountain lions — the frontier models — are too big for my ovens. Their layers ride four or five huge ships. Their recipes are already compiled. Almost no waiters run between plates.”", "vLLM — A SERVING KITCHEN, NOT THE FRONTIER", "vLLM batches requests for models you host yourself. Most people talking to a frontier model are not using it. Those models spread layers across several H200-class servers, run compiled tensors, and keep almost no CPU work in the hot path.", 6, CORAL)


def page_slm(c):
    draw_bg(c)
    img = IMG / "slm-pocket-mouse.jpg"
    margin = 0.45 * inch
    max_w = PAGE_W * 0.50
    max_h = PAGE_H - 2.7 * inch
    w, h = image_fit(img, max_w, max_h)
    c.drawImage(str(img), margin, PAGE_H - margin - h, width=w, height=h, preserveAspectRatio=True, mask="auto")
    tx = margin + w + 0.35 * inch
    max_text = PAGE_W - tx - margin
    ty = PAGE_H - 0.75 * inch
    c.setFillColor(NAVY)
    c.setFont("Playfair-Bold", 13)
    c.drawString(tx, ty, "The Pocket Mouse — SLM")
    h1 = draw_wrapped(c, "A mouse popped from Luma’s pocket. “I’m Scout,” she squeaked. “I don’t know every story in the mountain. I know enough for the path right here. I run on a little lamp. I am quick. I am quiet. I can work when the mountain library is far away.”", tx, ty - 0.35 * inch, "LB", 10, max_text, leading=14)
    draw_wrapped(c, "Some jobs needed the lion. Some jobs needed the mouse.", tx, ty - 0.35 * inch - h1 - 0.25 * inch, "LB-Italic", 10, max_text, leading=14, color=TEAL)
    draw_panel(c, margin, 0.4 * inch, PAGE_W - 2 * margin, 1.25 * inch, "SLM — SMALL LANGUAGE MODEL", "A compact model that uses less power and memory. Often runs on a laptop or phone. Best at focused everyday tasks. Choose an SLM when “good, fast, and nearby” beats “enormous and far away.”", accent=MUSTARD)
    draw_footer(c, 7)


def page_sdm(c):
    _spread(c, "sdm-shopkeeper.jpg", "The Neighborhood Shopkeeper — SDM", "On a side street stood a tiny shop with one perfect window. A raccoon named Dom sold only maps of this neighborhood. “I am a Specialized Domain Model,” said Dom. “I do not bake cakes. I do not sail ships. Ask me which alley has the bakery, and I will not guess.” Luma asked about the bakery alley. Dom answered in one breath.", "SDM — SPECIALIZED DOMAIN MODEL", "A model trained or tuned for one kind of work — medicine notes, legal clauses, warehouse codes, one company’s voice. Narrow on purpose. Sharp on purpose.", 8, TEAL)


def page_agents(c):
    _spread(c, "agents-backpack.jpg", "The Backpack — Agents", "“Talking is only the first step,” said Captain Context at the harbor. He buckled a backpack onto Luma. Inside were tools: a key, a pencil, a looking-glass, a tiny boat. “An agent does not only answer,” said the captain. “An agent acts.” Luma stood taller. She was still a question. Now she was a question that could work.", "AGENTS", "A model wrapped in permission to use tools. It plans a step, does the step, sees what happened, and continues until the job is done — or until it must ask a human. One agent is a worker with a backpack.", 9, CORAL)


def page_crews(c):
    _spread(c, "crews-supervisor.jpg", "The Harbor Crew — Supervisors", "On a bigger job the captain did not send Luma alone. He climbed onto a crate marked SUPERVISOR and pointed. “One backpack can pack a basket. A picnic for the whole dock needs a crew. I assign. I check. I stop the work when it is good enough.” A mouse checked the list. A raccoon read the map. A sparrow wrote the invitation.", "CREWS / SUPERVISORS", "Teams usually work with a supervisor — a boss or orchestrator — who assigns specialist agents, checks their work, and decides when to stop. A crew is not a pile of chat windows. It is a small company with a captain.", 10, MUSTARD)
