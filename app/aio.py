from flask import Blueprint, request, jsonify
import requests

aio_bp = Blueprint('aio', __name__)

@aio_bp.route('/igdl', methods=['GET'])
def aio():
    # Get the URL parameter from the request
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    # Construct the request URL with the API key included
    request_url = f'https://api.betabotz.eu.org/api/download/igdowloader?url={url}&apikey=eypz-izumi'

    try:
        # Send the request to the external server
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Get the JSON response from the external server
        data = response.json()

        # Extract media URLs from the message
        messages = data.get("message", [])
        if not messages:
            return jsonify({'error': 'No messages found in response'}), 500
        
        # Initialize a list to hold media URLs
        media_urls = []

        for message in messages:
            # Check if '_url' exists and add it to the media_urls list
            media_url = message.get("_url")
            if media_url:
                media_urls.append(media_url)

        # Prepare the result in the desired format
        result = {
            "creator": "Eypz",
            "medias": media_urls  # All media URLs in a list format
        }

        # Return the modified JSON response
        return jsonify(result)

    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except ValueError:
        return jsonify({'error': 'Invalid response format'}), 500
