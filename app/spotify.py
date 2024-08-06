# app/spotify.py
from flask import Blueprint, jsonify, request
import requests

spotify_bp = Blueprint('spotify', __name__)
SPOTIFY_SEARCH_API_URL = "https://api.maher-zubair.tech/search/spotify?q="

@spotify_bp.route('/spotify', methods=['GET'])
def search_spotify():
    query = request.args.get('search')

    if not query:
        return jsonify({'error': 'Missing query parameter `search`'}), 400

    try:
        response = requests.get(f"{SPOTIFY_SEARCH_API_URL}{query}")
        if response.status_code == 200:
            data = response.json()
            results = []
            for item in data.get('tracks', {}).get('items', []):
                track_info = {
                    'title': item['name'],
                    'artist': ', '.join(artist['name'] for artist in item['artists']),
                    'album': item['album']['name'],
                    'link': item['external_urls']['spotify'],
                }
                results.append(track_info)
            return jsonify(results)
        else:
            return jsonify({'error': 'Failed to fetch data from external API'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
