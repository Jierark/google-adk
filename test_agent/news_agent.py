from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os
import requests
from test_agent.models import news_article
from dotenv import load_dotenv

# Accessing project based environment variables
load_dotenv()
# Model to use
MODEL_OPENAI = "openai/gpt-4.1-2025-04-14"

NEWS_API_KEY = os.environ["NEWS_API_KEY"]
# Tool example
def get_news(topic: str) -> dict:
    """Get current news of a specific topic

    Args:
        topic (str): the topic for which to retrieve news articles
    Returns:
        A list of news articles for the specified topic, or an error if something goes wrong.
    """
    print(f"***TOOL CALLED: get_news with topic {topic}***")

    possible_topics = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    # https://newsapi.org/docs/endpoints/top-headlines
    if topic.lower() in possible_topics:
        params = {
            'apiKEY': NEWS_API_KEY,
            'category': topic.lower(),
            'pageSize': 5
        }
    else:
        params = {
            'apiKEY': NEWS_API_KEY,
            'q': topic.lower(),
            'pageSize': 5
        }
    response = requests.get('https://newsapi.org/v2/top-headlines', params=params)
    if response.status_code == 200:
        # Return the links to articles
        articles = response.json()['articles']
        urls = []
        for article in articles:
            urls.append(article['url'])
        return {'status': 'success', 'articles': urls}
    else:
        return {"status": 'error', "error_message": f"Sorry, I can't find any articles pertaining to {topic}"}

# Agent example
news_agent = Agent(
    name = "news_agent",
    model = LiteLlm(model=MODEL_OPENAI),
    description="Fetches up-to-date news from the web.",
    instruction="You are a news agent. Your task is to fetch news articles of a specified topic."
    "Use the tool get_news to get the articles of a topic of the user's choice. "
    "Output both the title of the article, as well as the url to the article."
    "If you have a success status, then present the information clearly and concisely. "
    "If you have an error status, then politely inform the user about the error message.",
    tools=[get_news]
)