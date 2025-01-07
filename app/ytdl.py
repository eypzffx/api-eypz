from flask import Blueprint, request, jsonify
import requests
from pytube import YouTube  # For fetching video details

# Create a blueprint for YouTube Downloader
ytdl_bp = Blueprint('ytdl', __name__)

# Method to fetch video details using pytube
def fetch_video_details_pytube(video_url):
    try:
        # Create a YouTube object using pytube
        yt = YouTube(video_url)

        # Extract details from the YouTube object
        video_details = {
            'title': yt.title,
            'description': yt.description,
            'thumbnail': yt.thumbnail_url,
            'duration': yt.length,  # Duration in seconds
            'id': yt.video_id,
            'source_url': video_url
        }

        return video_details
    except Exception as e:
        return None

@ytdl_bp.route('/ytdl', methods=['GET'])
def fetch_video_details():
    # Get the YouTube video URL from the query parameter
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    # Construct the direct API URLs for audio and video downloads
    api_audio_url = f"https://api.betabotz.eu.org/api/download/get-YoutubeResult?url={video_url}&type=audio&xky=xT%C2%8CTzK%C2%87N7K%7BS%C2%8CS%C2%82NyMuM"
    api_video_url = f"https://api.betabotz.eu.org/api/download/get-YoutubeResult?url={video_url}&type=video&xky=xT%C2%8CTzK%C2%87N7K%7BS%C2%8CS%C2%82NyMuM"

    # Fetch video details using pytube
    video_details_pytube = fetch_video_details_pytube(video_url)

    if video_details_pytube is None:
        return jsonify({"error": "Failed to fetch video details"}), 500

    # Return the final result by merging video details
    return jsonify({
        "creator": "Eypz",  # Set the creator name
        "title": video_details_pytube['title'],
        "description": video_details_pytube['description'],
        "thumbnail": video_details_pytube['thumbnail'],
        "duration": video_details_pytube['duration'],
        "id": video_details_pytube['id'],
        "source_url": video_details_pytube['source_url'],
        "download_links": {
            "audio": api_audio_url,
            "video": api_video_url
        }
    })
