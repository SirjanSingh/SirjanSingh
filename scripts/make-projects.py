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


# SurviveCity: the core 10x10 city is the v1 layout from the zombiee README
# (Z zombie spawn, F food, S safehouse, # wall). The outskirts on either side are
# decoration so the card is not empty: extra buildings and wandering zombies.
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
COLS, CORE = 30, 10  # core city sits in columns 10..19
CLEAR_COLS = {2, 6, 23, 27}  # outskirt streets kept free for zombies


def outskirts():
    import random
    rnd = random.Random(11)
    cells = set()
    for col in list(range(0, CORE)) + list(range(CORE * 2, COLS)):
        if col in CLEAR_COLS:
            continue
        for row in range(2, 8):
            if rnd.random() < .42:
                cells.add((col, row))
    return cells


def survivecity():
    gx, gy, c = 45, 88, 17
    RED, ZOMB, ZDARK = "#e0604f", "#8fbf6a", "#557a43"
    sprites = f"""<defs>
    <g id="zed"><rect x="-2.6" y="-8" width="5.2" height="4.6" fill="{ZOMB}"/>
      <rect x="-1.6" y="-6.6" width="1.2" height="1.2" fill="{RED}"/><rect x=".6" y="-6.6" width="1.2" height="1.2" fill="{RED}"/>
      <rect x="-2.2" y="-3.2" width="4.4" height="5.4" fill="{ZDARK}"/>
      <rect x="2" y="-2.6" width="4.2" height="1.6" fill="{ZOMB}"/><rect x="2" y="-.4" width="3.6" height="1.6" fill="{ZOMB}"/>
      <rect x="-2.2" y="2.2" width="1.7" height="3.4" fill="{ZDARK}"/><rect x=".5" y="2.2" width="1.7" height="3.4" fill="{ZDARK}"/></g>
    <g id="man"><circle cx="0" cy="-5.6" r="2.4"/><rect x="-2.2" y="-3" width="4.4" height="5.4"/>
      <rect x="-2.2" y="2.4" width="1.7" height="3.4"/><rect x=".5" y="2.4" width="1.7" height="3.4"/></g>
  </defs>
  <style>.shamble {{ transform-box: fill-box; transform-origin: center bottom; animation: sham .9s ease-in-out infinite alternate; }}
    @keyframes sham {{ from {{ transform: rotate(-9deg) }} to {{ transform: rotate(9deg) }} }}
    .win {{ animation: win 3s steps(1) infinite; }} @keyframes win {{ 50% {{ opacity: .15 }} }}
    @media (prefers-reduced-motion: reduce) {{ .shamble,.win {{ animation: none }} }}</style>"""

    def px(col, row):
        return gx + col * c + c / 2, gy + row * c + c / 2

    def walker(cells, kind, dur, infected=False, delay=0):
        pts = cells + cells[-2:0:-1]
        vals = ";".join(f"{px(cc, rr)[0]:.1f} {px(cc, rr)[1] + 2:.1f}" for cc, rr in pts + pts[:1])
        move = (f'<animateTransform attributeName="transform" type="translate" values="{vals}" '
                f'dur="{dur}" begin="-{delay}s" repeatCount="indefinite"/>')
        if kind == "zed":
            return f'<g>{move}<use href="#zed" class="shamble" style="animation-delay:-{delay}s"/></g>'
        fill = f'<animate attributeName="fill" values="{FG};{FG};{RED};{RED}" keyTimes="0;.45;.5;1" dur="{dur}" repeatCount="indefinite"/>' if infected else ""
        return f'<g>{move}<use href="#man" fill="{FG}">{fill}</use></g>'

    def building(x, y, k):
        s = (f'<rect x="{x + 1.5}" y="{y + 1.5}" width="{c - 3}" height="{c - 3}" fill="#2b2f35" stroke="{DIM}" stroke-opacity=".8"/>')
        for wx, wy in [(5, 5), (10, 5), (5, 10), (10, 10)]:
            lit = (k + wx + wy) % 4 == 0
            cls = ' class="win"' if lit and k % 2 else ""
            s += (f'<rect{cls} x="{x + wx}" y="{y + wy}" width="2.6" height="2.6" '
                  f'fill="{AMBER if lit else DIM}" fill-opacity="{1 if lit else .7}"/>')
        return s

    a = [sprites]
    out = outskirts()
    k = 0
    for row in range(10):
        for col in range(COLS):
            x, y = gx + col * c, gy + row * c
            core = CORE <= col < CORE * 2
            ch = CITY[row][col - CORE] if core else ("#" if (col, row) in out else ".")
            if ch == "#":
                a.append(building(x, y, k)); k += 1
            elif ch == "S":
                a.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{CYAN}" fill-opacity=".13"/>')
            elif ch == "F":
                a.append(f'<rect x="{x + 4}" y="{y + 5}" width="{c - 8}" height="{c - 9}" fill="{AMBER}" fill-opacity=".85"/>'
                         f'<path d="M{x + 4} {y + 5} l{c - 8} {c - 9} M{x + c - 4} {y + 5} l-{c - 8} {c - 9}" stroke="#7a5a1c"/>')
            else:
                a.append(f'<circle cx="{x + c / 2}" cy="{y + c / 2}" r=".8" fill="{DIM}"/>')
    sx, sy = gx + (CORE + 4) * c, gy + 4 * c
    a.append(f'<rect x="{sx}" y="{sy}" width="{3 * c}" height="{3 * c}" fill="none" stroke="{CYAN}" stroke-opacity=".7"/>'
             f'<path d="M{sx + 6} {sy} L{sx + 1.5 * c} {sy - 9} L{sx + 3 * c - 6} {sy}" fill="none" stroke="{CYAN}" stroke-opacity=".7"/>')

    o = CORE  # shift core coordinates
    # survivors leave the safehouse to forage; one is secretly infected
    a.append(walker([(o + 5, 5), (o + 5, 4), (o + 5, 3), (o + 4, 3), (o + 4, 2), (o + 3, 2), (o + 2, 2), (o + 2, 1), (o + 1, 1)], "man", "7s"))
    a.append(walker([(o + 4, 6), (o + 4, 7), (o + 4, 8), (o + 3, 8), (o + 2, 8), (o + 1, 8)], "man", "6s", infected=True))
    a.append(walker([(o + 6, 5), (o + 6, 4), (o + 7, 4), (o + 8, 4), (o + 8, 3), (o + 8, 2), (o + 8, 1)], "man", "6.5s"))
    # the three spawn-corner zombies
    a.append(walker([(o, 0), (o + 1, 0), (o + 2, 0), (o + 3, 0), (o + 3, 1), (o + 4, 1), (o + 4, 0)], "zed", "7s"))
    a.append(walker([(o + 9, 0), (o + 9, 1), (o + 9, 2), (o + 9, 3), (o + 8, 3), (o + 7, 3), (o + 7, 2)], "zed", "7.5s", delay=2))
    a.append(walker([(o + 9, 9), (o + 8, 9), (o + 7, 9), (o + 7, 8), (o + 6, 8), (o + 5, 8), (o + 5, 9)], "zed", "8s", delay=1))
    # the horde in the outskirts, shuffling along open streets
    for col, dur, d in [(2, "9s", 0), (6, "11s", 4), (23, "10s", 2), (27, "12s", 6)]:
        a.append(walker([(col, r) for r in range(0, 10)], "zed", dur, delay=d))
    a.append(walker([(cc, 0) for cc in range(0, 9)], "zed", "13s", delay=3))
    a.append(walker([(cc, 9) for cc in range(21, 30)], "zed", "12s", delay=5))
    a.append(walker([(cc, 9) for cc in range(0, 8)], "zed", "10s", delay=7))
    a.append(walker([(cc, 0) for cc in range(21, 30)], "zed", "14s", delay=1))

    # legend, top right under the badge
    lx, ly = W - 196, 62
    a.append(f'<use href="#man" fill="{FG}" transform="translate({lx} {ly})"/>' + t(lx + 8, ly + 3, "survivor", 10, MUTED))
    a.append(f'<use href="#zed" transform="translate({lx + 72} {ly})"/>' + t(lx + 84, ly + 3, "zombie", 10, MUTED))
    a.append(f'<use href="#man" fill="{RED}" transform="translate({lx + 136} {ly})"/>' + t(lx + 144, ly + 3, "infected", 10, MUTED))
    return frame("SurviveCity", "ZOMBIE SURVIVAL, HIDDEN INFECTED AGENT", AMBER,
                 "Agents forage, zombies roam, one agent is secretly infected. GRPO + LoRA on Qwen2.5-3B.",
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
