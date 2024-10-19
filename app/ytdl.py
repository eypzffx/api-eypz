from flask import Blueprint, request, jsonify
import yt_dlp
from concurrent.futures import ThreadPoolExecutor
import time

# Create a blueprint for YouTube Downloader
ytdl_bp = Blueprint('ytdl', __name__)

# Proxy details
proxy_ip = "103.66.233.137"
proxy_port = "4145"
proxy_protocol = "socks4"

# Simple in-memory cache
cache = {}

# Function to get video information
def get_video_info(video_url):
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,  # Avoid downloading playlists
        'proxy': f'{proxy_protocol}://{proxy_ip}:{proxy_port}',  # Using the SOCKS4 proxy
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)  # Extract info without downloading
        video_info = {
            'title': info.get('title'),
            'duration': info.get('duration'),  # Duration in seconds
            'author': info.get('uploader'),
            'download_url': info['url']
        }
    return video_info

# Route for YouTube downloader
@ytdl_bp.route('/ytdl', methods=['GET'])
def youtube_download_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    # Check if result is cached
    if url in cache:
        return jsonify({"success": True, **cache[url]})
    
    # Use ThreadPoolExecutor to handle video info extraction in a separate thread
    with ThreadPoolExecutor() as executor:
        future = executor.submit(get_video_info, url)
        try:
            video_info = future.result(timeout=10)  # Wait up to 10 seconds for the result
            # Cache the result
            cache[url] = {
                "title": video_info['title'],
                "duration": video_info['duration'],
                "author": video_info['author'],
                "download_url": video_info['download_url']
            }
            return jsonify({
                "success": True,
                "title": video_info['title'],
                "duration": video_info['duration'],
                "author": video_info['author'],
                "download_url": video_info['download_url']
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
