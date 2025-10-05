@echo off
REM Simple launcher for Windows
REM Double-click to run the game!

title Pong AI V2

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ============================================================
    echo   ERROR: Python not found
    echo ============================================================
    echo.
    echo Python 3.10+ is required to run this game.
    echo.
    echo Download from: https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo ============================================================
    pause
    exit /b 1
)

REM Try to run the game
echo Running Pong AI V2...
python main.py

REM If we get here, the game exited
if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo   Game exited with errors
    echo ============================================================
    echo.
    echo Try installing dependencies:
    echo   pip install -r requirements.txt
    echo.
    echo Or see BUILD.md for detailed instructions.
    echo ============================================================
)

pause
