@echo off
REM Build and run helper for Vision Inspector UI

SETLOCAL

REM Change to script directory
cd /d "%~dp0"

echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Dependencies installed.

echo To run the UI now, execute:
    python inspector_ui.py

echo.
echo Or press any key to exit.
pause >nul
ENDLOCAL
