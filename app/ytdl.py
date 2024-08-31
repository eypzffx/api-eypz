from flask import Blueprint, request, jsonify
import yt_dlp

# Create the blueprint
ytdl_bp = Blueprint('ytdl', __name__)

def get_video_info(url):
    # Configure yt-dlp options to get the highest quality video and audio
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Combine best video and audio quality
        'noplaylist': True,
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Extracting info for URL: {url}")  # Debugging: Print URL being processed
            info = ydl.extract_info(url, download=False)
            
            # For search results, extract the first video
            if 'entries' in info:
                info = info['entries'][0]  # Get the first search result
                print(f"First search result info: {info}")

            # Find the best video format URL
            formats = info.get('formats', [])
            video_url = None
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':  # Ensure both video and audio
                    video_url = f.get('url')
                    break

            title = info.get('title', 'Unknown Title')
            description = info.get('description', 'No description available.')
            author = info.get('uploader', 'Unknown Author')
            thumbnail = info.get('thumbnail', 'No thumbnail available.')

            if not video_url:
                raise ValueError("Video URL not found in extracted info.")

            print(f"Video title: {title}, Video URL: {video_url}, Author: {author}, Description: {description[:100]}..., Thumbnail: {thumbnail}")  # Debugging: Print extracted info
            return title, video_url, description, author, thumbnail

    except Exception as e:
        print(f"Error extracting video info: {e}")  # Debugging: Print error message
        raise e

@ytdl_bp.route('/ytdl', methods=['GET'])
def youtube_download_link():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Please provide a 'url' parameter"}), 400
    
    # If the URL is a text query, search on YouTube
    if not url.startswith("http"):
        url = f"ytsearch:{url}"
        print(f"Converted text to search query: {url}")  # Debugging: Print converted search query

    try:
        title, video_url, description, author, thumbnail = get_video_info(url)
        return jsonify({
            "message": f"Here is the download link for '{title}'",
            "download_url": video_url,
            "title": title,
            "author": author,
            "description": description,
            "thumbnail": thumbnail,
            "creator": "Eypz God"
        })
    except Exception as e:
        print(f"Internal Server Error: {e}")  # Debugging: Print exception
        return jsonify({"error": str(e)}), 500
