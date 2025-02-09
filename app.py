from flask import Flask, render_template, request, jsonify
from backend import updated_news_api, debrief, news_api, keyword_extractor
import os
from flask_cors import CORS
import re
import csv
import datetime
import json
import pandas as pd
from dotenv import load_dotenv

# Optionally load environment variables from a .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allows requests from the extension

# GLOBAL VARIABLES:
news_api_key = os.getenv("NEWS_API_KEY")

# Counts dictionaries for tracking biases, credibility, and factuality.
bias_counts = {
    'Left': 0,
    'Far Right': 0,
    'Center': 0,
    'Far Left': 0,
    'Not Available': 0,
    'Center Left': 0,
    'Right': 0,
    'Center Right': 0
}

credibility_counts = {
    'Low': 0,
    'High Credibility': 0,
    'N/A': 0,
    'Medium': 0,
    'Mixed': 0   # Added to match credibility_weights
}

factuality_counts = {
    'Low': 0,
    'Mostly': 0,
    'N/A': 0,
    'Very High': 0,
    'Very Low': 0,
    'High': 0,
    'Mixed': 0,
    'no factual reporting rating': 0
}

# Weights for each category.
bias_weights = {
    "Left": -2,
    "Far Right": 3,
    "Center": 0,
    "Far Left": -3,
    "Not Available": 0,
    "Center Left": -1,
    "Right": 2,
    "Center Right": 1
}

credibility_weights = {
    "Low": -2,
    "High Credibility": 2,
    "N/A": 0,
    "Medium": 1,
    "Mixed": -1
}

factuality_weights = {
    "Low": -1,
    "Mostly": 1,
    "N/A": 0,
    "Very High": 3,
    "Very Low": -2,
    "High": 2,
    "Mixed": 0,
    "no factual reporting rating": 0
}

