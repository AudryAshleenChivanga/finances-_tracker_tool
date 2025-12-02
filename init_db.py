"""
Database Initialization Script
Creates tables and adds profile_picture column if needed
"""

from app import app, db
from models import User
import os

def init_database():
    """Initialize database with all tables and migrations."""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if profile_picture column exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        if 'profile_picture' not in columns:
            print("Adding profile_picture column to users table...")
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE users ADD COLUMN profile_picture VARCHAR(255)'))
                conn.commit()
            print("[+] Profile picture column added")
        
        print("[+] Database initialized successfully!")
        
        # Create necessary directories
        directories = [
            'data/users',
            'data/charts',
            'static/uploads/profiles'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"[+] Created directory: {directory}")
        
        print("\n" + "="*60)
        print("Database and directories ready!")
        print("="*60)

if __name__ == '__main__':
    init_database()

