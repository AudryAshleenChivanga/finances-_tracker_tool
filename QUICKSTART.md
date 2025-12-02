# Quick Start Guide

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- pandas (data handling)
- tabulate (table formatting)
- colorama (colored terminal output)
- matplotlib (charts and graphs)

### 2. Run the Application

```bash
python main.py
```

## Example Usage Workflow

### Step 1: Add Some Income

1. Select option `1` (Add Income)
2. Enter amount: `3000`
3. Enter category: `Salary`
4. Enter description: `Monthly salary payment`

### Step 2: Add Some Expenses

1. Select option `2` (Add Expense)
2. Try adding various expenses:
   - Food: $250 (Groceries)
   - Transport: $100 (Gas and parking)
   - Bills: $400 (Rent and utilities)
   - Entertainment: $80 (Movies and dining)

### Step 3: View Your Summary

Select option `6` to see:
- Total Income
- Total Expenses
- Current Balance
- Number of transactions

### Step 4: Set Budgets

1. Select option `8` (Set Budget)
2. Set a budget for `Food`: $300/month
3. Set a budget for `Transport`: $150/month
4. Set a budget for `Entertainment`: $100/month

### Step 5: Check Budget Status

Select option `10` to view all your budgets and see:
- How much you've spent vs budgeted
- Percentage used
- Status indicators (Good, Warning, Over)

### Step 6: Generate Visual Reports

1. Select option `11` (Generate Charts)
2. Choose option `7` (Generate All Charts)
3. Open the charts folder to view your financial visualizations

## Tips

### Budget Management
- ✅ Set realistic budgets based on your spending patterns
- ⚠️ Watch for yellow warnings when you're at 80% of budget
- 🚨 Red alerts appear when you're over budget

### Categories
Common expense categories:
- Food (Groceries, Dining)
- Transport (Gas, Public Transit, Parking)
- Bills (Rent, Utilities, Phone)
- Entertainment (Movies, Games, Hobbies)
- Health (Medical, Gym, Insurance)
- Shopping (Clothing, Electronics)

Common income categories:
- Salary
- Freelance
- Investment
- Side Hustle

### Date Filtering
Format: `YYYY-MM-DD` (e.g., `2025-01-01`)

### Exporting Data
- Choose option `12` to export to CSV
- Default location: `data/transactions.csv`
- Open in Excel, Google Sheets, or any spreadsheet software

## Running Tests

To verify everything is working:

```bash
python test_finance_tracker.py -v
```

You should see all 23 tests pass!

## Troubleshooting

### Charts not generating?
Make sure matplotlib is installed:
```bash
pip install matplotlib
```

### Data not saving?
Check that the `data/` directory exists and is writable.

### Import errors?
Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. Track your expenses daily for a week
2. Review your spending patterns
3. Adjust budgets based on actual spending
4. Use visualizations to identify spending trends
5. Export data monthly for long-term tracking

Happy tracking! 💰📊