@app.route("/app", methods=["POST"])
def build_app():
    data = request.get_json()
    main_url = data.get("main_url", "")
    print(f"Received URL: {main_url}")

    # TASK 1: News API Call
    print("TASK 1: NEWS API CALL")
    # Keywords from the article act as the 
    print("Grabbing keywords for title searching:")
    keywords = keyword_extractor.extract_keywords(main_url)
    # title = "trump south africa"
    print(f"Searching keywords: {keywords}")
    title = keywords
    articles = news_api.get_news(news_api_key, title)
    processed_articles = news_api.process_articles(articles, "./media_bias.json")
    print("Processed articles (sources and meta info):")
    for article in processed_articles:
        print(str(article))

    # TASK 2: AI SUMMARY (Bulk Comparison for Top 3 Articles)
    print("TASK 2: AI SUMMARY")
    from backend import fetch_html, debrief  # Ensure both modules are imported

    # 1. Fetch the main article's text.
    main_text_dict = fetch_html.extract_article_text([main_url])
    main_article_text = main_text_dict.get(main_url, "")
    if not main_article_text:
        print(f"Failed to fetch main article text from {main_url}")
    else:
        print("Successfully fetched main article text.")

    # 2. Select the top 3 articles from processed_articles.
    top_articles = processed_articles[:3] if len(processed_articles) >= 3 else processed_articles

    # 3. Fetch texts for these top articles.
    top_article_urls = [article["article_url"] for article in top_articles]
    top_articles_text = fetch_html.extract_article_text(top_article_urls)

    # 4. Build the dictionary for analysis.
    articles_for_analysis = {"Main": main_article_text}
    for article in top_articles:
        source_name = article["name"]
        url = article["article_url"]
        text = top_articles_text.get(url, "Article text not available.")
        articles_for_analysis[source_name] = text

    # 5. Prepare the list of sources to compare (excluding "Main").
    compare_sources = [key for key in articles_for_analysis if key != "Main"]

    # 6. Call the bulk analysis function.
    additional_info_report = debrief.analyze_articles(articles_for_analysis, "Main", compare_sources)

    # TASK 3: MEDIA BIAS and MEDIA DIET
    print("TASK 3: MEDIA BIAS")
    # get_diet returns a tuple of four values.
    bias_counts_sum, factuality_counts_sum, credibility_counts_sum, score_dict = get_diet(main_url)
    media_diet = {
        "bias_counts": bias_counts_sum,
        "factuality_counts": factuality_counts_sum,
        "credibility_counts": credibility_counts_sum,
        "score_dict": score_dict
    }

    # Build the "sources" list (all processed articles) using the provided schema.
    sources = []
    for article in processed_articles:
        sources.append({
            "name": article.get("name", "Unknown"),
            "article_url": article.get("article_url", "URL"),
            "date": article.get("date", "Unknown"),
            "factuality": article.get("factuality", "Unknown"),
            "bias": article.get("bias", "Unknown"),
            "credibility": article.get("credibility", "Unknown")
        })

    # "summary_sources" will be the top_articles (the ones used for the AI summary).
    summary_sources = []
    for article in top_articles:
        summary_sources.append({
            "name": article.get("name", "Unknown"),
            "article_url": article.get("article_url", "URL"),
            "date": article.get("date", "Unknown"),
            "factuality": article.get("factuality", "Unknown"),
            "bias": article.get("bias", "Unknown"),
            "credibility": article.get("credibility", "Unknown")
        })

    # Determine "main_source": if the main_url exists in processed_articles, use that; otherwise, use defaults.
    main_source_dict = None
    for article in processed_articles:
        if article.get("article_url") == main_url:
            main_source_dict = {
                "name": article.get("name", "Unknown"),
                "article_url": article.get("article_url", "URL"),
                "date": article.get("date", "Unknown"),
                "factuality": article.get("factuality", "Unknown"),
                "bias": article.get("bias", "Unknown"),
                "credibility": article.get("credibility", "Unknown")
            }
            break
    if not main_source_dict:
        main_source_dict = {
            "name": "Main Source",
            "article_url": main_url,
            "date": "Unknown",
            "factuality": "Unknown",
            "bias": "Unknown",
            "credibility": "Unknown"
        }

    # "summary" is derived from the AI summary results.
    summary_final = additional_info_report

    print("\n\n\n\n\n\n\n\n")
    print("===========================")
    print(f"summary: {summary_final}\n")
    print(f"summary_sources: {summary_sources}\n")
    print(f"sources: {sources}\n")
    print(f"main_source: {main_source_dict}\n")
    print(f"media_diet: {media_diet}\n")


    return render_template("./testingbase.html",
                           summary=summary_final,
                           summary_sources=summary_sources,
                           sources=sources,
                           main_source=main_source_dict,
                           media_diet=media_diet)

# Helper Functions

def calculate_rating(counts, weights):
    """
    Calculate a weighted rating for a given counts dictionary and weights dictionary.
    Returns 0 if there are no recorded occurrences.
    """
    total_occurrences = sum(counts.values())
    if total_occurrences == 0:
        return 0
    weighted_sum = sum(weights.get(category, 0) * count for category, count in counts.items())
    return weighted_sum / total_occurrences

