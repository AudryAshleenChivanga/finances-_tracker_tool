"""
Finance Tracker - Core Module
Handles all financial tracking operations including adding, viewing, and analyzing transactions.
"""

import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd


class FinanceTracker:
    """Main class for tracking personal finances."""
    
    def __init__(self, data_file='data/transactions.json', budget_file='data/budgets.json'):
        """Initialize the finance tracker with a data file."""
        self.data_file = data_file
        self.budget_file = budget_file
        self.transactions = []
        self.budgets = {}
        self._ensure_data_directory()
        self._load_transactions()
        self._load_budgets()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        data_dir = Path(self.data_file).parent
        data_dir.mkdir(exist_ok=True)
    
    def _load_transactions(self):
        """Load transactions from the data file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.transactions = json.load(f)
            except json.JSONDecodeError:
                self.transactions = []
        else:
            self.transactions = []
    
    def _save_transactions(self):
        """Save transactions to the data file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.transactions, f, indent=2)
    
    def _load_budgets(self):
        """Load budgets from the budget file."""
        if os.path.exists(self.budget_file):
            try:
                with open(self.budget_file, 'r') as f:
                    self.budgets = json.load(f)
            except json.JSONDecodeError:
                self.budgets = {}
        else:
            self.budgets = {}
    
    def _save_budgets(self):
        """Save budgets to the budget file."""
        with open(self.budget_file, 'w') as f:
            json.dump(self.budgets, f, indent=2)
    
    def add_transaction(self, amount, category, description, transaction_type):
        """
        Add a new transaction.
        
        Args:
            amount (float): Transaction amount
            category (str): Category of the transaction
            description (str): Description of the transaction
            transaction_type (str): 'income' or 'expense'
        """
        transaction = {
            'id': len(self.transactions) + 1,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'amount': float(amount),
            'category': category,
            'description': description,
            'type': transaction_type
        }
        self.transactions.append(transaction)
        self._save_transactions()
        return transaction
    
    def get_all_transactions(self):
        """Return all transactions."""
        return self.transactions
    
    def get_balance(self):
        """Calculate and return current balance."""
        balance = 0
        for transaction in self.transactions:
            if transaction['type'] == 'income':
                balance += transaction['amount']
            else:
                balance -= transaction['amount']
        return balance
    
    def get_summary(self):
        """Generate a summary of transactions."""
        if not self.transactions:
            return {
                'total_income': 0,
                'total_expenses': 0,
                'balance': 0,
                'transaction_count': 0
            }
        
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        total_expenses = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': total_income - total_expenses,
            'transaction_count': len(self.transactions)
        }
    
    def get_category_summary(self):
        """Get spending summary by category."""
        categories = {}
        for transaction in self.transactions:
            category = transaction['category']
            amount = transaction['amount']
            
            if category not in categories:
                categories[category] = {'income': 0, 'expense': 0}
            
            if transaction['type'] == 'income':
                categories[category]['income'] += amount
            else:
                categories[category]['expense'] += amount
        
        return categories
    
    def export_to_csv(self, filename='data/transactions.csv'):
        """Export transactions to a CSV file."""
        if not self.transactions:
            return False
        
        df = pd.DataFrame(self.transactions)
        df.to_csv(filename, index=False)
        return True
    
    def delete_transaction(self, transaction_id):
        """
        Delete a transaction by ID.
        
        Args:
            transaction_id (int): ID of the transaction to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        for i, transaction in enumerate(self.transactions):
            if transaction['id'] == transaction_id:
                self.transactions.pop(i)
                self._save_transactions()
                return True
        return False
    
    def update_transaction(self, transaction_id, **kwargs):
        """
        Update a transaction by ID.
        
        Args:
            transaction_id (int): ID of the transaction to update
            **kwargs: Fields to update (amount, category, description, type)
            
        Returns:
            bool: True if updated, False if not found
        """
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                for key, value in kwargs.items():
                    if key in transaction and key != 'id':
                        transaction[key] = value
                self._save_transactions()
                return True
        return False
    
    def get_transactions_by_date_range(self, start_date=None, end_date=None):
        """
        Get transactions within a date range.
        
        Args:
            start_date (str): Start date in format 'YYYY-MM-DD'
            end_date (str): End date in format 'YYYY-MM-DD'
            
        Returns:
            list: Filtered transactions
        """
        filtered = []
        for transaction in self.transactions:
            trans_date = transaction['date'].split()[0]  # Get date part only
            
            if start_date and trans_date < start_date:
                continue
            if end_date and trans_date > end_date:
                continue
            
            filtered.append(transaction)
        
        return filtered
    
    def get_transactions_by_category(self, category):
        """Get all transactions for a specific category."""
        return [t for t in self.transactions if t['category'].lower() == category.lower()]
    
    # Budget Management Methods
    
    def set_budget(self, category, amount, period='monthly'):
        """
        Set a budget for a category.
        
        Args:
            category (str): Category name
            amount (float): Budget amount
            period (str): Budget period ('monthly', 'weekly', 'yearly')
        """
        self.budgets[category] = {
            'amount': float(amount),
            'period': period,
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }
        self._save_budgets()
    
    def get_budget(self, category):
        """Get budget for a specific category."""
        return self.budgets.get(category, None)
    
    def get_all_budgets(self):
        """Get all budgets."""
        return self.budgets
    
    def delete_budget(self, category):
        """Delete a budget for a category."""
        if category in self.budgets:
            del self.budgets[category]
            self._save_budgets()
            return True
        return False
    
    def get_budget_status(self, category):
        """
        Get budget status for a category (current spending vs budget).
        
        Args:
            category (str): Category name
            
        Returns:
            dict: Budget status information
        """
        budget = self.get_budget(category)
        if not budget:
            return None
        
        # Calculate total spending for this category
        category_expenses = sum(
            t['amount'] for t in self.transactions 
            if t['category'].lower() == category.lower() and t['type'] == 'expense'
        )
        
        budget_amount = budget['amount']
        remaining = budget_amount - category_expenses
        percentage_used = (category_expenses / budget_amount * 100) if budget_amount > 0 else 0
        
        return {
            'category': category,
            'budget': budget_amount,
            'spent': category_expenses,
            'remaining': remaining,
            'percentage_used': percentage_used,
            'period': budget.get('period', 'monthly'),
            'status': 'over' if remaining < 0 else 'warning' if percentage_used > 80 else 'good'
        }
    
    def get_all_budget_statuses(self):
        """Get budget status for all categories with budgets."""
        statuses = []
        for category in self.budgets.keys():
            status = self.get_budget_status(category)
            if status:
                statuses.append(status)
        return statuses

