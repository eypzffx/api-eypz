from flask import Blueprint, request, jsonify
import requests
import re

pin_bp = Blueprint('pin', __name__)

@pin_bp.route('/pin', methods=['GET'])
def pinterest_downloader():
    url = request.args.get('url')
    
    if not url:
        return jsonify({
            "creator": "Eypz God",
            "status": "error",
            "message": "No URL provided"
        }), 400
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({
                "creator": "Eypz God",
                "status": "error",
                "message": "Failed to retrieve the page"
            }), 400
        
        # This regex captures the full URL ending in jpg, mp4, or m3u8
        matches = re.findall(r'https://v1\.pinimg\.com/\S+\.(?:jpg|mp4|m3u8)', response.text)
        if not matches:
            return jsonify({
                "creator": "Eypz God",
                "status": "error",
                "message": "Media URLs not found"
            }), 404
        
        media_urls = {f"url{i+1}": match for i, match in enumerate(matches)}
        
        result = {
            "creator": "Eypz God",
            "status": "success",
            "media_urls": media_urls
        }
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            "creator": "Eypz God",
            "status": "error",
            "message": str(e)
        }), 500
