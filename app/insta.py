from flask import Blueprint, request, jsonify
import instaloader
import os

# Blueprint for Instagram routes
insta_bp = Blueprint('insta', __name__)

# Create an instaloader object
loader = instaloader.Instaloader()

# Path to the session file
session_file = os.path.join(os.path.dirname(__file__), 'session-insta')

# Load session from the session-insta file
if os.path.exists(session_file):
    try:
        loader.load_session_from_file(username=None, filename=session_file)
        print("Session loaded successfully!")
    except Exception as e:
        print(f"Failed to load session: {str(e)}")
else:
    print("Session file not found. Please log in and save the session.")

@insta_bp.route('/insta', methods=['GET'])
def download_instagram():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    shortcode = url.split('/')[-2]
    try:
        # Fetch the post using its shortcode
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Collect all media URLs
        media_urls = []
        if post.is_video:
            media_urls.append(post.video_url)
        else:
            media_urls.append(post.url)

        # Add additional media URLs if the post is a carousel
        for node in post.get_sidecar_nodes():
            if node.is_video:
                media_urls.append(node.video_url)
            else:
                media_urls.append(node.display_url)  # Use display_url for images

        if media_urls:
            return jsonify({"message": "Success", "media_urls": media_urls}), 200
        else:
            return jsonify({"error": "No media found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
