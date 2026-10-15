#!/usr/bin/env python3
"""Render a contribution activity line graph as SVG using the GitHub GraphQL API.

Usage: generate-activity-graph.py [output.svg] [label_step]
Env:   GITHUB_TOKEN (required), GITHUB_USER (default: SirjanSingh)
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request

USER = os.environ.get("GITHUB_USER", "SirjanSingh")
DAYS = 90
WIDTH, HEIGHT = 1200, 280
BG, ACCENT, GRID = "#1a1b27", "#7aa2f7", "#2a2e45"
PAD_L, PAD_R, PAD_T, PAD_B = 56, 24, 44, 40

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


def fetch_counts(token: str) -> list[tuple[dt.date, int]]:
    today = dt.datetime.now(dt.timezone.utc).date()
    start = today - dt.timedelta(days=DAYS - 1)
    variables = {
        "login": USER,
        "from": f"{start.isoformat()}T00:00:00Z",
        "to": f"{today.isoformat()}T23:59:59Z",
    }
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "activity-graph-generator",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)
    if payload.get("errors") or not payload.get("data", {}).get("user"):
        raise SystemExit(f"GraphQL error: {payload.get('errors') or 'user not found'}")

    weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    counts = {
        dt.date.fromisoformat(day["date"]): day["contributionCount"]
        for week in weeks
        for day in week["contributionDays"]
    }
    return [(start + dt.timedelta(days=i), counts.get(start + dt.timedelta(days=i), 0)) for i in range(DAYS)]


def render(points: list[tuple[dt.date, int]], step: int) -> str:
    peak = max(count for _, count in points)
    top = max(4, peak + (-peak % 2))  # round the y-axis up to an even number, minimum 4
    plot_w = WIDTH - PAD_L - PAD_R
    plot_h = HEIGHT - PAD_T - PAD_B

    def x(i: int) -> float:
        return PAD_L + plot_w * i / (len(points) - 1)

    def y(value: int) -> float:
        return PAD_T + plot_h * (1 - value / top)

    parts = [
        f'<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'fill="none" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="GitHub contributions for {USER} over the last {DAYS} days">',
        f'<rect width="100%" height="100%" fill="{BG}"/>',
        f'<text x="{PAD_L}" y="26" fill="{ACCENT}" font-family="Segoe UI, Ubuntu, sans-serif" '
        f'font-size="16" font-weight="600">Contributions, last {DAYS} days</text>',
    ]

    for tick in range(0, top + 1, top // 4 or 1):
        parts.append(f'<line x1="{PAD_L}" x2="{WIDTH - PAD_R}" y1="{y(tick):.1f}" y2="{y(tick):.1f}" stroke="{GRID}"/>')
        parts.append(
            f'<text x="{PAD_L - 10}" y="{y(tick) + 4:.1f}" fill="{ACCENT}" text-anchor="end" '
            f'font-family="Segoe UI, Ubuntu, sans-serif" font-size="12">{tick}</text>'
        )

    for i, (day, _) in enumerate(points):
        if i % step == 0:
            parts.append(
                f'<text x="{x(i):.1f}" y="{HEIGHT - 14}" fill="{ACCENT}" text-anchor="middle" '
                f'font-family="Segoe UI, Ubuntu, sans-serif" font-size="12">{day.strftime("%b %d").replace(" 0", " ")}</text>'
            )

    path = " ".join(f'{"M" if i == 0 else "L"}{x(i):.1f},{y(c):.1f}' for i, (_, c) in enumerate(points))
    parts.append(f'<path d="{path}" stroke="{ACCENT}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, (day, count) in enumerate(points):
        parts.append(
            f'<circle cx="{x(i):.1f}" cy="{y(count):.1f}" r="3" fill="{ACCENT}">'
            f"<title>{day.isoformat()}: {count} contributions</title></circle>"
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    output = sys.argv[1] if len(sys.argv) > 1 else "github-activity-graph.svg"
    step = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is not set")

    svg = render(fetch_counts(token), step)
    with open(output, "w", encoding="utf-8", newline="\n") as file:
        file.write(svg)
    print(f"Wrote {output} ({DAYS} days, labels every {step} days)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
