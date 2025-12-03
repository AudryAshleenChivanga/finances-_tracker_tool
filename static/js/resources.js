// Financial Resources Library JavaScript
// Automatically fetches finance videos from YouTube API

let resources = { videos: [] };
let isLoading = false;

// Load resources on page load
document.addEventListener('DOMContentLoaded', () => {
    loadVideosFromAPI();
});

// Fetch videos from backend API
async function loadVideosFromAPI(forceRefresh = false) {
    if (isLoading) return;
    isLoading = true;
    
    // Show loading state
    showLoadingState();
    
    try {
        const url = forceRefresh 
            ? '/api/resources/videos?refresh=true' 
            : '/api/resources/videos';
            
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success && data.videos.length > 0) {
            resources.videos = data.videos;
            console.log(`Loaded ${data.count} videos`);
        } else {
            // Use fallback videos if API fails
            console.log('Using fallback videos');
            resources.videos = getDefaultVideos();
        }
        
        // Render the videos
        loadResources();
        
    } catch (error) {
        console.error('Error fetching videos:', error);
        // Use fallback videos
        resources.videos = getDefaultVideos();
        loadResources();
    } finally {
        isLoading = false;
        hideLoadingState();
    }
}

// Show loading spinner
function showLoadingState() {
    const featuredGrid = document.getElementById('featured-grid');
    const videosGrid = document.getElementById('videos-grid');
    
    const loadingHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading finance videos...</p>
        </div>
    `;
    
    if (featuredGrid) featuredGrid.innerHTML = loadingHTML;
    if (videosGrid) videosGrid.innerHTML = loadingHTML;
}

// Hide loading spinner
function hideLoadingState() {
    // Loading state is replaced when videos are rendered
}

// Load resources into the page
function loadResources() {
    loadFeatured();
    loadAllVideos();
}

// Load featured resources
function loadFeatured() {
    const featured = resources.videos.filter(r => r.featured);
    const grid = document.getElementById('featured-grid');
    if (grid) {
        if (featured.length > 0) {
            grid.innerHTML = featured.map(video => createVideoCard(video)).join('');
        } else {
            grid.innerHTML = '<p class="no-results">No featured videos available</p>';
        }
    }
}

// Load all videos
function loadAllVideos() {
    const grid = document.getElementById('videos-grid');
    if (grid) {
        if (resources.videos.length > 0) {
            grid.innerHTML = resources.videos.map(video => createVideoCard(video)).join('');
        } else {
            grid.innerHTML = '<p class="no-results">No videos available</p>';
        }
    }
}

// Get YouTube thumbnail URL
function getYouTubeThumbnail(videoId) {
    return `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
}

// Create video card
function createVideoCard(video) {
    const thumbnail = video.youtubeId ? getYouTubeThumbnail(video.youtubeId) : (video.thumbnail || '');
    const duration = video.duration || '';
    const rating = video.rating || 4.5;
    const level = video.level || 'All Levels';
    
    return `
        <div class="resource-card video-card" onclick="openResource(${video.id})">
            <div class="video-thumbnail">
                <img src="${thumbnail}" alt="${video.title}" onerror="this.style.display='none'">
                <div class="play-overlay">
                    <div class="play-button">▶</div>
                </div>
                ${duration ? `<div class="video-duration">${duration}</div>` : ''}
            </div>
            <div class="resource-info">
                <h3 class="resource-title">${video.title}</h3>
                <p class="resource-author">${video.channel}</p>
                <p class="resource-description">${video.description}</p>
                <div class="resource-meta">
                    <span class="meta-item">⭐ ${rating}</span>
                    <span class="meta-badge">${level}</span>
                </div>
            </div>
        </div>
    `;
}

// Filter resources by category
function filterResources(type) {
    const tabs = document.querySelectorAll('.filter-tab');
    const featuredSection = document.querySelector('.featured-section');
    const videosGrid = document.getElementById('videos-grid');
    
    // Update active tab
    tabs.forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    if (type === 'all') {
        if (featuredSection) featuredSection.style.display = 'block';
        videosGrid.innerHTML = resources.videos.map(video => createVideoCard(video)).join('');
    } else {
        if (featuredSection) featuredSection.style.display = 'none';
        const filtered = resources.videos.filter(v => v.category === type);
        videosGrid.innerHTML = filtered.length > 0 
            ? filtered.map(video => createVideoCard(video)).join('')
            : '<p class="no-results">No videos found for this category</p>';
    }
}

