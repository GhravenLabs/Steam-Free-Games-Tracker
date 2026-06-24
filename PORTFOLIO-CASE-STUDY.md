# Portfolio Case Study: Steam Free Games Tracker

## Problem
Free-to-keep PC game offers are scattered across stores, giveaway sites, and limited-time promotions. It is easy to miss a legitimate free game unless you check multiple pages often.

## Build
Steam Free Games Tracker pulls public giveaway data, filters Steam offers that are free or 100% off, deduplicates the results, and generates a self-contained HTML page with claim links.

## Why it is useful
- Uses public APIs and does not require a login, API key, or browser extension.
- Produces a simple page that can be refreshed daily.
- Shows API fetching, data normalization, de-duplication, and static HTML generation in one small Python tool.
- Makes a relatable portfolio example that is easy for non-technical visitors to understand.

## Verification
- Generated HTML proof: `steam-free-games.html`
- Screenshot: `assets/screenshot.png`
- Smoke check: `.github/workflows/smoke.yml`

## Next upgrades
- Add a local history file so repeated offers can be marked "seen."
- Add optional Discord/email notification when new games appear.
- Split third-party key giveaways from native Steam free packages in the UI.
