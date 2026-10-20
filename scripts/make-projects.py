"""Write one SVG per project into projects/: a small animated sketch of how it works.

Facts mirror portfolio/src/data/portfolio.ts (the six projects on sirjansingh.dev).
Diagrams are schematic: the only numbers drawn are ones the portfolio states.
Cards always use the dark surface (GitHub drops <picture> out of links).
Run: python scripts/make-projects.py
"""

import textwrap
from html import escape
from pathlib import Path

W, H = 600, 330
MONO = "'IBM Plex Mono',Consolas,'SFMono-Regular',Menlo,monospace"
SANS = "'Schibsted Grotesk','Segoe UI',Helvetica,Arial,sans-serif"
BG, FG, MUTED, DIM = "#1d2025", "#ece8e0", "#a3a7ae", "#5b6068"
CYAN, AMBER, GREEN = "#4fb3c2", "#e3a83f", "#6cbf8a"

STYLE = """
    .draw { stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: draw 2.4s ease-out .2s forwards; }
    @keyframes draw { to { stroke-dashoffset: 0 } }
    .flow { stroke-dasharray: 4 6; animation: flow 1.2s linear infinite; }
    @keyframes flow { to { stroke-dashoffset: -20 } }
    .pulse { transform-box: fill-box; transform-origin: center; animation: pulse 1.8s ease-out infinite; }
    @keyframes pulse { 0% { transform: scale(.7); opacity: .9 } 100% { transform: scale(2.4); opacity: 0 } }
    .fade { opacity: 0; animation: fade .6s ease-out forwards; }
    @keyframes fade { to { opacity: 1 } }
    .slide { animation: slide 6s linear infinite; }
    @keyframes slide { from { transform: translateX(0) } to { transform: translateX(-120px) } }
    @media (prefers-reduced-motion: reduce) {
      .draw,.flow,.pulse,.fade,.slide { animation: none; stroke-dashoffset: 0; opacity: 1 }
    }
"""


def t(x, y, s, size=11, fill=MUTED, font=MONO, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def dot_on(path, color, dur, begin="0s", r=4):
    return (f'<circle r="{r}" fill="{color}"><animateMotion dur="{dur}" begin="{begin}" '
            f'repeatCount="indefinite" path="{path}"/></circle>')


def frame(title, kind, accent, caption, art, badge=None):
    o = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         t(28, 38, kind, 11, accent, extra='letter-spacing="1.8"'),
         t(28, 72, title, 32, FG, SANS, extra='font-weight="700" letter-spacing="-.5"')]
    if badge:
        o.append(t(W - 28, 38, badge, 11, AMBER, anchor="end", extra='letter-spacing="1.4"'))
    o.append(art)
    for i, ln in enumerate(textwrap.wrap(caption, 72, break_on_hyphens=False)[:2]):
        o.append(t(28, 284 + i * 21, ln, 15, FG, SANS))
    body = "\n  ".join(o)
    label = f"{title}. {caption}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="{escape(label)}">\n  <style>{STYLE}</style>\n  {body}\n</svg>\n')


