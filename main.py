"""
Finance Tracker Tool - Main Application
A command-line interface for tracking personal finances.
"""

from finance_tracker import FinanceTracker
from visualizer import FinanceVisualizer
from tabulate import tabulate
from colorama import init, Fore, Style
import sys
import os

# Initialize colorama for colored terminal output
init(autoreset=True)


def print_header():
    """Print application header."""
    print(Fore.CYAN + "\n" + "="*50)
    print(Fore.CYAN + "       PERSONAL FINANCE TRACKER TOOL")
    print(Fore.CYAN + "="*50 + "\n")


def print_menu():
    """Display the main menu."""
    print(Fore.YELLOW + "\n═══ Menu Options ═══")
    print(Fore.CYAN + "  Transactions:")
    print("    1. Add Income")
    print("    2. Add Expense")
    print("    3. View All Transactions")
    print("    4. View Transactions by Date")
    print("    5. Delete Transaction")
    print(Fore.CYAN + "  Summary & Reports:")
    print("    6. View Summary")
    print("    7. View Category Breakdown")
    print(Fore.CYAN + "  Budget Management:")
    print("    8. Set Budget")
    print("    9. View Budget Status")
    print("   10. View All Budgets")
    print(Fore.CYAN + "  Visualizations:")
    print("   11. Generate Charts")
    print(Fore.CYAN + "  Other:")
    print("   12. Export to CSV")
    print("   13. Exit")
    print()


def add_income(tracker):
    """Add an income transaction."""
    try:
        print(Fore.GREEN + "\n--- Add Income ---")
        amount = float(input("Enter amount: $"))
        category = input("Enter category (e.g., Salary, Freelance, Investment): ")
        description = input("Enter description: ")
        
        transaction = tracker.add_transaction(amount, category, description, 'income')
        print(Fore.GREEN + f"✓ Income of ${amount:.2f} added successfully!")
        
    except ValueError:
        print(Fore.RED + "✗ Invalid amount. Please enter a number.")
    except Exception as e:
        print(Fore.RED + f"✗ Error: {str(e)}")


def add_expense(tracker):
    """Add an expense transaction."""
    try:
        print(Fore.RED + "\n--- Add Expense ---")
        amount = float(input("Enter amount: $"))
        category = input("Enter category (e.g., Food, Transport, Bills, Entertainment): ")
        description = input("Enter description: ")
        
        transaction = tracker.add_transaction(amount, category, description, 'expense')
        print(Fore.GREEN + f"✓ Expense of ${amount:.2f} added successfully!")
        
    except ValueError:
        print(Fore.RED + "✗ Invalid amount. Please enter a number.")
    except Exception as e:
        print(Fore.RED + f"✗ Error: {str(e)}")


def view_transactions(tracker):
    """Display all transactions in a table format."""
    transactions = tracker.get_all_transactions()
    
    if not transactions:
        print(Fore.YELLOW + "\nNo transactions found.")
        return
    
    print(Fore.CYAN + "\n--- All Transactions ---")
    
    # Prepare data for tabulation
    table_data = []
    for t in transactions:
        color = Fore.GREEN if t['type'] == 'income' else Fore.RED
        amount_str = f"{color}${t['amount']:.2f}"
        table_data.append([
            t['id'],
            t['date'],
            t['type'].capitalize(),
            amount_str,
            t['category'],
            t['description']
        ])
    
    headers = ['ID', 'Date', 'Type', 'Amount', 'Category', 'Description']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))


def view_summary(tracker):
    """Display financial summary."""
    summary = tracker.get_summary()
    
    print(Fore.CYAN + "\n--- Financial Summary ---")
    print(Fore.GREEN + f"Total Income:     ${summary['total_income']:.2f}")
    print(Fore.RED + f"Total Expenses:   ${summary['total_expenses']:.2f}")
    print(Fore.YELLOW + "-" * 40)
    
    balance = summary['balance']
    balance_color = Fore.GREEN if balance >= 0 else Fore.RED
    print(balance_color + f"Current Balance:  ${balance:.2f}")
    print(Fore.CYAN + f"Total Transactions: {summary['transaction_count']}")


