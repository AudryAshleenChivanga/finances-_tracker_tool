// ChengeAI - AI Financial Advisor JavaScript

let chatHistory = [];

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
    
    try {
        const response = await apiCall('/api/ai/chat', {
            method: 'POST',
            body: JSON.stringify({ message: message })
        });
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add AI response
        if (response.success) {
            addMessage(response.response, 'ai');
            chatHistory.push({ user: message, ai: response.response });
        } else {
            addMessage('Sorry, I encountered an error. Please try again.', 'ai');
        }
        
    } catch (error) {
        removeTypingIndicator();
        addMessage('Sorry, I\'m having trouble connecting. Please try again.', 'ai');
    }
    
    // Scroll to bottom
    scrollToBottom();
}

// Add message to chat
function addMessage(text, sender) {
    const messagesArea = document.getElementById('messages-area');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${sender}`;
    
    if (sender === 'ai') {
        messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="message-bubble">${formatMessage(text)}</div>
                <div class="message-time">${new Date().toLocaleTimeString()}</div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-bubble">${text}</div>
                <div class="message-time">${new Date().toLocaleTimeString()}</div>
            </div>
            <div class="message-avatar user-avatar-small">${document.getElementById('chat-input').dataset.userInitial || 'U'}</div>
        `;
    }
    
    messagesArea.appendChild(messageDiv);
}

// Format message with markdown-like styling
function formatMessage(text) {
    // Bold text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Line breaks
    text = text.replace(/\n/g, '<br>');
    
    // Bullet points
    text = text.replace(/^- (.*?)$/gm, '<li>$1</li>');
    
    // Wrap lists
    if (text.includes('<li>')) {
        text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }
    
    return text;
}

// Show typing indicator
function showTypingIndicator() {
    const messagesArea = document.getElementById('messages-area');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message message-ai typing-indicator';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-bubble">
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
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

// Clear chat
function clearChat() {
    if (confirm('Clear chat history?')) {
        document.getElementById('messages-area').innerHTML = '';
        document.getElementById('chat-welcome').style.display = 'block';
        chatHistory = [];
        showToast('Chat cleared', 'info');
    }
}

// Ask pre-defined question
function askQuestion(question) {
    document.getElementById('chat-input').value = question;
    document.getElementById('chat-form').dispatchEvent(new Event('submit'));
}

// Handle form submission
document.getElementById('chat-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = document.getElementById('chat-input').value;
    sendMessage(message);
});

// Get user initial for avatar
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const userInfo = await apiCall('/api/user/info');
        const initial = (userInfo.data.full_name || userInfo.data.username).charAt(0).toUpperCase();
        document.getElementById('chat-input').dataset.userInitial = initial;
    } catch (error) {
        console.log('Could not load user info');
    }
});