def cassandra():
    xs = [48, 152, 256, 360, 464]
    labels = ["TRACES", "CLASSIFY", "ADV. TESTS", "PATCH", "REPLAY"]
    y = 140
    a = [f'<path class="draw" d="M{xs[0]} {y} H{xs[-1]}" stroke="{DIM}" fill="none"/>']
    for i, (x, lb) in enumerate(zip(xs, labels)):
        a.append(f'<path class="fade" style="animation-delay:{.2 + i * .25:.2f}s" '
                 f'd="M{x} {y - 7}L{x + 7} {y}L{x} {y + 7}L{x - 7} {y}Z" fill="{CYAN if i in (0, 4) else FG}"/>')
        a.append(t(x, y - 18, lb, 10.5, MUTED, anchor="middle", extra='letter-spacing="1.2"'))
    loop = f"M{xs[-1]} {y + 9} V{y + 54} H{xs[1]} V{y + 9}"
    a.append(f'<path class="flow" d="{loop}" stroke="{CYAN}" stroke-opacity=".7" fill="none"/>')
    a.append(t((xs[1] + xs[-1]) / 2, y + 72, "replay still fails? back to classify", 10.5, CYAN, anchor="middle"))
    a.append(dot_on(f"M{xs[0]} {y} H{xs[-1]} V{y + 54} H{xs[1]} V{y}", CYAN, "5s"))
    a.append(f'<path d="M{xs[-1] + 10} {y} H{xs[-1] + 26}" stroke="{FG}" stroke-opacity=".5"/>')
    a.append(t(xs[-1] + 32, y + 4, "resolve", 10.5, FG, extra='letter-spacing="1"'))
    return frame("Cassandra", "AGENT THAT SUPERVISES AGENTS", CYAN,
                 "Catches hallucinations, prompt drift and tool-call failures in under 10 seconds, "
                 "then proves the fix on the original failure.", "\n  ".join(a), "1ST PLACE · ARIZE")


def vendable():
    floor = 172
    a = [f'<line x1="40" y1="{floor}" x2="560" y2="{floor}" stroke="{DIM}" stroke-dasharray="2 5"/>',
         t(560, floor + 18, "published entitlement", 10.5, MUTED, anchor="end")]
    wav = "M40 110 C70 80 90 150 120 120 S170 90 200 135 S250 110 280 150 S330 128 360 162"
    a.append(f'<path class="draw" d="{wav}" stroke="{FG}" stroke-opacity=".8" fill="none" stroke-width="1.6"/>')
    a.append(t(40, 98, "buyer keeps pushing", 10.5, MUTED))
    # prompt-only rules give in
    a.append(f'<path class="draw" style="animation-delay:1.4s" d="M360 162 C400 175 420 205 470 222 L560 230" '
             f'stroke="{MUTED}" stroke-opacity=".6" stroke-dasharray="5 5" fill="none"/>')
    a.append(t(560, 248, "prompt-only rule: talked down", 10.5, MUTED, anchor="end"))
    # the guard
    a.append(f'<rect x="372" y="{floor - 34}" width="14" height="34" fill="{AMBER}"/>')
    a.append(t(379, floor - 44, "7-LINE GUARD, NO MODEL", 10.5, AMBER, anchor="middle", extra='letter-spacing="1.2"'))
    a.append(f'<path class="draw" style="animation-delay:1.4s" d="M386 {floor} H560" stroke="{AMBER}" stroke-width="2.4" fill="none"/>')
    a.append(dot_on(wav + f" L372 {floor} H560", AMBER, "4.5s"))
    return frame("Vendable", "AGENT-TRANSACTABLE COMMERCE", AMBER,
                 "Across 105 recorded negotiations, a 7-line statutory guard held every median "
                 "on the published entitlement.", "\n  ".join(a))


