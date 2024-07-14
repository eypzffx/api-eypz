# app/youtube.py
from flask import Blueprint, jsonify, request
from stalking.youtube import download_thumbnail  # Assuming the function is in stalking.youtube

youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route('/download_thumbnail', methods=['GET'])
def download_youtube_thumbnail():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    thumbnail_url, error = download_thumbnail(video_url)
    if error:
        return jsonify({'error': error}), 500

    return jsonify({'thumbnail_url': thumbnail_url})
