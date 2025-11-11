# DLSU-D CSO Attendance System

A lightweight, standalone web-based attendance system for the DLSU-D Council of Student Organizations (CSO). This system runs locally on a single office computer and provides reliable time tracking with birthday greetings and Excel DTR export functionality.

![DLSU Green](https://img.shields.io/badge/DLSU-Green-00693C?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Local-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

## Features

✅ **Simple Time In/Time Out Interface** - Clean, user-friendly single-page application  
✅ **Automatic Birthday Greetings** - Special messages for users on their birthday  
✅ **Excel DTR Export** - Generate formatted Daily Time Records with total hours  
✅ **State-Aware Tracking** - Prevents duplicate time-ins and tracks user status  
✅ **Local SQLite Database** - Reliable, file-based database with no external dependencies  
✅ **Professional DLSU Theme** - Minimalist design in official DLSU Green (#00693C)  
✅ **Auto-Start on Boot** - Configure to launch automatically when computer starts  
✅ **Utility Scripts** - Helper scripts for managing users and viewing records

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python Flask 3.0.0 |
| **Database** | SQLite (serverless) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Excel Export** | openpyxl 3.1.2 |
| **ORM** | Flask-SQLAlchemy 3.1.1 |

## Installation

### Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (included with Python)

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/mightbeian/dlsud-cso-attendance.git
cd dlsud-cso-attendance
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## Usage

### Time In
1. Enter your ID Number
2. Click **"TIME IN"**
3. See welcome message (or birthday greeting!)

### Time Out
1. Enter your ID Number
2. Click **"TIME OUT"**
3. See goodbye message

### Export DTR
- Click **"Export DTR"** at the bottom
- Download Excel file with attendance records

## Managing Users

### Using the Helper Script

```bash
python add_users.py
```

### Adding Users Manually

Edit `add_users.py` and modify the `users_to_add` list:

```python
users_to_add = [
    {
        'id_number': '20212348',
        'full_name': 'Anna Reyes',
        'birthday': '12-25'  # Format: MM-DD
    },
]
```

## Auto-Start on Windows

### Method 1: Startup Folder (Easiest)

1. Right-click `start_attendance.bat` → Create shortcut
2. Press `Win + R`, type `shell:startup`
3. Move shortcut to Startup folder
4. Right-click shortcut → Properties → Run: Minimized

### Method 2: Task Scheduler (Most Reliable)

1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create Basic Task
3. Trigger: "When the computer starts"
4. Action: Start program → Python executable
5. Arguments: `app.py`
6. Start in: Project directory

### Method 3: Silent Launcher

1. Create shortcut of `launcher.pyw`
2. Press `Win + R`, type `shell:startup`
3. Move shortcut to Startup folder

## Project Structure

```
dlsu-cso-attendance/
├── app.py                  # Main Flask application
├── database.py             # Database models
├── requirements.txt        # Dependencies
├── add_users.py           # User management
├── view_attendance.py     # View records
├── start_attendance.bat   # Batch launcher
├── launcher.pyw           # Silent launcher
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── exports/               # Excel files (auto-created)
```

## Database Schema

### Users Table
- `id` - Primary key
- `id_number` - Student/Employee ID (unique)
- `full_name` - Full name
- `birthday` - Format: MM-DD

### Attendance Table
- `id` - Primary key
- `user_id` - Foreign key to Users
- `timestamp` - Event date/time
- `event_type` - "In" or "Out"

## Troubleshooting

**Application won't start**
- Check Python version: `python --version`
- Install dependencies: `pip install -r requirements.txt`

**Can't access interface**
- Ensure Flask is running
- Open: `http://127.0.0.1:5000`

**Auto-start issues**
- Verify batch file path
- Check Task Scheduler logs

## Security Notes

⚠️ **This is a local-only application** for internal office use.  
- No authentication (designed for trusted environment)
- Runs on localhost only (127.0.0.1)
- Not intended for public deployment

## License

MIT License - see [LICENSE](LICENSE) file

## Author

**Christian Paul Cabrera**
- GitHub: [@mightbeian](https://github.com/mightbeian)
- LinkedIn: [mightbeian](https://www.linkedin.com/in/mightbeian/)

---

**Made with ❤️ for DLSU-D CSO**
