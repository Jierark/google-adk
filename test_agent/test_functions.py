# Testing file for various functions without invoking the agents

from dotenv import load_dotenv
import os
import requests
from urllib3 import response

# Accessing project based environment variables
load_dotenv()

NEWS_API_KEY = os.environ["NEWS_API_KEY"]


possible_topics = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

params = {
    'apiKEY': NEWS_API_KEY,
    'category': 'science',
    'pageSize': 5
}
response = requests.get('https://newsapi.org/v2/top-headlines', params=params)
if response.status_code == 200:
    articles = response.json()['articles']
    urls = []
    for i, source in enumerate(articles):
        print(source)
        print(f"article number {i}")
        urls.append(source['url'])
print(urls)