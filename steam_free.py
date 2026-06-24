#!/usr/bin/env python3
"""Steam Free Games Tracker — finds free / 100%-off Steam games and builds a
clickable HTML page with one-click claim links.

Safe by design: it only READS public data (no Steam login, no automation), so
there's zero account risk. You click "Claim" yourself — Steam adds the game in
a couple of seconds.

Sources:
  * GamerPower API  — free-to-keep Steam giveaways (title, value, end date, claim link)
  * Steam store API — current specials filtered to 100% off

Usage:
    python steam_free.py            # fetch + build the page + open it
    python steam_free.py --no-open  # build the page without opening a browser
"""
from __future__ import annotations

import argparse
import html
import json
import sys
import urllib.request
import webbrowser
from datetime import datetime

UA = {"User-Agent": "Steam-Free-Games-Tracker/1.0"}
OUT = "steam-free-games.html"


def _get(url, timeout=20):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout))


def gamerpower():
    """Free-to-keep Steam game giveaways."""
    try:
        data = _get("https://www.gamerpower.com/api/giveaways?platform=steam&type=game")
    except Exception as e:  # noqa
        print(f"  (GamerPower fetch failed: {e})", file=sys.stderr)
        return []
    out = []
    for g in data if isinstance(data, list) else []:
        if str(g.get("status", "")).lower() != "active":
            continue
        out.append({
            "title": g.get("title", "Unknown").replace(" Giveaway", ""),
            "worth": g.get("worth") or "Free",
            "ends": g.get("end_date") or "Limited time",
            "url": g.get("open_giveaway_url") or g.get("gamerpower_url"),
            "img": g.get("thumbnail") or g.get("image"),
            "source": "GamerPower",
        })
    return out


def steam_specials():
    """Steam's own specials, filtered to 100% off (genuinely free right now)."""
    try:
        data = _get("https://store.steampowered.com/api/featuredcategories/?cc=us&l=en")
    except Exception as e:  # noqa
        print(f"  (Steam specials fetch failed: {e})", file=sys.stderr)
        return []
    items = (data.get("specials") or {}).get("items", []) if isinstance(data, dict) else []
    out = []
    for it in items:
        if it.get("discount_percent", 0) >= 100 or (it.get("discounted") and it.get("final_price") == 0):
            orig = it.get("original_price")
            worth = f"${orig/100:,.2f}" if isinstance(orig, int) and orig else "Free"
            out.append({
                "title": it.get("name", "Unknown"),
                "worth": worth,
                "ends": "Limited-time Steam offer",
                "url": f"https://store.steampowered.com/app/{it.get('id')}/",
                "img": it.get("large_capsule_image") or it.get("header_image"),
                "source": "Steam 100% off",
            })
    return out


def collect():
    games = gamerpower() + steam_specials()
    seen, uniq = set(), []
    for g in games:
        key = g["title"].lower().replace("(steam)", "").strip()
        if key in seen:
            continue
        seen.add(key)
        uniq.append(g)
    uniq.sort(key=lambda g: str(g["ends"]))
    return uniq


def build_html(games):
    e = html.escape
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cards = []
    for g in games:
        img = e(g["img"] or "")
        cards.append(f"""
      <div class="card">
        <a class="thumb" href="{e(g['url'])}" target="_blank" rel="noopener"
           style="background-image:url('{img}')"><span class="free">FREE</span></a>
        <div class="body">
          <div class="title">{e(g['title'])}</div>
          <div class="meta"><span class="was">was {e(str(g['worth']))}</span>
            <span class="src">{e(g['source'])}</span></div>
          <div class="ends">Ends: {e(str(g['ends']))}</div>
          <a class="claim" href="{e(g['url'])}" target="_blank" rel="noopener">Claim free →</a>
        </div>
      </div>""")
    grid = "".join(cards) if cards else (
        '<div class="empty">No free or 100%-off Steam games right now. '
        'Re-run the tracker later — new giveaways appear often.</div>')
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Free Steam Games — {len(games)} available</title>
<style>
  :root{{--bg:#1b2838;--panel:#22344a;--line:#33455e;--text:#e7eef5;--muted:#8fa3b8;--green:#5ba32b;--green2:#6fc134}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);padding:26px}}
  .wrap{{max-width:1100px;margin:0 auto}}
  h1{{font-size:24px}} h1 span{{color:var(--green2)}}
  .sub{{color:var(--muted);font-size:13px;margin:4px 0 22px}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}}
  .card{{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;transition:.2s}}
  .card:hover{{transform:translateY(-4px);border-color:var(--green)}}
  .thumb{{display:block;height:130px;background:#0e1520 center/cover no-repeat;position:relative}}
  .free{{position:absolute;top:10px;left:10px;background:var(--green);color:#fff;font-size:12px;font-weight:700;padding:3px 10px;border-radius:5px;letter-spacing:.05em}}
  .body{{padding:14px 16px 16px}}
  .title{{font-size:16px;font-weight:600;margin-bottom:8px;line-height:1.3}}
  .meta{{display:flex;justify-content:space-between;align-items:center;font-size:12px;margin-bottom:6px}}
  .was{{color:var(--muted);text-decoration:line-through}} .src{{color:var(--muted)}}
  .ends{{color:var(--muted);font-size:12px;margin-bottom:14px}}
  .claim{{display:block;text-align:center;background:var(--green);color:#fff;text-decoration:none;font-weight:600;padding:10px;border-radius:7px}}
  .claim:hover{{background:var(--green2)}}
  .empty{{grid-column:1/-1;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:50px;text-align:center;color:var(--muted)}}
  .foot{{color:var(--muted);font-size:12px;text-align:center;margin-top:26px;line-height:1.6}}
</style></head>
<body><div class="wrap">
  <h1>🎮 Free Steam Games — <span>{len(games)} available</span></h1>
  <div class="sub">Last checked {now}. Click “Claim free” → it opens Steam; you confirm and it's yours. No login automation, no account risk.</div>
  <div class="grid">{grid}</div>
  <p class="foot">Re-run <b>steam_free.py</b> (or <b>run.bat</b>) to refresh.<br>
  Sources: GamerPower free-game giveaways + Steam 100%-off specials.</p>
</div></body></html>"""


def main(argv=None):
    ap = argparse.ArgumentParser(description="Find free / 100%-off Steam games and build a claim page.")
    ap.add_argument("--no-open", action="store_true", help="don't auto-open the page in a browser")
    args = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa
        pass

    print("Checking for free Steam games...")
    games = collect()
    open(OUT, "w", encoding="utf-8").write(build_html(games))

    if games:
        print(f"\n  {len(games)} free / 100%-off game(s):")
        for g in games:
            print(f"   • {g['title']}  (was {g['worth']}, ends {g['ends']})")
    else:
        print("  None available right now — page built anyway.")
    print(f"\nPage written to {OUT}")
    if not args.no_open:
        import os
        webbrowser.open("file://" + os.path.abspath(OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
