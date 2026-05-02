@echo off
REM Mini C Compiler - Simple Batch Launcher
REM Double-click this file to run the application

echo.
echo ========================================
echo   Mini C Compiler - Professional IDE
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Starting Mini C Compiler...
echo.

REM Run the application
python ui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start application
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Application closed
echo.
pause
