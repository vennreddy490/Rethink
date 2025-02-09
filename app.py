from flask import Flask, render_template, redirect, request
from backend import updated_news_api, debrief
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/app", methods=["POST"])
def build_app():

	main_url = request.get_json()
	title = "Trump executive order to South Africa"
	refined_query = updated_news_api.extract_keywords(title)
	updated_news_api.refined_query(title)
	news_api_key = os.getenv("NEWS_API_KEY")
	articles = updated_news_api.get_news(news_api_key, refined_query)
	
	updated_news_api.display_news(articles)

	summary = "CNN has highlighted prior safety concerns, reporting that in the three years leading up to the crash, pilots had reported near-misses with helicopters at Reagan National Airport. (cnn.com) Reuters provided detailed information on the investigation's progress, including the identification of the soldiers involved and preliminary data suggesting that the helicopter may have been flying above its designated altitude at the time of the collision. (reuters.com) CBS News has focused on the technical aspects of the investigation, reporting that both the plane's black boxes have been recovered and are being analyzed to determine the cause of the crash. (cbs.com)"
	sources = [{"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}, {"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}]
	summary_sources = [{"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}]
	main_source = {"name": "CNN", "image_url": "URL", "article_url": "URL", "date":"2/7/2025", "factuality":"High", "bias":"Center Left", "credibility":"High"}
	media_diet = {}

	return render_template("./testingbase.html", summary=summary, summary_sources=summary_sources, sources=sources, main_source=main_source, media_diet=media_diet)

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)