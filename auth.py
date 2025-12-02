"""
Authentication Routes
Handle user registration, login, logout
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User
import os
import uuid

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/landing')
def landing():
    """Landing page for visitors."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('landing.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember', False)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.update_last_login()
            
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'redirect': url_for('index')
                })
            return redirect(url_for('index'))
        
        error = 'Invalid username or password'
        if request.is_json:
            return jsonify({'success': False, 'message': error}), 401
        flash(error, 'error')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')
        
        # Validation
        if not username or not email or not password:
            error = 'All fields are required'
            if request.is_json:
                return jsonify({'success': False, 'message': error}), 400
            flash(error, 'error')
            return render_template('register.html')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            error = 'Username already exists'
            if request.is_json:
                return jsonify({'success': False, 'message': error}), 400
            flash(error, 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            error = 'Email already registered'
            if request.is_json:
                return jsonify({'success': False, 'message': error}), 400
            flash(error, 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email, full_name=full_name)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create user data directories
        user_data_dir = f'data/users/{user.id}'
        os.makedirs(user_data_dir, exist_ok=True)
        
        # Auto login after registration
        login_user(user)
        user.update_last_login()
        
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Registration successful',
                'redirect': url_for('index')
            })
        
        flash('Registration successful! Welcome to Chengeta.', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.landing'))


@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('profile.html')


@auth_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """User settings page."""
    if request.method == 'POST':
        data = request.get_json()
        
        # Update user settings
        if 'full_name' in data:
            current_user.full_name = data['full_name']
        if 'email' in data:
            # Check if email is already taken
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != current_user.id:
                return jsonify({'success': False, 'message': 'Email already in use'}), 400
            current_user.email = data['email']
        if 'theme' in data:
            current_user.theme = data['theme']
        if 'currency' in data:
            current_user.currency = data['currency']
        if 'budget_alert_threshold' in data:
            current_user.budget_alert_threshold = int(data['budget_alert_threshold'])
        if 'default_income_category' in data:
            current_user.default_income_category = data['default_income_category']
        if 'default_expense_category' in data:
            current_user.default_expense_category = data['default_expense_category']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Settings updated successfully'
        })
    
    return render_template('settings.html')


@auth_bp.route('/api/user/info')
@login_required
def user_info():
    """Get current user information."""
    return jsonify({
        'success': True,
        'data': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'full_name': current_user.full_name,
            'profile_picture': current_user.profile_picture,
            'theme': current_user.theme,
            'currency': current_user.currency,
            'budget_alert_threshold': current_user.budget_alert_threshold,
            'default_income_category': current_user.default_income_category,
            'default_expense_category': current_user.default_expense_category,
            'created_at': current_user.created_at.isoformat() if current_user.created_at else None,
            'last_login': current_user.last_login.isoformat() if current_user.last_login else None
        }
    })


@auth_bp.route('/api/user/upload-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    """Upload user profile picture."""
    try:
        if 'profile_picture' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['profile_picture']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify({'success': False, 'message': 'Invalid file type. Use PNG, JPG, GIF, or WEBP'}), 400
        
        # Generate unique filename
        filename = f"{current_user.id}_{uuid.uuid4().hex[:8]}.{file_ext}"
        
        # Create uploads directory
        upload_dir = os.path.join('static', 'uploads', 'profiles')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        
        # Delete old profile picture if exists
        if current_user.profile_picture:
            old_path = os.path.join('static', 'uploads', 'profiles', current_user.profile_picture)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        # Update user profile
        current_user.profile_picture = filename
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile picture uploaded successfully',
            'data': {
                'profile_picture': filename,
                'url': f'/uploads/profiles/{filename}'
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@auth_bp.route('/api/user/remove-picture', methods=['DELETE'])
@login_required
def remove_profile_picture():
    """Remove user profile picture."""
    try:
        if current_user.profile_picture:
            # Delete file
            filepath = os.path.join('static', 'uploads', 'profiles', current_user.profile_picture)
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Update database
            current_user.profile_picture = None
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile picture removed successfully'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@auth_bp.route('/uploads/profiles/<filename>')
def serve_profile_picture(filename):
    """Serve profile picture."""
    return send_from_directory(os.path.join('static', 'uploads', 'profiles'), filename)

