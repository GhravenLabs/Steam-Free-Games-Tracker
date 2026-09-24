# Automation scope: scheduled discovery, manual redemption

This tracker refreshes a local page of offers. It does not log into Steam, redeem
keys, add games to a library, install account tools, or create a scheduled task.
The filename is retained for existing links; this is not an auto-claim setup guide.

## Optional scheduled refresh on Windows

1. Run `run.bat` once and inspect `steam-free-games.html`.
2. Create a Windows Task Scheduler task with your preferred daily trigger.
3. Set its action to run `daily.bat` using the full path to your clone.
4. To see the browser window, configure the task to run while you are logged on.
   Test the task and inspect its last-run result.

The launcher uses its own folder and runs `steam_free.py --open-if-any`.
It opens the page only when offers are returned. Use `python steam_free.py --no-open`
if you want to generate the page without opening a browser.

No task or startup entry is installed automatically. Inspect Task Scheduler to
confirm whether a task exists on your computer. Refreshes need an available Python
runtime, network access, and working source APIs.

## Redeeming an offer

Check the link destination. Some offers lead to Steam; others lead to a third-party
page with separate key-redemption steps. Offers may expire, run out of keys, or
have regional restrictions. This tracker does not guarantee successful redemption
or that every giveaway is listed.

Account automation is outside this project's scope. Third-party account tools have
their own behavior, credential handling, and applicable service terms; this project
does not endorse their safety or install them.
