"""
Chengeta - Personal Finance Management Application
Flask backend with user authentication and multi-user support
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from models import db, User
from auth import auth_bp
from finance_tracker import FinanceTracker
from visualizer import FinanceVisualizer
from ai_service import get_ai_response
from youtube_service import fetch_finance_videos
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///finance_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

# Register blueprints
app.register_blueprint(auth_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_user_tracker():
    """Get tracker instance for current user."""
    return FinanceTracker(
        data_file=current_user.get_data_file(),
        budget_file=current_user.get_budget_file()
    )


def get_user_visualizer():
    """Get visualizer instance for current user."""
    tracker = get_user_tracker()
    return FinanceVisualizer(tracker)


# Public Routes

@app.route('/')
def home():
    """Home route - redirect to dashboard or landing."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return redirect(url_for('auth.landing'))


# Protected Routes (Require Login)

@app.route('/dashboard')
@login_required
def index():
    """Main dashboard page."""
    return render_template('index.html', user=current_user)


@app.route('/transactions')
@login_required
def transactions_page():
    """Transactions page."""
    return render_template('transactions.html', user=current_user)


@app.route('/budgets')
@login_required
def budgets_page():
    """Budgets page."""
    return render_template('budgets.html', user=current_user)


@app.route('/reports')
@login_required
def reports_page():
    """Reports and visualizations page."""
    return render_template('reports.html', user=current_user)


@app.route('/ai-advisor')
@login_required
def ai_advisor_page():
    """ChengeAI financial advisor page."""
    return render_template('ai_advisor.html', user=current_user)


@app.route('/resources')
@login_required
def resources_page():
    """Financial resources library page."""
    return render_template('resources.html', user=current_user)


# API Endpoints

@app.route('/api/summary', methods=['GET'])
@login_required
def get_summary():
    """Get financial summary for current user."""
    tracker = get_user_tracker()
    summary = tracker.get_summary()
    balance = tracker.get_balance()
    return jsonify({
        'success': True,
        'data': {
            'total_income': summary['total_income'],
            'total_expenses': summary['total_expenses'],
            'balance': balance,
            'transaction_count': summary['transaction_count']
        }
    })


@app.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    """Get all transactions or filtered by date range."""
    tracker = get_user_tracker()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date or end_date:
        transactions = tracker.get_transactions_by_date_range(start_date, end_date)
    else:
        transactions = tracker.get_all_transactions()
    
    return jsonify({
        'success': True,
        'data': transactions
    })


@app.route('/api/transactions', methods=['POST'])
@login_required
def add_transaction():
    """Add a new transaction."""
    try:
        tracker = get_user_tracker()
        data = request.get_json()
        
        amount = float(data.get('amount'))
        category = data.get('category')
        description = data.get('description')
        transaction_type = data.get('type')
        
        transaction = tracker.add_transaction(amount, category, description, transaction_type)
        
        return jsonify({
            'success': True,
            'message': 'Transaction added successfully',
            'data': transaction
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
@login_required
def delete_transaction(transaction_id):
    """Delete a transaction."""
    tracker = get_user_tracker()
    success = tracker.delete_transaction(transaction_id)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Transaction deleted successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Transaction not found'
        }), 404


