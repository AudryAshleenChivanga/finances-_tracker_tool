# Finance Tracker - Multi-User System Guide

## 🎉 Welcome to Your Personal Finance Tracker!

Your Finance Tracker now supports multiple users with secure authentication, personal data isolation, and customizable preferences!

## 🌐 Getting Started

### Access the Application

Open your browser and go to:
```
http://localhost:5000
```

You'll be greeted with a beautiful landing page showcasing all features!

---

## 📝 User Registration & Login

### Creating Your Account

1. Click **"Get Started"** or **"Sign Up"** on the landing page
2. Fill in your details:
   - **Full Name** (optional but recommended)
   - **Username** (unique, cannot be changed later)
   - **Email** (for account recovery in future updates)
   - **Password** (minimum 6 characters)
3. Click **"Create Account"**
4. You'll be automatically logged in and redirected to your dashboard!

### Logging In

1. Click **"Log In"** on the landing page
2. Enter your **username** and **password**
3. Optional: Check "Remember me" to stay logged in
4. Click **"Log In"**

### Logging Out

- Click on your **avatar** (circle with your initial) in the top right
- Select **"Logout"** from the dropdown menu

---

## 🏠 Your Personal Dashboard

Once logged in, you have access to your personalized dashboard showing:

### Summary Cards
- **Total Income** - All your income transactions
- **Total Expenses** - All your spending
- **Current Balance** - Income minus expenses
- **Transaction Count** - Total number of transactions

### Interactive Charts
- **Spending by Category** - Pie chart showing expense breakdown
- **Income vs Expenses** - Bar chart comparison

### Recent Transactions
- View your last 10 transactions at a glance
- Quick access to add income or expenses

---

## 💰 Managing Transactions

### Adding Income
1. Click **"+ Add Income"** button
2. Fill in:
   - **Amount**: e.g., 3000
   - **Category**: e.g., Salary, Freelance, Investment
   - **Description**: e.g., Monthly salary payment
3. Click **"Add Transaction"**

### Adding Expenses
1. Click **"+ Add Expense"** button
2. Fill in:
   - **Amount**: e.g., 250
   - **Category**: e.g., Food, Transport, Bills
   - **Description**: e.g., Groceries for the week
3. Click **"Add Transaction"**

### Viewing All Transactions
- Go to **Transactions** page from the navigation
- See all your transactions in a detailed table
- Filter by date range using the date selectors
- Delete transactions with the 🗑️ icon

### Exporting Data
- Click **"Export CSV"** on the Transactions page
- Downloads your transactions as a spreadsheet
- File name: `transactions_[username].csv`

---

## 📊 Budget Management

### Setting Budgets
1. Navigate to **Budgets** page
2. Click **"+ Set Budget"**
3. Enter:
   - **Category**: e.g., Food, Transport
   - **Amount**: e.g., 500
   - **Period**: Weekly, Monthly, or Yearly
4. Click **"Set Budget"**

### Understanding Budget Status

#### 🟢 On Track (Green)
- You've used less than 80% of your budget
- Keep up the good work!

#### 🟡 Warning (Yellow)
- You've used 80-100% of your budget
- Time to be more careful with spending

#### 🔴 Over Budget (Red)
- You've exceeded your budget
- Review your spending in this category

### Budget Cards Show:
- **Budget Amount**: Total allocated
- **Spent**: Amount used so far
- **Remaining**: Budget left
- **Progress Bar**: Visual indicator
- **Percentage**: How much you've used

---

## 📈 Reports & Visualizations

Navigate to the **Reports** page to access:

### Available Charts
1. **Income vs Expenses** - Compare totals
2. **Expense Breakdown** - See where money goes
3. **Income Breakdown** - See income sources
4. **Spending Over Time** - Track trends
5. **Budget Progress** - Visual budget tracking
6. **Cumulative Balance** - Balance over time

### Generating Charts
- Click **"Generate All Charts"** to create/update all charts
- Click **"Refresh"** on individual charts to update specific ones
- Charts are saved as high-quality PNG images

### Category Summary Table
- View income and expenses by category
- See net results (income minus expenses)
- Identify your spending patterns

---

## ⚙️ Settings & Customization

Access your settings by clicking your avatar → **"Settings"**

### Profile Information
- **Full Name**: Update your display name
- **Email**: Change your email address
- **Username**: (Cannot be changed)

### Preferences
- **Theme**: Light, Dark, or Auto (future feature)
- **Currency**: USD, EUR, GBP, JPY
- **Budget Alert Threshold**: Set when to get warnings (default: 80%)

### Default Categories
- **Default Income Category**: Auto-fill for income (e.g., Salary)
- **Default Expense Category**: Auto-fill for expenses (e.g., Other)

### Account Information
View your:
- Member since date
- Last login time
- User ID

---

## 🔒 Security & Privacy Features

