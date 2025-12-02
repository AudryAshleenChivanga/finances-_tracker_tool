"""
Unit tests for Finance Tracker
"""

import unittest
import os
import json
from datetime import datetime
from finance_tracker import FinanceTracker


class TestFinanceTracker(unittest.TestCase):
    """Test cases for FinanceTracker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data_file = 'data/test_transactions.json'
        self.test_budget_file = 'data/test_budgets.json'
        self.tracker = FinanceTracker(self.test_data_file, self.test_budget_file)
        
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        if os.path.exists(self.test_budget_file):
            os.remove(self.test_budget_file)
    
    def test_add_income_transaction(self):
        """Test adding an income transaction."""
        transaction = self.tracker.add_transaction(1000, 'Salary', 'Monthly salary', 'income')
        
        self.assertEqual(transaction['amount'], 1000)
        self.assertEqual(transaction['category'], 'Salary')
        self.assertEqual(transaction['type'], 'income')
        self.assertEqual(len(self.tracker.get_all_transactions()), 1)
    
    def test_add_expense_transaction(self):
        """Test adding an expense transaction."""
        transaction = self.tracker.add_transaction(50, 'Food', 'Groceries', 'expense')
        
        self.assertEqual(transaction['amount'], 50)
        self.assertEqual(transaction['category'], 'Food')
        self.assertEqual(transaction['type'], 'expense')
    
    def test_get_balance(self):
        """Test balance calculation."""
        self.tracker.add_transaction(1000, 'Salary', 'Income', 'income')
        self.tracker.add_transaction(200, 'Food', 'Groceries', 'expense')
        self.tracker.add_transaction(150, 'Transport', 'Gas', 'expense')
        
        balance = self.tracker.get_balance()
        self.assertEqual(balance, 650)  # 1000 - 200 - 150
    
    def test_get_summary(self):
        """Test getting transaction summary."""
        self.tracker.add_transaction(1000, 'Salary', 'Income', 'income')
        self.tracker.add_transaction(500, 'Freelance', 'Side job', 'income')
        self.tracker.add_transaction(200, 'Food', 'Groceries', 'expense')
        
        summary = self.tracker.get_summary()
        
        self.assertEqual(summary['total_income'], 1500)
        self.assertEqual(summary['total_expenses'], 200)
        self.assertEqual(summary['balance'], 1300)
        self.assertEqual(summary['transaction_count'], 3)
    
    def test_empty_summary(self):
        """Test summary with no transactions."""
        summary = self.tracker.get_summary()
        
        self.assertEqual(summary['total_income'], 0)
        self.assertEqual(summary['total_expenses'], 0)
        self.assertEqual(summary['balance'], 0)
        self.assertEqual(summary['transaction_count'], 0)
    
    def test_get_category_summary(self):
        """Test category-based summary."""
        self.tracker.add_transaction(1000, 'Salary', 'Income', 'income')
        self.tracker.add_transaction(200, 'Food', 'Groceries', 'expense')
        self.tracker.add_transaction(150, 'Food', 'Restaurant', 'expense')
        self.tracker.add_transaction(100, 'Transport', 'Gas', 'expense')
        
        categories = self.tracker.get_category_summary()
        
        self.assertEqual(categories['Salary']['income'], 1000)
        self.assertEqual(categories['Food']['expense'], 350)
        self.assertEqual(categories['Transport']['expense'], 100)
    
    def test_delete_transaction(self):
        """Test deleting a transaction."""
        t1 = self.tracker.add_transaction(100, 'Food', 'Lunch', 'expense')
        t2 = self.tracker.add_transaction(200, 'Food', 'Dinner', 'expense')
        
        # Delete first transaction
        result = self.tracker.delete_transaction(t1['id'])
        self.assertTrue(result)
        self.assertEqual(len(self.tracker.get_all_transactions()), 1)
        
        # Try to delete non-existent transaction
        result = self.tracker.delete_transaction(9999)
        self.assertFalse(result)
    
    def test_update_transaction(self):
        """Test updating a transaction."""
        transaction = self.tracker.add_transaction(100, 'Food', 'Lunch', 'expense')
        
        # Update the transaction
        result = self.tracker.update_transaction(
            transaction['id'],
            amount=150,
            description='Updated lunch'
        )
        
        self.assertTrue(result)
        updated = self.tracker.get_all_transactions()[0]
        self.assertEqual(updated['amount'], 150)
        self.assertEqual(updated['description'], 'Updated lunch')
    
    def test_get_transactions_by_date_range(self):
        """Test filtering transactions by date."""
        # Add transactions
        self.tracker.add_transaction(100, 'Food', 'Item 1', 'expense')
        self.tracker.add_transaction(200, 'Food', 'Item 2', 'expense')
        
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Filter by today
        filtered = self.tracker.get_transactions_by_date_range(today, today)
        self.assertEqual(len(filtered), 2)
    
    def test_get_transactions_by_category(self):
        """Test getting transactions by category."""
        self.tracker.add_transaction(100, 'Food', 'Item 1', 'expense')
        self.tracker.add_transaction(200, 'Food', 'Item 2', 'expense')
        self.tracker.add_transaction(300, 'Transport', 'Item 3', 'expense')
        
        food_transactions = self.tracker.get_transactions_by_category('Food')
        self.assertEqual(len(food_transactions), 2)
        
        # Test case insensitivity
        food_transactions = self.tracker.get_transactions_by_category('food')
        self.assertEqual(len(food_transactions), 2)
    
    def test_set_budget(self):
        """Test setting a budget."""
        self.tracker.set_budget('Food', 500, 'monthly')
        
        budget = self.tracker.get_budget('Food')
        self.assertIsNotNone(budget)
        self.assertEqual(budget['amount'], 500)
        self.assertEqual(budget['period'], 'monthly')
    
    def test_get_all_budgets(self):
        """Test getting all budgets."""
        self.tracker.set_budget('Food', 500, 'monthly')
        self.tracker.set_budget('Transport', 200, 'weekly')
        
        budgets = self.tracker.get_all_budgets()
        self.assertEqual(len(budgets), 2)
        self.assertIn('Food', budgets)
        self.assertIn('Transport', budgets)
    
    def test_delete_budget(self):
        """Test deleting a budget."""
        self.tracker.set_budget('Food', 500, 'monthly')
        
        result = self.tracker.delete_budget('Food')
        self.assertTrue(result)
        self.assertIsNone(self.tracker.get_budget('Food'))
        
        # Try to delete non-existent budget
        result = self.tracker.delete_budget('NonExistent')
        self.assertFalse(result)
    
    def test_get_budget_status(self):
        """Test getting budget status."""
        # Set budget
        self.tracker.set_budget('Food', 500, 'monthly')
        
        # Add some expenses
        self.tracker.add_transaction(200, 'Food', 'Groceries', 'expense')
        self.tracker.add_transaction(100, 'Food', 'Restaurant', 'expense')
        
        status = self.tracker.get_budget_status('Food')
        
        self.assertIsNotNone(status)
        self.assertEqual(status['budget'], 500)
        self.assertEqual(status['spent'], 300)
        self.assertEqual(status['remaining'], 200)
        self.assertEqual(status['percentage_used'], 60)
        self.assertEqual(status['status'], 'good')
    
    def test_budget_status_warning(self):
        """Test budget status warning threshold."""
        self.tracker.set_budget('Food', 500, 'monthly')
        self.tracker.add_transaction(450, 'Food', 'Groceries', 'expense')
        
        status = self.tracker.get_budget_status('Food')
        self.assertEqual(status['status'], 'warning')  # Over 80%
    
    def test_budget_status_over(self):
        """Test budget status when over budget."""
        self.tracker.set_budget('Food', 500, 'monthly')
        self.tracker.add_transaction(600, 'Food', 'Groceries', 'expense')
        
        status = self.tracker.get_budget_status('Food')
        self.assertEqual(status['status'], 'over')
        self.assertLess(status['remaining'], 0)
    
    def test_get_all_budget_statuses(self):
        """Test getting all budget statuses."""
        self.tracker.set_budget('Food', 500, 'monthly')
        self.tracker.set_budget('Transport', 200, 'monthly')
        
        self.tracker.add_transaction(300, 'Food', 'Groceries', 'expense')
        self.tracker.add_transaction(150, 'Transport', 'Gas', 'expense')
        
        statuses = self.tracker.get_all_budget_statuses()
        self.assertEqual(len(statuses), 2)
    
    def test_persistence(self):
        """Test that data persists between instances."""
        # Add transaction in first instance
        self.tracker.add_transaction(1000, 'Salary', 'Income', 'income')
        self.tracker.set_budget('Food', 500, 'monthly')
        
        # Create new instance with same files
        new_tracker = FinanceTracker(self.test_data_file, self.test_budget_file)
        
        # Check data persisted
        self.assertEqual(len(new_tracker.get_all_transactions()), 1)
        self.assertIsNotNone(new_tracker.get_budget('Food'))


class TestFinanceTrackerEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data_file = 'data/test_edge_transactions.json'
        self.test_budget_file = 'data/test_edge_budgets.json'
        self.tracker = FinanceTracker(self.test_data_file, self.test_budget_file)
        
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        if os.path.exists(self.test_budget_file):
            os.remove(self.test_budget_file)
    
    def test_zero_amount_transaction(self):
        """Test adding transaction with zero amount."""
        transaction = self.tracker.add_transaction(0, 'Test', 'Zero amount', 'expense')
        self.assertEqual(transaction['amount'], 0)
    
    def test_negative_amount_transaction(self):
        """Test adding transaction with negative amount (should still work)."""
        transaction = self.tracker.add_transaction(-100, 'Test', 'Negative', 'expense')
        self.assertEqual(transaction['amount'], -100)
    
    def test_empty_category(self):
        """Test transaction with empty category."""
        transaction = self.tracker.add_transaction(100, '', 'No category', 'expense')
        self.assertEqual(transaction['category'], '')
    
    def test_budget_status_no_budget(self):
        """Test getting status for non-existent budget."""
        status = self.tracker.get_budget_status('NonExistent')
        self.assertIsNone(status)
    
    def test_budget_zero_amount(self):
        """Test setting budget with zero amount."""
        self.tracker.set_budget('Test', 0, 'monthly')
        status = self.tracker.get_budget_status('Test')
        self.assertEqual(status['percentage_used'], 0)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