// Filter by topic
function filterByTopic(topic) {
    const filtered = resources.videos.filter(v => 
        v.category === topic || 
        (v.topics && v.topics.some(t => t.toLowerCase().includes(topic.toLowerCase())))
    );
    
    // Show toast with filter info
    if (typeof showToast === 'function') {
        showToast(`Found ${filtered.length} resources on ${topic}`, 'info');
    }
    
    const videosGrid = document.getElementById('videos-grid');
    if (videosGrid) {
        videosGrid.innerHTML = filtered.length > 0
            ? filtered.map(video => createVideoCard(video)).join('')
            : '<p class="no-results">No videos found for this topic</p>';
    }
    
    // Hide featured section when filtering
    const featuredSection = document.querySelector('.featured-section');
    if (featuredSection) featuredSection.style.display = 'none';
    
    // Update tabs
    const tabs = document.querySelectorAll('.filter-tab');
    tabs.forEach(tab => tab.classList.remove('active'));
}

// Open resource detail with embedded player
function openResource(id) {
    const resource = resources.videos.find(v => v.id === id);
    
    if (!resource) return;
    
    const modal = document.getElementById('resource-modal');
    const detail = document.getElementById('resource-detail');
    const titleEl = document.getElementById('resource-title');
    
    if (titleEl) {
        titleEl.textContent = resource.title;
    }
    
    // Create embedded YouTube player
    const playerHTML = resource.youtubeId ? `
        <div class="video-player-container">
            <iframe 
                id="youtube-player"
                src="https://www.youtube.com/embed/${resource.youtubeId}?rel=0&modestbranding=1&autoplay=0"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>
        </div>
    ` : '';
    
    const topics = resource.topics || ['Personal Finance'];
    
    detail.innerHTML = `
        <div class="resource-detail-content">
            ${playerHTML}
            <div class="resource-detail-info">
                <div class="detail-header">
                    <span class="detail-type video">🎥 Video</span>
                    <span class="detail-level">${resource.level || 'All Levels'}</span>
                </div>
                <p class="detail-author">${resource.channel}</p>
                <div class="detail-meta">
                    <span>⏱️ ${resource.duration || 'N/A'}</span>
                    <span>⭐ ${resource.rating || 4.5}/5.0</span>
                </div>
                <p class="detail-description">${resource.description}</p>
                <div class="detail-topics">
                    <strong>Topics Covered:</strong>
                    <div class="topics-list">
                        ${topics.map(t => `<span class="topic-tag">${t}</span>`).join('')}
                    </div>
                </div>
                <div class="detail-actions">
                    ${resource.youtubeId ? `
                        <a href="https://www.youtube.com/watch?v=${resource.youtubeId}" 
                           target="_blank" 
                           class="btn btn-primary">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/>
                            </svg>
                            Watch on YouTube
                        </a>
                    ` : ''}
                    <button class="btn btn-secondary" onclick="saveForLater(${id})">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                        </svg>
                        Save for Later
                    </button>
                </div>
            </div>
        </div>
    `;
    
    modal.classList.add('active');
    modal.style.display = 'flex';
}

// Close resource modal and stop any playing content
function closeResourceModal() {
    const modal = document.getElementById('resource-modal');
    
    // Stop YouTube video by removing iframe src
    const iframe = document.getElementById('youtube-player');
    if (iframe) {
        iframe.src = '';
    }
    
    modal.classList.remove('active');
    modal.style.display = 'none';
}

// Save for later
function saveForLater(id) {
    let saved = JSON.parse(localStorage.getItem('savedResources') || '[]');
    
    if (!saved.includes(id)) {
        saved.push(id);
        localStorage.setItem('savedResources', JSON.stringify(saved));
        if (typeof showToast === 'function') {
            showToast('Saved to your library!', 'success');
        }
    } else {
        if (typeof showToast === 'function') {
            showToast('Already in your library', 'info');
        }
    }
}

// Refresh videos from YouTube
function refreshVideos() {
    if (typeof showToast === 'function') {
        showToast('Refreshing videos from YouTube...', 'info');
    }
    loadVideosFromAPI(true);
}

// Reset filters
function resetFilters() {
    loadResources();
    const featuredSection = document.querySelector('.featured-section');
    if (featuredSection) featuredSection.style.display = 'block';
    
    const tabs = document.querySelectorAll('.filter-tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
        if (tab.textContent.includes('All')) {
            tab.classList.add('active');
        }
    });
}

// Close modal on escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeResourceModal();
    }
});

// Close modal on outside click
document.addEventListener('click', function(e) {
    const modal = document.getElementById('resource-modal');
    if (e.target === modal) {
        closeResourceModal();
    }
});

