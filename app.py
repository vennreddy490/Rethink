from flask import Flask, render_template, redirect, request, jsonify
from backend import updated_news_api, debrief, news_api
import os
from flask_cors import CORS
import re
import csv
import atexit
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
    main_url = data.get("main_url", "")  # Extract URL from JSON

    print(f"Received URL: {main_url}")

    # TASK 1: News API Call
    print("TASK 1: NEWS API CALL")
    title = "trump south africa"
    articles = news_api.get_news(news_api_key, title)
    processed_articles = news_api.process_articles(articles, "./media_bias.json")
    print("Processed articles (sources and meta info):")
    if not processed_articles:
        print("PROCESS ARTICLES IS EMPTY")
    for article in processed_articles:
        print(str(article))

    # TASK 2: AI SUMMARY (insert code here)
    print("TASK 2: AI SUMMARY")

    # TASK 3: MEDIA BIAS and MEDIA DIET
    print("TASK 3: MEDIA BIAS")
    diet_tuples = get_diet(main_url)
    # (You can use diet_tuples as needed.)

    return jsonify({"message": "URL received", "main_url": main_url})


@app.route("/")
def home():
    summary = (
        "CNN has highlighted prior safety concerns, reporting that in the three years leading up to the crash, "
        "pilots had reported near-misses with helicopters at Reagan National Airport. (cnn.com) Reuters provided "
        "detailed information on the investigation's progress, including the identification of the soldiers "
        "involved and preliminary data suggesting that the helicopter may have been flying above its designated "
        "altitude at the time of the collision. (reuters.com) CBS News has focused on the technical aspects of "
        "the investigation, reporting that both the plane's black boxes have been recovered and are being analyzed "
        "to determine the cause of the crash. (cbs.com)"
    )
    sources = [
        {"name": "CNN", "image_url": "URL", "article_url": "URL", "date": "2/7/2025", "factuality": "High", "bias": "Center Left", "credibility": "High"},
        {"name": "CNN", "image_url": "URL", "article_url": "URL", "date": "2/7/2025", "factuality": "High", "bias": "Center Left", "credibility": "High"}
    ]
    summary_sources = [
        {"name": "CNN", "image_url": "URL", "article_url": "URL", "date": "2/7/2025", "factuality": "High", "bias": "Center Left", "credibility": "High"}
    ]
    main_source = {"name": "CNN", "image_url": "URL", "article_url": "URL", "date": "2/7/2025", "factuality": "High", "bias": "Center Left", "credibility": "High"}
    media_diet = {}

    return render_template("./testingbase.html",
                           summary=summary,
                           summary_sources=summary_sources,
                           sources=sources,
                           main_source=main_source,
                           media_diet=media_diet)


# Legacy testing routes

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Hello from Flask!, SUCCESSFULLY PINGED"})


@app.route('/post-test', methods=['POST'])
def post_test():
    data = request.get_json()
    try:
        num_value = int(data.get("num", 0))
        result = num_value + 5
        return jsonify({"message": f"Received num: {num_value}, After adding 5: {result}"})
    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400


@app.route('/post-string', methods=['POST'])
def post_string():
    data = request.get_json()
    received_text = data.get("text", "No text provided")
    reversed_text = received_text[::-1]
    return jsonify({"original_text": received_text, "reversed_text": reversed_text})


@app.route('/cnn-loaded', methods=['POST'])
def cnn_loaded():
    data = request.get_json()
    received_site = data.get("site", "No site provided")
    modified_site = received_site.upper()
    root_site = get_root_url(received_site)
    print(f"✅ Page Loaded - Received URL: {received_site} | Modified: {modified_site} | Root: {root_site}")
    return jsonify({
        "original_site": received_site,
        "modified_site": modified_site,
        "root_site": root_site,
        "message": "Page load detected successfully!"
    })


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
        return  # Do not write mismatched rows
    
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
    If the CSV does not exist or is empty, it handles that gracefully.
    Returns a tuple with aggregated bias, factuality, and credibility counts plus a score dictionary.
    """
    global bias_counts, factuality_counts, credibility_counts

    # Reset counts without changing key order
    for key in bias_counts:
        bias_counts[key] = 0
    for key in factuality_counts:
        factuality_counts[key] = 0
    for key in credibility_counts:
        credibility_counts[key] = 0

    # Clean and extract root URL
    root_url = get_root_url(url)
    root_url = convert_url(root_url)
    root_url = root_url + "/"

    # Load media_bias.json for matching
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'backend/media_bias.json')
    try:
        with open(json_path, 'r') as file:
            sources = json.load(file)
    except Exception as e:
        print("Error reading JSON:", e)
        response = jsonify({'error': f'Error reading JSON: {str(e)}'})
        response.status_code = 500
        return response

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

    # Now tally the score columns vertically and compute the average for each
    bias_score_avg = (df["Bias Score"].mean())
    factuality_score_avg = (df["Factuality Score"].mean())
    credibility_score_avg = (df["Credibility Score"].mean())

    score_dict = {
        "Bias Score": bias_score_avg,
        "Factuality Score": factuality_score_avg,
        "Credibility Score": credibility_score_avg
    }

    # For debugging, also aggregate the raw counts for each category
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
