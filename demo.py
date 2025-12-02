"""
Demo script to showcase the Finance Tracker functionality
This script demonstrates the key features without requiring user interaction.
"""

from finance_tracker import FinanceTracker
from visualizer import FinanceVisualizer
from tabulate import tabulate
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

print(Fore.CYAN + "\n" + "="*60)
print(Fore.CYAN + "     FINANCE TRACKER - AUTOMATED DEMO")
print(Fore.CYAN + "="*60 + "\n")

# Create a demo tracker with a separate demo file
tracker = FinanceTracker('data/demo_transactions.json', 'data/demo_budgets.json')

print(Fore.YELLOW + "\n[DEMO] Adding Income Transactions...")
print("-" * 60)

# Add income
tracker.add_transaction(3000, 'Salary', 'Monthly salary payment', 'income')
print(Fore.GREEN + "[+] Added: $3000 - Salary")

tracker.add_transaction(500, 'Freelance', 'Website design project', 'income')
print(Fore.GREEN + "[+] Added: $500 - Freelance")

tracker.add_transaction(200, 'Investment', 'Stock dividends', 'income')
print(Fore.GREEN + "[+] Added: $200 - Investment")

print(Fore.YELLOW + "\n[DEMO] Adding Expense Transactions...")
print("-" * 60)

# Add expenses
expenses = [
    (800, 'Bills', 'Rent payment'),
    (200, 'Bills', 'Utilities (electric, water, internet)'),
    (250, 'Food', 'Groceries for the month'),
    (150, 'Food', 'Restaurants and dining out'),
    (100, 'Transport', 'Gas and parking'),
    (80, 'Transport', 'Public transit pass'),
    (120, 'Entertainment', 'Movies and streaming services'),
    (50, 'Entertainment', 'Concert tickets'),
    (150, 'Shopping', 'New clothes'),
    (75, 'Health', 'Gym membership'),
]

for amount, category, description in expenses:
    tracker.add_transaction(amount, category, description, 'expense')
    print(Fore.RED + f"[-] Added: ${amount} - {category} ({description})")

print(Fore.YELLOW + "\n[DEMO] Viewing All Transactions...")
print("-" * 60)

transactions = tracker.get_all_transactions()
table_data = []
for t in transactions[:10]:  # Show first 10
    color = Fore.GREEN if t['type'] == 'income' else Fore.RED
    table_data.append([
        t['id'],
        t['date'].split()[0],
        t['type'].capitalize(),
        f"${t['amount']:.2f}",
        t['category'],
        t['description'][:30] + '...' if len(t['description']) > 30 else t['description']
    ])

headers = ['ID', 'Date', 'Type', 'Amount', 'Category', 'Description']
print(tabulate(table_data, headers=headers, tablefmt='grid'))
print(f"\n(Showing 10 of {len(transactions)} transactions)")

print(Fore.YELLOW + "\n[DEMO] Financial Summary...")
print("-" * 60)

summary = tracker.get_summary()
print(Fore.GREEN + f"Total Income:     ${summary['total_income']:,.2f}")
print(Fore.RED + f"Total Expenses:   ${summary['total_expenses']:,.2f}")
print(Fore.YELLOW + "-" * 40)
balance = summary['balance']
balance_color = Fore.GREEN if balance >= 0 else Fore.RED
print(balance_color + f"Current Balance:  ${balance:,.2f}")
print(Fore.CYAN + f"Total Transactions: {summary['transaction_count']}")

print(Fore.YELLOW + "\n[DEMO] Category Breakdown...")
print("-" * 60)

categories = tracker.get_category_summary()
table_data = []
for category, amounts in sorted(categories.items()):
    income = amounts['income']
    expense = amounts['expense']
    net = income - expense
    table_data.append([
        category,
        f"${income:.2f}",
        f"${expense:.2f}",
        f"${net:.2f}"
    ])

headers = ['Category', 'Income', 'Expenses', 'Net']
print(tabulate(table_data, headers=headers, tablefmt='grid'))

print(Fore.YELLOW + "\n[DEMO] Setting Budgets...")
print("-" * 60)

# Set budgets
budgets_to_set = [
    ('Food', 500, 'monthly'),
    ('Transport', 200, 'monthly'),
    ('Entertainment', 150, 'monthly'),
    ('Shopping', 200, 'monthly'),
    ('Bills', 1100, 'monthly'),
]

for category, amount, period in budgets_to_set:
    tracker.set_budget(category, amount, period)
    print(Fore.GREEN + f"[+] Set budget: {category} = ${amount}/{period}")

print(Fore.YELLOW + "\n[DEMO] Budget Status for All Categories...")
print("-" * 60)

statuses = tracker.get_all_budget_statuses()
table_data = []

for status in statuses:
    # Status indicator
    if status['status'] == 'over':
        status_icon = Fore.RED + "[!] OVER"
    elif status['status'] == 'warning':
        status_icon = Fore.YELLOW + "[!] WARN"
    else:
        status_icon = Fore.GREEN + "[OK] GOOD"
    
    # Progress bar
    percentage = min(status['percentage_used'], 100)
    bar_length = 20
    filled = int(bar_length * percentage / 100)
    bar = '#' * filled + '-' * (bar_length - filled)
    
    if status['status'] == 'over':
        bar_color = Fore.RED
    elif status['status'] == 'warning':
        bar_color = Fore.YELLOW
    else:
        bar_color = Fore.GREEN
    
    table_data.append([
        status['category'],
        f"${status['budget']:.2f}",
        f"${status['spent']:.2f}",
        f"${status['remaining']:.2f}",
        f"{bar_color}{bar}{Fore.RESET} {percentage:.1f}%",
        status_icon
    ])

headers = ['Category', 'Budget', 'Spent', 'Remaining', 'Progress', 'Status']
print(tabulate(table_data, headers=headers, tablefmt='grid'))

print(Fore.YELLOW + "\n[DEMO] Generating Visualization Charts...")
print("-" * 60)

visualizer = FinanceVisualizer(tracker)
charts = visualizer.generate_all_charts()

print(Fore.GREEN + f"\n[+] Successfully generated {len(charts)} charts!")
print(Fore.CYAN + f"\nCharts saved to: {visualizer.output_dir}")
print(Fore.CYAN + "\nGenerated charts:")
for chart_name, filepath in charts.items():
    print(f"  - {chart_name}: {filepath}")

print(Fore.YELLOW + "\n[DEMO] Exporting to CSV...")
print("-" * 60)

if tracker.export_to_csv('data/demo_export.csv'):
    print(Fore.GREEN + "[+] Data exported to: data/demo_export.csv")

print(Fore.CYAN + "\n" + "="*60)
print(Fore.CYAN + "     DEMO COMPLETE!")
print(Fore.CYAN + "="*60)

print(Fore.WHITE + "\n[SUMMARY] Demo Results:")
print(f"  - Added {summary['transaction_count']} transactions")
print(f"  - Set {len(budgets_to_set)} budgets")
print(f"  - Generated {len(charts)} visualization charts")
print(f"  - Current balance: ${balance:,.2f}")

print(Fore.YELLOW + "\n[TIP] To use the interactive app, run: python main.py")
print(Fore.WHITE + "   Or see QUICKSTART.md for detailed instructions\n")

