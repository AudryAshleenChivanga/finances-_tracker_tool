/**
 * Chengeta Marketplace JavaScript
 * Handles filtering, click tracking, and analytics
 */

document.addEventListener('DOMContentLoaded', function() {
    initTabs();
    loadClickStats();
});

/**
 * Initialize category tabs
 */
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Filter services
            const category = this.dataset.category;
            filterServices(category);
        });
    });
}

/**
 * Filter services by category
 */
function filterServices(category) {
    const cards = document.querySelectorAll('.service-card');
    
    cards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.classList.remove('hidden');
            // Animate in
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.3s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 50);
        } else {
            card.classList.add('hidden');
        }
    });
}

/**
 * Track affiliate link clicks
 */
function trackClick(partnerId, category) {
    // Show toast
    showTrackingToast();
    
    // Send tracking data to backend
    fetch('/api/marketplace/track', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            partner_id: partnerId,
            category: category,
            timestamp: new Date().toISOString()
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Click tracked:', data);
        // Here you would redirect to the affiliate link
        // window.location.href = data.affiliate_url;
    })
    .catch(error => {
        console.error('Error tracking click:', error);
    });
    
    // Simulate redirect delay for demo
    setTimeout(() => {
        // In production, redirect to actual affiliate URL
        showNotification(`Opening ${partnerId} partner page...`, 'info');
    }, 1500);
}

/**
 * Show tracking toast notification
 */
function showTrackingToast() {
    const toast = document.getElementById('trackingToast');
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}

/**
 * Load click statistics (for admin dashboard)
 */
function loadClickStats() {
    // This would fetch stats from the backend
    // For now, we'll just log that it's ready
    console.log('Marketplace loaded and ready for tracking');
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'success') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            ${type === 'success' ? 
                '<path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>' :
                '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>'
            }
        </svg>
        <span>${message}</span>
    `;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        bottom: '5rem',
        left: '50%',
        transform: 'translateX(-50%)',
        background: type === 'success' ? '#00d4aa' : '#1a1a2e',
        color: '#fff',
        padding: '1rem 1.5rem',
        borderRadius: '12px',
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
        boxShadow: '0 10px 40px rgba(0, 0, 0, 0.2)',
        zIndex: '1001',
        animation: 'slideUp 0.3s ease'
    });
    
    document.body.appendChild(notification);
    
    // Remove after delay
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(-50%) translateY(20px)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
`;
document.head.appendChild(style);

/**
 * Search services
 */
function searchServices(query) {
    const cards = document.querySelectorAll('.service-card');
    const searchLower = query.toLowerCase();
    
    cards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('.description').textContent.toLowerCase();
        const provider = card.querySelector('.provider').textContent.toLowerCase();
        
        if (title.includes(searchLower) || 
            description.includes(searchLower) || 
            provider.includes(searchLower)) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
}

/**
 * Sort services by rating
 */
function sortByRating() {
    const grid = document.getElementById('servicesGrid');
    const cards = Array.from(grid.querySelectorAll('.service-card'));
    
    cards.sort((a, b) => {
        const ratingA = parseFloat(a.querySelector('.rating-text').textContent.match(/[\d.]+/)[0]);
        const ratingB = parseFloat(b.querySelector('.rating-text').textContent.match(/[\d.]+/)[0]);
        return ratingB - ratingA;
    });
    
    cards.forEach(card => grid.appendChild(card));
}

/**
 * Course enrollment handler
 */
function enrollCourse(courseId, price) {
    // In production, this would open a payment modal
    showNotification(`Starting enrollment for course (${courseId})...`, 'info');
    
    // Track the enrollment attempt
    fetch('/api/marketplace/track', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            partner_id: courseId,
            category: 'courses',
            action: 'enroll_attempt',
            price: price,
            timestamp: new Date().toISOString()
        })
    });
}