def agentos():
    y = 150
    a = [f'<line x1="40" y1="{y}" x2="560" y2="{y}" stroke="{DIM}"/>']
    ticks = []
    for k in range(9):
        x = 60 + k * 60
        ticks.append(f'<rect x="{x}" y="{y - 9}" width="26" height="18" fill="none" stroke="{GREEN}" stroke-opacity=".7"/>')
    a.append(f'<g clip-path="url(#lane)"><g class="slide">{"".join(ticks)}'
             f'{"".join(t.replace(f"x=\"{60 + k * 60}\"", f"x=\"{60 + (k + 9) * 60}\"") for k, t in enumerate(ticks))}</g></g>')
    a.insert(0, f'<defs><clipPath id="lane"><rect x="40" y="{y - 20}" width="300" height="40"/></clipPath></defs>')
    a.append(t(40, y - 26, "RUN EVENTS, LIVE OVER WEBSOCKET", 10.5, MUTED, extra='letter-spacing="1.2"'))
    # approval gate
    gx = 372
    a.append(f'<line x1="{gx}" y1="{y - 34}" x2="{gx}" y2="{y + 34}" stroke="{AMBER}" stroke-width="2"/>')
    a.append(f'<rect x="{gx - 40}" y="{y - 9}" width="26" height="18" fill="{AMBER}" fill-opacity=".25" stroke="{AMBER}"/>')
    a.append(f'<circle class="pulse" cx="{gx - 27}" cy="{y}" r="9" fill="none" stroke="{AMBER}"/>')
    a.append(f'<circle cx="{gx + 22}" cy="{y - 14}" r="6" fill="none" stroke="{FG}"/>'
             f'<path d="M{gx + 12} {y + 4} q10 -14 20 0" fill="none" stroke="{FG}"/>')
    a.append(t(gx + 40, y - 8, "sensitive tool waits", 10.5, FG))
    a.append(t(gx + 40, y + 8, "for a human yes", 10.5, FG))
    # per-skill cost
    for i, (w, lb) in enumerate([(120, "skill"), (64, "skill"), (180, "skill")]):
        yy = 206 + i * 14
        a.append(f'<rect class="fade" style="animation-delay:{.4 + i * .2:.1f}s" x="380" y="{yy}" width="{w}" height="7" fill="{GREEN}" fill-opacity=".55"/>')
    a.append(t(372, 216, "cost per", 10.5, MUTED, anchor="end"))
    a.append(t(372, 230, "skill", 10.5, MUTED, anchor="end"))
    return frame("AgentOS", "LOCAL CONTROL PLANE FOR CLAUDE CODE", GREEN,
                 "Watch an agent run as it happens, approve risky tool calls, and see which skill "
                 "the cost and failures came from.", "\n  ".join(a))


# SurviveCity city layout (v1, 3 agents), from the zombiee README (Z zombie spawn, F food, S safehouse, # wall).
CITY = [
    "Z........Z",
    ".F......F.",
    ".....#....",
    "...#..#...",
    "....SSS...",
    "..#.SSS#..",
    "....SSS...",
    "...#.##...",
    ".F......F.",
    ".........Z",
]


