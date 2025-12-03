"""
YouTube Service for Chengeta Resources
Automatically fetches finance education videos from YouTube.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, '.env')

# Load .env from the project directory
load_dotenv(ENV_PATH)

# YouTube Data API configuration
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

# Debug: Print API key status
print(f"YouTube API Key loaded: {'Yes' if YOUTUBE_API_KEY else 'No'}")
if YOUTUBE_API_KEY:
    print(f"API Key (first 10 chars): {YOUTUBE_API_KEY[:10]}...")

# Cache file to store fetched videos (reduces API calls)
CACHE_FILE = "data/youtube_cache.json"
CACHE_DURATION_HOURS = 24  # Refresh cache every 24 hours

# Finance-related search queries
FINANCE_SEARCHES = [
    "personal finance tips for beginners",
    "how to budget money",
    "investing for beginners 2024",
    "how to save money fast",
    "get out of debt strategies",
    "retirement planning basics",
    "credit score explained",
    "passive income ideas",
    "financial freedom tips",
    "money management skills"
]

# Trusted finance YouTube channels (channel IDs)
TRUSTED_CHANNELS = {
    "UCL8w_A8p8P1HWI3k6PR5Z6w": "Graham Stephan",
    "UC4a-Gbdw7vOaccHmFo40b9g": "Dave Ramsey",
    "UCGy7SkBjcIAgTiwkXEtPnYg": "Andrei Jikh",
    "UCnMn36GT_H0X-w5_ckLtlgQ": "The Financial Diet",
    "UCFCEuCsyWP0YkP3CZ3Mr01Q": "The Plain Bagel",
    "UCbta5YJJqHkMqRoIMBDpPGQ": "Humphrey Yang",
    "UC9ToMd6X_lgeC2KwC0mzRgQ": "Two Cents",
    "UCZR87-fsjZvDH1S2LGFoRHQ": "Nischa",
    "UCYkHwJW6Cx8qUjUt-k8A7Zw": "Rachel Cruze",
    "UCKMtY6cfrgXjAPBKHhf-TrA": "Marko WhiteBoard Finance"
}


def get_cached_videos():
    """Load videos from cache if valid."""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
                
            # Check if cache is still valid
            cached_time = datetime.fromisoformat(cache.get('timestamp', '2000-01-01'))
            if datetime.now() - cached_time < timedelta(hours=CACHE_DURATION_HOURS):
                return cache.get('videos', [])
    except Exception as e:
        print(f"Cache read error: {e}")
    
    return None


def save_to_cache(videos):
    """Save videos to cache file."""
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        cache = {
            'timestamp': datetime.now().isoformat(),
            'videos': videos
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"Cache write error: {e}")


def search_youtube_videos(query, max_results=5):
    """Search YouTube for videos matching query."""
    if not YOUTUBE_API_KEY:
        return []
    
    try:
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': max_results,
            'order': 'relevance',
            'videoDuration': 'medium',  # 4-20 minutes
            'safeSearch': 'strict',
            'key': YOUTUBE_API_KEY
        }
        
        response = requests.get(f"{YOUTUBE_API_URL}/search", params=params)
        response.raise_for_status()
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            video = {
                'youtubeId': item['id']['videoId'],
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'publishedAt': item['snippet']['publishedAt']
            }
            videos.append(video)
        
        return videos
    
    except Exception as e:
        print(f"YouTube search error: {e}")
        return []


def get_video_details(video_ids):
    """Get detailed information for specific videos."""
    if not YOUTUBE_API_KEY or not video_ids:
        return []
    
    try:
        params = {
            'part': 'snippet,contentDetails,statistics',
            'id': ','.join(video_ids),
            'key': YOUTUBE_API_KEY
        }
        
        response = requests.get(f"{YOUTUBE_API_URL}/videos", params=params)
        response.raise_for_status()
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            # Parse duration (ISO 8601 format)
            duration = parse_duration(item['contentDetails']['duration'])
            
            # Get view count for rating approximation
            views = int(item['statistics'].get('viewCount', 0))
            likes = int(item['statistics'].get('likeCount', 0))
            rating = calculate_rating(views, likes)
            
            video = {
                'youtubeId': item['id'],
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                'duration': duration,
                'rating': rating,
                'views': views
            }
            videos.append(video)
        
        return videos
    
    except Exception as e:
        print(f"YouTube details error: {e}")
        return []


def parse_duration(iso_duration):
    """Convert ISO 8601 duration to readable format."""
    import re
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    return "Unknown"


def calculate_rating(views, likes):
    """Calculate approximate rating based on engagement."""
    if views == 0:
        return 4.0
    
    # Simple engagement ratio
    ratio = likes / views if views > 0 else 0
    
    # Convert to 5-star rating (typical good ratio is 3-5%)
    if ratio >= 0.05:
        return 4.9
    elif ratio >= 0.04:
        return 4.8
    elif ratio >= 0.03:
        return 4.7
    elif ratio >= 0.02:
        return 4.5
    else:
        return 4.3


def categorize_video(title, description):
    """Auto-categorize video based on content."""
    text = (title + ' ' + description).lower()
    
    if any(word in text for word in ['budget', 'budgeting', '50/30/20', 'spending']):
        return 'budgeting'
    elif any(word in text for word in ['invest', 'stock', 'etf', 'index fund', 'portfolio']):
        return 'investing'
    elif any(word in text for word in ['save', 'saving', 'emergency fund', 'frugal']):
        return 'savings'
    elif any(word in text for word in ['debt', 'credit', 'loan', 'pay off', 'payoff']):
        return 'debt'
    elif any(word in text for word in ['retire', '401k', 'ira', 'pension']):
        return 'retirement'
    elif any(word in text for word in ['mindset', 'wealth', 'rich', 'millionaire', 'financial freedom']):
        return 'mindset'
    else:
        return 'general'


def determine_level(title, description):
    """Determine difficulty level of content."""
    text = (title + ' ' + description).lower()
    
    if any(word in text for word in ['beginner', 'basic', 'simple', 'easy', 'start', '101', 'introduction']):
        return 'Beginner'
    elif any(word in text for word in ['advanced', 'expert', 'complex', 'strategy']):
        return 'Advanced'
    else:
        return 'All Levels'


def extract_topics(title, description):
    """Extract relevant topics from video."""
    text = (title + ' ' + description).lower()
    topics = []
    
    topic_keywords = {
        'Budgeting': ['budget', 'budgeting', 'spending plan'],
        'Investing': ['invest', 'investing', 'investment'],
        'Saving': ['save', 'saving', 'savings'],
        'Debt': ['debt', 'loan', 'credit card'],
        'Retirement': ['retire', 'retirement', '401k', 'ira'],
        'Credit Score': ['credit score', 'fico', 'credit report'],
        'Emergency Fund': ['emergency fund', 'rainy day'],
        'Index Funds': ['index fund', 's&p 500', 'vanguard'],
        'Stocks': ['stock', 'shares', 'equity'],
        'Real Estate': ['real estate', 'property', 'rental'],
        'Side Hustle': ['side hustle', 'extra income', 'gig'],
        'Passive Income': ['passive income', 'dividend'],
        'Frugal Living': ['frugal', 'minimalist', 'save money'],
        'Financial Freedom': ['financial freedom', 'fire', 'independence']
    }
    
    for topic, keywords in topic_keywords.items():
        if any(kw in text for kw in keywords):
            topics.append(topic)
    
    return topics[:3] if topics else ['Personal Finance']


def fetch_finance_videos(force_refresh=False):
    """
    Fetch finance education videos from YouTube.
    Uses cache to minimize API calls.
    """
    print(f"=== fetch_finance_videos called (force_refresh={force_refresh}) ===")
    print(f"API Key present: {bool(YOUTUBE_API_KEY)}")
    
    # Check cache first (unless force refresh)
    if not force_refresh:
        cached = get_cached_videos()
        if cached:
            print("Using cached YouTube videos")
            return cached
    
    # Check if API key is configured
    if not YOUTUBE_API_KEY:
        print("YouTube API key not configured. Using default videos.")
        return get_default_videos()
    
    print("Fetching fresh videos from YouTube...")
    all_videos = []
    seen_ids = set()
    
    # Search for videos using different queries
    for query in FINANCE_SEARCHES:
        videos = search_youtube_videos(query, max_results=3)
        
        for video in videos:
            if video['youtubeId'] not in seen_ids:
                seen_ids.add(video['youtubeId'])
                all_videos.append(video)
    
    # Get detailed information for all videos
    if all_videos:
        video_ids = [v['youtubeId'] for v in all_videos[:25]]  # Limit to 25 videos
        detailed_videos = get_video_details(video_ids)
        
        # Merge and enhance video data
        final_videos = []
        for i, video in enumerate(detailed_videos):
            video['id'] = i + 1
            video['category'] = categorize_video(video['title'], video['description'])
            video['level'] = determine_level(video['title'], video['description'])
            video['topics'] = extract_topics(video['title'], video['description'])
            video['featured'] = i < 6  # First 6 are featured
            final_videos.append(video)
        
        # Save to cache
        save_to_cache(final_videos)
        
        return final_videos
    
    return get_default_videos()


def get_default_videos():
    """Return default videos when API is not available."""
    return [
        {
            "id": 1,
            "title": "How To Manage Your Money (50/30/20 Rule)",
            "channel": "Nischa",
            "category": "budgeting",
            "duration": "10:14",
            "rating": 4.9,
            "description": "Master the 50/30/20 budgeting rule to take control of your finances.",
            "topics": ["Budgeting", "50/30/20 Rule", "Money Management"],
            "level": "Beginner",
            "featured": True,
            "youtubeId": "HQzoZfc3GwQ"
        },
        {
            "id": 2,
            "title": "Stock Market For Beginners",
            "channel": "ClearValue Tax",
            "category": "investing",
            "duration": "36:12",
            "rating": 4.8,
            "description": "Complete beginner's guide to investing in the stock market.",
            "topics": ["Stocks", "Investing Basics", "Stock Market"],
            "level": "Beginner",
            "featured": True,
            "youtubeId": "p7HKvqRI_Bo"
        },
        {
            "id": 3,
            "title": "Dave Ramsey's 7 Baby Steps",
            "channel": "The Ramsey Show",
            "category": "debt",
            "duration": "14:23",
            "rating": 4.8,
            "description": "Learn Dave Ramsey's proven 7-step plan to get out of debt.",
            "topics": ["Debt Freedom", "Baby Steps", "Financial Peace"],
            "level": "Beginner",
            "featured": True,
            "youtubeId": "2bLkBLxKrVg"
        },
        {
            "id": 4,
            "title": "How To Create A Budget",
            "channel": "Rachel Cruze",
            "category": "budgeting",
            "duration": "8:45",
            "rating": 4.7,
            "description": "Step-by-step guide to creating a budget you'll stick to.",
            "topics": ["Budgeting", "Zero-Based Budget", "Money Plan"],
            "level": "Beginner",
            "featured": False,
            "youtubeId": "sVKQn2I4HDM"
        },
        {
            "id": 5,
            "title": "Index Funds Explained",
            "channel": "Two Cents",
            "category": "investing",
            "duration": "8:56",
            "rating": 4.8,
            "description": "Everything you need to know about index fund investing.",
            "topics": ["Index Funds", "Passive Investing", "S&P 500"],
            "level": "Beginner",
            "featured": True,
            "youtubeId": "fwe-PjrX23o"
        },
        {
            "id": 6,
            "title": "Build An Emergency Fund",
            "channel": "The Financial Diet",
            "category": "savings",
            "duration": "11:28",
            "rating": 4.7,
            "description": "Practical tips to build your emergency fund quickly.",
            "topics": ["Emergency Fund", "Savings", "Financial Security"],
            "level": "Beginner",
            "featured": True,
            "youtubeId": "vZyeeVnja78"
        },
        {
            "id": 7,
            "title": "Roth IRA Explained",
            "channel": "Humphrey Yang",
            "category": "retirement",
            "duration": "9:52",
            "rating": 4.9,
            "description": "Complete guide to Roth IRA retirement accounts.",
            "topics": ["Roth IRA", "Retirement", "Tax-Free Growth"],
            "level": "Beginner",
            "featured": False,
            "youtubeId": "vn3-EWs1Yfs"
        },
        {
            "id": 8,
            "title": "How To Pay Off Debt Fast",
            "channel": "Graham Stephan",
            "category": "debt",
            "duration": "15:47",
            "rating": 4.8,
            "description": "Strategies to pay off debt and save on interest.",
            "topics": ["Debt Payoff", "Debt Snowball", "Financial Freedom"],
            "level": "All Levels",
            "featured": False,
            "youtubeId": "mJCfLPftTKA"
        },
        {
            "id": 9,
            "title": "Credit Score Explained",
            "channel": "Two Cents",
            "category": "debt",
            "duration": "7:23",
            "rating": 4.8,
            "description": "Understand how credit scores work and improve yours.",
            "topics": ["Credit Score", "FICO", "Credit Building"],
            "level": "Beginner",
            "featured": False,
            "youtubeId": "DP6XSqV2VZs"
        },
        {
            "id": 10,
            "title": "Compound Interest Explained",
            "channel": "The Plain Bagel",
            "category": "investing",
            "duration": "8:56",
            "rating": 4.9,
            "description": "How compound interest works and why it's powerful.",
            "topics": ["Compound Interest", "Investing", "Wealth Building"],
            "level": "Beginner",
            "featured": False,
            "youtubeId": "wf91rEGw88Q"
        },
        {
            "id": 11,
            "title": "Start Investing With Little Money",
            "channel": "Andrei Jikh",
            "category": "investing",
            "duration": "18:34",
            "rating": 4.8,
            "description": "Start investing even if you only have $100.",
            "topics": ["Investing", "Beginners", "Small Amounts"],
            "level": "Beginner",
            "featured": True,
            "youtubeId": "gFQNPmLKj1k"
        },
        {
            "id": 12,
            "title": "401k Explained",
            "channel": "Two Cents",
            "category": "retirement",
            "duration": "3:42",
            "rating": 4.7,
            "description": "Quick explanation of 401k retirement accounts.",
            "topics": ["401k", "Retirement", "Employer Match"],
            "level": "Beginner",
            "featured": False,
            "youtubeId": "5MIR_gKLN0s"
        }
    ]