// Default/fallback videos when API is unavailable
function getDefaultVideos() {
    return [
        {
            id: 1,
            title: "How To Manage Your Money (50/30/20 Rule)",
            channel: "Nischa",
            category: "budgeting",
            duration: "10:14",
            rating: 4.9,
            description: "Master the 50/30/20 budgeting rule to take control of your finances.",
            topics: ["Budgeting", "50/30/20 Rule", "Money Management"],
            level: "Beginner",
            featured: true,
            youtubeId: "HQzoZfc3GwQ"
        },
        {
            id: 2,
            title: "Stock Market For Beginners",
            channel: "ClearValue Tax",
            category: "investing",
            duration: "36:12",
            rating: 4.8,
            description: "Complete beginner's guide to investing in the stock market.",
            topics: ["Stocks", "Investing Basics", "Stock Market"],
            level: "Beginner",
            featured: true,
            youtubeId: "p7HKvqRI_Bo"
        },
        {
            id: 3,
            title: "Dave Ramsey's 7 Baby Steps",
            channel: "The Ramsey Show",
            category: "debt",
            duration: "14:23",
            rating: 4.8,
            description: "Learn Dave Ramsey's proven 7-step plan to get out of debt.",
            topics: ["Debt Freedom", "Baby Steps", "Financial Peace"],
            level: "Beginner",
            featured: true,
            youtubeId: "2bLkBLxKrVg"
        },
        {
            id: 4,
            title: "How To Create A Budget",
            channel: "Rachel Cruze",
            category: "budgeting",
            duration: "8:45",
            rating: 4.7,
            description: "Step-by-step guide to creating a budget you'll stick to.",
            topics: ["Budgeting", "Zero-Based Budget", "Money Plan"],
            level: "Beginner",
            featured: false,
            youtubeId: "sVKQn2I4HDM"
        },
        {
            id: 5,
            title: "Index Funds Explained",
            channel: "Two Cents",
            category: "investing",
            duration: "8:56",
            rating: 4.8,
            description: "Everything you need to know about index fund investing.",
            topics: ["Index Funds", "Passive Investing", "S&P 500"],
            level: "Beginner",
            featured: true,
            youtubeId: "fwe-PjrX23o"
        },
        {
            id: 6,
            title: "Build An Emergency Fund",
            channel: "The Financial Diet",
            category: "savings",
            duration: "11:28",
            rating: 4.7,
            description: "Practical tips to build your emergency fund quickly.",
            topics: ["Emergency Fund", "Savings", "Financial Security"],
            level: "Beginner",
            featured: true,
            youtubeId: "vZyeeVnja78"
        },
        {
            id: 7,
            title: "Roth IRA Explained",
            channel: "Humphrey Yang",
            category: "retirement",
            duration: "9:52",
            rating: 4.9,
            description: "Complete guide to Roth IRA retirement accounts.",
            topics: ["Roth IRA", "Retirement", "Tax-Free Growth"],
            level: "Beginner",
            featured: false,
            youtubeId: "vn3-EWs1Yfs"
        },
        {
            id: 8,
            title: "How To Pay Off Debt Fast",
            channel: "Graham Stephan",
            category: "debt",
            duration: "15:47",
            rating: 4.8,
            description: "Strategies to pay off debt and save on interest.",
            topics: ["Debt Payoff", "Debt Snowball", "Financial Freedom"],
            level: "All Levels",
            featured: false,
            youtubeId: "mJCfLPftTKA"
        },
        {
            id: 9,
            title: "Credit Score Explained",
            channel: "Two Cents",
            category: "debt",
            duration: "7:23",
            rating: 4.8,
            description: "Understand how credit scores work and improve yours.",
            topics: ["Credit Score", "FICO", "Credit Building"],
            level: "Beginner",
            featured: false,
            youtubeId: "DP6XSqV2VZs"
        },
        {
            id: 10,
            title: "Compound Interest Explained",
            channel: "The Plain Bagel",
            category: "investing",
            duration: "8:56",
            rating: 4.9,
            description: "How compound interest works and why it's powerful.",
            topics: ["Compound Interest", "Investing", "Wealth Building"],
            level: "Beginner",
            featured: false,
            youtubeId: "wf91rEGw88Q"
        },
        {
            id: 11,
            title: "Start Investing With Little Money",
            channel: "Andrei Jikh",
            category: "investing",
            duration: "18:34",
            rating: 4.8,
            description: "Start investing even if you only have $100.",
            topics: ["Investing", "Beginners", "Small Amounts"],
            level: "Beginner",
            featured: true,
            youtubeId: "gFQNPmLKj1k"
        },
        {
            id: 12,
            title: "401k Explained",
            channel: "Two Cents",
            category: "retirement",
            duration: "3:42",
            rating: 4.7,
            description: "Quick explanation of 401k retirement accounts.",
            topics: ["401k", "Retirement", "Employer Match"],
            level: "Beginner",
            featured: false,
            youtubeId: "5MIR_gKLN0s"
        }
    ];
}
