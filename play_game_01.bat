@echo off
chcp 65001 > nul
title Turbine Control Room Game
cd /d "%~dp0"
python "game_01_control_room.py"
pause
