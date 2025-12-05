# Personalized Learning Platform

A Flask-based learning platform with real-time emotion detection, interactive courses, and personalized learning paths.

## 🎓 Features
- **User Authentication**: Secure login and registration system
- **Interactive Courses**: Structured courses with modules and quizzes
- **Real-time Emotion Detection**: Webcam-based emotion analysis for engagement tracking
- **Progress Tracking**: Detailed learning analytics and progress dashboard
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Quiz System**: Auto-graded quizzes with instant feedback
- **Personalized Learning**: Adaptive content based on user performance

## 📋 Prerequisites
- **Python 3.8+** (Python 3.12 recommended)
- **Webcam** (for emotion detection features)
- **Modern Browser**: Chrome, Firefox, or Edge

## 🚀 Quick Start

### Option 1: One-Click Start (Easiest)
Simply double-click the `start.bat` file in the project folder. This will:
1. Activate the virtual environment
2. Install/update dependencies if needed
3. Initialize the database
4. Start the application

### Option 2: Manual Setup

#### Step 1: Navigate to Project Directory
```bash
cd "path\to\personalize learning"
```

#### Step 2: Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Initialize Database
```bash
python db.py
```

#### Step 5: Run the Application
```bash
python app.py
```

#### Step 6: Access the Application
Open your browser and navigate to: **http://localhost:5000**

## 🔐 Default Login Credentials
- **Email**: admin@example.com
- **Password**: admin123

You can also create a new account using the signup page.

## 📁 Project Structure
```
personalize-learning/
├── start.bat               # Quick start batch file
├── app.py                  # Main Flask application
├── db.py                   # Database initialization
├── ml_models.py            # Emotion detection models
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── course.html
│   └── ...
├── static/                 # CSS, JavaScript, models
│   ├── css/
│   ├── js/
│   └── models/
├── data/                   # Quiz questions and course data
└── scripts/                # Database initialization scripts
```

## 🔧 Configuration

The application uses the following default configuration:
- **Host**: localhost (127.0.0.1)
- **Port**: 5000
- **Database**: SQLite (app.db)
- **Debug Mode**: Enabled (development)

## 🐛 Troubleshooting

### "Python not found" error
```
1. Install Python from https://www.python.org/
2. During installation, check "Add Python to PATH"
3. Restart your command prompt or PowerShell
```

### Package installation errors
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Webcam not working
1. Grant camera permissions when browser prompts
2. Ensure no other application is using the camera
3. Refresh the page
4. Try a different browser

### Application won't start
1. Verify virtual environment is activated (`.venv` in prompt)
2. Check Python version: `python --version`
3. Try running: `python -m flask run`
4. Check if port 5000 is already in use

### Virtual environment issues
```bash
# Recreate virtual environment
rmdir /s .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 📝 Notes
- Emotion detection requires a functioning webcam and camera permissions
- Some antivirus software may interfere with the application
- For production deployment, use a production WSGI server (Gunicorn, uWSGI)
- Database is stored locally as SQLite; consider PostgreSQL for production

## 📚 Support
For issues or questions:
1. Check that Python 3.8+ is installed
2. Verify all dependencies are installed
3. Ensure virtual environment is activated
4. Check browser console for errors (F12)

## 📄 License
This project is provided as-is for educational purposes.