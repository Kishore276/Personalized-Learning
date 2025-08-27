#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from db import get_connection, get_user_by_email_credentials, create_user

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        print(f"Login attempt - Email: {email}")
        
        user = get_user_by_email_credentials(email, password)
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[3] if len(user) > 3 else email
            print(f"Login successful for user: {user[1]}")
            return redirect(url_for('dashboard'))
        else:
            print(f"Login failed for email: {email}")
            flash('Invalid email or password', 'error')
    
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
                return redirect(url_for('dashboard'))
            else:
                flash('Failed to create account', 'error')
        except Exception as e:
            print(f"Signup error: {e}")
            flash('Email already exists or other error', 'error')
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Simple dashboard for testing
    return f"<h1>Welcome to Dashboard!</h1><p>User: {session.get('username')}</p><p>Email: {session.get('email')}</p><a href='/logout'>Logout</a>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("Starting simple Flask app for authentication testing...")
    app.run(debug=True, host='0.0.0.0', port=5000)