### Data Isolation
- Each user has completely separate data
- Your transactions and budgets are private
- No user can see another user's information

### Secure Authentication
- Passwords are hashed and encrypted
- Secure session management
- Login required for all financial data

### User-Specific Storage
```
data/users/[your-user-id]/
├── transactions.json    # Your transactions
└── budgets.json        # Your budgets
```

---

## 💡 Tips & Best Practices

### For Accurate Tracking
1. **Record Daily**: Add transactions as they happen
2. **Be Specific**: Use clear descriptions
3. **Consistent Categories**: Use the same category names
4. **Review Weekly**: Check reports every week

### Suggested Categories

#### Income Categories:
- Salary
- Freelance
- Investment
- Side Hustle
- Bonus
- Gift

#### Expense Categories:
- **Bills**: Rent, Utilities, Phone, Internet
- **Food**: Groceries, Dining, Coffee
- **Transport**: Gas, Public Transit, Uber, Parking
- **Entertainment**: Movies, Games, Hobbies, Subscriptions
- **Health**: Medical, Gym, Insurance, Pharmacy
- **Shopping**: Clothing, Electronics, Household
- **Education**: Courses, Books, Tuition
- **Personal**: Haircut, Cosmetics, Grooming

### Budget Setting Tips
1. Track spending for a month first
2. Set realistic budgets based on actual spending
3. Add 10-15% buffer for unexpected expenses
4. Review and adjust monthly

---

## 🎯 Use Cases & Scenarios

### Scenario 1: Monthly Salary Worker
1. Add salary as income at month start
2. Set budgets for all expense categories
3. Track daily expenses
4. Review budget status weekly
5. Export data at month end

### Scenario 2: Freelancer
1. Add income as projects are completed
2. Track business expenses separately
3. Use category breakdown to see profitability
4. Monitor cash flow with cumulative balance chart

### Scenario 3: Student
1. Add allowance/part-time income
2. Set strict budgets for entertainment
3. Track every small purchase
4. Use reports to identify savings opportunities

---

## 🔄 Multi-User Benefits

### Multiple People Can Use the Same System
- Each person creates their own account
- Completely separate financial data
- Share the same device/server
- Perfect for:
  - Roommates tracking individual expenses
  - Family members managing personal finances
  - Small businesses with multiple employees
  - Financial advisors managing client data

### Sharing & Collaboration
- Each user manages their own data
- No data mixing or confusion
- Secure and private

---

## 📱 Access from Multiple Devices

### Same Network
1. Find your computer's IP address
2. Open `http://[YOUR-IP]:5000` on other device
3. Log in with your credentials

### Tips
- Your data stays on the server
- Access from phone, tablet, or another computer
- All devices show the same data (synced)

---

## ⌨️ Keyboard Shortcuts

- **Esc**: Close modals/popups
- **Tab**: Navigate form fields
- **Enter**: Submit forms

---

## 🆘 Troubleshooting

### Can't Log In?
- Check username and password
- Username is case-sensitive
- Try resetting your password (future feature)

### Data Not Showing?
- Make sure you're logged in
- Refresh the page
- Check if transactions were added to your account

### Charts Not Generating?
- Ensure you have transactions
- Click "Generate All Charts"
- Wait a few seconds for processing

### Page Not Loading?
- Check if server is running
- Navigate to `http://localhost:5000`
- Restart the server if needed

---

## 🎨 Customization Options

### Coming Soon
- Dark mode theme
- Custom color schemes
- Configurable dashboard widgets
- Mobile app version
- Email notifications
- Export to PDF
- Recurring transactions
- Split transactions
- Multi-currency support

---

## 📊 Understanding Your Financial Health

### Green Flags (Good!)
- ✅ Positive balance
- ✅ All budgets on track
- ✅ Income > Expenses
- ✅ Consistent tracking

### Yellow Flags (Be Careful)
- ⚠️ Approaching budget limits
- ⚠️ Irregular income
- ⚠️ Increasing expenses trend

### Red Flags (Action Needed)
- 🚨 Negative balance
- 🚨 Multiple over-budget categories
- 🚨 Expenses > Income
- 🚨 Declining savings

---

## 🎓 Quick Start Checklist

- [ ] Create your account
- [ ] Add your first income
- [ ] Add a few expenses
- [ ] Set budgets for main categories
- [ ] Generate visualizations
- [ ] Review your spending
- [ ] Set up default categories
- [ ] Customize preferences
- [ ] Export your data

---

## 🎉 Congratulations!

You now have a fully functional, personalized finance tracker that will help you:
- Take control of your finances
- Understand spending patterns
- Stay within budgets
- Achieve financial goals

**Start tracking today and watch your financial health improve!** 💰📈

---

## 📞 Need Help?

- Check the tooltips in the app
- Review this guide
- Check the terminal for error messages
- Ensure all dependencies are installed

---

**Happy Tracking! 🚀**

*Your journey to financial freedom starts here!*

