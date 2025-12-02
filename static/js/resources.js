// Financial Resources Library JavaScript

// Resources database
const resources = {
    audiobooks: [
        {
            id: 1,
            title: "Rich Dad Poor Dad",
            author: "Robert Kiyosaki",
            category: "mindset",
            duration: "6h 9m",
            rating: 4.8,
            description: "Learn what the rich teach their kids about money that the poor and middle class do not.",
            topics: ["Financial Education", "Assets vs Liabilities", "Money Mindset"],
            level: "Beginner",
            featured: true
        },
        {
            id: 2,
            title: "The Total Money Makeover",
            author: "Dave Ramsey",
            category: "debt",
            duration: "3h 41m",
            rating: 4.7,
            description: "A proven plan for financial fitness. Get out of debt and build wealth.",
            topics: ["Debt Freedom", "Emergency Fund", "7 Baby Steps"],
            level: "Beginner",
            featured: true
        },
        {
            id: 3,
            title: "Think and Grow Rich",
            author: "Napoleon Hill",
            category: "mindset",
            duration: "10h 12m",
            rating: 4.9,
            description: "The classic success book that has influenced millions of successful people.",
            topics: ["Success Principles", "Wealth Building", "Mental Attitude"],
            level: "All Levels",
            featured: false
        },
        {
            id: 4,
            title: "The Intelligent Investor",
            author: "Benjamin Graham",
            category: "investing",
            duration: "15h 5m",
            rating: 4.8,
            description: "The definitive book on value investing. A must-read for serious investors.",
            topics: ["Value Investing", "Stock Market", "Long-term Strategy"],
            level: "Intermediate",
            featured: true
        },
        {
            id: 5,
            title: "Your Money or Your Life",
            author: "Vicki Robin",
            category: "savings",
            duration: "11h 32m",
            rating: 4.6,
            description: "Transform your relationship with money and achieve financial independence.",
            topics: ["Financial Independence", "Life Energy", "FIRE Movement"],
            level: "All Levels",
            featured: false
        },
        {
            id: 6,
            title: "I Will Teach You to Be Rich",
            author: "Ramit Sethi",
            category: "budgeting",
            duration: "12h 57m",
            rating: 4.7,
            description: "No-guilt, practical approach to managing your money in your 20s and 30s.",
            topics: ["Automation", "Conscious Spending", "Investing"],
            level: "Beginner",
            featured: false
        }
    ],
    
    videos: [
        {
            id: 101,
            title: "Personal Finance 101: Complete Beginner's Guide",
            channel: "Khan Academy",
            category: "budgeting",
            duration: "45:23",
            rating: 4.9,
            description: "Master the fundamentals of personal finance from budgeting to investing.",
            topics: ["Budgeting Basics", "Saving", "Debt", "Credit"],
            level: "Beginner",
            featured: true,
            thumbnail: "https://via.placeholder.com/300x200/10b981/ffffff?text=Personal+Finance+101"
        },
        {
            id: 102,
            title: "How to Invest for Beginners",
            channel: "Graham Stephan",
            category: "investing",
            duration: "32:15",
            rating: 4.8,
            description: "Step-by-step guide to start investing even with little money.",
            topics: ["Index Funds", "Stock Market", "Retirement Accounts"],
            level: "Beginner",
            featured: true,
            thumbnail: "https://via.placeholder.com/300x200/0891b2/ffffff?text=Investing+for+Beginners"
        },
        {
            id: 103,
            title: "Debt Freedom Journey: Pay Off $100K",
            channel: "The Financial Diet",
            category: "debt",
            duration: "28:47",
            rating: 4.7,
            description: "Real story of paying off massive debt and practical strategies you can use.",
            topics: ["Debt Snowball", "Budget Cutting", "Income Increase"],
            level: "All Levels",
            featured: false,
            thumbnail: "https://via.placeholder.com/300x200/22c55e/ffffff?text=Debt+Freedom"
        },
        {
            id: 104,
            title: "Building Wealth in Your 20s and 30s",
            channel: "Minority Mindset",
            category: "savings",
            duration: "41:19",
            rating: 4.8,
            description: "Essential wealth-building strategies for young adults.",
            topics: ["Compound Interest", "Asset Building", "Side Hustles"],
            level: "Beginner",
            featured: true,
            thumbnail: "https://via.placeholder.com/300x200/3b82f6/ffffff?text=Building+Wealth"
        },
        {
            id: 105,
            title: "The Psychology of Money",
            channel: "Morgan Housel",
            category: "mindset",
            duration: "52:34",
            rating: 4.9,
            description: "Understanding how emotions and psychology impact your financial decisions.",
            topics: ["Money Mindset", "Behavioral Finance", "Decision Making"],
            level: "All Levels",
            featured: false,
            thumbnail: "https://via.placeholder.com/300x200/8b5cf6/ffffff?text=Psychology+of+Money"
        },
        {
            id: 106,
            title: "Passive Income: 7 Proven Strategies",
            channel: "Andrei Jikh",
            category: "entrepreneurship",
            duration: "36:42",
            rating: 4.7,
            description: "Learn how to create passive income streams and achieve financial freedom.",
            topics: ["Passive Income", "Real Estate", "Dividends", "Online Business"],
            level: "Intermediate",
            featured: false,
            thumbnail: "https://via.placeholder.com/300x200/ec4899/ffffff?text=Passive+Income"
        }
    ]
};

// Load resources
function loadResources() {
    loadFeatured();
    loadAudiobooks();
    loadVideos();
}

