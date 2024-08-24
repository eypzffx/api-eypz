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

    # Build the request URL
    request_url = f'https://api.betabotz.eu.org/api/download/allin?url={url}&apikey={api_key}'

    try:
        # Send the request to the external server
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Get the JSON response from the external server
        data = response.json()

        # Extract the 'medias' field and set 'creator' to 'Eypz God'
        result = {
            "creator": "Eypz God",
            "medias": data.get("result", {}).get("medias", [])
        }

        # Return the modified JSON response
        return jsonify(result)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
