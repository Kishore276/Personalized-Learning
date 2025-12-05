# 📚 Personalized Learning Platform

A comprehensive Flask-based learning platform with real-time emotion detection, interactive courses, career pathways, and personalized learning analytics.

## ✨ Features

### Core Learning Features
- 🎓 **Interactive Courses**: Structured learning modules with progression tracking
- 📊 **Progress Tracking**: Real-time dashboard showing learning analytics
- 🧪 **Quiz System**: Auto-graded quizzes with instant feedback and explanations
- 🎯 **13+ Courses**: Diverse programming and technology courses

### Advanced Features
- 🎥 **Emotion Detection**: Real-time webcam-based emotion and concentration tracking
- 🚀 **Career Pathways**: 7 career recommendations with tech stack requirements
- 👤 **User Authentication**: Secure login and registration
- 📱 **Responsive Design**: Optimized for desktop and mobile devices
- 🔔 **Learning Analytics**: Detailed insights into learning patterns

## 📋 Prerequisites

- **Python 3.8+** (3.12 recommended)
- **Webcam** (for emotion detection features - optional)
- **Modern Browser**: Chrome, Firefox, Edge, or Safari

## 🚀 Quick Start

### Option 1: One-Click Start (Recommended)
Double-click `start.bat` in the project folder to automatically:
1. Setup virtual environment
2. Install dependencies
3. Initialize database
4. Launch the application

### Option 2: Manual Setup

```bash
# Navigate to project
cd "path\to\personalize learning"

# Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python db.py

# Run application
python app.py
```

Access the application at: **http://localhost:5000**

## 🔐 Login Credentials

**Default Account:**
- Email: `admin@example.com`
- Password: `admin123`

Or create a new account using the signup page.

## 📁 Project Structure

```
personalize-learning/
├── app.py                      # Main Flask application
├── db.py                        # Database initialization
├── ml_models.py                 # Emotion detection models
├── utils.py                     # Utility functions
├── requirements.txt             # Dependencies
├── career_recommendations.json  # Career pathway data
│
├── templates/                   # HTML templates
│   ├── dashboard.html          # Main dashboard
│   ├── career_recommendations.html  # Career pathways
│   ├── login.html
│   ├── signup.html
│   ├── course_modules.html
│   ├── quiz_page.html
│   └── ...
│
├── static/                     # CSS, JavaScript, assets
│   ├── css/
│   │   ├── dashboard.css
│   │   ├── ui-enhanced.css
│   │   └── ...
│   ├── js/
│   │   ├── webcam_hybrid.js    # Emotion detection
│   │   ├── quiz.js
│   │   └── ...
│   └── models/                 # ML model files
│
├── data/                       # Quiz data
│   └── quiz_questions/
│       ├── machine_learning.json
│       ├── java_programming.json
│       ├── react_development.json
│       └── ... (12+ more courses)
│
└── scripts/                    # Database utilities
    ├── init_quiz_schema.sql
    └── seed_courses.py
```

## 🎯 Available Courses

1. **Machine Learning** - Python-based ML fundamentals
2. **Java Programming** - Core Java concepts
3. **JavaScript Essentials** - JavaScript basics
4. **React Development** - Modern React framework
5. **Node.js Backend Development** - Server-side JavaScript
6. **Web Development with PHP** - PHP web development
7. **HTML & CSS Basics** - Web fundamentals
8. **Advanced CSS & Responsive Design** - Responsive web design
9. **Data Structures & Algorithms** - Core algorithms
10. **Docker & Containerization** - Container technology
11. **AWS** - Cloud computing basics
12. **And more...**

## 🚀 Career Pathways

Explore 7 professional career paths:

- **Machine Learning Developer** - Python, ML, Data Structures
- **Backend Developer** - Java, Node.js, PHP, Databases
- **Frontend Developer** - HTML/CSS, JavaScript, React
- **Full Stack Developer** - Complete web development
- **DevOps Engineer** - Docker, AWS, Infrastructure
- **Web Developer** - PHP, JavaScript, Web technologies
- **Data Structures Specialist** - Algorithms, Problem-solving

## 🎥 Emotion Detection

The platform includes real-time emotion and concentration tracking:
- 📹 Live webcam feed analysis
- 😊 Emotion classification (happy, focused, neutral, tired, etc.)
- 📊 Concentration scoring (0-100%)
- 💡 Real-time feedback on learning engagement

**Note**: Emotion detection is optional and requires webcam access.

## 🧪 Quiz System

Features include:
- ✅ Multiple difficulty levels (Basic, Intermediate, Advanced)
- 📝 20+ questions per level per course
- 💬 Detailed explanations for each answer
- 📊 Score tracking and analytics
- ⏱️ Timed quiz sessions

## 📊 Dashboard

The dashboard displays:
- 📚 Available courses to start
- 🔄 Ongoing courses with progress bars
- 📈 Learning statistics
- 🎯 Career pathways
- 🎥 Concentration detection status

## 🔧 Configuration

**Default Settings:**
- Host: localhost (127.0.0.1)
- Port: 5000
- Database: SQLite (app.db)
- Debug Mode: Enabled (development only)

To change settings, edit the bottom of `app.py`:
```python
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
```

## 🐛 Troubleshooting

### Python not found
Install Python from https://www.python.org/ or use Windows Store

### Port 5000 already in use
Change port in `app.py` or kill existing process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### Webcam not working
- Check browser permissions (Settings → Privacy → Camera)
- Ensure webcam is connected and working
- Try another browser
- Note: Not all features require webcam access

### Database issues
Delete `app.db` and run `python db.py` again to reinitialize

### Dependencies issues
```bash
pip install --upgrade -r requirements.txt
```

## 🔐 Security Notes

- **Development Only**: This is a development platform. Use appropriate security measures in production.
- **Password**: Hashed using werkzeug.security
- **Session**: Flask session-based authentication
- **Database**: Local SQLite (not recommended for production)

## 📱 Browser Compatibility

✅ Google Chrome (Latest)
✅ Mozilla Firefox (Latest)
✅ Microsoft Edge (Latest)
✅ Safari (Latest)
✅ Mobile Browsers

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Report bugs
2. Suggest features
3. Submit pull requests
4. Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the browser console (F12) for errors
3. Check application logs in the `logs/` directory

## 🎓 Learning Tips

1. **Start with Basics**: Complete foundational courses first
2. **Take Quizzes**: Test your knowledge after each module
3. **Check Career Paths**: Identify your learning goals
4. **Track Progress**: Monitor your advancement
5. **Use Emotion Detection**: Identify when concentration drops
6. **Practice Regularly**: Consistency is key to learning

## ✅ Getting Started Checklist

- [ ] Install Python 3.8+
- [ ] Clone/download the repository
- [ ] Run `start.bat` or follow manual setup
- [ ] Access http://localhost:5000
- [ ] Login with credentials or create account
- [ ] Explore courses and career pathways
- [ ] Enable webcam for emotion detection (optional)
- [ ] Start learning!

---

**Happy Learning!** 🎓📚

For the latest updates and issues, visit the project repository.
