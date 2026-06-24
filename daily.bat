@echo off
rem Silent daily run for Task Scheduler — only opens the page if a free game is found.
cd /d "%~dp0"
py steam_free.py --open-if-any 2>nul
if errorlevel 1 python steam_free.py --open-if-any
