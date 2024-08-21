from flask import Blueprint, request, jsonify
import instaloader
import re

insta_bp = Blueprint('insta', __name__)
L = instaloader.Instaloader()

def download_instagram_media(url):
    media_urls = []
    try:
        # Extract shortcode from URL
        if 'instagram.com/p/' in url:
            match = re.search(r'/p/([^/?]+)', url)
        elif 'instagram.com/reel/' in url:
            match = re.search(r'/reel/([^/?]+)', url)
        elif 'instagram.com/stories/' in url:
            match = re.search(r'/stories/([^/?]+)', url)
        else:
            raise ValueError("Unsupported URL format.")

        if not match:
            raise ValueError("Failed to extract shortcode.")

        shortcode = match.group(1)
        print(f"Extracted Shortcode: {shortcode}")

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Collecting data
        data = {
            "caption": post.caption,
            "likes": post.likes,
            "media": []
        }

        # Handle carousel posts
        if post.is_video:  # If it's a video post
            data["media"].append({
                "media_url": post.url,
                "is_video": True,
                "video_url": post.video_url
            })
        else:
            # Check for carousel (multiple media)
            if post.get_sidecar_nodes():
                for item in post.get_sidecar_nodes():
                    media_data = {
                        "media_url": item.display_url,
                        "is_video": item.is_video
                    }
                    if item.is_video:
                        media_data["video_url"] = item.video_url
                    data["media"].append(media_data)
            else:
                # Single media post
                data["media"].append({
                    "media_url": post.url,
                    "is_video": post.is_video,
                    "video_url": post.video_url if post.is_video else None
                })

        return data
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise

@insta_bp.route('/insta', methods=['GET'])
def download_media():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided."}), 400

    try:
        data = download_instagram_media(url)
        if not data["media"]:
            return jsonify({"error": "No media found."}), 404

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
