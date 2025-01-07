from flask import Blueprint, request, jsonify
import requests
import yt_dlp  # For fetching video details

# Create a blueprint for YouTube Downloader
ytdl_bp = Blueprint('ytdl', __name__)

# URL of your URL shortener API
SHORTENER_API_URL = 'https://combative-sarine-eypz-god-d4cce0fc.koyeb.app/shorten?url='

# Function to shorten URLs using the shortener API
def shorten_url(url):
    try:
        shortener_response = requests.get(SHORTENER_API_URL + url)
        if shortener_response.status_code == 200:
            short_data = shortener_response.json()
            return short_data.get('short_url')  # Get the shortened URL from the response
        else:
            return None
    except Exception as e:
        return None

# New method to fetch video details using yt-dlp
def fetch_video_details_yt_dlp(video_url):
    try:
        ydl_opts = {
            'quiet': True,  # Suppress unnecessary output
            'force_generic_extractor': True,  # Use a generic extractor
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            return {
                'title': info_dict.get('title'),
                'description': info_dict.get('description'),
                'thumbnail': info_dict.get('thumbnail'),
                'duration': info_dict.get('duration'),
                'id': info_dict.get('id'),
                'source_url': video_url,
            }
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

    # Shorten the URLs
    shortened_audio = shorten_url(api_audio_url) or api_audio_url  # Fall back to the original if shortening fails
    shortened_video = shorten_url(api_video_url) or api_video_url  # Fall back to the original if shortening fails

    # Fetch additional video details using yt-dlp
    video_details_yt_dlp = fetch_video_details_yt_dlp(video_url)

    if video_details_yt_dlp is None:
        return jsonify({"error": "Failed to fetch video details"}), 500

    # Return the final result by merging video details
    return jsonify({
        "creator": "Eypz",  # Set the creator name
        "title": video_details_yt_dlp['title'],
        "description": video_details_yt_dlp['description'],
        "thumbnail": video_details_yt_dlp['thumbnail'],
        "duration": video_details_yt_dlp['duration'],
        "id": video_details_yt_dlp['id'],
        "source_url": video_details_yt_dlp['source_url'],
        "download_links": {
            "audio": shortened_audio,
            "video": shortened_video
        }
    })
