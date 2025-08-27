# Personalized Learning Platform

A Flask-based learning platform with real-time emotion detection and interactive courses.

## Features
- User authentication and dashboard
- Interactive courses with modules and quizzes
- Real-time emotion detection using webcam
- Progress tracking and analytics
- Responsive web interface

## Prerequisites
- Python 3.8 or higher
- Webcam (for emotion detection)
- Modern web browser (Chrome, Firefox, Edge)

## Installation & Setup

### Step 1: Extract the Project
1. Extract the zip file to any folder on your computer
2. Open Command Prompt or PowerShell as Administrator

### Step 2: Navigate to Project Directory
```bash
cd "path\to\extracted\folder\personalize learning"
```

### Step 3: Create Virtual Environment (Recommended)
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Initialize Database
```bash
python db.py
```

### Step 6: Run the Application
```bash
python app.py
```

### Step 7: Access the Application
Open your web browser and go to: `http://localhost:5000`

## Default Login Credentials
- **Email:** admin@example.com
- **Password:** admin123

Or create a new account using the signup page.

## Troubleshooting

### If you get "Python not found" error:
1. Install Python from https://python.org
2. During installation, check "Add Python to PATH"
3. Restart your command prompt

### If you get package installation errors:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### If webcam doesn't work:
1. Allow browser to access camera when prompted
2. Make sure no other application is using the camera
3. Try refreshing the page

### If the app doesn't start:
1. Make sure you're in the correct directory
2. Check if virtual environment is activated
3. Try: `python -m flask run`

## Project Structure
```
personalize learning/
├── app.py              # Main Flask application
├── db.py               # Database functions
├── ml_models.py        # Emotion detection models
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
├── static/            # CSS, JS, and static files
├── data/              # Course data and questions
└── scripts/           # Utility scripts
```

## Support
If you encounter any issues, please check:
1. Python version is 3.8+
2. All dependencies are installed
3. Virtual environment is activated
4. Camera permissions are granted

## Notes
- The emotion detection feature requires a webcam
- Some antivirus software may block the application - add it to exceptions if needed
- For best performance, use Chrome or Firefox browser
