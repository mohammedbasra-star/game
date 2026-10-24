@echo off
chcp 65001 > nul
title Turbomachinery Diagnostic Detective Game
cd /d "%~dp0"
python "game_02_diagnostic_detective.py"
pause
