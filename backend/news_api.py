import requests
import os
import json
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load API key
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def get_news(api_key, query, language='en', page_size=20):
    """
    Fetch news articles from NewsAPI.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": api_key,
        "language": language,
        "pageSize": page_size
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        print("Error fetching news:", response.json())
        return []

def process_articles(articles, new_sources_path):
    """
    Processes a list of articles to extract metadata from new_sources.json.
    """
    with open(new_sources_path, "r") as f:
        new_sources = json.load(f)

    source_metadata = {entry["url"].rstrip("/"): entry for entry in new_sources}

    article_data = []
    for article in articles:
        parsed_url = urlparse(article["url"])
        shortened_url = parsed_url.netloc

        # Ensure "www." is present
        if not shortened_url.startswith("www."):
            shortened_url = "www." + shortened_url

        # Ensure '/' at the end
        shortened_url += "/"

        metadata = source_metadata.get(shortened_url.rstrip("/"), {})

        article_data.append({
            "shortened_url": shortened_url,
            "article_url": article["url"],
            "date": article["publishedAt"].split("T")[0],  # Extract date only
            "name": metadata.get("name", "Unknown"),
            "bias": metadata.get("bias", "Unknown"),
            "factuality": metadata.get("factual", "Unknown"),
            "credibility": metadata.get("credibility", "Unknown")
        })

    return article_data

if __name__ == "__main__":
    title = "trump citizenship ban"

    # Fetch news articles
    articles = get_news(API_KEY, query=title, page_size=20)  # Fixed the parameter name

    # Process the articles
    new_sources_path = "./media_bias.json"
    processed_articles = process_articles(articles, new_sources_path)

    # Return only processed articles
    # print(processed_articles)

    for i in processed_articles:
        print(str(i))
