#!/usr/bin/env python3
"""Download activity graph SVG and keep every Nth x-axis day label."""

from __future__ import annotations

import re
import sys
import urllib.request

GRAPH_URL = (
    "https://github-readme-activity-graph.vercel.app/graph"
    "?username=SirjanSingh"
    "&theme=tokyonight"
    "&hide_border=true"
    "&bg_color=1a1b27"
    "&color=7aa2f7"
    "&line=7aa2f7"
    "&point=7aa2f7"
    "&days=90"
    "&height=280"
)

HORIZONTAL_LABEL = re.compile(
    r'(<text[^>]*class="ct-label ct-horizontal ct-end"[^>]*>)[^<]*(</text>)'
)


def thin_x_labels(svg: str, step: int = 5) -> str:
    index = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal index
        keep = index % step == 0
        index += 1
        if keep:
            return match.group(0)
        return f"{match.group(1)}{match.group(2)}"

    return HORIZONTAL_LABEL.sub(replace, svg)


def main() -> int:
    output_path = sys.argv[1] if len(sys.argv) > 1 else "github-activity-graph.svg"
    step = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    with urllib.request.urlopen(GRAPH_URL, timeout=120) as response:
        svg = response.read().decode("utf-8")

    svg = thin_x_labels(svg, step=step)

    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(svg)

    print(f"Wrote {output_path} with x-axis labels every {step} days")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