def survivecity():
    gx, gy, c = 30, 90, 15
    RED = "#e0604f"

    def px(col, row):
        return gx + col * c + c / 2, gy + row * c + c / 2

    def walker(cells, color, dur, r=5, infected=False):
        pts = cells + cells[-2:0:-1]  # walk out and back
        vals = ";".join(f"{px(cc, rr)[0]:.1f} {px(cc, rr)[1]:.1f}" for cc, rr in pts + pts[:1])
        fill = color
        anim = ""
        if infected:  # hidden role: looks like everyone else until the reveal
            anim = (f'<animate attributeName="fill" values="{color};{color};{RED};{RED}" '
                    f'keyTimes="0;.45;.5;1" dur="{dur}" repeatCount="indefinite"/>')
        return (f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" '
                f'dur="{dur}" repeatCount="indefinite"/><circle r="{r}" fill="{fill}">{anim}</circle></g>')

    a = []
    for rr, line in enumerate(CITY):
        for cc, ch in enumerate(line):
            x, y = gx + cc * c, gy + rr * c
            if ch == "#":
                a.append(f'<rect x="{x + 1}" y="{y + 1}" width="{c - 2}" height="{c - 2}" fill="{DIM}"/>')
            elif ch == "S":
                a.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{CYAN}" fill-opacity=".14"/>')
            elif ch == "F":
                a.append(f'<rect x="{x + 5}" y="{y + 5}" width="{c - 10}" height="{c - 10}" fill="{GREEN}"/>')
            else:
                a.append(f'<circle cx="{x + c / 2}" cy="{y + c / 2}" r=".9" fill="{DIM}"/>')
    a.append(f'<rect x="{gx + 4 * c}" y="{gy + 4 * c}" width="{3 * c}" height="{3 * c}" fill="none" stroke="{CYAN}" stroke-opacity=".6"/>')
    # agents leave the safehouse to forage; one is secretly infected
    a.append(walker([(5, 5), (5, 4), (5, 3), (4, 3), (4, 2), (3, 2), (2, 2), (2, 1), (1, 1)], FG, "7s"))
    a.append(walker([(4, 6), (4, 7), (4, 8), (3, 8), (2, 8), (1, 8)], FG, "6s", infected=True))
    a.append(walker([(6, 5), (6, 4), (7, 4), (8, 4), (8, 3), (8, 2), (8, 1)], FG, "6.5s"))
    # zombies roam the edges
    a.append(walker([(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1), (4, 0)], AMBER, "5s", 4.5))
    a.append(walker([(9, 0), (9, 1), (9, 2), (9, 3), (8, 3), (7, 3), (7, 2)], AMBER, "5.5s", 4.5))
    a.append(walker([(9, 9), (8, 9), (7, 9), (7, 8), (6, 8), (5, 8), (5, 9)], AMBER, "6s", 4.5))
    ly = gy + 10 * c + 14
    a.append(f'<circle cx="{gx + 4}" cy="{ly - 3}" r="3.5" fill="{FG}"/>' + t(gx + 11, ly, "agent", 9.5, MUTED))
    a.append(f'<circle cx="{gx + 58}" cy="{ly - 3}" r="3.5" fill="{AMBER}"/>' + t(gx + 65, ly, "zombie", 9.5, MUTED))
    a.append(f'<circle cx="{gx + 118}" cy="{ly - 3}" r="3.5" fill="{RED}"/>' + t(gx + 125, ly, "infected", 9.5, MUTED))

    # the result, labelled as the README measures it
    rx = 250
    a.append(t(rx, 112, "MEAN AGENTS ALIVE AT END", 10.5, MUTED, extra='letter-spacing="1.2"'))
    a.append(t(rx, 160, "0.15", 38, FG, SANS, extra='font-weight="700"'))
    a.append(f'<path class="draw" d="M{rx + 92} 147 H{rx + 140}" stroke="{AMBER}" stroke-width="2" fill="none"/>'
             f'<path d="M{rx + 134} 141 l7 6 l-7 6" stroke="{AMBER}" stroke-width="2" fill="none"/>')
    a.append(t(rx + 152, 160, "0.60", 38, AMBER, SANS, extra='font-weight="700"'))
    a.append(t(rx + 258, 160, "4x", 16, AMBER, MONO))
    a.append(t(rx, 186, "random baseline vs trained policy", 11, MUTED))
    a.append(t(rx, 222, "3 REWARD HACKS CLOSED", 10.5, MUTED, extra='letter-spacing="1.2"'))
    for i, h in enumerate(["scan-spam", "vote-spam", "idle-wait"]):
        x = rx + i * 104
        a.append(f'<line class="fade" style="animation-delay:{.6 + i * .3:.1f}s" x1="{x}" y1="240" x2="{x + len(h) * 6.7:.0f}" y2="240" stroke="{AMBER}"/>')
        a.append(t(x, 245, h, 11, FG))
    return frame("SurviveCity", "ZOMBIE SURVIVAL, HIDDEN INFECTED AGENT", AMBER,
                 "GRPO + LoRA on Qwen2.5-3B, about 90 hours on a V100 DGX across 4 documented runs.",
                 "\n  ".join(a), "TOP 100 · META × PYTORCH")


