"""
DLSU-D CSO Attendance System - Main Application
Flask application with routes for attendance tracking, user management, and Excel export
"""

import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from models import db, User, Attendance
import pandas as pd
from io import BytesIO

# Initialize Flask app
app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'dlsud-cso-attendance-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "attendance.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'photos')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Initialize database
db.init_app(app)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================
# PAGE ROUTES
# ============================================

@app.route('/')
def dashboard():
    """Render main dashboard page"""
    return render_template('dashboard.html', committees=User.COMMITTEES)


# ============================================
# ATTENDANCE API ROUTES
# ============================================

@app.route('/api/scan', methods=['POST'])
def scan_id():
    """
    Process ID scan - implements no-touch logic
    Automatically determines Time In or Time Out based on current status
    """
    data = request.get_json()
    student_id = data.get('student_id', '').strip()
    
    if not student_id:
        return jsonify({'success': False, 'message': 'Please enter an ID number.'}), 400
    
    # Find user by student ID
    user = User.query.filter_by(student_id=student_id).first()
    
    if not user:
        return jsonify({
            'success': False, 
            'message': 'User not found. Please check the ID number.',
            'user': None
        }), 404
    
    # Determine action based on current status
    current_time = datetime.now()
    is_birthday = False
    
    if user.status == 'Offline':
        # Time In
        user.status = 'Online'
        event_type = 'Time In'
        
        # Check for birthday
        if user.birthday:
            today = current_time.strftime('%m-%d')
            if user.birthday == today:
                is_birthday = True
                message = f"🎂 Happy Birthday, {user.full_name}! You are timed in."
            else:
                message = f"Welcome, {user.full_name}!"
        else:
            message = f"Welcome, {user.full_name}!"
    else:
        # Time Out
        user.status = 'Offline'
        event_type = 'Time Out'
        message = f"Goodbye, {user.full_name}!"
    
    # Create attendance record
    attendance = Attendance(
        user_id=user.id,
        timestamp=current_time,
        event_type=event_type
    )
    
    db.session.add(attendance)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': message,
        'event_type': event_type,
        'is_birthday': is_birthday,
        'user': user.to_dict(),
        'timestamp': current_time.strftime('%I:%M %p')
    })


@app.route('/api/active-users')
def get_active_users():
    """Get all currently active (online) users grouped by committee"""
    active_users = User.query.filter_by(status='Online').all()
    
    # Group by committee
    grouped = {}
    for committee in User.COMMITTEES:
        grouped[committee] = []
    
    for user in active_users:
        if user.committee in grouped:
            grouped[user.committee].append(user.to_dict())
    
    return jsonify({
        'success': True,
        'active_users': grouped,
        'total_count': len(active_users)
    })


