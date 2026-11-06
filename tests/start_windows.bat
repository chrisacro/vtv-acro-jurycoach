@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python-launcher niet gevonden. Installeer Python 3.11 of 3.12.
  pause
  exit /b 1
)
py -m pip install --upgrade ultralytics opencv-python pyyaml
if errorlevel 1 (
 echo Installatie mislukt. Controleer je internetverbinding en Python.
 pause
 exit /b 1
)
py vergelijk_trackers.py --selftest
if errorlevel 1 (
 echo Zelftest mislukt; proef afgebroken.
 pause
 exit /b 1
)
py vergelijk_trackers.py --video "Js 9-9.mp4" --reference "VTV_Acro_Trainingsanalyse_v126.json" --start 50 --end 149.9 --fps 5 --snapshots
pause
