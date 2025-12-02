"""
Database Models for Finance Tracker
User authentication and profile management
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and profile."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile information
    full_name = db.Column(db.String(120))
    profile_picture = db.Column(db.String(255))  # Store file path
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Customization settings
    theme = db.Column(db.String(20), default='light')
    currency = db.Column(db.String(10), default='USD')
    timezone = db.Column(db.String(50), default='UTC')
    
    # Preferences
    default_income_category = db.Column(db.String(50), default='Salary')
    default_expense_category = db.Column(db.String(50), default='Other')
    budget_alert_threshold = db.Column(db.Integer, default=80)  # Percentage
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update the last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def get_data_file(self):
        """Get user-specific transactions file path."""
        return f'data/users/{self.id}/transactions.json'
    
    def get_budget_file(self):
        """Get user-specific budgets file path."""
        return f'data/users/{self.id}/budgets.json'
    
    def __repr__(self):
        return f'<User {self.username}>'

