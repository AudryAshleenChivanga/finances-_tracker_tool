// ChengeAI - AI Financial Advisor JavaScript

let chatHistory = [];
let userInitial = 'U';

// Send message to AI
async function sendMessage(message) {
    if (!message.trim()) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    document.getElementById('chat-input').value = '';
    
    // Hide welcome screen
    document.getElementById('chat-welcome').style.display = 'none';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Disable send button while processing
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    
    try {
        const response = await apiCall('/api/ai/chat', {
            method: 'POST',
            body: JSON.stringify({ 
                message: message,
                history: chatHistory.slice(-6) // Send last 6 exchanges for context
            })
        });
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add AI response
        if (response.success) {
            addMessage(response.response, 'ai');
            chatHistory.push({ user: message, ai: response.response });
            
            // Store in session storage for persistence during session
            sessionStorage.setItem('chengeai_history', JSON.stringify(chatHistory));
        } else {
            addMessage('Sorry, I encountered an error. Please try again.', 'ai');
        }
        
    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator();
        addMessage('Sorry, I\'m having trouble connecting. Please try again in a moment.', 'ai');
    }
    
    // Re-enable send button
    sendBtn.disabled = false;
    
    // Scroll to bottom
    scrollToBottom();
}

// Add message to chat
function addMessage(text, sender) {
    const messagesArea = document.getElementById('messages-area');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${sender}`;
    
    const avatarSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 2a10 10 0 1 0 10 10H12V2z"/>
        <circle cx="12" cy="12" r="3"/>
    </svg>`;
    
    if (sender === 'ai') {
        messageDiv.innerHTML = `
            <div class="message-avatar ai-avatar">${avatarSvg}</div>
            <div class="message-content">
                <div class="message-bubble">${formatMessage(text)}</div>
                <div class="message-time">${formatTime()}</div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-bubble">${escapeHtml(text)}</div>
                <div class="message-time">${formatTime()}</div>
            </div>
            <div class="message-avatar user-avatar-small">${userInitial}</div>
        `;
    }
    
    messagesArea.appendChild(messageDiv);
    
    // Add entrance animation
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(10px)';
    requestAnimationFrame(() => {
        messageDiv.style.transition = 'all 0.3s ease';
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
    });
}

// Format time
function formatTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format message with markdown-like styling
function formatMessage(text) {
    // Escape HTML first
    text = escapeHtml(text);
    
    // Bold text **text**
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic text *text*
    text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    // Line breaks
    text = text.replace(/\n/g, '<br>');
    
    // Bullet points
    text = text.replace(/^• (.*?)$/gm, '<li>$1</li>');
    text = text.replace(/^- (.*?)$/gm, '<li>$1</li>');
    
    // Numbered lists
    text = text.replace(/^\d+\. (.*?)$/gm, '<li>$1</li>');
    
    // Wrap consecutive list items in ul
    text = text.replace(/(<li>.*?<\/li>)(<br>)?(<li>)/g, '$1$3');
    text = text.replace(/(<li>.*?<\/li>)+/g, '<ul>$&</ul>');
    
    // Clean up any double breaks in lists
    text = text.replace(/<\/li><br><li>/g, '</li><li>');
    
    return text;
}

// Show typing indicator
function showTypingIndicator() {
    const messagesArea = document.getElementById('messages-area');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message message-ai typing-indicator';
    typingDiv.id = 'typing-indicator';
    
    const avatarSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 2a10 10 0 1 0 10 10H12V2z"/>
        <circle cx="12" cy="12" r="3"/>
    </svg>`;
    
    typingDiv.innerHTML = `
        <div class="message-avatar ai-avatar">${avatarSvg}</div>
        <div class="message-content">
            <div class="message-bubble typing-bubble">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    messagesArea.appendChild(typingDiv);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    const messagesArea = document.getElementById('messages-area');
    messagesArea.scrollTo({
        top: messagesArea.scrollHeight,
        behavior: 'smooth'
    });
}

// Clear chat
function clearChat() {
    if (confirm('Clear chat history?')) {
        document.getElementById('messages-area').innerHTML = '';
        document.getElementById('chat-welcome').style.display = 'flex';
        chatHistory = [];
        sessionStorage.removeItem('chengeai_history');
        showToast('Chat cleared', 'info');
    }
}

// Ask pre-defined question
function askQuestion(question) {
    document.getElementById('chat-input').value = question;
    sendMessage(question);
}

// Handle form submission
document.getElementById('chat-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = document.getElementById('chat-input').value;
    sendMessage(message);
});

// Handle enter key (without shift for new line)
document.getElementById('chat-input')?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const message = e.target.value;
        if (message.trim()) {
            sendMessage(message);
        }
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Get user initial for avatar
    try {
        const userInfo = await apiCall('/api/user/info');
        userInitial = (userInfo.data.full_name || userInfo.data.username || 'U').charAt(0).toUpperCase();
    } catch (error) {
        console.log('Could not load user info');
    }
    
    // Restore chat history from session storage
    const savedHistory = sessionStorage.getItem('chengeai_history');
    if (savedHistory) {
        try {
            chatHistory = JSON.parse(savedHistory);
            if (chatHistory.length > 0) {
                document.getElementById('chat-welcome').style.display = 'none';
                chatHistory.forEach(msg => {
                    addMessage(msg.user, 'user');
                    addMessage(msg.ai, 'ai');
                });
                scrollToBottom();
            }
        } catch (e) {
            console.log('Could not restore chat history');
        }
    }
    
    // Focus on input
    document.getElementById('chat-input')?.focus();
});
