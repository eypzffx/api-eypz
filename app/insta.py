from flask import Flask, Blueprint, request, jsonify
import instaloader
import re

# Create a Blueprint
insta_bp = Blueprint('insta', __name__)

def download_instagram_media(url):
    loader = instaloader.Instaloader()
    media_urls = []

    try:
        # Handle post media
        shortcode_match = re.search(r'instagram.com/p/([^/]+)/', url)
        if shortcode_match:
            shortcode = shortcode_match.group(1)
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            if post.typename == 'GraphImage':
                media_urls.append(post.url)
            elif post.typename == 'GraphVideo':
                media_urls.append(post.video_url)
            elif post.typename == 'GraphSidecar':
                for sidecar_node in post.get_sidecar_nodes():
                    if sidecar_node.is_video:
                        media_urls.append(sidecar_node.video_url)
                    else:
                        media_urls.append(sidecar_node.display_url)
    except Exception as e:
        print(f"Error downloading post: {e}")
    
    try:
        # Handle story media
        if 'stories' in url:
            username_match = re.search(r'instagram.com/stories/(.*?)/', url)
            if username_match:
                username = username_match.group(1)
                profile = instaloader.Profile.from_username(loader.context, username)
                stories = loader.get_stories(userids=[profile.userid])
                for story in stories:
                    for item in story.get_items():
                        if item.is_video:
                            media_urls.append(item.video_url)
                        else:
                            media_urls.append(item.url)
    except Exception as e:
        print(f"Error downloading stories: {e}")

    return media_urls

@insta_bp.route('/insta_story', methods=['GET'])
def insta_downloader():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    media_urls = download_instagram_media(url)
    if media_urls:
        return jsonify({"media_urls": media_urls}), 200
    else:
        return jsonify({"error": "Failed to download media"}), 500

# Create the Flask app
app = Flask(__name__)
app.register_blueprint(insta_bp)

if __name__ == '__main__':
    app.run(debug=True)
