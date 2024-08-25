# app/ytdl.py

from flask import Blueprint, request, jsonify
import requests
import os

# Define the Blueprint
ytdl_bp = Blueprint('ytdl', __name__)

@ytdl_bp.route('/ytdl', methods=['GET'])
def ytdl():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    # Load API key from environment variables
    api_key = os.getenv('API_KEY', 'eypz-izumi')  # Default to 'eypz-izumi' if not set

    # Build the request URL
    request_url = f'https://api.betabotz.eu.org/api/download/yt?url={url}&apikey={api_key}'

    try:
        # Send the request to the external server
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Get the JSON response from the external server
        data = response.json()

        # Modify the 'creator' field to 'Eypz God'
        result = {
            "status": data.get("status"),
            "creator": "Eypz God",
            "result": data.get("result", {})
        }

        # Return the modified JSON response
        return jsonify(result)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
