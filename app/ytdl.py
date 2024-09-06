from flask import Blueprint, request, jsonify
import requests

# Create a blueprint for YouTube Downloader
ytdl_bp = Blueprint('ytdl', __name__)

# Define the route for downloading YouTube media
@ytdl_bp.route('/ytdl', methods=['GET'])
def download_youtube():
    # Get URL from request arguments
    url = request.args.get('url')
    if not url:
        return jsonify({"status": False, "message": "URL parameter is missing."}), 400

    # API endpoint to download YouTube media
    api_endpoint = "https://api.betabotz.eu.org/api/download/allin"
    api_key = "eypz-izumi"
    
    # Request to the external API
    response = requests.get(api_endpoint, params={'url': url, 'apikey': api_key})
    
    # Check if the API request was successful
    if response.status_code != 200:
        return jsonify({"status": False, "message": "Failed to fetch data from API."}), response.status_code
    
    data = response.json()

    # Check the status of the response
    if not data.get('status'):
        return jsonify({"status": False, "message": "API response indicates failure."}), 400
    
    # Extract media information
    result = data.get('result', {})
    title = result.get('title')
    thumbnail = result.get('thumbnail')
    duration = result.get('duration')
    medias = result.get('medias', [])

    # Return the extracted information
    return jsonify({
        "status": True,
        "code": 200,
        "creator": "Eypz",
        "result": {
            "title": title,
            "thumbnail": thumbnail,
            "duration": duration,
            "medias": medias
        }
    })

# Error handler for not found routes
@ytdl_bp.errorhandler(404)
def not_found_error(error):
    return jsonify({"status": False, "message": "Route not found."}), 404
