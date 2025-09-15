#!/usr/bin/env python3
"""
User Management Script for Personalized Learning Platform
Usage: python add_user.py
"""

import os
import sys
from db import create_user, get_connection

def add_user_interactive():
    """Interactive script to add a new user"""
    print("=== Add New User ===")
    print()
    
    # Get user details
    email = input("Email address: ").strip()
    if not email or '@' not in email:
        print("Error: Please enter a valid email address")
        return False
    
    username = input("Username: ").strip()
    if not username:
        print("Error: Username cannot be empty")
        return False
    
    password = input("Password: ").strip()
    if not password:
        print("Error: Password cannot be empty")
        return False
    
    # Check if user already exists
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check email
    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        print(f"Error: User with email {email} already exists")
        conn.close()
        return False
    
    # Check username
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        print(f"Error: Username {username} already exists")
        conn.close()
        return False
    
    conn.close()
    
    # Create user
    try:
        user_id = create_user(username, password, is_guest=False, email=email)
        print(f"✅ User created successfully!")
        print(f"   User ID: {user_id}")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print()
        print("User can now login with their email and password.")
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def list_users():
    """List all existing users"""
    print("=== Current Users ===")
    print()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, created_at, is_guest FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    conn.close()
    
    if not users:
        print("No users found.")
        return
    
    print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Created':<20} {'Type':<10}")
    print("-" * 85)
    
    for user in users:
        user_type = "Guest" if user[4] else "Regular"
        print(f"{user[0]:<5} {user[1]:<20} {user[2] or 'N/A':<30} {user[3]:<20} {user_type:<10}")

def main():
    """Main menu"""
    while True:
        print("\n=== Personalized Learning - User Management ===")
        print("1. Add new user")
        print("2. List all users") 
        print("3. Exit")
        print()
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == '1':
            add_user_interactive()
        elif choice == '2':
            list_users()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
