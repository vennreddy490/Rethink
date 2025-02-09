# import os
# import json
# from flask import Blueprint, request, jsonify
# from flask_cors import cross_origin

# diet_evaluation_bp = Blueprint('diet_evaluation', __name__)

# @diet_evaluation_bp.route('/find_source', methods=['POST'])
# @cross_origin()  # This decorator will handle CORS including preflight OPTIONS
# def find_source():
#     print("find_source endpoint hit!")
#     data = request.get_json()
#     print("Received data:", data)
    
#     url = data.get('url')
#     print("URL from request:", url)
    
#     if not url:
#         return jsonify({'error': 'No URL provided'}), 400

#     # Build the full path to media_bias.json (located in the same directory as this file)
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     json_path = os.path.join(current_dir, 'media_bias.json')
#     print("Looking for JSON file at:", json_path)

#     try:
#         with open(json_path, 'r') as file:
#             sources = json.load(file)
#     except Exception as e:
#         print("Error reading JSON:", e)
#         return jsonify({'error': f'Error reading JSON: {str(e)}'}), 500

#     print("JSON file loaded. Contents:", sources)
    
#     matching_source = next((source for source in sources if source.get('url') == url), None)
#     print("Matching source:", matching_source)
    
#     return jsonify({'member': matching_source}), 200
