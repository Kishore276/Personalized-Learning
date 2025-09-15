#!/usr/bin/env python3
print("Starting test imports...")

try:
    print("1. Testing Flask import...")
    from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
    print("✓ Flask imports OK")
except Exception as e:
    print(f"✗ Flask import failed: {e}")

try:
    print("2. Testing other basic imports...")
    import os, sqlite3, hashlib, secrets, base64, json
    import numpy as np
    print("✓ Basic imports OK")
except Exception as e:
    print(f"✗ Basic imports failed: {e}")

try:
    print("3. Testing cv2 import...")
    import cv2
    print("✓ cv2 import OK")
except Exception as e:
    print(f"✗ cv2 import failed: {e}")

try:
    print("4. Testing dlib import...")
    import dlib
    print("✓ dlib import OK")
except Exception as e:
    print(f"✗ dlib import failed: {e}")

try:
    print("5. Testing db imports...")
    from db import get_connection, get_user_by_email_credentials, create_user
    print("✓ db imports OK")
except Exception as e:
    print(f"✗ db imports failed: {e}")

print("All import tests completed!")
