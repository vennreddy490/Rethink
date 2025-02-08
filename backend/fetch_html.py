import requests
import trafilatura

def fetch_html(url):
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str or None: The raw HTML content if successful, else None.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_article_text(urls):
    """
    Fetches HTML from a list of URLs and extracts clean article text.

    Args:
        urls (list): A list of article URLs.

    Returns:
        dict: A dictionary mapping each URL to its cleaned article text (or an error message).
    """
    return {
        url: (trafilatura.extract(html) if html else "Failed to fetch HTML")
        for url in urls
        if (html := fetch_html(url))  # Fetch HTML and ensure it's not None
    }

def main():
    """ Example usage of the extract_article_text function. """
    sample_urls = [
        "https://www.reuters.com/legal/second-us-judge-blocks-trumps-birthright-citizenship-order-2025-02-05/",
        "https://www.bbc.com/news/articles/cvg8kk9j3j0o",
        "https://www.theguardian.com/us-news/2025/jan/29/donald-trump-executive-orders-signed-list",
        "https://www.businessinsider.com/donald-trump-elon-musk-doge-executive-orders-blocked-courts-2025-2",
        "https://www.cnn.com/2025/02/06/us/birthright-citizenship-trump-order-maps-charts/index.html"
    ]

    # Get cleaned article text as a dictionary
    articles_dict = extract_article_text(sample_urls)

    # Print the extracted text for verification
    for url, text in articles_dict.items():
        print(f"Source: {url}\nExtracted Text: {text[:500]}...\n{'='*80}\n")  # Preview first 500 characters

if __name__ == "__main__":
    main()
