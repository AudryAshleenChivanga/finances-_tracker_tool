// Reports Page JavaScript

// Load category summary
async function loadCategorySummary() {
    try {
        const data = await apiCall('/api/categories');
        displayCategorySummary(data.data);
    } catch (error) {
        showToast('Error loading category summary', 'error');
        console.error(error);
    }
}

// Display category summary
function displayCategorySummary(categories) {
    const tbody = document.querySelector('#category-summary-table tbody');
    
    if (categories.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center">No data available</td></tr>';
        return;
    }
    
    tbody.innerHTML = categories.map(cat => `
        <tr>
            <td>${cat.name}</td>
            <td style="color: var(--success-color); font-weight: 600;">${formatCurrency(cat.income)}</td>
            <td style="color: var(--danger-color); font-weight: 600;">${formatCurrency(cat.expense)}</td>
            <td style="color: ${cat.net >= 0 ? 'var(--success-color)' : 'var(--danger-color)'}; font-weight: 600;">
                ${formatCurrency(cat.net)}
            </td>
        </tr>
    `).join('');
}

// Generate a specific chart
async function generateChart(chartName) {
    try {
        showToast('Generating chart...', 'info');
        
        await apiCall('/api/charts/generate', {
            method: 'POST'
        });
        
        // Reload the specific chart with cache busting
        const img = document.getElementById(`chart-${chartName.replace('_', '-')}`);
        if (img) {
            img.src = `/api/charts/${chartName}?t=${Date.now()}`;
        }
        
        showToast('Chart generated successfully!', 'success');
    } catch (error) {
        showToast('Error generating chart', 'error');
        console.error(error);
    }
}

// Generate all charts
async function generateAllCharts() {
    try {
        showToast('Generating all charts...', 'info');
        
        await apiCall('/api/charts/generate', {
            method: 'POST'
        });
        
        // Reload all chart images with cache busting
        const timestamp = Date.now();
        const chartImages = [
            'income_vs_expenses',
            'expense_breakdown',
            'income_breakdown',
            'spending_over_time',
            'budget_progress',
            'cumulative_balance'
        ];
        
        chartImages.forEach(chartName => {
            const img = document.getElementById(`chart-${chartName.replace('_', '-')}`);
            if (img) {
                img.src = `/api/charts/${chartName}?t=${timestamp}`;
            }
        });
        
        showToast('All charts generated successfully!', 'success');
    } catch (error) {
        showToast('Error generating charts', 'error');
        console.error(error);
    }
}

// Add cache busting to chart images on load
function setupChartImages() {
    const chartImages = document.querySelectorAll('.chart-container img');
    chartImages.forEach(img => {
        // Add timestamp to initial load
        if (!img.src.includes('?t=')) {
            img.src = img.src + '?t=' + Date.now();
        }
    });
}

// Load data on page load
document.addEventListener('DOMContentLoaded', () => {
    loadCategorySummary();
    setupChartImages();
});

