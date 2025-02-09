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

app = Flask(__name__)
CORS(app)  # Allows requests from the extension

# GLOBAL VARIABLES:
news_api_key = os.getenv("NEWS_API_KEY")

# Record the instances of vistied articles' biases 
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

# Weights for each category (use lower-case keys)
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
    main_url = data.get("main_url", "")  # Extracts URL from JSON

    print(f"Received URL: {main_url}")  # Debugging output	

    # TASK 1: Venn news api call
    print("TASK 1: NEWS API CALL")
    title = "trump south africa"
    articles = news_api.get_news(news_api_key, title)
    processed_articles = news_api.process_articles(articles, "./media_bias.json")
    print("processed articles (the sources and their meta info) is:")

    if not processed_articles:
        print("PROCESS ARTICLES IN EMPTY")

    for i in processed_articles:
        print(str(i))

    # TASK 2: Venn AI Summary call
    print("TASK 2: AI SUMMARY")
    # insert code

    # TASK 3: Sammy media bias and media diet call
    print("TASK 3: MEDIA BIAS")
    diet_tuples = get_diet(main_url)
    # print("diet is:")
    # for i in diet:
    #     print(str(i))


    return jsonify({"message": "URL received", "main_url": main_url})

    # title = "Trump executive order to South Africa"
    # refined_query = updated_news_api.extract_keywords(title)
    # updated_news_api.refined_query(title)
    # news_api_key = os.getenv("NEWS_API_KEY")
    # articles = updated_news_api.get_news(news_api_key, refined_query)

    # updated_news_api.display_news(articles)

    # summary = "CNN has highlighted prior safety concerns, reporting that in the three years leading up to the crash, pilots had reported near-misses with helicopters at Reagan National Airport. (cnn.com) Reuters provided detailed information on the investigation's progress, including the identification of the soldiers involved and preliminary data suggesting that the helicopter may have been flying above its designated altitude at the time of the collision. (reuters.com) CBS News has focused on the technical aspects of the investigation, reporting that both the plane's black boxes have been recovered and are being analyzed to determine the cause of the crash. (cbs.com)"
    # sources = [{"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}, {"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}]
    # summary_sources = [{"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}]
    # main_source = {"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}
    # media_diet = {}

    # return render_template("./testingbase.html", summary=summary, summary_sources=summary_sources, sources=sources, main_source=main_source, media_diet=media_diet)

