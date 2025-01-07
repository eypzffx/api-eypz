from flask import Blueprint, request, jsonify
import requests

# Create a blueprint for YouTube Downloader
ytdl_bp = Blueprint('ytdl', __name__)

# URL of your URL shortener API
SHORTENER_API_URL = 'https://combative-sarine-eypz-god-d4cce0fc.koyeb.app/shorten?url='

# Function to shorten URLs using the shortener API
def shorten_url(url):
    try:
        shortener_response = requests.get(SHORTENER_API_URL + url)
        if shortener_response.status_code == 200:
            short_data = shortener_response.json()
            return short_data.get('short_url')  # Get the shortened URL from the response
        else:
            return None
    except Exception as e:
        return None

@ytdl_bp.route('/ytdl', methods=['GET'])
def fetch_video_details():
    # Get the YouTube video URL from the query parameter
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    # Your BetaBotz API URL
    api_url = f"https://api.betabotz.eu.org/api/download/ytmp4?url={video_url}&apikey=eypz-izumi"

    # Fetch the data from the external API
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Verify the structure of the response
        if data.get("status") and "result" in data:
            result = data["result"]

            # Extract and shorten the URLs
            mp3_url = result.get("mp3")
            mp4_url = result.get("mp4")
            shortened_mp3 = shorten_url(mp3_url) or mp3_url  # Fall back to original if shortening fails
            shortened_mp4 = shorten_url(mp4_url) or mp4_url  # Fall back to original if shortening fails

            # Prepare the video details response
            video_details = {
                "creator": result.get("creator", "Eypz"),  # Use API creator or fallback
                "title": result.get("title"),
                "description": result.get("description"),
                "id": result.get("id"),
                "thumbnail": result.get("thumb"),
                "source_url": result.get("source"),
                "duration": result.get("duration"),
                "download_links": {
                    "mp3": shortened_mp3,
                    "mp4": shortened_mp4
                }
            }
            return jsonify(video_details)
        else:
            # Handle cases where the structure is invalid or status is False
            return jsonify({"error": "Invalid API response structure"}), 500
    else:
        # Log the response for debugging
        return jsonify({"error": f"API call failed with status code {response.status_code}"}), response.status_code
