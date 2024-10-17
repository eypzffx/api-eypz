from flask import Blueprint, request, jsonify
import yt_dlp

# Create a blueprint for YouTube Downloader
ytdl_bp = Blueprint('ytdl', __name__)

# Function to get video information
def get_video_info(video_url):
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,  # Avoid downloading playlists
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
    try:
        video_info = get_video_info(url)
        return jsonify({
            "success": True,
            "title": video_info['title'],
            "duration": video_info['duration'],  # Duration is in seconds
            "author": video_info['author'],
            "download_url": video_info['download_url']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
