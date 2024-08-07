from flask import Blueprint, jsonify, request
import requests

spotify_bp = Blueprint('spotify', __name__)

# Set your API key and external API URL
EXTERNAL_API_URL = 'https://api.betabotz.eu.org/api/download/spotify'
API_KEY = 'eypz-izumi'

@spotify_bp.route('/spotify', methods=['GET'])
def get_spotify_track_info():
    song_url = request.args.get('url')
    if not song_url:
        return jsonify({"status": False, "code": 400, "error": "URL parameter is required"}), 400

    try:
        # Request to the external API
        response = requests.get(EXTERNAL_API_URL, params={'url': song_url, 'apikey': API_KEY})
        response_data = response.json()

        # Check if the external API call was successful
        if response.status_code != 200 or not response_data.get('status'):
            return jsonify({"status": False, "code": 500, "error": response_data.get('error', 'Failed to fetch data')}), 500

        # Map the response data to your desired format
        track_data = {
            "thumbnail": response_data['result']['data']['thumbnail'],
            "title": response_data['result']['data']['title'],
            "artist": {
                "name": response_data['result']['data']['artist']['name'],
                "external_urls": {
                    "spotify": response_data['result']['data']['artist']['external_urls']['spotify']
                },
                "href": response_data['result']['data']['artist']['href'],
                "id": response_data['result']['data']['artist']['id'],
                "type": response_data['result']['data']['artist']['type'],
                "uri": response_data['result']['data']['artist']['uri']
            },
            "duration": response_data['result']['data']['duration'],
            "preview": response_data['result']['data']['preview'],
            "url": response_data['result']['data']['url']
        }

        return jsonify({
            "status": True,
            "code": 200,
            "creator": "Eypz God",
            "result": {
                "creator": "Eypz God",
                "status": True,
                "data": track_data
            }
        }), 200

    except requests.RequestException as e:
        return jsonify({"status": False, "code": 500, "error": "Request error: " + str(e)}), 500
    except Exception as e:
        return jsonify({"status": False, "code": 500, "error": str(e)}), 500