# ============================================
# USER MANAGEMENT API ROUTES
# ============================================

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users with optional search"""
    search = request.args.get('search', '').strip()
    
    if search:
        users = User.query.filter(
            (User.student_id.contains(search)) | 
            (User.full_name.ilike(f'%{search}%'))
        ).all()
    else:
        users = User.query.order_by(User.full_name).all()
    
    return jsonify({
        'success': True,
        'users': [user.to_dict() for user in users]
    })


@app.route('/api/users', methods=['POST'])
def add_user():
    """Add a new user"""
    # Handle form data (for file upload)
    student_id = request.form.get('student_id', '').strip()
    full_name = request.form.get('full_name', '').strip()
    birthday = request.form.get('birthday', '').strip()
    committee = request.form.get('committee', '').strip()
    
    # Validation
    if not student_id or not full_name or not committee:
        return jsonify({
            'success': False, 
            'message': 'Student ID, Name, and Committee are required.'
        }), 400
    
    if committee not in User.COMMITTEES:
        return jsonify({
            'success': False, 
            'message': 'Invalid committee selected.'
        }), 400
    
    # Check for duplicate student ID
    existing = User.query.filter_by(student_id=student_id).first()
    if existing:
        return jsonify({
            'success': False, 
            'message': 'A user with this Student ID already exists.'
        }), 400
    
    # Handle photo upload
    photo_filename = None
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename and allowed_file(file.filename):
            # Create unique filename
            ext = file.filename.rsplit('.', 1)[1].lower()
            photo_filename = f"{student_id}.{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
    
    # Create new user
    user = User(
        student_id=student_id,
        full_name=full_name,
        birthday=birthday if birthday else None,
        committee=committee,
        photo_filename=photo_filename,
        status='Offline'
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'User {full_name} added successfully!',
        'user': user.to_dict()
    })


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': 'User not found.'}), 404
    
    # Update fields
    if 'full_name' in request.form:
        user.full_name = request.form.get('full_name', '').strip()
    if 'birthday' in request.form:
        user.birthday = request.form.get('birthday', '').strip() or None
    if 'committee' in request.form:
        committee = request.form.get('committee', '').strip()
        if committee in User.COMMITTEES:
            user.committee = committee
    
    # Handle new photo upload
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename and allowed_file(file.filename):
            # Delete old photo if exists
            if user.photo_filename:
                old_path = os.path.join(app.config['UPLOAD_FOLDER'], user.photo_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            ext = file.filename.rsplit('.', 1)[1].lower()
            photo_filename = f"{user.student_id}.{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            user.photo_filename = photo_filename
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'User {user.full_name} updated successfully!',
        'user': user.to_dict()
    })


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user and their attendance records"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': 'User not found.'}), 404
    
    # Delete photo if exists
    if user.photo_filename:
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], user.photo_filename)
        if os.path.exists(photo_path):
            os.remove(photo_path)
    
    name = user.full_name
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'User {name} deleted successfully!'
    })


# ============================================
# EXCEL EXPORT ROUTES
# ============================================

@app.route('/api/export/dtr')
def export_dtr():
    """Export Daily Time Record as Excel file"""
    # Get date range parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default to current month if not specified
    if not start_date:
        today = datetime.now()
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    
    # Get all attendance records in date range
    records = Attendance.query.filter(
        Attendance.timestamp >= start_dt,
        Attendance.timestamp < end_dt
    ).order_by(Attendance.timestamp).all()
    
    # Process records into DTR format
    dtr_data = []
    user_daily_records = {}  # {(user_id, date): {'time_in': ..., 'time_out': ...}}
    
    for record in records:
        date_key = record.timestamp.strftime('%Y-%m-%d')
        user_key = (record.user_id, date_key)
        
        if user_key not in user_daily_records:
            user_daily_records[user_key] = {
                'user_name': record.user.full_name,
                'student_id': record.user.student_id,
                'committee': record.user.committee,
                'date': date_key,
                'time_in': None,
                'time_out': None
            }
        
        if record.event_type == 'Time In' and not user_daily_records[user_key]['time_in']:
            user_daily_records[user_key]['time_in'] = record.timestamp
        elif record.event_type == 'Time Out':
            user_daily_records[user_key]['time_out'] = record.timestamp
    
    # Convert to list and calculate hours
    for key, data in user_daily_records.items():
        time_in = data['time_in']
        time_out = data['time_out']
        
        # Calculate hours rendered
        hours_rendered = ''
        if time_in and time_out:
            delta = time_out - time_in
            hours = delta.total_seconds() / 3600
            hours_rendered = f'{hours:.2f}'
        
        dtr_data.append({
            'Date': data['date'],
            'Student ID': data['student_id'],
            'Full Name': data['user_name'],
            'Committee': data['committee'],
            'Time In': time_in.strftime('%I:%M %p') if time_in else '',
            'Time Out': time_out.strftime('%I:%M %p') if time_out else '',
            'Total Hours Rendered': hours_rendered
        })
    
    # Sort by date and name
    dtr_data.sort(key=lambda x: (x['Date'], x['Full Name']))
    
    # Create DataFrame
    df = pd.DataFrame(dtr_data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Daily Time Record', index=False)
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Daily Time Record']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).map(len).max() if len(df) > 0 else 0,
                len(col)
            ) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length
    
    output.seek(0)
    
    filename = f'CSO_DTR_{start_date}_to_{end_date}.xlsx'
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )


@app.route('/api/export/roster')
def export_roster():
    """Export complete user roster as Excel file"""
    users = User.query.order_by(User.committee, User.full_name).all()
    
    roster_data = []
    for user in users:
        roster_data.append({
            'Student ID': user.student_id,
            'Full Name': user.full_name,
            'Committee': user.committee,
            'Birthday': user.birthday or '',
            'Current Status': user.status
        })
    
    df = pd.DataFrame(roster_data)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='CSO Roster', index=False)
        
        worksheet = writer.sheets['CSO Roster']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).map(len).max() if len(df) > 0 else 0,
                len(col)
            ) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = max_length
    
    output.seek(0)
    
    filename = f'CSO_Roster_{datetime.now().strftime("%Y%m%d")}.xlsx'
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )


# ============================================
# DATABASE INITIALIZATION
# ============================================

def init_db():
    """Initialize the database and create tables"""
    with app.app_context():
        db.create_all()
        
        # Create photos directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        print("Database initialized successfully!")


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the application
    print("\n" + "="*50)
    print("DLSU-D CSO Attendance System")
    print("="*50)
    print("Server running at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
