from flask import Blueprint, request, jsonify
import requests

# Create a blueprint for YouTube Downloader
ytdl_bp = Blueprint('ytdl', __name__)

# URL of your URL shortener API
SHORTENER_API_URL = 'https://api-test-ajko.onrender.com/shorten?url='

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

        # Extract the relevant details from the 'result' field
        if data['status']:
            mp3_url = data['result']['mp3']
            mp4_url = data['result']['mp4']

            # Shorten the download URLs
            shortened_mp3 = shorten_url(mp3_url) or mp3_url  # Fall back to original if shortening fails
            shortened_mp4 = shorten_url(mp4_url) or mp4_url  # Fall back to original if shortening fails

            video_details = {
                "creator": "Eypz",  # Set the creator name to "Eypz"
                "title": data['result']['title'],
                "description": data['result']['description'],
                "id": data['result']['id'],
                "thumbnail": data['result']['thumb'],
                "source_url": data['result']['source'],
                "duration": data['result']['duration'],
                "download_links": {
                    "mp3": shortened_mp3,
                    "mp4": shortened_mp4
                }
            }
            return jsonify(video_details)  # Return the modified response with shortened URLs
        else:
            return jsonify({"error": "Failed to fetch video details"}), 500
    else:
        return jsonify({"error": "Failed to fetch data from API"}), response.status_code