def view_category_breakdown(tracker):
    """Display spending breakdown by category."""
    categories = tracker.get_category_summary()
    
    if not categories:
        print(Fore.YELLOW + "\nNo transactions found.")
        return
    
    print(Fore.CYAN + "\n--- Category Breakdown ---")
    
    table_data = []
    for category, amounts in categories.items():
        income = amounts['income']
        expense = amounts['expense']
        net = income - expense
        net_color = Fore.GREEN if net >= 0 else Fore.RED
        
        table_data.append([
            category,
            f"${income:.2f}",
            f"${expense:.2f}",
            f"{net_color}${net:.2f}"
        ])
    
    headers = ['Category', 'Income', 'Expenses', 'Net']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))


def export_data(tracker):
    """Export transactions to CSV."""
    filename = input("Enter filename (default: data/transactions.csv): ").strip()
    if not filename:
        filename = 'data/transactions.csv'
    
    if tracker.export_to_csv(filename):
        print(Fore.GREEN + f"✓ Data exported successfully to {filename}")
    else:
        print(Fore.RED + "✗ No data to export.")


def view_transactions_by_date(tracker):
    """Display transactions filtered by date range."""
    print(Fore.CYAN + "\n--- Filter Transactions by Date ---")
    print("Leave blank to skip date filtering")
    
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()
    
    start_date = start_date if start_date else None
    end_date = end_date if end_date else None
    
    transactions = tracker.get_transactions_by_date_range(start_date, end_date)
    
    if not transactions:
        print(Fore.YELLOW + "\nNo transactions found in this date range.")
        return
    
    print(Fore.CYAN + f"\n--- Transactions ({len(transactions)} found) ---")
    
    table_data = []
    for t in transactions:
        color = Fore.GREEN if t['type'] == 'income' else Fore.RED
        amount_str = f"{color}${t['amount']:.2f}"
        table_data.append([
            t['id'],
            t['date'],
            t['type'].capitalize(),
            amount_str,
            t['category'],
            t['description']
        ])
    
    headers = ['ID', 'Date', 'Type', 'Amount', 'Category', 'Description']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))


def delete_transaction(tracker):
    """Delete a transaction by ID."""
    print(Fore.CYAN + "\n--- Delete Transaction ---")
    
    # Show recent transactions first
    transactions = tracker.get_all_transactions()
    if not transactions:
        print(Fore.YELLOW + "No transactions to delete.")
        return
    
    # Show last 10 transactions
    print(Fore.CYAN + "\nRecent Transactions:")
    recent = transactions[-10:] if len(transactions) > 10 else transactions
    
    table_data = []
    for t in recent:
        color = Fore.GREEN if t['type'] == 'income' else Fore.RED
        amount_str = f"{color}${t['amount']:.2f}"
        table_data.append([
            t['id'],
            t['date'].split()[0],  # Just the date
            t['type'].capitalize(),
            amount_str,
            t['category']
        ])
    
    headers = ['ID', 'Date', 'Type', 'Amount', 'Category']
    print(tabulate(table_data, headers=headers, tablefmt='simple'))
    
    try:
        transaction_id = int(input("\nEnter transaction ID to delete (0 to cancel): "))
        if transaction_id == 0:
            print(Fore.YELLOW + "Cancelled.")
            return
        
        if tracker.delete_transaction(transaction_id):
            print(Fore.GREEN + f"✓ Transaction #{transaction_id} deleted successfully!")
        else:
            print(Fore.RED + f"✗ Transaction #{transaction_id} not found.")
    
    except ValueError:
        print(Fore.RED + "✗ Invalid transaction ID.")
    except Exception as e:
        print(Fore.RED + f"✗ Error: {str(e)}")


