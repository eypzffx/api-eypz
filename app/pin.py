from flask import Blueprint, request, jsonify
import requests
import re

pin_bp = Blueprint('pin', __name__)

@bp.route('/pin', methods=['GET'])
def pinterest_downloader():
    url = request.args.get('url')
    
    if not url:
        return jsonify({
            "creator": "Eypz God",
            "status": "error",
            "message": "No URL provided"
        }), 400
    
    try:
        # Perform a GET request to the provided URL
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({
                "creator": "Eypz God",
                "status": "error",
                "message": "Failed to retrieve the page"
            }), 400
        
        # Extract the media URL using regex
        match = re.search(r'https://v1\.pinimg\.com/\S+\.(jpg|mp4|m3u8)', response.text)
        if not match:
            return jsonify({
                "creator": "Eypz God",
                "status": "error",
                "message": "Media URL not found"
            }), 404
        
        media_url = match.group(0)
        # Format the response to be more informative
        result = {
            "creator": "Eypz God",
            "status": "success",
            "media_url": media_url
        }
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            "creator": "Eypz God",
            "status": "error",
            "message": str(e)
        }), 500
