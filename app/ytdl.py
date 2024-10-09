
from flask import Blueprint, request, jsonify, send_file
import requests
import os

# Create a blueprint for YouTube Downloader
ytdl_bp = Blueprint('ytdl', __name__)

# Define the route for downloading YouTube media
@ytdl_bp.route('/ytdl', methods=['GET'])
def download_youtube():
    # Get URL from request arguments
    url = request.args.get('url')
    if not url:
        return jsonify({"status": False, "message": "URL parameter is missing."}), 400

    # Updated API endpoint for downloading YouTube media
    api_endpoint = "https://api.betabotz.eu.org/api/download/ytmp4"
    api_key = "eypz-izumi"
    
    # Request to the external API with URL and API key as parameters
    response = requests.get(api_endpoint, params={'url': url, 'apikey': api_key})
    
    # Check if the API request was successful
    if response.status_code != 200:
        return jsonify({"status": False, "message": "Failed to fetch data from API."}), response.status_code
    
    data = response.json()

    # Check the status of the response
    if not data.get('status'):
        return jsonify({"status": False, "message": "API response indicates failure."}), 400
    
    # Extract media information
    result = data.get('result', {})
    title = result.get('title')
    description = result.get('description')
    video_id = result.get('id')
    thumbnail = result.get('thumb')
    source = result.get('source')
    duration = result.get('duration')
    
    # Get the original MP4 link
    original_mp4_link = result.get('mp4')
    if not original_mp4_link:
        return jsonify({"status": False, "message": "MP4 link not found."}), 400

    # Download the MP4 file
    video_response = requests.get(original_mp4_link, stream=True)
    if video_response.status_code != 200:
        return jsonify({"status": False, "message": "Failed to download video."}), 400

    # Define the upload directory and filename
    upload_directory = '../upload'
    video_file_name = f"{video_id}.mp4"
    video_file_path = os.path.join(upload_directory, video_file_name)

    # Save the video to the specified directory
    with open(video_file_path, 'wb') as f:
        for chunk in video_response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Construct the new URL for the uploaded video
    new_video_link = f"https://api.eypz.c0m.in/upload/file/{video_file_name}"

    # Return the extracted information with the new video link
    return jsonify({
        "status": True,
        "code": 200,
        "creator": "Eypz",
        "result": {
            "title": title,
            "description": description,
            "video_id": video_id,
            "thumbnail": thumbnail,
            "source": source,
            "duration": duration,
            "mp4_link": new_video_link
        }
    })

# Define a route to serve the uploaded video
@ytdl_bp.route('/upload/file/<filename>', methods=['GET'])
def serve_video(filename):
    upload_directory = '../upload'
    video_file_path = os.path.join(upload_directory, filename)

    # Check if the file exists
    if not os.path.exists(video_file_path):
        return jsonify({"status": False, "message": "File not found."}), 404
    
    return send_file(video_file_path, as_attachment=True)

# Error handler for not found routes
@ytdl_bp.errorhandler(404)
def not_found_error(error):
    return jsonify({"status": False, "message": "Route not found."}), 404