// Load featured resources
function loadFeatured() {
    const featured = [
        ...resources.audiobooks.filter(r => r.featured),
        ...resources.videos.filter(r => r.featured)
    ];
    
    const grid = document.getElementById('featured-grid');
    grid.innerHTML = featured.map(resource => createResourceCard(resource)).join('');
}

// Load audiobooks
function loadAudiobooks() {
    const grid = document.getElementById('audiobooks-grid');
    grid.innerHTML = resources.audiobooks.map(book => createAudiobookCard(book)).join('');
}

// Load videos
function loadVideos() {
    const grid = document.getElementById('videos-grid');
    grid.innerHTML = resources.videos.map(video => createVideoCard(video)).join('');
}

// Create resource card
function createResourceCard(resource) {
    const isVideo = resource.id > 100;
    const icon = isVideo ? '🎥' : '📖';
    const type = isVideo ? 'Video' : 'Audiobook';
    
    return `
        <div class="resource-card" onclick="openResource(${resource.id}, '${isVideo ? 'video' : 'audiobook'}')">
            ${resource.thumbnail ? `<img src="${resource.thumbnail}" alt="${resource.title}" class="resource-thumbnail">` : ''}
            <div class="resource-info">
                <div class="resource-type">${icon} ${type}</div>
                <h3 class="resource-title">${resource.title}</h3>
                <p class="resource-author">${resource.author || resource.channel}</p>
                <div class="resource-meta">
                    <span class="meta-item">⏱️ ${resource.duration}</span>
                    <span class="meta-item">⭐ ${resource.rating}</span>
                    <span class="meta-badge">${resource.level}</span>
                </div>
            </div>
        </div>
    `;
}

// Create audiobook card
function createAudiobookCard(book) {
    return `
        <div class="resource-card" onclick="openResource(${book.id}, 'audiobook')">
            <div class="audiobook-cover">
                <div class="audiobook-icon">📖</div>
                <div class="audiobook-badge">${book.level}</div>
            </div>
            <div class="resource-info">
                <h3 class="resource-title">${book.title}</h3>
                <p class="resource-author">by ${book.author}</p>
                <p class="resource-description">${book.description}</p>
                <div class="resource-meta">
                    <span class="meta-item">⏱️ ${book.duration}</span>
                    <span class="meta-item">⭐ ${book.rating}</span>
                </div>
                <div class="resource-topics">
                    ${book.topics.map(topic => `<span class="topic-tag">${topic}</span>`).join('')}
                </div>
            </div>
        </div>
    `;
}

// Create video card
function createVideoCard(video) {
    return `
        <div class="resource-card video-card" onclick="openResource(${video.id}, 'video')">
            <div class="video-thumbnail">
                <img src="${video.thumbnail}" alt="${video.title}">
                <div class="play-overlay">
                    <div class="play-button">▶</div>
                </div>
                <div class="video-duration">${video.duration}</div>
            </div>
            <div class="resource-info">
                <h3 class="resource-title">${video.title}</h3>
                <p class="resource-author">${video.channel}</p>
                <p class="resource-description">${video.description}</p>
                <div class="resource-meta">
                    <span class="meta-item">⭐ ${video.rating}</span>
                    <span class="meta-badge">${video.level}</span>
                </div>
            </div>
        </div>
    `;
}

// Filter resources
function filterResources(type) {
    const sections = document.querySelectorAll('.resource-section');
    const tabs = document.querySelectorAll('.filter-tab');
    
    // Update active tab
    tabs.forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    if (type === 'all') {
        sections.forEach(section => section.style.display = 'block');
    } else {
        sections.forEach(section => {
            if (section.dataset.category === type) {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        });
    }
}

// Filter by topic
function filterByTopic(topic) {
    // This would filter resources by topic
    showToast(`Showing ${topic} resources`, 'info');
    // Implementation for filtering
}

// Open resource detail
function openResource(id, type) {
    const resource = type === 'video' 
        ? resources.videos.find(v => v.id === id)
        : resources.audiobooks.find(b => b.id === id);
    
    if (!resource) return;
    
    const modal = document.getElementById('resource-modal');
    const detail = document.getElementById('resource-detail');
    
    detail.innerHTML = `
        <div class="resource-detail-content">
            ${resource.thumbnail ? `<img src="${resource.thumbnail}" class="detail-thumbnail">` : ''}
            <h3>${resource.title}</h3>
            <p class="detail-author">${resource.author || resource.channel}</p>
            <div class="detail-meta">
                <span>⏱️ ${resource.duration}</span>
                <span>⭐ ${resource.rating}/5.0</span>
                <span>${resource.level}</span>
            </div>
            <p class="detail-description">${resource.description}</p>
            <div class="detail-topics">
                <strong>Topics Covered:</strong><br>
                ${resource.topics.map(t => `<span class="topic-tag">${t}</span>`).join('')}
            </div>
            <div class="detail-actions">
                <button class="btn btn-primary" onclick="startLearning('${resource.title}')">
                    Start Learning
                </button>
                <button class="btn btn-secondary" onclick="saveForLater(${id})">
                    Save for Later
                </button>
            </div>
        </div>
    `;
    
    modal.classList.add('active');
    modal.style.display = 'flex';
}

// Close resource modal
function closeResourceModal() {
    const modal = document.getElementById('resource-modal');
    modal.classList.remove('active');
    modal.style.display = 'none';
}

// Start learning
function startLearning(title) {
    showToast(`Opening ${title}...`, 'info');
    // This would open the actual resource
}

// Save for later
function saveForLater(id) {
    showToast('Saved to your library!', 'success');
    // This would save to user's saved list
}

// Load resources on page load
document.addEventListener('DOMContentLoaded', loadResources);

