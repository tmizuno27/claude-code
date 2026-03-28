@echo off
REM Publish all Dev.to articles as drafts
cd /d "%~dp0"
python publish_to_devto.py
echo.
echo Done. Review drafts at https://dev.to/dashboard
pause
