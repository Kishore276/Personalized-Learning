@echo off
echo ==========================================
echo  Personalized Learning Platform Setup
echo ==========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Please make sure Python is installed and added to PATH
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call .venv\Scripts\activate.bat

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Trying with force reinstall...
    pip install -r requirements.txt --force-reinstall
)

echo Step 5: Initializing database...
python db.py

echo.
echo ==========================================
echo  Setup Complete!
echo ==========================================
echo.
echo To run the application:
echo 1. Make sure virtual environment is active
echo 2. Run: python app.py
echo 3. Open browser and go to: http://localhost:5000
echo.
echo Default login: admin@example.com / admin123
echo.
pause
