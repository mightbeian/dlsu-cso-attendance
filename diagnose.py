"""
Diagnostic script to test the DLSU-D CSO Attendance System
Run this to check if everything is working correctly
"""

import sys
import os

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def check_python_version():
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python version is compatible")
        return True
    else:
        print("✗ Python version is too old. Please upgrade to 3.8+")
        return False

def check_dependencies():
    print_header("Checking Dependencies")
    required = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'openpyxl': 'openpyxl',
        'werkzeug': 'Werkzeug'
    }
    
    all_ok = True
    for module, name in required.items():
        try:
            __import__(module)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is NOT installed")
            all_ok = False
    
    if not all_ok:
        print("\nTo install missing packages, run:")
        print("  pip install -r requirements.txt")
    
    return all_ok

def check_database():
    print_header("Checking Database")
    try:
        from app import app, db, User, Attendance
        
        with app.app_context():
            # Check if tables exist
            try:
                user_count = User.query.count()
                attendance_count = Attendance.query.count()
                print(f"✓ Database is accessible")
                print(f"  - Users in database: {user_count}")
                print(f"  - Attendance records: {attendance_count}")
                
                if user_count == 0:
                    print("\n⚠ Warning: No users in database!")
                    print("  Run the app first to create sample users: python app.py")
                
                return True
            except Exception as e:
                print(f"✗ Database tables not created: {str(e)}")
                print("  Run the app first: python app.py")
                return False
                
    except Exception as e:
        print(f"✗ Cannot load database: {str(e)}")
        return False

def check_files():
    print_header("Checking Project Files")
    required_files = {
        'app.py': 'Main application',
        'database.py': 'Database models',
        'requirements.txt': 'Dependencies list',
        'templates/index.html': 'Main HTML template',
        'static/style.css': 'CSS stylesheet',
        'static/script.js': 'JavaScript file'
    }
    
    all_ok = True
    for file, desc in required_files.items():
        if os.path.exists(file):
            print(f"✓ {file} - {desc}")
        else:
            print(f"✗ {file} - {desc} - MISSING!")
            all_ok = False
    
    return all_ok

def check_folders():
    print_header("Checking Folders")
    folders = ['templates', 'static', 'exports']
    
    for folder in folders:
        if os.path.exists(folder):
            print(f"✓ {folder}/ exists")
        else:
            if folder == 'exports':
                print(f"⚠ {folder}/ does not exist (will be created automatically)")
            else:
                print(f"✗ {folder}/ does not exist - REQUIRED!")

def test_imports():
    print_header("Testing Imports")
    try:
        print("Importing Flask...")
        from flask import Flask
        print("✓ Flask imported")
        
        print("Importing database...")
        from database import db, User, Attendance
        print("✓ Database models imported")
        
        print("Importing app...")
        from app import app
        print("✓ App imported")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {str(e)}")
        return False

def run_diagnostics():
    print("\n" + "="*60)
    print("  DLSU-D CSO Attendance System - Diagnostic Tool")
    print("="*60)
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Project Files': check_files(),
        'Folders': check_folders(),
        'Imports': test_imports(),
        'Database': check_database()
    }
    
    print_header("Diagnostic Summary")
    
    all_passed = True
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test:20s} : {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("✓ All checks passed! Your system is ready to use.")
        print("\nTo start the server, run:")
        print("  python app.py")
        print("\nThen open your browser to:")
        print("  http://127.0.0.1:5000")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Make sure you're in the project directory")
        print("3. Run the app once to create database: python app.py")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    run_diagnostics()
