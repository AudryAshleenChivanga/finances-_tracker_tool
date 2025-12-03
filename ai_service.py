"""
AI Service for ChengeAI - Financial Advisor
Integrates with OpenAI API for intelligent financial advice.
Falls back to rule-based system if API key not configured.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI package not installed. Using rule-based AI advisor.")


class ChengeAI:
    """AI-powered financial advisor for Chengeta."""
    
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.client = None
        self.use_openai = False
        
        if OPENAI_AVAILABLE and self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.use_openai = True
                print("OpenAI integration enabled.")
            except Exception as e:
                print(f"Failed to initialize OpenAI: {e}")
                self.use_openai = False
    
    def get_system_prompt(self, user_data):
        """Generate system prompt with user's financial context."""
        return f"""You are ChengeAI, a friendly and knowledgeable personal financial advisor built into the Chengeta finance tracking app.

Your role:
- Provide practical, actionable financial advice
- Be encouraging and supportive
- Give personalized recommendations based on the user's data
- Explain financial concepts in simple terms
- Never give specific investment advice (like "buy stock X")
- Recommend consulting a professional for complex situations

User's Financial Summary:
- Total Income: ${user_data.get('total_income', 0):,.2f}
- Total Expenses: ${user_data.get('total_expenses', 0):,.2f}
- Current Balance: ${user_data.get('balance', 0):,.2f}
- Number of Transactions: {user_data.get('transaction_count', 0)}

Top Expense Categories:
{self._format_categories(user_data.get('top_categories', []))}

Guidelines:
1. Keep responses concise but helpful (2-4 paragraphs max)
2. Use bullet points for lists
3. Include specific numbers from their data when relevant
4. End with an actionable next step or question
5. Be positive and motivating
6. Format key points in bold using **text**"""

    def _format_categories(self, categories):
        """Format expense categories for the prompt."""
        if not categories:
            return "No expense data yet"
        
        lines = []
        for cat in categories[:5]:
            lines.append(f"- {cat['category']}: ${cat['amount']:,.2f}")
        return "\n".join(lines) if lines else "No expense data yet"

    def chat(self, message, user_data, conversation_history=None):
        """
        Process a chat message and return AI response.
        
        Args:
            message: User's message
            user_data: Dictionary with user's financial data
            conversation_history: List of previous messages (optional)
        
        Returns:
            dict: Response with 'success' and 'response' keys
        """
        try:
            if self.use_openai:
                return self._openai_response(message, user_data, conversation_history)
            else:
                return self._rule_based_response(message, user_data)
        except Exception as e:
            print(f"AI chat error: {e}")
            return {
                'success': False,
                'response': "I'm having trouble processing your request. Please try again.",
                'error': str(e)
            }

    def _openai_response(self, message, user_data, conversation_history=None):
        """Generate response using OpenAI API."""
        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt(user_data)}
            ]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-6:]:  # Keep last 6 messages for context
                    messages.append({"role": "user", "content": msg.get('user', '')})
                    messages.append({"role": "assistant", "content": msg.get('ai', '')})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                'success': True,
                'response': ai_response,
                'source': 'openai'
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fall back to rule-based response
            return self._rule_based_response(message, user_data)

    def _rule_based_response(self, message, user_data):
        """Generate response using rule-based system (fallback)."""
        message_lower = message.lower()
        
        balance = user_data.get('balance', 0)
        total_income = user_data.get('total_income', 0)
        total_expenses = user_data.get('total_expenses', 0)
        
        # Determine response based on keywords
        if any(word in message_lower for word in ['save', 'saving', 'savings']):
            response = self._saving_advice(balance, total_income, total_expenses)
        elif any(word in message_lower for word in ['budget', 'budgeting', 'spending plan']):
            response = self._budget_advice(total_income, total_expenses)
        elif any(word in message_lower for word in ['debt', 'loan', 'credit card', 'owe', 'pay off']):
            response = self._debt_advice()
        elif any(word in message_lower for word in ['invest', 'investment', 'stock', 'portfolio', 'grow']):
            response = self._investment_advice(balance)
        elif any(word in message_lower for word in ['emergency', 'fund', 'rainy day', 'unexpected']):
            response = self._emergency_fund_advice(total_expenses)
        elif any(word in message_lower for word in ['retirement', 'retire', '401k', 'ira', 'pension', 'future']):
            response = self._retirement_advice()
        elif any(word in message_lower for word in ['income', 'earn', 'salary', 'side hustle', 'more money']):
            response = self._income_advice()
        elif any(word in message_lower for word in ['spend', 'spending', 'expense', 'cut', 'reduce']):
            response = self._spending_advice(user_data.get('top_categories', []))
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'help', 'what can you']):
            response = self._welcome_message(balance, total_income, total_expenses)
        elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            response = "You're welcome! I'm here to help you achieve your financial goals. Feel free to ask me anything else about saving, budgeting, investing, or any other financial topic!"
        else:
            response = self._general_advice(balance, total_income, total_expenses)
        
        return {
            'success': True,
            'response': response,
            'source': 'rule-based'
        }

    def _saving_advice(self, balance, total_income, total_expenses):
        """Generate saving advice."""
        savings_rate = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
        
        return f"""Great question about saving! Here's what I see from your finances:

**Your Current Situation:**
- Balance: **${balance:,.2f}**
- Savings Rate: **{savings_rate:.1f}%** of income

**Top Saving Strategies:**

• **Automate your savings** - Set up automatic transfers to a savings account on payday. Even $50/month adds up to $600/year!

• **Follow the 50/30/20 rule** - Allocate 50% to needs, 30% to wants, and 20% to savings

• **Cut subscription waste** - Review your recurring charges and cancel unused services

• **Use the 24-hour rule** - Wait a day before any purchase over $50 to avoid impulse buying

{"Your savings rate is great! Keep it up!" if savings_rate >= 20 else "Aim to boost your savings rate to at least 20% for healthy finances."}

What specific area would you like to save more in?"""

    def _budget_advice(self, total_income, total_expenses):
        """Generate budgeting advice."""
        expense_ratio = (total_expenses / total_income * 100) if total_income > 0 else 0
        
        return f"""Let's optimize your budget! Here's your overview:

**Your Numbers:**
- Total Income: **${total_income:,.2f}**
- Total Expenses: **${total_expenses:,.2f}**
- You're spending **{expense_ratio:.1f}%** of your income

**Effective Budgeting Tips:**

• **Zero-based budgeting** - Give every dollar a job before the month starts

• **Track daily** - Use Chengeta to log expenses as they happen (it takes 30 seconds!)

• **Review weekly** - Check your budget every Sunday to stay on track

• **Build in flexibility** - Include a "miscellaneous" category for unexpected small expenses

• **Celebrate wins** - When you stay under budget, reward yourself (within reason!)

{"You're in great shape with spending!" if expense_ratio < 80 else "Consider reviewing your expenses to find areas to cut back."}

Would you like tips on any specific budget category?"""

    def _debt_advice(self):
        """Generate debt management advice."""
        return """Taking control of debt is one of the best financial moves you can make! Here's how:

**Debt Payoff Strategies:**

• **Debt Avalanche** - Pay minimums on all debts, then throw extra money at the highest interest rate first. Saves the most money!

• **Debt Snowball** - Pay off smallest balances first for quick wins and motivation

• **Balance Transfer** - Move high-interest credit card debt to a 0% APR card (watch for fees)

**Action Steps:**

1. List all your debts with balances and interest rates
2. Always pay at least the minimum on everything
3. Put any extra money toward your target debt
4. Consider negotiating lower interest rates with creditors
5. Avoid taking on new debt while paying off existing debt

**Remember:** Being debt-free is achievable! Many people have paid off tens of thousands of dollars. You can do this!

What type of debt are you working on paying off?"""

    def _investment_advice(self, balance):
        """Generate investment advice."""
        return f"""Smart thinking about growing your wealth! Here's a beginner-friendly guide:

**Before You Invest:**
- Build an emergency fund (3-6 months expenses)
- Pay off high-interest debt first
- Your current balance: **${balance:,.2f}**

**Investment Basics:**

• **Start with retirement accounts** - 401(k) and IRA offer tax advantages

• **Index funds are your friend** - Low fees, instant diversification, great for beginners

• **Dollar-cost averaging** - Invest a fixed amount regularly regardless of market conditions

• **Think long-term** - Time in the market beats timing the market

**Key Principles:**

1. Only invest money you won't need for 5+ years
2. Diversify across different asset types
3. Keep fees low (under 0.5% if possible)
4. Don't panic during market dips
5. Increase contributions with each raise

**Note:** I provide general education, not specific investment advice. Consider consulting a financial advisor for personalized recommendations.

What aspect of investing would you like to learn more about?"""

    def _emergency_fund_advice(self, total_expenses):
        """Generate emergency fund advice."""
        monthly_expenses = total_expenses / 12 if total_expenses > 0 else 2000
        target_min = monthly_expenses * 3
        target_max = monthly_expenses * 6
        
        return f"""Building an emergency fund is crucial for financial security! Here's your guide:

**Your Target:**
- Minimum goal: **${target_min:,.2f}** (3 months expenses)
- Ideal goal: **${target_max:,.2f}** (6 months expenses)

**How to Build It:**

• **Start small** - Even $500 provides a safety net for minor emergencies

• **Automate transfers** - Set up weekly or bi-weekly automatic transfers

• **Use windfalls** - Tax refunds, bonuses, and gifts can boost your fund quickly

• **Keep it separate** - Use a high-yield savings account to earn interest while keeping it accessible

**What Counts as Emergency:**

✓ Job loss / reduced income
✓ Medical emergencies
✓ Major car repairs
✓ Home repairs
✗ Sales or "deals"
✗ Vacations
✗ Non-urgent purchases

**Pro Tip:** Start with a goal of $1,000, then build to 3 months, then 6 months. Breaking it into milestones makes it achievable!

How far along are you with your emergency fund?"""

    def _retirement_advice(self):
        """Generate retirement planning advice."""
        return """Planning for retirement early is one of the best gifts you can give yourself! Here's what to know:

**The Power of Starting Early:**
- Starting at 25 vs 35 can mean **2x more** at retirement (thanks to compound interest!)

**Accounts to Consider:**

• **401(k)** - Always get the employer match (it's free money!)

• **Roth IRA** - Pay taxes now, withdraw tax-free in retirement. Great if you expect higher taxes later

• **Traditional IRA** - Tax deduction now, pay taxes when you withdraw

• **HSA** - Triple tax advantage if you have a high-deductible health plan

**How Much to Save:**

- 20s: Aim for 10-15% of income
- 30s: Aim for 15-20% of income  
- 40s+: Aim for 20-25% of income

**Quick Math:**
- Rule of 25: You need ~25x your annual expenses
- 4% Rule: Withdraw 4% per year in retirement

**Action Steps:**

1. Calculate your retirement number
2. Max out employer 401(k) match
3. Open a Roth IRA
4. Increase contributions with each raise
5. Check your investments annually

What's your biggest retirement planning question?"""

    def _income_advice(self):
        """Generate income growth advice."""
        return """Looking to boost your income? That's a powerful wealth-building strategy! Here are proven methods:

**At Your Current Job:**

• **Ask for a raise** - Document your achievements, research market rates, and make your case

• **Seek promotions** - Take on visible projects and develop leadership skills

• **Learn new skills** - Certifications and training can lead to higher pay

**Side Hustle Ideas:**

• **Freelancing** - Writing, design, programming, consulting
• **Teaching/Tutoring** - Online or in-person
• **Gig economy** - Delivery, rideshare, task services
• **Selling** - Handmade items, reselling, digital products
• **Content creation** - YouTube, blogging, podcasting

**Passive Income (Takes Time to Build):**

• Dividend stocks
• Rental properties
• Online courses
• Affiliate marketing
• Digital products

**Quick Wins:**

1. Negotiate salary at your next job offer (10-20% more!)
2. Sell unused items around your home
3. Take on overtime or extra shifts
4. Monetize a hobby or skill

**Remember:** Track all income in Chengeta to see your progress!

What income-boosting strategy interests you most?"""

    def _spending_advice(self, top_categories):
        """Generate spending analysis advice."""
        categories_text = ""
        if top_categories:
            categories_text = "\n**Your Top Spending Categories:**\n"
            for cat in top_categories[:5]:
                categories_text += f"• {cat['category']}: ${cat['amount']:,.2f}\n"
        
        return f"""Let's analyze your spending and find opportunities to save!
{categories_text}
**Smart Spending Strategies:**

• **Track everything** - Awareness is the first step to control

• **Wait before buying** - Use a 24-48 hour rule for non-essentials

• **Compare prices** - Use apps and browser extensions to find deals

• **Question subscriptions** - Cancel what you don't use regularly

• **Cook more** - Eating out is typically 3-5x more expensive

**Common Money Leaks:**

1. Unused subscriptions and memberships
2. Bank fees and late payment fees
3. Impulse purchases
4. Brand premiums when generic works fine
5. Convenience charges (delivery, ATM fees)

**Challenge:** Try a "no-spend weekend" once a month and put the savings toward your goals!

Would you like specific tips for any spending category?"""

    def _welcome_message(self, balance, total_income, total_expenses):
        """Generate welcome/help message."""
        return f"""Hello! I'm ChengeAI, your personal financial advisor. I'm here to help you build a healthier financial future!

**Your Financial Snapshot:**
- Balance: **${balance:,.2f}**
- Total Income: **${total_income:,.2f}**
- Total Expenses: **${total_expenses:,.2f}**

**I can help you with:**

• **Saving money** - Tips and strategies to grow your savings
• **Budgeting** - Create and stick to a spending plan
• **Debt management** - Strategies to become debt-free
• **Investing basics** - Understand how to grow your wealth
• **Emergency funds** - Build financial security
• **Retirement planning** - Prepare for the future
• **Income growth** - Ideas to earn more money

**Just ask me questions like:**
- "How can I save more money?"
- "What's a good budget strategy?"
- "How do I start investing?"
- "Help me reduce my spending"

What would you like to work on today?"""

    def _general_advice(self, balance, total_income, total_expenses):
        """Generate general financial advice."""
        savings_rate = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
        
        return f"""Great question! Let me share some insights based on your finances:

**Your Overview:**
- Current Balance: **${balance:,.2f}**
- Savings Rate: **{savings_rate:.1f}%**

**Key Financial Principles:**

1. **Pay yourself first** - Save before you spend, not what's left over

2. **Live below your means** - The gap between income and spending is where wealth is built

3. **Avoid lifestyle inflation** - When income goes up, savings should too

4. **Compound interest is magic** - Start early and let time work for you

5. **Track everything** - What gets measured gets managed

**Your Next Steps:**

• Review your biggest expense categories
• Set up automatic savings transfers
• Build or strengthen your emergency fund
• Consider your retirement contributions

Would you like specific advice on saving, budgeting, investing, or debt management? Just ask!"""


# Create singleton instance
ai_advisor = ChengeAI()


def get_ai_response(message, user_data, conversation_history=None):
    """
    Convenience function to get AI response.
    
    Args:
        message: User's message
        user_data: Dictionary with user's financial data
        conversation_history: Optional list of previous messages
    
    Returns:
        dict: Response with 'success' and 'response' keys
    """
    return ai_advisor.chat(message, user_data, conversation_history)

