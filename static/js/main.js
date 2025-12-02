// Main JavaScript Utilities

// Toast Notification System
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// API Call Helper
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'An error occurred');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Modal Functions
function closeModal() {
    const modal = document.getElementById('add-transaction-modal');
    if (modal) {
        modal.classList.remove('active');
        modal.style.display = 'none';
    }
}

function showAddTransactionModal(type) {
    const modal = document.getElementById('add-transaction-modal');
    const title = document.getElementById('modal-title');
    const typeInput = document.getElementById('transaction-type');
    const form = document.getElementById('add-transaction-form');
    
    if (modal && title && typeInput) {
        title.textContent = type === 'income' ? 'Add Income' : 'Add Expense';
        typeInput.value = type;
        form.reset();
        
        modal.classList.add('active');
        modal.style.display = 'flex';
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.classList.remove('active');
            modal.style.display = 'none';
        }
    });
};

// Apply theme
function applyTheme(theme) {
    const body = document.body;
    
    // Remove existing theme classes
    body.classList.remove('theme-light', 'theme-dark');
    
    if (theme === 'dark') {
        body.classList.add('theme-dark');
    } else if (theme === 'light') {
        body.classList.add('theme-light');
    } else if (theme === 'auto') {
        // Check system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        body.classList.add(prefersDark ? 'theme-dark' : 'theme-light');
    }
}

// Load and apply user theme
async function loadUserTheme() {
    try {
        const data = await apiCall('/api/user/info');
        if (data.success && data.data.theme) {
            applyTheme(data.data.theme);
        }
    } catch (error) {
        // User not logged in or error, use default
        console.log('Using default theme');
    }
}

// Active navigation link
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = 'var(--primary-color)';
            link.style.fontWeight = '600';
        }
    });
    
    // Load user theme
    loadUserTheme();
});

