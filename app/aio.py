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

        # Debugging: print out the response data to understand its structure
        print(data)

        # Extract the 'message' field and get thumbnail and all _url
        messages = data.get("message", [])
        if not messages:
            return jsonify({'error': 'No messages found in response'}), 500
        
        thumbnail_url = messages[0].get("thumbnail") if messages else None

        # Extract and deduplicate media URLs
        media_urls = list(set(message.get("_url") for message in messages if message.get("_url")))

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
    except ValueError as e:
        return jsonify({'error': 'Invalid response format'}), 500
