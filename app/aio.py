from flask import Blueprint, request, jsonify
import requests
import os

aio_bp = Blueprint('aio', __name__)

@aio_bp.route('/aio', methods=['GET'])
def aio():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    # Load API key from environment variables
    api_key = os.getenv('API_KEY')

    # Build the request URL with the new API endpoint
    request_url = f'https://api.betabotz.eu.org/api/download/igdowloader?url={url}&apikey={api_key}'

    try:
        # Send the request to the external server
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Get the JSON response from the external server
        data = response.json()

        # Extract the 'message' field and get thumbnail and all _url
        messages = data.get("message", [])
        thumbnail_url = messages[0].get("thumbnail") if messages else None  # Get the first thumbnail URL
        media_urls = [message.get("_url") for message in messages if message.get("_url")]

        # Prepare the result with 'creator', 'wm', 'thumbnail', and 'medias'
        result = {
            "creator": "Eypz God",
            "wm": "powered by Eypz",
            "thumbnail": thumbnail_url,
            "medias": media_urls
        }

        # Return the modified JSON response
        return jsonify(result)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
