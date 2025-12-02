"""
Finance Tracker - Visualization Module
Generate charts and graphs for financial data visualization.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import defaultdict
import os


class FinanceVisualizer:
    """Class for generating financial data visualizations."""
    
    def __init__(self, tracker):
        """
        Initialize visualizer with a tracker instance.
        
        Args:
            tracker: FinanceTracker instance
        """
        self.tracker = tracker
        self.output_dir = 'data/charts'
        self._ensure_output_directory()
    
    def _ensure_output_directory(self):
        """Create output directory for charts if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def plot_income_vs_expenses(self, save=True, show=False):
        """
        Create a bar chart comparing total income vs expenses.
        
        Args:
            save (bool): Whether to save the chart to file
            show (bool): Whether to display the chart
            
        Returns:
            str: Path to saved chart file
        """
        summary = self.tracker.get_summary()
        
        categories = ['Income', 'Expenses']
        amounts = [summary['total_income'], summary['total_expenses']]
        colors = ['#2ecc71', '#e74c3c']
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, amounts, color=colors, alpha=0.8, edgecolor='black')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.2f}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        plt.title('Income vs Expenses', fontsize=16, fontweight='bold', pad=20)
        plt.ylabel('Amount ($)', fontsize=12)
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add balance line
        balance = summary['balance']
        balance_color = 'green' if balance >= 0 else 'red'
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        plt.tight_layout()
        
        filename = os.path.join(self.output_dir, 'income_vs_expenses.png')
        if save:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        
        return filename
    
    def plot_category_breakdown(self, transaction_type='expense', save=True, show=False):
        """
        Create a pie chart showing breakdown by category.
        
        Args:
            transaction_type (str): 'income' or 'expense'
            save (bool): Whether to save the chart to file
            show (bool): Whether to display the chart
            
        Returns:
            str: Path to saved chart file
        """
        categories = self.tracker.get_category_summary()
        
        # Filter by transaction type
        data = {}
        for category, amounts in categories.items():
            if transaction_type == 'expense':
                if amounts['expense'] > 0:
                    data[category] = amounts['expense']
            else:
                if amounts['income'] > 0:
                    data[category] = amounts['income']
        
        if not data:
            return None
        
        # Sort by amount
        sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
        
        plt.figure(figsize=(12, 8))
        
        # Create pie chart
        colors = plt.cm.Set3(range(len(sorted_data)))
        wedges, texts, autotexts = plt.pie(
            sorted_data.values(),
            labels=sorted_data.keys(),
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            pctdistance=0.85
        )
        
        # Enhance text
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        title = f'{transaction_type.capitalize()} Breakdown by Category'
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Add legend with amounts
        legend_labels = [f'{cat}: ${amt:,.2f}' for cat, amt in sorted_data.items()]
        plt.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.tight_layout()
        
        filename = os.path.join(self.output_dir, f'{transaction_type}_breakdown.png')
        if save:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        
        return filename
    
    def plot_spending_over_time(self, save=True, show=False):
        """
        Create a line chart showing spending over time.
        
        Args:
            save (bool): Whether to save the chart to file
            show (bool): Whether to display the chart
            
        Returns:
            str: Path to saved chart file
        """
        transactions = self.tracker.get_all_transactions()
        
        if not transactions:
            return None
        
        # Group transactions by date
        daily_data = defaultdict(lambda: {'income': 0, 'expense': 0})
        
        for t in transactions:
            date = t['date'].split()[0]  # Get date part
            if t['type'] == 'income':
                daily_data[date]['income'] += t['amount']
            else:
                daily_data[date]['expense'] += t['amount']
        
        # Sort by date
        sorted_dates = sorted(daily_data.keys())
        dates = [datetime.strptime(d, '%Y-%m-%d') for d in sorted_dates]
        incomes = [daily_data[d]['income'] for d in sorted_dates]
        expenses = [daily_data[d]['expense'] for d in sorted_dates]
        
        plt.figure(figsize=(14, 7))
        
        # Plot lines
        plt.plot(dates, incomes, marker='o', linewidth=2, label='Income', 
                color='#2ecc71', markersize=6)
        plt.plot(dates, expenses, marker='s', linewidth=2, label='Expenses', 
                color='#e74c3c', markersize=6)
        
        # Formatting
        plt.title('Income and Expenses Over Time', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Amount ($)', fontsize=12)
        plt.legend(fontsize=11, loc='best')
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Format x-axis dates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate()
        
        plt.tight_layout()
        
        filename = os.path.join(self.output_dir, 'spending_over_time.png')
        if save:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        
        return filename
    
    def plot_budget_progress(self, save=True, show=False):
        """
        Create a bar chart showing budget progress for all categories.
        
        Args:
            save (bool): Whether to save the chart to file
            show (bool): Whether to display the chart
            
        Returns:
            str: Path to saved chart file
        """
        statuses = self.tracker.get_all_budget_statuses()
        
        if not statuses:
            return None
        
        categories = [s['category'] for s in statuses]
        budgets = [s['budget'] for s in statuses]
        spent = [s['spent'] for s in statuses]
        
        x = range(len(categories))
        width = 0.35
        
        plt.figure(figsize=(12, 7))
        
        bars1 = plt.bar([i - width/2 for i in x], budgets, width, 
                       label='Budget', color='#3498db', alpha=0.8, edgecolor='black')
        bars2 = plt.bar([i + width/2 for i in x], spent, width, 
                       label='Spent', color='#e74c3c', alpha=0.8, edgecolor='black')
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}',
                    ha='center', va='bottom', fontsize=9)
        
        for bar in bars2:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}',
                    ha='center', va='bottom', fontsize=9)
        
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Amount ($)', fontsize=12)
        plt.title('Budget Progress by Category', fontsize=16, fontweight='bold', pad=20)
        plt.xticks(x, categories, rotation=45, ha='right')
        plt.legend(fontsize=11)
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        filename = os.path.join(self.output_dir, 'budget_progress.png')
        if save:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        
        return filename
    
    def plot_cumulative_balance(self, save=True, show=False):
        """
        Create a line chart showing cumulative balance over time.
        
        Args:
            save (bool): Whether to save the chart to file
            show (bool): Whether to display the chart
            
        Returns:
            str: Path to saved chart file
        """
        transactions = sorted(self.tracker.get_all_transactions(), 
                             key=lambda x: x['date'])
        
        if not transactions:
            return None
        
        dates = []
        balances = []
        current_balance = 0
        
        for t in transactions:
            date = datetime.strptime(t['date'], '%Y-%m-%d %H:%M:%S')
            if t['type'] == 'income':
                current_balance += t['amount']
            else:
                current_balance -= t['amount']
            
            dates.append(date)
            balances.append(current_balance)
        
        plt.figure(figsize=(14, 7))
        
        # Plot line
        plt.plot(dates, balances, linewidth=2.5, color='#3498db', marker='o', 
                markersize=5, markerfacecolor='white', markeredgewidth=2)
        
        # Fill area
        plt.fill_between(dates, balances, alpha=0.3, color='#3498db')
        
        # Add zero line
        plt.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.7)
        
        plt.title('Cumulative Balance Over Time', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Balance ($)', fontsize=12)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Format x-axis dates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate()
        
        plt.tight_layout()
        
        filename = os.path.join(self.output_dir, 'cumulative_balance.png')
        if save:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()
        
        return filename
    
    def generate_all_charts(self):
        """
        Generate all available charts.
        
        Returns:
            dict: Dictionary of chart names and their file paths
        """
        charts = {}
        
        print("Generating charts...")
        
        # Income vs Expenses
        filename = self.plot_income_vs_expenses()
        if filename:
            charts['income_vs_expenses'] = filename
            print(f"  [+] Income vs Expenses chart saved")
        
        # Expense Breakdown
        filename = self.plot_category_breakdown('expense')
        if filename:
            charts['expense_breakdown'] = filename
            print(f"  [+] Expense Breakdown chart saved")
        
        # Income Breakdown
        filename = self.plot_category_breakdown('income')
        if filename:
            charts['income_breakdown'] = filename
            print(f"  [+] Income Breakdown chart saved")
        
        # Spending Over Time
        filename = self.plot_spending_over_time()
        if filename:
            charts['spending_over_time'] = filename
            print(f"  [+] Spending Over Time chart saved")
        
        # Budget Progress
        filename = self.plot_budget_progress()
        if filename:
            charts['budget_progress'] = filename
            print(f"  [+] Budget Progress chart saved")
        
        # Cumulative Balance
        filename = self.plot_cumulative_balance()
        if filename:
            charts['cumulative_balance'] = filename
            print(f"  [+] Cumulative Balance chart saved")
        
        print(f"\nTotal charts generated: {len(charts)}")
        print(f"Charts saved to: {self.output_dir}")
        
        return charts

