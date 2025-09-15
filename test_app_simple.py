from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import sqlite3
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/')
def index():
    return "Test app running"

@app.route('/test_quiz')
def test_quiz():
    import glob
    quiz_dir = os.path.join('data', 'quiz_questions', '*.json')
    files = glob.glob(quiz_dir)
    return f"Found {len(files)} quiz files: {files}"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
