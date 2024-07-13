import requests
import re
from flask import jsonify

def download_thumbnail(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return {'error': 'Invalid YouTube URL'}, 400, {}

    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'

    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            return response.content, 200, {'Content-Type': 'image/jpeg'}
        else:
            return {'error': 'Failed to fetch thumbnail'}, 500, {}
    except Exception as e:
        return {'error': str(e)}, 500, {}

def extract_video_id(url):
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None
