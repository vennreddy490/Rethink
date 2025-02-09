import openai
from typing import Dict, List
import os
import json  # Needed for JSON parsing
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_bulk_additional_info(main_article: str, source_articles: Dict[str, str]) -> Dict[str, str]:
    """
    Uses OpenAI API to compare a main article against multiple source articles in one call.
    Returns a dictionary mapping each source name to its additional information.
    """
    prompt = (
        "Compare the following main news article with several source articles.\n\n"
        "Main Article (reference):\n"
        f"{main_article}\n\n"
        "For each of the following source articles, identify key facts, perspectives, or details that are present in the source article but NOT mentioned in the Main Article.\n"
        "Provide a concise summary for each.\n"
        "Respond ONLY with a valid JSON object. Do not include any additional text, markdown, or explanation.\n"
        "Each key in the JSON object should be the source name, and its value should be the summary of additional details.\n"
    )
    for source, text in source_articles.items():
        prompt += f"\nSource: {source}\nArticle:\n{text}\n"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    result_text = response.choices[0].message.content.strip()
    if not result_text:
        print("Empty response from bulk comparison API.")
        return {}
    try:
        result_dict = json.loads(result_text)
    except Exception as e:
        print("Error parsing JSON response from bulk comparison:", e)
        print("Raw API response:", result_text)
        result_dict = {}
    return result_dict

def analyze_articles(articles: Dict[str, str], main_source: str, compare_to: List[str]):
    """
    Compares multiple articles against the main source article to identify additional information using a bulk API call.
    """
    if main_source not in articles:
        raise ValueError("Main source article not found in the provided dictionary.")
    
    main_article = articles[main_source]
    # Build a dictionary of source articles to compare.
    source_articles = {source: articles[source] for source in compare_to if source in articles}
    print(f"Comparing the following sources against {main_source}: {list(source_articles.keys())}")
    additional_info = get_bulk_additional_info(main_article, source_articles)
    return additional_info

# Optional: Keep this function for individual comparisons if needed.
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

    # Run the analysis using the bulk function.
    additional_info_report = analyze_articles(articles, main_source, compare_to)

    # Print results
    for source, additional_details in additional_info_report.items():
        print(f"\nAdditional information in {source} (not mentioned in {main_source}):")
        print(additional_details)