def set_budget(tracker):
    """Set a budget for a category."""
    try:
        print(Fore.CYAN + "\n--- Set Budget ---")
        category = input("Enter category name: ").strip()
        if not category:
            print(Fore.RED + "✗ Category cannot be empty.")
            return
        
        amount = float(input("Enter budget amount: $"))
        if amount <= 0:
            print(Fore.RED + "✗ Budget amount must be positive.")
            return
        
        print("\nBudget period:")
        print("  1. Weekly")
        print("  2. Monthly (default)")
        print("  3. Yearly")
        period_choice = input("Enter choice (1-3): ").strip()
        
        period_map = {'1': 'weekly', '2': 'monthly', '3': 'yearly'}
        period = period_map.get(period_choice, 'monthly')
        
        tracker.set_budget(category, amount, period)
        print(Fore.GREEN + f"✓ Budget of ${amount:.2f} per {period} set for '{category}'")
        
    except ValueError:
        print(Fore.RED + "✗ Invalid amount. Please enter a number.")
    except Exception as e:
        print(Fore.RED + f"✗ Error: {str(e)}")


def view_budget_status(tracker):
    """View budget status for a specific category."""
    budgets = tracker.get_all_budgets()
    
    if not budgets:
        print(Fore.YELLOW + "\nNo budgets set. Use option 8 to set a budget.")
        return
    
    print(Fore.CYAN + "\n--- Available Budgets ---")
    for i, category in enumerate(budgets.keys(), 1):
        print(f"  {i}. {category}")
    
    category = input("\nEnter category name: ").strip()
    status = tracker.get_budget_status(category)
    
    if not status:
        print(Fore.RED + f"✗ No budget found for '{category}'")
        return
    
    print(Fore.CYAN + f"\n--- Budget Status: {status['category']} ---")
    print(f"Period: {status['period'].capitalize()}")
    print(f"Budget: ${status['budget']:.2f}")
    print(Fore.RED + f"Spent:  ${status['spent']:.2f}")
    
    remaining_color = Fore.GREEN if status['remaining'] >= 0 else Fore.RED
    print(remaining_color + f"Remaining: ${status['remaining']:.2f}")
    
    # Show percentage bar
    percentage = min(status['percentage_used'], 100)
    bar_length = 30
    filled = int(bar_length * percentage / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    if status['status'] == 'over':
        bar_color = Fore.RED
        status_text = "OVER BUDGET!"
    elif status['status'] == 'warning':
        bar_color = Fore.YELLOW
        status_text = "Warning"
    else:
        bar_color = Fore.GREEN
        status_text = "On Track"
    
    print(f"\n{bar_color}{bar} {percentage:.1f}%")
    print(f"Status: {bar_color}{status_text}")


def view_all_budgets(tracker):
    """View all budgets and their statuses."""
    statuses = tracker.get_all_budget_statuses()
    
    if not statuses:
        print(Fore.YELLOW + "\nNo budgets set. Use option 8 to set a budget.")
        return
    
    print(Fore.CYAN + "\n--- All Budget Statuses ---\n")
    
    table_data = []
    for status in statuses:
        # Status indicator
        if status['status'] == 'over':
            status_icon = Fore.RED + "⚠ OVER"
        elif status['status'] == 'warning':
            status_icon = Fore.YELLOW + "⚠ WARN"
        else:
            status_icon = Fore.GREEN + "✓ GOOD"
        
        remaining_color = Fore.GREEN if status['remaining'] >= 0 else Fore.RED
        
        table_data.append([
            status['category'],
            f"${status['budget']:.2f}",
            f"${status['spent']:.2f}",
            f"{remaining_color}${status['remaining']:.2f}",
            f"{status['percentage_used']:.1f}%",
            status_icon
        ])
    
    headers = ['Category', 'Budget', 'Spent', 'Remaining', 'Used %', 'Status']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))


