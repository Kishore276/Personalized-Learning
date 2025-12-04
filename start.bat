@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo  Personalized Learning Platform
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Please make sure Python is installed and added to PATH
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing/updating dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo WARNING: Some dependencies may not have installed correctly
    echo Attempting force reinstall...
    pip install -r requirements.txt --force-reinstall
)

echo.
echo ==========================================
echo  Starting Application
echo ==========================================
echo.
echo The application will be available at:
echo   http://localhost:5000
echo.
echo Default login credentials:
echo   Email: admin@example.com
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

python app.py

pause
