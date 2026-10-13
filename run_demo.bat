@echo off
cd /d "%~dp0"
python score_ceos.py demo --output-dir outputs/demo --resume
if errorlevel 1 (
  echo Demo failed. See the message above.
) else (
  echo Open outputs\demo\ratings.xlsx to inspect the results.
)
pause
