@echo off
cd /d "%~dp0"
python score_ceos.py pilot --check
if errorlevel 1 (
  echo Pilot settings are invalid. See the message above.
  pause
  exit /b 1
)
set /p "choice=Type YES to make paid API calls: "
if /I not "%choice%"=="YES" (
  echo Cancelled.
  pause
  exit /b 0
)
python score_ceos.py pilot --resume --confirm-live-api
if errorlevel 1 (
  echo Pilot failed. See the message above.
) else (
  echo Open the output folder shown above and inspect ratings.xlsx.
)
pause
