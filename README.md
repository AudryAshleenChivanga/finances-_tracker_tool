# Finance Tracker Tool

A simple and efficient tool to track your personal finances, manage expenses, and monitor your budget.

## Features

### Core Functionality
- ✅ Track income and expenses
- ✅ Categorize transactions
- ✅ View spending summaries by category
- ✅ Export data to CSV
- ✅ Beautiful command-line interface with colors

### Advanced Features
- 💰 **Budget Management**: Set and track budgets by category (weekly, monthly, yearly)
- 📊 **Data Visualization**: Generate charts and graphs
  - Income vs Expenses bar chart
  - Category breakdown pie charts
  - Spending trends over time
  - Budget progress tracking
  - Cumulative balance chart
- 🔍 **Date Filtering**: View transactions within specific date ranges
- ✏️ **Transaction Management**: Edit and delete transactions
- 📈 **Budget Status Tracking**: Real-time budget alerts and warnings
- 🎨 **Visual Budget Indicators**: Color-coded status (Good, Warning, Over Budget)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/AudryAshleenChivanga/finances-_tracker_tool.git
cd finances-_tracker_tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the finance tracker:
```bash
python main.py
```

### Menu Options

#### Transactions
1. **Add Income** - Record income with category and description
2. **Add Expense** - Record expenses with category and description
3. **View All Transactions** - Display all transactions in a formatted table
4. **View Transactions by Date** - Filter transactions by date range
5. **Delete Transaction** - Remove a transaction by ID

#### Summary & Reports
6. **View Summary** - See total income, expenses, and balance
7. **View Category Breakdown** - See spending/income by category

#### Budget Management
8. **Set Budget** - Create budgets for categories (weekly/monthly/yearly)
9. **View Budget Status** - Check budget status for a specific category
10. **View All Budgets** - See all budgets with spending status

#### Visualizations
11. **Generate Charts** - Create visual charts and graphs
    - Income vs Expenses comparison
    - Expense/Income breakdown (pie charts)
    - Spending trends over time
    - Budget progress visualization
    - Cumulative balance chart

#### Other
12. **Export to CSV** - Export transaction data to CSV file
13. **Exit** - Save and exit the application

## Project Structure

```
finances-_tracker_tool/
├── main.py                    # Main application entry point
├── finance_tracker.py         # Core finance tracking logic
├── visualizer.py              # Data visualization module
├── test_finance_tracker.py   # Unit tests
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
└── data/
    ├── transactions.json      # Transaction data (auto-created)
    ├── budgets.json           # Budget data (auto-created)
    └── charts/                # Generated charts (auto-created)
```

## Testing

Run the unit tests to verify functionality:

```bash
python test_finance_tracker.py
```

Or with verbose output:

```bash
python test_finance_tracker.py -v
```

The test suite includes:
- Transaction management tests
- Budget management tests
- Date filtering tests
- Summary and reporting tests
- Edge case handling

## License

MIT License

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

