from flask import Blueprint, request, jsonify
import yt_dlp

yt_bp = Blueprint('yt_bp', __name__)

def search_youtube(query):
    ydl_opts = {
        'default_search': 'ytsearch',
        'max_downloads': 1,
        'quiet': True,
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in result:
            video = result['entries'][0]
            return {
                "title": video['title'],
                "author": video['uploader'],
                "url": f"https://www.youtube.com/watch?v={video['id']}",
                "download_url": get_download_url(video['id'])  # Generate the download URL
            }
    return None

def get_download_url(video_id):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
        return info.get('url')

@yt_blueprint.route('/ytdl/video', methods=['GET'])
def get_video_info():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    video_info = search_youtube(query)
    if not video_info:
        return jsonify({"error": "No video found"}), 404

    return jsonify({
        "Creator": "Eypz",
        "result": video_info
    })
