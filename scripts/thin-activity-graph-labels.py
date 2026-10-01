#!/usr/bin/env python3
"""Render the README activity graph SVG from GitHub's contribution calendar.

The public github-readme-activity-graph.vercel.app instance started returning
HTTP 402 (Payment Required), so the graph is now drawn locally from the
GraphQL API. Only every Nth x-axis day label is shown to keep it readable.

Usage: thin-activity-graph-labels.py [output.svg] [label_step]
Requires GITHUB_TOKEN (or GH_TOKEN) in the environment.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request
from xml.sax.saxutils import escape

USERNAME = "SirjanSingh"
DISPLAY_NAME = "Sirjan Singh"
DAYS = 90

WIDTH = 1200
HEIGHT = 280
LEFT, RIGHT = 90, 1150
TOP, BOTTOM = 80, 210

BG_COLOR = "#1a1b27"
TITLE_COLOR = "#7aa2f7"
LABEL_COLOR = "#7aa2f7"
LINE_COLOR = "#7aa2f7"
POINT_COLOR = "#7aa2f7"
AREA_COLOR = "#9e4c98"

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch_contributions(token: str, days: int) -> list[tuple[dt.date, int]]:
    now = dt.datetime.now(dt.timezone.utc)
    start = (now - dt.timedelta(days=days - 1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    payload = json.dumps(
        {
            "query": QUERY,
            "variables": {
                "login": USERNAME,
                "from": start.isoformat(),
                "to": now.isoformat(),
            },
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{USERNAME}-activity-graph",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        body = json.load(response)

    if body.get("errors"):
        raise RuntimeError(f"GraphQL errors: {body['errors']}")

    weeks = body["data"]["user"]["contributionsCollection"]["contributionCalendar"][
        "weeks"
    ]
    counts = {
        dt.date.fromisoformat(day["date"]): day["contributionCount"]
        for week in weeks
        for day in week["contributionDays"]
    }

    # Always return exactly `days` consecutive days, filling gaps with zero.
    end = now.date()
    return [
        (end - dt.timedelta(days=offset), counts.get(end - dt.timedelta(days=offset), 0))
        for offset in range(days - 1, -1, -1)
    ]


def nice_max(value: int) -> int:
    """Round the y-axis maximum up to a multiple of 4 so the 4 bands are integers."""
    value = max(value, 4)
    return value + (-value % 4)


def smooth_path(points: list[tuple[float, float]]) -> str:
    """Monotone-ish cubic smoothing similar to Chartist's line interpolation."""
    if not points:
        return ""
    parts = [f"M{points[0][0]:.2f},{points[0][1]:.2f}"]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        cx = (x1 - x0) / 3
        parts.append(
            f"C{x0 + cx:.2f},{y0:.2f},{x1 - cx:.2f},{y1:.2f},{x1:.2f},{y1:.2f}"
        )
    return "".join(parts)


def render_svg(data: list[tuple[dt.date, int]], label_step: int) -> str:
    y_max = nice_max(max(count for _, count in data))
    step_x = (RIGHT - LEFT) / (len(data) - 1)

    def x_at(i: int) -> float:
        return LEFT + i * step_x

    def y_at(count: int) -> float:
        return BOTTOM - (count / y_max) * (BOTTOM - TOP)

    points = [(x_at(i), y_at(count)) for i, (_, count) in enumerate(data)]
    line = smooth_path(points)
    area = f"{line}L{RIGHT:.2f},{BOTTOM}L{LEFT:.2f},{BOTTOM}Z"

    grid = []
    for i in range(len(data)):
        x = x_at(i)
        grid.append(
            f'<line x1="{x:.2f}" x2="{x:.2f}" y1="{TOP}" y2="{BOTTOM}" class="ct-grid"/>'
        )
    y_labels = []
    for band in range(5):
        value = y_max * band // 4
        y = y_at(value)
        grid.append(
            f'<line x1="{LEFT}" x2="{RIGHT}" y1="{y:.2f}" y2="{y:.2f}" class="ct-grid"/>'
        )
        y_labels.append(
            f'<text x="{LEFT - 10}" y="{y + 4:.2f}" class="ct-label" '
            f'text-anchor="end">{value}</text>'
        )

    x_labels = [
        f'<text x="{x_at(i):.2f}" y="{BOTTOM + 22}" class="ct-label" '
        f'text-anchor="middle">{day.day}</text>'
        for i, (day, _) in enumerate(data)
        if i % label_step == 0
    ]

    dots = [
        f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{x + 0.01:.2f}" y2="{y:.2f}" '
        f'class="ct-point"><title>{day.isoformat()}: {count}</title></line>'
        for (x, y), (day, count) in zip(points, data)
    ]

    title = escape(f"{DISPLAY_NAME}'s Contribution Graph")
    return f"""<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    svg {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; user-select: none; }}
    .header {{ font: 600 20px 'Segoe UI', Ubuntu, Sans-Serif; fill: {TITLE_COLOR}; }}
    .axis-title {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {LABEL_COLOR}; }}
    .ct-label {{ fill: {LABEL_COLOR}; font-size: 12px; }}
    .ct-grid {{ stroke: {LINE_COLOR}; stroke-width: 1px; stroke-opacity: 0.3; stroke-dasharray: 2px; }}
    .ct-line {{ fill: none; stroke: {LINE_COLOR}; stroke-width: 4px; stroke-dasharray: 5000; stroke-dashoffset: 5000; animation: dash 5s ease-in-out forwards; }}
    .ct-area {{ stroke: none; fill: {AREA_COLOR}; fill-opacity: 0.1; }}
    .ct-point {{ stroke: {POINT_COLOR}; stroke-width: 10px; stroke-linecap: round; animation: blink 1s ease-in-out forwards; }}
    @keyframes blink {{ from {{ opacity: 0; transform: translateX(-20px); }} to {{ opacity: 1; transform: translateX(0); }} }}
    @keyframes dash {{ to {{ stroke-dashoffset: 0; }} }}
  </style>
  <rect x="0" y="0" width="100%" height="100%" fill="{BG_COLOR}"/>
  <text x="{WIDTH / 2}" y="40" text-anchor="middle" class="header">{title}</text>
  <g class="ct-grids">{"".join(grid)}</g>
  <path d="{area}" class="ct-area"/>
  <path d="{line}" class="ct-line"/>
  <g class="ct-points">{"".join(dots)}</g>
  <g class="ct-labels">{"".join(y_labels)}{"".join(x_labels)}</g>
  <text x="{(LEFT + RIGHT) / 2}" y="{HEIGHT - 12}" text-anchor="middle" class="axis-title">Days</text>
  <text x="30" y="{(TOP + BOTTOM) / 2}" text-anchor="middle" class="axis-title" transform="rotate(-90 30 {(TOP + BOTTOM) / 2})">Contributions</text>
</svg>
"""


def main() -> int:
    output_path = sys.argv[1] if len(sys.argv) > 1 else "github-activity-graph.svg"
    step = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("GITHUB_TOKEN (or GH_TOKEN) must be set", file=sys.stderr)
        return 1

    data = fetch_contributions(token, DAYS)
    svg = render_svg(data, label_step=step)

    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(svg)

    print(f"Wrote {output_path} ({len(data)} days, x-axis labels every {step} days)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
