# app/pin.py

from flask import Blueprint, jsonify, request
import requests
from bs4 import BeautifulSoup
import re

pin_bp = Blueprint('pin', __name__)

def extract_media_url(soup):
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string:
            # Use regex to find JSON-like structure
            video_data_match = re.search(r'videoList720P":\s*({.*?})\s*}', script.string)
            if video_data_match:
                video_data_str = video_data_match.group(1)
                try:
                    # Extract the thumbnail and URL from the found structure
                    thumbnail_match = re.search(r'"thumbnail":"(https://i.pinimg.com/[^"]+)', video_data_str)
                    url_match = re.search(r'"url":"(https://v1.pinimg.com/[^"]+\.mp4)', video_data_str)
                    if thumbnail_match and url_match:
                        return {
                            "thumbnail": thumbnail_match.group(1),
                            "media_url": url_match.group(1)
                        }
                except (AttributeError, KeyError):
                    continue

    # Fallback if video not found
    return None

@pin_bp.route('/pin', methods=['GET'])
def get_pinterest_media_url():
    pin_url = request.args.get('url')
    if not pin_url:
        return jsonify({"error": "URL parameter is required"}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(pin_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    media_data = extract_media_url(soup)
    if media_data:
        return jsonify(media_data)
    else:
        return jsonify({"error": "Failed to extract media URL"}), 500
