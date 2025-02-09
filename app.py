from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS
import json
import os 
import re
app = Flask(__name__)

# Enable CORS for all routes, allowing any origin.
CORS(app)
@app.route("/")
def home():
    return render_template("testingbase.html")

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

@app.route('/find-source', methods=['POST'])
def find_source(): 
    data = request.get_json()
    received_site = data.get("site", "No site provided")

    # Convert URL to uppercase
    modified_site = received_site.upper()

    # Extract root domain
    root_site = get_root_url(received_site)
    root_site = convert_url(root_site)
    root_site = root_site + "/"
    print("This should be right:", root_site)
    # Print to Flask terminal for debugging
    print(f"✅ Page Loaded - Received URL: {received_site} | Modified: {modified_site} | Root: {root_site}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'backend/media_bias.json')
    print("Looking for JSON file at:", json_path)

    try:
        with open(json_path, 'r') as file:
            sources = json.load(file)
    except Exception as e:
        print("Error reading JSON:", e)
        return jsonify({'error': f'Error reading JSON: {str(e)}'}), 500
    
    matching_source = next((source for source in sources if source.get('url') == root_site), None)
    print("Matching source:", matching_source)
    print(sources[0])
  
    return jsonify({
        "original_site": received_site,
        "modified_site": modified_site,
        "root_site": root_site,
        "message": "Page load detected successfully!"
    })

    



    # print("find_source endpoint hit!")
    # data = request.get_json()
    # print("Received data:", data[0])
    
    # url = data.get('url')
    # print("URL from request:", url)
    
    # if not url:
    #     return jsonify({'error': 'No URL provided'}), 400

    # Build the full path to media_bias.json (located in the same directory as this file)
    

    # try:
    #     with open(json_path, 'r') as file:
    #         sources = json.load(file)
    # except Exception as e:
    #     print("Error reading JSON:", e)
    #     return jsonify({'error': f'Error reading JSON: {str(e)}'}), 500

    # # print("JSON file loaded. Contents:", sources)
    
    # matching_source = next((source for source in sources if source.get('url') == url), None)
    # print("Matching source:", matching_source)
    
    # return jsonify({'member': matching_source}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