@app.route('/api/transactions/<int:transaction_id>', methods=['PUT'])
@login_required
def update_transaction(transaction_id):
    """Update a transaction."""
    try:
        tracker = get_user_tracker()
        data = request.get_json()
        success = tracker.update_transaction(transaction_id, **data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Transaction updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Transaction not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@app.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    """Get category summary."""
    tracker = get_user_tracker()
    categories = tracker.get_category_summary()
    
    category_list = []
    for category, amounts in categories.items():
        category_list.append({
            'name': category,
            'income': amounts['income'],
            'expense': amounts['expense'],
            'net': amounts['income'] - amounts['expense']
        })
    
    return jsonify({
        'success': True,
        'data': category_list
    })


@app.route('/api/budgets', methods=['GET'])
@login_required
def get_budgets():
    """Get all budgets with status."""
    tracker = get_user_tracker()
    statuses = tracker.get_all_budget_statuses()
    
    return jsonify({
        'success': True,
        'data': statuses
    })


@app.route('/api/budgets', methods=['POST'])
@login_required
def set_budget():
    """Set a budget for a category."""
    try:
        tracker = get_user_tracker()
        data = request.get_json()
        
        category = data.get('category')
        amount = float(data.get('amount'))
        period = data.get('period', 'monthly')
        
        tracker.set_budget(category, amount, period)
        
        return jsonify({
            'success': True,
            'message': 'Budget set successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@app.route('/api/budgets/<category>', methods=['DELETE'])
@login_required
def delete_budget(category):
    """Delete a budget."""
    tracker = get_user_tracker()
    success = tracker.delete_budget(category)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Budget deleted successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Budget not found'
        }), 404


@app.route('/api/charts/generate', methods=['POST'])
@login_required
def generate_charts():
    """Generate all visualization charts."""
    try:
        visualizer = get_user_visualizer()
        charts = visualizer.generate_all_charts()
        
        return jsonify({
            'success': True,
            'message': f'Generated {len(charts)} charts',
            'data': charts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/charts/<chart_name>')
@login_required
def get_chart(chart_name):
    """Serve a chart image."""
    chart_path = os.path.join('data', 'charts', f'{chart_name}.png')
    
    if os.path.exists(chart_path):
        return send_file(chart_path, mimetype='image/png')
    else:
        return jsonify({
            'success': False,
            'message': 'Chart not found'
        }), 404


@app.route('/api/export', methods=['GET'])
@login_required
def export_csv():
    """Export transactions to CSV."""
    try:
        tracker = get_user_tracker()
        filename = f'data/users/{current_user.id}/export.csv'
        tracker.export_to_csv(filename)
        
        return send_file(filename, 
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name=f'transactions_{current_user.username}.csv')
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/stats/recent', methods=['GET'])
@login_required
def get_recent_stats():
    """Get recent transactions and quick stats."""
    tracker = get_user_tracker()
    transactions = tracker.get_all_transactions()
    recent = transactions[-10:] if len(transactions) > 10 else transactions
    recent.reverse()  # Most recent first
    
    # Get category breakdown for pie chart
    categories = tracker.get_category_summary()
    expense_categories = {k: v['expense'] for k, v in categories.items() if v['expense'] > 0}
    
    return jsonify({
        'success': True,
        'data': {
            'recent_transactions': recent,
            'expense_by_category': expense_categories
        }
    })


@app.route('/api/ai/chat', methods=['POST'])
@login_required
def ai_chat():
    """ChengeAI chat endpoint - provides AI-powered financial advice."""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        # Get user's financial context
        tracker = get_user_tracker()
        summary = tracker.get_summary()
        
        # Get expense breakdown by category
        category_summary = tracker.get_category_summary()
        
        # Extract expense amounts from category summary
        expense_categories = {
            cat: data['expense'] 
            for cat, data in category_summary.items() 
            if data['expense'] > 0
        }
        
        # Prepare user data for AI
        user_data = {
            'total_income': summary['total_income'],
            'total_expenses': summary['total_expenses'],
            'balance': summary['balance'],
            'transaction_count': summary['transaction_count'],
            'top_categories': [
                {'category': cat, 'amount': amount}
                for cat, amount in sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
        }
        
        # Get AI response
        result = get_ai_response(user_message, user_data, conversation_history)
        
        return jsonify({
            'success': result['success'],
            'response': result['response'],
            'source': result.get('source', 'unknown')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/resources/videos', methods=['GET'])
@login_required
def get_resource_videos():
    """Fetch finance education videos from YouTube."""
    try:
        # Check if refresh is requested
        force_refresh = request.args.get('refresh', 'false').lower() == 'true'
        
        # Fetch videos (from cache or YouTube API)
        videos = fetch_finance_videos(force_refresh=force_refresh)
        
        return jsonify({
            'success': True,
            'videos': videos,
            'count': len(videos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'videos': []
        }), 500


# Database initialization
def init_database():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")


if __name__ == '__main__':
    # Create database tables
    init_database()
    
    # Ensure data directories exist
    os.makedirs('data/users', exist_ok=True)
    os.makedirs('data/charts', exist_ok=True)
    
    print("\n" + "="*60)
    print("Chengeta - Personal Finance Management App is starting...")
    print("="*60)
    print("\nAccess the application at: http://localhost:5000")
    print("Landing page: http://localhost:5000/landing")
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
