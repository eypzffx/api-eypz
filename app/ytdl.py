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

    # Updated API endpoint for downloading YouTube media
    api_endpoint = "https://api.betabotz.eu.org/api/download/ytmp4"
    api_key = "eypz-izumi"
    
    # Request to the external API with URL and API key as parameters
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
    description = result.get('description')
    video_id = result.get('id')
    thumbnail = result.get('thumb')
    source = result.get('source')
    duration = result.get('duration')
    
    # Get the original MP4 link
    original_mp4_link = result.get('mp4')

    # Shorten the MP4 link
    shorten_response = requests.get("https://api.eypz.c0m.in/shorten", params={'url': original_mp4_link})
    if shorten_response.status_code == 200:
        shorten_data = shorten_response.json()
        short_url = shorten_data.get('short_url')
    else:
        return jsonify({"status": False, "message": "Failed to shorten the URL."}), 400

    # Return the extracted information with the shortened MP4 link
    return jsonify({
        "status": True,
        "code": 200,
        "creator": "Eypz",
        "result": {
            "title": title,
            "description": description,
            "video_id": video_id,
            "thumbnail": thumbnail,
            "source": source,
            "duration": duration,
            "mp4_link": short_url  # Use the shortened URL here
        }
    })

# Error handler for not found routes
@ytdl_bp.errorhandler(404)
def not_found_error(error):
    return jsonify({"status": False, "message": "Route not found."}), 404