def generate_charts(tracker):
    """Generate financial visualization charts."""
    print(Fore.CYAN + "\n--- Generate Charts ---")
    
    transactions = tracker.get_all_transactions()
    if not transactions:
        print(Fore.YELLOW + "No transactions found. Add some transactions first.")
        return
    
    print("\nChart Options:")
    print("  1. Income vs Expenses")
    print("  2. Expense Breakdown (Pie Chart)")
    print("  3. Income Breakdown (Pie Chart)")
    print("  4. Spending Over Time")
    print("  5. Budget Progress")
    print("  6. Cumulative Balance")
    print("  7. Generate All Charts")
    print("  0. Cancel")
    
    choice = input("\nEnter your choice (0-7): ").strip()
    
    try:
        visualizer = FinanceVisualizer(tracker)
        
        if choice == '1':
            filename = visualizer.plot_income_vs_expenses()
            print(Fore.GREEN + f"\n✓ Chart saved: {filename}")
        elif choice == '2':
            filename = visualizer.plot_category_breakdown('expense')
            if filename:
                print(Fore.GREEN + f"\n✓ Chart saved: {filename}")
            else:
                print(Fore.YELLOW + "\n⚠ No expense data to visualize")
        elif choice == '3':
            filename = visualizer.plot_category_breakdown('income')
            if filename:
                print(Fore.GREEN + f"\n✓ Chart saved: {filename}")
            else:
                print(Fore.YELLOW + "\n⚠ No income data to visualize")
        elif choice == '4':
            filename = visualizer.plot_spending_over_time()
            if filename:
                print(Fore.GREEN + f"\n✓ Chart saved: {filename}")
            else:
                print(Fore.YELLOW + "\n⚠ Not enough data to visualize")
        elif choice == '5':
            filename = visualizer.plot_budget_progress()
            if filename:
                print(Fore.GREEN + f"\n✓ Chart saved: {filename}")
            else:
                print(Fore.YELLOW + "\n⚠ No budgets set. Set a budget first (option 8)")
        elif choice == '6':
            filename = visualizer.plot_cumulative_balance()
            if filename:
                print(Fore.GREEN + f"\n✓ Chart saved: {filename}")
            else:
                print(Fore.YELLOW + "\n⚠ Not enough data to visualize")
        elif choice == '7':
            print()
            charts = visualizer.generate_all_charts()
            print(Fore.GREEN + f"\n✓ Successfully generated {len(charts)} chart(s)!")
        elif choice == '0':
            print(Fore.YELLOW + "Cancelled.")
        else:
            print(Fore.RED + "✗ Invalid choice.")
        
        # Open the charts folder
        if choice != '0' and choice in ['1', '2', '3', '4', '5', '6', '7']:
            open_folder = input("\nOpen charts folder? (y/n): ").strip().lower()
            if open_folder == 'y':
                chart_path = os.path.abspath(visualizer.output_dir)
                os.startfile(chart_path)  # Windows-specific
                print(Fore.GREEN + "✓ Folder opened!")
    
    except ImportError:
        print(Fore.RED + "\n✗ Visualization requires matplotlib.")
        print("Install it with: pip install matplotlib")
    except Exception as e:
        print(Fore.RED + f"\n✗ Error generating chart: {str(e)}")


def main():
    """Main application loop."""
    tracker = FinanceTracker()
    
    print_header()
    print(Fore.WHITE + "Welcome to your Personal Finance Tracker!")
    print("Track your income and expenses with ease.")
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-13): ").strip()
        
        if choice == '1':
            add_income(tracker)
        elif choice == '2':
            add_expense(tracker)
        elif choice == '3':
            view_transactions(tracker)
        elif choice == '4':
            view_transactions_by_date(tracker)
        elif choice == '5':
            delete_transaction(tracker)
        elif choice == '6':
            view_summary(tracker)
        elif choice == '7':
            view_category_breakdown(tracker)
        elif choice == '8':
            set_budget(tracker)
        elif choice == '9':
            view_budget_status(tracker)
        elif choice == '10':
            view_all_budgets(tracker)
        elif choice == '11':
            generate_charts(tracker)
        elif choice == '12':
            export_data(tracker)
        elif choice == '13':
            print(Fore.CYAN + "\nThank you for using Finance Tracker!")
            print("Goodbye! 👋\n")
            sys.exit(0)
        else:
            print(Fore.RED + "✗ Invalid choice. Please enter a number between 1 and 13.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n\nInterrupted. Goodbye! 👋\n")
        sys.exit(0)

