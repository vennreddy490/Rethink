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

def get_sources(articles):
    """
    Extracts the sources from a list of news articles.

    :param articles: List of dictionaries, each representing a news article.
    :return: List of unique source names.
    """
    return list({article['source']['name'] for article in articles if article.get('source') and article['source'].get('name')})

def get_source_urls(articles):
    """
    Extracts the source URLs from a list of news articles.

    :param articles: List of dictionaries, each representing a news article.
    :return: List of unique source URLs.
    """
    return list({article['url'] for article in articles if 'url' in article})

def news_api(title, num_results=20):
    load_dotenv()
    API_KEY = os.getenv("NEWS_API_KEY") 

    if title is None:
        title = "trump citizenship ban"
    query = title
    # query = input("Enter a topic to search news about: ")
    articles = get_news(API_KEY, query, page_size=num_results)

    sources = get_sources(articles)

    source_urls = get_source_urls(articles)

  
    print(f"The type of articles is: \n{type(articles)}")
    print(f"And here is what articles looks like: \n{articles}")

    print("\n")

    print(f"The type of articles[0] is \n{type(articles[0])}")
    print(f"And here is what articles[0] looks like: \n{articles[0]}")

    print("\n\n\n")
    print(f"Here is the type of sources: \n{type(sources)}")
    print(f"And here is what sources looks like: \n{sources}")

    print("\n\n\n")
    print(f"Here is the type of source_urls: \n{type(source_urls)}")
    print(f"And here is what source_urls looks like: \n{source_urls}")

    return source_urls


    # display_news(articles)

if __name__ == "__main__":
    news_api(title="trump citizenship ban")