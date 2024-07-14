# app/search.py
from flask import Blueprint, jsonify, request
from info.youtube import search_youtube_videos

search_bp = Blueprint('search', __name__)

@search_bp.route('/youtube', methods=['GET'])
def search_youtube():
    query = request.args.get('search')

    if not query:
        return jsonify({'error': 'Missing search query parameter `search`'}), 400

    try:
        results, status_code = search_youtube_videos(query)
        if status_code == 200:
            return jsonify(results)
        else:
            return jsonify(results), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
