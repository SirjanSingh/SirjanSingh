"""Write one SVG card per project into projects/.

Facts mirror portfolio/src/data/portfolio.ts (the six projects on sirjansingh.dev).
Keep them in sync; never invent numbers. Each card links to its case study in the
README; GitHub keeps links on plain <img>, so cards always use the dark surface.
Run: python scripts/make-projects.py
"""

import textwrap
from html import escape
from pathlib import Path

W, H = 600, 340
MONO = "'IBM Plex Mono',Consolas,'SFMono-Regular',Menlo,monospace"
SANS = "'Schibsted Grotesk','Segoe UI',Helvetica,Arial,sans-serif"
C = dict(bg="#1d2025", fg="#ece8e0", muted="#a3a7ae", rule="#ece8e0", chip="#262a30")
ACCENT = {"cyan": "#4fb3c2", "amber": "#e3a83f", "green": "#6cbf8a"}

PROJECTS = [
    dict(slug="cassandra", title="Cassandra", kind="AGENT SUPERVISION", accent="cyan",
         badge="1ST PLACE · ARIZE",
         thesis="An agent that watches other agents fail, and verifies the repair.",
         result="Catches hallucinations, prompt drift and tool-call failures in under 10 seconds. "
                "5 supervision tools via cassandra-mcp.",
         stack=["PYTHON", "GOOGLE ADK", "GEMINI", "PHOENIX MCP"]),
    dict(slug="vendable", title="Vendable", kind="AGENT COMMERCE", accent="amber",
         thesis="Sometimes reliability means removing the model from the critical path.",
         result="Across 105 recorded negotiations, a 7-line statutory guard held every median "
                "on the published entitlement.",
         stack=["PYTHON", "MCP", "RAZORPAY"]),
    dict(slug="agentos", title="AgentOS", kind="AGENT OBSERVABILITY", accent="green",
         thesis="Agent execution should be inspectable while it is happening.",
         result="A real-time console for agent runs, human approvals, per-skill cost and outcomes.",
         stack=["TYPESCRIPT", "NODE", "REACT", "WEBSOCKETS"]),
    dict(slug="survivecity", title="SurviveCity", kind="MULTI-AGENT RL", accent="amber",
         badge="TOP 100 · META × PYTORCH",
         thesis="Reward design is part of the system, not a score added afterward.",
         result="Survival rate went from 15% to 60%, four times higher. "
                "3 reward-hacking exploits closed.",
         stack=["PYTORCH", "TRL", "GRPO", "LORA", "QWEN2.5-3B"]),
    dict(slug="contextual", title="Contextual", kind="REPO-AWARE RAG", accent="cyan",
         thesis="Retrieval quality is an evaluation problem before it is a generation problem.",
         result="30% better retrieval F1 than a semantic-only baseline, over 10k+ code chunks.",
         stack=["PYTHON", "FAISS", "BM25", "CROSS-ENCODER"]),
    dict(slug="claude-kit", title="claude-kit", kind="AGENT DEV TOOLING", accent="green",
         thesis="Guardrails should come from observed failure patterns, not intuition alone.",
         result="Open-source agent skills and guardrails scoped from counted telemetry. MIT licensed.",
         stack=["NODE", "PYTHON", "PLAYWRIGHT"]),
]


def card(i, p):
    a = ACCENT[p["accent"]]
    x0, y0, cw, ch = 14, 14, W - 28, H - 28
    tx = x0 + 26
    o = [f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>',
         f'<rect class="frame" x="{x0}" y="{y0}" width="{cw}" height="{ch}" fill="none" stroke="{C["rule"]}" stroke-opacity=".2" pathLength="100"/>',
         f'<rect class="bar" x="{x0}" y="{y0}" width="{cw}" height="3" fill="{a}"/>',
         f'<text x="{tx}" y="{y0 + 38}" font-family="{MONO}" font-size="12" letter-spacing="1.8" fill="{a}">P/{i:02d}  {escape(p["kind"])}</text>']
    if p.get("badge"):
        bw = len(p["badge"]) * 7.6 + 20
        bx = x0 + cw - 22 - bw
        o.append(f'<rect x="{bx:.0f}" y="{y0 + 22}" width="{bw:.0f}" height="22" fill="none" stroke="{ACCENT["amber"]}" stroke-opacity=".7"/>'
                 f'<text x="{bx + 10:.0f}" y="{y0 + 37}" font-family="{MONO}" font-size="11" letter-spacing="1.2" fill="{ACCENT["amber"]}">{escape(p["badge"])}</text>')
    o.append(f'<text x="{tx}" y="{y0 + 84}" font-family="{SANS}" font-size="36" font-weight="700" letter-spacing="-.5" fill="{C["fg"]}">{escape(p["title"])}</text>')
    y = y0 + 114
    for ln in textwrap.wrap(p["thesis"], 62, break_on_hyphens=False)[:2]:
        o.append(f'<text x="{tx}" y="{y}" font-family="{SANS}" font-size="17" font-style="italic" fill="{C["muted"]}">{escape(ln)}</text>')
        y += 23
    y += 12
    o.append(f'<line x1="{tx}" y1="{y - 6}" x2="{tx + 18}" y2="{y - 6}" stroke="{a}" stroke-width="2"/>')
    o.append(f'<text x="{tx + 26}" y="{y - 2}" font-family="{MONO}" font-size="11" letter-spacing="1.8" fill="{C["muted"]}">RESULT</text>')
    y += 20
    for ln in textwrap.wrap(p["result"], 68, break_on_hyphens=False)[:3]:
        o.append(f'<text x="{tx}" y="{y}" font-family="{SANS}" font-size="15.5" fill="{C["fg"]}">{escape(ln)}</text>')
        y += 21
    cx, cy = tx, y0 + ch - 42
    for j, t in enumerate(p["stack"]):
        w = len(t) * 7.6 + 18
        o.append(f'<g class="chip" style="animation-delay:{0.4 + j * 0.1:.2f}s">'
                 f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="22" fill="{C["chip"]}" stroke="{C["rule"]}" stroke-opacity=".15"/>'
                 f'<text x="{cx + 9:.0f}" y="{cy + 15}" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{C["fg"]}">{escape(t)}</text></g>')
        cx += w + 7
    o.append(f'<text x="{x0 + cw - 22}" y="{cy + 15}" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{a}">CASE STUDY &#8599;</text>')
    body = "\n  ".join(o)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(p["title"])}: {escape(p["thesis"])} {escape(p["result"])}">
  <style>
    .frame {{ stroke-dasharray: 100; stroke-dashoffset: 100; animation: draw 1.2s ease-out .1s forwards; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0 }} }}
    .bar {{ transform-box: fill-box; transform-origin: left; transform: scaleX(0); animation: grow .9s ease-out .2s forwards; }}
    @keyframes grow {{ to {{ transform: scaleX(1) }} }}
    .chip {{ opacity: 0; animation: in .5s ease-out forwards; }}
    @keyframes in {{ to {{ opacity: 1 }} }}
    @media (prefers-reduced-motion: reduce) {{ .frame,.bar,.chip {{ animation: none; stroke-dashoffset: 0; transform: none; opacity: 1 }} }}
  </style>
  {body}
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "projects"
    out.mkdir(exist_ok=True)
    for i, p in enumerate(PROJECTS, 1):
        (out / f"{i:02d}-{p['slug']}.svg").write_text(card(i, p), encoding="utf-8")
    print("wrote", len(PROJECTS), "cards to projects/")
