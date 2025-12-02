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
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance_tracker.db'
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
    """ChengeAI chat endpoint - provides financial advice."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        # Get user's financial context
        tracker = get_user_tracker()
        summary = tracker.get_summary()
        
        # Generate contextual response
        response = generate_financial_advice(user_message, summary, current_user)
        
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


def generate_financial_advice(message, summary, user):
    """Generate financial advice based on user question and their data."""
    
    # Financial advice database
    advice_responses = {
        'save': f"""Great question about saving! Based on your data:

💰 **Your Current Balance:** ${summary['balance']:,.2f}

Here are my top saving tips:

1. **Automate Your Savings**: Set up automatic transfers to savings account
2. **Track Every Expense**: Use Chengeta to monitor where your money goes
3. **Cut Unnecessary Subscriptions**: Review and cancel unused services
4. **50/30/20 Rule**: 50% needs, 30% wants, 20% savings
5. **Emergency Fund First**: Build 3-6 months of expenses

Would you like specific tips based on your spending patterns?""",

        'budget': f"""Excellent! Let's talk budgeting.

📊 **Your Stats:**
- Total Income: ${summary['total_income']:,.2f}
- Total Expenses: ${summary['total_expenses']:,.2f}

**Budgeting Strategy:**

1. **Zero-Based Budget**: Assign every dollar a job
2. **Use Chengeta Budgets**: Set limits for each category
3. **Review Weekly**: Check your budget status regularly
4. **Adjust Monthly**: Refine based on actual spending
5. **Include Fun Money**: Budget for entertainment to stay motivated

Try setting budgets in the Budgets page!""",

        'debt': """Let's tackle debt together! 💪

**Debt Reduction Strategies:**

1. **Debt Avalanche**: Pay highest interest rate first (saves most money)
2. **Debt Snowball**: Pay smallest balance first (quick wins, motivation)
3. **Balance Transfers**: Move high-interest debt to 0% cards
4. **Increase Income**: Side hustles to accelerate payoff
5. **Track Progress**: Use Chengeta to monitor debt reduction

**Quick Tips:**
- Stop adding new debt
- Pay more than minimum
- Negotiate lower rates
- Consider debt consolidation

You've got this!""",

        'invest': """Smart thinking about investing! 📈

**Investment Basics:**

1. **Start Small**: Begin with as little as $50/month
2. **Index Funds**: Low-cost, diversified option
3. **401(k) Match**: Free money from employer
4. **IRA/Roth IRA**: Tax-advantaged retirement accounts
5. **Emergency Fund First**: Save 3-6 months expenses before investing

**Golden Rules:**
- Invest consistently (dollar-cost averaging)
- Diversify (don't put all eggs in one basket)
- Think long-term (time in market beats timing)
- Keep fees low

**Resources:** Check our Videos section for beginner investment courses!""",

        'emergency': """Building an emergency fund is crucial! 🛡️

**Emergency Fund Basics:**

**How Much?**
- Minimum: $1,000 (starter fund)
- Goal: 3-6 months of expenses
- High-earning: 6-12 months

**Where to Keep It?**
- High-yield savings account
- Money market account
- Easy access, but separate from spending

**How to Build:**
1. Start with $500-1,000
2. Save $50-100 per paycheck
3. Use windfalls (tax refunds, bonuses)
4. Track progress in Chengeta
5. Don't touch it unless emergency!

**Pro Tip:** Set up automatic transfers on payday!""",

        'retirement': """Planning for retirement? Great! 🏖️

**Retirement Planning Essentials:**

**Start Now:**
- Age 20s: Save 10-15% of income
- Age 30s: Save 15-20% of income
- Age 40s: Save 20-25% of income

**Accounts to Use:**
1. **401(k)**: Employer match = free money!
2. **IRA**: Traditional or Roth
3. **Roth IRA**: Tax-free growth
4. **HSA**: Triple tax advantage

**Retirement Math:**
- Rule of 25: Need 25x annual expenses
- 4% Rule: Withdraw 4% annually
- Social Security: Extra cushion

**Action Steps:**
1. Calculate retirement needs
2. Maximize employer match
3. Open IRA account
4. Increase contributions annually
5. Track progress quarterly

Start today - compound interest is powerful!""",

        'income': """Want to increase your income? Let's explore! 💼

**Income Boosting Strategies:**

**Side Hustles:**
- Freelancing (Upwork, Fiverr)
- Online tutoring
- Selling digital products
- Consulting in your expertise

**Career Growth:**
- Ask for raise (prepare case)
- Develop new skills
- Get certifications
- Network actively
- Consider job change

**Passive Income:**
- Rental properties
- Dividend stocks
- Online courses
- Affiliate marketing

**Quick Wins:**
- Negotiate salary at job offers
- Take on overtime
- Monetize hobbies
- Sell unused items

Track all income sources in Chengeta!""",

        'default': f"""Hello! I'm ChengeAI, your personal financial advisor! 🤖

I can help you with:

💰 **Saving Money** - Tips and strategies
📊 **Budgeting** - Create and stick to budgets
💳 **Debt Management** - Get debt-free
📈 **Investing** - Grow your wealth
🛡️ **Emergency Funds** - Build financial security
🏖️ **Retirement Planning** - Secure your future
💼 **Income Growth** - Earn more money

**Your Financial Overview:**
- Total Income: ${summary['total_income']:,.2f}
- Total Expenses: ${summary['total_expenses']:,.2f}
- Current Balance: ${summary['balance']:,.2f}

What would you like to know about? Just ask me anything!"""
    }
    
    # Determine which response to give
    if any(word in message for word in ['save', 'saving', 'savings']):
        return advice_responses['save']
    elif any(word in message for word in ['budget', 'budgeting', 'spending plan']):
        return advice_responses['budget']
    elif any(word in message for word in ['debt', 'loan', 'credit card', 'owe']):
        return advice_responses['debt']
    elif any(word in message for word in ['invest', 'investment', 'stock', 'portfolio']):
        return advice_responses['invest']
    elif any(word in message for word in ['emergency', 'fund', 'rainy day']):
        return advice_responses['emergency']
    elif any(word in message for word in ['retirement', 'retire', '401k', 'ira', 'pension']):
        return advice_responses['retirement']
    elif any(word in message for word in ['income', 'earn', 'money', 'salary', 'side hustle']):
        return advice_responses['income']
    else:
        return advice_responses['default']


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
