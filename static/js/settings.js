// Settings Page JavaScript

// Load user info
async function loadUserInfo() {
    try {
        const data = await apiCall('/api/user/info');
        const user = data.data;
        
        // Populate profile form
        document.getElementById('full_name').value = user.full_name || '';
        document.getElementById('username').value = user.username;
        document.getElementById('email').value = user.email;
        
        // Load profile picture
        if (user.profile_picture) {
            const img = document.getElementById('profile-picture-img');
            const initial = document.getElementById('profile-initial');
            img.src = `/uploads/profiles/${user.profile_picture}`;
            img.style.display = 'block';
            initial.style.display = 'none';
            document.getElementById('remove-picture-btn').style.display = 'inline-block';
        } else {
            const initial = document.getElementById('profile-initial');
            initial.textContent = (user.full_name || user.username).charAt(0).toUpperCase();
        }
        
        // Populate preferences
        document.getElementById('theme').value = user.theme;
        document.getElementById('currency').value = user.currency;
        document.getElementById('budget_alert_threshold').value = user.budget_alert_threshold;
        
        // Apply current theme
        applyTheme(user.theme);
        
        // Populate categories
        document.getElementById('default_income_category').value = user.default_income_category;
        document.getElementById('default_expense_category').value = user.default_expense_category;
        
        // Populate account info
        document.getElementById('created_at').textContent = new Date(user.created_at).toLocaleDateString();
        document.getElementById('last_login').textContent = user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never';
        document.getElementById('user_id').textContent = user.id;
        
    } catch (error) {
        showToast('Error loading user information', 'error');
    }
}

// Apply theme to page
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

// Handle profile picture upload
document.getElementById('profile-picture-input')?.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    
    if (!file) return;
    
    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        showToast('File size must be less than 5MB', 'error');
        return;
    }
    
    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'];
    if (!validTypes.includes(file.type)) {
        showToast('Please upload a valid image file (PNG, JPG, GIF, or WEBP)', 'error');
        return;
    }
    
    try {
        // Show progress
        const progressContainer = document.getElementById('upload-progress');
        const progressBar = document.getElementById('upload-progress-bar');
        const progressText = document.getElementById('upload-progress-text');
        
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        progressText.textContent = 'Uploading...';
        
        // Create form data
        const formData = new FormData();
        formData.append('profile_picture', file);
        
        // Upload with progress
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressBar.style.width = percentComplete + '%';
                progressText.textContent = `Uploading... ${Math.round(percentComplete)}%`;
            }
        });
        
        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                
                // Update preview
                const img = document.getElementById('profile-picture-img');
                const initial = document.getElementById('profile-initial');
                
                img.src = response.data.url + '?t=' + Date.now();
                img.style.display = 'block';
                initial.style.display = 'none';
                
                // Show remove button
                document.getElementById('remove-picture-btn').style.display = 'inline-block';
                
                progressContainer.style.display = 'none';
                showToast('Profile picture updated successfully!', 'success');
            } else {
                const error = JSON.parse(xhr.responseText);
                progressContainer.style.display = 'none';
                showToast(error.message || 'Upload failed', 'error');
            }
        });
        
        xhr.addEventListener('error', () => {
            progressContainer.style.display = 'none';
            showToast('Upload failed. Please try again.', 'error');
        });
        
        xhr.open('POST', '/api/user/upload-picture');
        xhr.send(formData);
        
    } catch (error) {
        showToast('Error uploading image', 'error');
        document.getElementById('upload-progress').style.display = 'none';
    }
});

// Handle remove profile picture
document.getElementById('remove-picture-btn')?.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to remove your profile picture?')) {
        return;
    }
    
    try {
        await apiCall('/api/user/remove-picture', {
            method: 'DELETE'
        });
        
        // Reset preview
        const img = document.getElementById('profile-picture-img');
        const initial = document.getElementById('profile-initial');
        
        img.style.display = 'none';
        initial.style.display = 'flex';
        
        // Hide remove button
        document.getElementById('remove-picture-btn').style.display = 'none';
        
        showToast('Profile picture removed', 'success');
    } catch (error) {
        showToast('Error removing picture', 'error');
    }
});

// Handle profile form submission
document.getElementById('profile-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        full_name: document.getElementById('full_name').value,
        email: document.getElementById('email').value
    };
    
    try {
        await apiCall('/settings', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        showToast('Profile updated successfully!', 'success');
        
        // Update user name in navigation
        setTimeout(() => location.reload(), 1000);
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Handle preferences form submission
document.getElementById('preferences-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const theme = document.getElementById('theme').value;
    
    const formData = {
        theme: theme,
        currency: document.getElementById('currency').value,
        budget_alert_threshold: parseInt(document.getElementById('budget_alert_threshold').value)
    };
    
    try {
        await apiCall('/settings', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        // Apply theme immediately
        applyTheme(theme);
        
        showToast('Preferences updated successfully!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Handle categories form submission
document.getElementById('categories-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        default_income_category: document.getElementById('default_income_category').value,
        default_expense_category: document.getElementById('default_expense_category').value
    };
    
    try {
        await apiCall('/settings', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        showToast('Default categories updated successfully!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    }
});

// Load data on page load
document.addEventListener('DOMContentLoaded', loadUserInfo);
