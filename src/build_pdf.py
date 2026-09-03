#!/usr/bin/env python3
"""Build The Illustrated Guide to Using AI — landscape picture-book explainer PDF."""

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
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
        "LB": ["/usr/share/fonts/SlidesCarnival/google/Libre Baskerville/static/LibreBaskerville-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
        "LB-Bold": ["/usr/share/fonts/SlidesCarnival/google/Libre Baskerville/static/LibreBaskerville-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
        "LB-Italic": ["/usr/share/fonts/SlidesCarnival/google/Libre Baskerville/static/LibreBaskerville-Italic.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"],
        "Lora": ["/usr/share/fonts/SlidesCarnival/google/Lora/static/Lora-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
        "Lora-Bold": ["/usr/share/fonts/SlidesCarnival/google/Lora/static/Lora-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
        "Lora-Italic": ["/usr/share/fonts/SlidesCarnival/google/Lora/static/Lora-Italic.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"],
        "Playfair": ["/usr/share/fonts/SlidesCarnival/google/Playfair Display/static/PlayfairDisplay-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
        "Playfair-Bold": ["/usr/share/fonts/SlidesCarnival/google/Playfair Display/static/PlayfairDisplay-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
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
    lines = wrap_text(c, body, "LB", 8.5, w - 28)
    yy = y + h - 34
    c.setFillColor(INK)
    for line in lines:
        if yy < y + 10:
            break
        c.setFont("LB", 8.5)
        c.drawString(x + 14, yy, line)
        yy -= 11


def image_fit(path, max_w, max_h):
    ir = ImageReader(str(path))
    iw, ih = ir.getSize()
    scale = min(max_w / iw, max_h / ih)
    return iw * scale, ih * scale


def _spread(c, image_name, title, story, panel_title, panel_body, page_num, accent=TEAL):
    draw_bg(c)
    img = IMG / image_name
    margin = 0.4 * inch
    w, h = image_fit(img, PAGE_W - 2 * margin, PAGE_H - 3.3 * inch)
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
    w, h = image_fit(img, PAGE_W - 2 * margin, PAGE_H - 2.1 * inch)
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
    draw_wrapped(c, "For the professionals and leaders who have to explain AI in a room where half the people are certain and the other half are lost — and for anyone who needs a shared language without a research paper.", 1.7 * inch, PAGE_H - 2.35 * inch, "Lora-Italic", 12, PAGE_W - 3.4 * inch, leading=18)
    draw_wrapped(c, "This book is about using AI, not building or training models. The story is a vehicle. The panels are the brief.", 1.7 * inch, PAGE_H - 3.85 * inch, "LB", 10, PAGE_W - 3.4 * inch, leading=15, color=TEAL)
    draw_footer(c, 2)


def page_opening(c):
    draw_bg(c)
    img = IMG / "chat-booth.jpg"
    margin = 0.45 * inch
    w, h = image_fit(img, PAGE_W * 0.52, PAGE_H - 2.6 * inch)
    c.drawImage(str(img), margin, PAGE_H - margin - h - 0.1 * inch, width=w, height=h, preserveAspectRatio=True, mask="auto")
    tx = margin + w + 0.35 * inch
    ty = PAGE_H - 0.7 * inch
    max_text = PAGE_W - tx - margin
    c.setFillColor(NAVY)
    c.setFont("Playfair-Bold", 14)
    c.drawString(tx, ty, "Once upon a time…")
    h1 = draw_wrapped(c, "Once upon a time there was a little question named Luma. She had one wish and a tiny lantern of curiosity.", tx, ty - 0.35 * inch, "LB", 10, max_text, leading=14)
    h2 = draw_wrapped(c, "She lived in a crowded chat booth, where answers arrived like paper airplanes and blew away. The booth could talk. It could not do.", tx, ty - 0.35 * inch - h1 - 0.2 * inch, "LB", 10, max_text, leading=14)
    draw_wrapped(c, "Luma wished for a place where questions could grow into work.", tx, ty - 0.35 * inch - h1 - h2 - 0.4 * inch, "LB-Italic", 10, max_text, leading=14, color=TEAL)
    draw_panel(c, margin, 0.45 * inch, PAGE_W - 2 * margin, 1.15 * inch, "IN PRACTICE", "A chat box answers once and forgets. A working AI system keeps context, uses tools, and turns a request into finished work.", accent=CORAL)
    draw_footer(c, 3)


def page_prompt(c):
    _spread(c, "prompts.jpg", "The Folded Note — Prompts", "Captain Context sat Luma down. “A well-folded note names the job, the audience, the constraints, and what done looks like.” Luma folded one glowing airplane: picnic for four, no nuts, ready by sunset.", "PROMPT / PROMPT ENGINEERING", "A prompt is the instruction. Prompt engineering is writing it so the job is hard to misread.", 4, MUSTARD)

def page_llm(c):
    _spread(c, "llm-library-lion.jpg", "The Great Library Lion — LLM", "Leo the lion had read so many stories he could start almost any one. Luma asked for a picnic plan. Leo wrote a beautiful plan. Then he sat still. The plan was words. The picnic was not packed.", "LLM — LARGE LANGUAGE MODEL", "A general-purpose thinking engine. By itself it does not fetch calendars, open files, or pack sandwiches.", 5, TEAL)

def page_vllm(c):
    _spread(c, "vllm-kitchen.jpg", "The Busy Serving Kitchen — vLLM", "Vee the octopus fed the lions who live in this harbor. “The mountain lions — frontier models — are too big for my ovens. Their layers ride four or five huge ships. Their recipes are already compiled.”", "vLLM — A SERVING KITCHEN, NOT THE FRONTIER", "vLLM serves models you host yourself. Frontier models run compiled tensors across several H200-class servers, with almost no CPU in the hot path.", 6, CORAL)

def page_slm(c):
    _spread(c, "slm-pocket-mouse.jpg", "The Pocket Mouse — SLM", "Scout the mouse popped from Luma’s pocket. “I don’t know every story in the mountain. I know enough for the path right here. I run on a little lamp.” Some jobs needed the lion. Some jobs needed the mouse.", "SLM — SMALL LANGUAGE MODEL", "A compact model. Often runs on a laptop or phone. Choose an SLM when good, fast, and nearby beats enormous and far away.", 7, MUSTARD)

def page_sdm(c):
    _spread(c, "sdm-shopkeeper.jpg", "The Neighborhood Shopkeeper — SDM", "Dom the raccoon sold only maps of this neighborhood. “I do not bake cakes. I do not sail ships. Ask me which alley has the bakery, and I will not guess.”", "SDM — SPECIALIZED DOMAIN MODEL", "A model trained or tuned for one kind of work. Narrow on purpose. Sharp on purpose.", 8, TEAL)

def page_agents(c):
    _spread(c, "agents-backpack.jpg", "The Backpack — Agents", "Captain Context buckled a backpack onto Luma. “An agent does not only answer. An agent acts.” Luma was still a question. Now she was a question that could work.", "AGENTS", "A model wrapped in permission to use tools. It plans, acts, looks, and continues until the job is done — or a human must decide.", 9, CORAL)

def page_crews(c):
    _spread(c, "crews-supervisor.jpg", "The Harbor Crew — Supervisors", "The captain climbed onto a crate marked SUPERVISOR. “One backpack can pack a basket. A picnic for the whole dock needs a crew. I assign. I check. I stop the work when it is good enough.”", "CREWS / SUPERVISORS", "Teams usually work with a supervisor who assigns specialist agents, checks their work, and decides when to stop.", 10, MUSTARD)

def page_skills(c):
    _spread(c, "skills-shelf.jpg", "The Recipe Shelf — Skills", "A shelf of slim folders stood in the workshop. “These are Skills,” said Scout. “You open the right folder when the job matches.”", "SKILLS", "Reusable playbooks for agents — short instructions, checklists, and sometimes little scripts.", 11, MUSTARD)

def page_harness(c):
    _spread(c, "harness-rigging.jpg", "The Safety Rigging — Harnesses", "“This is the Harness,” said the captain. “It holds your tools. It watches your steps. It stops you at the cliff edge.”", "HARNESSES", "The runtime around an agent: loop runner, permissions, logs, tests, memory, budgets, and stop rules.", 12, TEAL)

def page_mcp(c):
    _spread(c, "mcp-docks.jpg", "The Universal Dock — MCP", "Along the pier were sockets of every color. A sign read MCP. “Before MCP, every tool spoke a private language. Now a dock is a dock.”", "MCP — MODEL CONTEXT PROTOCOL", "An open standard that lets models talk to tools and data sources through one kind of connection.", 13, CORAL)

def page_loops(c):
    _spread(c, "loops-garden.jpg", "The Garden Path — Loops", "A round garden path had four stones: THINK · ACT · LOOK · AGAIN. Luma walked it until the basket was ready.", "LOOPS", "The heartbeat of an agent. Decide when to continue, retry, ask a person, and stop.", 14, MUSTARD)


def page_friends(c):
    draw_bg(c)
    c.setFillColor(NAVY)
    c.setFont("Playfair-Bold", 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 0.6 * inch, "Other Friends at the Harbor")
    friends = [
        ("Context Window", "Luma’s satchel. At ~200k pages, stuffing scraps first mattered less than looking things up."),
        ("Memory", "Jars of glowing beads. Some last an afternoon. Some last seasons."),
        ("Vector store", "A map cabinet you search directly. Old RAG is largely left behind."),
        ("Tools", "Skills teach how. Tools do."),
        ("Guardrails", "A painted fence along the cliff. Kind, firm, not optional."),
        ("Human-in-the-loop", "For big choices, Luma waves. A person waves back."),
        ("Crews", "Specialist agents plus a supervisor who assigns, checks, and stops."),
        ("Context engineering", "Choosing what rides with the ask: examples, files, history, live lookups."),
    ]
    y = PAGE_H - 1.05 * inch
    left = 0.7 * inch
    col_w = (PAGE_W - 1.6 * inch) / 2
    for i, (title, body) in enumerate(friends):
        col, row = i % 2, i // 2
        x = left + col * (col_w + 0.25 * inch)
        yy = y - row * 1.35 * inch
        c.setFillColor(SOFT_TEAL if i % 2 == 0 else SOFT_MUSTARD)
        c.roundRect(x, yy - 1.05 * inch, col_w, 1.15 * inch, 6, fill=1, stroke=0)
        c.setFillColor(TEAL if i % 2 == 0 else MUSTARD)
        c.setFont("LB-Bold", 10)
        c.drawString(x + 12, yy - 0.22 * inch, title)
        draw_wrapped(c, body, x + 12, yy - 0.42 * inch, "LB", 8.5, col_w - 24, leading=11.5)
    draw_footer(c, 15)


def page_quality(c):
    draw_bg(c)
    c.setFillColor(NAVY)
    c.setFont("Playfair-Bold", 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 0.55 * inch, "Fog, Fences, and Checklists")
    items = [
        ("Hallucinations", "When Leo invents a bakery that is not there. Fluent is not the same as true."),
        ("Grounding", "Tying answers to fetched pages, tools, and systems of record."),
        ("Evals", "A checklist for the picnic. Did it pack what we asked? Can we measure that?"),
        ("Routing", "Mountain jobs to Leo. Pocket jobs to Scout. Alley jobs to Dom."),
        ("Workflows", "A fixed path of steps. An agent wanders the loop. A workflow follows the recipe."),
        ("Tokens & cost", "Every page in the satchel has a price. Long loops and big lions cost more."),
    ]
    y = PAGE_H - 1.35 * inch
    left = 0.7 * inch
    col_w = (PAGE_W - 1.6 * inch) / 2
    for i, (title, body) in enumerate(items):
        col, row = i % 2, i // 2
        x = left + col * (col_w + 0.25 * inch)
        yy = y - row * 1.7 * inch
        c.setFillColor(SOFT_CORAL if i % 2 == 0 else SOFT_TEAL)
        c.roundRect(x, yy - 1.4 * inch, col_w, 1.5 * inch, 6, fill=1, stroke=0)
        c.setFillColor(CORAL if i % 2 == 0 else TEAL)
        c.setFont("LB-Bold", 11)
        c.drawString(x + 14, yy - 0.28 * inch, title)
        draw_wrapped(c, body, x + 14, yy - 0.52 * inch, "LB", 9.5, col_w - 28, leading=13)
    draw_footer(c, 16)


def page_ending(c):
    _spread(c, "ending-picnic.jpg", "Home", "Together they packed the picnic. The folded note made the job clear. Skills kept the order. The harness kept the path safe. MCP plugged in the calendar. The loop walked until the work was done.", "THE END", "Luma had found her harbor. And she lived usefully ever after.", 17, TEAL)


def page_cast(c):
    draw_bg(c)
    c.setFillColor(NAVY)
    c.setFont("Playfair-Bold", 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 0.55 * inch, "Cast of Characters")
    cast = [
        ("Luma", "The request itself — a fox kit with a lantern of curiosity."),
        ("The Folded Note", "A prompt — the ask, constraints, and definition of done."),
        ("Leo", "The Library Lion — a Large Language Model (LLM)."),
        ("Vee", "The serving kitchen (vLLM), not how frontier lions run."),
        ("Scout", "The pocket mouse — a Small Language Model (SLM)."),
        ("Dom", "The raccoon shopkeeper — a Specialized Domain Model (SDM)."),
        ("Captain Context", "The owl — supervisor, context, and the agent’s backpack."),
        ("The Crew", "Specialist agents under a supervisor."),
        ("Skills", "Recipe folders — reusable playbooks."),
        ("The Harness", "Safety rigging — permissions, logs, budgets, stop rules."),
        ("MCP Docks", "Universal plugs — Model Context Protocol."),
        ("The Loop", "Think · Act · Look · Again."),
    ]
    y = PAGE_H - 0.95 * inch
    for name, desc in cast:
        c.setFillColor(TEAL)
        c.setFont("LB-Bold", 10)
        c.drawString(0.9 * inch, y, name)
        c.setFillColor(INK)
        c.setFont("LB", 9.5)
        c.drawString(2.6 * inch, y, desc)
        y -= 0.38 * inch
    draw_footer(c, 18)


def page_glossary(c):
    draw_bg(c)
    c.setFillColor(NAVY)
    c.setFont("Playfair-Bold", 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 0.5 * inch, "Field Glossary")
    items = [
        ("Prompt", "The instruction given to a model."),
        ("Prompt engineering", "Writing that instruction so it is hard to misread."),
        ("Context engineering", "Choosing what else rides with the prompt."),
        ("LLM", "Large Language Model — broad general reasoning."),
        ("vLLM", "Open serving stack for hosted models — not frontier serving."),
        ("SLM", "Small Language Model — efficient, often on-device."),
        ("SDM", "Specialized Domain Model — narrow expert."),
        ("Agent", "Model + tools + loop that acts toward a goal."),
        ("Crew", "Supervisor plus specialist agents."),
        ("Skill", "Reusable playbook an agent can load."),
        ("Harness", "Runtime around the agent."),
        ("MCP", "Model Context Protocol — standard tool connections."),
        ("Loop", "Reason → act → observe → decide."),
        ("Vector store", "Searchable notes beside the model. Replaced most RAG."),
        ("Hallucination", "A fluent, confident answer that is not true."),
        ("Grounding", "Tying answers to retrieved sources and live systems."),
        ("Evals", "Tests that measure whether the system did the job."),
        ("Routing", "Sending each job to the right model."),
        ("Workflow", "A fixed sequence of steps."),
        ("Guardrails", "Policy and safety limits."),
        ("Human-in-the-loop", "A person approves high-impact steps."),
    ]
    y = PAGE_H - 0.85 * inch
    for term, defn in items:
        c.setFillColor(CORAL)
        c.setFont("LB-Bold", 8)
        c.drawString(0.65 * inch, y, term)
        c.setFillColor(INK)
        c.setFont("LB", 8)
        c.drawString(2.35 * inch, y, defn)
        y -= 0.31 * inch
    draw_footer(c, 19)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=landscape(letter))
    c.setTitle("The Illustrated Guide to Using AI")
    c.setAuthor("Inspired by the Phippy tradition")
    pages = [page_cover, page_dedication, page_opening, page_prompt, page_llm, page_vllm, page_slm, page_sdm, page_agents, page_crews, page_skills, page_harness, page_mcp, page_loops, page_friends, page_quality, page_ending, page_cast, page_glossary]
    for i, fn in enumerate(pages):
        fn(c)
        if i < len(pages) - 1:
            c.showPage()
    c.save()
    print(f"Wrote {OUT}")
    print(f"Pages: {len(pages)}")


if __name__ == "__main__":
    main()
