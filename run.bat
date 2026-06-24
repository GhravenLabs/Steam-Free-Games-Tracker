@echo off
title Steam Free Games Tracker
cd /d "%~dp0"
py steam_free.py 2>nul
if errorlevel 1 python steam_free.py
echo.
pause
