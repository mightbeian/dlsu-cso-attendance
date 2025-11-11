# DLSU-D CSO Attendance System - Setup Guide

This guide provides detailed, step-by-step instructions for setting up the DLSU-D CSO Attendance System on a Windows computer.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Python Installation](#python-installation)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Auto-Start Configuration](#auto-start-configuration)
6. [User Management](#user-management)
7. [Maintenance & Backup](#maintenance--backup)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **Operating System:** Windows 7 or later (Windows 10/11 recommended)
- **RAM:** 2GB minimum
- **Storage:** 500MB free space
- **Python:** 3.8 or higher

### Recommended Requirements
- **Operating System:** Windows 10 or 11
- **RAM:** 4GB or more
- **Storage:** 1GB free space
- **Python:** 3.10 or higher

---

## Python Installation

### Step 1: Download Python

1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow button "Download Python 3.x.x"
3. Save the installer file (e.g., `python-3.11.5-amd64.exe`)

### Step 2: Install Python

1. **Run the installer** (double-click the downloaded file)
2. **⚠️ IMPORTANT:** Check these boxes:
   - ☑️ **"Add python.exe to PATH"** (bottom of installer window)
   - ☑️ "Install launcher for all users" (optional but recommended)
3. Click **"Install Now"**
4. Wait for installation to complete
5. Click **"Close"** when done

### Step 3: Verify Installation

1. Open **Command Prompt**:
   - Press `Win + R`
   - Type `cmd`
   - Press Enter

2. Type these commands to verify:
   ```bash
   python --version
   ```
   Should show: `Python 3.x.x`

   ```bash
   pip --version
   ```
   Should show: `pip xx.x.x from ...`

If both commands work, Python is installed correctly!

---

## Project Setup

### Step 1: Download the Project

**Option A: Using Git (if installed)**
```bash
git clone https://github.com/mightbeian/dlsud-cso-attendance.git
cd dlsud-cso-attendance
```

**Option B: Download ZIP**
1. Go to: https://github.com/mightbeian/dlsud-cso-attendance
2. Click green **"Code"** button
3. Click **"Download ZIP"**
4. Extract ZIP to desired location (e.g., `C:\dlsud-cso-attendance`)

### Step 2: Open Command Prompt in Project Folder

**Method 1: Using File Explorer**
1. Open File Explorer
2. Navigate to project folder
3. Click address bar at top
4. Type `cmd` and press Enter

**Method 2: Using cd command**
1. Open Command Prompt
2. Type: `cd C:\path\to\dlsud-cso-attendance`
3. Press Enter

### Step 3: Install Dependencies

In Command Prompt (in project folder):

```bash
pip install -r requirements.txt
```

Wait for installation to complete. You should see:
```
Successfully installed Flask-3.0.0 Flask-SQLAlchemy-3.1.1 openpyxl-3.1.2 Werkzeug-3.0.1
```

---

## Running the Application

### First Time Running

1. **Open Command Prompt** in project folder
2. **Run the application:**
   ```bash
   python app.py
   ```

3. **You should see:**
   ```
   Sample users added to database.
    * Running on http://127.0.0.1:5000
   Press CTRL+C to quit
   ```

4. **Open your web browser**
5. **Navigate to:** `http://127.0.0.1:5000`
6. **You should see the DLSU-D CSO Attendance System interface**

### Testing with Sample Users

The system comes with 3 sample users:

| ID Number | Name | Birthday |
|-----------|------|----------|
| 20212345 | Juan Dela Cruz | January 15 |
| 20212346 | Maria Santos | March 22 |
| 20212347 | Pedro Reyes | July 8 |

**Test the system:**
1. Type `20212345` in ID Number field
2. Click "TIME IN"
3. You should see: "Welcome, Juan Dela Cruz! You are timed in."
4. Try timing out: Type `20212345` again
5. Click "TIME OUT"
6. You should see: "Goodbye, Juan Dela Cruz! You are timed out."

---

## Auto-Start Configuration

Choose one of these methods to make the application start automatically when the computer boots.

### Method 1: Startup Folder (Easiest)

#### Step 1: Verify Batch File Path

1. Open `start_attendance.bat` with Notepad
2. Make sure the path is correct:
   ```batch
   cd /d "C:\your\actual\path\to\dlsud-cso-attendance"
   ```
3. Save if you made changes

#### Step 2: Create Shortcut

1. Right-click `start_attendance.bat`
2. Select **"Create shortcut"**

#### Step 3: Move to Startup Folder

1. Press `Win + R`
2. Type `shell:startup`
3. Press Enter (Startup folder opens)
4. **Drag the shortcut** to this folder

#### Step 4: Configure Shortcut (Optional)

1. Right-click the shortcut in Startup folder
2. Select **"Properties"**
3. In **"Run:"** dropdown, select **"Minimized"**
4. Click **"OK"**

#### Step 5: Test

1. Restart your computer
2. After login, the application should start automatically
3. Open browser to `http://127.0.0.1:5000` to verify

---

### Method 2: Task Scheduler (Most Reliable)

#### Step 1: Find Python Path

1. Open Command Prompt
2. Type: `where python`
3. Copy the path shown (e.g., `C:\Python311\python.exe`)

#### Step 2: Open Task Scheduler

1. Press `Win + R`
2. Type `taskschd.msc`
3. Press Enter

#### Step 3: Create Task

1. In right panel, click **"Create Basic Task..."**
2. **Name:** `DLSU CSO Attendance System`
3. **Description:** `Auto-start attendance system on boot`
4. Click **"Next"**

#### Step 4: Set Trigger

1. Select **"When the computer starts"**
2. Click **"Next"**

#### Step 5: Set Action

1. Select **"Start a program"**
2. Click **"Next"**

#### Step 6: Configure Program

1. **Program/script:**
   - Click **"Browse"**
   - Navigate to Python executable (from Step 1)
   - Or paste path: `C:\Python311\python.exe`

2. **Add arguments:**
   - Type: `app.py`

3. **Start in:**
   - Click **"Browse"**
   - Navigate to project folder
   - Or paste path: `C:\dlsud-cso-attendance`

4. Click **"Next"**, then **"Finish"**

#### Step 7: Modify Task Properties

1. Find your task in Task Scheduler Library
2. Right-click it → **"Properties"**

3. **General Tab:**
   - ☑️ Check **"Run with highest privileges"**

4. **Conditions Tab:**
   - ☐ Uncheck **"Start the task only if the computer is on AC power"**

5. **Settings Tab:**
   - ☑️ Check **"Allow task to be run on demand"**
   - ☑️ Check **"Run task as soon as possible after a scheduled start is missed"**

6. Click **"OK"**

#### Step 8: Test

1. Right-click the task
2. Select **"Run"**
3. Check if application starts
4. Restart computer to verify auto-start

---

## User Management

### Adding Users via Script

#### Step 1: Edit add_users.py

1. Open `add_users.py` with Notepad or any text editor
2. Find the `users_to_add` list
3. Add your users:

```python
users_to_add = [
    {
        'id_number': '20213001',
        'full_name': 'John Smith',
        'birthday': '05-20'  # May 20
    },
    {
        'id_number': '20213002',
        'full_name': 'Jane Doe',
        'birthday': '11-15'  # November 15
    },
    # Add more users here
]
```

#### Step 2: Run the Script

1. Open Command Prompt in project folder
2. Type: `python add_users.py`
3. Select option **1** (Add new users)
4. Press Enter

You should see:
```
✓ Added: 20213001 - John Smith
✓ Added: 20213002 - Jane Doe

==================================================
Successfully added: 2 user(s)
==================================================
```

### Viewing All Users

1. Open Command Prompt in project folder
2. Type: `python add_users.py`
3. Select option **2** (List all users)

### Checking Attendance Records

1. Open Command Prompt in project folder
2. Type: `python view_attendance.py`
3. Choose an option:
   - **1** - View all records
   - **2** - View today's records
   - **3** - View specific user's records

---

## Maintenance & Backup

### Regular Backups

#### Manual Backup

1. Locate `attendance.db` in project folder
2. Copy the file
3. Paste to backup location (e.g., USB drive, cloud storage)
4. Rename with date: `attendance_2025-11-11.db`

#### Automated Backup Script

The project includes `backup_database.bat` for automated backups:

1. Double-click `backup_database.bat` to create a backup
2. Backups are saved in `backups/` folder with timestamp
3. Set up in Task Scheduler to run daily (optional)

### Cleaning Old Exports

The `exports/` folder stores all generated Excel files. Periodically delete old files to save space:

1. Navigate to `exports/` folder
2. Sort by date
3. Delete files older than desired retention period

---

## Troubleshooting

### Problem: "python is not recognized as an internal or external command"

**Solution:**
1. Python not added to PATH during installation
2. Reinstall Python and check ☑️ "Add python.exe to PATH"
3. Or manually add Python to PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" in System Variables
   - Add Python installation folder

### Problem: "No module named 'flask'" or similar

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Application won't start - "Address already in use"

**Solution:**
Port 5000 is being used by another application.

**Option 1:** Close the other application

**Option 2:** Change port in `app.py`:
```python
app.run(debug=False, host='127.0.0.1', port=5001)
```

### Problem: Can't access http://127.0.0.1:5000

**Solutions:**
1. Check if Flask is running in Command Prompt
2. Try `http://localhost:5000` instead
3. Check Windows Firewall settings
4. Disable VPN if active

### Problem: Birthday greeting not working

**Verify:**
1. Birthday format is correct: `MM-DD` (e.g., `01-15` for January 15)
2. System date is correct
3. User is timing in (not timing out)

### Problem: Excel export fails

**Solutions:**
1. Install openpyxl: `pip install openpyxl`
2. Check if `exports/` folder exists (created automatically)
3. Ensure disk space is available
4. Check file permissions

### Problem: Database errors after update

**Solution (⚠️ Will delete all data):**
1. Close the application
2. Delete `attendance.db`
3. Restart application (new database created)
4. Re-add users

**Better Solution (Keeps data):**
1. Backup `attendance.db` first
2. Report issue on GitHub with error message

---

## Getting Help

### Check Logs

When troubleshooting, share the error messages from Command Prompt.

### Contact Support

- **GitHub Issues:** https://github.com/mightbeian/dlsud-cso-attendance/issues
- **Email:** cabrera.cpaul@gmail.com

When reporting issues, include:
1. Windows version
2. Python version
3. Error messages (copy from Command Prompt)
4. Steps to reproduce the problem

---

## Next Steps

After setup:

1. ✅ Add all CSO members to database
2. ✅ Test the system with a few users
3. ✅ Configure auto-start
4. ✅ Set up automated backups
5. ✅ Train staff on using the system
6. ✅ Place computer where users can easily access it

---

**Need more help? Visit: https://github.com/mightbeian/dlsud-cso-attendance**
