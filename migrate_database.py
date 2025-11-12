"""
Database Migration Script
Upgrades the old database schema to include committee and photo_filename fields
"""

import sqlite3
import os

def migrate_database():
    db_path = 'attendance.db'
    
    if not os.path.exists(db_path):
        print("No database found. A new database will be created when you run the app.")
        return
    
    print("="*60)
    print("  Database Migration Script")
    print("="*60)
    print("\nThis will upgrade your database to include:")
    print("  - Committee field for each user")
    print("  - Photo filename field for profile pictures")
    print("\nYour attendance data will be preserved.")
    
    response = input("\nDo you want to continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Migration cancelled.")
        return
    
    # Backup the database
    backup_path = f'attendance_backup_{int(os.path.getmtime(db_path))}.db'
    print(f"\n Creating backup: {backup_path}")
    
    import shutil
    shutil.copy2(db_path, backup_path)
    print("✓ Backup created successfully")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if committee column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'committee' not in columns:
            print("\n✓ Adding 'committee' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN committee VARCHAR(50) DEFAULT 'Executive Board'")
            print("  Committee column added")
        else:
            print("\n  'committee' column already exists")
        
        if 'photo_filename' not in columns:
            print("\n✓ Adding 'photo_filename' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN photo_filename VARCHAR(200)")
            print("  Photo filename column added")
        else:
            print("\n  'photo_filename' column already exists")
        
        conn.commit()
        conn.close()
        
        print("\n" + "="*60)
        print("✓ Migration completed successfully!")
        print("="*60)
        print(f"\nBackup saved as: {backup_path}")
        print("\nYou can now run the application with:")
        print("  python app.py")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n✗ Migration failed: {str(e)}")
        print(f"\nYour original database is backed up at: {backup_path}")
        print("You can restore it by:")
        print(f"  1. Delete attendance.db")
        print(f"  2. Rename {backup_path} to attendance.db")

if __name__ == '__main__':
    migrate_database()
