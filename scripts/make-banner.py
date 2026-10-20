"""Write banner-dark.svg and banner-light.svg for the profile README.

Palette mirrors the portfolio (sirjansingh.dev) tokens: paper, ink, graphite,
and three restrained signals (cyan, cobalt, amber). Run: python scripts/make-banner.py
"""

import random
from pathlib import Path

W, H = 1200, 360
THEMES = {
    "dark": dict(bg="#1d2025", fg="#ece8e0", muted="#a3a7ae", rule="#ece8e0", star="#ece8e0",
                 cyan="#4fb3c2", amber="#e3a83f", suit="#ece8e0", visor="#2a6fd6"),
    "light": dict(bg="#f7f3ec", fg="#1c1f24", muted="#5d6168", rule="#1c1f24", star="#1c1f24",
                  cyan="#1f8796", amber="#b87a12", suit="#ffffff", visor="#2f5bb5"),
}


def stars(c):
    rnd = random.Random(7)
    out = []
    for i in range(70):
        x, y = rnd.uniform(30, W - 30), rnd.uniform(30, H - 30)
        if x < 640 and 70 < y < 300:  # keep the text area clean
            continue
        r = rnd.choice([0.8, 1.0, 1.2, 1.6])
        out.append(f'<circle class="tw t{i % 3}" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c["star"]}"/>')
    return "\n    ".join(out)


def diamond(x, y, c, s=5):
    return f'<path d="M{x} {y - s}L{x + s} {y}L{x} {y + s}L{x - s} {y}Z" fill="{c["amber"]}"/>'


def svg(c):
    mono = "'IBM Plex Mono',Consolas,'SFMono-Regular',Menlo,monospace"
    sans = "'Schibsted Grotesk','Segoe UI',Helvetica,Arial,sans-serif"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sirjan Singh. ML and AI engineer. Figure out how things work, break them, build something better.">
  <style>
    .tw {{ animation: tw 4s ease-in-out infinite; }}
    .t1 {{ animation-delay: -1.3s; }} .t2 {{ animation-delay: -2.6s; }}
    @keyframes tw {{ 0%,100% {{ opacity: .15 }} 50% {{ opacity: .8 }} }}
    .float {{ animation: float 7s ease-in-out infinite; transform-origin: 930px 180px; }}
    @keyframes float {{ 0%,100% {{ transform: translate(0,0) rotate(-8deg) }} 50% {{ transform: translate(-10px,-14px) rotate(6deg) }} }}
    .orbit {{ animation: spin 18s linear infinite; transform-origin: 930px 180px; }}
    @keyframes spin {{ to {{ transform: rotate(360deg) }} }}
    .rocket {{ animation: fly 11s linear infinite; }}
    @keyframes fly {{ 0% {{ transform: translate(-80px,40px); opacity:0 }} 8% {{ opacity:1 }} 70% {{ opacity:1 }} 85%,100% {{ transform: translate(560px,-260px); opacity:0 }} }}
    .caret {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0 }} }}
    @media (prefers-reduced-motion: reduce) {{ .tw,.float,.orbit,.rocket,.caret {{ animation: none }} }}
  </style>
  <rect width="{W}" height="{H}" fill="{c["bg"]}"/>
  <g>
    {stars(c)}
  </g>

  <!-- hairline frame with diamond corners -->
  <rect x="18" y="18" width="{W - 36}" height="{H - 36}" fill="none" stroke="{c["rule"]}" stroke-opacity=".18"/>
  {diamond(18, 18, c)} {diamond(W - 18, 18, c)} {diamond(18, H - 18, c)} {diamond(W - 18, H - 18, c)}

  <!-- copy -->
  <text x="64" y="88" font-family="{mono}" font-size="15" letter-spacing="2.5" fill="{c["cyan"]}">SS / 001   ML + AI ENGINEER</text>
  <text x="60" y="176" font-family="{sans}" font-size="84" font-weight="700" letter-spacing="-2" fill="{c["fg"]}">Sirjan Singh</text>
  <text x="64" y="224" font-family="{sans}" font-size="23" fill="{c["muted"]}">Figure out how things work. Break them. Build something better.<tspan class="caret" fill="{c["amber"]}"> _</tspan></text>
  <line x1="64" y1="258" x2="610" y2="258" stroke="{c["rule"]}" stroke-opacity=".18"/>
  <text x="64" y="292" font-family="{mono}" font-size="14" letter-spacing="1" fill="{c["muted"]}">LNMIIT '27  <tspan fill="{c["amber"]}">&#9670;</tspan>  ex-research intern, King's College London  <tspan fill="{c["amber"]}">&#9670;</tspan>  sirjansingh.dev</text>
  <text x="{W - 64}" y="62" text-anchor="end" font-family="{mono}" font-size="12" letter-spacing="2" fill="{c["amber"]}">TRANSMISSION: YOOOOO</text>

  <!-- orbit + astronaut -->
  <ellipse cx="930" cy="180" rx="150" ry="150" fill="none" stroke="{c["rule"]}" stroke-opacity=".14" stroke-dasharray="2 7"/>
  <g class="orbit"><circle cx="1080" cy="180" r="5" fill="{c["cyan"]}"/></g>
  <g class="float">
    <rect x="904" y="196" width="52" height="56" rx="16" fill="{c["suit"]}" stroke="{c["rule"]}" stroke-opacity=".35"/>
    <rect x="884" y="200" width="22" height="40" rx="8" fill="{c["suit"]}" stroke="{c["rule"]}" stroke-opacity=".35"/>
    <rect x="890" y="204" width="14" height="30" rx="6" fill="{c["rule"]}" fill-opacity=".12"/>
    <rect x="950" y="204" width="34" height="14" rx="7" fill="{c["suit"]}" stroke="{c["rule"]}" stroke-opacity=".35" transform="rotate(-28 950 210)"/>
    <rect x="910" y="246" width="16" height="30" rx="7" fill="{c["suit"]}" stroke="{c["rule"]}" stroke-opacity=".35"/>
    <rect x="934" y="246" width="16" height="30" rx="7" fill="{c["suit"]}" stroke="{c["rule"]}" stroke-opacity=".35"/>
    <circle cx="930" cy="168" r="34" fill="{c["suit"]}" stroke="{c["rule"]}" stroke-opacity=".35"/>
    <rect x="906" y="152" width="48" height="30" rx="14" fill="{c["visor"]}"/>
    <rect x="914" y="157" width="14" height="6" rx="3" fill="#ffffff" fill-opacity=".55"/>
    <rect x="918" y="212" width="24" height="12" rx="3" fill="{c["amber"]}"/>
  </g>

  <!-- rocket crossing -->
  <g class="rocket">
    <g transform="translate(700 320) rotate(-62)">
      <path d="M0 -14 C6 -8 6 6 4 10 L-4 10 C-6 6 -6 -8 0 -14Z" fill="{c["fg"]}"/>
      <path d="M-4 6 L-8 12 L-4 10Z M4 6 L8 12 L4 10Z" fill="{c["cyan"]}"/>
      <path d="M-2 11 L0 20 L2 11Z" fill="{c["amber"]}"/>
    </g>
  </g>
</svg>
'''


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    for name, c in THEMES.items():
        (root / f"banner-{name}.svg").write_text(svg(c), encoding="utf-8")
        print("wrote", f"banner-{name}.svg")
