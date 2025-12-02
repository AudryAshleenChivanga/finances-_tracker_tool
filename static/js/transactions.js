// Transactions Page JavaScript

let currentTransactionId = null;

// Load all transactions
async function loadTransactions(startDate = null, endDate = null) {
    try {
        let url = '/api/transactions';
        const params = new URLSearchParams();
        
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        
        if (params.toString()) {
            url += '?' + params.toString();
        }
        
        const data = await apiCall(url);
        displayTransactions(data.data);
    } catch (error) {
        showToast('Error loading transactions', 'error');
        console.error(error);
    }
}

// Display transactions in table
function displayTransactions(transactions) {
    const tbody = document.querySelector('#all-transactions tbody');
    
    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No transactions found</td></tr>';
        return;
    }
    
    tbody.innerHTML = transactions.map(t => `
        <tr>
            <td>${t.id}</td>
            <td>${formatDate(t.date)}</td>
            <td>${t.description}</td>
            <td>${t.category}</td>
            <td>
                <span class="badge badge-${t.type}">${t.type}</span>
            </td>
            <td class="amount-${t.type}">${formatCurrency(t.amount)}</td>
            <td>
                <button class="btn-icon" onclick="deleteTransaction(${t.id})" title="Delete">
                    🗑️
                </button>
            </td>
        </tr>
    `).join('');
}

// Apply filters
function applyFilters() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    loadTransactions(startDate, endDate);
}

// Clear filters
function clearFilters() {
    document.getElementById('start-date').value = '';
    document.getElementById('end-date').value = '';
    loadTransactions();
}

// Delete transaction
function deleteTransaction(id) {
    currentTransactionId = id;
    const modal = document.getElementById('delete-modal');
    modal.classList.add('active');
    modal.style.display = 'flex';
}

// Confirm delete
async function confirmDelete() {
    try {
        await apiCall(`/api/transactions/${currentTransactionId}`, {
            method: 'DELETE'
        });
        
        showToast('Transaction deleted successfully', 'success');
        closeDeleteModal();
        loadTransactions();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// Close delete modal
function closeDeleteModal() {
    const modal = document.getElementById('delete-modal');
    modal.classList.remove('active');
    modal.style.display = 'none';
    currentTransactionId = null;
}

// Export to CSV
async function exportCSV() {
    try {
        window.location.href = '/api/export';
        showToast('Export started...', 'info');
    } catch (error) {
        showToast('Error exporting data', 'error');
    }
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
        loadTransactions();
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Load transactions on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTransactions();
});