@app.route("/")
def home():

	summary = "CNN has highlighted prior safety concerns, reporting that in the three years leading up to the crash, pilots had reported near-misses with helicopters at Reagan National Airport. (cnn.com) Reuters provided detailed information on the investigation's progress, including the identification of the soldiers involved and preliminary data suggesting that the helicopter may have been flying above its designated altitude at the time of the collision. (reuters.com) CBS News has focused on the technical aspects of the investigation, reporting that both the plane's black boxes have been recovered and are being analyzed to determine the cause of the crash. (cbs.com)"
	sources = [{"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}, {"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}]
	summary_sources = [{"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}]
	main_source = {"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}
	media_diet = {}
	
	return render_template("./testingbase.html", summary=summary, summary_sources=summary_sources, sources=sources, main_source=main_source, media_diet=media_diet)


#  ! ALL OF THE FOLLOWING METHODS ARE LEGACY TESTING CODE! SEE WHICH ONES WE ARE NOT USING!
def get_root_url(url):
    """
    Extracts the root domain from a given URL.
    Example: https://www.nbcnews.com/politics/... -> https://www.nbcnews.com
    """
    match = re.match(r'^(https?://[^/]+)', url)
    return match.group(1) if match else url  # Return root or original if no match

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Hello from Flask!, SUCCESSFULLY PINGED"})

# New POST Route
@app.route('/post-test', methods=['POST'])
def post_test():
    data = request.get_json()  # Get JSON data from request

    # Get "num" from request, default to 0 if not provided
    try:
        num_value = int(data.get("num", 0))  # Convert to int to prevent errors
        result = num_value + 5  # Add 5
        return jsonify({"message": f"Received num: {num_value}, After adding 5: {result}"})
    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400
    
# NEW: POST Route that accepts a string
@app.route('/post-string', methods=['POST'])
def post_string():
    data = request.get_json()
    received_text = data.get("text", "No text provided")  # Get text from request
    reversed_text = received_text[::-1]  # Reverse the string for fun
    return jsonify({"original_text": received_text, "reversed_text": reversed_text})

# NEW: Handle CNN load detection from background.js
@app.route('/cnn-loaded', methods=['POST'])
def cnn_loaded():
    data = request.get_json()
    received_site = data.get("site", "No site provided")

    # Convert URL to uppercase
    modified_site = received_site.upper()

    # Extract root domain
    root_site = get_root_url(received_site)

    # Print to Flask terminal for debugging
    print(f"✅ Page Loaded - Received URL: {received_site} | Modified: {modified_site} | Root: {root_site}")

    # Return both modified and root versions
    return jsonify({
        "original_site": received_site,
        "modified_site": modified_site,
        "root_site": root_site,
        "message": "Page load detected successfully!"
    })

#! Non-Route Helper Methods
def calculate_rating(counts, weights):
    """
    Calculate a weighted rating for a given counts dictionary and weights dictionary.
    Returns 0 if there are no recorded occurrences.
    """
    total_occurrences = sum(counts.values())  # Total number of occurrences
    if total_occurrences == 0:
        return 0

    weighted_sum = sum(weights.get(category, 0) * count for category, count in counts.items())
    
    return weighted_sum / total_occurrences

def write_all_counts_to_csv(bias_counts, factuality_counts, credibility_counts,
                            bias_weights, factuality_weights, credibility_weights,
                            filename='all_counts.csv'):
    """
    Appends a row to the CSV file containing the timestamp, scores, and counts for
    bias, factuality, and credibility.
    
    The CSV header includes:
      Timestamp, Bias Score, <bias categories...>,
      Factuality Score, <factuality categories...>,
      Credibility Score, <credibility categories...>
    """
    # Check if the file exists to decide whether to write a header.
    file_exists = os.path.isfile(filename)
    
    # Create the header.
    header = (['Timestamp', 'Bias Score'] + list(bias_counts.keys()) +
              ['Factuality Score'] + list(factuality_counts.keys()) +
              ['Credibility Score'] + list(credibility_counts.keys()))
    
    # Gather the current timestamp.
    timestamp = datetime.datetime.now().isoformat()
    
    # Calculate the scores.
    bias_score = calculate_rating(bias_counts, bias_weights)
    factuality_score = calculate_rating(factuality_counts, factuality_weights)
    credibility_score = calculate_rating(credibility_counts, credibility_weights)
    
    # Create the row: timestamp, bias score, bias counts, factuality score, factuality counts,
    # credibility score, credibility counts.
    row = ([timestamp, bias_score] + [bias_counts[k] for k in bias_counts] +
           [factuality_score] + [factuality_counts[k] for k in factuality_counts] +
           [credibility_score] + [credibility_counts[k] for k in credibility_counts])
    
    # Write to the CSV file.
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

def convert_url(url):
    """
    Convert a URL starting with 'http://' or 'https://' to one that starts with 'www.'.
    
    Examples:
      "http://example.com"        -> "www.example.com"
      "https://example.com"       -> "www.example.com"
      "http://www.example.com"    -> "www.example.com"
      "https://www.example.com"   -> "www.example.com"
    """
    # The pattern matches:
    #   ^https?://      -> the string must start with "http://" or "https://"
    #   (?:www\.)?      -> an optional "www." (non-capturing group)
    #   (.*)            -> capture the rest of the URL in group 1
    pattern = r'^https?://(?:www\.)?(.*)'
    # Replace the match with "www." followed by the captured group (the rest of the URL)
    return re.sub(pattern, r'www.\1', url)

def get_root_url(url):
    """
    Extracts the root domain from a given URL.
    Example: https://www.nbcnews.com/politics/... -> https://www.nbcnews.com
    """
    match = re.match(r'^(https?://[^/]+)', url)
    return match.group(1) if match else url 

# Returns a tuple of 4 dictionaries: 
#   1. Scores and their corresponding category 
#   2. Cred Counts
#   3. Fact Counts
#   4. Bias Counts
def get_diet(url): 
    global bias_counts, factuality_counts, credibility_counts  # Explicitly declare global variables

    # Clean and extract root URL
    root_url = get_root_url(url)
    root_url = convert_url(root_url)
    root_url = root_url + "/"

    # Load media_bias.json for matching process
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'backend/media_bias.json')

    try:
        with open(json_path, 'r') as file:
            sources = json.load(file)
    except Exception as e:
        print("Error reading JSON:", e)
        return jsonify({'error': f'Error reading JSON: {str(e)}'}), 500
    
    # Retrieve the corresponding source if URL exists in media_bias.json
    matching_source = next((source for source in sources if source.get('url') == root_url), None)

    if matching_source: 
        bias = matching_source.get('bias')
        factual = matching_source.get('factual')
        credibility = matching_source.get('credibility')

        # Update bias counts 
        if bias in bias_counts: 
            bias_counts[bias] += 1
        
        # Update factuality counts
        if factual in factuality_counts: 
            factuality_counts[factual] += 1
        
        # Update credibility counts
        if credibility in credibility_counts:
            credibility_counts[credibility] += 1
    else: 
        print("Source not found")

    # Write updated counts to CSV
    write_all_counts_to_csv(bias_counts, factuality_counts, credibility_counts,
                            bias_weights, factuality_weights, credibility_weights,
                            filename='all_counts.csv')
    
    # Load the updated CSV file for calculations
    df = pd.read_csv("./all_counts.csv")

    # Extract relevant columns
    bias_columns = list(bias_weights.keys())
    factuality_columns = list(factuality_weights.keys())
    credibility_columns = list(credibility_weights.keys())

    # Compute counts
    bias_counts = df[bias_columns].sum().to_dict()
    factuality_counts = df[factuality_columns].sum().to_dict()
    credibility_counts = df[credibility_columns].sum().to_dict()    

    # Compute weighted scores
    bias_score = sum(df[col].sum() * weight for col, weight in bias_weights.items()) / df.shape[0]
    credibility_score = sum(df[col].sum() * weight for col, weight in credibility_weights.items()) / df.shape[0]
    factuality_score = sum(df[col].sum() * weight for col, weight in factuality_weights.items()) / df.shape[0]

    # Store in a dictionary
    score_dict = {
        "Bias Score": bias_score,
        "Credibility Score": credibility_score,
        "Factuality Score": factuality_score
    }

    # Output results
    print("Bias Counts:", bias_counts)
    print("Factuality Counts:", factuality_counts)
    print("Credibility Counts:", credibility_counts)
    print("Score Dictionary:", score_dict)

    return bias_counts, factuality_counts, credibility_counts, score_dict  

if __name__ == '__main__':
    app.run(debug=True, port=5000)