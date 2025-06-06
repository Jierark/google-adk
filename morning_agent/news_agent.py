from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os
import requests
from morning_agent.models import news_article
from dotenv import load_dotenv
from pydantic import ValidationError
from typing import List, Optional
from morning_agent.rssparser import get_hacker_news

# Accessing project based environment variables
load_dotenv()
# Model to use
MODEL_OPENAI = "openai/gpt-4.1-2025-04-14"

NEWS_API_KEY = os.environ["NEWS_API_KEY"]
# Tool example
def get_news(topic: str, number: Optional[int]) -> dict:
    """Get current news of a specific topic

    Args:
        topic (str): the topic for which to retrieve news articles
        number: the number of articles to fetch. If not provided, uses a default of 5
    Returns:
        A list of news articles for the specified topic, or an error if something goes wrong.
    """
    print(f"***TOOL CALLED: get_news with topic {topic}***")
    if not number:
        number = 5
    possible_topics = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    # https://newsapi.org/docs/endpoints/top-headlines
    if topic.lower() in possible_topics:
        params = {
            'apiKEY': NEWS_API_KEY,
            'category': topic.lower(),
            'pageSize': number
        }
    else:
        params = {
            'apiKEY': NEWS_API_KEY,
            'q': topic.lower(),
            'pageSize': number
        }
    response = requests.get('https://newsapi.org/v2/top-headlines', params=params)
    if response.status_code == 200:
        # Return the links to articles
        articles = response.json()['articles']
        ret = []
        for article in articles:
            try:
                article = news_article(
                    title=article['title'],
                    author=article['author'],
                    description=article['description'],
                    url=article['url']
                )
                ret.append(article)
            except ValidationError as e:
                print(f"Invalid article: {e}")
        if ret:
            return {'status': 'success', 'articles': ret}
        else:
            return {"status": 'error', "error_message": f"Sorry, I can't find any articles pertaining to {topic}"}    
    else:
        return {"status": 'error', "error_message": f"Sorry, I can't find any articles pertaining to {topic}"}

# Agent example
news_agent = Agent(
    name = "news_agent",
    model = LiteLlm(model=MODEL_OPENAI),
    description="Fetches up-to-date news from the web.",
    instruction="""You are a news agent. Your task is to fetch news articles of a specified topic.
    Use the tool get_news to get the articles of a topic of the user's choice.
    If the user specifies that they want The Hacker News, then use the tool get_hacker_news.
    The user can optionally specify the number of articles. If the user does not specify, use 5 as the default.
    Output the results as a list of new_article objects, containing the following fields:
        title: The title of the article,
        author: The author of the article,
        description: a brief description of the article,
        url: a URL to the article.
    If you have a success status, then present the information clearly and concisely.
    If you have an error status, then politely inform the user about the error message.
    """,
    tools=[get_news, get_hacker_news]
)