// Budgets Page JavaScript

let currentBudgetCategory = null;

// Load all budgets
async function loadBudgets() {
    try {
        const data = await apiCall('/api/budgets');
        displayBudgets(data.data);
    } catch (error) {
        showToast('Error loading budgets', 'error');
        console.error(error);
    }
}

// Display budgets
function displayBudgets(budgets) {
    const container = document.getElementById('budgets-container');
    const emptyState = document.getElementById('empty-state');
    
    if (budgets.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    container.innerHTML = budgets.map(budget => {
        const percentage = Math.min(budget.percentage_used, 100);
        const progressClass = budget.status === 'over' ? 'progress-over' : 
                             budget.status === 'warning' ? 'progress-warning' : 'progress-good';
        const statusClass = budget.status === 'over' ? 'status-over' : 
                           budget.status === 'warning' ? 'status-warning' : 'status-good';
        const statusText = budget.status === 'over' ? 'Over Budget' : 
                          budget.status === 'warning' ? 'Warning' : 'On Track';
        
        return `
            <div class="budget-card">
                <div class="budget-header">
                    <div>
                        <div class="budget-category">${budget.category}</div>
                        <div class="budget-period">${budget.period}</div>
                    </div>
                    <button class="btn-icon" onclick="deleteBudget('${budget.category}')" title="Delete">
                        🗑️
                    </button>
                </div>
                
                <div class="budget-amounts">
                    <div class="budget-row">
                        <span class="budget-label">Budget</span>
                        <span class="budget-value">${formatCurrency(budget.budget)}</span>
                    </div>
                    <div class="budget-row">
                        <span class="budget-label">Spent</span>
                        <span class="budget-value">${formatCurrency(budget.spent)}</span>
                    </div>
                    <div class="budget-row">
                        <span class="budget-label">Remaining</span>
                        <span class="budget-value" style="color: ${budget.remaining >= 0 ? 'var(--success-color)' : 'var(--danger-color)'}">
                            ${formatCurrency(budget.remaining)}
                        </span>
                    </div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill ${progressClass}" style="width: ${percentage}%"></div>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="budget-status ${statusClass}">${statusText}</span>
                    <span style="font-weight: 600; color: var(--text-secondary);">${percentage.toFixed(1)}%</span>
                </div>
            </div>
        `;
    }).join('');
}

// Show set budget modal
function showSetBudgetModal() {
    const modal = document.getElementById('set-budget-modal');
    modal.classList.add('active');
    modal.style.display = 'flex';
}

// Close budget modal
function closeBudgetModal() {
    const modal = document.getElementById('set-budget-modal');
    modal.classList.remove('active');
    modal.style.display = 'none';
    document.getElementById('set-budget-form').reset();
}

// Handle set budget form
document.getElementById('set-budget-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        category: document.getElementById('budget-category').value,
        amount: parseFloat(document.getElementById('budget-amount').value),
        period: document.getElementById('budget-period').value
    };
    
    try {
        await apiCall('/api/budgets', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        showToast('Budget set successfully!', 'success');
        closeBudgetModal();
        loadBudgets();
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Delete budget
function deleteBudget(category) {
    currentBudgetCategory = category;
    const modal = document.getElementById('delete-budget-modal');
    modal.classList.add('active');
    modal.style.display = 'flex';
}

// Confirm delete budget
async function confirmDeleteBudget() {
    try {
        await apiCall(`/api/budgets/${encodeURIComponent(currentBudgetCategory)}`, {
            method: 'DELETE'
        });
        
        showToast('Budget deleted successfully', 'success');
        closeDeleteBudgetModal();
        loadBudgets();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// Close delete budget modal
function closeDeleteBudgetModal() {
    const modal = document.getElementById('delete-budget-modal');
    modal.classList.remove('active');
    modal.style.display = 'none';
    currentBudgetCategory = null;
}

// Load budgets on page load
document.addEventListener('DOMContentLoaded', () => {
    loadBudgets();
});

