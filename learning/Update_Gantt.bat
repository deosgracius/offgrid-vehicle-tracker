@echo off
REM ============================================================
REM  Update Training_Gantt.html from tasks.json
REM  1) Edit tasks.json and save it
REM  2) Double-click this file
REM  3) Open (or hard-refresh, Ctrl+Shift+R) Training_Gantt.html
REM  4) Commit tasks.json + Training_Gantt.html together
REM ============================================================
cd /d "%~dp0"
python build_gantt.py
if errorlevel 1 (
  echo.
  echo  Something went wrong. Check that tasks.json is valid JSON.
) else (
  echo.
  echo  Done! Training_Gantt.html has been updated from tasks.json.
)
echo.
pause
