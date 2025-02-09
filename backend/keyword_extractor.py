import requests
from bs4 import BeautifulSoup
import spacy

# Load spaCy's small English model. Loading it at the module level prevents re-loading on each call.
nlp = spacy.load("en_core_web_sm")

def extract_keywords(url):
    """
    Fetches the web page at the given URL, extracts text content, and returns up to 3 key
    named entities (as a space-separated string) using spaCy's NER. Suitable for news articles
    and similar content.
    
    :param url: The URL (string) of the article to process.
    :return: A string of space-separated keywords (entities) or an error message.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors.
    except Exception as e:
        return f"Error retrieving URL: {e}"

    # Parse the HTML content.
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script, style, and noscript tags.
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Extract visible text from the page.
    text = soup.get_text(separator=" ")

    # Process the text with spaCy.
    doc = nlp(text)

    # Define the entity labels we're interested in.
    entity_labels = {"PERSON", "ORG", "GPE", "EVENT", "PRODUCT", "WORK_OF_ART", "LANGUAGE"}
    entities = [ent.text.strip() for ent in doc.ents if ent.label_ in entity_labels]

    # Remove duplicate entities (ignoring case) while preserving order.
    seen = set()
    unique_entities = []
    for entity in entities:
        lower_entity = entity.lower()
        if lower_entity not in seen:
            seen.add(lower_entity)
            unique_entities.append(entity)

    # Return up to 3 keywords as a space-separated string (with no commas).
    return " ".join(unique_entities[:3])

if __name__ == '__main__':
    # This block is executed only if the module is run directly.
    url_input = input("Enter the URL: ").strip()
    print("Keywords:", extract_keywords(url_input))
