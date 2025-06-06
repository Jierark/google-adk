import feedparser
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv
from morning_agent.models import news_article
from typing import Dict, List, Optional

load_dotenv()

MODEL_OPENAI = "openai/gpt-4.1-2025-04-14"

def load_feed(url:str):
    """
    Load an rss feed from a url
    """
    feed = feedparser.parse(url)
    if feed.status == 200:
        return feed.entries
    else:
        return "Error"

def get_articles(url:str, num: int) -> List[news_article]:
    """
    Get a specified number of articles from an rss feed
    """
    feed = load_feed(url)
    ret = []
    if len(feed) < num:
        end = len(feed)
    else:
        end = num
    for article in feed[0:end]:
        ret.append(news_article(
            title=article.title,
            author=article.author,
            description=article.summary,
            url=article.link
    ))
    return ret

def get_hacker_news(number: Optional[int]) -> Dict:
    """
    Get current hacker news.

    Args:
        number (int): the number of articles to retrieve. If number is not specified, then uses a default of 5.
    Returns:
        A list of hacker news articles, or an error if something goes wrong.
    """
    print(f"***TOOL CALLED: get_hacker_news with number {number}***")
    if not number:
        number = 5
    articles = get_articles("https://feeds.feedburner.com/TheHackersNews", number)
    
    if articles == "Error":
        return {"status": "error", "error_message": "Sorry, I can't currently access the latest in The Hacker News."}
    else:
        return {'status': 'success', 'articles': articles}