# Finance Tracker Web Application Guide

## 🌐 Accessing the Application

The web application is now running! Open your browser and navigate to:

```
http://localhost:5000
```

## 📱 Application Features

### 1. Dashboard (Home Page)
**URL:** `http://localhost:5000/`

**Features:**
- **Summary Cards**: View at-a-glance statistics
  - Total Income (green)
  - Total Expenses (red)
  - Current Balance (blue)
  - Transaction Count
  
- **Interactive Charts**:
  - Spending by Category (Pie Chart)
  - Income vs Expenses (Bar Chart)
  
- **Recent Transactions**: View your latest 10 transactions
  
- **Quick Actions Buttons**: 
  - Add Income
  - Add Expense
  - Set Budget

### 2. Transactions Page
**URL:** `http://localhost:5000/transactions`

**Features:**
- View all transactions in a detailed table
- Filter by date range
- Add new income/expense
- Delete transactions
- Export to CSV

**How to Use:**
1. Click **"+ Income"** or **"+ Expense"** to add a transaction
2. Fill in amount, category, and description
3. Use date filters to view specific periods
4. Click 🗑️ icon to delete a transaction
5. Click **"Export CSV"** to download your data

### 3. Budgets Page
**URL:** `http://localhost:5000/budgets`

**Features:**
- Set budgets for different categories
- View budget progress with visual indicators
- Track spending against budgets
- Real-time status updates

**Budget Status Indicators:**
- 🟢 **On Track**: Under 80% of budget
- 🟡 **Warning**: 80-100% of budget used
- 🔴 **Over Budget**: Exceeded budget

**How to Use:**
1. Click **"+ Set Budget"**
2. Enter category name (e.g., Food, Transport)
3. Set amount and period (weekly/monthly/yearly)
4. Monitor progress with visual bars
5. Delete budgets with 🗑️ icon

### 4. Reports Page
**URL:** `http://localhost:5000/reports`

**Features:**
- Visual financial reports and charts
- 6 different chart types
- Category summary table

**Available Charts:**
1. **Income vs Expenses**: Bar chart comparison
2. **Expense Breakdown**: Pie chart of spending
3. **Income Breakdown**: Pie chart of income sources
4. **Spending Over Time**: Line graph showing trends
5. **Budget Progress**: Bar chart of budget status
6. **Cumulative Balance**: Balance over time

**How to Use:**
1. Click **"Generate All Charts"** to create/update all charts
2. Click **"Refresh"** on individual charts to update specific ones
3. View category summary table at the bottom

## 🎨 User Interface Features

### Color Coding
- 🟢 **Green**: Income, positive balances, on-track budgets
- 🔴 **Red**: Expenses, negative amounts, over-budget
- 🔵 **Blue**: Primary actions, neutral information
- 🟡 **Yellow**: Warnings, alerts

### Responsive Design
- Works on desktop, tablet, and mobile devices
- Automatic layout adjustments
- Touch-friendly buttons and controls

### Toast Notifications
- Success messages (green)
- Error messages (red)
- Info messages (blue)
- Auto-dismiss after 3 seconds

## 🚀 Quick Start Tutorial

### Step 1: Add Your First Transaction
1. Go to Dashboard
2. Click **"+ Add Income"**
3. Enter: Amount: $3000, Category: Salary, Description: Monthly salary
4. Click **"Add Transaction"**

### Step 2: Add Some Expenses
1. Click **"+ Add Expense"**
2. Add various expenses:
   - $800 - Bills - Rent
   - $200 - Food - Groceries
   - $100 - Transport - Gas

### Step 3: Set a Budget
1. Navigate to **"Budgets"** page
2. Click **"+ Set Budget"**
3. Category: Food, Amount: $500, Period: Monthly
4. Watch the progress bar appear!

### Step 4: View Reports
1. Go to **"Reports"** page
2. Click **"Generate All Charts"**
3. View your financial visualizations

## 📊 API Endpoints (For Developers)

The backend provides RESTful API endpoints:

### Summary
- `GET /api/summary` - Get financial summary

### Transactions
- `GET /api/transactions` - Get all transactions
- `POST /api/transactions` - Add transaction
- `DELETE /api/transactions/:id` - Delete transaction
- `PUT /api/transactions/:id` - Update transaction

### Budgets
- `GET /api/budgets` - Get all budgets
- `POST /api/budgets` - Set budget
- `DELETE /api/budgets/:category` - Delete budget

### Charts
- `POST /api/charts/generate` - Generate all charts
- `GET /api/charts/:name` - Get specific chart image

### Other
- `GET /api/export` - Export to CSV
- `GET /api/categories` - Get category summary

## 💡 Tips & Tricks

### Best Practices
1. **Regular Updates**: Add transactions daily for accurate tracking
2. **Realistic Budgets**: Set budgets based on actual spending patterns
3. **Category Consistency**: Use the same category names for better tracking
4. **Weekly Reviews**: Check reports weekly to spot trends

### Common Categories

**Income:**
- Salary
- Freelance
- Investment
- Side Hustle
- Bonus

**Expenses:**
- Bills (Rent, Utilities)
- Food (Groceries, Dining)
- Transport (Gas, Transit)
- Entertainment
- Health & Fitness
- Shopping
- Education

### Keyboard Shortcuts
- Press **Esc** to close modals
- Use **Tab** to navigate forms
- Press **Enter** to submit forms

## 🔧 Troubleshooting

### Application Not Loading?
1. Check if server is running in terminal
2. Verify the URL: `http://localhost:5000`
3. Restart the server: `python app.py`

### Charts Not Showing?
1. Add some transactions first
2. Click "Generate All Charts" button
3. Wait a few seconds for generation
4. Refresh the page

### Data Not Saving?
1. Check `data/` directory exists
2. Verify write permissions
3. Look for error messages in terminal

### Port Already in Use?
```bash
# Kill the process using port 5000
# On Windows PowerShell:
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

## 🛑 Stopping the Application

To stop the web server:
1. Go to the terminal where Flask is running
2. Press **Ctrl + C**

## 🎯 Next Steps

1. **Explore**: Try all features and pages
2. **Customize**: Add your own categories
3. **Track**: Monitor your spending daily
4. **Analyze**: Use reports to understand patterns
5. **Budget**: Set realistic budgets and stick to them

## 📱 Access from Other Devices

To access from other devices on your network:
1. Find your computer's IP address
2. Open `http://YOUR_IP:5000` on other device
3. Make sure firewall allows connections

---

**Enjoy your new Finance Tracker Web Application! 💰📊**

For CLI version, run: `python main.py`
For demo data, run: `python demo.py`

