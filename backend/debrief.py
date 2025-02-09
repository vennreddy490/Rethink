import openai
from typing import Dict, List
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def truncate_text(text: str, limit: int = 500) -> str:
    """
    Truncates the text to a maximum number of characters.
    """
    if len(text) > limit:
        return text[:limit] + "..."
    return text

def get_bulk_additional_info(main_article: str, source_articles: Dict[str, str]) -> Dict[str, str]:
    """
    Uses OpenAI API to compare a main article against multiple source articles in one call.
    The texts are truncated to keep the prompt short.
    Returns a dictionary mapping each source name to its additional information.
    """
    # Truncate main article text.
    main_article_short = truncate_text(main_article, 500)
    
    prompt = (
        "Compare the following main news article with several source articles.\n\n"
        "Main Article (reference):\n"
        f"{main_article_short}\n\n"
        "For each of the following source articles, identify key facts, perspectives, or details that are present in the source article but NOT mentioned in the Main Article.\n"
        "Provide a concise summary for each.\n"
        "Respond ONLY with a valid JSON object. Do not include any additional text, markdown, or explanation.\n"
        "Each key in the JSON object should be the source name, and its value should be the summary of additional details.\n"
    )
    
    # Append each source article (truncated) to the prompt.
    for source, text in source_articles.items():
        truncated_text = truncate_text(text, 500)
        prompt += f"\nSource: {source}\nArticle:\n{truncated_text}\n"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    result_text = response.choices[0].message.content.strip()

    print("RESULT TEXT RETRIEVED:")
    # print(f"\n\ntype of result text: {type(result_text)}\n\n")
    # print(f"result text: \n{result_text}\n\n")

    print("Now attempting to get string from it:")
    new_data = trim_string(result_text)
    data = new_data[:-4]
    # print('test 1')
    # print("and now data should look like:")
    # print(data)
    # print("======================\n\n\n\n")

    return data



    # if not result_text:
    #     print("Empty response from bulk comparison API.")
    #     return {}
    # try:
    #     result_dict = json.loads(result_text)
    # except Exception as e:
    #     print("Error parsing JSON response from bulk comparison:", e)
    #     print("Raw API response:", result_text)
    #     result_dict = {}
    # return result_dict

def trim_string(s):
    return s[8:]


def analyze_articles(articles: Dict[str, str], main_source: str, compare_to: List[str]):
    """
    Compares multiple articles against the main source article using a bulk API call.
    """
    if main_source not in articles:
        raise ValueError("Main source article not found in the provided dictionary.")
    
    main_article = articles[main_source]
    source_articles = {source: articles[source] for source in compare_to if source in articles}
    print(f"Comparing the following sources against {main_source}: {list(source_articles.keys())}")
    additional_info = get_bulk_additional_info(main_article, source_articles)
    # print(f"additional info is: \n{additional_info}")
    return additional_info

# (The rest of your debrief.py remains the same.)