def write_all_counts_to_csv(bias_counts, factuality_counts, credibility_counts,
                            bias_score, factuality_score, credibility_score):
    """
    Writes raw counts (NO SCORES) to CSV. If the file does not exist,
    it creates it with the proper header.
    """
    header = (['Timestamp'] +
              ['Bias Score'] + list(bias_counts.keys()) +
              ['Factuality Score'] + list(factuality_counts.keys()) +
              ['Credibility Score'] + list(credibility_counts.keys()))
    
    timestamp = datetime.datetime.now().isoformat()
    row = ([timestamp] +
           [bias_score] + [bias_counts.get(k, 0) for k in bias_counts] +
           [factuality_score] + [factuality_counts.get(k, 0) for k in factuality_counts] +
           [credibility_score] + [credibility_counts.get(k, 0) for k in credibility_counts])
    
    print(f"📏 Expected Columns: {len(header)}, | Row Columns: {len(row)}")
    if len(row) != len(header):
        print(f"⚠️ MISMATCH: Row has {len(row)} columns, expected {len(header)}.")
        return
    
    file_exists = os.path.isfile('./all_counts.csv')
    with open('./all_counts.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)
    
    print("✅ Data successfully written to CSV. Scores will be handled separately in `get_diet()`.")

def convert_url(url):
    """
    Convert a URL starting with 'http://' or 'https://' to one that starts with 'www.'.
    """
    pattern = r'^https?://(?:www\.)?(.*)'
    return re.sub(pattern, r'www.\1', url)

def get_root_url(url):
    """
    Extracts the root domain from a given URL.
    Example: https://www.nbcnews.com/politics/... -> https://www.nbcnews.com
    """
    match = re.match(r'^(https?://[^/]+)', url)
    return match.group(1) if match else url

def get_diet(url):
    """
    Updates counts based on the media_bias.json file,
    writes the updated counts to CSV, then reads and aggregates the CSV.
    Returns a tuple with aggregated bias, factuality, and credibility counts plus a score dictionary.
    """
    global bias_counts, factuality_counts, credibility_counts

    # Reset counts
    for key in bias_counts:
        bias_counts[key] = 0
    for key in factuality_counts:
        factuality_counts[key] = 0
    for key in credibility_counts:
        credibility_counts[key] = 0

    root_url = get_root_url(url)
    root_url = convert_url(root_url) + "/"

    # Load media_bias.json for matching.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'backend/media_bias.json')
    try:
        with open(json_path, 'r') as file:
            sources = json.load(file)
    except Exception as e:
        print("Error reading JSON:", e)
        return {}, {}, {}, {}

    matching_source = next((source for source in sources if source.get('url') == root_url), None)
    if matching_source:
        bias = matching_source.get('bias')
        factual = matching_source.get('factual')
        credibility = matching_source.get('credibility')
        if bias in bias_counts:
            bias_counts[bias] += 1
        if factual in factuality_counts:
            factuality_counts[factual] += 1
        if credibility in credibility_counts:
            credibility_counts[credibility] += 1
    else:
        print("Source not found")

    right_now_bias = bias_weights.get(bias, 0)
    right_now_factuality = factuality_weights.get(factual, 0)
    right_now_credibility = credibility_weights.get(credibility, 0)

    write_all_counts_to_csv(bias_counts, factuality_counts, credibility_counts,
                            right_now_bias, right_now_factuality, right_now_credibility)

    try:
        df = pd.read_csv("./all_counts.csv")
    except Exception as e:
        print("Error reading CSV file:", e)
        header = (['Timestamp'] +
                  ['Bias Score'] + list(bias_counts.keys()) +
                  ['Factuality Score'] + list(factuality_counts.keys()) +
                  ['Credibility Score'] + list(credibility_counts.keys()))
        df = pd.DataFrame(columns=header)

    if df.empty:
        print("CSV is empty. Returning current counts.")
        return bias_counts, factuality_counts, credibility_counts, {}

    bias_score_avg = df["Bias Score"].mean()
    factuality_score_avg = df["Factuality Score"].mean()
    credibility_score_avg = df["Credibility Score"].mean()

    score_dict = {
        "Bias Score": bias_score_avg,
        "Factuality Score": factuality_score_avg,
        "Credibility Score": credibility_score_avg
    }

    bias_columns = list(bias_weights.keys())
    factuality_columns = list(factuality_weights.keys())
    credibility_columns = list(credibility_weights.keys())

    bias_counts_sum = df[bias_columns].sum().to_dict()
    factuality_counts_sum = df[factuality_columns].sum().to_dict()
    credibility_counts_sum = df[credibility_columns].sum().to_dict()

    print("Bias Counts:", bias_counts_sum)
    print("Factuality Counts:", factuality_counts_sum)
    print("Credibility Counts:", credibility_counts_sum)
    print("Score Dictionary:", score_dict)

    return bias_counts_sum, factuality_counts_sum, credibility_counts_sum, score_dict

if __name__ == '__main__':
    app.run(debug=True, port=5000)
