from flask import Blueprint, request, jsonify
import requests

# Create a blueprint for YouTube Downloader
ytdl_bp = Blueprint('ytdl', __name__)

# URL of your URL shortener API
SHORTENER_API_URL = 'https://combative-sarine-eypz-god-d4cce0fc.koyeb.app/shorten?url='

# Function to shorten URLs using the shortener API
def shorten_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        shortener_response = requests.get(SHORTENER_API_URL + url, headers=headers)
        if shortener_response.status_code == 200:
            short_data = shortener_response.json()
            return short_data.get('short_url')  # Get the shortened URL from the response
        else:
            print(f"Shortener API error: {shortener_response.status_code} {shortener_response.text}")
            return None
    except Exception as e:
        print(f"Error shortening URL: {str(e)}")
        return None

@ytdl_bp.route('/ytdl', methods=['GET'])
def fetch_video_details():
    # Get the YouTube video URL from the query parameter
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    # BetaBotz API URL
    api_url = f"https://api.betabotz.eu.org/api/download/ytmp4?url={video_url}&apikey=eypz-izumi"

    try:
        # Adding headers to prevent 403 errors
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Fetch the data from the external API
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Verify the response structure
            if data.get("status") and "result" in data:
                result = data["result"]

                # Extract and shorten the URLs
                mp3_url = result.get("mp3")
                mp4_url = result.get("mp4")
                shortened_mp3 = shorten_url(mp3_url) or mp3_url  # Fallback to original if shortening fails
                shortened_mp4 = shorten_url(mp4_url) or mp4_url  # Fallback to original if shortening fails

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
                return jsonify({"error": "Invalid API response structure"}), 500

        elif response.status_code == 403:
            return jsonify({"error": "Forbidden: API key may be invalid or server is blocked"}), 403

        else:
            return jsonify({"error": f"Failed to fetch data from API. Status Code: {response.status_code}"}), response.status_code

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
