from pathlib import Path
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from dotenv import load_dotenv
import os
import praw

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base paths
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# Source-specific paths
EATER_DIR = RAW_DATA_DIR / "eater"
REDDIT_DIR = RAW_DATA_DIR / "reddit"
TRAVEL_BLOGS_DIR = RAW_DATA_DIR / "travel_blogs"
SUBSTACK_DIR = RAW_DATA_DIR / "substack"
TIKTOK_DIR = RAW_DATA_DIR / "tiktok"

def save_scraped_data(source: str, data: dict, filename: str):
    """Save scraped data to appropriate directory"""
    source_dir = RAW_DATA_DIR / source
    source_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = source_dir / filename
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Successfully saved data to {file_path}")
    except Exception as e:
        logger.error(f"Error saving data to {file_path}: {str(e)}")

def scrape_eater_articles():
    """Scrape luxury restaurant and travel articles from Eater"""

def scrape_reddit_luxury():
    """
    Scrape luxury travel content from relevant subreddits
    Requires Reddit API credentials in .env file
    """
    try:
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent="luxury_ai_agent"
        )
        
        # Target luxury-focused subreddits
        subreddits = ['luxurytravel', 'fivestar', 'luxury', 'VIPtravel']
        posts = []
        
        for subreddit_name in subreddits:
            logger.info(f"Scraping r/{subreddit_name}...")
            try:
                subreddit = reddit.subreddit(subreddit_name)
                for post in subreddit.hot(limit=50):
                    post_data = {
                        "title": post.title,
                        "url": f"https://reddit.com{post.permalink}",
                        "score": post.score,
                        "upvote_ratio": post.upvote_ratio,
                        "created_utc": datetime.fromtimestamp(post.created_utc).isoformat(),
                        "num_comments": post.num_comments,
                        "subreddit": subreddit_name,
                        "text": post.selftext,
                        "scraped_at": datetime.now().isoformat()
                    }
                    posts.append(post_data)
            except Exception as e:
                logger.error(f"Error scraping r/{subreddit_name}: {str(e)}")
                continue
        
        # Save scraped data
        if posts:
            save_scraped_data(
                source="reddit",
                data={"posts": posts},
                filename=f"luxury_posts_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            )
            logger.info(f"Successfully scraped {len(posts)} posts from Reddit")
        return posts
        
    except Exception as e:
        logger.error(f"Reddit scraping failed: {str(e)}")
        return []