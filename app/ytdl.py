from flask import Blueprint, request, jsonify
import requests

# Create a blueprint for YouTube Downloader and IP Whitelisting
api_bp = Blueprint('api', __name__)

# Define the list of allowed IPs (replace with your actual IP or range)
ALLOWED_IPS = ["<Your Koyeb App IP>"]

# URL for fetching public IP
IP_SERVICE_URL = "https://api.ipify.org"  # You can use other services like ifconfig.me

# Route to get the public IP address of the app
@api_bp.route('/get_ip', methods=['GET'])
def get_ip():
    try:
        # Use an external service to get the public IP address
        response = requests.get(IP_SERVICE_URL)
        if response.status_code == 200:
            return jsonify({"ip": response.text})  # Return the public IP address
        else:
            return jsonify({"error": "Could not retrieve IP"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for the /ytdl API with IP whitelisting
@api_bp.route('/ytdl', methods=['GET'])
def fetch_video_details():
    # Get the client's IP address
    client_ip = request.remote_addr

    # Check if the client IP is whitelisted
    if client_ip not in ALLOWED_IPS:
        return jsonify({"error": "Forbidden: Your IP is not whitelisted"}), 403

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


# Function to shorten URLs using the shortener API
def shorten_url(url):
    try:
        shortener_response = requests.get(f'https://combative-sarine-eypz-god-d4cce0fc.koyeb.app/shorten?url={url}')
        if shortener_response.status_code == 200:
            short_data = shortener_response.json()
            return short_data.get('short_url')  # Get the shortened URL from the response
        else:
            return None
    except Exception as e:
        return None
