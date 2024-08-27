from flask import Blueprint, request, jsonify
from youtubesearchpython import VideosSearch

search_bp = Blueprint('search', __name__)

def format_duration(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins}:{secs:02d}"

def search_youtube(query):
    search = VideosSearch(query, limit=20)
    result = search.result()
    videos = result['result']
    return [
        {
            "title": video['title'],
            "author": video['channel']['name'],
            "duration": format_duration(int(video['duration'].split(':')[0]) * 60 + int(video['duration'].split(':')[1])),
            "url": video['link']
        }
        for video in videos
    ]

@search_bp.route('/ytdl/search', methods=['GET'])
def search_videos():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    video_list = search_youtube(query)
    if not video_list:
        return jsonify({"error": "No videos found"}), 404

    return jsonify({
        "Creator": "Eypz",
        "results": video_list
    })
