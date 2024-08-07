from flask import Blueprint, jsonify, request
import requests

# Create a Blueprint for the Spotify search
spotifys_bp = Blueprint('spotify', __name__)

# External API URL for Spotify search
EXTERNAL_API_URL = 'https://api.maher-zubair.tech/search/spotify'

@spotify_bp.route('/spotify', methods=['GET'])
def search_spotify():
    query = request.args.get('search')
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400

    try:
        # Request to the external API
        response = requests.get(f'{EXTERNAL_API_URL}?q={query}')
        response_data = response.json()

        # Check if the external API call was successful
        if response.status_code != 200:
            return jsonify({'error': 'Failed to retrieve data from Spotify API'}), response.status_code

        # Modify the response data with the developer name
        response_data['developer'] = 'Eypz God'

        return jsonify({
            "status": True,
            "code": 200,
            "creator": "Eypz God",
            "result": response_data
        }), 200

    except requests.RequestException as e:
        return jsonify({"status": False, "code": 500, "error": "Request error: " + str(e)}), 500
    except Exception as e:
        return jsonify({"status": False, "code": 500, "error": str(e)}), 500
