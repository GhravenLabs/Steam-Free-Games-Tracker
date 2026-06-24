# Auto-claiming free Steam games (hands-off) — the safe way

You asked for auto-claim. Here's the honest setup. I deliberately did **not** write a custom
claimer that logs into your Steam account, because that means handling your credentials and
automating your account — which is what gets accounts flagged/banned. Instead, use the
established, open-source tool that's purpose-built for this.

## The two halves of "fully hands-off"
| Part | Tool | What it does |
|---|---|---|
| **Find** everything free | this tracker (`steam_free.py`, runs daily) | Lists *all* free / 100%-off games, **including third-party key giveaways**. |
| **Auto-claim** | **ArchiSteamFarm (ASF)** | Automatically adds **Steam-native free packages** to your library in the background. |

Together that's hands-off: ASF auto-grabs the Steam-native freebies; the tracker shows the rest
(key giveaways) so you one-click those.

## Important limits (be honest with yourself)
- ASF auto-claims **Steam "free-to-keep" packages / free-on-demand games** — the ones that are free
  *on Steam itself*.
- It **cannot** auto-claim **third-party key giveaways** (the GamerPower-style ones where you visit a
  page to grab a CD key). Those aren't a Steam package, so no tool can silently claim them — the
  tracker surfaces them and you click "Claim" (2 seconds).
- **Risk:** automating your account is a grey area in Steam's Subscriber Agreement. ASF is extremely
  widely used and bans for free-package claiming are rare — but it's **your account, your call.**
  Use a strong password + keep **Steam Guard** on. Only *you* enter your credentials into ASF locally.

## Setup (high level — follow the official wiki for exact steps)
1. Download **ArchiSteamFarm** from the official releases:
   https://github.com/JustArchiNET/ArchiSteamFarm/releases
2. Unzip and run it. Open the web UI it prints (usually `http://localhost:1242`).
3. **Create a bot** = add your Steam account (username; ASF prompts for password + Steam Guard on
   first login). Official guide: https://github.com/JustArchiNET/ArchiSteamFarm/wiki/Configuration
4. To auto-claim free games, add the community plugin **ASFFreeGames**
   (https://github.com/maxisoft/ASFFreeGames) — drop it in ASF's `plugins/` folder. It watches a
   maintained list of free-to-keep games and claims them on your account automatically.
5. Leave ASF running (or set it to start with Windows / on a schedule). It now claims new Steam-native
   freebies hands-off.

## What I set up for you (the tracker side)
- A **daily Windows task** ("SteamFreeGamesTracker", 11:00) runs the tracker silently and only opens
  the page when there's a free game — so you're notified without lifting a finger.
- To change the time or remove it: Windows **Task Scheduler** → find "SteamFreeGamesTracker".

*Bottom line: the tracker (mine) + ASF (theirs) = the safe, near-fully-hands-off combo. I'm not
building an account-automation claimer myself — ASF is the right, maintained tool for that part.*
