@echo off
echo ==========================================
echo  Starting Personalized Learning Platform
echo ==========================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Starting the application...
echo.
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