def contextual():
    top, bot, mx, my = 108, 210, 300, 159
    p1 = f"M60 {top} C180 {top} 200 {my} {mx} {my} H440 L540 {my}"
    p2 = f"M60 {bot} C180 {bot} 200 {my} {mx} {my} H440 L540 {my}"
    a = [f'<path d="{p1}" stroke="{DIM}" fill="none"/>', f'<path d="{p2}" stroke="{DIM}" fill="none"/>',
         t(60, top - 12, "BM25: exact symbols", 10.5, FG), t(60, bot + 20, "FAISS: meaning", 10.5, FG),
         f'<path d="M330 {my - 34} L430 {my - 10} L430 {my + 10} L330 {my + 34} Z" fill="{CYAN}" fill-opacity=".12" stroke="{CYAN}"/>',
         t(380, my - 42, "CROSS-ENCODER RERANK", 10.5, CYAN, anchor="middle", extra='letter-spacing="1.2"'),
         f'<rect x="510" y="{my - 22}" width="40" height="44" fill="none" stroke="{FG}" stroke-opacity=".6"/>',
         t(530, my + 40, "cited answer", 10.5, FG, anchor="middle")]
    for k in range(3):
        a.append(dot_on(p1, CYAN, "3.6s", f"{k * 1.2:.1f}s", 3))
        a.append(dot_on(p2, FG, "3.6s", f"{k * 1.2 + .6:.1f}s", 3))
    for k in range(3):
        a.append(f'<line x1="518" y1="{my - 12 + k * 10}" x2="542" y2="{my - 12 + k * 10}" stroke="{FG}" stroke-opacity=".5"/>')
    return frame("Contextual", "REPO-AWARE RAG", CYAN,
                 "30% better retrieval F1 than semantic-only search, over 10k+ code chunks. "
                 "CLI, web app and VS Code extension.", "\n  ".join(a))


def claude_kit():
    a = [t(40, 100, "SESSIONS", 10.5, MUTED, extra='letter-spacing="1.2"')]
    for i, w in enumerate([150, 110, 140, 90, 130, 100]):
        a.append(f'<rect class="fade" style="animation-delay:{i * .12:.2f}s" x="40" y="{112 + i * 16}" width="{w}" height="6" fill="{DIM}"/>')
    a.append(f'<path class="flow" d="M200 160 H250" stroke="{GREEN}" fill="none"/>')
    a.append(t(262, 100, "COUNT FAILURES", 10.5, MUTED, extra='letter-spacing="1.2"'))

    def tally(x, y, n, col):
        s = "".join(f'<line x1="{x + k * 7}" y1="{y}" x2="{x + k * 7}" y2="{y + 18}" stroke="{col}" stroke-width="1.6"/>' for k in range(min(n, 4)))
        if n >= 5:
            s += f'<line x1="{x - 3}" y1="{y + 14}" x2="{x + 25}" y2="{y + 4}" stroke="{col}" stroke-width="1.6"/>'
        return s
    a.append(f'<g class="fade" style="animation-delay:.6s">{tally(266, 118, 5, GREEN)}{tally(304, 118, 4, GREEN)}</g>')
    a.append(f'<g class="fade" style="animation-delay:.8s">{tally(266, 160, 1, DIM)}</g>')
    a.append(f'<g class="fade" style="animation-delay:1s">{tally(266, 202, 5, GREEN)}{tally(304, 202, 2, GREEN)}</g>')
    a.append(f'<path class="flow" d="M350 160 H400" stroke="{GREEN}" fill="none"/>')
    a.append(t(412, 100, "SHIP A RULE?", 10.5, MUTED, extra='letter-spacing="1.2"'))
    for y, ok, lb in [(132, True, "repeats: rule"), (174, False, "one-off: skip"), (216, True, "repeats: rule")]:
        if ok:
            a.append(f'<path class="draw" d="M414 {y - 4} l6 6 l12 -12" stroke="{GREEN}" stroke-width="2" fill="none"/>')
            a.append(t(442, y, lb, 11, FG))
        else:
            a.append(t(442, y, lb, 11, MUTED, extra='text-decoration="line-through"'))
    return frame("claude-kit", "AGENT DEV TOOLING, MIT", GREEN,
                 "Skills and guardrails for coding agents, each written for a failure that kept "
                 "showing up in counted session telemetry.", "\n  ".join(a))


CARDS = [("cassandra", cassandra), ("vendable", vendable), ("agentos", agentos),
         ("survivecity", survivecity), ("contextual", contextual), ("claude-kit", claude_kit)]

if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "projects"
    out.mkdir(exist_ok=True)
    for i, (slug, fn) in enumerate(CARDS, 1):
        (out / f"{i:02d}-{slug}.svg").write_text(fn(), encoding="utf-8")
    print("wrote", len(CARDS), "cards to projects/")
