# Steam Free Games Tracker

Finds **free / 100%-off Steam games** and builds a clean, clickable HTML page with one-click
**claim links**. Pure Python standard library — no dependencies, no Steam login.

![Steam Free Games Tracker screenshot](assets/screenshot.png)

## Portfolio proof
- [Case study](PORTFOLIO-CASE-STUDY.md) — how a small automation tool turns public APIs into a useful daily dashboard.
- GitHub Actions compiles the script, checks CLI help, renders a synthetic game in memory, and runs offline regression tests.

## Account access and offer limits
The tracker only **reads public data**. It does not request Steam credentials, log into your
account, or claim games for you. Offer links may lead to Steam or a third-party giveaway page;
check the destination and its requirements before signing in or redeeming a key.

Listings can expire, run out of keys, or have regional restrictions. The tracker does not
guarantee availability, successful redemption, or the safety of a third-party destination.
An empty page means no offers were returned by this run; check terminal warnings for failed
API requests before interpreting it as an absence of giveaways.

## Usage
```bash
python steam_free.py            # fetch, build the page, and open it
python steam_free.py --no-open  # build the page without opening a browser
```
Or just **double-click `run.bat`** (Windows).

The generated page is saved in the current working directory. Browser opening supports
paths containing spaces, `#`, and `%`; the Windows launchers use their own folder.

Run `python -m unittest -v` for offline regression checks of file links and browser-opening
flags. Tests use synthetic games and mock the browser; they do not contact either API.

## What it does
1. Pulls free-to-keep **Steam giveaways** from the GamerPower API (title, value, end date, claim link).
2. Pulls Steam's own **specials** and keeps the ones at **100% off** (free right now).
3. De-duplicates, sorts by end date, and writes `steam-free-games.html` — a card grid with claim buttons.

## Keep it automatic (optional)
Optionally use **Windows Task Scheduler** to run `daily.bat` once a day. It opens the page only
when offers are returned. Refreshes depend on the computer running, network access, and API
availability; the two sources do not cover every giveaway. Cloning or running this repository
does not install a scheduled task.

See [automation scope](AUTO-CLAIM-SETUP.md) for scheduling and manual-redemption boundaries.

## Tech
Standard-library only (`urllib`, `json`, `html`): fetches two public APIs, merges/dedupes, and
generates a self-contained HTML page. No `pip install`, no keys.

## License
MIT © Rolly Calma ([Ghraven](https://github.com/Ghraven))
