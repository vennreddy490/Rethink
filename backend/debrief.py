import openai
from typing import Dict, List
import requests
import os
from dotenv import load_dotenv

load_dotenv()


# Set OpenAI API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_additional_info(main_article: str, source_article: str) -> str:
    """
    Uses OpenAI API to find what information is present in source_article 
    but missing from main_article.
    """
    prompt = f"""
    Compare the following two news articles about the same topic.
    
    Main Article (reference):
    {main_article}
    
    Source Article:
    {source_article}
    
    Identify key facts, perspectives, or details present in the Source Article 
    that are NOT mentioned in the Main Article. Summarize the additional details clearly.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content

def analyze_articles(articles: Dict[str, str], main_source: str, compare_to: List[str]):
    """
    Compares multiple articles against the main source article to identify additional information.
    """
    if main_source not in articles:
        raise ValueError("Main source article not found in the provided dictionary.")

    main_article = articles[main_source]
    results = {}

    for source in compare_to:
        if source == main_source:
            continue  # Skip comparing the main article to itself

        if source not in articles:
            print(f"Warning: Source '{source}' not found in articles. Skipping.")
            continue

        print(f"Comparing {source} against {main_source} to find additional information...")
        additional_info = get_additional_info(main_article, articles[source])
        results[source] = additional_info

    return results


# Example usage
if __name__ == "__main__":
    # Storing articles as variables instead of hardcoding inside the dictionary
    cnn_article = """President Donald Trump is seeking to end birthright citizenship in the US..."""
    business_insider_article = """President Donald Trump's executive orders have faced a slew of legal roadblocks..."""
    guardian_article = """Donald Trump has signed dozens of executive orders in his first weeks back in office..."""

    # Dynamically create the articles dictionary using variables
    articles = {
        "CNN": cnn_article,
        "Business Insider": business_insider_article,
        "The Guardian": guardian_article
    }

    # Define the main source and comparison sources dynamically
    main_source = "CNN"  # The main article to compare others against
    compare_to = ["Business Insider", "The Guardian"]  # Excluding CNN itself

    # Run the analysis
    additional_info_report = analyze_articles(articles, main_source, compare_to)

    # Print results
    for source, additional_details in additional_info_report.items():
        print(f"\nAdditional information in {source} (not mentioned in {main_source}):")
        print(additional_details)