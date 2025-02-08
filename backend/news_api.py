import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")


def get_news(api_key, query, language='en', page_size=20):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": api_key,
        "language": language,
        "pageSize": page_size
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        news_data = response.json()
        return news_data["articles"]
    else:
        print("Error fetching news:", response.json())
        return []

def display_news(articles):
    if not articles:
        print("No articles found.")
        return
    
    for i, article in enumerate(articles, start=1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']['name']}")
        print(f"   URL: {article['url']}")
        print("-" * 60)

if __name__ == "__main__":
    API_KEY = os.getenv("NEWS_API_KEY") # Replace with your NewsAPI key
    query = input("Enter a topic to search news about: ")
    articles = get_news(API_KEY, query)
    display_news(articles)
