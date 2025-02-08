import requests
import spacy
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(title, max_keywords=5):
    """Extracts key terms from a news title using spaCy NLP."""
    doc = nlp(title.lower())  # Process text
    keywords = []
    
    # Identify relevant words (Nouns, Proper Nouns, Verbs)
    for token in doc:
        if token.pos_ in ("NOUN", "PROPN", "VERB") and not token.is_stop:
            keywords.append(token.lemma_)  # Use lemma to avoid duplicates
    
    # Count frequency & select most relevant
    keyword_freq = Counter(keywords)
    top_keywords = [word for word, _ in keyword_freq.most_common(max_keywords)]
    
    return " ".join(top_keywords)  # Convert list to string

def get_news(api_key, query, language='en', page_size=20):
    """Fetches news articles from NewsAPI based on refined query."""
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
    """Displays fetched news articles."""
    if not articles:
        print("No articles found.")
        return
    
    for i, article in enumerate(articles, start=1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']['name']}")
        print(f"   URL: {article['url']}")
        print("-" * 60)

if __name__ == "__main__":
    API_KEY = os.getenv("NEWS_API_KEY")  # Replace with your NewsAPI key
    title = input("Enter a news title: ")
    
    # Extract key terms
    refined_query = extract_keywords(title)
    print(f"Refined Search Query: {refined_query}")
    
    # Fetch news based on refined query
    articles = get_news(API_KEY, refined_query)
    display_news(articles)
