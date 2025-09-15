#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import json
from db import get_connection, get_user_by_email_credentials, create_user

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        print(f"Login attempt - Email: {email}")
        
        try:
            user = get_user_by_email_credentials(email, password)
            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['email'] = user[3] if len(user) > 3 else email
                print(f"Login successful for user: {user[1]}")
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                print(f"Login failed for email: {email}")
                flash('Invalid email or password. Please check your credentials.', 'error')
        except Exception as e:
            print(f"Login error: {e}")
            flash('An error occurred during login. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        print(f"Signup attempt - Email: {email}, Username: {username}")
        
        try:
            user_id = create_user(username, email, password)
            if user_id:
                session['user_id'] = user_id
                session['username'] = username
                session['email'] = email
                print(f"Signup successful for user: {username}")
                flash('Account created successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Failed to create account. Email might already exist.', 'error')
        except Exception as e:
            print(f"Signup error: {e}")
            flash('Email already exists or other error occurred.', 'error')
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    
    try:
        # Load course data for dashboard
        courses_data = []
        quiz_files = [
            "html_&_css_basics.json",
            "javascript_essentials.json", 
            "react_development.json",
            "node_js_backend_development.json",
            "web_development_with_php.json",
            "java_programming.json",
            "advanced_java.json",
            "data_structures_&_algorithms.json",
            "machine_learning.json",
            "aws.json",
            "docker_&_containerization.json",
            "advanced_css_&_responsive_design.json"
        ]
        
        for i, filename in enumerate(quiz_files, 1):
            course_name = filename.replace('.json', '').replace('_', ' ').replace('&', 'and').title()
            courses_data.append({
                'id': i,
                'title': course_name,
                'description': f'Master {course_name.lower()} with interactive lessons and quizzes'
            })
        
        return render_template('dashboard.html', courses=courses_data)
    except Exception as e:
        print(f"Dashboard error: {e}")
        flash('Error loading dashboard. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/quiz_page')
def quiz_page():
    if 'user_id' not in session:
        flash('Please log in to access quizzes.', 'error')
        return redirect(url_for('login'))
    
    try:
        # Simple quiz page for testing
        return "<h1>Quiz Page</h1><p>Quiz functionality will be implemented here.</p><a href='/dashboard'>Back to Dashboard</a>"
    except Exception as e:
        print(f"Quiz page error: {e}")
        flash('Error loading quiz. Please try again.', 'error')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    print("Starting authentication test Flask app...")
    print("Available user: 99220040045@klu.ac.in")
    app.run(debug=True, host='0.0.0.0', port=5000)
