@echo off
REM Simple wrapper to run the PowerShell build script
REM Double-click this file to build!

echo ============================================================
echo   PONG AI V2 - Windows EXE Builder
echo ============================================================
echo.
echo This will build a standalone .exe file (2-5 minutes)
echo.
pause

powershell -ExecutionPolicy Bypass -File "%~dp0build-exe.ps1"

pause
