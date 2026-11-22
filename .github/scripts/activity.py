#!/usr/bin/env python3
"""Render the profile activity panel (dist/activity.svg) from the GitHub GraphQL API.

Runs in GitHub Actions with GITHUB_TOKEN. Uses only the standard library.
For a local preview, pass a saved API response: activity.py --fixture data.json
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from collections import Counter
from xml.sax.saxutils import escape

USER = os.environ.get("ACTIVITY_USER", "GabsDevX")
OUT = os.environ.get("ACTIVITY_OUT", "dist/activity.svg")

QUERY = """
query($login: String!) {
  user(login: $login) {
    pullRequests(states: MERGED) { totalCount }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      commitContributionsByRepository(maxRepositories: 100) { repository { nameWithOwner } }
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""


def fetch():
    token = os.environ["GITHUB_TOKEN"]
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data


SANS = "font-family=\"'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif\""
MONO = "font-family=\"Consolas,'SFMono-Regular',Menlo,'Liberation Mono',monospace\""
BG, CARD, LINE = "#0b0f1a", "#111827", "#243047"
MUTED, DIM = "#8a9bb3", "#5f708a"
LEVELS = ["#161f2e", "#0e4429", "#006d32", "#26a641", "#39d353"]
ACCENTS = ["#22d3ee", "#34d399", "#f57c00", "#fbbf24"]
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
WEEKDAYS = "Sundays Mondays Tuesdays Wednesdays Thursdays Fridays Saturdays".split()


def level(n, peak):
    if n == 0:
        return 0
    q = n / max(peak, 1)
    return 1 if q <= 0.25 else 2 if q <= 0.5 else 3 if q <= 0.75 else 4


def stats(data):
    user = data["data"]["user"]
    cc = user["contributionsCollection"]
    cal = cc["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    counts = [d["contributionCount"] for d in days]

    longest = cur = 0
    best_end = None
    for i, d in enumerate(days):
        cur = cur + 1 if d["contributionCount"] > 0 else 0
        if cur > longest:
            longest, best_end = cur, i
    peak_day = max(days, key=lambda d: d["contributionCount"])
    by_month = Counter()
    by_weekday = Counter()
    for d in days:
        date = dt.date.fromisoformat(d["date"])
        by_month[(date.year, date.month)] += d["contributionCount"]
        by_weekday[d["weekday"]] += d["contributionCount"]
    busiest_month = max(by_month, key=by_month.get)
    return {
        "user": user,
        "cc": cc,
        "weeks": weeks,
        "days": days,
        "total": cal["totalContributions"],
        "public_commits": cc["totalCommitContributions"],
        "private": cc["restrictedContributionsCount"],
        "merged": user["pullRequests"]["totalCount"],
        "repos": len(cc["commitContributionsByRepository"]),
        "longest": longest,
        "streak_end": best_end,
        "peak": peak_day,
        "peak_count": max(counts) if counts else 0,
        "active": sum(1 for c in counts if c > 0),
        "busiest_month": busiest_month,
        "busiest_month_count": by_month[busiest_month],
        "busiest_weekday": WEEKDAYS[max(by_weekday, key=by_weekday.get)] if by_weekday else "—",
    }


def fmt(n):
    return f"{n:,}"


def render(s, today):
    W, out = 1200, []
    add = out.append
    add(f'<rect width="{W}" height="620" rx="18" fill="{BG}" stroke="{LINE}"/>')
    add(f'<line x1="0" y1="46" x2="{W}" y2="46" stroke="{LINE}"/>')
    for i, c in enumerate(["#f87171", "#fbbf24", "#34d399"]):
        add(f'<circle cx="{24 + i * 18}" cy="23" r="6" fill="{c}"/>')
    add(f'<text x="{W / 2}" y="28" fill="#e5ecf5" font-size="13" font-weight="600" text-anchor="middle" {SANS}>Activity — {escape(USER)}</text>')

    cards = [
        (fmt(s["total"]), "contributions in the last 12 months", "public and private, as counted by GitHub"),
        (fmt(s["public_commits"] + s["private"]), "commits and private contributions", f'{fmt(s["public_commits"])} public commits · {fmt(s["private"])} private'),
        (fmt(s["merged"]), "pull requests merged", "across public repositories"),
        (fmt(s["repos"]), "repositories with commits", "in the last 12 months"),
    ]
    cw = (W - 40 - 3 * 14) / 4
    for i, (big, label, sub) in enumerate(cards):
        x = 20 + i * (cw + 14)
        add(f'<rect x="{x}" y="64" width="{cw}" height="112" rx="14" fill="{CARD}" stroke="{LINE}"/>')
        add(f'<rect x="{x + 20}" y="80" width="26" height="4" rx="2" fill="{ACCENTS[i]}"/>')
        add(f'<text x="{x + 20}" y="128" fill="#fff" font-size="36" font-weight="800" {SANS}>{big}</text>')
        add(f'<text x="{x + 20}" y="152" fill="#e5ecf5" font-size="13" font-weight="600" {SANS}>{escape(label)}</text>')
        add(f'<text x="{x + 20}" y="168" fill="{DIM}" font-size="11.5" {SANS}>{escape(sub)}</text>')

    # heatmap
    add(f'<rect x="20" y="192" width="{W - 40}" height="250" rx="14" fill="{CARD}" stroke="{LINE}"/>')
    add(f'<text x="44" y="224" fill="#fff" font-size="15" font-weight="700" {SANS}>Last 12 months</text>')
    add(f'<text x="160" y="224" fill="{DIM}" font-size="12" {SANS}>every square is a day</text>')
    weeks = s["weeks"]
    cell, gap = 15, 4
    gx = W - 40 - len(weeks) * (cell + gap)
    gx = 20 + max(70, (W - 40 - len(weeks) * (cell + gap)) / 2)
    gy = 262
    for label, row in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
        add(f'<text x="{gx - 12}" y="{gy + row * (cell + gap) + 11}" fill="{DIM}" font-size="10.5" text-anchor="end" {SANS}>{label}</text>')
    peak = s["peak_count"]
    last_month = None
    flat_index = 0
    streak_start_idx = s["streak_end"] - s["longest"] + 1 if s["streak_end"] is not None else None
    streak_cols = set()
    for wi, w in enumerate(weeks):
        x = gx + wi * (cell + gap)
        first = dt.date.fromisoformat(w["contributionDays"][0]["date"])
        if first.month != last_month and first.day <= 7:
            add(f'<text x="{x}" y="{gy - 8}" fill="{DIM}" font-size="10.5" {SANS}>{MONTHS[first.month - 1]}</text>')
            last_month = first.month
        for d in w["contributionDays"]:
            y = gy + d["weekday"] * (cell + gap)
            lv = level(d["contributionCount"], peak)
            extra = ""
            if d["date"] == s["peak"]["date"] and peak > 0:
                extra = ' stroke="#e5ecf5" stroke-width="1.5"'
            add(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[lv]}"{extra}/>')
            if streak_start_idx is not None and streak_start_idx <= flat_index <= s["streak_end"]:
                streak_cols.add(wi)
            flat_index += 1
    if s["longest"] > 1 and streak_cols:
        x1 = gx + min(streak_cols) * (cell + gap)
        x2 = gx + max(streak_cols) * (cell + gap) + cell
        yb = gy + 7 * (cell + gap) + 4
        add(f'<path d="M {x1} {yb - 4} v 4 H {x2} v -4" stroke="#39d353" stroke-width="1.5" fill="none"/>')
        add(f'<text x="{(x1 + x2) / 2}" y="{yb + 15}" fill="#39d353" font-size="11.5" font-weight="700" text-anchor="middle" {SANS}>{s["longest"]}-day streak</text>')
    if peak > 0:
        pdate = dt.date.fromisoformat(s["peak"]["date"])
        tag = f'{peak} on {MONTHS[pdate.month - 1]} {pdate.day}'
        tw = len(tag) * 7 + 24
        add(f'<rect x="{W - 44 - tw}" y="206" width="{tw}" height="24" rx="12" fill="#e5ecf5"/>')
        add(f'<text x="{W - 44 - tw / 2}" y="222" fill="#0b0f1a" font-size="12" font-weight="700" text-anchor="middle" {SANS}>{tag}</text>')
    lx = W - 44 - 5 * 19 - 70
    add(f'<text x="{lx}" y="428" fill="{DIM}" font-size="10.5" {SANS}>Less</text>')
    for i, c in enumerate(LEVELS):
        add(f'<rect x="{lx + 30 + i * 19}" y="418" width="14" height="14" rx="3" fill="{c}"/>')
    add(f'<text x="{lx + 30 + 5 * 19 + 4}" y="428" fill="{DIM}" font-size="10.5" {SANS}>More</text>')

    small = [
        (f'{s["longest"]} days', "longest streak"),
        (fmt(s["peak_count"]), "contributions in one day"),
        (fmt(s["active"]), "active days of the last 365"),
        (fmt(s["busiest_month_count"]), f'in {MONTHS[s["busiest_month"][1] - 1]} {s["busiest_month"][0]}, the busiest month'),
        (s["busiest_weekday"], "busiest day of the week"),
    ]
    sw = (W - 40 - 4 * 12) / 5
    for i, (big, label) in enumerate(small):
        x = 20 + i * (sw + 12)
        add(f'<rect x="{x}" y="458" width="{sw}" height="96" rx="14" fill="{CARD}" stroke="{LINE}"/>')
        add(f'<text x="{x + 20}" y="500" fill="#fff" font-size="24" font-weight="800" {SANS}>{escape(big)}</text>')
        add(f'<text x="{x + 20}" y="528" fill="{DIM}" font-size="12" {SANS}>{escape(label)}</text>')

    add(f'<text x="24" y="592" fill="{DIM}" font-size="11.5" {SANS}>From the GitHub API, redrawn twice a day. Private work is counted, never named.</text>')
    add(f'<text x="{W - 24}" y="592" fill="{DIM}" font-size="11.5" text-anchor="end" {SANS}>updated {today.isoformat()}</text>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="620" viewBox="0 0 {W} 620" role="img" '
        f'aria-label="GitHub activity for {escape(USER)}: {fmt(s["total"])} contributions in the last 12 months">'
        + "".join(out)
        + "</svg>"
    )


def render_mobile(s, today):
    W, out = 640, []
    add = out.append
    cards = [
        (fmt(s["total"]), "contributions, 12 months"),
        (fmt(s["public_commits"] + s["private"]), "commits and private work"),
        (fmt(s["merged"]), "pull requests merged"),
        (fmt(s["repos"]), "repositories with commits"),
    ]
    y = 24
    for i, (big, label) in enumerate(cards):
        x = 20 + (i % 2) * 306
        yy = y + (i // 2) * 150
        add(f'<rect x="{x}" y="{yy}" width="294" height="136" rx="16" fill="{CARD}" stroke="{LINE}"/>')
        add(f'<rect x="{x + 22}" y="{yy + 22}" width="32" height="5" rx="2.5" fill="{ACCENTS[i]}"/>')
        add(f'<text x="{x + 22}" y="{yy + 82}" fill="#fff" font-size="44" font-weight="800" {SANS}>{big}</text>')
        add(f'<text x="{x + 22}" y="{yy + 116}" fill="#c9d4e3" font-size="19" {SANS}>{escape(label)}</text>')
    y += 312
    weeks = s["weeks"][-26:]
    cell, gap = 18, 4
    add(f'<rect x="20" y="{y}" width="600" height="250" rx="16" fill="{CARD}" stroke="{LINE}"/>')
    add(f'<text x="44" y="{y + 40}" fill="#fff" font-size="22" font-weight="700" {SANS}>Last 6 months</text>')
    gx, gy = 44, y + 66
    peak = s["peak_count"]
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            add(f'<rect x="{gx + wi * (cell + gap)}" y="{gy + d["weekday"] * (cell + gap)}" width="{cell}" height="{cell}" rx="4" fill="{LEVELS[level(d["contributionCount"], peak)]}"/>')
    y += 266
    small = [(f'{s["longest"]} days', "longest streak"), (fmt(s["active"]), "active days, 12 months"),
             (fmt(s["peak_count"]), "most in one day"), (s["busiest_weekday"], "busiest weekday")]
    for i, (big, label) in enumerate(small):
        x = 20 + (i % 2) * 306
        yy = y + (i // 2) * 124
        add(f'<rect x="{x}" y="{yy}" width="294" height="110" rx="16" fill="{CARD}" stroke="{LINE}"/>')
        add(f'<text x="{x + 22}" y="{yy + 56}" fill="#fff" font-size="32" font-weight="800" {SANS}>{escape(big)}</text>')
        add(f'<text x="{x + 22}" y="{yy + 90}" fill="{DIM}" font-size="18" {SANS}>{escape(label)}</text>')
    y += 252
    add(f'<text x="24" y="{y}" fill="{DIM}" font-size="16" {SANS}>Redrawn twice a day · updated {today.isoformat()}</text>')
    H = y + 24
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="GitHub activity for {escape(USER)}">'
        f'<rect width="{W}" height="{H}" rx="18" fill="{BG}" stroke="{LINE}"/>' + "".join(out) + "</svg>"
    )


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--fixture":
        with open(sys.argv[2], encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        data = fetch()
    svg = render(stats(data), dt.date.today())
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(svg)
    mobile_out = OUT.replace(".svg", "-mobile.svg")
    with open(mobile_out, "w", encoding="utf-8") as fh:
        fh.write(render_mobile(stats(data), dt.date.today()))
    print(f"wrote {OUT} and {mobile_out}")


if __name__ == "__main__":
    main()
