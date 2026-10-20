"""Write one SVG card per experience (dark + light) into timeline/.

The README stacks them, each inside its own link, so every stop on the timeline
is clickable (GitHub strips scripts and hover CSS, but keeps links on plain <img>).
Cards always use the dark surface: GitHub unwraps <picture> out of <a>, which breaks
the link, so there is no light/dark swap here.
Run: python scripts/make-timeline.py
"""

import textwrap
from html import escape
from pathlib import Path

W, H = 1200, 224
SPINE = 236
MONO = "'IBM Plex Mono',Consolas,'SFMono-Regular',Menlo,monospace"
SANS = "'Schibsted Grotesk','Segoe UI',Helvetica,Arial,sans-serif"

THEMES = {
    "dark": dict(bg="#1d2025", fg="#ece8e0", muted="#a3a7ae", rule="#ece8e0",
                 cyan="#4fb3c2", amber="#e3a83f", chip="#262a30"),
}

# Facts mirror portfolio/src/data/experience.ts. Keep them in sync; never invent.
EXPERIENCES = [
    dict(slug="aarm", when=("APR to SEP", "2026"), org="AARM Health Inc.",
         role="AI & FULL STACK INTERN  ·  REMOTE, CALIFORNIA",
         detail="Built and shipped Maya, an LLM medical assistant with intent classification and an "
                "agentic pipeline, plus a write-path safety layer that controls what the model may commit.",
         tags=["NODE", "POSTGRES", "REACT", "AWS", "AGENTS"], live=True),
    dict(slug="kcl", when=("JUN to JUL", "2026"), org="King's College London",
         role="VISITING RESEARCH INTERN",
         detail="Multimodal Vision Transformers and CLIP for skin-lesion classification with clinical "
                "metadata: fusion, text baselines and robustness studies.",
         tags=["VIT", "CLIP", "FUSION", "PYTORCH"]),
    dict(slug="cloudsprint", when=("JUN to JUL", "2025"), org="Cloudsprint Technologies / Trovex.ai",
         role="SOFTWARE DEVELOPMENT TRAINEE",
         detail="React.js components and REST API integrations for production applications.",
         tags=["REACT", "REST", "PRODUCT"]),
    dict(slug="lnmiit", when=("SUMMER", "2024"), org="LNMIIT · LUSIP",
         role="RESEARCH INTERN  ·  DR. PREETY SINGH",
         detail="A Selenium + ETL pipeline over 6,000+ Reddit pairs, and a neural sentiment classifier "
                "trained on it.",
         tags=["SELENIUM", "ETL", "NLP"]),
]


def card(e, c, first, last):
    lines = textwrap.wrap(e["detail"], 104)[:2]
    top = 0 if not first else 64
    bot = H if not last else 64
    node_y = 64
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>')
    # spine + node
    o.append(f'<line x1="{SPINE}" y1="{top}" x2="{SPINE}" y2="{bot}" stroke="{c["rule"]}" stroke-opacity=".22"/>')
    if e.get("live"):
        o.append(f'<circle class="pulse" cx="{SPINE}" cy="{node_y}" r="9" fill="none" stroke="{c["cyan"]}"/>')
    col = c["cyan"] if e.get("live") else c["amber"]
    o.append(f'<path d="M{SPINE} {node_y - 8}L{SPINE + 8} {node_y}L{SPINE} {node_y + 8}L{SPINE - 8} {node_y}Z" fill="{col}"/>')
    # date
    o.append(f'<text x="{SPINE - 30}" y="{node_y - 2}" text-anchor="end" font-family="{MONO}" font-size="15" letter-spacing="1.5" fill="{c["muted"]}">{e["when"][0]}</text>')
    o.append(f'<text x="{SPINE - 30}" y="{node_y + 26}" text-anchor="end" font-family="{SANS}" font-size="30" font-weight="700" fill="{c["fg"]}">{e["when"][1]}</text>')
    # card frame that draws itself in
    x0, y0, cw, ch = 276, 22, W - 276 - 24, H - 44
    o.append(f'<rect class="frame" x="{x0}" y="{y0}" width="{cw}" height="{ch}" fill="none" stroke="{c["rule"]}" stroke-opacity=".2" pathLength="100"/>')
    o.append(f'<line x1="{SPINE + 10}" y1="{node_y}" x2="{x0}" y2="{node_y}" stroke="{c["rule"]}" stroke-opacity=".22" stroke-dasharray="2 4"/>')
    # copy
    tx = x0 + 26
    o.append(f'<text x="{tx}" y="{y0 + 40}" font-family="{SANS}" font-size="25" font-weight="700" fill="{c["fg"]}">{escape(e["org"])}</text>')
    o.append(f'<text x="{x0 + cw - 22}" y="{y0 + 36}" text-anchor="end" font-family="{MONO}" font-size="13" letter-spacing="1.5" fill="{c["amber"]}">OPEN &#8599;</text>')
    o.append(f'<text x="{tx}" y="{y0 + 64}" font-family="{MONO}" font-size="13" letter-spacing="1.5" fill="{c["cyan"]}">{escape(e["role"])}</text>')
    for i, ln in enumerate(lines):
        o.append(f'<text x="{tx}" y="{y0 + 94 + i * 23}" font-family="{SANS}" font-size="17" fill="{c["muted"]}">{escape(ln)}</text>')
    # tags
    cx = tx
    cy = y0 + ch - 34
    for i, t in enumerate(e["tags"]):
        w = len(t) * 8.4 + 22
        o.append(f'<g class="chip" style="animation-delay:{0.5 + i * 0.12:.2f}s">'
                 f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="22" fill="{c["chip"]}" stroke="{c["rule"]}" stroke-opacity=".15"/>'
                 f'<text x="{cx + 11:.0f}" y="{cy + 15}" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{c["fg"]}">{t}</text></g>')
        cx += w + 8
    body = "\n  ".join(o)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(e["org"])}, {escape(e["role"].title())}, {" ".join(e["when"]).lower()}">
  <style>
    .frame {{ stroke-dasharray: 100; stroke-dashoffset: 100; animation: draw 1.4s ease-out .1s forwards; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0 }} }}
    .chip {{ opacity: 0; animation: in .5s ease-out forwards; }}
    @keyframes in {{ to {{ opacity: 1 }} }}
    .pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 2.2s ease-out infinite; }}
    @keyframes pulse {{ 0% {{ transform: scale(.8); opacity: .9 }} 100% {{ transform: scale(2.2); opacity: 0 }} }}
    @media (prefers-reduced-motion: reduce) {{ .frame,.chip,.pulse {{ animation: none; stroke-dashoffset: 0; opacity: 1 }} }}
  </style>
  {body}
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "timeline"
    out.mkdir(exist_ok=True)
    n = len(EXPERIENCES)
    for i, e in enumerate(EXPERIENCES):
        (out / f"{i + 1:02d}-{e['slug']}.svg").write_text(card(e, THEMES["dark"], i == 0, i == n - 1), encoding="utf-8")
    print("wrote", n, "cards to timeline/")
