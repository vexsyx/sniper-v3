@echo off
title Sol Sniper Builder
echo ================================
echo    Sol Sniper Build Script
echo ================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Attempting to install Python...
    echo Please download and install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo After installation, please run this script again.
    pause
    exit /b 1
)

echo [INFO] Python found, checking version...
python -c "import sys; print('Python version: ' + sys.version)"
python -c "import sys; exit(0) if sys.version_info >= (3, 8) else exit(1)"
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.8 or higher is required
    echo Current version is too old.
    pause
    exit /b 1
)

echo.
echo [INFO] Checking for PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] PyInstaller not found, installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo [SUCCESS] PyInstaller installed
) else (
    echo [INFO] PyInstaller found
)

echo.
echo [INFO] Installing/updating dependencies...
pip install -r ../requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [INFO] Starting build process...
echo [INFO] Using sniper.spec configuration...

:: Build the executable
pyinstaller sniper.spec

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed!
    echo Check the build log for details.
    pause
    exit /b 1
)

echo.
echo ================================
echo    BUILD SUCCESSFUL!
echo ================================
echo.
echo Your executable has been built in the 'dist' folder:
echo   - dist\Sol Sniper V3.exe
echo.
echo You can now distribute this standalone executable or run it directly.
echo.
pause