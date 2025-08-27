# User Management Guide

## Email-Based Authentication System

This learning platform now uses email-based authentication only. Guest access has been removed for security.

## Adding New Users

### Method 1: Using the User Management Script
```bash
python add_user.py
```
This will start an interactive script where you can:
- Add new users
- List existing users
- Manage user accounts

### Method 2: Using Python directly
```python
from db import create_user

# Create a new user
user_id = create_user(
    username="johndoe", 
    password="securepassword", 
    is_guest=False, 
    email="john@example.com"
)
print(f"User created with ID: {user_id}")
```

## User Login

Users can login using:
- **Email address** (required)
- **Password** (required)

## Access Control

- ✅ **Email-based login only** - Users must have a valid email
- ❌ **No guest access** - All users must be registered
- ❌ **No self-registration** - Only administrators can create accounts
- ✅ **Secure authentication** - Passwords are hashed and stored securely

## Default Test User

A test user has been created:
- **Email**: test@example.com
- **Password**: password123

## Database Structure

Users are stored with the following information:
- ID (auto-increment)
- Username (unique)
- Email (unique, required)
- Password (hashed)
- Created/Updated timestamps
- Guest flag (always 0 for regular users)

## Features

- **Secure Login**: Only registered users with valid email/password can access
- **Session Management**: Users stay logged in until they logout
- **Admin Control**: Only administrators can create new user accounts
- **Database Storage**: All user data stored in SQLite database
