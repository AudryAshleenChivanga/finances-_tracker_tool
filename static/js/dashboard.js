// Dashboard JavaScript

let categoryChart = null;
let comparisonChart = null;

// Load dashboard data
async function loadDashboard() {
    try {
        // Load summary
        const summaryData = await apiCall('/api/summary');
        updateSummaryCards(summaryData.data);
        
        // Load recent transactions and stats
        const statsData = await apiCall('/api/stats/recent');
        updateRecentTransactions(statsData.data.recent_transactions);
        updateCharts(summaryData.data, statsData.data.expense_by_category);
    } catch (error) {
        showToast('Error loading dashboard data', 'error');
        console.error(error);
    }
}

// Update summary cards
function updateSummaryCards(data) {
    document.getElementById('total-income').textContent = formatCurrency(data.total_income);
    document.getElementById('total-expenses').textContent = formatCurrency(data.total_expenses);
    document.getElementById('current-balance').textContent = formatCurrency(data.balance);
    document.getElementById('transaction-count').textContent = data.transaction_count;
    
    // Update balance color
    const balanceElement = document.getElementById('current-balance');
    if (data.balance >= 0) {
        balanceElement.style.color = 'var(--success-color)';
    } else {
        balanceElement.style.color = 'var(--danger-color)';
    }
}

// Update recent transactions table
function updateRecentTransactions(transactions) {
    const tbody = document.querySelector('#recent-transactions tbody');
    
    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">No transactions yet</td></tr>';
        return;
    }
    
    tbody.innerHTML = transactions.map(t => `
        <tr>
            <td>${formatDate(t.date)}</td>
            <td>${t.description}</td>
            <td>${t.category}</td>
            <td>
                <span class="badge badge-${t.type}">${t.type}</span>
            </td>
            <td class="amount-${t.type}">${formatCurrency(t.amount)}</td>
        </tr>
    `).join('');
}

// Update charts
function updateCharts(summary, expenseByCategory) {
    // Category Pie Chart
    const categoryCtx = document.getElementById('category-chart').getContext('2d');
    
    if (categoryChart) {
        categoryChart.destroy();
    }
    
    const categories = Object.keys(expenseByCategory);
    const amounts = Object.values(expenseByCategory);
    
    if (categories.length > 0) {
        categoryChart = new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: categories,
                datasets: [{
                    data: amounts,
                    backgroundColor: [
                        '#ef4444', '#f59e0b', '#10b981', '#3b82f6', 
                        '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Income vs Expenses Bar Chart
    const comparisonCtx = document.getElementById('comparison-chart').getContext('2d');
    
    if (comparisonChart) {
        comparisonChart.destroy();
    }
    
    comparisonChart = new Chart(comparisonCtx, {
        type: 'bar',
        data: {
            labels: ['Income', 'Expenses'],
            datasets: [{
                label: 'Amount',
                data: [summary.total_income, summary.total_expenses],
                backgroundColor: ['#10b981', '#ef4444']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// Handle add transaction form
document.getElementById('add-transaction-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        amount: parseFloat(document.getElementById('amount').value),
        category: document.getElementById('category').value,
        description: document.getElementById('description').value,
        type: document.getElementById('transaction-type').value
    };
    
    try {
        await apiCall('/api/transactions', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        showToast('Transaction added successfully!', 'success');
        closeModal();
        loadDashboard(); // Reload data
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Load data on page load
document.addEventListener('DOMContentLoaded', loadDashboard);

