@echo off
chcp 65001 > nul
title Combined Cycle CCGT Master Game
cd /d "%~dp0"
python "game_03_combined_cycle_ccgt.py"
pause
